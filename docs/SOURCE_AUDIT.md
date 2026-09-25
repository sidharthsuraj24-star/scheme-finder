# Source audit — Scheme Finder catalogue

**Audit date:** 2026-09-17 (Asia/Calcutta / IST)
**Schemes audited:** 225

## Policy

- Prefer official government domains: `*.gov.in`, `*.nic.in`, `*.gov.bd`, `*.gov.np`, `*.gov.lk`, `*.gov.mv`, `*.gov` (US), ministry/department portals, myScheme.gov.in.
- Replace blogs, aggregators, news mirrors, and broken/fragile URLs with stable official pages.
- Eligibility age/income/gender/disability updated **only** when the official page clearly states them; otherwise `verify=true` with notes — never invent.
- Domain type: `gov` = government TLD; `ok` = non-.gov but confirmed official programme portal; `other` = needs replacement.


## United States federal starter set (2026-09-17 IST)

Added 12 federal US catalogue rows (`us-*`) with `.gov` official sources (fns.usda.gov, medicaid.gov, ssa.gov, acf.hhs.gov, hud.gov, dol.gov, medicare.gov, insurekidsnow.gov). Prefer federal framing; income ceilings left unstructured when state-variable (`verify=true`). Domain policy extended to include `*.gov` (US) alongside existing `*.gov.in` / neighbour TLDs.









## United States Wave 10 (FINAL) state deepen (2026-09-17 IST)

Added **30** state-tagged schemes for **North Dakota, Alaska, Vermont, Wyoming, West Virginia, District of Columbia** (`nationwide:false`, exact `states` names). Official sources are `.gov` only (hhs.nd.gov; health.alaska.gov; dcf.vermont.gov + dvha.vermont.gov; dfs.wyo.gov + health.wyo.gov; bfa.wv.gov + bms.wv.gov + chip.wv.gov; dhs.dc.gov + dhcf.dc.gov + doee.dc.gov). Federal `us-*` rows not duplicated. All new rows `verify=true`; no hard income ceilings encoded (FPL/SMI notes only). IDs `nd-*`/`ak-*`/`vt-*`/`wy-*`/`wv-*`/`dc-*` — no India collisions. **US deepen waves 1–10 complete** (all 50 states + DC).

| State / District | IDs | Primary .gov hosts |
| --- | --- | --- |
| North Dakota | nd-snap, nd-tanf, nd-medicaid, nd-liheap, nd-chip | hhs.nd.gov, applyforhelp.nd.gov |
| Alaska | ak-snap, ak-atap, ak-medicaid, ak-hap, ak-child-care | health.alaska.gov |
| Vermont | vt-snap, vt-reach-up, vt-medicaid, vt-fuel, vt-ccfap | dcf.vermont.gov, dvha.vermont.gov |
| Wyoming | wy-snap, wy-power, wy-medicaid, wy-chip, wy-lieap | dfs.wyo.gov, health.wyo.gov |
| West Virginia | wv-snap, wv-works, wv-medicaid, wv-lieap, wv-chip | bfa.wv.gov, bms.wv.gov, chip.wv.gov |
| District of Columbia | dc-snap, dc-tanf, dc-medicaid, dc-liheap, dc-child-care | dhs.dc.gov, dhcf.dc.gov, doee.dc.gov |

**Skipped / deferred:** inventing energy-assistance dollar caps; non-`.gov` apply portals (Alaska Connect ilinx host; mylieapwyo.org) as `official_source_url`; standalone portal-only catalogue rows.

## United States Wave 9 state deepen (2026-09-17 IST)

Added **27** state-tagged schemes for **New Hampshire, Rhode Island, Montana, Delaware, South Dakota** (`nationwide:false`, exact `states` names). Official sources are `.gov` only (dhhs.nh.gov + energy.nh.gov; dhs.ri.gov + eohhs.ri.gov; dphhs.mt.gov; dhss.delaware.gov; dss.sd.gov). Federal `us-*` rows not duplicated. All new rows `verify=true`; no hard income ceilings encoded (FPL/SMI notes only). IDs `nh-*`/`ri-*`/`mt-*`/`de-*`/`sd-*` — no India collisions.

| State | IDs | Primary .gov hosts |
| --- | --- | --- |
| New Hampshire | nh-snap, nh-fanf, nh-medicaid, nh-liheap, nh-eap | dhhs.nh.gov, energy.nh.gov |
| Rhode Island | ri-snap, ri-works, ri-medicaid, ri-rite-care, ri-liheap, ri-child-care | dhs.ri.gov, eohhs.ri.gov |
| Montana | mt-snap, mt-tanf, mt-medicaid, mt-hmk, mt-liheap | dphhs.mt.gov |
| Delaware | de-snap, de-tanf, de-medicaid, de-chip, de-liheap | dhss.delaware.gov |
| South Dakota | sd-snap, sd-tanf, sd-medicaid, sd-chip, sd-lieap, sd-child-care | dss.sd.gov |

**Skipped / deferred:** inventing energy-assistance dollar caps; standalone portal-only catalogue rows; non-`.gov` CAA apply microsites as `official_source_url`.

## United States Wave 8 state deepen (2026-09-17 IST)

Added **25** state-tagged schemes for **New Mexico, Nebraska, Idaho, Hawaii, Maine** (`nationwide:false`, exact `states` names). Official sources are `.gov` only (hca.nm.gov + yes.nm.gov apply; dhhs.ne.gov + iserve.nebraska.gov; healthandwelfare.idaho.gov + idalink.idaho.gov; humanservices.hawaii.gov + medquest.hawaii.gov + pais-benefits.dhs.hawaii.gov; maine.gov/dhhs/ofi + maine.gov/energy for HEAP). Federal `us-*` rows not duplicated. All new rows `verify=true`; no hard income ceilings encoded (FPL notes only). IDs `nm-*`/`ne-*`/`id-*`/`hi-*`/`me-*` — no India collisions.

| State | IDs | Primary .gov hosts |
| --- | --- | --- |
| New Mexico | nm-snap, nm-tanf, nm-medicaid, nm-liheap, nm-general-assistance | hca.nm.gov |
| Nebraska | ne-snap, ne-adc, ne-medicaid, ne-liheap, ne-child-care | dhhs.ne.gov |
| Idaho | id-snap, id-tafi, id-medicaid, id-chip, id-liheap | healthandwelfare.idaho.gov |
| Hawaii | hi-snap, hi-tanf, hi-medquest, hi-hheap, hi-child-care | humanservices.hawaii.gov, medquest.hawaii.gov |
| Maine | me-snap, me-tanf, me-mainecare, me-heap, me-child-care | maine.gov |

**Skipped / deferred:** `nmececd.org` and `mainehousing.org` as `official_source_url` (not `.gov`); inventing energy-assistance dollar caps; standalone portal-only catalogue rows; separate Centennial Care row (superseded by Turquoise Care).

## United States Wave 7 state deepen (2026-09-17 IST)

Added **25** state-tagged schemes for **Iowa, Nevada, Arkansas, Mississippi, Kansas** (`nationwide:false`, exact `states` names). Official sources are `.gov` only (hhs.iowa.gov + hhsservices.iowa.gov apply; dss.nv.gov Access Nevada / SNAP/TANF/Medical/Check Up/EAP; humanservices.arkansas.gov + access.arkansas.gov + codeofarrules.arkansas.gov LIHEAP Part; mdhs.ms.gov + medicaid.ms.gov; dcf.ks.gov + cssp.kees.ks.gov KanCare Medical portal). Federal `us-*` rows not duplicated. All new rows `verify=true`; no hard income ceilings encoded (FPL/%SMI notes only). Arkansas IDs `us-ar-*` to avoid India Arunachal `ar-*`.

| State | ids | official_source_url hosts |
| --- | --- | --- |
| Iowa | ia-snap, ia-fip, ia-medicaid, ia-hawki, ia-liheap | hhs.iowa.gov |
| Nevada | nv-snap, nv-tanf, nv-medicaid, nv-check-up, nv-eap | dss.nv.gov |
| Arkansas | us-ar-snap, us-ar-tea, us-ar-medicaid, us-ar-arkids, us-ar-liheap | humanservices.arkansas.gov, codeofarrules.arkansas.gov |
| Mississippi | ms-snap, ms-tanf, ms-medicaid, ms-chip, ms-liheap | mdhs.ms.gov, medicaid.ms.gov |
| Kansas | ks-snap, ks-tanf, ks-kancare, ks-child-care, ks-lieap | dcf.ks.gov |

**Skipped / deferred:** `adeq.state.ar.us` LIHEAP as `official_source_url` (not `.gov`); inventing energy-assistance dollar caps; bare `ar-*` for Arkansas; standalone portal-only catalogue rows.

## United States Wave 6 state deepen (2026-09-17 IST)

Added **25** state-tagged schemes for **Kentucky, Oregon, Oklahoma, Connecticut, Utah** (`nationwide:false`, exact `states` names). Official sources are `.gov` only (chfs.ky.gov + kynect.ky.gov apply; oregon.gov ODHS/OHA/OHCS + one.oregon.gov apply; oklahoma.gov OKDHS/OHCA + OKDHSLive apply; portal.ct.gov DSS/OEC + connect.ct.gov apply; jobs.utah.gov / medicaid.utah.gov / chip.utah.gov + myCase apply). Federal `us-*` rows not duplicated. All new rows `verify=true`; no hard income ceilings encoded (FPL/%SMI notes only).

| State | ids | official_source_url hosts |
| --- | --- | --- |
| Kentucky | ky-snap, ky-ktap, ky-medicaid, ky-kchip, ky-liheap | chfs.ky.gov |
| Oregon | or-snap, or-tanf, or-ohp, or-liheap, or-oeap | oregon.gov |
| Oklahoma | ok-snap, ok-tanf, ok-soonercare, ok-liheap, ok-child-care-subsidy | oklahoma.gov |
| Connecticut | ct-snap, ct-tfa, ct-husky, ct-ceap, ct-care-4-kids | portal.ct.gov |
| Utah | ut-snap, ut-fep, ut-medicaid, ut-chip, ut-heat | jobs.utah.gov, medicaid.utah.gov, chip.utah.gov |

**Skipped / deferred:** Standalone ConneCT portal-only catalogue row; inventing energy-assistance dollar caps; non-`.gov` aggregator mirrors as `official_source_url`; `us-ky-*` prefixes unnecessary (no India `ky-*` collision).

## United States Wave 5 state deepen (2026-09-17 IST)

Added **25** state-tagged schemes for **Colorado, Minnesota, South Carolina, Alabama, Louisiana** (`nationwide:false`, exact `states` names). Official sources are `.gov` only (cdhs/hcpf.colorado.gov + colorado.gov/peak apply; dcyf.mn.gov / mn.gov DHS & Commerce + mnbenefits.mn.gov apply; dss.sc.gov / scdhhs.gov / oeo.sc.gov + Benefits Portal / apply.scdhhs.gov; dhr.alabama.gov / medicaid.alabama.gov / alabamapublichealth.gov / adeca.alabama.gov + MyDHR; ldh.la.gov / lhc.la.gov + CAFÉ / MyMedicaid). Federal `us-*` rows not duplicated. All new rows `verify=true`; no hard income ceilings encoded (FPL/%SMI notes only).

| State | ids | official_source_url hosts |
| --- | --- | --- |
| Colorado | co-snap, co-colorado-works, co-health-first-colorado, co-chp-plus, co-leap | cdhs.colorado.gov, hcpf.colorado.gov |
| Minnesota | us-mn-snap, us-mn-mfip, us-mn-medical-assistance, us-mn-minnesotacare, us-mn-energy-assistance | dcyf.mn.gov, mn.gov (`us-mn-*` avoids India Manipur `mn-*`) |
| South Carolina | sc-snap, sc-family-independence, sc-healthy-connections, sc-partners-healthy-children, sc-liheap | dss.sc.gov, scdhhs.gov, oeo.sc.gov |
| Alabama | al-snap, al-family-assistance, al-medicaid, al-all-kids, al-liheap | dhr.alabama.gov, medicaid.alabama.gov, alabamapublichealth.gov, adeca.alabama.gov |
| Louisiana | us-la-snap, us-la-fitap, us-la-medicaid, us-la-lachip, us-la-liheap | ldh.la.gov, lhc.la.gov (`us-la-*` avoids India Ladakh `la-*`) |

**Skipped / deferred:** Standalone portal-only rows for PEAK / MNbenefits / DSS Benefits / MyDHR / CAFÉ / MyMedicaid (covered as apply pathways); inventing LEAP/LIHEAP dollar caps; non-`.gov` aggregator mirrors; bare `mn-*`/`la-*` US ids (India collision).

