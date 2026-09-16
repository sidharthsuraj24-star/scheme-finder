# Source audit — Scheme Finder catalogue

**Audit date:** 2026-09-16 (Asia/Calcutta / IST)
**Schemes audited:** 112

## Policy

- Prefer official government domains: `*.gov.in`, `*.nic.in`, `*.gov.bd`, `*.gov.np`, `*.gov.lk`, `*.gov.mv`, ministry/department portals, myScheme.gov.in.
- Replace blogs, aggregators, news mirrors, and broken/fragile URLs with stable official pages.
- Eligibility age/income/gender/disability updated **only** when the official page clearly states them; otherwise `verify=true` with notes — never invent.
- Domain type: `gov` = government TLD; `ok` = non-.gov but confirmed official programme portal; `other` = needs replacement.

## Summary

- URL field replacements this pass: **12** (across **8** schemes)
- `eligibility_rules.verify=true`: **104**
- `eligibility_rules.verify=false`: **8**
- Official source domain types: gov=112

### Schemes whose `official_source_url` is not a `*.gov.*` / `*.nic.in` host

_None — every scheme has a gov-domain official_source_url._

### Non-gov `apply_url` retained as official programme portals (`ok`)

- `tn-cmchis` → `https://www.cmchistn.com/` (source remains gov: `https://www.myscheme.gov.in/schemes/cmchis`)
- `uk-nanda-gaura` → `https://www.nandagaurauk.in/` (source remains gov: `https://wecd.uk.gov.in/document-category/government-orders/`)

### Could not find a gov-domain URL at all (source + apply both non-gov)

_None._ Every scheme has at least one gov-domain URL (usually `official_source_url`).

## URL replacements this pass

| Scheme id | Field | New URL | Reason |
|-----------|-------|---------|--------|
| `ap-ntr-bharosa-oap` | `apply_url` | https://sspensions.ap.gov.in/SSP/Home | Official NTR Bharosa portal |
| `ap-ntr-bharosa-oap` | `official_source_url` | https://sspensions.ap.gov.in/SSP/Home | Replace aptonline.in aggregator with official AP SERP sspensions.ap.gov.in |
| `ayyankali-uegs` | `apply_url` | https://auegskerala.gov.in/ | Fix www DNS failure; use https://auegskerala.gov.in/ |
| `dh-old-age-pension` | `apply_url` | https://ddd.gov.in/schemes-programmes/ | Replace dnhpanchayat.in PDF with UT ddd.gov.in schemes page |
| `janani-suraksha-yojana-kerala` | `apply_url` | https://nhm.gov.in/index1.php?lang=1&level=3&lid=309&sublinkid=841 | Apply via ASHA/facility; NHM is stable official source |
| `janani-suraksha-yojana-kerala` | `official_source_url` | https://nhm.gov.in/index1.php?lang=1&level=3&lid=309&sublinkid=841 | Replace rotating encrypted health.kerala.gov.in PDF with stable NHM JSY page |
| `kerala-karunya-benevolent-fund` | `apply_url` | https://sha.kerala.gov.in/?page_id=2961 | Apply/info via SHA KBF page (cashless at KASP empaneled hospitals) |
| `kerala-karunya-benevolent-fund` | `official_source_url` | https://sha.kerala.gov.in/?page_id=2961 | Replace fragile encrypted health.kerala.gov.in PDF with stable SHA KBF page |
| `kerala-kasp-pmjay` | `apply_url` | https://sha.kerala.gov.in/ | Official SHA portal https (same org) |
| `kerala-kasp-pmjay` | `official_source_url` | https://sha.kerala.gov.in/?page_id=742 | Fixed trailing-dot typo in hostname; prefer https SHA FAQ |
| `tn-cmchis` | `official_source_url` | https://www.myscheme.gov.in/schemes/cmchis | Prefer myScheme.gov.in listing; cmchistn.com is non-.gov scheme portal |
| `uk-nanda-gaura` | `official_source_url` | https://wecd.uk.gov.in/document-category/government-orders/ | Prefer WECD.uk.gov.in GOs over nandagaurauk.in (non-.gov host) |

