#!/usr/bin/env python
"""Extract math-rock / Midwest emo guitar KG edges from transcript text."""

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

DEFAULT_MAX_CHARS_PER_CHUNK = 9000

SYSTEM_PROMPT = """你是一位现代吉他编曲知识图谱构建专家，专门处理 math rock / Midwest emo 吉他教程。

你将阅读一段英文视频课 ASR/OCR 转写。文本可能存在大量错词和断句问题。请自动纠正常见噪声：
- cord/quartz/core = chord
- rift/rif = riff
- stream/street/ring/shrink = string
- threat/fred/front/fret = fret
- dad gad / dad gatt = DADGAD
- shooting/chining = tuning
- pal court/pal corn/power quarter = power chord
- suspended quartz/god = suspended chord
- base = bass
- slap/pop/dead note/percussive slap = percussive articulation / dead-note attack
- ha ron/hammer onto = hammer-on
- pool off/pouring off = pull-off
- tap/tats = tapping
- melody/singing voice = top-line melody

项目最终目标：
本地解析 .gp5 吉他谱，得到调弦、BPM、拍号、节奏分组、riff 特征、和声进行、调性、分段、奏法线索，然后让 LLM 匹配知识库并给出吉他编配分析和建议。

只提取能帮助这个目标的知识。优先保留：
1. Math rock / Midwest emo 的特殊调弦策略，如 DADGAD、open/minor/add9/sus tuning。
2. 开放弦 common tone / ringing open strings / pedal tone 如何支撑可移动和弦形状。
3. tapping power chords、two-hand tapping、tap + pull-off to open string、tapped melodic top-line。
4. hammer-on / pull-off / slide / harmonics / slap-pop / dead note 与 riff 编配的关系。
5. odd grouping、3+4、triplets、32nd-note bursts、非四平方整乐句如何制造 math rock 感。
6. 同一和弦进行通过主题扩展：简单 fingerpicking -> strumming/power chord -> technical tapping/fill 的层级构建。
7. 可以由 .gp5 特征触发的规则，例如 alternate_tuning、open_string_drone、tapped_dyads、nonstandard_meter_grouping、high_hammer_pull_density。

过滤：
1. 不抽普通和声定义或逐音教学口播，除非它能改写为吉他编配决策。
2. 不保存完整练习答案、逐品位流水账、无抽象价值的具体谱例。
3. 如果只是说明“这里弹几品几弦”，必须抽象成可复用的 riff/调弦/奏法/编配规则。
4. 跳过营销、寒暄、纯练习提醒。

节点命名建议：
- style:math_rock, style:midwest_emo
- task:math_rock_riff_writing, task:alternate_tuning_arrangement
- feature:alternate_tuning, feature:open_string_drone, feature:common_tone_top_strings
- feature:tapped_power_chords, feature:odd_grouping, feature:hammer_pull_density
- technique:two_hand_tapping, technique:tapped_power_chord, technique:percussive_slap
- technique:harp_harmonics, technique:slide_to_open_string_pulloff
- tuning:DADGAD, tuning:open_minor_add9, tuning:DAEACsharpE
- heuristic:ringing_open_string_anchor, heuristic:theme_variation_layering
- caution:tuning_specific_shape_dependency, caution:overly_literal_fret_sequence
- color:jangly_open_midwest_emo, color:angular_math_rock_momentum

输出必须是 JSON 对象：
{
  "edges": [
    {
      "source": "标准节点ID",
      "relation": "evokes | can_inspire | suggests | enables | constrains | conflicts_with | cautions",
      "target": "标准节点ID",
      "knowledge_type": "ColorEmotion | GuitarIdiom | Caution",
      "confidence": 0.0,
      "context_condition": "触发该知识的乐谱/编配语境",
      "review_note": "面向吉他编曲 Copilot 的规则说明",
      "evidence": "短证据，不超过50字",
      "gp5_feature_triggers": ["可从 .gp5 或 MIDI/谱面分析得到的触发特征"],
      "style_tags": ["math_rock", "midwest_emo"]
    }
  ],
  "discarded_summary": {
    "theory_noise": 0,
    "practice_drill_noise": 0,
    "asr_noise": 0,
    "fret_by_fret_noise": 0
  }
}

如果片段没有高价值吉他编配知识，返回 {"edges": [], "discarded_summary": {...}}。
"""

HEADING_RE = re.compile(r"^(?P<title>tutorial\s+\d+.*)$", re.IGNORECASE)


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
        self.timeout = int(os.environ.get("LLM_TIMEOUT_SECONDS", "120"))
        self.max_retries = int(os.environ.get("LLM_MAX_RETRIES", "2"))
        self.max_output_tokens = int(os.environ.get("LLM_MAX_OUTPUT_TOKENS", "0") or 0)
        self.enable_thinking = os.environ.get("LLM_ENABLE_THINKING", "false").strip().lower() == "true"
        if not self.base_url or not self.model:
            raise ValueError("LLM_API_BASE_URL and LLM_MODEL must be set in .env")

    def chat_json(self, payload: dict[str, Any]) -> dict[str, Any]:
        request_payload: dict[str, Any] = {
            "model": self.model,
            "temperature": self.temperature,
            "response_format": {"type": "json_object"},
            "enable_thinking": self.enable_thinking,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ],
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


