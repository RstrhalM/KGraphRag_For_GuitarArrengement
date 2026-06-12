from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import re
import time
from collections import Counter
from dataclasses import asdict
from datetime import datetime
from functools import lru_cache
from pathlib import Path
import sys
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FRONTEND = ROOT / "frontend"
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from answer_composer import compose_answer, render_answer_markdown
from prompt_registry import get_prompt_registry, get_prompt_versions
from query_normalizer import normalize_query
from query_rag_bundle import DEFAULT_LOCAL_MODEL, VISUAL_COLLECTIONS, render_markdown, run_bundle
try:
    from .session_memory import SessionMemoryStore
except ImportError:  # Allow `python backend/app.py` style local debugging.
    from session_memory import SessionMemoryStore

CHUNK_SOURCES: dict[str, Path] = {
    "mathrock_text_course": DATA / "processed" / "mathrock" / "mathrock_text" / "chunks.json",
    "mathrock_pdf_steve_h": DATA / "processed" / "mathrock" / "pdf_kg_extract" / "chunks.json",
    "cory_wong_funk_core": DATA / "processed" / "style_rhythm" / "cory_wong_funk" / "chunks.json",
    "fretboard_exercise_answer_aligned": DATA
    / "processed"
    / "fretboard_handbook"
    / "exercise_answer_aligned"
    / "chunks.json",
    "fretboard_question_answer_segments": DATA
    / "processed"
    / "fretboard_handbook"
    / "question_answer_segment_manifest"
    / "chunks.json",
    "fretboard_handbook_clean_text": DATA / "processed" / "fretboard_handbook" / "text_clean" / "chunks.json",
    "fretboard_chunks_002_005": DATA / "processed" / "mineru_full_gpu" / "kg_extract_chunks_002_005" / "chunks.json",
    "fretboard_chunks_006_010": DATA / "processed" / "mineru_full_gpu" / "kg_extract_chunks_006_010" / "chunks.json",
}

MARKDOWN_CHUNK_SOURCES: dict[str, Path] = {
    "fretboard_handbook_full_md": DATA
    / "processed"
    / "mineru_full_gpu"
    / "吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)"
    / "ocr"
    / "吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org).md",
    "mathrock_pdf_full_md": DATA
    / "processed"
    / "mathrock"
    / "pdf_mineru"
    / "Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans"
    / "auto"
    / "Math-Rock-Guitar-E-book-November-2020-dcnauy_onlyTrans.md",
}

VISUAL_SOURCES: dict[str, Path] = {
    "fretboard_manifest": DATA / "processed" / "fretboard_handbook" / "visual_layer" / "fretboard_visual_manifest.jsonl",
    "mathrock_manifest": DATA / "processed" / "mathrock" / "visual_layer" / "mathrock_visual_manifest.jsonl",
    "visual_caption_layer": DATA / "processed" / "visual_caption_layer" / "visual_caption_accepted_all.jsonl",
    "fretboard_answer_caption_layer": DATA
    / "processed"
    / "fretboard_handbook"
    / "question_answer_visual_caption_layer"
    / "fretboard_answer_visual_caption_accepted_all.jsonl",
}

SOURCE_GROUP_HINTS: dict[str, list[str]] = {
    "mathrock_text_course": ["arrangement_kg_mathrock_text"],
    "mathrock_pdf_steve_h": ["mathrock_pdf_kg", "mathrock_pdf_visual_supplement_kg"],
    "cory_wong_funk_core": ["arrangement_kg_cory_wong_funk_core"],
    "fretboard_exercise_answer_aligned": ["arrangement_kg", "arrangement_kg_chunks_006_010", "arrangement_kg_integrated_chunks_011_015"],
    "fretboard_chunks_002_005": ["arrangement_kg", "arrangement_kg_visual_answer_chunks_002_010"],
    "fretboard_chunks_006_010": ["arrangement_kg_chunks_006_010", "arrangement_kg_visual_answer_chunks_002_010"],
    "fretboard_handbook_full_md": ["arrangement_kg", "arrangement_kg_chunks_006_010", "arrangement_kg_integrated_chunks_011_015"],
    "mathrock_pdf_full_md": ["mathrock_pdf_kg", "mathrock_pdf_visual_supplement_kg"],
}

BOOKS: dict[str, dict[str, Any]] = {
    "fretboard_handbook": {
        "title": "吉他指板手册",
        "kind": "book_pdf",
        "description": "MinerU 全书 Markdown、练习答案对照、早期 KG 抽取批次与指板视觉清单。",
        "source_ids": [
            "fretboard_handbook_full_md",
            "fretboard_handbook_clean_text",
            "fretboard_exercise_answer_aligned",
            "fretboard_question_answer_segments",
            "fretboard_chunks_002_005",
            "fretboard_chunks_006_010",
        ],
    },
    "cory_wong_funk": {
        "title": "Cory Wong Funk 吉他大师课",
        "kind": "course_text",
        "description": "Funk 节奏吉他课程文本与已审核 KG。",
        "source_ids": ["cory_wong_funk_core"],
    },
    "mathrock_text": {
        "title": "Math Rock 文字课程",
        "kind": "course_text",
        "description": "Math Rock / Midwest Emo 文字课程。",
        "source_ids": ["mathrock_text_course"],
    },
    "mathrock_pdf": {
        "title": "Math Rock PDF",
        "kind": "book_pdf",
        "description": "MinerU 全书 Markdown、KG 抽取 chunk 与多模态补抽 KG。",
        "source_ids": ["mathrock_pdf_full_md", "mathrock_pdf_steve_h"],
    },
}


app = FastAPI(title="Guitar Arrangement Knowledge Workbench", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_local_dev_cache_headers(request, call_next):
    response = await call_next(request)
    if request.url.path == "/" or request.url.path.startswith("/static/"):
        response.headers["Cache-Control"] = "no-store, max-age=0"
    return response

QUERY_LOG = DATA / "eval" / "manual_query_log.jsonl"
QUERY_FEEDBACK_LOG = DATA / "eval" / "query_normalizer_feedback.jsonl"
QUERY_REPORT_DIR = DATA / "eval" / "manual_queries"
SESSION_MEMORY = SessionMemoryStore(DATA / "eval" / "session_memory")

VISUAL_COLLECTION_LABELS = {
    "formal": "正式视觉库 · 389",
    "mathrock_mixed_trial": "Math Rock 混合试验库 · 398",
}


class QueryRunRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=1200)
    notes: str = Field(default="", max_length=2000)
    tags: list[str] = Field(default_factory=list)
    context: dict[str, Any] = Field(default_factory=dict)
    top_k: int = Field(default=5, ge=1, le=12)
    kg_limit: int = Field(default=8, ge=0, le=30)
    use_normalizer: bool = True
    rerank_backend: str = Field(default="none", max_length=20)
    rerank_model: str = Field(default="models/reranker/qwen3-reranker-0.6b", max_length=300)
    rerank_weight: float = Field(default=0.35, ge=0.0, le=1.0)
    rerank_batch_size: int = Field(default=4, ge=1, le=16)
    rerank_max_length: int = Field(default=1024, ge=256, le=8192)
    visual_collection: str = Field(default="formal", max_length=40)
    compose_answer: bool = False
    session_id: str = Field(default="", max_length=120)


class QueryNormalizeRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=1200)
    notes: str = Field(default="", max_length=2000)
    tags: list[str] = Field(default_factory=list)
    context: dict[str, Any] = Field(default_factory=dict)
    session_id: str = Field(default="", max_length=120)


class QuerySaveRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=1200)
    notes: str = Field(default="", max_length=2000)
    tags: list[str] = Field(default_factory=list)
    context: dict[str, Any] = Field(default_factory=dict)
    status: str = Field(default="draft", max_length=40)
    session_id: str = Field(default="", max_length=120)


class QueryFeedbackRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=1200)
    source: str = Field(default="normalize", max_length=40)
    normalized_query: str = Field(default="", max_length=2000)
    intent: str = Field(default="", max_length=80)
    expected_intent: str = Field(default="", max_length=80)
    expected_tools: list[str] = Field(default_factory=list)
    scores: dict[str, int] = Field(default_factory=dict)
    failure_tags: list[str] = Field(default_factory=list)
    notes: str = Field(default="", max_length=3000)
    query_plan: dict[str, Any] = Field(default_factory=dict)
    bundle_summary: dict[str, Any] = Field(default_factory=dict)
    report_md: str = Field(default="", max_length=500)
    session_id: str = Field(default="", max_length=120)


def safe_rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return str(path)


def utc_timestamp() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def query_report_stem(query: str) -> str:
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    digest = hashlib.sha1(query.encode("utf-8")).hexdigest()[:10]
    return f"manual_query_{now}_{digest}"


def append_query_log(row: dict[str, Any]) -> None:
    QUERY_LOG.parent.mkdir(parents=True, exist_ok=True)
    with QUERY_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def append_feedback_log(row: dict[str, Any]) -> None:
    QUERY_FEEDBACK_LOG.parent.mkdir(parents=True, exist_ok=True)
    with QUERY_FEEDBACK_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def rerank_request_config(request: QueryRunRequest) -> dict[str, Any]:
    backend = (request.rerank_backend or "none").strip().lower()
    if backend not in {"none", "local", "env"}:
        backend = "none"
    return {
        "backend": backend,
        "model": request.rerank_model.strip() or "models/reranker/qwen3-reranker-0.6b",
        "weight": request.rerank_weight,
        "batch_size": request.rerank_batch_size,
        "max_length": request.rerank_max_length,
    }


def resolve_visual_collection(profile: str) -> tuple[str, str]:
    normalized = (profile or "formal").strip().lower()
    if normalized not in VISUAL_COLLECTIONS:
        normalized = "formal"
    return normalized, VISUAL_COLLECTIONS[normalized]


def apply_rerank_env(config: dict[str, Any]) -> dict[str, str | None]:
    keys = ["RERANK_BACKEND", "RERANK_MODEL", "RERANK_WEIGHT", "RERANK_BATCH_SIZE", "RERANK_MAX_LENGTH"]
    previous = {key: os.environ.get(key) for key in keys}
    if config["backend"] != "env":
        os.environ["RERANK_BACKEND"] = str(config["backend"])
        os.environ["RERANK_MODEL"] = str(config["model"])
        os.environ["RERANK_WEIGHT"] = str(config["weight"])
        os.environ["RERANK_BATCH_SIZE"] = str(config["batch_size"])
        os.environ["RERANK_MAX_LENGTH"] = str(config["max_length"])
    return previous


def restore_rerank_env(previous: dict[str, str | None]) -> None:
    for key, value in previous.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


def render_query_plan_markdown(query_plan: dict[str, Any] | None, normalizer_error: str = "") -> str:
    lines: list[str] = ["", "## LLM QueryPlan", ""]
    if normalizer_error:
        lines.extend(["", f"- Normalizer error: `{normalizer_error}`", ""])
    if query_plan:
        lines.extend(["```json", json.dumps(query_plan, ensure_ascii=False, indent=2), "```", ""])
    else:
        lines.append("未使用 LLM normalizer；本次由规则层直接规划检索。")
    return "\n".join(lines)


def read_query_log(limit: int = 80) -> list[dict[str, Any]]:
    rows = read_jsonl(QUERY_LOG)
    return list(reversed(rows[-limit:]))


def read_feedback_log(limit: int = 80) -> list[dict[str, Any]]:
    rows = read_jsonl(QUERY_FEEDBACK_LOG)
    return list(reversed(rows[-limit:]))


def bundle_summary_from_payload(payload: dict[str, Any]) -> dict[str, Any]:
    judgement = payload.get("judgement") or {}
    answer = payload.get("composed_answer") or {}
    answer_seed = payload.get("answer_seed") or {}
    return {
        "text_count": len(payload.get("text_evidence") or []),
        "visual_count": len(payload.get("visual_evidence") or []),
        "kg_count": len(payload.get("kg_evidence") or []),
        "sufficient": judgement.get("sufficient"),
        "confidence": judgement.get("confidence"),
        "model_rerank": answer_seed.get("model_rerank", {}),
        "answer_summary": answer.get("summary", ""),
        "theory_check_count": len(answer.get("theory_checks") or []),
        "prompt_versions": payload.get("prompt_versions") or answer_seed.get("prompt_versions", {}),
    }


def append_memory_session(row: dict[str, Any]) -> dict[str, Any]:
    return SESSION_MEMORY.append_session(row)


def resolve_workspace_path(raw_path: str) -> Path:
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    resolved = candidate.resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise HTTPException(status_code=403, detail="Path is outside workspace") from exc
    if not resolved.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {raw_path}")
    return resolved


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path, limit: int | None = None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(row, dict):
                rows.append(row)
            if limit and len(rows) >= limit:
                break
    return rows


