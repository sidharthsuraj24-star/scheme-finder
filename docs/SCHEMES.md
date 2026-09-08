# Scheme Finder — Seed Schemes (Phase 1)
Curated from official government sources. **Do not treat as legal advice.** Re-verify before production matching.

**Count:** 18 schemes
**verify=true:** 12
**verify=false:** 6

| # | id | Name (EN) | Official source | Key eligibility | verify |
|---|----|-----------|-----------------|-----------------|--------|
| 1 | `kerala-old-age-pension` | Indira Gandhi National Old Age Pension Scheme (Kerala Sevana) | https://welfarepension.lsgkerala.gov.in/FAQsEng.aspx | min_age=60; max_annual_income=100000 | no |
| 2 | `kerala-widow-pension` | Indira Gandhi National Widow Pension Scheme (Kerala Sevana) | https://welfarepension.lsgkerala.gov.in/FAQsEng.aspx | max_annual_income=100000; gender=female; marital=widow,husband_missing_7_years,deserted_7_years_over_50 | no |
| 3 | `kerala-disability-pension-physical` | Indira Gandhi National Disability Pension – Physically Challenged (Kerala Sevana) | https://welfarepension.lsgkerala.gov.in/FAQsEng.aspx (+ LSGD ipcp) | max_annual_income=100000; disability>=40; no age limit | **YES** |
| 4 | `kerala-unmarried-women-pension` | Pension for Unmarried Women above 50 years (Kerala Sevana) | https://welfarepension.lsgkerala.gov.in/FAQsEng.aspx | min_age=50; max_annual_income=100000; gender=female; marital=unmarried | no |
| 5 | `kerala-agri-labour-pension` | Agricultural Labour Pension (Kerala Sevana) | https://welfarepension.lsgkerala.gov.in/FAQsEng.aspx | min_age=60; max_annual_income=100000; occupations=agricultural_labour | no |
| 6 | `kerala-disability-pension-mental` | Indira Gandhi National Disability Pension – Mentally Challenged (Kerala) | https://lsgkerala.gov.in/en/welfarepension/imcp | max_annual_income=100000; disability>=40 | **YES** |
| 7 | `pm-kisan` | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | https://pmkisan.gov.in/ | occupations=farmer,landholding_farmer | **YES** |
| 8 | `kerala-kasp-pmjay` | Ayushman Bharat PM-JAY – Karunya Arogya Suraksha Padhathi (KASP) | http://www.sha.kerala.gov.in./?lang=en&page_id=742 | categories=SECC_deprivation,RSBY_CHIS_2018_19 | **YES** |
| 9 | `nsap-nfbs` | National Family Benefit Scheme (NFBS) | https://nsap.nic.in/ | categories=BPL | **YES** |
| 10 | `kerala-egrantz` | e-Grantz – Post-Matric Educational Assistance (SC/ST/OBC Kerala) | https://www.egrantz.kerala.gov.in/ | occupations=student; categories=SC,ST,OBC,OEC | **YES** |
| 11 | `adip-assistive-devices` | ADIP – Assistance to Disabled Persons for Purchase/Fitting of Aids/Appliances | https://www.adip.depwd.gov.in/faq_adip | max_monthly_hh=30000; disability>=40 | no |
| 12 | `kerala-life-mission` | LIFE Mission (Livelihood Inclusion Financial Empowerment) – Kerala Housing | https://lifemission.kerala.gov.in/life-project | categories=homeless,landless,incomplete_house,temporary_shelter | **YES** |
| 13 | `pmmvy` | Pradhan Mantri Matru Vandana Yojana (PMMVY) | https://wcd.gov.in/women/pradhan-mantri-matru-vandana-yojna | max_annual_income=800000; gender=female; categories=SC,ST,BPL,PMJAY | no |
| 14 | `depwd-scholarship-swd` | Scholarships for Students with Disabilities (DEPwD / NSP) | https://depwd.gov.in/en/scholarship/ | max_annual_income=250000; disability>=40; occupations=student | **YES** |
| 15 | `kerala-matru-jyothi` | Matru Jyothi – Financial Assistance for PwD Mothers (Kerala) | https://sjd.kerala.gov.in/scheme-info.php?scheme_id=IDExOA%3D%3D | max_annual_income=100000; gender=female; disability>=60 | **YES** |
| 16 | `ayyankali-uegs` | Ayyankali Urban Employment Guarantee Scheme (Kerala) | https://lsgd.kerala.gov.in/en/state-sponsored-schemes-under-lsgd/ayyankali-uegs/ | min_age=18; occupations=unskilled_manual_labour; categories=urban_household | **YES** |
| 17 | `janani-suraksha-yojana-kerala` | Janani Suraksha Yojana (JSY) – Kerala | http://health.kerala.gov.in/financialaiditemPDF/eyJpdiI6IjJ3YVJ5TTJuK3VxTWIvaUMyWS8yU3c9PSIsInZhbHVlIjoiTXpfY3pGYzIrTUtHRU85NzVhNHl4QT09IiwibWFjIjoiMzU2YWYxZjFjZTNkYjM1ZmM5Nzk3ODhjYzhhNDA0MWZhNjJkZTZhYmFiNDZkMTZkNjNjNjEzNzFmNjVlM2E3YSIsInRhZyI6IiJ9 | min_age=19; gender=female; categories=BPL,SC,ST | **YES** |
| 18 | `kerala-karunya-benevolent-fund` | Karunya Benevolent Fund (KBF) | http://health.kerala.gov.in/financialaiditemPDF/eyJpdiI6IkhVc1VwY1FMNTlTSlpkZ1E5ZHZKcnc9PSIsInZhbHVlIjoiLzVqUzVvMEs5a0pTYkRGSGNERjBGZz09IiwibWFjIjoiNDFkMmIzZWViMTY3MGU2YmRkZTg0NWUxMDMxY2ZhOTg0NjRjN2JiNzFlMzAzODhjZTUwOTY5ZmQ5MjcwNzU5OSIsInRhZyI6IiJ9 | max_annual_income=300000 | **YES** |

