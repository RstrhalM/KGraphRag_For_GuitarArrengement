#!/usr/bin/env python
"""Import curated KG JSONL into Neo4j over Bolt."""

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


def node_type(node_id: str) -> str:
    return node_id.split(":", 1)[0] if ":" in node_id else "concept"


def node_name(node_id: str) -> str:
    return node_id.split(":", 1)[1] if ":" in node_id else node_id


def relation_type(relation: str) -> str:
    relation = relation.strip()
    if not RELATION_RE.match(relation):
        raise ValueError(f"Unsafe relation name: {relation}")
    return relation.upper()


def relationship_properties(edge: dict[str, Any]) -> dict[str, Any]:
    provenance = edge.get("provenance", {})
    if not isinstance(provenance, dict):
        provenance = {}
    return {
        "knowledge_type": edge.get("knowledge_type"),
        "confidence": float(edge.get("confidence", 0.5) or 0.5),
        "context_condition": edge.get("context_condition"),
        "review_note": edge.get("review_note"),
        "evidence": edge.get("evidence"),
        "needs_visual_context": bool(edge.get("needs_visual_context", False)),
        "review_id": provenance.get("review_id"),
        "chunk_id": provenance.get("chunk_id"),
        "page_hint": provenance.get("page_hint"),
        "review_decision": provenance.get("review_decision"),
        "final_review_decision": provenance.get("final_review_decision"),
        "final_review_id": provenance.get("final_review_id"),
        "final_review_status": provenance.get("final_review_status"),
        "revision_status": provenance.get("revision_status"),
        "human_revision_note": provenance.get("human_revision_note"),
        "ingested_at": provenance.get("ingested_at"),
        "source_review_file": provenance.get("source_review_file"),
    }


def import_edges(edges: list[dict[str, Any]], uri: str, user: str, password: str, database: str) -> None:
    try:
        from neo4j import GraphDatabase
    except ImportError as exc:
        raise RuntimeError("Missing dependency: pip install neo4j") from exc

    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            session.run("CREATE CONSTRAINT kg_node_id IF NOT EXISTS FOR (n:KGNode) REQUIRE n.id IS UNIQUE")
            for edge in edges:
                source_id = str(edge.get("source", "")).strip()
                target_id = str(edge.get("target", "")).strip()
                rel_type = relation_type(str(edge.get("relation", "")))
                props = {key: value for key, value in relationship_properties(edge).items() if value is not None}
                query = f"""
                MERGE (source:KGNode {{id: $source_id}})
                  SET source.type = $source_type, source.name = $source_name
                MERGE (target:KGNode {{id: $target_id}})
                  SET target.type = $target_type, target.name = $target_name
                MERGE (source)-[r:{rel_type} {{review_id: $review_id}}]->(target)
                  SET r += $props
                """
                session.run(
                    query,
                    source_id=source_id,
                    source_type=node_type(source_id),
                    source_name=node_name(source_id),
                    target_id=target_id,
                    target_type=node_type(target_id),
                    target_name=node_name(target_id),
                    review_id=props.get("review_id", f"{source_id}|{rel_type}|{target_id}"),
                    props=props,
                )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Curated edges.jsonl")
    parser.add_argument("--env-file", type=Path, default=Path(".env"), help="Path to .env")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    apply_env_file(args.env_file)
    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    user = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "")
    database = os.environ.get("NEO4J_DATABASE", "neo4j")
    if not password:
        raise ValueError("Set NEO4J_PASSWORD in .env before importing")
    edges = read_jsonl(args.input)
    import_edges(edges, uri, user, password, database)
    print(f"Imported {len(edges)} edges into {uri}/{database}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
