"""Evaluate text retrieval over VLM-generated visual captions."""

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
DEFAULT_COLLECTION = "guitar_visual_captions_qwen3_06b"
DEFAULT_TESTS = ROOT / "data" / "eval" / "visual_caption_trial_tests.json"
DEFAULT_REPORT_MD = ROOT / "data" / "eval" / "visual_caption_trial_report.md"
DEFAULT_REPORT_JSON = ROOT / "data" / "eval" / "visual_caption_trial_report.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def hit_result(item: dict[str, Any], test: dict[str, Any]) -> bool:
    haystack = "\n".join(
        [
            as_text(item.get("id")),
            as_text(item.get("document")),
            as_text(item.get("metadata")),
        ]
    ).lower()
    expected_any = test.get("expected_any", [])
    if expected_any and not any(str(token).lower() in haystack for token in expected_any):
        return False
    metadata = item.get("metadata") or {}
    expected_source_ids = {str(value) for value in test.get("expected_source_ids", [])}
    if expected_source_ids and str(metadata.get("source_id") or "") not in expected_source_ids:
        return False
    forbidden_layers = {str(value) for value in test.get("forbidden_caption_layers", [])}
    if forbidden_layers and str(metadata.get("caption_layer") or "") in forbidden_layers:
        return False
    return bool(expected_any or expected_source_ids)


def compact_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "visual_id",
        "source_title",
        "source_id",
        "page",
        "image_type",
        "topic",
        "tuning",
        "key",
        "root",
        "caption",
        "arrangement_value",
        "confidence",
        "visual_granularity",
        "topic_hint",
        "nearby_text",
        "image_path",
        "crop_path",
        "exercise_number",
        "subquestion_number",
        "visual_type",
        "musical_object",
        "position_or_shape",
        "quality_or_mode",
        "caption_layer",
    ]
    return {key: metadata.get(key) for key in keys if metadata.get(key) not in (None, "")}


CHORD_TOKEN_RE = re.compile(r"\b[a-g](?:#|b)?(?:maj|min|m|dim|aug|sus|add)?(?:\d+)?(?:[#b]?\d+)?\b", re.I)
WORD_TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9#/+.-]{1,}|[0-9]+(?:th)?|[\u4e00-\u9fff]{2,}")
CHINESE_NUMERALS = {
    "一": "1",
    "二": "2",
    "三": "3",
    "四": "4",
    "五": "5",
    "六": "6",
    "七": "7",
    "八": "8",
    "九": "9",
    "十": "10",
}
CHINESE_KEYWORDS = [
    "音阶",
    "和弦",
    "琶音",
    "点弦",
    "开放弦",
    "调弦",
    "指型",
    "指法",
    "大调",
    "小调",
    "声部",
    "谱例",
]


def query_tokens(query: str) -> set[str]:
    lowered = query.lower()
    tokens = {token.lower() for token in WORD_TOKEN_RE.findall(lowered)}
    tokens.update(token.lower() for token in CHORD_TOKEN_RE.findall(lowered))
    tokens.update(keyword for keyword in CHINESE_KEYWORDS if keyword in query)
    for zh, value in CHINESE_NUMERALS.items():
        if f"第{zh}品" in query:
            tokens.update({value, f"{value}品", f"第{value}品", f"{value}th", f"{value}th_fret"})
    return {token for token in tokens if len(token) >= 2 or token.isdigit()}


def text_blob(item: dict[str, Any]) -> str:
    metadata = item.get("metadata") or {}
    return "\n".join(
        [
            str(item.get("id") or ""),
            str(item.get("document") or ""),
            json.dumps(metadata, ensure_ascii=False),
        ]
    ).lower()


def is_specific_visual_query(query: str, tokens: set[str]) -> bool:
    markers = ["品", "fret", "指型", "shape", "图块", "局部", "指法", "voicing"]
    chord_like = len(CHORD_TOKEN_RE.findall(query.lower())) >= 2
    return chord_like or any(marker.lower() in query.lower() for marker in markers) or any(token.endswith("th_fret") for token in tokens)


