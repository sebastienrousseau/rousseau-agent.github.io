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
description: "Compact reference table of every rousseau-agent command mirroring the output of rousseau --help."
keywords: "cli, commands, reference, table, rousseau --help"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/reference/cli-commands/"
subtitle: "Every command tabulated."
tags: "reference, cli, commands"
title: "Comandos CLI"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cli, commands, reference, table, rousseau --help"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Comandos CLI"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 50
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/cli-commands/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/cli-commands/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Comandos CLI"
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
twitter_description: "Compact reference table of every rousseau-agent command mirroring the output of rousseau --help."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Comandos CLI"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Qué aprenderás</span><p>La superficie completa del CLI <code>rousseau</code>: cada comando, sus flags, la semántica de códigos de salida y las claves de configuración que cada flag sobrescribe. Esta es la referencia escaneable: consulta <a href="/es/user-guide/cli/">Guía de usuario: CLI</a> para un recorrido con ejemplos probados.</p></aside>

## Árbol de comandos

Cada comando expone su ayuda vía `rousseau <cmd> --help`. Esta página es el resumen tabulado.

| Comando | Descripción |
|---|---|
| `chat` | Abre la TUI interactiva de Bubble Tea. |
| `whatsapp` | Ejecuta el puente de WhatsApp (whatsmeow). |
| `signal` | Ejecuta el puente de Signal (JSON-RPC de signal-cli). |
| `telegram` | Ejecuta el long-poller de la API de Telegram Bot. |
| `matrix` | Ejecuta el puente client-server de Matrix. |
| `slack` | Ejecuta el puente Socket Mode de Slack. |
| `discord` | Ejecuta el puente Gateway de Discord. |
| `sms` | SMS de solo envío vía Twilio o Vonage. |
| `imessage` | Puente de iMessage respaldado por BlueBubbles. |
| `email` | Puente IMAP entrante + SMTP saliente. |
| `mcp` | Inicia el servidor MCP JSON-RPC 2.0 sobre stdio. |
| `cron add` | Añade un prompt programado. |
| `cron list` | Lista cada trabajo programado. |
| `cron remove` | Elimina un trabajo programado. |
| `cron enable` | Habilita un trabajo programado deshabilitado. |
| `cron disable` | Deshabilita un trabajo programado habilitado. |
| `session list` | Lista sesiones del almacén, las más recientes primero. |
| `session search` | Búsqueda FTS5 sobre el contenido de mensajes de todas las sesiones. |
| `session show` | Imprime el historial de mensajes de una sesión. |
| `session delete` | Elimina una sesión. |
| `skills list` | Lista skills descubiertos desde `skills_dir`. |
| `skills show` | Imprime el front-matter YAML y cuerpo de un skill. |
| `skills lint` | Valida los skills por conformidad de esquema. |
| `doctor` | Diagnostica la instalación local. Imprime un informe. |
| `status` | Imprime el estado del daemon. |
| `init` | Escribe una configuración por defecto en `~/.config/rousseau/`. |
| `version` | Imprime la versión, commit y fecha de build. |

## Flags globales

Cada comando acepta estos:

| Flag | Tipo | Clave de configuración | Notas |
|---|---|---|---|
| `--config` | string | — | Carga la configuración desde este archivo. Por defecto: `$XDG_CONFIG_HOME/rousseau/config.yaml`. |
| `--help`, `-h` | bool | — | Imprime la ayuda del comando actual. |

## Flags por transporte

### `rousseau whatsapp`

| Flag | Tipo | Clave de configuración | Notas |
|---|---|---|---|
| `--store` | string | — | Ruta al almacén de dispositivos de whatsmeow. Por defecto `$XDG_DATA_HOME/rousseau/whatsapp.db`. |
| `--allow` | []string | `whatsapp.allowlist` | Restringe la entrada a estos JIDs. Repetible. |

### `rousseau slack`

| Flag | Tipo | Clave de configuración |
|---|---|---|
| `--app-token` | string | `slack.app_token` |
| `--bot-token` | string | `slack.bot_token` |
| `--bot-user-id` | string | `slack.bot_user_id` |
| `--allow` | []string | `slack.allowlist` |

### `rousseau discord`

