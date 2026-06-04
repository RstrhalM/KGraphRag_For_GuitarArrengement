#!/usr/bin/env python
"""Extract fine-grained visual-caption items from answer-aware candidates."""

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


SYSTEM_PROMPT = """你是一位吉他教材视觉证据拆解助手。

你会看到一张练习答案图，以及与之对应的练习题干。答案图可能同时包含多个练习和很多指板小图。

目标：
把答案图中与指定 exercise_numbers 相关的内容拆成多个可检索的 visual_caption_items，用于文本 RAG。

必须遵守：
1. 不要输出“一张图整体 caption”。必须按练习编号、题号、指型、调性/音阶/音程关系拆成多个 item。
2. 不要逐题保存“答案是什么”的流水账；只保留可复用的指板规律、音阶/音程/指型映射、把位选择、编配价值。
3. 只处理输入 exercise_numbers 指定的练习；答案图里其他练习可忽略。
4. 不确定字段写 "unknown"，不要猜具体品位、调性、指型编号。
5. 每个 item 的 caption 应可被用户自然语言召回，例如“根音型式怎么换把位”“大调五声音阶和关系小调五声音阶怎么对应”。
6. 如果某个练习只是纯填空、背诵、没有可复用视觉规律，可以不生成 item，并在 discarded_items 说明。

输出 JSON 对象，格式严格如下：
{
  "parent_visual_id": "沿用输入 visual_id",
  "items": [
    {
      "item_id": "稳定短 id，如 exercise_4_root_form_overlap",
      "exercise_no": 4,
      "image_type": "answer_diagram | fretboard_diagram | exercise_diagram | unknown",
      "topic": "简短主题，如 root_fingering_forms / major_pentatonic_relative_minor",
      "tuning": "standard | unknown",
      "key": "如 A major / unknown",
      "root": "如 A / unknown",
      "entities": {
        "chords": [],
        "scales": [],
        "intervals": [],
        "techniques": [],
        "fingerings": []
      },
      "visible_structure": {
        "string_set": "如 6 strings / unknown",
        "fret_range": "如 5-9 / unknown",
        "open_strings": [],
        "omitted_tones": [],
        "included_tones": []
      },
      "caption": "一段可检索的中文乐理描述，不超过120字",
      "arrangement_value": "对吉他编配/把位选择/riff/solo/voicing 的价值，不超过120字",
      "confidence": 0.0,
      "uncertain_fields": []
    }
  ],
  "discarded_items": [
    {
      "exercise_no": 4,
      "reason": "为什么没有生成 item"
    }
  ]
}
"""


