#!/usr/bin/env python
"""Extract high-value guitar arrangement KG edges from Markdown chunks.

This is intentionally not an OCR typo cleaner. Chinese-native LLMs are expected
to tolerate OCR noise while the prompt filters textbook filler, definitions,
and practice drills.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_KG_MAX_CHARS_PER_CHUNK = 12000

KNOWN_MODEL_LIMITS: dict[str, dict[str, int]] = {
    "qwen3.6-plus": {
        "context_length": 1_000_000,
        "max_input_tokens": 991_000,
        "thinking_max_input_tokens": 983_000,
        "max_output_tokens": 64_000,
        "thinking_max_output_tokens": 64_000,
        "max_reasoning_tokens": 80_000,
        "rpm": 30_000,
        "tpm": 5_000_000,
        "vision_max_images": 256,
        "vision_max_base64_images": 250,
        "vision_max_pixels": 16_000_000,
        "vision_max_base64_chars": 10_000_000,
    }
}


SYSTEM_PROMPT = """你是一位现代吉他编曲知识图谱构建专家。

你将阅读吉他/乐理教材片段，并只提取对 AI 吉他编曲 Copilot 有价值的知识图谱边。

核心目标：
提取“经验法则（heuristics）”“色彩映射”“吉他指板/物理限制/编曲避坑”，而不是提取百科定义或教学练习。

绝对过滤：
1. 拒绝基础定义：不要提取和弦构成音、音阶公式、品位/琴弦等基础名词解释，除非它直接服务于编曲决策。
2. 拒绝练习指令：不要提取节拍器速度、画图、填空、背诵、练习次数、肌肉记忆训练。
3. 拒绝无证据谱例：如果文本只说“如下图/如谱例所示”但没有文字描述具体和弦、弦号、品位、声部或用途，不能编造；图片占位或文件名只用于定位证据，不能当作视觉内容本身；若仍有弱价值，confidence 必须 < 0.5，并写 [Missing Visual Context]。
4. 忽略 OCR 噪声：自动理解明显 OCR 错别字，但不要把乱码写进标准节点 ID。
5. 拒绝正确的废话：LLM 已知的普通乐理，不进入图谱。

编曲语境改写：
教材常把有价值的指板/指法约束写成“演奏建议”或“练习建议”。如果该建议能直接影响 riff 编配、独奏线编写、声部连接、和弦省略音或吉他可演奏性，应保留，但必须主动改写为编曲语境：
1. context_condition 不要写成“演奏某音程/练习某指型”，而要写成“编配 riff/独奏乐句/吉他声部/和弦 voicing 时”。
2. review_note 必须说明它如何影响编曲选择，例如：规避复杂跨弦、简化指法、选择更顺手的把位、使用滑音/击勾弦/交替指法、避免低频浑浊或跨度过大。
3. target 应优先落到可复用的编曲启发或吉他语汇节点，如 guitar_idiom:string_crossing_riff_design、heuristic:riff_playability、technique:omit_5th_for_space，而不是泛泛的 performance/practice 建议。
4. 如果内容只服务于手指训练、找音练习或肌肉记忆，且不能转化为 riff/独奏/voicing 的编曲决策，仍然丢弃。

只提取三类：
1. ColorEmotion：某种和弦、音阶、声部、奏法、音色在某语境下产生的听感/情绪/风格指向。
2. GuitarIdiom：吉他特有的指板语汇、开放弦、把位、弦组、省略音、可弹性、声部连接。
3. Caution：编曲/音色/频段/演奏场景中的避坑规则。

输出必须是 JSON 对象：
{
  "edges": [
    {
      "source": "标准节点ID，如 technique:let_ring / chord:maj13 / concept:string_set",
      "relation": "evokes | can_inspire | suggests | enables | constrains | conflicts_with | cautions",
      "target": "标准节点ID，如 color:bright_lush / pattern:pedal_tone / caution:muddy_distortion",
      "knowledge_type": "ColorEmotion | GuitarIdiom | Caution",
      "confidence": 0.0,
      "context_condition": "触发该知识的编曲语境",
      "review_note": "用自己的话说明教材中真正有价值的编曲原则",
      "evidence": "教材片段中的短证据，不超过50字",
      "needs_visual_context": false
    }
  ],
  "discarded_summary": {
    "definition_noise": 0,
    "practice_drill_noise": 0,
    "missing_visual_context": 0
  }
}

