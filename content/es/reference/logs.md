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
description: "rousseau-agent's slog output: message vocabulary, JSON vs text shape, and journalctl / jq recipes."
keywords: "slog, logs, json, text, journalctl, jq, observability"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/reference/logs/"
subtitle: "The full vocabulary of slog messages rousseau emits."
tags: "reference, logs, slog, observability, audit"
title: "Referencia: registros"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "slog, logs, json, text, journalctl, jq, observability"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Referencia: registros"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 52
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/logs/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/logs/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Referencia: registros"
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
twitter_description: "rousseau-agent's slog output: message vocabulary, JSON vs text shape, and journalctl / jq recipes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Referencia: registros"
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

## Configuración del logger

`internal/cli/root.go` construye un `*slog.Logger` por proceso — un `slog.NewTextHandler` cuando `log.format` está vacío o es `text`, un `slog.NewJSONHandler` cuando es `json`. El nivel mapea desde `log.level` (`debug`, `info`, `warn`/`warning`, `error`) con `info` como default. El handler escribe a stderr; cada demonio lo hereda.

Para un despliegue de producción, establece siempre `log.format: json`. Los pipelines de log aguas abajo (journald + `journalctl -o json`, Loki, Vector, Datadog Agent) parsean la salida estructurada de forma nativa.

## Forma de la salida

### Texto

```
time=2026-07-13T18:00:14.202Z level=INFO msg=tool.execute name=grep id=t_1
```

Disposición de texto por defecto de slog: `time`, `level`, `msg`, luego pares key=value.

### JSON

```json
{"time":"2026-07-13T18:00:14.202Z","level":"INFO","msg":"tool.execute","name":"grep","id":"t_1"}
```

Mismos campos, codificados en JSON. El campo `msg` es el identificador de evento estable — filtra y alerta sobre él, no sobre el texto para humanos.

## Vocabulario de mensajes

A continuación se listan todos los nombres de mensaje emitidos desde `internal/**/*.go` con su ubicación en el código y nivel esperado. Agrupados por subsistema; alfabetizados dentro de cada grupo.

### Bucle del agente (`internal/agent/`)

| Mensaje | Nivel | Campos | Significado |
|---|---|---|---|
| `agent.compressed` | INFO | `messages` | El compresor LLM reescribió una sesión; el nuevo número de mensajes es `messages`. |
| `agent.compress_failed` | WARN | `err` | El compresor devolvió un error; la sesión queda sin tocar. |
| `tool.denied` | WARN | `name`, `reason` | El approver bloqueó una llamada a herramienta. Campos desde `internal/agent/agent.go:179`. |
| `tool.execute` | INFO | `name`, `id` | El approver permitió y la herramienta se ejecutó. |
| `tool.error` | WARN | `name`, `err` | La herramienta se ejecutó pero devolvió error. |
| `turn.failed` | ERROR | `err` | El turno de TUI dio error. Emitido desde `internal/tui/model.go`. |
| `session.save_failed` | WARN | `err` | Persistir una sesión falló tras un turno. |

### Cron (`internal/cron/scheduler.go`)

| Mensaje | Nivel | Campos | Significado |
|---|---|---|---|
| `cron.started` | INFO | `poll_interval` | Arranque del planificador. |
| `cron.scheduled` | INFO | `job`, `expr` | Job añadido al schedule en memoria. |
| `cron.schedule_failed` | WARN | `job`, `expr`, `err` | robfig/cron/v3 rechazó la expresión. |
| `cron.sync_failed` | WARN | `err` | La pasada de reconciliación contra `cron_jobs` falló. |
| `cron.firing` | INFO | `job` | El job está a punto de ejecutarse. |
| `cron.completed` | INFO | `job` | El job terminó correctamente. |
| `cron.run_failed` | ERROR | `job`, `err` | La llamada al proveedor dentro del job falló. |
| `cron.delivery_failed` | ERROR | `job`, `target`, `err` | La entrega al transporte falló. |
| `cron.record_failed` | WARN | `job`, `err` | Escribir `last_run_at` falló. |

### MCP (`internal/mcp/server.go`)

| Mensaje | Nivel | Campos | Significado |
|---|---|---|---|
| `mcp.encode_error` | WARN | `err` | No se pudo codificar una respuesta como JSON (raro). |
| `mcp.tool_error` | WARN | `tool`, `err` | Un handler de herramienta devolvió error; expuesto al host con `isError=true`. |

