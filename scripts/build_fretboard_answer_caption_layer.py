#!/usr/bin/env python
"""Merge accepted fretboard answer visual captions into a formal layer."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BATCHES = ROOT / "data" / "processed" / "fretboard_handbook" / "question_answer_visual_caption_batches"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "fretboard_handbook" / "question_answer_visual_caption_layer"


BATCH_RE = re.compile(r"batch_(\d+)_(\d+)$")


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


def batch_key(path: Path) -> tuple[int, int, str]:
    match = BATCH_RE.match(path.name)
    if not match:
        return (10**9, 10**9, path.name)
    return (int(match.group(1)), int(match.group(2)), path.name)


def metadata_value(value: Any) -> str | int | float | bool:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return value
    return json.dumps(value, ensure_ascii=False)


def normalize_row(row: dict[str, Any], batch_name: str, batch_index: int) -> dict[str, Any]:
    segment_id = str(row.get("segment_id") or "").strip()
    if not segment_id:
        raise ValueError(f"Missing segment_id in {batch_name} item {batch_index}")

    meta = row.get("source_metadata") if isinstance(row.get("source_metadata"), dict) else {}
    crop_path = str(meta.get("crop_path") or "")
    exercise = meta.get("exercise_number", "")
    subquestion = meta.get("subquestion_number", "")
    question_text = str(meta.get("question_text") or meta.get("subquestion_prompt") or "")
    visual_type = str(row.get("visual_type") or row.get("image_type") or "")
    musical_object = str(row.get("musical_object") or row.get("topic") or "")

    enriched_meta = dict(meta)
    enriched_meta.update(
        {
            "visual_id": segment_id,
            "source_id": "fretboard_handbook_question_answer",
            "source_title": "吉他指板手册：题目级练习答案图",
            "source": meta.get("source") or "吉他指板手册",
            "page": str(meta.get("source_image") or ""),
            "priority": "fretboard_foundation_answer",
            "visual_granularity": "question_answer_crop",
            "image_path": crop_path,
            "topic_hint": musical_object or question_text,
            "nearby_text": question_text,
            "style_tags": ["guitar", "fretboard", "foundation", "exercise_answer"],
            "batch": batch_name,
            "batch_index": batch_index,
        }
    )

    normalized = dict(row)
    normalized["visual_id"] = segment_id
    normalized["image_type"] = visual_type
    normalized["topic"] = musical_object
    normalized["source_metadata"] = enriched_meta
    normalized["caption_layer"] = "fretboard_answer_caption_v1"
    normalized["accepted"] = True
    normalized["status"] = "accepted"
    normalized["metadata_flat"] = {
        key: metadata_value(value)
        for key, value in {
            "visual_id": segment_id,
            "source_id": enriched_meta["source_id"],
            "source_title": enriched_meta["source_title"],
            "exercise_number": exercise,
            "subquestion_number": subquestion,
            "evidence_type": meta.get("evidence_type", ""),
            "visual_type": visual_type,
            "musical_object": musical_object,
            "root": row.get("root", ""),
            "quality_or_mode": row.get("quality_or_mode", ""),
            "position_or_shape": row.get("position_or_shape", ""),
            "crop_path": crop_path,
            "source_image": meta.get("source_image", ""),
            "question_text": question_text,
            "caption_layer": "fretboard_answer_caption_v1",
        }.items()
    }
    return normalized


def render_report(rows: list[dict[str, Any]], output_jsonl: Path, batches: list[Path]) -> str:
    by_type = Counter(str(row.get("visual_type") or row.get("image_type") or "") for row in rows)
    by_exercise = Counter(str((row.get("source_metadata") or {}).get("exercise_number", "")) for row in rows)
    examples = rows[:5]
    lines = [
        "# 指板练习答案 Caption 正式层报告",
        "",
        "## Summary",
        "",
        f"- captions: {len(rows)}",
        f"- batches: {len(batches)}",
        f"- output_jsonl: `{output_jsonl.as_posix()}`",
        "- status: all accepted",
        "- layer: `fretboard_answer_caption_v1`",
        "- recommended_collection: `guitar_fretboard_answer_captions_qwen3_06b`",
        "",
        "## Visual Types",
        "",
    ]
    for name, count in by_type.most_common():
        lines.append(f"- `{name or 'unknown'}`: {count}")
    lines += ["", "## Exercise Distribution", ""]
    for name, count in sorted(by_exercise.items(), key=lambda item: int(item[0]) if item[0].isdigit() else 10**9):
        lines.append(f"- exercise `{name}`: {count}")
    lines += ["", "## Examples", ""]
    for row in examples:
        meta = row.get("source_metadata") or {}
        lines += [
            f"### {row.get('segment_id')}",
            "",
            f"- exercise/subquestion: `{meta.get('exercise_number')}` / `{meta.get('subquestion_number')}`",
            f"- crop: `{meta.get('crop_path')}`",
            f"- object: `{row.get('musical_object')}`",
            f"- caption: {row.get('caption')}",
            "",
        ]
    return "\n".join(lines).rstrip() + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batches-dir", type=Path, default=DEFAULT_BATCHES)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--expected-count", type=int, default=389)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    batch_dirs = sorted(
        [path for path in args.batches_dir.iterdir() if path.is_dir() and BATCH_RE.match(path.name)],
        key=batch_key,
    )
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    duplicates: list[str] = []
    missing_files: list[str] = []

    for batch_dir in batch_dirs:
        result_path = batch_dir / "caption_results.jsonl"
        if not result_path.exists():
            missing_files.append(str(result_path))
            continue
        for index, row in enumerate(read_jsonl(result_path), start=1):
            normalized = normalize_row(row, batch_dir.name, index)
            segment_id = normalized["segment_id"]
            if segment_id in seen:
                duplicates.append(segment_id)
                continue
            seen.add(segment_id)
            rows.append(normalized)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_jsonl = args.output_dir / "fretboard_answer_visual_caption_accepted_all.jsonl"
    output_json = args.output_dir / "fretboard_answer_visual_caption_accepted_all.json"
    report_json = args.output_dir / "fretboard_answer_visual_caption_layer_report.json"
    report_md = args.output_dir / "fretboard_answer_visual_caption_layer_report.md"

    with output_jsonl.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    output_json.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    report = {
        "captions": len(rows),
        "expected_count": args.expected_count,
        "complete": len(rows) == args.expected_count,
        "batches": [path.name for path in batch_dirs],
        "missing_files": missing_files,
        "duplicates": duplicates,
        "output_jsonl": str(output_jsonl),
        "recommended_collection": "guitar_fretboard_answer_captions_qwen3_06b",
        "layer": "fretboard_answer_caption_v1",
    }
    report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    report_md.write_text(render_report(rows, output_jsonl, batch_dirs), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["complete"] and not duplicates and not missing_files else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
