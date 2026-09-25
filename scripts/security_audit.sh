#!/usr/bin/env bash
# Dependency + secret audit (free tooling). Exit non-zero on findings.
#
#   bash scripts/security_audit.sh            # npm audit + pip-audit (+ gitleaks if installed)
#   AUDIT_LEVEL=high bash scripts/security_audit.sh
#   SKIP_GITLEAKS=1 bash scripts/security_audit.sh
#
# - npm audit: fails at AUDIT_LEVEL (default: moderate) for frontend deps.
# - pip-audit: resolves backend/requirements.txt against the PyPI advisory DB
#   (OSV). Requires `pip install pip-audit`.
# - gitleaks: scans full git history (all refs) when the binary is on PATH or
#   GITLEAKS_BIN points at it. Build output (.next/) is never committed.
#
# Needs network access (advisory databases). Not part of the offline unit tests.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LEVEL="${AUDIT_LEVEL:-moderate}"
fail=0

echo "== npm audit (frontend, level=${LEVEL}) =="
if (cd "$ROOT/frontend" && npm audit --audit-level="$LEVEL"); then
  echo "npm audit: OK"
else
  echo "npm audit: FINDINGS at >= ${LEVEL}"
  fail=1
fi

echo
echo "== pip-audit (backend/requirements.txt) =="
PIP_AUDIT="${PIP_AUDIT_BIN:-$(command -v pip-audit || true)}"
if [[ -z "$PIP_AUDIT" ]] && python3 -m pip_audit --version >/dev/null 2>&1; then
  PIP_AUDIT="python3 -m pip_audit"
fi
if [[ -n "$PIP_AUDIT" ]]; then
  if $PIP_AUDIT -r "$ROOT/backend/requirements.txt" --progress-spinner off; then
    echo "pip-audit: OK"
  else
    echo "pip-audit: FINDINGS"
    fail=1
  fi
else
  echo "pip-audit not installed (pip install pip-audit) — FAILING so this is not silently skipped"
  fail=1
fi

echo
echo "== gitleaks (git history, all refs) =="
GL="${GITLEAKS_BIN:-$(command -v gitleaks || true)}"
if [[ "${SKIP_GITLEAKS:-0}" == "1" ]]; then
  echo "gitleaks: skipped (SKIP_GITLEAKS=1)"
elif [[ -n "$GL" ]]; then
  if "$GL" git "$ROOT" --log-opts="--all" --redact --no-banner; then
    echo "gitleaks: OK (no leaks)"
  else
    echo "gitleaks: LEAKS FOUND"
    fail=1
  fi
else
  echo "gitleaks not installed — skipped (see docs/SECURITY.md for install)"
fi

echo
if [[ $fail -ne 0 ]]; then
  echo "SECURITY AUDIT: FAIL"
else
  echo "SECURITY AUDIT: PASS"
fi
exit $fail
