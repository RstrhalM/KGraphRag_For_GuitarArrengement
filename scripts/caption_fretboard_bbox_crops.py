from __future__ import annotations

import argparse
import base64
import http.client
import json
import mimetypes
import os
import time
import urllib.error
from pathlib import Path
from typing import Any

import requests

from extract_arrangement_kg import apply_env_file, extract_json_object
from run_fretboard_answer_bbox_tasks import ROOT, rel_path


SYSTEM_PROMPT = """你是一位吉他教材视觉证据 caption 助手。

你会看到若干张已经裁剪好的《吉他指板手册》参考答案小图。每张图已经有 item_id、练习号、小题号、题干摘要和可见标签。

任务：
为每张裁剪图生成结构化 caption，用于后续文本 RAG 检索。只描述图中真实可见内容和题干给出的语境。

规则：
1. 不要输出 bbox，不要生成知识图谱。
2. 不要凭空补充看不见的音名、品位、和弦/音阶名称；如果信息来自题干或 visible_label，要在 caption 中自然说明。
3. retrieval_text 必须适合检索，包含练习号、小题号、visible_label、图形类型和关键乐理词。
4. theory_tags 放短标签，例如：音符定位、大调音阶、根音型式、琶音、和弦指型、调式、音程。
5. confidence 反映 caption 对图片可见内容的把握；图太小或难辨认时降低 confidence 并写 notes。

输出严格 JSON 对象，不要 Markdown，不要代码块：
{
  "items": [
    {
      "item_id": "ex10_01_p01",
      "visual_type": "fretboard_diagram | chord_diagram | scale_pattern | interval_pattern | arpeggio_pattern | text_answer | mixed",
      "caption": "中文 caption",
      "retrieval_text": "中文检索文本",
      "theory_tags": ["音符定位"],
      "confidence": 0.0,
      "notes": ""
    }
  ]
}
"""


def image_to_data_url(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(path.name)
    mime_type = mime_type or "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def crop_path_for(output_dir: Path, item: dict[str, Any]) -> Path:
    raw = item.get("crop_path")
    if not raw:
        raw = f"crops/{item.get('item_id')}.png"
        item["crop_path"] = raw
    return output_dir / str(raw)


def call_vlm(batch: list[dict[str, Any]], output_dir: Path) -> dict[str, Any]:
    base_url = os.environ.get("LLM_API_BASE_URL", "").rstrip("/")
    api_key = os.environ.get("LLM_API_KEY", "")
    model = os.environ.get("LLM_MODEL", "")
    temperature = float(os.environ.get("LLM_TEMPERATURE", "0"))
    timeout = int(os.environ.get("LLM_TIMEOUT_SECONDS", "180"))
    max_retries = int(os.environ.get("LLM_MAX_RETRIES", "1"))
    max_output_tokens = int(os.environ.get("LLM_MAX_OUTPUT_TOKENS", "8192") or 8192)
    enable_thinking = os.environ.get("LLM_ENABLE_THINKING", "false").strip().lower() == "true"
    if not base_url or not model:
        raise ValueError("LLM_API_BASE_URL and LLM_MODEL must be set in .env")

    payload_items = []
    content: list[dict[str, Any]] = [
        {
            "type": "text",
            "text": "请按下面每个 item_id 对应的裁剪图生成 caption。图片会紧跟在各自的 item metadata 后面。",
        }
    ]
    for item in batch:
        crop_path = crop_path_for(output_dir, item)
        payload = {
            "item_id": item.get("item_id"),
            "exercise_number": item.get("exercise_number"),
            "subquestion_number": item.get("subquestion_number"),
            "part_index": item.get("part_index"),
            "visible_label": item.get("visible_label"),
            "bbox": item.get("bbox"),
            "crop_path": rel_path(crop_path),
        }
        payload_items.append(payload)
        content.append({"type": "text", "text": json.dumps(payload, ensure_ascii=False)})
        content.append({"type": "image_url", "image_url": {"url": image_to_data_url(crop_path)}})

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
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    proxy_url = os.environ.get("LLM_PROXY_URL") or os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None

    last_error: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            response = requests.post(
                f"{base_url}/chat/completions",
                headers=headers,
                json=request_payload,
                proxies=proxies,
                timeout=timeout,
            )
            if response.status_code >= 400:
                raise RuntimeError(f"HTTP {response.status_code}: {response.text[:1000]}")
            data = response.json()
            return extract_json_object(data["choices"][0]["message"]["content"])
        except (
            TimeoutError,
            ConnectionResetError,
            http.client.RemoteDisconnected,
            http.client.HTTPException,
            requests.RequestException,
            urllib.error.URLError,
            urllib.error.HTTPError,
            KeyError,
            json.JSONDecodeError,
            ValueError,
            RuntimeError,
        ) as exc:
            last_error = exc
            if attempt < max_retries:
                time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"VLM crop caption request failed: {last_error}")


