from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw

from run_fretboard_answer_bbox_tasks import ROOT, TASK_QUEUE, load_queue, rel_path, workspace_path


DEFAULT_OUTPUT_ROOT = ROOT / "data" / "processed" / "fretboard_handbook" / "bbox_tasks"


def merge_ranges(ranges: list[tuple[int, int]], max_gap: int) -> list[tuple[int, int]]:
    if not ranges:
        return []
    merged = [ranges[0]]
    for start, end in ranges[1:]:
        last_start, last_end = merged[-1]
        if start - last_end <= max_gap:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def projection_ranges(values: np.ndarray, threshold: float, max_gap: int, min_size: int) -> list[tuple[int, int]]:
    indexes = np.where(values > threshold)[0]
    if len(indexes) == 0:
        return []
    raw: list[tuple[int, int]] = []
    start = prev = int(indexes[0])
    for raw_index in indexes[1:]:
        index = int(raw_index)
        if index - prev > 1:
            raw.append((start, prev + 1))
            start = index
        prev = index
    raw.append((start, prev + 1))
    return [(start, end) for start, end in merge_ranges(raw, max_gap) if end - start >= min_size]


def expand_box(box: tuple[int, int, int, int], width: int, height: int, pad_x: int = 10, pad_y: int = 8) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = box
    return (
        max(0, x1 - pad_x),
        max(0, y1 - pad_y),
        min(width, x2 + pad_x),
        min(height, y2 + pad_y),
    )


