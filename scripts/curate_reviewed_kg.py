#!/usr/bin/env python
"""Curate reviewed KG edges into a local import-ready knowledge store."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ALLOWED_RELATIONS = {
    "evokes",
    "can_inspire",
    "suggests",
    "enables",
    "constrains",
    "conflicts_with",
    "cautions",
}
ALLOWED_TYPES = {"ColorEmotion", "GuitarIdiom", "Caution"}

REVISE_PROMPT = """你是吉他编曲知识图谱审稿助手。

你会收到一条已人工标记为 revise 的图谱边、原始教材证据、以及人工修改意见。

任务：
1. 严格服从人工修改意见。
2. 只输出一条更适合“编曲建议知识库”的图谱边。
3. 不要把纯演奏练习、指板训练或基础乐理作为图谱目标。
4. 如果人工意见说明应保存为 riff/编曲手法，就把 context_condition 和 review_note 改成编曲语境，而不是练习语境。
5. 保留短证据，不超过 80 字。
6. 对教材中的“演奏/练习建议”，只有在能转化为 riff 编配、独奏线编写、声部连接、和弦 voicing 或吉他可演奏性决策时才保留；此时 context_condition 必须写成“编配 riff/独奏乐句/吉他声部/和弦 voicing 时”等编曲语境。
7. target 应优先使用可复用的编曲启发或吉他语汇节点，例如 guitar_idiom:string_crossing_riff_design、heuristic:riff_playability、technique:omit_5th_for_space，而不是泛泛的 performance/practice 建议。

输出 JSON 对象：
{
  "edge": {
    "source": "标准节点ID",
    "relation": "evokes | can_inspire | suggests | enables | constrains | conflicts_with | cautions",
    "target": "标准节点ID",
    "knowledge_type": "ColorEmotion | GuitarIdiom | Caution",
    "confidence": 0.0,
    "context_condition": "编曲语境",
    "review_note": "面向编曲 Copilot 的知识说明",
    "evidence": "短证据",
    "needs_visual_context": false
  }
}
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


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_no}: {exc}") from exc
            if isinstance(row, dict):
                rows.append(row)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def extract_json_object(text: str) -> dict[str, Any]:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def edge_from_review(row: dict[str, Any], *, revision_status: str) -> dict[str, Any]:
    return {
        "source": str(row.get("source", "")).strip(),
        "relation": str(row.get("relation", "")).strip(),
        "target": str(row.get("target", "")).strip(),
        "knowledge_type": str(row.get("knowledge_type", "")).strip(),
        "confidence": float(row.get("confidence", 0.5) or 0.5),
        "context_condition": str(row.get("context_condition", "")).strip(),
        "review_note": str(row.get("review_note", "")).strip(),
        "evidence": str(row.get("evidence", "")).strip()[:80],
        "needs_visual_context": bool(row.get("needs_visual_context", False)),
        "provenance": {
            "review_id": row.get("review_id"),
            "chunk_id": row.get("chunk_id"),
            "page_hint": row.get("page_hint"),
            "review_decision": row.get("decision"),
            "revision_status": revision_status,
        },
    }


def validate_edge(edge: dict[str, Any]) -> dict[str, Any]:
    source = str(edge.get("source", "")).strip()
    relation = str(edge.get("relation", "")).strip()
    target = str(edge.get("target", "")).strip()
    knowledge_type = str(edge.get("knowledge_type", "")).strip()
    if not source or not target:
        raise ValueError("edge source/target is required")
    if relation not in ALLOWED_RELATIONS:
        raise ValueError(f"invalid relation: {relation}")
    if knowledge_type not in ALLOWED_TYPES:
        raise ValueError(f"invalid knowledge_type: {knowledge_type}")
    try:
        confidence = float(edge.get("confidence", 0.5))
    except (TypeError, ValueError):
        confidence = 0.5
    edge["source"] = source
    edge["relation"] = relation
    edge["target"] = target
    edge["knowledge_type"] = knowledge_type
    edge["confidence"] = max(0.0, min(1.0, confidence))
    edge["context_condition"] = str(edge.get("context_condition", "")).strip()
    edge["review_note"] = str(edge.get("review_note", "")).strip()
    edge["evidence"] = str(edge.get("evidence", "")).strip()[:80]
    edge["needs_visual_context"] = bool(edge.get("needs_visual_context", False))
    return edge


