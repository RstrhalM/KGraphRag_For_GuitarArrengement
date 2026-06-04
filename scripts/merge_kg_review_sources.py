#!/usr/bin/env python
"""Merge selected KG review JSONL files while preserving source labels."""

from __future__ import annotations

import argparse
import json
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
                raise ValueError(f"Invalid JSON on {path}:{line_no}: {exc}") from exc
            if isinstance(row, dict):
                rows.append(row)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def parse_source_arg(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("source must be LABEL=PATH")
    label, raw_path = value.split("=", 1)
    label = label.strip()
    if not label:
        raise argparse.ArgumentTypeError("source label cannot be empty")
    return label, Path(raw_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", action="append", type=parse_source_arg, required=True, help="LABEL=review.jsonl")
    parser.add_argument("--chunk-id", action="append", default=[], help="Chunk id to keep; repeatable")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Merged review JSONL")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    chunk_filter = set(args.chunk_id)
    merged: list[dict[str, Any]] = []
    source_counts: dict[str, int] = {}

    for label, path in args.source:
        rows = read_jsonl(path)
        source_index = 1
        for row in rows:
            chunk_id = str(row.get("chunk_id", ""))
            if chunk_filter and chunk_id not in chunk_filter:
                continue
            item = dict(row)
            original_review_id = str(item.get("review_id", ""))
            item["source_pass"] = item.get("source_pass") or label
            item["original_review_id"] = original_review_id
            item["review_id"] = f"{chunk_id}:{label}:{source_index:03d}"
            merged.append(item)
            source_counts[label] = source_counts.get(label, 0) + 1
            source_index += 1

    write_jsonl(args.output, merged)
    report = {
        "output": str(args.output),
        "items": len(merged),
        "chunk_filter": sorted(chunk_filter),
        "source_counts": source_counts,
    }
    report_path = args.output.with_name("merge_report.json")
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(merged)} merged review items to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
