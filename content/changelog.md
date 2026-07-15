---

# Front Matter (YAML)

author: "sebastian.rousseau@gmail.com (Sebastien Rousseau)"
banner_alt: "rousseau-agent banner"
banner_height: "398"
banner_width: "1440"
banner: ""
cdn: "https://cloudcdn.pro"
charset: "utf-8"
cname: "docs.rousseau-agent.dev"
copyright: "Copyright © 2026 Sebastien Rousseau. Released under the MIT License."
date: "July 12, 2026"
download: ""
format-detection: "telephone=no"
hreflang: "en"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "en-GB"
locale: "en_GB"
logo_alt: "rousseau-agent logo"
logo_height: "33"
logo_width: "100"
logo: ""
name: "rousseau-agent"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "rousseau"
theme-color: "26, 58, 138"
url: "https://docs.rousseau-agent.dev"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
changefreq: "weekly"
description: "Chronological release notes for rousseau-agent. First public snapshot: 9 transports, 5 providers, MCP server, SLSA-3, 76% coverage."
keywords: "changelog, release notes, versions, snapshot"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/changelog/"
subtitle: "Chronological release notes for rousseau-agent."
tags: "changelog, reference"
title: "Changelog"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "changelog, release notes, versions, snapshot"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Changelog"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 28
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/changelog/index.html"
item_link: "https://docs.rousseau-agent.dev/changelog/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Changelog"
last_build_date: "Sun, 12 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
ttl: "60"
type: "website"
webmaster: sebastian.rousseau@gmail.com (Sebastien Rousseau)

# Apple - The Apple front matter (YAML).
apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "rousseau-agent"
apple-touch-fullscreen: "yes"

# MS Application - The MS Application front matter (YAML).
msapplication-navbutton-color: "rgb(26,58,138)"

# Twitter Card - The Twitter Card front matter (YAML).
twitter_card: "summary"
twitter_creator: "rousseauagent"
twitter_description: "Chronological release notes for rousseau-agent. First public snapshot: 9 transports, 5 providers, MCP server, SLSA-3, 76% coverage."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Changelog"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Current state — July 2026

First public snapshot. Highlights of what ships today:

- **Nine chat transports.** WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, Email, SMS.
- **Five LLM providers.** claudecli, Anthropic direct, AWS Bedrock, Google Vertex AI, OpenAI-compatible.
- **MCP server.** JSON-RPC 2.0 over stdio, spec revision 2024-11-05.
- **SLSA Level 3** build provenance, cosign-signed release checksums, CycloneDX SBOM.
- **76% test coverage** across the module (core packages sit 85–100%).
- **Zero open Dependabot alerts.**
- **Full race-mode CI** on `ubuntu-latest` and `macos-latest`.

## Detail

For the full commit-by-commit history, see the git log at https://github.com/sebastienrousseau/rousseau-agent.

Every commit uses [Conventional Commits](https://www.conventionalcommits.org/). The changelog page will land structured entries once the first tagged release is cut; until then, `git log --oneline` is the authoritative reference.

## Compatibility policy

- **Config file format** is versioned by field additions, not schema breaks. New keys are safe to ignore; renames and removals will land behind a deprecation warning in the release preceding removal.
- **`agent.Provider`, `agent.Message`, `agent.Session`** are stable exports intended for third-party embedders. Breaking changes will land at a major version bump.
- **`internal/*` packages** are not stable API — they are internal to the project. Third-party consumers should not import them (Go's `internal` visibility enforces this).

## Where to file feedback

- Bugs and feature requests: GitHub issues.
- Security: `sebastian.rousseau@gmail.com` (see [/security/](/security/)).
