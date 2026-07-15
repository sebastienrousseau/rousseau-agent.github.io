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
description: "Agente de codificación autoalojado con 9 transportes de chat, 5 proveedores LLM, servidor MCP, procedencia SLSA-3, versiones firmadas con cosign."
keywords: "rousseau-agent, coding agent, self-hosted, container-native, MCP, SLSA-3, cosign, SBOM, LLM, WhatsApp, Signal, Slack"
layout: "index"
permalink: "https://docs.rousseau-agent.dev/es/"
subtitle: "Agente de codificación autoalojado, nativo de contenedores, nativo de MCP."
tags: "overview, self-hosted, mcp, security"
title: "rousseau-agent"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "rousseau-agent, coding agent, self-hosted, container-native, MCP, SLSA-3, cosign, SBOM, LLM, WhatsApp, Signal, Slack"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "rousseau-agent"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "welcome"
order: 1
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/index.html"
item_link: "https://docs.rousseau-agent.dev/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "rousseau-agent"
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
twitter_description: "Agente de codificación autoalojado con 9 transportes de chat, 5 proveedores LLM, servidor MCP, procedencia SLSA-3, versiones firmadas con cosign."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "rousseau-agent"
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

## Agente de codificación autoalojado, nativo de contenedores, nativo de MCP

**rousseau-agent** es un asistente de codificación en Go que se ejecuta donde se ejecuta tu código. El demonio, el material de autenticación y el tráfico al modelo permanecen en hardware controlado por el operador. **9 transportes · 5 proveedores LLM · SLSA-3 · cosign · SBOM.**

```sh
rousseau chat
```

Este único comando lanza una TUI Bubble Tea respaldada por el proveedor LLM que hayas configurado. Nada cruza el perímetro de tu red excepto la propia llamada al proveedor.

## Tres pilares

### Endurecido para empresa

- Procedencia de build **SLSA nivel 3** mediante `slsa-framework/slsa-github-generator`.
- Firmas **cosign** sin claves sobre cada archivo de checksums, verificables contra el registro de transparencia de Sigstore.
- SBOM **CycloneDX** en JSON adjunto a cada versión.
- **Builds reproducibles** verificados en CI sobre un checkout limpio.
- Podman sin root con `ReadOnly=true`, `DropCapability=all`, `NoNewPrivileges=true`, filtro seccomp por defecto, UID 1000 sin privilegios, mapeo de espacio de nombres `keep-id`.
- Puerta de 18 linters `golangci-lint` v2, CodeQL (Go), `govulncheck` en cada ejecución de CI, Dependabot para `gomod` y `github-actions`.

### Alcance multi-modal

Nueve transportes de chat detrás de un único demonio:

- [WhatsApp](/es/transports/whatsapp/) (`go.mau.fi/whatsmeow`, compatible con el protocolo Signal)
- [Signal](/es/transports/signal/) (subproceso `signal-cli` JSON-RPC)
- [Telegram](/es/transports/telegram/) (long-polling de la API Bot)
- [Matrix](/es/transports/matrix/) (API cliente-servidor)
- [Slack](/es/transports/slack/) (Socket Mode, sin superficie HTTP pública)
- [Discord](/es/transports/discord/) (Gateway v10)
- [iMessage](/es/transports/imessage/) (polling HTTP de BlueBubbles)
- [Email](/es/transports/email/) (IMAP + SMTP)
- [SMS](/es/transports/sms/) (Twilio o Vonage, solo envío)

### Agnóstico al modelo

Cinco familias de proveedores LLM, una única interfaz `agent.Provider`:

- [claudecli](/es/providers/claudecli/) — subproceso sobre tu CLI local `claude`, hereda su autenticación.
- [Anthropic](/es/providers/anthropic/) — API directa con marcadores efímeros de caché de prompt.
- [AWS Bedrock](/es/providers/bedrock/) — cadena estándar de credenciales de AWS.
- [Google Vertex AI](/es/providers/vertex/) — JSON de cuenta de servicio o ADC.
- [Compatible con OpenAI](/es/providers/openai-compatible/) — OpenAI, OpenRouter, Ollama, vLLM, LM Studio.

## Siguientes pasos

- [Primeros pasos](/es/getting-started/) — instalar, primera ejecución, primer transporte.
- [Configuración](/es/configuration/) — cada campo de `internal/config/config.go`.
- [Despliegue](/es/deployment/) — Podman sin root + Quadlet, nota sobre Kubernetes.
- [Seguridad](/es/security/) — postura de cadena de suministro, modelo de confianza, receta de cosign.
- [Conceptos](/es/concepts/) — bucle del agente, almacén de sesiones, MCP, cron, habilidades.
