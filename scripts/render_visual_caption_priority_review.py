"""Render a compact priority-review file for visual captions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def should_focus(row: dict[str, Any], threshold: float) -> bool:
    confidence = float(row.get("confidence") or 0)
    uncertain = row.get("uncertain_fields") or []
    return confidence < threshold or bool(uncertain)


def render(rows: list[dict[str, Any]], threshold: float) -> str:
    focus = [(idx, row) for idx, row in enumerate(rows, start=1) if should_focus(row, threshold)]
    lines = [
        "# Visual Caption Priority Review",
        "",
        f"- 总 caption：{len(rows)}",
        f"- 建议优先审核：{len(focus)}",
        f"- 入选条件：confidence < {threshold} 或 uncertain_fields 非空",
        "",
    ]
    for idx, row in focus:
        meta = row.get("source_metadata") or {}
        nearby_text = " ".join(str(meta.get("nearby_text") or "").split())[:500]
        lines.extend(
            [
                f"## {idx:02d}. {row.get('visual_id')}",
                "",
                f"- source/page: `{meta.get('source_id')}` / `{meta.get('page')}`",
                f"- image_type: `{row.get('image_type')}`",
                f"- topic: `{row.get('topic')}`",
                f"- confidence: `{row.get('confidence')}`",
                f"- uncertain: `{', '.join(row.get('uncertain_fields') or [])}`",
                f"- image_path: `{meta.get('image_path')}`",
                "",
                "**Caption**",
                "",
                f"> {row.get('caption')}",
                "",
                "**附近文字摘要**",
                "",
                f"> {nearby_text}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--threshold", type=float, default=0.93)
    args = parser.parse_args()

    rows = read_jsonl(args.results)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(rows, args.threshold), encoding="utf-8")
    focus_count = sum(1 for row in rows if should_focus(row, args.threshold))
    print(json.dumps({"rows": len(rows), "priority_items": focus_count, "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
