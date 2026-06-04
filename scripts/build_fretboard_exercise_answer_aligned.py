from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_MD = (
    ROOT
    / "data"
    / "processed"
    / "mineru_full_gpu"
    / "吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)"
    / "ocr"
    / "吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org).md"
)
DEFAULT_OUTPUT_DIR = ROOT / "data" / "processed" / "fretboard_handbook" / "exercise_answer_aligned"

HEADING_RE = re.compile(r"^\s{0,3}#{1,3}\s+(.+?)\s*$")
EXERCISE_HEADING_RE = re.compile(r"^练习\s*(\d+)\s*$")
BARE_EXERCISE_HEADING_RE = re.compile(r"^\s*练习\s*\d+\s*$")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


@dataclass
class Section:
    title: str
    lines: list[str]
    start_line: int

    @property
    def text(self) -> str:
        return "\n".join(self.lines).strip()


def rel_to_root(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return str(path.resolve()).replace("\\", "/")


def split_sections(lines: list[str]) -> list[Section]:
    sections: list[Section] = []
    current_title = "Front Matter"
    current_lines: list[str] = []
    current_start = 1
    for index, line in enumerate(lines, start=1):
        match = HEADING_RE.match(line)
        bare_exercise = BARE_EXERCISE_HEADING_RE.match(line)
        if (match or bare_exercise) and current_lines:
            sections.append(Section(current_title, current_lines, current_start))
            current_lines = []
            current_start = index
        if match:
            current_title = match.group(1).strip()
        elif bare_exercise:
            current_title = line.strip()
        current_lines.append(line)
    if current_lines:
        sections.append(Section(current_title, current_lines, current_start))
    return sections


def exercise_number(title: str) -> int | None:
    match = EXERCISE_HEADING_RE.match(title.strip())
    if not match:
        return None
    return int(match.group(1))


def collect_exercises(sections: Iterable[Section]) -> dict[int, Section]:
    rows: dict[int, Section] = {}
    for section in sections:
        number = exercise_number(section.title)
        if number is not None:
            rows.setdefault(number, section)
    return rows


def image_refs(text: str) -> list[str]:
    return IMAGE_RE.findall(text)


def rewrite_image_paths(text: str, source_md: Path, output_md: Path) -> str:
    source_dir = source_md.parent
    output_dir = output_md.parent
    image_output_dir = output_dir / "images"
    image_output_dir.mkdir(parents=True, exist_ok=True)

    def repl(match: re.Match[str]) -> str:
        raw_path = match.group(1)
        image_path = Path(raw_path)
        if not image_path.is_absolute():
            image_path = source_dir / image_path
        dest_path = image_output_dir / image_path.name
        if image_path.exists() and not dest_path.exists():
            shutil.copy2(image_path, dest_path)
        rel_path = os.path.relpath(dest_path.resolve(), output_dir.resolve())
        return f"![]({rel_path.replace('\\', '/')})"

    return IMAGE_RE.sub(repl, text)


def remove_non_example_question_images(text: str) -> tuple[str, int, int]:
    """Drop blank exercise diagrams while retaining one explicitly answered example diagram."""
    refs = image_refs(text)
    if not refs:
        return text, 0, 0

    keep_first_example = "例子" in text and "答案" in text
    kept = 0
    removed = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal kept, removed
        if keep_first_example and kept == 0:
            kept += 1
            return match.group(0)
        removed += 1
        return ""

    cleaned = IMAGE_RE.sub(repl, text)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    return cleaned, kept, removed


def strip_heading(text: str) -> str:
    lines = text.splitlines()
    if lines and HEADING_RE.match(lines[0]):
        return "\n".join(lines[1:]).strip()
    return text.strip()


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def build(source_md: Path, output_dir: Path) -> dict[str, int | str]:
    lines = source_md.read_text(encoding="utf-8").splitlines()
    sections = split_sections(lines)
    answer_index = next(
        (i for i, section in enumerate(sections) if section.title.strip() == "练习答案"),
        None,
    )
    if answer_index is None:
        raise RuntimeError("未找到 `练习答案` 标题，无法区分题目区和答案区。")

    question_sections = collect_exercises(sections[:answer_index])
    answer_sections = collect_exercises(sections[answer_index + 1 :])
    all_numbers = sorted(set(question_sections) | set(answer_sections))

    output_dir.mkdir(parents=True, exist_ok=True)
    output_md = output_dir / "fretboard_exercise_answer_aligned.md"
    output_jsonl = output_dir / "fretboard_exercise_answer_aligned.jsonl"
    output_chunks = output_dir / "chunks.json"
    report_md = output_dir / "fretboard_exercise_answer_aligned_report.md"

    rows: list[dict] = []
    md_parts: list[str] = [
        "# 吉他指板手册：练习与参考答案对照",
        "",
        "说明：题目区默认删除空白作答图；仅当题干明确写出“例子/已给出答案”时，保留第一个例子图。参考答案区保留全部文本与图片。",
        "",
    ]
    report_rows: list[str] = [
        "# 吉他指板手册：练习答案对照构建报告",
        "",
        f"- source_md: `{rel_to_root(source_md)}`",
        f"- output_md: `{rel_to_root(output_md)}`",
        f"- output_jsonl: `{rel_to_root(output_jsonl)}`",
        f"- chunks_json: `{rel_to_root(output_chunks)}`",
        "",
        "| exercise | question_images_kept | question_images_removed | answer_images | has_question | has_answer |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]

    for number in all_numbers:
        question = question_sections.get(number)
        answer = answer_sections.get(number)
        question_text = strip_heading(question.text) if question else ""
        answer_text = strip_heading(answer.text) if answer else ""
        cleaned_question, kept_question_images, removed_question_images = remove_non_example_question_images(question_text)

        cleaned_question = rewrite_image_paths(cleaned_question, source_md, output_md)
        answer_text = rewrite_image_paths(answer_text, source_md, output_md)
        answer_images = len(image_refs(answer_text))

        md_parts.extend(
            [
                f"## 练习{number}",
                "",
                "### 题目",
                "",
                cleaned_question or "_题目区未解析到内容_",
                "",
                "### 参考答案",
                "",
                answer_text or "_参考答案区未解析到内容_",
                "",
                "---",
                "",
            ]
        )
        rows.append(
            {
                "exercise_id": f"fretboard_exercise_{number:02d}",
                "exercise_number": number,
                "source": "吉他指板手册",
                "question_text": cleaned_question,
                "answer_text": answer_text,
                "question_images_kept": kept_question_images,
                "question_images_removed": removed_question_images,
                "answer_images": answer_images,
                "question_start_line": question.start_line if question else None,
                "answer_start_line": answer.start_line if answer else None,
                "has_question": question is not None,
                "has_answer": answer is not None,
            }
        )
        report_rows.append(
            "| "
            + " | ".join(
                [
                    str(number),
                    str(kept_question_images),
                    str(removed_question_images),
                    str(answer_images),
                    "yes" if question else "no",
                    "yes" if answer else "no",
                ]
            )
            + " |"
        )

    output_md.write_text("\n".join(md_parts), encoding="utf-8")
    write_jsonl(output_jsonl, rows)
    chunk_rows = []
    for row in rows:
        text = (
            f"## 练习{row['exercise_number']}\n\n"
            f"### 题目\n\n{row['question_text'] or '_题目区未解析到内容_'}\n\n"
            f"### 参考答案\n\n{row['answer_text'] or '_参考答案区未解析到内容_'}"
        )
        chunk_rows.append(
            {
                "chunk_id": row["exercise_id"],
                "lesson_title": f"练习{row['exercise_number']} 题目-参考答案对照",
                "page_hint": None,
                "text": text,
                "image_refs": image_refs(text),
                "metadata": {
                    "exercise_number": row["exercise_number"],
                    "question_images_kept": row["question_images_kept"],
                    "question_images_removed": row["question_images_removed"],
                    "answer_images": row["answer_images"],
                    "has_question": row["has_question"],
                    "has_answer": row["has_answer"],
                },
            }
        )
    output_chunks.write_text(json.dumps(chunk_rows, ensure_ascii=False, indent=2), encoding="utf-8")
    report_md.write_text("\n".join(report_rows) + "\n", encoding="utf-8")

    return {
        "exercises": len(rows),
        "questions": len(question_sections),
        "answers": len(answer_sections),
        "question_images_kept": sum(int(row["question_images_kept"]) for row in rows),
        "question_images_removed": sum(int(row["question_images_removed"]) for row in rows),
        "answer_images": sum(int(row["answer_images"]) for row in rows),
        "output_md": rel_to_root(output_md),
        "output_jsonl": rel_to_root(output_jsonl),
        "chunks_json": rel_to_root(output_chunks),
        "report_md": rel_to_root(report_md),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build exercise-answer aligned chunks for Fretboard Workbook.")
    parser.add_argument("--source-md", type=Path, default=DEFAULT_SOURCE_MD)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    summary = build(args.source_md, args.output_dir)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
