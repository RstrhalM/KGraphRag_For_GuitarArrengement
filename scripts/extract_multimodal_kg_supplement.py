#!/usr/bin/env python
"""Extract image-grounded KG supplement edges from paired text chunks and images."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from extract_arrangement_kg import (
    SYSTEM_PROMPT,
    apply_env_file,
    build_review_items,
    extract_json_object,
    get_model_limits,
    validate_edges,
    write_jsonl,
)


MULTIMODAL_SYSTEM_PROMPT = (
    SYSTEM_PROMPT
    + """

多模态视觉补抽规则：
你会同时看到 Math Rock 吉他教材的 Markdown 文本片段，以及与该片段对应的整页图或局部图。
这些图片只用于补足文字中“见图/谱例/指法图/和弦图/节奏图”没有展开的具体信息。

本轮是“视觉补充层”，不能覆盖已有文字图谱。只提取图片带来的增量知识：
1. 谱例或图示明确展示的 riff 节奏组织、切分、重音、休止、拍号/分组、循环结构。
2. 和弦图或指板图明确展示的 voicing、省略音、开放弦、弦组、把位跨度、转位、声部连接。
3. 图中动作/奏法明确影响编曲的技法，如 tapping、hammer-on/pull-off、slide、muting、hybrid picking。
4. 图示让文字原则变得可操作时，可以抽成可复用编曲规则。

必须丢弃：
1. 只能复述文字、没有视觉增量的信息。
2. 单纯题目答案、练习编号、页面装饰、目录、页眉页脚。
3. 无法从图片辨认具体节奏/品位/弦组/和弦形状时，不要猜；返回空或 needs_visual_context=true。

