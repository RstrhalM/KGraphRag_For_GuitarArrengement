#!/usr/bin/env python
"""Optional local cross-encoder rerank backend for RAG evidence items."""

from __future__ import annotations

import math
import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any


DEFAULT_RERANK_MODEL = "models/reranker/qwen3-reranker-0.6b"


@dataclass
class RerankConfig:
    backend: str = "none"
    model: str = DEFAULT_RERANK_MODEL
    device: str = "auto"
    batch_size: int = 8
    max_length: int = 1024
    weight: float = 0.45
    instruction: str = (
        "Given a guitar arrangement query, retrieve textbook passages, visual captions, "
        "or knowledge graph evidence that directly help answer the query."
    )
    enabled_types: tuple[str, ...] = ("text", "visual_caption", "kg")

    @classmethod
    def from_env(cls) -> "RerankConfig":
        enabled_types = tuple(
            item.strip()
            for item in os.environ.get("RERANK_ENABLED_TYPES", "text,visual_caption,kg").split(",")
            if item.strip()
        )
        return cls(
            backend=os.environ.get("RERANK_BACKEND", "none").strip().lower(),
            model=os.environ.get("RERANK_MODEL", DEFAULT_RERANK_MODEL),
            device=os.environ.get("RERANK_DEVICE", "auto"),
            batch_size=int(os.environ.get("RERANK_BATCH_SIZE", "8")),
            max_length=int(os.environ.get("RERANK_MAX_LENGTH", "1024")),
            weight=float(os.environ.get("RERANK_WEIGHT", "0.45")),
            instruction=os.environ.get(
                "RERANK_INSTRUCTION",
                "Given a guitar arrangement query, retrieve textbook passages, visual captions, "
                "or knowledge graph evidence that directly help answer the query.",
            ),
            enabled_types=enabled_types or ("text", "visual_caption", "kg"),
        )


def sigmoid(value: float) -> float:
    if value >= 0:
        z = math.exp(-value)
        return 1 / (1 + z)
    z = math.exp(value)
    return z / (1 + z)


def evidence_text_for_rerank(item: Any, limit: int = 1600) -> str:
    parts = [
        f"type: {getattr(item, 'evidence_type', '')}",
        f"source: {getattr(item, 'source_id', '')}",
        f"title: {getattr(item, 'title', '')}",
        f"content: {getattr(item, 'content', '')}",
    ]
    metadata = getattr(item, "metadata", {}) or {}
    canonical_terms = metadata.get("canonical_terms")
    if canonical_terms:
        parts.append(f"canonical_terms: {canonical_terms}")
    if metadata.get("canonical_retrieval"):
        parts.append(f"canonical_retrieval: {metadata.get('canonical_retrieval')}")
    text = "\n".join(str(part) for part in parts if part)
    return text if len(text) <= limit else text[: limit - 3] + "..."


class BaseReranker:
    provider = "none"

    def score_pairs(self, query: str, docs: list[str]) -> list[float]:
        return [0.0 for _ in docs]


class SentenceTransformersReranker(BaseReranker):
    provider = "sentence_transformers"

    def __init__(self, config: RerankConfig) -> None:
        from sentence_transformers import CrossEncoder

        device = None if config.device == "auto" else config.device
        self.model = CrossEncoder(config.model, device=device, max_length=config.max_length)
        self.batch_size = config.batch_size

    def score_pairs(self, query: str, docs: list[str]) -> list[float]:
        pairs = [(query, doc) for doc in docs]
        scores = self.model.predict(pairs, batch_size=self.batch_size, show_progress_bar=False)
        return [float(score) for score in scores]


class TransformersSequenceReranker(BaseReranker):
    provider = "transformers_sequence_classification"

    def __init__(self, config: RerankConfig) -> None:
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(config.model, local_files_only=True, trust_remote_code=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            config.model,
            local_files_only=True,
            trust_remote_code=True,
        )
        if config.device != "auto":
            self.device = torch.device(config.device)
        else:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()
        self.batch_size = config.batch_size
        self.max_length = config.max_length

    def score_pairs(self, query: str, docs: list[str]) -> list[float]:
        scores: list[float] = []
        with self.torch.no_grad():
            for start in range(0, len(docs), self.batch_size):
                batch_docs = docs[start : start + self.batch_size]
                encoded = self.tokenizer(
                    [query] * len(batch_docs),
                    batch_docs,
                    padding=True,
                    truncation=True,
                    max_length=self.max_length,
                    return_tensors="pt",
                ).to(self.device)
                logits = self.model(**encoded).logits
                if logits.shape[-1] == 1:
                    batch_scores = logits.squeeze(-1).detach().cpu().tolist()
                else:
                    batch_scores = logits[:, -1].detach().cpu().tolist()
                if isinstance(batch_scores, float):
                    batch_scores = [batch_scores]
                scores.extend(float(score) for score in batch_scores)
        return scores


