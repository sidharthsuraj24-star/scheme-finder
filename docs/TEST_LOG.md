# Phase 4 - Test and debug log

Date: 2026-09-08 (Asia/Calcutta)

Mobile-first: large tap targets, single column, short steps, EN/ML toggle. District collected but unused in seed rules.

Backend: uvicorn :8000 with backend/.venv. Frontend: next build OK; next dev :3000.
Scheme count: 18.

## Summary

| Suite | Pass | Fail |
|-------|------|------|
| Live API profiles | 14 | 0 |
| Backend pytest | 23 | 0 |

## Cases

### 1. senior - PASS
- Summary: Senior 68M low income Ernakulam, disability false, occ other
- HTTP: 200
- Count: 4
- Matched: ["kerala-old-age-pension", "kerala-karunya-benevolent-fund", "kerala-life-mission", "kerala-kasp-pmjay"]
- Expected: ["kerala-old-age-pension"]
- First: {"id": "kerala-old-age-pension", "status": "likely_eligible"}
- Result: PASS

### 2. widow - PASS
- Summary: Widow 52F BPL not pregnant Kollam
- HTTP: 200
- Count: 3
- Matched: ["kerala-widow-pension", "kerala-karunya-benevolent-fund", "kerala-kasp-pmjay"]
- Expected: ["kerala-widow-pension"]
- First: {"id": "kerala-widow-pension", "status": "likely_eligible"}
- Result: PASS

### 3. disabled - PASS
- Summary: PwD 55% Thrissur
- HTTP: 200
- Count: 6
- Matched: ["adip-assistive-devices", "kerala-disability-pension-mental", "kerala-disability-pension-physical", "kerala-karunya-benevolent-fund", "kerala-life-mission", "kerala-kasp-pmjay"]
- Expected: ["kerala-disability-pension-physical", "adip-assistive-devices"]
- First: {"id": "adip-assistive-devices", "status": "likely_eligible"}
- Result: PASS

### 4. farmer_land - PASS
- Summary: Farmer+land Palakkad
- HTTP: 200
- Count: 4
- Matched: ["kerala-karunya-benevolent-fund", "pm-kisan", "kerala-kasp-pmjay", "kerala-life-mission"]
- Expected: ["pm-kisan"]
- First: {"id": "kerala-karunya-benevolent-fund", "status": "uncertain"}
- Result: PASS

### 5. student_sc - PASS
- Summary: SC student Kozhikode
- HTTP: 200
- Count: 3
- Matched: ["kerala-egrantz", "kerala-karunya-benevolent-fund", "kerala-kasp-pmjay"]
- Expected: ["kerala-egrantz"]
- First: {"id": "kerala-egrantz", "status": "uncertain"}
- Result: PASS

### 6. pregnant_maternity - PASS
- Summary: Pregnant SC Malappuram
- HTTP: 200
- Count: 4
- Matched: ["pmmvy", "janani-suraksha-yojana-kerala", "kerala-karunya-benevolent-fund", "kerala-kasp-pmjay"]
- Expected: ["pmmvy", "janani-suraksha-yojana-kerala"]
- First: {"id": "pmmvy", "status": "likely_eligible"}
- Result: PASS

### 7. high_income_no_match - PASS
- Summary: High-income professional
- HTTP: 200
- Count: 2
- Matched: ["kerala-kasp-pmjay", "kerala-life-mission"]
- Expected: []
- First: {"id": "kerala-kasp-pmjay", "status": "uncertain"}
- Result: PASS

### 8. agri_labour - PASS
- Summary: Agri labour Wayanad
- HTTP: 200
- Count: 5
- Matched: ["kerala-agri-labour-pension", "kerala-old-age-pension", "kerala-karunya-benevolent-fund", "kerala-life-mission", "kerala-kasp-pmjay"]
- Expected: ["kerala-agri-labour-pension"]
- First: {"id": "kerala-agri-labour-pension", "status": "likely_eligible"}
- Result: PASS

### 9. unmarried_woman_50plus - PASS
- Summary: Unmarried woman 55 Kannur
- HTTP: 200
- Count: 4
- Matched: ["kerala-unmarried-women-pension", "kerala-karunya-benevolent-fund", "kerala-life-mission", "kerala-kasp-pmjay"]
- Expected: ["kerala-unmarried-women-pension"]
- First: {"id": "kerala-unmarried-women-pension", "status": "likely_eligible"}
- Result: PASS

### 10. deserted_edge - PASS
- Summary: Deserted age45 fail / age52 pass
- HTTP: 200
- Matched: {"45": ["kerala-karunya-benevolent-fund", "kerala-life-mission", "kerala-kasp-pmjay"], "52": ["kerala-widow-pension", "kerala-karunya-benevolent-fund", "kerala-life-mission", "kerala-kasp-pmjay"]}
- Result: PASS

### 11. kerala_district_variation - PASS
- Summary: TVM vs Kasaragod identical
- HTTP: 200
- Matched: {"TVM": ["kerala-karunya-benevolent-fund", "kerala-kasp-pmjay", "kerala-life-mission", "kerala-old-age-pension"], "Kasaragod": ["kerala-karunya-benevolent-fund", "kerala-kasp-pmjay", "kerala-life-mission", "kerala-old-age-pension"]}
- Note: District collected in UI but unused in seed eligibility_rules
- Result: PASS

### 12. zero_match - PASS
- Summary: Goa child high income → 200+message
- HTTP: 200
- Count: 0
- Message: No schemes matched this profile based on published eligibility rules. Try adjusting income, occupation, category, or disability fields, or browse GET /schemes for the full catalogue. Always verify with the implementing office before applying.
- Result: PASS

### 13. lang_en_ml - PASS
- Summary: Bilingual explanations present
- HTTP: None
- EN: Likely eligible for Indira Gandhi National Old Age Pension Scheme (Kerala Sevana
- ML: ഇന്ദിരാഗാന്ധി ദേശീയ വയോജന പെൻഷൻ പദ്ധതി (സേവന) യ്ക്ക് യോഗ്യതയുണ്ടാകാം: സംസ്ഥാനം '
- Result: PASS

### 14. bereaved_nfbs - PASS
- Summary: BPL widow + breadwinner deceased
- HTTP: 200
- Matched: ["kerala-widow-pension", "kerala-karunya-benevolent-fund", "nsap-nfbs", "kerala-kasp-pmjay"]
- Result: PASS

## Bugs fixed

1. Non-maternity profiles were matching PMMVY/JSY/Matru Jyothi as likely - added maternity_required structured rule + matcher + wizard questions.
2. NFBS matched BPL without bereavement flag - added primary_breadwinner_deceased_required + matcher + wizard.
3. Uncertain results ranked above likely on score ties - sort likely first.
4. Frontend could not send maternity/bereavement - Wizard step 7 + api mapping; farmer+land adds landholding_farmer.

## Known limitations

- verify=true schemes stay uncertain.
- District unused in matcher.
- PMMVY pregnancy-order / employment exclusions not fully structured.
- NFBS deceased age band still verify_notes.
- ML copy may need native review.
- SECC/KASP and LIFE often uncertain without survey signals.

## Suggested next features

- Shareable results link
- District / LSG deep links
- More structured PMMVY rules from WCD FAQ only
- Native ML review
- PWA offline shell
