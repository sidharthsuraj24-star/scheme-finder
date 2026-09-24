"""Read-only ops summary helpers (no PII)."""

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


def url_health_path() -> Path:
    candidates = [
        _REPO_ROOT / "data" / "url_health_snapshot.json",
        Path("/app/data/url_health_snapshot.json"),
        Path("/workspace/scheme-finder-repo/data/url_health_snapshot.json"),
    ]
    for path in candidates:
        if path.is_file():
            return path
    return candidates[0]


def load_url_health() -> dict[str, Any] | None:
    path = url_health_path()
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


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
        },
        "analytics": analytics,
        "trust_checklist_doc": "docs/TRUST.md",
        "product_doc": "docs/PRODUCT.md",
        "show_ops_env": os.environ.get("NEXT_PUBLIC_SHOW_OPS", ""),
        "ops_token_configured": bool(os.environ.get("OPS_DASHBOARD_TOKEN", "").strip()),
    }
