# Canada — catalogue country notes

**Added:** 2026-09-25 (IST) · **Rows:** 67 (`can-*`: 29 federal + 38 provincial/territorial)
**Packs:** `canada-federal` + 13 `canada-<province>` packs (all `@1.0.0`)
**Generator:** `scripts/canada_starter_pack_2026_09_25.py`. Rows are in `..._rows.py` (helpers), `..._federal.py` and `..._provincial.py`.

Product aim: one worldwide benefits hub for poor, middle-class **and** wealthy households.
The Canada pack covers means-tested support *and* universal, tax and savings programmes
that higher earners can use within their real limits.

## Conventions

| Topic | Canada rule |
|-------|-------------|
| Scheme id prefix | `can-`. **`ca-` is already used by US/California rows** — never use it for Canada. Provincial rows: `can-<code>-*` with codes `ab bc mb nb nl nt ns nu on pe qc sk yt`. |
| `eligibility_rules.countries` | `["Canada"]` |
| Country aliases | `canada`, `can`. **Not `ca`** (California prefix). |
| Regions | All 13 provinces and territories: Alberta, British Columbia, Manitoba, New Brunswick, Newfoundland and Labrador, Northwest Territories, Nova Scotia, Nunavut, Ontario, Prince Edward Island, Quebec, Saskatchewan, Yukon. |
| All-Canada federal rows | `states: []`, `nationwide: true`, tag `canada_federal` → pack `canada-federal` (kind `country_federal`). |
| Federal rows that exclude a province | Listed with the other provinces explicitly and `nationwide: false`, still tagged `canada_federal` and kept in `canada-federal`. Covers CPP retirement / disability / survivor and EI maternity-parental (not Quebec: QPP / QPIP), and the Canada Student Grants (not QC / NT / NU). |
| Provincial rows | `states: [<province>]`, `nationwide: false`, province tag (e.g. `ontario`) → pack `canada-<province-slug>` (kind `province`). |
| Tags | `canada` (+ `canada_federal` or a province tag). **Never** `central` / `nationwide` / `federal` (those drive India/US pack buckets). |
| Currency | **`C$` (CAD)** in the wizard/results (`currencySymbol("Canada") = "C$"`) and in explanations (`C$45,000`, `C$58,523`). Never a bare `$`, which the catalogue uses for USD. Scheme text always writes `C$`. |
| Sources | Official only: canada.ca (CRA, ESDC / Service Canada) plus alberta.ca, gov.bc.ca, gov.mb.ca, gnb.ca, novascotia.ca, ece.gov.nt.ca, ontario.ca, quebec.ca, retraitequebec.gouv.qc.ca, revenuquebec.ca, saskatchewan.ca, yukon.ca. Where CRA pays a provincial benefit, its official page is the CRA "provincial and territorial programs" page. |
| Verification | Every row has `verify: true` and `last_verified: 2026-09-25`. |

## Income handling (no India bands, no US gate)

- **India PRICE ICE 360 bands never apply** to Canada profiles (`income_band*` stay null).
- **The US $60k gate is never used.** Canada has its own soft gate,
  `IMPLIES_LOW_INCOME_ANNUAL_GATE_CAD = 58_523`, in backend `app/matcher.py` and frontend
  `src/lib/matching/matcher.ts`.
  - **Anchor:** the 2026 top of the lowest federal income-tax bracket, C$58,523. ESDC uses
    the same figure as its low-income line for the Canada Learning Bond (1–3 children,
    July 2026 – June 2027) and as the top of the 20% additional-CESG tier. It is a
    **catalogue heuristic, not an official means test**.
  - It applies **only** to rows with `implies_low_income: true` **and** no numeric max.
    These are genuinely low-income programmes with no single published figure: Canada
    Disability Benefit, AISH, ODSP, SAID, BC Senior's Supplement, MB 55 PLUS / Child
    Benefit, NB / NL / NS / NT / NU / YT child benefits and credits, SK SIP, NB seniors'
    benefit, PE sales tax credit, and the Quebec solidarity tax credit.
  - Boundary: income ≥ C$58,523 fails the soft gate. A test proves C$59,000 is excluded
    even though it is under the US $60k gate.
- **Official ceilings are encoded as `max_annual_income`.** Where the ceiling varies by
  household, the **highest published cut-off** is encoded and the smaller-household
  figures go in `notes`:

  | Programme | Encoded max | Other published limits |
  |-----------|-------------|------------------------|
  | CGEB | C$82,952 (4+ children) | single C$60,012 |
  | CWB | C$60,629 | basic family C$49,393 |
  | GIS | C$54,624 | single C$22,800 |
  | Allowance | C$42,144 | |
  | Allowance for the Survivor | C$30,696 | |
  | CLB | C$73,577 (5 children) | 1–3 children C$58,523 |
  | CDCP | < C$90,000 | |
  | Canada Student Grants | C$161,321 (family of 7+) | |
  | AB Seniors Benefit | C$53,800 couple | |
  | BC renter's credit | C$86,189 | |
  | MB Rent Assist | C$60,768 | |
  | NL Seniors' Benefit | C$46,549 | |
  | NL Disability Benefit | C$55,404 | |
  | NS Child Benefit | C$34,000 | |
  | NS Poverty Reduction Credit | C$16,000 | |
  | NT Senior Home Heating Subsidy | C$87,000 (Zone 3) | |
  | ON Seniors Dental | C$42,290 couple | |
  | PE Child Benefit | C$80,000 | |
  | SK Low-Income Tax Credit | C$81,668 | |
  | YT Pioneer Utility Grant | C$217,470 couple | |