def text_preview(text: str, chars: int = 220) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= chars:
        return text
    return text[:chars].rstrip() + "..."


def image_ref_basename(ref: str) -> str:
    return Path(str(ref).replace("\\", "/")).name


def extract_image_refs(text: str) -> list[str]:
    refs = re.findall(r"\[IMAGE_BLOCK:([^\]]+)\]", text)
    refs.extend(re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text))
    seen: set[str] = set()
    ordered: list[str] = []
    for ref in refs:
        if ref not in seen:
            seen.add(ref)
            ordered.append(ref)
    return ordered


def split_markdown_chunks(path: Path, source_id: str, max_chars: int = 3200) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    sections: list[tuple[str, str]] = []
    current_title = "Front Matter"
    current_lines: list[str] = []
    for line in lines:
        heading = re.match(r"^\s{0,3}(#{1,3})\s+(.+?)\s*$", line)
        if heading and current_lines:
            sections.append((current_title, "\n".join(current_lines).strip()))
            current_lines = []
        if heading:
            current_title = heading.group(2).strip()
        current_lines.append(line)
    if current_lines:
        sections.append((current_title, "\n".join(current_lines).strip()))

    chunks: list[dict[str, Any]] = []
    for title, section_text in sections:
        if not section_text:
            continue
        part = 1
        start = 0
        while start < len(section_text):
            end = min(start + max_chars, len(section_text))
            if end < len(section_text):
                paragraph_break = section_text.rfind("\n\n", start, end)
                if paragraph_break > start + 500:
                    end = paragraph_break
            chunk_text = section_text[start:end].strip()
            if chunk_text:
                chunks.append(
                    {
                        "chunk_id": f"md_chunk_{len(chunks) + 1:04d}",
                        "lesson_title": title if part == 1 else f"{title} / part {part}",
                        "page_hint": None,
                        "text": chunk_text,
                        "image_refs": extract_image_refs(chunk_text),
                        "source_id": source_id,
                        "source_title": source_title(source_id),
                        "path": safe_rel(path),
                    }
                )
            part += 1
            start = end
    return chunks


def source_title(source_id: str) -> str:
    titles = {
        "mathrock_text_course": "Math Rock 文字课程",
        "mathrock_pdf_full_md": "Math Rock PDF full Markdown",
        "mathrock_pdf_steve_h": "Math Rock PDF",
        "cory_wong_funk_core": "Cory Wong Funk 课程",
        "fretboard_exercise_answer_aligned": "吉他指板手册练习答案对照",
        "fretboard_question_answer_segments": "吉他指板手册练习答案题目级分块",
        "fretboard_handbook_clean_text": "吉他指板手册正文清洗层",
        "fretboard_chunks_002_005": "吉他指板手册 chunks 002-005",
        "fretboard_chunks_006_010": "吉他指板手册 chunks 006-010",
        "fretboard_handbook_full_md": "吉他指板手册 full Markdown",
        "fretboard_manifest": "吉他指板手册视觉清单",
        "mathrock_manifest": "Math Rock PDF 视觉清单",
        "visual_caption_layer": "实验视觉 Caption 层",
        "fretboard_answer_caption_layer": "吉他指板手册题目级答案 Caption 层",
    }
    return titles.get(source_id, source_id)


@lru_cache(maxsize=1)
def load_chunks() -> dict[str, list[dict[str, Any]]]:
    loaded: dict[str, list[dict[str, Any]]] = {}
    for source_id, path in MARKDOWN_CHUNK_SOURCES.items():
        loaded[source_id] = split_markdown_chunks(path, source_id)
    for source_id, path in CHUNK_SOURCES.items():
        raw = read_json(path, [])
        if not isinstance(raw, list):
            raw = []
        rows: list[dict[str, Any]] = []
        for index, item in enumerate(raw):
            if not isinstance(item, dict):
                continue
            row = dict(item)
            row.setdefault("chunk_id", f"chunk_{index + 1:04d}")
            row["source_id"] = source_id
            row["source_title"] = source_title(source_id)
            row["path"] = safe_rel(path)
            rows.append(row)
        loaded[source_id] = rows
    return loaded


@lru_cache(maxsize=1)
def load_visuals() -> dict[str, list[dict[str, Any]]]:
    loaded: dict[str, list[dict[str, Any]]] = {}
    for source_id, path in VISUAL_SOURCES.items():
        rows = []
        for row in read_jsonl(path):
            item = dict(row)
            item["visual_source"] = source_id
            item["visual_source_title"] = source_title(source_id)
            meta = item.get("source_metadata") if isinstance(item.get("source_metadata"), dict) else {}
            item.setdefault("source_id", meta.get("source_id") or source_id)
            item.setdefault("source_title", meta.get("source_title") or source_title(source_id))
            item.setdefault("image_path", meta.get("image_path"))
            item.setdefault("page", meta.get("page"))
            item.setdefault("priority", meta.get("priority"))
            rows.append(item)
        loaded[source_id] = rows
    return loaded


@lru_cache(maxsize=1)
def load_edges() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    knowledge_dir = DATA / "knowledge"
    if not knowledge_dir.exists():
        return rows
    for path in sorted(knowledge_dir.glob("*/accepted_edges.jsonl")):
        source_group = path.parent.name
        for edge in read_jsonl(path):
            item = dict(edge)
            item["source_group"] = source_group
            item["path"] = safe_rel(path)
            rows.append(item)
    return rows


@lru_cache(maxsize=1)
def load_image_index() -> dict[str, list[str]]:
    image_index: dict[str, list[str]] = {}
    for root in [DATA / "processed", DATA / "练习解答（图片）"]:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
                continue
            image_index.setdefault(path.name, []).append(safe_rel(path))
    return image_index


@lru_cache(maxsize=1)
def visual_by_image_name() -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = {}
    for rows in load_visuals().values():
        for row in rows:
            image_path = row.get("image_path")
            if not image_path:
                continue
            index.setdefault(image_ref_basename(str(image_path)), []).append(row)
    return index


def edge_matches_chunk(edge: dict[str, Any], source_id: str, chunk_id: str) -> bool:
    provenance = edge.get("provenance") if isinstance(edge.get("provenance"), dict) else {}
    if str(provenance.get("chunk_id") or "") != chunk_id:
        return False
    hints = SOURCE_GROUP_HINTS.get(source_id)
    if not hints:
        return True
    return str(edge.get("source_group") or "") in hints


