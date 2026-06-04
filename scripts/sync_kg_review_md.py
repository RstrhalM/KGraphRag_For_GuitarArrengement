#!/usr/bin/env python
"""Sync Markdown KG review decisions back into the review JSONL file."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


CHECKBOX_RE = re.compile(r"^-\s+\[(?P<mark>[ xX])\]\s+(?P<decision>accept|revise|reject)\s*$")
REVIEW_ID_RE = re.compile(r"^<!--\s*review_id:\s*(?P<review_id>.*?)\s*-->$")


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


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def parse_review_markdown(path: Path) -> dict[str, dict[str, str]]:
    reviews: dict[str, dict[str, str]] = {}
    current_id: str | None = None
    in_reason = False
    reason_lines: list[str] = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        id_match = REVIEW_ID_RE.match(line)
        if id_match:
            current_id = id_match.group("review_id").strip()
            reviews.setdefault(current_id, {"decision": "", "reject_reason": ""})
            in_reason = False
            reason_lines = []
            continue

        if current_id is None:
            continue

        if line.strip() == "<!-- review_reason_start -->":
            in_reason = True
            reason_lines = []
            continue
        if line.strip() == "<!-- review_reason_end -->":
            reviews[current_id]["reject_reason"] = "\n".join(reason_lines).strip()
            in_reason = False
            continue
        if in_reason:
            reason_lines.append(line)
            continue

        checkbox_match = CHECKBOX_RE.match(line.strip())
        if checkbox_match and checkbox_match.group("mark").lower() == "x":
            existing = reviews[current_id].get("decision", "")
            decision = checkbox_match.group("decision")
            if existing and existing != decision:
                raise ValueError(f"Multiple decisions checked for {current_id}: {existing}, {decision}")
            reviews[current_id]["decision"] = decision

    return reviews


def sync_reviews(jsonl_path: Path, markdown_path: Path, output_path: Path, *, all_accept: bool = False) -> tuple[int, int]:
    rows = read_jsonl(jsonl_path)
    reviews = {} if all_accept else parse_review_markdown(markdown_path)
    updated = 0

    for row in rows:
        if all_accept:
            row["decision"] = "accept"
            row["review_status"] = "reviewed"
            row["reject_reason"] = ""
            updated += 1
            continue
        review_id = str(row.get("review_id", ""))
        review = reviews.get(review_id)
        if not review:
            continue
        decision = review.get("decision", "")
        reject_reason = review.get("reject_reason", "")
        if decision:
            row["decision"] = decision
            row["review_status"] = "reviewed"
        else:
            row["decision"] = ""
            row["review_status"] = "pending"
        row["reject_reason"] = reject_reason
        updated += 1

    write_jsonl(output_path, rows)
    return updated, len(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jsonl", type=Path, required=True, help="Source arrangement_kg_review.jsonl")
    parser.add_argument("--md", type=Path, required=True, help="Reviewed Markdown file")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Synced output JSONL path")
    parser.add_argument("--all-accept", action="store_true", help="Mark every review item as accepted")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    updated, total = sync_reviews(args.jsonl, args.md, args.output, all_accept=args.all_accept)
    print(f"Synced {updated}/{total} review items to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
