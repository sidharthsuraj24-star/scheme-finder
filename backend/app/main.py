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

app = FastAPI(
    title="Scheme Finder API",
    version=__version__,
    description="Deterministic Kerala/India welfare scheme matcher (Phase 2).",
)

# CORS: default * for demo. Set CORS_ORIGINS=https://your-app.vercel.app,... in prod.
# allow_credentials must be False when origins is *.
_cors = [o.strip() for o in os.environ.get("CORS_ORIGINS", "*").split(",") if o.strip()]
_allow_creds = _cors != ["*"] and "*" not in _cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors,
    allow_credentials=_allow_creds,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
@app.get("/api/v1/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", version=__version__)


@app.get("/schemes", response_model=SchemeListResponse)
@app.get("/api/v1/schemes", response_model=SchemeListResponse)
def list_schemes(
    lang: str | None = Query(default=None, pattern="^(en|ml)$"),
    state: str | None = None,
    tag: str | None = None,
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
