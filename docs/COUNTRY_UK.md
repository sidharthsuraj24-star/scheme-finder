# United Kingdom — catalogue country notes

**Added:** 2026-09-25 (IST) · **Rows:** 60 (`gb-*`) · **Packs:** `uk-wide`, `uk-england`,
`uk-scotland`, `uk-wales`, `uk-northern-ireland` (all `@1.0.0`)
**Generator:** `scripts/uk_starter_pack_2026_09_25.py` (rows in `scripts/uk_starter_pack_2026_09_25_rows.py`)

Product aim: one worldwide benefits hub for poor, middle-class **and** wealthy households.
The UK starter pack therefore covers means-tested support *and* universal / tax / savings
schemes that higher earners can use within their real limits.

## Conventions

| Topic | UK rule |
|-------|---------|
| Scheme id prefix | `gb-` (ISO 3166 GB). **`uk-` is already used by India/Uttarakhand** — never use it for UK rows. Nation-only rows: `gb-eng-*`, `gb-sct-*`, `gb-wls-*`, `gb-ni-*`. |
| `eligibility_rules.countries` | `["United Kingdom"]` |
| Regions | The four nations: `England`, `Scotland`, `Wales`, `Northern Ireland` (wizard region picker; normalised to `england` / `scotland` / `wales` / `northern_ireland`). |
| UK-wide rows | `states: []`, `nationwide: true` → pack `uk-wide` (kind `country_national`). |
| Nation rows | `states: [..nations..]`, `nationwide: false` → one `uk-<nation>` pack per listed nation (kind `nation`). A row valid in several nations (e.g. PIP for England + Wales + NI) appears in each. |
| Tags | `united_kingdom` + nation tags. **Never** `central` / `nationwide` / `federal` (those drive India/US pack buckets). |
| Currency | `£` (GBP) in the wizard/results (`frontend/src/lib/countries.ts`) and in explanation strings (`£60,000`, `£45,000`). |
| Sources | Official only: gov.uk, mygov.scot, gov.scot, transport.gov.scot, gov.wales, nidirect.gov.uk. Healthy Start apply link is the NHS BSA service linked from gov.uk. |

**Why mygov.scot:** it is the Scottish Government's official citizen information portal;
Social Security Scotland (socialsecurity.gov.scot) links to mygov.scot for eligibility
detail and applications for Scottish Child Payment, Best Start, ADP, CDP, Carer Support
Payment, etc.

## Income handling (no India bands, no US gate)

- **India PRICE ICE 360 bands never apply** to UK profiles (`income_band*` fields stay null).
- **US $60k gate is not reused.** The UK has its own soft gate:
  `IMPLIES_LOW_INCOME_ANNUAL_GATE_GBP = 60_000` (backend `app/matcher.py`, frontend
  `src/lib/matching/matcher.ts`).
  - It is a **catalogue heuristic**, not an official means-test line. The anchor is HMRC's
    High Income Child Benefit Charge threshold (£60,000 adjusted net income), which is the
    UK's clearest official "higher income" marker.
  - It applies **only** to rows with `implies_low_income: true` **and** no numeric
    `max_annual_income` / `max_monthly_household_income`. Those rows are genuinely
    means-tested (UC, Pension Credit, Help to Save, Healthy Start, Scottish Child Payment,
    Best Start, CTR, Warm Home Discount, Cold Weather Payment, etc.). Real UK means tests
    are benefit-linked or taper, so no single official annual figure exists for them.
- **Official household ceilings are encoded as hard caps only where gov pages state one:**
  Shared Ownership and First Homes use £90,000 (London cap; £80,000 elsewhere, noted in
  verify_notes), NI Education Maintenance Allowance uses £22,500, and NI Discretionary
  Support uses £29,741.
- **Per-parent childcare limits imply a household maximum (2026-09-25).** Tax-Free
  Childcare, childcare for working parents (England) and the Wales Childcare Offer require
  **each** parent to be at or under £100,000 (adjusted net income on GOV.UK; gross income in
  Wales), so no eligible household has more than 2 × £100,000: these carry
  `max_annual_income: 200000` with the basis in notes. A £250k household no longer sees them;
  a £150k two-earner household still does.
