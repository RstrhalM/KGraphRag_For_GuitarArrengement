#!/usr/bin/env python
"""Query the visual Chroma collection with qwen3-vl-embedding text input."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from embedding_cache import EmbeddingCache
from smoke_qwen_vl_embedding import QwenVLEmbedder, apply_env_file


DEFAULT_EMBEDDING_CACHE = Path("data/cache/embeddings.sqlite")


FRETBOARD_PRIORITY_RULES: list[dict] = [
    {
        "priority": "P3_common_scales_chords",
        "strong": ["其他常用和弦", "常用和弦", "六和弦", "九和弦", "加九", "6/9", "add9", "add 9"],
        "weak": ["extended chord", "dominant 9", "dom9"],
    },
    {
        "priority": "P2_arpeggios_chords",
        "strong": ["琶音", "三和弦", "七和弦", "大三和弦", "arpeggio", "triad", "maj7", "m7", "dom7"],
        "weak": ["caged", "shape", "shapes", "voicing"],
    },
    {
        "priority": "P1_scales_intervals",
        "strong": ["音程", "八度", "大三度", "小三度", "纯五度", "interval", "octave", "third", "fifth", "pentatonic", "scale"],
        "weak": ["double stop", "two notes per string", "音阶"],
    },
    {
        "priority": "P0_root_fingering_forms",
        "strong": ["根音型式", "根音指型", "五种根音", "root fingering", "root pattern", "root form"],
        "weak": ["root shape", "root cycle", "cycle", "overlap", "重叠", "循环"],
    },
]


def score_visual_priorities(query: str) -> dict[str, float]:
    lowered = query.lower()
    scores: dict[str, float] = {}
    for rule in FRETBOARD_PRIORITY_RULES:
        priority = str(rule["priority"])
        score = 0.0
        for needle in rule.get("strong", []):
            if str(needle).lower() in lowered:
                score += 3.0
        for needle in rule.get("weak", []):
            if str(needle).lower() in lowered:
                score += 1.0
        scores[priority] = score
    if "根音" in query and "指型" in query:
        scores["P0_root_fingering_forms"] = scores.get("P0_root_fingering_forms", 0.0) + 1.5
    if ("八度" in query or "octave" in lowered) and ("根音" in query or "root" in lowered):
        scores["P1_scales_intervals"] = scores.get("P1_scales_intervals", 0.0) + 1.5
    if ("caged" in lowered or "五种" in query) and ("三和弦" in query or "triad" in lowered):
        scores["P2_arpeggios_chords"] = scores.get("P2_arpeggios_chords", 0.0) + 1.5
    if ("add9" in lowered or "加九" in query) and ("dom" in lowered or "dominant" in lowered or "属" in query):
        scores["P3_common_scales_chords"] = scores.get("P3_common_scales_chords", 0.0) + 1.5
    return scores


def infer_visual_priorities(query: str) -> list[str]:
    scores = score_visual_priorities(query)
    return [priority for priority, score in sorted(scores.items(), key=lambda item: (-item[1], item[0])) if score > 0]


def chroma_where(source_id: str, priority: str) -> dict | None:
    filters = []
    if source_id:
        filters.append({"source_id": source_id})
    if priority:
        filters.append({"priority": priority})
    if not filters:
        return None
    if len(filters) == 1:
        return filters[0]
    return {"$and": filters}


def keyword_overlap_score(query: str, metadata: dict) -> float:
    text = " ".join(
        str(metadata.get(key) or "")
        for key in ["topic_hint", "nearby_text", "source_title", "priority", "image_name"]
    ).lower()
    lowered = query.lower()
    score = 0.0
    for token in set(lowered.replace("/", " ").replace("_", " ").split()):
        if len(token) >= 3 and token in text:
            score += 0.25
    for token in ["根音", "指型", "音程", "八度", "琶音", "三和弦", "七和弦", "六和弦", "九和弦", "五声音阶"]:
        if token in query and token in text:
            score += 0.75
    return score


def rerank_rows(rows: list[tuple[str, dict, float]], query: str, priority_scores: dict[str, float]) -> list[tuple[str, dict, float, float]]:
    reranked = []
    for doc_id, metadata, distance in rows:
        priority = str(metadata.get("priority") or "")
        score = priority_scores.get(priority, 0.0) + keyword_overlap_score(query, metadata)
        reranked.append((doc_id, metadata, distance, score))
    reranked.sort(key=lambda row: (-row[3], row[2]))
    return reranked


def merge_rows(*groups: list[tuple[str, dict, float]]) -> list[tuple[str, dict, float]]:
    merged: dict[str, tuple[str, dict, float]] = {}
    for group in groups:
        for row in group:
            current = merged.get(row[0])
            if current is None or row[2] < current[2]:
                merged[row[0]] = row
    return list(merged.values())


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    parser.add_argument("--chroma-path", type=Path, default=Path("data/chroma"))
    parser.add_argument("--collection", default="guitar_visual_chunks")
    parser.add_argument("--query", required=True)
    parser.add_argument("--n-results", type=int, default=5)
    parser.add_argument("--source-id", default="")
    parser.add_argument("--priority", default="")
    parser.add_argument("--no-auto-priority", action="store_true")
    parser.add_argument("--embedding-cache", type=Path, default=DEFAULT_EMBEDDING_CACHE)
    parser.add_argument("--no-embedding-cache", action="store_true")
    args = parser.parse_args(argv)
    apply_env_file(args.env_file)
    args.chroma_path = Path(os.environ.get("CHROMA_PATH", str(args.chroma_path)))
    args.collection = os.environ.get("CHROMA_VISUAL_COLLECTION", args.collection)
    return args


def embed_text_cached(embedder: QwenVLEmbedder, query: str, cache: EmbeddingCache) -> tuple[list[float], bool]:
    cache_key = EmbeddingCache.make_key(
        provider="dashscope_multimodal",
        model=embedder.model,
        dimensions=embedder.dimensions,
        input_type="multimodal_text",
        content=query,
        endpoint=embedder.api_url,
    )
    cached = cache.get(cache_key)
    if cached is not None:
        return cached, True
    vector = embedder.embed_text(query)
    cache.set(
        cache_key,
        vector,
        provider="dashscope_multimodal",
        model=embedder.model,
        dimensions=embedder.dimensions,
        input_type="multimodal_text",
        content=query,
    )
    return vector, False


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    import chromadb

    embedder = QwenVLEmbedder()
    cache = EmbeddingCache(args.embedding_cache, enabled=not args.no_embedding_cache)
    collection = chromadb.PersistentClient(path=str(args.chroma_path)).get_collection(args.collection)
    priority_scores = score_visual_priorities(args.query)
    priority = args.priority
    inferred_priorities = infer_visual_priorities(args.query) if not args.no_auto_priority else []
    if not priority and inferred_priorities:
        priority = ""
    where = chroma_where(args.source_id, priority)
    query_vector, cache_hit = embed_text_cached(embedder, args.query, cache)
    result = collection.query(
        query_embeddings=[query_vector],
        n_results=max(args.n_results * 5, args.n_results),
        where=where,
        include=["documents", "metadatas", "distances"],
    )
    if not result.get("ids", [[]])[0] and where is not None and priority and not args.priority:
        result = collection.query(
            query_embeddings=[query_vector],
            n_results=args.n_results,
            where=chroma_where(args.source_id, ""),
            include=["documents", "metadatas", "distances"],
        )
    rows = []
    for idx, doc_id in enumerate(result.get("ids", [[]])[0]):
        rows.append((doc_id, result["metadatas"][0][idx], float(result["distances"][0][idx])))
    if inferred_priorities and not args.no_auto_priority:
        priority_rows = []
        for inferred_priority in inferred_priorities[:3]:
            priority_result = collection.query(
                query_embeddings=[query_vector],
                n_results=max(args.n_results, 8),
                where=chroma_where(args.source_id, inferred_priority),
                include=["documents", "metadatas", "distances"],
            )
            for idx, doc_id in enumerate(priority_result.get("ids", [[]])[0]):
                priority_rows.append(
                    (doc_id, priority_result["metadatas"][0][idx], float(priority_result["distances"][0][idx]))
                )
        rows = merge_rows(rows, priority_rows)
    reranked = rerank_rows(rows, args.query, priority_scores)[: args.n_results]
    print(
        json.dumps(
            {
                "inferred_priorities": inferred_priorities,
                "priority_scores": priority_scores,
                "where": where,
                "embedding_cache_hit": cache_hit,
                "embedding_cache": cache.stats(),
            },
            ensure_ascii=False,
        )
    )
    for idx, (doc_id, metadata, distance, rerank_score) in enumerate(reranked, start=1):
        print(f"\n## {idx}. {doc_id} distance={distance:.4f} rerank={rerank_score:.2f}")
        print(f"- source: {metadata.get('source_title')} / page {metadata.get('page')}")
        print(f"- priority: {metadata.get('priority')}")
        print(f"- image: {metadata.get('image_path')}")
        print(f"- topic: {metadata.get('topic_hint')}")
        print(f"- nearby: {metadata.get('nearby_text')}")
    print(json.dumps({"count": len(result.get("ids", [[]])[0])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