## United States Wave 4 state deepen (2026-09-17 IST)

Added **25** state-tagged schemes for **Tennessee, Indiana, Missouri, Maryland, Wisconsin** (`nationwide:false`, exact `states` names). Official sources are `.gov` only (tn.gov; in.gov FSSA/IHCDA + fssabenefits.in.gov apply; mydss.mo.gov / dss.mo.gov; dhs.maryland.gov / health.maryland.gov + benefits.maryland.gov apply; dhs/dcf/energyandhousing.wi.gov + access.wisconsin.gov / energybenefit.wi.gov apply). Federal `us-*` rows not duplicated. All new rows `verify=true`; no hard income ceilings encoded (FPL/%SMI notes only).

| State | ids | official_source_url hosts |
| --- | --- | --- |
| Tennessee | us-tn-snap, us-tn-families-first, us-tn-tenncare, us-tn-coverkids, us-tn-liheap | tn.gov (`us-tn-*` avoids India Tamil Nadu `tn-*`) |
| Indiana | in-snap, in-tanf, in-medicaid, in-hoosier-healthwise, in-eap-liheap | in.gov |
| Missouri | mo-snap, mo-temporary-assistance, mo-healthnet, mo-chip, mo-liheap | mydss.mo.gov, dss.mo.gov |
| Maryland | md-snap, md-tca, md-medicaid, md-mchp, md-ohep-liheap | dhs.maryland.gov, health.maryland.gov |
| Wisconsin | wi-foodshare, wi-w2, wi-badgercare, wi-medicaid, wi-wheap | dhs.wisconsin.gov, dcf.wisconsin.gov, energyandhousing.wi.gov |

**Skipped / deferred:** Standalone portal-only rows for One DHS / FSSA Benefits / myDSS / MarylandBenefits / ACCESS (covered as apply pathways); THDA.org-only LIHEAP mirrors as `official_source_url` (used tn.gov LIHEAP page instead); inventing LIHEAP dollar caps; non-`.gov` aggregator mirrors.

## United States Wave 3 state deepen (2026-09-17 IST)

Added **26** state-tagged schemes for **New Jersey, Virginia, Washington, Arizona, Massachusetts** (`nationwide:false`, exact `states` names). Official sources are `.gov` only (nj.gov; dss.virginia.gov / coverva.dmas.virginia.gov / commonhelp.virginia.gov; dshs.wa.gov / hca.wa.gov / commerce.wa.gov / dcyf.wa.gov; des.az.gov / azahcccs.gov / healthearizonaplus.gov; mass.gov). Federal `us-*` rows not duplicated. All new rows `verify=true`; no hard income ceilings encoded (FPL/%SMI notes only).

| State | ids | official_source_url hosts |
| --- | --- | --- |
| New Jersey | nj-snap, nj-workfirst-tanf, nj-workfirst-ga, nj-familycare, nj-liheap, nj-usf | nj.gov (+ mynjhelps.gov apply) |
| Virginia | va-snap, va-tanf, va-medicaid, va-famis, va-energy-assistance | dss.virginia.gov, coverva.dmas.virginia.gov (+ commonhelp.virginia.gov apply) |
| Washington | wa-basic-food, wa-tanf, wa-apple-health, wa-liheap, wa-wccc | dshs.wa.gov, hca.wa.gov, commerce.wa.gov, dcyf.wa.gov (+ washingtonconnection.org apply) |
| Arizona | az-nutrition-assistance, az-cash-assistance, az-ahcccs, az-kidscare, az-liheap | des.az.gov, azahcccs.gov (+ healthearizonaplus.gov apply) |
| Massachusetts | ma-snap, ma-tafdc, ma-eaedc, ma-masshealth, ma-heap | mass.gov |

**Skipped / deferred:** Portal-only catalogue rows for CommonHelp, Washington Connection, Health-e-Arizona Plus, and DTA Connect (covered as apply pathways on program rows); inventing LIHEAP/HEAP dollar caps; non-`.gov` aggregator mirrors.

## United States Wave 2 state deepen (2026-09-17 IST)

Added **27** state-tagged schemes for **Pennsylvania, Ohio, Georgia, North Carolina, Michigan** (`nationwide:false`, exact `states` names). Official sources are `.gov` only (pa.gov; benefits/medicaid/development.ohio.gov; gateway.ga.gov + dhs/dch/dfcs.georgia.gov; epass.nc.gov + ncdhhs.gov / medicaid.ncdhhs.gov; michigan.gov MDHHS / MI Bridges). Federal `us-*` rows not duplicated. All new rows `verify=true`; no hard income ceilings encoded (FPL/%SMI/tier notes only).

| State | ids | official_source_url hosts |
| --- | --- | --- |
| Pennsylvania | pa-snap, pa-tanf, pa-medicaid, pa-liheap, pa-chip, pa-pace | pa.gov |
| Ohio | oh-snap, oh-owf-tanf, oh-medicaid, oh-healthy-start, oh-heap | benefits.ohio.gov, medicaid.ohio.gov, development.ohio.gov |
| Georgia | ga-snap, ga-tanf, ga-medicaid, ga-peachcare, ga-liheap | dhs.georgia.gov, dch.georgia.gov, dfcs.georgia.gov (+ gateway.ga.gov apply) |
| North Carolina | nc-snap, nc-work-first, nc-medicaid, nc-health-choice, nc-lieap | ncdhhs.gov, medicaid.ncdhhs.gov (+ epass.nc.gov apply) |
| Michigan | mi-snap, mi-fip, mi-medicaid, mi-michild, mi-ser, mi-liheap-energy | michigan.gov |

**Skipped / deferred:** Separate PACENET-only row (covered under `pa-pace` notes); Georgia Pathways-only adult expansion as standalone row (noted under `ga-medicaid`); non-`.gov` aggregator mirrors; inventing LIHEAP dollar caps.

## United States Wave 1 state deepen (2026-09-17 IST)

Added **31** state-tagged schemes for **California, New York, Texas, Florida, Illinois** (`nationwide:false`, `states` matching COUNTRY_REGIONS exact names). Official sources are `.gov` only (cdss/dhcs/csd/ftb.ca.gov; otda/health/nyc.gov; hhs/tdhca.texas.gov; healthfinder/flsenate/floridahealth.gov; abe/hfs/dceo.illinois.gov). Federal `us-*` rows not duplicated or weakened. All new rows `verify=true`; income ceilings encoded only where clearly published (CalEITC TY2025 max $32,900).

**Skipped (no clear `.gov` eligibility page or not a fit):** Covered California marketplace (private plans / careful); Florida LIHEAP primary pages on floridajobs.org (not `.gov`); Illinois IDHS narrative pages on `dhs.state.il.us` used as notes only with `abe.illinois.gov` / `hfs.illinois.gov` / `dceo.illinois.gov` as official_source_url.


## Summary

- URL field replacements this pass: **12** (across **8** schemes)
- `eligibility_rules.verify=true`: **217**
- `eligibility_rules.verify=false`: **8**
- Official source domain types: gov=149

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


## Wave 2 deepen (2026-09-16 IST)

Added curated local schemes for **Andhra Pradesh, Telangana, Assam, Chhattisgarh, Jharkhand** (official `.gov.in` / `.nic.in` sources only; all `verify=true`).
New ids include NTR Bharosa category pensions + Dr NTR Vaidya Seva / Talliki Vandanam (AP); Aasara category pensions + Kalyana Lakshmi / Shaadi Mubarak + Rythu Bharosa + Aarogyasri (TG); Assam NSAP components + Atal Amrit / Ayushman Asom + Nijut Moina; CG IGNOAPS / Sukhad Sahara / SSP disability / CM Pension / disabled scholarship / landless labour; JH NSAP + Sarvajan component pensions.

