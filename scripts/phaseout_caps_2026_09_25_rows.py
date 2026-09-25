"""Official zero-points for gradual phase-out benefits (2026-09-25).

Each entry: scheme id -> cap (local currency, annual), basis sentence appended to notes,
verify_notes (replaces), and optional tag changes. Figures come ONLY from official pages:
CRA (canada.ca), provincial governments / statutes, GOV.UK / gov.wales. The cap is the
income at which the benefit reaches zero for a generous but realistic family (4 children,
or the largest family size the official page tabulates). Rounded UP to the next dollar.
"""
from __future__ import annotations

CRA_CCB = "https://www.canada.ca/en/revenue-agency/services/child-family-benefits/canada-child-benefit/how-much.html"
CRA_CDB_TABLE = "https://www.canada.ca/en/revenue-agency/services/child-family-benefits/cdb-table-july-2026.html"
CRA_ON = "https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/province-ontario.html"
ON_LAW = "https://www.ontario.ca/laws/statute/07t11 (Taxation Act, 2007, s. 104(5))"
BC_FB = "https://www2.gov.bc.ca/gov/content/family-social-supports/affordability/family-benefit"
AB_LAW = "Alberta Personal Income Tax Act, RSA 2000 c A-30, s. 30.2 (kings-printer.alberta.ca)"
CRA_AB = "https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/province-alberta.html"
OEPTC_SR = "CRA 2026 OEPTC calculation sheet for married or common-law seniors"
CRA_NB = "https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/province-new-brunswick.html"
CRA_NT = "https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/northwest-territories.html"
CRA_NS = "https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/province-nova-scotia.html"

