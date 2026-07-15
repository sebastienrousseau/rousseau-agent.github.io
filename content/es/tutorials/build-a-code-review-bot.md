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
description: "Wire rousseau-agent to a Slack channel that runs read and grep over the workspace whenever an operator asks."
keywords: "slack, code review, socket mode, read tool, grep tool, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/tutorials/build-a-code-review-bot/"
subtitle: "A Slack channel that lets rousseau review a repo on demand."
tags: "tutorials, slack, code review, socket mode, read, grep"
title: "Tutorial: crear un bot de revisión de código"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "slack, code review, socket mode, read tool, grep tool, allowlist"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorial: crear un bot de revisión de código"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 42
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/build-a-code-review-bot/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/build-a-code-review-bot/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorial: crear un bot de revisión de código"
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
twitter_description: "Wire rousseau-agent to a Slack channel that runs read and grep over the workspace whenever an operator asks."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorial: crear un bot de revisión de código"
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

## Qué vas a construir

Un canal privado de Slack donde los miembros del equipo mencionan `@rousseau` con una ruta de repositorio y una pregunta. Rousseau accede al workspace, ejecuta `read` y `grep` desde `internal/tools/builtin/`, y publica una respuesta con referencias a líneas citadas. Sin superficie HTTP pública: Slack Socket Mode dirige todo desde un WebSocket saliente.

Tiempo estimado: 20 minutos, asumiendo que ya tienes acceso de administrador de Slack a un workspace.

## Requisitos previos

- Rousseau instalado y un proveedor configurado (consulta [Quickstart](/es/quickstart/)).
- Administrador de un workspace de Slack.
- Un repositorio ya clonado en alguna ruta bajo tu `$HOME`; ese se convierte en el "workspace" sobre el que el bot puede ejecutar `read`/`grep`.

## Paso 1: crear una aplicación de Slack

Socket Mode de Slack es lo que hace posible este bot: tu servicio abre un WebSocket saliente hacia Slack, sin necesidad de ingreso.

1. Ve a <https://api.slack.com/apps> y crea una nueva aplicación **from scratch**.
2. En **Socket Mode**, habilítalo y genera un **app-level token** con `connections:write`. Copia el valor `xapp-...`.
3. En **OAuth & Permissions**, agrega estos **Bot Token Scopes**:
   - `chat:write`
   - `app_mentions:read`
   - `channels:history` (o `groups:history` para canales privados)
4. Instala la aplicación en tu workspace. Copia el **Bot User OAuth Token**: el valor `xoxb-...`.
5. En **Event Subscriptions**, habilita los eventos y suscribe al bot a `app_mention` y `message.channels` (o `message.groups`).
6. Invita al bot al canal de revisión: `/invite @rousseau`.

## Paso 2: configurar rousseau

Añade a `~/.config/rousseau/config.yaml`. Los campos relevantes provienen de `SlackConfig` en `internal/config/config.go`:

```yaml
provider: claudecli           # o anthropic — lo que hayas configurado en el Quickstart

slack:
  app_token:  xapp-1-…
  bot_token:  xoxb-…
  bot_user_id: U0ROUSSEAU     # obtenido desde https://api.slack.com/methods/auth.test
  reply_header: "*rousseau-agent*\n\n"
  allowlist:
    - U01ABC…                 # tus IDs de usuario de Slack

agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
    # sin bash, sin write, sin edit — revisor de solo lectura
```

La `allowlist` restringe de quién aceptará mensajes el router. El router en `internal/transport/router.go` emite `transport.rejected` para cualquier otro remitente.

## Paso 3: ejecutar el puente

```sh
rousseau slack \
  --app-token "$SLACK_APP_TOKEN" \
  --bot-token "$SLACK_BOT_TOKEN" \
  --bot-user-id "$SLACK_BOT_USER_ID"
```

`--bot-user-id` impide que el bot responda a sus propios mensajes. Los logs estructurados de `internal/transport/slack/client.go` mostrarán:

```
INFO slack.started
INFO slack.incoming from=U01ABC channel=C01REVIEW text="…"
INFO tool.execute name=read id=t_1
INFO tool.execute name=grep id=t_2
```

## Paso 4: probarlo

En el canal de revisión:

```
@rousseau look under /home/seb/repos/acme-api and tell me
where request logging is set up
```

El proveedor `claudecli` (o Anthropic, el que hayas elegido) llamará a `read` y `grep` desde `internal/tools/builtin/` contra el bind mount del workspace. Como el approver corre en modo `pattern` con solo `read` y `grep` en la allowlist, el modelo no puede escribir ni ejecutar comandos de shell, aunque un prompt comprometido se lo pida.

## Paso 5: endurecer

Los approvers en modo pattern son **regex sobre la entrada JSON de la herramienta**. Para restringir `read` y `grep` a un árbol de proyecto específico:

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: "\"path\":\"/home/seb/repos/acme-api/[^\"]*\""}
      - {tool: grep, match: "\"path\":\"/home/seb/repos/acme-api\""}
```

Consulta [Tutorial: Endurecer el approver](/es/tutorials/harden-approver-policy/) para el recorrido completo de `default: deny` + auditoría.

## Desplegar bajo systemd

Para cualquier cosa más allá de una sesión de laptop, ejecuta el puente de Slack bajo la unidad Podman Quadlet en `docker/rousseau-agent.container`: reemplaza `Exec=whatsapp --allow …` por `Exec=slack --app-token … --bot-token …`. Consulta [Despliegue](/es/deployment/) para ver la unidad completa.

## Relacionado

- [Transportes: Slack](/es/transports/slack/)
- [Guía del usuario: Políticas de aprobación](/es/user-guide/approval-policies/)
- [Guía del usuario: Herramientas](/es/user-guide/tools/)
- [Tutorial: Endurecer el approver](/es/tutorials/harden-approver-policy/)