def merge_captions(items: list[dict[str, Any]], caption_rows: list[dict[str, Any]]) -> None:
    by_id = {str(row.get("item_id")): row for row in caption_rows if isinstance(row, dict)}
    for item in items:
        row = by_id.get(str(item.get("item_id")))
        if not row:
            continue
        for key in ["visual_type", "caption", "retrieval_text", "theory_tags", "confidence", "notes"]:
            if key in row:
                item[key] = row[key]


def render_caption_review(output_dir: Path, items: list[dict[str, Any]]) -> None:
    lines = [
        "# 裁剪图 Caption 审核",
        "",
        "| accept | item | crop | visual_type | confidence | caption | retrieval_text | tags | notes |",
        "| --- | --- | --- | --- | ---: | --- | --- | --- | --- |",
    ]
    for item in items:
        tags = item.get("theory_tags")
        if isinstance(tags, list):
            tags_text = ", ".join(str(tag) for tag in tags)
        else:
            tags_text = str(tags or "")
        lines.append(
            "| [ ] | "
            + str(item.get("item_id") or "")
            + " | "
            + f"![]({item.get('crop_path')})"
            + " | "
            + str(item.get("visual_type") or "").replace("|", "/")
            + " | "
            + f"{float(item.get('confidence') or 0):.2f}"
            + " | "
            + str(item.get("caption") or "").replace("|", "/").replace("\n", " ")
            + " | "
            + str(item.get("retrieval_text") or "").replace("|", "/").replace("\n", " ")
            + " | "
            + tags_text.replace("|", "/")
            + " | "
            + str(item.get("notes") or "").replace("|", "/").replace("\n", " ")
            + " |"
        )
    (output_dir / "crop_caption_review.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Caption cropped fretboard answer bbox images.")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--env", type=Path, default=ROOT / ".env")
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--proxy", help="Optional proxy URL, e.g. http://127.0.0.1:7890")
    args = parser.parse_args()

    if args.env.exists():
        apply_env_file(args.env)
    if args.proxy:
        os.environ["LLM_PROXY_URL"] = args.proxy
    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir
    result_path = output_dir / "bbox_result.json"
    result = json.loads(result_path.read_text(encoding="utf-8"))
    items = result.get("normalized_items")
    if not isinstance(items, list):
        raise SystemExit("bbox_result.json does not contain normalized_items")

    all_caption_rows: list[dict[str, Any]] = []
    for start in range(0, len(items), args.batch_size):
        batch = items[start : start + args.batch_size]
        raw = call_vlm(batch, output_dir)
        rows = raw.get("items") if isinstance(raw, dict) else None
        if not isinstance(rows, list):
            raise RuntimeError("Caption response must contain an `items` list")
        all_caption_rows.extend(rows)
        merge_captions(items, rows)

    result["normalized_items"] = items
    result["crop_captions"] = all_caption_rows
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    render_caption_review(output_dir, items)
    print(
        json.dumps(
            {
                "items": len(items),
                "captions": len(all_caption_rows),
                "output_dir": rel_path(output_dir),
                "review_md": rel_path(output_dir / "crop_caption_review.md"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
