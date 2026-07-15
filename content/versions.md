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
date: "July 14, 2026"
description: "Every published snapshot of the rousseau-agent docs with headline changes."
format-detection: "telephone=no"
hreflang: "en"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
keywords: "reference"
language: "en-GB"
layout: "page"
locale: "en_GB"
logo_alt: "rousseau-agent logo"
logo_height: "33"
logo_width: "100"
logo: ""
name: "rousseau-agent"
permalink: "https://docs.rousseau-agent.dev/"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "rousseau"
subtitle: "Every published snapshot of the rousseau-agent docs with headline changes."
tags: "reference"
theme-color: "26, 58, 138"
title: "Versions & diffs"
url: "https://docs.rousseau-agent.dev"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
changefreq: "monthly"

news_genres: "Blog"
news_keywords: "reference"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 14 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Versions & diffs"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 87
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/"
item_link: "https://docs.rousseau-agent.dev/"
item_pub_date: "Mon, 14 Jul 2026 00:00:00 GMT"
item_title: "Versions & diffs"
last_build_date: "Mon, 14 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Mon, 14 Jul 2026 00:00:00 GMT"
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
twitter_description: "Every published snapshot of the rousseau-agent docs with headline changes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Versions & diffs"
twitter_url: "https://docs.rousseau-agent.dev"

author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-14"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Overview

<aside class="admonition" data-type="tip"><span class="admonition-title">Version selector</span><p>Use the version dropdown in the top navigation to jump between snapshots.</p></aside>

## Timeline

| Tag | Cut | Highlights |
|---|---|---|
| **v0.5** (archived) | pre-2026-06 | 3 transports, 3 providers, no MCP, no cron |
| **v0.6** (archived) | 2026-06 | +Matrix, +Bedrock, +MCP, +cron, SLSA-3 shipped |
| **v0.7** (preview) | 2026-07 · main | +5 transports (Slack, Discord, iMessage, SMS, Email), +Vertex, +7 languages, +PWA, +semantic search, +Ask-AI dialog, +signed content provenance, +version selector, +carbon posture |

## Headline diffs

### 0.5 → 0.6

- +1 transport: Matrix
- +1 provider: AWS Bedrock
- +MCP server (JSON-RPC 2.0 stdio)
- +cron scheduler
- +skills loader
- +SLSA-3 + cosign + SBOM discipline

### 0.6 → 0.7 (in progress)

- +5 transports: Slack, Discord, iMessage, SMS, Email
- +1 provider: Google Vertex AI
- +7 languages
- +PWA + service worker
- +BM25 semantic search with stemming + synonyms
- +Ask-AI dialog
- +Content provenance manifest
- +Version selector + archives
- +Carbon posture page

## Reading order

1. Start at [Quickstart](/quickstart/).
2. Check the [changelog](/changelog/) for the current commit.
3. If migrating, follow [Migrations](/migrations/overview/) between adjacent versions.
4. If auditing, verify content via [/reference/provenance/](/reference/provenance/) against `/provenance.json`.
