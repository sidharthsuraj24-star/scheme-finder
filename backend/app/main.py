"""FastAPI application — Scheme Finder Phase 3 foundation."""

from __future__ import annotations

import hashlib
import logging
import os
import time
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from . import __version__
from .analytics import record_event
from .catalogue import catalogue_payload, load_catalogue_release
from .db import get_store
from .explanations import DISCLAIMER_EN, build_explanation, generator_mode
from .match_cache import get_cached_match, match_cache_ttl_sec, set_cached_match
from .matcher import evaluate_scheme, match_schemes
from .models import (
    AnalyticsEventRequest,
    ErrorBody,
    ErrorResponse,
    ExplainRequest,
    ExplainResponse,
    HealthResponse,
    MatchRequest,
    MatchResponse,
    SchemeListResponse,
    SchemeSummary,
)
from .ops import build_ops_summary
from .redis_client import ping_redis, rate_limit_backend
from .security import (
    MatchRateLimitMiddleware,
    RequestSizeLimitMiddleware,
    SecurityHeadersMiddleware,
    ops_authorized,
)

_ENV = os.environ.get("ENV", os.environ.get("ENVIRONMENT", "development")).strip().lower()
_IS_PROD = _ENV == "production"

# CORS: production defaults to no browser origins until CORS_ORIGINS is set.
# Non-production keeps * for local demo. Env override always wins.
_cors_raw = os.environ.get("CORS_ORIGINS", "").strip()
if _cors_raw:
    _cors = [o.strip() for o in _cors_raw.split(",") if o.strip()]
elif _IS_PROD:
    _cors = []
else:
    _cors = ["*"]
_allow_creds = bool(_cors) and "*" not in _cors

logger = logging.getLogger("scheme_finder.access")


def _client_ip_hash(request: Request) -> str | None:
    """Optional non-reversible IP hint for access logs; omit raw IP/PII."""
    if os.environ.get("ACCESS_LOG_IP_HASH", "1").strip().lower() in ("0", "false", "no"):
        return None
    forwarded = (request.headers.get("x-forwarded-for") or "").split(",")[0].strip()
    ip = forwarded or (request.client.host if request.client else "") or ""
    if not ip:
        return None
    salt = os.environ.get("ACCESS_LOG_IP_SALT", "scheme-finder")
    return hashlib.sha256(f"{salt}:{ip}".encode()).hexdigest()[:16]


app = FastAPI(
    title="Scheme Finder API",
    version=__version__,
    description="Deterministic Kerala/India welfare scheme matcher (Phase 2).",
    docs_url=None if _IS_PROD else "/docs",
    redoc_url=None if _IS_PROD else "/redoc",
    openapi_url=None if _IS_PROD else "/openapi.json",
)

# Middleware order: last added runs first on request.
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors,
    allow_credentials=_allow_creds,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept", "Authorization"],
)
app.add_middleware(MatchRateLimitMiddleware)
app.add_middleware(RequestSizeLimitMiddleware)
app.add_middleware(SecurityHeadersMiddleware)


@app.get("/health", response_model=HealthResponse)
@app.get("/api/v1/health", response_model=HealthResponse)
def health() -> HealthResponse:
    store = get_store()
    freshness = catalogue_payload()
    return HealthResponse(
        status="ok",
        version=__version__,
        scheme_count=len(store.schemes),
        catalogue=freshness["catalogue"],
        is_stale=freshness["is_stale"],
    )


@app.get("/ready")
@app.get("/api/v1/ready")
def ready() -> JSONResponse:
    """Readiness: schemes loaded; Redis ping when REDIS_URL is set (optional)."""
    store = get_store()
    scheme_count = len(store.schemes)
    schemes_ok = scheme_count > 0
    redis_info = ping_redis()
    backend = rate_limit_backend()
    # Redis is optional: configured-but-down does not fail readiness (fail-to-memory).
    ready_ok = schemes_ok
    body: dict[str, Any] = {
        "status": "ready" if ready_ok else "not_ready",
        "version": __version__,
        "schemes_loaded": schemes_ok,
        "scheme_count": scheme_count,
        "rate_limit_backend": backend,
        "match_cache_ttl_sec": match_cache_ttl_sec(),
        "redis": redis_info,
    }
    release = load_catalogue_release()
    if release:
        body["schemes_sha256"] = release.get("schemes_sha256")
        body["catalogue_updated_as_of"] = release.get("updated_as_of")
        body["release_generated_at"] = release.get("generated_at")
    return JSONResponse(content=body, status_code=200 if ready_ok else 503)


