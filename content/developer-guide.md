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
changefreq: "monthly"
description: "Landing page for the rousseau-agent developer guide: architecture, how to add a transport, provider, or tool, testing pattern, contributing."
keywords: "developer guide, architecture, add transport, add provider, add tool, testing, contributing"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/developer-guide/"
subtitle: "Architecture, extension points, testing, contributing."
tags: "developer-guide, architecture, extend"
title: "Developer Guide"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "developer guide, architecture, add transport, add provider, add tool, testing, contributing"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Developer Guide"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 60
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Developer Guide"
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
twitter_title: "Developer Guide"
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

## For contributors and integrators

The developer guide covers everything you need to modify rousseau or embed its agent loop in your own binary. If you only want to run rousseau, read the [User Guide](/user-guide/cli/) instead.

## Pages

| Page | Topic |
|---|---|
| [Architecture](/developer-guide/architecture/) | Layered architecture: agent, provider, tools, transport, cli. Module boundaries. |
| [Add a transport](/developer-guide/add-a-transport/) | Implement `transport.Transport` and register it in the CLI. |
| [Add a provider](/developer-guide/add-a-provider/) | Implement `agent.Provider` (and optionally `agent.StreamingProvider`). |
| [Add a tool](/developer-guide/add-a-tool/) | Implement `tools.Tool` and wire it into the registry. |
| [Testing](/developer-guide/testing/) | Dependency injection via interfaces, fake generators, coverage thresholds. |
| [Contributing](/developer-guide/contributing/) | PR checklist, commit style, quality gate. |

## Repository layout

```
cmd/rousseau/                 Entry point (signal handling + Execute)
internal/agent/               Session, Message, Turn, agent loop, Provider interfaces, compression
internal/cli/                 Cobra command tree (chat, per-transport commands, doctor, status, cron, mcp, skills, init, version)
internal/config/              Viper-based; flag > env > file > default precedence
internal/cron/                robfig/cron/v3 scheduler goroutine with durable job storage
internal/llm/anthropic/       Direct Anthropic API provider with cache markers
internal/llm/bedrock/         AWS Bedrock provider
internal/llm/claudecli/       Subprocess provider (claude CLI + JSON parser)
internal/llm/openai/          OpenAI-compatible provider
internal/llm/vertex/          Google Vertex AI provider
internal/mcp/                 MCP server (JSON-RPC 2.0 over stdio, spec 2024-11-05)
internal/skills/              agentskills.io-style skill loader + composition
internal/state/               Store interface + Summary type
internal/state/sqlite/        SQLite implementation (WAL, JIDMap, claude cache, FTS5 recall, cron table)
internal/tools/               Tool interface + concurrency-safe Registry
internal/tools/builtin/       read, write, edit, grep, bash
internal/transport/           Transport interface + Router
internal/transport/{whatsapp,signal,telegram,matrix,slack,discord,sms,imessage,email}/
                              Nine transport adapters
internal/tui/                 Bubble Tea model
docker/                       Dockerfile, Podman Quadlet unit
docs/                         Roadmap, gap analysis
examples/embed-agent/         Minimal library-embedding example
```

## Dependency direction

`agent` depends only on interfaces exposed by `tools`, on its own `Provider` types, and on the standard library. Concrete providers, stores, and transports depend on `agent` — never the reverse.

This is enforced by convention and by the CI lint gate. If you find yourself needing to import a concrete provider from `agent`, you are doing something the layering does not sanction; step back.

## Quality gate

Every commit must pass, locally and in CI:

- `go vet ./...`
- `golangci-lint run` (18 linters, exact pins in `.golangci.yml`)
- `go test -race -count=1 -covermode=atomic ./...` on Linux and macOS
- Coverage floor (currently 75% total; core packages sit 85–100%)
- `govulncheck ./...`
- CodeQL static analysis (Go)
- Reproducible-build verification

Run the gate locally with `make check`.

## Next

- [Architecture](/developer-guide/architecture/) — the map.
- [Contributing](/developer-guide/contributing/) — the process.
