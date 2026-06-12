#!/usr/bin/env python
"""Normalize free-form guitar arrangement queries into RAG tool plans."""

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

try:
    from prompt_registry import get_prompt_versions, load_prompt
except ImportError:
    from scripts.prompt_registry import get_prompt_versions, load_prompt

SYSTEM_PROMPT = load_prompt("query_normalizer")

INTENTS = {
    "style_arrangement",
    "fretboard_voicing",
    "visual_shape_recommendation",
    "rhythm_riff_design",
    "harmonic_reharmonization",
    "mixed_arrangement",
    "score_analysis_followup",
    "caption_regression_test",
}

TOOLS = ["fretboard_text", "style_text", "visual_caption", "kg"]
STYLE_HINTS = {
    "funk": ["funk", "groove", "ghost", "muted", "chuck", "切分", "十六分", "律动", "消音"],
    "mathrock": ["mathrock", "math rock", "数摇", "数学摇滚", "midwest"],
    "blues": ["blues", "shuffle", "turnaround", "布鲁斯"],
    "metal": ["metal", "djent", "palm mute", "金属"],
    "jazz": ["jazz", "ii-V-I", "shell voicing", "chord melody", "爵士"],
}
TECHNIQUE_HINTS = [
    "riff",
    "groove",
    "tapping",
    "点弦",
    "hammer",
    "pull",
    "slide",
    "滑音",
    "击弦",
    "勾弦",
    "muted",
    "ghost",
    "消音",
    "切分",
    "开放弦",
    "open string",
    "drone",
    "comping",
    "voicing",
]
CHORD_RE = re.compile(r"\b[A-G](?:#|b)?(?:maj|min|m|mi|dim|aug|sus|add)?\d*(?:[#b]\d+)?(?:/[A-G](?:#|b)?)?\b", re.I)
ROOT_RE = re.compile(r"\b([A-G](?:#|b)?)(?=(?:maj|min|m|mi|dim|aug|sus|add|\d|#|b|/|\b))", re.I)
CHINESE_KEY_RE = re.compile(r"([A-G](?:#|b|♭|♯)?|[A-G]\s*flat|[A-G]\s*sharp)\s*(大调|小调|调)", re.I)
CHORD_QUALITY_RE = re.compile(r"(maj9#11|maj7#11|maj#11|maj9|m11|min11|mi11|11|13|7#9|7b9|7#5|7b5|maj7|m7|mi7|min7|dim7|m7b5|sus4|sus2|add9|6/9|7)", re.I)

VISUAL_QUERY_TERMS = ["图", "图示", "指型", "指法", "把位", "排列", "voicing", "diagram", "fingering", "shape"]
ALT_TUNING_TERMS = ["dadgad", "facgce", "drop tuning", "drop d", "open tuning", "alternate tuning", "特殊调弦", "开放调弦", "降弦", "特调"]