Skipped (insufficient clear official eligibility or inactive/unclear): AP Amma Vodi successor variants without stable GO page; Assam Annapurna (P&RD notes rice allocation not received); CG Godhan Nyay (participation model unclear for matcher); TG KCR Nutrition without clear eligibility page in this pass; JH Savitribai Kishori portal timeout this pass.

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
| `up-old-age-pension` | https://lalitpur.nic.in/scheme/%E0%A4%B5%E0%A5%83%E0%A4%A6%E0%A5%8D%E0%A4%A7%E0%A4%BE%E0%A4%B5%E0%A4%B8%E0%A5%8D%E0%A4%A5%E0%A4%BE-%E0%A4%AA%E0%A5%87%E0%A4%82%E0%A4%B6%E0%A4%A8-%E0%A4%AF%E0%A5%8B%E0%A4%9C%E0%A4%A8%E0%A4%BE/ | gov | https://sspy-up.gov.in/ | gov | `True` | 2026-09-16 |
| `up-destitute-widow-pension` | https://saharanpur.nic.in/scheme/destitute-widow-pension-scheme/ | gov | https://sspy-up.gov.in/ | gov | `True` | 2026-09-16 |
| `up-disability-pension` | https://mau.nic.in/en/service/application-for-disability-grant-disability-pension/ | gov | https://sspy-up.gov.in/ | gov | `True` | 2026-09-16 |
| `up-daughter-marriage-grant` | https://hamirpur.nic.in/social-welfare-department/ | gov | http://shadianudan.upsdc.gov.in | gov | `True` | 2026-09-16 |
| `up-post-matric-scholarship` | https://hamirpur.nic.in/social-welfare-department/ | gov | http://scholarship.up.nic.in | gov | `True` | 2026-09-16 |
| `up-cm-comprehensive-marriage` | https://hamirpur.nic.in/social-welfare-department/ | gov | https://sspy-up.gov.in/ | gov | `True` | 2026-09-16 |
| `up-scst-prematric-scholarship` | https://hamirpur.nic.in/social-welfare-department/ | gov | http://scholarship.up.nic.in | gov | `True` | 2026-09-16 |
| `br-mukhyamantri-vridhjan-pension` | https://www.sspmis.bihar.gov.in/aboutUs | gov | https://www.sspmis.bihar.gov.in/ | gov | `True` | 2026-09-16 |
| `br-laxmi-bai-pension` | https://www.sspmis.bihar.gov.in/aboutUs | gov | https://www.sspmis.bihar.gov.in/ | gov | `True` | 2026-09-16 |
| `br-state-disability-pension` | https://www.sspmis.bihar.gov.in/aboutUs | gov | https://www.sspmis.bihar.gov.in/ | gov | `True` | 2026-09-16 |
| `br-ignwps` | https://www.sspmis.bihar.gov.in/aboutUs | gov | https://www.sspmis.bihar.gov.in/ | gov | `True` | 2026-09-16 |
| `br-ignoaps` | https://www.sspmis.bihar.gov.in/aboutUs | gov | https://www.sspmis.bihar.gov.in/ | gov | `True` | 2026-09-16 |
| `br-ayushman-biswass` | https://biswass.bihar.gov.in/ | gov | https://biswass.bihar.gov.in/ | gov | `True` | 2026-09-16 |
| `br-post-matric-scholarship` | https://pmsonline.bihar.gov.in/ | gov | https://pmsonline.bihar.gov.in/ | gov | `True` | 2026-09-16 |
| `mp-samagra-social-security-oap` | https://www.socialjustice.mp.gov.in/schemes/view/WlFNUHFJc2dpRHFIcVI1RlEyb3Q1UT09 | gov | https://socialsecurity.mp.gov.in/Home.aspx | gov | `True` | 2026-09-16 |
| `mp-kalyani-widow-pension` | https://cmhelpline.mp.gov.in/Schmedetail.aspx?Schemeid=355 | gov | https://socialsecurity.mp.gov.in/Home.aspx | gov | `True` | 2026-09-16 |
| `mp-deserted-women-pension` | https://www.socialjustice.mp.gov.in/schemes/view/WlFNUHFJc2dpRHFIcVI1RlEyb3Q1UT09 | gov | https://socialsecurity.mp.gov.in/Home.aspx | gov | `True` | 2026-09-16 |
| `mp-disability-pension` | https://www.socialjustice.mp.gov.in/schemes/view/WlFNUHFJc2dpRHFIcVI1RlEyb3Q1UT09 | gov | https://socialsecurity.mp.gov.in/Home.aspx | gov | `True` | 2026-09-16 |
| `mp-unmarried-women-pension` | https://cmhelpline.mp.gov.in/Schmedetail.aspx?Schemeid=355 | gov | https://socialsecurity.mp.gov.in/Home.aspx | gov | `True` | 2026-09-16 |
| `mp-ladli-laxmi` | https://cmhelpline.mp.gov.in/Schmedetail.aspx?Schemeid=246 | gov | https://ladlilaxmi.mp.gov.in | gov | `True` | 2026-09-16 |
| `mp-niramayam-ayushman` | https://betul.nic.in/en/scheme/niramayam-ayushman-bharat-scheme/ | gov | http://ayushmanbharat.mp.gov.in/ | gov | `True` | 2026-09-16 |
| `mp-kalyani-vivah-sahayata` | https://cmhelpline.mp.gov.in/Schmedetail.aspx?Schemeid=573 | gov | http://socialjustice.mp.gov.in | gov | `True` | 2026-09-16 |
| `rj-ekal-nari-samman-pension` | https://ssp.rajasthan.gov.in/rajsspmob/forms/Reports/frmReportSchemeFlow.aspx | gov | https://ssp.rajasthan.gov.in/ | gov | `True` | 2026-09-16 |
| `rj-vishesh-yogyajan-samman-pension` | https://ssp.rajasthan.gov.in/rajsspmob/forms/Reports/frmReportSchemeFlow.aspx | gov | https://ssp.rajasthan.gov.in/ | gov | `True` | 2026-09-16 |
| `rj-laghu-simant-farmer-pension` | https://ssp.rajasthan.gov.in/rajsspmob/forms/Reports/frmReportSchemeFlow.aspx | gov | https://ssp.rajasthan.gov.in/ | gov | `True` | 2026-09-16 |
| `rj-palanhar` | https://sje.rajasthan.gov.in/schemes/palanhar.html | gov | https://sje.rajasthan.gov.in/schemes/palanhar.html | gov | `True` | 2026-09-16 |
| `rj-mukhyamantri-ayushman-arogya` | https://rajswasthya.rajasthan.gov.in/schemes.php?id=1 | gov | https://maayojana.rajasthan.gov.in/ | gov | `True` | 2026-09-16 |
| `rj-janani-suraksha` | https://rajswasthya.rajasthan.gov.in/schemes.php?id=1 | gov | https://rajswasthya.rajasthan.gov.in/schemes.php?id=1 | gov | `True` | 2026-09-16 |
| `rj-nirirogi-free-medicine` | https://rajswasthya.rajasthan.gov.in/schemes.php?id=1 | gov | https://rajswasthya.rajasthan.gov.in/schemes.php?id=1 | gov | `True` | 2026-09-16 |
| `od-mbpy-widow` | https://ssepd.odisha.gov.in/index.php/schemes-programmes/schemes/madhu-babu-pension-yojana | gov | https://www.myscheme.gov.in/schemes/mbypvy | gov | `True` | 2026-09-16 |
| `od-mbpy-disability` | https://ssepd.odisha.gov.in/index.php/schemes-programmes/schemes/madhu-babu-pension-yojana | gov | https://www.myscheme.gov.in/schemes/mbypvy | gov | `True` | 2026-09-16 |
| `od-bsky` | https://gjaydashboard.odisha.gov.in/About | gov | https://gjaydashboard.odisha.gov.in/About | gov | `True` | 2026-09-16 |
| `od-mission-shakti-loan` | https://missionshakti.odisha.gov.in/programme/mission-shakti-loan-state-interest-subvention | gov | https://missionshakti.odisha.gov.in/programme/mission-shakti-loan-state-interest-subvention | gov | `True` | 2026-09-16 |
| `od-mamata` | https://wcd.odisha.gov.in/about-us/department-works/for-women | gov | https://emamata.odisha.gov.in/ | gov | `True` | 2026-09-16 |
| `od-ignwps` | https://ssepd.odisha.gov.in/schemes-programmes/schemes/indira-gandhi-national-widow-pension-0 | gov | https://ssepd.odisha.gov.in/schemes-programmes/schemes/indira-gandhi-national-widow-pension-0 | gov | `True` | 2026-09-16 |
| `od-mission-shakti` | https://missionshakti.odisha.gov.in/en/more/msd-FAQs | gov | https://missionshakti.odisha.gov.in/ | gov | `True` | 2026-09-16 |
| `ap-ntr-bharosa-widow` | https://sspensions.ap.gov.in/ssp/home/about | gov | https://sspensions.ap.gov.in/SSP/Home | gov | `True` | 2026-09-16 |
| `ap-ntr-bharosa-disability` | https://sspensions.ap.gov.in/ssp/home/about | gov | https://sspensions.ap.gov.in/SSP/Home | gov | `True` | 2026-09-16 |
| `ap-ntr-bharosa-single-women` | https://sspensions.ap.gov.in/ssp/home/about | gov | https://sspensions.ap.gov.in/SSP/Home | gov | `True` | 2026-09-16 |
| `ap-ntr-bharosa-weavers` | https://sspensions.ap.gov.in/ssp/home/about | gov | https://sspensions.ap.gov.in/SSP/Home | gov | `True` | 2026-09-16 |
| `ap-ntr-bharosa-fishermen` | https://sspensions.ap.gov.in/ssp/home/about | gov | https://sspensions.ap.gov.in/SSP/Home | gov | `True` | 2026-09-16 |
| `ap-ntr-bharosa-transgender` | https://sspensions.ap.gov.in/ssp/home/about | gov | https://sspensions.ap.gov.in/SSP/Home | gov | `True` | 2026-09-16 |
| `ap-ntr-vaidya-seva` | https://hmfw.ap.gov.in/ntr-aarogyaseva-org.aspx | gov | https://hmfw.ap.gov.in/ntr-aarogyaseva-org.aspx | gov | `True` | 2026-09-16 |
| `ap-talliki-vandanam` | https://tirupati.ap.gov.in/intermediate-education/ | gov | https://tirupati.ap.gov.in/intermediate-education/ | gov | `True` | 2026-09-16 |
| `tg-aasara-widow` | https://hyderabad.telangana.gov.in/scheme/aasara-pensions/ | gov | https://hyderabad.telangana.gov.in/scheme/aasara-pensions/ | gov | `True` | 2026-09-16 |
| `tg-aasara-disability` | https://hyderabad.telangana.gov.in/scheme/aasara-pensions/ | gov | https://hyderabad.telangana.gov.in/scheme/aasara-pensions/ | gov | `True` | 2026-09-16 |
| `tg-aasara-weavers` | https://hyderabad.telangana.gov.in/scheme/aasara-pensions/ | gov | https://hyderabad.telangana.gov.in/scheme/aasara-pensions/ | gov | `True` | 2026-09-16 |
| `tg-kalyana-lakshmi` | https://yadadri.telangana.gov.in/scheme/kalyana-lakshmi-shaadi-mubarak/ | gov | https://telanganaepass.cgg.gov.in/KalyanLakshmi.do | gov | `True` | 2026-09-16 |
| `tg-shaadi-mubarak` | https://yadadri.telangana.gov.in/scheme/kalyana-lakshmi-shaadi-mubarak/ | gov | https://telanganaepass.cgg.gov.in/KalyanaLakshmiLinks.jsp | gov | `True` | 2026-09-16 |
| `tg-rythu-bharosa` | https://wanaparthy.telangana.gov.in/scheme/rythu-bharosa-scheme/ | gov | https://rythubharosa.telangana.gov.in/ | gov | `True` | 2026-09-16 |
| `tg-aarogyasri` | https://aarogyasri.telangana.gov.in/ | gov | https://aarogyasri.telangana.gov.in/ | gov | `True` | 2026-09-16 |
| `as-ignoaps` | https://pnrd.assam.gov.in/schemes/national-social-assistance-programme-0 | gov | https://pnrd.assam.gov.in/schemes/national-social-assistance-programme-0 | gov | `True` | 2026-09-16 |
| `as-ignwps` | https://pnrd.assam.gov.in/how-to/apply-for-widow-pension-0 | gov | https://pnrd.assam.gov.in/how-to/apply-for-widow-pension-0 | gov | `True` | 2026-09-16 |
| `as-igndps` | https://pnrd.assam.gov.in/how-to/apply-for-disability-pension-0 | gov | https://pnrd.assam.gov.in/how-to/apply-for-disability-pension-0 | gov | `True` | 2026-09-16 |
| `as-nfbs` | https://pnrd.assam.gov.in/schemes/national-social-assistance-programme-0 | gov | https://pnrd.assam.gov.in/schemes/national-social-assistance-programme-0 | gov | `True` | 2026-09-16 |
| `as-atal-amrit-abhiyan` | https://hfw.assam.gov.in/schemes/detail/atal-amrit-abhiyan | gov | https://hfw.assam.gov.in/schemes/detail/atal-amrit-abhiyan | gov | `True` | 2026-09-16 |
| `as-ayushman-asom-mmjay` | https://atalamritabhiyan.assam.gov.in/schemes/atal-amrit-abhiyan-scheme | gov | https://atalamritabhiyan.assam.gov.in/schemes/atal-amrit-abhiyan-scheme | gov | `True` | 2026-09-16 |
| `as-nijut-moina` | https://directorateofhighereducation.assam.gov.in/documents-detail/final-guideline-for-nijut-moina-scheme-2024-25 | gov | https://directorateofhighereducation.assam.gov.in/documents-detail/final-guideline-for-nijut-moina-scheme-2024-25 | gov | `True` | 2026-09-16 |
| `cg-ignoaps` | https://jashpur.nic.in/en/scheme/indira-gandhi-national-old-age-pension-scheme/ | gov | https://jashpur.nic.in/en/scheme/indira-gandhi-national-old-age-pension-scheme/ | gov | `True` | 2026-09-16 |
| `cg-sukhad-sahara` | https://jashpur.nic.in/en/scheme/pleasant-support-scheme/ | gov | https://jashpur.nic.in/en/scheme/pleasant-support-scheme/ | gov | `True` | 2026-09-16 |
| `cg-ssp-disability` | https://jashpur.nic.in/en/scheme/social-security-pension-scheme/ | gov | https://jashpur.nic.in/en/scheme/social-security-pension-scheme/ | gov | `True` | 2026-09-16 |
| `cg-cm-pension-old-age` | https://korea.gov.in/en/scheme/cm-pension-yojna/ | gov | https://korea.gov.in/en/scheme/cm-pension-yojna/ | gov | `True` | 2026-09-16 |
| `cg-cm-pension-widow` | https://korea.gov.in/en/scheme/cm-pension-yojna/ | gov | https://korea.gov.in/en/scheme/cm-pension-yojna/ | gov | `True` | 2026-09-16 |
| `cg-disabled-scholarship` | https://jashpur.nic.in/en/scheme/disabled-scholarship-scheme/ | gov | https://jashpur.nic.in/en/scheme/disabled-scholarship-scheme/ | gov | `True` | 2026-09-16 |
| `cg-rg-landless-labour` | https://manendragarh-chirmiri-bharatpur.cg.gov.in/en/scheme/rajiv-gandhi-gramin-bhumiheen-kisan-majdoor-nyan-yojna/ | gov | https://manendragarh-chirmiri-bharatpur.cg.gov.in/en/scheme/rajiv-gandhi-gramin-bhumiheen-kisan-majdoor-nyan-yojna/ | gov | `True` | 2026-09-16 |
| `jh-ignoaps` | https://jamshedpur.nic.in/social-security-cell/ | gov | https://jharsewa.jharkhand.gov.in/ | gov | `True` | 2026-09-16 |
| `jh-ignwps` | https://jamshedpur.nic.in/social-security-cell/ | gov | https://jharsewa.jharkhand.gov.in/ | gov | `True` | 2026-09-16 |
| `jh-igndps` | https://jamshedpur.nic.in/social-security-cell/ | gov | https://jharsewa.jharkhand.gov.in/ | gov | `True` | 2026-09-16 |
| `jh-nfbs` | https://jamshedpur.nic.in/social-security-cell/ | gov | https://jharsewa.jharkhand.gov.in/ | gov | `True` | 2026-09-16 |
| `jh-mmsoaps` | https://jamshedpur.nic.in/social-security-cell/ | gov | https://jharsewa.jharkhand.gov.in/ | gov | `True` | 2026-09-16 |
| `jh-mmrnspy` | https://jamshedpur.nic.in/social-security-cell/ | gov | https://jharsewa.jharkhand.gov.in/ | gov | `True` | 2026-09-16 |
| `jh-svnspy` | https://jamshedpur.nic.in/social-security-cell/ | gov | https://jharsewa.jharkhand.gov.in/ | gov | `True` | 2026-09-16 |
| `jh-sarvajan-pension` | https://seraikela.nic.in/scheme/sarv-jan-pension-yojna/ | gov | https://jharsewa.jharkhand.gov.in/ | gov | `True` | 2026-09-16 |

## Wave 3 source audit (2026-09-16)

