from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

import torch


DEFAULT_LOCAL_MODEL = "Qwen/Qwen3-Embedding-0.6B"


class LocalTransformerEmbedder:
    """Local text embedding backend using Transformers mean pooling.

    This keeps the project independent from hosted embedding APIs for text
    retrieval experiments. It intentionally exposes the same ``embed(list[str])``
    shape as the existing Chroma ingestion embedders.
    """

    def __init__(
        self,
        model_name_or_path: str = DEFAULT_LOCAL_MODEL,
        *,
        device: str = "auto",
        max_length: int = 2048,
        normalize: bool = True,
        trust_remote_code: bool = True,
    ) -> None:
        try:
            from transformers import AutoModel, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError("Missing dependency: install transformers and torch") from exc

        self.model_name_or_path = model_name_or_path
        self.max_length = max_length
        self.normalize = normalize
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device

        started = time.perf_counter()
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=trust_remote_code)
        self.model = AutoModel.from_pretrained(model_name_or_path, trust_remote_code=trust_remote_code)
        self.model.eval()
        self.model.to(self.device)
        self.load_seconds = time.perf_counter() - started

    @staticmethod
    def _mean_pool(last_hidden_state: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        mask = attention_mask.unsqueeze(-1).to(last_hidden_state.dtype)
        summed = (last_hidden_state * mask).sum(dim=1)
        counts = mask.sum(dim=1).clamp(min=1e-9)
        return summed / counts

    def embed(self, texts: list[str], *, batch_size: int = 8) -> list[list[float]]:
        vectors: list[list[float]] = []
        with torch.no_grad():
            for start in range(0, len(texts), batch_size):
                batch = texts[start : start + batch_size]
                encoded = self.tokenizer(
                    batch,
                    padding=True,
                    truncation=True,
                    max_length=self.max_length,
                    return_tensors="pt",
                )
                encoded = {key: value.to(self.device) for key, value in encoded.items()}
                output = self.model(**encoded)
                pooled = self._mean_pool(output.last_hidden_state, encoded["attention_mask"])
                if self.normalize:
                    pooled = torch.nn.functional.normalize(pooled, p=2, dim=1)
                vectors.extend(pooled.detach().cpu().float().tolist())
        return vectors

    def metadata(self) -> dict[str, Any]:
        hidden_size = getattr(getattr(self.model, "config", None), "hidden_size", None)
        return {
            "provider": "local_transformers",
            "model": self.model_name_or_path,
            "device": self.device,
            "max_length": self.max_length,
            "normalize": self.normalize,
            "dimensions": hidden_size,
            "load_seconds": self.load_seconds,
        }


def write_model_metadata(path: Path, metadata: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = dict(metadata)
    payload["env"] = {
        "LOCAL_EMBEDDING_MODEL": os.environ.get("LOCAL_EMBEDDING_MODEL", ""),
        "LOCAL_EMBEDDING_DEVICE": os.environ.get("LOCAL_EMBEDDING_DEVICE", ""),
        "LOCAL_EMBEDDING_MAX_LENGTH": os.environ.get("LOCAL_EMBEDDING_MAX_LENGTH", ""),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
