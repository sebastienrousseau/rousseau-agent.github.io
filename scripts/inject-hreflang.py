#!/usr/bin/env python3
"""Inject <link rel="alternate" hreflang="…"> tags for the 7-language
scaffold into every built HTML page.

Runs after `ssg build` so crawlers that don't execute JS still see the
alternates. Language-prefixed URLs are computed from the page's path.
"""
from __future__ import annotations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "public"
BASE = "https://docs.rousseau-agent.dev"
LANGS = [
    ("en-GB", ""),
    ("fr", "/fr"),
    ("de", "/de"),
    ("es", "/es"),
    ("ja", "/ja"),
    ("pt-BR", "/pt-BR"),
    ("zh-Hans", "/zh-Hans"),
]


def canonical_path(url_path: str) -> str:
    """Strip a leading `/<lang>/` prefix so we compute the canonical URL."""
    for _, pfx in LANGS:
        if pfx and url_path.startswith(pfx + "/"):
            return url_path[len(pfx):]
    return url_path


def main() -> None:
    injected = 0
    for html_file in ROOT.rglob("*.html"):
        text = html_file.read_text(errors="ignore")
        if text.count("hreflang=") > 2:
            continue  # already injected on a prior run
        rel = html_file.relative_to(ROOT).parent
        seg = str(rel).replace("\\", "/")
        url_path = "/" if seg == "." else f"/{seg}/"
        canon = canonical_path(url_path)

        alts = "".join(
            f'<link rel="alternate" hreflang="{lang}" href="{BASE}{pfx}{canon}"/>'
            for lang, pfx in LANGS
        )
        alts += f'<link rel="alternate" hreflang="x-default" href="{BASE}{canon}"/>'

        new = text.replace("</head>", alts + "</head>", 1)
        if new != text:
            html_file.write_text(new)
            injected += 1

    print(f"    hreflang: {injected} pages received 8 alternates")


if __name__ == "__main__":
    main()
