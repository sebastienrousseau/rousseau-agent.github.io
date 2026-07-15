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
changefreq: "monthly"
description: "Landing page for the rousseau-agent developer guide: architecture, how to add a transport, provider, or tool, testing pattern, contributing."
keywords: "developer guide, architecture, add transport, add provider, add tool, testing, contributing"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/developer-guide/"
subtitle: "Architecture, points d'extension, tests, contribution."
tags: "developer-guide, architecture, extend"
title: "Guide du développeur"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "developer guide, architecture, add transport, add provider, add tool, testing, contributing"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide du développeur"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 60
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guide du développeur"
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
twitter_description: "Landing page for the rousseau-agent developer guide: architecture, how to add a transport, provider, or tool, testing pattern, contributing."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide du développeur"
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

## Pour les contributeurs et les intégrateurs

Le guide développeur couvre tout ce dont vous avez besoin pour modifier rousseau ou embarquer sa boucle d'agent dans votre propre binaire. Si vous voulez uniquement exécuter rousseau, lisez plutôt le [Guide utilisateur](/fr/user-guide/cli/).

## Pages

| Page | Sujet |
|---|---|
| [Architecture](/fr/developer-guide/architecture/) | Architecture en couches : agent, fournisseur, outils, transport, cli. Frontières de modules. |
| [Ajouter un transport](/fr/developer-guide/add-a-transport/) | Implémenter `transport.Transport` et l'enregistrer dans la CLI. |
| [Ajouter un fournisseur](/fr/developer-guide/add-a-provider/) | Implémenter `agent.Provider` (et optionnellement `agent.StreamingProvider`). |
| [Ajouter un outil](/fr/developer-guide/add-a-tool/) | Implémenter `tools.Tool` et le câbler dans le registry. |
| [Testing](/fr/developer-guide/testing/) | Injection de dépendances via interfaces, générateurs de fakes, seuils de couverture. |
| [Contribuer](/fr/developer-guide/contributing/) | Checklist des PR, style de commit, gate qualité. |

## Organisation du dépôt

```
cmd/rousseau/                 Point d'entrée (gestion des signaux + Execute)
internal/agent/               Session, Message, Turn, boucle d'agent, interfaces Provider, compression
internal/cli/                 Arborescence de commandes Cobra (chat, commandes par transport, doctor, status, cron, mcp, skills, init, version)
internal/config/              Basé sur Viper ; précédence flag > env > fichier > défaut
internal/cron/                Goroutine planificateur robfig/cron/v3 avec stockage durable des tâches
internal/llm/anthropic/       Fournisseur API Anthropic direct avec marqueurs de cache
internal/llm/bedrock/         Fournisseur AWS Bedrock
internal/llm/claudecli/       Fournisseur sous-processus (CLI claude + parseur JSON)
internal/llm/openai/          Fournisseur compatible OpenAI
internal/llm/vertex/          Fournisseur Google Vertex AI
internal/mcp/                 Serveur MCP (JSON-RPC 2.0 sur stdio, spec 2024-11-05)
internal/skills/              Chargeur et composition de skills style agentskills.io
internal/state/               Interface Store + type Summary
internal/state/sqlite/        Implémentation SQLite (WAL, JIDMap, cache claude, rappel FTS5, table cron)
internal/tools/               Interface Tool + Registry sûr en concurrence
internal/tools/builtin/       read, write, edit, grep, bash
internal/transport/           Interface Transport + Router
internal/transport/{whatsapp,signal,telegram,matrix,slack,discord,sms,imessage,email}/
                              Neuf adaptateurs de transport
internal/tui/                 Modèle Bubble Tea
docker/                       Dockerfile, unité Quadlet Podman
docs/                         Roadmap, analyse d'écarts
examples/embed-agent/         Exemple minimal d'embedding en bibliothèque
```

## Direction des dépendances

`agent` ne dépend que des interfaces exposées par `tools`, de ses propres types `Provider` et de la bibliothèque standard. Les fournisseurs, magasins et transports concrets dépendent de `agent` — jamais l'inverse.

C'est imposé par convention et par le gate lint CI. Si vous vous retrouvez à devoir importer un fournisseur concret depuis `agent`, vous faites quelque chose que le layering ne sanctionne pas ; reculez.

## Gate qualité

Chaque commit doit passer, localement et en CI :

- `go vet ./...`
- `golangci-lint run` (18 linters, épinglages exacts dans `.golangci.yml`)
- `go test -race -count=1 -covermode=atomic ./...` sur Linux et macOS
- Plancher de couverture (actuellement 75 % au global ; les packages cœur sont à 85–100 %)
- `govulncheck ./...`
- Analyse statique CodeQL (Go)
- Vérification de build reproductible

Exécutez le gate en local avec `make check`.

## Suite

- [Architecture](/fr/developer-guide/architecture/) — la carte.
- [Contribuer](/fr/developer-guide/contributing/) — le processus.
