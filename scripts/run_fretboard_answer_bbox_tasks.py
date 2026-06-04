from __future__ import annotations

import argparse
import base64
import http.client
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import requests
from PIL import Image

from extract_arrangement_kg import apply_env_file, extract_json_object
from extract_fretboard_answer_bboxes import (
    ROOT,
    DEFAULT_CHUNKS,
    draw_and_crop,
    local_grid_result,
    normalize_items,
    question_only,
    read_chunks,
    render_review_md,
)


DEFAULT_IMAGE_DIR = ROOT / "data" / "练习解答（图片）"
DEFAULT_OUTPUT_ROOT = ROOT / "data" / "processed" / "fretboard_handbook" / "bbox_tasks"
TASK_QUEUE = DEFAULT_OUTPUT_ROOT / "task_queue.jsonl"
TASK_QUEUE_MD = DEFAULT_OUTPUT_ROOT / "task_queue.md"


GENERIC_SYSTEM_PROMPT = """你是一位吉他教材答案页版面分析助手。

你会看到：
1. 《吉他指板手册》中若干练习的完整题目文本；
2. 一张覆盖这些练习参考答案的整页图片。

任务：
把整页答案图片切分成“每个小题对应一张图”的 bbox，并为每个可裁剪区域生成结构化 caption。bbox 必须对应真实可裁剪的小图区域，而不是整道大题区域。

重要规则：
1. 坐标使用像素坐标，原点在图片左上角，x 向右，y 向下。
2. bbox 尽量紧贴每张指板图、和弦图、音阶图、答案图，但要保留题号、调名、品位标记等紧邻标签。
3. 只处理输入 expected_exercises 中列出的练习；不要扩展到图片外或猜测其他题。
4. 每个练习可能包含若干小题。请尽量按图片中可见的小题编号输出 subquestion_number。
5. 不要把相邻小题合并为一个 bbox；如果两个图靠得很近，也要拆开。
6. 若一个小题有多个必要图块，返回多个 bbox，并用 part_index 标识。
7. caption 只描述图中可见内容与题干给出的语境，避免凭空补全看不见的音名、把位、和弦/音阶名称。
8. retrieval_text 要适合作为文本 RAG 检索字段，包含练习号、小题号、题干关键词、visible_label 和图中明确可见的乐理/指板信息。
9. 不要生成知识图谱，不要判断题目答案对错。
10. 如果判断不确定，保留 bbox，但 confidence 降低，并在 notes 中说明。

输出严格 JSON 对象，不要 Markdown，不要代码块：
{
  "image_width": 0,
  "image_height": 0,
  "items": [
    {
      "exercise_number": 10,
      "subquestion_number": 1,
      "part_index": 1,
      "visible_label": "图片中可见的小题标签/调名/品位提示",
      "bbox": {"x1": 0, "y1": 0, "x2": 100, "y2": 100},
      "visual_type": "fretboard_diagram | chord_diagram | scale_pattern | interval_pattern | arpeggio_pattern | text_answer | mixed",
      "caption": "用中文简洁描述该裁剪区域的视觉内容和题目语境",
      "retrieval_text": "面向检索的中文描述，必须包含练习号、小题号和关键乐理词",
      "theory_tags": ["根音型式", "大调音阶", "七和弦琶音"],
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


def rel_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return str(path.resolve()).replace("\\", "/")


def task_id_for(image_path: Path, exercises: list[int]) -> str:
    if exercises:
        return f"exercise_{exercises[0]:02d}_{exercises[-1]:02d}"
    return image_path.stem


def parse_exercises_from_name(name: str) -> list[int]:
    clean = Path(name).stem
    match = re.search(r"练习\s*(\d+)\s*[-_－—~～]\s*(?:练习)?\s*(\d+)", clean)
    if match:
        start, end = int(match.group(1)), int(match.group(2))
        if start <= end:
            return list(range(start, end + 1))
        return list(range(end, start + 1))
    numbers = [int(value) for value in re.findall(r"练习\s*(\d+)|(?<![A-Za-z0-9])(\d+)(?![A-Za-z0-9])", clean) for value in value if value]
    return sorted(set(numbers))


def image_to_data_url(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(path.name)
    mime_type = mime_type or "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def load_queue(path: Path = TASK_QUEUE) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def build_queue(image_dir: Path, chunks_path: Path, output_root: Path) -> list[dict[str, Any]]:
    chunks = read_chunks(chunks_path)
    rows: list[dict[str, Any]] = []
    for image_path in sorted(image_dir.glob("*")):
        if image_path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        exercises = [number for number in parse_exercises_from_name(image_path.name) if number in chunks]
        with Image.open(image_path) as image:
            width, height = image.size
        task_id = task_id_for(image_path, exercises)
        rows.append(
            {
                "task_id": task_id,
                "image_path": rel_path(image_path),
                "image_name": image_path.name,
                "exercises": exercises,
                "image_width": width,
                "image_height": height,
                "output_dir": rel_path(output_root / task_id),
                "status": "pending",
            }
        )
    write_jsonl(output_root / "task_queue.jsonl", rows)
    render_queue_md(rows, output_root / "task_queue.md")
    return rows


def render_queue_md(rows: list[dict[str, Any]], path: Path) -> None:
    lines = [
        "# 指板手册答案图 bbox 任务队列",
        "",
        "| task_id | image | exercises | size | status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['task_id']}` | `{row['image_name']}` | "
            f"{','.join(str(x) for x in row.get('exercises', [])) or '-'} | "
            f"{row.get('image_width')}x{row.get('image_height')} | {row.get('status', 'pending')} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def find_task(task_id: str | None, image: Path | None, queue: list[dict[str, Any]]) -> dict[str, Any]:
    if task_id:
        for row in queue:
            if row.get("task_id") == task_id:
                return row
        raise SystemExit(f"Task not found: {task_id}")
    if image:
        exercises = parse_exercises_from_name(image.name)
        with Image.open(image) as im:
            width, height = im.size
        return {
            "task_id": task_id_for(image, exercises),
            "image_path": rel_path(image),
            "image_name": image.name,
            "exercises": exercises,
            "image_width": width,
            "image_height": height,
            "output_dir": rel_path(DEFAULT_OUTPUT_ROOT / task_id_for(image, exercises)),
        }
    for row in queue:
        status = str(row.get("status") or "pending")
        if status == "pending":
            return row
    raise SystemExit("No pending task found. Pass --task-id or rebuild the queue.")


def workspace_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if not path.is_absolute():
        path = ROOT / path
    return path


def expected_exercises_payload(exercises: list[int]) -> dict[str, dict[str, Any]]:
    return {
        str(number): {
            "expected_subquestions": "unknown; infer from visible answer labels and question text",
        }
        for number in exercises
    }


def build_request_payload(task: dict[str, Any], chunks_path: Path) -> tuple[Path, Path, dict[int, str], dict[str, Any]]:
    image_path = workspace_path(str(task["image_path"]))
    chunks = read_chunks(chunks_path)
    exercises = [int(number) for number in task.get("exercises", [])]
    questions = {number: question_only(chunks[number]["text"]) for number in exercises if number in chunks}
    with Image.open(image_path) as image:
        width, height = image.size
    payload = {
        "source": "吉他指板手册",
        "task": "single_answer_image_bbox_segmentation",
        "image_path": str(image_path),
        "image_width": width,
        "image_height": height,
        "expected_exercises": expected_exercises_payload(exercises),
        "questions": questions,
        "instruction": "请根据题目文本和单张答案图，逐小题返回像素 bbox。只返回当前图片的结果。",
    }
    output_dir = workspace_path(str(task.get("output_dir") or DEFAULT_OUTPUT_ROOT / str(task["task_id"])))
    return image_path, output_dir, questions, payload


def write_request_package(task: dict[str, Any], chunks_path: Path) -> dict[str, str]:
    image_path, output_dir, questions, payload = build_request_payload(task, chunks_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    prompt_path = output_dir / "vlm_prompt.md"
    payload_path = output_dir / "vlm_request_payload.json"
    result_template_path = output_dir / "bbox_result_to_fill.json"
    prompt_path.write_text(
        "\n".join(
            [
                "# VLM bbox 请求",
                "",
                f"- task_id: `{task['task_id']}`",
                f"- image_path: `{image_path}`",
                "",
                "## System Prompt",
                "",
                GENERIC_SYSTEM_PROMPT,
                "",
                "## User Payload",
                "",
                "```json",
                json.dumps(payload, ensure_ascii=False, indent=2),
                "```",
                "",
                "把上面的 payload 和图片一起发给 VLM，只返回 JSON 对象。",
            ]
        ),
        encoding="utf-8",
    )
    payload_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    if not result_template_path.exists():
        result_template_path.write_text(
            json.dumps(
                {
                    "image_width": payload["image_width"],
                    "image_height": payload["image_height"],
                    "items": [],
                    "missing_items": [],
                    "layout_notes": "",
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
    return {
        "prompt_md": rel_path(prompt_path),
        "payload_json": rel_path(payload_path),
        "result_template": rel_path(result_template_path),
    }


def call_vlm_for_task(image_path: Path, payload: dict[str, Any]) -> dict[str, Any]:
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

    content: list[dict[str, Any]] = [
        {"type": "text", "text": json.dumps(payload, ensure_ascii=False, indent=2)},
        {"type": "image_url", "image_url": {"url": image_to_data_url(image_path)}},
    ]
    request_payload: dict[str, Any] = {
        "model": model,
        "temperature": temperature,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": GENERIC_SYSTEM_PROMPT},
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
                raise RuntimeError(
                    f"HTTP {response.status_code}: {response.text[:1000]}"
                )
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
    raise RuntimeError(f"VLM bbox request failed: {last_error}")


def parse_bbox_result_object(raw: Any) -> dict[str, Any]:
    """Accept direct bbox JSON, full Qwen/OpenAI response JSON, or nested message content."""
    if isinstance(raw, dict) and isinstance(raw.get("items"), list):
        return raw
    if isinstance(raw, dict) and isinstance(raw.get("choices"), list) and raw["choices"]:
        message = raw["choices"][0].get("message") if isinstance(raw["choices"][0], dict) else None
        if isinstance(message, dict):
            return parse_bbox_result_object(message.get("content"))
    if isinstance(raw, dict) and "content" in raw:
        return parse_bbox_result_object(raw.get("content"))
    if isinstance(raw, str):
        text = raw.strip()
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = extract_json_object(text)
        return parse_bbox_result_object(parsed)
    raise ValueError("Could not find bbox result object. Expected an object with `items`, or a chat response with choices[0].message.content.")


def load_bbox_result_json(path_or_dash: str) -> dict[str, Any]:
    if path_or_dash == "-":
        text = sys.stdin.read()
    else:
        text = Path(path_or_dash).read_text(encoding="utf-8")
    return parse_bbox_result_object(json.loads(text))


def process_result(
    *,
    task: dict[str, Any],
    image_path: Path,
    output_dir: Path,
    questions: dict[int, str],
    result: dict[str, Any],
) -> dict[str, Any]:
    with Image.open(image_path) as image:
        width, height = image.size
    result["image_width"] = width
    result["image_height"] = height
    items = normalize_items(result, width, height)
    result["normalized_items"] = items
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "bbox_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    draw_and_crop(image_path, items, output_dir)
    render_review_md(output_dir, image_path, questions, result, items)
    summary = {
        "task_id": task["task_id"],
        "items": len(items),
        "output_dir": rel_path(output_dir),
        "review_md": rel_path(output_dir / "bbox_review.md"),
        "annotated_image": rel_path(output_dir / "annotated_bbox.png"),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run fretboard answer-image bbox tasks one image at a time.")
    parser.add_argument("action", choices=["list", "prepare", "run-one", "apply-json"])
    parser.add_argument("--image-dir", type=Path, default=DEFAULT_IMAGE_DIR)
    parser.add_argument("--chunks", type=Path, default=DEFAULT_CHUNKS)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--queue", type=Path, default=TASK_QUEUE)
    parser.add_argument("--task-id")
    parser.add_argument("--image", type=Path)
    parser.add_argument("--env", type=Path, default=ROOT / ".env")
    parser.add_argument("--backend", choices=["api", "local-rule"], default="api")
    parser.add_argument("--proxy", help="Optional proxy URL, e.g. http://127.0.0.1:7890")
    parser.add_argument(
        "--json-result",
        help="For apply-json: bbox JSON, full Qwen/OpenAI response JSON, or '-' for stdin.",
    )
    args = parser.parse_args()

    if args.env.exists():
        apply_env_file(args.env)
    if args.proxy:
        os.environ["LLM_PROXY_URL"] = args.proxy

    if args.action == "list":
        rows = build_queue(args.image_dir, args.chunks, args.output_root)
        print(json.dumps({"tasks": len(rows), "queue": rel_path(args.output_root / "task_queue.jsonl"), "queue_md": rel_path(args.output_root / "task_queue.md")}, ensure_ascii=False, indent=2))
        return

    queue = load_queue(args.queue)
    task = find_task(args.task_id, args.image, queue)
    image_path, output_dir, questions, payload = build_request_payload(task, args.chunks)

    if args.action == "prepare":
        package = write_request_package(task, args.chunks)
        print(json.dumps({"task_id": task["task_id"], **package}, ensure_ascii=False, indent=2))
        return

    if args.action == "apply-json":
        if not args.json_result:
            raise SystemExit("--json-result is required for apply-json")
        result = load_bbox_result_json(args.json_result)
        summary = process_result(task=task, image_path=image_path, output_dir=output_dir, questions=questions, result=result)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return

    if args.action == "run-one":
        write_request_package(task, args.chunks)
        if args.backend == "local-rule":
            result = local_grid_result(image_path)
        else:
            result = call_vlm_for_task(image_path, payload)
        summary = process_result(task=task, image_path=image_path, output_dir=output_dir, questions=questions, result=result)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return


if __name__ == "__main__":
    main()
