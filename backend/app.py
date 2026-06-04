from __future__ import annotations

import json
import mimetypes
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FRONTEND = ROOT / "frontend"

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


def safe_rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return str(path)


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
