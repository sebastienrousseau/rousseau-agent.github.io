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
description: "Set up rousseau-agent's Slack transport: Socket Mode (xapp-* app token + xoxb-* bot token), no public webhook, allowlist by user ID."
keywords: "Slack, Socket Mode, xapp, xoxb, chat.postMessage, connections:write, no webhook, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/transports/slack/"
subtitle: "Socket Mode with no public HTTP surface."
tags: "transports, Slack"
title: "Transporte Slack"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Slack, Socket Mode, xapp, xoxb, chat.postMessage, connections:write, no webhook, allowlist"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transporte Slack"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 16
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/slack/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/slack/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transporte Slack"
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
twitter_description: "Set up rousseau-agent's Slack transport: Socket Mode (xapp-* app token + xoxb-* bot token), no public webhook, allowlist by user ID."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transporte Slack"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Qué aprenderás</span><p>El recorrido completo por el asistente de app.slack.com, los scopes OAuth exactos a otorgar, las suscripciones a eventos a configurar, cómo Socket Mode evita la necesidad de un webhook público y cómo funciona la prevención de bucles de mensajes propios de rousseau. Lee <code>internal/transport/slack/client.go</code> junto a esta página.</p></aside>

## Descripción general

El transporte de Slack (`internal/transport/slack/`) usa **Socket Mode** — un WebSocket saliente a Slack — para que el servicio no necesite una superficie HTTP pública. Los eventos entrantes fluyen sobre el socket; las llamadas salientes van a la Web API estándar (`chat.postMessage`).

<aside class="admonition" data-type="tip"><span class="admonition-title">Por qué Socket Mode</span><p>La alternativa (Events API + Request URL) requiere un endpoint HTTPS público con un certificado SSL. Rousseau no incluye ninguna superficie HTTP entrante por diseño, por lo que Socket Mode es la única ruta de ingreso soportada.</p></aside>

## Dos tokens

Slack Socket Mode requiere dos tokens con responsabilidades disjuntas:

| Token | Prefijo | Alcance | Propósito |
|---|---|---|---|
| Token a nivel de app | `xapp-` | `connections:write` | Abre el WebSocket de Socket Mode. |
| Token de bot | `xoxb-` | `chat:write` + suscripciones a eventos | Envía mensajes, se suscribe a eventos. |

## Configuración de la app

Paso a paso completo en https://app.slack.com/apps :

1. **Crea una nueva app** ("From scratch"). Elige un workspace.
2. **Habilita Socket Mode** (Settings → Socket Mode). Genera un **token a nivel de app** con `connections:write`. Este es el token `xapp-*`.
3. **Configura las suscripciones a eventos** (Features → Event Subscriptions). Suscríbete a `message.channels`, `message.im`, o los scopes de canal que el bot deba escuchar. **No** necesitas una Request URL porque Socket Mode entrega los eventos sobre el socket.
4. **Añade scopes de bot** (Features → OAuth & Permissions). Mínimo: `chat:write`. Añade `im:history`, `channels:history`, `groups:history`, o `mpim:history` según tus suscripciones a eventos.
5. **Instala la app en el workspace.** La pantalla de instalación devuelve el token de bot `xoxb-*`.
6. **Opcionalmente registra el ID de usuario propio del bot** (empieza con `U…`). Esto es lo que rousseau usa para la prevención de bucles de mensajes propios.

## Configuración

```yaml
slack:
  app_token: "xapp-1-A0..."
  bot_token: "xoxb-1234..."
  bot_user_id: "U0123ABCD"
  reply_header: ""
  allowlist:
    - "U0ALICE"
    - "U0BOB"
```

| Campo | Por defecto | Efecto |
|---|---|---|
| `app_token` | *requerido* | Token a nivel de app `xapp-*` con `connections:write`. |
| `bot_token` | *requerido* | Token de bot `xoxb-*` con `chat:write`. |
| `bot_user_id` | *vacío* | ID `U…` del usuario bot para la prevención de bucles de mensajes propios. Opcional; recae en inspeccionar el campo `bot_id`. |
| `reply_header` | *vacío* | Antepuesto a cada mensaje saliente. |
| `allowlist` | `[]` | IDs de usuario de Slack cuyos mensajes se procesan. |

## Línea de comandos

```sh
rousseau slack \
  --app-token xapp-... \
  --bot-token xoxb-... \
  --bot-user-id U0123ABCD
```

## Formato de cable

- **Entrante.** Slack envía envoltorios JSON sobre el WebSocket. rousseau confirma el envoltorio, extrae el texto del mensaje y el remitente, y lo entrega al handler.
- **Saliente.** `POST https://slack.com/api/chat.postMessage` con `{"channel": "<id>", "text": "…"}` y `Authorization: Bearer <bot_token>`.

## Scopes de OAuth explicados

Cada scope otorga una superficie de API específica. Los scopes que rousseau necesita, y qué se rompe sin ellos:

