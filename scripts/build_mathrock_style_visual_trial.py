from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "data" / "processed" / "mathrock" / "pdf_page_images"
OUTPUT_ROOT = ROOT / "data" / "processed" / "mathrock" / "style_visual_caption_trial" / "batch_001_visual_crops"


ITEMS = [
    {
        "visual_id": "mr_style_001_fmaj9",
        "parent_visual_id": "mr_style_001",
        "page": 33,
        "bbox": [175, 220, 397, 500],
        "visual_type": "chord_shape",
        "tuning": "FACGCE",
        "canonical_chord": "Fmaj9",
        "known_techniques": ["open_string", "voicing"],
        "target": "FACGCE 调弦中的 Fmaj9 和弦指型",
        "caption_goal": "基于 FACGCE 调弦，独立识别 Fmaj9 指型的开放弦、按弦位置和编配用途。",
        "review_status": "accepted",
        "decision": "accept",
    },
    {
        "visual_id": "mr_style_001_g7",
        "parent_visual_id": "mr_style_001",
        "page": 33,
        "bbox": [400, 220, 625, 500],
        "visual_type": "chord_shape",
        "tuning": "FACGCE",
        "canonical_chord": "G7",
        "known_techniques": ["mute", "open_string", "voicing"],
        "target": "FACGCE 调弦中的 G7 和弦指型",
        "caption_goal": "基于 FACGCE 调弦，独立识别 G7 指型的开放弦、闷弦、按弦位置和编配用途。",
        "review_status": "accepted",
        "decision": "accept",
    },
    {
        "visual_id": "mr_style_001_am",
        "parent_visual_id": "mr_style_001",
        "page": 33,
        "bbox": [630, 220, 870, 500],
        "visual_type": "chord_shape",
        "tuning": "FACGCE",
        "canonical_chord": "Am",
        "known_techniques": ["mute", "open_string", "voicing"],
        "target": "FACGCE 调弦中的 Am 和弦指型",
        "caption_goal": "基于 FACGCE 调弦，独立识别 Am 指型的闷弦、按弦位置和编配用途。",
        "review_status": "accepted",
        "decision": "accept",
    },
    {
        "visual_id": "mr_style_001_am_add11",
        "parent_visual_id": "mr_style_001",
        "page": 33,
        "bbox": [865, 220, 1095, 500],
        "visual_type": "chord_shape",
        "tuning": "FACGCE",
        "canonical_chord": "Am(add11)",
        "known_techniques": ["mute", "open_string", "extended_chord_voicing"],
        "source_label": "Am+11",
        "target": "FACGCE 调弦中的 Am(add11) 和弦指型",
        "caption_goal": "基于 FACGCE 调弦，独立识别 Am(add11) 指型的开放弦、按弦位置和延伸音效果。",
        "review_status": "accepted",
        "decision": "accept",
    },
    {
        "visual_id": "mr_style_001_bm7b5",
        "parent_visual_id": "mr_style_001",
        "page": 33,
        "bbox": [1098, 220, 1315, 500],
        "visual_type": "chord_shape",
        "tuning": "FACGCE",
        "canonical_chord": "Bm7b5",
        "known_techniques": ["movable_voicing", "half_diminished_voicing"],
        "target": "FACGCE 调弦中的 Bm7b5 和弦指型",
        "caption_goal": "基于 FACGCE 调弦，独立识别 Bm7b5 指型的把位、按弦位置和半减七和声功能。",
        "review_status": "accepted",
        "decision": "accept",
    },
    {
        "visual_id": "mr_style_002",
        "page": 34,
        "bbox": [170, 540, 1325, 1685],
        "visual_type": "scale_pattern",
        "tuning": "FACGCE",
        "known_scales": ["major"],
        "known_techniques": ["open_string", "tapping", "melodic_riff"],
        "target": "FACGCE 调弦的大调实用音符指板图及其点弦/旋律用途说明",
        "caption_goal": "描述特殊调弦音阶图中的开放弦、重复音和适合点弦 riff 的几何布局。",
        "review_status": "accepted",
        "decision": "accept",
    },
    {
        "visual_id": "mr_style_008",
        "page": 61,
        "bbox": [170, 650, 1280, 1125],
        "visual_type": "shell_voicing_group",
        "tuning": "standard",
        "canonical_chord": "G7",
        "known_techniques": ["shell_voicing", "mute", "voicing"],
        "target": "G7 属七和弦三种壳式按法",
        "caption_goal": "识别不同弦组/把位的 G7 shell voicing，并说明稀疏编配与增益音色价值。",
        "review_status": "accepted",
        "decision": "accept",
    },
    {
        "visual_id": "mr_style_010",
        "page": 73,
        "bbox": [175, 1030, 1320, 1285],
        "visual_type": "tapping_example",
        "tuning": "standard",
        "canonical_chord": "Cmaj7",
        "known_techniques": ["tapping", "pull_off", "let_ring", "open_string"],
        "target": "Cmaj7 点弦琶音谱例",
        "caption_goal": "读取点弦标记、开放弦/持续音、把位移动和乐句轮廓。",
        "review_status": "accepted",
        "decision": "accept",
    },
    {
        "visual_id": "mr_style_015",
        "page": 78,
        "bbox": [170, 465, 1320, 815],
        "visual_type": "riff_tab",
        "tuning": "standard",
        "canonical_chords": ["Cmaj7", "Fmaj7"],
        "known_techniques": ["rapid_chord_changes", "irregular_meter", "open_string", "voicing"],
        "known_meters": ["6/8", "9/8"],
        "target": "I-IV 和弦进行中的快速转换与 6/8、9/8 非常规节拍 riff",
        "caption_goal": "读取节拍变化、和弦转换和 Math Rock riff 的编配价值。",
        "review_status": "accepted",
        "decision": "accept",
    },
]


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def source_path(page: int) -> Path:
    return SOURCE_ROOT / f"mathrock_pdf_page_{page:03d}.jpg"


