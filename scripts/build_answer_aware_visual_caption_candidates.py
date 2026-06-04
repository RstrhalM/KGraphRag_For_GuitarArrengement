#!/usr/bin/env python
"""Build answer-aware visual-caption candidates for fretboard exercises.

This converts exercise-heavy body-image candidates into fewer candidates whose
primary visual evidence is the corresponding answer image. The body candidates
are retained as metadata/context, but blank exercise diagrams are not sent as
the main image evidence.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


EXERCISE_HEADING_RE = re.compile(r"^\s*##\s*练习\s*(\d+)\s*$", re.MULTILINE)
ANY_HEADING_RE = re.compile(r"^\s*##\s+.+$", re.MULTILINE)
ANSWER_START_RE = re.compile(r"^\s*##\s*练习答案\s*$", re.MULTILINE)
IMAGE_MD_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")


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


def parse_answer_image_range(path: Path) -> set[int]:
    match = re.search(r"练习\s*(\d+)(?:\s*[-—－]\s*(?:练习)?\s*(\d+))?", path.stem)
    if not match:
        return set()
    start = int(match.group(1))
    end = int(match.group(2) or start)
    if end < start:
        start, end = end, start
    return set(range(start, end + 1))


def parse_exercise_numbers(text: str) -> set[int]:
    return {int(match.group(1)) for match in re.finditer(r"练习\s*(\d+)", text)}


def clean_context(text: str, max_chars: int) -> str:
    text = IMAGE_MD_RE.sub("[IMAGE]", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = text.strip()
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "..."


def extract_body_exercise_sections(markdown_path: Path, max_chars: int) -> dict[int, str]:
    text = markdown_path.read_text(encoding="utf-8")
    answer_start = ANSWER_START_RE.search(text)
    if answer_start:
        text = text[: answer_start.start()]

    exercise_matches = list(EXERCISE_HEADING_RE.finditer(text))
    heading_starts = [match.start() for match in ANY_HEADING_RE.finditer(text)]
    sections: dict[int, str] = {}
    for match in exercise_matches:
        exercise_no = int(match.group(1))
        start = match.start()
        end = next((pos for pos in heading_starts if pos > start), len(text))
        section = clean_context(text[start:end], max_chars)
        # Keep the first body occurrence; later duplicates are usually answer-like or OCR leftovers.
        sections.setdefault(exercise_no, section)
    return sections


def build_answer_index(answers_dir: Path) -> dict[Path, set[int]]:
    answer_index: dict[Path, set[int]] = {}
    for path in sorted(answers_dir.iterdir()):
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        exercises = parse_answer_image_range(path)
        if exercises:
            answer_index[path] = exercises
    return answer_index


def selected_body_exercises(rows: list[dict[str, Any]]) -> set[int]:
    exercises: set[int] = set()
    for row in rows:
        exercises.update(parse_exercise_numbers(str(row.get("topic_hint") or "")))
        exercises.update(parse_exercise_numbers(str(row.get("nearby_text") or "")))
    return exercises


def body_rows_by_exercise(rows: list[dict[str, Any]]) -> dict[int, list[dict[str, Any]]]:
    grouped: dict[int, list[dict[str, Any]]] = {}
    for row in rows:
        numbers = parse_exercise_numbers(
            " ".join([str(row.get("topic_hint") or ""), str(row.get("nearby_text") or "")])
        )
        for exercise_no in numbers:
            grouped.setdefault(exercise_no, []).append(row)
    return grouped


def render_md(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Answer-Aware Visual Caption Candidates",
        "",
        f"- 候选数量：{len(rows)}",
        "- 用途：用练习题干 + 参考答案图生成结构化 visual caption。",
        "- 当前文件只包含本地候选，不代表已发送到 VLM API。",
        "- 正文练习小图只作为溯源 metadata；主视觉证据是答案图。",
        "",
    ]
    for idx, row in enumerate(rows, start=1):
        meta = row.get("answer_metadata", {}) if isinstance(row.get("answer_metadata"), dict) else {}
        body_visuals = row.get("body_visual_ids") if isinstance(row.get("body_visual_ids"), list) else []
        lines.extend(
            [
                f"## {idx:02d}. {row.get('visual_id')}",
                "",
                f"- source_id: `{row.get('source_id')}`",
                f"- visual_role: `{row.get('visual_role')}`",
                f"- priority: `{row.get('priority')}`",
                f"- exercise_numbers: `{', '.join(map(str, row.get('exercise_numbers') or []))}`",
                f"- answer_image: `{row.get('image_path')}`",
                f"- answer_range: `{', '.join(map(str, meta.get('answer_range') or []))}`",
                f"- linked body visuals: `{len(body_visuals)}`",
                "",
                "body_context:",
                "",
                "```text",
                str(row.get("nearby_text") or "")[:1800],
                "```",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--body-candidates", type=Path, required=True)
    parser.add_argument("--body-markdown", type=Path, required=True)
    parser.add_argument("--answers-dir", type=Path, required=True)
    parser.add_argument("-o", "--output-dir", type=Path, required=True)
    parser.add_argument("--context-chars-per-exercise", type=int, default=900)
    parser.add_argument("--only-selected-exercises", action="store_true", default=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    body_candidates = read_jsonl(args.body_candidates)
    selected_exercises = selected_body_exercises(body_candidates)
    grouped_body_rows = body_rows_by_exercise(body_candidates)
    body_sections = extract_body_exercise_sections(args.body_markdown, args.context_chars_per_exercise)
    answer_index = build_answer_index(args.answers_dir)

    rows: list[dict[str, Any]] = []
    for answer_path, answer_range in sorted(answer_index.items(), key=lambda item: (min(item[1]), answer_path_sort_key(item[0]))):
        relevant = sorted(answer_range & selected_exercises)
        if args.only_selected_exercises and not relevant:
            continue
        context_parts: list[str] = []
        body_visual_ids: list[str] = []
        body_image_paths: list[str] = []
        for exercise_no in relevant:
            section = body_sections.get(exercise_no, f"## 练习{exercise_no}\n[body context not found]")
            context_parts.append(section)
            for body_row in grouped_body_rows.get(exercise_no, []):
                visual_id = str(body_row.get("visual_id") or "")
                image_path = str(body_row.get("image_path") or "")
                if visual_id and visual_id not in body_visual_ids:
                    body_visual_ids.append(visual_id)
                if image_path and image_path not in body_image_paths:
                    body_image_paths.append(image_path)
        if not relevant:
            continue
        if not answer_path.exists():
            raise FileNotFoundError(answer_path)
        first_ex = min(relevant)
        last_ex = max(relevant)
        visual_id = f"fretboard_answer:e{first_ex:03d}_{last_ex:03d}:{answer_path.stem}"
        rows.append(
            {
                "visual_id": visual_id,
                "source_id": "fretboard_handbook_answer_solutions",
                "source_title": "吉他指板手册",
                "source_type": "answer_aware_visual_caption",
                "visual_role": "answer_solution",
                "image_type_hint": "answer_diagram",
                "priority": "P0_P1_foundation_answer",
                "style_tags": ["fretboard", "guitar_foundation", "answer_solution"],
                "exercise_numbers": relevant,
                "image_path": str(answer_path),
                "image_paths": [str(answer_path)],
                "body_image_paths": body_image_paths,
                "body_visual_ids": body_visual_ids,
                "topic_hint": " | ".join(f"练习{num}" for num in relevant),
                "nearby_text": "\n\n---\n\n".join(context_parts),
                "answer_metadata": {
                    "answer_image": str(answer_path),
                    "answer_range": sorted(answer_range),
                    "selected_exercises": relevant,
                    "body_candidate_count": len(body_visual_ids),
                },
                "caption_status": "pending",
                "caption_decision": "",
            }
        )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = args.output_dir / "visual_caption_candidates.jsonl"
    write_jsonl(jsonl_path, rows)
    (args.output_dir / "visual_caption_candidates.md").write_text(render_md(rows), encoding="utf-8")
    report = {
        "body_candidates": str(args.body_candidates),
        "body_markdown": str(args.body_markdown),
        "answers_dir": str(args.answers_dir),
        "selected_exercises": sorted(selected_exercises),
        "candidates": len(rows),
        "answer_images": [row["image_path"] for row in rows],
        "output": str(jsonl_path),
    }
    (args.output_dir / "visual_caption_candidate_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def answer_path_sort_key(path: Path) -> str:
    return path.name


if __name__ == "__main__":
    raise SystemExit(main())