| Flag | Tipo | Clave de configuración |
|---|---|---|
| `--token` | string | `discord.token` |
| `--allow` | []string | `discord.allowlist` |

### `rousseau telegram`

| Flag | Tipo | Clave de configuración |
|---|---|---|
| `--token` | string | `telegram.token` |
| `--allow` | []string | `telegram.allowlist` |

### `rousseau matrix`

| Flag | Tipo | Clave de configuración |
|---|---|---|
| `--homeserver-url` | string | `matrix.homeserver_url` |
| `--access-token` | string | `matrix.access_token` |
| `--user-id` | string | `matrix.user_id` |
| `--allow` | []string | `matrix.allowlist` |

### `rousseau signal`

| Flag | Tipo | Clave de configuración |
|---|---|---|
| `--account` | string | `signal.account` |
| `--binary` | string | `signal.binary` |
| `--allow` | []string | `signal.allowlist` |

### `rousseau email`

| Flag | Tipo | Clave de configuración |
|---|---|---|
| `--imap-addr` | string | `email.imap_addr` |
| `--imap-username` | string | `email.imap_username` |
| `--imap-password` | string | `email.imap_password` |
| `--smtp-addr` | string | `email.smtp_addr` |
| `--smtp-username` | string | `email.smtp_username` |
| `--smtp-password` | string | `email.smtp_password` |
| `--from` | string | `email.from` |
| `--mailbox` | string | `email.mailbox` |
| `--poll-interval` | string | `email.poll_interval` |

### `rousseau sms`

| Flag | Tipo | Clave de configuración |
|---|---|---|
| `--provider` | string | `sms.provider` |
| `--from` | string | `sms.from` |
| `--to` | string | (posicional) |

### `rousseau imessage`

| Flag | Tipo | Clave de configuración |
|---|---|---|
| `--base-url` | string | `imessage.base_url` |
| `--password` | string | `imessage.password` |
| `--chat-guid` | string | `imessage.chat_guid` |

## Códigos de salida

| Código | Significado |
|---|---|
| 0 | Salida limpia: el comando se completó. No es típico para daemons de larga duración (usualmente terminan por señal). |
| 1 | Cualquier error expuesto desde `Execute`. Consulta [Referencia: Códigos de salida](/es/reference/exit-codes/) para la clasificación. |

## Precedencia

Los valores de configuración se resuelven en el orden **flag &gt; env &gt; archivo &gt; default** (consulta `config.Load` en `internal/config/config.go`). Las variables de entorno tienen el prefijo `ROUSSEAU_` con puntos reemplazados por guiones bajos, p. ej. `ROUSSEAU_ANTHROPIC_MODEL` sobrescribe `anthropic.model`. La variable de entorno pelada `ANTHROPIC_API_KEY` también se respeta (caso especial en `config.Load`).

## Solución de problemas

### `unknown flag: --allow` en `rousseau chat`

`--allow` es específico de transporte. `chat` no tiene allowlist porque no hay ingreso. Usa `rousseau whatsapp --allow …` en su lugar.

### El orden de los flags importa para flags repetibles

`--allow A --allow B` son dos valores, pero `--allow=A,B` es un valor que contiene una coma. Prefiere flags separados.

### La sobrescritura por env no se detecta

Rousseau lee el entorno solo al arrancar. Reinicia el daemon tras cambiar variables de entorno, o usa `--config` para forzar una recarga.

### `flag provided but not defined`

Cobra rechaza flags desconocidos. Si copias un flag de una versión más nueva, comprueba `rousseau <cmd> --help` para la escritura actual.

## Páginas relacionadas

- [Guía de usuario: CLI](/es/user-guide/cli/): cada comando con ejemplos probados.
- [Referencia: Códigos de salida](/es/reference/exit-codes/): semántica de señales.
- [Referencia: Esquema de configuración](/es/reference/config-schema/): cada campo de configuración.
- [Referencia: Variables de entorno](/es/reference/environment-variables/): matriz de sobrescritura por env.
- [Configuración](/es/configuration/): recorrido completo del archivo de configuración.

## Lecturas adicionales

- `internal/cli/root.go`: árbol de comandos de Cobra.
- `internal/cli/*.go`: un archivo por subcomando.
- `internal/config/config.go`: `Load` y resolución de defaults.
