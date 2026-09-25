# Scheme Finder — Security

**Last pass:** 2026-09-25 (IST) · **Type:** free, tool-driven security pass (Phase 2).
**This is not a penetration test** and not a SOC 2 audit. Both are still needed before
handling sensitive data at scale (see [Remaining gaps](#remaining-gaps)).

Earlier hardening history: `docs/SECURITY_REVIEW.md`. Privacy: `docs/PRIVACY.md`.

## Reporting a vulnerability

Please report privately via **GitHub Security Advisories**:
<https://github.com/sidharthsuraj24-star/scheme-finder/security/advisories/new>

- Don't open public issues for security problems.
- We aim to acknowledge within 5 working days (best-effort; this is a small project).
- Contact placeholder: the repository owner, via the advisory link above. No
  email address is published. `/.well-known/security.txt` points at the same link.
- Good-faith research is welcome. Keep testing **passive** against production: no
  DoS, no brute force, no automated active scanning of the live site. Use a local
  build (`npm run build && npx next start`) for active testing.

## Threat model (summary)

| Asset | Notes |
|-------|-------|
| User answers (age, income, caste category, disability, district…) | Sent to `POST /api/match`, processed ephemerally, not stored server-side. Share links carry them in `?p=` (base64url); saved profiles live in the user's `localStorage` only |
| Catalogue integrity (`schemes.json`) | Wrong eligibility data harms users. Changes go through git + signed releases + audit log (`docs/TRUST.md`) |
| Ops dashboard (`/ops`, `/api/ops/summary`) | Aggregate counters only; gated by `OPS_DASHBOARD_TOKEN` (or the open demo flag) |
| Availability | Public, unauthenticated API on serverless |

| Threat | Mitigation |
|--------|------------|
| XSS → exfiltrating answers from the page | React escaping; **strict nonce-based CSP** (`script-src 'nonce-…' 'strict-dynamic'`, no `unsafe-inline`/`unsafe-eval`, `style-src 'self' 'nonce-…'`, `object-src 'none'`, `base-uri 'none'`); zero CSP violations asserted across the real flows in CI |
| Clickjacking | `frame-ancestors 'none'` + `X-Frame-Options: DENY` |
| Answers leaking via Referer (share URL contains `?p=`) | `Referrer-Policy: no-referrer`; WhatsApp link opens with `rel="noopener noreferrer"` |
| Cross-origin window attacks | `Cross-Origin-Opener-Policy: same-origin`, `Cross-Origin-Resource-Policy: same-origin` |
| Downgrade / cookie-less MITM | HSTS 2 years + `includeSubDomains; preload`; `upgrade-insecure-requests` |
| MIME sniffing | `X-Content-Type-Options: nosniff` everywhere |
| API abuse / memory DoS | Body caps enforced on the **streamed** body (a chunked request with no Content-Length can't bypass them): match 64 KiB, analytics 4 KiB. Per-IP rate limits on match (Upstash Redis when configured), analytics (60/min) and ops auth (30/min). Bounded in-memory maps. Strict input validation and allow-lists |
| Ops token guessing / leakage | Constant-time compare (SHA-256 + `timingSafeEqual`; backend `hmac.compare_digest`). Token accepted in headers only (`Authorization: Bearer` / `X-Ops-Token`), never from the URL, never logged. The `/ops` token input has no `name`, so a pre-hydration submit can't put it in the URL. Generic `401 Unauthorized` that doesn't leak env var names |
| Information leakage | `X-Powered-By` removed. Errors are generic (no stack traces or paths). The 404 for `/api/schemes/[id]` no longer echoes input. `Cache-Control: no-store` on all API responses |
| Open proxy | The `/backend/*` rewrite is dev-only (it was reachable in production before) |
| Supply chain | `npm audit` + `pip-audit` + gitleaks in `scripts/security_audit.sh` and the parked CI workflow; offline lockfile guards in pytest |
| CORS | Next API: same-origin only (no ACAO set by the app). FastAPI: explicit `CORS_ORIGINS`, credentials **never** allowed (the API is stateless) |

## What was scanned (2026-09-25)

| Tool | Target | Mode |
|------|--------|------|
| OWASP ZAP 2.17.0 automation framework | **Production** `https://frontend-theta-wheat-82.vercel.app` | **Passive only**: GETs of key routes + a 1-minute spider + passive rules. No active attacks against production |
| OWASP ZAP 2.17.0 (spider, 776 URLs, **plus active scan**) | **Local production build** (`next build && next start`) | Full active scan, including `POST /api/match` and `POST /api/analytics/event` |
| `npm audit` | `frontend/package-lock.json` | Advisory DB |
| `pip-audit` 2.10.1 | `backend/requirements.txt` | PyPI/OSV advisories |
| gitleaks 8.30.1 | Full git history, all refs (70 commits) + working tree | Secret patterns |
| Manual review | Next API routes, middleware, FastAPI security middleware, ops auth | Input validation, limits, error messages, CORS, token handling |

## Findings — before → after

### ZAP (alert types by risk)

| Risk | Prod passive **before** | Local full **before** | Local full **after** |
|------|------|------|------|
| High | 0 | 0 | **0** |
| Medium | 3: CSP not set · anti-clickjacking missing · cross-domain misconfiguration (Vercel `ACAO: *`) | 2: CSP not set · anti-clickjacking missing | **0** |
| Low | 2: X-Content-Type-Options missing · timestamp disclosure (FP) | 3: X-Powered-By leak · X-Content-Type-Options missing · timestamp disclosure (FP) | **1**: timestamp disclosure (FP) |
| Info | 4: token in URL (`/ops?ops-token=`) · suspicious comments · cache-control · retrieved from cache | 3: token in URL · suspicious comments · UA fuzzer | **2**: suspicious comments (FP, minified React) · UA fuzzer (informational) |

During the fix pass, an intermediate "after" scan flagged **Path Traversal (High, low
confidence)** on the `language` field of `POST /api/match`. It was a false positive:
a long random value got a 422 while the URL's own filename got a 200, and ZAP read that
difference as file access. The field is never used as a path. It's now an allow-list
(`en`/`hi`/`ml`, anything else falls back), and the final scan is clean.

The false positives, with reasons:

- **Timestamp disclosure:** `2023030494` is catalogue data, not a timestamp.
- **Suspicious comments:** the word "bug" appears in minified React/Next chunks.

**Production after:** Vercel auto-deploys `main`. The deployed headers are checked in
the post-push notes of `/workspace/security-and-p4-automation-2026-09-25.md`. The
cross-domain finding comes from Vercel's own `Access-Control-Allow-Origin: *` on
static/HTML responses. The content is public and uses no cookies or credentials, so this
is **accepted** and documented rather than "fixed".

### Dependencies

| Scanner | Before | After |
|---------|--------|-------|
| npm audit | **1 high + 1 moderate**: `postcss@8.4.31`, bundled inside `next@15.5.25` (GHSA-6g55-p6wh-862q, GHSA-r28c-9q8g-f849, GHSA-qx2v-qp2m-jg93, GHSA-fxqj-rqcc-2cmp). npm's only suggested fix was Next 16 (semver-major) | **0**. `next@15.5.26` + `overrides: { next: { postcss: ^8.5.28 } }`; `postcss` 8.5.28 everywhere; `eslint-config-next` aligned |
| pip-audit | 0 known vulnerabilities (27 packages resolved) | 0 |

### Secrets

gitleaks over the full history, all refs (70 commits): **no leaks**. A working-tree scan
flagged 6 hits, all in `frontend/.next/` build output: Next's generated preview and
encryption keys. That output is gitignored and was never committed.

### Manual review fixes

- Ops token compare: `===` → constant-time; generic 401 + `WWW-Authenticate`;
  rate-limited; the URL-leak bug in the `/ops` form is fixed.
- Streamed body cap: `readBodyLimited`. FastAPI returns 411 for chunked POSTs
  without a Content-Length.
- Analytics: size cap, rate limit, event allow-list, country/scheme-id patterns,
  bounded memory. Forwards a **sanitised** body (it used to forward the raw client
  payload) with a 3 s timeout.
- `/api/schemes/[id]`: id pattern check, and the 404 no longer echoes input.
- Security headers on every response, including API, static, 404 and
  `/.well-known/*`. API responses get `Cache-Control: no-store`.
- FastAPI: HSTS, COOP, Permissions-Policy and `no-store` added; CORS credentials off.

## Headers now served

| Header | Value |
|--------|-------|
| Content-Security-Policy (pages) | `default-src 'self'; script-src 'self' 'nonce-<per request>' 'strict-dynamic'; style-src 'self' 'nonce-<same>'; img-src 'self' data: blob:; font-src 'self'; connect-src 'self' [NEXT_PUBLIC_API_URL origin]; manifest-src 'self'; worker-src 'self'; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'; frame-src 'none'; upgrade-insecure-requests` |
| Content-Security-Policy (API, `.well-known`) | `default-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'` |
| Strict-Transport-Security | `max-age=63072000; includeSubDomains; preload` |
| X-Content-Type-Options | `nosniff` |
| Referrer-Policy | `no-referrer` |
| Permissions-Policy | camera, microphone, geolocation, payment, usb, topics, sensors… `=()`; `clipboard-write=(self)` for "Copy link" |
| X-Frame-Options | `DENY` |
| Cross-Origin-Opener-Policy | `same-origin` |
| Cross-Origin-Resource-Policy | `same-origin` |
| X-DNS-Prefetch-Control / X-Permitted-Cross-Domain-Policies | `off` / `none` |
| X-Powered-By | removed |

How the nonce works:

- `src/middleware.ts` generates a fresh nonce for each request.
- `src/app/layout.tsx` calls `headers()`, so pages render dynamically.
- Next.js stamps the nonce on its own `<script>` tags.

Static headers live in `src/lib/securityHeaders.mjs`, which `next.config.mjs` loads.
`next dev` relaxes the policy only to allow `'unsafe-eval'`, inline styles and `ws:`
for HMR.

## Automated checks

| Check | Command | Where |
|-------|---------|-------|
| Header, CSP and API hardening e2e (10 tests, 12 runs across desktop + 375 px; a second server with `OPS_DASHBOARD_TOKEN` runs on :3101) | `cd frontend && npm run build && npm run test:security` | `frontend/e2e/security-headers.spec.ts` |
| Full Playwright suite (a11y + security) | `cd frontend && npm run test:a11y` | `frontend/e2e/` |
| Dependency + secret audit (network) | `bash scripts/security_audit.sh` (`AUDIT_LEVEL`, `SKIP_GITLEAKS`, `GITLEAKS_BIN`) | `scripts/security_audit.sh` |
| Offline guards: lockfile has no vulnerable postcss, Next ≥ 15.5.26, security.txt, this doc | `cd backend && pytest tests/test_security_deps.py` | pytest |
| FastAPI: headers, constant-time ops, generic 401, ops throttle, 411, CORS credentials | `cd backend && pytest tests/test_security.py` | pytest |
| CI (parked, because the token lacks the `workflow` scope) | copy `docs/workflows/security.yml` → `.github/workflows/` | audit + headers jobs on PR/push; weekly passive ZAP baseline on prod |

Re-running ZAP locally, with Java 17+ and the ZAP 2.17 zip:

```bash
zap.sh -cmd -dir /tmp/zaphome -autorun plan.yaml
```

The prod plan must stay passive: `requestor`, `spider`, `passiveScan-wait`, `report`.
Never add `activeScan` to it.

## Remaining gaps

- **No paid penetration test yet.** Tool-driven scanning misses business-logic and
  chained issues. Commission one before collecting accounts or PII.
- **No SOC 2 or formal controls.** Logging and retention, access reviews and incident
  response are not audited.
- **Rate limits are per instance** (memory) on Vercel unless Upstash Redis is configured.
  That only applies to match; the analytics and ops limits are always per instance.
  A determined distributed client can exceed them. Vercel's platform DDoS mitigation
  is the backstop.
- **Vercel `Access-Control-Allow-Origin: *`** on static/HTML: accepted, since the content
  is public and credential-less.
- **Share links put answers in the URL** (`?p=`). This is by design for sharing. No-referrer
  limits leakage, but links can still end up in chat or browser history.
- **Private vulnerability reporting must be enabled** on the GitHub repo (Settings →
  Code security) for the advisory link to accept reports.
- ZAP was run in CLI mode with default rules. There was no authenticated scan of `/ops`
  with a real production token, and no DAST of the optional FastAPI deployment, which
  isn't deployed.
