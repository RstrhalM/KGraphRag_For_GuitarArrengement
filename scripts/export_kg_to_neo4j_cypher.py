#!/usr/bin/env python
"""Export curated KG JSONL to a Neo4j Browser-friendly Cypher file."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


RELATION_RE = re.compile(r"^[a-z_]+$")


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


def cypher_string(value: Any) -> str:
    return json.dumps("" if value is None else str(value), ensure_ascii=False)


def cypher_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if value is None:
        return "null"
    return cypher_string(value)


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
        "confidence": edge.get("confidence"),
        "context_condition": edge.get("context_condition"),
        "review_note": edge.get("review_note"),
        "evidence": edge.get("evidence"),
        "needs_visual_context": edge.get("needs_visual_context", False),
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


def properties_literal(props: dict[str, Any]) -> str:
    parts = []
    for key, value in props.items():
        if value is None:
            continue
        parts.append(f"{key}: {cypher_value(value)}")
    return "{ " + ", ".join(parts) + " }"


def render_cypher(edges: list[dict[str, Any]]) -> str:
    lines = [
        "// Generated from curated KG JSONL.",
        "CREATE CONSTRAINT kg_node_id IF NOT EXISTS FOR (n:KGNode) REQUIRE n.id IS UNIQUE;",
        "",
    ]

    node_ids = sorted({str(edge.get("source", "")) for edge in edges} | {str(edge.get("target", "")) for edge in edges})
    for node_id in node_ids:
        if not node_id:
            continue
        lines.append(
            "MERGE (n:KGNode {id: "
            + cypher_string(node_id)
            + "}) SET n.type = "
            + cypher_string(node_type(node_id))
            + ", n.name = "
            + cypher_string(node_name(node_id))
            + ";"
        )

    lines.append("")
    for edge in edges:
        source = str(edge.get("source", "")).strip()
        target = str(edge.get("target", "")).strip()
        relation = relation_type(str(edge.get("relation", "")))
        props = properties_literal(relationship_properties(edge))
        lines.extend(
            [
                f"MATCH (source:KGNode {{id: {cypher_string(source)}}})",
                f"MATCH (target:KGNode {{id: {cypher_string(target)}}})",
                f"MERGE (source)-[r:{relation} {{review_id: {cypher_string(edge.get('provenance', {}).get('review_id'))}}}]->(target)",
                f"SET r += {props};",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Curated edges.jsonl")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output .cypher file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    edges = read_jsonl(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_cypher(edges), encoding="utf-8", newline="\n")
    print(f"Wrote {len(edges)} edges to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
