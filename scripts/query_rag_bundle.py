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
from functools import lru_cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from local_text_embedding import DEFAULT_LOCAL_MODEL, LocalTransformerEmbedder
from rerank_backend import RerankConfig, apply_model_rerank


DEFAULT_CHROMA_PATH = ROOT / "data" / "chroma"
DEFAULT_REPORT_MD = ROOT / "data" / "eval" / "query_rag_bundle_report.md"
DEFAULT_REPORT_JSON = ROOT / "data" / "eval" / "query_rag_bundle_report.json"
DEFAULT_CANONICAL_VISUAL_SIDECAR = (
    ROOT
    / "data"
    / "processed"
    / "fretboard_handbook"
    / "question_answer_visual_caption_canonical"
    / "fretboard_answer_visual_caption_canonical_terms.jsonl"
)
DEFAULT_VISUAL_CAPTION_SOURCE = (
    ROOT
    / "data"
    / "processed"
    / "fretboard_handbook"
    / "question_answer_visual_caption_layer"
    / "fretboard_answer_visual_caption_accepted_all.jsonl"
)
MATHROCK_CANONICAL_VISUAL_SIDECAR = (
    ROOT
    / "data"
    / "processed"
    / "mathrock"
    / "style_visual_caption_trial"
    / "batch_001_canonical"
    / "canonical_terms_review.jsonl"
)
MATHROCK_VISUAL_CAPTION_SOURCE = (
    ROOT
    / "data"
    / "processed"
    / "mathrock"
    / "style_visual_caption_trial"
    / "batch_001_captions"
    / "visual_caption_results.jsonl"
)

COLLECTIONS = {
    "fretboard_text": "guitar_fretboard_handbook_text_qwen3_06b",
    "visual_caption": "guitar_fretboard_answer_captions_qwen3_06b",
    "style_text": "guitar_text_chunks_qwen3_06b",
}

VISUAL_COLLECTIONS = {
    "formal": COLLECTIONS["visual_caption"],
    "mathrock_mixed_trial": "guitar_visual_mixed_mathrock_trial_qwen3_06b",
}

TEXT_COLLECTIONS = {"fretboard_text", "style_text"}


@lru_cache(maxsize=2)
def get_cached_embedder(model: str, device: str, max_length: int) -> LocalTransformerEmbedder:
    return LocalTransformerEmbedder(model, device=device, max_length=max_length)


@lru_cache(maxsize=2)
def get_cached_chroma_client(chroma_path: str) -> Any:
    import chromadb

    return chromadb.PersistentClient(path=chroma_path)

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
    "指型",
    "指型图",
    "和弦图",
    "答案图",
    "答案",
    "把位",
    "同把位",
    "映射",
    "参考",
    "省略",
    "高把位",
    "低把位",
    "按法",
    "排列",
    "shape",
    "diagram",
    "voicing",
    "omit",
]