### Router (`internal/transport/router.go`)

| Mensaje | Nivel | Campos | Significado |
|---|---|---|---|
| `transport.rejected` | WARN | `from` | Remitente no está en la allowlist; mensaje descartado. |
| `router.save_failed` | WARN | `err` | El guardado de sesión tras el turno falló. |
| `router.stale_mapping` | WARN | `jid`, `err` | El mapeo JID→sesión apuntaba a una sesión que ya no carga. |

### WhatsApp (`internal/transport/whatsapp/`)

| Mensaje | Nivel | Campos | Significado |
|---|---|---|---|
| `whatsapp.starting` | INFO | `store`, `allowlist` | Arranque del bridge; `store` es el DSN. |
| `whatsapp.qr_ready` | INFO | — | QR renderizado a stdout; escanéalo. |
| `whatsapp.qr_event` | WARN | `event` | Evento QR no exitoso desde whatsmeow. |
| `whatsapp.paired` | INFO | — | El teléfono aceptó el QR. |
| `whatsapp.connected` | INFO | — | WebSocket con Meta activo. |
| `whatsapp.disconnected` | WARN | — | Se perdió el socket. Reintenta automáticamente. |
| `whatsapp.logged_out` | ERROR | `reason` | Meta cerró la sesión del dispositivo — normalmente por incumplimiento de política. |
| `whatsapp.voice_enabled` | INFO | `binary`, `model` | Transcripción de notas de voz activada. |
| `whatsapp.incoming` | INFO | `from` | Mensaje entrante aceptado. |
| `whatsapp.skipped` | DEBUG | `reason` | El router descartó un mensaje (auto-eco, etc). |
| `whatsapp.empty_reply` | INFO | `elapsed` | El agente no produjo texto en este turno. |
| `whatsapp.handler_ok` | INFO | `elapsed`, `bytes` | Respuesta entregada. |
| `whatsapp.handler_failed` | ERROR | `err` | El turno dio error — normalmente fallo de proveedor o herramienta. |
| `whatsapp.send_failed` | ERROR | `err` | La entrega a Meta falló. |
| `whatsapp.presence_failed` | DEBUG | `err` | Escritura de presencia "escribiendo" falló (best-effort). |
| `whatsapp.audio_ignored` | INFO | `size` | Nota de voz recibida pero la transcripción está deshabilitada. |
| `whatsapp.audio_downloaded` | INFO | `size` | Bytes de nota de voz obtenidos de Meta. |
| `whatsapp.transcribed` | INFO | `elapsed` | whisper.cpp devolvió una transcripción. |
| `whatsapp.transcribe_failed` | ERROR | `err` | La invocación de whisper falló. |

### Slack (`internal/transport/slack/client.go`)

| Mensaje | Nivel | Campos | Significado |
|---|---|---|---|
| `slack.starting` | INFO | `allowlist` | Arranque del bridge. |
| `slack.started` | INFO | — | Sesión de Socket Mode aceptada. |
| `slack.session_failed` | WARN | `err` | Falló abrir la sesión de Socket Mode; retry. |
| `slack.frame_failed` | WARN | `err` | Frame mal formado desde Slack. |
| `slack.incoming` | INFO | `from`, `channel`, `text` | Mensaje aceptado. |
| `slack.handler_failed` | ERROR | `err` | El turno dio error. |

### Discord (`internal/transport/discord/client.go`)

| Mensaje | Nivel | Campos | Significado |
|---|---|---|---|
| `discord.starting` | INFO | `allowlist` | Arranque del bridge. |
| `discord.ready` | INFO | `bot_id` | Gateway de Discord listo. |
| `discord.started` | INFO | — | Sesión activa. |
| `discord.session_failed` | WARN | `err` | Apertura del gateway falló; retry. |
| `discord.frame_failed` | WARN | `err` | Frame incorrecto desde Discord. |
| `discord.incoming` | INFO | `from`, `channel` | Mensaje aceptado. |
| `discord.handler_failed` | ERROR | `err` | El turno dio error. |

### Telegram (`internal/transport/telegram/client.go`)

