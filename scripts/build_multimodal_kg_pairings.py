#!/usr/bin/env python
"""Build image pairings for multimodal KG supplement extraction."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def image_page_index(content_list: Path) -> dict[str, int]:
    mapping: dict[str, int] = {}
    for item in read_json(content_list):
        img_path = item.get("img_path")
        page_idx = item.get("page_idx")
        if img_path and isinstance(page_idx, int):
            mapping[str(img_path).replace("\\", "/")] = page_idx + 1
    return mapping


def full_page_index(manifest: Path) -> dict[int, Path]:
    index: dict[int, Path] = {}
    for row in read_jsonl(manifest):
        page = int(row.get("page", 0) or 0)
        path = Path(str(row.get("image_path", "")))
        if page > 0 and path.is_file():
            index[page] = path
    return index


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunks-json", type=Path, required=True)
    parser.add_argument("--content-list", type=Path, required=True)
    parser.add_argument("--full-page-manifest", type=Path, required=True)
    parser.add_argument("--book-dir", type=Path, required=True)
    parser.add_argument("--chunk-id", action="append", default=[])
    parser.add_argument("--max-images", type=int, default=5)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()

    chunks = read_json(args.chunks_json)
    selected = set(args.chunk_id)
    page_by_image = image_page_index(args.content_list)
    full_pages = full_page_index(args.full_page_manifest)

    pairings: list[dict[str, Any]] = []
    for chunk in chunks:
        chunk_id = str(chunk.get("chunk_id", ""))
        if selected and chunk_id not in selected:
            continue
        image_refs = [str(ref).replace("\\", "/") for ref in chunk.get("image_refs", []) or []]
        pages = [page_by_image[ref] for ref in image_refs if ref in page_by_image]
        page_counts = Counter(pages)
        sorted_pages = [page for page, _ in page_counts.most_common()]

        image_paths: list[Path] = []
        selected_pages: list[int] = []
        for page in sorted_pages:
            page_image = full_pages.get(page)
            if page_image and page_image not in image_paths:
                image_paths.append(page_image)
                selected_pages.append(page)
            if len(image_paths) >= args.max_images:
                break

        if len(image_paths) < args.max_images:
            for ref in image_refs:
                path = args.book_dir / ref
                if path.is_file() and path not in image_paths:
                    image_paths.append(path)
                if len(image_paths) >= args.max_images:
                    break

        pairings.append(
            {
                "chunk_id": chunk_id,
                "chars": len(str(chunk.get("text", ""))),
                "image_refs": len(image_refs),
                "page_counts": dict(sorted(page_counts.items())),
                "selected_pages": selected_pages,
                "image_paths": [str(path) for path in image_paths],
                "omitted_images": max(0, len(image_refs) - len(image_paths)),
                "selection_reason": "Prefer full-page images for dense visual context; fallback to MinerU image blocks.",
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(pairings, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"pairings": len(pairings), "output": str(args.output)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
