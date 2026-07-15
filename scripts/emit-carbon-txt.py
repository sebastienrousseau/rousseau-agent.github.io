#!/usr/bin/env python3
"""Emit /carbon.txt — the sustainability manifest for docs.rousseau-agent.dev.

Follows the community carbon.txt schema (https://carbontxt.org/) with
enough detail for auditors to verify page-weight discipline and
zero-telemetry posture.
"""
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "public"


def main() -> None:
    # Page-weight sample (kilobytes)
    landing = (ROOT / "index.html").stat().st_size / 1024
    quickstart = (ROOT / "quickstart" / "index.html").stat().st_size / 1024
    total = sum(p.stat().st_size for p in ROOT.rglob("*")) / (1024 * 1024)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    content = f"""# carbon.txt for docs.rousseau-agent.dev
# https://carbontxt.org/ — community sustainability manifest
# Generated at build time by scripts/emit-carbon-txt.py

[upstream]
# The hosting provider(s) upstream of this domain.
# Any static host — Cloudflare Pages, Netlify, S3+CloudFront, or self-hosted.

[org]
# rousseau-agent is an open-source project maintained by Sebastien Rousseau.
# The docs site itself has no analytics, no third-party scripts, no CDN
# beyond fonts served same-origin, and no tracking pixels.
name = "rousseau-agent"
maintainer = "sebastian.rousseau@gmail.com"
repository = "https://github.com/sebastienrousseau/rousseau-agent"

[metrics]
last_measured = "{now}"
landing_page_kb = {landing:.1f}
quickstart_page_kb = {quickstart:.1f}
total_site_mb = {total:.1f}

[budget]
# CI-enforced weight limits per rendered HTML file.
landing_max_kb = 60
interior_max_kb = 100

[practices]
# Sustainable Web Design Model v4 alignment.
telemetry = "none"
third_party_scripts = "none"
third_party_fonts = "none — Inter / Newsreader / JetBrains Mono served same-origin"
external_analytics = "none"
external_cdn = "none for docs assets (fonts, CSS, JS all fingerprinted and same-origin)"
service_worker = "cache-first for hashed assets + fonts; network-first for HTML"
reduced_motion = "@media (prefers-reduced-motion: reduce) respected across all animations"
"""
    out = ROOT / "carbon.txt"
    out.write_text(content)
    print(f"    carbon:   emitted {out.stat().st_size:,} bytes at /carbon.txt")


if __name__ == "__main__":
    main()
