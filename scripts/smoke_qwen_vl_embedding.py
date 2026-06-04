#!/usr/bin/env python
"""Smoke-test qwen3-vl-embedding and optionally store image vectors in Chroma."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_CHROMA_PATH = Path("data/chroma")
DEFAULT_VISUAL_COLLECTION = "guitar_visual_chunks"
DEFAULT_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding"


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


def image_data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def extract_embeddings(payload: dict[str, Any]) -> list[list[float]]:
    output = payload.get("output", {})
    candidates = output.get("embeddings") or output.get("embedding") or payload.get("embeddings")
    if isinstance(candidates, list) and candidates and isinstance(candidates[0], dict):
        return [item["embedding"] for item in candidates if "embedding" in item]
    if isinstance(candidates, list) and candidates and isinstance(candidates[0], (int, float)):
        return [candidates]
    raise ValueError(f"Cannot find embeddings in response keys: {list(payload.keys())}")


class QwenVLEmbedder:
    def __init__(self) -> None:
        self.api_url = os.environ.get("MULTIMODAL_EMBEDDING_API_URL", DEFAULT_API_URL)
        self.api_key = os.environ.get("VL_EMBEDDING_API_KEY") or os.environ.get("LLM_API_KEY", "")
        self.model = os.environ.get("VL_EMBEDDING_MODEL", "qwen3-vl-embedding")
        self.dimensions = int(os.environ.get("VL_EMBEDDING_DIMENSIONS", "1024") or 1024)
        self.timeout = int(os.environ.get("VL_EMBEDDING_TIMEOUT_SECONDS", "120"))
        self.max_retries = int(os.environ.get("VL_EMBEDDING_MAX_RETRIES", "2"))
        if not self.api_key:
            raise ValueError("Set VL_EMBEDDING_API_KEY or LLM_API_KEY in .env")

    def embed_contents(self, contents: list[dict[str, str]], *, fusion: bool = False) -> list[list[float]]:
        request_payload: dict[str, Any] = {
            "model": self.model,
            "input": {"contents": contents},
            "parameters": {
                "dimension": self.dimensions,
                "enable_fusion": fusion,
            },
        }
        body = json.dumps(request_payload, ensure_ascii=False).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                req = urllib.request.Request(self.api_url, data=body, headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                return extract_embeddings(data)
            except (urllib.error.URLError, urllib.error.HTTPError, KeyError, ValueError, json.JSONDecodeError) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(1.5 * (attempt + 1))
        raise RuntimeError(f"qwen3-vl-embedding request failed: {last_error}")

    def embed_text(self, text: str) -> list[float]:
        return self.embed_contents([{"text": text}], fusion=False)[0]

    def embed_image(self, path: Path) -> list[float]:
        return self.embed_contents([{"image": image_data_uri(path)}], fusion=False)[0]


def upsert_images(args: argparse.Namespace) -> None:
    try:
        import chromadb
    except ImportError as exc:
        raise RuntimeError("Missing dependency: install chromadb first") from exc

    embedder = QwenVLEmbedder()
    client = chromadb.PersistentClient(path=str(args.chroma_path))
    if args.reset:
        try:
            client.delete_collection(args.collection)
        except Exception:
            pass
    collection = client.get_or_create_collection(name=args.collection, metadata={"hnsw:space": "cosine"})

    ids: list[str] = []
    docs: list[str] = []
    metadatas: list[dict[str, str | int]] = []
    embeddings: list[list[float]] = []
    for index, image_path in enumerate(args.images, start=1):
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(path)
        vector = embedder.embed_image(path)
        doc = f"Visual evidence image: {path.name}"
        ids.append(f"visual:{path.stem}:{index}")
        docs.append(doc)
        metadatas.append(
            {
                "image_path": str(path),
                "image_name": path.name,
                "source_type": "image",
                "embedding_model": embedder.model,
                "embedding_dimensions": len(vector),
            }
        )
        embeddings.append(vector)
        print(f"embedded image {index}/{len(args.images)}: {path} dim={len(vector)}")

    collection.upsert(ids=ids, documents=docs, metadatas=metadatas, embeddings=embeddings)
    print(
        json.dumps(
            {
                "chroma_path": str(args.chroma_path),
                "collection": args.collection,
                "images": len(ids),
                "collection_count": collection.count(),
                "model": embedder.model,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def query(args: argparse.Namespace) -> None:
    try:
        import chromadb
    except ImportError as exc:
        raise RuntimeError("Missing dependency: install chromadb first") from exc

    embedder = QwenVLEmbedder()
    client = chromadb.PersistentClient(path=str(args.chroma_path))
    collection = client.get_collection(name=args.collection)
    result = collection.query(
        query_embeddings=[embedder.embed_text(args.query)],
        n_results=args.n_results,
        include=["documents", "metadatas", "distances"],
    )
    for idx, doc_id in enumerate(result.get("ids", [[]])[0]):
        metadata = result["metadatas"][0][idx]
        distance = result["distances"][0][idx]
        print(f"\n## {idx + 1}. {doc_id} distance={distance:.4f}")
        print(f"- image: {metadata.get('image_path')}")
        print(f"- model: {metadata.get('embedding_model')} dim={metadata.get('embedding_dimensions')}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    parser.add_argument(
        "--chroma-path",
        type=Path,
        default=Path(os.environ.get("CHROMA_PATH", str(DEFAULT_CHROMA_PATH))),
    )
    parser.add_argument(
        "--collection",
        default=os.environ.get("CHROMA_VISUAL_COLLECTION", DEFAULT_VISUAL_COLLECTION),
    )
    parser.add_argument("--image", dest="images", action="append", default=[], help="Local image path")
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--query", default="")
    parser.add_argument("--n-results", type=int, default=3)
    args = parser.parse_args(argv)
    apply_env_file(args.env_file)
    args.chroma_path = Path(os.environ.get("CHROMA_PATH", str(args.chroma_path)))
    args.collection = os.environ.get("CHROMA_VISUAL_COLLECTION", args.collection)
    return args


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.query:
        query(args)
    else:
        if not args.images:
            raise ValueError("Provide at least one --image, or use --query")
        upsert_images(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
