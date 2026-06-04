#!/usr/bin/env python
"""Reprocess exercise-heavy chunks with answer images for KG extraction."""

from __future__ import annotations

import argparse
import base64
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

from extract_arrangement_kg import (
    SYSTEM_PROMPT,
    apply_env_file,
    build_review_items,
    extract_json_object,
    get_model_limits,
    validate_edges,
    write_jsonl,
)


VISION_SYSTEM_PROMPT = (
    SYSTEM_PROMPT
    + """

视觉补抽取规则：
你会同时看到教材中的练习文字和对应的“练习解答图片”。解答图片只作为理解缺失图示的证据，
不能把练习答案逐条写入图谱。

只在答案图片揭示以下可复用信息时产边：
1. 指板几何：相邻弦同音、四度/五度/八度/六度/七度等在不同弦组上的位移规律。
2. 编配可用性：某个音程、指型或弦组如何影响 riff、独奏线、声部连接、和弦 voicing 的可弹性。
3. 调式/音阶关系：同一组指型如何在不同和声背景下转为不同调式色彩，且能服务于编曲选择。
4. 和弦构型：答案图显示省略音、弦组、低音位置、跨度或把位限制，能形成 voicing 规则。

必须丢弃：
1. 纯填空答案、题号对应答案、让学生画点/标音名/背诵的内容。
2. 只能说明“这个练习的正确答案是什么”的信息。
3. 没有编曲启发的音阶/和弦基础知识。

如果图片补足了证据，needs_visual_context 必须为 false；evidence 可引用“练习文字+答案图”中的短证据。
"""
)


class VisionLLMClient:
    def __init__(self) -> None:
        self.base_url = os.environ.get("LLM_API_BASE_URL", "").rstrip("/")
        self.api_key = os.environ.get("LLM_API_KEY", "")
        self.model = os.environ.get("LLM_MODEL", "")
        self.temperature = float(os.environ.get("LLM_TEMPERATURE", "0"))
        self.timeout = int(os.environ.get("LLM_TIMEOUT_SECONDS", "120"))
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
                {"role": "system", "content": VISION_SYSTEM_PROMPT},
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
            except (urllib.error.URLError, urllib.error.HTTPError, KeyError, json.JSONDecodeError, ValueError) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(1.5 * (attempt + 1))
        raise RuntimeError(f"LLM request failed: {last_error}")