如果片段没有高价值编曲知识，返回 {"edges": [], "discarded_summary": {...}}。
"""


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
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


class LLMClient:
    def __init__(self) -> None:
        self.base_url = os.environ.get("LLM_API_BASE_URL", "").rstrip("/")
        self.api_key = os.environ.get("LLM_API_KEY", "")
        self.model = os.environ.get("LLM_MODEL", "")
        self.temperature = float(os.environ.get("LLM_TEMPERATURE", "0"))
        self.timeout = int(os.environ.get("LLM_TIMEOUT_SECONDS", "60"))
        self.max_retries = int(os.environ.get("LLM_MAX_RETRIES", "2"))
        self.max_output_tokens = int(os.environ.get("LLM_MAX_OUTPUT_TOKENS", "0") or 0)
        self.enable_thinking = os.environ.get("LLM_ENABLE_THINKING", "false").strip().lower() == "true"
        if not self.base_url or not self.model:
            raise ValueError("LLM_API_BASE_URL and LLM_MODEL must be set in .env")

    def chat_json(self, payload: dict[str, Any]) -> dict[str, Any]:
        request_payload = {
            "model": self.model,
            "temperature": self.temperature,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
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


def normalize_markdown(text: str) -> str:
    text = re.sub(r"<!--\s*page:\s*(\d+)\s*-->", r"\n\n[PAGE:\1]\n\n", text)
    text = re.sub(r"!\[[^\]]*\]\(([^)]+)\)", r"[IMAGE_BLOCK:\1]", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_chunks(text: str, max_chars: int) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    current_lines: list[str] = []
    current_page: int | None = None
    chunk_index = 1

    def flush() -> None:
        nonlocal current_lines, chunk_index
        body = "\n".join(current_lines).strip()
        if body:
            image_refs = re.findall(r"\[IMAGE_BLOCK:([^\]]+)\]", body)
            chunks.append(
                {
                    "chunk_id": f"chunk_{chunk_index:04d}",
                    "page_hint": current_page,
                    "text": body,
                    "image_refs": image_refs,
                }
            )
            chunk_index += 1
        current_lines = []

    for line in normalize_markdown(text).splitlines():
        page_match = re.match(r"\[PAGE:(\d+)\]", line.strip())
        if page_match:
            current_page = int(page_match.group(1))
        if line.startswith("#") and sum(len(x) + 1 for x in current_lines) > max_chars * 0.45:
            flush()
        current_lines.append(line)
        if sum(len(x) + 1 for x in current_lines) >= max_chars:
            flush()
    flush()
    return chunks


def validate_edges(result: dict[str, Any], chunk: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    edges = result.get("edges", [])
    if not isinstance(edges, list):
        edges = []
    clean_edges: list[dict[str, Any]] = []
    allowed_relations = {
        "evokes",
        "can_inspire",
        "suggests",
        "enables",
        "constrains",
        "conflicts_with",
        "cautions",
    }
    allowed_types = {"ColorEmotion", "GuitarIdiom", "Caution"}

    for edge in edges:
        if not isinstance(edge, dict):
            continue
        source = str(edge.get("source", "")).strip()
        target = str(edge.get("target", "")).strip()
        relation = str(edge.get("relation", "")).strip()
        knowledge_type = str(edge.get("knowledge_type", "")).strip()
        if not source or not target or relation not in allowed_relations or knowledge_type not in allowed_types:
            continue
        try:
            confidence = float(edge.get("confidence", 0.5))
        except (TypeError, ValueError):
            confidence = 0.5
        confidence = max(0.0, min(1.0, confidence))
        clean_edges.append(
            {
                "source": source,
                "relation": relation,
                "target": target,
                "knowledge_type": knowledge_type,
                "confidence": confidence,
                "context_condition": str(edge.get("context_condition", "")),
                "review_note": str(edge.get("review_note", "")),
                "evidence": str(edge.get("evidence", ""))[:80],
                "needs_visual_context": bool(edge.get("needs_visual_context", False)),
                "chunk_id": chunk["chunk_id"],
                "page_hint": chunk.get("page_hint"),
            }
        )

    discarded = result.get("discarded_summary", {})
    if not isinstance(discarded, dict):
        discarded = {}
    clean_discarded = {
        "definition_noise": int(discarded.get("definition_noise", 0) or 0),
        "practice_drill_noise": int(discarded.get("practice_drill_noise", 0) or 0),
        "missing_visual_context": int(discarded.get("missing_visual_context", 0) or 0),
    }
    return clean_edges, clean_discarded


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def make_review_context(text: str, evidence: str, max_chars: int) -> str:
    normalized = re.sub(r"\s+", " ", text).strip()
    if max_chars <= 0 or len(normalized) <= max_chars:
        return normalized

    evidence = re.sub(r"\s+", " ", evidence).strip()
    if evidence:
        index = normalized.find(evidence)
        if index >= 0:
            half = max_chars // 2
            start = max(0, index - half)
            end = min(len(normalized), index + len(evidence) + half)
            context = normalized[start:end].strip()
            prefix = "..." if start > 0 else ""
            suffix = "..." if end < len(normalized) else ""
            return f"{prefix}{context}{suffix}"

    return normalized[:max_chars].strip() + "..."


def build_review_items(
    edges: list[dict[str, Any]],
    chunk: dict[str, Any],
    candidate_image_refs: list[str],
    max_context_chars: int,
) -> list[dict[str, Any]]:
    review_items: list[dict[str, Any]] = []
    for edge in edges:
        review_item = {
            "review_id": f"{chunk['chunk_id']}:{len(review_items) + 1:03d}",
            "review_status": "pending",
            "decision": "",
            "reject_reason": "",
            "chunk_id": chunk["chunk_id"],
            "page_hint": chunk.get("page_hint"),
            "source": edge["source"],
            "relation": edge["relation"],
            "target": edge["target"],
            "knowledge_type": edge["knowledge_type"],
            "confidence": edge["confidence"],
            "context_condition": edge.get("context_condition", ""),
            "review_note": edge.get("review_note", ""),
            "evidence": edge.get("evidence", ""),
            "evidence_context": make_review_context(chunk["text"], edge.get("evidence", ""), max_context_chars),
            "needs_visual_context": edge.get("needs_visual_context", False),
            "candidate_image_refs": candidate_image_refs,
        }
        review_items.append(review_item)
    return review_items


def get_model_limits(model: str) -> dict[str, int]:
    limits = KNOWN_MODEL_LIMITS.get(model, {}).copy()
    env_to_limit = {
        "LLM_CONTEXT_LENGTH": "context_length",
        "LLM_MAX_INPUT_TOKENS": "max_input_tokens",
        "LLM_MAX_OUTPUT_TOKENS": "max_output_tokens",
        "LLM_RPM": "rpm",
        "LLM_TPM": "tpm",
        "LLM_VISION_MAX_IMAGES": "vision_max_images",
        "LLM_VISION_MAX_BASE64_IMAGES": "vision_max_base64_images",
        "LLM_VISION_MAX_PIXELS": "vision_max_pixels",
        "LLM_VISION_MAX_BASE64_CHARS": "vision_max_base64_chars",
    }
    for env_key, limit_key in env_to_limit.items():
        raw_value = os.environ.get(env_key, "")
        if raw_value:
            limits[limit_key] = int(raw_value)
    return limits


def select_candidate_image_refs(chunk: dict[str, Any], model_limits: dict[str, int]) -> list[str]:
    model_max_images = int(model_limits.get("vision_max_images", 0) or 0)
    project_max_images = int(os.environ.get("KG_MAX_IMAGES_PER_REQUEST", "5") or 5)
    max_images = min(model_max_images, project_max_images) if model_max_images > 0 else project_max_images
    image_refs = list(chunk.get("image_refs", []) or [])
    if max_images <= 0:
        return image_refs
    return image_refs[:max_images]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-i", "--input", type=Path, required=True, help="Markdown file")
    parser.add_argument("-o", "--output-dir", type=Path, required=True, help="Output directory")
    parser.add_argument("--env-file", type=Path, default=Path(".env"), help="Path to .env")
    parser.add_argument(
        "--max-chars",
        type=int,
        default=0,
        help=(
            "Approximate max chars per chunk. Defaults to KG_MAX_CHARS_PER_CHUNK "
            f"or {DEFAULT_KG_MAX_CHARS_PER_CHUNK}."
        ),
    )
    parser.add_argument("--max-chunks", type=int, default=0, help="Limit chunks for testing; 0 means all")
    parser.add_argument(
        "--start-chunk",
        type=int,
        default=1,
        help="1-based chunk index to start from after splitting",
    )
    parser.add_argument(
        "--review-context-chars",
        type=int,
        default=900,
        help="Maximum nearby text context stored per edge in arrangement_kg_review.jsonl",
    )
    parser.add_argument("--dry-run", action="store_true", help="Only split chunks and write chunks.json; do not call the LLM API")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    apply_env_file(args.env_file)
    text = args.input.read_text(encoding="utf-8")
    max_chars = args.max_chars or int(os.environ.get("KG_MAX_CHARS_PER_CHUNK", DEFAULT_KG_MAX_CHARS_PER_CHUNK))
    chunks = split_chunks(text, max_chars)
    if args.start_chunk < 1:
        raise ValueError("--start-chunk must be >= 1")
    if args.start_chunk > 1:
        chunks = chunks[args.start_chunk - 1 :]
    if args.max_chunks > 0:
        chunks = chunks[: args.max_chunks]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "chunks.json").write_text(json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.dry_run:
        report = {
            "input": str(args.input),
            "chunks": len(chunks),
            "max_chars": max_chars,
            "model": os.environ.get("LLM_MODEL", ""),
            "model_limits": get_model_limits(os.environ.get("LLM_MODEL", "")),
            "dry_run": True,
            "edges": 0,
        }
        (args.output_dir / "arrangement_kg_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Dry run wrote {len(chunks)} chunks to {args.output_dir}")
        return 0

    client = LLMClient()
    model_limits = get_model_limits(client.model)
    all_edges: list[dict[str, Any]] = []
    all_review_items: list[dict[str, Any]] = []
    discarded_total = {"definition_noise": 0, "practice_drill_noise": 0, "missing_visual_context": 0}
    chunk_reports: list[dict[str, Any]] = []

    for chunk in chunks:
        candidate_image_refs = select_candidate_image_refs(chunk, model_limits)
        result = client.chat_json(
            {
                "chunk_id": chunk["chunk_id"],
                "page_hint": chunk.get("page_hint"),
                "text": chunk["text"],
                "candidate_image_refs": candidate_image_refs,
                "omitted_image_refs_count": max(0, len(chunk.get("image_refs", []) or []) - len(candidate_image_refs)),
                "model_limits": model_limits,
            }
        )
        edges, discarded = validate_edges(result, chunk)
        all_edges.extend(edges)
        review_items = build_review_items(edges, chunk, candidate_image_refs, args.review_context_chars)
        all_review_items.extend(review_items)
        for key, value in discarded.items():
            discarded_total[key] += value
        chunk_reports.append(
            {
                "chunk_id": chunk["chunk_id"],
                "page_hint": chunk.get("page_hint"),
                "chars": len(chunk["text"]),
                "image_refs": len(chunk.get("image_refs", [])),
                "candidate_image_refs": len(candidate_image_refs),
                "edges": len(edges),
                "discarded_summary": discarded,
            }
        )
        print(f"{chunk['chunk_id']}: {len(edges)} edge(s)")

    write_jsonl(args.output_dir / "arrangement_kg_edges.jsonl", all_edges)
    write_jsonl(args.output_dir / "arrangement_kg_review.jsonl", all_review_items)
    report = {
        "input": str(args.input),
        "chunks": len(chunks),
        "max_chars": max_chars,
        "review_context_chars": args.review_context_chars,
        "model": client.model,
        "model_limits": model_limits,
        "edges": len(all_edges),
        "review_items": len(all_review_items),
        "discarded_summary": discarded_total,
        "chunk_reports": chunk_reports,
    }
    (args.output_dir / "arrangement_kg_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(all_edges)} edges to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
