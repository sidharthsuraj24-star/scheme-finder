# Browser Sevana research notes — 2026-09-08

Structured summary of live Sevana FAQ + LSGD ipcp research used to update Phase 1 seed data.
**Source of truth for this pass:** https://welfarepension.lsgkerala.gov.in/FAQsEng.aspx (home last updated **08 Sep 2026**) and https://lsgkerala.gov.in/en/welfarepension/ipcp.

Do not treat as legal advice. Re-check against latest Government Orders before user-facing benefit quotes.

---

## Global / home observations

- Sevana home last updated: **08 Sep 2026**.
- Monthly amount criteria table shows **Rs 2,000** for listed pensions.
- Additional notes on the same pages:
  - Old Age **75+ special amount: Rs 1,500**
  - Disability **80%+ special amount: Rs 1,100**
- These special amounts **conflict with / sit alongside** the base Rs 2,000 table. **Do NOT invent** whether special amounts are additive or replacement. Record in benefits text + `verify_notes` only.

### Common Sevana exclusion themes (appear across pension types)

- Destitute / not under protection (where stated per scheme)
- Family annual income ≤ **Rs 1,00,000**
- Family land ≤ **2 acres** (ST excluded)
- Not income-tax payer
- Not service/family pensioner (with stated NPS/ex-gratia nuances on some pages)
- Not Central/State salary or pension; not PSU pensioner
- Vehicle / building exclusions (building often ≤2000 sq ft where stated)
- **Max two pensions including EPF**; other welfare pensions barred **except disability** (Sevana framing)
- Apply at **local body of permanent residence** (Grama Panchayat / Municipality / Corporation)

---

## Scheme-by-scheme

### 1. `kerala-agri-labour-pension`

| Field | Value from research |
|-------|---------------------|
| min_age | 60 |
| max_annual_income | 100000 |
| occupations | agricultural_labour |
| how_to_apply | Local body of permanent residence |
| official_source_url | https://welfarepension.lsgkerala.gov.in/FAQsEng.aspx |

**Notes (eligibility detail):**
- Destitute
- Worked as agri labour ≥10 years under landowners
- Member of Kerala Agricultural Workers Welfare Fund (KAWWF)
- Kerala residence ≥10 years continuous
- Family land ≤2 acres (ST excluded)
- Not IT payer; not plantation labourer
- Not service/family pensioner; not Central/State salary/pension; not PSU pensioner
- Vehicle/building exclusions
- Max two pensions incl EPF; other welfare pensions barred except disability

**verify policy:** `false` for hard filters UI will ask (age, income, occupation). Put fund membership / 10yr work / 10yr residence / plantation exclusion in notes + `verify_notes` that UI does not collect those yet.

---

### 2. `kerala-old-age-pension`

| Field | Value |
|-------|-------|
| min_age | 60 |
| max_annual_income | 100000 |
| official_source_url | https://welfarepension.lsgkerala.gov.in/FAQsEng.aspx |

**Notes:** Destitute; not under anyone's protection; not IT payer; family land ≤2 acres (ST excl); Kerala residence ≥3 years continuous; pensioner/salary/vehicle/building exclusions; other welfare pensions barred except disability; max two pensions incl EPF.

**Benefits:** Rs 2000/month per criteria table; page also mentions **75+ special amount Rs 1500** — verify interpretation (additive vs replacement unknown).

**verify policy:** `false` for age+income hard filters; `verify_notes` on 75+ amount and disqualifiers not in questionnaire.

---

### 3. `kerala-disability-pension-physical`

| Field | Value |
|-------|-------|
| min_age | null (no age limit) |
| max_annual_income | 100000 |
| disability_required | true |
| min_disability_percent | 40 |
| sources | FAQsEng.aspx + https://lsgkerala.gov.in/en/welfarepension/ipcp |

**Notes:**
- Sevana: no age limit
- LSGD ipcp: >40% incapability; medical certificate + Social Security Mission ID card
- Apply Grama Panchayat / Municipality / Corporation Secretary; enquiry within 45 days

**CONFLICT (keep verify=true):**
- **Sevana** allows additional pension (max two)
- **LSGD ipcp** says must not receive/apply for another social-welfare pension

**Benefits:** Rs 2000 table; **80%+ special Rs 1100** — verify amount meaning (do not invent additive vs replacement).

---

### 4. `kerala-unmarried-women-pension`

| Field | Value |
|-------|-------|
| min_age | 50 |
| gender | female |
| marital_status | unmarried |
| max_annual_income | 100000 |

**Notes:** Unmarried mothers 50+ allowed; permanent Kerala resident; not under protection; land ≤2 acres; same pensioner/vehicle/building exclusions; other welfare pensions barred except disability.

**verify policy:** `false` for hard fields.

---

### 5. `kerala-widow-pension`

| Field | Value |
|-------|-------|
| min_age | null (no age limit on Sevana for widow/missing) |
| gender | female |
| marital_status | widow, husband_missing_7_years, deserted_7_years_over_50 |
| max_annual_income | 100000 |

**Notes:**
- Must not have remarried
- Deserted case only if woman **over 50** deserted **>7 years**
- Husband missing **>7 years**
- Destitute; Kerala residence ≥2 years continuous; land ≤2 acres
- Exclusions as Sevana; other welfare pensions barred except disability

**verify policy:** `false` for core widow/income; `verify_notes` that deserted needs age≥50 which matcher should encode via `deserted_7_years_over_50`.

---

### 6. `kerala-disability-pension-mental`

- Sevana FAQ table had **blank names** for some rows — **do NOT invent** a distinct mental scheme name from blank rows.
- Browser could not confirm distinct Sevana scheme name for mental vs physical.
- HPWC various-pension-details page **timed out**.
- Keep existing entry; strengthen `verify_notes`.
- Prefer aligning hard filters with physical IGNDPS rules + separate LSGD **imcp** page if still cited.
- `verify` remains **true**.

---

## Conflicts left flagged (verify=true)

1. **Disability dual-pension rule:** Sevana (max two / disability may be additional) vs LSGD ipcp (no other social-welfare pension).
2. **Special amounts vs base Rs 2000:** Old Age 75+ Rs 1500; Disability 80%+ Rs 1100 — meaning unknown.
3. **Mental vs physical Sevana type code:** unconfirmed distinct name; blank FAQ rows; HPWC timeout.

---

## Seed update actions taken (same day)

- Updated the six Sevana-related rows in `data/schemes.json`.
- Recomputed verify counts; refreshed `docs/SCHEMES.md` and `docs/SOURCES.md`.
- Widow marital token renamed to `deserted_7_years_over_50` to encode the age≥50 constraint for deserted cases.
