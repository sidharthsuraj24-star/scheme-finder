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
4. **Retention = none by default on the server.** We do not keep match request bodies.
5. **Device-only saved profiles (Phase 3 foundation).** Optional “Save on this device”
   stores ProfileAnswers + language in the browser `localStorage` (cap 5). These stay
   on the device unless the user shares a `?p=` link. Not uploaded to a profile database.
6. **Aggregate analytics only.** Counters may record match_ok volume, country, result
   buckets, and scheme_id hits — never profile PII. Analytics must never invent
   eligibility (see `docs/ANALYTICS.md`).

## Access logging (structured, minimal)

Match endpoints may log:

- HTTP status
- Latency (ms)
- Country (coarse geography already on the profile)
- Optional salted **IP hash** (not raw IP); disable with `ACCESS_LOG_IP_HASH=0`

They must **not** log by default: age, income, district, gender, disability,
occupation lists, flags, or full JSON bodies.

## Contact / changes

Encrypted cloud profiles, OTP/DigiLocker accounts, and richer retention require
updating this file and `docs/TRUST.md` before enabling.
