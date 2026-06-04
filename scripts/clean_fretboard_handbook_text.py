from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = (
    ROOT
    / "data"
    / "processed"
    / "mineru_full_gpu"
    / "吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)"
    / "ocr"
    / "吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org).md"
)
DEFAULT_OUTPUT_DIR = ROOT / "data" / "processed" / "fretboard_handbook" / "text_clean"

IMAGE_RE = re.compile(r"!\[\]\((images/[^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s*(.+?)\s*$")
CHAPTER_RE = re.compile(r"第\s*(\d+)\s*章\s*(.+)")
EXERCISE_RE = re.compile(r"练习\s*(\d+)")
STANDALONE_PAGE_RE = re.compile(r"^\d{1,3}$")

CHAPTER_START_PAGES = {
    "引言": 4,
    "第1章": 6,
    "第2章": 8,
    "第3章": 12,
    "第4章": 15,
    "第5章": 17,
    "第6章": 20,
    "第7章": 23,
    "第8章": 26,
    "第9章": 29,
    "第10章": 33,
    "第11章": 37,
    "第12章": 39,
    "第13章": 41,
    "第14章": 44,
    "第15章": 48,
    "第16章": 51,
    "第17章": 54,
    "第18章": 58,
    "第19章": 59,
    "第20章": 63,
    "第21章": 65,
    "第22章": 67,
    "练习答案": 68,
    "关于作者": 79,
    "致谢": 80,
}


@dataclass
class Block:
    title: str
    chunk_type: str
    chapter: str
    page_hint: str = ""
    exercise_number: int | None = None
    lines: list[str] = field(default_factory=list)
    image_refs: list[str] = field(default_factory=list)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def normalize_line(line: str) -> str:
    line = line.strip()
    line = line.replace("\u3000", " ")
    line = re.sub(r"[ \t]+", " ", line)
    line = line.replace("．", ".")
    return line


def normalize_heading_text(text: str) -> str:
    text = normalize_line(text)
    text = text.replace("引 言", "引言")
    text = re.sub(r"第(\d+)章([^\s])", r"第\1章 \2", text)
    text = re.sub(r"(第\d+章)\s*[：:]\s*", r"\1 ", text)
    return text


def find_content_start(lines: list[str]) -> int:
    for index, line in enumerate(lines):
        normalized = normalize_heading_text(line.lstrip("# ").strip())
        if normalized == "引言" and line.lstrip().startswith("#"):
            return index
    for index, line in enumerate(lines):
        if "学习用吉他演奏一首歌曲" in line:
            return index
    return 0


def chapter_key(title: str) -> str:
    normalized = normalize_heading_text(title)
    if normalized == "引言":
        return "引言"
    if normalized.startswith("练习答案"):
        return "练习答案"
    if normalized.startswith("关于作者"):
        return "关于作者"
    if normalized.startswith("致谢"):
        return "致谢"
    match = CHAPTER_RE.search(normalized)
    if match:
        return f"第{int(match.group(1))}章"
    return ""


def classify_heading(title: str, current_chapter: str) -> tuple[str, str, int | None, str]:
    normalized = normalize_heading_text(title)
    key = chapter_key(normalized)
    if key:
        if key == "引言":
            return "chapter_intro", "引言", None, str(CHAPTER_START_PAGES.get(key, ""))
        if key == "练习答案":
            return "answer_text", "练习答案", None, str(CHAPTER_START_PAGES.get(key, ""))
        if key in {"关于作者", "致谢"}:
            return "appendix", key, None, str(CHAPTER_START_PAGES.get(key, ""))
        return "chapter_intro", normalized, None, str(CHAPTER_START_PAGES.get(key, ""))

    exercise = EXERCISE_RE.search(normalized)
    if exercise:
        number = int(exercise.group(1))
        chunk_type = "answer_text" if current_chapter.startswith("练习答案") else "exercise_prompt"
        return chunk_type, current_chapter, number, ""

    if "学习目标" in normalized:
        return "lesson_goal", current_chapter, None, ""
    return "concept", current_chapter, None, ""


def should_drop_line(line: str) -> bool:
    if not line:
        return True
    if STANDALONE_PAGE_RE.fullmatch(line):
        return True
    noisy = (
        "人民音乐出版社出版发行",
        "中国版本图书馆CIP",
        "版权所有翻版必究",
        "新华书店北京发行所经销",
        "Http://www.rymusic.com.cn",
        "E-mail:",
    )
    return any(token in line for token in noisy)


def split_long_text(text: str, max_chars: int) -> list[str]:
    paragraphs = [part.strip() for part in re.split(r"\n{2,}", text) if part.strip()]
    pieces: list[str] = []
    current: list[str] = []
    current_len = 0
    for paragraph in paragraphs:
        extra = len(paragraph) + (2 if current else 0)
        if current and current_len + extra > max_chars:
            pieces.append("\n\n".join(current))
            current = []
            current_len = 0
        if len(paragraph) > max_chars:
            if current:
                pieces.append("\n\n".join(current))
                current = []
                current_len = 0
            for start in range(0, len(paragraph), max_chars):
                pieces.append(paragraph[start : start + max_chars])
            continue
        current.append(paragraph)
        current_len += extra
    if current:
        pieces.append("\n\n".join(current))
    return pieces


