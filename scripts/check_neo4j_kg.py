#!/usr/bin/env python
"""Check Neo4j connectivity and summarize imported KG data."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


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


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=Path(".env"), help="Path to .env")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    apply_env_file(args.env_file)
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

    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            counts = session.run(
                """
                MATCH (n:KGNode)
                WITH count(n) AS nodes
                MATCH ()-[r]->()
                RETURN nodes, count(r) AS relationships
                """
            ).single()
            by_type = session.run(
                """
                MATCH (n:KGNode)
                RETURN n.type AS type, count(*) AS count
                ORDER BY count DESC, type
                """
            ).data()
            by_rel = session.run(
                """
                MATCH ()-[r]->()
                RETURN type(r) AS relation, count(*) AS count
                ORDER BY count DESC, relation
                """
            ).data()
            samples = session.run(
                """
                MATCH (a:KGNode)-[r]->(b:KGNode)
                RETURN a.id AS source, type(r) AS relation, b.id AS target,
                       r.knowledge_type AS knowledge_type, r.confidence AS confidence
                ORDER BY source, relation, target
                LIMIT 8
                """
            ).data()

    print("Neo4j connection OK")
    print({"uri": uri, "database": database, "nodes": counts["nodes"], "relationships": counts["relationships"]})
    print("Node types:", by_type)
    print("Relation types:", by_rel)
    print("Samples:", samples)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
