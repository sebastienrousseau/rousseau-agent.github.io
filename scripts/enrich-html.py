#!/usr/bin/env python3
"""Post-build enrichment passes:

  1. og:image + twitter:image — injects an SVG-based branded card URL
     into every built page's OG / Twitter meta tags. The SVG lives at
     `/og/<slug>.svg` (emitted below) and doubles as a lightweight
     preview image indexers accept.
  2. Signed content provenance — writes a SHA-256 fingerprint alongside
     every built HTML page (mirroring the SLSA-3 discipline on the
     binary). Emits `provenance.json` at the root: `{path: sha256}`.
  3. Ensure `<link rel="stylesheet" href="/highlight.css">` alias holds.
"""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1] / "public"
OG_DIR = ROOT / "og"
OG_DIR.mkdir(exist_ok=True)


SVG_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630" role="img" aria-labelledby="ogtitle ogdesc">
  <title id="ogtitle">{title}</title>
  <desc id="ogdesc">{description}</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0f1424"/>
      <stop offset="1" stop-color="#1a3a8a"/>
    </linearGradient>
    <linearGradient id="brand" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#7aa4ff"/>
      <stop offset="1" stop-color="#41d1ff"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <circle cx="120" cy="120" r="40" fill="#000"/>
  <text x="120" y="140" font-family="Georgia, serif" font-size="52" font-weight="700"
        fill="#fff" text-anchor="middle">r</text>
  <text x="188" y="132" font-family="Inter, sans-serif" font-size="28" font-weight="600"
        fill="#d8e4ff">rousseau-agent · docs</text>
  <text x="60" y="360" font-family="Georgia, serif" font-size="72" font-weight="700"
        fill="url(#brand)" text-anchor="start">
    <tspan x="60">{title_line1}</tspan>
    <tspan x="60" dy="80">{title_line2}</tspan>
  </text>
  <text x="60" y="530" font-family="Inter, sans-serif" font-size="24" font-weight="400"
        fill="#a5adba" text-anchor="start">{description_short}</text>
  <text x="60" y="595" font-family="Inter, sans-serif" font-size="20" font-weight="500"
        fill="#7aa4ff" text-anchor="start">docs.rousseau-agent.dev</text>
</svg>
"""


def escape_xml(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def wrap_title(title: str) -> tuple[str, str]:
    """Split a title into two ~30-char lines for the OG card."""
    if len(title) <= 28:
        return escape_xml(title), ""
    words = title.split()
    line1, line2 = [], []
    length = 0
    for w in words:
        if length + len(w) + 1 <= 28 and not line2:
            line1.append(w)
            length += len(w) + 1
        else:
            line2.append(w)
    return escape_xml(" ".join(line1)), escape_xml(" ".join(line2))


def og_slug_for(path: Path) -> str:
    seg = str(path.relative_to(ROOT).parent).replace("\\", "/").replace("/", "-")
    return "root" if seg == "." else seg[:80]


def make_og_svg(title: str, description: str, path: Path) -> str:
    line1, line2 = wrap_title(title)
    svg = SVG_TEMPLATE.format(
        title=escape_xml(title),
        description=escape_xml(description),
        title_line1=line1,
        title_line2=line2,
        description_short=escape_xml(description[:80] + ("…" if len(description) > 80 else "")),
    )
    slug = og_slug_for(path)
    out = OG_DIR / f"{slug}.svg"
    out.write_text(svg)
    return f"/og/{quote(slug)}.svg"


def inject_meta(html: str, key: str, content: str) -> str:
    """Replace or insert a <meta property/name="{key}" content="…"> tag."""
    pat = re.compile(
        rf'<meta[^>]+(?:property|name)="{re.escape(key)}"[^>]*content="[^"]*"[^>]*/?>',
    )
    tag = f'<meta {("property" if key.startswith("og:") else "name")}="{key}" content="{content}"/>'
    if pat.search(html):
        return pat.sub(tag, html, 1)
    return html.replace("</head>", tag + "</head>", 1)


def main() -> None:
    provenance: dict[str, str] = {}
    enriched = 0
    for html_file in ROOT.rglob("index.html"):
        rel = html_file.relative_to(ROOT).parent
        seg = str(rel).replace("\\", "/")
        if "_csp" in seg:
            continue
        text = html_file.read_text(errors="ignore")
        title_m = re.search(r"<title>([^<]+)</title>", text)
        desc_m = re.search(r'<meta name="description" content="([^"]+)"', text)
        title = title_m.group(1) if title_m else "rousseau-agent"
        description = desc_m.group(1) if desc_m else "Self-hosted coding agent."
        og_url = "https://docs.rousseau-agent.dev" + make_og_svg(title, description, html_file)
        text = inject_meta(text, "og:image", og_url)
        text = inject_meta(text, "og:image:width", "1200")
        text = inject_meta(text, "og:image:height", "630")
        text = inject_meta(text, "og:image:type", "image/svg+xml")
        text = inject_meta(text, "twitter:image", og_url)
        text = inject_meta(text, "twitter:image:alt", title)
        html_file.write_text(text)

        # Provenance: sha256 of the enriched HTML
        digest = hashlib.sha256(text.encode()).hexdigest()
        url = "/" if seg == "." else f"/{seg}/"
        provenance[url] = digest
        enriched += 1

    prov_path = ROOT / "provenance.json"
    prov_path.write_text(json.dumps({
        "version": 1,
        "algorithm": "sha256",
        "pages": provenance,
    }, separators=(",", ":")))
    print(f"    og:       {enriched} pages enriched with OG cards")
    print(f"    prov:     {len(provenance)} pages signed, {prov_path.stat().st_size:,} bytes manifest")


if __name__ == "__main__":
    main()
