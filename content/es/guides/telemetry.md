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
description: "Rousseau-agent ships zero telemetry. No analytics endpoint, no crash-report upload, no license server, no unique identifiers."
keywords: "telemetry, privacy, no phone home, no analytics, no license server"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/guides/telemetry/"
subtitle: "Cero analíticas, cero telemetría. Verificable."
tags: "guides, telemetry, privacy, security"
title: "Guía: telemetría"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "telemetry, privacy, no phone home, no analytics, no license server"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guía: telemetría"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 40
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/telemetry/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/telemetry/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guía: telemetría"
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
twitter_description: "Rousseau-agent ships zero telemetry. No analytics endpoint, no crash-report upload, no license server, no unique identifiers."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guía: telemetría"
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

## El compromiso

Rousseau-agent distribuye cero telemetría. La lista de cosas que rousseau explícitamente **no** hace:

- Sin endpoint de analítica. No hay `metrics.rousseau-agent.dev` ni equivalente.
- Sin envío de reportes de crashes. Los panics van a stderr; nada se sube a ningún lado.
- Sin servidor de licencias. No hay check-in periódico ni verificación de puestos.
- Sin identificador único de instalación. El binario es idéntico byte a byte en cada instalación de la misma etiqueta.
- Sin servicio de feature flags. Cada interruptor en rousseau está en `config.yaml` o en un flag del CLI.
- Sin ping de actualización. `rousseau version` es una consulta local; no hay round trip de "checking for updates".

## Cómo verificar

El binario de rousseau es de código abierto (MIT, consulta `LICENSE`). Cada llamada de red es grep-able:

```sh
grep -rn 'http.Get\|http.Post\|http.Client\|http.NewRequest\|net/http' \
  /path/to/rousseau-agent/internal/ | head
```

Cada coincidencia cae en una de estas categorías:

| Paquete | Propósito |
|---|---|
| `internal/llm/anthropic/` | Llamadas a la API de Anthropic (vía el SDK oficial). |
| `internal/llm/openai/` | Llamadas a endpoints compatibles con OpenAI. |
| `internal/transport/telegram/` | API de Telegram Bot. |
| `internal/transport/matrix/` | API client-server de Matrix. |
| `internal/transport/whatsapp/` | Websockets de Whatsmeow hacia Meta. |
| `internal/transport/slack/`, `discord/` | Socket Mode / Discord Gateway. |
| `internal/transport/imessage/` | Servidor BlueBubbles (en tu LAN). |
| `internal/transport/sms/` | Twilio / Vonage. |
| `internal/transport/email/` | IMAP + SMTP. |

Ninguno es endpoint de analítica. Cada uno es o el proveedor de LLM que configuraste o el transporte que habilitaste.

Ejecuta el daemon bajo `strace -e network` o obsérvalo con `ss -tanp`: los únicos sockets que verás son hacia los endpoints listados arriba.

## El logging estructurado es local

Rousseau usa `log/slog` (`internal/cli/root.go`). Por defecto el handler escribe a stderr, que bajo la unidad Quadlet cae en el journal de systemd. Nada se transmite fuera del host. Si quieres enviar logs a Loki, Datadog u otro lugar, configuras esa canalización tú mismo: consulta [Guías: Observabilidad](/es/guides/observability/).

## Comparación

| Producto | Analítica | Envío de crashes | Servidor de licencias |
|---|---|---|---|
| rousseau-agent | ninguna | ninguno | ninguno |
| Proveedor A (asistente de codificación SaaS típico) | sí | sí | sí |
| Proveedor B (plano de control gestionado) | sí | opt-out | sí |

El modelo operativo de rousseau es: tú traes la clave del LLM, tú hospedas el daemon. No hay pieza de rousseau que se ejecute en servidores controlados por Sebastien.

## Lo que rousseau _sí_ envía a los proveedores de LLM

Por definición, cuando enrutas mensajes a través de Anthropic, Bedrock, Vertex, OpenAI o cualquier otra API, ese proveedor ve el contenido del mensaje. Esto es inherente a cómo funciona la inferencia de LLM: rousseau es un cliente, no un shim.

Dos mitigaciones si te importa el manejo de datos del proveedor:

1. **Ejecuta contra un modelo autohospedado.** Ollama, vLLM, LM Studio o cualquier endpoint compatible con OpenAI. Nada sale de tu máquina. Consulta [Guías: vLLM autohospedado](/es/guides/self-hosted-vllm/).
2. **Usa Bedrock o Vertex en una región con adenda de procesamiento de datos.** Tanto AWS como GCP publican garantías de residencia de datos por región.

## Lo que ve el puente de WhatsApp

El protocolo no oficial de WhatsApp Web implementado por whatsmeow habla con los servidores de Meta: ese tráfico está fuera del control de rousseau. Meta ve tus mensajes de la misma forma que cuando usas WhatsApp Web desde un navegador. Si que Meta vea tus mensajes no es aceptable, no ejecutes el puente de WhatsApp.

El cliente whatsmeow es auditable públicamente: cada paquete está documentado; no hay llamadas de red específicas de rousseau superpuestas.

## Relacionado

- [Seguridad](/es/security/): fronteras de confianza y postura de auditoría.
- [Privacidad](/es/privacy/): la postura de privacidad a nivel del sitio.
- [Proveedores: Compatible con OpenAI](/es/providers/openai-compatible/): inferencia autohospedada.
- [Guías: vLLM autohospedado](/es/guides/self-hosted-vllm/): un ejemplo probado.