class Qwen3CausalReranker(BaseReranker):
    provider = "qwen3_causal_lm"

    def __init__(self, config: RerankConfig) -> None:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(
            config.model,
            local_files_only=True,
            padding_side="left",
            trust_remote_code=True,
        )
        if config.device != "auto":
            self.device = torch.device(config.device)
        else:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = AutoModelForCausalLM.from_pretrained(
            config.model,
            local_files_only=True,
            dtype="auto",
            trust_remote_code=True,
        )
        self.model.to(self.device)
        self.model.eval()
        self.batch_size = config.batch_size
        self.max_length = config.max_length
        self.instruction = config.instruction
        self.token_false_id = self.tokenizer.convert_tokens_to_ids("no")
        self.token_true_id = self.tokenizer.convert_tokens_to_ids("yes")
        prefix = (
            "<|im_start|>system\n"
            'Judge whether the Document meets the requirements based on the Query and the Instruct provided. '
            'Note that the answer can only be "yes" or "no".'
            "<|im_end|>\n<|im_start|>user\n"
        )
        suffix = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
        self.prefix_tokens = self.tokenizer.encode(prefix, add_special_tokens=False)
        self.suffix_tokens = self.tokenizer.encode(suffix, add_special_tokens=False)

    def format_instruction(self, query: str, doc: str) -> str:
        return f"<Instruct>: {self.instruction}\n<Query>: {query}\n<Document>: {doc}"

    def process_inputs(self, pairs: list[str]) -> Any:
        body_max_length = max(32, self.max_length - len(self.prefix_tokens) - len(self.suffix_tokens))
        inputs = self.tokenizer(
            pairs,
            padding=False,
            truncation="longest_first",
            return_attention_mask=False,
            max_length=body_max_length,
        )
        for index, ids in enumerate(inputs["input_ids"]):
            inputs["input_ids"][index] = self.prefix_tokens + ids + self.suffix_tokens
        padded = self.tokenizer.pad(inputs, padding=True, return_tensors="pt")
        return {key: value.to(self.device) for key, value in padded.items()}

    def score_pairs(self, query: str, docs: list[str]) -> list[float]:
        scores: list[float] = []
        with self.torch.no_grad():
            for start in range(0, len(docs), self.batch_size):
                batch_docs = docs[start : start + self.batch_size]
                pairs = [self.format_instruction(query, doc) for doc in batch_docs]
                inputs = self.process_inputs(pairs)
                batch_logits = self.model(**inputs).logits[:, -1, :]
                true_logits = batch_logits[:, self.token_true_id]
                false_logits = batch_logits[:, self.token_false_id]
                logit_diff = (true_logits - false_logits).detach().float().cpu().tolist()
                if isinstance(logit_diff, float):
                    logit_diff = [logit_diff]
                scores.extend(float(score) for score in logit_diff)
        return scores


@lru_cache(maxsize=1)
def get_reranker(config_key: tuple[Any, ...]) -> BaseReranker:
    config = RerankConfig(
        backend=config_key[0],
        model=config_key[1],
        device=config_key[2],
        batch_size=config_key[3],
        max_length=config_key[4],
        weight=config_key[5],
        instruction=config_key[6],
        enabled_types=tuple(config_key[7]),
    )
    if config.backend in {"", "none", "off", "false"}:
        return BaseReranker()
    if config.backend != "local":
        return BaseReranker()
    try:
        return SentenceTransformersReranker(config)
    except Exception:
        try:
            return Qwen3CausalReranker(config)
        except Exception:
            try:
                return TransformersSequenceReranker(config)
            except Exception:
                return BaseReranker()


def config_cache_key(config: RerankConfig) -> tuple[Any, ...]:
    return (
        config.backend,
        config.model,
        config.device,
        config.batch_size,
        config.max_length,
        config.weight,
        config.instruction,
        config.enabled_types,
    )


def apply_model_rerank(query: str, items: list[Any], config: RerankConfig | None = None) -> tuple[list[Any], dict[str, Any]]:
    config = config or RerankConfig.from_env()
    if config.backend in {"", "none", "off", "false"} or not items:
        return items, {"enabled": False, "provider": "none", "reason": "disabled"}

    eligible = [item for item in items if getattr(item, "evidence_type", "") in config.enabled_types]
    if not eligible:
        return items, {"enabled": False, "provider": "none", "reason": "no_eligible_items"}

    reranker = get_reranker(config_cache_key(config))
    if reranker.provider == "none":
        return items, {"enabled": False, "provider": "none", "reason": "backend_unavailable"}

    docs = [evidence_text_for_rerank(item) for item in eligible]
    raw_scores = reranker.score_pairs(query, docs)
    normalized_scores = [sigmoid(score) for score in raw_scores]
    by_id = {id(item): (raw, norm) for item, raw, norm in zip(eligible, raw_scores, normalized_scores)}
    for item in items:
        raw, normalized = by_id.get(id(item), (None, None))
        if raw is None or normalized is None:
            continue
        original_score = float(getattr(item, "score", 0.0) or 0.0)
        item.score = round(original_score + normalized * config.weight, 5)
        metadata = getattr(item, "metadata", None)
        if isinstance(metadata, dict):
            metadata["model_rerank"] = {
                "provider": reranker.provider,
                "model": config.model,
                "raw_score": raw,
                "normalized_score": normalized,
                "weight": config.weight,
                "delta": round(normalized * config.weight, 5),
            }
    items.sort(key=lambda entry: float(getattr(entry, "score", 0.0) or 0.0), reverse=True)
    return items, {
        "enabled": True,
        "provider": reranker.provider,
        "model": config.model,
        "count": len(eligible),
        "weight": config.weight,
    }
