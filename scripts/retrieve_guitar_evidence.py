#!/usr/bin/env python
"""Retrieve guitar textbook evidence with style/task filters over Chroma and Neo4j."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_CHROMA_PATH = Path("data/chroma")
DEFAULT_TEXT_COLLECTION = "guitar_text_chunks"
DEFAULT_EVAL_PATH = Path("data/eval/retrieval_smoke_tests.json")


STYLE_KEYWORDS: dict[str, list[str]] = {
    "funk": [
        "funk",
        "cory",
        "wong",
        "bubble",
        "chuck",
        "chucks",
        "muted",
        "palm mute",
        "sixteenth",
        "16th",
        "nile",
        "ghost",
        "rhythm guitar",
        "groove",
        "闷音",
        "律动",
        "切分",
        "十六分",
        "16分",
        "放克",
    ],
    "rhythm_guitar": ["rhythm guitar", "comping", "groove", "伴奏", "节奏吉他", "律动"],
    "math_rock": [
        "math rock",
        "mathrock",
        "数摇",
        "dadgad",
        "alternate tuning",
        "open string",
        "open strings",
        "tapping",
        "power chord",
        "odd meter",
        "开放弦",
        "特殊调弦",
        "点弦",
        "奇数",
    ],
    "midwest_emo": ["midwest", "emo", "midwest emo", "open string", "开放弦", "清亮"],
    "fretboard": ["fretboard", "position", "string set", "interval", "指板", "把位", "弦组", "音程"],
    "guitar_foundation": ["指板", "把位", "音程", "fretboard", "foundation"],
}


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


def parse_jsonish_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    text = str(value).strip()
    if not text:
        return []
    try:
        loaded = json.loads(text)
    except json.JSONDecodeError:
        return [part.strip() for part in re.split(r"[,;]", text) if part.strip()]
    if isinstance(loaded, list):
        return [str(item) for item in loaded]
    return [str(loaded)]


def infer_style_tags(query: str, explicit_tags: list[str]) -> list[str]:
    tags = set(explicit_tags)
    lower = query.lower()
    for tag, keywords in STYLE_KEYWORDS.items():
        if any(keyword.lower() in lower for keyword in keywords):
            tags.add(tag)
    return sorted(tags)


class APIEmbedder:
    def __init__(self) -> None:
        self.base_url = (
            os.environ.get("EMBEDDING_API_BASE_URL")
            or os.environ.get("LLM_API_BASE_URL", "")
        ).rstrip("/")
        self.api_key = os.environ.get("EMBEDDING_API_KEY") or os.environ.get("LLM_API_KEY", "")
        self.model = os.environ.get("EMBEDDING_MODEL", "")
        self.dimensions = int(os.environ.get("EMBEDDING_DIMENSIONS", "0") or 0)
        self.timeout = int(os.environ.get("EMBEDDING_TIMEOUT_SECONDS", "120"))
        self.max_retries = int(os.environ.get("EMBEDDING_MAX_RETRIES", "2"))
        if not self.base_url or not self.model:
            raise ValueError("Set EMBEDDING_API_BASE_URL and EMBEDDING_MODEL in .env")

    def embed(self, text: str) -> list[float]:
        payload: dict[str, Any] = {"model": self.model, "input": [text]}
        if self.dimensions > 0:
            payload["dimensions"] = self.dimensions
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers = {"Content-Type": "application/json; charset=utf-8"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                req = urllib.request.Request(
                    f"{self.base_url}/embeddings",
                    data=body,
                    headers=headers,
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                return data["data"][0]["embedding"]
            except (urllib.error.URLError, urllib.error.HTTPError, KeyError, json.JSONDecodeError) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(1.5 * (attempt + 1))
        raise RuntimeError(f"Embedding request failed: {last_error}")


@dataclass
class EvidenceResult:
    doc_id: str
    distance: float
    metadata: dict[str, Any]
    document: str
    filter_score: int


def metadata_matches(
    metadata: dict[str, Any],
    *,
    style_tags: list[str],
    source_ids: list[str],
    kg_nodes: list[str],
    gp5_features: list[str],
) -> tuple[bool, int]:
    score = 0
    if source_ids:
        if metadata.get("source_id") not in source_ids:
            return False, 0
        score += 3

    meta_styles = set(parse_jsonish_list(metadata.get("style_tags")))
    if style_tags:
        if not meta_styles.intersection(style_tags):
            return False, 0
        score += len(meta_styles.intersection(style_tags)) * 2

    meta_nodes = set(parse_jsonish_list(metadata.get("linked_kg_nodes")))
    if kg_nodes:
        if not meta_nodes.intersection(kg_nodes):
            return False, 0
        score += len(meta_nodes.intersection(kg_nodes)) * 2

    meta_features = " ".join(parse_jsonish_list(metadata.get("gp5_feature_triggers"))).lower()
    if gp5_features:
        matched = [feature for feature in gp5_features if feature.lower() in meta_features]
        if not matched:
            return False, 0
        score += len(matched) * 2
    return True, score


def query_chroma(args: argparse.Namespace, style_tags: list[str]) -> list[EvidenceResult]:
    try:
        import chromadb
    except ImportError as exc:
        raise RuntimeError("Missing dependency: install chromadb first") from exc

    client = chromadb.PersistentClient(path=str(args.chroma_path))
    collection = client.get_collection(name=args.collection)
    embedder = APIEmbedder()
    result = collection.query(
        query_embeddings=[embedder.embed(args.query)],
        n_results=args.preselect,
        include=["documents", "metadatas", "distances"],
    )

    results: list[EvidenceResult] = []
    for idx, doc_id in enumerate(result.get("ids", [[]])[0]):
        metadata = result["metadatas"][0][idx]
        passed, score = metadata_matches(
            metadata,
            style_tags=style_tags if not args.no_auto_filter else args.style_tag,
            source_ids=args.source_id,
            kg_nodes=args.kg_node,
            gp5_features=args.gp5_feature,
        )
        if not passed:
            continue
        results.append(
            EvidenceResult(
                doc_id=doc_id,
                distance=float(result["distances"][0][idx]),
                metadata=metadata,
                document=result["documents"][0][idx],
                filter_score=score,
            )
        )
    results.sort(key=lambda item: (-item.filter_score, item.distance))
    return results[: args.top_k]


def fetch_neo4j_edges(style_tags: list[str], limit: int, env_file: Path) -> list[dict[str, Any]]:
    if not style_tags:
        return []
    apply_env_file(env_file)
    try:
        from neo4j import GraphDatabase
    except ImportError:
        return []

    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    user = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "")
    database = os.environ.get("NEO4J_DATABASE", "neo4j")
    if not password:
        return []

    style_ids = [f"style:{tag}" for tag in style_tags]
    rows: list[dict[str, Any]] = []
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver:
        with driver.session(database=database) as session:
            rows = session.run(
                """
                MATCH (a:KGNode)-[r]-(b:KGNode)
                WHERE a.id IN $style_ids OR b.id IN $style_ids
                RETURN a.id AS source, type(r) AS relation, b.id AS target,
                       r.review_note AS review_note, r.context_condition AS context_condition,
                       r.confidence AS confidence
                ORDER BY coalesce(r.confidence, 0) DESC
                LIMIT $limit
                """,
                style_ids=style_ids,
                limit=limit,
            ).data()
    return rows


def render_results(query: str, style_tags: list[str], neo4j_edges: list[dict[str, Any]], results: list[EvidenceResult]) -> None:
    print(json.dumps({"query": query, "inferred_style_tags": style_tags}, ensure_ascii=False, indent=2))
    if neo4j_edges:
        print("\n# Neo4j related edges")
        for edge in neo4j_edges[:8]:
            print(f"- {edge['source']} -[{edge['relation']}]-> {edge['target']}")

    print("\n# Chroma evidence")
    for index, item in enumerate(results, start=1):
        metadata = item.metadata
        snippet = item.document[:650].replace("\n", " ")
        if len(item.document) > 650:
            snippet += "..."
        print(f"\n## {index}. {item.doc_id} distance={item.distance:.4f} filter_score={item.filter_score}")
        print(f"- source: {metadata.get('source_title')} / {metadata.get('chunk_id')}")
        print(f"- source_id: {metadata.get('source_id')}")
        print(f"- style_tags: {metadata.get('style_tags')}")
        print(f"- review_ids: {metadata.get('linked_review_ids')}")
        print(snippet)


def run_eval(args: argparse.Namespace) -> int:
    tests = json.loads(args.eval_path.read_text(encoding="utf-8"))
    report: list[dict[str, Any]] = []
    passed = 0
    for test in tests:
        args.query = test["query"]
        style_tags = infer_style_tags(args.query, args.style_tag)
        for tag in test.get("expected_style_tags", []):
            if tag not in style_tags:
                style_tags.append(tag)
        results = query_chroma(args, sorted(style_tags))
        top_sources = [item.metadata.get("source_id") for item in results]
        expected = test.get("expected_source_id")
        top1_ok = bool(top_sources and top_sources[0] == expected)
        topk_clean = bool(top_sources and all(source == expected for source in top_sources))
        passed += 1 if top1_ok else 0
        report.append(
            {
                "name": test.get("name"),
                "query": args.query,
                "inferred_style_tags": sorted(style_tags),
                "expected_source_id": expected,
                "top_sources": top_sources,
                "top1_ok": top1_ok,
                "topk_clean": topk_clean,
            }
        )
    print(json.dumps({"passed_top1": passed, "total": len(tests), "tests": report}, ensure_ascii=False, indent=2))
    return 0 if passed == len(tests) else 1


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    parser.add_argument("--chroma-path", type=Path, default=DEFAULT_CHROMA_PATH)
    parser.add_argument("--collection", default=DEFAULT_TEXT_COLLECTION)
    parser.add_argument("--query", default="")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--preselect", type=int, default=25)
    parser.add_argument("--style-tag", action="append", default=[])
    parser.add_argument("--source-id", action="append", default=[])
    parser.add_argument("--kg-node", action="append", default=[])
    parser.add_argument("--gp5-feature", action="append", default=[])
    parser.add_argument("--no-auto-filter", action="store_true")
    parser.add_argument("--neo4j-limit", type=int, default=12)
    parser.add_argument("--eval", action="store_true", help="Run smoke retrieval tests")
    parser.add_argument("--eval-path", type=Path, default=DEFAULT_EVAL_PATH)
    args = parser.parse_args(argv)
    apply_env_file(args.env_file)
    args.chroma_path = Path(os.environ.get("CHROMA_PATH", str(args.chroma_path)))
    args.collection = os.environ.get("CHROMA_TEXT_COLLECTION", args.collection)
    return args


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.eval:
        return run_eval(args)
    if not args.query:
        raise ValueError("Provide --query or --eval")
    style_tags = infer_style_tags(args.query, args.style_tag)
    results = query_chroma(args, style_tags)
    neo4j_edges = fetch_neo4j_edges(style_tags, args.neo4j_limit, args.env_file)
    render_results(args.query, style_tags, neo4j_edges, results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