| Scope | Endpoint usado | Roto sin |
|---|---|---|
| `connections:write` | `apps.connections.open` (WebSocket de Socket Mode) | No se puede abrir el socket. **Requerido.** |
| `chat:write` | `chat.postMessage` | No se puede responder a ningún mensaje. **Requerido.** |
| `im:history` | `conversations.history` para DMs (indirecto vía eventos) | El bot no verá el contenido de los DMs en los eventos. |
| `im:read` | `im.list`, metadatos de DM | No se pueden listar los DMs abiertos. |
| `im:write` | `conversations.open` | No se puede abrir un nuevo DM (solo relevante si quieres que el bot envíe DM a alguien sin ser solicitado). |
| `mpim:history`, `channels:history`, `groups:history` | IMs multi-participante / canales / canales privados | El bot no verá el contenido de mensajes fuera de DMs. |

Establece los scopes en *OAuth &amp; Permissions &gt; Bot Token Scopes*. Solo añade los scopes que realmente necesites — Slack muestra un aviso al instalar sobre cada scope, y es más probable que los usuarios finales instalen un bot con una superficie de permisos estrecha.

## Prevención de bucles de mensajes propios

Sin protección, un bot que responde a mensajes también verá sus propias respuestas como eventos entrantes — llevando a bucles descontrolados. Rousseau maneja esto vía `bot_user_id`:

```go
// Simplificado — lógica real en internal/transport/slack/client.go
if msg.User == cfg.BotUserID {
    continue // Omite: este es nuestro propio mensaje saliente haciendo eco.
}
```

Obtén el ID de usuario de tu bot una vez vía:

```sh
curl -H "Authorization: Bearer xoxb-your-token" \
  https://slack.com/api/auth.test
```

La respuesta incluye `user_id`. Pégalo en `slack.bot_user_id` en la configuración, o pásalo con `--bot-user-id`.

<aside class="admonition" data-type="warning"><span class="admonition-title">Prevención de bucles de respaldo</span><p>Incluso sin <code>bot_user_id</code>, el transporte ignora los eventos de subtipo <code>bot_message</code>. Pero depender solo del subtipo es frágil — establece <code>bot_user_id</code> en producción.</p></aside>

## Threading

Los mensajes de Slack llevan un `thread_ts` cuando son respuestas en un hilo. Las llamadas salientes de rousseau incluyen `thread_ts` cuando el evento entrante tenía uno, para que las respuestas del bot permanezcan en el hilo. Los mensajes de nivel superior se convierten en nuevos hilos solo cuando el usuario inicia uno.

## Modos de fallo

| Síntoma | Corrección |
|---|---|
| `invalid_auth` al abrir el socket | `app_token` es incorrecto o le falta `connections:write`. Regenéralo. |
| Los eventos entrantes nunca llegan | Verifica que **Event Subscriptions** esté habilitado y que los eventos `message.*` relevantes estén suscritos. |
| El bot responde a sus propios mensajes | Establece `bot_user_id` en la configuración. |
| `not_in_channel` al enviar | Invita al bot al canal (`/invite @rousseau-bot`). |
| El DM funciona pero el canal no | Falta el scope `channels:history`, o el bot no ha sido invitado al canal. |

## Solución de problemas

### `invalid_auth` al abrir el socket

El token `xapp-…` es incorrecto o perdió su scope. Regenera desde *Basic Information &gt; App-Level Tokens*, asegúrate de que `connections:write` esté en el nuevo token.

### `not_authed` en `chat.postMessage`

Token de bot (`xoxb-…`) faltante o incorrecto. Regenera desde *OAuth &amp; Permissions &gt; Bot User OAuth Token*.

### Los eventos llegan pero rousseau no responde a ninguno

Revisa la allowlist. En modo `pattern` con `default: deny`, los usuarios no listados se descartan silenciosamente. Busca `router.transport.rejected` en los logs.

### `channel_not_found` en saliente

El ID de canal de Slack (`C…`) ha cambiado — por ejemplo, un canal fue archivado y recreado. Actualiza cualquier ID de canal codificado. Rousseau normalmente usa el canal del evento entrante, así que esto solo ocurre con entrega cron a un canal fijo.

### El bot aparece offline en Slack

Socket Mode inactiva el WebSocket cada ~30s. Si Slack muestra el bot como offline, verifica: (1) el servicio está en ejecución (`systemctl --user status`), (2) el WebSocket está conectado (línea de log `slack.connected`), (3) el reloj de la máquina está dentro de 30s del tiempo real.

## Páginas relacionadas

- [Primeros pasos: Tu primer transporte](/es/getting-started/first-transport/) — recorrido de principio a fin.
- [Configuración](/es/configuration/) — el bloque de configuración `slack`.
- [Transportes](/es/transports/) — transportes hermanos.
- [Despliegue](/es/deployment/) — ejecutar Slack en un contenedor Podman.
- [Guías: Auditoría y políticas de aprobación](/es/guides/audit-approval-policies/) — conjuntos de reglas para un workspace de Slack compartido.

## Lectura adicional

- `internal/transport/slack/client.go` — conexión Socket Mode, bombeo de eventos, `chat.postMessage`.
- `internal/cli/slack.go` — cableado de CLI.
- `internal/transport/router.go` — aplicación de allowlist.
- [Documentación de la API de Slack: Socket Mode](https://api.slack.com/apis/socket-mode).
