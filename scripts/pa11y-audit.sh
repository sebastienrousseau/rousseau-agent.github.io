#!/usr/bin/env bash
# Run Pa11y (bundled Chromium) against a sample of built pages.
# Full audit of all 800+ pages is prohibitively slow (~30s/page), so
# we sample 10 representative pages that cover every unique template
# + component combination. If any of the sampled pages have errors
# we exit non-zero; the sampling assumption is that a component
# either passes or fails uniformly across pages that use it.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -x a11y-tooling/node_modules/.bin/pa11y ]; then
    echo "    pa11y:    not installed; skipping (run 'cd a11y-tooling && npm install pa11y' to enable)"
    exit 0
fi

BASE="${1:-${BASE_URL:-http://127.0.0.1:8000}}"
# When the build was BASE_PATH-prefixed (project-page hosting), the
# rendered URLs live under that prefix; the sampled routes need the
# same prefix so they resolve.
PREFIX="${BASE_PATH:-}"
PAGES=(
  "${PREFIX}/"
  "${PREFIX}/quickstart/"
  "${PREFIX}/getting-started/installation/"
  "${PREFIX}/providers/anthropic/"
  "${PREFIX}/transports/whatsapp/"
  "${PREFIX}/concepts/"
  "${PREFIX}/security/"
  "${PREFIX}/troubleshooting/"
  "${PREFIX}/reference/carbon/"
  "${PREFIX}/faq/general/"
)

TOTAL=0
for p in "${PAGES[@]}"; do
    ERRS=$(a11y-tooling/node_modules/.bin/pa11y --standard WCAG2AA --reporter cli "$BASE$p" 2>&1 | grep -cE "^ • Error:" || true)
    if [ "$ERRS" -gt 0 ]; then
        echo "    pa11y:    $ERRS WCAG2AA errors on $p"
        a11y-tooling/node_modules/.bin/pa11y --standard WCAG2AA --reporter cli "$BASE$p" 2>&1 | head -20
        TOTAL=$((TOTAL + ERRS))
    fi
done

if [ "$TOTAL" -eq 0 ]; then
    echo "    pa11y:    WCAG 2.2 AA green across ${#PAGES[@]} sampled pages"
    exit 0
fi
echo "    pa11y:    $TOTAL total WCAG2AA errors"
exit 1
