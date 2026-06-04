from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from pathlib import Path
from typing import Any


class EmbeddingCache:
    def __init__(self, path: Path, *, enabled: bool = True) -> None:
        self.path = path
        self.enabled = enabled
        if self.enabled:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.path))
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS embeddings (
                    cache_key TEXT PRIMARY KEY,
                    provider TEXT NOT NULL,
                    model TEXT NOT NULL,
                    dimensions INTEGER,
                    input_type TEXT NOT NULL,
                    content_sha256 TEXT NOT NULL,
                    vector_json TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    last_accessed_at REAL NOT NULL,
                    hits INTEGER NOT NULL DEFAULT 0
                )
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_embeddings_model ON embeddings(model)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_embeddings_content ON embeddings(content_sha256)")

    @staticmethod
    def content_hash(content: str | bytes | dict[str, Any]) -> str:
        if isinstance(content, bytes):
            payload = content
        elif isinstance(content, str):
            payload = content.encode("utf-8")
        else:
            payload = json.dumps(content, ensure_ascii=False, sort_keys=True).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    @classmethod
    def make_key(
        cls,
        *,
        provider: str,
        model: str,
        dimensions: int | None,
        input_type: str,
        content: str | bytes | dict[str, Any],
        endpoint: str = "",
    ) -> str:
        payload = {
            "provider": provider,
            "model": model,
            "dimensions": dimensions,
            "input_type": input_type,
            "content_sha256": cls.content_hash(content),
            "endpoint": endpoint,
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

    def get(self, cache_key: str) -> list[float] | None:
        if not self.enabled:
            return None
        with self._connect() as conn:
            row = conn.execute("SELECT vector_json FROM embeddings WHERE cache_key = ?", (cache_key,)).fetchone()
            if row is None:
                return None
            conn.execute(
                "UPDATE embeddings SET last_accessed_at = ?, hits = hits + 1 WHERE cache_key = ?",
                (time.time(), cache_key),
            )
        return json.loads(row[0])

    def set(
        self,
        cache_key: str,
        vector: list[float],
        *,
        provider: str,
        model: str,
        dimensions: int | None,
        input_type: str,
        content: str | bytes | dict[str, Any],
    ) -> None:
        if not self.enabled:
            return
        now = time.time()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO embeddings (
                    cache_key, provider, model, dimensions, input_type,
                    content_sha256, vector_json, created_at, last_accessed_at, hits
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, COALESCE(
                    (SELECT hits FROM embeddings WHERE cache_key = ?), 0
                ))
                """,
                (
                    cache_key,
                    provider,
                    model,
                    dimensions,
                    input_type,
                    self.content_hash(content),
                    json.dumps(vector, separators=(",", ":")),
                    now,
                    now,
                    cache_key,
                ),
            )

    def stats(self) -> dict[str, Any]:
        if not self.enabled or not self.path.exists():
            return {"enabled": self.enabled, "path": str(self.path), "rows": 0}
        with self._connect() as conn:
            rows = conn.execute("SELECT count(*) FROM embeddings").fetchone()[0]
            by_model = conn.execute(
                "SELECT model, input_type, count(*), sum(hits) FROM embeddings GROUP BY model, input_type"
            ).fetchall()
        return {
            "enabled": self.enabled,
            "path": str(self.path),
            "rows": rows,
            "by_model": [
                {"model": row[0], "input_type": row[1], "rows": row[2], "hits": row[3] or 0}
                for row in by_model
            ],
        }
