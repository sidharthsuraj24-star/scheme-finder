"""In-memory scheme store (SQLite optional fallback stub).

Phase 2 loads schemes.json into memory. If DATABASE_URL is set later,
callers can swap the store; for now SQLite is prepared but unused unless
explicitly requested.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any

from .schemes_loader import index_by_id, load_schemes


class SchemeStore:
    """Thread-safe-enough read-only scheme catalogue held in process memory."""

    def __init__(self, schemes: list[dict[str, Any]] | None = None) -> None:
        self._schemes: list[dict[str, Any]] = schemes if schemes is not None else load_schemes()
        self._by_id: dict[str, dict[str, Any]] = index_by_id(self._schemes)

    @property
    def schemes(self) -> list[dict[str, Any]]:
        return self._schemes

    def get(self, scheme_id: str) -> dict[str, Any] | None:
        return self._by_id.get(scheme_id)

    def list(
        self,
        *,
        state: str | None = None,
        tag: str | None = None,
        verify: bool | None = None,
    ) -> list[dict[str, Any]]:
        results = self._schemes
        if state:
            state_l = state.lower()
            results = [
                s
                for s in results
                if any(
                    st.lower() == state_l or st.lower() == "india"
                    for st in (s.get("eligibility_rules") or {}).get("states") or []
                )
                or not (s.get("eligibility_rules") or {}).get("states")
            ]
        if tag:
            tag_l = tag.lower()
            results = [s for s in results if tag_l in [t.lower() for t in s.get("tags") or []]]
        if verify is not None:
            results = [
                s
                for s in results
                if bool((s.get("eligibility_rules") or {}).get("verify")) is verify
            ]
        return results


_STORE: SchemeStore | None = None


def get_store() -> SchemeStore:
    global _STORE
    if _STORE is None:
        _STORE = SchemeStore()
    return _STORE


def reset_store(schemes: list[dict[str, Any]] | None = None) -> SchemeStore:
    global _STORE
    _STORE = SchemeStore(schemes)
    return _STORE


def maybe_init_sqlite(db_path: Path | None = None) -> Path | None:
    """Optional: dump schemes into a local SQLite file when DATABASE_URL empty.

    Returns path if created/opened; None if skipped.
    """
    database_url = os.environ.get("DATABASE_URL", "").strip()
    if database_url:
        return None  # Postgres/Supabase path reserved for later phases

    path = db_path or Path(__file__).resolve().parents[1] / "scheme_finder.db"
    store = get_store()
    conn = sqlite3.connect(path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS schemes (
                id TEXT PRIMARY KEY,
                payload TEXT NOT NULL
            )
            """
        )
        conn.execute("DELETE FROM schemes")
        import json

        for scheme in store.schemes:
            conn.execute(
                "INSERT INTO schemes (id, payload) VALUES (?, ?)",
                (scheme["id"], json.dumps(scheme, ensure_ascii=False)),
            )
        conn.commit()
    finally:
        conn.close()
    return path
