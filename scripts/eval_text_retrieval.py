"""Evaluate local text RAG retrieval over a Chroma collection."""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from local_text_embedding import DEFAULT_LOCAL_MODEL, LocalTransformerEmbedder


DEFAULT_CHROMA_PATH = ROOT / "data" / "chroma"
DEFAULT_COLLECTION = "guitar_text_chunks_qwen3_06b"
DEFAULT_TESTS = ROOT / "data" / "eval" / "text_rag_expanded_tests.json"
DEFAULT_REPORT_MD = ROOT / "data" / "eval" / "text_rag_expanded_report.md"
DEFAULT_REPORT_JSON = ROOT / "data" / "eval" / "text_rag_expanded_report.json"


def load_tests(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("tests", [])
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON array or an object with a tests array")
    return data


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def compact_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "source_id",
        "source_title",
        "source_type",
        "chunk_id",
        "lesson_title",
        "page_hint",
        "style_tags",
        "gp5_feature_triggers",
        "linked_kg_nodes",
        "linked_kg_edges",
        "image_refs",
    ]
    return {key: metadata.get(key) for key in keys if metadata.get(key) not in (None, "")}


def text_blob(hit: dict[str, Any]) -> str:
    return "\n".join(
        [
            str(hit.get("id") or ""),
            str(hit.get("document") or ""),
            json.dumps(hit.get("metadata") or {}, ensure_ascii=False),
        ]
    ).lower()


def contains_any(hit: dict[str, Any], needles: list[str]) -> bool:
    blob = text_blob(hit)
    return any(str(needle).lower() in blob for needle in needles)


TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9#/+.-]{1,}|[\u4e00-\u9fff]{2,}")
CHINESE_KEYWORDS = [
    "点弦",
    "调弦",
    "开放弦",
    "和弦",
    "琶音",
    "指板",
    "节奏",
    "律动",
    "消音",
    "留白",
    "声部",
    "音阶",
    "根音",
    "转位",
    "密集",
    "切分",
]


def query_tokens(query: str) -> set[str]:
    lowered = query.lower()
    tokens = {token.lower() for token in TOKEN_RE.findall(lowered)}
    tokens.update(keyword for keyword in CHINESE_KEYWORDS if keyword in query)
    return {token for token in tokens if len(token) >= 2}


def inferred_source_boosts(query: str) -> dict[str, float]:
    q = query.lower()
    boosts: dict[str, float] = {}
    if any(marker in q for marker in ["cory", "funk", "groove", "muted", "chuck", "ghost", "sixteenth", "pocket"]):
        boosts["cory_wong_funk_core"] = boosts.get("cory_wong_funk_core", 0.0) + 0.055
    if any(marker in q for marker in ["math rock", "midwest", "dadgad", "tapping", "hammer", "pull", "open string"]):
        boosts["mathrock_text_course"] = boosts.get("mathrock_text_course", 0.0) + 0.035
        boosts["mathrock_pdf_steve_h"] = boosts.get("mathrock_pdf_steve_h", 0.0) + 0.025
    if any(marker in q for marker in ["pdf", "facgce", "daeac#e", "shell", "cm9", "dsus4", "g6/9", "c6", "jazz"]):
        boosts["mathrock_pdf_steve_h"] = boosts.get("mathrock_pdf_steve_h", 0.0) + 0.060
    if any(marker in q for marker in ["指板", "琶音", "根音", "大三和弦", "小三和弦", "减三和弦", "属七", "加九", "六九"]):
        boosts["fretboard_handbook_mineru"] = boosts.get("fretboard_handbook_mineru", 0.0) + 0.050
    return boosts


def rerank_hits(hits: list[dict[str, Any]], query: str) -> list[dict[str, Any]]:
    tokens = query_tokens(query)
    source_boosts = inferred_source_boosts(query)
    ranked = []
    for original_rank, hit in enumerate(hits, start=1):
        blob = text_blob(hit)
        metadata = hit.get("metadata") or {}
        source_id = str(metadata.get("source_id") or "")
        matched = sorted(token for token in tokens if token in blob)
        token_score = len(matched) * 0.010
        source_score = source_boosts.get(source_id, 0.0)
        generic_penalty = 0.0
        chunk_id = str(metadata.get("chunk_id") or "")
        if source_id == "fretboard_handbook_mineru" and chunk_id in {"md_chunk_0002", "md_chunk_0037"}:
            generic_penalty -= 0.060
        if "关于作" in str(hit.get("document") or "") or "如何应用本书" in str(hit.get("document") or ""):
            generic_penalty -= 0.040
        final_score = -float(hit.get("distance") or 0.0) + token_score + source_score + generic_penalty
        row = dict(hit)
        row["original_rank"] = original_rank
        row["rerank_score"] = final_score
        row["rerank_details"] = {
            "matched_tokens": matched[:12],
            "token_score": token_score,
            "source_score": source_score,
            "generic_penalty": generic_penalty,
        }
        ranked.append(row)
    ranked.sort(key=lambda item: (-float(item["rerank_score"]), int(item["original_rank"])))
    for rank, item in enumerate(ranked, start=1):
        item["rank"] = rank
    return ranked


