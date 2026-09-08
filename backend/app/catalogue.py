"""Catalogue meta + freshness for health/match responses."""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from .schemes_loader import _REPO_ROOT

_DEFAULT_META = {
    "updated_as_of": "2026-09-08",
    "updated_as_of_iso": "2026-09-08T00:00:00+05:30",
    "stale_after_days": 30,
    "disclaimer": (
        "Confirm eligibility with the official source before applying. "
        "This catalogue is curated and may be incomplete or outdated."
    ),
}


def catalogue_meta_path() -> Path:
    candidates = [
        _REPO_ROOT / "data" / "catalogue_meta.json",
        Path("/app/data/catalogue_meta.json"),
        Path("/workspace/scheme-finder-repo/data/catalogue_meta.json"),
    ]
    for path in candidates:
        if path.is_file():
            return path
    return candidates[0]


def load_catalogue_meta() -> dict[str, Any]:
    path = catalogue_meta_path()
    if not path.is_file():
        return dict(_DEFAULT_META)
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        return dict(_DEFAULT_META)
    out = dict(_DEFAULT_META)
    out.update(data)
    out.setdefault("stale_after_days", 30)
    out.setdefault("disclaimer", _DEFAULT_META["disclaimer"])
    return out


def days_since_updated(as_of: str, today: date | None = None) -> int:
    today = today or datetime.now(timezone.utc).date()
    try:
        updated = date.fromisoformat(as_of[:10])
    except ValueError:
        return 10**9
    return (today - updated).days


def is_catalogue_stale(meta: dict[str, Any] | None = None, today: date | None = None) -> bool:
    meta = meta or load_catalogue_meta()
    limit = int(meta.get("stale_after_days") or 30)
    return days_since_updated(str(meta.get("updated_as_of") or ""), today) > limit


def catalogue_payload(today: date | None = None) -> dict[str, Any]:
    meta = load_catalogue_meta()
    return {"catalogue": meta, "is_stale": is_catalogue_stale(meta, today)}


def resolve_last_verified(scheme: dict[str, Any], meta: dict[str, Any] | None = None) -> str | None:
    v = scheme.get("last_verified")
    if isinstance(v, str) and v.strip():
        return v.strip()
    meta = meta or load_catalogue_meta()
    as_of = meta.get("updated_as_of")
    return str(as_of) if as_of else None
