#!/usr/bin/env bash
# Post-build verification pipeline.
#
# Runs the 5 monitors that need a live HTTP server serving public/:
#   a. Broken internal links       (curl against BASE_URL)
#   b. WCAG 2.2 static audit       (static — no server needed)
#   c. Content-truthiness          (static — no server needed)
#   d. Page-weight carbon budget   (static — no server needed)
#   e. Pa11y WCAG 2.2 AA           (Chromium against BASE_URL)
#
# BASE_URL defaults to http://127.0.0.1:8000 (local dev with
# `python3 -m http.server 8000 --directory public`).
set -euo pipefail

DOCS_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$DOCS_ROOT"

BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"

echo "==> Monitors (target: $BASE_URL)"
echo "  a. Broken internal links"
python3 scripts/check-links.py "$BASE_URL"

echo "  b. WCAG 2.2 static audit (Pa11y-equivalent regex)"
python3 scripts/wcag-static-audit.py

echo "  c. HTML content-truthiness against source"
python3 scripts/verify-content.py

echo "  d. Page-weight carbon budget"
python3 scripts/check-perf-budget.py

echo "  e. Pa11y WCAG 2.2 AA browser audit (sampled)"
bash scripts/pa11y-audit.sh "$BASE_URL"

echo "==> Verification complete"
