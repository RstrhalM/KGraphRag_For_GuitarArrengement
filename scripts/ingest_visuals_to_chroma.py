#!/usr/bin/env python
"""Ingest MinerU image blocks and optional full-page images into Chroma."""

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

from embedding_cache import EmbeddingCache


DEFAULT_CHROMA_PATH = Path("data/chroma")
DEFAULT_COLLECTION = "guitar_visual_chunks"
DEFAULT_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding"
DEFAULT_EMBEDDING_CACHE = Path("data/cache/embeddings.sqlite")


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
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def extract_embeddings(payload: dict[str, Any]) -> list[list[float]]:
    output = payload.get("output", {})
    candidates = output.get("embeddings") or output.get("embedding") or payload.get("embeddings")
    if isinstance(candidates, list) and candidates and isinstance(candidates[0], dict):
        return [item["embedding"] for item in candidates if "embedding" in item]
    if isinstance(candidates, list) and candidates and isinstance(candidates[0], (int, float)):
        return [candidates]
    raise ValueError(f"Cannot find embeddings in response keys: {list(payload.keys())}")


class QwenVLEmbedder:
    def __init__(self, cache: EmbeddingCache) -> None:
        self.api_url = os.environ.get("MULTIMODAL_EMBEDDING_API_URL", DEFAULT_API_URL)
        self.api_key = os.environ.get("VL_EMBEDDING_API_KEY") or os.environ.get("LLM_API_KEY", "")
        self.model = os.environ.get("VL_EMBEDDING_MODEL", "qwen3-vl-embedding")
        self.dimensions = int(os.environ.get("VL_EMBEDDING_DIMENSIONS", "1024") or 1024)
        self.timeout = int(os.environ.get("VL_EMBEDDING_TIMEOUT_SECONDS", "120"))
        self.max_retries = int(os.environ.get("VL_EMBEDDING_MAX_RETRIES", "2"))
        self.cache = cache
        self.cache_hits = 0
        self.cache_misses = 0
        if not self.api_key:
            raise ValueError("Set VL_EMBEDDING_API_KEY or LLM_API_KEY in .env")

    def embed_images(self, paths: list[Path]) -> list[list[float]]:
        vectors: list[list[float] | None] = [None] * len(paths)
        misses: list[tuple[int, Path, bytes, str]] = []
        for idx, path in enumerate(paths):
            payload = path.read_bytes()
            key = EmbeddingCache.make_key(
                provider="dashscope",
                model=self.model,
                dimensions=self.dimensions,
                input_type="image",
                content=payload,
                endpoint=self.api_url,
            )
            cached = self.cache.get(key)
            if cached is not None:
                vectors[idx] = cached
                self.cache_hits += 1
            else:
                misses.append((idx, path, payload, key))
                self.cache_misses += 1

        if misses:
            miss_paths = [path for _, path, _, _ in misses]
            payload = {
                "model": self.model,
                "input": {"contents": [{"image": image_data_uri(path)} for path in miss_paths]},
                "parameters": {"dimension": self.dimensions, "enable_fusion": False},
            }
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            last_error: Exception | None = None
            for attempt in range(self.max_retries + 1):
                try:
                    req = urllib.request.Request(self.api_url, data=body, headers=headers, method="POST")
                    with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                    embeddings = extract_embeddings(data)
                    if len(embeddings) != len(misses):
                        raise ValueError(f"Expected {len(misses)} embeddings, got {len(embeddings)}")
                    for (idx, _path, image_bytes, key), vector in zip(misses, embeddings):
                        vectors[idx] = vector
                        self.cache.set(
                            key,
                            vector,
                            provider="dashscope",
                            model=self.model,
                            dimensions=self.dimensions,
                            input_type="image",
                            content=image_bytes,
                        )
                    break
                except (urllib.error.URLError, urllib.error.HTTPError, KeyError, ValueError, json.JSONDecodeError) as exc:
                    last_error = exc
                    if attempt < self.max_retries:
                        time.sleep(1.5 * (attempt + 1))
                    else:
                        raise RuntimeError(f"qwen3-vl-embedding request failed: {last_error}") from exc

        return [vector for vector in vectors if vector is not None]


