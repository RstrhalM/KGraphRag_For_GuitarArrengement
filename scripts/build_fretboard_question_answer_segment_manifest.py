from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TASK_ROOT = ROOT / "data" / "processed" / "fretboard_handbook" / "bbox_tasks"
ALIGNED_JSONL = (
    ROOT
    / "data"
    / "processed"
    / "fretboard_handbook"
    / "exercise_answer_aligned"
    / "fretboard_exercise_answer_aligned.jsonl"
)
OUTPUT_DIR = ROOT / "data" / "processed" / "fretboard_handbook" / "question_answer_segment_manifest"

ACCEPTED_ROW_RE = re.compile(r"\| \[x\] \| `(qseg_\d+)` \|")
NUMBERED_PROMPT_RE = re.compile(r"(?<!\d)(\d{1,2})\s*[）).．]\s*")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def compact_text(text: str, limit: int = 500) -> str:
    text = IMAGE_RE.sub("", text or "")
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "..."


def extract_subquestion_prompts(question_text: str) -> dict[str, str]:
    text = compact_text(question_text, limit=4000)
    matches = list(NUMBERED_PROMPT_RE.finditer(text))
    if len(matches) < 2:
        return {}

    prompts: dict[str, str] = {}
    for index, match in enumerate(matches):
        number = match.group(1)
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end].strip(" ;；,，")
        if body:
            prompts[number] = body
    return prompts


def accepted_item_ids(review_md: Path) -> set[str]:
    if not review_md.exists():
        return set()
    text = review_md.read_text(encoding="utf-8")
    return set(ACCEPTED_ROW_RE.findall(text))


def segment_sort_key(row: dict[str, Any]) -> tuple[int, int, int, str]:
    sub = row["subquestion_number"]
    try:
        sub_num = int(sub)
    except (TypeError, ValueError):
        sub_num = 0
    return int(row["exercise_number"]), sub_num, int(row.get("part_index") or 1), row["segment_id"]


