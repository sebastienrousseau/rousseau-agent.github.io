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
description: "Full CLI reference for rousseau-agent: every command, every flag, exit codes, per-transport subcommands."
keywords: "cli, cobra, commands, flags, subcommands, exit codes"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/user-guide/cli/"
subtitle: "Every command, every flag."
tags: "cli, reference, commands"
title: "Referencia CLI"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cli, cobra, commands, flags, subcommands, exit codes"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Referencia CLI"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 40
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/cli/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/cli/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Referencia CLI"
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
twitter_description: "Full CLI reference for rousseau-agent: every command, every flag, exit codes, per-transport subcommands."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Referencia CLI"
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

## Invocación

```
rousseau [--config <path>] <command> [flags]
```

Cada comando lee los valores por defecto desde `~/.config/rousseau/config.yaml` (o el archivo pasado vía `--config`). Los flags tienen prioridad sobre las variables de entorno, estas sobre el archivo y el archivo sobre los valores por defecto embebidos.

## Flags globales

| Flag | Tipo | Por defecto | Notas |
|---|---|---|---|
| `--config` | string | `$XDG_CONFIG_HOME/rousseau/config.yaml` | Carga la configuración desde este archivo. Si se omite, se usa la ruta XDG por defecto. |
| `--help`, `-h` | bool | — | Imprime la ayuda del comando actual. |

## Árbol de comandos

```
rousseau
├── chat                Bubble Tea TUI
├── whatsapp            WhatsApp bridge (whatsmeow)
├── signal              Signal bridge (signal-cli JSON-RPC)
├── telegram            Telegram Bot API long-polling
├── matrix              Matrix client-server API
├── slack               Slack Socket Mode
├── discord             Discord Gateway
├── sms                 SMS send-only (Twilio / Vonage)
├── imessage            BlueBubbles-backed iMessage bridge
├── email               IMAP inbound + SMTP outbound
├── mcp                 MCP JSON-RPC 2.0 server over stdio
├── cron                Manage scheduled prompts
├── session             Inspect / delete session store
├── skills              List / show / lint skills
├── doctor              Diagnose the local installation
├── status              Print daemon status
├── init                Write a default config to ~/.config/rousseau/
└── version             Print version, commit, build date
```

## `rousseau chat`

Abre la TUI interactiva de Bubble Tea.

| Flag | Tipo | Por defecto | Notas |
|---|---|---|---|
| `--session` | string | — | Reanuda una sesión existente por ID. |
| `--title` | string | timestamp | Título para una sesión nueva. |

## `rousseau whatsapp`

Ejecuta el bridge de WhatsApp. Imprime un código QR en el primer arranque.

| Flag | Tipo | Por defecto | Notas |
|---|---|---|---|
| `--store` | string | `$XDG_DATA_HOME/rousseau/whatsapp.db` | Ruta al store de dispositivos de whatsmeow. |
| `--allow` | []string | ninguno | Restringe el manejo entrante a estos JIDs. Repetible. **Nunca lo dejes vacío en un número público.** |

## `rousseau signal`

Ejecuta el bridge de Signal. Lanza `signal-cli jsonRpc` como subproceso.

| Flag | Tipo | Por defecto | Notas |
|---|---|---|---|
| `--account` | string | desde `signal.account` | Número de teléfono E.164 con el que se ejecuta el demonio. |
| `--binary` | string | `signal-cli` | Ruta al ejecutable de signal-cli. |
| `--allow` | []string | ninguno | Restringe la entrada a estos números E.164. |

## `rousseau telegram`

Ejecuta el long-poller de la API de Telegram Bot.

| Flag | Tipo | Por defecto | Notas |
|---|---|---|---|
| `--token` | string | desde `telegram.token` | Token de BotFather. |
| `--allow` | []string | ninguno | Restringe la entrada a estos IDs de chat. |

## `rousseau matrix`

Ejecuta el bridge de Matrix.