def lexical_rerank_score(item: dict[str, Any], query: str, tokens: set[str]) -> tuple[float, dict[str, Any]]:
    metadata = item.get("metadata") or {}
    blob = text_blob(item)
    matched = sorted(token for token in tokens if token and token in blob)
    match_score = len(matched) * 0.012

    topic = str(metadata.get("topic") or "").lower()
    caption = str(metadata.get("caption") or "").lower()
    image_type = str(metadata.get("image_type") or "").lower()
    granularity = str(metadata.get("visual_granularity") or "").lower()
    tuning = str(metadata.get("tuning") or "").lower()
    caption_layer = str(metadata.get("caption_layer") or "").lower()

    detail_bonus = 0.0
    if is_specific_visual_query(query, tokens):
        if granularity == "image_block":
            detail_bonus += 0.018
        if granularity == "full_page":
            detail_bonus -= 0.018
        if "fret" in topic or "品" in caption:
            detail_bonus += 0.010

    for token in tokens:
        if token in topic:
            detail_bonus += 0.006
        if token in caption:
            detail_bonus += 0.003

    scale_intent = "音阶" in query or "scale" in query.lower()
    chord_intent = "和弦" in query or "chord" in query.lower() or bool(CHORD_TOKEN_RE.findall(query.lower()))
    arpeggio_intent = "琶音" in query or "arpeggio" in query.lower()
    if scale_intent:
        if "scale" in blob or "音阶" in blob:
            detail_bonus += 0.030
        if "chord_shape" in topic or image_type == "chord_diagram":
            detail_bonus -= 0.028
    if chord_intent:
        if "chord" in blob or "和弦" in blob:
            detail_bonus += 0.018
    if arpeggio_intent:
        if "arpeggio" in blob or "琶音" in blob:
            detail_bonus += 0.024
        if "chord_shape" in topic:
            detail_bonus -= 0.010

    lowered_query = query.lower()
    mathrock_intent = "math rock" in lowered_query or "mathrock" in lowered_query or "数摇" in query or "数学摇滚" in query
    foundation_intent = any(marker in query for marker in ["普通", "基础", "常规"]) or any(
        marker in lowered_query for marker in ["basic", "plain", "generic"]
    )
    if mathrock_intent and caption_layer == "mathrock_style_visual_caption_v1":
        detail_bonus += 0.050
    if foundation_intent and not mathrock_intent and caption_layer == "mathrock_style_visual_caption_v1":
        detail_bonus -= 0.100

    standard_tuning_intent = "标准调弦" in query or "standard tuning" in lowered_query
    if standard_tuning_intent:
        if tuning == "standard":
            detail_bonus += 0.035
        elif tuning and tuning != "unknown":
            detail_bonus -= 0.120

    negative_techniques = {
        "tapping": ["不需要点弦", "不要点弦", "非点弦", "without tapping", "no tapping"],
        "arpeggio": ["不需要琶音", "不要琶音", "非琶音", "without arpeggio", "no arpeggio"],
        "open_string": ["不需要开放弦", "不要开放弦", "非开放弦", "without open strings", "no open strings"],
    }
    for technique, markers in negative_techniques.items():
        if any(marker in lowered_query for marker in markers) and technique in blob:
            detail_bonus -= 0.140

    vector_score = -float(item.get("distance") or 0.0)
    final_score = vector_score + match_score + detail_bonus
    details = {
        "vector_score": vector_score,
        "match_score": match_score,
        "detail_bonus": detail_bonus,
        "matched_tokens": matched[:12],
        "final_score": final_score,
    }
    return final_score, details


def rerank_hits(hits: list[dict[str, Any]], query: str) -> list[dict[str, Any]]:
    tokens = query_tokens(query)
    ranked = []
    for original_rank, item in enumerate(hits, start=1):
        score, details = lexical_rerank_score(item, query, tokens)
        row = dict(item)
        row["original_rank"] = original_rank
        row["rerank_score"] = score
        row["rerank_details"] = details
        ranked.append(row)
    ranked.sort(key=lambda item: (-float(item["rerank_score"]), int(item["original_rank"])))
    for rank, item in enumerate(ranked, start=1):
        item["rank"] = rank
    return ranked


