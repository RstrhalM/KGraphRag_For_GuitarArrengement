#!/usr/bin/env python
"""Build a Markdown queue for chunks that likely need visual reprocessing."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


IMAGE_RE = re.compile(r"\[IMAGE_BLOCK:([^\]]+)\]")
VISUAL_HINT_RE = re.compile(r"(图示|如下图|上图|下图|右边|左边|下面|上面|谱例|指板图|练习\d+|画出|写出|构建)")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def image_page_map(content_list_path: Path) -> dict[str, int]:
    mapping: dict[str, int] = {}
    for item in read_json(content_list_path):
        if not isinstance(item, dict):
            continue
        img_path = item.get("img_path")
        page_idx = item.get("page_idx")
        if img_path and isinstance(page_idx, int):
            mapping[str(img_path).replace("\\", "/")] = page_idx
    return mapping


def chunk_reports(report_path: Path) -> dict[str, dict[str, Any]]:
    report = read_json(report_path)
    rows = report.get("chunk_reports", [])
    if not isinstance(rows, list):
        rows = []
    return {str(row.get("chunk_id")): row for row in rows if isinstance(row, dict)}


def visual_snippets(text: str, max_snippets: int, max_chars: int) -> list[str]:
    lines = text.splitlines()
    snippets: list[str] = []
    for index, line in enumerate(lines):
        if IMAGE_RE.search(line) or VISUAL_HINT_RE.search(line):
            start = max(0, index - 2)
            end = min(len(lines), index + 5)
            snippet = "\n".join(x for x in lines[start:end]).strip()
            snippet = re.sub(r"\n{3,}", "\n\n", snippet)
            if len(snippet) > max_chars:
                snippet = snippet[:max_chars].rstrip() + "..."
            if snippet and snippet not in snippets:
                snippets.append(snippet)
            if len(snippets) >= max_snippets:
                break
    return snippets


def load_extract_dir(path: Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    chunks = read_json(path / "chunks.json")
    reports = chunk_reports(path / "arrangement_kg_report.json")
    if not isinstance(chunks, list):
        chunks = []
    return chunks, reports


def render_queue(
    extract_dirs: list[Path],
    image_pages: dict[str, int],
    min_missing: int,
    min_images: int,
) -> str:
    lines = [
        "# Visual Reprocess Queue",
        "",
        "说明：PDF 页码按 MinerU 的 `page_idx + 1` 计算，方便定位原始扫描页。",
        "优先级：`missing_visual_context > 0` 的 chunk 优先；图多但未缺图的 chunk 作为备选。",
        "",
    ]

    total = 0
    for extract_dir in extract_dirs:
        chunks, reports = load_extract_dir(extract_dir)
        selected: list[tuple[dict[str, Any], dict[str, Any], str]] = []
        for chunk in chunks:
            chunk_id = str(chunk.get("chunk_id", ""))
            report = reports.get(chunk_id, {})
            missing = int((report.get("discarded_summary") or {}).get("missing_visual_context", 0) or 0)
            image_refs = chunk.get("image_refs", [])
            if not isinstance(image_refs, list):
                image_refs = []
            reason = ""
            if missing >= min_missing and missing > 0:
                reason = f"missing_visual_context={missing}"
            elif len(image_refs) >= min_images:
                reason = f"image_refs={len(image_refs)}"
            if reason:
                selected.append((chunk, report, reason))

        if not selected:
            continue

        lines.extend([f"## {extract_dir.name}", ""])
        for chunk, report, reason in selected:
            total += 1
            chunk_id = str(chunk.get("chunk_id", ""))
            image_refs = [str(x).replace("\\", "/") for x in (chunk.get("image_refs", []) or [])]
            page_numbers = sorted({image_pages[x] + 1 for x in image_refs if x in image_pages})
            missing = int((report.get("discarded_summary") or {}).get("missing_visual_context", 0) or 0)
            lines.extend(
                [
                    f"### {chunk_id}",
                    "",
                    f"- 触发原因：`{reason}`",
                    f"- missing_visual_context：`{missing}`",
                    f"- 图片引用数：`{len(image_refs)}`",
                    f"- 可能 PDF 页码：`{', '.join(str(x) for x in page_numbers) if page_numbers else 'unknown'}`",
                    f"- 建议补跑：优先把上述页码对应的单页 PDF/页面截图作为图片输入；若跨多页，先按页拆开补跑。",
                    "",
                    "**涉及文本片段**",
                    "",
                ]
            )
            for snippet in visual_snippets(str(chunk.get("text", "")), max_snippets=8, max_chars=700):
                lines.append("```text")
                lines.append(snippet)
                lines.append("```")
                lines.append("")
            lines.extend(["**前 12 个图片引用**", ""])
            for image_ref in image_refs[:12]:
                page = image_pages.get(image_ref)
                page_label = f"page {page + 1}" if page is not None else "page unknown"
                lines.append(f"- `{image_ref}` ({page_label})")
            lines.append("")

    lines.insert(4, f"- 队列条目数：{total}")
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content-list", type=Path, required=True, help="MinerU *_content_list.json")
    parser.add_argument("--extract-dir", type=Path, action="append", required=True, help="KG extract output dir")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output Markdown path")
    parser.add_argument("--min-missing", type=int, default=1)
    parser.add_argument("--min-images", type=int, default=60, help="Also list image-heavy chunks")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pages = image_page_map(args.content_list)
    md = render_queue(args.extract_dir, pages, args.min_missing, args.min_images)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(md, encoding="utf-8", newline="\n")
    print(f"Wrote visual queue to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
