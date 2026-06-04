#!/usr/bin/env python
"""Inspect PDF pages for text length and embedded image density."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from pypdf import PdfReader


def count_page_images(page: Any) -> int:
    resources = page.get("/Resources") or {}
    xobject = resources.get("/XObject") if resources else None
    if not xobject:
        return 0
    count = 0
    for obj in xobject.get_object().values():
        try:
            if obj.get_object().get("/Subtype") == "/Image":
                count += 1
        except Exception:
            continue
    return count


def compact_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def inspect_pdf(path: Path) -> list[dict[str, Any]]:
    reader = PdfReader(str(path))
    rows: list[dict[str, Any]] = []
    for index, page in enumerate(reader.pages, start=1):
        text = compact_text(page.extract_text() or "")
        rows.append(
            {
                "page": index,
                "chars": len(text),
                "images": count_page_images(page),
                "sample": text[:180],
            }
        )
    return rows


def contiguous_ranges(pages: list[int]) -> list[str]:
    if not pages:
        return []
    pages = sorted(set(pages))
    ranges: list[str] = []
    start = prev = pages[0]
    for page in pages[1:]:
        if page == prev + 1:
            prev = page
            continue
        ranges.append(str(start) if start == prev else f"{start}-{prev}")
        start = prev = page
    ranges.append(str(start) if start == prev else f"{start}-{prev}")
    return ranges


def render_markdown(path: Path, rows: list[dict[str, Any]]) -> str:
    heavy = [
        row["page"]
        for row in rows
        if row["images"] >= 3 or (row["images"] >= 2 and row["chars"] < 500)
    ]
    low_text = [row["page"] for row in rows if row["images"] >= 1 and row["chars"] < 350]
    lines = [
        f"# PDF Visual Density Report: {path.name}",
        "",
        f"- Pages: {len(rows)}",
        f"- Image-heavy pages: {', '.join(contiguous_ranges(heavy)) or 'None'}",
        f"- Low-text visual pages: {', '.join(contiguous_ranges(low_text)) or 'None'}",
        "",
        "## Image-Heavy / Visual-Reprocess Candidates",
        "",
        "| Page | Chars | Images | Sample |",
        "| --- | ---: | ---: | --- |",
    ]
    for row in rows:
        if row["page"] in set(heavy):
            sample = str(row["sample"]).replace("|", "\\|")
            lines.append(f"| {row['page']} | {row['chars']} | {row['images']} | {sample} |")
    lines.extend(["", "## All Pages", "", "| Page | Chars | Images | Sample |", "| --- | ---: | ---: | --- |"])
    for row in rows:
        sample = str(row["sample"]).replace("|", "\\|")
        lines.append(f"| {row['page']} | {row['chars']} | {row['images']} | {sample} |")
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="PDF path")
    parser.add_argument("-o", "--output", type=Path, help="Output report Markdown")
    parser.add_argument("--json", type=Path, help="Output page stats JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = inspect_pdf(args.input)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(render_markdown(args.input, rows), encoding="utf-8", newline="\n")
    heavy = [
        row["page"]
        for row in rows
        if row["images"] >= 3 or (row["images"] >= 2 and row["chars"] < 500)
    ]
    print(json.dumps({"pages": len(rows), "image_heavy_pages": contiguous_ranges(heavy)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
