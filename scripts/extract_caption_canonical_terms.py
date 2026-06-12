#!/usr/bin/env python
"""Extract canonical music terms from existing visual-caption text.

This script does not send images. It sends already accepted caption text to the
configured LLM API and writes a reviewable sidecar JSONL/Markdown layer.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    ROOT
    / "data"
    / "processed"
    / "fretboard_handbook"
    / "question_answer_visual_caption_layer"
    / "fretboard_answer_visual_caption_accepted_all.jsonl"
)
DEFAULT_OUTPUT_DIR = (
    ROOT
    / "data"
    / "processed"
    / "fretboard_handbook"
    / "question_answer_visual_caption_canonical_trial"
)

SYSTEM_PROMPT = """你是吉他编曲 RAG 系统的乐理术语规范化器。

你的任务：读取已经由 VLM 生成并人工通过的教材视觉 caption 文本，将其中的中文、英文、符号化乐理表达标准化为 canonical_terms。

不要重新解释图片，不要扩展图中没有出现的信息，不要把不确定内容硬判定为确定事实。

canonical_terms 命名建议：
- key:g_minor, key:d_major
- root:g, root:ab
- scale:natural_minor, scale:major, scale:pentatonic_minor, mode:dorian
- chord_quality:maj7, chord_quality:m11, chord_quality:maj9_sharp11, chord_quality:dominant7_sharp9
- chord:c7_sharp9, chord:abm11
- interval:minor_3rd, interval:perfect_5th, interval:major_7th
- fret_region:low, fret_region:middle, fret_region:high
- visual_type:scale_pattern, visual_type:chord_diagram, visual_type:text_answer
- technique:tapping, technique:open_string, technique:voicing
- tuning:standard
- concept:caged, concept:root_form, concept:relative_major_minor