def render_preview(text: str, limit: int = 220) -> str:
    text = " ".join(text.split())
    text = text.replace("|", "\\|")
    return text if len(text) <= limit else text[: limit - 1] + "..."


def evaluate(args: argparse.Namespace) -> dict[str, Any]:
    import chromadb

    tests = load_tests(args.tests)
    embedder = LocalTransformerEmbedder(args.model, device=args.device, max_length=args.max_length)
    collection = chromadb.PersistentClient(path=str(args.chroma_path)).get_collection(args.collection)

    rows: list[dict[str, Any]] = []
    for test in tests[: args.limit or None]:
        started = time.perf_counter()
        embedding = embedder.embed([test["query"]], batch_size=1)[0]
        embed_seconds = time.perf_counter() - started

        query_started = time.perf_counter()
        candidate_count = max(args.top_k, args.rerank_candidates if args.rerank else args.top_k)
        result = collection.query(query_embeddings=[embedding], n_results=candidate_count)
        query_seconds = time.perf_counter() - query_started

        hits = []
        for rank, (item_id, document, metadata, distance) in enumerate(
            zip(
                result.get("ids", [[]])[0],
                result.get("documents", [[]])[0],
                result.get("metadatas", [[]])[0],
                result.get("distances", [[]])[0],
            ),
            start=1,
        ):
            hit = {
                "rank": rank,
                "id": item_id,
                "distance": distance,
                "document": document,
                "metadata": compact_metadata(metadata or {}),
            }
            expected_sources = test.get("text_sources", [])
            expected_keywords = test.get("expected_keywords_any", [])
            hit["source_expected"] = bool(expected_sources) and hit["metadata"].get("source_id") in expected_sources
            hit["keyword_expected"] = bool(expected_keywords) and contains_any(hit, expected_keywords)
            hits.append(hit)

        if args.rerank:
            hits = rerank_hits(hits, test["query"])
        hits = hits[: args.top_k]

        expected_sources = test.get("text_sources", [])
        expected_keywords = test.get("expected_keywords_any", [])
        source_first = next((hit["rank"] for hit in hits if hit["source_expected"]), None)
        keyword_first = next((hit["rank"] for hit in hits if hit["keyword_expected"]), None)
        pass_source = not expected_sources or source_first is not None
        pass_keyword = not expected_keywords or keyword_first is not None
        rows.append(
            {
                "id": test["id"],
                "query": test["query"],
                "text_sources": expected_sources,
                "expected_keywords_any": expected_keywords,
                "rerank": args.rerank,
                "rerank_candidates": candidate_count,
                "source_first_rank": source_first,
                "keyword_first_rank": keyword_first,
                "pass_source": pass_source,
                "pass_keyword": pass_keyword,
                "pass_all": pass_source and pass_keyword,
                "embed_seconds": embed_seconds,
                "query_seconds": query_seconds,
                "total_seconds": embed_seconds + query_seconds,
                "results": hits,
            }
        )

    totals = [row["total_seconds"] for row in rows]
    model_metadata = embedder.metadata()
    summary = {
        "tests": len(rows),
        "collection": args.collection,
        "collection_count": collection.count(),
        "top_k": args.top_k,
        "rerank": args.rerank,
        "rerank_candidates": args.rerank_candidates if args.rerank else args.top_k,
        "pass_all": sum(1 for row in rows if row["pass_all"]),
        "source_hit_at_k": sum(1 for row in rows if row["pass_source"]),
        "keyword_hit_at_k": sum(1 for row in rows if row["pass_keyword"]),
        "source_hit_at_1": sum(1 for row in rows if row["source_first_rank"] == 1),
        "keyword_hit_at_1": sum(1 for row in rows if row["keyword_first_rank"] == 1),
        "misses": [row["id"] for row in rows if not row["pass_all"]],
        "avg_total_seconds": statistics.mean(totals) if totals else 0,
        "median_total_seconds": statistics.median(totals) if totals else 0,
        "model": {
            "provider": "local_transformers",
            "model": str(args.model),
            "device": model_metadata.get("device", ""),
            "max_length": args.max_length,
            "dimensions": model_metadata.get("dimensions", 0),
        },
    }
    return {"summary": summary, "rows": rows}


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Text RAG Retrieval Evaluation",
        "",
        "## Summary",
        "",
        f"- Collection: `{summary['collection']}` ({summary['collection_count']} docs)",
        f"- Model: `{summary['model']['model']}` on `{summary['model']['device']}`, dim={summary['model']['dimensions']}",
        f"- Tests: {summary['tests']}, TopK: {summary['top_k']}",
        f"- Rerank: `{summary['rerank']}`, candidates: {summary['rerank_candidates']}",
        f"- Pass all: {summary['pass_all']}/{summary['tests']}",
        f"- Source Hit@1: {summary['source_hit_at_1']}/{summary['tests']}",
        f"- Source Hit@K: {summary['source_hit_at_k']}/{summary['tests']}",
        f"- Keyword Hit@1: {summary['keyword_hit_at_1']}/{summary['tests']}",
        f"- Keyword Hit@K: {summary['keyword_hit_at_k']}/{summary['tests']}",
        f"- Avg latency/query: {summary['avg_total_seconds']:.3f}s",
        f"- Median latency/query: {summary['median_total_seconds']:.3f}s",
        "",
    ]
    if summary["misses"]:
        lines += ["## Misses", "", ", ".join(f"`{item}`" for item in summary["misses"]), ""]

    lines += ["## Cases", ""]
    for row in report["rows"]:
        status = "PASS" if row["pass_all"] else "MISS"
        lines += [
            f"### {row['id']} - {status}",
            "",
            f"- Query: {row['query']}",
            f"- Expected sources: {', '.join(row['text_sources'])}",
            f"- Expected keywords any: {', '.join(row['expected_keywords_any'])}",
            f"- Rerank: `{row['rerank']}`, candidates: {row['rerank_candidates']}",
            f"- Source first rank: {row['source_first_rank']}",
            f"- Keyword first rank: {row['keyword_first_rank']}",
            f"- Latency: total {row['total_seconds']:.3f}s = embed {row['embed_seconds']:.3f}s + chroma {row['query_seconds']:.3f}s",
            "",
            "| Rank | Orig | SrcOK | KeyOK | Distance | Rerank | Source | Chunk | Matched | Preview |",
            "|---:|---:|:---:|:---:|---:|---:|---|---|---|---|",
        ]
        for hit in row["results"]:
            metadata = hit["metadata"]
            details = hit.get("rerank_details") or {}
            lines.append(
                "| {rank} | {orig} | {src} | {key} | {distance:.4f} | {rerank:.4f} | `{source}` | `{chunk}` | {matched} | {preview} |".format(
                    rank=hit["rank"],
                    orig=hit.get("original_rank", hit["rank"]),
                    src="Y" if hit["source_expected"] else "",
                    key="Y" if hit["keyword_expected"] else "",
                    distance=float(hit["distance"]),
                    rerank=float(hit.get("rerank_score", -float(hit["distance"]))),
                    source=metadata.get("source_id", ""),
                    chunk=metadata.get("chunk_id", ""),
                    matched=", ".join(details.get("matched_tokens") or [])[:120],
                    preview=render_preview(hit["document"]),
                )
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tests", type=Path, default=DEFAULT_TESTS)
    parser.add_argument("--chroma-path", type=Path, default=DEFAULT_CHROMA_PATH)
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--model", default=DEFAULT_LOCAL_MODEL)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--max-length", type=int, default=2048)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--rerank-candidates", type=int, default=25)
    parser.add_argument("--no-rerank", dest="rerank", action="store_false")
    parser.set_defaults(rerank=True)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--report-md", type=Path, default=DEFAULT_REPORT_MD)
    parser.add_argument("--report-json", type=Path, default=DEFAULT_REPORT_JSON)
    args = parser.parse_args()

    report = evaluate(args)
    args.report_json.parent.mkdir(parents=True, exist_ok=True)
    args.report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    args.report_md.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
