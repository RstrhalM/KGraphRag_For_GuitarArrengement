from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

from extract_arrangement_kg import apply_env_file, extract_json_object


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHUNKS = ROOT / "data" / "processed" / "fretboard_handbook" / "exercise_answer_aligned" / "chunks.json"
DEFAULT_IMAGE = ROOT / "data" / "练习解答（图片）" / "练习10-练习11.png"
DEFAULT_OUTPUT_DIR = ROOT / "data" / "processed" / "fretboard_handbook" / "bbox_trials" / "exercise_10_11"


SYSTEM_PROMPT = """你是一位吉他教材答案页版面分析助手。

你会看到：
1. 《吉他指板手册》中练习10、练习11的完整题目文本；
2. 一张同时包含练习10和练习11参考答案的整页图片。

任务：
把整页答案图片切分成“每个小题对应一张图”的 bbox。bbox 必须对应真实可裁剪的小图区域，而不是整道大题区域。

重要规则：
1. 坐标使用像素坐标，原点在图片左上角，x 向右，y 向下。
2. bbox 尽量紧贴每张指板图/答案图，但要保留题号、调名、品位标记等紧邻标签。
3. 练习10预期包含小题 1-10；练习11预期包含小题 1-10。若某小题在图中确实看不到，写到 missing_items。
4. 不要把相邻小题合并为一个 bbox；如果两个图靠得很近，也要拆开。
5. 若一个小题有多个必要图块，返回多个 bbox，并用 part_index 标识。
6. 不要识别具体答案对错，不要生成 caption，不要生成知识图谱。
7. 如果判断不确定，保留 bbox，但 confidence 降低，并在 notes 中说明。

输出严格 JSON 对象，不要 Markdown，不要代码块：
{
  "image_width": 1425,
  "image_height": 1239,
  "items": [
    {
      "exercise_number": 10,
      "subquestion_number": 1,
      "part_index": 1,
      "visible_label": "1 / F / VI",
      "bbox": {"x1": 0, "y1": 0, "x2": 100, "y2": 100},
      "confidence": 0.0,
      "notes": ""
    }
  ],
  "missing_items": [
    {"exercise_number": 10, "subquestion_number": 1, "reason": ""}
  ],
  "layout_notes": ""
}
"""


EX10_LABELS = {
    1: "F / VI",
    2: "F# / IV",
    3: "Bb / III",
    4: "G / V",
    5: "A / V",
    6: "Eb / IV",
    7: "C / VIII",
    8: "B / II",
    9: "Db / XI",
    10: "C / XV",
}

EX11_LABELS = {
    1: "G major scale",
    2: "A major scale",
    3: "Eb major scale",
    4: "B major scale",
    5: "Ab major scale",
    6: "D major scale",
    7: "Bb major scale",
    8: "E major scale",
    9: "F# major scale",
    10: "Db major scale",
}


