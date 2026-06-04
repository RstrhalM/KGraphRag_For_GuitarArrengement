#!/usr/bin/env python
"""Clean MinerU OCR blocks with rules and an optional OpenAI-compatible LLM.

The script keeps raw OCR text, cleaned text, edits, page metadata, and image
references so downstream KG ingestion can stay traceable.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


TEXT_TYPES = {"text"}
IMAGE_TYPES = {"image"}
SKIP_TYPES = {"page_number"}


DEFAULT_RULES_FILE = Path("config/ocr_cleaning_rules.json")


SYSTEM_PROMPT = """你是一个中文音乐教材 OCR 清洗器。

任务：在不改写原意、不扩写内容的前提下，纠正明显 OCR 错字、漏字、断句和标点问题。

约束：
1. 不要总结，不要润色成新文风。
2. 只修正根据上下文能确定的错误。
3. 音乐术语要保守修正，例如：音阶、琶音、音程、和弦、品位、琴弦、指板、节拍器。
4. 不要删除题号、练习编号、音名、弦号、品位编号。
5. 如果无法确定，保留原文并设置 needs_review=true。
6. 只返回 JSON，不要返回 Markdown 或解释文字。

JSON 格式：
{
  "clean_text": "清洗后的文本",
  "edits": [
    {"from": "原片段", "to": "新片段", "reason": "简短原因"}
  ],
  "confidence": 0.0,
  "needs_review": false
}
"""


RULE_SUGGESTION_PROMPT = """你是中文音乐教材 OCR 规则审校员。

任务：阅读一批 OCR 文本块、规则预清洗结果、附近文本，提出“可复用的 OCR 清洗规则”候选。

你不是在逐段润色，而是在发现可以沉淀到规则层的高频、低风险修正规则。

规则要求：
1. 不要为简单中文错字、漏字、普通短语补全提出规则；这些由中文原生 LLM 在清洗阶段直接处理。
2. 只建议可复用、保守、低幻觉风险的规则。
3. 优先结构类、格式类、版面伪影类规则，例如页眉页脚、异常列表符号、练习编号格式、图注格式、反复出现的扫描噪声。
4. 音乐术语规则只有在跨多页稳定出现、且误伤风险很低时才建议。
5. 不要建议会误伤正常文本的宽泛规则，例如把所有“动。”替换成“动力。”。
6. 如果规则只适合很窄上下文，请把 risk 设为 medium 或 high，并写清楚 scope_note。
7. from 必须是 OCR 或预清洗文本中真实出现过的片段。
8. 只返回 JSON。

