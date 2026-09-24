"""Catalogue meta + freshness + signed release metadata for health/match responses."""

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


def catalogue_release_path() -> Path:
    candidates = [
        _REPO_ROOT / "data" / "catalogue_release.json",
        Path("/app/data/catalogue_release.json"),
        Path("/workspace/scheme-finder-repo/data/catalogue_release.json"),
    ]
    for path in candidates:
        if path.is_file():
            return path
    return candidates[0]


_META_CACHE: dict[str, Any] | None = None
_RELEASE_CACHE: dict[str, Any] | None = None


def load_catalogue_meta(*, force_reload: bool = False) -> dict[str, Any]:
    global _META_CACHE
    if _META_CACHE is not None and not force_reload:
        return _META_CACHE
    path = catalogue_meta_path()
    if not path.is_file():
        _META_CACHE = dict(_DEFAULT_META)
        return _META_CACHE
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        _META_CACHE = dict(_DEFAULT_META)
        return _META_CACHE
    out = dict(_DEFAULT_META)
    out.update(data)
    out.setdefault("stale_after_days", 30)
    out.setdefault("disclaimer", _DEFAULT_META["disclaimer"])
    _META_CACHE = out
    return _META_CACHE


def load_catalogue_release(*, force_reload: bool = False) -> dict[str, Any] | None:
    """Public signed-release metadata (checksum is not a secret)."""
    global _RELEASE_CACHE
    if _RELEASE_CACHE is not None and not force_reload:
        return _RELEASE_CACHE
    path = catalogue_release_path()
    if not path.is_file():
        _RELEASE_CACHE = None
        return None
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        _RELEASE_CACHE = None
        return None
    public = {
        "updated_as_of": data.get("updated_as_of"),
        "scheme_count": data.get("scheme_count"),
        "schemes_sha256": data.get("schemes_sha256"),
        "generated_at": data.get("generated_at"),
        "timezone": data.get("timezone", "Asia/Kolkata"),
        "latest_changelog": data.get("latest_changelog"),
        "commit_sha": data.get("commit_sha"),
    }
    _RELEASE_CACHE = {k: v for k, v in public.items() if v is not None}
    return _RELEASE_CACHE


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
    out: dict[str, Any] = {"catalogue": meta, "is_stale": is_catalogue_stale(meta, today)}
    release = load_catalogue_release()
    if release:
        merged = dict(meta)
        merged["schemes_sha256"] = release.get("schemes_sha256")
        merged["release_generated_at"] = release.get("generated_at")
        out["catalogue"] = merged
        out["release"] = release
    return out


def resolve_last_verified(scheme: dict[str, Any], meta: dict[str, Any] | None = None) -> str | None:
    v = scheme.get("last_verified")
    if isinstance(v, str) and v.strip():
        return v.strip()
    meta = meta or load_catalogue_meta()
    as_of = meta.get("updated_as_of")
    return str(as_of) if as_of else None
