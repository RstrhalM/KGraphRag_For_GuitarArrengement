from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


EXERCISE_TERMS = ("练习", "答案", "exercise", "answer", "question")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            text = line.strip()
            if not text:
                continue
            row = json.loads(text)
            row["_line_number"] = line_number
            rows.append(row)
    return rows


def dump_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            clean = {k: v for k, v in row.items() if not k.startswith("_")}
            handle.write(json.dumps(clean, ensure_ascii=False) + "\n")


def row_text(row: dict[str, Any]) -> str:
    fields = (
        "visual_id",
        "source_id",
        "source_title",
        "source_type",
        "priority",
        "image_path",
        "image_name",
        "topic_hint",
        "nearby_text",
    )
    chunks: list[str] = []
    for field in fields:
        value = row.get(field)
        if value is None:
            continue
        if isinstance(value, list):
            chunks.extend(str(item) for item in value)
        else:
            chunks.append(str(value))
    return "\n".join(chunks).lower()


def is_exercise_related(row: dict[str, Any]) -> bool:
    text = row_text(row)
    return any(term.lower() in text for term in EXERCISE_TERMS)


def write_markdown(path: Path, rows: list[dict[str, Any]], title: str) -> None:
    lines = [f"# {title}", ""]
    lines.append(f"- total: {len(rows)}")
    lines.append("- note: exercise-related legacy visual blocks have been removed; use the formal question-answer caption layer for exercises.")
    lines.append("")

    for index, row in enumerate(rows, start=1):
        lines.append(f"## {index:03d}. {row.get('visual_id', '')}")
        lines.append(f"- source_title: {row.get('source_title', '')}")
        lines.append(f"- priority: {row.get('priority', '')}")
        lines.append(f"- page: {row.get('page', '')}")
        lines.append(f"- topic_hint: {row.get('topic_hint', '')}")
        lines.append(f"- image_path: {row.get('image_path', '')}")
        bbox = row.get("bbox", "")
        lines.append(f"- bbox: {bbox}")
        nearby = str(row.get("nearby_text", "")).replace("\n", " ").strip()
        if len(nearby) > 500:
            nearby = nearby[:500] + "..."
        lines.append(f"- nearby_text: {nearby}")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def write_report(
    path: Path,
    manifest_path: Path,
    archive_dir: Path,
    original_count: int,
    kept: list[dict[str, Any]],
    removed: list[dict[str, Any]],
) -> None:
    removed_priorities = Counter(str(row.get("priority", "")) for row in removed)
    removed_pages = Counter(str(row.get("page", "")) for row in removed)
    lines = [
        "# Fretboard Visual Manifest Cleanup Report",
        "",
        f"- date: {date.today().isoformat()}",
        f"- manifest: `{manifest_path.as_posix()}`",
        f"- original_count: {original_count}",
        f"- kept_non_exercise_count: {len(kept)}",
        f"- removed_exercise_related_count: {len(removed)}",
        f"- filter_terms: {', '.join(EXERCISE_TERMS)}",
        f"- archive_dir: `{archive_dir.as_posix()}`",
        "",
        "## Removed By Priority",
        "",
    ]
    if removed_priorities:
        for key, value in removed_priorities.most_common():
            lines.append(f"- {key or '(empty)'}: {value}")
    else:
        lines.append("- none")
    lines.extend(["", "## Removed By Page", ""])
    if removed_pages:
        for key, value in sorted(removed_pages.items(), key=lambda item: (int(item[0]) if item[0].isdigit() else 10_000, item[0])):
            lines.append(f"- page {key or '(empty)'}: {value}")
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Policy",
            "",
            "旧版 MinerU 图片块中凡是 `topic_hint`、`nearby_text`、路径或标识字段包含练习/答案语义的条目均从旧视觉清单中移除。",
            "练习答案图以后只保留新版题目级 `question_answer_visual_caption_layer`，避免同一练习同时从旧图块和新版题目级 caption 层召回。",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        default="data/processed/fretboard_handbook/visual_layer/fretboard_visual_manifest.jsonl",
        type=Path,
    )
    parser.add_argument(
        "--manifest-md",
        default="data/processed/fretboard_handbook/visual_layer/fretboard_visual_manifest.md",
        type=Path,
    )
    parser.add_argument(
        "--archive-dir",
        default=f"data/archive/fretboard_visual_manifest_cleanup_{date.today().isoformat()}",
        type=Path,
    )
    args = parser.parse_args()

    rows = read_jsonl(args.manifest)
    kept = [row for row in rows if not is_exercise_related(row)]
    removed = [row for row in rows if is_exercise_related(row)]

    args.archive_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(args.manifest, args.archive_dir / "fretboard_visual_manifest.original.jsonl")
    if args.manifest_md.exists():
        shutil.copy2(args.manifest_md, args.archive_dir / "fretboard_visual_manifest.original.md")

    dump_jsonl(args.archive_dir / "fretboard_visual_manifest.kept_non_exercise.jsonl", kept)
    dump_jsonl(args.archive_dir / "fretboard_visual_manifest.removed_exercise_related.jsonl", removed)
    dump_jsonl(args.manifest, kept)
    write_markdown(args.manifest_md, kept, "Fretboard Visual Manifest")

    report_json = {
        "manifest": str(args.manifest),
        "original_count": len(rows),
        "kept_non_exercise_count": len(kept),
        "removed_exercise_related_count": len(removed),
        "filter_terms": list(EXERCISE_TERMS),
        "archive_dir": str(args.archive_dir),
    }
    (args.archive_dir / "cleanup_report.json").write_text(
        json.dumps(report_json, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_report(
        args.archive_dir / "cleanup_report.md",
        args.manifest,
        args.archive_dir,
        len(rows),
        kept,
        removed,
    )
    write_report(
        args.manifest.parent / "fretboard_visual_manifest_cleanup_report.md",
        args.manifest,
        args.archive_dir,
        len(rows),
        kept,
        removed,
    )
    print(json.dumps(report_json, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
