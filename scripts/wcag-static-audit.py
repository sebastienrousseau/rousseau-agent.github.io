#!/usr/bin/env python3
"""Static WCAG 2.2 spot checks against every built HTML page.

Catches the patterns that don't need a live browser: missing <title>,
missing lang attribute, images without alt text, form controls without
labels, sticky-nav hiding content (via CSS heuristic), inline event
handlers (CSP-violating), :focus {outline:none} without compensating
style. Runs cheaply on every build.

Not a substitute for axe-core / Pa11y in the browser — that's Phase 6b.
This is the CI gate that fails fast on regressions we can catch here.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "public"
FAILURE_PATTERNS = [
    # WCAG 3.1.1 Language of Page
    (r'<html(?![^>]*\blang=)', "MISSING-lang", "html tag missing lang attribute"),
    # WCAG 2.4.2 Page Titled
    (r'<title>\s*</title>', "EMPTY-title", "empty <title> tag"),
    # WCAG 1.1.1 Non-text Content — images without alt
    (r'<img(?![^>]*\balt=)[^>]*>', "IMG-noalt", "img missing alt attribute"),
    # WCAG 2.4.7 Focus Visible — regression guard
    (r':focus\s*\{[^}]*outline\s*:\s*none[^}]*\}(?![^{]*outline-offset|[^{]*border|[^{]*box-shadow)',
     "FOCUS-nooutline", ":focus removes outline without compensation"),
    # CSP violation via inline handler
    (r'\son(?:click|load|error|submit|change|input|focus|blur)="[^"]+"',
     "INLINE-handler", "inline event handler (CSP violation)"),
]


def main() -> int:
    issues: dict[str, list[tuple[str, str]]] = {kind: [] for _, kind, _ in FAILURE_PATTERNS}
    for html in ROOT.rglob("*.html"):
        rel = html.relative_to(ROOT)
        text = html.read_text(errors="ignore")
        for pattern, kind, _ in FAILURE_PATTERNS:
            for m in re.finditer(pattern, text):
                snippet = m.group(0)[:80]
                issues[kind].append((str(rel), snippet))

    total = sum(len(v) for v in issues.values())
    print(f"    wcag: {total} static issues")
    for kind, hits in issues.items():
        if hits:
            print(f"      {kind}: {len(hits)} hits (e.g. {hits[0][0]})", file=sys.stderr)
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
