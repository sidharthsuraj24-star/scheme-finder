# Scheme Finder — Security Review

**Date:** 2026-09-08 (IST)  
**Scope:** Backend FastAPI (`main.py`, models, matcher, db/loader), frontend API client & result rendering, env examples, CORS, deploy configs.  
**Target:** Public demo on the internet.

## Overall risk rating (public demo)

### Before hardening: **Medium–High**
Not a classic “RCE in 5 minutes” app (no `eval`/`exec`/`pickle`, no raw SQL concat, React text escaping), but several vibe-coded defaults would hurt on the open internet: CORS `*`, open `/docs`, no rate limits, unbounded profile numbers/lists, and unconfined `SCHEMES_PATH`.

### After hardening in this pass: **Low–Medium**
Hardening removes the easy abuse paths (DoS via spam/`/match`, absurd payloads, path escape via env misconfig, docs exposure in prod, missing security headers, `javascript:` hrefs). Residual risk is mostly **unauthenticated public matcher abuse** (expected for a demo) and **single-process in-memory rate limits** (bypassable across replicas).

**Honest answer:** It was not “easily hackable” for data theft or RCE, but it *was* easy to annoy/DoS and misconfigure. After fixes, a casual attacker cannot trivially break out of the matcher sandbox; they can still call `/match` without auth (by design).

---

## Findings table

| Severity | Issue | Evidence | Exploit sketch | Fix (status) |
|----------|--------|----------|----------------|--------------|
| **High** | No rate limiting on `/match` | `backend/app/main.py` (pre-fix) | Flood POSTs → CPU/mem pressure on free-tier host | In-memory per-IP limit middleware (`security.py`) — **fixed** |
| **High** | CORS default `*` even for “prod” if env unset | `main.py` CORS block | Any site can browser-call the API (no creds, still abuse) | Prod (`ENV=production`) defaults to empty origins; override via `CORS_ORIGINS` — **fixed** |
| **Med** | Unbounded profile fields (age/income/lists/`max_results`/`flags`) | `models.py` | Giant JSON / absurd values → validation waste / oversized responses | Pydantic `ge`/`le`/list caps/shallow flags — **fixed** |
| **Med** | `SCHEMES_PATH` could point outside repo | `schemes_loader.py` | Mis-set env loads unexpected JSON (or fails oddly); traversal risk in ops | `confine_schemes_path()` to repo/`/app` roots + `.json` only — **fixed** |
| **Med** | OpenAPI `/docs` always enabled | `FastAPI(...)` defaults | Aids attackers fingerprinting & probing | Disabled when `ENV=production` — **fixed** |
| **Med** | No request body size guard | Starlette defaults | Large bodies chew bandwidth/CPU | `Content-Length` check (~64 KiB) — **fixed** |
| **Low** | Missing security headers on API | responses | Clickjacking/MIME sniffing on API responses | Headers middleware — **fixed** |
| **Low** | Scheme `apply_url` / `official_source_url` rendered as `href` | `SchemeCard.tsx` | If seed/API ever returns `javascript:`… → XSS via link | `safeHttpUrl()` allows http(s) only — **fixed** |
| **Low** | Frontend `NEXT_PUBLIC_API_URL` not validated | `lib/api.ts` | Malformed / non-http base breaks or confuses clients | `resolveApiBase()` http(s) only — **fixed** |
| **Info** | No auth on matcher | API design | Anyone can match (PII-ish profile fields in transit) | Documented as OK for public demo; use HTTPS at edge — **accepted** |
| **Info** | In-memory rate limit not shared across workers | `MatchRateLimitMiddleware` | Multi-instance deploy weakens limits | Edge/WAF or Redis limiter later — **residual** |
| **Info** | `LLM_API_KEY` stub only | `explanations.py` | N/A today; future LLM calls need egress/allowlists | Keep stub; never let LLM decide eligibility — **OK** |
| **Info** | SQLite helper unused in request path | `db.py` | Parameterized inserts if used — fine | Keep unused path; no raw SQL — **OK** |

### Previously OK (no change needed)

- No `eval` / `exec` / `shell=True` / `pickle` / `subprocess` in app code.
- Matcher is deterministic rule evaluation — no dynamic code from input.
- SQLite uses `?` placeholders (if ever enabled).
- Frontend does **not** use `dangerouslySetInnerHTML`; copy is React text nodes.
- `.gitignore` already ignored `.env` / `.env.local` (strengthened further).
- Seed URLs in `data/schemes.json` are https only.
- Deploy configs force HTTPS at platform (`fly.toml` `force_https`).

---

## Recommended hardening before public internet exposure

1. Set **`ENV=production`**, **`CORS_ORIGINS=https://<your-vercel-app>`**, and **`NEXT_PUBLIC_API_URL=https://<api>`**.
2. Put the API behind a host with **HTTPS**, request logging, and preferably a **CDN/WAF rate limit** (do not rely only on in-process limits).
3. Keep **docs off** in prod (already automatic with `ENV=production`).
4. Do not set `SCHEMES_PATH` outside the image/`data/` tree.
5. Treat match profiles as **sensitive**: no long-term logging of full bodies; privacy notice already in UI disclaimer.
6. Optional next steps: Redis rate limit, CAPTCHA on wizard submit, CSP on the Next.js frontend, allowlist scheme link hosts to `.gov.in` domains.

---

## What changed in this pass

| Area | Change |
|------|--------|
| Backend | `security.py` middleware; CORS prod default; docs off in prod; model caps; path confinement |
| Frontend | API URL validation; `safeHttpUrl` for links; income/age clamps |
| Repo | Stronger `.gitignore` / `.env.example`; `docs/SECURITY_REVIEW.md`; `tests/test_security.py` |

---

## Residual risks (accepted for demo)

- **No authentication** on `/match` — intentional for a public eligibility helper; document that profiles may be sensitive and should only be sent over HTTPS.
- **Rate limit is per-process memory** — fine for a single free-tier dyno; not a hard DoS guarantee.
- **Trust of seed JSON** — compromise of `schemes.json` or the deploy artifact could change eligibility copy/links; protect the repo and deploy pipeline.
