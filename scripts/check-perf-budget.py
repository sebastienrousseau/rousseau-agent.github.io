#!/usr/bin/env python3
"""Fail on pages exceeding the page-weight carbon budget.

Enforces two ceilings measured against the built HTML file (not the
transferred / gzipped size, which would be smaller):

    landing (`/index.html`)  ≤ 60 KB
    interior pages           ≤ 100 KB

If a page grows past these ceilings we've likely regressed on the
content-in-shell ratio or accidentally shipped a huge inline asset.
The gate is a build-time carbon-posture check, not a purely aesthetic
size limit.
"""
from __future__ import annotations
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "public"
LANDING_MAX = 60 * 1024
INTERIOR_MAX = 100 * 1024


def main() -> int:
    over_budget: list[tuple[str, int, int]] = []
    for html in ROOT.rglob("*.html"):
        rel = html.relative_to(ROOT)
        size = html.stat().st_size
        limit = LANDING_MAX if str(rel) == "index.html" else INTERIOR_MAX
        if size > limit:
            over_budget.append((str(rel), size, limit))

    print(
        f"    perf:     landing budget {LANDING_MAX // 1024} KB · interior budget {INTERIOR_MAX // 1024} KB · "
        f"{len(over_budget)} over"
    )
    if over_budget:
        for r, s, l in sorted(over_budget, key=lambda x: -x[1])[:10]:
            print(f"      OVER  {s // 1024:4} KB > {l // 1024:3} KB   {r}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
