import argparse
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_FULL_PAGE_RANGES = "33-40,48-57,59-62,64-68,72-78"


def parse_page_ranges(value: str) -> set[int]:
    pages: set[int] = set()
    for part in re.split(r"[,，]\s*", value.strip()):
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            pages.update(range(int(start), int(end) + 1))
        else:
            pages.add(int(part))
    return pages


def page_ranges(pages: list[int]) -> str:
    if not pages:
        return ""
    ranges: list[str] = []
    start = prev = pages[0]
    for page in pages[1:]:
        if page == prev + 1:
            prev = page
            continue
        ranges.append(f"{start}" if start == prev else f"{start}-{prev}")
        start = prev = page
    ranges.append(f"{start}" if start == prev else f"{start}-{prev}")
    return ", ".join(ranges)


def compact(text: str, limit: int = 160) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text[: limit - 1] + "..." if len(text) > limit else text


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def select_pages(
    rows: list[dict[str, Any]],
    include_pages: set[int],
    exclude_pages: set[int],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    density_by_page = {int(row["page"]): row for row in rows}
    full_pages: set[int] = set(include_pages)

    for row in rows:
        page = int(row["page"])
        chars = int(row.get("chars") or 0)
        images = int(row.get("images") or 0)
        if images >= 6:
            full_pages.add(page)
        elif images >= 3 and chars < 450:
            full_pages.add(page)
        elif images >= 2 and chars < 350:
            full_pages.add(page)

    full_pages -= exclude_pages
    selected = [density_by_page[p] for p in sorted(full_pages) if p in density_by_page]

    manual: list[dict[str, Any]] = []
    for row in rows:
        page = int(row["page"])
        chars = int(row.get("chars") or 0)
        images = int(row.get("images") or 0)
        if page in full_pages or page in exclude_pages:
            continue
        if images >= 2:
            manual.append(
                {
                    **row,
                    "reason": "含多张练习/谱例/图示，整页优先级不高；如小图切分不准再人工局部截图。",
                }
            )
        elif images == 1 and chars < 500:
            manual.append(
                {
                    **row,
                    "reason": "单图低文本页，建议后续抽取时检查 MinerU 小图是否完整。",
                }
            )
    return selected, manual


def render_pages(pdf_path: Path, selected: list[dict[str, Any]], output_dir: Path, dpi: int) -> list[dict[str, Any]]:
    try:
        import pypdfium2 as pdfium
    except ImportError as exc:
        raise RuntimeError("Missing dependency: pypdfium2 is required to render PDF pages.") from exc

    output_dir.mkdir(parents=True, exist_ok=True)
    pdf = pdfium.PdfDocument(str(pdf_path))
    scale = dpi / 72.0
    manifest: list[dict[str, Any]] = []
    try:
        for row in selected:
            page_num = int(row["page"])
            page = pdf[page_num - 1]
            bitmap = page.render(scale=scale)
            image = bitmap.to_pil()
            out_file = output_dir / f"mathrock_pdf_page_{page_num:03d}.jpg"
            image.save(out_file, "JPEG", quality=92, optimize=True)
            manifest.append(
                {
                    "page": page_num,
                    "image_path": str(out_file),
                    "dpi": dpi,
                    "chars": int(row.get("chars") or 0),
                    "images": int(row.get("images") or 0),
                    "sample": compact(str(row.get("sample") or ""), 220),
                    "reason": full_page_reason(row),
                }
            )
    finally:
        pdf.close()
    return manifest


def full_page_reason(row: dict[str, Any]) -> str:
    page = int(row["page"])
    chars = int(row.get("chars") or 0)
    images = int(row.get("images") or 0)
    if 33 <= page <= 40:
        return "特殊调弦/指型/音阶密集页，整页保留上下文。"
    if 48 <= page <= 68:
        return "和弦 voicing/和弦进行密集页，整页布局信息重要。"
    if 72 <= page <= 78:
        return "琶音/riff/节拍谱例密集页，整页适合作视觉证据。"
    if images >= 6:
        return "图片数量高，局部图之间关系依赖整页布局。"
    if chars < 350:
        return "OCR 文本少，主要信息在图像中。"
    return "自动规则判定适合整页图。"


def write_reports(
    manifest: list[dict[str, Any]],
    manual: list[dict[str, Any]],
    output_dir: Path,
    manifest_jsonl: Path,
    report_md: Path,
) -> None:
    manifest_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with manifest_jsonl.open("w", encoding="utf-8", newline="\n") as fh:
        for row in manifest:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    full_pages = [row["page"] for row in manifest]
    manual_pages = [int(row["page"]) for row in manual]
    lines = [
        "# Math Rock PDF 整页图自动生成清单",
        "",
        "用途：把适合整页理解的谱例/和弦图/指板图页面预先转成图片，剩余页面再由人工按需局部截图。",
        "",
        "## 输出",
        "",
        f"- 整页图目录：`{output_dir}`",
        f"- 整页图 manifest：`{manifest_jsonl}`",
        f"- 已生成整页图：{len(manifest)} 页",
        f"- 页码：P{page_ranges(full_pages)}",
        "",
        "## 已转整页图",
        "",
        "| PDF 页 | 图片 | 原因 | OCR 样本 |",
        "| ---: | --- | --- | --- |",
    ]
    for row in manifest:
        lines.append(
            f"| P{row['page']} | `{row['image_path']}` | {row['reason']} | {compact(row.get('sample', ''), 120)} |"
        )

    lines.extend(
        [
            "",
            "## 仍建议人工按需局部截图",
            "",
            f"- 候选页：P{page_ranges(manual_pages)}",
            "- 这些页通常已有 MinerU 小图，或正文足够；只有在后续审核发现小图切分不完整时，再手工补局部截图。",
            "",
            "| PDF 页 | 字符 | 图片 | 原因 | OCR 样本 |",
            "| ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in manual:
        lines.append(
            f"| P{row['page']} | {row.get('chars', 0)} | {row.get('images', 0)} | {row['reason']} | "
            f"{compact(str(row.get('sample') or ''), 140)} |"
        )
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--density-json", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--manifest-jsonl", required=True, type=Path)
    parser.add_argument("--report-md", required=True, type=Path)
    parser.add_argument("--dpi", type=int, default=180)
    parser.add_argument("--include-pages", default=DEFAULT_FULL_PAGE_RANGES)
    parser.add_argument("--exclude-pages", default="")
    args = parser.parse_args()

    rows = load_json(args.density_json)
    selected, manual = select_pages(
        rows,
        parse_page_ranges(args.include_pages),
        parse_page_ranges(args.exclude_pages),
    )
    manifest = render_pages(args.pdf, selected, args.output_dir, args.dpi)
    write_reports(manifest, manual, args.output_dir, args.manifest_jsonl, args.report_md)
    print(f"rendered={len(manifest)} pages=P{page_ranges([row['page'] for row in manifest])}")
    print(f"manual_candidates={len(manual)} pages=P{page_ranges([int(row['page']) for row in manual])}")
    print(args.report_md)


if __name__ == "__main__":
    main()