def run_eval(args: argparse.Namespace) -> dict[str, Any]:
    import chromadb

    tests = load_json(args.tests)
    embedder = LocalTransformerEmbedder(args.model, device=args.device, max_length=args.max_length)
    client = chromadb.PersistentClient(path=str(args.chroma_path))
    collection = client.get_collection(args.collection)

    rows = []
    for test in tests:
        started = time.perf_counter()
        embedding = embedder.embed([test["query"]], batch_size=1)[0]
        embed_seconds = time.perf_counter() - started

        query_started = time.perf_counter()
        candidate_count = max(args.top_k, args.rerank_candidates if args.rerank else args.top_k)
        result = collection.query(query_embeddings=[embedding], n_results=candidate_count)
        query_seconds = time.perf_counter() - query_started

        ids = result.get("ids", [[]])[0]
        docs = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]
        hits = []
        for rank, (item_id, doc, metadata, distance) in enumerate(zip(ids, docs, metadatas, distances), start=1):
            row = {
                "rank": rank,
                "id": item_id,
                "distance": distance,
                "metadata": compact_metadata(metadata or {}),
                "document": doc,
            }
            row["is_expected"] = hit_result(row, test)
            hits.append(row)

        if args.rerank:
            hits = rerank_hits(hits, test["query"])
        hits = hits[: args.top_k]

        first_hit_rank = next((hit["rank"] for hit in hits if hit["is_expected"]), None)
        rows.append(
            {
                "id": test["id"],
                "group": test.get("group", "default"),
                "query": test["query"],
                "expected_any": test.get("expected_any", []),
                "expected_source_ids": test.get("expected_source_ids", []),
                "forbidden_caption_layers": test.get("forbidden_caption_layers", []),
                "top_k": args.top_k,
                "rerank": args.rerank,
                "rerank_candidates": candidate_count,
                "first_hit_rank": first_hit_rank,
                "hit_at_1": first_hit_rank == 1,
                "hit_at_k": first_hit_rank is not None,
                "embed_seconds": embed_seconds,
                "query_seconds": query_seconds,
                "total_seconds": embed_seconds + query_seconds,
                "results": hits,
            }
        )

    totals = [row["total_seconds"] for row in rows]
    model_metadata = embedder.metadata()
    group_names = sorted({str(row.get("group") or "default") for row in rows})
    groups = {}
    for group in group_names:
        group_rows = [row for row in rows if row.get("group") == group]
        groups[group] = {
            "tests": len(group_rows),
            "hit_at_1": sum(1 for row in group_rows if row["hit_at_1"]),
            "hit_at_k": sum(1 for row in group_rows if row["hit_at_k"]),
            "misses": [row["id"] for row in group_rows if not row["hit_at_k"]],
        }
    summary = {
        "tests": len(rows),
        "collection": args.collection,
        "collection_count": collection.count(),
        "top_k": args.top_k,
        "rerank": args.rerank,
        "rerank_candidates": args.rerank_candidates if args.rerank else args.top_k,
        "hit_at_1": sum(1 for row in rows if row["hit_at_1"]),
        "hit_at_k": sum(1 for row in rows if row["hit_at_k"]),
        "misses": [row["id"] for row in rows if not row["hit_at_k"]],
        "groups": groups,
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


def clip(text: str, limit: int = 180) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + "..."


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    rows = report["rows"]
    lines = [
        "# Visual Caption Retrieval Trial",
        "",
        "## Summary",
        "",
        f"- Collection: `{summary['collection']}` ({summary['collection_count']} docs)",
        f"- Model: `{summary['model']['model']}` on `{summary['model']['device']}`, dim={summary['model']['dimensions']}",
        f"- Tests: {summary['tests']}, TopK: {summary['top_k']}",
        f"- Rerank: `{summary['rerank']}`, candidates: {summary['rerank_candidates']}",
        f"- Hit@1: {summary['hit_at_1']}/{summary['tests']}",
        f"- Hit@K: {summary['hit_at_k']}/{summary['tests']}",
        f"- Avg total latency/query: {summary['avg_total_seconds']:.3f}s",
        f"- Median total latency/query: {summary['median_total_seconds']:.3f}s",
        "",
    ]
    if summary["misses"]:
        lines += ["## Misses", "", ", ".join(f"`{item}`" for item in summary["misses"]), ""]

    lines += ["## Cases", ""]
    for row in rows:
        status = "PASS" if row["hit_at_k"] else "MISS"
        lines += [
            f"### {row['id']} - {status}",
            "",
            f"- Query: {row['query']}",
            f"- Expected any: {', '.join(row['expected_any'])}",
            f"- First hit rank: {row['first_hit_rank']}",
            f"- Rerank: `{row['rerank']}`, candidates: {row['rerank_candidates']}",
            f"- Latency: total {row['total_seconds']:.3f}s = embed {row['embed_seconds']:.3f}s + chroma {row['query_seconds']:.3f}s",
            "",
            "| Rank | Orig | Expected | Distance | Rerank | Topic | Page | Type | Matched | Caption |",
            "|---:|---:|:---:|---:|---:|---|---:|---|---|---|",
        ]
        for hit in row["results"]:
            metadata = hit["metadata"]
            details = hit.get("rerank_details") or {}
            lines.append(
                "| {rank} | {original_rank} | {expected} | {distance:.4f} | {rerank:.4f} | `{topic}` | {page} | {image_type} | {matched} | {caption} |".format(
                    rank=hit["rank"],
                    original_rank=hit.get("original_rank", hit["rank"]),
                    expected="Y" if hit["is_expected"] else "",
                    distance=float(hit["distance"]),
                    rerank=float(hit.get("rerank_score", -float(hit["distance"]))),
                    topic=metadata.get("topic", ""),
                    page=metadata.get("page", ""),
                    image_type=metadata.get("image_type", ""),
                    matched=", ".join(details.get("matched_tokens") or [])[:120],
                    caption=clip(metadata.get("caption", "")).replace("|", "\\|"),
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
    parser.add_argument("--rerank-candidates", type=int, default=20)
    parser.add_argument("--no-rerank", dest="rerank", action="store_false", help="Disable lexical/granularity reranking.")
    parser.set_defaults(rerank=True)
    parser.add_argument("--report-md", type=Path, default=DEFAULT_REPORT_MD)
    parser.add_argument("--report-json", type=Path, default=DEFAULT_REPORT_JSON)
    args = parser.parse_args()

    report = run_eval(args)
    args.report_json.parent.mkdir(parents=True, exist_ok=True)
    args.report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    args.report_md.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
