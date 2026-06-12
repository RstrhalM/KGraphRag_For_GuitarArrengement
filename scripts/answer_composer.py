#!/usr/bin/env python
"""Compose a grounded guitar-arrangement answer from a RAG evidence bundle."""

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

SYSTEM_PROMPT = load_prompt("answer_composer")


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


def compact(value: Any, limit: int = 900) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text if len(text) <= limit else text[: limit - 3] + "..."


def as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value in (None, ""):
        return []
    return [value]


def normalize_answer(answer: dict[str, Any]) -> dict[str, Any]:
    return {
        "summary": str(answer.get("summary") or "").strip(),
        "answer": str(answer.get("answer") or "").strip(),
        "evidence_used": [item for item in as_list(answer.get("evidence_used")) if isinstance(item, dict)],
        "fretboard_options": [item for item in as_list(answer.get("fretboard_options")) if isinstance(item, dict)],
        "style_arrangement_advice": [item for item in as_list(answer.get("style_arrangement_advice")) if isinstance(item, dict)],
        "kg_reasoning": [item for item in as_list(answer.get("kg_reasoning")) if isinstance(item, dict)],
        "theory_checks": [str(item) for item in as_list(answer.get("theory_checks")) if str(item).strip()],
        "uncertainties": [str(item) for item in as_list(answer.get("uncertainties")) if str(item).strip()],
        "next_steps": [str(item) for item in as_list(answer.get("next_steps")) if str(item).strip()],
    }


def evidence_rows(bundle: dict[str, Any], group_name: str, limit: int, content_limit: int) -> list[dict[str, Any]]:
    rows = []
    for item in as_list(bundle.get(group_name))[:limit]:
        if not isinstance(item, dict):
            continue
        metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
        rows.append(
            {
                "evidence_id": item.get("evidence_id", ""),
                "evidence_type": item.get("evidence_type", ""),
                "source_id": item.get("source_id", ""),
                "title": item.get("title", ""),
                "score": item.get("score", 0),
                "content": compact(item.get("content", ""), content_limit),
                "canonical_terms": metadata.get("canonical_terms", []),
                "domain_rerank": metadata.get("domain_rerank", {}),
                "model_rerank": metadata.get("model_rerank", {}),
            }
        )
    return rows


def build_compose_payload(bundle: dict[str, Any], evidence_limit: int = 6, content_limit: int = 900) -> dict[str, Any]:
    return {
        "query": bundle.get("query", ""),
        "analysis": bundle.get("analysis", {}),
        "query_plan": bundle.get("query_plan", {}),
        "judgement": bundle.get("judgement", {}),
        "answer_seed": bundle.get("answer_seed", {}),
        "rerank_config": bundle.get("rerank_config", {}),
        "evidence": {
            "text": evidence_rows(bundle, "text_evidence", evidence_limit, content_limit),
            "visual": evidence_rows(bundle, "visual_evidence", evidence_limit, content_limit),
            "kg": evidence_rows(bundle, "kg_evidence", evidence_limit, content_limit),
        },
    }


def build_user_prompt(bundle: dict[str, Any]) -> str:
    payload = build_compose_payload(bundle)
    return (
        "请基于下面 evidence bundle 生成最终编曲建议答案。\n\n"
        "要求：\n"
        "- 必须引用 evidence_id。\n"
        "- 回答要面向吉他编曲用户，给出可操作建议。\n"
        "- 如果视觉证据是练习答案图，只把它当作指型/把位/voicing 参考。\n"
        "- 涉及具体音名、级数、和弦内音、tension 时必须在 theory_checks 里自检。\n"
        "- 如果 judgement.missing 非空，必须在 uncertainties 中说明。\n"
        "- 输出合法 JSON。\n\n"
        f"Evidence bundle:\n{json.dumps(payload, ensure_ascii=False, indent=2)}"
    )