def parse_pages(value: str) -> set[int] | None:
    value = value.strip()
    if not value:
        return None
    pages: set[int] = set()
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            pages.update(range(int(start), int(end) + 1))
        else:
            pages.add(int(part))
    return pages


def metadata_value(value: Any) -> str | int | float | bool:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return value
    return json.dumps(value, ensure_ascii=False)


def text_items_by_page(items: list[dict[str, Any]]) -> dict[int, list[dict[str, Any]]]:
    pages: dict[int, list[dict[str, Any]]] = {}
    for item in items:
        if item.get("type") != "text":
            continue
        page = int(item.get("page_idx", -1)) + 1
        if page <= 0:
            continue
        pages.setdefault(page, []).append(item)
    return pages


def page_context(text_items: list[dict[str, Any]], image_bbox: list[int]) -> tuple[str, str]:
    if not text_items:
        return "", ""
    image_y = image_bbox[1] if len(image_bbox) >= 2 else 0
    titles: list[str] = []
    nearby: list[tuple[int, str]] = []
    for item in text_items:
        text = " ".join(str(item.get("text", "")).split())
        if not text:
            continue
        if item.get("text_level"):
            titles.append(text[:100])
        bbox = item.get("bbox") or [0, 0, 0, 0]
        y = int(bbox[1]) if len(bbox) >= 2 else 0
        nearby.append((abs(y - image_y), text[:180]))
    return " | ".join(titles[:5]), " | ".join(text for _, text in sorted(nearby)[:5])


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path or not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def build_rows(args: argparse.Namespace) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    selected_pages = parse_pages(args.pages)
    include_types = {part.strip() for part in args.include_types.split(",") if part.strip()}
    style_tags = [part.strip() for part in args.style_tags.split(",") if part.strip()]

    if args.content_list:
        items = json.loads(args.content_list.read_text(encoding="utf-8"))
        text_by_page = text_items_by_page(items)
        for item in items:
            if item.get("type") not in include_types:
                continue
            page = int(item.get("page_idx", -1)) + 1
            if page <= 0 or (selected_pages is not None and page not in selected_pages):
                continue
            rel_path = str(item.get("img_path", ""))
            image_path = args.book_dir / rel_path
            if not image_path.is_file():
                continue
            topic_hint, nearby_text = page_context(text_by_page.get(page, []), item.get("bbox") or [])
            rows.append(
                {
                    "visual_id": f"{args.source_id}:mineru:p{page:03d}:{image_path.stem}",
                    "source_id": args.source_id,
                    "source_title": args.source_title,
                    "source_type": "mineru_image_block",
                    "visual_granularity": "image_block",
                    "page": page,
                    "page_idx": page - 1,
                    "image_path": str(image_path),
                    "image_name": image_path.name,
                    "bbox": item.get("bbox") or [],
                    "style_tags": style_tags,
                    "topic_hint": topic_hint,
                    "nearby_text": nearby_text,
                    "original_block_type": item.get("type", ""),
                }
            )

    for item in read_jsonl(args.full_page_manifest):
        page = int(item.get("page", 0) or 0)
        if page <= 0 or (selected_pages is not None and page not in selected_pages):
            continue
        image_path = Path(str(item.get("image_path", "")))
        if not image_path.is_file():
            continue
        rows.append(
            {
                "visual_id": f"{args.source_id}:page:p{page:03d}",
                "source_id": args.source_id,
                "source_title": args.source_title,
                "source_type": "pdf_page_image",
                "visual_granularity": "full_page",
                "page": page,
                "page_idx": page - 1,
                "image_path": str(image_path),
                "image_name": image_path.name,
                "bbox": [],
                "style_tags": style_tags,
                "topic_hint": item.get("reason", ""),
                "nearby_text": item.get("sample", ""),
                "original_block_type": "page",
            }
        )

    return rows