def build() -> dict[str, Any]:
    exercise_rows = {row["exercise_number"]: row for row in read_jsonl(ALIGNED_JSONL)}
    subquestion_prompts = {
        number: extract_subquestion_prompts(row.get("question_text", ""))
        for number, row in exercise_rows.items()
    }

    manifest_rows: list[dict[str, Any]] = []
    for segments_path in sorted(TASK_ROOT.glob("*/question_segments_v2/question_segments.json")):
        task_dir = segments_path.parent
        review_md = task_dir / "question_segment_review.md"
        accepted = accepted_item_ids(review_md)
        if not accepted:
            continue

        payload = json.loads(segments_path.read_text(encoding="utf-8"))
        task_id = payload["task_id"]
        for item in payload["items"]:
            if item["item_id"] not in accepted:
                continue

            exercise_number = int(item["exercise_number"])
            subquestion = str(item["subquestion_number"])
            part_index = int(item.get("part_index") or 1)
            exercise = exercise_rows.get(exercise_number, {})
            prompt = subquestion_prompts.get(exercise_number, {}).get(subquestion, "")
            mapping_method = "exercise_subquestion_number"
            if not prompt:
                prompt = compact_text(exercise.get("question_text", ""))
                mapping_method = "exercise_level_fallback"

            crop_path = task_dir / item["crop_path"]
            stable_suffix = f"E{exercise_number:02d}_{subquestion}"
            if part_index != 1:
                stable_suffix += f"_part{part_index}"

            manifest_rows.append(
                {
                    "segment_id": f"fretboard_answer_{stable_suffix}",
                    "source": "吉他指板手册",
                    "task_id": task_id,
                    "item_id": item["item_id"],
                    "exercise_id": exercise.get("exercise_id", f"fretboard_exercise_{exercise_number:02d}"),
                    "exercise_number": exercise_number,
                    "subquestion_number": item["subquestion_number"],
                    "part_index": part_index,
                    "evidence_type": item.get("evidence_type", "fretboard_diagram"),
                    "mapping_method": mapping_method,
                    "question_text": compact_text(exercise.get("question_text", "")),
                    "subquestion_prompt": prompt,
                    "answer_text": compact_text(exercise.get("answer_text", "")),
                    "crop_path": rel(crop_path),
                    "source_image": item.get("source_image", payload.get("image_path", "")),
                    "bbox": item["bbox"],
                    "review_status": "accepted",
                    "caption_status": "pending",
                    "notes": item.get("notes", ""),
                }
            )

    manifest_rows.sort(key=segment_sort_key)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_jsonl = OUTPUT_DIR / "fretboard_question_answer_segment_manifest.jsonl"
    manifest_json = OUTPUT_DIR / "fretboard_question_answer_segment_manifest.json"
    chunks_json = OUTPUT_DIR / "chunks.json"
    manifest_md = OUTPUT_DIR / "fretboard_question_answer_segment_manifest.md"
    report_md = OUTPUT_DIR / "fretboard_question_answer_segment_manifest_report.md"

    write_jsonl(manifest_jsonl, manifest_rows)
    manifest_json.write_text(json.dumps(manifest_rows, ensure_ascii=False, indent=2), encoding="utf-8")
    chunks = [
        {
            "chunk_id": row["segment_id"],
            "lesson_title": f"练习{row['exercise_number']} / 小题{row['subquestion_number']}",
            "page_hint": row["task_id"],
            "text": "\n\n".join(
                part
                for part in [
                    f"练习{row['exercise_number']} 小题{row['subquestion_number']}",
                    f"证据类型：{row['evidence_type']}",
                    f"映射方式：{row['mapping_method']}",
                    f"小题提示：{row['subquestion_prompt']}",
                    f"原题题干：{row['question_text']}",
                    f"参考答案：{row['answer_text']}",
                    f"答案裁切图：{row['crop_path']}",
                ]
                if part
            ),
            "image_refs": [row["crop_path"]],
            "segment_id": row["segment_id"],
            "exercise_number": row["exercise_number"],
            "subquestion_number": row["subquestion_number"],
            "evidence_type": row["evidence_type"],
            "mapping_method": row["mapping_method"],
            "crop_path": row["crop_path"],
            "source_image": row["source_image"],
            "bbox": row["bbox"],
        }
        for row in manifest_rows
    ]
    chunks_json.write_text(json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = [
        "# 指板手册答案图题目映射 Manifest",
        "",
        "说明：每一行代表一个已审核通过的题目级答案 crop。映射依据为答案图中的练习号/小题号，与 `exercise_answer_aligned` 中的原题干对齐。",
        "",
        "| segment_id | exercise | subquestion | evidence_type | mapping | crop | prompt |",
        "| --- | ---: | --- | --- | --- | --- | --- |",
    ]
    for row in manifest_rows:
        prompt = row["subquestion_prompt"].replace("|", "\\|")
        if len(prompt) > 90:
            prompt = prompt[:89].rstrip() + "..."
        md_lines.append(
            f"| `{row['segment_id']}` | {row['exercise_number']} | {row['subquestion_number']} | "
            f"{row['evidence_type']} | {row['mapping_method']} | `{row['crop_path']}` | {prompt} |"
        )
    manifest_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    by_type: dict[str, int] = {}
    fallback_count = 0
    for row in manifest_rows:
        by_type[row["evidence_type"]] = by_type.get(row["evidence_type"], 0) + 1
        if row["mapping_method"] == "exercise_level_fallback":
            fallback_count += 1

    report_lines = [
        "# 指板手册答案图题目映射构建报告",
        "",
        f"- manifest_jsonl: `{rel(manifest_jsonl)}`",
        f"- manifest_json: `{rel(manifest_json)}`",
        f"- chunks_json: `{rel(chunks_json)}`",
        f"- manifest_md: `{rel(manifest_md)}`",
        f"- accepted_segments: {len(manifest_rows)}",
        f"- exercise_level_fallback: {fallback_count}",
        "",
        "## Evidence Type",
        "",
        "| evidence_type | count |",
        "| --- | ---: |",
    ]
    for evidence_type, count in sorted(by_type.items()):
        report_lines.append(f"| {evidence_type} | {count} |")
    report_md.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    return {
        "manifest_jsonl": rel(manifest_jsonl),
        "manifest_json": rel(manifest_json),
        "chunks_json": rel(chunks_json),
        "manifest_md": rel(manifest_md),
        "report_md": rel(report_md),
        "accepted_segments": len(manifest_rows),
        "exercise_level_fallback": fallback_count,
        "evidence_type": by_type,
    }


def main() -> None:
    print(json.dumps(build(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
