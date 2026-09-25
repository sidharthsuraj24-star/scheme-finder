"""Offline dependency / security-artifact guards (Phase 2 free security pass).

The live advisory scans need network and run via scripts/security_audit.sh
(npm audit + pip-audit + gitleaks) and the parked CI workflow. These tests pin
the fixes offline so a lockfile regression is caught by plain pytest.
"""

from __future__ import annotations

import json
import os
import re
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend"


def _ver(v: str) -> tuple[int, ...]:
    return tuple(int(x) for x in re.findall(r"\d+", v)[:3])


def _lock_packages() -> dict:
    return json.loads((FRONTEND / "package-lock.json").read_text())["packages"]


def test_no_vulnerable_postcss_in_lockfile():
    # GHSA-6g55-p6wh-862q, GHSA-r28c-9q8g-f849, GHSA-qx2v-qp2m-jg93,
    # GHSA-fxqj-rqcc-2cmp: postcss <= 8.5.22 (Next 15 bundled 8.4.31).
    bad = {
        path: meta.get("version")
        for path, meta in _lock_packages().items()
        if path.endswith("node_modules/postcss") and _ver(meta.get("version", "0")) <= (8, 5, 22)
    }
    assert not bad, f"vulnerable postcss in lockfile: {bad}"


def test_next_is_patched_15x():
    next_meta = _lock_packages()["node_modules/next"]
    v = _ver(next_meta["version"])
    assert v[0] == 15 and v >= (15, 5, 26), next_meta["version"]


def test_postcss_override_present():
    pkg = json.loads((FRONTEND / "package.json").read_text())
    assert pkg.get("overrides", {}).get("next", {}).get("postcss")


def test_audit_script_and_ci_present():
    script = ROOT / "scripts" / "security_audit.sh"
    assert script.exists()
    assert os.stat(script).st_mode & stat.S_IXUSR
    text = script.read_text()
    for tool in ("npm audit", "pip-audit", "gitleaks"):
        assert tool in text
    wf = ROOT / "docs" / "workflows" / "security.yml"
    assert wf.exists()
    wf_text = wf.read_text()
    assert "security_audit.sh" in wf_text and "security-headers.spec.ts" in wf_text


def test_security_txt_uses_repo_advisory_contact():
    txt = (FRONTEND / "public" / ".well-known" / "security.txt").read_text()
    assert re.search(
        r"^Contact: https://github\.com/sidharthsuraj24-star/scheme-finder/security/advisories/new$",
        txt,
        re.M,
    )
    assert "mailto:" not in txt
    assert re.search(r"^Expires: 20\d\d-", txt, re.M)


def test_security_doc_is_honest_about_scope():
    doc = (ROOT / "docs" / "SECURITY.md").read_text().lower()
    assert "not a penetration test" in doc
    assert "soc 2" in doc
    assert "security/advisories/new" in doc
