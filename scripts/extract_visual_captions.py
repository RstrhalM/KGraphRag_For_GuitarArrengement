#!/usr/bin/env python
"""Generate structured visual captions for guitar textbook images with a VLM."""

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


SYSTEM_PROMPT = """你是一位吉他教材视觉证据标注助手。

你会看到一张或多张教材图片，以及该图片附近的文字、页码、来源和主题提示。

目标：
把图片降维成可检索的结构化乐理 caption，用于后续文本 RAG。不要生成知识图谱边。

必须遵守：
1. 只描述图片和 nearby_text 明确支持的信息。
2. 不确定字段写 "unknown"，不要猜调性、品位、构成音、指型编号。
3. 区分练习说明、答案图、和弦图、指板图、谱例图、节奏图。
4. 如果图片是练习题或答案图，只提取可检索的结构信息，不要逐题罗列答案。
5. 如果 visual_role 是 answer_solution，答案图是主证据；正文练习文字只用于判断题目语境。不要把纯填空答案或逐题答案写入 caption。
6. caption 要适合文本检索，包含可检索关键词，如调弦、和弦、音阶、根音、指型、弦组、技法。
7. arrangement_value 面向吉他编配，说明这个图对 riff、solo、voicing、声部连接、风格色彩有什么用。
8. 如果无法看清或 nearby_text 不足，不要硬编，降低 confidence 并记录 uncertain_fields。

输出 JSON 对象，格式严格如下：
{
  "visual_id": "沿用输入 visual_id",
  "image_type": "chord_diagram | fretboard_diagram | tab_excerpt | rhythm_notation | exercise_diagram | answer_diagram | page_context | unknown",
  "topic": "简短主题，如 major_triad_arpeggio / FACGCE_chord_shapes / add9_voicings",
  "tuning": "standard | DADGAD | FACGCE | DAEAC#E | unknown",
  "key": "如 D major / F minor / unknown",
  "root": "如 D / F / unknown",
  "entities": {
    "chords": [],
    "scales": [],
    "intervals": [],
    "techniques": [],
    "fingerings": []
  },
  "visible_structure": {
    "string_set": "如 1-4 strings / 6 strings / unknown",
    "fret_range": "如 5-9 / unknown",
    "open_strings": [],
    "omitted_tones": [],
    "included_tones": []
  },
  "caption": "一段可检索的中文乐理描述，不超过120字",
  "arrangement_value": "对吉他编配/风格/可演奏性的价值，不超过120字",
  "confidence": 0.0,
  "uncertain_fields": []
}
"""


def image_to_data_url(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(path.name)
    mime_type = mime_type or "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


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


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


class VisionCaptionClient:
    def __init__(self) -> None:
        self.base_url = os.environ.get("LLM_API_BASE_URL", "").rstrip("/")
        self.api_key = os.environ.get("LLM_API_KEY", "")
        self.model = os.environ.get("LLM_MODEL", "")
        self.temperature = float(os.environ.get("LLM_TEMPERATURE", "0"))
        self.timeout = int(os.environ.get("LLM_TIMEOUT_SECONDS", "180"))
        self.max_retries = int(os.environ.get("LLM_MAX_RETRIES", "2"))
        self.max_output_tokens = int(os.environ.get("LLM_MAX_OUTPUT_TOKENS", "0") or 0)
        self.enable_thinking = os.environ.get("LLM_ENABLE_THINKING", "false").strip().lower() == "true"
        if not self.base_url or not self.model:
            raise ValueError("LLM_API_BASE_URL and LLM_MODEL must be set in .env")

    def caption(self, candidate: dict[str, Any]) -> dict[str, Any]:
        image_paths = candidate_image_paths(candidate)
        if not image_paths:
            raise FileNotFoundError(candidate.get("image_path") or candidate.get("image_paths"))
        payload = {
            "visual_id": candidate.get("visual_id"),
            "source_id": candidate.get("source_id"),
            "source_title": candidate.get("source_title"),
            "source_type": candidate.get("source_type"),
            "visual_role": candidate.get("visual_role"),
            "page": candidate.get("page"),
            "priority": candidate.get("priority"),
            "visual_granularity": candidate.get("visual_granularity"),
            "image_type_hint": candidate.get("image_type_hint"),
            "topic_hint": candidate.get("topic_hint"),
            "nearby_text": candidate.get("nearby_text"),
            "style_tags": candidate.get("style_tags"),
            "exercise_numbers": candidate.get("exercise_numbers"),
            "answer_metadata": candidate.get("answer_metadata"),
            "image_paths": [str(path) for path in image_paths],
            "instruction": "请结合图片和附近文字生成结构化视觉 caption。不要生成知识图谱边。",
        }
        content: list[dict[str, Any]] = [
            {"type": "text", "text": json.dumps(payload, ensure_ascii=False, indent=2)},
        ]
        for image_path in image_paths:
            content.append({"type": "image_url", "image_url": {"url": image_to_data_url(image_path)}})
        request_payload: dict[str, Any] = {
            "model": self.model,
            "temperature": self.temperature,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": content},
            ],
            "enable_thinking": self.enable_thinking,
        }
        if self.max_output_tokens > 0:
            request_payload["max_tokens"] = self.max_output_tokens

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
        raise RuntimeError(f"VLM caption request failed: {last_error}")


