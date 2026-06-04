#!/usr/bin/env python
"""Check whether a curated KG JSONL would duplicate Neo4j relationships."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


RELATION_RE = re.compile(r"^[a-z_]+$")


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
                raise ValueError(f"Invalid JSON on line {line_no}: {exc}") from exc
            if isinstance(row, dict):
                rows.append(row)
    return rows


def rel_type(relation: str) -> str:
    relation = relation.strip()
    if not RELATION_RE.match(relation):
        raise ValueError(f"Unsafe relation name: {relation}")
    return relation.upper()


def review_id(edge: dict[str, Any]) -> str:
    provenance = edge.get("provenance", {})
    if not isinstance(provenance, dict):
        provenance = {}
    return str(provenance.get("review_id") or "")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Curated edges.jsonl")
    parser.add_argument("--env-file", type=Path, default=Path(".env"), help="Path to .env")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    apply_env_file(args.env_file)
    edges = read_jsonl(args.input)

    try:
        from neo4j import GraphDatabase
    except ImportError as exc:
        raise RuntimeError("Missing dependency: pip install neo4j") from exc

    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    user = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "")
    database = os.environ.get("NEO4J_DATABASE", "neo4j")
    if not password:
        raise ValueError("NEO4J_PASSWORD is empty")

    duplicate_review_ids: list[str] = []
    duplicate_context_keys: list[dict[str, str]] = []

    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            for edge in edges:
                rid = review_id(edge)
                if rid:
                    exists = session.run(
                        """
                        MATCH ()-[r]->()
                        WHERE r.review_id = $review_id
                        RETURN count(r) AS count
                        """,
                        review_id=rid,
                    ).single()["count"]
                    if exists:
                        duplicate_review_ids.append(rid)

                source = str(edge.get("source", "")).strip()
                target = str(edge.get("target", "")).strip()
                relation = rel_type(str(edge.get("relation", "")))
                context = str(edge.get("context_condition", "")).strip()
                query = f"""
                MATCH (a:KGNode {{id: $source}})-[r:{relation}]->(b:KGNode {{id: $target}})
                WHERE coalesce(r.context_condition, '') = $context
                RETURN count(r) AS count
                """
                exists = session.run(query, source=source, target=target, context=context).single()["count"]
                if exists:
                    duplicate_context_keys.append(
                        {
                            "source": source,
                            "relation": relation,
                            "target": target,
                            "context_condition": context,
                        }
                    )

    print(
        json.dumps(
            {
                "input": str(args.input),
                "edges": len(edges),
                "duplicate_review_id": len(duplicate_review_ids),
                "duplicate_same_context": len(duplicate_context_keys),
                "duplicate_review_id_samples": duplicate_review_ids[:10],
                "duplicate_same_context_samples": duplicate_context_keys[:5],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
