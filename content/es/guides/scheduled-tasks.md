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
description: "Worked example: use rousseau-agent's cron scheduler + WhatsApp to run a scheduled prompt daily and deliver the result to your phone."
keywords: "cron, scheduled tasks, whatsapp, code review, robfig, daily reminder"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/guides/scheduled-tasks/"
subtitle: "Nag yourself daily via WhatsApp."
tags: "guides, cron, scheduled, whatsapp"
title: "Guía: tareas programadas"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, scheduled tasks, whatsapp, code review, robfig, daily reminder"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guía: tareas programadas"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 31
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/scheduled-tasks/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/scheduled-tasks/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guía: tareas programadas"
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
twitter_description: "Worked example: use rousseau-agent's cron scheduler + WhatsApp to run a scheduled prompt daily and deliver the result to your phone."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guía: tareas programadas"
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

## Escenario

Quieres un recordatorio diario en WhatsApp a las 09:00 preguntando si la bandeja de revisiones de código tiene algo pendiente. El agente debe leer tu archivo local de cola de revisión, resumirlo y entregar el resumen a tu teléfono, sin importar si tu laptop está en medio de otra tarea.

Las piezas móviles:

- Un daemon `rousseau whatsapp` en ejecución.
- Un trabajo cron persistido en SQLite mediante `rousseau cron add`.
- La goroutine del planificador `robfig/cron/v3` dentro del daemon dispara el trabajo; la respuesta se envía a través del mismo transporte de WhatsApp.

## Requisitos previos

- `rousseau whatsapp` emparejado y entregando mensajes a al menos un JID ([Primer transporte](/es/getting-started/first-transport/)).
- Un archivo al que el prompt pueda apuntar: para este recorrido, una cola Markdown en `/workspace/review-queue.md`.

## Paso 1: Registrar el trabajo

```sh
rousseau cron add \
  --name daily-review-nag \
  --schedule "0 9 * * *" \
  --prompt "Read /workspace/review-queue.md and list every PR that has been open for more than 3 days. Reply with 3 bullets max." \
  --deliver-to 447900123456@s.whatsapp.net
```

`--schedule` es una expresión cron estilo POSIX de 5 campos, analizada por `robfig/cron/v3` (`min hour dom mon dow`). Rousseau valida la expresión al añadirla; un cronograma inválido falla rápidamente antes de llegar al almacén.

`--deliver-to` es el JID de WhatsApp que recibirá la respuesta. Para grupos, usa el formato `@g.us`.

## Paso 2: Confirmar que el trabajo está activo

```sh
rousseau cron list
```

Salida:

```
b7a3f2e1  on   daily-review-nag      0 9 * * *             last=never
    Read /workspace/review-queue.md and list every PR that has been open for more than 3 days. Reply with 3 bullets max. → 447900123456@s.whatsapp.net
```

Los nuevos trabajos se activan dentro del siguiente intervalo de polling del planificador (60 segundos por defecto). No se requiere reinicio.

## Paso 3: Forzar una ejecución de prueba

Los trabajos programados son disparados por el daemon `rousseau whatsapp` en ejecución. Para verificar el cableado sin esperar hasta las 09:00, cambia temporalmente el cronograma para que se ejecute dentro de un minuto:

```sh
rousseau cron remove daily-review-nag
rousseau cron add \
  --name daily-review-nag \
  --schedule "*/1 * * * *" \
  --prompt "..." \
  --deliver-to 447900123456@s.whatsapp.net
```

Observa el log del daemon:

```
cron.fire   name=daily-review-nag job=b7a3f2e1
tool.execute name=read id=t_1
cron.deliver name=daily-review-nag target=447900123456@s.whatsapp.net bytes=284
```

Una vez que veas el mensaje en tu teléfono, elimina la copia de cada minuto y vuelve a añadir la versión diaria.

## Paso 4: Deshabilitar sin eliminar

```sh
rousseau cron disable daily-review-nag
```

Alternar `enabled=false` deja el trabajo en el almacén pero lo omite en cada disparo. Vuelve a habilitarlo con `rousseau cron enable daily-review-nag`.

## Qué sucede bajo el capó

1. `rousseau cron add` escribe una fila en la tabla `cron` de `~/.local/share/rousseau/sessions.db`.
2. El daemon `rousseau whatsapp` inicia una goroutine del planificador `robfig/cron/v3` en el arranque y consulta la tabla cada `PollInterval` (60s por defecto).
3. Cuando la expresión cron se dispara, `Runner.RunOnce(ctx, prompt)` ejecuta un turno único del agente contra una sesión nueva (sin historial de disparos previos).
4. La respuesta pasa por `Delivery`: un callback agnóstico al transporte que el daemon conecta a `client.Deliver(ctx, target, body)`.
5. `last_run_at` se actualiza en el almacén. Las fallas se registran pero no deshabilitan el trabajo.

El planificador es durable: si el daemon muere en medio de un disparo, el siguiente arranque retoma la cola. Los trabajos nunca se disparan dos veces en el mismo minuto porque `robfig/cron/v3` deduplica por tick.

## Patrones comunes

| Cronograma | Significado |
|---|---|
| `0 9 * * *` | 09:00 todos los días. |
| `*/15 9-17 * * 1-5` | Cada 15 minutos, 09:00–17:59, lun–vie. |
| `0 * * * *` | Al inicio de cada hora. |
| `0 0 * * 0` | Medianoche todos los domingos. |

## Combinar con skills

Los prompts largos se vuelven tediosos. Si el prompt de un trabajo programado sigue creciendo, mueve el texto repetitivo a un [skill](/es/skills/) y deja que el prompt lo referencie. El skill se inserta en el prompt del sistema en el momento del disparo.

## Advertencias

- Los trabajos programados se ejecutan contra el proveedor configurado del daemon. Si tu proveedor principal es `claudecli` y rotas el login subyacente de `claude`, el disparo falla hasta que te vuelvas a autenticar.
- El destino de entrega debe pertenecer a la allowlist del daemon. Rousseau no entregará a un JID fuera de la allowlist aunque un trabajo programado se lo pida.
- El planificador cron se ejecuta dentro del daemon `rousseau whatsapp` por diseño. Ejecutar `rousseau slack` en paralelo te da dos planificadores independientes leyendo la misma tabla: los trabajos se dispararán dos veces. Elige un daemon como dueño del cronograma.

## Siguiente

- [Referencia de cron](/es/cron/): cada subcomando, cada opción.
- [Skills](/es/skills/): comparte texto repetitivo de prompt entre trabajos.
- [Auditoría + políticas de aprobación](/es/guides/audit-approval-policies/): restringe lo que puede hacer el prompt programado.
