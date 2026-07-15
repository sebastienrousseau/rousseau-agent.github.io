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
hreflang: "fr"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "fr"
locale: "fr_FR"
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
permalink: "https://docs.rousseau-agent.dev/fr/changelog/"
subtitle: "Notes de version chronologiques pour rousseau-agent."
tags: "changelog, reference"
title: "Journal des modifications"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "changelog, release notes, versions, snapshot"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Journal des modifications"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 28
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/changelog/index.html"
item_link: "https://docs.rousseau-agent.dev/changelog/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Journal des modifications"
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
twitter_title: "Journal des modifications"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Merci à chaque opérateur qui exploite son propre agent de codage."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## État actuel — juillet 2026

Premier instantané public. Points saillants de ce qui est livré aujourd'hui :

- **Neuf transports chat.** WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, Email, SMS.
- **Cinq fournisseurs LLM.** claudecli, Anthropic direct, AWS Bedrock, Google Vertex AI, compatible OpenAI.
- **Serveur MCP.** JSON-RPC 2.0 sur stdio, révision de spec 2024-11-05.
- **Provenance de build SLSA niveau 3**, checksums de release signés cosign, SBOM CycloneDX.
- **76 % de couverture de tests** sur le module (les packages cœur sont à 85–100 %).
- **Zéro alerte Dependabot ouverte.**
- **CI en mode race complet** sur `ubuntu-latest` et `macos-latest`.

## Détail

Pour l'historique complet commit par commit, voir le git log à https://github.com/sebastienrousseau/rousseau-agent.

Chaque commit utilise [Conventional Commits](https://www.conventionalcommits.org/). La page changelog recevra des entrées structurées une fois la première release taguée coupée ; jusque-là, `git log --oneline` est la référence faisant autorité.

## Politique de compatibilité

- **Le format du fichier de config** est versionné par ajouts de champs, pas par ruptures de schéma. Les nouvelles clés sont sûres à ignorer ; les renommages et suppressions atterriront derrière un avertissement de dépréciation dans la release précédant la suppression.
- **`agent.Provider`, `agent.Message`, `agent.Session`** sont des exports stables destinés aux intégrateurs tiers. Les changements cassants atterriront à un bump de version majeure.
- **Les packages `internal/*`** ne sont pas une API stable — ils sont internes au projet. Les consommateurs tiers ne devraient pas les importer (la visibilité `internal` de Go l'impose).

## Où déposer les retours

- Bugs et demandes de fonctionnalités : GitHub issues.
- Sécurité : `sebastian.rousseau@gmail.com` (voir [/security/](/fr/security/)).
