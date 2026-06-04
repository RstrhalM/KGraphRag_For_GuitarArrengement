#!/usr/bin/env python
"""Ingest local guitar textbook chunks into a persistent Chroma collection."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from local_text_embedding import DEFAULT_LOCAL_MODEL, LocalTransformerEmbedder, write_model_metadata


DEFAULT_CATALOG = Path("data/sources/catalog.json")
DEFAULT_CHROMA_PATH = Path("data/chroma")
DEFAULT_COLLECTION = "guitar_text_chunks"
DEFAULT_HASH_DIM = 384


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


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path or not path.exists() or not path.is_file():
        return rows
    with path.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON in {path} line {line_no}: {exc}") from exc
            if isinstance(row, dict):
                rows.append(row)
    return rows


def stable_id(*parts: str) -> str:
    raw = "::".join(parts)
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]
    safe = re.sub(r"[^a-zA-Z0-9_.:-]+", "_", raw)[:120]
    return f"{safe}:{digest}"


def normalize_text(text: str) -> str:
    text = text.replace("\ufeff", "")
    text = re.sub(r"\bnbsp\b", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def metadata_value(value: Any) -> str | int | float | bool:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return value
    return json.dumps(value, ensure_ascii=False)


def load_review_index(path: Path) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    if not path or not path.exists() or not path.is_file():
        return index
    for row in read_jsonl(path):
        chunk_id = str(row.get("chunk_id", "")).strip()
        if not chunk_id:
            continue
        item = index.setdefault(
            chunk_id,
            {
                "review_ids": [],
                "kg_edges": [],
                "kg_nodes": set(),
                "gp5_feature_triggers": set(),
                "style_tags": set(),
            },
        )
        review_id = str(row.get("review_id", "")).strip()
        if review_id:
            item["review_ids"].append(review_id)
        source = str(row.get("source", "")).strip()
        relation = str(row.get("relation", "")).strip()
        target = str(row.get("target", "")).strip()
        if source and target and relation:
            item["kg_edges"].append(f"{source} -[{relation}]-> {target}")
            item["kg_nodes"].update([source, target])
        for trigger in row.get("gp5_feature_triggers", []) or []:
            item["gp5_feature_triggers"].add(str(trigger))
        for tag in row.get("style_tags", []) or []:
            item["style_tags"].add(str(tag))

    for item in index.values():
        item["kg_nodes"] = sorted(item["kg_nodes"])
        item["gp5_feature_triggers"] = sorted(item["gp5_feature_triggers"])
        item["style_tags"] = sorted(item["style_tags"])
    return index


def source_chunk_paths(source: dict[str, Any]) -> list[Path]:
    paths: list[Path] = []
    if source.get("chunks_path"):
        paths.append(Path(str(source["chunks_path"])))
    for path in source.get("chunks_paths", []) or []:
        paths.append(Path(str(path)))
    return paths


def load_json_chunks(source: dict[str, Any], review_index: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    docs: list[dict[str, Any]] = []
    source_id = str(source["source_id"])
    for chunks_path in source_chunk_paths(source):
        if not chunks_path.exists():
            continue
        chunks = read_json(chunks_path)
        if not isinstance(chunks, list):
            continue
        for chunk in chunks:
            if not isinstance(chunk, dict):
                continue
            chunk_id = str(chunk.get("chunk_id") or f"chunk_{len(docs) + 1:04d}")
            text = normalize_text(str(chunk.get("text", "")))
            if not text:
                continue
            linked = review_index.get(chunk_id, {})
            style_tags = sorted(
                set(source.get("style_tags", []) or []) | set(linked.get("style_tags", []) or [])
            )
            metadata = {
                "source_id": source_id,
                "source_title": source.get("title", ""),
                "source_type": source.get("type", ""),
                "chunk_id": chunk_id,
                "lesson_title": chunk.get("lesson_title", ""),
                "page_hint": chunk.get("page_hint", ""),
                "style_tags": style_tags,
                "raw_path": source.get("raw_path", ""),
                "chunks_path": str(chunks_path),
                "review_jsonl": source.get("review_jsonl", ""),
                "linked_review_ids": linked.get("review_ids", []),
                "linked_kg_edges": linked.get("kg_edges", []),
                "linked_kg_nodes": linked.get("kg_nodes", []),
                "gp5_feature_triggers": linked.get("gp5_feature_triggers", []),
                "image_refs": chunk.get("image_refs", []),
            }
            docs.append(
                {
                    "id": stable_id(source_id, chunk_id),
                    "document": text,
                    "metadata": {key: metadata_value(value) for key, value in metadata.items()},
                }
            )
    return docs


def split_markdown(text: str, max_chars: int) -> list[dict[str, Any]]:
    text = re.sub(r"!\[[^\]]*\]\(([^)]+)\)", r"[IMAGE_BLOCK:\1]", normalize_text(text))
    blocks = re.split(r"(?=\n#{1,3}\s+)", "\n" + text)
    chunks: list[dict[str, Any]] = []
    buffer: list[str] = []
    index = 1

    def flush() -> None:
        nonlocal buffer, index
        body = "\n".join(buffer).strip()
        if not body:
            buffer = []
            return
        chunks.append({"chunk_id": f"md_chunk_{index:04d}", "text": body})
        index += 1
        buffer = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if sum(len(x) + 1 for x in buffer) + len(block) > max_chars and buffer:
            flush()
        if len(block) <= max_chars:
            buffer.append(block)
            continue
        for start in range(0, len(block), max_chars):
            if buffer:
                flush()
            chunks.append({"chunk_id": f"md_chunk_{index:04d}", "text": block[start : start + max_chars]})
            index += 1
    flush()
    return chunks


def load_markdown_source(source: dict[str, Any], max_chars: int) -> list[dict[str, Any]]:
    markdown_path = Path(str(source.get("markdown_path", "")))
    if not markdown_path.exists():
        return []
    docs: list[dict[str, Any]] = []
    source_id = str(source["source_id"])
    for chunk in split_markdown(markdown_path.read_text(encoding="utf-8"), max_chars=max_chars):
        chunk_id = str(chunk["chunk_id"])
        metadata = {
            "source_id": source_id,
            "source_title": source.get("title", ""),
            "source_type": source.get("type", ""),
            "chunk_id": chunk_id,
            "lesson_title": "",
            "page_hint": "",
            "style_tags": source.get("style_tags", []),
            "raw_path": source.get("raw_path", ""),
            "markdown_path": str(markdown_path),
            "linked_review_ids": [],
            "linked_kg_edges": [],
            "linked_kg_nodes": [],
            "gp5_feature_triggers": [],
            "image_refs": re.findall(r"\[IMAGE_BLOCK:([^\]]+)\]", chunk["text"]),
        }
        docs.append(
            {
                "id": stable_id(source_id, chunk_id),
                "document": chunk["text"],
                "metadata": {key: metadata_value(value) for key, value in metadata.items()},
            }
        )
    return docs


TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_+\-/'.#]*|\d+(?:\.\d+)?|[\u4e00-\u9fff]")


class HashEmbedder:
    def __init__(self, dim: int = DEFAULT_HASH_DIM) -> None:
        self.dim = dim

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_one(text) for text in texts]

    def _embed_one(self, text: str) -> list[float]:
        vector = [0.0] * self.dim
        tokens = TOKEN_RE.findall(text.lower())
        for token in tokens:
            digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
            bucket = int.from_bytes(digest[:4], "little") % self.dim
            sign = 1.0 if digest[4] & 1 else -1.0
            vector[bucket] += sign
        norm = math.sqrt(sum(value * value for value in vector))
        if norm:
            vector = [value / norm for value in vector]
        return vector


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
            raise ValueError("Set EMBEDDING_API_BASE_URL/EMBEDDING_MODEL or use --embedding-provider hash")

    def embed(self, texts: list[str]) -> list[list[float]]:
        payload = {"model": self.model, "input": texts}
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
                rows = sorted(data["data"], key=lambda item: int(item.get("index", 0)))
                return [row["embedding"] for row in rows]
            except (urllib.error.URLError, urllib.error.HTTPError, KeyError, json.JSONDecodeError) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(1.5 * (attempt + 1))
        raise RuntimeError(f"Embedding request failed: {last_error}")


class LocalEmbedder:
    def __init__(self, batch_size: int) -> None:
        self.batch_size = batch_size
        self.backend = LocalTransformerEmbedder(
            os.environ.get("LOCAL_EMBEDDING_MODEL", DEFAULT_LOCAL_MODEL),
            device=os.environ.get("LOCAL_EMBEDDING_DEVICE", "auto"),
            max_length=int(os.environ.get("LOCAL_EMBEDDING_MAX_LENGTH", "2048")),
        )

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self.backend.embed(texts, batch_size=self.batch_size)

    def metadata(self) -> dict[str, Any]:
        return self.backend.metadata()


def make_embedder(provider: str, batch_size: int = 8) -> HashEmbedder | APIEmbedder | LocalEmbedder:
    if provider == "api":
        return APIEmbedder()
    if provider == "local_qwen3":
        return LocalEmbedder(batch_size=batch_size)
    return HashEmbedder(dim=int(os.environ.get("CHROMA_HASH_EMBEDDING_DIM", str(DEFAULT_HASH_DIM))))


def batched(items: list[dict[str, Any]], size: int) -> list[list[dict[str, Any]]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def build_documents(catalog_path: Path, markdown_max_chars: int) -> list[dict[str, Any]]:
    catalog = read_json(catalog_path)
    if not isinstance(catalog, list):
        raise ValueError("Catalog must be a JSON array")
    docs: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for source in catalog:
        if not isinstance(source, dict) or not source.get("source_id"):
            continue
        review_index = load_review_index(Path(str(source.get("review_jsonl", ""))))
        source_docs = load_json_chunks(source, review_index)
        if not source_docs and source.get("markdown_path"):
            source_docs = load_markdown_source(source, max_chars=markdown_max_chars)
        for doc in source_docs:
            if doc["id"] in seen_ids:
                continue
            seen_ids.add(doc["id"])
            docs.append(doc)
    return docs


def ingest(args: argparse.Namespace) -> None:
    try:
        import chromadb
    except ImportError as exc:
        raise RuntimeError("Missing dependency: install chromadb first") from exc

    docs = build_documents(args.catalog, markdown_max_chars=args.markdown_max_chars)
    if args.reset and args.chroma_path.exists():
        # Chroma handles collection-level replacement below; keep the directory itself intact.
        pass

    client = chromadb.PersistentClient(path=str(args.chroma_path))
    if args.reset:
        try:
            client.delete_collection(args.collection)
        except Exception:
            pass
    collection = client.get_or_create_collection(name=args.collection, metadata={"hnsw:space": "cosine"})
    embedder = make_embedder(args.embedding_provider, batch_size=args.batch_size)
    batch_size = min(args.batch_size, 10) if args.embedding_provider == "api" else args.batch_size
    embedder_metadata = embedder.metadata() if hasattr(embedder, "metadata") else {}

    total = 0
    for batch in batched(docs, batch_size):
        embeddings = embedder.embed([item["document"] for item in batch])
        collection.upsert(
            ids=[item["id"] for item in batch],
            documents=[item["document"] for item in batch],
            metadatas=[item["metadata"] for item in batch],
            embeddings=embeddings,
        )
        total += len(batch)
        print(f"upserted {total}/{len(docs)}")

    print(
        json.dumps(
            {
                "chroma_path": str(args.chroma_path),
                "collection": args.collection,
                "embedding_provider": args.embedding_provider,
                "embedding": embedder_metadata,
                "documents": len(docs),
                "collection_count": collection.count(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    if args.embedding_provider.startswith("local"):
        write_model_metadata(
            args.chroma_path / f"{args.collection}.embedding_metadata.json",
            {
                "collection": args.collection,
                "embedding_provider": args.embedding_provider,
                **embedder_metadata,
            },
        )


def query(args: argparse.Namespace) -> None:
    try:
        import chromadb
    except ImportError as exc:
        raise RuntimeError("Missing dependency: install chromadb first") from exc

    client = chromadb.PersistentClient(path=str(args.chroma_path))
    collection = client.get_collection(name=args.collection)
    embedder = make_embedder(args.embedding_provider, batch_size=args.batch_size)
    result = collection.query(
        query_texts=None,
        query_embeddings=embedder.embed([args.query]),
        n_results=args.n_results,
        include=["documents", "metadatas", "distances"],
    )
    for idx, doc_id in enumerate(result.get("ids", [[]])[0]):
        metadata = result["metadatas"][0][idx]
        distance = result["distances"][0][idx]
        document = result["documents"][0][idx]
        print(f"\n## {idx + 1}. {doc_id}  distance={distance:.4f}")
        print(f"- source: {metadata.get('source_title')} / {metadata.get('chunk_id')}")
        print(f"- tags: {metadata.get('style_tags')}")
        print(f"- reviews: {metadata.get('linked_review_ids')}")
        print(document[:700].replace("\n", " ") + ("..." if len(document) > 700 else ""))


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=Path(".env"), help="Path to .env")
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG, help="Source catalog JSON")
    parser.add_argument(
        "--chroma-path",
        type=Path,
        default=None,
        help="Persistent Chroma directory",
    )
    parser.add_argument(
        "--collection",
        default=None,
        help="Chroma collection name",
    )
    parser.add_argument(
        "--embedding-provider",
        choices=["hash", "api", "local_qwen3"],
        default=None,
        help="Embedding backend. hash is local and dependency-free; api calls /embeddings; local_qwen3 loads a local/HF Qwen3 embedding model.",
    )
    parser.add_argument("--batch-size", type=int, default=int(os.environ.get("CHROMA_BATCH_SIZE", "16")))
    parser.add_argument("--markdown-max-chars", type=int, default=3500)
    parser.add_argument("--reset", action="store_true", help="Delete and recreate the target collection")
    parser.add_argument("--query", default="", help="Query after opening the collection instead of ingesting")
    parser.add_argument("--n-results", type=int, default=5)
    args = parser.parse_args(argv)
    apply_env_file(args.env_file)
    args.chroma_path = args.chroma_path or Path(os.environ.get("CHROMA_PATH", str(DEFAULT_CHROMA_PATH)))
    args.collection = args.collection or os.environ.get("CHROMA_TEXT_COLLECTION", DEFAULT_COLLECTION)
    args.embedding_provider = args.embedding_provider or os.environ.get("EMBEDDING_PROVIDER", "hash")
    return args


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.query:
        query(args)
    else:
        ingest(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