class LLMClient:
    def __init__(self) -> None:
        self.base_url = os.environ.get("LLM_API_BASE_URL", "").rstrip("/")
        self.api_key = os.environ.get("LLM_API_KEY", "")
        self.model = os.environ.get("LLM_MODEL", "")
        self.timeout = int(os.environ.get("LLM_TIMEOUT_SECONDS", "120"))
        self.max_retries = int(os.environ.get("LLM_MAX_RETRIES", "2"))
        if not self.base_url or not self.model:
            raise ValueError("LLM_API_BASE_URL and LLM_MODEL must be set")

    def revise_edge(self, row: dict[str, Any]) -> dict[str, Any]:
        payload = {
            "human_revision_note": row.get("reject_reason", ""),
            "original_edge": {
                "source": row.get("source"),
                "relation": row.get("relation"),
                "target": row.get("target"),
                "knowledge_type": row.get("knowledge_type"),
                "confidence": row.get("confidence"),
                "context_condition": row.get("context_condition"),
                "review_note": row.get("review_note"),
                "evidence": row.get("evidence"),
                "needs_visual_context": row.get("needs_visual_context"),
            },
            "evidence_context": row.get("evidence_context", ""),
        }
        request_payload = {
            "model": self.model,
            "temperature": 0,
            "response_format": {"type": "json_object"},
            "enable_thinking": False,
            "messages": [
                {"role": "user", "content": REVISE_PROMPT + "\n\n" + json.dumps(payload, ensure_ascii=False)},
            ],
        }
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
                result = extract_json_object(data["choices"][0]["message"]["content"])
                return validate_edge(result["edge"])
            except (urllib.error.URLError, urllib.error.HTTPError, KeyError, json.JSONDecodeError, ValueError) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(1.5 * (attempt + 1))
        raise RuntimeError(f"LLM revision failed: {last_error}")


def dedupe_edges(edges: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str, str, str]] = set()
    deduped: list[dict[str, Any]] = []
    for edge in edges:
        key = (
            str(edge.get("source", "")),
            str(edge.get("relation", "")),
            str(edge.get("target", "")),
            str(edge.get("context_condition", "")),
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(edge)
    return deduped


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-jsonl", type=Path, required=True, help="Reviewed arrangement_kg_review.jsonl")
    parser.add_argument("--output-dir", type=Path, required=True, help="Curated KG output directory")
    parser.add_argument("--env-file", type=Path, default=Path(".env"), help="Path to .env")
    parser.add_argument("--fix-revise", action="store_true", help="Call LLM to fix revise items")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    apply_env_file(args.env_file)
    rows = read_jsonl(args.review_jsonl)
    client = LLMClient() if args.fix_revise else None

    accepted_edges: list[dict[str, Any]] = []
    revised_edges: list[dict[str, Any]] = []
    rejected_rows: list[dict[str, Any]] = []
    pending_rows: list[dict[str, Any]] = []

    for row in rows:
        decision = str(row.get("decision", "")).strip()
        if decision == "accept":
            accepted_edges.append(validate_edge(edge_from_review(row, revision_status="accepted")))
        elif decision == "revise":
            if client is None:
                pending_rows.append(row)
                continue
            revised = client.revise_edge(row)
            revised["provenance"] = {
                "review_id": row.get("review_id"),
                "chunk_id": row.get("chunk_id"),
                "page_hint": row.get("page_hint"),
                "review_decision": row.get("decision"),
                "human_revision_note": row.get("reject_reason"),
                "revision_status": "llm_revised",
            }
            revised_edges.append(revised)
        elif decision == "reject":
            rejected_rows.append(row)
        else:
            pending_rows.append(row)

    curated_edges = dedupe_edges(accepted_edges + revised_edges)
    ingested_at = datetime.now(timezone.utc).isoformat()
    for edge in curated_edges:
        edge.setdefault("provenance", {})
        edge["provenance"]["ingested_at"] = ingested_at
        edge["provenance"]["source_review_file"] = str(args.review_jsonl)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "edges.jsonl", curated_edges)
    write_jsonl(args.output_dir / "accepted_edges.jsonl", accepted_edges)
    write_jsonl(args.output_dir / "revised_edges.jsonl", revised_edges)
    write_jsonl(args.output_dir / "rejected_review_items.jsonl", rejected_rows)
    write_jsonl(args.output_dir / "pending_review_items.jsonl", pending_rows)

    report = {
        "review_file": str(args.review_jsonl),
        "output_dir": str(args.output_dir),
        "accepted": len(accepted_edges),
        "revised": len(revised_edges),
        "rejected": len(rejected_rows),
        "pending": len(pending_rows),
        "curated_edges": len(curated_edges),
        "ingested_at": ingested_at,
    }
    (args.output_dir / "curation_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