def image_to_data_url(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(path.name)
    mime_type = mime_type or "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def parse_answer_image_range(path: Path) -> set[int]:
    match = re.search(r"练习\s*(\d+)(?:\s*[-—－]\s*(?:练习)?\s*(\d+))?", path.stem)
    if not match:
        return set()
    start = int(match.group(1))
    end = int(match.group(2) or start)
    if end < start:
        start, end = end, start
    return set(range(start, end + 1))


def parse_chunk_exercises(text: str) -> set[int]:
    return {int(match.group(1)) for match in re.finditer(r"练习\s*(\d+)", text)}


def load_chunks(path: Path, chunk_ids: list[str]) -> list[dict[str, Any]]:
    chunks = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(chunks, list):
        raise ValueError(f"{path} must contain a JSON array")
    selected_ids = set(chunk_ids)
    selected = [chunk for chunk in chunks if not selected_ids or chunk.get("chunk_id") in selected_ids]
    if selected_ids:
        found_ids = {chunk.get("chunk_id") for chunk in selected}
        missing = sorted(selected_ids - found_ids)
        if missing:
            raise ValueError(f"Missing chunk_id(s): {', '.join(missing)}")
    return selected


def build_answer_index(answers_dir: Path) -> dict[int, list[Path]]:
    index: dict[int, list[Path]] = {}
    for path in sorted(answers_dir.iterdir()):
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        for exercise_no in parse_answer_image_range(path):
            index.setdefault(exercise_no, []).append(path)
    return index


def matching_answer_images(exercise_numbers: set[int], answer_index: dict[int, list[Path]]) -> list[Path]:
    seen: set[Path] = set()
    images: list[Path] = []
    for exercise_no in sorted(exercise_numbers):
        for path in answer_index.get(exercise_no, []):
            if path not in seen:
                seen.add(path)
                images.append(path)
    return images


def enforce_image_limits(image_paths: list[Path], max_images: int, max_base64_chars: int) -> tuple[list[Path], list[str]]:
    selected: list[Path] = []
    skipped: list[str] = []
    for image_path in image_paths:
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
    parser.add_argument("--chunks-json", type=Path, required=True, help="chunks.json produced by extract_arrangement_kg.py")
    parser.add_argument("--answers-dir", type=Path, required=True, help="Directory containing exercise answer images")
    parser.add_argument("-o", "--output-dir", type=Path, required=True, help="Output directory")
    parser.add_argument("--env-file", type=Path, default=Path(".env"), help="Path to .env")
    parser.add_argument("--chunk-id", action="append", default=[], help="Chunk id to reprocess; repeatable")
    parser.add_argument("--review-context-chars", type=int, default=900)
    parser.add_argument("--max-images", type=int, default=5, help="Max answer images per request")
    parser.add_argument("--dry-run", action="store_true", help="Only build pairings; do not call the API")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    apply_env_file(args.env_file)
    model_limits = get_model_limits(os.environ.get("LLM_MODEL", ""))
    max_base64_chars = int(model_limits.get("vision_max_base64_chars", 10_000_000) or 10_000_000)
    chunks = load_chunks(args.chunks_json, args.chunk_id)
    answer_index = build_answer_index(args.answers_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    pairings: list[dict[str, Any]] = []
    for chunk in chunks:
        exercise_numbers = parse_chunk_exercises(str(chunk.get("text", "")))
        answer_images = matching_answer_images(exercise_numbers, answer_index)
        selected_images, skipped = enforce_image_limits(answer_images, args.max_images, max_base64_chars)
        pairings.append(
            {
                "chunk_id": chunk.get("chunk_id"),
                "exercise_numbers": sorted(exercise_numbers),
                "answer_images": [str(path) for path in selected_images],
                "skipped": skipped,
                "chars": len(str(chunk.get("text", ""))),
            }
        )

    (args.output_dir / "visual_answer_pairings.json").write_text(
        json.dumps(pairings, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    if args.dry_run:
        print(f"Dry run wrote {len(pairings)} visual-answer pairing(s) to {args.output_dir}")
        return 0

    client = VisionLLMClient()
    all_edges: list[dict[str, Any]] = []
    all_review_items: list[dict[str, Any]] = []
    discarded_total = {"definition_noise": 0, "practice_drill_noise": 0, "missing_visual_context": 0}
    chunk_reports: list[dict[str, Any]] = []

    for chunk, pairing in zip(chunks, pairings, strict=True):
        image_paths = [Path(path) for path in pairing["answer_images"]]
        if not image_paths:
            chunk_reports.append({**pairing, "edges": 0, "discarded_summary": discarded_total.copy(), "error": "no answer images"})
            print(f"{chunk['chunk_id']}: skipped, no matching answer images")
            continue
        result = client.chat_json_with_images(
            {
                "task": "visual_answer_reprocess",
                "chunk_id": chunk["chunk_id"],
                "page_hint": chunk.get("page_hint"),
                "exercise_numbers": pairing["exercise_numbers"],
                "answer_image_filenames": [path.name for path in image_paths],
                "text": chunk["text"],
                "instruction": "结合练习文字和答案图片，只提取可复用的吉他编曲知识图谱边；不要保存习题答案。",
            },
            image_paths,
        )
        edges, discarded = validate_edges(result, chunk)
        candidate_refs = [str(path) for path in image_paths]
        for edge in edges:
            edge["visual_answer_images"] = candidate_refs
        review_items = build_review_items(edges, chunk, candidate_refs, args.review_context_chars)
        for item in review_items:
            item["source_pass"] = "visual_answer_reprocess"
            item["exercise_numbers"] = pairing["exercise_numbers"]
        all_edges.extend(edges)
        all_review_items.extend(review_items)
        for key, value in discarded.items():
            discarded_total[key] += value
        chunk_reports.append({**pairing, "edges": len(edges), "discarded_summary": discarded})
        print(f"{chunk['chunk_id']}: {len(edges)} edge(s), images={len(image_paths)}")

    write_jsonl(args.output_dir / "arrangement_kg_edges.jsonl", all_edges)
    write_jsonl(args.output_dir / "arrangement_kg_review.jsonl", all_review_items)
    report = {
        "input": str(args.chunks_json),
        "answers_dir": str(args.answers_dir),
        "chunks": len(chunks),
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
    print(f"Wrote {len(all_edges)} visual-answer edge(s) to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