| id | official_source_url | domain | apply_url | apply domain | verify | verified |
| --- | --- | --- | --- | --- | --- | --- |
| `tn-magalir-urimai-thogai` | https://kmut.tn.gov.in/ | gov | https://kmut.tn.gov.in/ | gov | `True` | 2026-09-16 |
| `tn-ignoaps` | https://kanniyakumari.nic.in/social-security-schemes/ | nic | https://oap.tn.gov.in/ | gov | `True` | 2026-09-16 |
| `tn-ignwps` | https://kanniyakumari.nic.in/social-security-schemes/ | nic | https://oap.tn.gov.in/ | gov | `True` | 2026-09-16 |
| `tn-destitute-widow-pension` | https://kanniyakumari.nic.in/social-security-schemes/ | nic | https://oap.tn.gov.in/ | gov | `True` | 2026-09-16 |
| `tn-destitute-disabled-pension` | https://kanniyakumari.nic.in/social-security-schemes/ | nic | https://oap.tn.gov.in/ | gov | `True` | 2026-09-16 |
| `tn-deserted-wives-pension` | https://kanniyakumari.nic.in/social-security-schemes/ | nic | https://oap.tn.gov.in/ | gov | `True` | 2026-09-16 |
| `tn-unmarried-women-pension` | https://kanniyakumari.nic.in/social-security-schemes/ | nic | https://oap.tn.gov.in/ | gov | `True` | 2026-09-16 |
| `tn-igndps` | https://kanniyakumari.nic.in/social-security-schemes/ | nic | https://oap.tn.gov.in/ | gov | `True` | 2026-09-16 |
| `tn-cmupt-oap` | https://kanniyakumari.nic.in/social-security-schemes/ | nic | https://oap.tn.gov.in/ | gov | `True` | 2026-09-16 |
| `ka-sandhya-suraksha` | https://chitradurga.nic.in/en/scheme/ssp-en/ | nic | https://dssp.karnataka.gov.in/dssp/Beneficiary_Status.aspx | gov | `True` | 2026-09-16 |
| `ka-widow-pension` | https://chitradurga.nic.in/en/scheme/ssp-en/ | nic | https://dssp.karnataka.gov.in/dssp/Beneficiary_Status.aspx | gov | `True` | 2026-09-16 |
| `ka-disability-pension` | https://chitradurga.nic.in/en/scheme/ssp-en/ | nic | https://dssp.karnataka.gov.in/dssp/Beneficiary_Status.aspx | gov | `True` | 2026-09-16 |
| `ka-ignoaps` | https://chitradurga.nic.in/en/scheme/ssp-en/ | nic | https://dssp.karnataka.gov.in/dssp/Beneficiary_Status.aspx | gov | `True` | 2026-09-16 |
| `ka-manaswini` | https://chitradurga.nic.in/en/scheme/ssp-en/ | nic | https://dssp.karnataka.gov.in/dssp/Beneficiary_Status.aspx | gov | `True` | 2026-09-16 |
| `ka-nfbs` | https://chitradurga.nic.in/en/scheme/ssp-en/ | nic | https://dssp.karnataka.gov.in/dssp/Beneficiary_Status.aspx | gov | `True` | 2026-09-16 |
| `ka-adarsha-vivaha` | https://chitradurga.nic.in/en/scheme/ssp-en/ | nic | https://dssp.karnataka.gov.in/dssp/Beneficiary_Status.aspx | gov | `True` | 2026-09-16 |
| `mh-sanjay-gandhi-niradhar` | https://sjsa.maharashtra.gov.in/en/scheme/sanjay-gandhi-niradhar-anudan-yojana/ | gov | https://sjsa.maharashtra.gov.in/en/scheme/sanjay-gandhi-niradhar-anudan-yojana/ | gov | `True` | 2026-09-16 |
| `mh-shravanbal-pension` | https://sjsa.maharashtra.gov.in/en/scheme/shravan-bal-rajya-nivruttivetan-yojana/ | gov | https://sjsa.maharashtra.gov.in/en/scheme/shravan-bal-rajya-nivruttivetan-yojana/ | gov | `True` | 2026-09-16 |
| `mh-ignoaps` | https://sjsa.maharashtra.gov.in/en/scheme/indira-gandhi-national-old-age-pension-scheme/ | gov | https://sjsa.maharashtra.gov.in/en/scheme/indira-gandhi-national-old-age-pension-scheme/ | gov | `True` | 2026-09-16 |
| `mh-ignwps` | https://sjsa.maharashtra.gov.in/en/scheme/indira-gandhi-national-widow-pension-scheme/ | gov | https://sjsa.maharashtra.gov.in/en/scheme/indira-gandhi-national-widow-pension-scheme/ | gov | `True` | 2026-09-16 |
| `mh-igndps` | https://sjsa.maharashtra.gov.in/en/scheme/indira-gandhi-national-disability-pension-scheme/ | gov | https://sjsa.maharashtra.gov.in/en/scheme/indira-gandhi-national-disability-pension-scheme/ | gov | `True` | 2026-09-16 |
| `mh-mahadbt-scholarships` | https://mahadbt.maharashtra.gov.in/Home/Index | gov | https://mahadbt.maharashtra.gov.in/Home/Index | gov | `True` | 2026-09-16 |
| `wb-rupashree` | https://malda.gov.in/rupashree-prakalpa/ | gov | https://wbrupashree.gov.in/ | gov | `True` | 2026-09-16 |
| `wb-taposili-bandhu` | https://bankura.gov.in/scheme/taposili-bandu-jai-johar-under-jai-bangla-prakalpa/ | gov | https://jaibangla.wb.gov.in/ | gov | `True` | 2026-09-16 |
| `wb-jai-johar` | https://bankura.gov.in/scheme/taposili-bandu-jai-johar-under-jai-bangla-prakalpa/ | gov | https://jaibangla.wb.gov.in/ | gov | `True` | 2026-09-16 |
| `wb-manabik` | https://bankura.gov.in/form/manobik-form/ | gov | https://jaibangla.wb.gov.in/ | gov | `True` | 2026-09-16 |
| `wb-st-old-age-pension` | https://bankura.gov.in/scheme/st-old-age-pension/ | gov | https://bankura.gov.in/scheme/st-old-age-pension/ | gov | `True` | 2026-09-16 |
| `wb-sc-girl-meritorious-assist` | https://bankura.gov.in/scheme/additional-financial-assistance-benefit-to-sc-st-poor-meritorious-girl-students-reading-in-class-v-x/ | gov | https://bankura.gov.in/scheme/additional-financial-assistance-benefit-to-sc-st-poor-meritorious-girl-students-reading-in-class-v-x/ | gov | `True` | 2026-09-16 |
| `wb-pre-matric-obc-scholarship` | https://bankura.gov.in/scheme/pre-matric-obc-scholarship/ | gov | https://bankura.gov.in/scheme/pre-matric-obc-scholarship/ | gov | `True` | 2026-09-16 |
| `gj-niradhar-vriddha-pension` | https://sje.gujarat.gov.in/dsd/schemes/2212?lang=English | gov | https://www.digitalgujarat.gov.in/ | gov | `True` | 2026-09-16 |
| `gj-ganga-swarupa` | https://wcd.gujarat.gov.in/initiativedetails?id=231 | gov | https://wcd.gujarat.gov.in/initiativedetails?id=231 | gov | `True` | 2026-09-16 |
| `gj-sant-surdas` | https://sje.gujarat.gov.in/dsd/scheme/sant-surdash-yojana?lang=english | gov | https://esamajkalyan.gujarat.gov.in/ | gov | `True` | 2026-09-16 |
| `gj-nfbs-sankatmochan` | https://sje.gujarat.gov.in/dsd/schemes/2210?lang=English | gov | https://sje.gujarat.gov.in/dsd/schemes/2210?lang=English | gov | `True` | 2026-09-16 |
| `gj-vahli-dikri` | https://wcd.gujarat.gov.in/posts?id=328 | gov | https://wcd.gujarat.gov.in/posts?id=328 | gov | `True` | 2026-09-16 |
| `gj-divyang-marriage-assist` | https://sje.gujarat.gov.in/dsd/scheme/sant-surdash-yojana?lang=english | gov | https://esamajkalyan.gujarat.gov.in/ | gov | `True` | 2026-09-16 |
| `gj-ignoaps-vayvandana` | https://sje.gujarat.gov.in/dsd/schemes/2212?lang=English | gov | https://www.digitalgujarat.gov.in/ | gov | `True` | 2026-09-16 |

Skipped (quality / official eligibility unclear from reachable pages): TN Sri Lankan refugee pension variants (niche); MH Mukhyamantri Vayoshree (SJSA category page lacked eligibility text); WB Swasthya Sathi / Krishak Bandhu (portals 403/unreachable from curator network — not invented); KA Shakti / Anna Bhagya / Gruha Jyothi (utility guarantees — weak wizard fit); GJ Namo Shakti (no clear official eligibility page confirmed in this pass). Magalir Urimai eligibility grounded in G.O.(Ms) No.15 / KMUT portal.

## Wave 4 source audit (2026-09-16)

