#!/usr/bin/env python
"""Ingest Math Rock PDF visual evidence into Chroma."""

from __future__ import annotations

import sys

from ingest_visuals_to_chroma import main


ARGS = [
    "--source-id",
    "mathrock_pdf_steve_h",
    "--source-title",
    "Math Rock Guitar E-book",
    "--style-tags",
    "math_rock,midwest_emo,tapping,alternate_tuning,voicing",
    "--book-dir",
    r"data\processed\mathrock\pdf_mineru\Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans\auto",
    "--content-list",
    r"data\processed\mathrock\pdf_mineru\Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans\auto\Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans_content_list.json",
    "--full-page-manifest",
    r"data\processed\mathrock\pdf_page_images\mathrock_pdf_page_images_manifest.jsonl",
    "--manifest-jsonl",
    r"data\processed\mathrock\visual_layer\mathrock_visual_manifest.jsonl",
    "--report-md",
    r"data\processed\mathrock\visual_layer\mathrock_visual_manifest.md",
    "--batch-size",
    "5",
]


if __name__ == "__main__":
    raise SystemExit(main(ARGS + sys.argv[1:]))