def image_to_data_url(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(path.name)
    mime_type = mime_type or "image/png"
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


class AnswerVisualItemClient:
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

    def extract_items(self, candidate: dict[str, Any]) -> dict[str, Any]:
        image_path = Path(str(candidate.get("image_path") or ""))
        if not image_path.is_file():
            raise FileNotFoundError(image_path)
        payload = {
            "visual_id": candidate.get("visual_id"),
            "source_id": candidate.get("source_id"),
            "source_title": candidate.get("source_title"),
            "visual_role": candidate.get("visual_role"),
            "exercise_numbers": candidate.get("exercise_numbers"),
            "topic_hint": candidate.get("topic_hint"),
            "nearby_text": candidate.get("nearby_text"),
            "answer_metadata": candidate.get("answer_metadata"),
            "instruction": "只围绕 exercise_numbers 指定练习拆成多个细粒度 visual_caption_items。",
        }
        content: list[dict[str, Any]] = [
            {"type": "text", "text": json.dumps(payload, ensure_ascii=False, indent=2)},
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
        raise RuntimeError(f"Answer visual item request failed: {last_error}")


def normalize_items(result: dict[str, Any], candidate: dict[str, Any]) -> list[dict[str, Any]]:
    parent_visual_id = str(result.get("parent_visual_id") or candidate.get("visual_id") or "")
    raw_items = result.get("items")
    if not isinstance(raw_items, list):
        raw_items = []
    rows: list[dict[str, Any]] = []
    for index, item in enumerate(raw_items, start=1):
        if not isinstance(item, dict):
            continue
        item_id = str(item.get("item_id") or f"{parent_visual_id}:item_{index:02d}")
        row = dict(item)
        row["parent_visual_id"] = parent_visual_id
        row["visual_id"] = f"{parent_visual_id}:{item_id}"
        row["item_index"] = index
        row["source_metadata"] = {
            "source_id": candidate.get("source_id"),
            "source_title": candidate.get("source_title"),
            "source_type": candidate.get("source_type"),
            "visual_role": candidate.get("visual_role"),
            "exercise_numbers": candidate.get("exercise_numbers"),
            "answer_image": candidate.get("image_path"),
            "answer_metadata": candidate.get("answer_metadata"),
            "body_visual_ids": candidate.get("body_visual_ids"),
            "body_image_paths": candidate.get("body_image_paths"),
            "nearby_text": candidate.get("nearby_text"),
            "topic_hint": candidate.get("topic_hint"),
            "style_tags": candidate.get("style_tags"),
        }
        row["caption_text"] = build_caption_text(row)
        rows.append(row)
    return rows


def list_text(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value if str(item).strip())
    if value is None:
        return ""
    return str(value)


def build_caption_text(row: dict[str, Any]) -> str:
    meta = row.get("source_metadata") if isinstance(row.get("source_metadata"), dict) else {}
    entities = row.get("entities") if isinstance(row.get("entities"), dict) else {}
    structure = row.get("visible_structure") if isinstance(row.get("visible_structure"), dict) else {}
    parts = [
        f"来源: {meta.get('source_title')} / {meta.get('source_id')}",
        f"视觉角色: {meta.get('visual_role')}",
        f"父图: {row.get('parent_visual_id')}",
        f"练习编号: {row.get('exercise_no')}",
        f"图像类型: {row.get('image_type')}",
        f"主题: {row.get('topic')}",
        f"调弦: {row.get('tuning')}",
        f"调性: {row.get('key')}",
        f"根音: {row.get('root')}",
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
        f"caption: {row.get('caption')}",
        f"编配价值: {row.get('arrangement_value')}",
    ]
    return "\n".join(part for part in parts if part and not part.endswith(": "))


def render_review_md(rows: list[dict[str, Any]], discarded: list[dict[str, Any]]) -> str:
    lines = [
        "# Answer Visual Caption Item Review",
        "",
        f"- 待审核 item：{len(rows)}",
        f"- discarded_items：{len(discarded)}",
        "- 审核重点：是否拆得足够细；是否只是保存答案；是否有可复用指板/编配价值。",
        "",
    ]
    for idx, row in enumerate(rows, start=1):
        meta = row.get("source_metadata") if isinstance(row.get("source_metadata"), dict) else {}
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
                f"| parent | `{row.get('parent_visual_id')}` |",
                f"| answer_image | `{meta.get('answer_image')}` |",
                f"| exercise_no | `{row.get('exercise_no')}` |",
                f"| image_type | `{row.get('image_type')}` |",
                f"| topic | `{row.get('topic')}` |",
                f"| tuning/key/root | `{row.get('tuning')}` / `{row.get('key')}` / `{row.get('root')}` |",
                f"| confidence | `{row.get('confidence')}` |",
                f"| uncertain | `{', '.join(map(str, row.get('uncertain_fields') or []))}` |",
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
    if discarded:
        lines.extend(["## Discarded", ""])
        for item in discarded:
            lines.append(f"- exercise `{item.get('exercise_no')}`: {item.get('reason')}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("-o", "--output-dir", type=Path, required=True)
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--limit", type=int, default=1)
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
        (args.output_dir / "answer_visual_caption_item_report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    client = AnswerVisualItemClient()
    rows: list[dict[str, Any]] = []
    discarded: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for index, candidate in enumerate(candidates, start=1):
        print(f"[{index}/{len(candidates)}] {candidate.get('visual_id')}", flush=True)
        try:
            result = client.extract_items(candidate)
            rows.extend(normalize_items(result, candidate))
            raw_discarded = result.get("discarded_items")
            if isinstance(raw_discarded, list):
                discarded.extend(item for item in raw_discarded if isinstance(item, dict))
        except Exception as exc:
            errors.append({"visual_id": candidate.get("visual_id"), "error": str(exc)})
            print(f"  error: {exc}", flush=True)

    write_jsonl(args.output_dir / "answer_visual_caption_items.jsonl", rows)
    (args.output_dir / "answer_visual_caption_item_review.md").write_text(
        render_review_md(rows, discarded),
        encoding="utf-8",
    )
    report = {
        "candidates": len(candidates),
        "items": len(rows),
        "discarded_items": len(discarded),
        "errors": errors,
        "model": os.environ.get("LLM_MODEL", ""),
    }
    (args.output_dir / "answer_visual_caption_item_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
