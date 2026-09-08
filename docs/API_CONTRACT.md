# Scheme Finder — Proposed FastAPI contract (Phase 2+)

Base path: `/api/v1`  
Content-Type: `application/json`

## Endpoints

### `GET /health`
Liveness.

**Response 200**
```json
{ "status": "ok", "version": "0.1.0" }
```

### `GET /schemes`
List schemes (summary).

**Query**
- `state` (optional): e.g. `Kerala`
- `tag` (optional): filter by tag
- `verify` (optional bool): filter by `eligibility_rules.verify`

**Response 200**
```json
{
  "count": 18,
  "schemes": [
    {
      "id": "kerala-old-age-pension",
      "scheme_name": { "en": "...", "ml": "..." },
      "tags": ["pension"],
      "official_source_url": "https://...",
      "verify": false
    }
  ]
}
```

### `GET /schemes/{scheme_id}`
Full scheme record (same shape as `data/schemes.json` item).

**Response 404** if unknown id.

### `POST /match`
Match a user profile to schemes.

**Request**
```json
{
  "profile": {
    "age": 68,
    "gender": "male",
    "state": "Kerala",
    "marital_status": "widow",
    "annual_income": 45000,
    "monthly_household_income": 4000,
    "occupations": ["farmer"],
    "categories": ["SC", "BPL"],
    "disability_percent": null,
    "land_ownership": "none",
    "is_student": false,
    "is_pregnant": false,
    "pregnancy_order": null,
    "housing_status": null,
    "income_tax_payer": false,
    "flags": {
      "kawwf_member": false,
      "secc_eligible": false,
      "rsby_chis_2018_19": false
    }
  },
  "options": {
    "include_verify_uncertain": true,
    "lang": "en",
    "max_results": 20
  }
}
```

**Response 200**
```json
{
  "matched": [
    {
      "scheme_id": "kerala-old-age-pension",
      "score": 0.92,
      "status": "likely_eligible",
      "matched_rules": ["min_age", "max_annual_income", "states"],
      "unmatched_rules": [],
      "missing_profile_fields": [],
      "verify": false,
      "verify_notes": "",
      "explanation": {
        "en": "Age 68 meets 60+; annual income under Rs.1 lakh; Kerala resident.",
        "ml": "..."
      },
      "scheme_name": { "en": "...", "ml": "..." },
      "benefits": { "en": "...", "ml": "..." },
      "apply_url": "https://...",
      "official_source_url": "https://..."
    }
  ],
  "excluded": [
    {
      "scheme_id": "pm-kisan",
      "status": "not_eligible",
      "reasons": ["land_ownership_required"]
    }
  ],
  "needs_verification": [
    {
      "scheme_id": "kerala-life-mission",
      "status": "uncertain",
      "verify_notes": "..."
    }
  ]
}
```

**Status values:** `likely_eligible` | `uncertain` | `not_eligible`

### `POST /explain`
Optional LLM/template explanation for one scheme + profile.

**Request**
```json
{
  "scheme_id": "kerala-widow-pension",
  "profile": { "...": "same as /match profile" },
  "lang": "en"
}
```

**Response 200**
```json
{
  "scheme_id": "kerala-widow-pension",
  "explanation": { "en": "...", "ml": "..." },
  "disclaimer": "Based on published eligibility rules; confirm with the implementing office. Not legal advice.",
  "generator": "template" 
}
```
`generator`: `template` | `llm`

### `GET /sources`
Return curated source list (from docs or DB).

## Matching rules (engine sketch)

1. Hard filters: `states`, age min/max, gender, disability required/%, income caps when present.
2. Soft filters: occupations, categories, marital_status (set intersection).
3. If `eligibility_rules.verify=true`, never return `likely_eligible` without `uncertain`/`needs_verification` path unless profile supplies all verify-critical flags.
4. Missing profile fields → `uncertain` + `missing_profile_fields`, not silent exclude.
5. Explanations must cite rule field names; never invent thresholds.

## Error shape
```json
{ "error": { "code": "scheme_not_found", "message": "..." } }
```