| Mensaje | Nivel | Campos | Significado |
|---|---|---|---|
| `telegram.starting` | INFO | `allowlist` | Arranque del bridge. |
| `telegram.started` | INFO | — | Primer long-poll con éxito. |
| `telegram.poll_failed` | WARN | `err` | HTTP del long-poll falló. |
| `telegram.incoming` | INFO | `from` | Mensaje aceptado. |
| `telegram.handler_failed` | ERROR | `err` | El turno dio error. |
| `telegram.send_failed` | ERROR | `err` | HTTP saliente falló. |

### Matrix (`internal/transport/matrix/client.go`)

| Mensaje | Nivel | Campos | Significado |
|---|---|---|---|
| `matrix.starting` | INFO | `homeserver`, `allowlist` | Arranque del bridge. |
| `matrix.started` | INFO | `homeserver` | Primer `/sync` aceptado. |
| `matrix.sync_failed` | WARN | `err` | HTTP de `/sync` falló. |
| `matrix.incoming` | INFO | `from`, `room` | Mensaje aceptado. |
| `matrix.handler_failed` | ERROR | `err` | El turno dio error. |
| `matrix.send_failed` | ERROR | `err` | HTTP saliente falló. |

### Signal (`internal/transport/signal/`)

| Mensaje | Nivel | Campos | Significado |
|---|---|---|---|
| `signal.starting` | INFO | `account`, `allowlist` | Arrancando el subproceso JSON-RPC de signal-cli. |
| `signal.started` | INFO | — | El subproceso reportó listo. |
| `signal.frame_failed` | WARN | `err` | Frame JSON mal formado desde signal-cli. |
| `signal.stderr` | WARN | `line` | Passthrough de stderr de signal-cli. |
| `signal.incoming` | INFO | `from` | Mensaje aceptado. |
| `signal.handler_failed` | ERROR | `err` | El turno dio error. |

### iMessage (`internal/transport/imessage/client.go`)

| Mensaje | Nivel | Campos | Significado |
|---|---|---|---|
| `imessage.starting` | INFO | `base` | URL del servidor BlueBubbles registrada. |
| `imessage.started` | INFO | `server` | Primer poll con éxito. |
| `imessage.prime_failed` | WARN | `err` | Fetch de priming state falló; reintenta. |
| `imessage.poll_failed` | WARN | `err` | HTTP del poll falló. |
| `imessage.incoming` | INFO | `from` | Mensaje aceptado. |
| `imessage.handler_failed` | ERROR | `err` | El turno dio error. |
| `imessage.send_failed` | ERROR | `err` | HTTP saliente falló. |

### Email + SMS (`internal/transport/email/`, `internal/transport/sms/`)

Sigue el mismo esquema `<transport>.starting / .started / .poll_failed / .incoming / .handler_failed / .send_failed` que los transportes de polling anteriores.

## Recetas

### Mostrar todas las llamadas a herramientas denegadas hoy

```sh
journalctl --user -u rousseau-agent --since today -o json \
  | jq -c 'select(.MESSAGE | fromjson? | .msg == "tool.denied")'
```

### Seguir una única sesión de transporte en vivo

```sh
journalctl --user -u rousseau-agent -f -o cat \
  | grep -E 'whatsapp\.|tool\.|cron\.'
```

### Alerta sobre fallos de cron

Boceto de regla de Prometheus/alertmanager (vía el pipeline `promtail` → Loki → alerta en [Guías: observabilidad](/es/guides/observability/)):

```yaml
- alert: RousseauCronFailure
  expr: |
    sum by (job) (
      count_over_time({app="rousseau-agent"} |= "cron.run_failed" [5m])
    ) > 0
```

### Redacción

`slog` no redacta por defecto. Configura un procesador aguas abajo para redactar los campos `err` en `whatsapp.send_failed`, `tool.error`, etc. — los errores de proveedor pueden incluir ocasionalmente fragmentos de prompt. Consulta [Guías: observabilidad](/es/guides/observability/) para el pipeline.

## Relacionado

- [Guía de usuario: políticas de aprobación](/es/user-guide/approval-policies/) — la fuente de `tool.denied`.
- [Guías: observabilidad](/es/guides/observability/) — receta completa de pipeline.
- [Guías: auditoría y políticas de aprobación](/es/guides/audit-approval-policies/) — trata estos logs como registro de auditoría.