## Verify flags detail

### `kerala-old-age-pension` (verify=false)
- **verify_notes:** Hard filters age≥60 and income≤1 lakh are UI-collectable. Sevana criteria table lists Rs.2000/month; page also mentions 75+ special amount Rs.1500 — do NOT invent whether special amount is additive or replacement. Disqualifiers not fully in questionnaire.

### `kerala-widow-pension` (verify=false)
- **verify_notes:** Hard filters gender/marital/income UI-collectable. Matcher must encode deserted case as age≥50 (`deserted_7_years_over_50`). Residence ≥2 years, remarriage, land, other Sevana exclusions not fully in questionnaire.

### `kerala-disability-pension-physical` (verify=true)
- **verify_notes:** CONFLICT: Sevana FAQ allows max two pensions (disability may be additional); LSGD ipcp says must not receive/apply for another social-welfare pension. Also Rs.2000 table vs 80%+ special Rs.1100 — amount meaning unverified. Keep verify=true.

### `kerala-unmarried-women-pension` (verify=false)
- **verify_notes:** Hard filters age≥50, female, unmarried, income≤1 lakh UI-collectable. Land/protection/pensioner exclusions retained in notes.

### `kerala-agri-labour-pension` (verify=false)
- **verify_notes:** Hard filters age/income/occupation UI-collectable. UI does not yet collect KAWWF membership, ≥10 years agri work, ≥10 years residence, plantation exclusion — kept in notes.

### `kerala-disability-pension-mental` (verify=true)
- **verify_notes:** Browser Sevana pass 2026-09-08 could not confirm distinct Sevana scheme name for mental vs physical (blank FAQ rows; HPWC timed out). Prefer physical IGNDPS hard filters + LSGD imcp cite; do not invent name from blank rows.

### `pm-kisan`
- **verify_notes:** Reconcile historical 'upto 2 hectare' FAQ wording with current pmkisan.gov.in homepage text 'all land holding farmer families'. Exclusions are clear from official portal.

### `kerala-kasp-pmjay`
- **verify_notes:** SHA FAQ states new registrations other than Q1 categories had not started; confirm whether Kerala has since expanded beneficiary universe. Matching should treat SECC/RSBY/CHIS flags as primary signals rather than raw income.

### `nsap-nfbs`
- **verify_notes:** Age of deceased breadwinner differs across NSAP pages (18-59 in Nov 2025 PIB brief vs 18-64 on some nsap.nic.in FAQ text). Confirm Kerala implementation channel and current amount before matching on age band.

### `kerala-egrantz`
- **verify_notes:** e-Grantz hosts multiple department schemes with different income ceilings. Do not apply a single income cap to all categories; verify per caste department circular for the academic year.

### `kerala-life-mission`
- **verify_notes:** HEAVY VERIFY: Primary lifemission.kerala.gov.in pages define beneficiary categories but do not publish a single clear numeric income ceiling. Secondary blogs cite varying income limits — ignore those. Confirm current PMAY-LIFE convergence rules, waitlist process, and whether open online application exists vs survey-only before enabling hard income filters.

### `depwd-scholarship-swd`
- **verify_notes:** Guidelines revised Sept 2024/2025 on depwd.gov.in — confirm latest income ceilings and component names from current PDF before hard-coding Top Class vs Pre/Post Matric distinctions in matcher.

### `kerala-matru-jyothi`
- **verify_notes:** Page states '60 percent or more' in eligibility point 1, but disability-type table includes some categories at 50% (e.g., autism, muscular dystrophy). Matcher should prefer type-specific % from official table; set verify until type mapping is encoded.

### `ayyankali-uegs`
- **verify_notes:** LSGD page is high-level; fetch auegskerala.gov.in operational guidelines for exact registration age, residency, and exclusion rules before tightening matcher fields.

### `janani-suraksha-yojana-kerala`
- **verify_notes:** Confirm whether Kerala still uses these exact cash amounts and age (>19) on current NHM circulars; page is an official health.kerala.gov.in financial-aid item.

### `kerala-karunya-benevolent-fund`
- **verify_notes:** Eligibility/benefits from Kerala Health Dept Karunya financial-aid item (KBF income < Rs.3 lakh, not KASP-eligible; up to Rs.2 lakh / Rs.3 lakh kidney). Encrypted financialaiditemPDF URL may rotate — re-verify permalink.


## Notes
- Malayalam (`ml`) fields: UI + main scheme copy improved; document lists translated for catalogue entries. Still welcome native review (see DECISIONS).
- Sevana pension amounts (browser pass 2026-09-08): criteria tables list **Rs.2000** base for listed pensions; special amounts noted for Old Age 75+ (Rs.1500) and Disability 80%+ (Rs.1100) — **do not invent** whether special amounts are additive or replacement; keep benefits.verify-style notes.
- See `docs/BROWSER_SEVANA_NOTES.md` for the full 2026-09-08 Sevana FAQ research summary.