| id | official_source_url | domain | apply_url | apply domain | verify | verified |
| --- | --- | --- | --- | --- | --- | --- |
| `pb-disability-pension` | https://cdnbbsr.s3waas.gov.in/s3ec01512fc3c5227f637e41437c999a2d/uploads/2023/03/2023030494.pdf | gov | https://connect.punjab.gov.in/ | gov | `True` | 2026-09-16 |
| `pb-acid-attack-assistance` | https://sswcd.punjab.gov.in/en/wcd/state-schemes | gov | https://connect.punjab.gov.in/ | gov | `True` | 2026-09-16 |
| `pb-attendance-scholarship-disabled-girls` | https://sswcd.punjab.gov.in/en/wcd/state-schemes | gov | https://sswcd.punjab.gov.in/en/wcd/state-schemes | gov | `True` | 2026-09-16 |
| `pb-pwd-student-scholarship` | https://sswcd.punjab.gov.in/en/wcd/state-schemes | gov | https://connect.punjab.gov.in/ | gov | `True` | 2026-09-16 |
| `pb-ashirwad-marriage` | https://cdnbbsr.s3waas.gov.in/s3ec01512fc3c5227f637e41437c999a2d/uploads/2023/03/2023030494.pdf | gov | https://connect.punjab.gov.in/ | gov | `True` | 2026-09-16 |
| `pb-mai-bhago-vidya` | https://cdnbbsr.s3waas.gov.in/s3ec01512fc3c5227f637e41437c999a2d/uploads/2023/03/2023030494.pdf | gov | https://sswcd.punjab.gov.in/en | gov | `True` | 2026-09-16 |
| `hr-divyang-pension` | https://sewa.haryana.gov.in/haryana-divyang-pension-schemes/ | gov | https://sewa.haryana.gov.in/haryana-divyang-pension-schemes/ | gov | `True` | 2026-09-16 |
| `hr-ladli-social-security` | https://sewa.haryana.gov.in/ladli-social-security-allowance-scheme/ | gov | https://sewa.haryana.gov.in/ladli-social-security-allowance-scheme/ | gov | `True` | 2026-09-16 |
| `hr-destitute-children` | https://sewa.haryana.gov.in/financial-assistance-to-destitute-children-schemes/ | gov | https://sewa.haryana.gov.in/financial-assistance-to-destitute-children-schemes/ | gov | `True` | 2026-09-16 |
| `hr-nonschool-disabled-children` | https://sewa.haryana.gov.in/financial-assistance-to-non-school-going-disabled-children/ | gov | https://sewa.haryana.gov.in/financial-assistance-to-non-school-going-disabled-children/ | gov | `True` | 2026-09-16 |
| `hr-ddlly` | https://sewa.haryana.gov.in/deen-dayal-lado-lakshmi-yojana-ddlly/ | gov | https://sewa.haryana.gov.in/deen-dayal-lado-lakshmi-yojana-ddlly/ | gov | `True` | 2026-09-16 |
| `hr-widower-unmarried-assist` | https://socialjusticehry.gov.in/financial-assistance-to-widower-and-unmarried-persons-scheme-2023/ | gov | https://sewa.haryana.gov.in/social-security-pension-schemes/ | gov | `True` | 2026-09-16 |
| `hr-acid-attack-assist` | https://sewa.haryana.gov.in/financial-assistance-to-women-and-girls-acid-attack-victims/ | gov | https://sewa.haryana.gov.in/financial-assistance-to-women-and-girls-acid-attack-victims/ | gov | `True` | 2026-09-16 |
| `hr-cancer-stage-iii-iv` | https://sewa.haryana.gov.in/financial-assistance-for-stage-iii-iv-cancer-patients/ | gov | https://sewa.haryana.gov.in/financial-assistance-for-stage-iii-iv-cancer-patients/ | gov | `True` | 2026-09-16 |
| `hr-allowance-eunuchs` | https://sewa.haryana.gov.in/allowance-to-eunuchs/ | gov | https://sewa.haryana.gov.in/allowance-to-eunuchs/ | gov | `True` | 2026-09-16 |
| `hp-disability-relief-allowance` | http://esomsa.hp.gov.in/?q=social-security-pension | gov | https://himparivar.hp.gov.in/ekalyan | gov | `True` | 2026-09-16 |
| `hp-ignoaps` | http://esomsa.hp.gov.in/?q=social-security-pension | gov | https://himparivar.hp.gov.in/ekalyan | gov | `True` | 2026-09-16 |
| `hp-ignwps` | http://esomsa.hp.gov.in/?q=social-security-pension | gov | https://himparivar.hp.gov.in/ekalyan | gov | `True` | 2026-09-16 |
| `hp-igndps` | http://esomsa.hp.gov.in/?q=social-security-pension | gov | https://himparivar.hp.gov.in/ekalyan | gov | `True` | 2026-09-16 |
| `hp-transgender-pension` | http://esomsa.hp.gov.in/?q=social-security-pension | gov | https://himparivar.hp.gov.in/ekalyan | gov | `True` | 2026-09-16 |
| `hp-leprosy-rehab-allowance` | http://esomsa.hp.gov.in/?q=social-security-pension | gov | https://himparivar.hp.gov.in/ekalyan | gov | `True` | 2026-09-16 |
| `hp-intercaste-marriage` | https://hpshimla.nic.in/dwo-shimla/ | nic | http://esomsa.hp.gov.in/ | gov | `True` | 2026-09-16 |
| `hp-house-subsidy-sc-obc` | https://hpshimla.nic.in/dwo-shimla/ | nic | https://hpshimla.nic.in/dwo-shimla/ | nic | `True` | 2026-09-16 |
| `uk-widow-pension` | https://socialwelfare.uk.gov.in/service/widow-pension/ | gov | https://ssp.uk.gov.in/ | gov | `True` | 2026-09-16 |
| `uk-disability-pension` | https://socialwelfare.uk.gov.in/service/%e0%a4%a6%e0%a4%bf%e0%a4%b5%e0%a5%8d%e0%a4%af%e0%a4%be%e0%a4%82%e0%a4%97-%e0%a4%aa%e0%a5%87%e0%a4%82%e0%a4%b6%e0%a4%a8/ | gov | https://ssp.uk.gov.in/ | gov | `True` | 2026-09-16 |
| `uk-parityakta-pension` | https://socialwelfare.uk.gov.in/service/destitute-pension/ | gov | https://ssp.uk.gov.in/ | gov | `True` | 2026-09-16 |
| `uk-kisan-pension` | https://socialwelfare.uk.gov.in/hi/service/%e0%a4%95%e0%a4%bf%e0%a4%b8%e0%a4%be%e0%a4%a8-%e0%a4%aa%e0%a5%87%e0%a4%82%e0%a4%b6%e0%a4%a8/ | gov | https://ssp.uk.gov.in/ | gov | `True` | 2026-09-16 |
| `uk-bauna-pension` | https://socialwelfare.uk.gov.in/service/bauna-pension/ | gov | https://ssp.uk.gov.in/ | gov | `True` | 2026-09-16 |
| `uk-teelu-rauteli-pension` | https://socialwelfare.uk.gov.in/service/teelurautelipension/ | gov | https://ssp.uk.gov.in/ | gov | `True` | 2026-09-16 |
| `uk-divyang-bharan-poshan` | https://socialwelfare.uk.gov.in/service/divyang-bharan-poshan-anudaan/ | gov | https://ssp.uk.gov.in/ | gov | `True` | 2026-09-16 |
| `uk-marriage-grant` | https://socialwelfare.uk.gov.in/service/marriage-grant-scheme/ | gov | https://ssp.uk.gov.in/OnlineRegistration/FrmShaadiOnlineApplicationForm.aspx | gov | `True` | 2026-09-16 |
| `ga-dsss-senior` | https://scpwd.goa.gov.in/statesectorschemes/ | gov | https://socialwelfare.goa.gov.in/dayanand-social-security-scheme-dsss/ | gov | `True` | 2026-09-16 |
| `ga-dsss-disability` | https://scpwd.goa.gov.in/statesectorschemes/ | gov | https://socialwelfare.goa.gov.in/dayanand-social-security-scheme-dsss/ | gov | `True` | 2026-09-16 |
| `ga-dsss-single-widow` | https://scpwd.goa.gov.in/statesectorschemes/ | gov | https://socialwelfare.goa.gov.in/dayanand-social-security-scheme-dsss/ | gov | `True` | 2026-09-16 |
| `ga-stipend-disabled-students` | https://scpwd.goa.gov.in/statesectorschemes/ | gov | https://cmscholarship.goa.gov.in/ | gov | `True` | 2026-09-16 |
| `ga-scholarship-differently-abled` | https://scpwd.goa.gov.in/statesectorschemes/ | gov | https://cmscholarship.goa.gov.in/ | gov | `True` | 2026-09-16 |
| `ga-bachpan` | https://scpwd.goa.gov.in/statesectorschemes/ | gov | https://scpwd.goa.gov.in/statesectorschemes/ | gov | `True` | 2026-09-16 |
| `ga-marriage-award-disabled` | https://scpwd.goa.gov.in/statesectorschemes/ | gov | https://scpwd.goa.gov.in/statesectorschemes/ | gov | `True` | 2026-09-16 |
| `ga-severe-disability-fa` | https://scpwd.goa.gov.in/statesectorschemes/ | gov | https://scpwd.goa.gov.in/statesectorschemes/ | gov | `True` | 2026-09-16 |
| `ga-traditional-occupation-assist` | https://scpwd.goa.gov.in/statesectorschemes/ | gov | https://scpwd.goa.gov.in/statesectorschemes/ | gov | `True` | 2026-09-16 |

Skipped (quality / official eligibility unclear from reachable pages this pass): Punjab Bebe Nanki Laadli Beti Kalyan (india.gov.in 404; SSWCD portal timed out from curator network — income ceiling not re-verified on live HTML); Punjab Mai Bhago Widows Benefit myScheme page errored; HP Indira Gandhi Pyari Behna Sukh-Samman Nidhi (notification PDF scanned/image-only — eligibility not OCR-verified); Haryana Allowance to Dwarfs / Rare Diseases / Kashmiri Migrants (kept out for focus/quality); Goa NGO institutional grants (Mamta/Braille/Jeevan Jyot — not citizen matcher fits); UK marriage-grant sub-scheme rupee ceilings only partially published on the short service card.



## Wave 5 source audit (2026-09-16)

Northeast deepen — Arunachal Pradesh, Manipur, Meghalaya, Mizoram, Nagaland, Sikkim, Tripura. Official `.gov.in` / `.nic.in` only; Tripura rates/MSSP form verified from Directorate PDF/notification (live site intermittently unreachable from curator network; URLs remain official).

