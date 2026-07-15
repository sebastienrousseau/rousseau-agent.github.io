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
hreflang: "pt-BR"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "pt-BR"
locale: "pt_BR"
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
permalink: "https://docs.rousseau-agent.dev/pt-BR/developer-guide/"
subtitle: "Arquitetura, pontos de extensão, testes, contribuição."
tags: "developer-guide, architecture, extend"
title: "Guia do desenvolvedor"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "developer guide, architecture, add transport, add provider, add tool, testing, contributing"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guia do desenvolvedor"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 60
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guia do desenvolvedor"
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
twitter_title: "Guia do desenvolvedor"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Obrigado a cada operador que executa seu próprio agente de codificação."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Para contribuidores e integradores

O guia do desenvolvedor cobre tudo o que você precisa para modificar o rousseau ou embutir seu loop de agente no seu próprio binário. Se você só quer executar o rousseau, leia o [Guia do usuário](/pt-BR/user-guide/cli/).

## Páginas

| Página | Tópico |
|---|---|
| [Arquitetura](/pt-BR/developer-guide/architecture/) | Arquitetura em camadas: agent, provider, tools, transport, cli. Fronteiras de módulo. |
| [Adicionar um transporte](/pt-BR/developer-guide/add-a-transport/) | Implemente `transport.Transport` e registre-o na CLI. |
| [Adicionar um provider](/pt-BR/developer-guide/add-a-provider/) | Implemente `agent.Provider` (e opcionalmente `agent.StreamingProvider`). |
| [Adicionar uma tool](/pt-BR/developer-guide/add-a-tool/) | Implemente `tools.Tool` e conecte-a no registry. |
| [Testes](/pt-BR/developer-guide/testing/) | Injeção de dependência via interfaces, geradores fake, limiares de cobertura. |
| [Contribuindo](/pt-BR/developer-guide/contributing/) | Checklist de PR, estilo de commit, gate de qualidade. |

## Layout do repositório

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

## Direção das dependências

`agent` depende apenas das interfaces expostas por `tools`, dos seus próprios tipos `Provider` e da biblioteca padrão. Providers, stores e transportes concretos dependem de `agent` — nunca o contrário.

Isso é aplicado por convenção e pelo gate de lint em CI. Se você se pegar precisando importar um provider concreto a partir de `agent`, está fazendo algo que o layering não sanciona; recue.

## Gate de qualidade

Cada commit deve passar, localmente e em CI:

- `go vet ./...`
- `golangci-lint run` (18 linters, pins exatos em `.golangci.yml`)
- `go test -race -count=1 -covermode=atomic ./...` em Linux e macOS
- Piso de cobertura (atualmente 75% no total; pacotes core ficam entre 85–100%)
- `govulncheck ./...`
- Análise estática CodeQL (Go)
- Verificação de builds reprodutíveis

Rode o gate localmente com `make check`.

## Próximo

- [Arquitetura](/pt-BR/developer-guide/architecture/) — o mapa.
- [Contribuindo](/pt-BR/developer-guide/contributing/) — o processo.
