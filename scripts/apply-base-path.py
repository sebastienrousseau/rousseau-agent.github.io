#!/usr/bin/env python3
"""Rewrite root-relative asset URLs to include BASE_PATH.

When the site is hosted at a subpath (e.g. GitHub Pages project sites
serve at `<user>.github.io/<repo>/`), all `href="/foo"`, `src="/foo"`,
`fetch('/foo')`, sitemap `<loc>`, service-worker precache lists, and
manifest URLs must be rewritten to include the subpath prefix.

Set BASE_PATH="/rousseau-agent.github.io" (no trailing slash) and this
pass touches every built HTML, XML, JSON, JS asset in public/ that
uses a root-relative reference.
"""
from __future__ import annotations
import json
import os
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "public"


def rewrite_html(text: str, prefix: str) -> str:
    """Prefix href/src/action/data-* etc. that begin with a single '/'.
    Ignore already-prefixed URLs, protocol-relative URLs, and anchor-only.
    """
    # href|src|action|content|poster|data-<x> = "/..."   (double-quoted)
    def repl(m: re.Match[str]) -> str:
        attr, value = m.group(1), m.group(2)
        if value.startswith(prefix + "/") or value == prefix:
            return m.group(0)
        return f'{attr}="{prefix}{value}"'

    pattern = re.compile(
        r'(href|src|action|poster|content|srcset)="(/(?!/)[^"#?]*)"'
    )
    text = pattern.sub(repl, text)

    # og:url and twitter:url should stay absolute (they include the domain
    # in the frontmatter already). We only rewrite root-relative refs.
    return text


def rewrite_xml(text: str, prefix: str, host: str) -> str:
    """Rewrite root-relative URLs inside sitemap/atom/rss.
    Sitemap loc values are absolute — no change needed. But xhtml:link
    hreflang alternates and any relative sitemap paths need care.
    """
    # No-op today — sitemap already uses absolute URLs with the host.
    # Keep this function so we can add rules later without churning callers.
    return text


def rewrite_search_json(text: str, prefix: str) -> str:
    d = json.loads(text)
    for doc in d.get("docs", []):
        if doc["u"].startswith("/") and not doc["u"].startswith(prefix + "/"):
            doc["u"] = prefix + doc["u"]
    return json.dumps(d, separators=(",", ":"))


def rewrite_qa_json(text: str, prefix: str) -> str:
    d = json.loads(text)
    for pair in d.get("pairs", []):
        if pair["src"].startswith("/") and not pair["src"].startswith(prefix + "/"):
            pair["src"] = prefix + pair["src"]
    return json.dumps(d, separators=(",", ":"))


def rewrite_provenance_json(text: str, prefix: str) -> str:
    d = json.loads(text)
    pages = d.get("pages", {})
    new_pages = {}
    for url, digest in pages.items():
        if url.startswith("/") and not url.startswith(prefix + "/"):
            new_pages[prefix + url] = digest
        else:
            new_pages[url] = digest
    d["pages"] = new_pages
    return json.dumps(d, separators=(",", ":"))


def rewrite_manifest(text: str, prefix: str) -> str:
    d = json.loads(text)
    # start_url + scope + id
    for key in ("start_url", "scope", "id"):
        v = d.get(key)
        if isinstance(v, str) and v.startswith("/") and not v.startswith(prefix + "/"):
            # Preserve any query string
            d[key] = prefix + v if key != "scope" else prefix + "/"
    # icons + screenshots + shortcuts
    for icon in d.get("icons", []) + d.get("screenshots", []):
        s = icon.get("src", "")
        if s.startswith("/") and not s.startswith(prefix + "/"):
            icon["src"] = prefix + s
    for sc in d.get("shortcuts", []):
        u = sc.get("url", "")
        if u.startswith("/") and not u.startswith(prefix + "/"):
            sc["url"] = prefix + u
    st = d.get("share_target", {})
    if isinstance(st, dict):
        a = st.get("action", "")
        if a.startswith("/") and not a.startswith(prefix + "/"):
            st["action"] = prefix + a
    return json.dumps(d, indent=2)


