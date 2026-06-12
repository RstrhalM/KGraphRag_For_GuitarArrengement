#!/usr/bin/env python
"""Merge reviewed canonical terms into accepted visual-caption rows."""

from __future__ import annotations

import argparse
import json
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


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--captions", type=Path, required=True)
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--accept-trusted", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    captions = read_jsonl(args.captions)
    canonical_rows = read_jsonl(args.canonical)
    canonical_by_id = {str(row.get("visual_id") or ""): row for row in canonical_rows}
    merged: list[dict[str, Any]] = []
    missing: list[str] = []
    for caption in captions:
        visual_id = str(caption.get("visual_id") or "")
        sidecar = canonical_by_id.get(visual_id)
        if not sidecar:
            missing.append(visual_id)
            continue
        row = dict(caption)
        row["canonical_terms"] = sidecar.get("canonical_terms") or []
        row["canonical_sidecar"] = {
            "status": "accepted" if args.accept_trusted else sidecar.get("status", "pending_review"),
            "aliases_detected": sidecar.get("aliases_detected") or [],
            "roots": sidecar.get("roots") or [],
            "chord_qualities": sidecar.get("chord_qualities") or [],
            "scale_or_mode": sidecar.get("scale_or_mode") or [],
            "visual_type": sidecar.get("visual_type") or "",
            "confidence": sidecar.get("confidence", 0.0),
            "uncertainty_notes": sidecar.get("uncertainty_notes") or [],
        }
        merged.append(row)
    write_jsonl(args.output, merged)
    report = {
        "captions": len(captions),
        "canonical_rows": len(canonical_rows),
        "merged": len(merged),
        "missing": missing,
        "output": str(args.output),
    }
    args.output.with_suffix(".report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
