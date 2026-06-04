#!/usr/bin/env python
"""Build a Markdown plan for answer-image KG reprocessing coverage."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def image_name(path: str) -> str:
    return Path(path).name


def render_table(rows: list[dict[str, Any]], already_processed: set[str]) -> str:
    lines = [
        "| chunk | 练习编号 | 答案图 | 状态 | 建议 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        chunk_id = str(row.get("chunk_id", ""))
        exercises = ", ".join(str(x) for x in row.get("exercise_numbers", []))
        images = "<br>".join(image_name(x) for x in row.get("answer_images", []))
        skipped = row.get("skipped", [])
        if skipped:
            images += "<br>⚠ " + "<br>⚠ ".join(str(x) for x in skipped)
        if chunk_id in already_processed:
            status = "已补抽"
            advice = "等待/合并人工审核结果"
        elif row.get("answer_images"):
            status = "可补抽"
            advice = "用练习文字+答案图重跑，严格过滤纯答案"
        elif row.get("exercise_numbers"):
            status = "缺答案图"
            advice = "需要补图或跳过"
        else:
            status = "无练习编号"
            advice = "无需答案图补抽"
        lines.append(f"| `{chunk_id}` | {exercises or '-'} | {images or '-'} | {status} | {advice} |")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairings", type=Path, required=True, help="visual_answer_pairings.json")
    parser.add_argument("--processed-pairings", type=Path, action="append", default=[], help="Already processed pairings JSON")
    parser.add_argument("-o", "--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = load_json(args.pairings)
    already_processed: set[str] = set()
    for path in args.processed_pairings:
        if not path.exists():
            continue
        for row in load_json(path):
            already_processed.add(str(row.get("chunk_id", "")))

    covered_exercises: set[int] = set()
    missing_answer_exercises: set[int] = set()
    for row in rows:
        exercises = {int(x) for x in row.get("exercise_numbers", [])}
        if row.get("answer_images"):
            covered_exercises.update(exercises)
        else:
            missing_answer_exercises.update(exercises)
    missing_answer_exercises -= covered_exercises

    lines = [
        "# Visual Answer Integration Plan",
        "",
        "这份清单用于对照教材练习文字和你补充的答案图片，判断哪些 chunk 已经走过视觉补抽，哪些还可以补抽。",
        "",
        f"- chunk 数：{len(rows)}",
        f"- 已补抽 chunk：{', '.join(sorted(already_processed)) or '无'}",
        f"- 答案图覆盖练习数：{len(covered_exercises)}",
        f"- 仍缺答案图的练习编号：{', '.join(str(x) for x in sorted(missing_answer_exercises)) or '无'}",
        "",
        render_table(rows, already_processed),
        "",
        "建议：优先补抽 `可补抽` 且包含和弦 voicing、音程几何、指板位移、调式/音阶编配语境的 chunk；纯找音、填空、背诵练习由 prompt 丢弃即可。",
        "",
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"Wrote integration plan to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
