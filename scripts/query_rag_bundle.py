#!/usr/bin/env python
"""Build an Agentic-ready RAG evidence bundle for a guitar arrangement query.

This script intentionally stops before final answer generation. It analyzes a
query, plans retrieval over text / visual-caption / KG tools, merges evidence,
judges sufficiency, and writes JSON + Markdown reports for debugging.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from local_text_embedding import DEFAULT_LOCAL_MODEL, LocalTransformerEmbedder


DEFAULT_CHROMA_PATH = ROOT / "data" / "chroma"
DEFAULT_REPORT_MD = ROOT / "data" / "eval" / "query_rag_bundle_report.md"
DEFAULT_REPORT_JSON = ROOT / "data" / "eval" / "query_rag_bundle_report.json"

COLLECTIONS = {
    "fretboard_text": "guitar_fretboard_handbook_text_qwen3_06b",
    "visual_caption": "guitar_fretboard_answer_captions_qwen3_06b",
    "style_text": "guitar_text_chunks_qwen3_06b",
}

TEXT_COLLECTIONS = {"fretboard_text", "style_text"}

FRETBOARD_TERMS = [
    "指板",
    "根音",
    "指型",
    "音阶",
    "琶音",
    "和弦",
    "音程",
    "品位",
    "琴弦",
    "大调",
    "小调",
    "五声音阶",
    "三和弦",
    "七和弦",
    "延伸和弦",
    "调式",
    "voicing",
    "arpeggio",
    "triad",
    "scale",
    "interval",
]

VISUAL_TERMS = [
    "图",
    "图示",
    "指法",
    "指型图",
    "和弦图",
    "答案图",
    "答案",
    "省略",
    "高把位",
    "低把位",
    "按法",
    "shape",
    "diagram",
    "voicing",
    "omit",
]

STYLE_KEYWORDS = {
    "funk": ["funk", "groove", "ghost", "muted", "chuck", "切分", "十六分", "律动", "消音"],
    "mathrock": ["mathrock", "math rock", "midwest", "DADGAD", "FACGCE", "tapping", "open string", "开放弦", "点弦", "奇数"],
    "blues": ["blues", "shuffle", "turnaround", "bending", "布鲁斯"],
    "metal": ["metal", "djent", "palm mute", "alternate picking", "金属"],
    "jazz": ["jazz", "ii-V-I", "shell voicing", "chord melody", "爵士"],
}

TECHNIQUE_TERMS = [
    "riff",
    "groove",
    "tapping",
    "点弦",
    "hammer",
    "pull",
    "slide",
    "滑音",
    "击弦",
    "勾弦",
    "muted",
    "ghost",
    "消音",
    "切分",
    "开放弦",
    "open string",
    "drone",
    "comping",
]

KG_TERMS = [
    "怎么",
    "如何",
    "建议",
    "发展",
    "迁移",
    "编配",
    "启发",
    "关系",
    "搭配",
    "冲突",
    "适合",
    "inspire",
    "arrange",
    "suggest",
]

CHORD_RE = re.compile(r"\b[A-G](?:#|b)?(?:maj|min|m|mi|dim|aug|sus|add)?\d*(?:[#b]\d+)?(?:/[A-G](?:#|b)?)?\b", re.I)
TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_+\-/'.#]*|\d+(?:\.\d+)?|[\u4e00-\u9fff]{2,}")


@dataclass
class QueryAnalysis:
    query: str
    intent: str
    style_hints: list[str] = field(default_factory=list)
    theory_terms: list[str] = field(default_factory=list)
    technique_terms: list[str] = field(default_factory=list)
    needs_fretboard_text: bool = False
    needs_visual: bool = False
    needs_style_text: bool = False
    needs_kg: bool = False
    confidence: float = 0.0
    matched_rules: list[str] = field(default_factory=list)


@dataclass
class SearchTask:
    name: str
    backend: str
    collection: str | None
    query: str
    top_k: int
    reason: str


@dataclass
class EvidenceItem:
    evidence_id: str
    evidence_type: str
    source_id: str
    title: str
    content: str
    score: float
    metadata: dict[str, Any] = field(default_factory=dict)
    trace: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvidenceBundle:
    query: str
    analysis: QueryAnalysis
    plan: list[SearchTask]
    text_evidence: list[EvidenceItem]
    visual_evidence: list[EvidenceItem]
    kg_evidence: list[EvidenceItem]
    judgement: dict[str, Any]
    answer_seed: dict[str, Any]
    timings: dict[str, float]


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


def as_list(value: Any) -> list[Any]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return parsed
        except json.JSONDecodeError:
            return [value]
    return [value]


def compact(text: str, limit: int = 600) -> str:
    text = " ".join(str(text or "").split())
    return text if len(text) <= limit else text[: limit - 1] + "..."


def query_tokens(query: str) -> set[str]:
    tokens = {token.lower() for token in TOKEN_RE.findall(query)}
    for term in FRETBOARD_TERMS + VISUAL_TERMS + TECHNIQUE_TERMS:
        if term.lower() in query.lower():
            tokens.add(term.lower())
    return {token for token in tokens if len(token) >= 2}


def has_any(query: str, terms: list[str]) -> bool:
    q = query.lower()
    return any(term.lower() in q for term in terms)


def infer_style_hints(query: str) -> list[str]:
    q = query.lower()
    hints = []
    for style, terms in STYLE_KEYWORDS.items():
        if any(term.lower() in q for term in terms):
            hints.append(style)
    return hints


def extract_theory_terms(query: str) -> list[str]:
    terms = set(CHORD_RE.findall(query))
    for term in FRETBOARD_TERMS:
        if term.lower() in query.lower():
            terms.add(term)
    return sorted(terms)


def extract_technique_terms(query: str) -> list[str]:
    q = query.lower()
    return sorted({term for term in TECHNIQUE_TERMS if term.lower() in q})


def analyze_query(query: str, context: dict[str, Any] | None = None) -> QueryAnalysis:
    context = context or {}
    style_hints = infer_style_hints(query)
    theory_terms = extract_theory_terms(query)
    technique_terms = extract_technique_terms(query)
    matched_rules: list[str] = []

    needs_fretboard_text = has_any(query, FRETBOARD_TERMS) or bool(theory_terms)
    if needs_fretboard_text:
        matched_rules.append("fretboard_terms")

    needs_visual = has_any(query, VISUAL_TERMS)
    if needs_visual:
        matched_rules.append("visual_terms")

    needs_style_text = bool(style_hints) or has_any(query, TECHNIQUE_TERMS)
    if needs_style_text:
        matched_rules.append("style_or_technique_terms")

    needs_kg = has_any(query, KG_TERMS) or bool(context.get("gp5_features"))
    if needs_kg:
        matched_rules.append("arrangement_or_relation_terms")

    if context.get("need_visual") is True:
        needs_visual = True
        matched_rules.append("context_need_visual")
    if context.get("preferred_style") and str(context["preferred_style"]) not in style_hints:
        style_hints.append(str(context["preferred_style"]))
        needs_style_text = True
        matched_rules.append("context_preferred_style")
    if context.get("gp5_features"):
        needs_style_text = True
        needs_kg = True
        matched_rules.append("context_gp5_features")

    if not any([needs_fretboard_text, needs_visual, needs_style_text, needs_kg]):
        needs_style_text = True
        needs_kg = True
        matched_rules.append("default_style_kg")

    if needs_fretboard_text and needs_style_text:
        intent = "mixed_arrangement" if needs_kg else "mixed_lookup"
    elif needs_visual:
        intent = "visual_voicing_lookup"
    elif needs_style_text and needs_kg:
        intent = "style_arrangement"
    elif needs_style_text:
        intent = "style_lookup"
    elif needs_fretboard_text:
        intent = "fretboard_lookup"
    else:
        intent = "kg_relation_lookup"

    confidence = min(0.95, 0.45 + 0.1 * len(matched_rules) + 0.05 * len(style_hints))
    return QueryAnalysis(
        query=query,
        intent=intent,
        style_hints=style_hints,
        theory_terms=theory_terms,
        technique_terms=technique_terms,
        needs_fretboard_text=needs_fretboard_text,
        needs_visual=needs_visual,
        needs_style_text=needs_style_text,
        needs_kg=needs_kg,
        confidence=round(confidence, 3),
        matched_rules=matched_rules,
    )


def plan_retrieval(analysis: QueryAnalysis, top_k: int) -> list[SearchTask]:
    tasks: list[SearchTask] = []
    if analysis.needs_fretboard_text:
        tasks.append(
            SearchTask(
                name="fretboard_text",
                backend="chroma",
                collection=COLLECTIONS["fretboard_text"],
                query=analysis.query,
                top_k=top_k,
                reason="指板/理论/练习题干证据",
            )
        )
    if analysis.needs_visual:
        visual_query = analysis.query
        if "图" not in visual_query and "voicing" not in visual_query.lower():
            visual_query += " 指型图 和弦图 voicing"
        tasks.append(
            SearchTask(
                name="visual_caption",
                backend="chroma",
                collection=COLLECTIONS["visual_caption"],
                query=visual_query,
                top_k=top_k,
                reason="具体图形/指法/voicing/答案图证据",
            )
        )
    if analysis.needs_style_text:
        style_query = analysis.query
        if analysis.style_hints:
            style_query += " " + " ".join(analysis.style_hints)
        tasks.append(
            SearchTask(
                name="style_text",
                backend="chroma",
                collection=COLLECTIONS["style_text"],
                query=style_query,
                top_k=top_k,
                reason="风格/riff/节奏/技法文本证据",
            )
        )
    if analysis.needs_kg:
        terms = " ".join(analysis.style_hints + analysis.theory_terms + analysis.technique_terms)
        kg_query = f"{analysis.query} {terms}".strip()
        tasks.append(
            SearchTask(
                name="kg",
                backend="neo4j_or_file",
                collection=None,
                query=kg_query,
                top_k=max(top_k, 8),
                reason="技法关系/风格迁移/编配启发",
            )
        )
    return tasks


def normalize_distance(distance: float | int | None) -> float:
    if distance is None:
        return 0.0
    return max(0.0, 1.0 - float(distance))


def token_boost(query: str, text: str) -> float:
    tokens = query_tokens(query)
    if not tokens:
        return 0.0
    blob = text.lower()
    matches = sum(1 for token in tokens if token in blob)
    return min(0.25, matches * 0.025)


def evidence_from_chroma_hit(
    task: SearchTask,
    item_id: str,
    document: str,
    metadata: dict[str, Any],
    distance: float,
    rank: int,
) -> EvidenceItem:
    source_id = str(metadata.get("source_id") or "")
    chunk_id = str(metadata.get("chunk_id") or metadata.get("segment_id") or metadata.get("visual_id") or item_id)
    title = str(
        metadata.get("source_title")
        or metadata.get("topic")
        or metadata.get("musical_object")
        or metadata.get("lesson_title")
        or task.name
    )
    score = normalize_distance(distance) + token_boost(task.query, document + " " + json.dumps(metadata, ensure_ascii=False))
    evidence_type = "visual_caption" if task.name == "visual_caption" else "text"
    return EvidenceItem(
        evidence_id=f"{evidence_type}:{chunk_id}",
        evidence_type=evidence_type,
        source_id=source_id,
        title=title,
        content=document,
        score=round(score, 5),
        metadata={
            "collection": task.collection,
            "chunk_id": chunk_id,
            "page_hint": metadata.get("page_hint") or metadata.get("page") or "",
            "exercise_number": metadata.get("exercise_number") or "",
            "subquestion_number": metadata.get("subquestion_number") or "",
            "image_path": metadata.get("image_path") or metadata.get("crop_path") or "",
            "style_tags": as_list(metadata.get("style_tags")),
            "raw_metadata": metadata,
        },
        trace={"rank": rank, "distance": distance, "task": asdict(task)},
    )


def search_chroma(
    client: Any,
    embedder: LocalTransformerEmbedder,
    task: SearchTask,
    batch_size: int,
) -> list[EvidenceItem]:
    if not task.collection:
        return []
    collection = client.get_collection(task.collection)
    embedding = embedder.embed([task.query], batch_size=batch_size)[0]
    result = collection.query(
        query_embeddings=[embedding],
        n_results=task.top_k,
        include=["documents", "metadatas", "distances"],
    )
    items: list[EvidenceItem] = []
    for rank, (item_id, document, metadata, distance) in enumerate(
        zip(
            result.get("ids", [[]])[0],
            result.get("documents", [[]])[0],
            result.get("metadatas", [[]])[0],
            result.get("distances", [[]])[0],
        ),
        start=1,
    ):
        items.append(evidence_from_chroma_hit(task, item_id, document or "", metadata or {}, float(distance), rank))
    items.sort(key=lambda item: item.score, reverse=True)
    return items


def kg_terms_from_query(query: str) -> list[str]:
    tokens = sorted(query_tokens(query))
    expanded = []
    for token in tokens:
        expanded.append(token)
        if token == "mathrock":
            expanded.extend(["math rock", "math_rock", "midwest", "tapping", "open_string"])
        if token == "funk":
            expanded.extend(["groove", "muted", "rhythm", "chuck", "ghost"])
    return sorted({token.lower() for token in expanded if len(token) >= 2})[:32]


def rerank_kg_items(query: str, items: list[EvidenceItem], limit: int) -> list[EvidenceItem]:
    terms = kg_terms_from_query(query)
    style_hints = infer_style_hints(query)
    for item in items:
        blob = (item.content + " " + json.dumps(item.metadata, ensure_ascii=False)).lower()
        term_matches = sum(1 for term in terms if term in blob)
        style_matches = 0
        for style in style_hints:
            for marker in STYLE_KEYWORDS.get(style, []):
                if marker.lower() in blob:
                    style_matches += 1
                    break
        generic_penalty = 0.0
        if "concept:standard_tuning" in blob and style_hints:
            generic_penalty -= 0.12
        if "riff" in query.lower() and any(term in blob for term in ["riff", "rhythm", "groove", "chuck", "open_string", "tapping"]):
            term_matches += 1
        item.score = round(item.score + term_matches * 0.08 + style_matches * 0.18 + generic_penalty, 5)
        item.metadata["kg_rerank"] = {
            "term_matches": term_matches,
            "style_matches": style_matches,
            "generic_penalty": generic_penalty,
        }
    items.sort(key=lambda entry: entry.score, reverse=True)
    return items[:limit]


def kg_edge_to_evidence(edge: dict[str, Any], rank: int, backend: str) -> EvidenceItem:
    source = str(edge.get("source") or "")
    relation = str(edge.get("relation") or edge.get("type") or "")
    target = str(edge.get("target") or "")
    context = str(edge.get("context_condition") or "")
    note = str(edge.get("review_note") or "")
    evidence = str(edge.get("evidence") or "")
    content = "\n".join(part for part in [f"{source} -[{relation}]-> {target}", context, note, evidence] if part)
    confidence = edge.get("confidence", 0.0)
    try:
        score = float(confidence)
    except (TypeError, ValueError):
        score = 0.0
    provenance = edge.get("provenance") if isinstance(edge.get("provenance"), dict) else {}
    return EvidenceItem(
        evidence_id=f"kg:{source}:{relation}:{target}",
        evidence_type="kg",
        source_id=str(provenance.get("source_review_file") or edge.get("knowledge_type") or "kg"),
        title=f"{source} -[{relation}]-> {target}",
        content=content,
        score=round(score, 5),
        metadata={
            "source": source,
            "relation": relation,
            "target": target,
            "knowledge_type": edge.get("knowledge_type", ""),
            "confidence": confidence,
            "context_condition": context,
            "review_note": note,
            "provenance": provenance,
            "backend": backend,
        },
        trace={"rank": rank, "backend": backend},
    )


def search_neo4j(task: SearchTask, env_file: Path) -> tuple[list[EvidenceItem], str]:
    apply_env_file(env_file)
    password = os.environ.get("NEO4J_PASSWORD", "")
    if not password:
        return [], "neo4j_skipped_no_password"
    try:
        from neo4j import GraphDatabase
    except ImportError:
        return [], "neo4j_skipped_missing_driver"

    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    user = os.environ.get("NEO4J_USER", "neo4j")
    database = os.environ.get("NEO4J_DATABASE", "neo4j")
    terms = kg_terms_from_query(task.query)
    if not terms:
        return [], "neo4j_skipped_no_terms"
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver:
            with driver.session(database=database) as session:
                rows = session.run(
                    """
                    MATCH (a:KGNode)-[r]->(b:KGNode)
                    WHERE any(term IN $terms WHERE
                        toLower(a.id) CONTAINS term OR
                        toLower(b.id) CONTAINS term OR
                        toLower(type(r)) CONTAINS term OR
                        toLower(coalesce(r.context_condition, '')) CONTAINS term OR
                        toLower(coalesce(r.review_note, '')) CONTAINS term OR
                        toLower(coalesce(r.evidence, '')) CONTAINS term
                    )
                    RETURN a.id AS source, type(r) AS relation, b.id AS target,
                           r.knowledge_type AS knowledge_type,
                           r.confidence AS confidence,
                           r.context_condition AS context_condition,
                           r.review_note AS review_note,
                           r.evidence AS evidence
                    ORDER BY coalesce(r.confidence, 0) DESC
                    LIMIT $limit
                    """,
                    terms=terms,
                    limit=max(task.top_k * 5, task.top_k),
                ).data()
        items = [kg_edge_to_evidence(row, rank, "neo4j") for rank, row in enumerate(rows, start=1)]
        return rerank_kg_items(task.query, items, task.top_k), "neo4j"
    except Exception as exc:  # Keep query layer usable when Neo4j is offline.
        return [], f"neo4j_failed:{type(exc).__name__}"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(row, dict):
                rows.append(row)
    return rows


def search_kg_files(task: SearchTask, root: Path) -> list[EvidenceItem]:
    terms = kg_terms_from_query(task.query)
    scored: list[tuple[float, dict[str, Any]]] = []
    for path in sorted((root / "data" / "knowledge").glob("**/edges.jsonl")):
        for edge in read_jsonl(path):
            blob = json.dumps(edge, ensure_ascii=False).lower()
            matches = sum(1 for term in terms if term in blob)
            if matches <= 0:
                continue
            confidence = edge.get("confidence") or 0
            try:
                confidence_f = float(confidence)
            except (TypeError, ValueError):
                confidence_f = 0.0
            scored.append((matches + confidence_f, edge))
    scored.sort(key=lambda item: item[0], reverse=True)
    items = [kg_edge_to_evidence(edge, rank, "file_edges") for rank, (_, edge) in enumerate(scored[: max(task.top_k * 5, task.top_k)], start=1)]
    return rerank_kg_items(task.query, items, task.top_k)


def search_kg(task: SearchTask, env_file: Path) -> tuple[list[EvidenceItem], str]:
    neo4j_items, status = search_neo4j(task, env_file)
    if neo4j_items:
        return neo4j_items, status
    file_items = search_kg_files(task, ROOT)
    return file_items, f"{status};file_fallback"


def dedupe_items(items: list[EvidenceItem]) -> list[EvidenceItem]:
    seen: set[str] = set()
    deduped: list[EvidenceItem] = []
    for item in sorted(items, key=lambda entry: entry.score, reverse=True):
        key = item.evidence_id
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def merge_evidence(results: dict[str, list[EvidenceItem]]) -> tuple[list[EvidenceItem], list[EvidenceItem], list[EvidenceItem]]:
    text_items = dedupe_items(results.get("fretboard_text", []) + results.get("style_text", []))
    visual_items = dedupe_items(results.get("visual_caption", []))
    kg_items = dedupe_items(results.get("kg", []))

    text_exercises = {str(item.metadata.get("exercise_number")) for item in text_items if item.metadata.get("exercise_number")}
    for item in visual_items:
        exercise = str(item.metadata.get("exercise_number") or "")
        if exercise and exercise in text_exercises:
            item.metadata["paired_with_text_exercise"] = True
            item.score = round(item.score + 0.05, 5)
    visual_items.sort(key=lambda entry: entry.score, reverse=True)
    return text_items, visual_items, kg_items


def judge_bundle(analysis: QueryAnalysis, text: list[EvidenceItem], visual: list[EvidenceItem], kg: list[EvidenceItem]) -> dict[str, Any]:
    missing: list[str] = []
    warnings: list[str] = []
    if analysis.needs_fretboard_text and not any(item.source_id == "fretboard_handbook_clean_text" for item in text):
        missing.append("fretboard_text")
    if analysis.needs_style_text and not any(item.source_id != "fretboard_handbook_clean_text" for item in text):
        missing.append("style_text")
    if analysis.needs_visual and not visual:
        missing.append("visual_caption")
    if analysis.needs_kg and not kg:
        missing.append("kg")
    if kg and not text:
        warnings.append("kg_without_text_grounding")
    if analysis.style_hints and text:
        style_blob = json.dumps([item.metadata for item in text], ensure_ascii=False).lower()
        if not any(style.lower() in style_blob for style in analysis.style_hints):
            warnings.append("possible_style_mismatch")
    evidence_types = sum(bool(group) for group in [text, visual, kg])
    sufficient = not missing and evidence_types >= (2 if analysis.intent.startswith("mixed") else 1)
    confidence = 0.35 + 0.18 * evidence_types - 0.12 * len(missing) - 0.05 * len(warnings)
    return {
        "sufficient": sufficient,
        "confidence": round(max(0.0, min(0.95, confidence)), 3),
        "missing": missing,
        "warnings": warnings,
        "evidence_type_count": evidence_types,
        "text_count": len(text),
        "visual_count": len(visual),
        "kg_count": len(kg),
        "next_queries": build_next_queries(analysis, missing),
    }


def build_next_queries(analysis: QueryAnalysis, missing: list[str]) -> list[str]:
    queries = []
    if "visual_caption" in missing:
        queries.append(f"{analysis.query} 指型图 和弦图 voicing 答案图")
    if "style_text" in missing and analysis.style_hints:
        queries.append(f"{analysis.query} {' '.join(analysis.style_hints)} riff rhythm arrangement")
    if "kg" in missing:
        terms = " ".join(analysis.style_hints + analysis.technique_terms + analysis.theory_terms)
        queries.append(f"{analysis.query} {terms} technique relation arrangement")
    return queries


def build_answer_seed(bundle: EvidenceBundle | None, analysis: QueryAnalysis, text: list[EvidenceItem], visual: list[EvidenceItem], kg: list[EvidenceItem]) -> dict[str, Any]:
    return {
        "recommended_structure": [
            "结论",
            "相关教材证据",
            "视觉/指法证据",
            "KG/风格关系",
            "可操作编配建议",
            "不确定点",
        ],
        "top_text_ids": [item.evidence_id for item in text[:3]],
        "top_visual_ids": [item.evidence_id for item in visual[:3]],
        "top_kg_ids": [item.evidence_id for item in kg[:5]],
        "composer_instruction": (
            "只能基于 evidence_id 引用证据；区分教材明确内容与系统推断；"
            "如果 judgement.missing 非空，需要先说明证据不足。"
        ),
    }


def run_bundle(args: argparse.Namespace) -> EvidenceBundle:
    import chromadb

    started = time.perf_counter()
    context = json.loads(args.context_json) if args.context_json else {}
    analysis = analyze_query(args.query, context=context)
    plan = plan_retrieval(analysis, args.top_k)

    model_started = time.perf_counter()
    embedder = LocalTransformerEmbedder(args.model, device=args.device, max_length=args.max_length)
    model_seconds = time.perf_counter() - model_started
    client = chromadb.PersistentClient(path=str(args.chroma_path))

    results: dict[str, list[EvidenceItem]] = {}
    timings: dict[str, float] = {"model_load_seconds": model_seconds}
    kg_status = ""
    for task in plan:
        task_started = time.perf_counter()
        if task.backend == "chroma":
            results[task.name] = search_chroma(client, embedder, task, args.batch_size)
        else:
            items, kg_status = search_kg(task, args.env_file)
            results[task.name] = items
        timings[f"{task.name}_seconds"] = time.perf_counter() - task_started

    text, visual, kg = merge_evidence(results)
    judgement = judge_bundle(analysis, text, visual, kg)
    answer_seed = build_answer_seed(None, analysis, text, visual, kg)
    timings["total_seconds"] = time.perf_counter() - started
    if kg_status:
        timings["kg_status"] = kg_status  # type: ignore[assignment]

    return EvidenceBundle(
        query=args.query,
        analysis=analysis,
        plan=plan,
        text_evidence=text[: args.top_k * 2],
        visual_evidence=visual[: args.top_k],
        kg_evidence=kg[: args.kg_limit],
        judgement=judgement,
        answer_seed=answer_seed,
        timings=timings,
    )


def evidence_preview(item: EvidenceItem, limit: int = 260) -> str:
    return compact(item.content, limit=limit).replace("|", "\\|")


def render_evidence_table(items: list[EvidenceItem]) -> list[str]:
    lines = [
        "| Rank | Evidence ID | Source | Score | Title | Preview |",
        "|---:|---|---|---:|---|---|",
    ]
    if not items:
        lines.append("| - | - | - | - | - | - |")
        return lines
    for rank, item in enumerate(items, start=1):
        lines.append(
            f"| {rank} | `{item.evidence_id}` | `{item.source_id}` | {item.score:.4f} | {compact(item.title, 80)} | {evidence_preview(item)} |"
        )
    return lines


def render_markdown(bundle: EvidenceBundle) -> str:
    lines = [
        "# Query RAG Bundle Report",
        "",
        f"- Query: {bundle.query}",
        f"- Intent: `{bundle.analysis.intent}`",
        f"- Sufficient: `{bundle.judgement['sufficient']}`",
        f"- Confidence: {bundle.judgement['confidence']}",
        f"- Total latency: {bundle.timings.get('total_seconds', 0):.3f}s",
        "",
        "## Query Analysis",
        "",
        "```json",
        json.dumps(asdict(bundle.analysis), ensure_ascii=False, indent=2),
        "```",
        "",
        "## Retrieval Plan",
        "",
        "| Name | Backend | Collection | TopK | Reason | Query |",
        "|---|---|---|---:|---|---|",
    ]
    for task in bundle.plan:
        lines.append(
            f"| `{task.name}` | `{task.backend}` | `{task.collection or ''}` | {task.top_k} | {task.reason} | {compact(task.query, 120)} |"
        )
    lines.extend(["", "## Text Evidence", ""])
    lines.extend(render_evidence_table(bundle.text_evidence))
    lines.extend(["", "## Visual Evidence", ""])
    lines.extend(render_evidence_table(bundle.visual_evidence))
    lines.extend(["", "## KG Evidence", ""])
    lines.extend(render_evidence_table(bundle.kg_evidence))
    lines.extend(
        [
            "",
            "## Bundle Judgement",
            "",
            "```json",
            json.dumps(bundle.judgement, ensure_ascii=False, indent=2),
            "```",
            "",
            "## Answer Seed",
            "",
            "```json",
            json.dumps(bundle.answer_seed, ensure_ascii=False, indent=2),
            "```",
            "",
            "## Timings",
            "",
            "```json",
            json.dumps(bundle.timings, ensure_ascii=False, indent=2),
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True)
    parser.add_argument("--context-json", default="")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--kg-limit", type=int, default=10)
    parser.add_argument("--chroma-path", type=Path, default=DEFAULT_CHROMA_PATH)
    parser.add_argument("--model", default=os.environ.get("LOCAL_EMBEDDING_MODEL", DEFAULT_LOCAL_MODEL))
    parser.add_argument("--device", default=os.environ.get("LOCAL_EMBEDDING_DEVICE", "auto"))
    parser.add_argument("--max-length", type=int, default=int(os.environ.get("LOCAL_EMBEDDING_MAX_LENGTH", "2048")))
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    parser.add_argument("--report-md", type=Path, default=DEFAULT_REPORT_MD)
    parser.add_argument("--report-json", type=Path, default=DEFAULT_REPORT_JSON)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    bundle = run_bundle(args)
    args.report_json.parent.mkdir(parents=True, exist_ok=True)
    args.report_json.write_text(json.dumps(asdict(bundle), ensure_ascii=False, indent=2), encoding="utf-8")
    args.report_md.write_text(render_markdown(bundle), encoding="utf-8")
    print(
        json.dumps(
            {
                "query": bundle.query,
                "intent": bundle.analysis.intent,
                "plan": [task.name for task in bundle.plan],
                "text": len(bundle.text_evidence),
                "visual": len(bundle.visual_evidence),
                "kg": len(bundle.kg_evidence),
                "judgement": bundle.judgement,
                "report_md": str(args.report_md),
                "report_json": str(args.report_json),
                "timings": bundle.timings,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
