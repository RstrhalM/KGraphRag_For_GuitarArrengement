from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def utc_timestamp() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"status": "corrupt_jsonl_row", "raw": line[:500]})
    return rows


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def stable_session_id(query: str, timestamp: str | None = None) -> str:
    stamp = timestamp or utc_timestamp()
    digest = hashlib.sha1(f"{stamp}|{query}".encode("utf-8")).hexdigest()[:10]
    compact_time = stamp.replace("-", "").replace(":", "").replace(".", "_").replace("+", "Z")[:22]
    return f"session_{compact_time}_{digest}"


class SessionMemoryStore:
    """Append-only memory store for local Agentic RAG sessions.

    The first version intentionally uses JSONL so each query run, normalization,
    and feedback action remains inspectable and easy to archive.
    """

    def __init__(self, root: Path) -> None:
        self.root = root
        self.session_log = root / "sessions.jsonl"
        self.event_log = root / "session_events.jsonl"

    def append_session(self, row: dict[str, Any]) -> dict[str, Any]:
        timestamp = row.get("timestamp") or utc_timestamp()
        query = str(row.get("query") or "")
        session_id = str(row.get("session_id") or stable_session_id(query, timestamp))
        normalized = {
            **row,
            "session_id": session_id,
            "timestamp": timestamp,
            "schema_version": row.get("schema_version", "session_memory.v1"),
        }
        append_jsonl(self.session_log, normalized)
        append_jsonl(
            self.event_log,
            {
                "timestamp": utc_timestamp(),
                "session_id": session_id,
                "event_type": normalized.get("status", "session_recorded"),
                "summary": self._event_summary(normalized),
            },
        )
        return normalized

    def append_event(self, session_id: str, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        row = {
            "timestamp": utc_timestamp(),
            "session_id": session_id,
            "event_type": event_type,
            "payload": payload,
        }
        append_jsonl(self.event_log, row)
        return row

    def list_sessions(
        self,
        *,
        limit: int = 80,
        status: str = "",
        q: str = "",
        tag: str = "",
    ) -> list[dict[str, Any]]:
        rows = read_jsonl(self.session_log)
        if status:
            rows = [row for row in rows if str(row.get("status") or "") == status]
        if tag:
            rows = [row for row in rows if tag in [str(item) for item in row.get("tags", [])]]
        if q:
            needle = q.lower()
            rows = [
                row
                for row in rows
                if needle
                in " ".join(
                    [
                        str(row.get("query") or ""),
                        str(row.get("normalized_query") or ""),
                        str(row.get("intent") or ""),
                        str(row.get("notes") or ""),
                        " ".join(str(item) for item in row.get("tags", [])),
                    ]
                ).lower()
            ]
        return list(reversed(rows[-limit:]))

    def get_session(self, session_id: str) -> dict[str, Any] | None:
        for row in reversed(read_jsonl(self.session_log)):
            if str(row.get("session_id") or "") == session_id:
                events = [
                    event
                    for event in read_jsonl(self.event_log)
                    if str(event.get("session_id") or "") == session_id
                ]
                return {**row, "events": events}
        return None

    @staticmethod
    def _event_summary(row: dict[str, Any]) -> dict[str, Any]:
        return {
            "query": row.get("query", ""),
            "intent": row.get("intent", ""),
            "status": row.get("status", ""),
            "tags": row.get("tags", []),
            "report_md": row.get("report_md", ""),
            "compose_answer": row.get("compose_answer", False),
            "answer_status": row.get("answer_status", ""),
        }