@app.get("/catalogue/meta")
@app.get("/api/v1/catalogue/meta")
def catalogue_meta() -> dict[str, Any]:
    """Read-only public catalogue + signed-release metadata (checksum is not a secret)."""
    freshness = catalogue_payload()
    return {
        "catalogue": freshness["catalogue"],
        "is_stale": freshness["is_stale"],
        "release": freshness.get("release"),
    }


@app.get("/schemes", response_model=SchemeListResponse)
@app.get("/api/v1/schemes", response_model=SchemeListResponse)
def list_schemes(
    lang: str | None = Query(default=None, pattern="^(en|ml|hi)$"),
    state: str | None = Query(default=None, max_length=64),
    tag: str | None = Query(default=None, max_length=64),
    verify: bool | None = None,
) -> SchemeListResponse:
    store = get_store()
    schemes = store.list(state=state, tag=tag, verify=verify)
    summaries: list[SchemeSummary] = []
    for s in schemes:
        name = dict(s.get("scheme_name") or {})
        if lang == "hi" and name.get("hi"):
            name = {
                "en": name.get("en", ""),
                "ml": name.get("ml", ""),
                "hi": name["hi"],
            }
        elif lang == "ml" and name.get("ml"):
            name = {
                "en": name.get("en", ""),
                "ml": name["ml"],
                "hi": name.get("hi", ""),
            }
        elif lang == "en" and name.get("en"):
            name = {
                "en": name["en"],
                "ml": name.get("ml", ""),
                "hi": name.get("hi", ""),
            }
        summaries.append(
            SchemeSummary(
                id=s["id"],
                scheme_name=name,
                tags=s.get("tags") or [],
                official_source_url=s.get("official_source_url"),
                verify=bool((s.get("eligibility_rules") or {}).get("verify")),
            )
        )
    return SchemeListResponse(count=len(summaries), schemes=summaries)


@app.get("/schemes/{scheme_id}")
@app.get("/api/v1/schemes/{scheme_id}")
def get_scheme(scheme_id: str) -> dict[str, Any]:
    if len(scheme_id) > 128:
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(
                error=ErrorBody(code="invalid_scheme_id", message="scheme_id too long")
            ).model_dump(),
        )
    store = get_store()
    scheme = store.get(scheme_id)
    if scheme is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error=ErrorBody(code="scheme_not_found", message=f"Unknown scheme id: {scheme_id}")
            ).model_dump(),
        )
    return scheme


@app.post("/match", response_model=MatchResponse)
@app.post("/api/v1/match", response_model=MatchResponse)
def match(request: MatchRequest, http_request: Request) -> MatchResponse:
    """Match schemes. Structured access log: status, latency, country, optional IP hash — never full profiles."""
    t0 = time.perf_counter()
    profile = request.resolved_profile()
    options = request.resolved_options()
    profile_dump = profile.model_dump()
    options_dump = options.model_dump()
    country = getattr(profile, "country", None) or profile_dump.get("country")
    status_code = 200
    cache_hit = False
    match_count: int | None = None

    try:
        cached = get_cached_match(profile_dump, options_dump)
        if cached is not None:
            cache_hit = True
            result = MatchResponse(**cached)
            match_count = result.count
            try:
                top_ids = [m.scheme_id for m in (result.matched or [])[:10]]
                record_event(
                    "match_ok",
                    country=str(country) if country else None,
                    scheme_ids=top_ids,
                    result_count=match_count,
                )
            except Exception:  # noqa: BLE001 — analytics must fail open
                pass
            return result

        store = get_store()
        result = match_schemes(store.schemes, profile, options, geo_index=store.geo_index)
        set_cached_match(profile_dump, options_dump, result.model_dump())
        match_count = result.count
        try:
            top_ids = [m.scheme_id for m in (result.matched or [])[:10]]
            record_event(
                "match_ok",
                country=str(country) if country else None,
                scheme_ids=top_ids,
                result_count=match_count,
            )
        except Exception:  # noqa: BLE001
            pass
        return result
    except Exception:
        status_code = 500
        raise
    finally:
        # Privacy: do NOT log age, income, district, flags, or full profile bodies.
        latency_ms = int((time.perf_counter() - t0) * 1000)
        logger.info(
            "match_access status=%s latency_ms=%s country=%s cache_hit=%s match_count=%s ip_hash=%s",
            status_code,
            latency_ms,
            country or "-",
            cache_hit,
            match_count if match_count is not None else "-",
            _client_ip_hash(http_request) or "-",
        )


