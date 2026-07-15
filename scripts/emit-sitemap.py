#!/usr/bin/env python3
"""Emit a proper sitemap.xml + robots.txt.

The SSG's built-in sitemap plugin produces an empty <urlset/> for
reasons we haven't investigated. Since docs.rousseau-agent.dev needs
its sitemap for SEO, we walk public/ ourselves.

Runs at the end of every build via scripts/build.sh.
"""
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "public"
BASE = "https://docs.rousseau-agent.dev"
LANGS = ("en-GB", "fr", "de", "es", "ja", "pt-BR", "zh-Hans")


def main() -> None:
    lastmod = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    urls: list[str] = []
    for p in ROOT.rglob("index.html"):
        rel = p.relative_to(ROOT).parent
        seg = str(rel).replace("\\", "/")
        url = BASE + "/" if seg == "." else f"{BASE}/{seg}/"
        # Skip fingerprinted CSP asset directories and tag pages
        if "_csp" in url or "/tags/" in url or "/category/" in url:
            continue
        urls.append(url)
    urls = sorted(set(urls))

    def strip_lang(u: str) -> str:
        for pfx in ("/fr/", "/de/", "/es/", "/ja/", "/pt-BR/", "/zh-Hans/"):
            if u.startswith(BASE + pfx):
                return BASE + "/" + u[len(BASE + pfx):]
        return u

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for u in urls:
        canonical = strip_lang(u)
        lines.append("  <url>")
        lines.append(f"    <loc>{u}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        for lang in LANGS:
            prefix = "" if lang == "en-GB" else f"/{lang}"
            alt_path = canonical[len(BASE):]
            lines.append(
                f'    <xhtml:link rel="alternate" hreflang="{lang}" '
                f'href="{BASE}{prefix}{alt_path}"/>'
            )
        lines.append(
            f'    <xhtml:link rel="alternate" hreflang="x-default" '
            f'href="{canonical}"/>'
        )
        lines.append("  </url>")
    lines.append("</urlset>")

    sitemap = ROOT / "sitemap.xml"
    sitemap.write_text("\n".join(lines))

    robots = ROOT / "robots.txt"
    robots.write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n"
    )

    print(f"    sitemap: {len(urls)} URLs, {sitemap.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
