#!/usr/bin/env python
"""Ingest selected visual blocks from the fretboard handbook into Chroma."""

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


DEFAULT_BOOK_DIR = Path(
    "data/processed/mineru_full_gpu/"
    "吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)/ocr"
)
DEFAULT_CONTENT_LIST = DEFAULT_BOOK_DIR / "吉他指板手册 by （美）巴雷特·塔利亚里诺著；刘洋，刘刚译 (z-lib.org)_content_list.json"
DEFAULT_OUTPUT_DIR = Path("data/processed/fretboard_handbook/visual_layer")
DEFAULT_CHROMA_PATH = Path("data/chroma")
DEFAULT_COLLECTION = "guitar_visual_chunks"
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
    def __init__(self) -> None:
        self.api_url = os.environ.get("MULTIMODAL_EMBEDDING_API_URL", DEFAULT_API_URL)
        self.api_key = os.environ.get("VL_EMBEDDING_API_KEY") or os.environ.get("LLM_API_KEY", "")
        self.model = os.environ.get("VL_EMBEDDING_MODEL", "qwen3-vl-embedding")
        self.dimensions = int(os.environ.get("VL_EMBEDDING_DIMENSIONS", "1024") or 1024)
        self.timeout = int(os.environ.get("VL_EMBEDDING_TIMEOUT_SECONDS", "120"))
        self.max_retries = int(os.environ.get("VL_EMBEDDING_MAX_RETRIES", "2"))
        if not self.api_key:
            raise ValueError("Set VL_EMBEDDING_API_KEY or LLM_API_KEY in .env")

    def embed_image(self, path: Path) -> list[float]:
        return self.embed_images([path])[0]

    def embed_images(self, paths: list[Path]) -> list[list[float]]:
        payload = {
            "model": self.model,
            "input": {"contents": [{"image": image_data_uri(path)} for path in paths]},
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
                if len(embeddings) != len(paths):
                    raise ValueError(f"Expected {len(paths)} embeddings, got {len(embeddings)}")
                return embeddings
            except (urllib.error.URLError, urllib.error.HTTPError, KeyError, ValueError, json.JSONDecodeError) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(1.5 * (attempt + 1))
        raise RuntimeError(f"qwen3-vl-embedding request failed: {last_error}")


def parse_pages(value: str) -> set[int]:
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


def priority_for_page(page: int) -> str:
    if page == 14:
        return "P0_root_fingering_forms"
    if 35 <= page <= 40:
        return "P1_scales_intervals"
    if 45 <= page <= 62:
        return "P2_arpeggios_chords"
    if 67 <= page <= 69:
        return "P3_common_scales_chords"
    if 72 <= page <= 82:
        return "P4_answers"
    return "other"


def text_items_by_page(items: list[dict[str, Any]]) -> dict[int, list[dict[str, Any]]]:
    by_page: dict[int, list[dict[str, Any]]] = {}
    for item in items:
        if "text" not in item:
            continue
        page = int(item.get("page_idx", -1)) + 1
        by_page.setdefault(page, []).append(item)
    return by_page


def page_context(text_items: list[dict[str, Any]], image_bbox: list[int]) -> tuple[str, str]:
    titles: list[str] = []
    nearby: list[tuple[int, str]] = []
    image_y = int(image_bbox[1]) if image_bbox else 0
    for item in text_items:
        text = str(item.get("text", "")).strip()
        if not text:
            continue
        bbox = item.get("bbox") or [0, 0, 0, 0]
        y = int(bbox[1]) if len(bbox) > 1 else 0
        if item.get("text_level") or text.startswith("第") or text.startswith("练习"):
            titles.append(text[:80])
        nearby.append((abs(y - image_y), text[:160]))
    nearby_text = " | ".join(text for _, text in sorted(nearby)[:4])
    title_text = " | ".join(titles[:5])
    return title_text, nearby_text


def build_manifest(args: argparse.Namespace) -> list[dict[str, Any]]:
    items = json.loads(args.content_list.read_text(encoding="utf-8"))
    image_root = args.book_dir / "images"
    text_by_page = text_items_by_page(items)
    selected_pages = parse_pages(args.pages)
    rows: list[dict[str, Any]] = []
    for item in items:
        if item.get("type") != "image":
            continue
        page = int(item.get("page_idx", -1)) + 1
        if page not in selected_pages:
            continue
        rel_path = str(item.get("img_path", ""))
        image_path = args.book_dir / rel_path
        if not image_path.exists():
            continue
        title_text, nearby_text = page_context(text_by_page.get(page, []), item.get("bbox") or [])
        rows.append(
            {
                "visual_id": f"fretboard_handbook:p{page:03d}:{image_path.stem}",
                "source_id": "fretboard_handbook_mineru",
                "source_title": "吉他指板手册",
                "source_type": "mineru_image_block",
                "priority": priority_for_page(page),
                "page": page,
                "page_idx": page - 1,
                "image_path": str(image_path),
                "image_name": image_path.name,
                "bbox": item.get("bbox") or [],
                "style_tags": ["fretboard", "guitar_foundation"],
                "topic_hint": title_text,
                "nearby_text": nearby_text,
            }
        )
    return rows


def write_manifest(output_dir: Path, rows: list[dict[str, Any]]) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = output_dir / "fretboard_visual_manifest.jsonl"
    md_path = output_dir / "fretboard_visual_manifest.md"
    with jsonl_path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    lines = [
        "# Fretboard Handbook Visual Manifest",
        "",
        f"- visual blocks: {len(rows)}",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {row['visual_id']}",
                "",
                f"- priority: `{row['priority']}`",
                f"- page: `{row['page']}`",
                f"- image: `{row['image_path']}`",
                f"- topic_hint: {row['topic_hint']}",
                f"- nearby_text: {row['nearby_text']}",
                "",
            ]
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return jsonl_path, md_path


def metadata_value(value: Any) -> str | int | float | bool:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return value
    return json.dumps(value, ensure_ascii=False)


def batched(items: list[dict[str, Any]], size: int) -> list[list[dict[str, Any]]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def ingest_visuals(args: argparse.Namespace, rows: list[dict[str, Any]]) -> None:
    try:
        import chromadb
    except ImportError as exc:
        raise RuntimeError("Missing dependency: install chromadb first") from exc

    client = chromadb.PersistentClient(path=str(args.chroma_path))
    collection = client.get_or_create_collection(name=args.collection, metadata={"hnsw:space": "cosine"})
    embedder = QwenVLEmbedder()

    done = 0
    for batch in batched(rows, args.batch_size):
        image_paths = [Path(row["image_path"]) for row in batch]
        embeddings = embedder.embed_images(image_paths)
        ids: list[str] = []
        documents: list[str] = []
        metadatas: list[dict[str, Any]] = []
        for row, vector in zip(batch, embeddings):
            document = " | ".join(
                part
                for part in [
                    row.get("source_title", ""),
                    row.get("priority", ""),
                    f"page {row.get('page')}",
                    row.get("topic_hint", ""),
                    row.get("nearby_text", ""),
                ]
                if part
            )
            metadata = dict(row)
            metadata["embedding_model"] = embedder.model
            metadata["embedding_dimensions"] = len(vector)
            ids.append(row["visual_id"])
            documents.append(document)
            metadatas.append({key: metadata_value(value) for key, value in metadata.items()})
        collection.upsert(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)
        done += len(batch)
        print(f"embedded/upserted {done}/{len(rows)}")

    print(
        json.dumps(
            {
                "collection": args.collection,
                "collection_count": collection.count(),
                "ingested": len(rows),
                "chroma_path": str(args.chroma_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    parser.add_argument("--book-dir", type=Path, default=DEFAULT_BOOK_DIR)
    parser.add_argument("--content-list", type=Path, default=DEFAULT_CONTENT_LIST)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--pages", default="14,35-40,45-62,67-69")
    parser.add_argument("--priority", action="append", default=[])
    parser.add_argument("--max-images", type=int, default=0)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--manifest-only", action="store_true")
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--chroma-path", type=Path, default=DEFAULT_CHROMA_PATH)
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    args = parser.parse_args(argv)
    apply_env_file(args.env_file)
    args.chroma_path = Path(os.environ.get("CHROMA_PATH", str(args.chroma_path)))
    args.collection = os.environ.get("CHROMA_VISUAL_COLLECTION", args.collection)
    return args


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    rows = build_manifest(args)
    if args.priority:
        allowed = set(args.priority)
        rows = [row for row in rows if row["priority"] in allowed]
    if args.offset:
        rows = rows[args.offset :]
    if args.limit:
        rows = rows[: args.limit]
    elif args.max_images:
        rows = rows[: args.max_images]
    jsonl_path, md_path = write_manifest(args.output_dir, rows)
    print(json.dumps({"manifest_jsonl": str(jsonl_path), "manifest_md": str(md_path), "rows": len(rows)}, ensure_ascii=False, indent=2))
    if not args.manifest_only:
        ingest_visuals(args, rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