ROOT_CANONICAL = {
    "cb": "b",
    "c": "c",
    "c#": "c_sharp",
    "csharp": "c_sharp",
    "db": "db",
    "d": "d",
    "d#": "d_sharp",
    "dsharp": "d_sharp",
    "eb": "eb",
    "e": "e",
    "e#": "f",
    "fb": "e",
    "f": "f",
    "f#": "f_sharp",
    "fsharp": "f_sharp",
    "gb": "gb",
    "g": "g",
    "g#": "g_sharp",
    "gsharp": "g_sharp",
    "ab": "ab",
    "a": "a",
    "a#": "a_sharp",
    "asharp": "a_sharp",
    "bb": "bb",
    "b": "b",
    "b#": "c",
}
CHORD_QUALITY_CANONICAL = {
    "maj": "maj",
    "major": "maj",
    "m": "m",
    "mi": "m",
    "min": "m",
    "minor": "m",
    "maj7": "maj7",
    "m7": "m7",
    "mi7": "m7",
    "min7": "m7",
    "dim7": "dim7",
    "m7b5": "m7b5",
    "m11": "m11",
    "mi11": "m11",
    "min11": "m11",
    "maj9": "maj9",
    "maj#11": "maj_sharp11",
    "maj7#11": "maj7_sharp11",
    "maj9#11": "maj9_sharp11",
    "7#9": "dominant7_sharp9",
    "7b9": "dominant7_flat9",
    "7#5": "dominant7_sharp5",
    "7b5": "dominant7_flat5",
    "sus4": "sus4",
    "sus2": "sus2",
    "add9": "add9",
    "6/9": "six_nine",
    "13": "13",
    "11": "11",
    "7": "dominant7",
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


def as_list(value: Any) -> list[Any]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    return [value]


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return bool(value)


def default_tool_plan() -> dict[str, dict[str, Any]]:
    return {tool: {"enabled": False, "query": "", "reason": ""} for tool in TOOLS}


def infer_style_hints(text: str) -> list[str]:
    lowered = text.lower()
    hints: list[str] = []
    for style, terms in STYLE_HINTS.items():
        if any(term.lower() in lowered for term in terms):
            hints.append(style)
    return hints


def infer_technique_hints(text: str) -> list[str]:
    lowered = text.lower()
    return [term for term in TECHNIQUE_HINTS if term.lower() in lowered]


def infer_harmonic_materials(text: str) -> list[str]:
    seen: set[str] = set()
    materials: list[str] = []
    for match in CHORD_RE.findall(text):
        if match not in seen:
            seen.add(match)
            materials.append(match)
    return materials


def unique_texts(values: list[Any]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        text = str(value).strip()
        if not text or text.lower() in seen:
            continue
        seen.add(text.lower())
        out.append(text)
    return out


def infer_target_keys(text: str) -> list[str]:
    keys: list[str] = []
    for raw_root, quality in CHINESE_KEY_RE.findall(text):
        root = raw_root.replace("♭", "b").replace("♯", "#").replace(" ", "")
        if quality == "大调":
            keys.append(f"{root} major")
        elif quality == "小调":
            keys.append(f"{root} minor")
        else:
            keys.append(root)
    lowered = text.lower()
    for match in re.finditer(r"\b([a-g](?:#|b)?)\s+(major|minor|maj|min)\b", lowered):
        root, mode = match.groups()
        keys.append(f"{root.upper()}{' major' if mode in {'major', 'maj'} else ' minor'}")
    return unique_texts(keys)


def infer_target_roots(text: str, materials: list[str]) -> list[str]:
    roots: list[str] = []
    for value in materials:
        match = ROOT_RE.search(value)
        if match:
            roots.append(match.group(1).replace("♭", "b").replace("♯", "#"))
    for key in infer_target_keys(text):
        match = ROOT_RE.search(key)
        if match:
            roots.append(match.group(1).replace("♭", "b").replace("♯", "#"))
    return unique_texts(roots)


def infer_chord_qualities(text: str, materials: list[str]) -> list[str]:
    qualities: list[str] = []
    for value in materials + [text]:
        for match in CHORD_QUALITY_RE.findall(str(value)):
            qualities.append(match)
    return unique_texts(qualities)


def infer_target_tuning(text: str) -> str:
    lowered = str(text or "").lower().replace("♭", "b").replace("♯", "#")
    compacted = re.sub(r"\s+", "", lowered)
    if "facgce" in compacted:
        return "facgce"
    if "dadgad" in compacted:
        return "dadgad"
    if "dropd" in compacted or "drop d" in lowered:
        return "drop_d"
    if "drop" in lowered or "降弦" in lowered:
        return "drop"
    if "open tuning" in lowered or "开放调弦" in lowered:
        return "open"
    if any(term in lowered for term in ["standard tuning", "standard-tuning", "标准调弦", "标调", "标准弦"]):
        return "standard"
    return "standard"


def canonical_tuning(value: Any) -> str:
    raw = str(value or "").strip().lower().replace(" ", "_").replace("-", "_")
    if not raw:
        return "standard"
    aliases = {
        "std": "standard",
        "standard_tuning": "standard",
        "标准调弦": "standard",
        "标调": "standard",
        "facgce": "facgce",
        "dadgad": "dadgad",
        "drop_d": "drop_d",
        "dropd": "drop_d",
        "drop": "drop",
        "open_tuning": "open",
        "开放调弦": "open",
        "alternate": "alternate",
        "alternate_tuning": "alternate",
        "特殊调弦": "alternate",
    }
    return aliases.get(raw, raw)


def infer_scale_or_mode(text: str) -> list[str]:
    lowered = text.lower()
    modes = []
    for term in ["major scale", "minor scale", "natural minor", "dorian", "mixolydian", "pentatonic", "大调音阶", "小调音阶", "自然小调", "五声音阶"]:
        if term in lowered or term in text:
            modes.append(term)
    return unique_texts(modes)


def infer_fret_region(text: str) -> str:
    lowered = text.lower()
    if "高把位" in text or "high position" in lowered or "high fret" in lowered:
        return "high"
    if "低把位" in text or "low position" in lowered or "low fret" in lowered:
        return "low"
    if "中把位" in text or "middle position" in lowered:
        return "middle"
    return ""


def canonical_root(root: str) -> str:
    normalized = str(root or "").strip().lower().replace("♭", "b").replace("♯", "#").replace(" ", "")
    return ROOT_CANONICAL.get(normalized, normalized.replace("#", "_sharp"))


def canonical_chord_quality(quality: str) -> str:
    normalized = str(quality or "").strip().lower().replace("♭", "b").replace("♯", "#")
    if normalized in CHORD_QUALITY_CANONICAL:
        return CHORD_QUALITY_CANONICAL[normalized]
    if re.fullmatch(r"(?:maj|min|m|mi|dim|aug|sus|add)?\d+(?:[#b]\d+)?(?:/\d+)?", normalized):
        return normalized.replace("#", "_sharp").replace("b", "_flat").replace("/", "_")
    return ""


def normalize_canonical_term(term: str) -> str:
    raw = str(term or "").strip().replace("♭", "b").replace("♯", "#")
    if not raw:
        return ""
    lowered = raw.lower().replace(" ", "_")
    if lowered in {"high_position", "high_fret", "position:high_fret", "高把位"}:
        return "fret_region:high"
    if lowered in {"low_position", "low_fret", "position:low_fret", "低把位"}:
        return "fret_region:low"
    if lowered in {"middle_position", "mid_position", "position:middle_fret", "中把位"}:
        return "fret_region:middle"
    if lowered in {"fingering", "shape", "指型"}:
        return "visual_type:scale_pattern"
    if lowered in {"chord_diagram", "voicing_diagram", "和弦图", "排列图示"}:
        return "visual_type:chord_diagram"
    if lowered in {"alternate_tuning", "special_tuning", "特殊调弦"}:
        return "tuning:alternate"

    if ":" in lowered:
        prefix, value = lowered.split(":", 1)
        value = value.strip("_")
        if prefix == "key":
            if value.endswith("_major") or value.endswith("_minor"):
                root, mode = value.rsplit("_", 1)
                return f"key:{canonical_root(root)}_{mode}"
            return f"root:{canonical_root(value)}"
        if prefix == "root":
            return f"root:{canonical_root(value)}"
        if prefix == "chord_quality":
            return f"chord_quality:{canonical_chord_quality(value)}"
        if prefix == "tuning":
            return f"tuning:{canonical_tuning(value)}"
        if prefix in {"scale", "mode", "visual_type", "fret_region", "fret_range", "technique", "concept", "voicing", "interval"}:
            return f"{prefix}:{value}"
        return ""

    key = canonical_key_from_text(raw)
    if key:
        return key
    if re.fullmatch(r"[A-G](?:#|b)?", raw, re.I):
        return f"root:{canonical_root(raw)}"
    quality = canonical_chord_quality(raw)
    if quality and quality != lowered:
        return f"chord_quality:{quality}"
    if lowered in {"m11", "maj9#11", "maj7", "m7", "7#9", "7b9", "13", "11", "7"}:
        return f"chord_quality:{canonical_chord_quality(raw)}"
    return ""


def normalize_canonical_terms(values: list[Any]) -> list[str]:
    return unique_texts([term for value in values if (term := normalize_canonical_term(str(value)))])


def canonical_key_from_text(text: str) -> str:
    raw = str(text or "").strip().replace("♭", "b").replace("♯", "#")
    match = re.fullmatch(r"([A-G](?:#|b)?)[_\s-]*(major|minor|maj|min)", raw, re.I)
    if match:
        root = canonical_root(match.group(1))
        mode = "major" if match.group(2).lower() in {"major", "maj"} else "minor"
        return f"key:{root}_{mode}"
    match = re.search(r"\b([A-G](?:#|b)?)\s*(major|minor|maj|min)\b", raw, re.I)
    if match:
        root = canonical_root(match.group(1))
        mode = "major" if match.group(2).lower() in {"major", "maj"} else "minor"
        return f"key:{root}_{mode}"
    match = re.search(r"([A-G](?:#|b)?)\s*(大调|小调)", raw, re.I)
    if match:
        root = canonical_root(match.group(1))
        mode = "major" if match.group(2) == "大调" else "minor"
        return f"key:{root}_{mode}"
    return ""


def build_canonical_terms(plan: dict[str, Any]) -> tuple[list[str], list[str], list[str], list[str]]:
    canonical_terms: list[str] = normalize_canonical_terms(as_list(plan.get("canonical_terms")))
    required_terms: list[str] = normalize_canonical_terms(as_list(plan.get("required_terms")))
    optional_terms: list[str] = normalize_canonical_terms(as_list(plan.get("optional_terms")))
    negative_constraints: list[str] = normalize_canonical_terms(as_list(plan.get("negative_constraints")))

    target_tuning = canonical_tuning(plan.get("target_tuning") or "standard")
    tuning_term = f"tuning:{target_tuning}"
    canonical_terms.append(tuning_term)
    required_terms.append(tuning_term)

    for key in as_list(plan.get("target_keys")) + as_list(plan.get("key_or_tonality")):
        term = canonical_key_from_text(str(key))
        if term:
            canonical_terms.append(term)
            required_terms.append(term)

    for root in as_list(plan.get("target_roots")):
        canon = canonical_root(str(root))
        if canon:
            canonical_terms.append(f"root:{canon}")

    for quality in as_list(plan.get("chord_qualities")):
        canon = canonical_chord_quality(str(quality))
        if canon:
            term = f"chord_quality:{canon}"
            canonical_terms.append(term)
            required_terms.append(term)

    for mode in as_list(plan.get("scale_or_mode")):
        normalized = str(mode).strip().lower().replace(" ", "_")
        if not normalized:
            continue
        if normalized.startswith("mode:") or normalized.startswith("scale:"):
            term = normalized
        elif "dorian" in normalized or "多利亚" in normalized:
            term = "mode:dorian"
        elif "mixolydian" in normalized or "混合利底亚" in normalized:
            term = "mode:mixolydian"
        elif "pentatonic" in normalized or "五声" in normalized:
            term = "scale:pentatonic_minor" if "minor" in normalized or "小" in normalized else "scale:pentatonic"
        elif "minor" in normalized or "小调" in normalized:
            term = "scale:natural_minor"
        elif "major" in normalized or "大调" in normalized:
            term = "scale:major"
        else:
            term = f"scale:{normalized}"
        canonical_terms.append(term)

    fret_region = str(plan.get("fret_region") or "").strip().lower()
    if fret_region in {"low", "middle", "high"}:
        canonical_terms.append(f"fret_region:{fret_region}")
        optional_terms.append(f"fret_region:{fret_region}")

    if as_bool(plan.get("visual_evidence_required")):
        raw_query = f"{plan.get('raw_query', '')} {plan.get('normalized_query', '')}".lower()
        if any(term in raw_query for term in ["和弦图", "chord diagram", "voicing", "排列"]):
            canonical_terms.append("visual_type:chord_diagram")
            required_terms.append("visual_type:chord_diagram")
        elif any(term in raw_query for term in ["音阶", "scale", "指型", "fingering", "pattern"]):
            canonical_terms.append("visual_type:scale_pattern")
            required_terms.append("visual_type:scale_pattern")

    for technique in as_list(plan.get("techniques")):
        normalized = str(technique).strip().lower().replace(" ", "_")
        if not normalized:
            continue
        if normalized in {"开放弦", "open_string", "open"}:
            normalized = "open_string"
        elif normalized in {"点弦", "tapping"}:
            normalized = "tapping"
        elif normalized in {"voicing", "riff", "groove"}:
            pass
        else:
            normalized = normalized.replace("-", "_")
        canonical_terms.append(f"technique:{normalized}")

    if target_tuning == "standard":
        negative_constraints.extend(["tuning:dadgad", "tuning:facgce", "tuning:drop", "tuning:drop_d", "tuning:open", "tuning:alternate"])
    elif not as_bool(plan.get("allow_alternate_tuning")):
        negative_constraints.extend(["tuning:dadgad", "tuning:facgce", "tuning:drop", "tuning:drop_d", "tuning:open", "tuning:alternate"])
    else:
        raw_query = f"{plan.get('raw_query', '')} {plan.get('normalized_query', '')}".lower()
        if "facgce" in raw_query:
            canonical_terms.append("tuning:facgce")
        if "dadgad" in raw_query:
            canonical_terms.append("tuning:dadgad")
        if "drop d" in raw_query or "dropd" in raw_query:
            canonical_terms.append("tuning:drop_d")
        elif "drop" in raw_query or "降弦" in raw_query:
            canonical_terms.append("tuning:drop")
        if "open tuning" in raw_query or "开放调弦" in raw_query:
            canonical_terms.append("tuning:open")

    return (
        unique_texts(canonical_terms),
        unique_texts(required_terms),
        unique_texts(optional_terms),
        unique_texts(negative_constraints),
    )


def sanitize_query_plan(raw_query: str, plan: dict[str, Any]) -> dict[str, Any]:
    query_blob_seed = f"{raw_query} {plan.get('normalized_query', '')}"
    target_tuning = canonical_tuning(plan.get("target_tuning") or infer_target_tuning(query_blob_seed))
    sanitized: dict[str, Any] = {
        "raw_query": str(plan.get("raw_query") or raw_query),
        "normalized_query": str(plan.get("normalized_query") or raw_query),
        "intent": str(plan.get("intent") or "mixed_arrangement"),
        "confidence": float(plan.get("confidence") or 0.0),
        "style_hints": [str(item) for item in as_list(plan.get("style_hints")) if str(item).strip()],
        "key_or_tonality": str(plan.get("key_or_tonality") or ""),
        "meter_or_rhythm": str(plan.get("meter_or_rhythm") or ""),
        "tempo_hint": str(plan.get("tempo_hint") or ""),
        "target_tuning": target_tuning,
        "harmonic_materials": [str(item) for item in as_list(plan.get("harmonic_materials")) if str(item).strip()],
        "melodic_materials": [str(item) for item in as_list(plan.get("melodic_materials")) if str(item).strip()],
        "techniques": [str(item) for item in as_list(plan.get("techniques")) if str(item).strip()],
        "fretboard_constraints": [str(item) for item in as_list(plan.get("fretboard_constraints")) if str(item).strip()],
        "arrangement_goals": [str(item) for item in as_list(plan.get("arrangement_goals")) if str(item).strip()],
        "target_keys": [str(item) for item in as_list(plan.get("target_keys")) if str(item).strip()],
        "target_roots": [str(item) for item in as_list(plan.get("target_roots")) if str(item).strip()],
        "chord_qualities": [str(item) for item in as_list(plan.get("chord_qualities")) if str(item).strip()],
        "scale_or_mode": [str(item) for item in as_list(plan.get("scale_or_mode")) if str(item).strip()],
        "fret_region": str(plan.get("fret_region") or ""),
        "position_constraints": [str(item) for item in as_list(plan.get("position_constraints")) if str(item).strip()],
        "requires_exact_key": as_bool(plan.get("requires_exact_key")),
        "requires_exact_chord": as_bool(plan.get("requires_exact_chord")),
        "visual_evidence_required": as_bool(plan.get("visual_evidence_required")),
        "allow_alternate_tuning": as_bool(plan.get("allow_alternate_tuning")),
        "allow_exercise_reference": True if plan.get("allow_exercise_reference") is None else as_bool(plan.get("allow_exercise_reference")),
        "canonical_terms": normalize_canonical_terms(as_list(plan.get("canonical_terms"))),
        "required_terms": normalize_canonical_terms(as_list(plan.get("required_terms"))),
        "optional_terms": normalize_canonical_terms(as_list(plan.get("optional_terms"))),
        "negative_constraints": normalize_canonical_terms(as_list(plan.get("negative_constraints"))),
        "retrieval_plan": default_tool_plan(),
        "composer_intent": {
            "answer_type": "",
            "must_include": [],
            "avoid": [],
            "uncertainty_notes": [],
        },
        "eval_tags": [str(item) for item in as_list(plan.get("eval_tags")) if str(item).strip()],
    }
    if sanitized["intent"] not in INTENTS:
        sanitized["intent"] = "mixed_arrangement"
    sanitized["confidence"] = max(0.0, min(1.0, sanitized["confidence"]))
    query_blob = f"{raw_query} {sanitized['normalized_query']}"
    if not sanitized["style_hints"]:
        sanitized["style_hints"] = infer_style_hints(query_blob)
    if not sanitized["techniques"]:
        sanitized["techniques"] = infer_technique_hints(query_blob)
    if not sanitized["harmonic_materials"]:
        sanitized["harmonic_materials"] = infer_harmonic_materials(query_blob)
    if sanitized["key_or_tonality"] and not sanitized["target_keys"]:
        sanitized["target_keys"].append(sanitized["key_or_tonality"])
    if not sanitized["target_keys"]:
        sanitized["target_keys"] = infer_target_keys(query_blob)
    if not sanitized["target_roots"]:
        sanitized["target_roots"] = infer_target_roots(query_blob, sanitized["harmonic_materials"] + sanitized["target_keys"])
    if not sanitized["chord_qualities"]:
        sanitized["chord_qualities"] = infer_chord_qualities(query_blob, sanitized["harmonic_materials"])
    if not sanitized["scale_or_mode"]:
        sanitized["scale_or_mode"] = infer_scale_or_mode(query_blob)
    if not sanitized["fret_region"]:
        sanitized["fret_region"] = infer_fret_region(query_blob)
    if not sanitized["requires_exact_key"]:
        sanitized["requires_exact_key"] = bool(sanitized["target_keys"]) or any(term in query_blob for term in ["同把位", "转成", "转为", "relative"])
    if not sanitized["requires_exact_chord"]:
        sanitized["requires_exact_chord"] = bool(sanitized["chord_qualities"] and sanitized["target_roots"])
    if not sanitized["visual_evidence_required"]:
        sanitized["visual_evidence_required"] = any(term.lower() in query_blob.lower() for term in VISUAL_QUERY_TERMS)
    if sanitized["target_tuning"] != "standard":
        sanitized["allow_alternate_tuning"] = True
    elif not sanitized["allow_alternate_tuning"]:
        sanitized["allow_alternate_tuning"] = any(term in query_blob.lower() for term in ALT_TUNING_TERMS)
    (
        sanitized["canonical_terms"],
        sanitized["required_terms"],
        sanitized["optional_terms"],
        sanitized["negative_constraints"],
    ) = build_canonical_terms(sanitized)

    raw_retrieval = plan.get("retrieval_plan") if isinstance(plan.get("retrieval_plan"), dict) else {}
    for tool in TOOLS:
        item = raw_retrieval.get(tool) if isinstance(raw_retrieval.get(tool), dict) else {}
        sanitized["retrieval_plan"][tool] = {
            "enabled": as_bool(item.get("enabled")),
            "query": str(item.get("query") or sanitized["normalized_query"]),
            "reason": str(item.get("reason") or ""),
        }

    composer = plan.get("composer_intent") if isinstance(plan.get("composer_intent"), dict) else {}
    sanitized["composer_intent"] = {
        "answer_type": str(composer.get("answer_type") or ""),
        "must_include": [str(item) for item in as_list(composer.get("must_include")) if str(item).strip()],
        "avoid": [str(item) for item in as_list(composer.get("avoid")) if str(item).strip()],
        "uncertainty_notes": [str(item) for item in as_list(composer.get("uncertainty_notes")) if str(item).strip()],
    }
    if not any(item["enabled"] for item in sanitized["retrieval_plan"].values()):
        sanitized["retrieval_plan"]["style_text"]["enabled"] = True
        sanitized["retrieval_plan"]["kg"]["enabled"] = True
    if sanitized["confidence"] <= 0 and any(item["enabled"] for item in sanitized["retrieval_plan"].values()):
        enabled_count = sum(1 for item in sanitized["retrieval_plan"].values() if item["enabled"])
        sanitized["confidence"] = min(0.9, 0.55 + enabled_count * 0.08)
    sanitized["prompt_versions"] = {"query_normalizer": get_prompt_versions()["query_normalizer"]}
    return sanitized


def build_user_prompt(query: str, context: dict[str, Any] | None = None) -> str:
    context = context or {}
    return (
        "请将下面用户 query 标准化为 QueryPlan JSON。\n\n"
        f"用户 query：\n{query}\n\n"
        "可选上下文：\n"
        f"{json.dumps(context, ensure_ascii=False, indent=2)}\n\n"
        "输出要求：\n"
        "- 必须是合法 JSON。\n"
        "- normalized_query 要适合直接用于 RAG 检索。\n"
        "- retrieval_plan 中每个工具都要给 enabled、query、reason。\n"
        "- 必须输出 target_tuning；用户未指定调弦时 target_tuning=standard。\n"
        "- 如果用户指定 FACGCE/DADGAD/Drop D/开放调弦，target_tuning 必须对应为 facgce/dadgad/drop_d/open，并且 tuning:xxx 必须进入 required_terms。\n"
        "- 尽量输出 target_keys、target_roots、chord_qualities、scale_or_mode、fret_region、requires_exact_key、requires_exact_chord、visual_evidence_required、allow_alternate_tuning。\n"
        "- 必须尽量输出 canonical_terms、required_terms、optional_terms、negative_constraints。\n"
        "- 如果需要图形证据，visual_caption.enabled=true。\n"
        "- 如果是编曲建议或风格迁移，kg.enabled=true。\n"
        "- 不要回答用户问题。\n"
    )


class LLMClient:
    def __init__(self, env_file: Path = Path(".env")) -> None:
        apply_env_file(env_file)
        self.base_url = os.environ.get("LLM_API_BASE_URL", "").rstrip("/")
        self.api_key = os.environ.get("LLM_API_KEY", "")
        self.model = os.environ.get("LLM_MODEL", "")
        self.temperature = float(os.environ.get("QUERY_NORMALIZER_TEMPERATURE", os.environ.get("LLM_TEMPERATURE", "0")))
        self.timeout = int(os.environ.get("QUERY_NORMALIZER_TIMEOUT_SECONDS", os.environ.get("LLM_TIMEOUT_SECONDS", "60")))
        self.max_retries = int(os.environ.get("QUERY_NORMALIZER_MAX_RETRIES", os.environ.get("LLM_MAX_RETRIES", "1")))
        self.max_output_tokens = int(os.environ.get("QUERY_NORMALIZER_MAX_OUTPUT_TOKENS", "4096"))
        self.enable_thinking = os.environ.get("QUERY_NORMALIZER_ENABLE_THINKING", os.environ.get("LLM_ENABLE_THINKING", "false")).strip().lower() == "true"
        if not self.base_url or not self.model:
            raise ValueError("LLM_API_BASE_URL and LLM_MODEL must be set in .env")

    def chat_json(self, query: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        request_payload: dict[str, Any] = {
            "model": self.model,
            "temperature": self.temperature,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(query, context)},
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
        raise RuntimeError(f"Query normalizer LLM request failed: {last_error}")


def normalize_query(query: str, context: dict[str, Any] | None = None, env_file: Path = Path(".env")) -> dict[str, Any]:
    client = LLMClient(env_file)
    raw_plan = client.chat_json(query, context=context)
    return sanitize_query_plan(query, raw_plan)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True)
    parser.add_argument("--context-json", default="")
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    context = json.loads(args.context_json) if args.context_json else {}
    plan = normalize_query(args.query, context=context, env_file=args.env_file)
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
