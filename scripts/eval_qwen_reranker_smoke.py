#!/usr/bin/env python
"""Small A/B smoke test for Qwen3 reranker in the RAG bundle pipeline."""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from query_rag_bundle import DEFAULT_CHROMA_PATH, DEFAULT_LOCAL_MODEL, run_bundle


QUERIES = [
    {
        "id": "gminor_visual",
        "query": "给出G小调的吉他指型参考",
        "context": ROOT / "data" / "eval" / "canonical_visual_gminor_context.json",
    },
    {
        "id": "funk_groove",
        "query": "funk 十六分闷音 groove 伴奏怎么编",
        "context": None,
    },
    {
        "id": "mathrock_fmaj7",
        "query": "Fmaj7 做 mathrock riff 怎么结合开放弦和高把位指型",
        "context": None,
    },
]


def load_context(path: Path | None) -> str:
    if path and path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def make_args(query: str, context_json: str, top_k: int, kg_limit: int) -> argparse.Namespace:
    return argparse.Namespace(
        query=query,
        context_json=context_json,
        top_k=top_k,
        kg_limit=kg_limit,
        chroma_path=DEFAULT_CHROMA_PATH,
        model=os.environ.get("LOCAL_EMBEDDING_MODEL", DEFAULT_LOCAL_MODEL),
        device=os.environ.get("LOCAL_EMBEDDING_DEVICE", "auto"),
        max_length=int(os.environ.get("LOCAL_EMBEDDING_MAX_LENGTH", "2048")),
        batch_size=8,
        env_file=ROOT / ".env",
        report_md=ROOT / "data" / "eval" / "_unused.md",
        report_json=ROOT / "data" / "eval" / "_unused.json",
    )


def summarize_items(items: list[Any], limit: int = 5) -> list[dict[str, Any]]:
    rows = []
    for item in items[:limit]:
        model_rerank = item.metadata.get("model_rerank", {}) if isinstance(item.metadata, dict) else {}
        rows.append(
            {
                "evidence_id": item.evidence_id,
                "source_id": item.source_id,
                "score": item.score,
                "rerank_delta": model_rerank.get("delta"),
                "rerank_raw": model_rerank.get("raw_score"),
                "title": item.title,
            }
        )
    return rows


def run_case(query: str, context_json: str, backend: str, top_k: int, kg_limit: int) -> dict[str, Any]:
    os.environ["RERANK_BACKEND"] = backend
    if backend == "local":
        os.environ.setdefault("RERANK_MODEL", "models/reranker/qwen3-reranker-0.6b")
        os.environ.setdefault("RERANK_DEVICE", "auto")
        os.environ.setdefault("RERANK_BATCH_SIZE", "4")
        os.environ.setdefault("RERANK_MAX_LENGTH", "1024")
        os.environ.setdefault("RERANK_WEIGHT", "0.35")
    args = make_args(query, context_json, top_k, kg_limit)
    bundle = run_bundle(args)
    return {
        "backend": backend,
        "intent": bundle.analysis.intent,
        "judgement": bundle.judgement,
        "timings": bundle.timings,
        "answer_seed": bundle.answer_seed,
        "top_text": summarize_items(bundle.text_evidence),
        "top_visual": summarize_items(bundle.visual_evidence),
        "top_kg": summarize_items(bundle.kg_evidence),
    }


def render_markdown(results: list[dict[str, Any]]) -> str:
    lines = [
        "# Qwen Reranker Smoke A/B Report",
        "",
        "对同一批 query 分别运行 `RERANK_BACKEND=none` 与 `RERANK_BACKEND=local`。",
        "",
    ]
    for result in results:
        lines.extend(
            [
                f"## {result['id']}",
                "",
                f"- Query: {result['query']}",
                "",
                "| Backend | Intent | Sufficient | Confidence | Total | Model Rerank | Top Visual | Top Text |",
                "|---|---|---:|---:|---:|---:|---|---|",
            ]
        )
        for run in result["runs"]:
            judgement = run["judgement"]
            timings = run["timings"]
            top_visual = run["top_visual"][0]["evidence_id"] if run["top_visual"] else "-"
            top_text = run["top_text"][0]["evidence_id"] if run["top_text"] else "-"
            lines.append(
                "| {backend} | `{intent}` | {sufficient} | {confidence} | {total:.3f}s | {rerank:.3f}s | `{top_visual}` | `{top_text}` |".format(
                    backend=run["backend"],
                    intent=run["intent"],
                    sufficient=judgement.get("sufficient"),
                    confidence=judgement.get("confidence", 0),
                    total=float(timings.get("total_seconds", 0) or 0),
                    rerank=float(timings.get("model_rerank_seconds", 0) or 0),
                    top_visual=top_visual,
                    top_text=top_text,
                )
            )
        lines.extend(["", "### Local rerank top evidence", ""])
        local_run = next((run for run in result["runs"] if run["backend"] == "local"), None)
        if local_run:
            for label, key in [("Text", "top_text"), ("Visual", "top_visual"), ("KG", "top_kg")]:
                lines.extend([f"#### {label}", "", "| Rank | Evidence | Score | Delta | Raw | Title |", "|---:|---|---:|---:|---:|---|"])
                for rank, item in enumerate(local_run[key], start=1):
                    lines.append(
                        f"| {rank} | `{item['evidence_id']}` | {float(item['score']):.4f} | "
                        f"{float(item['rerank_delta'] or 0):.4f} | {float(item['rerank_raw'] or 0):.4f} | {item['title']} |"
                    )
                lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--kg-limit", type=int, default=8)
    parser.add_argument("--report-md", type=Path, default=ROOT / "data" / "eval" / "qwen_reranker_smoke_ab_report.md")
    parser.add_argument("--report-json", type=Path, default=ROOT / "data" / "eval" / "qwen_reranker_smoke_ab_report.json")
    args = parser.parse_args()

    results = []
    for case in QUERIES:
        context_json = load_context(case["context"])
        runs = [
            run_case(case["query"], context_json, "none", args.top_k, args.kg_limit),
            run_case(case["query"], context_json, "local", args.top_k, args.kg_limit),
        ]
        results.append({"id": case["id"], "query": case["query"], "runs": runs})

    payload = {"results": results}
    args.report_json.parent.mkdir(parents=True, exist_ok=True)
    args.report_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    args.report_md.write_text(render_markdown(results), encoding="utf-8")
    print(json.dumps({"report_md": str(args.report_md), "report_json": str(args.report_json)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