def edges_for_chunk(source_id: str, chunk_id: str) -> list[dict[str, Any]]:
    return [edge for edge in load_edges() if edge_matches_chunk(edge, source_id, chunk_id)]


def compact_edge(edge: dict[str, Any]) -> dict[str, Any]:
    provenance = edge.get("provenance") if isinstance(edge.get("provenance"), dict) else {}
    return {
        "source": edge.get("source"),
        "relation": edge.get("relation"),
        "target": edge.get("target"),
        "knowledge_type": edge.get("knowledge_type"),
        "confidence": edge.get("confidence"),
        "context_condition": edge.get("context_condition"),
        "review_note": edge.get("review_note"),
        "evidence": edge.get("evidence"),
        "source_group": edge.get("source_group"),
        "chunk_id": provenance.get("chunk_id"),
        "review_id": provenance.get("review_id"),
        "path": edge.get("path"),
    }


def book_id_for_source(source_id: str) -> str | None:
    for book_id, book in BOOKS.items():
        if source_id in book.get("source_ids", []):
            return book_id
    return None


def images_for_refs(refs: list[Any]) -> list[dict[str, Any]]:
    image_index = load_image_index()
    visual_index = visual_by_image_name()
    rows: list[dict[str, Any]] = []
    for ref in refs:
        basename = image_ref_basename(str(ref))
        paths = image_index.get(basename, [])
        visuals = visual_index.get(basename, [])
        rows.append(
            {
                "ref": str(ref),
                "basename": basename,
                "paths": paths,
                "primary_path": paths[0] if paths else None,
                "visuals": [
                    {
                        "visual_id": item.get("visual_id"),
                        "topic": item.get("topic") or item.get("topic_hint"),
                        "image_type": item.get("image_type") or item.get("source_type") or item.get("priority"),
                        "page": item.get("page"),
                        "caption": text_preview(str(item.get("caption") or item.get("nearby_text") or ""), 180),
                    }
                    for item in visuals[:5]
                ],
            }
        )
    return rows


def report_files() -> list[Path]:
    eval_dir = DATA / "eval"
    if not eval_dir.exists():
        return []
    return sorted(eval_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)


@app.get("/api/health")
def health() -> dict[str, Any]:
    return {"ok": True, "root": str(ROOT)}


@app.get("/api/dashboard")
def dashboard() -> dict[str, Any]:
    chunks = load_chunks()
    visuals = load_visuals()
    edges = load_edges()
    relation_counts = Counter(str(edge.get("relation") or "unknown") for edge in edges)
    nodes = {str(edge.get("source")) for edge in edges if edge.get("source")}
    nodes.update(str(edge.get("target")) for edge in edges if edge.get("target"))
    visual_count = sum(len(rows) for rows in visuals.values())
    accepted_caption_count = len(visuals.get("fretboard_answer_caption_layer", []))
    return {
        "sources": len(chunks),
        "chunks": sum(len(rows) for rows in chunks.values()),
        "visual_items": visual_count,
        "visual_captions": accepted_caption_count,
        "kg_edges": len(edges),
        "kg_nodes": len(nodes),
        "relations": relation_counts.most_common(12),
        "reports": len(report_files()),
        "collections": [
            {"name": "guitar_text_chunks_qwen3_06b", "kind": "text", "docs": 68},
            {"name": "guitar_fretboard_handbook_text_qwen3_06b", "kind": "text_clean", "docs": 174},
            {"name": "guitar_fretboard_answer_captions_qwen3_06b", "kind": "visual_caption", "docs": 389},
            {"name": "guitar_visual_captions_qwen3_06b", "kind": "visual_caption_experiment", "docs": 60},
            {"name": "guitar_visual_chunks", "kind": "raw_visual", "docs": 504},
        ],
    }


@app.get("/api/sources")
def sources() -> dict[str, Any]:
    chunks = load_chunks()
    visuals = load_visuals()
    edge_counts = Counter(edge.get("source_group") for edge in load_edges())
    rows = []
    for source_id, chunk_rows in chunks.items():
        if source_id in MARKDOWN_CHUNK_SOURCES:
            rows.append(
                {
                    "source_id": source_id,
                    "title": source_title(source_id),
                    "kind": "markdown_chunks",
                    "path": safe_rel(MARKDOWN_CHUNK_SOURCES[source_id]),
                    "chunks": len(chunk_rows),
                    "visuals": 0,
                    "kg_edges": edge_counts.get(source_id, 0),
                }
            )
    for source_id, chunk_rows in chunks.items():
        if source_id not in CHUNK_SOURCES:
            continue
        rows.append(
            {
                "source_id": source_id,
                "title": source_title(source_id),
                "kind": "text_chunks",
                "path": safe_rel(CHUNK_SOURCES[source_id]),
                "chunks": len(chunk_rows),
                "visuals": 0,
                "kg_edges": edge_counts.get(source_id, 0),
            }
        )
    for source_id, visual_rows in visuals.items():
        rows.append(
            {
                "source_id": source_id,
                "title": source_title(source_id),
                "kind": "visuals",
                "path": safe_rel(VISUAL_SOURCES[source_id]),
                "chunks": 0,
                "visuals": len(visual_rows),
                "kg_edges": 0,
            }
        )
    knowledge_dirs = sorted((DATA / "knowledge").glob("*")) if (DATA / "knowledge").exists() else []
    for path in knowledge_dirs:
        if path.is_dir():
            rows.append(
                {
                    "source_id": path.name,
                    "title": path.name,
                    "kind": "knowledge_edges",
                    "path": safe_rel(path),
                    "chunks": 0,
                    "visuals": 0,
                    "kg_edges": edge_counts.get(path.name, 0),
                }
            )
    return {"items": rows}


