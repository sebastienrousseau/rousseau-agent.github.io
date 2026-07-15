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
description: "rousseau-agent is self-hosted. No telemetry endpoint, no SaaS control plane. LLM providers have their own retention policies; everything else stays in the operator's infrastructure."
keywords: "privacy, telemetry, self-hosted, data handling, retention, LLM providers"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/privacy/"
subtitle: "Autoalojado significa autocontrolado — nada sale de tu infraestructura salvo la llamada al LLM."
tags: "privacy, legal, self-hosted"
title: "Privacidad"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "privacy, telemetry, self-hosted, data handling, retention, LLM providers"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Privacidad"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "legal"
order: 30
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/privacy/index.html"
item_link: "https://docs.rousseau-agent.dev/privacy/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Privacidad"
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
twitter_description: "rousseau-agent is self-hosted. No telemetry endpoint, no SaaS control plane. LLM providers have their own retention policies; everything else stays in the operator's infrastructure."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Privacidad"
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

## Manejo de datos

`rousseau-agent` es autohospedado. Cuando el operador ejecuta el daemon en su propia infraestructura, **ningún dato sale de esa infraestructura excepto la llamada al LLM en sí**.

No hay:

- **Ningún endpoint de telemetría.** rousseau no hace llamadas a `rousseau-agent.dev` ni a ningún otro servidor controlado por el autor en tiempo de ejecución.
- **Ningún plano de control SaaS.** No hay servidor de licencias, ni panel en la nube, ni phone-home.
- **Ninguna analítica de uso.** El daemon no reporta qué herramientas se invocaron, cuántos turnos se ejecutaron o qué modelos se llamaron.
- **Ningún reporte de crashes.** Los crashes se muestran en los logs locales (`journalctl --user -u rousseau-agent.service`). No se envían stack traces a ningún lado.

## Dónde viven los datos de sesión

| Datos | Ubicación | Cifrado en reposo |
|---|---|---|
| Sesiones (historial de mensajes) | `~/.local/share/rousseau/sessions.db` | Solo a nivel de sistema de archivos (LUKS / FileVault si el operador lo configuró). |
| Trabajos cron | Misma base de datos SQLite | Igual. |
| Emparejamiento de dispositivo de WhatsApp | `~/.local/share/rousseau/whatsapp.db` | Igual. |
| Salida de log | Journal de systemd (típicamente `~/.local/state/`) | Igual. |
| Archivo de configuración | `~/.config/rousseau/config.yaml` | Igual. |
| Tokens OAuth del CLI `claude` | `~/.claude/` | Igual. |

Ninguno de estos es transmitido a ningún lado por el daemon.

## Proveedores de LLM

El proveedor de LLM es el único punto de contacto externo. Cada proveedor tiene su propia política de manejo de datos y retención, ninguna de las cuales rousseau controla:

| Proveedor | Política de retención |
|---|---|
| [claudecli](/es/providers/claudecli/) | Lo que el CLI local `claude` esté configurado para enviar. Típicamente la retención estándar de Anthropic. |
| [Anthropic direct](/es/providers/anthropic/) | Consulta https://www.anthropic.com/legal/aup |
| [AWS Bedrock](/es/providers/bedrock/) | Definida por contrato; típicamente sin retención a largo plazo del tráfico de inferencia en Bedrock. |
| [Google Vertex AI](/es/providers/vertex/) | Definida por contrato; típicamente sin retención a largo plazo de la inferencia de Vertex. |
| [Compatible con OpenAI](/es/providers/openai-compatible/) | Depende del endpoint. Ollama y vLLM autohospedado no retienen nada externo; OpenAI y OpenRouter tienen sus propias políticas. |

Elige el proveedor cuya política de retención coincida con tus requisitos operativos. Para la postura más estricta, ejecuta contra un Ollama, vLLM o LM Studio autohospedado: ningún dato sale de tu infraestructura.

## Datos del lado del transporte

Los transportes de chat envían mensajes a través de los servidores del proveedor (WhatsApp, Signal, Slack, Discord, etc.). Cada uno tiene su propia postura de manejo de datos. rousseau no añade una capa por encima: el proveedor ve lo que el protocolo subyacente le muestra, lo cual es específico del protocolo:

- Signal y WhatsApp: cifrado de extremo a extremo; el proveedor ve metadatos pero no contenido de mensajes.
- Slack, Discord: no cifrados de extremo a extremo; el proveedor ve el contenido del mensaje.
- Matrix: cifrado de extremo a extremo cuando la sala tiene E2E habilitado; del lado del servidor en caso contrario.
- Email: no cifrado de extremo a extremo salvo que le pongas PGP o S/MIME por encima (rousseau no lo hace).
- iMessage: cifrado de extremo a extremo; BlueBubbles se sitúa entre rousseau y Apple.

## Eliminar una sesión

Las sesiones son filas en una base de datos SQLite. Elimina con:

```sh
rousseau session delete <session-id>
```

O descarta toda la base de datos:

```sh
rm ~/.local/share/rousseau/sessions.db
```

El siguiente arranque recreará una vacía. Esto también purga el índice de recall cross-session de FTS5.

## Dependencias de terceros

`go.mod` lista cada dependencia. Ninguna de ellas está configurada para hacer phone-home. Las dependencias de tiempo de build (linters, analizadores estáticos) se ejecutan solo en CI. Las dependencias de tiempo de ejecución se enumeran en el SBOM CycloneDX adjunto a cada release.