| id | official_source_url | domain | apply_url | apply domain | verify | verified |
| --- | --- | --- | --- | --- | --- | --- |
| `sk-ignoaps` | https://pensionscheme.sikkim.gov.in/ | gov | https://pensionscheme.sikkim.gov.in/ | gov | `True` | 2026-09-16 |
| `sk-ignwps` | https://pensionscheme.sikkim.gov.in/ | gov | https://pensionscheme.sikkim.gov.in/ | gov | `True` | 2026-09-16 |
| `sk-igndps` | https://pensionscheme.sikkim.gov.in/ | gov | https://pensionscheme.sikkim.gov.in/ | gov | `True` | 2026-09-16 |
| `sk-nfbs` | https://pensionscheme.sikkim.gov.in/ | gov | https://pensionscheme.sikkim.gov.in/ | gov | `True` | 2026-09-16 |
| `sk-cm-disability-pension` | https://pensionscheme.sikkim.gov.in/ | gov | https://pensionscheme.sikkim.gov.in/ | gov | `True` | 2026-09-16 |
| `sk-transgender-grant` | https://pensionscheme.sikkim.gov.in/ | gov | https://pensionscheme.sikkim.gov.in/ | gov | `True` | 2026-09-16 |
| `nl-ignoaps` | https://dsw.nagaland.gov.in/about-the-national-social-assistance-programme-nsap/ | gov | https://dsw.nagaland.gov.in/about-the-national-social-assistance-programme-nsap/ | gov | `True` | 2026-09-16 |
| `nl-ignwps` | https://dsw.nagaland.gov.in/about-the-national-social-assistance-programme-nsap/ | gov | https://dsw.nagaland.gov.in/about-the-national-social-assistance-programme-nsap/ | gov | `True` | 2026-09-16 |
| `nl-igndps` | https://dsw.nagaland.gov.in/about-the-national-social-assistance-programme-nsap/ | gov | https://dsw.nagaland.gov.in/about-the-national-social-assistance-programme-nsap/ | gov | `True` | 2026-09-16 |
| `nl-nfbs` | https://dsw.nagaland.gov.in/about-the-national-social-assistance-programme-nsap/ | gov | https://dsw.nagaland.gov.in/about-the-national-social-assistance-programme-nsap/ | gov | `True` | 2026-09-16 |
| `nl-emrs` | https://dsw.nagaland.gov.in/eklvya-model-residential-school/ | gov | https://dsw.nagaland.gov.in/eklvya-model-residential-school/ | gov | `True` | 2026-09-16 |
| `nl-st-hostels` | https://dsw.nagaland.gov.in/centrally-sponsored-scheme-of-hostels-for-st-boys-and-st-girls/ | gov | https://dsw.nagaland.gov.in/centrally-sponsored-scheme-of-hostels-for-st-boys-and-st-girls/ | gov | `True` | 2026-09-16 |
| `ml-ignwps` | https://meghalaya.gov.in/schemes/content/37326 | gov | https://meghalaya.gov.in/schemes/content/37326 | gov | `True` | 2026-09-16 |
| `ml-igndps` | https://meghalaya.gov.in/schemes/content/37326 | gov | https://meghalaya.gov.in/schemes/content/37326 | gov | `True` | 2026-09-16 |
| `ml-nfbs` | https://meghalaya.gov.in/schemes/content/37326 | gov | https://meghalaya.gov.in/schemes/content/37326 | gov | `True` | 2026-09-16 |
| `ml-rehab-disabled` | https://meghalaya.gov.in/schemes/content/15649 | gov | https://meghalaya.gov.in/schemes/content/15649 | gov | `True` | 2026-09-16 |
| `ml-border-areas-scholarship` | https://meghalaya.gov.in/schemes/content/37489 | gov | https://meghalaya.gov.in/schemes/content/37489 | gov | `True` | 2026-09-16 |
| `ml-primary-upper-scholarship` | https://meghalaya.gov.in/schemes/content/37593 | gov | https://meghalaya.gov.in/schemes/content/37593 | gov | `True` | 2026-09-16 |
| `mz-ignwps` | https://socialwelfare.mizoram.gov.in/page/ignwp-scheme | gov | https://socialwelfare.mizoram.gov.in/page/ignwp-scheme | gov | `True` | 2026-09-16 |
| `mz-igndps` | https://socialwelfare.mizoram.gov.in/page/indira-gandhi-national-disability-pension-scheme-igndps | gov | https://socialwelfare.mizoram.gov.in/page/indira-gandhi-national-disability-pension-scheme-igndps | gov | `True` | 2026-09-16 |
| `mz-nfbs` | https://socialwelfare.mizoram.gov.in/page/national-benefit-scheme | gov | https://socialwelfare.mizoram.gov.in/page/national-benefit-scheme | gov | `True` | 2026-09-16 |
| `mz-state-disability-pension` | https://socialwelfare.mizoram.gov.in/page/schemes-on-disability1688554472 | gov | https://socialwelfare.mizoram.gov.in/page/schemes-on-disability1688554472 | gov | `True` | 2026-09-16 |
| `mz-handicapped-students-stipend` | https://socialwelfare.mizoram.gov.in/page/schemes-on-disability1688554472 | gov | https://socialwelfare.mizoram.gov.in/page/schemes-on-disability1688554472 | gov | `True` | 2026-09-16 |
| `mz-pwd-unemployment-stipend` | https://socialwelfare.mizoram.gov.in/page/schemes-on-disability1688554472 | gov | https://socialwelfare.mizoram.gov.in/page/schemes-on-disability1688554472 | gov | `True` | 2026-09-16 |
| `mz-economic-rehabilitation-pwd` | https://socialwelfare.mizoram.gov.in/page/economic-rehabilitation-scheme | gov | https://socialwelfare.mizoram.gov.in/page/economic-rehabilitation-scheme | gov | `True` | 2026-09-16 |
| `mn-ignoaps` | https://assembly.mn.gov.in/user/pages/files/administrative-reports/AA%20Report%20Social%20Welfare%202025-26.pdf | gov | https://socialwelfare.mn.gov.in/en/centrally-sponsored-schemes/national-social-assistance-program-nsap/ | gov | `True` | 2026-09-16 |
| `mn-ignwps` | https://assembly.mn.gov.in/user/pages/files/administrative-reports/AA%20Report%20Social%20Welfare%202025-26.pdf | gov | https://socialwelfare.mn.gov.in/downloads/ | gov | `True` | 2026-09-16 |
| `mn-igndps` | https://assembly.mn.gov.in/user/pages/files/administrative-reports/AA%20Report%20Social%20Welfare%202025-26.pdf | gov | https://socialwelfare.mn.gov.in/downloads/ | gov | `True` | 2026-09-16 |
| `mn-nfbs` | https://assembly.mn.gov.in/user/pages/files/administrative-reports/AA%20Report%20Social%20Welfare%202025-26.pdf | gov | https://socialwelfare.mn.gov.in/downloads/ | gov | `True` | 2026-09-16 |
| `mn-cmwps` | https://assembly.mn.gov.in/user/pages/files/administrative-reports/AA%20Report%20Social%20Welfare%202025-26.pdf | gov | https://socialwelfare.mn.gov.in/downloads/ | gov | `True` | 2026-09-16 |
| `mn-caregiver-allowance-pwd` | https://socialwelfare.mn.gov.in/media/filer_public/e9/40/e940dbc8-1ea2-4a91-a3b4-3871f3f2f0b0/care_giver_1.pdf | gov | https://socialwelfare.mn.gov.in/downloads/ | gov | `True` | 2026-09-16 |
| `mn-disability-pension-cmst` | https://socialwelfare.mn.gov.in/en/sctet-sckim/disabled/ | gov | https://socialwelfare.mn.gov.in/en/sctet-sckim/disabled/ | gov | `True` | 2026-09-16 |
| `mn-marriage-incentive-disabled` | https://assembly.mn.gov.in/user/pages/files/administrative-reports/AA%20Report%20Social%20Welfare%202025-26.pdf | gov | https://socialwelfare.mn.gov.in/downloads/ | gov | `True` | 2026-09-16 |
| `tr-ignoaps` | https://socialwelfare.tripura.gov.in/monthly-revised-rate-following-social-security-pension-schemes-including-nsap-state-social-pension | gov | https://socialwelfare.tripura.gov.in/application-form-mukhyamantri-samajik-sahayata-prakalpa | gov | `True` | 2026-09-16 |
| `tr-ignwps` | https://socialwelfare.tripura.gov.in/monthly-revised-rate-following-social-security-pension-schemes-including-nsap-state-social-pension | gov | https://socialwelfare.tripura.gov.in/application-form-mukhyamantri-samajik-sahayata-prakalpa | gov | `True` | 2026-09-16 |
| `tr-igndps` | https://socialwelfare.tripura.gov.in/monthly-revised-rate-following-social-security-pension-schemes-including-nsap-state-social-pension | gov | https://socialwelfare.tripura.gov.in/application-form-mukhyamantri-samajik-sahayata-prakalpa | gov | `True` | 2026-09-16 |
| `tr-widow-deserted-pension` | https://socialwelfare.tripura.gov.in/monthly-revised-rate-following-social-security-pension-schemes-including-nsap-state-social-pension | gov | https://socialwelfare.tripura.gov.in/application-form-mukhyamantri-samajik-sahayata-prakalpa | gov | `True` | 2026-09-16 |
| `tr-unmarried-women-pension` | https://socialwelfare.tripura.gov.in/monthly-revised-rate-following-social-security-pension-schemes-including-nsap-state-social-pension | gov | https://socialwelfare.tripura.gov.in/application-form-mukhyamantri-samajik-sahayata-prakalpa | gov | `True` | 2026-09-16 |
| `tr-disability-60-allowance` | https://socialwelfare.tripura.gov.in/monthly-revised-rate-following-social-security-pension-schemes-including-nsap-state-social-pension | gov | https://socialwelfare.tripura.gov.in/application-form-mukhyamantri-samajik-sahayata-prakalpa | gov | `True` | 2026-09-16 |
| `tr-blind-handicap-pension` | https://socialwelfare.tripura.gov.in/monthly-revised-rate-following-social-security-pension-schemes-including-nsap-state-social-pension | gov | https://socialwelfare.tripura.gov.in/application-form-mukhyamantri-samajik-sahayata-prakalpa | gov | `True` | 2026-09-16 |
| `tr-state-old-age-pension` | https://socialwelfare.tripura.gov.in/monthly-revised-rate-following-social-security-pension-schemes-including-nsap-state-social-pension | gov | https://socialwelfare.tripura.gov.in/application-form-mukhyamantri-samajik-sahayata-prakalpa | gov | `True` | 2026-09-16 |
| `ar-old-age-pension-cmseva` | https://cmeseva.arunachal.gov.in/all_services.php?category=Social+Welfare | gov | https://cmeseva.arunachal.gov.in/all_services.php?category=Social+Welfare | gov | `True` | 2026-09-16 |
| `ar-widow-pension-cmseva` | https://cmeseva.arunachal.gov.in/all_services.php?category=Social+Welfare | gov | https://cmeseva.arunachal.gov.in/all_services.php?category=Social+Welfare | gov | `True` | 2026-09-16 |
| `ar-bpl-certificate-cmseva` | https://cmeseva.arunachal.gov.in/all_services.php?category=Social+Welfare | gov | https://cmeseva.arunachal.gov.in/all_services.php?category=Social+Welfare | gov | `True` | 2026-09-16 |
| `ar-scholarship-cmseva` | https://cmeseva.arunachal.gov.in/all_services.php?category=Education | gov | https://cmeseva.arunachal.gov.in/all_services.php?category=Education | gov | `True` | 2026-09-16 |

Skipped: Manipur unemployment-allowance PDF (image-heavy); Tripura many occupational social pensions (rate table only); Nagaland SOAP (DIPR list without eligibility page); Arunachal numeric NSAP rules pages not found — CM-SEVA gateways only; Mizoram live portal often 403 (content taken from official page HTML/snapshots).


## Wave 6 source audit (2026-09-16 IST)

Final India UT deepen — Delhi, Chandigarh, Jammu and Kashmir, Ladakh, Puducherry, Andaman and Nicobar Islands, Dadra and Nagar Haveli and Daman and Diu, Lakshadweep. Official `.gov.in` / `.nic.in` / ServiceOnline / India.gov / UT Help Hub only; all new rows `verify=true`. India deepen waves 1–6 marked complete in catalogue_meta (quality over forced count).

| id | official_source_url | verify |
| --- | --- | --- |
| `dl-women-distress-pension` | https://wcd.delhi.gov.in/faqs | true |
| `dl-fapsn-disability` | https://delhi.nalsa.gov.in/schemes-for-the-welfare-of-children-with-disabilities-run-by-department-of-social-welfare-gnctd/ | true |
| `dl-ladli-scheme` | https://wcd.delhi.gov.in/wcd/delhi-ladli-scheme-2008 | true |
| `dl-sugamya-sahayak` | https://delhi.nalsa.gov.in/schemes-for-the-welfare-of-children-with-disabilities-run-by-department-of-social-welfare-gnctd/ | true |
| `ch-widow-pension` | https://serviceonline.gov.in/dbt/getServiceDesc.html?serviceId=16400001 | true |
| `ch-disability-pension` | https://serviceonline.gov.in/dbt/getServiceDesc.html?serviceId=15940001 | true |
| `ch-dependent-children-widows` | https://serviceonline.gov.in/dbt/getServiceDesc.html?serviceId=14280001 | true |
| `ch-marriage-sc-widows-daughter` | https://serviceonline.gov.in/dbt/getServiceDesc.html?serviceId=15700004 | true |
| `ch-aids-disabled` | https://serviceonline.gov.in/dbt/getServiceDesc.html?serviceId=16210001 | true |
| `jk-ignoaps` | https://socialwelfarekashmir.jk.gov.in/IGNOAPS.html | true |
| `jk-ignwps` | https://socialwelfarekashmir.jk.gov.in/welfareschemes.html | true |
| `jk-igndps` | https://socialwelfarekashmir.jk.gov.in/welfareschemes.html | true |
| `jk-isss-women-distress` | https://socialwelfarekashmir.jk.gov.in/welfareschemes.html | true |
| `jk-isss-pcp` | https://socialwelfarekashmir.jk.gov.in/welfareschemes.html | true |
| `jk-motorized-tricycle` | https://jansugam.jk.gov.in/getServiceDesc.html?serviceId=19560004 | true |
| `la-ignwps` | https://helphub.ladakh.gov.in/landing/pension | true |
| `la-igndps` | https://helphub.ladakh.gov.in/landing/pension | true |
| `la-women-distress` | https://helphub.ladakh.gov.in/landing/pension | true |
| `la-pcp` | https://helphub.ladakh.gov.in/landing/pension | true |
| `la-nfbs` | https://helphub.ladakh.gov.in/landing/national-family-benefit-scheme | true |
| `py-disability-fa` | https://socwelfare.py.gov.in/grant-financial-assistance-differently-abled-person | true |
| `py-widow-remarriage-incentive` | https://wcd.py.gov.in/incentive-widow-remarriage | true |
| `py-marriage-widow-daughter` | https://wcd.py.gov.in/grant-marriage-allowances-widows-daughter-0 | true |
| `py-funeral-assistance-pensioner` | https://wcd.py.gov.in/grant-financial-assistance-funeral-expenses-old-agedestitute-pensioner | true |
| `py-widow-deserted-unmarried-pension` | https://services.india.gov.in/service/detail/pension-for-old-age-widows-deserted-women-unmarried-women-and-transgender-puducherry | true |
| `an-widow-pension` | http://andssw1.and.nic.in/socialwelfare/pdf/RTI-DSW.pdf | true |
| `an-destitute-allowance` | http://andssw1.and.nic.in/socialwelfare/pdf/RTI-DSW.pdf | true |
| `an-disability-allowance` | http://andssw1.and.nic.in/socialwelfare/pdf/RTI-DSW.pdf | true |
| `an-ignoaps` | http://andssw1.and.nic.in/socialwelfare/ | true |
| `dh-building-worker-child-education` | https://cdnbbsr.s3waas.gov.in/s371e09b16e21f7b6919bbfc43f6a5b2f0/uploads/2023/04/2023041949-2.pdf | true |
| `dh-nsp-scholarships` | https://cdnbbsr.s3waas.gov.in/s371e09b16e21f7b6919bbfc43f6a5b2f0/uploads/2023/10/202310191939831564.pdf | true |
| `ld-widow-pension` | https://lakshadweep.gov.in/departments/social-welfare-and-tribal-affairs/ | true |
| `ld-disability-pension` | https://lakshadweep.gov.in/departments/social-welfare-and-tribal-affairs/ | true |
| `ld-marriage-allowance-pwd` | https://lakshadweep.gov.in/departments/social-welfare-and-tribal-affairs/ | true |
| `ld-adip-rvy-camps` | https://lakshadweep.gov.in/departments/social-welfare-and-tribal-affairs/ | true |
| `ld-specialized-treatment-pwd` | https://lakshadweep.gov.in/departments/social-welfare-and-tribal-affairs/ | true |
| `ld-daycare-pwd-children` | https://lakshadweep.gov.in/departments/social-welfare-and-tribal-affairs/ | true |

Skipped: DNH&DD dedicated widow/disability pension eligibility pages not published with clear ceilings on ddd.gov.in this pass; J&K Marriage Assistance (18750017) and militancy pensions (eligibility incomplete); Puducherry live WCD/socwelfare HTML often connection-closed from curator network (used official URL + indexed page content / India.gov); Chandigarh numeric ceilings inferred cautiously from ServiceOnline enclosure pattern + existing OAP encoding.

## US Trump Accounts (2026-09-17)
- `us-trump-accounts` — https://www.irs.gov/trumpaccounts (also TrumpAccounts.gov / Form 4547). Federal IRA for children under 18; pilot $1,000 for eligible U.S. citizen children born 2025–2028. Not means-tested. Profile age = child beneficiary.