输出仍必须遵守原 JSON schema。若图片已经补足证据，needs_visual_context 必须为 false。
evidence 可以写“文本+图示”中的短证据，但不要长篇抄写教材。
"""
)


def image_to_data_url(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(path.name)
    mime_type = mime_type or "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


class MultimodalLLMClient:
    def __init__(self) -> None:
        self.base_url = os.environ.get("LLM_API_BASE_URL", "").rstrip("/")
        self.api_key = os.environ.get("LLM_API_KEY", "")
        self.model = os.environ.get("LLM_MODEL", "")
        self.temperature = float(os.environ.get("LLM_TEMPERATURE", "0"))
        self.timeout = int(os.environ.get("LLM_TIMEOUT_SECONDS", "180"))
        self.max_retries = int(os.environ.get("LLM_MAX_RETRIES", "2"))
        self.max_output_tokens = int(os.environ.get("LLM_MAX_OUTPUT_TOKENS", "0") or 0)
        self.enable_thinking = os.environ.get("LLM_ENABLE_THINKING", "false").strip().lower() == "true"
        if not self.base_url or not self.model:
            raise ValueError("LLM_API_BASE_URL and LLM_MODEL must be set in .env")

    def chat_json_with_images(self, payload: dict[str, Any], image_paths: list[Path]) -> dict[str, Any]:
        content: list[dict[str, Any]] = [
            {"type": "text", "text": json.dumps(payload, ensure_ascii=False, indent=2)}
        ]
        for image_path in image_paths:
            content.append({"type": "image_url", "image_url": {"url": image_to_data_url(image_path)}})

        request_payload: dict[str, Any] = {
            "model": self.model,
            "temperature": self.temperature,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": MULTIMODAL_SYSTEM_PROMPT},
                {"role": "user", "content": content},
            ],
            "enable_thinking": self.enable_thinking,
        }
        if self.max_output_tokens > 0:
            request_payload["max_tokens"] = self.max_output_tokens

        body = json.dumps(request_payload, ensure_ascii=False).encode("utf-8")
        headers = {"Content-Type": "application/json; charset=utf-8"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                req = urllib.request.Request(
                    f"{self.base_url}/chat/completions",
                    data=body,
                    headers=headers,
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
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
                if attempt < self.max_retries:
                    time.sleep(1.5 * (attempt + 1))
        raise RuntimeError(f"LLM request failed: {last_error}")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_chunks(path: Path) -> dict[str, dict[str, Any]]:
    rows = read_json(path)
    if not isinstance(rows, list):
        raise ValueError(f"{path} must contain a JSON array")
    return {str(row.get("chunk_id")): row for row in rows if isinstance(row, dict)}


def load_pairings(path: Path, chunk_ids: list[str]) -> list[dict[str, Any]]:
    pairings = read_json(path)
    if not isinstance(pairings, list):
        raise ValueError(f"{path} must contain a JSON array")
    if chunk_ids:
        selected = set(chunk_ids)
        pairings = [row for row in pairings if str(row.get("chunk_id")) in selected]
    return [row for row in pairings if isinstance(row, dict)]


def enforce_image_limits(image_paths: list[Path], max_images: int, max_base64_chars: int) -> tuple[list[Path], list[str]]:
    selected: list[Path] = []
    skipped: list[str] = []
    for image_path in image_paths:
        if not image_path.exists():
            skipped.append(f"missing file: {image_path}")
            continue
        encoded_chars = ((image_path.stat().st_size + 2) // 3) * 4
        if max_base64_chars > 0 and encoded_chars > max_base64_chars:
            skipped.append(f"{image_path} exceeds base64 limit")
            continue
        selected.append(image_path)
        if max_images > 0 and len(selected) >= max_images:
            omitted = len(image_paths) - len(selected)
            if omitted > 0:
                skipped.append(f"omitted {omitted} image(s) due to max image limit")
            break
    return selected, skipped


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunks-json", type=Path, required=True)
    parser.add_argument("--pairings-json", type=Path, required=True)
    parser.add_argument("-o", "--output-dir", type=Path, required=True)
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    parser.add_argument("--chunk-id", action="append", default=[], help="Chunk id to process; repeatable")
    parser.add_argument("--max-images", type=int, default=5)
    parser.add_argument("--review-context-chars", type=int, default=900)
    parser.add_argument("--review-id-prefix", default="mathrock_pdf_visual")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    apply_env_file(args.env_file)
    chunks_by_id = load_chunks(args.chunks_json)
    pairings = load_pairings(args.pairings_json, args.chunk_id)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    model_limits = get_model_limits(os.environ.get("LLM_MODEL", ""))
    max_base64_chars = int(model_limits.get("vision_max_base64_chars", 10_000_000) or 10_000_000)
    prepared: list[dict[str, Any]] = []
    for pairing in pairings:
        chunk_id = str(pairing.get("chunk_id"))
        chunk = chunks_by_id.get(chunk_id)
        if not chunk:
            raise ValueError(f"Missing chunk in chunks json: {chunk_id}")
        image_paths = [Path(path) for path in pairing.get("image_paths", [])]
        selected_images, skipped = enforce_image_limits(image_paths, args.max_images, max_base64_chars)
        prepared.append(
            {
                "chunk_id": chunk_id,
                "chars": len(str(chunk.get("text", ""))),
                "page_hint": chunk.get("page_hint"),
                "selected_pages": pairing.get("selected_pages", []),
                "image_paths": [str(path) for path in selected_images],
                "skipped": skipped,
            }
        )

    (args.output_dir / "multimodal_pairings_prepared.json").write_text(
        json.dumps(prepared, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    if args.dry_run:
        print(f"Dry run wrote {len(prepared)} prepared pairing(s) to {args.output_dir}")
        return 0

    client = MultimodalLLMClient()
    all_edges: list[dict[str, Any]] = []
    all_review_items: list[dict[str, Any]] = []
    discarded_total = {"definition_noise": 0, "practice_drill_noise": 0, "missing_visual_context": 0}
    chunk_reports: list[dict[str, Any]] = []

    for item in prepared:
        chunk = chunks_by_id[item["chunk_id"]]
        image_paths = [Path(path) for path in item["image_paths"]]
        if not image_paths:
            chunk_reports.append({**item, "edges": 0, "error": "no images"})
            print(f"{item['chunk_id']}: skipped, no images")
            continue

        print(
            f"{item['chunk_id']}: sending {len(image_paths)} image(s), chars={len(str(chunk.get('text', '')))}",
            flush=True,
        )
        result = client.chat_json_with_images(
            {
                "task": "mathrock_pdf_multimodal_kg_supplement",
                "chunk_id": item["chunk_id"],
                "page_hint": chunk.get("page_hint"),
                "selected_pages": item["selected_pages"],
                "image_filenames": [path.name for path in image_paths],
                "text": chunk["text"],
                "instruction": "只提取图片相对文字新增的、可复用的吉他编曲知识图谱边；不要覆盖已有文字抽取结果。",
            },
            image_paths,
        )
        edges, discarded = validate_edges(result, chunk)
        candidate_refs = [str(path) for path in image_paths]
        for edge in edges:
            edge["source_pass"] = "multimodal_visual_supplement"
            edge["visual_image_paths"] = candidate_refs
        review_items = build_review_items(edges, chunk, candidate_refs, args.review_context_chars)
        for review_item in review_items:
            review_item["review_id"] = f"{args.review_id_prefix}:{review_item['review_id']}"
            review_item["source_pass"] = "multimodal_visual_supplement"
            review_item["selected_pages"] = item["selected_pages"]
        all_edges.extend(edges)
        all_review_items.extend(review_items)
        for key, value in discarded.items():
            discarded_total[key] += value
        chunk_reports.append(
            {
                **item,
                "edges": len(edges),
                "discarded_summary": discarded,
            }
        )
        print(f"{item['chunk_id']}: {len(edges)} edge(s)", flush=True)

    write_jsonl(args.output_dir / "arrangement_kg_edges.jsonl", all_edges)
    write_jsonl(args.output_dir / "arrangement_kg_review.jsonl", all_review_items)
    report = {
        "chunks": len(prepared),
        "model": client.model,
        "model_limits": model_limits,
        "edges": len(all_edges),
        "review_items": len(all_review_items),
        "discarded_summary": discarded_total,
        "chunk_reports": chunk_reports,
    }
    (args.output_dir / "arrangement_kg_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {len(all_edges)} visual supplement edge(s) to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