def rewrite_service_worker(text: str, prefix: str) -> str:
    """Rewrite hardcoded route literals in sw.js: precache URLs, OFFLINE_URL,
    and the pathname startswith() checks that decide caching strategy.
    """
    # PRECACHE_URLS: string literals like '/', '/quickstart/', '/offline/index.html', ...
    def prefix_literal(m: re.Match[str]) -> str:
        q, url, q2 = m.group(1), m.group(2), m.group(3)
        if url.startswith(prefix + "/") or url == prefix:
            return m.group(0)
        return f"{q}{prefix}{url}{q2}"

    # Match quoted strings starting with '/'
    text = re.sub(r"(['\"])(/[^'\"]*)(['\"])", prefix_literal, text)

    # Also handle url.pathname.startsWith('/_csp/') etc.
    # The rewrite above already covers them if we treat them as quoted strings.

    return text


def rewrite_js_asset(text: str, prefix: str) -> str:
    """For extracted _csp/*.js bundles that inline root paths.
    Prefix `fetch('/foo')`, `location.href='/foo'` etc.
    """
    def prefix_literal(m: re.Match[str]) -> str:
        q, url, q2 = m.group(1), m.group(2), m.group(3)
        if url.startswith(prefix + "/") or url == prefix:
            return m.group(0)
        return f"{q}{prefix}{url}{q2}"

    # Only rewrite short quoted strings that look like paths (no whitespace).
    text = re.sub(r"(['\"])(/[a-zA-Z0-9_.~/-]*[a-zA-Z0-9_.~/-])(['\"])",
                  prefix_literal, text)
    return text


def rewrite_robots(text: str, prefix: str, host: str) -> str:
    # Sitemap URL uses absolute (already includes host). Only Allow/Disallow
    # paths are root-relative and cannot be prefixed (they refer to
    # sub-paths of the SITE root, which for a project-site IS the prefix).
    # No-op.
    return text


def main() -> int:
    prefix = os.environ.get("BASE_PATH", "").rstrip("/")
    if not prefix:
        print("    base-path: no BASE_PATH set — skipping (site serves at root)")
        return 0
    if not prefix.startswith("/"):
        prefix = "/" + prefix

    host = os.environ.get("BASE_HOST", "https://docs.rousseau-agent.dev")

    stats = {"html": 0, "xml": 0, "js": 0, "css": 0, "json": 0, "sw": 0, "manifest": 0}

    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        rel = str(p.relative_to(ROOT))

        if p.suffix == ".html":
            text = p.read_text(errors="ignore")
            new = rewrite_html(text, prefix)
            if new != text:
                p.write_text(new)
                stats["html"] += 1
            continue

        if rel == "sw.js":
            text = p.read_text()
            new = rewrite_service_worker(text, prefix)
            if new != text:
                p.write_text(new)
                stats["sw"] += 1
            continue

        if rel == "manifest.json":
            text = p.read_text()
            p.write_text(rewrite_manifest(text, prefix))
            stats["manifest"] += 1
            continue

        if rel == "search.json":
            p.write_text(rewrite_search_json(p.read_text(), prefix))
            stats["json"] += 1
            continue

        if rel == "qa.json":
            p.write_text(rewrite_qa_json(p.read_text(), prefix))
            stats["json"] += 1
            continue

        if rel == "provenance.json":
            p.write_text(rewrite_provenance_json(p.read_text(), prefix))
            stats["json"] += 1
            continue

        if p.suffix == ".js" and rel.startswith("_csp/"):
            new = rewrite_js_asset(p.read_text(), prefix)
            if new != p.read_text():
                p.write_text(new)
                stats["js"] += 1
            continue

        if p.suffix in (".xml", ".txt") and rel in ("sitemap.xml", "robots.txt", "news-sitemap.xml"):
            # Sitemap loc uses absolute URLs with the host; no-op for now.
            pass

    print(f"    base-path: prefixed with '{prefix}' — "
          f"html={stats['html']} sw={stats['sw']} manifest={stats['manifest']} "
          f"json={stats['json']} js={stats['js']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
