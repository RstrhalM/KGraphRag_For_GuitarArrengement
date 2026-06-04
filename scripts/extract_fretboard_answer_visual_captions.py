#!/usr/bin/env python
"""Generate structured VLM captions for reviewed fretboard exercise-answer crops."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from extract_arrangement_kg import apply_env_file, extract_json_object


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = (
    ROOT
    / "data"
    / "processed"
    / "fretboard_handbook"
    / "question_answer_segment_manifest"
    / "fretboard_question_answer_segment_manifest.jsonl"
)
DEFAULT_OUTPUT_DIR = (
    ROOT
    / "data"
    / "processed"
    / "fretboard_handbook"
    / "question_answer_visual_caption_trial"
)
DEFAULT_TEST_SEGMENTS = [
    "fretboard_answer_E52_all",
    "fretboard_answer_E54_all",
    "fretboard_answer_E49_1",
    "fretboard_answer_E50_5",
    "fretboard_answer_E53_1",
    "fretboard_answer_E56_3",
    "fretboard_answer_E58_8",
    "fretboard_answer_E59_11",
]

SYSTEM_PROMPT = """你是一位吉他教材答案图 visual caption 标注助手。

你会看到一张已经人工审核过的题目级教材图片 crop，以及该 crop 对应的练习号、小题号和题目上下文。

目标：
把图片降维为“后续文本检索可用”的结构化乐理 caption。输出只用于 RAG 检索与视觉证据回链，不生成知识图谱边。

严格规则：
1. 只根据图片中可见信息和输入上下文作答；不要脑补未显示的弦号、指法、音名或功能。
2. 图片文字优先级高于上下文；上下文只用于理解题目语境。
   如果图片中可见的音名/和弦名/调式名与上下文示例冲突，必须以图片为准，并在 uncertain_fields 中加入 "context_conflict"。
3. 如果 evidence_type 是 text_answer_ocr，请识别图片中的答案文字，保留题号到答案的对应。
4. 如果 evidence_type 是 fretboard_diagram，请识别图中可见的和弦名/音阶名/调式名/指型编号/把位罗马数字/声部构成/可见按点。
5. 不确定字段写空字符串或空数组，并把字段名放进 uncertain_fields。
6. caption 必须适合文本检索，包含中文术语和图中可见英文/符号，例如 Bbmi6/9、Cma7/D = D13、E 和声小调。
7. 可以根据图中罗马把位、弦线和按点推断位置；但如果图片没有明确显示调弦方向、弦号或起始品，请在 visible_dots_summary 中使用“约为/推断为”，并把 fret_range 或 string_position 加入 uncertain_fields。
8. 对单弦音阶图，如果图片中有首尾圈出的音名，musical_object 应按图片可见的首尾音名确定，例如 G-A-B-C-D-E-F#-G 应标为 G major / G Ionian，而不是采用上下文中的示例调名。
9. 不要输出解释文字，只输出 JSON 对象。