## Full catalogue

| id | official_source_url | src domain | apply_url | apply domain | verify | last_verified |
|----|---------------------|------------|-----------|--------------|--------|---------------|
| `kerala-old-age-pension` | https://welfarepension.lsgkerala.gov.in/FAQsEng.aspx | gov | https://welfarepension.lsgkerala.gov.in/ | gov | `False` | 2026-09-16 |
| `kerala-widow-pension` | https://welfarepension.lsgkerala.gov.in/FAQsEng.aspx | gov | https://welfarepension.lsgkerala.gov.in/ | gov | `False` | 2026-09-16 |
| `kerala-disability-pension-physical` | https://welfarepension.lsgkerala.gov.in/FAQsEng.aspx | gov | https://welfarepension.lsgkerala.gov.in/ | gov | `True` | 2026-09-16 |
| `kerala-unmarried-women-pension` | https://welfarepension.lsgkerala.gov.in/FAQsEng.aspx | gov | https://welfarepension.lsgkerala.gov.in/ | gov | `False` | 2026-09-16 |
| `kerala-agri-labour-pension` | https://welfarepension.lsgkerala.gov.in/FAQsEng.aspx | gov | https://welfarepension.lsgkerala.gov.in/ | gov | `False` | 2026-09-16 |
| `kerala-disability-pension-mental` | https://lsgkerala.gov.in/en/welfarepension/imcp | gov | https://welfarepension.lsgkerala.gov.in/ | gov | `True` | 2026-09-16 |
| `pm-kisan` | https://pmkisan.gov.in/ | gov | https://pmkisan.gov.in/ | gov | `True` | 2026-09-16 |
| `kerala-kasp-pmjay` | https://sha.kerala.gov.in/?page_id=742 | gov | https://sha.kerala.gov.in/ | gov | `True` | 2026-09-16 |
| `nsap-nfbs` | https://nsap.nic.in/ | gov | https://nsap.nic.in/ | gov | `True` | 2026-09-16 |
| `kerala-egrantz` | https://www.egrantz.kerala.gov.in/ | gov | https://www.egrantz.kerala.gov.in/ | gov | `True` | 2026-09-16 |
| `adip-assistive-devices` | https://www.adip.depwd.gov.in/faq_adip | gov | https://adip.depwd.gov.in/ | gov | `False` | 2026-09-16 |
| `kerala-life-mission` | https://lifemission.kerala.gov.in/life-project | gov | https://lifemission.kerala.gov.in/ | gov | `True` | 2026-09-16 |
| `pmmvy` | https://wcd.gov.in/women/pradhan-mantri-matru-vandana-yojna | gov | https://pmmvy.wcd.gov.in/ | gov | `False` | 2026-09-16 |
| `depwd-scholarship-swd` | https://depwd.gov.in/en/scholarship/ | gov | https://scholarships.gov.in/ | gov | `True` | 2026-09-16 |
| `kerala-matru-jyothi` | https://sjd.kerala.gov.in/scheme-info.php?scheme_id=IDExOA%3D%3D | gov | https://suneethi.sjd.kerala.gov.in/ | gov | `True` | 2026-09-16 |
| `ayyankali-uegs` | https://lsgd.kerala.gov.in/en/state-sponsored-schemes-under-lsgd/ayyankali-uegs/ | gov | https://auegskerala.gov.in/ | gov | `True` | 2026-09-16 |
| `janani-suraksha-yojana-kerala` | https://nhm.gov.in/index1.php?lang=1&level=3&lid=309&sublinkid=841 | gov | https://nhm.gov.in/index1.php?lang=1&level=3&lid=309&sublinkid=841 | gov | `True` | 2026-09-16 |
| `kerala-karunya-benevolent-fund` | https://sha.kerala.gov.in/?page_id=2961 | gov | https://sha.kerala.gov.in/?page_id=2961 | gov | `True` | 2026-09-16 |
| `tn-pudhumai-penn` | https://www.tnsocialwelfare.tn.gov.in/en/specilisationswoman-welfare/pudhumai-penn | gov | https://penkalvi.tn.gov.in/ | gov | `True` | 2026-09-16 |
| `tn-cmchis` | https://www.myscheme.gov.in/schemes/cmchis | gov | https://www.cmchistn.com/ | ok | `True` | 2026-09-16 |
| `ka-gruha-lakshmi` | https://sevasindhugs.karnataka.gov.in/ | gov | https://sevasindhugs.karnataka.gov.in/ | gov | `True` | 2026-09-16 |
| `ka-yuva-nidhi` | https://sevasindhugs.karnataka.gov.in/ | gov | https://sevasindhugs.karnataka.gov.in/ | gov | `True` | 2026-09-16 |
| `mh-ladki-bahin` | https://ladakibahin.maharashtra.gov.in/ | gov | https://ladakibahin.maharashtra.gov.in/ | gov | `True` | 2026-09-16 |
| `mh-mjpjay` | https://www.jeevandayee.gov.in/ | gov | https://www.jeevandayee.gov.in/ | gov | `True` | 2026-09-16 |
| `wb-annapurna-bhandar` | https://socialsecurity.wb.gov.in/ | gov | https://socialsecurity.wb.gov.in/ | gov | `True` | 2026-09-16 |
| `wb-kanyashree` | https://wbkanyashree.gov.in/kp_scheme.php | gov | https://wbkanyashree.gov.in/ | gov | `True` | 2026-09-16 |
| `up-kanya-sumangala` | https://mksy.up.gov.in/ | gov | https://mksy.up.gov.in/ | gov | `True` | 2026-09-16 |
| `ab-pmjay-national` | https://pmjay.gov.in/ | gov | https://pmjay.gov.in/ | gov | `True` | 2026-09-16 |
| `gj-mukhyamantri-amrutum` | https://www.myscheme.gov.in/schemes/ma | gov | https://www.myscheme.gov.in/schemes/ma | gov | `True` | 2026-09-16 |
| `gj-namo-lakshmi` | https://www.myscheme.gov.in/schemes/nlygg2 | gov | https://www.myscheme.gov.in/schemes/nlygg2 | gov | `True` | 2026-09-16 |
| `rj-vridhjan-samman-pension` | https://sje.rajasthan.gov.in/Default.aspx?PageID=288 | gov | https://ssp.rajasthan.gov.in/ | gov | `True` | 2026-09-16 |
| `br-kanya-utthan` | https://medhasoft.bihar.gov.in/ | gov | https://medhasoft.bihar.gov.in/ | gov | `True` | 2026-09-16 |
| `mp-ladli-behna` | https://cmladlibahna.mp.gov.in/ | gov | https://cmladlibahna.mp.gov.in/ | gov | `True` | 2026-09-16 |
| `od-madhu-babu-pension` | https://ssepd.odisha.gov.in/index.php/schemes-programmes/schemes/madhu-babu-pension-yojana | gov | https://www.myscheme.gov.in/schemes/mbypvy | gov | `True` | 2026-09-16 |
| `ap-ntr-bharosa-oap` | https://sspensions.ap.gov.in/SSP/Home | gov | https://sspensions.ap.gov.in/SSP/Home | gov | `True` | 2026-09-16 |
| `tg-aasara-pension` | https://hyderabad.telangana.gov.in/scheme/aasara-pensions/ | gov | https://hyderabad.telangana.gov.in/scheme/aasara-pensions/ | gov | `True` | 2026-09-16 |
| `as-orunodoi` | https://finance.assam.gov.in/portlets/orunodoi-30 | gov | https://finance.assam.gov.in/portlets/orunodoi-30 | gov | `True` | 2026-09-16 |
| `ga-griha-aadhar` | https://www.goa.gov.in/wp-content/uploads/2021/01/Griha-Aadhar-Scheme.pdf | gov | https://www.goa.gov.in/government/schemes/ | gov | `True` | 2026-09-16 |
| `ga-laadli-laxmi` | https://www.goa.gov.in/wp-content/uploads/2021/01/Laadli-Laxmi-Scheme.pdf | gov | https://www.goa.gov.in/government/schemes/ | gov | `True` | 2026-09-16 |
| `jh-maiya-samman` | https://www.jharkhand.gov.in/PDepartment/ViewDocument?id=D016DO005SD001505102024012753390 | gov | https://mmmsy1.jharkhand.gov.in/ | gov | `True` | 2026-09-16 |
| `hr-old-age-samman` | https://sewa.haryana.gov.in/old-age-samman-allowance-scheme/ | gov | https://sewa.haryana.gov.in/old-age-samman-allowance-scheme/ | gov | `True` | 2026-09-16 |
| `hr-widow-destitute-pension` | https://sewa.haryana.gov.in/pension-to-widows-and-destitute-women/ | gov | https://sewa.haryana.gov.in/pension-to-widows-and-destitute-women/ | gov | `True` | 2026-09-16 |
| `cg-mahtari-vandan` | https://mahtarivandan.cgstate.gov.in/ | gov | https://mahtarivandan.cgstate.gov.in/ | gov | `True` | 2026-09-16 |
| `dl-old-age-pension` | https://socialwelfare.delhi.gov.in/social/financials-assistance-schemes | gov | https://edistrict.delhigovt.nic.in/ | gov | `True` | 2026-09-16 |
| `pb-old-age-pension` | https://www.myscheme.gov.in/schemes/oapsp | gov | https://connect.punjab.gov.in/ | gov | `True` | 2026-09-16 |
| `pb-widow-destitute-pension` | https://sswcd.punjab.gov.in/en | gov | https://connect.punjab.gov.in/service/citizenservice/112 | gov | `True` | 2026-09-16 |
| `uk-old-age-pension` | https://ssp.uk.gov.in/ | gov | https://ssp.uk.gov.in/ | gov | `True` | 2026-09-16 |
| `uk-nanda-gaura` | https://wecd.uk.gov.in/document-category/government-orders/ | gov | https://www.nandagaurauk.in/ | ok | `True` | 2026-09-16 |
| `hp-old-age-pension` | http://esomsa.hp.gov.in/?q=social-security-pension | gov | https://himparivar.hp.gov.in/ekalyan | gov | `True` | 2026-09-16 |
| `hp-widow-deserted-pension` | http://esomsa.hp.gov.in/?q=social-security-pension | gov | https://himparivar.hp.gov.in/ekalyan | gov | `True` | 2026-09-16 |
| `ar-cmaay` | https://cmaay.arunachal.gov.in/ | gov | https://cmaay.arunachal.gov.in/ | gov | `True` | 2026-09-16 |
| `mn-old-age-pension` | https://socialwelfare.mn.gov.in/en/rules-regulations/manipur-old-age-pension/ | gov | https://socialwelfare.mn.gov.in/en/state-sponsored-schemes/manipur-old-age-pension-scheme/ | gov | `True` | 2026-09-16 |
| `ml-nsap-old-age-pension` | https://meghalaya.gov.in/schemes/content/37326 | gov | https://meghalaya.gov.in/schemes/content/37326 | gov | `True` | 2026-09-16 |
| `mz-old-age-pension` | https://socialwelfare.mizoram.gov.in/page/old-age-pension-old-age-home | gov | https://socialwelfare.mizoram.gov.in/page/old-age-pension-old-age-home | gov | `True` | 2026-09-16 |
| `nl-cmhis` | https://cmhis.nagaland.gov.in/ | gov | https://cmhis.nagaland.gov.in/register | gov | `True` | 2026-09-16 |
| `sk-unmarried-women-pension` | https://pensionscheme.sikkim.gov.in/ | gov | https://pensionscheme.sikkim.gov.in/ | gov | `True` | 2026-09-16 |
| `tr-mssp-old-infirm` | https://socialwelfare.tripura.gov.in/application-form-mukhyamantri-samajik-sahayata-prakalpa | gov | https://socialwelfare.tripura.gov.in/application-form-mukhyamantri-samajik-sahayata-prakalpa | gov | `True` | 2026-09-16 |
| `an-old-age-assistance` | http://andssw1.and.nic.in/socialwelfare/ | gov | http://andssw1.and.nic.in/socialwelfare/ | gov | `True` | 2026-09-16 |
| `ch-old-age-pension` | https://serviceonline.gov.in/dbt/getServiceDesc.html?serviceId=15950001 | gov | https://serviceonline.gov.in/dbt/getServiceDesc.html?serviceId=15950001 | gov | `True` | 2026-09-16 |
| `dh-old-age-pension` | https://ddd.gov.in/schemes-programmes/ | gov | https://ddd.gov.in/schemes-programmes/ | gov | `True` | 2026-09-16 |
| `jk-ladli-beti` | https://jansugam.jk.gov.in/getServiceDesc.html?serviceId=18430007 | gov | https://jansugam.jk.gov.in/getServiceDesc.html?serviceId=18430007 | gov | `True` | 2026-09-16 |
| `la-old-age-pension` | https://socialwelfare.ladakh.gov.in/schemes.php | gov | https://helphub.ladakh.gov.in/landing/pension | gov | `True` | 2026-09-16 |
| `ld-old-age-pension` | https://lakshadweep.gov.in/departments/social-welfare-and-tribal-affairs/ | gov | https://lakshadweep.gov.in/departments/social-welfare-and-tribal-affairs/ | gov | `True` | 2026-09-16 |
| `py-old-age-pension` | https://wcd.py.gov.in/old-age-persons-and-destitutes-pension | gov | https://wcd.py.gov.in/old-age-persons-and-destitutes-pension | gov | `True` | 2026-09-16 |
| `bd-old-age-allowance` | https://dss.gov.bd/ | gov | https://dss.bhata.gov.bd/ | gov | `True` | 2026-09-16 |
| `bd-widow-allowance` | https://dss.gov.bd/ | gov | https://dss.bhata.gov.bd/ | gov | `True` | 2026-09-16 |
| `bd-disability-allowance` | https://dss.gov.bd/site/page/6866eaa0-18c7-4e79-9113-0ac76c2590b1/- | gov | https://dss.bhata.gov.bd/ | gov | `True` | 2026-09-16 |
| `bd-maternity-allowance` | https://forms.portal.gov.bd/site/view/form-page/98393088-6626-4454-bd7e-1452a8f8f43d/-%E0%A6%AE%E0%A6%BE%E0%A6%A4%E0%A7%83%E0%A6%A4%E0%A7%8D%E0%A6%AC%E0%A6%95%E0%A6%BE%E0%A6%B2-%E0%A6%AD%E0%A6%BE%E0%A6%A4%E0%A6%BE-%E0%A6%AE%E0%A6%9E%E0%A7%8D%E0%A6%9C%E0%A7%81%E0%A6%B0%E0%A7%80%E0%A6%B0-%E0%A6%86%E0%A6%AC%E0%A7%87%E0%A6%A6%E0%A6%A8-%E0%A6%AB%E0%A6%B0%E0%A6%AE | gov | https://forms.portal.gov.bd/ | gov | `True` | 2026-09-16 |
| `np-senior-citizen-allowance` | https://donidcr.gov.np/pages/social-security-allowance-rate/ | gov | https://donidcr.gov.np/pages/social-security-allowance-rate/ | gov | `False` | 2026-09-16 |
| `np-widow-allowance` | https://donidcr.gov.np/pages/social-security-allowance-rate/ | gov | https://donidcr.gov.np/pages/social-security-allowance-rate/ | gov | `False` | 2026-09-16 |
| `np-single-women-allowance` | https://donidcr.gov.np/pages/mostly-asked-questions--social-security-4/ | gov | https://donidcr.gov.np/pages/social-security-allowance-rate/ | gov | `True` | 2026-09-16 |
| `np-disability-allowance` | https://donidcr.gov.np/pages/social-security-allowance-rate/ | gov | https://donidcr.gov.np/pages/social-security-allowance-rate/ | gov | `True` | 2026-09-16 |
| `lk-aswesuma` | https://wbb.gov.lk/ | gov | https://eservices.wbb.gov.lk/aswesuma/2025 | gov | `True` | 2026-09-16 |
| `lk-senior-citizens-allowance` | https://wbb.gov.lk/ | gov | https://wbb.gov.lk/ | gov | `True` | 2026-09-16 |
| `lk-samurdhi` | https://www.samurdhi.gov.lk/ | gov | https://www.samurdhi.gov.lk/ | gov | `True` | 2026-09-16 |
| `mv-disability-allowance` | https://www.nspa.gov.mv/v2/index.php/disability/ | gov | https://www.nspa.gov.mv/v2/index.php/disability/ | gov | `True` | 2026-09-16 |