| Flag | Tipo | Por defecto | Notas |
|---|---|---|---|
| `--homeserver-url` | string | desde la config | por ejemplo, `https://matrix.org`. |
| `--access-token` | string | desde la config | Access token del bot. |
| `--user-id` | string | desde la config | ID de usuario de Matrix del bot (`@bot:matrix.org`). |
| `--allow` | []string | ninguno | Restringe la entrada a estos IDs de usuario. |

## `rousseau slack`

Ejecuta el bridge de Slack en Socket Mode.

| Flag | Tipo | Por defecto | Notas |
|---|---|---|---|
| `--app-token` | string | desde la config | Token de Socket Mode `xapp-...`. |
| `--bot-token` | string | desde la config | Token de OAuth de usuario bot `xoxb-...`. |
| `--allow` | []string | ninguno | Restringe la entrada a estos IDs de usuario de Slack. |

## `rousseau discord`

Ejecuta el bridge de Discord Gateway.

| Flag | Tipo | Por defecto | Notas |
|---|---|---|---|
| `--token` | string | desde la config | Token del bot. |
| `--allow` | []string | ninguno | Restringe la entrada a estos IDs de usuario de Discord. |

## `rousseau sms`

SMS de solo envío mediante Twilio o Vonage. Sin entrada.

| Flag | Tipo | Por defecto | Notas |
|---|---|---|---|
| `--provider` | string | desde la config | `twilio` o `vonage`. |
| `--from` | string | desde la config | Número emisor E.164. |
| `--account-sid` | string | desde la config | Account SID de Twilio. |
| `--auth-token` | string | desde la config | Auth token de Twilio o secret de Vonage. |
| `--api-key` | string | desde la config | API key de Vonage. |

## `rousseau imessage`

Bridge de iMessage respaldado por BlueBubbles.

| Flag | Tipo | Por defecto | Notas |
|---|---|---|---|
| `--base-url` | string | `http://localhost:1234` | URL del servidor BlueBubbles. |
| `--password` | string | desde la config | Contraseña del servidor BlueBubbles. |
| `--chat-guid` | string | desde la config | Destino de salida. |
| `--poll-interval` | duration | 5s | Frecuencia de sondeo para nuevos mensajes. |
| `--allow` | []string | ninguno | Restringe la entrada. |

## `rousseau email`

Bridge de correo sobre IMAP + SMTP.

| Flag | Tipo | Por defecto | Notas |
|---|---|---|---|
| `--imap-addr` | string | desde la config | por ejemplo, `imap.example.com:993`. |
| `--imap-username`, `--imap-password` | string | desde la config | Credenciales IMAP. |
| `--smtp-addr` | string | desde la config | por ejemplo, `smtp.example.com:587`. |
| `--smtp-username`, `--smtp-password` | string | desde la config | Credenciales SMTP. |
| `--from` | string | desde la config | Remitente del sobre. |
| `--poll-interval` | duration | 30s | Cadencia de sondeo IMAP. |
| `--allow` | []string | ninguno | Restringe las direcciones remitentes entrantes. |

## `rousseau mcp`

Inicia el servidor MCP sobre stdio. Sin flags — cada opción vive en `config.yaml`.

## `rousseau cron`

| Subcomando | Descripción |
|---|---|
| `cron add` | Añade un prompt programado. Flags: `--name`, `--schedule` (cron de 5 campos), `--prompt`, `--deliver-to`. |
| `cron list` | Lista cada trabajo con estado `on/off` y timestamp de la última ejecución. |
| `cron remove <name-or-id>` | Elimina un trabajo. |
| `cron enable <name-or-id>` | Habilita un trabajo deshabilitado. |
| `cron disable <name-or-id>` | Deshabilita un trabajo habilitado (sin eliminarlo). |

## `rousseau session`

| Subcomando | Descripción |
|---|---|
| `session list` | Lista las sesiones del store, con las más recientes primero. |
| `session search <query>` | Búsqueda FTS5 sobre el contenido de mensajes de todas las sesiones. |
| `session show <id>` | Imprime el historial de mensajes de una sesión. |
| `session delete <id>` | Elimina una sesión. |