def build() -> list[dict]:
    crop_dir = OUTPUT_ROOT / "crops"
    annotated_dir = OUTPUT_ROOT / "annotated"
    crop_dir.mkdir(parents=True, exist_ok=True)
    annotated_dir.mkdir(parents=True, exist_ok=True)

    for obsolete_path in (
        crop_dir / "mr_style_001.png",
        annotated_dir / "mr_style_001_page_033.jpg",
    ):
        if obsolete_path.exists():
            obsolete_path.unlink()

    rows: list[dict] = []
    for item in ITEMS:
        image_path = source_path(item["page"])
        image = Image.open(image_path).convert("RGB")
        x1, y1, x2, y2 = item["bbox"]
        if not (0 <= x1 < x2 <= image.width and 0 <= y1 < y2 <= image.height):
            raise ValueError(f"Invalid bbox for {item['visual_id']}: {item['bbox']} on {image.size}")

        crop_path = crop_dir / f"{item['visual_id']}.png"
        image.crop((x1, y1, x2, y2)).save(crop_path)

        annotated = image.copy()
        draw = ImageDraw.Draw(annotated)
        draw.rectangle((x1, y1, x2, y2), outline=(220, 45, 45), width=6)
        annotated_path = annotated_dir / f"{item['visual_id']}_page_{item['page']:03d}.jpg"
        annotated.save(annotated_path, quality=90)

        rows.append(
            {
                **item,
                "source_image": relative(image_path),
                "source_size": [image.width, image.height],
                "crop_path": relative(crop_path),
                "annotated_path": relative(annotated_path),
                "review_status": item.get("review_status", "pending"),
                "decision": item.get("decision", ""),
                "notes": "",
            }
        )
    return rows


