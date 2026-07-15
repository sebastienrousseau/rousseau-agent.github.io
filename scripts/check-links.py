#!/usr/bin/env python3
"""Fail on any broken internal link.

Walks public/, extracts every href="/…" URL, and hits it via HEAD
against a dev server. Exits non-zero if anything returns != 200.
"""
from __future__ import annotations
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "public"
SKIP_EXT = (".css", ".js", ".json", ".xml", ".txt", ".ico",
            ".png", ".jpg", ".svg", ".webp", ".woff", ".woff2", ".map")
LINK_RE = re.compile(r'href="(/[^"#?]*)"')


def main(base: str = "http://127.0.0.1:8000") -> int:
    urls: set[str] = set()
    for html in ROOT.rglob("*.html"):
        for m in LINK_RE.finditer(html.read_text(errors="ignore")):
            u = m.group(1)
            if not u.endswith(SKIP_EXT):
                urls.add(u)

    broken: list[tuple[str, str]] = []
    for u in sorted(urls):
        r = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", base + u],
            capture_output=True, text=True,
        )
        code = r.stdout.strip()
        if code != "200":
            broken.append((u, code))

    print(f"    links: {len(urls)} unique URLs scanned")
    if broken:
        print(f"    BROKEN: {len(broken)}", file=sys.stderr)
        for u, c in broken[:20]:
            print(f"      {c}  {u}", file=sys.stderr)
        return 1
    print("    all links green")
    return 0


if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    sys.exit(main(base))
