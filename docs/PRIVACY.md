# Privacy — Scheme Finder

**Date:** 2026-09-24 (IST)  
**Scope:** Public demo matcher (no user accounts).

## Principles

1. **No account PII stored by default.** There is no signup, profile database, or
   persistent user store for match answers.
2. **Profiles are ephemeral.** Wizard answers are sent to the match API, evaluated
   in memory (or short-lived match cache keyed by a hash of the request), and not
   written to a user table. Share links encode answers in the URL fragment/query
   on the client — treat shared URLs as sensitive.
3. **Confirm on the official portal.** Matching is a helper only; eligibility and
   applications happen on government / official sites.
4. **Retention = none by default.** We do not keep match request bodies. Optional
   encrypted saved profiles are a later Phase 2 item — not implemented here.

## Access logging (structured, minimal)

Match endpoints may log:

- HTTP status
- Latency (ms)
- Country (coarse geography already on the profile)
- Optional salted **IP hash** (not raw IP); disable with `ACCESS_LOG_IP_HASH=0`

They must **not** log by default: age, income, district, gender, disability,
occupation lists, flags, or full JSON bodies.

## Contact / changes

If retention or analytics are added later, update this file and `docs/TRUST.md`
before enabling.
