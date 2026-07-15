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
description: "Set up rousseau-agent's Telegram transport: BotFather token, long-polling, allowlist by numeric user ID, reply-header customisation."
keywords: "Telegram, Bot API, BotFather, long polling, getUpdates, allowlist, chat ID"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/transports/telegram/"
subtitle: "Telegram Bot API over long-polling."
tags: "transports, Telegram"
title: "Transporte Telegram"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Telegram, Bot API, BotFather, long polling, getUpdates, allowlist, chat ID"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transporte Telegram"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 14
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/telegram/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/telegram/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transporte Telegram"
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
twitter_description: "Set up rousseau-agent's Telegram transport: BotFather token, long-polling, allowlist by numeric user ID, reply-header customisation."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transporte Telegram"
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

El transporte de Telegram (`internal/transport/telegram/`) se comunica directamente con la API HTTP de Telegram Bot, sin SDK de terceros. Usa long-polling con `getUpdates` para la entrada y `sendMessage` para la salida.

## Requisitos previos

1. **Un bot.** En Telegram, envía un mensaje a [@BotFather](https://t.me/BotFather), envía `/newbot`, elige un nombre y un nombre de usuario con sufijo `_bot`. BotFather devuelve un token de API HTTP con formato `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`.
2. **Los IDs de usuario que deseas autorizar.** Los IDs de usuario de Telegram son numéricos. El bot no puede resolver `@username` a un ID de usuario por sí mismo; el método estándar consiste en pedirle a cada usuario autorizado que envíe `/start` al bot una vez, y luego leer el campo `from.id` en el log.

## Configuración

```yaml
telegram:
  token: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
  reply_header: ""
  allowlist:
    - "12345678"
    - "98765432"
```

| Campo | Predeterminado | Efecto |
|---|---|---|
| `token` | *requerido* | Token del bot proporcionado por BotFather. |
| `base_url` | `https://api.telegram.org` | Sobrescritura para un servidor local de Bot API. |
| `reply_header` | *vacío* | Se antepone a cada respuesta saliente. |
| `allowlist` | `[]` | IDs de usuario de Telegram cuyos mensajes se procesan. |

## Línea de comandos

```sh
rousseau telegram --token 123456:ABC... --allow 12345678 --allow 98765432
```

`--allow` puede repetirse.

## Long-polling

El transporte llama a `getUpdates` con un `PollTimeout` de 30 segundos por defecto (`internal/transport/telegram/client.go`). Cada actualización recibida avanza un `offset` interno, por lo que los mensajes nunca se vuelven a entregar, incluso tras reinicios.

No hay webhook. El servicio no requiere ninguna superficie HTTP entrante.

## Formato del mensaje

Solo se procesan mensajes de texto. Los archivos multimedia, stickers y notas de voz se ignoran (una futura mejora podría enrutar el audio a través de la misma ruta de whisper.cpp que WhatsApp).

## Modos de fallo

| Síntoma | Solución |
|---|---|
| No llegan actualizaciones | Confirma que el bot recibió al menos un mensaje: Telegram no entrega mensajes históricos. |
| 409 Conflict en getUpdates | Otra instancia está haciendo polling con el mismo token. Detén la otra. |
| La allowlist rechaza a un usuario real | Registra el campo `from.id`; los IDs de usuario son numéricos y no coinciden con `@username`. |
