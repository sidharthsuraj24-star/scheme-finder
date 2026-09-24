#!/usr/bin/env python3
"""Append-only URL ticket helpers for catalogue ops (Phase 4 foundation).

Tickets live in data/url_tickets.jsonl. Upsert open tickets on probe failure;
mark fixed when the same scheme_id+url recovers. Never invents eligibility.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[1]
TICKETS_PATH = REPO_ROOT / "data" / "url_tickets.jsonl"
IST = ZoneInfo("Asia/Kolkata")

OPENISH = frozenset({"open", "investigating"})
ALL_STATUSES = frozenset({"open", "investigating", "fixed", "wontfix"})


def ist_now() -> str:
    return datetime.now(IST).isoformat(timespec="seconds")


def read_tickets(path: Path = TICKETS_PATH) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            out.append(row)
    return out


def _append(row: dict[str, Any], path: Path = TICKETS_PATH) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    return row


def latest_by_key(tickets: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    """Latest ticket row per (scheme_id, url)."""
    latest: dict[tuple[str, str], dict[str, Any]] = {}
    for t in tickets:
        sid = str(t.get("scheme_id") or "")
        url = str(t.get("url") or "")
        key = (sid, url)
        latest[key] = t
    return latest


def is_failure_status(status: str) -> bool:
    s = (status or "").upper()
    if not s:
        return False
    if s.startswith("HEAD 2") or s.startswith("GET 2") or s.startswith("OK"):
        return False
    if " 200" in s and "FAIL" not in s:
        return False
    return (
        s.startswith("FAIL")
        or "HTTP 404" in s
        or "HTTP 5" in s
        or "DNS" in s
        or "SSL" in s
        or "CERTIFICATE" in s
        or "NAME OR SERVICE NOT KNOWN" in s
        or "TIMED OUT" in s
        or "TIMEOUT" in s
    )


def host_of(url: str) -> str:
    try:
        return urlparse(url).netloc.lower() or url
    except Exception:  # noqa: BLE001
        return url


def upsert_failure(
    *,
    scheme_id: str | None,
    url: str,
    http_or_error: str,
    notes: str = "",
    path: Path = TICKETS_PATH,
    now: str | None = None,
) -> dict[str, Any]:
    """Open or refresh an open/investigating ticket for a failed probe."""
    ts = now or ist_now()
    sid = scheme_id or ""
    tickets = read_tickets(path)
    latest = latest_by_key(tickets)
    prev = latest.get((sid, url))
    if prev and str(prev.get("status")) in OPENISH:
        # Append a refresh row keeping same ticket_id (append-only history)
        row = {
            "ticket_id": prev["ticket_id"],
            "scheme_id": sid or None,
            "url": url,
            "host": host_of(url),
            "status": prev.get("status") or "open",
            "http_or_error": (http_or_error or "")[:300],
            "first_seen": prev.get("first_seen") or ts,
            "last_seen": ts,
            "notes": notes or prev.get("notes") or "probe failure refresh",
        }
        return _append(row, path)
    row = {
        "ticket_id": f"url-{uuid.uuid4().hex[:12]}",
        "scheme_id": sid or None,
        "url": url,
        "host": host_of(url),
        "status": "open",
        "http_or_error": (http_or_error or "")[:300],
        "first_seen": ts,
        "last_seen": ts,
        "notes": notes or "Opened from URL probe failure",
    }
    return _append(row, path)


def resolve_ok(
    *,
    scheme_id: str | None,
    url: str,
    http_or_error: str = "OK",
    notes: str = "Recovered on probe",
    path: Path = TICKETS_PATH,
    now: str | None = None,
) -> dict[str, Any] | None:
    """If an open/investigating ticket exists for scheme_id+url, append fixed."""
    ts = now or ist_now()
    sid = scheme_id or ""
    tickets = read_tickets(path)
    latest = latest_by_key(tickets)
    prev = latest.get((sid, url))
    if not prev or str(prev.get("status")) not in OPENISH:
        return None
    row = {
        "ticket_id": prev["ticket_id"],
        "scheme_id": sid or None,
        "url": url,
        "host": host_of(url),
        "status": "fixed",
        "http_or_error": (http_or_error or "OK")[:300],
        "first_seen": prev.get("first_seen") or ts,
        "last_seen": ts,
        "notes": notes,
    }
    return _append(row, path)


def open_ticket_count(path: Path = TICKETS_PATH) -> int:
    latest = latest_by_key(read_tickets(path))
    return sum(1 for t in latest.values() if str(t.get("status")) in OPENISH)


def summarize(path: Path = TICKETS_PATH) -> dict[str, Any]:
    latest = latest_by_key(read_tickets(path))
    by_status: dict[str, int] = {}
    for t in latest.values():
        st = str(t.get("status") or "unknown")
        by_status[st] = by_status.get(st, 0) + 1
    open_n = sum(by_status.get(s, 0) for s in OPENISH)
    return {
        "open_count": open_n,
        "by_status": by_status,
        "ticket_rows_total": len(read_tickets(path)),
        "unique_keys": len(latest),
    }
