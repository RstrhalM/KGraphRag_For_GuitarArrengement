from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from embedding_cache import EmbeddingCache
from local_text_embedding import DEFAULT_LOCAL_MODEL, LocalTransformerEmbedder


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHROMA_DIR = ROOT / "data" / "chroma"
DEFAULT_REPORT_MD = ROOT / "data" / "eval" / "retrieval_bundle_report.md"
DEFAULT_REPORT_JSON = ROOT / "data" / "eval" / "retrieval_bundle_report.json"
DEFAULT_KG_ALIASES = ROOT / "data" / "knowledge" / "kg_aliases.json"
DEFAULT_EMBEDDING_CACHE = ROOT / "data" / "cache" / "embeddings.sqlite"
DEFAULT_MULTIMODAL_EMBEDDING_URL = (
    "https://dashscope.aliyuncs.com/api/v1/services/embeddings/"
    "multimodal-embedding/multimodal-embedding"
)


TESTS: list[dict[str, Any]] = [
    {
        "id": "funk_muted_chuck",
        "query": "funk rhythm guitar sixteenth note muted chuck bubble groove",
        "text_sources": ["cory_wong_funk_core"],
        "style_tags": ["funk", "rhythm_guitar"],
        "kg_nodes_any": [
            "feature:muted_chuck_density",
            "feature:sixteenth_note_undercurrent",
            "feature:staccato_bubble",
        ],
    },
    {
        "id": "funk_upstroke_downstroke",
        "query": "upstroke hit downstroke muted strings funk rhythm guitar",
        "text_sources": ["cory_wong_funk_core"],
        "style_tags": ["funk", "rhythm_guitar"],
        "kg_nodes_any": [
            "technique:upstroke_hit_downstroke",
            "technique:left_hand_muting",
            "technique:right_hand_muting",
        ],
    },
    {
        "id": "funk_sparse_voicing_space",
        "query": "funk rhythm guitar sparse voicing leave space for bass drums keys horns",
        "text_sources": ["cory_wong_funk_core"],
        "style_tags": ["funk", "rhythm_guitar"],
        "kg_nodes_any": [
            "heuristic:leave_space_for_band",
            "voicing:sparse_funk_voicing",
            "feature:frequency_slotting",
        ],
    },
    {
        "id": "funk_section_energy",
        "query": "section build rhythm guitar verse chorus wider strum more velocity",
        "text_sources": ["cory_wong_funk_core"],
        "style_tags": ["funk", "rhythm_guitar"],
        "kg_nodes_any": [
            "heuristic:section_energy_stair_step",
            "feature:section_energy_lift",
            "arrangement:chorus_lift",
        ],
    },
    {
        "id": "mathrock_dadgad_open_strings",
        "query": "DADGAD open strings common tones tapping power chords math rock",
        "text_sources": ["mathrock_text_course"],
        "style_tags": ["math_rock", "midwest_emo"],
        "kg_nodes_any": [
            "tuning:DADGAD",
            "feature:open_string_drone",
            "technique:tapped_power_chords",
        ],
    },
    {
        "id": "mathrock_alternate_tuning",
        "query": "alternate tuning movable chord shapes open string drone midwest emo",
        "text_sources": ["mathrock_text_course"],
        "style_tags": ["math_rock", "midwest_emo"],
        "kg_nodes_any": [
            "heuristic:alternate_tuning_for_ease",
            "feature:open_string_drone",
            "tuning:open_tuning",
        ],
    },
    {
        "id": "mathrock_tapping_power_chord",
        "query": "tapping power chord suspended chord math rock riff",
        "text_sources": ["mathrock_text_course"],
        "style_tags": ["math_rock", "midwest_emo"],
        "kg_nodes_any": [
            "technique:tapped_power_chords",
            "technique:tapping_power_chords",
            "voicing:suspended_power_chord",
        ],
    },
    {
        "id": "mathrock_non_diatonic_passing",
        "query": "midwest emo chromatic passing chord jazzy non diatonic triad slide",
        "text_sources": ["mathrock_text_course"],
        "style_tags": ["math_rock", "midwest_emo"],
        "kg_nodes_any": [
            "heuristic:non_diatonic_passing_chords",
            "color:jazzy_midwest_emo",
            "technique:triad_slide",
        ],
    },
    {
        "id": "fretboard_root_fingering_forms",
        "query": "根音 指型 五种 root fingering form",
        "text_sources": ["fretboard_handbook_mineru"],
        "style_tags": ["fretboard", "guitar_foundation"],
        "visual_sources": ["fretboard_handbook_mineru"],
        "visual_priorities": ["P0_root_fingering_forms"],
        "kg_nodes_any": ["concept:根音", "concept:指型", "concept:把位"],
    },
    {
        "id": "fretboard_intervals_octave",
        "query": "八度 音程 指板 interval octave",
        "text_sources": ["fretboard_handbook_mineru"],
        "style_tags": ["fretboard", "guitar_foundation"],
        "visual_sources": ["fretboard_handbook_mineru"],
        "visual_priorities": ["P1_scales_intervals"],
        "kg_nodes_any": ["concept:八度", "concept:音程", "concept:指板"],
    },
    {
        "id": "fretboard_triad_arpeggio",
        "query": "大三和弦 琶音 指型 根音 major triad arpeggio",
        "text_sources": ["fretboard_handbook_mineru"],
        "style_tags": ["fretboard", "guitar_foundation"],
        "visual_sources": ["fretboard_handbook_mineru"],
        "visual_priorities": ["P2_arpeggios_chords"],
        "kg_nodes_any": ["concept:琶音", "concept:三和弦", "concept:大三和弦"],
    },
    {
        "id": "fretboard_common_chords_6_9",
        "query": "其他常用和弦 指型 六和弦 九和弦 add9 6/9",
        "text_sources": ["fretboard_handbook_mineru"],
        "style_tags": ["fretboard", "guitar_foundation"],
        "visual_sources": ["fretboard_handbook_mineru"],
        "visual_priorities": ["P3_common_scales_chords"],
        "kg_nodes_any": ["concept:六和弦", "concept:九和弦", "concept:常用和弦"],
    },
    {
        "id": "funk_ghost_note_left_hand_muting",
        "query": "funk ghost note left hand muting sixteenth rhythm guitar tight groove",
        "text_sources": ["cory_wong_funk_core"],
        "style_tags": ["funk", "rhythm_guitar"],
        "kg_nodes_any": ["technique:left_hand_muting", "feature:sixteenth_note_undercurrent"],
    },
    {
        "id": "funk_timing_groove_density",
        "query": "funk timing groove density range tone space rhythm guitar",
        "text_sources": ["cory_wong_funk_core"],
        "style_tags": ["funk", "rhythm_guitar"],
        "kg_nodes_any": ["heuristic:leave_space_for_band", "feature:staccato_bubble"],
    },
    {
        "id": "mathrock_open_string_drone_odd_meter",
        "query": "math rock open string drone odd meter clean tapping riff",
        "text_sources": ["mathrock_text_course"],
        "style_tags": ["math_rock", "midwest_emo"],
        "kg_nodes_any": ["feature:open_string_drone", "technique:two_hand_tapping"],
    },
    {
        "id": "mathrock_dyad_pull_off_open_string",
        "query": "tapped dyads pull off to open string math rock melodic power chord",
        "text_sources": ["mathrock_text_course"],
        "style_tags": ["math_rock", "midwest_emo"],
        "kg_nodes_any": ["feature:tapped_dyads", "technique:pull-off_to_open_string", "technique:tapped_power_chord"],
    },
    {
        "id": "fretboard_root_octave_ambiguous",
        "query": "根音 八度 指型 octave root pattern",
        "text_sources": ["fretboard_handbook_mineru"],
        "style_tags": ["fretboard", "guitar_foundation"],
        "visual_sources": ["fretboard_handbook_mineru"],
        "visual_priorities": ["P1_scales_intervals"],
        "kg_nodes_any": ["concept:八度", "concept:根音", "concept:指型"],
    },
    {
        "id": "fretboard_perfect_fifth_power_chord_interval",
        "query": "纯五度 音程 power chord root finding 指板",
        "text_sources": ["fretboard_handbook_mineru"],
        "style_tags": ["fretboard", "guitar_foundation"],
        "visual_sources": ["fretboard_handbook_mineru"],
        "visual_priorities": ["P1_scales_intervals"],
        "kg_nodes_any": ["concept:音程", "heuristic:power_chord_root_finding"],
    },
    {
        "id": "fretboard_caged_major_triad_shapes",
        "query": "CAGED 大三和弦 五种指型 major triad shapes",
        "text_sources": ["fretboard_handbook_mineru"],
        "style_tags": ["fretboard", "guitar_foundation"],
        "visual_sources": ["fretboard_handbook_mineru"],
        "visual_priorities": ["P2_arpeggios_chords"],
        "kg_nodes_any": ["concept:大三和弦", "concept:指型"],
    },
    {
        "id": "fretboard_add9_not_dom9",
        "query": "add9 加九和弦 不含七音 不要混淆 dominant 9",
        "text_sources": ["fretboard_handbook_mineru"],
        "style_tags": ["fretboard", "guitar_foundation"],
        "visual_sources": ["fretboard_handbook_mineru"],
        "visual_priorities": ["P3_common_scales_chords"],
        "kg_nodes_any": ["concept:九和弦", "concept:常用和弦"],
    },
    {
        "id": "fretboard_pentatonic_two_notes_per_string",
        "query": "五声音阶 每根弦两个音 pentatonic two notes per string",
        "text_sources": ["fretboard_handbook_mineru"],
        "style_tags": ["fretboard", "guitar_foundation"],
        "visual_sources": ["fretboard_handbook_mineru"],
        "visual_priorities": ["P1_scales_intervals"],
        "kg_nodes_any": ["scale:pentatonic_major", "heuristic:two_notes_per_string_geometry"],
    },
    {
        "id": "fretboard_root_pattern_cycle_overlap",
        "query": "五种根音型式 循环 重叠 root pattern cycle overlap",
        "text_sources": ["fretboard_handbook_mineru"],
        "style_tags": ["fretboard", "guitar_foundation"],
        "visual_sources": ["fretboard_handbook_mineru"],
        "visual_priorities": ["P0_root_fingering_forms"],
        "kg_nodes_any": ["concept:根音", "concept:指型"],
    },
]