def write_outputs(rows: list[dict]) -> None:
    manifest_path = OUTPUT_ROOT / "style_visual_crop_manifest.jsonl"
    manifest_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )

    caption_candidates = []
    for row in rows:
        if row["decision"] != "accept":
            continue
        context_parts = [
            row["target"],
            row["caption_goal"],
            "教材章节语境：Math Rock 吉他编配与演奏。",
        ]
        if row.get("tuning"):
            context_parts.append(f"已确认调弦上下文：{row['tuning']}。")
        if row.get("canonical_chord"):
            context_parts.append(f"图示标题对应标准和弦名：{row['canonical_chord']}。")
        caption_candidates.append(
            {
                "visual_id": row["visual_id"],
                "source_id": "mathrock_pdf",
                "source_title": "Math Rock 吉他教材",
                "source_type": "manual_semantic_crop",
                "visual_role": "style_visual_evidence",
                "priority": "P1_mathrock_style_trial",
                "page": row["page"],
                "image_path": row["crop_path"],
                "style_tags": ["math_rock", "guitar_arrangement"],
                "topic_hint": row["target"],
                "nearby_text": " ".join(context_parts),
                "visual_granularity": "single_retrievable_unit",
                "image_type_hint": row["visual_type"],
                "crop_bbox": row["bbox"],
                "parent_visual_id": row.get("parent_visual_id"),
                "known_tuning": row.get("tuning"),
                "known_chord": row.get("canonical_chord"),
                "known_chords": row.get("canonical_chords") or ([row["canonical_chord"]] if row.get("canonical_chord") else []),
                "known_scales": row.get("known_scales") or [],
                "known_techniques": row.get("known_techniques") or [],
                "known_meters": row.get("known_meters") or [],
                "caption_status": "pending",
                "caption_decision": "",
            }
        )
    caption_candidates_path = OUTPUT_ROOT / "style_visual_caption_candidates.jsonl"
    caption_candidates_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in caption_candidates),
        encoding="utf-8",
    )

    lines = [
        "# Math Rock 风格视觉裁切首批审核",
        "",
        "说明：每张 crop 应是一个可独立召回的风格视觉证据。请重点检查是否保留必要标题、和弦名、调弦、节拍、TAB 和演奏标记，且没有混入相邻无关内容。",
        "",
        "- [ ] all accept",
        "",
    ]
    for row in rows:
        accepted = row["decision"] == "accept"
        crop_ref = Path(row["crop_path"]).relative_to(
            Path("data/processed/mathrock/style_visual_caption_trial/batch_001_visual_crops")
        )
        annotated_ref = Path(row["annotated_path"]).relative_to(
            Path("data/processed/mathrock/style_visual_caption_trial/batch_001_visual_crops")
        )
        lines.extend(
            [
                f"## {row['visual_id']} · P{row['page']} · {row['visual_type']}",
                "",
                f"- [{'x' if accepted else ' '}] accept",
                "- [ ] revise",
                "- [ ] reject",
                f"- 裁切目标：{row['target']}",
                f"- Caption 目标：{row['caption_goal']}",
                *(
                    [
                        f"- 父证据：`{row['parent_visual_id']}`",
                        f"- 调弦上下文：`{row['tuning']}`",
                        f"- 标准和弦名：`{row['canonical_chord']}`",
                    ]
                    if row.get("parent_visual_id")
                    else []
                ),
                f"- bbox：`{row['bbox']}`",
                f"- source：`{row['source_image']}`",
                "",
                "### Crop",
                "",
                f"![]({crop_ref.as_posix()})",
                "",
                "<details>",
                "<summary>查看整页 bbox</summary>",
                "",
                f"![]({annotated_ref.as_posix()})",
                "",
                "</details>",
                "",
                "审核备注：",
                "",
                "---",
                "",
            ]
        )
    (OUTPUT_ROOT / "style_visual_crop_review.md").write_text("\n".join(lines), encoding="utf-8")

    report = {
        "item_count": len(rows),
        "source_pages": sorted({row["page"] for row in rows}),
        "accepted_count": sum(row["decision"] == "accept" for row in rows),
        "pending_count": sum(row["review_status"] == "pending" for row in rows),
        "manifest": relative(manifest_path),
        "caption_candidates": relative(caption_candidates_path),
        "review_md": relative(OUTPUT_ROOT / "style_visual_crop_review.md"),
        "status": "crop_review_complete_caption_pending",
    }
    (OUTPUT_ROOT / "style_visual_crop_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    rows = build()
    write_outputs(rows)
    print(
        json.dumps(
            {
                "items": len(rows),
                "output": relative(OUTPUT_ROOT),
                "review": relative(OUTPUT_ROOT / "style_visual_crop_review.md"),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
