#!/usr/bin/env bash
# rousseau-agent docs build pipeline. Produces a ready-to-serve `public/`.
# Idempotent — safe to re-run.
#
# Run `scripts/verify.sh` afterwards (against a running server) to gate
# on broken links + WCAG static/browser checks + carbon budget.

set -euo pipefail

DOCS_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$DOCS_ROOT"

echo "==> Cleaning public/"
rm -rf public

echo "==> Running ssg build"
ssg build -c content -o public -t templates > /tmp/rousseau-docs-build.log 2>&1
grep -E "Site built|failed" /tmp/rousseau-docs-build.log | tail -3

# --- Post-processing ---
echo "==> Stripping data-ssg-livereload injections"
find public -name "*.html" -exec perl -i -0pe 's|<script data-ssg-livereload>.*?</script>||gs' {} \;

echo "==> Fixing CSP (SSG strips unsafe-inline)"
find public -name "*.html" -exec sed -i "s|script-src 'self' ;|script-src 'self' 'unsafe-inline';|g; s|style-src 'self' ;|style-src 'self' 'unsafe-inline';|g" {} \;

echo "==> Aliasing highlight.<hash>.css -> highlight.css"
HL=$(ls public/highlight.*.css 2>/dev/null | head -1)
[ -n "$HL" ] && cp "$HL" public/highlight.css

echo "==> Copying local fonts to public/fonts/"
mkdir -p public/fonts
cp -u local-assets/fonts/* public/fonts/

echo "==> Installing service worker + manifest"
cp local-assets/sw.js public/sw.js
cp local-assets/manifest.json public/manifest.json

echo "==> Building semantic search index (BM25)"
python3 scripts/build-search-index.py

echo "==> Building Q&A pairs index for Ask-AI panel"
python3 scripts/build-qa-pairs.py

echo "==> Enriching HTML: OG cards + content provenance (SHA-256 per page)"
python3 scripts/enrich-html.py

echo "==> Injecting hreflang alternates (SSG doesn't emit them)"
python3 scripts/inject-hreflang.py

echo "==> Stripping deprecated align= (WCAG2AA H49)"
find public -name "*.html" -exec perl -i -pe 's/\s+align="[^"]*"//g' {} \;

echo "==> Uniquifying duplicate id= attributes (WCAG2AA F77)"
python3 scripts/uniquify-ids.py

echo "==> Rewriting sitemap.xml (SSG plugin produces empty)"
python3 scripts/emit-sitemap.py

echo "==> Encoding rousseau-chat.webm + captions"
bash scripts/build-video-assets.sh

echo "==> Emitting carbon.txt"
python3 scripts/emit-carbon-txt.py

echo "==> Build complete"
find public -name "index.html" | wc -l | xargs -I{} echo "  pages: {}"
du -sh public | awk '{print "  size:  "$1}'
echo
echo "Run scripts/verify.sh against a running server to gate the build."
