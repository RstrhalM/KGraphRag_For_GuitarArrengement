#!/usr/bin/env python
"""Versioned prompt registry for Agentic RAG sub-agents."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from functools import lru_cache
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = ROOT / "prompts"


@dataclass(frozen=True)
class PromptSpec:
    agent: str
    version: str
    file: str
    status: str = "active"

    @property
    def path(self) -> Path:
        return PROMPTS_DIR / self.file


PROMPT_REGISTRY: dict[str, PromptSpec] = {
    "query_normalizer": PromptSpec(
        agent="query_normalizer",
        version="query_normalizer_v1.1",
        file="query_normalizer_v1.1.md",
    ),
    "answer_composer": PromptSpec(
        agent="answer_composer",
        version="answer_composer_v1.0",
        file="answer_composer_v1.0.md",
    ),
    "answer_verifier": PromptSpec(
        agent="answer_verifier",
        version="answer_verifier_v0.1",
        file="answer_verifier_v0.1.md",
        status="planned",
    ),
}


@lru_cache(maxsize=16)
def load_prompt(agent: str) -> str:
    spec = PROMPT_REGISTRY[agent]
    return spec.path.read_text(encoding="utf-8").strip()


def get_prompt_spec(agent: str) -> dict[str, Any]:
    spec = PROMPT_REGISTRY[agent]
    data = asdict(spec)
    data["path"] = str(spec.path.relative_to(ROOT))
    return data


def get_prompt_versions(include_planned: bool = True) -> dict[str, str]:
    return {
        agent: spec.version
        for agent, spec in PROMPT_REGISTRY.items()
        if include_planned or spec.status == "active"
    }


def get_prompt_registry() -> dict[str, dict[str, Any]]:
    return {agent: get_prompt_spec(agent) for agent in PROMPT_REGISTRY}