@app.post("/explain", response_model=ExplainResponse)
@app.post("/api/v1/explain", response_model=ExplainResponse)
def explain(request: ExplainRequest) -> ExplainResponse:
    store = get_store()
    scheme = store.get(request.scheme_id)
    if scheme is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error=ErrorBody(
                    code="scheme_not_found",
                    message=f"Unknown scheme id: {request.scheme_id}",
                )
            ).model_dump(),
        )
    result = evaluate_scheme(scheme, request.profile)
    status = "uncertain" if (result.uncertain or result.missing or bool((scheme.get("eligibility_rules") or {}).get("verify"))) else (
        "not_eligible" if result.hard_fail else "likely_eligible"
    )
    explanation = build_explanation(
        scheme=scheme,
        profile=request.profile,
        matched_rules=result.matched,
        unmatched_rules=result.unmatched,
        missing_fields=result.missing,
        status=status if status != "not_eligible" else "uncertain",
    )
    return ExplainResponse(
        scheme_id=request.scheme_id,
        explanation=explanation,
        disclaimer=DISCLAIMER_EN,
        generator=generator_mode(),  # type: ignore[arg-type]
    )


@app.get("/sources")
@app.get("/api/v1/sources")
def sources() -> dict[str, Any]:
    """Curated source list derived from loaded schemes."""
    store = get_store()
    items = []
    seen: set[str] = set()
    for s in store.schemes:
        url = s.get("official_source_url")
        if not url or url in seen:
            continue
        seen.add(url)
        items.append(
            {
                "scheme_id": s["id"],
                "scheme_name": s.get("scheme_name"),
                "official_source_url": url,
                "apply_url": s.get("apply_url"),
            }
        )
    return {"count": len(items), "sources": items}


@app.post("/analytics/event")
@app.post("/api/v1/analytics/event")
def analytics_event(body: AnalyticsEventRequest) -> dict[str, Any]:
    """Privacy-preserving aggregate counter. Never stores profile PII."""
    result = record_event(
        body.event,
        country=body.country,
        scheme_ids=body.scheme_ids,
        result_count=body.result_count,
        result_count_bucket=body.result_count_bucket,
    )
    if not result.get("ok"):
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(
                error=ErrorBody(
                    code="invalid_analytics_event",
                    message=str(result.get("error") or "invalid event"),
                )
            ).model_dump(),
        )
    return result


@app.get("/ops/summary")
@app.get("/api/v1/ops/summary")
def ops_summary(
    http_request: Request,
    days: int = Query(default=1, ge=1, le=7),
) -> dict[str, Any]:
    """Read-only ops dashboard payload. Optional bearer OPS_DASHBOARD_TOKEN."""
    if not ops_authorized(http_request):
        raise HTTPException(
            status_code=401,
            detail=ErrorResponse(
                error=ErrorBody(
                    code="ops_unauthorized",
                    message="Ops dashboard requires Authorization: Bearer <OPS_DASHBOARD_TOKEN> "
                    "when OPS_DASHBOARD_TOKEN is set; or NEXT_PUBLIC_SHOW_OPS=1 for open demo.",
                )
            ).model_dump(),
        )
    return build_ops_summary(analytics_days=days)