def image_to_data_url(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(path.name)
    mime_type = mime_type or "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def read_chunks(path: Path) -> dict[int, dict[str, Any]]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    by_number: dict[int, dict[str, Any]] = {}
    for row in rows:
        meta = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        number = meta.get("exercise_number")
        if isinstance(number, int):
            by_number[number] = row
    return by_number


def question_only(chunk_text: str) -> str:
    marker = "### 参考答案"
    if marker in chunk_text:
        chunk_text = chunk_text.split(marker, 1)[0]
    return chunk_text.strip()


def call_vlm(image_path: Path, questions: dict[int, str], width: int, height: int) -> dict[str, Any]:
    base_url = os.environ.get("LLM_API_BASE_URL", "").rstrip("/")
    api_key = os.environ.get("LLM_API_KEY", "")
    model = os.environ.get("LLM_MODEL", "")
    temperature = float(os.environ.get("LLM_TEMPERATURE", "0"))
    timeout = int(os.environ.get("LLM_TIMEOUT_SECONDS", "180"))
    max_retries = int(os.environ.get("LLM_MAX_RETRIES", "2"))
    max_output_tokens = int(os.environ.get("LLM_MAX_OUTPUT_TOKENS", "8192") or 8192)
    enable_thinking = os.environ.get("LLM_ENABLE_THINKING", "false").strip().lower() == "true"
    if not base_url or not model:
        raise ValueError("LLM_API_BASE_URL and LLM_MODEL must be set in .env")

    payload = {
        "source": "吉他指板手册",
        "task": "exercise_answer_bbox_segmentation",
        "image_path": str(image_path),
        "image_width": width,
        "image_height": height,
        "expected_exercises": {
            "10": {"expected_subquestions": list(range(1, 11))},
            "11": {"expected_subquestions": list(range(1, 11))},
        },
        "questions": questions,
        "instruction": "请根据题目文本和整页答案图，返回每个小题对应小图的像素 bbox。",
    }
    content: list[dict[str, Any]] = [
        {"type": "text", "text": json.dumps(payload, ensure_ascii=False, indent=2)},
        {"type": "image_url", "image_url": {"url": image_to_data_url(image_path)}},
    ]
    request_payload: dict[str, Any] = {
        "model": model,
        "temperature": temperature,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ],
        "enable_thinking": enable_thinking,
        "max_tokens": max_output_tokens,
    }
    body = json.dumps(request_payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    last_error: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            req = urllib.request.Request(
                f"{base_url}/chat/completions",
                data=body,
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return extract_json_object(data["choices"][0]["message"]["content"])
        except (
            TimeoutError,
            urllib.error.URLError,
            urllib.error.HTTPError,
            KeyError,
            json.JSONDecodeError,
            ValueError,
        ) as exc:
            last_error = exc
            if attempt < max_retries:
                time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"VLM bbox request failed: {last_error}")


def clip_bbox(raw_bbox: Any, width: int, height: int) -> tuple[int, int, int, int] | None:
    if not isinstance(raw_bbox, dict):
        return None
    try:
        x1 = int(round(float(raw_bbox["x1"])))
        y1 = int(round(float(raw_bbox["y1"])))
        x2 = int(round(float(raw_bbox["x2"])))
        y2 = int(round(float(raw_bbox["y2"])))
    except (KeyError, TypeError, ValueError):
        return None
    x1 = max(0, min(width - 1, x1))
    y1 = max(0, min(height - 1, y1))
    x2 = max(1, min(width, x2))
    y2 = max(1, min(height, y2))
    if x2 <= x1 or y2 <= y1:
        return None
    return x1, y1, x2, y2


def normalize_items(result: dict[str, Any], width: int, height: int) -> list[dict[str, Any]]:
    items = result.get("items")
    if not isinstance(items, list):
        return []
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            continue
        bbox = clip_bbox(item.get("bbox"), width, height)
        if bbox is None:
            continue
        try:
            exercise_number = int(item.get("exercise_number"))
            subquestion_number = int(item.get("subquestion_number"))
            part_index = int(item.get("part_index") or 1)
        except (TypeError, ValueError):
            continue
        try:
            confidence = float(item.get("confidence", 0))
        except (TypeError, ValueError):
            confidence = 0.0
        normalized.append(
            {
                **item,
                "item_id": f"ex{exercise_number:02d}_{subquestion_number:02d}_p{part_index:02d}",
                "exercise_number": exercise_number,
                "subquestion_number": subquestion_number,
                "part_index": part_index,
                "bbox": {"x1": bbox[0], "y1": bbox[1], "x2": bbox[2], "y2": bbox[3]},
                "confidence": max(0.0, min(1.0, confidence)),
                "order_index": index,
            }
        )
    return normalized


def detect_row_clusters(image: Image.Image, x1: int, x2: int, min_y: int = 80) -> list[tuple[int, int]]:
    import numpy as np

    gray = image.convert("L")
    arr = np.array(gray)
    dark = arr < 190
    projection = dark[:, x1:x2].sum(axis=1)
    rows = np.where(projection > 20)[0]
    clusters: list[tuple[int, int]] = []
    if len(rows) == 0:
        return clusters
    start = prev = int(rows[0])
    for raw_y in rows[1:]:
        y = int(raw_y)
        if y - prev > 6:
            if prev - start > 8 and start >= min_y:
                clusters.append((start, prev))
            start = y
        prev = y
    if prev - start > 8 and start >= min_y:
        clusters.append((start, prev))
    return clusters


def local_grid_result(image_path: Path) -> dict[str, Any]:
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    left_rows = detect_row_clusters(image, 35, 620)[:10]
    right_rows = detect_row_clusters(image, 700, width)[:10]
    items: list[dict[str, Any]] = []
    for index, (y1, y2) in enumerate(left_rows, start=1):
        items.append(
            {
                "exercise_number": 10,
                "subquestion_number": index,
                "part_index": 1,
                "visible_label": EX10_LABELS.get(index, ""),
                "bbox": {
                    "x1": 50,
                    "y1": max(0, y1 - 12),
                    "x2": 612,
                    "y2": min(height, y2 + 10),
                },
                "confidence": 0.82,
                "notes": "local projection bbox; includes grid and nearby label",
            }
        )
    for index, (y1, y2) in enumerate(right_rows, start=1):
        items.append(
            {
                "exercise_number": 11,
                "subquestion_number": index,
                "part_index": 1,
                "visible_label": EX11_LABELS.get(index, ""),
                "bbox": {
                    "x1": 720,
                    "y1": max(0, y1 - 12),
                    "x2": min(width, 1410),
                    "y2": min(height, y2 + 10),
                },
                "confidence": 0.82,
                "notes": "local projection bbox; includes grid and nearby label",
            }
        )
    return {
        "image_width": width,
        "image_height": height,
        "items": items,
        "missing_items": [],
        "layout_notes": "Local-only projection segmentation. No external VLM call was used.",
    }


def draw_and_crop(image_path: Path, items: list[dict[str, Any]], output_dir: Path) -> None:
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    crop_dir = output_dir / "crops"
    crop_dir.mkdir(parents=True, exist_ok=True)
    colors = {10: (220, 40, 40), 11: (40, 90, 220)}
    for item in items:
        bbox = item["bbox"]
        box = (bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"])
        color = colors.get(item["exercise_number"], (20, 160, 90))
        draw.rectangle(box, outline=color, width=4)
        label = f"{item['exercise_number']}-{item['subquestion_number']}"
        if item.get("part_index", 1) != 1:
            label += f".{item['part_index']}"
        text_box = (box[0], max(0, box[1] - 20), box[0] + 90, box[1])
        draw.rectangle(text_box, fill=color)
        draw.text((text_box[0] + 4, text_box[1] + 3), label, fill=(255, 255, 255))
        crop = Image.open(image_path).convert("RGB").crop(box)
        crop_name = f"{item['item_id']}.png"
        crop.save(crop_dir / crop_name)
        item["crop_path"] = str((crop_dir / crop_name).relative_to(output_dir)).replace("\\", "/")
    image.save(output_dir / "annotated_bbox.png")


def render_review_md(output_dir: Path, image_path: Path, questions: dict[int, str], result: dict[str, Any], items: list[dict[str, Any]]) -> None:
    lines = [
        "# 练习10-11 答案图 bbox 试验审核",
        "",
        f"- source_image: `{image_path}`",
        f"- annotated_image: `annotated_bbox.png`",
        f"- raw_result: `bbox_result.json`",
        "",
        "## 标注总览",
        "",
        "![](annotated_bbox.png)",
        "",
        "## 题干文本",
        "",
    ]
    for number in sorted(questions):
        lines.extend([f"### 练习{number}", "", questions[number], ""])
    lines.extend(
        [
            "## VLM 布局备注",
            "",
            str(result.get("layout_notes") or ""),
            "",
            "## 小题 bbox",
            "",
            "| accept | item | confidence | visible_label | bbox | crop | caption | retrieval_text | notes |",
            "| --- | --- | ---: | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in items:
        bbox = item["bbox"]
        crop_path = item.get("crop_path", "")
        lines.append(
            "| [ ] | "
            + f"练习{item['exercise_number']}-{item['subquestion_number']}"
            + (f".{item['part_index']}" if item.get("part_index", 1) != 1 else "")
            + " | "
            + f"{item.get('confidence', 0):.2f}"
            + " | "
            + str(item.get("visible_label") or "").replace("|", "/")
            + " | "
            + f"{bbox['x1']},{bbox['y1']},{bbox['x2']},{bbox['y2']}"
            + " | "
            + (f"![]({crop_path})" if crop_path else "-")
            + " | "
            + str(item.get("caption") or "").replace("|", "/").replace("\n", " ")
            + " | "
            + str(item.get("retrieval_text") or "").replace("|", "/").replace("\n", " ")
            + " | "
            + str(item.get("notes") or "").replace("|", "/")
            + " |"
        )
    missing = result.get("missing_items") if isinstance(result.get("missing_items"), list) else []
    lines.extend(["", "## Missing Items", "", "```json", json.dumps(missing, ensure_ascii=False, indent=2), "```", ""])
    (output_dir / "bbox_review.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract VLM bboxes for fretboard answer image trial.")
    parser.add_argument("--chunks", type=Path, default=DEFAULT_CHUNKS)
    parser.add_argument("--image", type=Path, default=DEFAULT_IMAGE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--env", type=Path, default=ROOT / ".env")
    parser.add_argument("--local-grid-only", action="store_true", help="Use local image projection instead of external VLM.")
    args = parser.parse_args()

    if args.env.exists():
        apply_env_file(args.env)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(args.image) as image:
        width, height = image.size

    chunks = read_chunks(args.chunks)
    questions = {number: question_only(chunks[number]["text"]) for number in [10, 11]}
    request_preview = {
        "image": str(args.image),
        "image_width": width,
        "image_height": height,
        "questions": questions,
    }
    (args.output_dir / "bbox_request_preview.json").write_text(
        json.dumps(request_preview, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    if args.local_grid_only:
        result = local_grid_result(args.image)
    else:
        result = call_vlm(args.image, questions, width, height)
    result["image_width"] = width
    result["image_height"] = height
    items = normalize_items(result, width, height)
    result["normalized_items"] = items
    (args.output_dir / "bbox_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    draw_and_crop(args.image, items, args.output_dir)
    render_review_md(args.output_dir, args.image, questions, result, items)

    print(
        json.dumps(
            {
                "items": len(items),
                "output_dir": str(args.output_dir),
                "review_md": str(args.output_dir / "bbox_review.md"),
                "annotated_image": str(args.output_dir / "annotated_bbox.png"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
