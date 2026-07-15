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
description: "Set up rousseau-agent's Matrix transport: homeserver URL, access token, user ID, long-polling /sync, allowlist by MXID."
keywords: "Matrix, client-server, MXID, access token, homeserver, /sync, long polling, Synapse"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/transports/matrix/"
subtitle: "Matrix client-server API with long-polling /sync."
tags: "transports, Matrix"
title: "Transporte Matrix"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Matrix, client-server, MXID, access token, homeserver, /sync, long polling, Synapse"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transporte Matrix"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 15
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/matrix/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/matrix/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transporte Matrix"
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
twitter_description: "Set up rousseau-agent's Matrix transport: homeserver URL, access token, user ID, long-polling /sync, allowlist by MXID."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transporte Matrix"
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

El transporte de Matrix (`internal/transport/matrix/`) se comunica directamente con la API cliente-servidor de Matrix, sin SDK de terceros. Usa long-polling con `/sync` para la entrada y `/rooms/{room}/send/{event_type}/{txn_id}` para la salida.

Funciona con cualquier homeserver conforme a la especificación: Synapse, Dendrite o Conduit.

## Requisitos previos

1. **Una cuenta de bot** en el homeserver de tu elección. Regístrala mediante el cliente estándar de Matrix o a través de la API de administración del homeserver.
2. **Un token de acceso** para esa cuenta. Inicia sesión con el bot en un cliente Matrix normal una vez, luego copia el token desde **Ajustes → Ayuda y Acerca de → Token de acceso**. Alternativamente, usa la API de login directamente:

   ```sh
   curl -X POST https://matrix.org/_matrix/client/v3/login \
     -H 'Content-Type: application/json' \
     -d '{"type":"m.login.password","user":"bot","password":"..."}'
   ```

3. **El MXID completo del bot** (por ejemplo, `@rousseau-bot:matrix.org`) para suprimir el eco de sus propios mensajes.

## Configuración

```yaml
matrix:
  homeserver_url: "https://matrix.org"
  access_token: "syt_..."
  user_id: "@rousseau-bot:matrix.org"
  reply_header: ""
  allowlist:
    - "@alice:matrix.org"
    - "@bob:example.com"
```

| Campo | Predeterminado | Efecto |
|---|---|---|
| `homeserver_url` | *requerido* | URL base (`https://matrix.org`). |
| `access_token` | *requerido* | Token de acceso del usuario bot. |
| `user_id` | *vacío* | MXID completo del usuario bot. Opcional pero recomendado (supresión de eco). |
| `reply_header` | *vacío* | Se antepone a cada respuesta saliente. |
| `allowlist` | `[]` | MXIDs cuyos mensajes se procesan. |

## Línea de comandos

```sh
rousseau matrix \
  --homeserver-url https://matrix.org \
  --access-token syt_... \
  --user-id @rousseau-bot:matrix.org \
  --allow @alice:matrix.org
```

## Long-polling

`PollTimeout` es de 30 segundos por defecto. El cursor `since` de cada respuesta `/sync` se almacena en memoria y se usa en la siguiente llamada, de modo que los mensajes nunca se vuelven a entregar durante la vida del proceso. En un reinicio, el servicio retrocede al cursor activo más antiguo que devuelva el homeserver: esto es una semántica normal de `sync` y coincide con la de cualquier cliente Matrix.

## Invitaciones a salas

El bot ya debe ser miembro de cualquier sala en la que deba responder. Invítalo desde un cliente Matrix normal. rousseau no acepta invitaciones automáticamente; unirse a salas queda fuera del alcance.

## Modos de fallo

| Síntoma | Solución |
|---|---|
| 401 en `/sync` | Token de acceso expirado o invalidado. Vuelve a iniciar sesión. |
| El bot nunca ve un mensaje | Confirma que el bot es miembro de la sala, no solo invitado. |
| Bucle de eco de sus propios mensajes | Configura `user_id` para que rousseau pueda filtrar sus propios mensajes. |
