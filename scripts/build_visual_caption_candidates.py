#!/usr/bin/env python
"""Build a small visual-caption trial queue from existing visual manifests."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


FRETBOARD_PRIORITIES = {"P2_arpeggios_chords", "P3_common_scales_chords"}
FRETBOARD_PRIORITY_BASE = {
    "P0_root_fingering_forms": 12.0,
    "P1_scales_intervals": 11.0,
    "P2_arpeggios_chords": 10.0,
    "P3_common_scales_chords": 9.0,
}
MATHROCK_KEYWORDS = [
    "FACGCE",
    "DAEAC",
    "maj9",
    "m7b5",
    "和弦",
    "调弦",
    "点弦",
    "tapping",
    "voicing",
    "open",
    "chord",
]
NOISE_KEYWORDS = ["目录", "版权", "封面", "finger exerciser", "训练器"]


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


def text_of(row: dict[str, Any]) -> str:
    return " ".join(
        str(row.get(key) or "")
        for key in ["source_title", "priority", "topic_hint", "nearby_text", "image_name", "original_block_type"]
    )


def has_noise(row: dict[str, Any]) -> bool:
    text = text_of(row).lower()
    return any(keyword.lower() in text for keyword in NOISE_KEYWORDS)


def score_fretboard(row: dict[str, Any], priorities: set[str] | None = None) -> float:
    priority = str(row.get("priority") or "")
    priorities = priorities or FRETBOARD_PRIORITIES
    if priority not in priorities:
        return -999.0
    if has_noise(row):
        return -999.0
    score = FRETBOARD_PRIORITY_BASE.get(priority, 8.0)
    text = text_of(row)
    for keyword in [
        "根音型式",
        "指型",
        "音阶",
        "音程",
        "琶音",
        "三和弦",
        "七和弦",
        "常用和弦",
        "六和弦",
        "九和弦",
        "add9",
    ]:
        if keyword in text:
            score += 2.0
    if row.get("nearby_text"):
        score += 1.0
    return score


def score_mathrock(row: dict[str, Any]) -> float:
    if str(row.get("source_id")) != "mathrock_pdf_steve_h":
        return -999.0
    if has_noise(row):
        return -999.0
    text = text_of(row)
    if not str(row.get("nearby_text") or "").strip():
        return -999.0
    score = 0.0
    for keyword in MATHROCK_KEYWORDS:
        if keyword.lower() in text.lower():
            score += 2.0
    page = int(row.get("page") or 0)
    if page in {33, 34, 35, 36, 37, 38, 39, 40, 49, 50, 51, 60, 61, 64, 65, 67}:
        score += 3.0
    if row.get("visual_granularity") == "full_page":
        score += 1.5
    return score if score > 0 else -999.0


def row_keys(row: dict[str, Any]) -> set[str]:
    return {
        str(row.get("visual_id") or ""),
        str(row.get("image_path") or ""),
    } - {""}


def read_excludes(paths: list[Path]) -> set[str]:
    excluded: set[str] = set()
    for path in paths:
        if not path.exists():
            continue
        for row in read_jsonl(path):
            excluded.update(row_keys(row))
            source_metadata = row.get("source_metadata")
            if isinstance(source_metadata, dict):
                excluded.update(row_keys(source_metadata))
    return excluded


def pick_diverse(
    rows: list[dict[str, Any]],
    score_fn,
    limit: int,
    per_page: int,
    excluded: set[str] | None = None,
) -> list[dict[str, Any]]:
    if limit <= 0:
        return []
    excluded = excluded or set()
    scored: list[tuple[float, dict[str, Any]]] = []
    for row in rows:
        if row_keys(row) & excluded:
            continue
        score = score_fn(row)
        if score > -100:
            scored.append((score, row))
    scored.sort(key=lambda item: (-item[0], int(item[1].get("page") or 999), str(item[1].get("visual_id"))))

    selected: list[dict[str, Any]] = []
    page_counts: dict[int, int] = {}
    seen_images: set[str] = set()
    for score, row in scored:
        page = int(row.get("page") or 0)
        image_path = str(row.get("image_path") or "")
        if not image_path or image_path in seen_images:
            continue
        if page_counts.get(page, 0) >= per_page:
            continue
        row = dict(row)
        row["selection_score"] = score
        row["caption_status"] = "pending"
        row["caption_decision"] = ""
        selected.append(row)
        seen_images.add(image_path)
        page_counts[page] = page_counts.get(page, 0) + 1
        if len(selected) >= limit:
            break
    return selected


def caption_context(row: dict[str, Any]) -> str:
    text = re.sub(r"\s+", " ", str(row.get("nearby_text") or "")).strip()
    return text[:500]


def render_md(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Visual Caption Trial Candidates",
        "",
        f"- 候选数量：{len(rows)}",
        "- 用途：人工快速检查候选图片是否适合做 VLM 结构化 caption。",
        "- 当前文件只包含本地候选，不代表已发送到 VLM API。",
        "",
    ]
    for idx, row in enumerate(rows, start=1):
        lines.extend(
            [
                f"## {idx:02d}. {row.get('visual_id')}",
                "",
                f"- source_id: `{row.get('source_id')}`",
                f"- page: `{row.get('page')}`",
                f"- priority/granularity: `{row.get('priority') or row.get('visual_granularity')}`",
                f"- score: `{row.get('selection_score')}`",
                f"- image_path: `{row.get('image_path')}`",
                f"- topic_hint: {row.get('topic_hint') or ''}",
                "",
                "nearby_text:",
                "",
                f"> {caption_context(row)}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fretboard-manifest", type=Path, required=True)
    parser.add_argument("--mathrock-manifest", type=Path, required=True)
    parser.add_argument("-o", "--output-dir", type=Path, required=True)
    parser.add_argument("--fretboard-limit", type=int, default=10)
    parser.add_argument("--mathrock-limit", type=int, default=10)
    parser.add_argument("--per-page", type=int, default=2)
    parser.add_argument(
        "--fretboard-priority",
        action="append",
        default=[],
        help=(
            "Fretboard priority bucket to include. Can be passed more than once. "
            "Defaults to P2_arpeggios_chords and P3_common_scales_chords."
        ),
    )
    parser.add_argument(
        "--exclude-jsonl",
        type=Path,
        action="append",
        default=[],
        help="JSONL files whose visual_id/image_path values should be skipped. Can be passed more than once.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    fretboard_rows = read_jsonl(args.fretboard_manifest)
    mathrock_rows = read_jsonl(args.mathrock_manifest)
    excluded = read_excludes(args.exclude_jsonl)
    fretboard_priorities = set(args.fretboard_priority) if args.fretboard_priority else FRETBOARD_PRIORITIES
    selected = []
    selected.extend(
        pick_diverse(
            fretboard_rows,
            lambda row: score_fretboard(row, fretboard_priorities),
            args.fretboard_limit,
            args.per_page,
            excluded,
        )
    )
    selected.extend(pick_diverse(mathrock_rows, score_mathrock, args.mathrock_limit, args.per_page, excluded))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = args.output_dir / "visual_caption_candidates.jsonl"
    with jsonl_path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in selected:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    (args.output_dir / "visual_caption_candidates.md").write_text(render_md(selected), encoding="utf-8")
    report = {
        "fretboard_manifest": str(args.fretboard_manifest),
        "mathrock_manifest": str(args.mathrock_manifest),
        "candidates": len(selected),
        "fretboard": sum(1 for row in selected if row.get("source_id") == "fretboard_handbook_mineru"),
        "fretboard_priorities": sorted(fretboard_priorities),
        "mathrock": sum(1 for row in selected if row.get("source_id") == "mathrock_pdf_steve_h"),
        "excluded_keys": len(excluded),
        "output": str(jsonl_path),
    }
    (args.output_dir / "visual_caption_candidate_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