- **Phase-outs that reach middle incomes are not gated.** These keep
  `implies_low_income: false` and `max_annual_income: null`, with the phase-out explained
  in notes: CCB, Child Disability Benefit, BC Family Benefit, Alberta Child and Family
  Benefit, Ontario Trillium Benefit, and Ontario Child Benefit.
- **Non-means-tested rows** have `implies_low_income: false` and `max_annual_income: null`.
  These are OAS (the recovery-tax clawback is a note, not a cap), CPP / QPP, EI, QPIP,
  DTC, RDSP, RESP / CESG, TFSA, RRSP, FHSA, HBP, home buyers' amount, caregiver credit,
  BCTESG and Quebec Family Allowance. They are tagged `universal` / `middle-class` /
  `upper-middle-class` / `high-income-eligible` as accurate.

## Schemes (July 2026 – June 2027 or 2026 rates; last_verified 2026-09-25)

**Federal (29):** Canada Child Benefit; Child Disability Benefit; Canada Groceries and
Essentials Benefit (CGEB, formerly the GST/HST credit); Canada Workers Benefit; OAS (with
the recovery-tax note); GIS; Allowance; Allowance for the Survivor; CPP retirement / disability /
survivor (not QC); EI regular, maternity & parental (not QC), sickness, caregiving;
Canada Disability Benefit (**active**: C$204.20/month from July 2026, with a C$150
supplement on Sept 17, 2026); Disability Tax Credit; RDSP + CDSG/CDSB; RESP + CESG;
Canada Learning Bond; TFSA; RRSP; FHSA; Home Buyers' Plan; home buyers' amount; Canadian
Dental Care Plan (open to all eligible ages for 2026–27; AFNI < C$90k); Canada Student
Grant full-time and part-time (not QC / NT / NU); Canada caregiver amount.

**Provinces and territories (38):**

| Province / territory | Rows |
|----------------------|------|
| Alberta (3) | Alberta Child and Family Benefit; Alberta Seniors Benefit; AISH |
| British Columbia (4) | BC Family Benefit; renter's tax credit; Senior's Supplement; BC Training and Education Savings Grant |
| Manitoba (3) | 55 PLUS; Rent Assist (non-EIA); Manitoba Child Benefit |
| New Brunswick (3) | NB Child Tax Benefit (+ WIS / school supplement); NB HST credit; Low-Income Seniors' Benefit |
| Newfoundland and Labrador (4) | NL Child Benefit (+ nutrition supplement); Income Supplement; Seniors' Benefit; Disability Benefit |
| Nova Scotia (3) | NS Child Benefit; Affordable Living Tax Credit; Poverty Reduction Credit |
| Northwest Territories (2) | NWT Child Benefit; Senior Home Heating Subsidy (2026–27) |
| Nunavut (1) | Nunavut Child Benefit |
| Ontario (4) | Ontario Trillium Benefit; Ontario Child Benefit; Seniors Dental Care Program; ODSP |
| Prince Edward Island (2) | PEI Child Benefit; PEI Sales Tax Credit (PEI Essentials Benefit from Nov 2026) |
| Quebec (4) | Family Allowance; QPIP; Solidarity Tax Credit; QPP retirement pension |
| Saskatchewan (3) | Low-Income Tax Credit; Seniors Income Plan; SAID |
| Yukon (2) | Yukon Child Benefit; Pioneer Utility Grant |

## Honest skips (2026-09-25)

| Programme | Why skipped |
|-----------|-------------|
| Canada Carbon Rebate | Ended. The consumer fuel charge stopped March 15, 2025 and the last payment was April 2025 (canada.ca). |
| GST/HST credit | Renamed the **Canada Groceries and Essentials Benefit** in July 2026 with the same rules. It is added as CGEB, and the old canada.ca page says "no longer available". |
| BC Climate Action Tax Credit | Ended with BC's consumer carbon tax (April 2025). |
| Nunavut Senior Fuel Subsidy | gov.nu.ca returns 403 to our network. The only reachable official document (the application form) does not state the eligibility thresholds. |
| Nova Scotia Heating Assistance Rebate Program (HARP) | The 2025–26 window has closed. novascotia.ca says new applications open 1 October 2026, but the 2026–27 amount and income limits are not yet published. |
| Ontario GAINS | Verified (up to C$92/month, OAS + GIS recipients) but held back to keep Ontario at 4 rows. It is the next candidate for Ontario. |
| BC Fair PharmaCare, Alberta Child Care Subsidy, provincial student grants | Not added this pass (they need income tables from separate pages). Candidates for the next wave. |

## Adding / updating Canada rows

1. Edit the `_federal.py` or `_provincial.py` rows (C$ amounts, official URL, notes, verify_notes).
2. Run `python3 scripts/canada_starter_pack_2026_09_25.py`. It is idempotent: it replaces rows by id and syncs both data trees plus catalogue_meta.
3. Run `python3 scripts/generate_pack_manifests.py`.
4. Append audit entries, re-sign (`scripts/sign_catalogue_release.py`), and run `scripts/check_catalogue_publish_ready.py`.
5. Run `backend/tests/test_canada_catalogue.py`, the full pytest suite, `npx tsx scripts/matcher-smoke.mts` and `next build`.