def normalize_caption(result: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    result = dict(result)
    result["visual_id"] = str(candidate.get("visual_id") or result.get("visual_id") or "")
    for key in ["entities", "visible_structure"]:
        if not isinstance(result.get(key), dict):
            result[key] = {}
    for key in ["image_type", "topic", "tuning", "key", "root", "caption", "arrangement_value"]:
        result[key] = str(result.get(key) or "unknown").strip()
    try:
        confidence = float(result.get("confidence", 0.0))
    except (TypeError, ValueError):
        confidence = 0.0
    result["confidence"] = max(0.0, min(1.0, confidence))
    if not isinstance(result.get("uncertain_fields"), list):
        result["uncertain_fields"] = []
    result["caption_text"] = build_caption_text(result, candidate)
    result["source_metadata"] = {
        "source_id": candidate.get("source_id"),
        "source_title": candidate.get("source_title"),
        "source_type": candidate.get("source_type"),
        "visual_role": candidate.get("visual_role"),
        "page": candidate.get("page"),
        "priority": candidate.get("priority"),
        "visual_granularity": candidate.get("visual_granularity"),
        "image_path": candidate.get("image_path"),
        "image_paths": candidate.get("image_paths"),
        "body_image_paths": candidate.get("body_image_paths"),
        "body_visual_ids": candidate.get("body_visual_ids"),
        "exercise_numbers": candidate.get("exercise_numbers"),
        "answer_metadata": candidate.get("answer_metadata"),
        "topic_hint": candidate.get("topic_hint"),
        "nearby_text": candidate.get("nearby_text"),
        "style_tags": candidate.get("style_tags"),
    }
    return result


def candidate_image_paths(candidate: dict[str, Any]) -> list[Path]:
    raw_paths = candidate.get("image_paths")
    values: list[Any]
    if isinstance(raw_paths, list) and raw_paths:
        values = raw_paths
    else:
        values = [candidate.get("image_path")]
    paths: list[Path] = []
    for value in values:
        if not value:
            continue
        path = Path(str(value))
        if not path.is_file():
            raise FileNotFoundError(path)
        paths.append(path)
    return paths


def list_text(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value if str(item).strip())
    if value is None:
        return ""
    return str(value)


def build_caption_text(result: dict[str, Any], candidate: dict[str, Any]) -> str:
    entities = result.get("entities") if isinstance(result.get("entities"), dict) else {}
    structure = result.get("visible_structure") if isinstance(result.get("visible_structure"), dict) else {}
    parts = [
        f"来源: {candidate.get('source_title')} / {candidate.get('source_id')}",
        f"视觉角色: {candidate.get('visual_role')}",
        f"练习编号: {list_text(candidate.get('exercise_numbers'))}",
        f"页码: {candidate.get('page')}",
        f"图像类型: {result.get('image_type')}",
        f"主题: {result.get('topic')}",
        f"调弦: {result.get('tuning')}",
        f"调性: {result.get('key')}",
        f"根音: {result.get('root')}",
        f"和弦: {list_text(entities.get('chords'))}",
        f"音阶: {list_text(entities.get('scales'))}",
        f"音程: {list_text(entities.get('intervals'))}",
        f"技法: {list_text(entities.get('techniques'))}",
        f"指型: {list_text(entities.get('fingerings'))}",
        f"弦组: {structure.get('string_set', '')}",
        f"品位范围: {structure.get('fret_range', '')}",
        f"开放弦: {list_text(structure.get('open_strings'))}",
        f"省略音: {list_text(structure.get('omitted_tones'))}",
        f"包含音: {list_text(structure.get('included_tones'))}",
        f"caption: {result.get('caption')}",
        f"编配价值: {result.get('arrangement_value')}",
        f"附近文字: {candidate.get('nearby_text')}",
    ]
    return "\n".join(part for part in parts if part and not part.endswith(": "))


def review_image_ref(value: Any, review_path: Path) -> str:
    if not value:
        return ""
    image_path = Path(str(value))
    if not image_path.is_absolute():
        image_path = Path.cwd() / image_path
    try:
        return os.path.relpath(image_path.resolve(), review_path.parent.resolve()).replace("\\", "/")
    except (OSError, ValueError):
        return str(value).replace("\\", "/")


def render_review_md(rows: list[dict[str, Any]], review_path: Path) -> str:
    lines = [
        "# Visual Caption Review",
        "",
        f"- 待审核 caption：{len(rows)}",
        "- 审核建议：重点看 VLM 是否瞎猜调性/品位/构成音；可接受轻微概括。",
        "",
    ]
    for idx, row in enumerate(rows, start=1):
        meta = row.get("source_metadata", {}) if isinstance(row.get("source_metadata"), dict) else {}
        image_ref = review_image_ref(meta.get("image_path"), review_path)
        lines.extend(
            [
                f"## {idx:02d}. {row.get('visual_id')}",
                "",
                f"<!-- visual_id: {row.get('visual_id')} -->",
                "",
                "**审核**",
                "",
                "- [ ] accept",
                "- [ ] revise",
                "- [ ] reject",
                "",
                "**修改建议/驳回原因**",
                "",
                "<!-- review_reason_start -->",
                "",
                "<!-- review_reason_end -->",
                "",
                "| 字段 | 内容 |",
                "| --- | --- |",
                f"| source | `{meta.get('source_id')}` page `{meta.get('page')}` |",
                f"| image_type | `{row.get('image_type')}` |",
                f"| topic | `{row.get('topic')}` |",
                f"| tuning/key/root | `{row.get('tuning')}` / `{row.get('key')}` / `{row.get('root')}` |",
                f"| confidence | `{row.get('confidence')}` |",
                f"| uncertain | `{', '.join(map(str, row.get('uncertain_fields') or []))}` |",
                f"| image_path | `{meta.get('image_path')}` |",
                f"| image_paths | `{', '.join(map(str, meta.get('image_paths') or []))}` |",
                f"| visual_role | `{meta.get('visual_role')}` |",
                f"| exercise_numbers | `{', '.join(map(str, meta.get('exercise_numbers') or []))}` |",
                "",
                "**图片对照**",
                "",
                f"![]({image_ref})" if image_ref else "> 无可用图片路径",
                "",
                "**Caption**",
                "",
                f"> {row.get('caption')}",
                "",
                "**编配价值**",
                "",
                f"> {row.get('arrangement_value')}",
                "",
                "**Embedding Text**",
                "",
                "```text",
                str(row.get("caption_text") or "")[:1600],
                "```",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("-o", "--output-dir", type=Path, required=True)
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    parser.add_argument("--offset", type=int, default=0, help="Skip this many candidates before applying --limit.")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--resume", action="store_true", help="Reuse existing results/errors and skip processed visual_id values.")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    apply_env_file(args.env_file)
    candidates = read_jsonl(args.candidates)
    if args.offset > 0:
        candidates = candidates[args.offset :]
    if args.limit > 0:
        candidates = candidates[: args.limit]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.dry_run:
        report = {"candidates": len(candidates), "dry_run": True}
        (args.output_dir / "visual_caption_report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    result_path = args.output_dir / "visual_caption_results.jsonl"
    error_path = args.output_dir / "visual_caption_errors.jsonl"
    review_path = args.output_dir / "visual_caption_review.md"
    report_path = args.output_dir / "visual_caption_report.json"

    client = VisionCaptionClient()
    rows: list[dict[str, Any]] = read_jsonl(result_path) if args.resume and result_path.exists() else []
    errors: list[dict[str, Any]] = read_jsonl(error_path) if args.resume and error_path.exists() else []
    processed = {str(row.get("visual_id") or "") for row in rows + errors}
    if not args.resume:
        write_jsonl(result_path, [])
        write_jsonl(error_path, [])
    for index, candidate in enumerate(candidates, start=1):
        visual_id = str(candidate.get("visual_id") or "")
        if visual_id in processed:
            print(f"[{index}/{len(candidates)}] skip {visual_id}", flush=True)
            continue
        print(f"[{index}/{len(candidates)}] {candidate.get('visual_id')}", flush=True)
        try:
            result = client.caption(candidate)
            row = normalize_caption(result, candidate)
            rows.append(row)
            append_jsonl(result_path, row)
            review_path.write_text(render_review_md(rows, review_path), encoding="utf-8")
        except Exception as exc:
            error_row = {"visual_id": str(candidate.get("visual_id")), "error": str(exc)}
            errors.append(error_row)
            append_jsonl(error_path, error_row)
            print(f"  error: {exc}", flush=True)
        report = {
            "candidates": len(candidates),
            "captions": len(rows),
            "errors": len(errors),
            "error_samples": errors[:5],
            "model": os.environ.get("LLM_MODEL", ""),
        }
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    write_jsonl(result_path, rows)
    write_jsonl(error_path, errors)
    review_path.write_text(render_review_md(rows, review_path), encoding="utf-8")
    report = {
        "candidates": len(candidates),
        "captions": len(rows),
        "errors": len(errors),
        "error_samples": errors[:5],
        "model": os.environ.get("LLM_MODEL", ""),
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
