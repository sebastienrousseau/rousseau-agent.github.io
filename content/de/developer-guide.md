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
changefreq: "monthly"
description: "Landing page for the rousseau-agent developer guide: architecture, how to add a transport, provider, or tool, testing pattern, contributing."
keywords: "developer guide, architecture, add transport, add provider, add tool, testing, contributing"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/developer-guide/"
subtitle: "Architektur, Erweiterungspunkte, Tests, Mitwirken."
tags: "developer-guide, architecture, extend"
title: "Entwicklerhandbuch"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "developer guide, architecture, add transport, add provider, add tool, testing, contributing"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Entwicklerhandbuch"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 60
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Entwicklerhandbuch"
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
twitter_title: "Entwicklerhandbuch"
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

## Für Mitwirkende und Integratoren

Der Entwicklerleitfaden deckt alles ab, was Sie benötigen, um rousseau zu modifizieren oder seine Agent-Schleife in Ihr eigenes Binary einzubetten. Wenn Sie rousseau nur ausführen wollen, lesen Sie stattdessen den [Benutzerleitfaden](/de/user-guide/cli/).

## Seiten

| Seite | Thema |
|---|---|
| [Architektur](/de/developer-guide/architecture/) | Geschichtete Architektur: agent, provider, tools, transport, cli. Modulgrenzen. |
| [Transport hinzufügen](/de/developer-guide/add-a-transport/) | `transport.Transport` implementieren und in der CLI registrieren. |
| [Provider hinzufügen](/de/developer-guide/add-a-provider/) | `agent.Provider` (und optional `agent.StreamingProvider`) implementieren. |
| [Tool hinzufügen](/de/developer-guide/add-a-tool/) | `tools.Tool` implementieren und in die Registry einbinden. |
| [Tests](/de/developer-guide/testing/) | Dependency Injection über Schnittstellen, Fake-Generatoren, Coverage-Schwellen. |
| [Mitwirken](/de/developer-guide/contributing/) | PR-Checkliste, Commit-Stil, Qualitäts-Gate. |

## Repository-Layout

```
cmd/rousseau/                 Einstiegspunkt (Signalbehandlung + Execute)
internal/agent/               Session, Message, Turn, Agent-Schleife, Provider-Schnittstellen, Kompression
internal/cli/                 Cobra-Befehlsbaum (chat, transport-spezifische Befehle, doctor, status, cron, mcp, skills, init, version)
internal/config/              Viper-basiert; Rangfolge flag > env > file > default
internal/cron/                robfig/cron/v3 Scheduler-Goroutine mit dauerhaftem Job-Speicher
internal/llm/anthropic/       Direkter Anthropic-API-Provider mit Cache-Markern
internal/llm/bedrock/         AWS-Bedrock-Provider
internal/llm/claudecli/       Subprozess-Provider (claude CLI + JSON-Parser)
internal/llm/openai/          OpenAI-kompatibler Provider
internal/llm/vertex/          Google-Vertex-AI-Provider
internal/mcp/                 MCP-Server (JSON-RPC 2.0 über stdio, Spezifikation 2024-11-05)
internal/skills/              agentskills.io-Style-Skill-Loader + Komposition
internal/state/               Store-Schnittstelle + Summary-Typ
internal/state/sqlite/        SQLite-Implementierung (WAL, JIDMap, claude-Cache, FTS5-Recall, Cron-Tabelle)
internal/tools/               Tool-Schnittstelle + concurrency-sichere Registry
internal/tools/builtin/       read, write, edit, grep, bash
internal/transport/           Transport-Schnittstelle + Router
internal/transport/{whatsapp,signal,telegram,matrix,slack,discord,sms,imessage,email}/
                              Neun Transport-Adapter
internal/tui/                 Bubble-Tea-Modell
docker/                       Dockerfile, Podman-Quadlet-Unit
docs/                         Roadmap, Gap-Analyse
examples/embed-agent/         Minimales Beispiel für Bibliotheks-Einbettung
```

## Abhängigkeitsrichtung

`agent` hängt nur von Schnittstellen ab, die von `tools` exponiert werden, von seinen eigenen `Provider`-Typen und von der Standardbibliothek. Konkrete Provider, Stores und Transporte hängen von `agent` ab – niemals umgekehrt.

Dies wird per Konvention und durch das CI-Lint-Gate erzwungen. Wenn Sie merken, dass Sie einen konkreten Provider aus `agent` importieren müssen, tun Sie etwas, das die Schichtung nicht sanktioniert; treten Sie einen Schritt zurück.

## Qualitäts-Gate

Jeder Commit muss lokal und in der CI bestehen:

- `go vet ./...`
- `golangci-lint run` (18 Linter, exakte Pins in `.golangci.yml`)
- `go test -race -count=1 -covermode=atomic ./...` auf Linux und macOS
- Coverage-Untergrenze (derzeit 75 % gesamt; Kernpakete liegen bei 85–100 %)
- `govulncheck ./...`
- CodeQL-Statikanalyse (Go)
- Verifikation reproduzierbarer Builds

Führen Sie das Gate lokal mit `make check` aus.

## Nächstes

- [Architektur](/de/developer-guide/architecture/) — die Karte.
- [Mitwirken](/de/developer-guide/contributing/) — der Prozess.
