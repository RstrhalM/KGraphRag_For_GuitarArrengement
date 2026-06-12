#!/usr/bin/env python
"""Finalize a reviewed visual-caption batch into an accepted JSONL layer."""

from __future__ import annotations

import argparse
import json
import re
import sys
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
                raise ValueError(f"Invalid JSON in {path} line {line_no}: {exc}") from exc
            if isinstance(row, dict):
                rows.append(row)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def accepted_ids_from_review(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    accepted: set[str] = set()
    blocks = re.split(r"(?=^##\s+\d+\.\s+)", text, flags=re.MULTILINE)
    for block in blocks:
        id_match = re.search(r"<!--\s*visual_id:\s*(.*?)\s*-->", block)
        if id_match and re.search(r"^- \[[xX]\] accept\s*$", block, flags=re.MULTILINE):
            accepted.add(id_match.group(1).strip())
    return accepted


def mark_all_accept(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^- \[ \] accept\s*$", "- [x] accept", text, flags=re.MULTILINE)
    path.write_text(text, encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--review-md", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--candidates", type=Path)
    parser.add_argument("--all-accept", action="store_true")
    parser.add_argument("--layer", default="mathrock_style_visual_caption_v1")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.all_accept:
        mark_all_accept(args.review_md)
    accepted_ids = accepted_ids_from_review(args.review_md)
    source_rows = read_jsonl(args.results)
    candidates = read_jsonl(args.candidates) if args.candidates else []
    candidate_by_id = {str(row.get("visual_id") or ""): row for row in candidates}
    output_rows: list[dict[str, Any]] = []
    for row in source_rows:
        visual_id = str(row.get("visual_id") or "")
        if visual_id not in accepted_ids:
            continue
        normalized = dict(row)
        normalized["accepted"] = True
        normalized["status"] = "accepted"
        normalized["caption_layer"] = args.layer
        candidate = candidate_by_id.get(visual_id, {})
        normalized["trusted_facts"] = {
            "tuning": candidate.get("known_tuning"),
            "chords": candidate.get("known_chords") or ([candidate["known_chord"]] if candidate.get("known_chord") else []),
            "scales": candidate.get("known_scales") or [],
            "techniques": candidate.get("known_techniques") or [],
            "meters": candidate.get("known_meters") or [],
            "visual_type": normalized.get("image_type"),
            "visual_subtype": candidate.get("image_type_hint"),
            "style_tags": candidate.get("style_tags") or [],
        }
        output_rows.append(normalized)
    write_jsonl(args.output, output_rows)
    report = {
        "source_rows": len(source_rows),
        "accepted_ids": len(accepted_ids),
        "output_rows": len(output_rows),
        "output": str(args.output),
        "layer": args.layer,
    }
    report_path = args.output.with_suffix(".report.json")
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if len(output_rows) == len(accepted_ids) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