def block_to_chunks(block: Block, index_start: int, max_chars: int, raw_path: Path) -> list[dict[str, Any]]:
    meaningful_lines = [line for line in block.lines if line.strip() and not line.strip().startswith("## ")]
    if block.chunk_type == "answer_text" and not meaningful_lines:
        return []
    if not meaningful_lines and not block.image_refs:
        return []

    body = "\n".join(line for line in block.lines if line.strip()).strip()
    if not body and not block.image_refs:
        return []

    text = body
    if block.image_refs:
        marker = f"[图示引用 {len(block.image_refs)} 张，详见 image_refs]"
        text = f"{text}\n\n{marker}".strip()

    pieces = split_long_text(text, max_chars)
    rows: list[dict[str, Any]] = []
    for offset, piece in enumerate(pieces, start=1):
        suffix = "" if len(pieces) == 1 else f"_part{offset:02d}"
        rows.append(
            {
                "chunk_id": f"fretboard_text_{index_start + len(rows):04d}{suffix}",
                "source_id": "fretboard_handbook_clean_text",
                "source_title": "吉他指板手册",
                "source_type": "clean_markdown",
                "raw_path": rel(raw_path),
                "chapter": block.chapter,
                "title": block.title,
                "chunk_type": block.chunk_type,
                "exercise_number": block.exercise_number,
                "page_hint": block.page_hint,
                "style_tags": ["fretboard", "guitar_foundation"],
                "image_refs": block.image_refs,
                "linked_visual_collection": (
                    "guitar_fretboard_answer_captions_qwen3_06b"
                    if block.chunk_type in {"exercise_prompt", "answer_text"}
                    else ""
                ),
                "text": piece,
            }
        )
    return rows


def build_blocks(source_text: str, source_dir: Path) -> list[Block]:
    lines = source_text.splitlines()
    start = find_content_start(lines)
    current_chapter = "引言"
    current = Block(title="引言", chunk_type="chapter_intro", chapter="引言", page_hint="4")
    blocks: list[Block] = []

    def flush() -> None:
        nonlocal current
        if current.lines or current.image_refs:
            blocks.append(current)

    for raw_line in lines[start:]:
        image_match = IMAGE_RE.search(raw_line.strip())
        if image_match:
            image_path = source_dir / image_match.group(1)
            current.image_refs.append(rel(image_path))
            continue

        line = normalize_line(raw_line)
        if should_drop_line(line):
            continue

        heading = HEADING_RE.match(line)
        if heading:
            title = normalize_heading_text(heading.group(2))
            flush()
            chunk_type, maybe_chapter, exercise_number, page_hint = classify_heading(title, current_chapter)
            if chunk_type == "chapter_intro" or maybe_chapter in {"练习答案", "关于作者", "致谢"} or CHAPTER_RE.search(title):
                current_chapter = maybe_chapter or current_chapter
            current = Block(
                title=title,
                chunk_type=chunk_type,
                chapter=current_chapter,
                page_hint=page_hint or str(CHAPTER_START_PAGES.get(chapter_key(current_chapter), "")),
                exercise_number=exercise_number,
                lines=[f"## {title}"],
            )
            continue

        if re.fullmatch(r"练习\s*\d+", line):
            title = normalize_heading_text(line)
            flush()
            chunk_type, maybe_chapter, exercise_number, page_hint = classify_heading(title, current_chapter)
            current = Block(
                title=title,
                chunk_type=chunk_type,
                chapter=maybe_chapter or current_chapter,
                page_hint=page_hint or str(CHAPTER_START_PAGES.get(chapter_key(current_chapter), "")),
                exercise_number=exercise_number,
                lines=[f"## {title}"],
            )
            continue

        if line.startswith("学习目标"):
            flush()
            current = Block(
                title=f"{current_chapter} 学习目标",
                chunk_type="lesson_goal",
                chapter=current_chapter,
                page_hint=str(CHAPTER_START_PAGES.get(chapter_key(current_chapter), "")),
                lines=[line],
            )
            continue

        current.lines.append(line)

    flush()
    return blocks


