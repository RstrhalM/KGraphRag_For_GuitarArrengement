#!/usr/bin/env python
"""Ingest structured visual captions into a text-embedding Chroma collection."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

from local_text_embedding import DEFAULT_LOCAL_MODEL, LocalTransformerEmbedder, write_model_metadata


DEFAULT_CHROMA_PATH = Path("data/chroma")
DEFAULT_COLLECTION = "guitar_visual_captions_qwen3_06b"


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
                raise ValueError(f"Invalid JSON in {path} line {line_no}: {exc}") from exc
            if isinstance(row, dict):
                rows.append(row)
    return rows


def metadata_value(value: Any) -> str | int | float | bool:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return value
    return json.dumps(value, ensure_ascii=False)


def stable_id(value: str) -> str:
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:16]
    safe = "".join(ch if ch.isalnum() or ch in "_.:-" else "_" for ch in value)[:140]
    return f"{safe}:{digest}"


def row_to_doc(row: dict[str, Any]) -> dict[str, Any]:
    meta = row.get("source_metadata") if isinstance(row.get("source_metadata"), dict) else {}
    visual_id = str(row.get("visual_id") or meta.get("visual_id") or "")
    caption_text = str(row.get("caption_text") or row.get("caption") or "")
    canonical_terms = [str(item) for item in row.get("canonical_terms") or [] if str(item).strip()]
    document = caption_text
    if canonical_terms:
        document += "\ncanonical_terms: " + ", ".join(canonical_terms)
    metadata = {
        "visual_id": visual_id,
        "source_id": meta.get("source_id", ""),
        "source_title": meta.get("source_title", ""),
        "page": meta.get("page", ""),
        "priority": meta.get("priority", ""),
        "visual_granularity": meta.get("visual_granularity", ""),
        "image_path": meta.get("image_path", ""),
        "crop_path": meta.get("crop_path", meta.get("image_path", "")),
        "source_image": meta.get("source_image", ""),
        "exercise_number": meta.get("exercise_number", ""),
        "subquestion_number": meta.get("subquestion_number", ""),
        "evidence_type": meta.get("evidence_type", ""),
        "mapping_method": meta.get("mapping_method", ""),
        "question_text": meta.get("question_text", meta.get("subquestion_prompt", "")),
        "topic_hint": meta.get("topic_hint", ""),
        "nearby_text": meta.get("nearby_text", ""),
        "style_tags": meta.get("style_tags", []),
        "caption_layer": row.get("caption_layer", ""),
        "segment_id": row.get("segment_id", visual_id),
        "visual_type": row.get("visual_type", row.get("image_type", "")),
        "musical_object": row.get("musical_object", row.get("topic", "")),
        "quality_or_mode": row.get("quality_or_mode", ""),
        "position_or_shape": row.get("position_or_shape", ""),
        "intervals": row.get("intervals", []),
        "retrieval_keywords": row.get("retrieval_keywords", []),
        "image_type": row.get("image_type", ""),
        "topic": row.get("topic", ""),
        "tuning": row.get("tuning", ""),
        "key": row.get("key", ""),
        "root": row.get("root", ""),
        "caption": row.get("caption", ""),
        "arrangement_value": row.get("arrangement_value", ""),
        "confidence": row.get("confidence", 0.0),
        "uncertain_fields": row.get("uncertain_fields", []),
        "entities": row.get("entities", {}),
        "visible_structure": row.get("visible_structure", {}),
        "canonical_terms": canonical_terms,
        "canonical_status": (row.get("canonical_sidecar") or {}).get("status", "")
        if isinstance(row.get("canonical_sidecar"), dict)
        else "",
    }
    return {
        "id": stable_id(visual_id),
        "document": document,
        "metadata": {key: metadata_value(value) for key, value in metadata.items()},
    }


def batched(items: list[dict[str, Any]], size: int) -> list[list[dict[str, Any]]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--captions", type=Path, required=True)
    parser.add_argument("--chroma-path", type=Path, default=DEFAULT_CHROMA_PATH)
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--model", default=os.environ.get("LOCAL_EMBEDDING_MODEL", DEFAULT_LOCAL_MODEL))
    parser.add_argument("--device", default=os.environ.get("LOCAL_EMBEDDING_DEVICE", "auto"))
    parser.add_argument("--max-length", type=int, default=int(os.environ.get("LOCAL_EMBEDDING_MAX_LENGTH", "2048")))
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--reset", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        import chromadb
    except ImportError as exc:
        raise RuntimeError("Missing dependency: install chromadb first") from exc

    rows = read_jsonl(args.captions)
    docs = [row_to_doc(row) for row in rows if str(row.get("caption_text") or row.get("caption") or "").strip()]
    embedder = LocalTransformerEmbedder(args.model, device=args.device, max_length=args.max_length)

    client = chromadb.PersistentClient(path=str(args.chroma_path))
    if args.reset:
        try:
            client.delete_collection(args.collection)
        except Exception:
            pass
    collection = client.get_or_create_collection(name=args.collection, metadata={"hnsw:space": "cosine"})

    total = 0
    for batch in batched(docs, args.batch_size):
        embeddings = embedder.embed([item["document"] for item in batch], batch_size=args.batch_size)
        collection.upsert(
            ids=[item["id"] for item in batch],
            documents=[item["document"] for item in batch],
            metadatas=[item["metadata"] for item in batch],
            embeddings=embeddings,
        )
        total += len(batch)
        print(f"upserted {total}/{len(docs)}")

    metadata = {
        "collection": args.collection,
        "source_captions": str(args.captions),
        **embedder.metadata(),
    }
    write_model_metadata(args.chroma_path / f"{args.collection}.embedding_metadata.json", metadata)
    report = {
        "captions": len(rows),
        "documents": len(docs),
        "collection": args.collection,
        "collection_count": collection.count(),
        "embedding": metadata,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