## `rousseau skills`

| Subcomando | Descripción |
|---|---|
| `skills list` | Lista las skills descubiertas en `skills_dir`. |
| `skills show <name>` | Imprime el front-matter YAML y el cuerpo de una skill. |
| `skills lint` | Valida las skills contra su esquema. |

## `rousseau doctor`

Recorre cada dependencia de runtime y cada elección de configuración. Imprime un informe de estado con filas etiquetadas como `ok`, `warn`, `fail`, `info`. Código de salida 1 si alguna fila es `fail`.

Sin flags por ahora; extiende mediante `--config` a nivel global.

## `rousseau status`

Imprime un resumen compacto del estado del demonio — proveedor, número de sesiones, trabajos de cron. Solo lectura.

## `rousseau init`

Escribe un `config.yaml` por defecto en `~/.config/rousseau/`. Se niega a sobrescribir un archivo existente salvo que se pase `--force`.

| Flag | Tipo | Por defecto | Notas |
|---|---|---|---|
| `--force` | bool | false | Sobrescribe la configuración existente. |

## `rousseau version`

Imprime la versión, el hash del commit y la fecha de build. Sellado en tiempo de build vía `-ldflags`.

## Códigos de salida

| Código | Significado |
|---|---|
| 0 | El comando se completó correctamente. |
| 1 | El comando falló. El error se imprime en stderr. |

Consulta [Referencia: códigos de salida](/es/reference/exit-codes/) para la semántica de señales del demonio.

## Variables de entorno

Cada campo de configuración puede sobrescribirse mediante una variable de entorno usando el prefijo `ROUSSEAU_` y `_` como separador de sección: `ROUSSEAU_LOG_LEVEL=debug`, `ROUSSEAU_ANTHROPIC_API_KEY=sk-ant-...`, etc.

El caso especial es `ANTHROPIC_API_KEY` (sin prefijo) — el cargador de configuración la reconoce directamente por convención.

## Solución de problemas

### `unknown command` al pasar un subcomando

Los subcomandos de Rousseau se declaran en `internal/cli/root.go`. Si `rousseau <cmd>` reporta un comando desconocido, o el flag está mal escrito o estás en un binario más antiguo. `rousseau version` muestra la versión que tienes.

### Los flags repetibles necesitan múltiples invocaciones

`--allow` acepta un JID por flag. Repite el flag para múltiples valores: `--allow A --allow B`, no `--allow A,B`.

### Variables de entorno ignoradas silenciosamente

Rousseau usa el prefijo `ROUSSEAU_` y guion bajo como separador de sección: `anthropic.model` se convierte en `ROUSSEAU_ANTHROPIC_MODEL`. Las mayúsculas y minúsculas importan.

### `rousseau chat` solo muestra una pantalla en blanco

La TUI de Bubble Tea necesita una terminal compatible con ANSI. Establece `TERM=xterm-256color` y ejecuta interactivamente (no bajo `nohup` ni tuberías).

### El comando termina con 0 inmediatamente

Algunos flags (`--help`, variantes de `--version`) hacen cortocircuito. Si tu comando no se ejecuta, revisa los flags que has pasado.

## Páginas relacionadas

- [Guía de usuario: TUI](/es/user-guide/tui/) — atajos de teclado dentro de `rousseau chat`.
- [Guía de usuario: herramientas](/es/user-guide/tools/) — el esquema JSON de cada herramienta integrada.
- [Referencia: comandos CLI](/es/reference/cli-commands/) — tabla de comandos.
- [Referencia: variables de entorno](/es/reference/environment-variables/) — matriz de sobrescritura.
- [Configuración](/es/configuration/) — el archivo de configuración que respalda cada comando.

## Lecturas adicionales

- `internal/cli/root.go` — el árbol de Cobra.
- `internal/cli/chat.go`, `internal/cli/whatsapp.go`, `internal/cli/slack.go`, … — un archivo por subcomando.
- `internal/config/config.go` — resolución de variables de entorno / flags.