FRETBOARD_PRIORITY_RULES: list[dict[str, Any]] = [
    {
        "priority": "P3_common_scales_chords",
        "strong": [
            "其他常用和弦",
            "常用和弦",
            "六和弦",
            "九和弦",
            "加九",
            "6/9",
            "add9",
            "add 9",
            "whole tone",
            "diminished scale",
        ],
        "weak": ["extended chord", "dominant 9", "dom9", "6th chord", "9th chord"],
    },
    {
        "priority": "P2_arpeggios_chords",
        "strong": [
            "琶音",
            "三和弦",
            "七和弦",
            "大三和弦",
            "小三和弦",
            "增三和弦",
            "减三和弦",
            "arpeggio",
            "triad",
            "maj7",
            "m7",
            "dom7",
        ],
        "weak": ["caged", "shape", "shapes", "voicing"],
    },
    {
        "priority": "P1_scales_intervals",
        "strong": [
            "音程",
            "八度",
            "大三度",
            "小三度",
            "纯五度",
            "六度",
            "七度",
            "interval",
            "octave",
            "third",
            "fifth",
            "sixth",
            "seventh",
            "pentatonic",
            "scale",
        ],
        "weak": ["double stop", "two notes per string", "音阶"],
    },
    {
        "priority": "P0_root_fingering_forms",
        "strong": [
            "根音型式",
            "根音指型",
            "五种根音",
            "root fingering",
            "root pattern",
            "root form",
        ],
        "weak": ["root shape", "root cycle", "cycle", "overlap", "重叠", "循环"],
    },
]


def apply_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def first_env(*names: str, default: str = "") -> str:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return default


def normalize_base_url(url: str) -> str:
    url = url.rstrip("/")
    if url.endswith("/embeddings"):
        return url[: -len("/embeddings")]
    return url


