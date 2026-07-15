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
description: "rousseau-agent's SMS transport is send-only. Twilio (account_sid + auth_token) or Vonage (api_key + auth_token). Inbound not supported because it requires a public webhook."
keywords: "SMS, Twilio, Vonage, Nexmo, send-only, Messaging Service SID, E.164, no webhook"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/transports/sms/"
subtitle: "Send-only SMS via Twilio or Vonage."
tags: "transports, SMS"
title: "Transporte SMS"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "SMS, Twilio, Vonage, Nexmo, send-only, Messaging Service SID, E.164, no webhook"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transporte SMS"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 19
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/sms/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/sms/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transporte SMS"
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
twitter_description: "rousseau-agent's SMS transport is send-only. Twilio (account_sid + auth_token) or Vonage (api_key + auth_token). Inbound not supported because it requires a public webhook."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transporte SMS"
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

## Solo envío, por diseño

El transporte SMS es **solo de envío**. La entrada SMS requiere un webhook HTTP público al que el operador telefónico envía POST, lo que entra en conflicto directo con la postura de superficie de entrada nula de rousseau. Si tu caso de uso necesita SMS entrantes, ejecuta rousseau junto con un receptor de webhooks dedicado y enruta los mensajes a través del programador cron o la API de integración del agent-loop.

`Start` se implementa como un no-op que se bloquea en `ctx.Done()`, para que el transporte encaje en la forma estándar de cableado del servicio.

## Operadores admitidos

| Operador | `provider` en configuración | Campos requeridos |
|---|---|---|
| Twilio | `twilio` | `from`, `account_sid`, `auth_token` |
| Vonage (antes Nexmo) | `vonage` | `from`, `api_key`, `auth_token` (el API secret) |

## Configuración de Twilio

```yaml
sms:
  provider: twilio
  from: "+15550000000"
  account_sid: "AC..."
  auth_token: "..."
```

`from` puede ser un número remitente en formato E.164 o un **Twilio Messaging Service SID** (empieza con `MG…`). Los Messaging Services gestionan flotas, enrutamiento sticky-sender y selección de remitente por geografía; recomendados para cualquier tráfico que exceda un solo país.

`base_url` es `https://api.twilio.com/2010-04-01` por defecto y solo requiere sobrescritura para endpoints regionales o pruebas.

## Configuración de Vonage

```yaml
sms:
  provider: vonage
  from: "+15550000000"
  api_key: "abcd1234"
  auth_token: "efgh5678"
```

`auth_token` en la configuración de Vonage corresponde al **API secret** de Vonage, no a su clave de firma JWT; Vonage autentica los envíos de SMS con un par clave/secreto simple.

`base_url` es `https://rest.nexmo.com` por defecto.

## Línea de comandos

```sh
# Twilio
rousseau sms \
  --provider twilio \
  --from '+15550000000' \
  --account-sid AC... \
  --auth-token ...

# Vonage
rousseau sms \
  --provider vonage \
  --from '+15550000000' \
  --api-key abcd1234 \
  --auth-token efgh5678
```

Al no haber lado de entrada, `--allow` no aplica.

## API de entrega

Ambos proveedores usan sus respectivos endpoints REST:

- **Twilio.** `POST /2010-04-01/Accounts/{sid}/Messages.json` con autenticación básica SID/token.
- **Vonage.** `POST /sms/json` con `api_key` + `api_secret` en el cuerpo.

Los IDs de mensaje devueltos se registran; los webhooks de estado de entrega **no** se consumen (de nuevo, sin superficie HTTP pública).

## Formato E.164

Los números de `from` y destino deben estar en formato E.164 (`+<país><suscriptor>`). Sin espacios ni guiones. Los Messaging Service SIDs de Twilio omiten este requisito solo en el campo `from`.

## Higiene de costos

- Configura `max_tokens` de forma agresiva en tu proveedor: los SMS son baratos por mensaje pero los bytes se multiplican rápido si el modelo genera respuestas largas (Twilio segmenta cada 160 caracteres en GSM-7 o cada 70 en UCS-2).
- Considera reescribir la respuesta saliente para que sea concisa antes de entregarla al transporte SMS. `agent.Options.SystemPrompt` es el lugar correcto.