def overlap_ratio(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    if ix2 <= ix1 or iy2 <= iy1:
        return 0.0
    inter = (ix2 - ix1) * (iy2 - iy1)
    area = min((ax2 - ax1) * (ay2 - ay1), (bx2 - bx1) * (by2 - by1))
    return inter / max(1, area)


def dedupe_boxes(boxes: list[tuple[int, int, int, int]]) -> list[tuple[int, int, int, int]]:
    ordered = sorted(boxes, key=lambda box: ((box[1] // 80), box[0], box[1]))
    kept: list[tuple[int, int, int, int]] = []
    for box in ordered:
        if any(overlap_ratio(box, old) > 0.75 for old in kept):
            continue
        kept.append(box)
    return kept


def classify_block(box: tuple[int, int, int, int], dark_pixels: int) -> str:
    x1, y1, x2, y2 = box
    w = x2 - x1
    h = y2 - y1
    if w >= 220 and h >= 35:
        return "diagram_candidate"
    if w >= 38 and h >= 70 and dark_pixels >= 180:
        return "diagram_candidate"
    if dark_pixels > 1000 and w >= 100:
        return "text_or_mixed_candidate"
    return "small_label_or_noise"


def segment_image(image_path: Path) -> list[dict[str, Any]]:
    image = Image.open(image_path).convert("L")
    arr = np.array(image)
    height, width = arr.shape
    # Keep faint printed grid lines while dropping paper background.
    dark = arr < 218
    # Ignore tiny page-border noise by using projection thresholds.
    col_values = dark.sum(axis=0)
    column_threshold = max(12, height * 0.012)
    columns = projection_ranges(
        col_values,
        threshold=column_threshold,
        max_gap=max(18, width // 45),
        min_size=max(32, width // 35),
    )
    if not columns:
        columns = [(0, width)]

    boxes: list[tuple[int, int, int, int]] = []
    for col_x1, col_x2 in columns:
        column_mask = dark[:, col_x1:col_x2]
        row_values = column_mask.sum(axis=1)
        row_threshold = max(10, (col_x2 - col_x1) * 0.018)
        rows = projection_ranges(
            row_values,
            threshold=row_threshold,
            max_gap=max(10, height // 95),
            min_size=14,
        )
        for row_y1, row_y2 in rows:
            # Re-split horizontally inside each row. This handles rows that contain
            # multiple adjacent answer diagrams.
            row_mask = dark[row_y1:row_y2, col_x1:col_x2]
            inner_values = row_mask.sum(axis=0)
            inner_threshold = max(3, (row_y2 - row_y1) * 0.055)
            inner_columns = projection_ranges(
                inner_values,
                threshold=inner_threshold,
                max_gap=max(14, width // 70),
                min_size=28,
            )
            if not inner_columns:
                inner_columns = [(0, col_x2 - col_x1)]
            for ix1, ix2 in inner_columns:
                box = expand_box((col_x1 + ix1, row_y1, col_x1 + ix2, row_y2), width, height)
                x1, y1, x2, y2 = box
                if x2 - x1 < 32 or y2 - y1 < 18:
                    continue
                local_dark = int(dark[y1:y2, x1:x2].sum())
                if local_dark < 60:
                    continue
                boxes.append(box)

    boxes = dedupe_boxes(boxes)
    blocks: list[dict[str, Any]] = []
    for index, box in enumerate(boxes, start=1):
        x1, y1, x2, y2 = box
        dark_pixels = int(dark[y1:y2, x1:x2].sum())
        block_type = classify_block(box, dark_pixels)
        if block_type == "small_label_or_noise":
            continue
        blocks.append(
            {
                "block_id": f"block_{index:03d}",
                "order_index": index,
                "bbox": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                "width": x2 - x1,
                "height": y2 - y1,
                "dark_pixels": dark_pixels,
                "block_type": block_type,
                "review_status": "pending",
                "exercise_number": None,
                "subquestion_number": None,
                "part_index": 1,
                "notes": "",
            }
        )
    if not blocks:
        blocks.append(
            {
                "block_id": "block_001",
                "order_index": 1,
                "bbox": {"x1": 0, "y1": 0, "x2": width, "y2": height},
                "width": width,
                "height": height,
                "dark_pixels": int(dark.sum()),
                "block_type": "full_image_fallback",
                "review_status": "pending",
                "exercise_number": None,
                "subquestion_number": None,
                "part_index": 1,
                "notes": "Fallback because local segmentation found no confident blocks.",
            }
        )
    return blocks


def draw_and_crop(image_path: Path, blocks: list[dict[str, Any]], output_dir: Path) -> None:
    image = Image.open(image_path).convert("RGB")
    annotated = image.copy()
    draw = ImageDraw.Draw(annotated)
    crop_dir = output_dir / "crops"
    crop_dir.mkdir(parents=True, exist_ok=True)
    for index, block in enumerate(blocks, start=1):
        bbox = block["bbox"]
        box = (bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"])
        color = (220, 40, 40) if block.get("block_type") == "diagram_candidate" else (40, 90, 220)
        draw.rectangle(box, outline=color, width=3)
        label = str(block["block_id"])
        label_box = (box[0], max(0, box[1] - 18), box[0] + 82, box[1])
        draw.rectangle(label_box, fill=color)
        draw.text((label_box[0] + 4, label_box[1] + 2), label, fill=(255, 255, 255))
        crop_name = f"{block['block_id']}.png"
        image.crop(box).save(crop_dir / crop_name)
        block["crop_path"] = str((crop_dir / crop_name).relative_to(output_dir)).replace("\\", "/")
    annotated.save(output_dir / "annotated_local_segments.png")


def render_review(task: dict[str, Any], image_path: Path, output_dir: Path, blocks: list[dict[str, Any]]) -> None:
    exercises = ", ".join(str(x) for x in task.get("exercises", [])) or "-"
    lines = [
        "# 本地答案图分块审核",
        "",
        f"- task_id: `{task.get('task_id')}`",
        f"- source_image: `{rel_path(image_path)}`",
        f"- exercises_hint: `{exercises}`",
        f"- segments_json: `segments.json`",
        f"- annotated_image: `annotated_local_segments.png`",
        "",
        "## 标注总览",
        "",
        "![](annotated_local_segments.png)",
        "",
        "## 候选分块",
        "",
        "说明：请把要保留的候选块改成 `[x]`；必要时在表格里填写 exercise/subquestion/part/notes。当前 exercise/subquestion 为空，避免自动误标。",
        "",
        "| accept | block | type | exercise | subquestion | part | bbox | crop | notes |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for block in blocks:
        bbox = block["bbox"]
        lines.append(
            "| [ ] | "
            + f"`{block['block_id']}`"
            + " | "
            + str(block.get("block_type") or "")
            + " |  |  | "
            + str(block.get("part_index") or 1)
            + " | "
            + f"{bbox['x1']},{bbox['y1']},{bbox['x2']},{bbox['y2']}"
            + " | "
            + f"![]({block.get('crop_path')})"
            + " |  |"
        )
    (output_dir / "local_segment_review.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def process_task(task: dict[str, Any]) -> dict[str, Any]:
    image_path = workspace_path(str(task["image_path"]))
    output_dir = workspace_path(str(task.get("output_dir") or DEFAULT_OUTPUT_ROOT / str(task["task_id"]))) / "local_segments"
    output_dir.mkdir(parents=True, exist_ok=True)
    blocks = segment_image(image_path)
    draw_and_crop(image_path, blocks, output_dir)
    (output_dir / "segments.json").write_text(json.dumps({"task": task, "blocks": blocks}, ensure_ascii=False, indent=2), encoding="utf-8")
    render_review(task, image_path, output_dir, blocks)
    return {
        "task_id": task.get("task_id"),
        "image_name": task.get("image_name"),
        "blocks": len(blocks),
        "output_dir": rel_path(output_dir),
        "review_md": rel_path(output_dir / "local_segment_review.md"),
        "annotated_image": rel_path(output_dir / "annotated_local_segments.png"),
    }


def render_batch_report(rows: list[dict[str, Any]], output_root: Path) -> None:
    lines = [
        "# 指板手册答案图本地分块报告",
        "",
        "| task_id | image | blocks | review | annotated |",
        "| --- | --- | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['task_id']}` | `{row['image_name']}` | {row['blocks']} | "
            f"`{row['review_md']}` | `{row['annotated_image']}` |"
        )
    (output_root / "local_segment_batch_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Locally segment fretboard answer images into reviewable candidate blocks.")
    parser.add_argument("--queue", type=Path, default=TASK_QUEUE)
    parser.add_argument("--task-id")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    args = parser.parse_args()

    queue = load_queue(args.queue)
    if args.task_id:
        queue = [row for row in queue if row.get("task_id") == args.task_id]
        if not queue:
            raise SystemExit(f"Task not found: {args.task_id}")

    summaries = [process_task(task) for task in queue]
    output_root = args.output_root if args.output_root.is_absolute() else ROOT / args.output_root
    render_batch_report(summaries, output_root)
    print(json.dumps({"tasks": len(summaries), "blocks": sum(row["blocks"] for row in summaries), "report": rel_path(output_root / "local_segment_batch_report.md")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
