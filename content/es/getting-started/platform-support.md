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
description: "Support matrix for rousseau-agent: operating systems, CPU architectures, container runtimes, provider authentication methods, transport backing libraries."
keywords: "platform support, os matrix, architecture, container runtime, provider auth, linux, macos, windows, arm64, amd64"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/getting-started/platform-support/"
subtitle: "OS, architectures, container runtimes, provider auth methods."
tags: "platform, support, matrix"
title: "Plataformas admitidas"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "platform support, os matrix, architecture, container runtime, provider auth, linux, macos, windows, arm64, amd64"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Plataformas admitidas"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 23
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/platform-support/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/platform-support/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Plataformas admitidas"
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
twitter_description: "Support matrix for rousseau-agent: operating systems, CPU architectures, container runtimes, provider authentication methods, transport backing libraries."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Plataformas admitidas"
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

## Sistemas operativos

| SO | Nivel de soporte | Notas |
|---|---|---|
| Linux (glibc, kernel 5.10+) | Nivel 1 | CI ejecuta `ubuntu-latest` en cada push. Objetivo de despliegue de referencia. |
| Linux (musl / Alpine) | Nivel 1 | La imagen de contenedor está basada en Alpine. |
| macOS 13+ (Ventura o más reciente) | Nivel 1 | CI ejecuta `macos-latest` en cada push. TUI Bubble Tea verificada. |
| Windows 10 / 11 | Nivel 2 | Los binarios se compilan y distribuyen, pero CI no ejecuta la matriz completa de race en Windows. Los transportes de chat funcionan; el despliegue de referencia Podman + Quadlet asume Linux. |
| FreeBSD / OpenBSD | Mejor esfuerzo | Compilación Go puro, pero sin tarea de CI. Se agradecen reportes de la comunidad. |

## Arquitecturas de CPU

| Arquitectura | Nivel de soporte | Nomenclatura de release |
|---|---|---|
| `amd64` (x86-64) | Nivel 1 | `_linux_amd64`, `_darwin_amd64`, `_windows_amd64` |
| `arm64` (aarch64) | Nivel 1 | `_linux_arm64`, `_darwin_arm64` (Apple Silicon) |
| `armv7` (ARM 32 bits) | Mejor esfuerzo | Compilable con `GOARCH=arm GOARM=7`; no se publica. |
| `riscv64` | Mejor esfuerzo | Compilable con `GOARCH=riscv64`; no se publica. |

`CGO_ENABLED=0` en cada objetivo: `modernc.org/sqlite` es Go puro, por lo que la compilación cruzada no tiene fricción.

## Runtimes de contenedor

| Runtime | Nivel de soporte | Notas |
|---|---|---|
| Podman 4.4+ (rootless) | Nivel 1 | Despliegue de referencia. Usa unidades Quadlet de systemd para endurecimiento declarativo. |
| Docker 24+ | Nivel 1 | El Dockerfile funciona sin cambios. El endurecimiento en tiempo de ejecución es tu responsabilidad (no hay equivalente a Quadlet). |
| containerd + `nerdctl` | Nivel 2 | Misma imagen; nerdctl consume el mismo artefacto OCI. |
| Kubernetes 1.27+ | Nivel 2 | Consulta [Guías: Despliegue en Kubernetes](/es/guides/kubernetes-deployment/). |

## Métodos de autenticación de proveedores

| Proveedor | Mecanismo de autenticación | Claves de configuración |
|---|---|---|
| `claudecli` (predeterminado) | Hereda los tokens OAuth de Claude Code desde `~/.claude/`. Sin clave en la configuración de rousseau. | `claudecli.binary`, `claudecli.permission_mode` |
| `anthropic` | Clave de API directa. | Variable de entorno `ANTHROPIC_API_KEY`, o `anthropic.api_key` |
| `openai` | Clave de API de OpenAI o token de terceros. | `OPENAI_API_KEY`, o `openai.api_key` |
| `openrouter` | Clave de API de OpenRouter. Usa el esquema OpenAI con `openrouter.base_url` preconfigurado. | `openrouter.api_key` |
| `ollama` | Endpoint local, no requiere clave (`ollama.api_key` por defecto es `not-required`). | `ollama.base_url` preconfigurado en `http://localhost:11434/v1` |
| `bedrock` | Cadena estándar de credenciales AWS (variables de entorno, `~/.aws/credentials`, IMDS, rol IAM). | `bedrock.region`, `bedrock.profile`, `bedrock.model` |
| `vertex` | JSON de cuenta de servicio de GCP, o Application Default Credentials. | `vertex.project`, `vertex.region`, `vertex.credentials_file` |

## Bibliotecas subyacentes de los transportes

Cada transporte es un adaptador ligero sobre un cliente upstream. El soporte está limitado por la viabilidad del proyecto upstream.

| Transporte | Upstream | Protocolo |
|---|---|---|
| WhatsApp | `go.mau.fi/whatsmeow` | Protocolo no oficial de WhatsApp Web (compatible con Signal). |
| Signal | Subproceso `signal-cli` | JSON-RPC de Signal. |
| Telegram | Cliente directo de Bot API | Long polling. |
| Matrix | Cliente directo de API client-server | Polling HTTPS. |
| Slack | Cliente directo de Socket Mode | WebSocket saliente. |
| Discord | Cliente directo de Gateway | WebSocket saliente + intents. |
| iMessage | Cliente HTTP de BlueBubbles | Polling de BlueBubbles. Requiere un host macOS ejecutando BlueBubbles Server. |
| Email | Cliente estándar `net/smtp` + IMAP | IMAP + SMTP sobre TLS. |
| SMS | REST directo de Twilio / Vonage | Solo saliente. |

## Dependencias opcionales de tiempo de ejecución

| Dependencia | Requerida para | Versión |
|---|---|---|
| CLI `claude` | `provider: claudecli` (predeterminado). | Última. |
| `signal-cli` | Transporte Signal. | 0.13+. Requiere una JVM. |
| BlueBubbles Server | Transporte iMessage. | 1.9+. Se ejecuta en un host macOS. |
| CLI `whisper.cpp` | Transcripción de notas de voz de WhatsApp (`whatsapp.voice.enabled: true`). | 1.5+. No se incluye en la imagen del contenedor. |
| `podman` | Despliegue de referencia. | 4.4+ para soporte de Quadlet. |
| `systemd` (sesión de usuario) | Despliegue de referencia. | 249+ para Quadlet. |

## Compilador y cadena de herramientas

| Componente | Versión | Notas |
|---|---|---|
| Go | 1.26+ | `go.mod` fija exactamente el grafo del módulo. |
| golangci-lint | v2 | 18 linters, pines exactos en `.golangci.yml`. |
| govulncheck | Última | Se ejecuta en cada build de CI. |
| cosign | 2.2+ | Solo para verificar releases firmados. |

## Siguiente

- [Instalación](/es/getting-started/installation/): instalación acorde a tu plataforma.
- [Actualización](/es/getting-started/updating/): moverse entre versiones de forma segura.
