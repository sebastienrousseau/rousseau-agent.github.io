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
hreflang: "de"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "de"
locale: "de_DE"
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
permalink: "https://docs.rousseau-agent.dev/de/changelog/"
subtitle: "Chronologische Release-Notes für rousseau-agent."
tags: "changelog, reference"
title: "Änderungsprotokoll"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "changelog, release notes, versions, snapshot"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Änderungsprotokoll"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 28
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/changelog/index.html"
item_link: "https://docs.rousseau-agent.dev/changelog/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Änderungsprotokoll"
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
twitter_title: "Änderungsprotokoll"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Danke an jeden Operator, der seinen eigenen Coding-Agenten betreibt."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Aktueller Stand — Juli 2026

Erste öffentliche Momentaufnahme. Höhepunkte dessen, was heute ausgeliefert wird:

- **Neun Chat-Transporte.** WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, Email, SMS.
- **Fünf LLM-Anbieter.** claudecli, Anthropic direkt, AWS Bedrock, Google Vertex AI, OpenAI-kompatibel.
- **MCP-Server.** JSON-RPC 2.0 über stdio, Spezifikations-Revision 2024-11-05.
- **SLSA Level 3** Build-Provenienz, cosign-signierte Release-Prüfsummen, CycloneDX-SBOM.
- **76 % Testabdeckung** über das Modul (Kernpakete liegen bei 85–100 %).
- **Null offene Dependabot-Warnungen.**
- **Vollständige Race-Mode-CI** auf `ubuntu-latest` und `macos-latest`.

## Details

Für die vollständige Commit-für-Commit-Historie siehe den git log unter https://github.com/sebastienrousseau/rousseau-agent.

Jeder Commit verwendet [Conventional Commits](https://www.conventionalcommits.org/). Die Changelog-Seite erhält strukturierte Einträge, sobald das erste getaggte Release veröffentlicht wird; bis dahin ist `git log --oneline` die maßgebliche Referenz.

## Kompatibilitätsrichtlinie

- **Das Konfigurationsdateiformat** wird durch Feld-Ergänzungen versioniert, nicht durch Schemabrüche. Neue Schlüssel können sicher ignoriert werden; Umbenennungen und Entfernungen erfolgen mit einer Deprecation-Warnung im Release vor der Entfernung.
- **`agent.Provider`, `agent.Message`, `agent.Session`** sind stabile Exports, die für Drittanbieter-Einbetter gedacht sind. Breaking Changes erfolgen bei einem Major-Versionssprung.
- **`internal/*`-Pakete** sind keine stabile API – sie sind projektintern. Drittanbieter-Consumer sollten sie nicht importieren (Gos `internal`-Sichtbarkeit erzwingt dies).

## Wohin mit Feedback

- Bugs und Feature-Wünsche: GitHub-Issues.
- Sicherheit: `sebastian.rousseau@gmail.com` (siehe [/security/](/de/security/)).