STYLE_KEYWORDS = {
    "funk": ["funk", "groove", "ghost", "muted", "chuck", "切分", "十六分", "律动", "消音"],
    "mathrock": ["mathrock", "math rock", "midwest", "数摇", "数学摇滚", "DADGAD", "FACGCE", "奇数"],
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
    "编",
    "写",
    "写一段",
    "伴奏",
    "主奏",
    "分解",
    "对位",
    "改写",
    "生成",
    "推荐",
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

ALT_TUNING_TERMS = [
    "dadgad",
    "facgce",
    "drop tuning",
    "open tuning",
    "alternate tuning",
    "特殊调弦",
    "开放调弦",
    "降弦",
    "特调",
    "tuning:dadgad",
    "tuning:drop",
]
FRET_REGION_TERMS = {
    "low": ["低把位", "low position", "low fret", "open position", "first position", "1st position"],
    "middle": ["中把位", "middle position", "mid position"],
    "high": ["高把位", "high position", "high fret", "upper position", "upper fret"],
}
DIRECT_KG_GOAL_TERMS = [
    "riff",
    "groove",
    "voicing",
    "leave_space",
    "space",
    "贝斯",
    "频率",
    "relative",
    "相对",
    "phrasing",
    "hook",
    "arrangement",
    "编配",
]


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


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return bool(value)


def compact(text: str, limit: int = 600) -> str:
    text = " ".join(str(text or "").split())
    return text if len(text) <= limit else text[: limit - 1] + "..."


def query_tokens(query: str) -> set[str]:
    tokens = {token.lower() for token in TOKEN_RE.findall(query)}
    for term in FRETBOARD_TERMS + VISUAL_TERMS + TECHNIQUE_TERMS:
        if term.lower() in query.lower():
            tokens.add(term.lower())
    return {token for token in tokens if len(token) >= 2}


def compact_blob(*parts: Any) -> str:
    return " ".join(str(part or "") for part in parts).lower().replace("♭", "b").replace("♯", "#")


def unique_strings(values: list[Any]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        text = str(value).strip()
        if not text or text.lower() in seen:
            continue
        seen.add(text.lower())
        out.append(text)
    return out


def term_in_blob(term: str, blob: str) -> bool:
    needle = str(term or "").strip().lower().replace("♭", "b").replace("♯", "#")
    if not needle:
        return False
    if re.fullmatch(r"[a-g](?:#|b)?", needle):
        return re.search(rf"(?<![a-z0-9]){re.escape(needle)}(?![a-z0-9])", blob) is not None
    return needle in blob


def key_term_aliases(term: str) -> list[str]:
    raw = str(term or "").strip().replace("♭", "b").replace("♯", "#")
    if not raw:
        return []
    aliases = [raw]
    lowered = raw.lower()
    english_match = re.search(r"\b([a-g](?:#|b)?)\s*(major|minor|maj|min)\b", lowered)
    if english_match:
        root, mode = english_match.groups()
        root = root.upper()
        if mode in {"major", "maj"}:
            aliases.extend([f"{root} major", f"{root} maj", f"{root}大调", f"{root} 大调", f"{root}大调音阶"])
        else:
            aliases.extend([f"{root} minor", f"{root} min", f"{root}m", f"{root}小调", f"{root} 小调", f"{root}自然小调", f"{root}小调音阶"])
    chinese_match = re.search(r"([A-G](?:#|b)?)\s*(大调|小调)", raw, re.I)
    if chinese_match:
        root, mode = chinese_match.groups()
        root = root.upper()
        if mode == "大调":
            aliases.extend([f"{root} major", f"{root} maj", f"{root}大调", f"{root} 大调", f"{root}大调音阶"])
        else:
            aliases.extend([f"{root} minor", f"{root} min", f"{root}m", f"{root}小调", f"{root} 小调", f"{root}自然小调", f"{root}小调音阶"])
    return unique_strings(aliases)


def key_term_in_blob(term: str, blob: str) -> bool:
    normalized_blob = compact_blob(blob)
    return any(term_in_blob(alias, normalized_blob) for alias in key_term_aliases(term))


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
    if style_hints and (technique_terms or theory_terms) and has_any(query, KG_TERMS + ["riff", "voicing", "groove"]):
        needs_kg = True
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


def plan_retrieval(
    analysis: QueryAnalysis,
    top_k: int,
    visual_collection: str = COLLECTIONS["visual_caption"],
) -> list[SearchTask]:
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
                collection=visual_collection,
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


def query_plan_enabled_tools(query_plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw_plan = query_plan.get("retrieval_plan")
    if not isinstance(raw_plan, dict):
        return {}
    enabled: dict[str, dict[str, Any]] = {}
    for name in ("fretboard_text", "style_text", "visual_caption", "kg"):
        item = raw_plan.get(name)
        if not isinstance(item, dict) or not item.get("enabled"):
            continue
        enabled[name] = item
    return enabled


def analysis_from_query_plan(raw_query: str, query_plan: dict[str, Any]) -> QueryAnalysis:
    enabled = query_plan_enabled_tools(query_plan)
    normalized = str(query_plan.get("normalized_query") or raw_query)
    theory_terms: list[str] = []
    for key in ("harmonic_materials", "melodic_materials", "fretboard_constraints"):
        theory_terms.extend(str(item) for item in as_list(query_plan.get(key)) if str(item).strip())
    technique_terms = [str(item) for item in as_list(query_plan.get("techniques")) if str(item).strip()]
    matched_rules = [f"llm_plan:{name}" for name in enabled]
    return QueryAnalysis(
        query=normalized,
        intent=str(query_plan.get("intent") or "mixed_arrangement"),
        style_hints=[str(item) for item in as_list(query_plan.get("style_hints")) if str(item).strip()],
        theory_terms=theory_terms,
        technique_terms=technique_terms,
        needs_fretboard_text="fretboard_text" in enabled,
        needs_visual="visual_caption" in enabled,
        needs_style_text="style_text" in enabled,
        needs_kg="kg" in enabled,
        confidence=round(float(query_plan.get("confidence") or 0.0), 3),
        matched_rules=matched_rules or ["llm_plan_empty_fallback"],
    )


def plan_retrieval_from_query_plan(
    query_plan: dict[str, Any],
    top_k: int,
    visual_collection: str = COLLECTIONS["visual_caption"],
) -> list[SearchTask]:
    enabled = query_plan_enabled_tools(query_plan)
    normalized = str(query_plan.get("normalized_query") or query_plan.get("raw_query") or "").strip()
    specs = {
        "fretboard_text": ("chroma", COLLECTIONS["fretboard_text"], top_k, "LLM QueryPlan: 指板/理论教材文本证据"),
        "style_text": ("chroma", COLLECTIONS["style_text"], top_k, "LLM QueryPlan: 风格/riff/节奏教材文本证据"),
        "visual_caption": ("chroma", visual_collection, top_k, "LLM QueryPlan: 指型/voicing/图形 caption 证据"),
        "kg": ("neo4j_or_file", None, max(top_k, 8), "LLM QueryPlan: 技法关系/风格迁移/编配启发"),
    }
    tasks: list[SearchTask] = []
    for name, item in enabled.items():
        backend, collection, task_top_k, default_reason = specs[name]
        task_query = str(item.get("query") or normalized or query_plan.get("raw_query") or "").strip()
        if not task_query:
            continue
        tasks.append(
            SearchTask(
                name=name,
                backend=backend,
                collection=collection,
                query=task_query,
                top_k=task_top_k,
                reason=str(item.get("reason") or default_reason),
            )
        )
    return tasks


def normalize_distance(distance: float | int | None) -> float:
    if distance is None:
        return 0.0
    return max(0.0, 1.0 - float(distance))


def append_unique_term(terms: list[str], term: str) -> None:
    normalized = term.strip().lower()
    if normalized and normalized not in {item.strip().lower() for item in terms}:
        terms.append(normalized)


def remove_terms_by_prefix(terms: list[str], prefixes: tuple[str, ...]) -> list[str]:
    return [term for term in terms if not str(term).strip().lower().startswith(prefixes)]


def normalize_root_token(value: str) -> str:
    return value.strip().lower().replace("♭", "b").replace("♯", "#")


def normalize_chord_quality_token(value: str) -> str:
    quality = value.strip().lower().replace("major", "maj").replace("minor", "min")
    mapping = {
        "ma7": "maj7",
        "major7": "maj7",
        "m7": "min7",
        "mi7": "min7",
        "min7": "min7",
    }
    return mapping.get(quality, quality)


def exact_chord_terms_from_plan(query_plan: dict[str, Any], target_roots: list[str], chord_qualities: list[str]) -> list[str]:
    terms: list[str] = []
    for material in as_list(query_plan.get("harmonic_materials")):
        match = re.search(r"\b([A-G](?:#|b|♭|♯)?)(maj9#11|maj7#11|maj#11|maj9|m11|min11|mi11|11|13|7#9|7b9|7#5|7b5|maj7|m7|mi7|min7|dim7|m7b5|sus4|sus2|add9|6/9|7)\b", str(material), re.I)
        if match:
            root = normalize_root_token(match.group(1))
            quality = normalize_chord_quality_token(match.group(2))
            terms.append(f"chord:{root}_{quality}")
    if not terms and target_roots and chord_qualities:
        for root in target_roots[:1]:
            for quality in chord_qualities[:1]:
                terms.append(f"chord:{normalize_root_token(str(root))}_{normalize_chord_quality_token(str(quality))}")
    return unique_strings(terms)


def is_tapping_tab_request(query_plan: dict[str, Any], query_blob: str) -> bool:
    values = " ".join(
        [
            query_blob,
            " ".join(str(item) for item in as_list(query_plan.get("techniques"))),
            " ".join(str(item) for item in as_list(query_plan.get("canonical_terms"))),
            " ".join(str(item) for item in as_list(query_plan.get("required_terms"))),
        ]
    ).lower()
    return any(term in values for term in ["tapping", "点弦", "two_hand_tapping", "two-hand tapping"])


def is_riff_tab_request(query_plan: dict[str, Any], query_blob: str) -> bool:
    values = " ".join(
        [
            query_blob,
            " ".join(str(item) for item in as_list(query_plan.get("techniques"))),
            " ".join(str(item) for item in as_list(query_plan.get("canonical_terms"))),
        ]
    ).lower()
    return any(term in values for term in ["riff", "乐句", "谱例", "tab", "节奏型", "节拍"])


def meter_terms_from_query(query_blob: str) -> list[str]:
    terms: list[str] = []
    for match in re.findall(r"\b(\d+)\s*/\s*(\d+)\b", query_blob):
        terms.append(f"meter:{match[0]}_{match[1]}")
    return unique_strings(terms)


def refine_visual_query_terms(
    query_plan: dict[str, Any],
    query_blob: str,
    target_roots: list[str],
    chord_qualities: list[str],
    canonical_terms: list[str],
    required_terms: list[str],
    optional_terms: list[str],
) -> tuple[list[str], list[str], list[str]]:
    chord_terms = exact_chord_terms_from_plan(query_plan, target_roots, chord_qualities)
    for term in chord_terms:
        append_unique_term(canonical_terms, term)

    tapping_request = is_tapping_tab_request(query_plan, query_blob)
    riff_request = is_riff_tab_request(query_plan, query_blob)
    meter_terms = meter_terms_from_query(query_blob)

    for term in meter_terms:
        append_unique_term(canonical_terms, term)

    if riff_request:
        # Riff/tab queries should not be forced into generic scale or chord
        # diagrams; the visual layer should prefer concrete notation excerpts.
        required_terms = remove_terms_by_prefix(required_terms, ("visual_type:scale_pattern", "chord_quality:maj"))
        for term in ["visual_type:tab_excerpt", "visual_subtype:riff_tab", "technique:riff", "concept:riff_composition"]:
            append_unique_term(canonical_terms, term)
        append_unique_term(required_terms, "visual_type:tab_excerpt")
        append_unique_term(optional_terms, "visual_subtype:riff_tab")
        if "math rock" in query_blob or "mathrock" in query_blob or "数摇" in query_blob or "数学摇滚" in query_blob:
            append_unique_term(canonical_terms, "style:math_rock")
            append_unique_term(required_terms, "style:math_rock")
        if meter_terms:
            append_unique_term(canonical_terms, "technique:irregular_meter")
            append_unique_term(optional_terms, "technique:irregular_meter")
            for term in meter_terms:
                append_unique_term(required_terms, term)

    if tapping_request:
        required_terms = remove_terms_by_prefix(required_terms, ("visual_type:scale_pattern", "key:"))
        for term in ["technique:tapping", "visual_type:tab_excerpt", "visual_subtype:tapping_example", "concept:arpeggio"]:
            append_unique_term(canonical_terms, term)
        append_unique_term(required_terms, "technique:tapping")
        append_unique_term(optional_terms, "visual_subtype:tapping_example")

    if chord_terms and tapping_request:
        for term in chord_terms:
            append_unique_term(required_terms, term)

    return unique_strings(canonical_terms), unique_strings(required_terms), unique_strings(optional_terms)


def token_boost(query: str, text: str) -> float:
    tokens = query_tokens(query)
    if not tokens:
        return 0.0
    blob = text.lower()
    matches = sum(1 for token in tokens if token in blob)
    return min(0.25, matches * 0.025)


def style_source_boost(query: str, source_id: str, title: str, document: str, metadata: dict[str, Any]) -> float:
    style_hints = infer_style_hints(query)
    if not style_hints:
        return 0.0
    blob = " ".join([source_id, title, document[:500], json.dumps(metadata, ensure_ascii=False)]).lower()
    boost = 0.0
    for style in style_hints:
        if style == "funk":
            if "funk" in blob or "cory_wong" in blob or "cory wong" in blob:
                boost += 0.18
            if "mathrock" in blob or "math rock" in blob:
                boost -= 0.12
        elif style == "mathrock":
            if "mathrock" in blob or "math rock" in blob or "midwest" in blob:
                boost += 0.18
            if "cory_wong" in blob or "cory wong" in blob:
                boost -= 0.08
        elif style.lower() in blob:
            boost += 0.12
    return boost


def extract_constraints(query_plan: dict[str, Any] | None, analysis: QueryAnalysis) -> dict[str, Any]:
    query_plan = query_plan or {}
    raw_query = str(query_plan.get("raw_query") or analysis.query)
    normalized_query = str(query_plan.get("normalized_query") or analysis.query)
    query_blob = compact_blob(raw_query, normalized_query, analysis.query)
    target_tuning = str(query_plan.get("target_tuning") or "").strip().lower().replace(" ", "_").replace("-", "_")
    if not target_tuning:
        if "facgce" in query_blob:
            target_tuning = "facgce"
        elif "dadgad" in query_blob:
            target_tuning = "dadgad"
        elif "drop d" in query_blob or "dropd" in query_blob:
            target_tuning = "drop_d"
        elif "drop" in query_blob or "降弦" in query_blob:
            target_tuning = "drop"
        elif "open tuning" in query_blob or "开放调弦" in query_blob:
            target_tuning = "open"
        else:
            target_tuning = "standard"
    if target_tuning in {"std", "standard_tuning", "标调", "标准调弦"}:
        target_tuning = "standard"
    tuning_term = f"tuning:{target_tuning}"
    target_keys = unique_strings(as_list(query_plan.get("target_keys")) + as_list(query_plan.get("key_or_tonality")))
    target_roots = unique_strings(as_list(query_plan.get("target_roots")))
    chord_qualities = unique_strings(as_list(query_plan.get("chord_qualities")))
    scale_or_mode = unique_strings(as_list(query_plan.get("scale_or_mode")))
    canonical_terms = unique_strings(as_list(query_plan.get("canonical_terms")))
    required_terms = unique_strings(as_list(query_plan.get("required_terms")))
    optional_terms = unique_strings(as_list(query_plan.get("optional_terms")))
    negative_constraints = unique_strings(as_list(query_plan.get("negative_constraints")))
    fret_region = str(query_plan.get("fret_region") or "").strip().lower()
    position_constraints = unique_strings(as_list(query_plan.get("position_constraints")) + as_list(query_plan.get("fretboard_constraints")))
    if not target_keys:
        for match in re.finditer(r"\b([a-g](?:#|b)?)\s+(major|minor|maj|min)\b", query_blob):
            root, mode = match.groups()
            target_keys.append(f"{root.upper()}{' major' if mode in {'major', 'maj'} else ' minor'}")
        for match in re.finditer(r"([A-G](?:#|b|♭|♯)?)\s*(大调|小调)", raw_query):
            root = match.group(1).replace("♭", "b").replace("♯", "#")
            target_keys.append(f"{root} {'major' if match.group(2) == '大调' else 'minor'}")
    if not target_roots:
        for value in target_keys + analysis.theory_terms:
            match = re.search(r"\b([A-G](?:#|b)?)", str(value), re.I)
            if match:
                target_roots.append(match.group(1))
    if not chord_qualities:
        for value in analysis.theory_terms + [raw_query, normalized_query]:
            for match in re.findall(r"(maj9#11|maj7#11|maj#11|maj9|m11|min11|mi11|11|13|7#9|7b9|7#5|7b5|maj7|m7|mi7|min7|dim7|m7b5|sus4|sus2|add9|6/9|7)", str(value), re.I):
                chord_qualities.append(match)
    if not fret_region:
        for region, terms in FRET_REGION_TERMS.items():
            if any(term in query_blob for term in terms):
                fret_region = region
                break
    allow_alternate_tuning = as_bool(query_plan.get("allow_alternate_tuning")) or any(term in query_blob for term in ALT_TUNING_TERMS)
    if tuning_term not in {term.lower() for term in canonical_terms}:
        canonical_terms.append(tuning_term)
    if tuning_term not in {term.lower() for term in required_terms}:
        required_terms.append(tuning_term)
    if target_tuning != "standard":
        allow_alternate_tuning = True
    visual_required = as_bool(query_plan.get("visual_evidence_required")) or analysis.needs_visual
    explicit_mathrock_intent = any(
        marker in query_blob for marker in ["math rock", "mathrock", "数摇", "数学摇滚"]
    )
    style_hints = unique_strings(as_list(query_plan.get("style_hints")) + analysis.style_hints)
    if not explicit_mathrock_intent:
        style_hints = [style for style in style_hints if style.lower() != "mathrock"]
    standard_tuning_intent = "标准调弦" in query_blob or "standard tuning" in query_blob
    negative_techniques = {
        technique
        for technique, markers in {
            "tapping": ["不需要点弦", "不要点弦", "非点弦", "without tapping", "no tapping"],
            "arpeggio": ["不需要琶音", "不要琶音", "非琶音", "without arpeggio", "no arpeggio"],
            "open_string": ["不需要开放弦", "不要开放弦", "非开放弦", "without open strings", "no open strings"],
        }.items()
        if any(marker in query_blob for marker in markers)
    }
    canonical_terms, required_terms, optional_terms = refine_visual_query_terms(
        query_plan,
        query_blob,
        target_roots,
        chord_qualities,
        canonical_terms,
        required_terms,
        optional_terms,
    )
    return {
        "target_keys": unique_strings(target_keys),
        "target_roots": unique_strings(target_roots),
        "chord_qualities": unique_strings(chord_qualities),
        "scale_or_mode": unique_strings(scale_or_mode),
        "fret_region": fret_region,
        "position_constraints": position_constraints,
        "canonical_terms": canonical_terms,
        "required_terms": required_terms,
        "optional_terms": optional_terms,
        "negative_constraints": negative_constraints,
        "target_tuning": target_tuning,
        "requires_exact_key": as_bool(query_plan.get("requires_exact_key")) or bool(target_keys),
        "requires_exact_chord": as_bool(query_plan.get("requires_exact_chord")) or bool(chord_qualities and target_roots),
        "visual_evidence_required": visual_required,
        "allow_alternate_tuning": allow_alternate_tuning,
        "allow_exercise_reference": True if query_plan.get("allow_exercise_reference") is None else as_bool(query_plan.get("allow_exercise_reference")),
        "style_hints": style_hints,
        "techniques": unique_strings(as_list(query_plan.get("techniques")) + analysis.technique_terms),
        "mathrock_intent": explicit_mathrock_intent,
        "standard_tuning_intent": standard_tuning_intent,
        "negative_techniques": sorted(negative_techniques),
        "query_blob": query_blob,
    }


def evidence_blob(item: EvidenceItem) -> str:
    return compact_blob(item.title, item.source_id, item.content, json.dumps(item.metadata, ensure_ascii=False))


def evidence_canonical_terms(item: EvidenceItem) -> set[str]:
    terms: list[Any] = []
    metadata_terms = item.metadata.get("canonical_terms")
    if metadata_terms:
        terms.extend(as_list(metadata_terms))
    raw = item.metadata.get("raw_metadata")
    if isinstance(raw, dict):
        for key in ["canonical_terms", "required_terms", "optional_terms"]:
            terms.extend(as_list(raw.get(key)))
    domain = item.metadata.get("domain_rerank")
    if isinstance(domain, dict):
        terms.extend(as_list(domain.get("canonical_terms")))
    term_set = {str(term).strip().lower() for term in terms if str(term).strip()}
    raw = item.metadata.get("raw_metadata")
    raw = raw if isinstance(raw, dict) else {}
    tuning = str(item.metadata.get("tuning") or raw.get("tuning") or "").strip().lower().replace(" ", "_").replace("-", "_")
    if tuning:
        if tuning in {"std", "standard_tuning"}:
            tuning = "standard"
        term_set.add(f"tuning:{tuning}")
    elif item.evidence_type == "visual_caption":
        source_id = str(item.source_id or raw.get("source_id") or "").lower()
        caption_layer = str(item.metadata.get("caption_layer") or raw.get("caption_layer") or "").lower()
        collection = str(item.metadata.get("collection") or "").lower()
        if (
            "fretboard" in source_id
            or "fretboard_answer" in caption_layer
            or "fretboard_answer" in collection
            or source_id == "canonical_visual"
            or collection == "canonical_visual_sidecar"
        ):
            term_set.add("tuning:standard")
    return term_set


def domain_constraint_score(item: EvidenceItem, constraints: dict[str, Any]) -> tuple[float, dict[str, Any]]:
    blob = evidence_blob(item)
    item_terms = evidence_canonical_terms(item)
    raw_metadata = item.metadata.get("raw_metadata")
    raw_metadata = raw_metadata if isinstance(raw_metadata, dict) else {}
    caption_layer = str(item.metadata.get("caption_layer") or raw_metadata.get("caption_layer") or "").lower()
    tuning = str(item.metadata.get("tuning") or raw_metadata.get("tuning") or "").lower()
    score = 0.0
    details: dict[str, Any] = {
        "matched_keys": [],
        "matched_roots": [],
        "matched_chord_qualities": [],
        "matched_scale_or_mode": [],
        "matched_style": [],
        "matched_techniques": [],
        "matched_canonical_terms": [],
        "missing_required_terms": [],
        "matched_negative_constraints": [],
        "penalties": [],
    }

    query_terms = {str(term).strip().lower() for term in constraints.get("canonical_terms", []) if str(term).strip()}
    required_terms = {str(term).strip().lower() for term in constraints.get("required_terms", []) if str(term).strip()}
    optional_terms = {str(term).strip().lower() for term in constraints.get("optional_terms", []) if str(term).strip()}
    negative_terms = {str(term).strip().lower() for term in constraints.get("negative_constraints", []) if str(term).strip()}
    matched_canonical = sorted(query_terms.intersection(item_terms))
    matched_required = sorted(required_terms.intersection(item_terms))
    missing_required = sorted(required_terms.difference(item_terms))
    matched_optional = sorted(optional_terms.intersection(item_terms))
    matched_negative = sorted(negative_terms.intersection(item_terms))
    required_key_terms = {term for term in required_terms if term.startswith("key:")}
    required_tuning_terms = {term for term in required_terms if term.startswith("tuning:")}
    matched_required_key_terms = sorted(required_key_terms.intersection(item_terms))
    matched_required_tuning_terms = sorted(required_tuning_terms.intersection(item_terms))
    if matched_canonical:
        score += min(0.45, 0.12 * len(matched_canonical))
    if matched_required:
        score += min(0.3, 0.12 * len(matched_required))
    if matched_optional:
        score += min(0.16, 0.06 * len(matched_optional))
    if matched_negative:
        score -= min(0.5, 0.25 * len(matched_negative))
        details["penalties"].append("matched_negative_constraints")
    if item_terms and missing_required:
        score -= min(0.45, 0.12 * len(missing_required))
        details["penalties"].append("missing_required_canonical_terms")
    if item_terms and required_key_terms and not matched_required_key_terms:
        score -= 0.35
        details["penalties"].append("missing_required_key_term")
    if item.evidence_type == "visual_caption" and required_tuning_terms and not matched_required_tuning_terms:
        score -= 1.2
        details["penalties"].append("missing_required_tuning_term")
        item.metadata["optional_expansion_only"] = True
    details["matched_canonical_terms"] = matched_canonical
    details["matched_required_terms"] = matched_required
    details["matched_optional_terms"] = matched_optional
    details["missing_required_terms"] = missing_required
    details["matched_negative_constraints"] = matched_negative
    details["matched_required_key_terms"] = matched_required_key_terms
    details["matched_required_tuning_terms"] = matched_required_tuning_terms

    matched_keys = [term for term in constraints["target_keys"] if key_term_in_blob(term, blob)]
    details["matched_keys"] = matched_keys
    if matched_keys:
        score += min(0.42, 0.28 + 0.07 * len(matched_keys))
    elif constraints["requires_exact_key"] and item.evidence_type in {"visual_caption", "text"}:
        score -= 0.08 if item.evidence_type == "visual_caption" else 0.04
        details["penalties"].append("missing_exact_key")

    matched_roots = [term for term in constraints["target_roots"] if term_in_blob(term, blob)]
    details["matched_roots"] = matched_roots
    if matched_roots:
        score += min(0.18, 0.07 * len(matched_roots))

    matched_qualities = [term for term in constraints["chord_qualities"] if term_in_blob(term, blob)]
    details["matched_chord_qualities"] = matched_qualities
    if matched_qualities:
        score += min(0.35, 0.15 * len(matched_qualities))
    elif constraints["requires_exact_chord"] and item.evidence_type == "visual_caption":
        score -= 0.12
        details["penalties"].append("missing_exact_chord_quality")

    matched_modes = [term for term in constraints["scale_or_mode"] if term_in_blob(term, blob)]
    details["matched_scale_or_mode"] = matched_modes
    if matched_modes:
        score += min(0.18, 0.09 * len(matched_modes))

    fret_region = constraints.get("fret_region") or ""
    if fret_region:
        region_terms = FRET_REGION_TERMS.get(fret_region, [])
        opposite_regions = [region for region in FRET_REGION_TERMS if region != fret_region]
        if any(term in blob for term in region_terms):
            score += 0.18
            details["matched_fret_region"] = fret_region
        elif any(term in blob for region in opposite_regions for term in FRET_REGION_TERMS[region]):
            score -= 0.1
            details["penalties"].append("opposite_fret_region")

    matched_styles = [style for style in constraints["style_hints"] if term_in_blob(style, blob)]
    details["matched_style"] = matched_styles
    if matched_styles:
        score += min(0.25, 0.12 * len(matched_styles))

    matched_techniques = [term for term in constraints["techniques"] if term_in_blob(term, blob)]
    details["matched_techniques"] = matched_techniques
    if matched_techniques:
        score += min(0.28, 0.09 * len(matched_techniques))

    if constraints["visual_evidence_required"] and item.evidence_type == "visual_caption":
        score += 0.05
        details["visual_required_bonus"] = True

    is_mathrock_visual = caption_layer == "mathrock_style_visual_caption_v1"
    if item.evidence_type == "visual_caption" and is_mathrock_visual:
        if constraints["mathrock_intent"]:
            score += 0.12
            details["mathrock_visual_bonus"] = True
        else:
            score -= 0.35
            details["penalties"].append("mathrock_visual_without_style_intent")
            item.metadata["optional_expansion_only"] = True

    if item.evidence_type == "visual_caption" and constraints["standard_tuning_intent"]:
        if tuning == "standard":
            score += 0.035
            details["standard_tuning_bonus"] = True
        elif tuning and tuning != "unknown":
            score -= 0.12
            details["penalties"].append("nonstandard_tuning_for_standard_query")

    for technique in constraints.get("negative_techniques", []):
        aliases = {
            "tapping": ["tapping", "点弦"],
            "arpeggio": ["arpeggio", "琶音"],
            "open_string": ["open_string", "open string", "开放弦"],
        }.get(technique, [technique])
        if any(alias in blob or alias in item_terms for alias in aliases):
            score -= 0.35
            details["penalties"].append(f"negative_technique:{technique}")

    if not constraints["allow_exercise_reference"] and item.metadata.get("exercise_number"):
        score -= 0.2
        details["penalties"].append("exercise_reference_disallowed")

    has_alt_tuning = any(term in blob for term in ALT_TUNING_TERMS)
    if has_alt_tuning and not constraints["allow_alternate_tuning"]:
        score -= 0.45 if item.evidence_type == "kg" else 0.25
        details["penalties"].append("alternate_tuning_not_requested")
        item.metadata["optional_expansion_only"] = True
    elif has_alt_tuning and constraints["allow_alternate_tuning"]:
        score += 0.2
        details["matched_alternate_tuning"] = True

    if item.evidence_type == "kg":
        direct_matches = [term for term in DIRECT_KG_GOAL_TERMS if term in blob and term in constraints["query_blob"]]
        if direct_matches:
            score += min(0.25, 0.08 * len(direct_matches))
            details["matched_direct_kg_goals"] = direct_matches

    return round(score, 5), details


def apply_domain_rerank(
    text: list[EvidenceItem],
    visual: list[EvidenceItem],
    kg: list[EvidenceItem],
    analysis: QueryAnalysis,
    query_plan: dict[str, Any] | None,
) -> tuple[list[EvidenceItem], list[EvidenceItem], list[EvidenceItem]]:
    constraints = extract_constraints(query_plan, analysis)
    for group in (text, visual, kg):
        for item in group:
            delta, details = domain_constraint_score(item, constraints)
            item.score = round(item.score + delta, 5)
            item.metadata["domain_rerank"] = {
                "delta": delta,
                "constraints": {key: value for key, value in constraints.items() if key != "query_blob"},
                "details": details,
            }
    text.sort(key=lambda entry: entry.score, reverse=True)
    visual.sort(key=lambda entry: entry.score, reverse=True)
    kg.sort(key=lambda entry: entry.score, reverse=True)
    return text, visual, kg


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
    score = (
        normalize_distance(distance)
        + token_boost(task.query, document + " " + json.dumps(metadata, ensure_ascii=False))
        + style_source_boost(task.query, source_id, title, document, metadata)
    )
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
    candidate_count = min(max(task.top_k * 5, task.top_k), collection.count())
    result = collection.query(
        query_embeddings=[embedding],
        n_results=candidate_count,
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
        return rerank_kg_items(task.query, items, max(task.top_k * 3, task.top_k)), "neo4j"
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


def visual_id_from_caption_row(row: dict[str, Any]) -> str:
    metadata = row.get("metadata_flat") if isinstance(row.get("metadata_flat"), dict) else {}
    return str(row.get("visual_id") or row.get("segment_id") or metadata.get("visual_id") or "")


@lru_cache(maxsize=2)
def get_canonical_visual_rows(sidecar_path: str) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    rows = [row for row in read_jsonl(Path(sidecar_path)) if str(row.get("status") or "").lower() == "accepted"]
    by_id = {str(row.get("visual_id") or ""): row for row in rows if row.get("visual_id")}
    return by_id, rows


@lru_cache(maxsize=2)
def get_visual_caption_source_rows(source_path: str) -> dict[str, dict[str, Any]]:
    rows = read_jsonl(Path(source_path))
    return {visual_id_from_caption_row(row): row for row in rows if visual_id_from_caption_row(row)}


def canonical_set(values: Any) -> set[str]:
    return {str(value).strip().lower() for value in as_list(values) if str(value).strip()}


def canonical_visual_score(query_plan: dict[str, Any], row: dict[str, Any]) -> tuple[float, dict[str, Any]]:
    item_terms = canonical_set(row.get("canonical_terms"))
    if not any(term.startswith("tuning:") for term in item_terms):
        item_terms.add("tuning:standard")
    query_blob = compact_blob(
        str(query_plan.get("raw_query") or ""),
        str(query_plan.get("normalized_query") or ""),
        " ".join(str(item) for item in as_list(query_plan.get("techniques"))),
    )
    canonical_terms, required_terms_raw, optional_terms_raw = refine_visual_query_terms(
        query_plan,
        query_blob,
        [str(item) for item in as_list(query_plan.get("target_roots"))],
        [str(item) for item in as_list(query_plan.get("chord_qualities"))],
        [str(item) for item in as_list(query_plan.get("canonical_terms"))],
        [str(item) for item in as_list(query_plan.get("required_terms"))],
        [str(item) for item in as_list(query_plan.get("optional_terms"))],
    )
    query_terms = canonical_set(canonical_terms)
    required_terms = canonical_set(required_terms_raw)
    optional_terms = canonical_set(optional_terms_raw)
    negative_terms = canonical_set(query_plan.get("negative_constraints"))
    matched_query = sorted(query_terms.intersection(item_terms))
    matched_required = sorted(required_terms.intersection(item_terms))
    matched_optional = sorted(optional_terms.intersection(item_terms))
    matched_negative = sorted(negative_terms.intersection(item_terms))
    missing_required = sorted(required_terms.difference(item_terms))
    required_key_terms = {term for term in required_terms if term.startswith("key:")}
    required_tuning_terms = {term for term in required_terms if term.startswith("tuning:")}
    matched_required_key_terms = sorted(required_key_terms.intersection(item_terms))
    matched_required_tuning_terms = sorted(required_tuning_terms.intersection(item_terms))
    score = 0.0
    score += len(matched_query) * 0.35
    score += len(matched_required) * 0.75
    score += len(matched_optional) * 0.18
    score -= len(matched_negative) * 1.0
    if required_terms and not matched_required:
        score -= 0.45
    if missing_required:
        score -= min(0.8, 0.18 * len(missing_required))
    if required_key_terms and not matched_required_key_terms:
        score -= 1.8
    if required_tuning_terms and not matched_required_tuning_terms:
        score -= 3.0
    if len(matched_required) >= max(1, min(2, len(required_terms))):
        score += 0.35
    return round(score, 5), {
        "matched_query_terms": matched_query,
        "matched_required_terms": matched_required,
        "matched_optional_terms": matched_optional,
        "matched_negative_terms": matched_negative,
        "missing_required_terms": missing_required,
        "matched_required_key_terms": matched_required_key_terms,
        "matched_required_tuning_terms": matched_required_tuning_terms,
        "item_terms": sorted(item_terms),
    }


def canonical_visual_to_evidence(
    row: dict[str, Any],
    source_row: dict[str, Any] | None,
    score: float,
    details: dict[str, Any],
    rank: int,
) -> EvidenceItem:
    visual_id = str(row.get("visual_id") or "")
    source_row = source_row or {}
    metadata_flat = source_row.get("metadata_flat") if isinstance(source_row.get("metadata_flat"), dict) else {}
    source_metadata = source_row.get("source_metadata") if isinstance(source_row.get("source_metadata"), dict) else {}
    preview = row.get("source_preview") if isinstance(row.get("source_preview"), dict) else {}
    content = str(preview.get("caption") or source_row.get("caption_text") or source_row.get("caption") or "")
    title = str(
        preview.get("musical_object")
        or source_row.get("musical_object")
        or source_row.get("topic")
        or "canonical visual caption"
    )
    image_path = (
        metadata_flat.get("image_path")
        or metadata_flat.get("crop_path")
        or source_metadata.get("image_path")
        or source_metadata.get("crop_path")
        or source_row.get("image_path")
        or source_row.get("crop_path")
        or ""
    )
    return EvidenceItem(
        evidence_id=f"visual_caption:{visual_id}",
        evidence_type="visual_caption",
        source_id="canonical_visual",
        title=title,
        content=content,
        score=round(1.0 + score, 5),
        metadata={
            "collection": "canonical_visual_sidecar",
            "chunk_id": visual_id,
            "visual_id": visual_id,
            "exercise_number": metadata_flat.get("exercise_number") or "",
            "subquestion_number": metadata_flat.get("subquestion_number") or "",
            "image_path": image_path,
            "canonical_terms": as_list(row.get("canonical_terms")),
            "required_terms": as_list(row.get("required_terms")),
            "optional_terms": as_list(row.get("optional_terms")),
            "negative_constraints": as_list(row.get("negative_constraints")),
            "canonical_retrieval": details,
            "raw_metadata": metadata_flat or source_metadata or source_row,
        },
        trace={"rank": rank, "backend": "canonical_visual_sidecar"},
    )


def search_canonical_visual(
    query_plan: dict[str, Any] | None,
    limit: int,
    sidecar_path: Path = DEFAULT_CANONICAL_VISUAL_SIDECAR,
    source_path: Path = DEFAULT_VISUAL_CAPTION_SOURCE,
) -> list[EvidenceItem]:
    if not query_plan:
        return []
    if not sidecar_path.exists():
        return []
    query_terms = canonical_set(query_plan.get("canonical_terms"))
    required_terms = canonical_set(query_plan.get("required_terms"))
    if not query_terms and not required_terms:
        return []
    _, rows = get_canonical_visual_rows(str(sidecar_path))
    source_by_id = get_visual_caption_source_rows(str(source_path)) if source_path.exists() else {}
    scored: list[tuple[float, dict[str, Any], dict[str, Any]]] = []
    for row in rows:
        score, details = canonical_visual_score(query_plan, row)
        if score <= 0:
            continue
        scored.append((score, row, details))
    scored.sort(key=lambda item: item[0], reverse=True)
    items: list[EvidenceItem] = []
    for rank, (score, row, details) in enumerate(scored[: max(limit * 3, limit)], start=1):
        visual_id = str(row.get("visual_id") or "")
        items.append(canonical_visual_to_evidence(row, source_by_id.get(visual_id), score, details, rank))
    return items


def canonical_visual_sources_for_collection(visual_collection: str) -> list[tuple[Path, Path]]:
    sources = [(DEFAULT_CANONICAL_VISUAL_SIDECAR, DEFAULT_VISUAL_CAPTION_SOURCE)]
    if visual_collection == VISUAL_COLLECTIONS["mathrock_mixed_trial"]:
        sources.append((MATHROCK_CANONICAL_VISUAL_SIDECAR, MATHROCK_VISUAL_CAPTION_SOURCE))
    return sources


def search_canonical_visual_all(
    query_plan: dict[str, Any] | None,
    limit: int,
    visual_collection: str,
) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    seen: set[str] = set()
    for sidecar_path, source_path in canonical_visual_sources_for_collection(visual_collection):
        for item in search_canonical_visual(query_plan, limit, sidecar_path=sidecar_path, source_path=source_path):
            key = str(item.evidence_id)
            if key in seen:
                continue
            seen.add(key)
            items.append(item)
    items.sort(key=lambda item: item.score, reverse=True)
    return items[: max(limit * 4, limit)]


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
    return rerank_kg_items(task.query, items, max(task.top_k * 3, task.top_k))


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


def enrich_visual_items_with_canonical(items: list[EvidenceItem]) -> None:
    if not DEFAULT_CANONICAL_VISUAL_SIDECAR.exists():
        return
    by_id, _ = get_canonical_visual_rows(str(DEFAULT_CANONICAL_VISUAL_SIDECAR))
    for item in items:
        visual_id = str(item.metadata.get("visual_id") or item.metadata.get("chunk_id") or "").replace("visual_caption:", "")
        row = by_id.get(visual_id)
        if not row:
            continue
        item.metadata.setdefault("canonical_terms", as_list(row.get("canonical_terms")))
        item.metadata.setdefault("required_terms", as_list(row.get("required_terms")))
        item.metadata.setdefault("optional_terms", as_list(row.get("optional_terms")))
        item.metadata.setdefault("negative_constraints", as_list(row.get("negative_constraints")))
        item.metadata["canonical_sidecar_status"] = row.get("status")


def merge_evidence(results: dict[str, list[EvidenceItem]]) -> tuple[list[EvidenceItem], list[EvidenceItem], list[EvidenceItem]]:
    text_items = dedupe_items(results.get("fretboard_text", []) + results.get("style_text", []))
    raw_visual_items = results.get("visual_caption", [])
    enrich_visual_items_with_canonical(raw_visual_items)
    visual_items = dedupe_items(raw_visual_items)
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
        style_blob = " ".join(
            value
            for item in text
            for value in [
                json.dumps(item.metadata, ensure_ascii=False),
                item.source_id,
                item.title,
                item.content[:500],
            ]
            if value
        ).lower()
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
    started = time.perf_counter()
    context = json.loads(args.context_json) if args.context_json else {}
    query_plan = context.get("query_plan") if isinstance(context.get("query_plan"), dict) else None
    visual_collection = str(
        getattr(args, "visual_collection", "") or COLLECTIONS["visual_caption"]
    )
    if query_plan:
        analysis = analysis_from_query_plan(args.query, query_plan)
        plan = plan_retrieval_from_query_plan(query_plan, args.top_k, visual_collection)
        if not plan:
            plan = plan_retrieval(analysis, args.top_k, visual_collection)
    else:
        analysis = analyze_query(args.query, context=context)
        plan = plan_retrieval(analysis, args.top_k, visual_collection)

    model_started = time.perf_counter()
    embedder = get_cached_embedder(args.model, args.device, args.max_length)
    model_seconds = time.perf_counter() - model_started
    client = get_cached_chroma_client(str(args.chroma_path))

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

    if query_plan:
        canonical_started = time.perf_counter()
        canonical_items = search_canonical_visual_all(query_plan, args.top_k, visual_collection)
        if canonical_items:
            results.setdefault("visual_caption", []).extend(canonical_items)
        timings["canonical_visual_seconds"] = time.perf_counter() - canonical_started

    text, visual, kg = merge_evidence(results)
    model_rerank_started = time.perf_counter()
    rerank_config = RerankConfig.from_env()
    text, text_model_rerank = apply_model_rerank(analysis.query, text, rerank_config)
    visual, visual_model_rerank = apply_model_rerank(analysis.query, visual, rerank_config)
    kg, kg_model_rerank = apply_model_rerank(analysis.query, kg, rerank_config)
    timings["model_rerank_seconds"] = time.perf_counter() - model_rerank_started
    text, visual, kg = apply_domain_rerank(text, visual, kg, analysis, query_plan)
    judgement = judge_bundle(analysis, text, visual, kg)
    answer_seed = build_answer_seed(None, analysis, text, visual, kg)
    if query_plan:
        answer_seed["query_plan"] = query_plan
    answer_seed["visual_collection"] = visual_collection
    answer_seed["model_rerank"] = {
        "text": text_model_rerank,
        "visual": visual_model_rerank,
        "kg": kg_model_rerank,
    }
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
    parser.add_argument(
        "--visual-collection",
        default=COLLECTIONS["visual_caption"],
        choices=sorted(set(VISUAL_COLLECTIONS.values())),
    )
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
