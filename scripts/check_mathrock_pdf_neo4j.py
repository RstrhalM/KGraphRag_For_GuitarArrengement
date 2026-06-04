from pathlib import Path
import os

from neo4j import GraphDatabase


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env(Path(".env"))

uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
user = os.environ.get("NEO4J_USER", "neo4j")
password = os.environ.get("NEO4J_PASSWORD", "")

queries = {
    "nodes_total": "MATCH (n) RETURN count(n) AS c",
    "rels_total": "MATCH ()-[r]->() RETURN count(r) AS c",
    "mathrock_pdf_nodes": """
        MATCH (n)
        WHERE any(k IN keys(n)
          WHERE toString(n[k]) CONTAINS 'mathrock_pdf_steve_h'
             OR toString(n[k]) CONTAINS 'Math Rock Guitar E-book')
        RETURN count(n) AS c
    """,
    "mathrock_pdf_rels": """
        MATCH ()-[r]->()
        WHERE any(k IN keys(r)
          WHERE toString(r[k]) CONTAINS 'mathrock_pdf_steve_h'
             OR toString(r[k]) CONTAINS 'Math Rock Guitar E-book')
        RETURN count(r) AS c
    """,
}

with GraphDatabase.driver(uri, auth=(user, password)) as driver:
    with driver.session() as session:
        result = {name: session.run(query).single()["c"] for name, query in queries.items()}

print(result)