JSON 格式：
{
  "candidate_rules": [
    {
      "type": "literal",
      "from": "OCR片段",
      "to": "修正片段",
      "reason": "为什么建议这条规则",
      "confidence": 0.0,
      "risk": "low",
      "examples": ["p0001_b001"],
      "scope_note": "适用范围"
    }
  ],
  "notes": ["整体观察"]
}
"""


def read_env(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        env[key.strip()] = value
    return env


def apply_env_file(path: Path) -> None:
    for key, value in read_env(path).items():
        os.environ.setdefault(key, value)


def normalize_whitespace(text: str) -> str:
    text = text.replace("\u3000", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_rules(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    rules = data.get("rules", [])
    if not isinstance(rules, list):
        raise ValueError(f"{path} must contain a 'rules' list")
    return [rule for rule in rules if rule.get("enabled", True)]


def rule_clean(text: str, rules: list[dict[str, Any]]) -> tuple[str, list[dict[str, str]]]:
    clean = normalize_whitespace(text)
    edits: list[dict[str, str]] = []
    for rule in rules:
        rule_type = rule.get("type", "literal")
        src = str(rule.get("from", ""))
        dst = str(rule.get("to", ""))
        if not src:
            continue
        before = clean
        if rule_type == "literal":
            clean = clean.replace(src, dst)
        elif rule_type == "regex":
            clean = re.sub(src, dst, clean)
        else:
            continue
        if clean != before:
            edits.append(
                {
                    "from": src,
                    "to": dst,
                    "reason": str(rule.get("reason", "rule")),
                    "rule_id": str(rule.get("id", "")),
                    "rule_type": str(rule_type),
                }
            )
    return clean, edits


def extract_json_object(text: str) -> dict[str, Any]:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError("LLM response did not contain a JSON object")
    return json.loads(match.group(0))


class LLMClient:
    def __init__(self) -> None:
        self.base_url = os.environ.get("LLM_API_BASE_URL", "").rstrip("/")
        self.api_key = os.environ.get("LLM_API_KEY", "")
        self.model = os.environ.get("LLM_MODEL", "")
        self.temperature = float(os.environ.get("LLM_TEMPERATURE", "0"))
        self.timeout = int(os.environ.get("LLM_TIMEOUT_SECONDS", "60"))
        self.max_retries = int(os.environ.get("LLM_MAX_RETRIES", "2"))
        if not self.base_url or not self.model:
            raise ValueError("LLM_API_BASE_URL and LLM_MODEL must be set in .env")

    def chat_json(self, *, system_prompt: str, user_payload: dict[str, Any]) -> dict[str, Any]:
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": json.dumps(user_payload, ensure_ascii=False),
                },
            ],
        }
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers = {"Content-Type": "application/json; charset=utf-8"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        url = f"{self.base_url}/chat/completions"
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                req = urllib.request.Request(url, data=body, headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                content = data["choices"][0]["message"]["content"]
                return extract_json_object(content)
            except (urllib.error.URLError, urllib.error.HTTPError, ValueError, KeyError, json.JSONDecodeError) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(1.5 * (attempt + 1))
                else:
                    break
        raise RuntimeError(f"LLM request failed: {last_error}")

    def clean_text(
        self,
        *,
        block: dict[str, Any],
        preclean_text: str,
        nearby_text: list[str],
    ) -> dict[str, Any]:
        user_payload = {
            "block_id": block["block_id"],
            "page": block["page"],
            "block_type": block["type"],
            "ocr_text": block.get("ocr_text", ""),
            "rule_preclean_text": preclean_text,
            "nearby_text": nearby_text,
        }
        parsed = self.chat_json(system_prompt=SYSTEM_PROMPT, user_payload=user_payload)
        return validate_llm_result(parsed, fallback=preclean_text)


def validate_llm_result(result: dict[str, Any], fallback: str) -> dict[str, Any]:
    clean_text = str(result.get("clean_text") or fallback).strip()
    edits = result.get("edits", [])
    if not isinstance(edits, list):
        edits = []
    try:
        confidence = float(result.get("confidence", 0.5))
    except (TypeError, ValueError):
        confidence = 0.5
    confidence = max(0.0, min(1.0, confidence))
    return {
        "clean_text": clean_text,
        "edits": edits,
        "confidence": confidence,
        "needs_review": bool(result.get("needs_review", confidence < 0.75)),
    }


def validate_candidate_rules(result: dict[str, Any]) -> dict[str, Any]:
    candidates = result.get("candidate_rules", [])
    if not isinstance(candidates, list):
        candidates = []

    clean_candidates: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for index, rule in enumerate(candidates, start=1):
        if not isinstance(rule, dict):
            continue
        rule_type = str(rule.get("type", "literal"))
        src = str(rule.get("from", "")).strip()
        dst = str(rule.get("to", "")).strip()
        if rule_type not in {"literal", "regex"} or not src or not dst or src == dst:
            continue
        key = (rule_type, src, dst)
        if key in seen:
            continue
        seen.add(key)
        try:
            confidence = float(rule.get("confidence", 0.5))
        except (TypeError, ValueError):
            confidence = 0.5
        confidence = max(0.0, min(1.0, confidence))
        risk = str(rule.get("risk", "medium")).lower()
        if risk not in {"low", "medium", "high"}:
            risk = "medium"
        examples = rule.get("examples", [])
        if not isinstance(examples, list):
            examples = []
        clean_candidates.append(
            {
                "id": f"llm_candidate_{index:03d}",
                "enabled": False,
                "type": rule_type,
                "from": src,
                "to": dst,
                "reason": str(rule.get("reason", "")),
                "confidence": confidence,
                "risk": risk,
                "examples": [str(example) for example in examples],
                "scope_note": str(rule.get("scope_note", "")),
                "review_status": "pending",
            }
        )

    notes = result.get("notes", [])
    if not isinstance(notes, list):
        notes = []
    return {"candidate_rules": clean_candidates, "notes": [str(note) for note in notes]}


def find_nearby_text(items: list[dict[str, Any]], index: int, window: int = 2) -> list[str]:
    current_page = items[index].get("page_idx")
    nearby: list[str] = []
    for pos in range(max(0, index - window), min(len(items), index + window + 1)):
        if pos == index:
            continue
        item = items[pos]
        if item.get("page_idx") != current_page:
            continue
        text = item.get("text")
        if isinstance(text, str) and text.strip():
            nearby.append(text.strip())
    return nearby


def block_id_for(page: int, seq: int) -> str:
    return f"p{page:04d}_b{seq:03d}"


def load_content_list(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON list")
    return data


def build_rule_suggestion_samples(
    items: list[dict[str, Any]],
    *,
    source_page_offset: int,
    rules: list[dict[str, Any]],
    max_blocks: int,
) -> list[dict[str, Any]]:
    samples: list[dict[str, Any]] = []
    page_counts: dict[int, int] = {}
    for index, item in enumerate(items):
        item_type = item.get("type", "unknown")
        raw_page_idx = int(item.get("page_idx", 0))
        page = raw_page_idx + 1 + source_page_offset
        page_counts[page] = page_counts.get(page, 0) + 1
        if item_type not in TEXT_TYPES and not isinstance(item.get("text"), str):
            continue
        ocr_text = str(item.get("text", "")).strip()
        if not ocr_text:
            continue
        preclean, edits = rule_clean(ocr_text, rules)
        samples.append(
            {
                "block_id": block_id_for(page, page_counts[page]),
                "page": page,
                "type": item_type,
                "text_level": item.get("text_level"),
                "ocr_text": ocr_text,
                "rule_preclean_text": preclean,
                "rule_edits": edits,
                "nearby_text": find_nearby_text(items, index),
            }
        )
        if len(samples) >= max_blocks:
            break
    return samples


def suggest_rules_with_llm(
    *,
    items: list[dict[str, Any]],
    rules: list[dict[str, Any]],
    args: argparse.Namespace,
) -> dict[str, Any]:
    client = LLMClient()
    samples = build_rule_suggestion_samples(
        items,
        source_page_offset=args.source_page_offset,
        rules=rules,
        max_blocks=args.max_suggest_blocks,
    )
    existing_rules = [
        {
            "id": rule.get("id"),
            "type": rule.get("type", "literal"),
            "from": rule.get("from"),
            "to": rule.get("to"),
            "reason": rule.get("reason"),
        }
        for rule in rules
    ]
    payload = {
        "domain": "中文吉他教材 OCR",
        "existing_rules": existing_rules,
        "samples": samples,
        "instructions": "请只提出可沉淀为规则层的候选规则，不要做逐段清洗。",
    }
    raw = client.chat_json(system_prompt=RULE_SUGGESTION_PROMPT, user_payload=payload)
    validated = validate_candidate_rules(raw)
    validated["source"] = {
        "input": str(args.input),
        "rules_file": str(args.rules_file),
        "sample_blocks": len(samples),
        "source_page_offset": args.source_page_offset,
    }
    return validated


def convert_blocks(
    items: list[dict[str, Any]],
    *,
    source_page_offset: int,
    use_llm: bool,
    include_page_numbers: bool,
    rules: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    client = LLMClient() if use_llm else None
    page_counts: dict[int, int] = {}
    blocks: list[dict[str, Any]] = []

    for index, item in enumerate(items):
        item_type = item.get("type", "unknown")
        raw_page_idx = int(item.get("page_idx", 0))
        page = raw_page_idx + 1 + source_page_offset
        page_counts[page] = page_counts.get(page, 0) + 1

        if item_type in SKIP_TYPES and not include_page_numbers:
            continue

        block: dict[str, Any] = {
            "block_id": block_id_for(page, page_counts[page]),
            "type": item_type,
            "page": page,
            "mineru_page_idx": raw_page_idx,
            "bbox": item.get("bbox"),
            "raw": item,
        }

        if item_type in TEXT_TYPES or isinstance(item.get("text"), str):
            ocr_text = str(item.get("text", ""))
            preclean, rule_edits = rule_clean(ocr_text, rules)
            block["ocr_text"] = ocr_text
            block["rule_preclean_text"] = preclean
            block["rule_edits"] = rule_edits
            block["text_level"] = item.get("text_level")

            if client:
                llm_result = client.clean_text(
                    block=block,
                    preclean_text=preclean,
                    nearby_text=find_nearby_text(items, index),
                )
                block.update(llm_result)
                block["cleaning_method"] = "rules+llm"
            else:
                block["clean_text"] = preclean
                block["edits"] = rule_edits
                block["confidence"] = 0.65 if rule_edits else 0.55
                block["needs_review"] = False
                block["cleaning_method"] = "rules"

        elif item_type in IMAGE_TYPES:
            block["image_path"] = item.get("img_path") or item.get("image_path")
            block["img_caption"] = item.get("img_caption")
            block["cleaning_method"] = "passthrough"
            block["confidence"] = 1.0
            block["needs_review"] = False

        else:
            block["cleaning_method"] = "passthrough"
            block["confidence"] = 0.5
            block["needs_review"] = True

        blocks.append(block)

    return blocks


def write_jsonl(path: Path, blocks: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for block in blocks:
            fh.write(json.dumps(block, ensure_ascii=False) + "\n")


def copy_image_assets(blocks: list[dict[str, Any]], source_dir: Path, output_dir: Path) -> None:
    for block in blocks:
        image_path = block.get("image_path")
        if not image_path:
            continue
        src = Path(str(image_path))
        if not src.is_absolute():
            src = source_dir / src
        if not src.exists():
            block["asset_copy_error"] = f"missing source image: {src}"
            block["needs_review"] = True
            continue
        rel = Path(str(image_path)) if not Path(str(image_path)).is_absolute() else Path("images") / src.name
        dst = output_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        block["markdown_image_path"] = rel.as_posix()


def write_markdown(path: Path, blocks: list[dict[str, Any]]) -> None:
    lines: list[str] = []
    current_page: int | None = None
    for block in blocks:
        page = int(block["page"])
        if current_page != page:
            current_page = page
            lines.append(f"\n\n<!-- page: {page} -->\n")

        if block.get("clean_text") is not None:
            text = str(block["clean_text"]).strip()
            if not text:
                continue
            level = block.get("text_level")
            if isinstance(level, int) and level > 0:
                heading_level = min(max(level, 1), 6)
                lines.append(f"{'#' * heading_level} {text}\n")
            else:
                lines.append(f"{text}\n")
        elif block.get("type") == "image" and (block.get("markdown_image_path") or block.get("image_path")):
            image_path = block.get("markdown_image_path") or block.get("image_path")
            lines.append(f"![]({image_path})\n")

    path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def write_report(path: Path, blocks: list[dict[str, Any]], args: argparse.Namespace) -> None:
    by_type: dict[str, int] = {}
    review_count = 0
    edit_count = 0
    for block in blocks:
        by_type[block["type"]] = by_type.get(block["type"], 0) + 1
        review_count += int(bool(block.get("needs_review")))
        edit_count += len(block.get("edits") or [])

    report = {
        "input": str(args.input),
        "output_dir": str(args.output_dir),
        "use_llm": args.use_llm,
        "rules_file": str(args.rules_file),
        "source_page_offset": args.source_page_offset,
        "blocks": len(blocks),
        "by_type": by_type,
        "needs_review": review_count,
        "edit_count": edit_count,
    }
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-i", "--input", type=Path, required=True, help="MinerU *_content_list.json")
    parser.add_argument("-o", "--output-dir", type=Path, required=True, help="Output directory")
    parser.add_argument("--env-file", type=Path, default=Path(".env"), help="Path to .env")
    parser.add_argument("--rules-file", type=Path, default=DEFAULT_RULES_FILE, help="JSON rule file")
    parser.add_argument("--use-llm", action="store_true", help="Call OpenAI-compatible LLM API")
    parser.add_argument(
        "--suggest-rules",
        action="store_true",
        help="Ask the LLM to propose candidate cleaning rules instead of cleaning the document",
    )
    parser.add_argument(
        "--max-suggest-blocks",
        type=int,
        default=40,
        help="Maximum text blocks sent to the LLM in --suggest-rules mode",
    )
    parser.add_argument(
        "--source-page-offset",
        type=int,
        default=0,
        help="Offset added to MinerU zero-based page_idx when creating source page numbers. Use 8 if MinerU parsed -s 8.",
    )
    parser.add_argument("--include-page-numbers", action="store_true", help="Keep MinerU page_number blocks")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    apply_env_file(args.env_file)
    items = load_content_list(args.input)
    rules = load_rules(args.rules_file)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.suggest_rules:
        suggestions = suggest_rules_with_llm(items=items, rules=rules, args=args)
        output_path = args.output_dir / "suggested_rules.json"
        output_path.write_text(json.dumps(suggestions, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {len(suggestions['candidate_rules'])} candidate rules to {output_path}")
        return 0

    blocks = convert_blocks(
        items,
        source_page_offset=args.source_page_offset,
        use_llm=args.use_llm,
        include_page_numbers=args.include_page_numbers,
        rules=rules,
    )

    copy_image_assets(blocks, args.input.parent, args.output_dir)
    write_jsonl(args.output_dir / "clean_blocks.jsonl", blocks)
    write_markdown(args.output_dir / "clean.md", blocks)
    write_report(args.output_dir / "clean_report.json", blocks, args)

    print(f"Wrote {len(blocks)} blocks to {args.output_dir}")
    print(f"Review blocks: {sum(1 for b in blocks if b.get('needs_review'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
