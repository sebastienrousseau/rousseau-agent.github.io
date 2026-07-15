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
hreflang: "es"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "es"
locale: "es_ES"
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
permalink: "https://docs.rousseau-agent.dev/es/developer-guide/"
subtitle: "Arquitectura, puntos de extensión, pruebas, contribuir."
tags: "developer-guide, architecture, extend"
title: "Guía del desarrollador"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "developer guide, architecture, add transport, add provider, add tool, testing, contributing"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guía del desarrollador"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 60
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guía del desarrollador"
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
twitter_title: "Guía del desarrollador"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Gracias a cada operador que ejecuta su propio agente de codificación."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Para colaboradores e integradores

La guía del desarrollador cubre todo lo necesario para modificar rousseau o integrar su bucle de agente en tu propio binario. Si solo quieres ejecutar rousseau, lee la [Guía de usuario](/es/user-guide/cli/) en su lugar.

## Páginas

| Página | Tema |
|---|---|
| [Arquitectura](/es/developer-guide/architecture/) | Arquitectura por capas: agent, provider, tools, transport, cli. Fronteras entre módulos. |
| [Añadir un transporte](/es/developer-guide/add-a-transport/) | Implementa `transport.Transport` y regístralo en el CLI. |
| [Añadir un proveedor](/es/developer-guide/add-a-provider/) | Implementa `agent.Provider` (y opcionalmente `agent.StreamingProvider`). |
| [Añadir una herramienta](/es/developer-guide/add-a-tool/) | Implementa `tools.Tool` y cablealo al registro. |
| [Pruebas](/es/developer-guide/testing/) | Inyección de dependencias vía interfaces, generadores fake, umbrales de cobertura. |
| [Contribuir](/es/developer-guide/contributing/) | Lista de verificación de PR, estilo de commit, gate de calidad. |

## Disposición del repositorio

```
cmd/rousseau/                 Punto de entrada (manejo de señales + Execute)
internal/agent/               Session, Message, Turn, bucle del agente, interfaces Provider, compresión
internal/cli/                 Árbol de comandos Cobra (chat, comandos por transporte, doctor, status, cron, mcp, skills, init, version)
internal/config/              Basado en Viper; precedencia flag > env > archivo > default
internal/cron/                Goroutine planificadora robfig/cron/v3 con almacenamiento durable de jobs
internal/llm/anthropic/       Proveedor directo de la API de Anthropic con marcadores de caché
internal/llm/bedrock/         Proveedor AWS Bedrock
internal/llm/claudecli/       Proveedor de subproceso (CLI claude + parser JSON)
internal/llm/openai/          Proveedor compatible con OpenAI
internal/llm/vertex/          Proveedor Google Vertex AI
internal/mcp/                 Servidor MCP (JSON-RPC 2.0 sobre stdio, spec 2024-11-05)
internal/skills/              Cargador y composición de skills estilo agentskills.io
internal/state/               Interfaz Store + tipo Summary
internal/state/sqlite/        Implementación SQLite (WAL, JIDMap, caché de claude, recall FTS5, tabla cron)
internal/tools/               Interfaz Tool + Registry seguro para concurrencia
internal/tools/builtin/       read, write, edit, grep, bash
internal/transport/           Interfaz Transport + Router
internal/transport/{whatsapp,signal,telegram,matrix,slack,discord,sms,imessage,email}/
                              Nueve adaptadores de transporte
internal/tui/                 Modelo Bubble Tea
docker/                       Dockerfile, unidad Quadlet de Podman
docs/                         Roadmap, análisis de brechas
examples/embed-agent/         Ejemplo mínimo de integración como biblioteca
```

## Dirección de dependencias

`agent` depende solo de interfaces expuestas por `tools`, de sus propios tipos `Provider` y de la biblioteca estándar. Los proveedores, stores y transportes concretos dependen de `agent`, nunca al revés.

Esto se aplica por convención y por el gate de lint de CI. Si te encuentras necesitando importar un proveedor concreto desde `agent`, estás haciendo algo que la estratificación no sanciona; retrocede.

## Gate de calidad

Cada commit debe pasar, localmente y en CI:

- `go vet ./...`
- `golangci-lint run` (18 linters, pines exactos en `.golangci.yml`)
- `go test -race -count=1 -covermode=atomic ./...` en Linux y macOS
- Piso de cobertura (actualmente 75% total; los paquetes centrales están entre 85–100%)
- `govulncheck ./...`
- Análisis estático CodeQL (Go)
- Verificación de build reproducible

Ejecuta el gate localmente con `make check`.

## Siguiente

- [Arquitectura](/es/developer-guide/architecture/): el mapa.
- [Contribuir](/es/developer-guide/contributing/): el proceso.
