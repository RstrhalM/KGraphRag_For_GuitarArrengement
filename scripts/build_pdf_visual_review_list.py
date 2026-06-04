import argparse
import json
import re
from pathlib import Path


def compact(text: str, limit: int = 180) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text[: limit - 1] + "..." if len(text) > limit else text


def page_ranges(pages: list[int]) -> str:
    if not pages:
        return ""
    ranges = []
    start = prev = pages[0]
    for page in pages[1:]:
        if page == prev + 1:
            prev = page
            continue
        ranges.append(f"{start}" if start == prev else f"{start}-{prev}")
        start = prev = page
    ranges.append(f"{start}" if start == prev else f"{start}-{prev}")
    return ", ".join(ranges)


def infer_focus(sample: str, section: str) -> str:
    text = f"{section} {sample}".lower()
    checks = [
        (["tapping", "点弦"], "点弦/双手点弦谱例"),
        (["finger picking", "指弹"], "指弹节奏与跨弦练习"),
        (["hybrid picking", "混合拨弦"], "混合拨弦/跳弦练习"),
        (["facgce", "daeac#e", "调弦"], "特殊调弦、和弦指型与音阶"),
        (["voicing", "chord shapes", "和弦指法", "和弦发声", "壳式"], "和弦 voicing/指法图"),
        (["progression", "和弦进行", "和弦进⾏", "借用和弦"], "和弦进行与替代方案"),
        (["arpeggio", "琶音"], "琶音指型与 riff"),
    ]
    for keys, label in checks:
        if any(key in text for key in keys):
            return label
    return "教材视觉证据"


def infer_action(chars: int, image_count: int, focus: str) -> str:
    if image_count >= 6 or chars < 350:
        return "优先整页或全页截图处理，MD 文本只能作上下文。"
    if "谱例" in focus or "练习" in focus or "riff" in focus:
        return "保留该页图片，并绑定前后 1-2 段文字。"
    return "可先用 MD 文本抽取，图片作为视觉证据补充。"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--density-json", required=True)
    parser.add_argument("--content-list", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    density = load_json(Path(args.density_json))
    content = load_json(Path(args.content_list))
    out_path = Path(args.output)

    page_items: dict[int, list[dict]] = {}
    for item in content:
        page = int(item.get("page_idx", -1)) + 1
        if page <= 0:
            continue
        page_items.setdefault(page, []).append(item)

    sections_by_page: dict[int, str] = {}
    current_section = ""
    for page in sorted(page_items):
        for item in page_items[page]:
            if item.get("type") == "text" and item.get("text_level") == 2:
                current_section = compact(item.get("text", ""), 80)
        sections_by_page[page] = current_section

    heavy_pages = [
        row["page"]
        for row in density
        if row.get("images", 0) >= 3 or (row.get("images", 0) >= 2 and row.get("chars", 0) < 650)
    ]
    low_text_pages = [
        row["page"]
        for row in density
        if row.get("images", 0) >= 1 and row.get("chars", 0) < 350
    ]

    lines = [
        "# Math Rock PDF 图片密集页对照清单",
        "",
        "用途：提前人工处理图片/谱例页，避免 KG 抽取流程中途等待补图。",
        "",
        "## 输入",
        "",
        "- 原 PDF：`data/book/Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans.pdf`",
        "- MinerU MD：`data/processed/mathrock/pdf_mineru/Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans/auto/Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans.md`",
        "- MinerU 图片目录：`data/processed/mathrock/pdf_mineru/Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans/auto/images`",
        "",
        "## 总览",
        "",
        f"- 图片密集页：P{page_ranges(heavy_pages)}",
        f"- 低文本视觉页：P{page_ranges(low_text_pages)}",
        "- 判定口径：图片数 >= 3，或图片数 >= 2 且 OCR 正文少于 650 字符。",
        "",
        "## 优先处理批次",
        "",
        "| 批次 | 页码 | 主要内容 | 建议 |",
        "| --- | --- | --- | --- |",
        "| A | P33-P40 | FACGCE / DAEAC#E 特殊调弦、和弦指型、音阶、创意 riff | 优先整页截图，适合直接进视觉库。 |",
        "| A | P48-P57, P59-P62, P64-P68 | 七/九/挂留/六和弦、壳式 voicing、和弦进行 | 优先整页截图，后续用于 voicing 与进行建议。 |",
        "| A | P72-P78 | 琶音指型、点弦/即兴 riff、非常规节拍例子 | 优先整页截图，适合做风格素材。 |",
        "| B | P5, P7-P8, P15 | 点弦姿势、点弦练习和开放和弦点弦 | 可整页，也可保留局部谱例图。 |",
        "| B | P18-P22, P25-P26 | 指弹、混合拨弦、跳弦练习 | 绑定前后正文，作为技法动作证据。 |",
        "| C | P45, P70 | 调号/八度定位等辅助图 | 可作为补充证据，优先级低于 A/B。 |",
        "",
        "## 逐页对照",
        "",
        "| PDF 页 | MD 章节/附近标题 | 字符 | 图片 | 重点 | 建议 | MD/OCR 样本 | 图片文件 |",
        "| ---: | --- | ---: | ---: | --- | --- | --- | --- |",
    ]

    density_by_page = {int(row["page"]): row for row in density}
    for page in heavy_pages:
        row = density_by_page[page]
        items = page_items.get(page, [])
        image_paths = [
            item.get("img_path")
            for item in items
            if item.get("type") in {"image", "table"} and item.get("img_path")
        ]
        section = sections_by_page.get(page, "")
        sample = compact(row.get("sample", ""), 160)
        focus = infer_focus(sample, section)
        action = infer_action(int(row.get("chars", 0)), int(row.get("images", 0)), focus)
        paths = "<br>".join(f"`{p}`" for p in image_paths[:8])
        if len(image_paths) > 8:
            paths += f"<br>... +{len(image_paths) - 8}"
        lines.append(
            f"| P{page} | {section or '-'} | {row.get('chars', 0)} | {row.get('images', 0)} | "
            f"{focus} | {action} | {sample} | {paths or '-'} |"
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out_path)
    print(f"heavy_pages={len(heavy_pages)} low_text_pages={len(low_text_pages)}")


if __name__ == "__main__":
    main()
