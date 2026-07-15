---
author: "sebastian.rousseau@gmail.com (Sebastien Rousseau)"
banner_alt: "rousseau-agent banner"
banner_height: "398"
banner_width: "1440"
banner: ""
cdn: "https://cloudcdn.pro"
charset: "utf-8"
cname: "docs.rousseau-agent.dev"
copyright: "Copyright © 2026 Sebastien Rousseau. Released under the MIT License."
date: "July 13, 2026"
description: "Verify every docs page against its build-time SHA-256 signature."
format-detection: "telephone=no"
hreflang: "en"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
keywords: "security, rousseau-agent"
language: "en-GB"
layout: "page"
locale: "en_GB"
logo_alt: "rousseau-agent logo"
logo_height: "33"
logo_width: "100"
logo: ""
name: "rousseau-agent"
permalink: "https://docs.rousseau-agent.dev/reference/provenance/"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "rousseau"
subtitle: "Verify every docs page against its build-time SHA-256 signature."
tags: "security"
theme-color: "26, 58, 138"
title: "Content provenance"
url: "https://docs.rousseau-agent.dev"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
changefreq: "monthly"

news_genres: "Blog"
news_keywords: "security"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Content provenance"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "security"
order: 90
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/provenance/"
item_link: "https://docs.rousseau-agent.dev/reference/provenance/"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Content provenance"
last_build_date: "Mon, 13 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
ttl: "60"
type: "website"
webmaster: sebastian.rousseau@gmail.com (Sebastien Rousseau)

apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "rousseau-agent"
apple-touch-fullscreen: "yes"

msapplication-navbutton-color: "rgb(26,58,138)"

twitter_card: "summary"
twitter_creator: "rousseauagent"
twitter_description: "Verify every docs page against its build-time SHA-256 signature."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Content provenance"
twitter_url: "https://docs.rousseau-agent.dev"

author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Overview

<aside class="admonition" data-type="tip"><span class="admonition-title">Every page is signed at build time</span><p>Rousseau ships a SHA-256 fingerprint of every rendered HTML page in <code>/provenance.json</code>. This mirrors the SLSA-3 discipline on the binary — pages should render bit-identically from a clean checkout.</p></aside>

## Where the signatures live

- **Manifest**: <a href="/provenance.json"><code>/provenance.json</code></a>
- **Schema**: <code>{"version": 1, "algorithm": "sha256", "pages": {url: sha256hex}}</code>

## Verify a page you're reading

Copy this into your terminal (the second command reads the current URL and cross-checks):

```sh
curl -s https://docs.rousseau-agent.dev/provenance.json | jq '.pages["/quickstart/"]'
# Expected: a hex digest matching the current page's sha256
curl -sL https://docs.rousseau-agent.dev/quickstart/ | sha256sum | awk '{print $1}'
```

If the two match, the page hasn't been tampered with in transit.

## Roadmap: page-level cosign signatures

The current manifest is unsigned. The roadmap is to publish `/provenance.json.sig` (cosign-signed against the GitHub Actions OIDC identity of this repo). Tracking issue: rousseau-agent#TBD.

## Why we don't sign every HTML directly

Per-file cosign signatures would balloon the site (2× the HTML count) and cache poorly. A single signed manifest gives the same integrity guarantee with 1 signature check.

