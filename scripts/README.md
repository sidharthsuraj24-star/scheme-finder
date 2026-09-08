# Scripts

## Scheme freshness checklist

```bash
# Local checklist (no network)
python3 scripts/scheme_freshness_check.py

# Also HEAD/GET official_source_url values
python3 scripts/scheme_freshness_check.py --check-urls
```

Exits `0` even when URLs fail (report-only). Exit `1` only on script crash.
Does **not** edit eligibility rules.
