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
description: "Set up rousseau-agent's iMessage transport: BlueBubbles server on macOS, HTTP polling, poll interval, cursor deduplication, chat GUID for outbound."
keywords: "iMessage, BlueBubbles, macOS, HTTP polling, chat GUID, cursor, deduplication"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/transports/imessage/"
subtitle: "BlueBubbles HTTP polling from a macOS host."
tags: "transports, iMessage"
title: "Transporte iMessage"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "iMessage, BlueBubbles, macOS, HTTP polling, chat GUID, cursor, deduplication"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transporte iMessage"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 18
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/imessage/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/imessage/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transporte iMessage"
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
twitter_description: "Set up rousseau-agent's iMessage transport: BlueBubbles server on macOS, HTTP polling, poll interval, cursor deduplication, chat GUID for outbound."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transporte iMessage"
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

El transporte de iMessage (`internal/transport/imessage/`) no interactúa con iMessage directamente; Apple no provee una API oficial orientada al cliente. En su lugar, hace polling sobre [BlueBubbles](https://bluebubbles.app), un servicio de macOS que expone iMessage vía HTTP + Socket.IO.

rousseau usa únicamente los endpoints HTTP de BlueBubbles (Socket.IO se evita deliberadamente para mantener una huella de dependencias reducida).

## Arquitectura

```
+-----------+     iMessage      +---------+     HTTP      +-----------+
| Apple ID  | <---------------> | macOS   | <-----------> | rousseau  |
|  server   |                   | Blue    |               | daemon    |
+-----------+                   | Bubbles |               |           |
                                +---------+               +-----------+
```

El host macOS ejecuta BlueBubbles y permanece con la sesión iniciada en iMessage. rousseau hace polling sobre el endpoint `/api/v1/message` de BlueBubbles a la cadencia configurada y reenvía los mensajes nuevos al handler.

## Requisitos previos

1. **Un host macOS** con iMessage iniciado. No necesariamente la misma máquina en que se ejecuta rousseau.
2. **Servidor BlueBubbles** instalado en ese host, escuchando en una URL que rousseau pueda alcanzar (dirección LAN, VPN o Tailscale).
3. **Contraseña de BlueBubbles** desde la GUI del servidor (Settings → Server Password).
4. **Un GUID de chat** para la salida. Encuéntralo en la GUI de BlueBubbles o vía `GET /api/v1/chat`.

## Configuración

```yaml
imessage:
  base_url: "http://mac.internal:1234"
  password: "..."
  chat_guid: "iMessage;-;+15550001234"
  poll_interval: "5s"
  reply_header: ""
```

| Campo | Predeterminado | Efecto |
|---|---|---|
| `base_url` | *requerido* | URL del servidor BlueBubbles. |
| `password` | *requerido* | Contraseña del servidor BlueBubbles. |
| `chat_guid` | *vacío* | GUID del destino de salida. |
| `poll_interval` | `5s` | Cadencia de polling contra `/api/v1/message`. |
| `reply_header` | *vacío* | Se antepone a cada mensaje saliente. |

## Línea de comandos

```sh
rousseau imessage \
  --base-url http://mac.internal:1234 \
  --password ... \
  --chat-guid 'iMessage;-;+15550001234' \
  --poll-interval 5s
```

## Deduplicación por cursor

Al iniciar, el transporte prepara su cursor `lastID` con el mensaje más reciente existente, para que el operador no reciba todo el historial de iMessage. Cada polling posterior obtiene los `PageSize` mensajes más recientes (25 por defecto) y solo reenvía los más recientes que el cursor.

El cursor se mantiene en memoria. En un reinicio, el cursor se vuelve a preparar desde BlueBubbles: se perderá una ventana pequeña de mensajes que llegaron mientras el servicio estaba caído. Es un compromiso deliberado; una lógica de cursor persistente requeriría otra tabla en el almacén de estado, y las marcas de tiempo de entrega de iMessage no son monótonas garantizadas entre dispositivos.

## Alcanzabilidad

BlueBubbles debe ser alcanzable por red desde donde rousseau se ejecute. Patrones comunes:

- **Misma LAN.** `http://<mac-lan-ip>:1234`.
- **Tailscale.** `http://mac.tailnet.ts.net:1234`. Cifra el enlace y funciona a través de NAT.
- **Túnel inverso.** `http://localhost:1234` en el host de rousseau con un túnel SSH `-R` desde el Mac.

No expongas BlueBubbles al internet público a menos que entiendas su modelo de autenticación (una única contraseña).

## Modos de fallo

| Síntoma | Solución |
|---|---|
| `imessage.prime_failed` en el arranque | BlueBubbles inalcanzable: revisa `base_url` y `password`. |
| Se repiten todos los mensajes históricos | `lastID` no se preparó. Revisa permisos y autenticación. |
| Mensajes salientes descartados silenciosamente | `chat_guid` incorrecto. Búscalo vía `GET /api/v1/chat`. |
| Los mensajes llegan con minutos de retraso | Aumenta la frecuencia de polling propia de BlueBubbles o reduce `poll_interval`. |
