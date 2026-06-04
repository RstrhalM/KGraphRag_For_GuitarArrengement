#!/usr/bin/env python
"""Render KG review JSONL into a human-friendly Markdown file."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


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
                raise ValueError(f"Invalid JSON on line {line_no}: {exc}") from exc
            if isinstance(row, dict):
                rows.append(row)
    return rows


def md_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def checkbox(status: str, expected: str) -> str:
    return "x" if status == expected else " "


def render_review_item(item: dict[str, Any]) -> str:
    status = str(item.get("review_status", "pending"))
    decision = str(item.get("decision", ""))
    reject_reason = str(item.get("reject_reason", ""))
    image_refs = item.get("candidate_image_refs", [])
    if not isinstance(image_refs, list):
        image_refs = []

    lines = [
        f"### {md_escape(item.get('review_id'))}",
        "",
        f"<!-- review_id: {item.get('review_id')} -->",
        "",
        "**审核**",
        "",
        f"- [{checkbox(decision, 'accept')}] accept",
        f"- [{checkbox(decision, 'revise')}] revise",
        f"- [{checkbox(decision, 'reject')}] reject",
        "",
        "**修改建议/驳回原因**",
        "",
        "<!-- review_reason_start -->",
        reject_reason,
        "<!-- review_reason_end -->",
        "",
        "| 字段 | 内容 |",
        "| --- | --- |",
        f"| 状态 | `{md_escape(status)}` |",
        f"| 类型 | `{md_escape(item.get('knowledge_type'))}` |",
        f"| 置信度 | `{md_escape(item.get('confidence'))}` |",
        f"| 边 | `{md_escape(item.get('source'))}` -> `{md_escape(item.get('relation'))}` -> `{md_escape(item.get('target'))}` |",
        f"| 语境 | {md_escape(item.get('context_condition'))} |",
        f"| 说明 | {md_escape(item.get('review_note'))} |",
        f"| 证据 | {md_escape(item.get('evidence'))} |",
        f"| 需看图 | `{md_escape(item.get('needs_visual_context'))}` |",
    ]
    if item.get("gp5_feature_triggers"):
        lines.append(f"| GP5触发特征 | {md_escape(', '.join(map(str, item.get('gp5_feature_triggers', []))))} |")
    if item.get("style_tags"):
        lines.append(f"| 风格标签 | {md_escape(', '.join(map(str, item.get('style_tags', []))))} |")

    lines.extend(
        [
            "",
            "**证据上下文**",
            "",
            "> " + str(item.get("evidence_context", "")).replace("\n", "\n> "),
            "",
        ]
    )

    if image_refs:
        lines.append("**候选图片**")
        lines.append("")
        for image_ref in image_refs:
            lines.append(f"- `{md_escape(image_ref)}`")
        lines.append("")

    return "\n".join(lines)


def render_markdown(rows: list[dict[str, Any]], title: str) -> str:
    by_chunk: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_chunk[str(row.get("chunk_id", "unknown"))].append(row)

    lines = [
        f"# {title}",
        "",
        f"- 待审核边数：{len(rows)}",
        f"- 分块数：{len(by_chunk)}",
        "",
        "审核建议：在 Markdown 中勾选 `accept` / `revise` / `reject`，修改建议写在预留区域，再用同步脚本写回 JSONL。",
        "",
    ]

    for chunk_id in sorted(by_chunk):
        chunk_rows = by_chunk[chunk_id]
        lines.extend([f"## {chunk_id}", "", f"- 本块待审核：{len(chunk_rows)}", ""])
        for item in chunk_rows:
            lines.append(render_review_item(item))

    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="arrangement_kg_review.jsonl")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output Markdown path")
    parser.add_argument("--title", default="KG Review", help="Markdown title")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = read_jsonl(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_markdown(rows, args.title), encoding="utf-8", newline="\n")
    print(f"Wrote {len(rows)} review items to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
