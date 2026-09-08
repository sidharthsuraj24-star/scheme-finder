"""FastAPI application — Scheme Finder Phase 2."""

from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from . import __version__
from .db import get_store
from .explanations import DISCLAIMER_EN, build_explanation, generator_mode
from .matcher import evaluate_scheme, match_schemes
from .models import (
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
from .security import (
    MatchRateLimitMiddleware,
    RequestSizeLimitMiddleware,
    SecurityHeadersMiddleware,
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
    return HealthResponse(status="ok", version=__version__)


@app.get("/schemes", response_model=SchemeListResponse)
@app.get("/api/v1/schemes", response_model=SchemeListResponse)
def list_schemes(
    lang: str | None = Query(default=None, pattern="^(en|ml)$"),
    state: str | None = Query(default=None, max_length=64),
    tag: str | None = Query(default=None, max_length=64),
    verify: bool | None = None,
) -> SchemeListResponse:
    store = get_store()
    schemes = store.list(state=state, tag=tag, verify=verify)
    summaries: list[SchemeSummary] = []
    for s in schemes:
        name = dict(s.get("scheme_name") or {})
        if lang == "ml" and name.get("ml"):
            name = {"en": name.get("en", ""), "ml": name["ml"]}
        elif lang == "en" and name.get("en"):
            name = {"en": name["en"], "ml": name.get("ml", "")}
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
def match(request: MatchRequest) -> MatchResponse:
    profile = request.resolved_profile()
    options = request.resolved_options()
    store = get_store()
    return match_schemes(store.schemes, profile, options)


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
