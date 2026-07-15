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
description: "Sustainability commitments and page-weight budget."
format-detection: "telephone=no"
hreflang: "en"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
keywords: "reference, rousseau-agent"
language: "en-GB"
layout: "page"
locale: "en_GB"
logo_alt: "rousseau-agent logo"
logo_height: "33"
logo_width: "100"
logo: ""
name: "rousseau-agent"
permalink: "https://docs.rousseau-agent.dev/reference/carbon/"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "rousseau"
subtitle: "Sustainability commitments and page-weight budget."
tags: "reference"
theme-color: "26, 58, 138"
title: "Carbon posture"
url: "https://docs.rousseau-agent.dev"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
changefreq: "monthly"

news_genres: "Blog"
news_keywords: "reference"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Carbon posture"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 90
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/carbon/"
item_link: "https://docs.rousseau-agent.dev/reference/carbon/"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Carbon posture"
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
twitter_description: "Sustainability commitments and page-weight budget."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Carbon posture"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Zero telemetry, small pages, single-origin fonts</span><p>rousseau-agent docs are engineered to be light, green, and locally cacheable. This page documents the numbers.</p></aside>

## Page weight budget

| Route | Budget | Measured (build 2026-07-13) |
|---|:-:|:-:|
| Landing (`/`) | ≤ 40 KB | ~28 KB |
| Interior docs | ≤ 60 KB | ~50 KB |
| First-visit assets total | ≤ 250 KB | ~180 KB (fonts + CSS + JS + search index page) |
| Semantic search index (`/search.json`) | ≤ 400 KB | measured at build time |

## What we do

- **Fonts** self-hosted at `/fonts/*` with `font-display: swap` (no third-party CDN request).
- **JS** extracted to fingerprinted `/_csp/*.js` with SRI, cached indefinitely.
- **CSS** extracted to fingerprinted `/_csp/*.css` with SRI, cached indefinitely.
- **HTML** minified by the SSG; further gzip/brotli by the host.
- **Zero client analytics**, zero tracking pixels, zero third-party fonts, zero third-party scripts.
- **Service worker** (`/sw.js`) enables offline reads for previously-visited pages.
- **Reduced-motion** is respected via `@media (prefers-reduced-motion: reduce)`.

## Carbon estimate

Following the [Sustainable Web Design Model v4](https://sustainablewebdesign.org/estimating-digital-emissions/):

- ~50 KB per interior page ≈ **0.02 g CO₂e per view** on 100% renewable-powered infrastructure.
- Cached repeat views: essentially zero.

Verify at [Website Carbon Calculator](https://www.websitecarbon.com/) after production deployment.

## Green hosting

Static host operators — check [Green Web Foundation](https://www.thegreenwebfoundation.org/) for their power mix. Rousseau's own container runs where you put it: co-locate in a green region if this matters to you.

