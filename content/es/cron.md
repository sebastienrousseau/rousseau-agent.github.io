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
description: "rousseau-agent's cron scheduler runs stored jobs on a schedule and delivers replies through any registered transport. Backed by robfig/cron/v3 and SQLite job persistence."
keywords: "cron, robfig/cron, scheduler, scheduled jobs, delivery, transport-agnostic, SQLite persistence"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/cron/"
subtitle: "Trabajos programados persistentes que se ejecutan por cualquier transporte."
tags: "cron, scheduler, reference"
title: "Planificador cron"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, robfig/cron, scheduler, scheduled jobs, delivery, transport-agnostic, SQLite persistence"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Planificador cron"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 24
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/cron/index.html"
item_link: "https://docs.rousseau-agent.dev/cron/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Planificador cron"
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
twitter_description: "rousseau-agent's cron scheduler runs stored jobs on a schedule and delivers replies through any registered transport. Backed by robfig/cron/v3 and SQLite job persistence."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Planificador cron"
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

## Descripción general

El programador cron (`internal/cron/scheduler.go`) es una goroutine que ejecuta las entradas `CronJob` almacenadas en su horario configurado, ejecuta el prompt de cada job a través del agente y entrega la respuesta a una función `Delivery` agnóstica al transporte.

El programador se ejecuta junto a cualquier servicio de larga duración (típicamente `rousseau whatsapp` u otro transporte de chat). Los jobs se almacenan en la misma base de datos SQLite que las sesiones, así que sobreviven a los reinicios.

## Sintaxis de horario

Respaldado por [robfig/cron/v3](https://pkg.go.dev/github.com/robfig/cron/v3). El parser admite:

- Cron estándar de 5 campos: `<minuto> <hora> <día-del-mes> <mes> <día-de-la-semana>`.
- Atajos predefinidos: `@yearly`, `@monthly`, `@weekly`, `@daily`, `@hourly`, `@every <duration>`.

Ejemplos de horarios:

| Expresión | Se dispara |
|---|---|
| `0 9 * * 1-5` | 09:00 los días laborables |
| `*/15 * * * *` | Cada 15 minutos |
| `@daily` | Una vez al día a medianoche (zona horaria del servidor) |
| `@every 30m` | Cada 30 minutos |

## CLI

```sh
# Listar todos los jobs almacenados.
rousseau cron list

# Añadir un job.
rousseau cron add \
  --name morning-standup \
  --schedule '0 9 * * 1-5' \
  --prompt 'What are the top three engineering priorities today?' \
  --target '447900123456@s.whatsapp.net'

# Eliminar por nombre o ID.
rousseau cron remove morning-standup
```

## Configuración

Los jobs se almacenan en la base de datos de estado, no en el archivo de configuración. No hay nada en `~/.config/rousseau/config.yaml` para configurar el programador en sí; usa el predeterminado `PollInterval = 60s`.

## Flujo del job

1. El programador vuelve a sincronizar la lista de jobs desde SQLite cada `PollInterval`.
2. `robfig/cron/v3` dispara el job en su hora programada.
3. `TurnRunner.RunOnce(ctx, job.Prompt)` ejecuta una corrida de agente **de un solo turno** contra una sesión nueva (sin historial, sin recall entre sesiones a menos que el runner lo habilite).
4. El texto de la respuesta se pasa a `Delivery(ctx, job.Target, replyText)`.
5. Si `Delivery` devuelve error, se registra; el próximo tick reintenta.

## Delivery

`Delivery` es un tipo de función simple:

```go
type Delivery func(ctx context.Context, target, body string) error
```

El programador no importa `internal/transport`; el contrato de entrega es agnóstico al transporte. En la práctica, los servicios `rousseau <transport>` conectan un `Delivery` que resuelve la cadena de destino contra el transporte activo (`Deliver` en el cliente de transporte).

`target` depende del transporte:

- WhatsApp: un JID (`447900123456@s.whatsapp.net`).
- Telegram: un chat ID numérico.
- Slack: un ID de canal (`C012345`) o ID de usuario (`U012345`).
- Discord: un ID de canal.
- SMS: un destino E.164.
- iMessage: un GUID de chat.
- Signal: un destino E.164.
- Matrix: un ID de sala.
- Email: una dirección RFC 5322 completa.

## Persistencia

Los jobs se almacenan en la tabla `cron_jobs` de la base de datos de estado (`internal/state/sqlite/`). Campos: `id`, `name`, `schedule`, `prompt`, `target`, `created_at`, `updated_at`. Los reinicios recogen cada job en el próximo `PollInterval`.

Los nuevos jobs añadidos vía `rousseau cron add` quedan activos en un `PollInterval`: hasta 60 segundos por defecto.

## Interacción con los transportes

El closure `Delivery` captura una referencia al transporte en ejecución. Un solo servicio normalmente ejecuta un transporte, así que el programador cron entrega a través de ese transporte. Los despliegues multi-transporte ejecutan un servicio por transporte, y el operador apunta el `target` de cada cron job al servicio del transporte correspondiente.

La entrega entre transportes (el job se ejecuta en el servicio de WhatsApp, responde vía Slack) no está soportada hoy; el programador solo conoce el `Delivery` que se le entregó.

## Modos de fallo

| Síntoma | Solución |
|---|---|
| El job no se dispara | Verifica `rousseau status`; el programador registra `cron.fired` en cada activación. |
| El job se dispara pero no llega nada | Error de entrega: revisa los logs por `cron.delivery_failed`. |
| El job se ejecuta pero el modelo se rehúsa a actuar | Política de aprobación que deniega llamadas a herramientas. Afloja `agent.approver` o cambia a modo `pattern`. |
| La entrega va al destino equivocado | El programador es agnóstico al transporte; el servicio interpreta `target`. Confirma que el transporte que ejecuta tu servicio coincide con el formato del destino. |