## US federal tax-favored savings accounts (2026-09-17)
- `us-coverdell-esa` — https://www.irs.gov/taxtopics/tc310 — Coverdell ESA; beneficiary under 18 when established (or special needs).
- `us-529-qtp` — https://www.irs.gov/taxtopics/tc313 — Federal §529 QTP / 529 plan framework (state-administered plans).
- `us-able-accounts` — https://www.irs.gov/instructions/i1099qa (+ Pub. 907 / SSA ABLE) — ABLE §529A; disability/blindness onset before age 46 for tax years beginning after Dec. 31, 2025.
- Skipped: custodial Roth/traditional IRA for minors (general IRA earned-income rules, not a distinct named benefit program); separate federal “baby bonds” (not enacted beyond Trump Accounts); closed SEED OK pilot; state baby-bond programs (CT/DC) left for a later state pass.

## United Kingdom starter pack (2026-09-25 IST)

Added **60** `gb-*` rows (UK-wide + England / Scotland / Wales / Northern Ireland). Official hosts only: gov.uk, mygov.scot (Scottish Government citizen portal used by Social Security Scotland), gov.scot, transport.gov.scot, gov.wales, nidirect.gov.uk; Healthy Start apply link = NHS BSA service linked from gov.uk. Every URL returned HTTP 200 on GET from the curator box on 2026-09-25 (mygov.scot/gov.scot need a browser User-Agent; plain scripted requests get HTTP 202 bot challenge). Conventions: `docs/COUNTRY_UK.md`.

| id | official_source_url | nations | verify |
|----|---------------------|---------|--------|
| `gb-universal-credit` | https://www.gov.uk/universal-credit | UK-wide | true |
| `gb-child-benefit` | https://www.gov.uk/child-benefit | UK-wide | true |
| `gb-tax-free-childcare` | https://www.gov.uk/tax-free-childcare | UK-wide | true |
| `gb-new-state-pension` | https://www.gov.uk/new-state-pension | UK-wide | true |
| `gb-pension-credit` | https://www.gov.uk/pension-credit | UK-wide | true |
| `gb-help-to-save` | https://www.gov.uk/get-help-savings-low-income | UK-wide | true |
| `gb-lifetime-isa` | https://www.gov.uk/lifetime-isa | UK-wide | true |
| `gb-junior-isa` | https://www.gov.uk/junior-individual-savings-accounts | UK-wide | true |
| `gb-isa-allowance` | https://www.gov.uk/individual-savings-accounts | UK-wide | true |
| `gb-marriage-allowance` | https://www.gov.uk/marriage-allowance | UK-wide | true |
| `gb-maternity-allowance` | https://www.gov.uk/maternity-allowance | UK-wide | true |
| `gb-pension-tax-relief` | https://www.gov.uk/tax-on-your-private-pension | UK-wide | true |
| `gb-personal-independence-payment` | https://www.gov.uk/pip | England, Wales, Northern Ireland | true |
| `gb-dla-children` | https://www.gov.uk/disability-living-allowance-children | England, Wales, Northern Ireland | true |
| `gb-carers-allowance` | https://www.gov.uk/carers-allowance | England, Wales, Northern Ireland | true |
| `gb-attendance-allowance` | https://www.gov.uk/attendance-allowance | England, Wales, Northern Ireland | true |
| `gb-winter-fuel-payment` | https://www.gov.uk/winter-fuel-payment | England, Wales, Northern Ireland | true |
| `gb-cold-weather-payment` | https://www.gov.uk/cold-weather-payment | England, Wales | true |
| `gb-sure-start-maternity-grant` | https://www.gov.uk/sure-start-maternity-grant | England, Wales | true |
| `gb-healthy-start` | https://www.gov.uk/healthy-start | England, Wales, Northern Ireland | true |
| `gb-warm-home-discount` | https://www.gov.uk/the-warm-home-discount-scheme | England, Wales, Scotland | true |
| `gb-disabled-facilities-grant` | https://www.gov.uk/disabled-facilities-grants | England, Wales, Northern Ireland | true |
| `gb-access-to-work` | https://www.gov.uk/access-to-work | England, Wales, Scotland | true |
| `gb-blue-badge` | https://www.gov.uk/apply-blue-badge | England, Scotland, Wales | true |
| `gb-council-tax-reduction` | https://www.gov.uk/apply-council-tax-reduction | England, Scotland, Wales | true |
| `gb-council-tax-single-person-discount` | https://www.gov.uk/council-tax | England, Wales | true |
| `gb-budgeting-loan` | https://www.gov.uk/budgeting-help-benefits | England, Scotland, Wales | true |
| `gb-sdlt-first-time-buyer-relief` | https://www.gov.uk/stamp-duty-land-tax | England, Northern Ireland | true |
| `gb-boiler-upgrade-scheme` | https://www.gov.uk/apply-boiler-upgrade-scheme | England, Wales | true |
| `gb-eng-free-childcare-working-parents` | https://www.gov.uk/free-childcare-if-working | England | true |
| `gb-eng-15-hours-3-4-year-olds` | https://www.gov.uk/help-with-childcare-costs/free-childcare-and-education-for-3-to-4-year-olds | England | true |
| `gb-eng-free-school-meals` | https://www.gov.uk/apply-free-school-meals | England | true |
| `gb-eng-shared-ownership` | https://www.gov.uk/shared-ownership-scheme | England | true |
| `gb-eng-first-homes` | https://www.gov.uk/first-homes-scheme | England | true |
| `gb-eng-right-to-buy` | https://www.gov.uk/right-to-buy-buying-your-council-home | England | true |
| `gb-eng-student-finance` | https://www.gov.uk/student-finance | England | true |
| `gb-eng-older-persons-bus-pass` | https://www.gov.uk/apply-for-elderly-person-bus-pass | England | true |
| `gb-sct-scottish-child-payment` | https://www.mygov.scot/scottish-child-payment | Scotland | true |
| `gb-sct-best-start-grant` | https://www.mygov.scot/best-start-grant-best-start-foods | Scotland | true |
| `gb-sct-best-start-foods` | https://www.mygov.scot/best-start-grant-best-start-foods | Scotland | true |
| `gb-sct-adult-disability-payment` | https://www.mygov.scot/adult-disability-payment | Scotland | true |
| `gb-sct-child-disability-payment` | https://www.mygov.scot/child-disability-payment | Scotland | true |
| `gb-sct-carer-support-payment` | https://www.mygov.scot/carer-support-payment | Scotland | true |
| `gb-sct-pension-age-disability-payment` | https://www.mygov.scot/pension-age-disability-payment | Scotland | true |
| `gb-sct-pension-age-winter-heating-payment` | https://www.mygov.scot/pension-age-winter-heating-payment | Scotland | true |
| `gb-sct-winter-heating-payment` | https://www.mygov.scot/winter-heating-payment | Scotland | true |
| `gb-sct-young-carer-grant` | https://www.mygov.scot/young-carer-grant | Scotland | true |
| `gb-sct-job-start-payment` | https://www.mygov.scot/job-start-payment | Scotland | true |
| `gb-sct-funded-elc-1140` | https://www.gov.scot/policies/early-education-and-care/early-learning-and-childcare/ | Scotland | true |
| `gb-sct-free-school-lunches-p1-p5` | https://www.mygov.scot/primary-school-meals | Scotland | true |
| `gb-sct-under-22-free-bus` | https://www.transport.gov.scot/concessionary-travel/under-22s-free-bus-travel/ | Scotland | true |
| `gb-sct-60-plus-disabled-free-bus` | https://www.transport.gov.scot/concessionary-travel/60plus-or-disabled-free-bus-travel/ | Scotland | true |
| `gb-wls-childcare-offer` | https://www.gov.wales/get-30-hours-childcare-3-and-4-year-olds/eligibility | Wales | true |
| `gb-wls-universal-primary-free-school-meals` | https://www.gov.wales/universal-primary-free-school-meals-upfsm | Wales | true |
| `gb-wls-school-essentials-grant` | https://www.gov.wales/school-essentials-grant-help-school-costs | Wales | true |
| `gb-wls-discretionary-assistance-fund` | https://www.gov.wales/discretionary-assistance-fund-daf | Wales | true |
| `gb-wls-free-prescriptions` | https://www.gov.wales/free-prescriptions | Wales | true |
| `gb-ni-education-maintenance-allowance` | https://www.nidirect.gov.uk/articles/education-maintenance-allowance-explained | Northern Ireland | true |
| `gb-ni-discretionary-support` | https://www.nidirect.gov.uk/articles/discretionary-support | Northern Ireland | true |
| `gb-ni-lone-pensioner-allowance` | https://www.nidirect.gov.uk/articles/lone-pensioner-allowance | Northern Ireland | true |

Skipped: Help to Buy Equity Loan (closed 2023); Help to Buy ISA (closed to new savers 2019); tax credits (ended April 2025); Child Trust Fund (closed); Nest Wales (eligibility unclear); NI rate relief / free school meals / Affordable Warmth and NI variants of Cold Weather Payment, Sure Start Maternity Grant, Access to Work, Blue Badge (official nidirect page not confirmed); Scottish free prescriptions and Funeral Support Payment (page not confirmed this pass).

## URL ticket fixes (2026-09-25 IST)

| scheme | old URL | new URL | evidence |
|--------|---------|---------|----------|
| `nsap-nfbs` | https://nsap.nic.in/ (NXDOMAIN) | https://nsap.dord.gov.in/ | NIC DNS → 164.100.54.176; HTTP 200 from check-host.net India nodes (Mumbai, Rajpura); geo-fenced outside India; listed as NSAP-PPS in MoRD material on s3waas.gov.in |
| `ap-ntr-bharosa-oap` | https://sspensions.ap.gov.in/SSP/Home (official_source) | https://sspensions.ap.gov.in/ssp/home/about (official_source; apply_url unchanged) | GET 200 on both; HEAD 500 → probe artefact + intermittent 5xx; mirror abdg.aptonline.in/SSP noted |
| `sk-unmarried-women-pension` | https://pensionscheme.sikkim.gov.in/ | unchanged | GET 200 (Women & Child Welfare Dept; SUWPS age 45+, Rs 2000/month listed); HEAD 404 (IIS) false positive |

## Canada starter pack (2026-09-25 IST)

Official sources only, checked 2026-09-25: canada.ca (CRA, ESDC / Service Canada) and provincial/territorial government sites. canada.ca blocks plain HTTP clients from the box, so pages were rendered in headless Chromium. Figures are July 2026 – June 2027 (benefit year) or 2026 rates. All rows have `verify: true`. Amounts are C$ (CAD).

