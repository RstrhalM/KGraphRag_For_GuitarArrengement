#!/usr/bin/env python
"""Merge visual-caption canonical term batch outputs into one sidecar."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from query_normalizer import normalize_canonical_terms
DEFAULT_INPUT_CAPTIONS = (
    ROOT
    / "data"
    / "processed"
    / "fretboard_handbook"
    / "question_answer_visual_caption_layer"
    / "fretboard_answer_visual_caption_accepted_all.jsonl"
)
DEFAULT_BATCH_DIR = ROOT / "data" / "processed" / "fretboard_handbook" / "question_answer_visual_caption_canonical_batches"
DEFAULT_OUTPUT_DIR = ROOT / "data" / "processed" / "fretboard_handbook" / "question_answer_visual_caption_canonical"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(row, dict):
                rows.append(row)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def visual_id_from_caption(row: dict[str, Any]) -> str:
    metadata = row.get("metadata_flat") if isinstance(row.get("metadata_flat"), dict) else {}
    return str(row.get("visual_id") or row.get("segment_id") or metadata.get("visual_id") or "")


def clean_item(row: dict[str, Any]) -> dict[str, Any]:
    item = dict(row)
    for key in ["canonical_terms", "required_terms", "optional_terms", "negative_constraints"]:
        item[key] = normalize_canonical_terms(item.get(key) or [])
    # LLM outputs in detailed fields sometimes include canonical-looking values;
    # normalize them when possible, but keep raw aliases for audit.
    item["roots"] = normalize_canonical_terms(item.get("roots") or [])
    item["chord_qualities"] = normalize_canonical_terms(item.get("chord_qualities") or [])
    item["key_or_tonality"] = normalize_canonical_terms(item.get("key_or_tonality") or [])
    return item


def render_review(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Fretboard Visual Caption Canonical Terms",
        "",
        "合并自分批 LLM canonical_terms 抽取结果。当前状态为待审核 sidecar，不覆盖原始 caption。",
        "",
    ]
    for index, row in enumerate(rows, start=1):
        preview = row.get("source_preview") if isinstance(row.get("source_preview"), dict) else {}
        lines.extend(
            [
                f"## {index}. `{row.get('visual_id')}`",
                "",
                "- [ ] accept",
                "- [ ] revise",
                f"- status: `{row.get('status')}`",
                f"- visual_type: `{row.get('visual_type')}`",
                f"- confidence: `{row.get('confidence')}`",
                f"- canonical_terms: `{', '.join(str(x) for x in row.get('canonical_terms') or [])}`",
                f"- key_or_tonality: `{', '.join(str(x) for x in row.get('key_or_tonality') or [])}`",
                f"- chord_qualities: `{', '.join(str(x) for x in row.get('chord_qualities') or [])}`",
                f"- scale_or_mode: `{', '.join(str(x) for x in row.get('scale_or_mode') or [])}`",
                f"- constraints: `{', '.join(str(x) for x in row.get('fretboard_constraints') or [])}`",
                f"- batch_file: `{row.get('_batch_file', '')}`",
                "",
                "<details><summary>source caption</summary>",
                "",
                str(preview.get("caption") or ""),
                "",
                "</details>",
                "",
            ]
        )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-captions", type=Path, default=DEFAULT_INPUT_CAPTIONS)
    parser.add_argument("--batch-dir", type=Path, default=DEFAULT_BATCH_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_rows = read_jsonl(args.input_captions)
    source_order = {visual_id_from_caption(row): index for index, row in enumerate(source_rows)}
    batch_files = sorted(args.batch_dir.glob("*/canonical_terms_review.jsonl"))

    merged_by_id: dict[str, dict[str, Any]] = {}
    duplicate_ids: list[str] = []
    for path in batch_files:
        for row in read_jsonl(path):
            visual_id = str(row.get("visual_id") or "")
            if not visual_id:
                continue
            item = clean_item(row)
            item["_batch_file"] = str(path)
            if visual_id in merged_by_id:
                duplicate_ids.append(visual_id)
            merged_by_id[visual_id] = item

    missing_ids = [visual_id for visual_id in source_order if visual_id not in merged_by_id]
    merged = sorted(
        merged_by_id.values(),
        key=lambda row: source_order.get(str(row.get("visual_id") or ""), 10**9),
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_jsonl = args.output_dir / "fretboard_answer_visual_caption_canonical_terms.jsonl"
    output_md = args.output_dir / "fretboard_answer_visual_caption_canonical_terms_review.md"
    report_json = args.output_dir / "canonical_terms_merge_report.json"
    write_jsonl(output_jsonl, merged)
    output_md.write_text(render_review(merged), encoding="utf-8")
    report = {
        "input_captions": str(args.input_captions),
        "batch_dir": str(args.batch_dir),
        "batch_files": len(batch_files),
        "source_count": len(source_rows),
        "merged_count": len(merged),
        "unique_ids": len(merged_by_id),
        "duplicate_ids": sorted(set(duplicate_ids)),
        "duplicate_count": len(duplicate_ids),
        "missing_count": len(missing_ids),
        "missing_ids": missing_ids,
        "output_jsonl": str(output_jsonl),
        "output_md": str(output_md),
    }
    report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not missing_ids else 1


if __name__ == "__main__":
    raise SystemExit(main())
