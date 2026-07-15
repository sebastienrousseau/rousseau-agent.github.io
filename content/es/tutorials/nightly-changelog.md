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
description: "Schedule a rousseau cron job that summarises git log every evening and posts the result to WhatsApp."
keywords: "cron, git log, changelog, whatsapp, scheduled prompt, deliver-to"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/tutorials/nightly-changelog/"
subtitle: "A daily 18:00 cron job that pushes a git-log summary to WhatsApp."
tags: "tutorials, cron, changelog, whatsapp, git"
title: "Tutorial: changelog nocturno"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, git log, changelog, whatsapp, scheduled prompt, deliver-to"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorial: changelog nocturno"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/nightly-changelog/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/nightly-changelog/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorial: changelog nocturno"
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
twitter_description: "Schedule a rousseau cron job that summarises git log every evening and posts the result to WhatsApp."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorial: changelog nocturno"
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

## Qué construyes

Un trabajo cron almacenado en el estado SQLite propio de rousseau (tabla `cron_jobs`, esquema en `internal/state/sqlite/cron.go`) que se dispara a las 18:00 hora local en días laborables. Ejecuta un prompt que le pide al modelo resumir `git log --since=today` y entrega el resultado a tu teléfono por WhatsApp.

Tiempo estimado: 10 minutos.

## Requisitos previos

- Puente de WhatsApp ya emparejado (consulta el paso 4 de [Inicio rápido](/es/quickstart/) o [Transportes: WhatsApp](/es/transports/whatsapp/)).
- El daemon `rousseau whatsapp` en ejecución: el planificador cron en `internal/cron/scheduler.go` es iniciado por los daemons de transporte vía `wiring.startCron()`, no por `rousseau chat`.
- Un workspace que contenga el repositorio git que quieres resumir, montado con bind en el contenedor (o en el host si ejecutas rousseau fuera de un contenedor).

## Cómo funciona rousseau cron

`rousseau cron add` escribe una fila en la tabla `cron_jobs` (`internal/state/sqlite/cron.go`). Cada ~15 segundos, `scheduler.sync` vuelve a leer la tabla y reconcilia el cronograma en memoria de robfig/cron/v3. Cuando un trabajo se dispara, el planificador emite `cron.firing`, ejecuta el prompt a través del proveedor configurado y entrega el resultado a `deliver_to` mediante el puente de transporte que posee el proceso (WhatsApp en este tutorial).

Nombres de log estructurado que verás (de `internal/cron/scheduler.go`):

- `cron.started`: planificador iniciado con `poll_interval=…`.
- `cron.scheduled`: un trabajo fue aceptado.
- `cron.firing`: un trabajo está por ejecutarse.
- `cron.completed`: un trabajo terminó exitosamente.
- `cron.run_failed`, `cron.delivery_failed`, `cron.record_failed`: modos de falla.

## Paso 1: añadir el trabajo

```sh
rousseau cron add \
  --name        nightly-changelog \
  --schedule    "0 18 * * 1-5" \
  --prompt      "Summarise git log --since=yesterday under /workspace/rousseau-agent as a Slack-style bullet list. Keep it under 200 words. If nothing changed, reply with a single line 'no commits'." \
  --deliver-to  447900123456@s.whatsapp.net
```

La expresión cron es analizada por `robfig/cron/v3` en `newCronAddCmd` (`internal/cli/cron.go`). Las expresiones inválidas se rechazan antes de escribir. El valor de `--deliver-to` es el JID E.164 para WhatsApp (`<dígitos>@s.whatsapp.net`); el formato del destino de entrega es específico del transporte.

## Paso 2: verificar

```sh
rousseau cron list
```

Formato de salida (de `newCronListCmd`):

```
NAME               STATUS SCHEDULE       PROMPT                       DELIVER-TO
nightly-changelog  on     0 18 * * 1-5   Summarise git log …          447900123456@s.whatsapp.net
```

La lista también se expone por MCP como `rousseau_cron_list` (consulta `internal/mcp/tools.go`).

## Paso 3: prueba en seco

No existe un disparador "fire now" integrado. Para hacer un smoke test, programa temporalmente el trabajo dentro de un minuto:

```sh
rousseau cron remove nightly-changelog
rousseau cron add --name test --schedule "*/1 * * * *" --prompt "say hi" --deliver-to "$JID"
journalctl --user -u rousseau-agent -f | grep cron.
```

Secuencia de log esperada:

```
INFO cron.scheduled  job=test expr=*/1 * * * *
INFO cron.firing     job=test
INFO cron.completed  job=test
```

Elimina el trabajo de prueba y vuelve a añadir el real cuando termines.

## Paso 4: ajustar el prompt

Los mejores prompts de cron son autocontenidos: el modelo no tiene memoria de ejecuciones anteriores. Incluye la ruta del repo, el formato de salida esperado y un fallback para el caso vacío. Ejemplo de segunda iteración:

```
Summarise commits authored since 07:00 UTC today under
/workspace/rousseau-agent. Use this format:

- <short type>: <one-line summary> — <sha>

Group by author. If no commits landed, reply exactly: no commits.
```

## Activar y eliminar

```sh
rousseau cron disable nightly-changelog   # mantiene la fila, detiene el disparo
rousseau cron enable  nightly-changelog
rousseau cron remove  nightly-changelog   # elimina la fila
```

`SetEnabled` y `Delete` de `internal/state/sqlite/cron.go` son lo que estos llaman.

## Relacionado

- [Cron](/es/cron/): referencia del planificador.
- [Guías: Tareas programadas](/es/guides/scheduled-tasks/): discusión más profunda.
- [Transportes: WhatsApp](/es/transports/whatsapp/): cómo funciona delivery-to.
- [Referencia: Comandos CLI](/es/reference/cli-commands/): cada flag de `rousseau cron`.