| scheme | official_source_url | region | max_annual_income (C$) | implies_low_income |
|--------|---------------------|--------|------------------------|--------------------|
| `can-canada-child-benefit` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/canada-child-benefit-overview.html | Federal | 318,300 | false |
| `can-child-disability-benefit` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/child-disability-benefit.html | Federal | 266,005 | false |
| `can-groceries-essentials-benefit` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/canada-groceries-essentials-benefit/who-eligible.html | Federal | 82,952 | false |
| `can-canada-workers-benefit` | https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/tax-return/completing-a-tax-return/deductions-credits-expenses/line-45300-canada-workers-benefit-cwb/who-is-eligible.html | Federal | 60,629 | false |
| `can-old-age-security` | https://www.canada.ca/en/services/benefits/publicpensions/old-age-security.html | Federal | null | false |
| `can-guaranteed-income-supplement` | https://www.canada.ca/en/services/benefits/publicpensions/old-age-security/guaranteed-income-supplement.html | Federal | 54,624 | false |
| `can-oas-allowance` | https://www.canada.ca/en/services/benefits/publicpensions/old-age-security/guaranteed-income-supplement/allowance.html | Federal | 42,144 | false |
| `can-oas-allowance-survivor` | https://www.canada.ca/en/services/benefits/publicpensions/old-age-security/guaranteed-income-supplement/allowance-survivor.html | Federal | 30,696 | false |
| `can-cpp-retirement` | https://www.canada.ca/en/services/benefits/publicpensions/cpp.html | Federal (excl. Quebec) | null | false |
| `can-cpp-disability` | https://www.canada.ca/en/services/benefits/publicpensions/cpp/cpp-disability-benefit.html | Federal (excl. Quebec) | null | false |
| `can-cpp-survivor` | https://www.canada.ca/en/services/benefits/publicpensions/cpp/cpp-survivor-pension.html | Federal (excl. Quebec) | null | false |
| `can-ei-regular` | https://www.canada.ca/en/services/benefits/ei/ei-regular-benefit.html | Federal | null | false |
| `can-ei-maternity-parental` | https://www.canada.ca/en/services/benefits/ei/ei-maternity-parental.html | Federal (excl. Quebec) | null | false |
| `can-ei-sickness` | https://www.canada.ca/en/services/benefits/ei/ei-sickness.html | Federal | null | false |
| `can-ei-caregiving` | https://www.canada.ca/en/services/benefits/ei/caregiving.html | Federal | null | false |
| `can-canada-disability-benefit` | https://www.canada.ca/en/services/benefits/disability/canada-disability-benefit.html | Federal | null | true |
| `can-disability-tax-credit` | https://www.canada.ca/en/revenue-agency/services/tax/individuals/segments/tax-credits-deductions-persons-disabilities/disability-tax-credit.html | Federal | null | false |
| `can-rdsp` | https://www.canada.ca/en/employment-social-development/programs/disability/savings/how-much.html | Federal | null | false |
| `can-resp-cesg` | https://www.canada.ca/en/services/benefits/education/education-savings/estimating-amounts.html | Federal | null | false |
| `can-canada-learning-bond` | https://www.canada.ca/en/services/benefits/education/education-savings/canada-learning-bond.html | Federal | 73,577 | false |
| `can-tfsa` | https://www.canada.ca/en/revenue-agency/services/tax/registered-plans-administrators/pspa/mp-rrsp-dpsp-tfsa-limits-ympe.html | Federal | null | false |
| `can-rrsp` | https://www.canada.ca/en/revenue-agency/services/tax/registered-plans-administrators/pspa/mp-rrsp-dpsp-tfsa-limits-ympe.html | Federal | null | false |
| `can-fhsa` | https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/first-home-savings-account/opening-your-fhsas.html | Federal | null | false |
| `can-home-buyers-plan` | https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/rrsps-related-plans/what-home-buyers-plan.html | Federal | null | false |
| `can-home-buyers-amount` | https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/tax-return/completing-a-tax-return/deductions-credits-expenses/line-31270-home-buyers-amount.html | Federal | null | false |
| `can-canada-dental-care-plan` | https://www.canada.ca/en/services/benefits/dental/dental-care-plan/qualify.html | Federal | 89,999 | false |
| `can-canada-student-grant-full-time` | https://www.canada.ca/en/services/benefits/education/student-aid/grants-loans/full-time.html | Federal (excl. Northwest Territories, Nunavut, Quebec) | 161,321 | false |
| `can-canada-student-grant-part-time` | https://www.canada.ca/en/services/benefits/education/student-aid/grants-loans/part-time.html | Federal (excl. Northwest Territories, Nunavut, Quebec) | 161,321 | false |
| `can-canada-caregiver-credit` | https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/tax-return/completing-a-tax-return/deductions-credits-expenses/canada-caregiver-amount.html | Federal | null | false |
| `can-ab-child-family-benefit` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/province-alberta.html | Alberta | 70,143 | false |
| `can-ab-seniors-benefit` | https://www.alberta.ca/alberta-seniors-benefit | Alberta | 53,800 | false |
| `can-ab-aish` | https://www.alberta.ca/aish | Alberta | null | true |
| `can-bc-family-benefit` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/province-british-columbia.html | British Columbia | 170,937 | false |
| `can-bc-renters-tax-credit` | https://www2.gov.bc.ca/gov/content/taxes/income-taxes/personal/credits/renters-tax-credit | British Columbia | 86,189 | false |
| `can-bc-seniors-supplement` | https://www2.gov.bc.ca/gov/content/family-social-supports/seniors/financial-legal-matters/income-security-programs/seniors-supplement | British Columbia | null | true |
| `can-bc-training-education-savings-grant` | https://www2.gov.bc.ca/gov/content/education-training/k-12/support/scholarships/bc-training-and-education-savings-grant | British Columbia | null | false |
| `can-mb-55-plus` | https://www.gov.mb.ca/fs/eia/55plus.html | Manitoba | null | true |
| `can-mb-rent-assist` | https://www.gov.mb.ca/fs/eia/non_rentassist_facts.html | Manitoba | 60,768 | false |
| `can-mb-child-benefit` | https://www.gov.mb.ca/fs/eia/mcb.html | Manitoba | null | true |
| `can-nb-child-tax-benefit` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/province-new-brunswick.html | New Brunswick | null | true |
| `can-nb-hst-credit` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/province-new-brunswick.html | New Brunswick | 85,000 | true |
| `can-nb-low-income-seniors-benefit` | https://www2.gnb.ca/content/gnb/en/corporate/promo/new-brunswick-low-income-seniors-benefit.html | New Brunswick | null | true |
| `can-nl-child-benefit` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/province-newfoundland-labrador.html | Newfoundland and Labrador | null | true |
| `can-nl-income-supplement` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/province-newfoundland-labrador.html | Newfoundland and Labrador | null | true |
| `can-nl-seniors-benefit` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/province-newfoundland-labrador.html | Newfoundland and Labrador | 46,549 | false |
| `can-nl-disability-benefit` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/province-newfoundland-labrador.html | Newfoundland and Labrador | 55,404 | false |
| `can-ns-child-benefit` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/province-nova-scotia.html | Nova Scotia | 34,000 | false |
| `can-ns-affordable-living-tax-credit` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/province-nova-scotia.html | Nova Scotia | 39,900 | true |
| `can-ns-poverty-reduction-credit` | https://novascotia.ca/coms/PovertyReductionCredit.html | Nova Scotia | 16,000 | false |
| `can-pe-child-benefit` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/province-prince-edward-island.html | Prince Edward Island | 80,000 | false |
| `can-pe-sales-tax-credit` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/province-prince-edward-island.html | Prince Edward Island | null | true |
| `can-sk-low-income-tax-credit` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/province-saskatchewan.html | Saskatchewan | 81,668 | false |
| `can-sk-seniors-income-plan` | https://www.saskatchewan.ca/residents/family-and-social-support/seniors-services/seniors-income-plan | Saskatchewan | null | true |
| `can-sk-said` | https://www.saskatchewan.ca/said | Saskatchewan | null | true |
| `can-nt-child-benefit` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/northwest-territories.html | Northwest Territories | 80,000 | true |
| `can-nt-senior-home-heating-subsidy` | https://www.ece.gov.nt.ca/en/services/income-security-programs/senior-home-heating-subsidy | Northwest Territories | 87,000 | false |
| `can-nu-child-benefit` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/nunavut.html | Nunavut | null | true |
| `can-on-trillium-benefit` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/province-ontario.html | Ontario | 117,971 | false |
| `can-on-child-benefit` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/province-ontario.html | Ontario | 114,861 | false |
| `can-on-seniors-dental-care` | https://www.ontario.ca/page/dental-care-seniors | Ontario | 42,290 | false |
| `can-on-odsp` | https://www.ontario.ca/page/ontario-disability-support-program | Ontario | null | true |
| `can-qc-family-allowance` | https://www.retraitequebec.gouv.qc.ca/en/benefits-amounts-key-data | Quebec | null | false |
| `can-qc-qpip` | https://www.quebec.ca/en/family-and-support-for-individuals/pregnancy-parenthood/financial-support-pregnant-women-families/quebec-parental-insurance-plan/pregnancy-childbirth/choice-plan | Quebec | null | false |
| `can-qc-solidarity-tax-credit` | https://www.revenuquebec.ca/en/citizens/tax-credits/solidarity-tax-credit/ | Quebec | null | true |
| `can-qc-qpp-retirement` | https://www.retraitequebec.gouv.qc.ca/en/benefits-amounts-key-data | Quebec | null | false |
| `can-yt-child-benefit` | https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/yukon.html | Yukon | null | true |
| `can-yt-pioneer-utility-grant` | https://yukon.ca/en/pioneer-utility-grant | Yukon | 217,470 | false |

Skipped:
- Canada Carbon Rebate: ended; the last payment was April 2025.
- GST/HST credit: renamed CGEB in July 2026 and added as CGEB.
- BC Climate Action Tax Credit: ended.
- Nunavut Senior Fuel Subsidy: gov.nu.ca returns 403, and the application form states no thresholds.
- Nova Scotia HARP: 2026–27 terms not published; applications open 1 Oct 2026.
- Ontario GAINS: verified, but deferred by the 4-per-province cap.

## Phase-out zero-points (2026-09-25 IST)

Production smoke: a C$250k Ontario family still saw the Ontario Child Benefit. Gradual phase-out benefits now carry `max_annual_income` = the official zero-point for a generous family (4 children, or the largest size tabulated). Sources checked 2026-09-25 (rendered in headless Chromium where needed):

| scheme | cap | official source |
|--------|-----|-----------------|
| `can-canada-child-benefit` | C$318,300 | CRA CCB "How much you can get" (Jul 2026–Jun 2027): C$8,157 under 6; 4+ children reduced by C$10,260 + 9.5% over C$82,847 |
| `can-child-disability-benefit` | C$266,005 | CRA CDB page + CDB guideline table effective July 2026 (3 dependants: C$0 at C$270,000) |
| `can-on-child-benefit` | C$114,861 | CRA Ontario page (C$146.66/month, C$26,865) + Ontario Taxation Act, 2007 s. 104(5) (8% reduction) |
| `can-bc-family-benefit` | C$170,937 | gov.bc.ca B.C. family benefit (minimums C$775/750/725; 4% over C$96,562 "until they are reduced to zero") |
| `can-ab-child-family-benefit` | C$70,143 | CRA Alberta page + alberta.ca (2026–27 amounts/thresholds) + Alberta Personal Income Tax Act s. 30.2 (20.11% / 8.95% rates for 4+ children) |
| `can-on-trillium-benefit` | C$117,971 | CRA 2026 OEPTC calculation sheet (senior couple: C$290 + C$581 + C$617; 2% over C$43,571), CRA 2026 NOEC family sheet (zero at C$94,356), CRA OSTC seniors' threshold Q&A (C$378/person, 4% over C$37,273) |
| `can-nb-hst-credit` | C$85,000 | CRA New Brunswick page (C$300 + C$300 + C$100/child; 2% over C$35,000) |
| `can-nt-child-benefit` | C$80,000 | CRA NWT page / T4114 ("eliminated when your adjusted family income reaches $80,000") |
| `can-ns-affordable-living-tax-credit` | C$39,900 | CRA Nova Scotia page (C$255 + C$60/child; 5% over C$30,000) |
| `gb-tax-free-childcare` | £200,000 | GOV.UK: not eligible if you or your partner expects adjusted net income over £100,000 |
| `gb-eng-free-childcare-working-parents` | £200,000 | GOV.UK: each parent's adjusted net income under £100,000 |
| `gb-wls-childcare-offer` | £200,000 | gov.wales eligibility: each parent's gross income £100,000 or less |

Reviewed, left ungated: Quebec Family Allowance (minimum C$1,221/child at any income, Retraite Québec 2026); OAS (individual recovery tax); RESP/CESG and RDSP (basic grant at all incomes); UK Child Benefit (HICBC), Marriage Allowance (tax-band test), Winter Fuel / Pension Age Winter Heating (individual £35k recovery). Left on the Canada soft gate because official pages do not publish the reduction rate: NB child tax benefit, NL child benefit, NL income supplement, Nunavut and Yukon child benefits.

## India freshness candidates (2026-09-25 IST)

| candidate | outcome | official evidence |
|-----------|---------|-------------------|
| PM-JANMAN | added `in-pm-janman` (verify) | myscheme.gov.in/schemes/pm-janman (official; geo-fenced from the box); PIB, Ministry of Tribal Affairs, 11 Feb and 12 Mar 2026 (mission 2023-24 to 2025-26; relaxed PMAY-G exclusions); Lok Sabha unstarred Q1879 and Q2031, answered 30.07.2026 (progress to 30.06.2026) |
| PM-KUSUM | deferred | pmkusum.mnre.gov.in: MNRE OM F.No.32/645/2017-SPV dated 28.03.2026 (scheme timeline ended 31.03.2026; PM KUSUM 2.0 in proposal stage; extension to 31.03.2027 only for PPAs/NTPs issued by 31.12.2025) |
| SVAMITVA | deferred | svamitva.nic.in; Lok Sabha Q2553 answered 04.08.2026 (3.30 of 3.38 lakh villages surveyed; 2.72 crore cards distributed). Delivered by village-wide survey; no individual application |
| Jal Jeevan Mission | rejected (infrastructure) | jaljeevanmission.gov.in: State and village water-supply schemes |
| PM SHRI | rejected (infrastructure) | pmshrischools.education.gov.in: upgrades to selected schools |
| PM e-Bus Sewa | rejected (infrastructure) | mohua.gov.in: city e-bus fleet and depot funding |