def write_clean_markdown(path: Path, chunks: list[dict[str, Any]]) -> None:
    lines = ["# 吉他指板手册 Clean Text", ""]
    last_chapter = None
    for chunk in chunks:
        if chunk["chapter"] != last_chapter:
            lines.append(f"# {chunk['chapter']}")
            lines.append("")
            last_chapter = chunk["chapter"]
        lines.append(f"## {chunk['chunk_id']} | {chunk['chunk_type']} | {chunk['title']}")
        if chunk.get("exercise_number"):
            lines.append(f"- exercise_number: {chunk['exercise_number']}")
        if chunk.get("page_hint"):
            lines.append(f"- page_hint: {chunk['page_hint']}")
        if chunk.get("image_refs"):
            lines.append(f"- image_refs: {len(chunk['image_refs'])}")
        lines.append("")
        lines.append(chunk["text"])
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def review_sample(chunks: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    if limit <= 0:
        return []
    selected: list[dict[str, Any]] = []
    seen: set[str] = set()

    def add(rows: list[dict[str, Any]], count: int) -> None:
        for row in rows:
            if len(selected) >= limit or count <= 0:
                return
            chunk_id = str(row.get("chunk_id", ""))
            if chunk_id in seen:
                continue
            selected.append(row)
            seen.add(chunk_id)
            count -= 1

    add(chunks, min(10, limit))
    add([row for row in chunks if row.get("chunk_type") == "exercise_prompt"], 4)
    add([row for row in chunks if row.get("chunk_type") == "answer_text"], 4)
    add([row for row in chunks if str(row.get("chapter", "")).startswith(("第13章", "第14章", "第15章", "第16章"))], 4)
    add(chunks, limit - len(selected))
    return selected[:limit]


def write_review(path: Path, chunks: list[dict[str, Any]], limit: int) -> None:
    sample = review_sample(chunks, limit)
    lines = [
        "# 指板手册正文清洗分块审核",
        "",
        "说明：这是 dry-run 代表性样本，混合了开头正文、练习题干、练习答案和中后段和弦/琶音章节。请重点看正文是否被误删、练习题是否混入答案、音名/和弦/指型号是否被改坏。",
        "",
    ]
    for chunk in sample:
        lines.append(f"## {chunk['chunk_id']} | {chunk['chunk_type']} | {chunk['title']}")
        lines.append("- [ ] accept")
        lines.append("- [ ] revise")
        lines.append("- [ ] reject")
        lines.append(f"- chapter: {chunk['chapter']}")
        lines.append(f"- page_hint: {chunk.get('page_hint') or ''}")
        if chunk.get("exercise_number"):
            lines.append(f"- exercise_number: {chunk['exercise_number']}")
        lines.append(f"- image_refs: {len(chunk.get('image_refs') or [])}")
        lines.append("")
        lines.append("```text")
        lines.append(chunk["text"][:2500])
        if len(chunk["text"]) > 2500:
            lines.append("... [truncated for review]")
        lines.append("```")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean and structurally chunk Fretboard Handbook Markdown.")
    parser.add_argument("--input", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-chars", type=int, default=1800)
    parser.add_argument("--review-limit", type=int, default=20)
    args = parser.parse_args()

    source_text = args.input.read_text(encoding="utf-8")
    blocks = build_blocks(source_text, args.input.parent)
    chunks: list[dict[str, Any]] = []
    next_index = 1
    for block in blocks:
        block_chunks = block_to_chunks(block, next_index, args.max_chars, args.input)
        chunks.extend(block_chunks)
        next_index += len(block_chunks)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = args.output_dir / "fretboard_handbook_clean_chunks.jsonl"
    json_path = args.output_dir / "chunks.json"
    clean_md_path = args.output_dir / "fretboard_handbook_clean.md"
    review_path = args.output_dir / "fretboard_text_clean_review.md"
    report_md_path = args.output_dir / "fretboard_text_clean_report.md"
    report_json_path = args.output_dir / "fretboard_text_clean_report.json"

    jsonl_path.write_text(
        "\n".join(json.dumps(chunk, ensure_ascii=False) for chunk in chunks) + "\n",
        encoding="utf-8",
    )
    json_path.write_text(json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8")
    write_clean_markdown(clean_md_path, chunks)
    write_review(review_path, chunks, args.review_limit)

    type_counts: dict[str, int] = {}
    chapter_counts: dict[str, int] = {}
    for chunk in chunks:
        type_counts[chunk["chunk_type"]] = type_counts.get(chunk["chunk_type"], 0) + 1
        chapter_counts[chunk["chapter"]] = chapter_counts.get(chunk["chapter"], 0) + 1

    report = {
        "input": rel(args.input),
        "output_dir": rel(args.output_dir),
        "blocks": len(blocks),
        "chunks": len(chunks),
        "max_chars": args.max_chars,
        "type_counts": type_counts,
        "chapter_counts": chapter_counts,
        "review_path": rel(review_path),
        "chunks_json": rel(json_path),
        "chunks_jsonl": rel(jsonl_path),
        "clean_md": rel(clean_md_path),
    }
    report_json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# 指板手册正文清洗报告",
        "",
        f"- input: `{report['input']}`",
        f"- output_dir: `{report['output_dir']}`",
        f"- blocks: {len(blocks)}",
        f"- chunks: {len(chunks)}",
        f"- max_chars: {args.max_chars}",
        f"- review_path: `{report['review_path']}`",
        f"- chunks_json: `{report['chunks_json']}`",
        f"- chunks_jsonl: `{report['chunks_jsonl']}`",
        f"- clean_md: `{report['clean_md']}`",
        "",
        "## Chunk Types",
        "",
    ]
    for key, value in sorted(type_counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Chapters", ""])
    for key, value in chapter_counts.items():
        lines.append(f"- {key}: {value}")
    report_md_path.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
