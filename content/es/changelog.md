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
changefreq: "weekly"
description: "Chronological release notes for rousseau-agent. First public snapshot: 9 transports, 5 providers, MCP server, SLSA-3, 76% coverage."
keywords: "changelog, release notes, versions, snapshot"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/changelog/"
subtitle: "Notas de versión cronológicas para rousseau-agent."
tags: "changelog, reference"
title: "Registro de cambios"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "changelog, release notes, versions, snapshot"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Registro de cambios"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 28
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/changelog/index.html"
item_link: "https://docs.rousseau-agent.dev/changelog/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Registro de cambios"
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
twitter_title: "Registro de cambios"
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

## Estado actual — julio 2026

Primera instantánea pública. Aspectos destacados de lo que se distribuye hoy:

- **Nueve transportes de chat.** WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, Email, SMS.
- **Cinco proveedores de LLM.** claudecli, Anthropic direct, AWS Bedrock, Google Vertex AI, compatible con OpenAI.
- **Servidor MCP.** JSON-RPC 2.0 sobre stdio, revisión de la spec 2024-11-05.
- **SLSA Nivel 3** de procedencia de build, checksums de release firmados con cosign, SBOM CycloneDX.
- **76% de cobertura de pruebas** en el módulo (los paquetes centrales están entre 85–100%).
- **Cero alertas abiertas de Dependabot.**
- **CI completa en modo race** en `ubuntu-latest` y `macos-latest`.

## Detalle

Para el historial completo commit por commit, consulta el git log en https://github.com/sebastienrousseau/rousseau-agent.

Cada commit usa [Conventional Commits](https://www.conventionalcommits.org/). La página de registro de cambios tendrá entradas estructuradas una vez que se corte la primera release etiquetada; hasta entonces, `git log --oneline` es la referencia autoritativa.

## Política de compatibilidad

- **El formato del archivo de configuración** se versiona por adiciones de campos, no por rupturas de esquema. Las nuevas claves son seguras de ignorar; los renombrados y eliminaciones se harán detrás de una advertencia de deprecación en la release previa a la eliminación.
- **`agent.Provider`, `agent.Message`, `agent.Session`** son exportaciones estables destinadas a integradores de terceros. Los cambios disruptivos aterrizarán en un bump de versión mayor.
- **Los paquetes `internal/*`** no son API estable: son internos del proyecto. Los consumidores externos no deberían importarlos (la visibilidad `internal` de Go lo aplica).

## Dónde reportar comentarios

- Bugs y solicitudes de características: issues de GitHub.
- Seguridad: `sebastian.rousseau@gmail.com` (consulta [/security/](/es/security/)).
