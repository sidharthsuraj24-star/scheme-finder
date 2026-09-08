# Decisions — Scheme Finder Phase 1

## Data curation

1. **No invented eligibility.** Only fields supported by official pages were populated; unclear items set `verify=true` with `verify_notes`.
2. **Kerala Sevana over bare NSAP for Kerala pensions.** Central NSAP age/BPL frames differ from Sevana FAQ (e.g., widow age). Matcher for Kerala residents should prefer Sevana rules; NSAP cited for NFBS/central context.
3. **Mentally vs physically challenged.** Kept as separate scheme ids because KSSP/LSGD publish distinct pages; Sevana forms group them. Marked verify for operational distinctness and age conflict on imcp page.
4. **LIFE Mission.** Included with heavy verify; no numeric income ceiling taken from blogs.
5. **PM-KISAN land size.** Homepage says all landholding families (with exclusions); older FAQ said ≤2 ha → verify flag.
6. **Benefits amounts.** Sevana tables show Rs.2000 — recorded as listed on FAQ criteria tables; advise re-check against latest GO before user-facing benefit quotes.

## Malayalam copy

- Where confident short ML titles/descriptions were available or straightforward, ML was provided.
- Otherwise `ml` fields reuse English with suffix ` [ML copy pending native review]`.
- **Do not ship user-facing ML without native speaker review.**

## Planned stack fallbacks (Phase 2+)

| Concern | Preferred | Fallback |
|---------|-----------|----------|
| Database | Supabase (Postgres) | **SQLite** local file (`scheme_finder.db`) if no Supabase credentials |
| Explanations | LLM (API key) | **Template explanations** from matched/unmatched rule lists if no LLM key |
| Auth | Supabase Auth / optional API key | None for local demo |
| Hosting | Container / serverless | Local Uvicorn |

Env example:
```
DATABASE_URL=          # empty → SQLite
SUPABASE_URL=
SUPABASE_KEY=
LLM_API_KEY=           # empty → templates only
```

## Sample profiles

`data/sample_profiles.json` has 15 synthetic profiles for matcher tests (senior, widow, PwD, farmer, student, pregnant, high-income control, etc.). Not real persons.

## Out of scope for Phase 1

- Live matching engine / FastAPI implementation
- Scrapers or automatic GO sync
- Storing user PII
