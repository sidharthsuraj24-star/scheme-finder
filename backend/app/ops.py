"""Read-only ops summary helpers (no PII). Phase 4 adds tickets / candidates / packs."""

from __future__ import annotations

import json
import os
from collections import Counter
from pathlib import Path
from typing import Any

from .analytics import snapshot as analytics_snapshot
from .catalogue import catalogue_payload, load_catalogue_release
from .db import get_store
from .schemes_loader import _REPO_ROOT


def _data_candidates(name: str) -> list[Path]:
    return [
        _REPO_ROOT / "data" / name,
        Path("/app/data") / name,
        Path("/workspace/scheme-finder-repo/data") / name,
        _REPO_ROOT / "frontend" / "data" / name,
    ]


def url_health_path() -> Path:
    for path in _data_candidates("url_health_snapshot.json"):
        if path.is_file():
            return path
    return _data_candidates("url_health_snapshot.json")[0]


def load_url_health() -> dict[str, Any] | None:
    path = url_health_path()
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def _load_json_first(name: str) -> Any | None:
    for path in _data_candidates(name):
        if not path.is_file():
            continue
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
    return None


def _read_jsonl(name: str) -> list[dict[str, Any]]:
    for path in _data_candidates(name):
        if not path.is_file():
            continue
        rows: list[dict[str, Any]] = []
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(row, dict):
                    rows.append(row)
            return rows
        except OSError:
            continue
    return []


def url_tickets_summary() -> dict[str, Any]:
    rows = _read_jsonl("url_tickets.jsonl")
    latest: dict[tuple[str, str], dict[str, Any]] = {}
    for t in rows:
        key = (str(t.get("scheme_id") or ""), str(t.get("url") or ""))
        latest[key] = t
    by_status: Counter[str] = Counter()
    for t in latest.values():
        by_status[str(t.get("status") or "unknown")] += 1
    open_count = by_status.get("open", 0) + by_status.get("investigating", 0)
    return {
        "open_count": open_count,
        "by_status": dict(by_status),
        "unique_tickets": len(latest),
        "rows_total": len(rows),
    }


def candidates_summary() -> dict[str, Any]:
    raw = _load_json_first("catalogue_candidates.json")
    cands: list[Any] = []
    if isinstance(raw, dict):
        cands = raw.get("candidates") or []
    elif isinstance(raw, list):
        cands = raw
    by_status: Counter[str] = Counter()
    for c in cands:
        if isinstance(c, dict):
            by_status[str(c.get("status") or "unknown")] += 1
    return {
        "total": len([c for c in cands if isinstance(c, dict)]),
        "by_status": dict(by_status),
        "needs_review": by_status.get("needs_review", 0),
        "queued": by_status.get("queued", 0),
        "researching": by_status.get("researching", 0),
        "deferred": by_status.get("deferred", 0),
        "verified_add": by_status.get("verified_add", 0),
        "rejected": by_status.get("rejected", 0),
    }


def packs_summary() -> dict[str, Any]:
    raw = _load_json_first("packs/index.json")
    if not isinstance(raw, dict):
        # Count files if index missing
        for base in (_REPO_ROOT / "data" / "packs", Path("/app/data/packs")):
            if base.is_dir():
                files = [p for p in base.glob("*@*.json") if p.is_file()]
                return {"pack_count": len(files), "index_generated_at": None}
        return {"pack_count": 0, "index_generated_at": None}
    return {
        "pack_count": int(raw.get("pack_count") or len(raw.get("packs") or [])),
        "default_version": raw.get("default_version"),
        "index_generated_at": raw.get("generated_at"),
    }


def coverage_summary(schemes: list[dict[str, Any]]) -> dict[str, Any]:
    by_country: Counter[str] = Counter()
    by_state_tag: Counter[str] = Counter()
    verify_true = 0
    for s in schemes:
        tags = [str(t).lower() for t in (s.get("tags") or [])]
        er = s.get("eligibility_rules") or {}
        if er.get("verify"):
            verify_true += 1
        if "united_states" in tags or "united-states" in tags:
            by_country["United States"] += 1
        elif "united_kingdom" in tags or (s.get("id") or "").startswith("gb-"):
            by_country["United Kingdom"] += 1
        elif any(t in ("bangladesh", "nepal", "sri-lanka", "maldives") for t in tags) or (
            s.get("id") or ""
        ).startswith(("bd-", "np-", "lk-", "mv-")):
            by_country["Neighbours (BD/NP/LK/MV)"] += 1
        else:
            by_country["India / other"] += 1
        for t in tags:
            if t in (
                "kerala",
                "california",
                "texas",
                "new_york",
                "united_kingdom",
                "federal",
                "nationwide",
                "central",
            ):
                by_state_tag[t] += 1
    return {
        "by_country": dict(by_country.most_common()),
        "sample_tags": dict(by_state_tag.most_common(12)),
        "verify_true": verify_true,
        "verify_false": max(0, len(schemes) - verify_true),
    }


def build_ops_summary(*, analytics_days: int = 1) -> dict[str, Any]:
    store = get_store()
    freshness = catalogue_payload()
    release = load_catalogue_release() or freshness.get("release")
    cat = freshness.get("catalogue") or {}
    coverage = coverage_summary(store.schemes)
    url_health = load_url_health()
    flaky: list[Any] = []
    if isinstance(url_health, dict):
        raw = url_health.get("flaky_hosts") or url_health.get("hosts") or []
        if isinstance(raw, list):
            flaky = raw[:40]
    analytics = analytics_snapshot(days=analytics_days)
    tickets = url_tickets_summary()
    candidates = candidates_summary()
    packs = packs_summary()
    return {
        "scheme_count": len(store.schemes),
        "updated_as_of": cat.get("updated_as_of") or (release or {}).get("updated_as_of"),
        "schemes_sha256": (release or {}).get("schemes_sha256") or cat.get("schemes_sha256"),
        "is_stale": freshness.get("is_stale"),
        "stale_after_days": cat.get("stale_after_days"),
        "release_generated_at": (release or {}).get("generated_at") or cat.get("release_generated_at"),
        "verify_true_count": coverage["verify_true"],
        "verify_false_count": coverage["verify_false"],
        "coverage": coverage,
        "url_health": {
            "generated_at": (url_health or {}).get("generated_at"),
            "note": (url_health or {}).get("note")
            or "Run scripts/write_url_health_snapshot.py after freshness checks.",
            "flaky_hosts": flaky,
            "checked_count": (url_health or {}).get("checked_count"),
            "ok_count": (url_health or {}).get("ok_count"),
            "open_url_tickets": tickets["open_count"],
        },
        "url_tickets": tickets,
        "candidates": candidates,
        "packs": packs,
        "analytics": analytics,
        "trust_checklist_doc": "docs/TRUST.md",
        "product_doc": "docs/PRODUCT.md",
        "catalogue_ops_doc": "docs/CATALOGUE_OPS.md",
        "show_ops_env": os.environ.get("NEXT_PUBLIC_SHOW_OPS", ""),
        "ops_token_configured": bool(os.environ.get("OPS_DASHBOARD_TOKEN", "").strip()),
    }