输出必须是合法 JSON，格式：
{
  "items": [
    {
      "visual_id": "原 visual_id",
      "canonical_terms": [],
      "aliases_detected": [{"surface": "原文词", "canonical": "canonical_term"}],
      "music_objects": [],
      "key_or_tonality": [],
      "roots": [],
      "chord_qualities": [],
      "scale_or_mode": [],
      "fretboard_constraints": [],
      "visual_type": "",
      "uncertainty_notes": [],
      "confidence": 0.0
    }
  ]
}
"""

ROOT_ALIASES = {
    "C": ["C", "do"],
    "C#": ["C#", "C♯", "Db", "D♭", "升C", "降D"],
    "D": ["D", "re"],
    "D#": ["D#", "D♯", "Eb", "E♭", "升D", "降E"],
    "E": ["E", "mi"],
    "F": ["F", "fa"],
    "F#": ["F#", "F♯", "Gb", "G♭", "升F", "降G"],
    "G": ["G", "sol"],
    "G#": ["G#", "G♯", "Ab", "A♭", "升G", "降A"],
    "A": ["A", "la"],
    "A#": ["A#", "A♯", "Bb", "B♭", "升A", "降B"],
    "B": ["B", "si"],
}
QUALITY_ALIASES = {
    "major": ["major", "maj", "大调", "大音阶"],
    "minor": ["minor", "min", "小调", "自然小调", "小音阶"],
    "pentatonic_major": ["major pentatonic", "大调五声", "大五声音阶"],
    "pentatonic_minor": ["minor pentatonic", "小调五声", "小五声音阶"],
}
CHORD_QUALITY_ALIASES = {
    "maj7": ["maj7", "major 7", "大七"],
    "m7": ["m7", "min7", "minor 7", "小七"],
    "m11": ["m11", "min11", "minor 11", "小十一"],
    "maj9_sharp11": ["maj9#11", "maj9 sharp 11", "大九升十一"],
    "dominant7_sharp9": ["7#9", "dominant 7 sharp 9", "属七升九"],
    "dominant7_flat9": ["7b9", "7♭9", "dominant 7 flat 9", "属七降九"],
    "dominant7": ["7", "dominant 7", "属七"],
    "13": ["13", "十三"],
    "11": ["11", "十一"],
    "maj9": ["maj9", "major 9", "大九"],
    "m7b5": ["m7b5", "m7♭5", "半减七", "half diminished"],
    "m_add11": ["m(add11)", "m+11", "minor add11", "小和弦加十一"],
}

TECHNIQUE_ALIASES = {
    "tapping": ["tapping", "点弦"],
    "pull_off": ["pull-off", "pull off", "勾弦"],
    "hammer_on": ["hammer-on", "hammer on", "击弦"],
    "let_ring": ["let ring", "持续音"],
    "open_string": ["open string", "open_strings", "开放弦", "空弦"],
    "shell_voicing": ["shell voicing", "壳式"],
    "voicing": ["voicing", "和弦配置", "声部配置"],
    "rapid_chord_changes": ["rapid_chord_changes", "快速转换", "快速切换"],
    "irregular_meter": ["irregular_meter", "非常规节拍", "不规则节拍", "变拍"],
}


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


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(row, dict):
                rows.append(row)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def compact(text: str, limit: int = 1600) -> str:
    text = "\n".join(line.strip() for line in str(text or "").splitlines() if line.strip())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        value = str(value).strip()
        if not value or value.lower() in seen:
            continue
        seen.add(value.lower())
        out.append(value)
    return out


def contains_alias(blob: str, alias: str) -> bool:
    if re.fullmatch(r"[A-G](?:#|b)?", alias, re.I):
        return re.search(rf"(?<![A-Za-z0-9]){re.escape(alias)}(?![A-Za-z0-9])", blob, re.I) is not None
    return alias.lower() in blob.lower()


def canonical_root_token(root: str) -> str:
    value = root.strip()
    if not value:
        return ""
    token = value[0].lower()
    accidental = value[1:]
    if accidental == "#":
        token += "_sharp"
    elif accidental.lower() == "b":
        token += "_flat"
    return token


def canonical_chord_parts(chord: str) -> tuple[str, str] | None:
    match = re.fullmatch(
        r"([A-G](?:#|b)?)(maj9#11|maj7#11|maj9|maj7|m\(add11\)|m\+11|m11|m7b5|m7|7#9|7b9|7|dim7|sus4|sus2|add9|6/9|m)",
        chord.strip(),
        flags=re.I,
    )
    if not match:
        return None
    quality_map = {
        "maj9#11": "maj9_sharp11",
        "maj7#11": "maj7_sharp11",
        "maj9": "maj9",
        "maj7": "maj7",
        "m(add11)": "m_add11",
        "m+11": "m_add11",
        "m11": "m11",
        "m7b5": "m7b5",
        "m7": "m7",
        "7#9": "dominant7_sharp9",
        "7b9": "dominant7_flat9",
        "7": "dominant7",
        "dim7": "dim7",
        "sus4": "sus4",
        "sus2": "sus2",
        "add9": "add9",
        "6/9": "6_9",
        "m": "minor",
    }
    return canonical_root_token(match.group(1)), quality_map[match.group(2).lower()]


def local_extract_trusted(source: dict[str, Any], trusted: dict[str, Any]) -> dict[str, Any]:
    terms: list[str] = []
    aliases: list[dict[str, str]] = []
    roots: list[str] = []
    chord_qualities: list[str] = []
    scales: list[str] = []

    tuning = str(trusted.get("tuning") or "").strip()
    if tuning:
        terms.append(f"tuning:{tuning.lower().replace('#', '_sharp').replace(' ', '')}")
    visual_type = str(trusted.get("visual_type") or source.get("visual_type") or "").strip()
    if visual_type:
        terms.append(f"visual_type:{visual_type}")
    visual_subtype = str(trusted.get("visual_subtype") or "").strip()
    if visual_subtype and visual_subtype != visual_type:
        terms.append(f"visual_subtype:{visual_subtype}")
    for style in trusted.get("style_tags") or []:
        token = str(style).strip().lower().replace(" ", "_")
        if token:
            terms.append(f"style:{token}")
    for chord in trusted.get("chords") or []:
        parsed = canonical_chord_parts(str(chord))
        if not parsed:
            continue
        root_token, quality = parsed
        chord_term = f"chord:{root_token}_{quality}"
        terms.extend([f"root:{root_token}", f"chord_quality:{quality}", chord_term])
        roots.append(root_token.replace("_sharp", "#").replace("_flat", "b").upper())
        chord_qualities.append(f"chord_quality:{quality}")
        aliases.append({"surface": str(chord), "canonical": chord_term})
    for scale in trusted.get("scales") or []:
        token = str(scale).strip().lower().replace(" ", "_")
        if token:
            term = f"scale:{token}"
            terms.append(term)
            scales.append(term)
    for technique in trusted.get("techniques") or []:
        token = str(technique).strip().lower().replace(" ", "_")
        if token:
            terms.append(f"technique:{token}")
    for meter in trusted.get("meters") or []:
        token = str(meter).strip().replace("/", "_")
        if token:
            terms.append(f"meter:{token}")
    return {
        "visual_id": source.get("visual_id"),
        "canonical_terms": unique(terms),
        "aliases_detected": aliases,
        "music_objects": unique([str(source.get("musical_object") or "")]),
        "key_or_tonality": [],
        "roots": unique(roots),
        "chord_qualities": unique(chord_qualities),
        "scale_or_mode": unique(scales),
        "fretboard_constraints": [],
        "visual_type": visual_type,
        "uncertainty_notes": ["trusted_manifest_whitelist"],
        "confidence": 1.0,
    }


def local_extract_item(source: dict[str, Any]) -> dict[str, Any]:
    trusted = source.get("trusted_facts")
    if isinstance(trusted, dict) and any(trusted.get(key) for key in ("tuning", "chords", "scales", "techniques", "meters")):
        return local_extract_trusted(source, trusted)
    blob = "\n".join(
        json.dumps(source.get(key), ensure_ascii=False) if isinstance(source.get(key), (dict, list)) else str(source.get(key) or "")
        for key in [
            "visual_type",
            "musical_object",
            "root",
            "key",
            "tuning",
            "quality_or_mode",
            "position_or_shape",
            "entities",
            "style_tags",
            "caption_text",
        ]
    )
    canonical_terms: list[str] = []
    aliases: list[dict[str, str]] = []
    keys: list[str] = []
    roots: list[str] = []
    chord_qualities: list[str] = []
    scales: list[str] = []
    constraints: list[str] = []

    explicit_root = str(source.get("root") or "").strip()
    if explicit_root and explicit_root.lower() not in {"unknown", "none", "未知"}:
        for root, alias_list in ROOT_ALIASES.items():
            if any(explicit_root.lower() == alias.lower() for alias in alias_list):
                roots.append(root)
                canonical_terms.append(f"root:{root.lower().replace('#', '_sharp')}")
                aliases.append({"surface": explicit_root, "canonical": f"root:{root.lower().replace('#', '_sharp')}"})
                break

    for root, alias_list in ROOT_ALIASES.items():
        for quality, quality_aliases in QUALITY_ALIASES.items():
            for root_alias in alias_list:
                for quality_alias in quality_aliases:
                    patterns = [f"{root_alias}{quality_alias}", f"{root_alias} {quality_alias}"]
                    if any(pattern.lower() in blob.lower() for pattern in patterns):
                        key_term = f"key:{root.lower().replace('#', '_sharp')}_{'major' if quality == 'major' else 'minor'}" if quality in {"major", "minor"} else f"scale:{root.lower().replace('#', '_sharp')}_{quality}"
                        keys.append(key_term)
                        roots.append(root)
                        canonical_terms.append(f"root:{root.lower().replace('#', '_sharp')}")
                        canonical_terms.append(key_term)
                        aliases.append({"surface": f"{root_alias}{quality_alias}", "canonical": key_term})
                        if quality.startswith("pentatonic"):
                            scales.append(f"scale:{quality}")
                        else:
                            scales.append(f"scale:{quality}")

    chord_quality_map = {
        "maj9#11": "maj9_sharp11",
        "maj7#11": "maj7_sharp11",
        "maj#11": "maj_sharp11",
        "maj9": "maj9",
        "maj7": "maj7",
        "m11": "m11",
        "min11": "m11",
        "mi11": "m11",
        "m7b5": "m7b5",
        "m(add11)": "m_add11",
        "m+11": "m_add11",
        "m7": "m7",
        "mi7": "m7",
        "min7": "m7",
        "7#9": "dominant7_sharp9",
        "7b9": "dominant7_flat9",
        "7": "dominant7",
        "dim7": "dim7",
        "sus4": "sus4",
        "sus2": "sus2",
        "add9": "add9",
        "6/9": "6_9",
        "11": "11",
        "13": "13",
    }
    chord_pattern = r"\b([A-G](?:#|b)?)(maj9#11|maj7#11|maj#11|maj9|m\(add11\)|m\+11|m11|min11|mi11|m7b5|11|13|7#9|7b9|7#5|7b5|maj7|m7|mi7|min7|dim7|sus4|sus2|add9|6/9|7|m)\b"
    for match in re.finditer(chord_pattern, blob, re.I):
        root = match.group(1).replace("b", "b").replace("#", "#").upper()
        surface_quality = match.group(2).lower()
        quality = chord_quality_map.get(surface_quality, "minor" if surface_quality == "m" else surface_quality)
        root_token = root.lower().replace("#", "_sharp").replace("b", "_flat")
        roots.append(root)
        canonical_terms.append(f"root:{root_token}")
        canonical_terms.append(f"chord_quality:{quality}")
        canonical_terms.append(f"chord:{root_token}_{quality}")
        chord_qualities.append(f"chord_quality:{quality}")
        aliases.append({"surface": match.group(0), "canonical": f"chord:{root_token}_{quality}"})

    # Do not treat standalone A-G letters as roots; captions contain ids,
    # string names, and English words that produce too many false positives.

    for canonical, alias_list in CHORD_QUALITY_ALIASES.items():
        for alias in alias_list:
            if alias.lower() in blob.lower():
                term = f"chord_quality:{canonical}"
                chord_qualities.append(term)
                canonical_terms.append(term)
                aliases.append({"surface": alias, "canonical": term})

    visual_type = str(source.get("visual_type") or "")
    if visual_type:
        canonical_terms.append(f"visual_type:{visual_type}")
    tuning = str(source.get("tuning") or "").strip()
    if tuning and tuning.lower() not in {"unknown", "none"}:
        tuning_token = tuning.lower().replace("#", "_sharp").replace(" ", "")
        canonical_terms.append(f"tuning:{tuning_token}")
    elif "标准调弦" in blob or "standard tuning" in blob.lower() or "eadgbe" in blob.lower():
        canonical_terms.append("tuning:standard")
    for style_tag in source.get("style_tags") or []:
        style_token = str(style_tag).strip().lower().replace(" ", "_")
        if style_token:
            canonical_terms.append(f"style:{style_token}")
    for canonical, alias_list in TECHNIQUE_ALIASES.items():
        for alias in alias_list:
            if alias.lower() in blob.lower():
                canonical_terms.append(f"technique:{canonical}")
                aliases.append({"surface": alias, "canonical": f"technique:{canonical}"})
                break
    if re.search(r"(?<!\d)6/8(?!\d)", blob):
        canonical_terms.append("meter:6_8")
    if re.search(r"(?<!\d)9/8(?!\d)", blob):
        canonical_terms.append("meter:9_8")
    if "高把位" in blob or "high position" in blob.lower():
        canonical_terms.append("fret_region:high")
        constraints.append("fret_region:high")
    if "低把位" in blob or "low position" in blob.lower():
        canonical_terms.append("fret_region:low")
        constraints.append("fret_region:low")
    if "第" in blob and "把位" in blob:
        constraints.append("fretboard:position_reference")
    if "根音型式" in blob:
        canonical_terms.append("concept:root_form")
    if "caged" in blob.lower():
        canonical_terms.append("concept:caged")

    result = {
        "visual_id": source.get("visual_id"),
        "canonical_terms": unique(canonical_terms),
        "aliases_detected": aliases,
        "music_objects": unique([str(source.get("musical_object") or "")]),
        "key_or_tonality": unique(keys),
        "roots": unique(roots),
        "chord_qualities": unique(chord_qualities),
        "scale_or_mode": unique(scales),
        "fretboard_constraints": unique(constraints),
        "visual_type": visual_type,
        "uncertainty_notes": ["local_rule_extractor; LLM review recommended"],
        "confidence": 0.65 if canonical_terms else 0.25,
    }
    return result


def extract_json_object(text: str) -> dict[str, Any]:
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError("LLM response did not contain a JSON object")
    parsed = json.loads(match.group(0))
    if not isinstance(parsed, dict):
        raise ValueError("LLM response JSON is not an object")
    return parsed


class LLMClient:
    def __init__(self, env_file: Path) -> None:
        apply_env_file(env_file)
        self.base_url = os.environ.get("LLM_API_BASE_URL", "").rstrip("/")
        self.api_key = os.environ.get("LLM_API_KEY", "")
        self.model = os.environ.get("LLM_MODEL", "")
        self.temperature = float(os.environ.get("CANONICAL_EXTRACT_TEMPERATURE", "0"))
        self.timeout = int(os.environ.get("CANONICAL_EXTRACT_TIMEOUT_SECONDS", os.environ.get("LLM_TIMEOUT_SECONDS", "90")))
        self.max_retries = int(os.environ.get("CANONICAL_EXTRACT_MAX_RETRIES", os.environ.get("LLM_MAX_RETRIES", "1")))
        self.max_output_tokens = int(os.environ.get("CANONICAL_EXTRACT_MAX_OUTPUT_TOKENS", "8192"))
        self.enable_thinking = os.environ.get("CANONICAL_EXTRACT_ENABLE_THINKING", "false").strip().lower() == "true"
        if not self.base_url or not self.model:
            raise ValueError("LLM_API_BASE_URL and LLM_MODEL must be set in .env")

    def chat_json(self, items: list[dict[str, Any]]) -> dict[str, Any]:
        user_payload = {
            "instruction": "请为每条 caption 提取 canonical_terms。只使用 caption 中已有信息。",
            "items": items,
        }
        request_payload: dict[str, Any] = {
            "model": self.model,
            "temperature": self.temperature,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False, indent=2)},
            ],
            "enable_thinking": self.enable_thinking,
        }
        if self.max_output_tokens > 0:
            request_payload["max_tokens"] = self.max_output_tokens
        body = json.dumps(request_payload, ensure_ascii=False).encode("utf-8")
        headers = {"Content-Type": "application/json; charset=utf-8"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                req = urllib.request.Request(
                    f"{self.base_url}/chat/completions",
                    data=body,
                    headers=headers,
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                return extract_json_object(data["choices"][0]["message"]["content"])
            except (urllib.error.URLError, urllib.error.HTTPError, KeyError, json.JSONDecodeError, ValueError) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(1.5 * (attempt + 1))
        raise RuntimeError(f"Canonical term extraction failed: {last_error}")


def make_llm_item(row: dict[str, Any]) -> dict[str, Any]:
    metadata = row.get("metadata_flat") if isinstance(row.get("metadata_flat"), dict) else {}
    source_metadata = row.get("source_metadata") if isinstance(row.get("source_metadata"), dict) else {}
    return {
        "visual_id": row.get("visual_id") or row.get("segment_id") or metadata.get("visual_id"),
        "visual_type": row.get("visual_type") or metadata.get("visual_type") or row.get("image_type"),
        "musical_object": row.get("musical_object") or metadata.get("musical_object") or row.get("topic"),
        "root": row.get("root") or metadata.get("root"),
        "key": row.get("key"),
        "tuning": row.get("tuning"),
        "entities": row.get("entities") if isinstance(row.get("entities"), dict) else {},
        "style_tags": source_metadata.get("style_tags") or [],
        "trusted_facts": row.get("trusted_facts") if isinstance(row.get("trusted_facts"), dict) else {},
        "quality_or_mode": row.get("quality_or_mode") or metadata.get("quality_or_mode"),
        "position_or_shape": row.get("position_or_shape") or metadata.get("position_or_shape"),
        "caption_text": compact(row.get("caption_text") or row.get("caption") or row.get("retrieval_text") or ""),
        "retrieval_keywords": row.get("retrieval_keywords") or [],
    }


def select_rows(rows: list[dict[str, Any]], offset: int, limit: int, prefer_visual: bool) -> list[dict[str, Any]]:
    selected = rows[offset:]
    if prefer_visual:
        visual = [row for row in selected if str(row.get("visual_type") or row.get("image_type") or "") != "text_answer"]
        text_answer = [row for row in selected if row not in visual]
        selected = visual + text_answer
    return selected[:limit]


def visual_id_from_row(row: dict[str, Any]) -> str:
    metadata = row.get("metadata_flat") if isinstance(row.get("metadata_flat"), dict) else {}
    return str(row.get("visual_id") or row.get("segment_id") or metadata.get("visual_id") or "")


def normalize_item(raw: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
    visual_id = str(raw.get("visual_id") or source.get("visual_id") or "")
    canonical_terms = [str(item) for item in raw.get("canonical_terms", []) if str(item).strip()] if isinstance(raw.get("canonical_terms"), list) else []
    return {
        "visual_id": visual_id,
        "status": "pending_review",
        "canonical_terms": canonical_terms,
        "aliases_detected": raw.get("aliases_detected") if isinstance(raw.get("aliases_detected"), list) else [],
        "music_objects": raw.get("music_objects") if isinstance(raw.get("music_objects"), list) else [],
        "key_or_tonality": raw.get("key_or_tonality") if isinstance(raw.get("key_or_tonality"), list) else [],
        "roots": raw.get("roots") if isinstance(raw.get("roots"), list) else [],
        "chord_qualities": raw.get("chord_qualities") if isinstance(raw.get("chord_qualities"), list) else [],
        "scale_or_mode": raw.get("scale_or_mode") if isinstance(raw.get("scale_or_mode"), list) else [],
        "fretboard_constraints": raw.get("fretboard_constraints") if isinstance(raw.get("fretboard_constraints"), list) else [],
        "visual_type": str(raw.get("visual_type") or source.get("visual_type") or ""),
        "uncertainty_notes": raw.get("uncertainty_notes") if isinstance(raw.get("uncertainty_notes"), list) else [],
        "confidence": raw.get("confidence", 0.0),
        "source_preview": {
            "visual_type": source.get("visual_type"),
            "musical_object": source.get("musical_object"),
            "caption": compact(source.get("caption_text") or "", limit=700),
        },
    }


def render_review(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Visual Caption Canonical Terms Review",
        "",
        "勾选 accept 后，后续可作为视觉 caption 的旁路 canonical_terms 索引层。",
        "",
    ]
    for index, row in enumerate(rows, start=1):
        preview = row.get("source_preview") if isinstance(row.get("source_preview"), dict) else {}
        lines.extend(
            [
                f"## {index}. `{row.get('visual_id')}`",
                "",
                "- [ ] accept",
                "- [ ] revise",
                f"- visual_type: `{row.get('visual_type')}`",
                f"- confidence: `{row.get('confidence')}`",
                f"- canonical_terms: `{', '.join(row.get('canonical_terms') or [])}`",
                f"- key_or_tonality: `{', '.join(str(x) for x in row.get('key_or_tonality') or [])}`",
                f"- chord_qualities: `{', '.join(str(x) for x in row.get('chord_qualities') or [])}`",
                f"- scale_or_mode: `{', '.join(str(x) for x in row.get('scale_or_mode') or [])}`",
                f"- constraints: `{', '.join(str(x) for x in row.get('fretboard_constraints') or [])}`",
                "",
                "<details><summary>aliases_detected</summary>",
                "",
                "```json",
                json.dumps(row.get("aliases_detected") or [], ensure_ascii=False, indent=2),
                "```",
                "",
                "</details>",
                "",
                "<details><summary>source caption</summary>",
                "",
                str(preview.get("caption") or ""),
                "",
                "</details>",
                "",
            ]
        )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--env-file", type=Path, default=ROOT / ".env")
    parser.add_argument("--prefer-visual", action="store_true", default=True)
    parser.add_argument("--backend", choices=["local", "llm"], default="local")
    parser.add_argument("--visual-ids", default="", help="Comma-separated visual_id list. Overrides offset/limit when set.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = read_jsonl(args.input)
    if args.visual_ids.strip():
        wanted = {item.strip() for item in args.visual_ids.split(",") if item.strip()}
        selected = [row for row in rows if visual_id_from_row(row) in wanted]
    else:
        selected = select_rows(rows, args.offset, args.limit, args.prefer_visual)
    source_by_id = {str(make_llm_item(row).get("visual_id")): make_llm_item(row) for row in selected}
    outputs: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    if args.backend == "local":
        for row in selected:
            source = make_llm_item(row)
            outputs.append(normalize_item(local_extract_item(source), source))
    else:
        client = LLMClient(args.env_file)
        for start in range(0, len(selected), args.batch_size):
            batch_rows = selected[start : start + args.batch_size]
            batch_items = [make_llm_item(row) for row in batch_rows]
            try:
                response = client.chat_json(batch_items)
                raw_items = response.get("items") if isinstance(response.get("items"), list) else []
                for raw in raw_items:
                    if not isinstance(raw, dict):
                        continue
                    visual_id = str(raw.get("visual_id") or "")
                    outputs.append(normalize_item(raw, source_by_id.get(visual_id, {})))
            except Exception as exc:
                errors.append({"batch_start": start, "error": f"{type(exc).__name__}: {exc}"})

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_jsonl = args.output_dir / "canonical_terms_review.jsonl"
    output_md = args.output_dir / "canonical_terms_review.md"
    report_json = args.output_dir / "canonical_terms_report.json"
    write_jsonl(output_jsonl, outputs)
    output_md.write_text(render_review(outputs), encoding="utf-8")
    report_json.write_text(
        json.dumps(
            {
                "input": str(args.input),
                "limit": args.limit,
                "offset": args.offset,
                "batch_size": args.batch_size,
                "backend": args.backend,
                "selected": len(selected),
                "extracted": len(outputs),
                "errors": errors,
                "output_jsonl": str(output_jsonl),
                "output_md": str(output_md),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(json.dumps(json.loads(report_json.read_text(encoding="utf-8")), ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