CAPS: dict[str, dict] = {
    "can-canada-child-benefit": {
        "cap": 318_300,
        "basis": "Catalogue cap C$318,300 = where the CCB reaches zero for 4 children under 6 (July 2026 – June 2027): max 4 × C$8,157 = C$32,628, reduced by C$10,260 + 9.5% of AFNI over C$82,847 (CRA formula for 4+ children). Smaller or older families reach zero earlier (e.g. 1 child under 6: about C$240,160).",
        "verify_notes": f"max_annual_income = official zero-point for 4 children under 6 (largest family size CRA tabulates as '4 or more'); computed from CRA 'How much you can get' ({CRA_CCB}). Still reaches middle and upper-middle incomes.",
        "remove_tags": ["universal"],
    },
    "can-child-disability-benefit": {
        "cap": 266_005,
        "basis": "Catalogue cap C$266,005 = where the CDB reaches zero for 3 DTC-eligible children (largest size in CRA's guideline table): 3 × C$3,480 reduced by 5.7% of AFNI over C$82,847. CRA's July 2026 table shows C$0.00 at C$270,000 for three dependants; one dependant reaches zero at about C$191,597.",
        "verify_notes": f"max_annual_income = official zero-point for 3 eligible dependants from CRA CDB guideline table July 2026 – June 2027 ({CRA_CDB_TABLE}).",
    },
    "can-on-child-benefit": {
        "cap": 114_861,
        "basis": "Catalogue cap C$114,861 = where the OCB reaches zero for 4 children: 4 × C$1,759.92 (C$146.66/month, July 2026 – June 2027, CRA) reduced by 8% of AFNI over C$26,865 (8% rate: Ontario Taxation Act, 2007 s. 104(5)). A 1-child family reaches zero at about C$48,864.",
        "verify_notes": f"max_annual_income = official zero-point for 4 children. Amount and threshold: CRA Ontario page ({CRA_ON}); 8% reduction rate: {ON_LAW}.",
    },
    "can-bc-family-benefit": {
        "cap": 170_937,
        "basis": "Catalogue cap C$170,937 = where the BC family benefit reaches zero for 4 children: the guaranteed minimums (C$775 + C$750 + C$725 + C$725 = C$2,975) are reduced by 4% of AFNI over C$96,562 until zero (July 2026 – June 2027, gov.bc.ca).",
        "verify_notes": f"max_annual_income = official zero-point for 4 children from the BC government page ({BC_FB}); the single-parent supplement is reduced in the first phase, so it does not raise the zero-point.",
    },
    "can-ab-child-family-benefit": {
        "cap": 70_143,
        "basis": "Catalogue cap C$70,143 = where the ACFB reaches zero for 4+ children: the base component (C$3,821) is reduced by 20.11% of AFNI over C$28,116 (zero at about C$47,115) and the working component (max C$2,061) by 8.95% of AFNI over C$47,115 (2026–27 amounts: CRA/alberta.ca; rates: Alberta Personal Income Tax Act s. 30.2). Every family size reaches zero at about C$70,100–70,150.",
        "verify_notes": f"max_annual_income = official zero-point for 4 or more children. Amounts/thresholds: CRA Alberta page ({CRA_AB}) and alberta.ca; reduction rates: {AB_LAW}.",
    },
    "can-on-trillium-benefit": {
        "cap": 117_971,
        "basis": "Catalogue cap C$117,971 = highest zero-point of the OTB components (2026 benefit year, 2025 income): OEPTC for a senior couple (max C$290 energy + C$1,198 property tax = C$1,488, reduced by 2% of AFNI over C$43,571). Other components end earlier: OEPTC non-senior family about C$101,659; OSTC for 2 adults + 4 children (6 × C$378, 4% over C$37,273 seniors' threshold) about C$93,973; NOEC family C$94,356.",
        "verify_notes": f"max_annual_income = largest official zero-point across OTB components, from {OEPTC_SR}, the CRA NOEC family calculation sheet, the CRA OSTC seniors' threshold Q&A and the CRA Ontario page ({CRA_ON}).",
    },
    "can-nb-hst-credit": {
        "cap": 85_000,
        "basis": "Catalogue cap C$85,000 = where the NB HST credit reaches zero for a couple with 4 children: C$300 + C$300 + 4 × C$100 = C$1,000, reduced by 2% of AFNI over C$35,000 (CRA New Brunswick page).",
        "verify_notes": f"max_annual_income = official zero-point for a couple with 4 children ({CRA_NB}); replaces the catalogue soft gate.",
    },
    "can-nt-child-benefit": {
        "cap": 80_000,
        "basis": "Catalogue cap C$80,000: CRA states the NWT child benefit is eliminated when adjusted family net income reaches C$80,000.",
        "verify_notes": f"max_annual_income = official elimination point stated by CRA ({CRA_NT} and T4114); replaces the catalogue soft gate.",
    },
    "can-ns-affordable-living-tax-credit": {
        "cap": 39_900,
        "basis": "Catalogue cap C$39,900 = where the NS affordable living tax credit reaches zero for a couple with 4 children: C$255 + 4 × C$60 = C$495, reduced by 5% of AFNI over C$30,000 (CRA Nova Scotia page, July 2026 – June 2027).",
        "verify_notes": f"max_annual_income = official zero-point for a family with 4 children ({CRA_NS}); replaces the catalogue soft gate.",
    },
    # --- United Kingdom: per-parent £100,000 limits imply a household maximum of £200,000
    "gb-tax-free-childcare": {
        "cap": 200_000,
        "basis": "Catalogue cap £200,000: you cannot get Tax-Free Childcare if you or your partner expects adjusted net income over £100,000, so no eligible two-parent household has more than 2 × £100,000 (single parents: £100,000).",
        "verify_notes": "max_annual_income = household maximum implied by the official per-parent £100,000 adjusted-net-income limit (GOV.UK Tax-Free Childcare eligibility). Adjusted net income is after pension contributions, so check gross incomes near the limit.",
    },
    "gb-eng-free-childcare-working-parents": {
        "cap": 200_000,
        "basis": "Catalogue cap £200,000: each parent must expect adjusted net income of £100,000 or less, so no eligible two-parent household has more than 2 × £100,000.",
        "verify_notes": "max_annual_income = household maximum implied by the official per-parent £100,000 limit (GOV.UK childcare for working parents).",
    },
    "gb-wls-childcare-offer": {
        "cap": 200_000,
        "basis": "Catalogue cap £200,000: each parent's gross income must be £100,000 or less, so no eligible two-parent household has more than 2 × £100,000.",
        "verify_notes": "max_annual_income = household maximum implied by the official per-parent £100,000 gross income limit (gov.wales Childcare Offer).",
    },
}

# Reviewed and deliberately left without a numeric cap (reason recorded in docs/COUNTRY_CANADA.md).
LEFT_UNGATED = {
    "can-qc-family-allowance": "Retraite Québec pays a minimum C$1,221 per child (2026) at every family income — no zero-point.",
    "can-old-age-security": "Recovery tax is on individual net income (full recovery ~C$150k+ per person); a household income figure cannot identify ineligibility for couples.",
    "can-resp-cesg": "Basic 20% CESG is paid at all incomes; only the additional CESG/CLB are income-tested.",
    "can-rdsp": "Grant is paid at all incomes (1:1 above the threshold); only the bond phases out.",
    "gb-child-benefit": "Universal; HICBC is a tax charge on individual income, and claiming still protects NI credits.",
    "gb-marriage-allowance": "Basic-rate test is on taxable income after pension contributions/Gift Aid ('usually' £12,571–£50,270) — no firm household zero-point.",
    "gb-winter-fuel-payment": "Recovered through tax only when an individual's taxable income is over £35,000; a lower-income partner keeps theirs.",
    "gb-sct-pension-age-winter-heating-payment": "Same individual £35,000 recovery rule as Winter Fuel Payment.",
}
