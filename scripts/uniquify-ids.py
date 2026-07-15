#!/usr/bin/env python3
"""Suffix duplicate id="…" attributes on every built HTML page.

The SSG's heading-id generator can emit the same id twice when two
headings share the same slug ("Verifying a signed release" appears
under Install AND under a Troubleshooting section, etc.). Pa11y flags
this as WCAG2AA F77. This pass keeps the first occurrence and
suffixes later ones with -2, -3, ….
"""
from __future__ import annotations
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "public"
ID_RE = re.compile(r'\bid="([^"]+)"')


def uniquify(html: str) -> str:
    seen: dict[str, int] = {}
    def sub(m: re.Match[str]) -> str:
        original = m.group(1)
        seen[original] = seen.get(original, 0) + 1
        if seen[original] == 1:
            return m.group(0)
        return f'id="{original}-{seen[original]}"'
    return ID_RE.sub(sub, html)


def main() -> None:
    fixed = 0
    for html_file in ROOT.rglob("*.html"):
        text = html_file.read_text(errors="ignore")
        new = uniquify(text)
        if new != text:
            html_file.write_text(new)
            fixed += 1
    print(f"    ids:      uniquified duplicate ids on {fixed} pages")


if __name__ == "__main__":
    main()