def post_json(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {body[:800]}") from exc


class EmbeddingClient:
    def __init__(
        self,
        model: str,
        dimensions: int | None = None,
        timeout: int = 90,
        cache: EmbeddingCache | None = None,
    ):
        self.model = model
        self.dimensions = dimensions
        self.timeout = timeout
        self.cache = cache
        self.last_cache_hit = False
        self.api_key = first_env(
            "EMBEDDING_API_KEY",
            "LLM_API_KEY",
            "OPENAI_API_KEY",
            "DASHSCOPE_API_KEY",
            "API_KEY",
        )
        base_url = first_env(
            "EMBEDDING_BASE_URL",
            "LLM_BASE_URL",
            "OPENAI_BASE_URL",
            "DASHSCOPE_BASE_URL",
            default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        self.url = normalize_base_url(base_url) + "/embeddings"
        if not self.api_key:
            raise RuntimeError("Missing embedding API key in .env")

    def embed_text(self, text: str, *, vl_format: bool = False) -> list[float]:
        input_type = "openai_text_vl_format" if vl_format else "openai_text"
        cache_key = EmbeddingCache.make_key(
            provider="openai_compatible",
            model=self.model,
            dimensions=self.dimensions,
            input_type=input_type,
            content=text,
            endpoint=self.url,
        )
        if self.cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                self.last_cache_hit = True
                return cached
        self.last_cache_hit = False
        payload: dict[str, Any] = {"model": self.model, "input": [{"text": text}] if vl_format else text}
        if self.dimensions:
            payload["dimensions"] = self.dimensions
        try:
            data = post_json(self.url, payload, self.api_key, self.timeout)
        except RuntimeError:
            if not vl_format:
                raise
            payload["input"] = text
            data = post_json(self.url, payload, self.api_key, self.timeout)
        try:
            vector = data["data"][0]["embedding"]
            if self.cache:
                self.cache.set(
                    cache_key,
                    vector,
                    provider="openai_compatible",
                    model=self.model,
                    dimensions=self.dimensions,
                    input_type=input_type,
                    content=text,
                )
            return vector
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(f"Unexpected embedding response: {json.dumps(data, ensure_ascii=False)[:800]}") from exc


class LocalEmbeddingClient:
    def __init__(
        self,
        model: str,
        dimensions: int | None = None,
        timeout: int = 90,
        cache: EmbeddingCache | None = None,
    ):
        self.model = model or os.environ.get("LOCAL_EMBEDDING_MODEL", DEFAULT_LOCAL_MODEL)
        self.dimensions = dimensions
        self.timeout = timeout
        self.cache = cache
        self.last_cache_hit = False
        self.backend: LocalTransformerEmbedder | None = None

    def _backend(self) -> LocalTransformerEmbedder:
        if self.backend is None:
            self.backend = LocalTransformerEmbedder(
                self.model,
                device=os.environ.get("LOCAL_EMBEDDING_DEVICE", "auto"),
                max_length=int(os.environ.get("LOCAL_EMBEDDING_MAX_LENGTH", "2048")),
            )
        return self.backend

    def embed_text(self, text: str, *, vl_format: bool = False) -> list[float]:
        cache_key = EmbeddingCache.make_key(
            provider="local_transformers",
            model=self.model,
            dimensions=self.dimensions,
            input_type="local_text",
            content=text,
            endpoint="local",
        )
        if self.cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                self.last_cache_hit = True
                return cached
        self.last_cache_hit = False
        vector = self._backend().embed([text], batch_size=1)[0]
        if self.cache:
            self.cache.set(
                cache_key,
                vector,
                provider="local_transformers",
                model=self.model,
                dimensions=self.dimensions,
                input_type="local_text",
                content=text,
            )
        return vector


def extract_multimodal_embeddings(payload: dict[str, Any]) -> list[list[float]]:
    output = payload.get("output", {})
    candidates = output.get("embeddings") or output.get("embedding") or payload.get("embeddings")
    if isinstance(candidates, list) and candidates and isinstance(candidates[0], dict):
        return [item["embedding"] for item in candidates if "embedding" in item]
    if isinstance(candidates, list) and candidates and isinstance(candidates[0], (int, float)):
        return [candidates]
    raise RuntimeError(f"Cannot find embeddings in response keys: {list(payload.keys())}")


class MultiModalEmbeddingClient:
    def __init__(
        self,
        model: str,
        dimensions: int,
        timeout: int = 120,
        cache: EmbeddingCache | None = None,
    ):
        self.model = model
        self.dimensions = dimensions
        self.timeout = timeout
        self.cache = cache
        self.last_cache_hit = False
        self.max_retries = int(first_env("VL_EMBEDDING_MAX_RETRIES", default="2"))
        self.api_key = first_env("VL_EMBEDDING_API_KEY", "LLM_API_KEY", "DASHSCOPE_API_KEY", "API_KEY")
        self.url = first_env("MULTIMODAL_EMBEDDING_API_URL", default=DEFAULT_MULTIMODAL_EMBEDDING_URL)
        if not self.api_key:
            raise RuntimeError("Missing VL_EMBEDDING_API_KEY or LLM_API_KEY in .env")

    def embed_text(self, text: str) -> list[float]:
        cache_key = EmbeddingCache.make_key(
            provider="dashscope_multimodal",
            model=self.model,
            dimensions=self.dimensions,
            input_type="multimodal_text",
            content=text,
            endpoint=self.url,
        )
        if self.cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                self.last_cache_hit = True
                return cached
        self.last_cache_hit = False
        payload = {
            "model": self.model,
            "input": {"contents": [{"text": text}]},
            "parameters": {
                "dimension": self.dimensions,
                "enable_fusion": False,
            },
        }
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                data = post_json(self.url, payload, self.api_key, self.timeout)
                vector = extract_multimodal_embeddings(data)[0]
                if self.cache:
                    self.cache.set(
                        cache_key,
                        vector,
                        provider="dashscope_multimodal",
                        model=self.model,
                        dimensions=self.dimensions,
                        input_type="multimodal_text",
                        content=text,
                    )
                return vector
            except Exception as exc:
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(1.5 * (attempt + 1))
        raise RuntimeError(f"qwen3-vl-embedding text request failed: {last_error}")


def parse_jsonish_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    if not isinstance(value, str):
        return [str(value)]
    value = value.strip()
    if not value:
        return []
    try:
        parsed = json.loads(value)
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
    except json.JSONDecodeError:
        pass
    return [part.strip() for part in value.split(",") if part.strip()]


def infer_style_tags(query: str, explicit_tags: list[str]) -> list[str]:
    text = query.lower()
    tags = set(explicit_tags)
    if any(token in text for token in ["funk", "chuck", "bubble", "muted"]):
        tags.update(["funk", "rhythm_guitar"])
    if any(token in text for token in ["math", "midwest", "dadgad", "tapping"]):
        tags.update(["math_rock", "midwest_emo"])
    if any(token in text for token in ["指板", "把位", "音程", "琶音", "和弦", "fretboard", "interval", "arpeggio"]):
        tags.update(["fretboard", "guitar_foundation"])
    return sorted(tags)


def infer_visual_priorities(query: str, explicit_priorities: list[str] | None = None) -> list[str]:
    scores = score_visual_priorities(query)
    priorities = list(explicit_priorities or [])
    for priority, score in sorted(scores.items(), key=lambda item: (-item[1], item[0])):
        if score > 0 and priority not in priorities:
            priorities.append(priority)
    return priorities


def score_visual_priorities(query: str) -> dict[str, float]:
    lowered = query.lower()
    scores: dict[str, float] = {}
    for rule in FRETBOARD_PRIORITY_RULES:
        priority = str(rule["priority"])
        score = 0.0
        for needle in rule.get("strong", []):
            if str(needle).lower() in lowered:
                score += 3.0
        for needle in rule.get("weak", []):
            if str(needle).lower() in lowered:
                score += 1.0
        scores[priority] = score
    if "根音" in query and "指型" in query:
        scores["P0_root_fingering_forms"] = scores.get("P0_root_fingering_forms", 0.0) + 1.5
    if ("八度" in query or "octave" in lowered) and ("根音" in query or "root" in lowered):
        scores["P1_scales_intervals"] = scores.get("P1_scales_intervals", 0.0) + 1.5
    if ("caged" in lowered or "五种" in query) and ("三和弦" in query or "triad" in lowered):
        scores["P2_arpeggios_chords"] = scores.get("P2_arpeggios_chords", 0.0) + 1.5
    if ("add9" in lowered or "加九" in query) and ("dom" in lowered or "dominant" in lowered or "属" in query):
        scores["P3_common_scales_chords"] = scores.get("P3_common_scales_chords", 0.0) + 1.5
    return scores


def chroma_where(source_ids: list[str], priorities: list[str]) -> dict[str, Any] | None:
    filters: list[dict[str, Any]] = []
    if len(source_ids) == 1:
        filters.append({"source_id": source_ids[0]})
    if len(priorities) == 1:
        filters.append({"priority": priorities[0]})
    if not filters:
        return None
    if len(filters) == 1:
        return filters[0]
    return {"$and": filters}


def chroma_client(path: Path):
    import chromadb

    return chromadb.PersistentClient(path=str(path))


def query_collection(collection, embedding: list[float], n_results: int, where: dict[str, Any] | None = None):
    result = collection.query(query_embeddings=[embedding], n_results=n_results, where=where)
    docs = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]
    ids = result.get("ids", [[]])[0]
    rows = []
    for idx, item_id in enumerate(ids):
        rows.append(
            {
                "id": item_id,
                "document": docs[idx] if idx < len(docs) else "",
                "metadata": metadatas[idx] if idx < len(metadatas) else {},
                "distance": distances[idx] if idx < len(distances) else None,
            }
        )
    return rows


def keyword_overlap_score(query: str, metadata: dict[str, Any]) -> float:
    text = " ".join(
        str(metadata.get(key) or "")
        for key in ["topic_hint", "nearby_text", "source_title", "priority", "image_name"]
    ).lower()
    lowered = query.lower()
    score = 0.0
    for token in set(lowered.replace("/", " ").replace("_", " ").split()):
        if len(token) >= 3 and token in text:
            score += 0.25
    for token in ["根音", "指型", "音程", "八度", "琶音", "三和弦", "七和弦", "六和弦", "九和弦", "五声音阶"]:
        if token in query and token in text:
            score += 0.75
    return score


def rerank_visual_rows(rows: list[dict[str, Any]], query: str, priority_scores: dict[str, float], limit: int) -> list[dict[str, Any]]:
    reranked = []
    for row in rows:
        meta = row["metadata"]
        priority = str(meta.get("priority") or "")
        score = priority_scores.get(priority, 0.0) + keyword_overlap_score(query, meta)
        row = dict(row)
        row["rerank_score"] = score
        reranked.append(row)
    reranked.sort(key=lambda row: (-float(row.get("rerank_score") or 0), float(row.get("distance") or 999)))
    return reranked[:limit]


def merge_rows(*groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for group in groups:
        for row in group:
            current = merged.get(row["id"])
            if current is None or float(row.get("distance") or 999) < float(current.get("distance") or 999):
                merged[row["id"]] = row
    return list(merged.values())


def query_collection_by_sources(collection, embedding: list[float], n_results: int, source_ids: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id in source_ids:
        rows.extend(query_collection(collection, embedding, n_results, where={"source_id": source_id}))
    rows = merge_rows(rows)
    rows.sort(key=lambda row: float(row.get("distance") or 999))
    return rows


def active_retrieval_mode(args: argparse.Namespace, test: dict[str, Any]) -> str:
    return str(test.get("retrieval_mode") or args.retrieval_mode)


def active_primary_sources(args: argparse.Namespace, test: dict[str, Any]) -> list[str]:
    sources = list(args.primary_source or [])
    sources.extend(str(source) for source in test.get("primary_sources", []) or [])
    if not sources and active_retrieval_mode(args, test) == "source_focus":
        sources.extend(str(source) for source in test.get("text_sources", []) or [])
    seen: set[str] = set()
    return [source for source in sources if source and not (source in seen or seen.add(source))]


def filter_text_rows(rows: list[dict[str, Any]], style_tags: list[str], limit: int) -> list[dict[str, Any]]:
    if not style_tags:
        return rows[:limit]
    wanted = set(style_tags)
    filtered = []
    for row in rows:
        tags = set(parse_jsonish_list(row["metadata"].get("style_tags")))
        if tags & wanted:
            filtered.append(row)
    return (filtered or rows)[:limit]


def source_ok(row: dict[str, Any], expected_sources: list[str]) -> bool:
    if not expected_sources:
        return False
    return row["metadata"].get("source_id") in set(expected_sources)


def visual_ok(row: dict[str, Any], sources: list[str], priorities: list[str]) -> bool:
    meta = row["metadata"]
    source_match = not sources or meta.get("source_id") in set(sources)
    priority_match = not priorities or meta.get("priority") in set(priorities)
    return source_match and priority_match


def summarize_text_row(row: dict[str, Any]) -> dict[str, Any]:
    meta = row["metadata"]
    doc = " ".join((row.get("document") or "").split())
    return {
        "id": row["id"],
        "distance": row["distance"],
        "source_id": meta.get("source_id"),
        "chunk_id": meta.get("chunk_id"),
        "title": meta.get("title") or meta.get("heading"),
        "style_tags": parse_jsonish_list(meta.get("style_tags")),
        "snippet": doc[:180],
    }


def summarize_visual_row(row: dict[str, Any]) -> dict[str, Any]:
    meta = row["metadata"]
    return {
        "id": row["id"],
        "distance": row["distance"],
        "rerank_score": row.get("rerank_score"),
        "source_id": meta.get("source_id"),
        "priority": meta.get("priority"),
        "page": meta.get("page_idx") or meta.get("page") or meta.get("page_number"),
        "topic": meta.get("topic_hint") or meta.get("topic") or meta.get("caption") or meta.get("image_type"),
        "nearby_text": meta.get("nearby_text"),
        "path": meta.get("image_path") or meta.get("path"),
    }


def load_kg_aliases(path: Path) -> dict[str, list[str]]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    aliases: dict[str, list[str]] = {}
    for key, values in data.items():
        if isinstance(values, list):
            aliases[key] = [str(value) for value in values]
    return aliases


def expand_kg_node_aliases(nodes: list[str], aliases: dict[str, list[str]]) -> list[str]:
    expanded: list[str] = []
    for node in nodes:
        if node not in expanded:
            expanded.append(node)
        for alias in aliases.get(node, []):
            if alias not in expanded:
                expanded.append(alias)
    return expanded


def query_neo4j(test: dict[str, Any]) -> dict[str, Any]:
    nodes = test.get("kg_nodes_any") or []
    if not nodes:
        return {"expected": [], "hits": [], "sample_edges": [], "available": False}
    aliases = load_kg_aliases(DEFAULT_KG_ALIASES)
    expanded_nodes = expand_kg_node_aliases(nodes, aliases)
    try:
        from neo4j import GraphDatabase
    except Exception as exc:
        return {"expected": nodes, "hits": [], "sample_edges": [], "available": False, "error": str(exc)}

    uri = first_env("NEO4J_URI", default="bolt://localhost:7687")
    user = first_env("NEO4J_USER", default="neo4j")
    password = first_env("NEO4J_PASSWORD")
    database = first_env("NEO4J_DATABASE", default="neo4j")
    if not password:
        return {"expected": nodes, "hits": [], "sample_edges": [], "available": False, "error": "Missing NEO4J_PASSWORD"}

    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session(database=database) as session:
            hit_rows = session.run(
                """
                MATCH (n)
                WHERE n.id IN $ids
                OPTIONAL MATCH (n)-[r]-()
                RETURN n.id AS id, labels(n) AS labels, count(r) AS degree
                ORDER BY degree DESC, id
                """,
                ids=expanded_nodes,
            ).data()
            edge_rows = session.run(
                """
                MATCH (a)-[r]-(b)
                WHERE a.id IN $ids OR b.id IN $ids
                RETURN coalesce(a.id, a.name) AS a, type(r) AS rel, coalesce(b.id, b.name) AS b
                LIMIT 6
                """,
                ids=expanded_nodes,
            ).data()
        driver.close()
        hits = [row for row in hit_rows if row.get("degree", 0) > 0]
        return {
            "expected": nodes,
            "expanded": expanded_nodes,
            "alias_hits": [node for node in expanded_nodes if node not in nodes],
            "hits": hits,
            "sample_edges": edge_rows,
            "available": True,
        }
    except Exception as exc:
        return {"expected": nodes, "expanded": expanded_nodes, "hits": [], "sample_edges": [], "available": False, "error": str(exc)}


@dataclass
class EvalTotals:
    tests: int = 0
    bundle_pass: int = 0
    text_tests: int = 0
    text_top1_pass: int = 0
    text_recall5_pass: int = 0
    text_precision5_sum: float = 0.0
    visual_tests: int = 0
    visual_top1_pass: int = 0
    visual_recall5_pass: int = 0
    visual_precision5_sum: float = 0.0
    kg_tests: int = 0
    kg_pass: int = 0
    duration_sum: float = 0.0
    text_duration_sum: float = 0.0
    visual_duration_sum: float = 0.0
    kg_duration_sum: float = 0.0


def pct(num: float, den: float) -> str:
    if not den:
        return "n/a"
    return f"{num / den * 100:.1f}%"


def pct_from_summary(summary: dict[str, Any], rate_key: str, count_key: str) -> str:
    rate = summary.get(rate_key)
    count = summary.get(count_key) or 0
    if rate is None or not count:
        return "n/a"
    return pct(rate * count, count)


def avg_from_summary(summary: dict[str, Any], key: str) -> str:
    value = summary.get(key)
    if value is None:
        return "n/a"
    return f"{value:.2f}"


def fmt_distance(value: Any) -> str:
    if value is None:
        return ""
    try:
        return f"{float(value):.4f}"
    except (TypeError, ValueError):
        return str(value)


def fmt_seconds(value: Any) -> str:
    if value is None:
        return "n/a"
    try:
        return f"{float(value):.2f}s"
    except (TypeError, ValueError):
        return str(value)


def run_eval(args: argparse.Namespace) -> dict[str, Any]:
    apply_env_file(ROOT / ".env")
    embedding_cache = EmbeddingCache(args.embedding_cache, enabled=not args.no_embedding_cache)
    client = chroma_client(args.chroma_dir)
    text_collection = client.get_collection(args.text_collection)
    visual_collection = client.get_collection(args.visual_collection)
    text_client_cls = LocalEmbeddingClient if args.text_embedding_provider == "local_qwen3" else EmbeddingClient
    text_embedder = text_client_cls(args.text_model, args.text_dimensions, args.timeout, cache=embedding_cache)
    visual_embedder = MultiModalEmbeddingClient(
        args.visual_model,
        args.visual_dimensions,
        args.timeout,
        cache=embedding_cache,
    )

    tests = load_tests(args.tests_file) if args.tests_file else TESTS
    tests = tests[: args.limit] if args.limit else tests
    results = []
    totals = EvalTotals(tests=len(tests))

    for index, test in enumerate(tests, start=1):
        test_started = time.perf_counter()
        timings: dict[str, float] = {}
        print(f"[{index}/{len(tests)}] {test['id']}", flush=True)
        style_tags = infer_style_tags(test["query"], test.get("style_tags") or [])
        retrieval_mode = active_retrieval_mode(args, test)
        primary_sources = active_primary_sources(args, test)

        text_started = time.perf_counter()
        text_embedding = text_embedder.embed_text(test["query"])
        timings["text_embedding_seconds"] = time.perf_counter() - text_started
        timings["text_embedding_cache_hit"] = text_embedder.last_cache_hit
        text_search_started = time.perf_counter()
        global_text_candidates = query_collection(text_collection, text_embedding, args.candidate_k)
        if retrieval_mode == "source_focus" and primary_sources:
            text_candidates = query_collection_by_sources(text_collection, text_embedding, args.candidate_k, primary_sources)
            support_text_top = [
                row
                for row in filter_text_rows(global_text_candidates, style_tags, args.top_k)
                if row["metadata"].get("source_id") not in set(primary_sources)
            ][: args.support_top_k]
        else:
            text_candidates = global_text_candidates
            support_text_top = []
        text_top = filter_text_rows(text_candidates, style_tags, args.top_k)
        timings["text_search_seconds"] = time.perf_counter() - text_search_started
        timings["text_total_seconds"] = timings["text_embedding_seconds"] + timings["text_search_seconds"]
        text_expected = test.get("text_sources") or []
        text_hits = [row for row in text_top if source_ok(row, text_expected)]
        text_top1_ok = bool(text_top and source_ok(text_top[0], text_expected))
        text_recall5_ok = bool(text_hits)
        text_precision = len(text_hits) / max(len(text_top), 1) if text_expected else None

        visual_top = []
        visual_hits: list[dict[str, Any]] = []
        visual_top1_ok = None
        visual_recall5_ok = None
        visual_precision = None
        if test.get("visual_sources") or test.get("visual_priorities"):
            visual_started = time.perf_counter()
            inferred_priorities = infer_visual_priorities(test["query"])
            priority_scores = score_visual_priorities(test["query"])
            visual_where = {"source_id": test["visual_sources"][0]} if len(test.get("visual_sources") or []) == 1 else None
            if args.no_visual_intent_filter:
                visual_where = None
            visual_embedding_started = time.perf_counter()
            visual_embedding = visual_embedder.embed_text(test["query"])
            timings["visual_embedding_seconds"] = time.perf_counter() - visual_embedding_started
            timings["visual_embedding_cache_hit"] = visual_embedder.last_cache_hit
            visual_search_started = time.perf_counter()
            visual_candidates = query_collection(visual_collection, visual_embedding, args.candidate_k, where=visual_where)
            if inferred_priorities and not args.no_visual_intent_filter:
                priority_candidates: list[dict[str, Any]] = []
                for priority in inferred_priorities[: args.max_visual_priority_probes]:
                    priority_where = chroma_where(test.get("visual_sources") or [], [priority])
                    priority_candidates.extend(
                        query_collection(
                            visual_collection,
                            visual_embedding,
                            max(args.top_k, args.visual_priority_probe_k),
                            where=priority_where,
                        )
                    )
                visual_candidates = merge_rows(visual_candidates, priority_candidates)
            visual_top = rerank_visual_rows(visual_candidates, test["query"], priority_scores, args.top_k)
            timings["visual_search_seconds"] = time.perf_counter() - visual_search_started
            timings["visual_total_seconds"] = time.perf_counter() - visual_started
            visual_hits = [
                row
                for row in visual_top
                if visual_ok(row, test.get("visual_sources") or [], test.get("visual_priorities") or [])
            ]
            visual_top1_ok = bool(
                visual_top and visual_ok(visual_top[0], test.get("visual_sources") or [], test.get("visual_priorities") or [])
            )
            visual_recall5_ok = bool(visual_hits)
            visual_precision = len(visual_hits) / max(len(visual_top), 1)

        kg_started = time.perf_counter()
        kg = query_neo4j(test)
        timings["kg_seconds"] = time.perf_counter() - kg_started
        kg_expected = bool(test.get("kg_nodes_any"))
        kg_ok = bool(kg.get("hits")) if kg_expected and kg.get("available") else None

        text_ok_for_bundle = text_recall5_ok if text_expected else True
        visual_ok_for_bundle = visual_recall5_ok if (test.get("visual_sources") or test.get("visual_priorities")) else True
        kg_ok_for_bundle = kg_ok if kg_expected and kg_ok is not None else True
        bundle_ok = bool(text_ok_for_bundle and visual_ok_for_bundle and kg_ok_for_bundle)

        if text_expected:
            totals.text_tests += 1
            totals.text_top1_pass += int(text_top1_ok)
            totals.text_recall5_pass += int(text_recall5_ok)
            totals.text_precision5_sum += float(text_precision or 0)
        if test.get("visual_sources") or test.get("visual_priorities"):
            totals.visual_tests += 1
            totals.visual_top1_pass += int(bool(visual_top1_ok))
            totals.visual_recall5_pass += int(bool(visual_recall5_ok))
            totals.visual_precision5_sum += float(visual_precision or 0)
        if kg_expected and kg_ok is not None:
            totals.kg_tests += 1
            totals.kg_pass += int(bool(kg_ok))
        timings["total_seconds"] = time.perf_counter() - test_started
        totals.duration_sum += timings["total_seconds"]
        totals.text_duration_sum += timings.get("text_total_seconds", 0.0)
        totals.visual_duration_sum += timings.get("visual_total_seconds", 0.0)
        totals.kg_duration_sum += timings.get("kg_seconds", 0.0)
        totals.bundle_pass += int(bundle_ok)

        results.append(
            {
                "id": test["id"],
                "query": test["query"],
                "retrieval_mode": retrieval_mode,
                "primary_sources": primary_sources,
                "style_tags": style_tags,
                "expected": {
                    "text_sources": text_expected,
                    "visual_sources": test.get("visual_sources") or [],
                    "visual_priorities": test.get("visual_priorities") or [],
                    "inferred_visual_priorities": infer_visual_priorities(test["query"]),
                    "visual_priority_scores": score_visual_priorities(test["query"]),
                    "kg_nodes_any": test.get("kg_nodes_any") or [],
                },
                "metrics": {
                    "text_top1_ok": text_top1_ok,
                    "text_recall5_ok": text_recall5_ok,
                    "text_precision5": text_precision,
                    "visual_top1_ok": visual_top1_ok,
                    "visual_recall5_ok": visual_recall5_ok,
                    "visual_precision5": visual_precision,
                    "kg_ok": kg_ok,
                    "bundle_ok": bundle_ok,
                },
                "timings": timings,
                "text_top": [summarize_text_row(row) for row in text_top],
                "support_text_top": [summarize_text_row(row) for row in support_text_top],
                "visual_top": [summarize_visual_row(row) for row in visual_top],
                "kg": kg,
            }
        )
        time.sleep(args.pause)

    summary = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "retrieval_mode": args.retrieval_mode,
        "primary_sources": args.primary_source,
        "tests": totals.tests,
        "bundle_pass": totals.bundle_pass,
        "bundle_pass_rate": totals.bundle_pass / totals.tests if totals.tests else None,
        "text_tests": totals.text_tests,
        "text_top1_accuracy": totals.text_top1_pass / totals.text_tests if totals.text_tests else None,
        "text_recall_at_5": totals.text_recall5_pass / totals.text_tests if totals.text_tests else None,
        "text_precision_at_5_avg": totals.text_precision5_sum / totals.text_tests if totals.text_tests else None,
        "visual_tests": totals.visual_tests,
        "visual_top1_accuracy": totals.visual_top1_pass / totals.visual_tests if totals.visual_tests else None,
        "visual_recall_at_5": totals.visual_recall5_pass / totals.visual_tests if totals.visual_tests else None,
        "visual_precision_at_5_avg": totals.visual_precision5_sum / totals.visual_tests if totals.visual_tests else None,
        "kg_tests": totals.kg_tests,
        "kg_hit_rate": totals.kg_pass / totals.kg_tests if totals.kg_tests else None,
        "duration_seconds_total": totals.duration_sum,
        "duration_seconds_avg": totals.duration_sum / totals.tests if totals.tests else None,
        "text_seconds_avg": totals.text_duration_sum / totals.text_tests if totals.text_tests else None,
        "visual_seconds_avg": totals.visual_duration_sum / totals.visual_tests if totals.visual_tests else None,
        "kg_seconds_avg": totals.kg_duration_sum / totals.kg_tests if totals.kg_tests else None,
        "embedding_cache": embedding_cache.stats(),
    }
    return {"summary": summary, "results": results}


def yn(value: Any) -> str:
    if value is True:
        return "OK"
    if value is False:
        return "MISS"
    return "n/a"


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Retrieval Bundle 小规模评测",
        "",
        f"- 生成时间：{summary['generated_at']}",
        f"- 检索模式：`{summary.get('retrieval_mode', 'global')}`",
        f"- CLI primary sources：{', '.join(summary.get('primary_sources') or []) or 'n/a'}",
        f"- 测试数：{summary['tests']}",
        f"- Bundle 通过率：{summary['bundle_pass']}/{summary['tests']} ({pct(summary['bundle_pass'], summary['tests'])})",
        f"- 文本 Top1 准确率：{pct_from_summary(summary, 'text_top1_accuracy', 'text_tests')}",
        f"- 文本 Recall@5：{pct_from_summary(summary, 'text_recall_at_5', 'text_tests')}",
        f"- 文本 Precision@5 平均：{avg_from_summary(summary, 'text_precision_at_5_avg')}",
        f"- 视觉 Top1 准确率：{pct_from_summary(summary, 'visual_top1_accuracy', 'visual_tests')}",
        f"- 视觉 Recall@5：{pct_from_summary(summary, 'visual_recall_at_5', 'visual_tests')}",
        f"- 视觉 Precision@5 平均：{avg_from_summary(summary, 'visual_precision_at_5_avg')}",
        f"- Neo4j 预期节点命中率：{pct_from_summary(summary, 'kg_hit_rate', 'kg_tests')}",
        f"- 总耗时：{fmt_seconds(summary.get('duration_seconds_total'))}",
        f"- 单条平均耗时：{fmt_seconds(summary.get('duration_seconds_avg'))}",
        f"- 文本平均耗时：{fmt_seconds(summary.get('text_seconds_avg'))}",
        f"- 视觉平均耗时：{fmt_seconds(summary.get('visual_seconds_avg'))}",
        f"- Neo4j 平均耗时：{fmt_seconds(summary.get('kg_seconds_avg'))}",
        f"- Embedding 缓存：{summary.get('embedding_cache', {}).get('rows', 0)} 条，路径 `{summary.get('embedding_cache', {}).get('path', '')}`",
        "",
        "## 总览",
        "",
        "| 用例 | 文本Top1 | 文本R@5 | 视觉Top1 | 视觉R@5 | KG | Bundle | 耗时 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for item in report["results"]:
        metrics = item["metrics"]
        timings = item.get("timings") or {}
        lines.append(
            f"| {item['id']} | {yn(metrics['text_top1_ok'])} | {yn(metrics['text_recall5_ok'])} | "
            f"{yn(metrics['visual_top1_ok'])} | {yn(metrics['visual_recall5_ok'])} | "
            f"{yn(metrics['kg_ok'])} | {yn(metrics['bundle_ok'])} | {fmt_seconds(timings.get('total_seconds'))} |"
        )

    lines.extend(["", "## 明细", ""])
    for item in report["results"]:
        metrics = item["metrics"]
        expected = item["expected"]
        lines.extend(
            [
                f"### {item['id']}",
                "",
                f"- 查询：`{item['query']}`",
                f"- 检索模式：`{item.get('retrieval_mode', 'global')}`",
                f"- Primary sources：{', '.join(item.get('primary_sources') or []) or 'n/a'}",
                f"- 期望文本源：{', '.join(expected['text_sources']) or 'n/a'}",
                f"- 期望视觉：{', '.join(expected['visual_priorities']) or 'n/a'}",
                f"- 结果：文本R@5={yn(metrics['text_recall5_ok'])}，视觉R@5={yn(metrics['visual_recall5_ok'])}，KG={yn(metrics['kg_ok'])}，Bundle={yn(metrics['bundle_ok'])}",
                f"- 耗时：total={fmt_seconds((item.get('timings') or {}).get('total_seconds'))}，text={fmt_seconds((item.get('timings') or {}).get('text_total_seconds'))}，visual={fmt_seconds((item.get('timings') or {}).get('visual_total_seconds'))}，kg={fmt_seconds((item.get('timings') or {}).get('kg_seconds'))}",
                f"- 缓存：text_embedding={yn((item.get('timings') or {}).get('text_embedding_cache_hit'))}，visual_embedding={yn((item.get('timings') or {}).get('visual_embedding_cache_hit'))}",
                "",
                "文本 Top5：",
            ]
        )
        for rank, row in enumerate(item["text_top"], start=1):
            lines.append(
                f"{rank}. `{row['source_id']}` / `{row['chunk_id']}` / dist={fmt_distance(row['distance'])} / "
                f"{row.get('title') or ''}  \n   {row.get('snippet') or ''}"
            )
        if item.get("support_text_top"):
            lines.append("")
            lines.append("Support 文本 Top：")
            for rank, row in enumerate(item["support_text_top"], start=1):
                lines.append(
                    f"{rank}. `{row['source_id']}` / `{row['chunk_id']}` / dist={fmt_distance(row['distance'])} / "
                    f"{row.get('title') or ''}  \n   {row.get('snippet') or ''}"
                )
        if item["visual_top"]:
            lines.append("")
            lines.append("视觉 Top5：")
            if expected.get("inferred_visual_priorities"):
                lines.append(f"- 推断 priority：{', '.join(expected['inferred_visual_priorities'])}")
            for rank, row in enumerate(item["visual_top"], start=1):
                lines.append(
                    f"{rank}. `{row['priority']}` / page={row.get('page') or ''} / dist={fmt_distance(row['distance'])} / rerank={fmt_distance(row.get('rerank_score'))} / "
                    f"{row.get('topic') or ''}  \n   `{row.get('path') or row.get('id')}`"
                )
        kg = item["kg"]
        if expected["kg_nodes_any"]:
            lines.append("")
            lines.append("Neo4j：")
            if kg.get("error"):
                lines.append(f"- 检查失败：{kg['error']}")
            else:
                hit_ids = [row.get("id") for row in kg.get("hits", [])]
                lines.append(f"- 命中节点：{', '.join(hit_ids) or '无'}")
                if kg.get("expanded"):
                    expanded_only = [node for node in kg["expanded"] if node not in expected["kg_nodes_any"]]
                    if expanded_only:
                        lines.append(f"- Alias 扩展：{', '.join(expanded_only[:8])}")
                for edge in kg.get("sample_edges", [])[:3]:
                    lines.append(f"- 关系样例：`{edge.get('a')}` -[{edge.get('rel')}]- `{edge.get('b')}`")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def load_tests(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("tests", [])
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON array or an object with a tests array")
    tests: list[dict[str, Any]] = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"test #{index} is not an object")
        if "id" not in item and "name" in item:
            item["id"] = item["name"]
        if "id" not in item or "query" not in item:
            raise ValueError(f"test #{index} must contain id/name and query")
        tests.append(item)
    return tests


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate text Chroma + visual Chroma + Neo4j retrieval coverage.")
    parser.add_argument("--chroma-dir", type=Path, default=DEFAULT_CHROMA_DIR)
    parser.add_argument("--text-collection", default="guitar_text_chunks")
    parser.add_argument("--visual-collection", default="guitar_visual_chunks")
    parser.add_argument("--text-embedding-provider", choices=["api", "local_qwen3"], default="api")
    parser.add_argument("--text-model", default=first_env("EMBEDDING_MODEL", default="text-embedding-v4"))
    parser.add_argument("--visual-model", default=first_env("VISUAL_EMBEDDING_MODEL", default="qwen3-vl-embedding"))
    parser.add_argument("--text-dimensions", type=int, default=1024)
    parser.add_argument("--visual-dimensions", type=int, default=1024)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--candidate-k", type=int, default=25)
    parser.add_argument("--visual-priority-probe-k", type=int, default=8)
    parser.add_argument("--max-visual-priority-probes", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--pause", type=float, default=0.2)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--tests-file", type=Path, help="Optional JSON file containing custom evaluation tests")
    parser.add_argument(
        "--retrieval-mode",
        choices=["global", "source_focus"],
        default="global",
        help="global keeps open retrieval; source_focus evaluates a primary source pool plus support evidence.",
    )
    parser.add_argument("--primary-source", action="append", default=[], help="Primary source_id for source_focus mode")
    parser.add_argument("--support-top-k", type=int, default=3, help="Support text rows shown in source_focus mode")
    parser.add_argument("--no-visual-intent-filter", action="store_true")
    parser.add_argument("--embedding-cache", type=Path, default=DEFAULT_EMBEDDING_CACHE)
    parser.add_argument("--no-embedding-cache", action="store_true")
    parser.add_argument("--out-md", type=Path, default=DEFAULT_REPORT_MD)
    parser.add_argument("--out-json", type=Path, default=DEFAULT_REPORT_JSON)
    args = parser.parse_args()

    report = run_eval(args)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    args.out_md.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    print(f"wrote {args.out_md}")
    print(f"wrote {args.out_json}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