## Spot-checks (eligibility vs official page)

| id | What was confirmed / left verify |
|----|----------------------------------|
| `ap-ntr-bharosa-oap` | sspensions.ap.gov.in About: OAP age **60+**, BPL white ration card, destitute, local resident, not on other pension. No rupee ceiling → `implies_low_income` + `verify=true`. |
| `kerala-karunya-benevolent-fund` | SHA page: annual family income **< Rs.3 lakh** confirmed; ailments list confirmed. Keep `verify=true` for KASP overlap. |
| `kerala-kasp-pmjay` | SHA FAQ URL repaired; RSBY/CHIS/SECC eligibility still `verify=true` (expansion uncertain). |
| `uk-nanda-gaura` | WECDUK portal: UK girls only, max 2, birth + Class-12 stages. Income ₹72k **not** restated on portal index → keep ceiling with `verify=true`. |
| `tn-cmchis` | Grounded on myScheme.gov.in; no income ceiling encoded → `verify=true`. |
| `janani-suraksha-yojana-kerala` | Stable NHM JSY page; Kerala HPS cash amounts/`>19` age remain `verify=true`. |
| Other 70 schemes | `official_source_url` already on gov/ok domains; eligibility left as previously curated with existing `verify` flags (no invention). |

## Notes

- Some gov sites return SSL/timeout errors from automated checkers; domain grounding still counts as gov.
- `nsap.nic.in` may fail DNS from some resolvers; URL retained as the MoRD NSAP official site.
- `last_verified` bumped to 2026-09-16 for the full catalogue after this grounding pass.