class AnswerComposerClient:
    def __init__(self, env_file: Path = Path(".env")) -> None:
        apply_env_file(env_file)
        self.base_url = os.environ.get("LLM_API_BASE_URL", "").rstrip("/")
        self.api_key = os.environ.get("LLM_API_KEY", "")
        self.model = os.environ.get("ANSWER_COMPOSER_MODEL", os.environ.get("LLM_MODEL", ""))
        self.temperature = float(os.environ.get("ANSWER_COMPOSER_TEMPERATURE", "0.2"))
        self.timeout = int(os.environ.get("ANSWER_COMPOSER_TIMEOUT_SECONDS", os.environ.get("LLM_TIMEOUT_SECONDS", "120")))
        self.max_retries = int(os.environ.get("ANSWER_COMPOSER_MAX_RETRIES", os.environ.get("LLM_MAX_RETRIES", "1")))
        self.max_output_tokens = int(os.environ.get("ANSWER_COMPOSER_MAX_OUTPUT_TOKENS", "8192"))
        self.enable_thinking = os.environ.get("ANSWER_COMPOSER_ENABLE_THINKING", os.environ.get("LLM_ENABLE_THINKING", "false")).strip().lower() == "true"
        if not self.base_url or not self.model:
            raise ValueError("LLM_API_BASE_URL and LLM_MODEL or ANSWER_COMPOSER_MODEL must be set in .env")

    def chat_json(self, bundle: dict[str, Any]) -> dict[str, Any]:
        request_payload: dict[str, Any] = {
            "model": self.model,
            "temperature": self.temperature,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(bundle)},
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
                return normalize_answer(extract_json_object(data["choices"][0]["message"]["content"]))
            except (urllib.error.URLError, urllib.error.HTTPError, KeyError, json.JSONDecodeError, ValueError) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(1.5 * (attempt + 1))
        raise RuntimeError(f"Answer composer LLM request failed: {last_error}")


def compose_answer(bundle: dict[str, Any], env_file: Path = Path(".env")) -> dict[str, Any]:
    client = AnswerComposerClient(env_file)
    answer = client.chat_json(bundle)
    answer["composer"] = {
        "provider": "llm_api",
        "model": client.model,
        "temperature": client.temperature,
        "prompt_version": get_prompt_versions()["answer_composer"],
    }
    answer["prompt_versions"] = {"answer_composer": get_prompt_versions()["answer_composer"]}
    return answer


def render_answer_markdown(answer: dict[str, Any]) -> str:
    lines = ["", "## Composed Answer", ""]
    if not answer:
        lines.append("未生成答案。")
        return "\n".join(lines)
    lines.extend([f"**Summary:** {answer.get('summary', '')}", "", str(answer.get("answer", "")), ""])
    for title, key in [
        ("Evidence Used", "evidence_used"),
        ("Fretboard Options", "fretboard_options"),
        ("Style Arrangement Advice", "style_arrangement_advice"),
        ("KG Reasoning", "kg_reasoning"),
        ("Theory Checks", "theory_checks"),
        ("Uncertainties", "uncertainties"),
        ("Next Steps", "next_steps"),
    ]:
        values = as_list(answer.get(key))
        lines.extend([f"### {title}", ""])
        if not values:
            lines.append("- 无")
        elif all(isinstance(item, dict) for item in values):
            for item in values:
                lines.append(f"- `{json.dumps(item, ensure_ascii=False)}`")
        else:
            for item in values:
                lines.append(f"- {item}")
        lines.append("")
    lines.extend(["### Raw JSON", "", "```json", json.dumps(answer, ensure_ascii=False, indent=2), "```", ""])
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle-json", type=Path, required=True)
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    parser.add_argument("--out-json", type=Path, default=Path("data/eval/answer_composer_smoke.json"))
    parser.add_argument("--out-md", type=Path, default=Path("data/eval/answer_composer_smoke.md"))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    bundle = json.loads(args.bundle_json.read_text(encoding="utf-8"))
    answer = compose_answer(bundle, env_file=args.env_file)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(answer, ensure_ascii=False, indent=2), encoding="utf-8")
    args.out_md.write_text(render_answer_markdown(answer), encoding="utf-8")
    print(json.dumps({"out_json": str(args.out_json), "out_md": str(args.out_md)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