def normalize_text(text: str) -> str:
    text = text.replace("\ufeff", "")
    text = re.sub(r"\bnbsp\b", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_long_section(section: dict[str, Any], max_chars: int, start_index: int) -> tuple[list[dict[str, Any]], int]:
    text = section["text"].strip()
    if len(text) <= max_chars:
        section["chunk_id"] = f"chunk_{start_index:04d}"
        return [section], start_index + 1

    sentences = re.split(r"(?<=[。！？.!?])\s+", text)
    chunks: list[dict[str, Any]] = []
    current: list[str] = []
    part = 1
    chunk_index = start_index
    for sentence in sentences:
        if current and sum(len(x) + 1 for x in current) + len(sentence) > max_chars:
            chunks.append(
                {
                    "chunk_id": f"chunk_{chunk_index:04d}",
                    "lesson_title": f"{section['lesson_title']} / part {part}",
                    "text": " ".join(current).strip(),
                }
            )
            chunk_index += 1
            part += 1
            current = []
        current.append(sentence)
    if current:
        chunks.append(
            {
                "chunk_id": f"chunk_{chunk_index:04d}",
                "lesson_title": f"{section['lesson_title']} / part {part}",
                "text": " ".join(current).strip(),
            }
        )
        chunk_index += 1
    return chunks, chunk_index


def split_chunks(text: str, max_chars: int) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    title = "untitled"
    lines: list[str] = []

    def flush() -> None:
        nonlocal lines
        body = "\n".join(lines).strip()
        if body:
            sections.append({"lesson_title": title, "text": body})
        lines = []

    for raw_line in normalize_text(text).splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = HEADING_RE.match(line)
        if match:
            flush()
            title = match.group("title").strip()
            continue
        lines.append(line)
    flush()

    chunks: list[dict[str, Any]] = []
    chunk_index = 1
    for section in sections:
        pieces, chunk_index = split_long_section(section, max_chars, chunk_index)
        chunks.extend(pieces)
    return chunks


def int_from_summary(summary: dict[str, Any], key: str) -> int:
    try:
        return int(summary.get(key, 0) or 0)
    except (TypeError, ValueError):
        return 0


def validate_edges(result: dict[str, Any], chunk: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    allowed_relations = {"evokes", "can_inspire", "suggests", "enables", "constrains", "conflicts_with", "cautions"}
    allowed_types = {"ColorEmotion", "GuitarIdiom", "Caution"}
    raw_edges = result.get("edges", [])
    if not isinstance(raw_edges, list):
        raw_edges = []
    edges: list[dict[str, Any]] = []
    for edge in raw_edges:
        if not isinstance(edge, dict):
            continue
        source = str(edge.get("source", "")).strip()
        relation = str(edge.get("relation", "")).strip()
        target = str(edge.get("target", "")).strip()
        knowledge_type = str(edge.get("knowledge_type", "")).strip()
        if not source or not target or relation not in allowed_relations or knowledge_type not in allowed_types:
            continue
        try:
            confidence = float(edge.get("confidence", 0.5))
        except (TypeError, ValueError):
            confidence = 0.5
        triggers = edge.get("gp5_feature_triggers", [])
        tags = edge.get("style_tags", [])
        edges.append(
            {
                "source": source,
                "relation": relation,
                "target": target,
                "knowledge_type": knowledge_type,
                "confidence": max(0.0, min(1.0, confidence)),
                "context_condition": str(edge.get("context_condition", "")).strip(),
                "review_note": str(edge.get("review_note", "")).strip(),
                "evidence": str(edge.get("evidence", "")).strip()[:80],
                "needs_visual_context": False,
                "gp5_feature_triggers": triggers if isinstance(triggers, list) else [],
                "style_tags": tags if isinstance(tags, list) else [],
                "chunk_id": chunk["chunk_id"],
                "lesson_title": chunk.get("lesson_title", ""),
            }
        )
    discarded = result.get("discarded_summary", {})
    if not isinstance(discarded, dict):
        discarded = {}
    return edges, {
        "theory_noise": int_from_summary(discarded, "theory_noise"),
        "practice_drill_noise": int_from_summary(discarded, "practice_drill_noise"),
        "asr_noise": int_from_summary(discarded, "asr_noise"),
        "fret_by_fret_noise": int_from_summary(discarded, "fret_by_fret_noise"),
    }


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
            return ("..." if start > 0 else "") + normalized[start:end].strip() + ("..." if end < len(normalized) else "")
    return normalized[:max_chars].strip() + "..."


def build_review_items(edges: list[dict[str, Any]], chunk: dict[str, Any], max_context_chars: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for edge in edges:
        rows.append(
            {
                "review_id": f"{chunk['chunk_id']}:mathrock_text:{len(rows) + 1:03d}",
                "review_status": "pending",
                "decision": "",
                "reject_reason": "",
                "chunk_id": chunk["chunk_id"],
                "page_hint": chunk.get("lesson_title"),
                "source": edge["source"],
                "relation": edge["relation"],
                "target": edge["target"],
                "knowledge_type": edge["knowledge_type"],
                "confidence": edge["confidence"],
                "context_condition": edge.get("context_condition", ""),
                "review_note": edge.get("review_note", ""),
                "evidence": edge.get("evidence", ""),
                "evidence_context": make_review_context(chunk["text"], edge.get("evidence", ""), max_context_chars),
                "needs_visual_context": False,
                "candidate_image_refs": [],
                "source_pass": "mathrock_text",
                "lesson_title": chunk.get("lesson_title", ""),
                "gp5_feature_triggers": edge.get("gp5_feature_triggers", []),
                "style_tags": edge.get("style_tags", []),
            }
        )
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-i", "--input", type=Path, required=True, help="Transcript text file")
    parser.add_argument("-o", "--output-dir", type=Path, required=True, help="Output directory")
    parser.add_argument("--env-file", type=Path, default=Path(".env"), help="Path to .env")
    parser.add_argument("--max-chars", type=int, default=0, help=f"Max chars per chunk; default {DEFAULT_MAX_CHARS_PER_CHUNK}")
    parser.add_argument("--start-chunk", type=int, default=1, help="1-based chunk index to start from")
    parser.add_argument("--max-chunks", type=int, default=0, help="Limit chunks; 0 means all")
    parser.add_argument("--review-context-chars", type=int, default=1200, help="Nearby text context stored per review item")
    parser.add_argument("--dry-run", action="store_true", help="Only split chunks and write chunks.json")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    apply_env_file(args.env_file)
    text = args.input.read_text(encoding="utf-8")
    max_chars = args.max_chars or int(os.environ.get("MATHROCK_KG_MAX_CHARS_PER_CHUNK", DEFAULT_MAX_CHARS_PER_CHUNK))
    chunks = split_chunks(text, max_chars)
    if args.start_chunk < 1:
        raise ValueError("--start-chunk must be >= 1")
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
            "dry_run": True,
            "edges": 0,
        }
        (args.output_dir / "mathrock_kg_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Dry run wrote {len(chunks)} chunks to {args.output_dir}")
        return 0

    client = LLMClient()
    all_edges: list[dict[str, Any]] = []
    all_review_items: list[dict[str, Any]] = []
    discarded_total = {"theory_noise": 0, "practice_drill_noise": 0, "asr_noise": 0, "fret_by_fret_noise": 0}
    chunk_reports: list[dict[str, Any]] = []
    for chunk in chunks:
        result = client.chat_json(
            {
                "chunk_id": chunk["chunk_id"],
                "lesson_title": chunk.get("lesson_title"),
                "text": chunk["text"],
                "extraction_focus": [
                    "math rock riff writing",
                    "midwest emo guitar",
                    "alternate tuning",
                    "open-string drones/common tones",
                    "tapping power chords",
                    "odd grouping / nonstandard meter feel",
                    ".gp5 feature triggers",
                ],
            }
        )
        edges, discarded = validate_edges(result, chunk)
        all_edges.extend(edges)
        all_review_items.extend(build_review_items(edges, chunk, args.review_context_chars))
        for key, value in discarded.items():
            discarded_total[key] += value
        chunk_reports.append(
            {
                "chunk_id": chunk["chunk_id"],
                "lesson_title": chunk.get("lesson_title"),
                "chars": len(chunk["text"]),
                "edges": len(edges),
                "discarded_summary": discarded,
            }
        )
        print(f"{chunk['chunk_id']} {chunk.get('lesson_title', '')}: {len(edges)} edge(s)")

    write_jsonl(args.output_dir / "mathrock_kg_edges.jsonl", all_edges)
    write_jsonl(args.output_dir / "arrangement_kg_review.jsonl", all_review_items)
    report = {
        "input": str(args.input),
        "chunks": len(chunks),
        "max_chars": max_chars,
        "review_context_chars": args.review_context_chars,
        "model": client.model,
        "edges": len(all_edges),
        "review_items": len(all_review_items),
        "discarded_summary": discarded_total,
        "chunk_reports": chunk_reports,
    }
    (args.output_dir / "mathrock_kg_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(all_edges)} edges to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