def write_manifest(rows: list[dict[str, Any]], manifest_jsonl: Path, report_md: Path) -> None:
    manifest_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with manifest_jsonl.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    lines = ["# Visual Chroma Ingest Manifest", "", f"- visual items: {len(rows)}", ""]
    for row in rows[:300]:
        lines.extend(
            [
                f"## {row['visual_id']}",
                "",
                f"- source_type: `{row['source_type']}`",
                f"- granularity: `{row['visual_granularity']}`",
                f"- page: `{row['page']}`",
                f"- image: `{row['image_path']}`",
                f"- topic_hint: {row['topic_hint']}",
                f"- nearby_text: {row['nearby_text']}",
                "",
            ]
        )
    if len(rows) > 300:
        lines.append(f"... {len(rows) - 300} more items omitted")
    report_md.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def batched(items: list[dict[str, Any]], size: int) -> list[list[dict[str, Any]]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def ingest(args: argparse.Namespace, rows: list[dict[str, Any]]) -> None:
    try:
        import chromadb
    except ImportError as exc:
        raise RuntimeError("Missing dependency: install chromadb first") from exc

    client = chromadb.PersistentClient(path=str(args.chroma_path))
    collection = client.get_or_create_collection(name=args.collection, metadata={"hnsw:space": "cosine"})
    cache = EmbeddingCache(args.embedding_cache, enabled=not args.no_embedding_cache)
    embedder = QwenVLEmbedder(cache)

    done = 0
    for batch in batched(rows, args.batch_size):
        image_paths = [Path(row["image_path"]) for row in batch]
        embeddings = embedder.embed_images(image_paths)
        ids: list[str] = []
        documents: list[str] = []
        metadatas: list[dict[str, Any]] = []
        for row, vector in zip(batch, embeddings):
            document = " | ".join(
                str(part)
                for part in [
                    row.get("source_title", ""),
                    row.get("visual_granularity", ""),
                    f"page {row.get('page')}",
                    row.get("topic_hint", ""),
                    row.get("nearby_text", ""),
                ]
                if part
            )
            metadata = {key: metadata_value(value) for key, value in row.items()}
            metadata["embedding_model"] = embedder.model
            metadata["embedding_dimensions"] = len(vector)
            ids.append(row["visual_id"])
            documents.append(document)
            metadatas.append(metadata)
        collection.upsert(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)
        done += len(batch)
        print(
            f"upserted {done}/{len(rows)} "
            f"(cache_hits={embedder.cache_hits}, cache_misses={embedder.cache_misses})",
            flush=True,
        )

    print(
        json.dumps(
            {
                "chroma_path": str(args.chroma_path),
                "collection": args.collection,
                "items": len(rows),
                "collection_count": collection.count(),
                "embedding_model": embedder.model,
                "embedding_cache": cache.stats(),
            },
            ensure_ascii=False,
            indent=2,
        ),
        flush=True,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--source-title", required=True)
    parser.add_argument("--style-tags", default="")
    parser.add_argument("--book-dir", type=Path, default=Path("."))
    parser.add_argument("--content-list", type=Path)
    parser.add_argument("--include-types", default="image,table")
    parser.add_argument("--full-page-manifest", type=Path, default=Path(""))
    parser.add_argument("--pages", default="")
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--manifest-jsonl", type=Path, required=True)
    parser.add_argument("--report-md", type=Path, required=True)
    parser.add_argument("--manifest-only", action="store_true")
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--chroma-path", type=Path, default=Path(os.environ.get("CHROMA_PATH", str(DEFAULT_CHROMA_PATH))))
    parser.add_argument("--collection", default=os.environ.get("CHROMA_VISUAL_COLLECTION", DEFAULT_COLLECTION))
    parser.add_argument("--embedding-cache", type=Path, default=DEFAULT_EMBEDDING_CACHE)
    parser.add_argument("--no-embedding-cache", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    apply_env_file(args.env_file)
    all_rows = build_rows(args)
    write_manifest(all_rows, args.manifest_jsonl, args.report_md)
    rows = all_rows[args.offset :]
    if args.limit:
        rows = rows[: args.limit]
    print(f"manifest_items={len(all_rows)} ingest_items={len(rows)} offset={args.offset} limit={args.limit}", flush=True)
    if not args.manifest_only:
        ingest(args, rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