输出 JSON 对象，字段严格如下：
{
  "segment_id": "沿用输入 segment_id",
  "visual_type": "text_answer | chord_diagram | scale_pattern | mode_fretboard_map | arpeggio_pattern | unknown",
  "musical_object": "图中主要对象，如 C9 / E 和声小调 指型3 / G Mixolydian 指型4",
  "root": "如 C / E / unknown",
  "quality_or_mode": "如 dominant ninth / harmonic minor / Mixolydian / unknown",
  "position_or_shape": "把位、罗马数字、指型编号等可见信息",
  "intervals": [],
  "answer_items": [{"number": "1", "answer": "Eb"}],
  "visible_fretboard": {
    "orientation": "vertical | horizontal | text_only | unknown",
    "roman_position": "",
    "fret_range": "",
    "visible_labels": [],
    "visible_dots_summary": ""
  },
  "caption": "不超过160字的可检索中文描述",
  "retrieval_keywords": [],
  "arrangement_value": "不超过120字，说明对编配/指板理解/voicing/solo 的用途",
  "confidence": 0.0,
  "uncertain_fields": []
}
"""


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON in {path} line {line_no}: {exc}") from exc
            if isinstance(row, dict):
                rows.append(row)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def image_to_data_url(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(path.name)
    mime_type = mime_type or "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def load_candidates(
    manifest: Path,
    segment_ids: list[str],
    use_all: bool,
    offset: int,
    limit: int,
) -> list[dict[str, Any]]:
    rows = read_jsonl(manifest)
    by_id = {str(row.get("segment_id")): row for row in rows}
    if use_all:
        selected = rows
    else:
        selected = []
        wanted = segment_ids or DEFAULT_TEST_SEGMENTS
        for segment_id in wanted:
            row = by_id.get(segment_id)
            if not row:
                raise KeyError(f"segment_id not found: {segment_id}")
            selected.append(row)
    if offset > 0:
        selected = selected[offset:]
    if limit > 0:
        selected = selected[:limit]
    return selected


class Client:
    def __init__(self) -> None:
        self.base_url = os.environ.get("LLM_API_BASE_URL", "").rstrip("/")
        self.api_key = os.environ.get("LLM_API_KEY", "")
        self.model = os.environ.get("LLM_MODEL", "")
        self.temperature = float(os.environ.get("LLM_TEMPERATURE", "0"))
        self.timeout = int(os.environ.get("LLM_TIMEOUT_SECONDS", "180"))
        self.max_retries = int(os.environ.get("LLM_MAX_RETRIES", "2"))
        self.max_output_tokens = int(os.environ.get("LLM_MAX_OUTPUT_TOKENS", "4096") or 4096)
        self.enable_thinking = os.environ.get("LLM_ENABLE_THINKING", "false").strip().lower() == "true"
        if not self.base_url or not self.model:
            raise ValueError("LLM_API_BASE_URL and LLM_MODEL must be set in .env")

    def caption(self, candidate: dict[str, Any]) -> dict[str, Any]:
        image_path = ROOT / str(candidate["crop_path"])
        if not image_path.exists():
            raise FileNotFoundError(image_path)
        input_payload = {
            "segment_id": candidate["segment_id"],
            "source": candidate["source"],
            "exercise_number": candidate["exercise_number"],
            "subquestion_number": candidate["subquestion_number"],
            "evidence_type": candidate["evidence_type"],
            "mapping_method": candidate["mapping_method"],
            "subquestion_prompt": candidate["subquestion_prompt"],
            "question_text": candidate["question_text"],
            "crop_path": candidate["crop_path"],
            "source_image": candidate["source_image"],
            "bbox": candidate["bbox"],
            "instruction": "请为这张题目级答案 crop 生成结构化 visual caption。",
        }
        content: list[dict[str, Any]] = [
            {"type": "text", "text": json.dumps(input_payload, ensure_ascii=False, indent=2)},
            {"type": "image_url", "image_url": {"url": image_to_data_url(image_path)}},
        ]
        request_payload: dict[str, Any] = {
            "model": self.model,
            "temperature": self.temperature,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": content},
            ],
            "enable_thinking": self.enable_thinking,
            "max_tokens": self.max_output_tokens,
        }
        body = json.dumps(request_payload, ensure_ascii=False).encode("utf-8")
        headers = {"Content-Type": "application/json; charset=utf-8"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                req = urllib.request.Request(
                    f"{self.base_url}/chat/completions",
                    data=body,
                    headers=headers,
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                return extract_json_object(data["choices"][0]["message"]["content"])
            except (
                TimeoutError,
                urllib.error.URLError,
                urllib.error.HTTPError,
                KeyError,
                json.JSONDecodeError,
                ValueError,
            ) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(1.5 * (attempt + 1))
        raise RuntimeError(f"caption request failed: {last_error}")


def normalize(result: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    row = dict(result)
    row["segment_id"] = candidate["segment_id"]
    row.setdefault("visual_type", "unknown")
    row.setdefault("musical_object", "")
    row.setdefault("root", "")
    row.setdefault("quality_or_mode", "")
    row.setdefault("position_or_shape", "")
    row.setdefault("intervals", [])
    row.setdefault("answer_items", [])
    row.setdefault("visible_fretboard", {})
    row.setdefault("caption", "")
    row.setdefault("retrieval_keywords", [])
    row.setdefault("arrangement_value", "")
    row.setdefault("uncertain_fields", [])
    try:
        row["confidence"] = max(0.0, min(1.0, float(row.get("confidence", 0.0))))
    except (TypeError, ValueError):
        row["confidence"] = 0.0
    row["source_metadata"] = {
        "source": candidate["source"],
        "exercise_number": candidate["exercise_number"],
        "subquestion_number": candidate["subquestion_number"],
        "evidence_type": candidate["evidence_type"],
        "mapping_method": candidate["mapping_method"],
        "crop_path": candidate["crop_path"],
        "source_image": candidate["source_image"],
        "bbox": candidate["bbox"],
        "subquestion_prompt": candidate["subquestion_prompt"],
        "question_text": candidate["question_text"],
    }
    row["caption_text"] = caption_text(row)
    return row


def list_text(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value if str(item).strip())
    if value is None:
        return ""
    return str(value)


def caption_text(row: dict[str, Any]) -> str:
    meta = row.get("source_metadata", {}) if isinstance(row.get("source_metadata"), dict) else {}
    vf = row.get("visible_fretboard", {}) if isinstance(row.get("visible_fretboard"), dict) else {}
    answer_items = row.get("answer_items")
    if isinstance(answer_items, list) and answer_items:
        answers = "; ".join(f"{item.get('number')}: {item.get('answer')}" for item in answer_items if isinstance(item, dict))
    else:
        answers = ""
    parts = [
        f"来源: {meta.get('source')}",
        f"练习: {meta.get('exercise_number')} 小题: {meta.get('subquestion_number')}",
        f"证据类型: {meta.get('evidence_type')}",
        f"视觉类型: {row.get('visual_type')}",
        f"对象: {row.get('musical_object')}",
        f"根音: {row.get('root')}",
        f"性质/调式: {row.get('quality_or_mode')}",
        f"位置/指型: {row.get('position_or_shape')}",
        f"音程: {list_text(row.get('intervals'))}",
        f"答案项: {answers}",
        f"方向: {vf.get('orientation', '')}",
        f"把位: {vf.get('roman_position', '')}",
        f"品位范围: {vf.get('fret_range', '')}",
        f"可见标签: {list_text(vf.get('visible_labels'))}",
        f"按点概述: {vf.get('visible_dots_summary', '')}",
        f"caption: {row.get('caption')}",
        f"检索关键词: {list_text(row.get('retrieval_keywords'))}",
        f"编配价值: {row.get('arrangement_value')}",
        f"题目上下文: {meta.get('subquestion_prompt')}",
    ]
    return "\n".join(part for part in parts if part and not part.endswith(": "))


def review_image_ref(raw_path: str, output_dir: Path) -> str:
    path = ROOT / raw_path
    return os.path.relpath(path.resolve(), output_dir.resolve()).replace("\\", "/")


def render_review(rows: list[dict[str, Any]], output_dir: Path) -> str:
    lines = [
        "# 指板手册题目级答案图 Caption 测试审核",
        "",
        f"- caption_count: {len(rows)}",
        "- 审核重点：和弦名/调式名/指型/答案文字是否准确；不要接受明显脑补的弦号、音名或指法。",
        "",
    ]
    for index, row in enumerate(rows, start=1):
        meta = row["source_metadata"]
        image = review_image_ref(str(meta["crop_path"]), output_dir)
        lines.extend(
            [
                f"## {index:02d}. {row['segment_id']}",
                "",
                f"<!-- segment_id: {row['segment_id']} -->",
                "",
                "- [ ] accept",
                "- [ ] revise",
                "- [ ] reject",
                "",
                "### 图片",
                "",
                f"![]({image})",
                "",
                "### 字段",
                "",
                "| 字段 | 内容 |",
                "| --- | --- |",
                f"| exercise/subquestion | `{meta.get('exercise_number')}` / `{meta.get('subquestion_number')}` |",
                f"| evidence_type | `{meta.get('evidence_type')}` |",
                f"| visual_type | `{row.get('visual_type')}` |",
                f"| musical_object | `{row.get('musical_object')}` |",
                f"| root | `{row.get('root')}` |",
                f"| quality_or_mode | `{row.get('quality_or_mode')}` |",
                f"| position_or_shape | `{row.get('position_or_shape')}` |",
                f"| intervals | `{list_text(row.get('intervals'))}` |",
                f"| keywords | `{list_text(row.get('retrieval_keywords'))}` |",
                f"| confidence | `{row.get('confidence')}` |",
                f"| uncertain | `{list_text(row.get('uncertain_fields'))}` |",
                "",
                "### Caption",
                "",
                f"> {row.get('caption')}",
                "",
                "### 编配价值",
                "",
                f"> {row.get('arrangement_value')}",
                "",
                "### Answer Items",
                "",
                "```json",
                json.dumps(row.get("answer_items") or [], ensure_ascii=False, indent=2),
                "```",
                "",
                "### Embedding Text",
                "",
                "```text",
                str(row.get("caption_text") or ""),
                "```",
                "",
            ]
        )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("-o", "--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    parser.add_argument("--segment-id", action="append", default=[])
    parser.add_argument("--all", action="store_true", help="Use all manifest rows instead of the default small trial set.")
    parser.add_argument("--offset", type=int, default=0, help="Skip this many selected candidates before --limit.")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--resume", action="store_true", help="Reuse existing output-dir results/errors and skip processed segment_id values.")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    apply_env_file(args.env_file)
    candidates = load_candidates(args.manifest, args.segment_id, args.all, args.offset, args.limit)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    candidates_path = args.output_dir / "caption_candidates.jsonl"
    result_path = args.output_dir / "caption_results.jsonl"
    error_path = args.output_dir / "caption_errors.jsonl"
    review_path = args.output_dir / "visual_caption_review.md"
    report_path = args.output_dir / "caption_report.json"
    write_jsonl(candidates_path, candidates)
    if args.dry_run:
        report = {
            "dry_run": True,
            "all": args.all,
            "offset": args.offset,
            "limit": args.limit,
            "candidates": len(candidates),
            "candidate_ids": [row["segment_id"] for row in candidates],
        }
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    client = Client()
    results: list[dict[str, Any]] = read_jsonl(result_path) if args.resume and result_path.exists() else []
    errors: list[dict[str, Any]] = read_jsonl(error_path) if args.resume and error_path.exists() else []
    processed = {str(row.get("segment_id") or "") for row in [*results, *errors]}
    if not args.resume:
        write_jsonl(result_path, [])
        write_jsonl(error_path, [])
    skipped = 0
    for index, candidate in enumerate(candidates, start=1):
        if str(candidate.get("segment_id") or "") in processed:
            skipped += 1
            print(f"[{index}/{len(candidates)}] skip {candidate['segment_id']}", flush=True)
            continue
        print(f"[{index}/{len(candidates)}] {candidate['segment_id']}", flush=True)
        try:
            result = client.caption(candidate)
            results.append(normalize(result, candidate))
            write_jsonl(result_path, results)
            review_path.write_text(render_review(results, args.output_dir), encoding="utf-8")
        except Exception as exc:
            error = {"segment_id": candidate.get("segment_id"), "error": str(exc)}
            errors.append(error)
            write_jsonl(error_path, errors)
            print(f"  error: {exc}", flush=True)
    report = {
        "candidates": len(candidates),
        "captions": len(results),
        "errors": len(errors),
        "skipped": skipped,
        "all": args.all,
        "offset": args.offset,
        "limit": args.limit,
        "resume": args.resume,
        "error_samples": errors[:5],
        "model": os.environ.get("LLM_MODEL", ""),
        "candidates_path": rel(candidates_path),
        "result_path": rel(result_path),
        "review_path": rel(review_path),
    }
    write_jsonl(result_path, results)
    write_jsonl(error_path, errors)
    review_path.write_text(render_review(results, args.output_dir), encoding="utf-8")
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