@app.get("/api/books")
def books() -> dict[str, Any]:
    chunks = load_chunks()
    edge_counts = Counter(edge.get("source_group") for edge in load_edges())
    rows: list[dict[str, Any]] = []
    for book_id, book in BOOKS.items():
        source_rows: list[dict[str, Any]] = []
        total_chunks = 0
        total_edges = 0
        total_images = 0
        for source_id in book.get("source_ids", []):
            chunk_rows = chunks.get(source_id, [])
            source_edges = sum(
                len(edges_for_chunk(source_id, str(row.get("chunk_id") or "")))
                for row in chunk_rows
            )
            source_images = sum(
                len(row.get("image_refs") if isinstance(row.get("image_refs"), list) else [])
                for row in chunk_rows
            )
            total_chunks += len(chunk_rows)
            total_edges += source_edges
            total_images += source_images
            source_rows.append(
                {
                    "source_id": source_id,
                    "title": source_title(source_id),
                    "chunks": len(chunk_rows),
                    "kg_edges": source_edges,
                    "image_refs": source_images,
                    "source_group_edges": edge_counts.get(source_id, 0),
                }
            )
        rows.append(
            {
                "book_id": book_id,
                "title": book["title"],
                "kind": book["kind"],
                "description": book["description"],
                "chunks": total_chunks,
                "kg_edges": total_edges,
                "image_refs": total_images,
                "sources": source_rows,
            }
        )
    return {"items": rows}