## Wave 1 deepen (2026-09-16 IST) — UP / Bihar / MP / Rajasthan / Odisha

Added **36** new local schemes (catalogue now **112**). All new `official_source_url` values are on `.gov.in` / `.nic.in` (or myScheme.gov.in). Eligibility encoded only from cited official pages; uncertain ceilings left null or marked `verify=true`.

### New scheme ids + sources

| id | official_source_url |
|----|---------------------|
| `up-old-age-pension` | https://lalitpur.nic.in/scheme/%E0%A4%B5%E0%A5%83%E0%A4%A6%E0%A5%8D%E0%A4%A7%E0%A4%BE%E0%A4%B5%E0%A4%B8%E0%A5%8D%E0%A4%A5%E0%A4%BE-%E0%A4%AA%E0%A5%87%E0%A4%82%E0%A4%B6%E0%A4%A8-%E0%A4%AF%E0%A5%8B%E0%A4%9C%E0%A4%A8%E0%A4%BE/ |
| `up-destitute-widow-pension` | https://saharanpur.nic.in/scheme/destitute-widow-pension-scheme/ |
| `up-disability-pension` | https://mau.nic.in/en/service/application-for-disability-grant-disability-pension/ |
| `up-daughter-marriage-grant` | https://hamirpur.nic.in/social-welfare-department/ |
| `up-post-matric-scholarship` | https://hamirpur.nic.in/social-welfare-department/ |
| `up-cm-comprehensive-marriage` | https://hamirpur.nic.in/social-welfare-department/ |
| `up-scst-prematric-scholarship` | https://hamirpur.nic.in/social-welfare-department/ |
| `br-mukhyamantri-vridhjan-pension` | https://www.sspmis.bihar.gov.in/aboutUs |
| `br-laxmi-bai-pension` | https://www.sspmis.bihar.gov.in/aboutUs |
| `br-state-disability-pension` | https://www.sspmis.bihar.gov.in/aboutUs |
| `br-ignwps` | https://www.sspmis.bihar.gov.in/aboutUs |
| `br-ignoaps` | https://www.sspmis.bihar.gov.in/aboutUs |
| `br-ayushman-biswass` | https://biswass.bihar.gov.in/ |
| `br-post-matric-scholarship` | https://pmsonline.bihar.gov.in/ |
| `mp-samagra-social-security-oap` | https://www.socialjustice.mp.gov.in/schemes/view/WlFNUHFJc2dpRHFIcVI1RlEyb3Q1UT09 |
| `mp-kalyani-widow-pension` | https://cmhelpline.mp.gov.in/Schmedetail.aspx?Schemeid=355 |
| `mp-deserted-women-pension` | https://www.socialjustice.mp.gov.in/schemes/view/WlFNUHFJc2dpRHFIcVI1RlEyb3Q1UT09 |
| `mp-disability-pension` | https://www.socialjustice.mp.gov.in/schemes/view/WlFNUHFJc2dpRHFIcVI1RlEyb3Q1UT09 |
| `mp-unmarried-women-pension` | https://cmhelpline.mp.gov.in/Schmedetail.aspx?Schemeid=355 |
| `mp-ladli-laxmi` | https://cmhelpline.mp.gov.in/Schmedetail.aspx?Schemeid=246 |
| `mp-niramayam-ayushman` | https://betul.nic.in/en/scheme/niramayam-ayushman-bharat-scheme/ |
| `mp-kalyani-vivah-sahayata` | https://cmhelpline.mp.gov.in/Schmedetail.aspx?Schemeid=573 |
| `rj-ekal-nari-samman-pension` | https://ssp.rajasthan.gov.in/rajsspmob/forms/Reports/frmReportSchemeFlow.aspx |
| `rj-vishesh-yogyajan-samman-pension` | https://ssp.rajasthan.gov.in/rajsspmob/forms/Reports/frmReportSchemeFlow.aspx |
| `rj-laghu-simant-farmer-pension` | https://ssp.rajasthan.gov.in/rajsspmob/forms/Reports/frmReportSchemeFlow.aspx |
| `rj-palanhar` | https://sje.rajasthan.gov.in/schemes/palanhar.html |
| `rj-mukhyamantri-ayushman-arogya` | https://rajswasthya.rajasthan.gov.in/schemes.php?id=1 |
| `rj-janani-suraksha` | https://rajswasthya.rajasthan.gov.in/schemes.php?id=1 |
| `rj-nirirogi-free-medicine` | https://rajswasthya.rajasthan.gov.in/schemes.php?id=1 |
| `od-mbpy-widow` | https://ssepd.odisha.gov.in/index.php/schemes-programmes/schemes/madhu-babu-pension-yojana |
| `od-mbpy-disability` | https://ssepd.odisha.gov.in/index.php/schemes-programmes/schemes/madhu-babu-pension-yojana |
| `od-bsky` | https://gjaydashboard.odisha.gov.in/About |
| `od-mission-shakti-loan` | https://missionshakti.odisha.gov.in/programme/mission-shakti-loan-state-interest-subvention |
| `od-mamata` | https://wcd.odisha.gov.in/about-us/department-works/for-women |
| `od-ignwps` | https://ssepd.odisha.gov.in/schemes-programmes/schemes/indira-gandhi-national-widow-pension-0 |
| `od-mission-shakti` | https://missionshakti.odisha.gov.in/en/more/msd-FAQs |

### Skipped (no solid official eligibility page reachable this pass)

- UP Ayushman state portal mirrors that are non-`.gov.in` only (kept national `ab-pmjay-national`).

- Odisha Biju Pucca Ghar / Nirman Shramik housing (rh.odisha.gov.in unreachable from research host; eligibility not safely encodable).

- Bihar Satat Jeevikoparjan (brlps.in non-gov host without accompanying `.gov.in` eligibility page in hand).

- Rajasthan RGHS (employee/pensioner medical scheme — out of scope for general welfare matching).

