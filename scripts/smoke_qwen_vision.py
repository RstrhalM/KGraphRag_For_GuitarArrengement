#!/usr/bin/env python
"""Smoke-test a Qwen OpenAI-compatible vision endpoint with one local image."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def read_env(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def apply_env_file(path: Path) -> None:
    for key, value in read_env(path).items():
        os.environ.setdefault(key, value)


def extract_json_object(text: str) -> dict[str, Any]:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start < 0 or end <= start:
            raise
        return json.loads(text[start : end + 1])


def image_data_url(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(path.name)
    if not mime_type:
        mime_type = "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path, help="Local image path")
    parser.add_argument("--env-file", type=Path, default=Path(".env"), help="Path to .env")
    parser.add_argument("--timeout", type=int, default=120, help="Request timeout in seconds")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    apply_env_file(args.env_file)

    base_url = os.environ.get("LLM_API_BASE_URL", "").rstrip("/")
    api_key = os.environ.get("LLM_API_KEY", "")
    model = os.environ.get("LLM_MODEL", "")
    if not base_url or not api_key or not model:
        raise ValueError("LLM_API_BASE_URL, LLM_API_KEY, and LLM_MODEL must be set")
    if not args.image.exists():
        raise FileNotFoundError(args.image)

    user_text = (
        "请观察图片并只输出 JSON 对象，字段包括："
        "scene_cn、main_objects、visible_text、is_smoke_test_ok、confidence。"
        "不要输出 Markdown。"
    )
    request_payload = {
        "model": model,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_data_url(args.image)}},
                    {"type": "text", "text": user_text},
                ],
            }
        ],
        "enable_thinking": False,
    }

    body = json.dumps(request_payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json; charset=utf-8",
    }
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=body,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as resp:
            response_payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {error_body}") from exc

    content = response_payload["choices"][0]["message"]["content"]
    result = extract_json_object(content)
    print(json.dumps({"model": response_payload.get("model"), "result": result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