@app.get("/api/chunks")
def chunks(
    book_id: str | None = None,
    source_id: str | None = None,
    q: str | None = None,
    limit: int = Query(default=500, ge=1, le=500),
) -> dict[str, Any]:
    loaded = load_chunks()
    if source_id:
        selected_sources = [source_id]
    elif book_id:
        book = BOOKS.get(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        selected_sources = [sid for sid in book.get("source_ids", []) if sid in loaded]
    else:
        selected_sources = list(loaded)
    rows: list[dict[str, Any]] = []
    total = 0
    query = (q or "").lower().strip()
    for sid in selected_sources:
        for row in loaded.get(sid, []):
            text = str(row.get("text") or "")
            if query and query not in text.lower() and query not in str(row.get("chunk_id", "")).lower():
                continue
            total += 1
            if len(rows) >= limit:
                continue
            image_refs = row.get("image_refs")
            if not isinstance(image_refs, list):
                image_refs = []
            related_edges = edges_for_chunk(sid, str(row.get("chunk_id") or ""))
            rows.append(
                {
                    "source_id": sid,
                    "book_id": book_id_for_source(sid),
                    "source_title": row.get("source_title"),
                    "chunk_id": row.get("chunk_id"),
                    "lesson_title": row.get("lesson_title") or row.get("page_hint") or "",
                    "chars": len(text),
                    "image_refs": len(image_refs),
                    "kg_edges": len(related_edges),
                    "preview": text_preview(text),
                }
            )
    return {"items": rows, "limit": limit, "total": total, "truncated": total > len(rows)}


@app.get("/api/chunk")
def chunk_detail(source_id: str, chunk_id: str) -> dict[str, Any]:
    for row in load_chunks().get(source_id, []):
        if str(row.get("chunk_id")) == chunk_id:
            result = dict(row)
            image_refs = row.get("image_refs")
            if not isinstance(image_refs, list):
                image_refs = []
            related_edges = edges_for_chunk(source_id, chunk_id)
            result["resolved_images"] = images_for_refs(image_refs)
            result["kg_edges"] = [compact_edge(edge) for edge in related_edges]
            result["kg_edge_count"] = len(related_edges)
            return result
    raise HTTPException(status_code=404, detail="Chunk not found")


@app.get("/api/visuals")
def visuals(
    source_id: str | None = None,
    q: str | None = None,
    limit: int = Query(default=80, ge=1, le=500),
) -> dict[str, Any]:
    loaded = load_visuals()
    selected_sources = [source_id] if source_id else list(loaded)
    query = (q or "").lower().strip()
    rows: list[dict[str, Any]] = []
    for sid in selected_sources:
        for row in loaded.get(sid, []):
            meta = row.get("source_metadata") if isinstance(row.get("source_metadata"), dict) else {}
            crop_path = row.get("crop_path") or meta.get("crop_path") or row.get("image_path") or meta.get("image_path")
            question_text = row.get("question_text") or meta.get("question_text") or meta.get("subquestion_prompt") or ""
            caption_text = row.get("caption_text") or row.get("caption") or row.get("nearby_text") or ""
            primary_haystack = " ".join(
                str(value or "")
                for value in [
                    row.get("visual_id"),
                    row.get("segment_id"),
                    row.get("caption"),
                    row.get("caption_text"),
                    row.get("topic"),
                    row.get("topic_hint"),
                    row.get("musical_object"),
                    row.get("root"),
                    row.get("quality_or_mode"),
                    row.get("position_or_shape"),
                    row.get("retrieval_keywords"),
                    row.get("image_type"),
                    row.get("visual_type"),
                    row.get("priority"),
                    meta.get("exercise_number"),
                    meta.get("subquestion_number"),
                ]
            ).lower()
            secondary_haystack = " ".join(
                str(value or "")
                for value in [question_text, row.get("nearby_text")]
            ).lower()
            if query and query not in primary_haystack and query not in secondary_haystack:
                continue
            score = 0
            if query:
                if query in str(row.get("visual_id") or row.get("segment_id") or "").lower():
                    score += 40
                if query in str(row.get("musical_object") or row.get("topic") or "").lower():
                    score += 30
                if query in str(row.get("caption") or "").lower():
                    score += 20
                if query in primary_haystack:
                    score += 10
                if query in secondary_haystack:
                    score += 1
            rows.append(
                {
                    "_score": score,
                    "visual_source": sid,
                    "visual_source_title": row.get("visual_source_title") or source_title(sid),
                    "visual_id": row.get("visual_id") or row.get("segment_id"),
                    "segment_id": row.get("segment_id") or row.get("visual_id"),
                    "source_id": row.get("source_id") or meta.get("source_id"),
                    "page": row.get("page") or meta.get("page") or meta.get("source_image"),
                    "image_type": row.get("image_type") or row.get("visual_type") or row.get("source_type") or row.get("priority"),
                    "visual_type": row.get("visual_type") or row.get("image_type") or "",
                    "topic": row.get("topic") or row.get("musical_object") or row.get("topic_hint") or "",
                    "musical_object": row.get("musical_object") or row.get("topic") or "",
                    "root": row.get("root") or "",
                    "quality_or_mode": row.get("quality_or_mode") or "",
                    "position_or_shape": row.get("position_or_shape") or "",
                    "intervals": row.get("intervals") or [],
                    "retrieval_keywords": row.get("retrieval_keywords") or [],
                    "exercise_number": meta.get("exercise_number") or row.get("exercise_number") or "",
                    "subquestion_number": meta.get("subquestion_number") or row.get("subquestion_number") or "",
                    "evidence_type": meta.get("evidence_type") or row.get("evidence_type") or "",
                    "caption_layer": row.get("caption_layer") or "",
                    "image_path": crop_path,
                    "source_image": meta.get("source_image") or "",
                    "bbox": meta.get("bbox") or row.get("bbox") or {},
                    "question_text": question_text,
                    "caption": text_preview(str(row.get("caption") or caption_text), 260),
                    "caption_full": str(caption_text),
                    "arrangement_value": row.get("arrangement_value") or "",
                }
            )
            if len(rows) >= limit and not query:
                return {"items": rows, "limit": limit}
    if query:
        rows.sort(key=lambda item: int(item.get("_score") or 0), reverse=True)
    for item in rows:
        item.pop("_score", None)
    return {"items": rows[:limit], "limit": limit}


@app.get("/api/graph/summary")
def graph_summary() -> dict[str, Any]:
    edges = load_edges()
    relation_counts = Counter(str(edge.get("relation") or "unknown") for edge in edges)
    type_counts = Counter(str(edge.get("knowledge_type") or "unknown") for edge in edges)
    group_counts = Counter(str(edge.get("source_group") or "unknown") for edge in edges)
    nodes = {str(edge.get("source")) for edge in edges if edge.get("source")}
    nodes.update(str(edge.get("target")) for edge in edges if edge.get("target"))
    return {
        "edges": len(edges),
        "nodes": len(nodes),
        "relations": relation_counts.most_common(),
        "knowledge_types": type_counts.most_common(),
        "source_groups": group_counts.most_common(),
    }


@app.get("/api/graph/filters")
def graph_filters() -> dict[str, Any]:
    edges = load_edges()
    return {
        "relations": sorted({str(edge.get("relation") or "") for edge in edges if edge.get("relation")}),
        "source_groups": sorted({str(edge.get("source_group") or "") for edge in edges if edge.get("source_group")}),
        "knowledge_types": sorted({str(edge.get("knowledge_type") or "") for edge in edges if edge.get("knowledge_type")}),
    }


@app.get("/api/graph/search")
def graph_search(
    q: str = "",
    relation: str | None = None,
    source_group: str | None = None,
    knowledge_type: str | None = None,
    limit: int = Query(default=60, ge=1, le=300),
) -> dict[str, Any]:
    query = q.lower().strip()
    matched: list[dict[str, Any]] = []
    for edge in load_edges():
        if relation and str(edge.get("relation") or "") != relation:
            continue
        if source_group and str(edge.get("source_group") or "") != source_group:
            continue
        if knowledge_type and str(edge.get("knowledge_type") or "") != knowledge_type:
            continue
        haystack = " ".join(
            str(edge.get(key) or "")
            for key in ["source", "relation", "target", "knowledge_type", "context_condition", "review_note", "evidence"]
        ).lower()
        if query and query not in haystack:
            continue
        matched.append(edge)
        if len(matched) >= limit:
            break
    node_ids: dict[str, str] = {}
    nodes: list[dict[str, Any]] = []
    links: list[dict[str, Any]] = []
    for index, edge in enumerate(matched):
        source = str(edge.get("source") or "")
        target = str(edge.get("target") or "")
        for label in [source, target]:
            if label and label not in node_ids:
                node_id = f"n{len(node_ids) + 1}"
                node_ids[label] = node_id
                nodes.append({"id": node_id, "label": label})
        if source and target:
            links.append(
                {
                    "id": f"e{index + 1}",
                    "source": node_ids[source],
                    "target": node_ids[target],
                    "label": str(edge.get("relation") or ""),
                    "evidence": edge.get("evidence") or edge.get("context_condition") or "",
                    "source_group": edge.get("source_group"),
                }
            )
    return {"nodes": nodes, "edges": links, "raw_edges": [compact_edge(edge) for edge in matched]}


@app.get("/api/graph/neighborhood")
def graph_neighborhood(node: str, limit: int = Query(default=80, ge=1, le=300)) -> dict[str, Any]:
    query = node.strip()
    matched = [
        edge
        for edge in load_edges()
        if str(edge.get("source") or "") == query or str(edge.get("target") or "") == query
    ][:limit]
    node_ids: dict[str, str] = {}
    nodes: list[dict[str, Any]] = []
    links: list[dict[str, Any]] = []
    for index, edge in enumerate(matched):
        source = str(edge.get("source") or "")
        target = str(edge.get("target") or "")
        for label in [source, target]:
            if label and label not in node_ids:
                node_id = f"n{len(node_ids) + 1}"
                node_ids[label] = node_id
                nodes.append({"id": node_id, "label": label})
        if source and target:
            links.append(
                {
                    "id": f"e{index + 1}",
                    "source": node_ids[source],
                    "target": node_ids[target],
                    "label": str(edge.get("relation") or ""),
                    "evidence": edge.get("evidence") or edge.get("context_condition") or "",
                    "source_group": edge.get("source_group"),
                }
            )
    return {"nodes": nodes, "edges": links, "raw_edges": [compact_edge(edge) for edge in matched]}


@app.get("/api/reports")
def reports() -> dict[str, Any]:
    items = [
        {
            "name": path.name,
            "path": safe_rel(path),
            "size": path.stat().st_size,
            "modified": path.stat().st_mtime,
        }
        for path in report_files()
    ]
    return {"items": items}


@app.get("/api/query/prompts")
def query_prompts() -> dict[str, Any]:
    return {
        "principles": [
            {
                "title": "面向编曲任务，不面向练习编号",
                "text": "正式 query 应描述你要解决的编曲问题。练习答案图只作为指型/和弦图/音阶图的可视化证据参与召回。",
            },
            {
                "title": "写清风格目标",
                "text": "尽量写出 funk、math rock、midwest emo、blues、jazz fusion 等风格，或描述 groove、开放弦、切分、riff 密度等声音目标。",
            },
            {
                "title": "写清素材和限制",
                "text": "给出和弦、调性、音阶、riff 材料、把位限制、是否需要开放弦、是否要省略音、是否面向伴奏或主奏。",
            },
            {
                "title": "让视觉 caption 做证据",
                "text": "如果你需要具体指型、voicing、同把位大小调映射，可以在 query 里写“给我可视化指型/把位参考”。",
            },
        ],
        "templates": [
            {
                "label": "和声材料 -> 风格 riff",
                "query": "我想把 Fmaj7 琶音发展成 math rock 风格的开放弦 riff，有哪些把位和指型可选？",
                "tags": ["mathrock", "riff", "fretboard"],
            },
            {
                "label": "节奏风格 -> voicing",
                "query": "funk 十六分切分节奏里，如何选择更省动作的双音或三音和弦指型，让 riff 更有 groove？",
                "tags": ["funk", "rhythm", "voicing"],
            },
            {
                "label": "调性转换 -> 同把位指型",
                "query": "D 大调旋律想转成 B 小调色彩时，有没有同把位指型可以参考，并说明适合怎样的 riff 写法？",
                "tags": ["fretboard", "relative-minor", "visual"],
            },
            {
                "label": "谱例分析 -> 编配建议",
                "query": "一段 120bpm 的 Am-F-C-G 进行想做成 math rock 伴奏，节奏、开放弦和 tapping 可以怎么安排？",
                "tags": ["workflow", "mathrock", "arrangement"],
            },
            {
                "label": "约束型指型推荐",
                "query": "在 5 到 9 品范围内，用 E 小调五声音阶做 funk riff，哪些指型适合和闷音切分结合？",
                "tags": ["funk", "constraint", "visual"],
            },
        ],
        "evaluation_axes": [
            "是否命中正确意图：风格编配、指板/把位、视觉指型、KG 关系",
            "是否召回至少两类互相支持的证据：文本、视觉 caption、KG",
            "视觉证据是否服务于具体指型/voicing/riff，而不是练习编号本身",
            "风格 query 是否能保持风格边界，不被其他教材误召回",
            "耗时是否符合后端常驻 embedding 模型后的交互要求",
        ],
    }


@app.get("/api/prompts/versions")
def prompt_versions() -> dict[str, Any]:
    return {
        "active": get_prompt_versions(include_planned=False),
        "registry": get_prompt_registry(),
    }


@app.get("/api/query/logs")
def query_logs(limit: int = Query(default=80, ge=1, le=300)) -> dict[str, Any]:
    return {"items": read_query_log(limit)}


@app.get("/api/query/feedback")
def query_feedback_logs(limit: int = Query(default=80, ge=1, le=300)) -> dict[str, Any]:
    return {"items": read_feedback_log(limit)}


@app.get("/api/memory/sessions")
def memory_sessions(
    limit: int = Query(default=80, ge=1, le=300),
    status: str = "",
    q: str = "",
    tag: str = "",
) -> dict[str, Any]:
    return {
        "items": SESSION_MEMORY.list_sessions(limit=limit, status=status.strip(), q=q.strip(), tag=tag.strip()),
        "store": safe_rel(SESSION_MEMORY.session_log),
    }


@app.get("/api/memory/session")
def memory_session(session_id: str) -> dict[str, Any]:
    session = SESSION_MEMORY.get_session(session_id.strip())
    if not session:
        raise HTTPException(status_code=404, detail=f"Session not found: {session_id}")
    return {"item": session}


@app.post("/api/query/feedback")
def save_query_feedback(request: QueryFeedbackRequest) -> dict[str, Any]:
    allowed_score_keys = {
        "schema_score",
        "intent_score",
        "tool_selection_score",
        "slot_score",
        "tool_query_score",
        "downstream_score",
        "overall_score",
    }
    scores = {
        key: int(value)
        for key, value in request.scores.items()
        if key in allowed_score_keys and isinstance(value, int | float)
    }
    row = {
        "timestamp": utc_timestamp(),
        "status": "feedback",
        "query": request.query.strip(),
        "source": request.source,
        "normalized_query": request.normalized_query.strip(),
        "intent": request.intent,
        "expected_intent": request.expected_intent,
        "expected_tools": request.expected_tools,
        "scores": scores,
        "failure_tags": request.failure_tags,
        "notes": request.notes.strip(),
        "query_plan": request.query_plan,
        "bundle_summary": request.bundle_summary,
        "report_md": request.report_md,
        "session_id": request.session_id.strip(),
    }
    append_feedback_log(row)
    if request.session_id.strip():
        SESSION_MEMORY.append_event(request.session_id.strip(), "feedback_saved", row)
    return {"ok": True, "item": row, "feedback_log": safe_rel(QUERY_FEEDBACK_LOG)}


@app.post("/api/query/save")
def save_query(request: QuerySaveRequest) -> dict[str, Any]:
    row = {
        "timestamp": utc_timestamp(),
        "status": request.status,
        "query": request.query.strip(),
        "notes": request.notes.strip(),
        "tags": request.tags,
        "context": request.context,
    }
    append_query_log(row)
    session = append_memory_session(
        {
            **row,
            "session_id": request.session_id.strip(),
            "memory_type": "query_draft",
            "source": "frontend_manual_query_workbench",
        }
    )
    return {"ok": True, "item": row, "session": session, "session_id": session["session_id"]}


@app.post("/api/query/normalize")
def normalize_manual_query(request: QueryNormalizeRequest) -> dict[str, Any]:
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query is empty")
    context = dict(request.context or {})
    if request.notes:
        context["human_notes"] = request.notes.strip()
    if request.tags:
        context["human_tags"] = request.tags
    try:
        query_plan = normalize_query(query, context=context, env_file=ROOT / ".env")
    except Exception as exc:
        append_query_log(
            {
                "timestamp": utc_timestamp(),
                "status": "normalize_error",
                "query": query,
                "notes": request.notes.strip(),
                "tags": request.tags,
                "error": str(exc),
            }
        )
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    row = {
        "timestamp": utc_timestamp(),
        "status": "normalized",
        "query": query,
        "normalized_query": query_plan.get("normalized_query", ""),
        "notes": request.notes.strip(),
        "tags": request.tags,
        "intent": query_plan.get("intent", ""),
        "style_hints": query_plan.get("style_hints", []),
        "query_plan": query_plan,
        "prompt_versions": get_prompt_versions(),
    }
    append_query_log(row)
    session = append_memory_session(
        {
            **row,
            "session_id": request.session_id.strip(),
            "memory_type": "query_normalization",
            "source": "frontend_manual_query_workbench",
            "notes": request.notes.strip(),
            "context": context,
        }
    )
    return {"ok": True, "query_plan": query_plan, "log_item": row, "session": session, "session_id": session["session_id"]}


@app.post("/api/query/run")
def run_query(request: QueryRunRequest) -> dict[str, Any]:
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query is empty")
    QUERY_REPORT_DIR.mkdir(parents=True, exist_ok=True)
    visual_profile, visual_collection = resolve_visual_collection(request.visual_collection)
    stem = f"{query_report_stem(query)}_{visual_profile}"
    report_md = QUERY_REPORT_DIR / f"{stem}.md"
    report_json = QUERY_REPORT_DIR / f"{stem}.json"
    context = dict(request.context or {})
    if request.notes:
        context["human_notes"] = request.notes
    if request.tags:
        context["human_tags"] = request.tags
    rerank_config = rerank_request_config(request)
    context["rerank_config"] = rerank_config
    context["prompt_versions"] = get_prompt_versions()
    context["visual_collection"] = {
        "profile": visual_profile,
        "collection": visual_collection,
        "label": VISUAL_COLLECTION_LABELS[visual_profile],
    }
    query_plan: dict[str, Any] | None = None
    normalizer_error = ""
    if request.use_normalizer:
        try:
            query_plan = normalize_query(query, context=context, env_file=ROOT / ".env")
            context["query_plan"] = query_plan
            context["query_normalizer"] = {
                "provider": "llm_api",
                "status": "ok",
                "spec": "QUERY_NORMALIZATION_PROMPT_SPEC.md",
            }
        except Exception as exc:
            normalizer_error = str(exc)
            context["query_normalizer"] = {
                "provider": "llm_api",
                "status": "error_fallback_to_rules",
                "error": normalizer_error,
            }
    args = argparse.Namespace(
        query=query,
        context_json=json.dumps(context, ensure_ascii=False),
        top_k=request.top_k,
        kg_limit=request.kg_limit,
        chroma_path=DATA / "chroma",
        model=os.environ.get("LOCAL_EMBEDDING_MODEL", DEFAULT_LOCAL_MODEL),
        device=os.environ.get("LOCAL_EMBEDDING_DEVICE", "auto"),
        max_length=int(os.environ.get("LOCAL_EMBEDDING_MAX_LENGTH", "2048")),
        batch_size=8,
        visual_collection=visual_collection,
        env_file=ROOT / ".env",
        report_md=report_md,
        report_json=report_json,
    )
    previous_rerank_env = apply_rerank_env(rerank_config)
    try:
        bundle = run_bundle(args)
    except Exception as exc:
        error_row = {
            "timestamp": utc_timestamp(),
            "status": "run_error",
            "query": query,
            "notes": request.notes.strip(),
            "tags": request.tags,
            "rerank_config": rerank_config,
            "error": str(exc),
            "session_id": request.session_id.strip(),
            "memory_type": "rag_run_error",
            "source": context.get("source", "frontend_manual_query_workbench"),
        }
        append_query_log(error_row)
        append_memory_session(error_row)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        restore_rerank_env(previous_rerank_env)
    payload = asdict(bundle)
    payload["rerank_config"] = rerank_config
    payload["visual_collection"] = context["visual_collection"]
    payload["prompt_versions"] = context["prompt_versions"]
    if query_plan:
        payload["query_plan"] = query_plan
    if normalizer_error:
        payload["normalizer_error"] = normalizer_error
    composed_answer: dict[str, Any] | None = None
    answer_error = ""
    if request.compose_answer:
        try:
            answer_started = time.perf_counter()
            composed_answer = compose_answer(payload, env_file=ROOT / ".env")
            payload["composed_answer"] = composed_answer
            bundle.timings["answer_composer_seconds"] = time.perf_counter() - answer_started
            payload["timings"] = bundle.timings
        except Exception as exc:
            answer_error = str(exc)
            payload["answer_composer_error"] = answer_error
    report_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    report_md.write_text(
        render_markdown(bundle)
        + render_query_plan_markdown(query_plan, normalizer_error)
        + (render_answer_markdown(composed_answer or {}) if request.compose_answer and composed_answer else "")
        + (f"\n\n## Answer Composer Error\n\n`{answer_error}`\n" if answer_error else ""),
        encoding="utf-8",
    )
    log_row = {
        "timestamp": utc_timestamp(),
        "status": "ran",
        "query": query,
        "normalized_query": query_plan.get("normalized_query", "") if query_plan else "",
        "notes": request.notes.strip(),
        "tags": request.tags,
        "intent": bundle.analysis.intent,
        "style_hints": bundle.analysis.style_hints,
        "judgement": bundle.judgement,
        "timings": bundle.timings,
        "rerank_config": rerank_config,
        "visual_collection": context["visual_collection"],
        "prompt_versions": context["prompt_versions"],
        "model_rerank": bundle.answer_seed.get("model_rerank", {}),
        "normalizer_used": request.use_normalizer,
        "normalizer_error": normalizer_error,
        "compose_answer": request.compose_answer,
        "answer_summary": composed_answer.get("summary", "") if composed_answer else "",
        "answer_composer_error": answer_error,
        "query_plan": query_plan,
        "report_md": safe_rel(report_md),
        "report_json": safe_rel(report_json),
    }
    append_query_log(log_row)
    session = append_memory_session(
        {
            **log_row,
            "session_id": request.session_id.strip(),
            "memory_type": "full_chain_run" if request.compose_answer else "rag_run",
            "source": context.get("source", "frontend_manual_query_workbench"),
            "context": context,
            "bundle_summary": bundle_summary_from_payload(payload),
            "answer_status": "ok" if composed_answer else ("error" if answer_error else "not_requested"),
        }
    )
    return {
        "ok": True,
        "bundle": payload,
        "report_md": safe_rel(report_md),
        "report_json": safe_rel(report_json),
        "log_item": log_row,
        "session": session,
        "session_id": session["session_id"],
        "query_plan": query_plan,
        "normalizer_error": normalizer_error,
        "composed_answer": composed_answer,
        "answer_composer_error": answer_error,
    }


@app.get("/api/report")
def report(name: str) -> PlainTextResponse:
    path = DATA / "eval" / name
    resolved = resolve_workspace_path(str(path))
    if resolved.suffix.lower() != ".md":
        raise HTTPException(status_code=400, detail="Only markdown reports are exposed")
    return PlainTextResponse(resolved.read_text(encoding="utf-8"), media_type="text/markdown; charset=utf-8")


@app.get("/api/file")
def file(path: str) -> FileResponse:
    resolved = resolve_workspace_path(path)
    media_type, _ = mimetypes.guess_type(resolved.name)
    return FileResponse(resolved, media_type=media_type or "application/octet-stream")


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    index_path = FRONTEND / "index.html"
    if not index_path.exists():
        return "<h1>Frontend not found</h1>"
    return index_path.read_text(encoding="utf-8")


if FRONTEND.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND), name="static")
