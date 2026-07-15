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
description: "Overview of rousseau-agent's nine chat transports: WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, Email, SMS. Every transport implements Start / Stop / Deliver."
keywords: "transports, WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, email, SMS"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/transports/"
subtitle: "Nueve transportes de chat detrás de una única interfaz Transport."
tags: "transports, overview"
title: "Transportes"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "transports, WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, email, SMS"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transportes"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 11
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transportes"
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
twitter_description: "Overview of rousseau-agent's nine chat transports: WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, Email, SMS. Every transport implements Start / Stop / Deliver."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transportes"
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

## La interfaz Transport

Cada transporte implementa una pequeña interfaz (`internal/transport/transport.go`):

```go
type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

Por encima del transporte se sitúa el `Router`, que maneja la búsqueda de sesión por remitente, la aplicación de allowlist y el despacho al `Agent`. Debajo se encuentra el código específico del cable del transporte.

Ninguno de los transportes distribuidos expone una superficie HTTP pública por defecto. Esta es una elección de postura deliberada: los daemons de rousseau deben ser seguros para ejecutarse detrás de NAT sin reglas de reenvío de puertos.

## Transportes soportados

| Transporte | Entrada | Salida | Biblioteca / protocolo subyacente | Auth | Configuración de una línea |
|---|:---:|:---:|---|---|---|
| [WhatsApp](/es/transports/whatsapp/) | sí | sí | `go.mau.fi/whatsmeow` | Emparejamiento de dispositivo (QR) | `rousseau whatsapp --allow <jid>` |
| [Signal](/es/transports/signal/) | sí | sí | JSON-RPC de `signal-cli` | Cuenta pre-registrada | `rousseau signal --account +447900123456` |
| [Telegram](/es/transports/telegram/) | sí | sí | Long-polling de Bot API | Token de BotFather | `rousseau telegram --token <token>` |
| [Matrix](/es/transports/matrix/) | sí | sí | API client-server `/sync` | Access token | `rousseau matrix --homeserver-url … --access-token …` |
| [Slack](/es/transports/slack/) | sí | sí | Socket Mode + Web API | `xapp-*` + `xoxb-*` | `rousseau slack --app-token … --bot-token …` |
| [Discord](/es/transports/discord/) | sí | sí | Gateway v10 + REST | Token del bot | `rousseau discord --token <token>` |
| [iMessage](/es/transports/imessage/) | sí | sí | Polling HTTP de BlueBubbles | Contraseña del servidor | `rousseau imessage --base-url … --password …` |
| [Email](/es/transports/email/) | sí | sí | IMAP + SMTP | Usuario + contraseña | `rousseau email --imap-addr … --smtp-addr …` |
| [SMS](/es/transports/sms/) | no | sí | REST de Twilio o Vonage | Account SID / API key | `rousseau sms --provider twilio --account-sid … --auth-token …` |

## Por qué no hay superficie HTTP pública

Dos decisiones de diseño mantienen cada transporte listado alejado de un webhook público:

- **Entrada basada en WebSocket.** Slack Socket Mode y Discord Gateway son solo salientes desde la perspectiva del daemon: el daemon marca al proveedor por TLS y los mensajes llegan por la misma conexión.
- **Polling.** WhatsApp, Telegram, Matrix, iMessage y email extraen actualizaciones a su propio ritmo. No hay webhook que el proveedor invoque.

SMS es la excepción, y rousseau lo resuelve haciendo SMS **solo salida**. El SMS entrante requeriría un webhook de Twilio / Vonage, que es exactamente la superficie que este proyecto rechaza introducir.

## Comportamiento del Router

El router (`internal/transport/router.go`) se sitúa entre cada transporte y el `Agent`:

- **Aislamiento de sesión.** Cada valor `From` distinto obtiene su propia `Session`, para que las conversaciones paralelas no se contaminen entre sí. Las identidades LID de WhatsApp se normalizan primero a JIDs de teléfono (consulta `internal/transport/whatsapp/resolve.go`).
- **Allowlist.** Cada transporte que soporta entrada tiene un `Allowlist []string` en su configuración. Vacío significa "aceptar cada remitente": para daemons siempre quieres al menos una entrada.
- **Despacho.** El router serializa los turnos por sesión, para que un usuario no pueda apilar dos mensajes entrantes concurrentes.

## Añadir un décimo transporte

Implementa `transport.Transport` (tres métodos). Añade un tipo `Config` que refleje el diseño de bloque bajo `internal/config/`. Cablea un comando CLI en `internal/cli/`. Esa es la superficie: el núcleo del agente permanece intacto.

## Páginas por transporte

- [WhatsApp](/es/transports/whatsapp/)
- [Signal](/es/transports/signal/)
- [Telegram](/es/transports/telegram/)
- [Matrix](/es/transports/matrix/)
- [Slack](/es/transports/slack/)
- [Discord](/es/transports/discord/)
- [iMessage](/es/transports/imessage/)
- [Email](/es/transports/email/)
- [SMS](/es/transports/sms/)
