#!/usr/bin/env python
"""Clone a Chroma collection locally without recomputing embeddings."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chroma-path", type=Path, default=Path("data/chroma"))
    parser.add_argument("--source", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--batch-size", type=int, default=200)
    parser.add_argument("--reset", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    import chromadb

    client = chromadb.PersistentClient(path=str(args.chroma_path))
    source = client.get_collection(args.source)
    if args.reset:
        try:
            client.delete_collection(args.target)
        except Exception:
            pass
    target = client.get_or_create_collection(
        args.target,
        metadata=dict(source.metadata or {"hnsw:space": "cosine"}),
    )
    total = source.count()
    copied = 0
    for offset in range(0, total, args.batch_size):
        batch: dict[str, Any] = source.get(
            limit=args.batch_size,
            offset=offset,
            include=["documents", "metadatas", "embeddings"],
        )
        ids = batch.get("ids") or []
        if not ids:
            continue
        target.upsert(
            ids=ids,
            documents=batch.get("documents"),
            metadatas=batch.get("metadatas"),
            embeddings=batch.get("embeddings"),
        )
        copied += len(ids)
        print(f"copied {copied}/{total}")
    report = {
        "source": args.source,
        "source_count": total,
        "target": args.target,
        "target_count": target.count(),
        "copied": copied,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if copied == total and target.count() == total else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
