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
date: "July 13, 2026"
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
description: "Off-by-default rousseau-agent behaviour: voice mode via whisper.cpp, FTS5 recall, LLM compression, and other opt-in surface."
keywords: "experimental, voice, whisper, fts5, compression, opt-in, feature flag"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/experimental/"
subtitle: "Comportamiento desactivado por defecto y por qué."
tags: "experimental, opt-in, voice, compression, fts5"
title: "Experimental"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "experimental, voice, whisper, fts5, compression, opt-in, feature flag"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Experimental"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "system"
order: 60
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/experimental/index.html"
item_link: "https://docs.rousseau-agent.dev/experimental/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Experimental"
last_build_date: "Mon, 13 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
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
twitter_description: "Off-by-default rousseau-agent behaviour: voice mode via whisper.cpp, FTS5 recall, LLM compression, and other opt-in surface."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Experimental"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Gracias a cada operador que ejecuta su propio agente de codificación."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Qué significa "experimental" aquí

La postura por defecto de rousseau es minimalista: un binario Go estático, un archivo SQLite, sin dependencias externas. Cualquier característica que requiera un runtime adicional (`whisper.cpp`), estado adicional (índice FTS5 para recall) o costo adicional del proveedor (compresión respaldada por LLM) es opt-in.

Ninguna de estas es inestable. Se distribuyen, tienen pruebas, están soportadas. Pero como cambian el costo o la superficie operativa, están desactivadas por defecto: activas las que necesitas.

## Modo voz (whisper.cpp)

Desactivado por defecto porque requiere que el binario `whisper` de whisper.cpp esté instalado en el host del daemon.

**Toggle:** `whatsapp.voice.enabled: true` en `config.yaml`. Consulta `VoiceConfig` en `internal/config/config.go`.

**Qué hace.** Cuando WhatsApp entrega una nota de voz, el cliente whatsmeow descarga el payload OGG, invoca a `whisper` con el modelo configurado y trata la transcripción como el texto del mensaje entrante. Eventos de log estructurado (`internal/transport/whatsapp/dispatch.go`):

- `whatsapp.audio_downloaded size=N`
- `whatsapp.transcribed elapsed=N`

**Por qué está desactivado.** Dos razones: (1) una instalación nueva fallaría de forma confusa cuando el binario `whisper` esté ausente, (2) la transcripción es un gasto de CPU en tiempo real por el que la mayoría de operadores preferirían optar en lugar de encontrarlo por sorpresa.

Consulta [Guía de usuario: Modo voz](/es/user-guide/voice-mode/) para la configuración completa.

## Recall FTS5

**Toggle.** Activado por defecto, pero solo lo usan las herramientas que lo piden. El índice FTS5 se construye y mantiene igualmente (`EnsureSearch` en `internal/state/sqlite/search.go`); el "opt-in" es si el agente le pide al modelo que lo busque.

**Qué hace.** Índice full-text de SQLite FTS5 sobre cada sesión almacenada. Se alimenta a través de `rousseau session search`, la herramienta MCP `rousseau_search_sessions` y (cuando el agente está configurado con un buscador de recall) el modelo puede consultarlo a mitad de turno.

**Por qué está estructurado así.** El índice es barato de mantener (los triggers en `internal/state/sqlite/search.go` se encargan) pero exponerlo al modelo en cada turno tiene un costo. Se cablea solo cuando el bucle del agente se construye con un `RecallSearcher` (`internal/state/sqlite/recall.go`).

Consulta [Guía de usuario: Compresión + Recall](/es/user-guide/compression-recall/).

## Compresión respaldada por LLM

Desactivada por defecto porque cuesta tokens.

**Toggle:** `agent.compression.enabled: true`. Lista completa de campos en la [Guía: Gestión de contexto](/es/guides/context-management/).

**Qué hace.** Cuando una sesión crece más allá de `trigger_messages` (60 por defecto), el `LLMCompressor` (`internal/agent/compressor.go`) resume el slice más antiguo en un mensaje de usuario sintético, preservando los `keep_recent` mensajes más recientes textualmente. Cada turno posterior es más pequeño y barato.

**Por qué está desactivado.** El despliegue de referencia ejecuta `claudecli` en un nivel de suscripción donde no se factura el conteo de tokens. La compresión se paga a sí misma en Anthropic direct, Bedrock, Vertex y proveedores compatibles con OpenAI.

## URLs base de OpenRouter y Ollama (preconfiguradas, aún opt-in)

No estrictamente experimental, pero vale la pena nombrarlo: `setDefaults` de rousseau en `internal/config/config.go` preconfigura las URLs base de OpenRouter y Ollama:

- `openrouter.base_url: https://openrouter.ai/api/v1`
- `ollama.base_url: http://localhost:11434/v1`
- `ollama.api_key: not-required`

Seleccionar estos proveedores es opt-in vía `provider: openrouter` / `provider: ollama`: los endpoints simplemente están pre-rellenados para que no tengas que recordarlos.

## Detección de inyección de prompts (roadmap)

No se distribuye. Consulta [Guías: Inyección de prompts](/es/guides/prompt-injection/) para el modelo de amenazas honesto. La mitigación hoy es enteramente basada en el aprobador; la detección basada en clasificadores es un ítem del roadmap pendiente de investigación que realmente funcione.

## Streaming a proveedores no-Anthropic (parcial)

El proveedor Anthropic (`internal/llm/anthropic/client.go`) admite la interfaz de streaming del SDK. Otros adaptadores actualmente se ejecutan en modo no-streaming. Streaming en todos los adaptadores es una pasada de uniformidad planeada.

## Relacionado

- [Configuración](/es/configuration/): cada perilla de configuración.
- [Guía de usuario: Modo voz](/es/user-guide/voice-mode/).
- [Guías: Gestión de contexto](/es/guides/context-management/): profundización en compresión.
- [Referencia: Almacén de sesiones](/es/reference/session-store/): esquema FTS5.
