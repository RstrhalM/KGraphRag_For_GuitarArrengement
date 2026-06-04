#!/usr/bin/env python
"""Split KG review items by chunks with missing visual context."""

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


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def missing_visual_chunks(report_path: Path) -> set[str]:
    report = json.loads(report_path.read_text(encoding="utf-8"))
    chunks: set[str] = set()
    for item in report.get("chunk_reports", []) or []:
        discarded = item.get("discarded_summary", {}) or {}
        if int(discarded.get("missing_visual_context", 0) or 0) > 0:
            chunks.add(str(item.get("chunk_id", "")))
    return chunks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-jsonl", type=Path, required=True)
    parser.add_argument("--report-json", type=Path, required=True)
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--missing-jsonl", type=Path, required=True)
    parser.add_argument("--raw-backup", type=Path, required=True)
    args = parser.parse_args()

    rows = read_jsonl(args.review_jsonl)
    if not args.raw_backup.exists():
        write_jsonl(args.raw_backup, rows)

    missing_chunks = missing_visual_chunks(args.report_json)
    missing_rows: list[dict[str, Any]] = []
    updated_rows: list[dict[str, Any]] = []
    auto_accept = 0

    for row in rows:
        row = dict(row)
        if str(row.get("chunk_id", "")) in missing_chunks:
            row["review_status"] = "pending"
            row["decision"] = ""
            row["reject_reason"] = "需视觉补抽/复核：该 chunk 的报告存在 missing_visual_context。"
            missing_rows.append(row)
        else:
            row["review_status"] = "reviewed"
            row["decision"] = "accept"
            row["reject_reason"] = ""
            auto_accept += 1
        updated_rows.append(row)

    write_jsonl(args.output_jsonl, updated_rows)
    write_jsonl(args.missing_jsonl, missing_rows)
    print(
        json.dumps(
            {
                "total": len(rows),
                "missing_visual_chunks": sorted(missing_chunks),
                "missing_review_items": len(missing_rows),
                "auto_accept_items": auto_accept,
                "output_jsonl": str(args.output_jsonl),
                "missing_jsonl": str(args.missing_jsonl),
                "raw_backup": str(args.raw_backup),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