- **Other per-person limits are NOT household caps.** Marriage Allowance uses tax bands on
  taxable income ("usually" £12,571–£50,270, moved by pension contributions / Gift Aid),
  HICBC uses £60k/£80k (Child Benefit stays universal), and Winter Fuel / Pension Age
  Winter Heating Payment are recovered above £35k of an individual's income. These stay in
  `notes` with `max_annual_income: null`.
- Non-means-tested rows (Child Benefit, State Pension, ISAs / LISA / JISA, pension
  relief, SDLT relief, Boiler Upgrade Scheme, PIP / ADP / AA / PADP, universal meals and
  childcare, free bus travel) have `implies_low_income: false` and `max_annual_income: null`.
  Tag them `universal` / `middle-class` / `upper-middle-class` / `high-income-eligible`
  as accurate.

## Schemes (2026-27 rates, last_verified 2026-09-25)

**UK-wide (12):** Universal Credit; Child Benefit (HICBC note); Tax-Free Childcare;
New State Pension; Pension Credit; Help to Save; Lifetime ISA; Junior ISA; ISA allowance;
Marriage Allowance; Maternity Allowance; pension tax relief.

**Multi-nation (17):**
- England, Wales and NI: PIP, DLA for children, Carer's Allowance, Attendance
  Allowance, Winter Fuel Payment, Healthy Start, Disabled Facilities Grant.
- England and Wales: Cold Weather Payment, Sure Start Maternity Grant, Council Tax
  single person discount, Boiler Upgrade Scheme.
- England, Scotland and Wales: Warm Home Discount, Access to Work, Blue Badge,
  Council Tax Reduction, Budgeting Loan.
- England and NI: SDLT first-time buyer relief.

**England (8):** Free childcare for working parents (30 hours), 15 hours for all 3–4 year
olds, free school meals, Shared Ownership, First Homes, Right to Buy, student finance,
older person's bus pass.

**Scotland (15):** Scottish Child Payment, Best Start Grant, Best Start Foods, Adult
Disability Payment, Child Disability Payment, Carer Support Payment, Pension Age Disability
Payment, Pension Age Winter Heating Payment, Winter Heating Payment, Young Carer Grant, Job
Start Payment, 1,140 hours funded ELC, P1–P5 free school lunches, under-22s free bus,
60+/disabled free bus.

**Wales (5):** Childcare Offer for Wales, Universal Primary Free School Meals, School
Essentials Grant, Discretionary Assistance Fund, free prescriptions.

**Northern Ireland (3):** Education Maintenance Allowance, Discretionary Support, Lone
Pensioner Allowance. (NI claims for UC, PIP, Carer's Allowance, AA, DLA, Pension Credit
and Winter Fuel Payment are noted on the UK / multi-nation rows, which route to nidirect.)

## Honest skips (this pass)

- Help to Buy Equity Loan: closed to new applications in 2023.
- Help to Buy ISA: closed to new savers in 2019.
- Tax credits: ended April 2025 (replaced by UC).
- Child Trust Fund: closed.
- Nest (Wales): eligibility not clear enough on the official page.
- NI rate relief, NI free school meals / uniform grant, NI Affordable Warmth, NI Cold
  Weather Payment / Sure Start Maternity Grant / Access to Work / Blue Badge: official
  nidirect page not confirmed (404s or not checked). Those multi-nation rows are limited
  to GB nations.
- Scottish free prescriptions and Scottish Funeral Support Payment: official page not
  confirmed this pass.

## Known limitations

- Child-disability rows (DLA children, Child Disability Payment) use the profile
  `disability` flag as a household signal because the wizard has no separate child
  disability field.
- State Pension age is encoded as `min_age: 66`. The phased rise to 67 means some
  borderline birth dates need checking on gov.uk.
- `ml`/`hi` scheme text copies EN (same as US rows); country names in the UI are not
  translated.
