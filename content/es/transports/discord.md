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
description: "Set up rousseau-agent's Discord transport: Gateway v10 WebSocket, bot token, Message Content intent, allowlist by user ID."
keywords: "Discord, Gateway v10, WebSocket, bot token, Message Content intent, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/transports/discord/"
subtitle: "Discord Gateway v10 over WebSocket."
tags: "transports, Discord"
title: "Transporte Discord"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Discord, Gateway v10, WebSocket, bot token, Message Content intent, allowlist"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transporte Discord"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 17
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/discord/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/discord/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transporte Discord"
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
twitter_description: "Set up rousseau-agent's Discord transport: Gateway v10 WebSocket, bot token, Message Content intent, allowlist by user ID."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transporte Discord"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Lo que aprenderás</span><p>El recorrido por el Discord Developer Portal, qué intents del Gateway necesita rousseau y por qué, el cálculo de la máscara de permisos explicado, y los modos de fallo para configuraciones erróneas comunes. Lee <code>internal/transport/discord/client.go</code> junto con esta página.</p></aside>

## Descripción general

El transporte de Discord (`internal/transport/discord/`) habla directamente el protocolo Discord Gateway v10, sin SDK de terceros. WebSocket para entrada (`Identify → Ready → Heartbeat/Ack → Dispatch(MESSAGE_CREATE)`); REST para salida (`POST /channels/{id}/messages`).

## Requisitos previos

1. **Una aplicación de Discord con un usuario Bot.** Créala en https://discord.com/developers/applications → **New Application** → pestaña **Bot** → **Add Bot**.
2. **Un token de bot** (pestaña Bot → **Reset Token** → copia el token, solo se muestra una vez).
3. **Intent Message Content habilitado** (pestaña Bot → **Privileged Gateway Intents**). Sin esto, el Gateway elimina el texto del mensaje de cada evento y rousseau verá cuerpos vacíos.
4. **El bot invitado a al menos un servidor** (o los DMs habilitados). Genera la URL de invitación en **OAuth2 → URL Generator** con el scope `bot` y los permisos `Send Messages` + `Read Message History`.

## Configuración

```yaml
discord:
  token: "Bot MTIz..."
  reply_header: ""
  allowlist:
    - "123456789012345678"
```

| Campo | Predeterminado | Efecto |
|---|---|---|
| `token` | *requerido* | Token del bot desde el Developer Portal. |
| `reply_header` | *vacío* | Se antepone a cada respuesta saliente. |
| `allowlist` | `[]` | IDs de usuario de Discord cuyos mensajes se procesan. |

## Línea de comandos

```sh
rousseau discord --token 'MTIz...' --allow 123456789012345678
```

## Intents del Gateway

rousseau solicita tres intents (`internal/transport/discord/client.go`):

| Intent | Bit | Propósito |
|---|---|---|
| `GUILD_MESSAGES` | `1 << 9` | Mensajes en canales de servidores. |
| `DIRECT_MESSAGES` | `1 << 12` | DMs al bot. |
| `MESSAGE_CONTENT` | `1 << 15` | Rellena el campo `content`. **Debe habilitarse en el portal.** |

Sin el intent Message Content, los eventos `MESSAGE_CREATE` llegan con `content` vacío y rousseau registrará `discord.empty_body`.

## Heartbeat

El transporte respeta el `heartbeat_interval` del Gateway proveniente del opcode Hello, enviando Heartbeat y rastreando `heartbeat_ack`. Los ACK perdidos cierran el socket y permiten que systemd reinicie el proceso.

## Encabezado de respuesta

Discord renderiza `**texto**` como negrita y no requiere un formato de encabezado específico. Sobrescríbelo según sea necesario:

```yaml
discord:
  reply_header: "**Rousseau Agent**\n"
```

## Calculadora de bits de permisos

Discord usa una máscara de bits para codificar los permisos de un bot en un canal. Cada permiso es una potencia de 2. Los más comunes para rousseau:

| Permiso | Bit |
|---|---|
| Read Messages / View Channels | `1 << 10` = `1024` |
| Send Messages | `1 << 11` = `2048` |
| Send Messages in Threads | `1 << 38` = `274877906944` |
| Read Message History | `1 << 16` = `65536` |
| Add Reactions | `1 << 6` = `64` |

Para otorgar múltiples permisos, aplica OR a los bits y pega el entero resultante en el parámetro `permissions=` del OAuth2 URL Generator:

```
Read Messages (1024) OR Send Messages (2048) OR Read Message History (65536) = 68608
```

<aside class="admonition" data-type="note"><span class="admonition-title">Ayuda del portal</span><p>El <em>OAuth2 URL Generator</em> del developer portal permite marcar casillas de permisos y calcula el entero por ti. Guarda como marcador la URL generada: permite a los administradores del servidor invitar al bot a cualquier servidor de Discord.</p></aside>

## Ciclo de vida del Gateway

El Gateway mantiene estado:

```
Cliente                       Discord Gateway
  │
  │   ────  Connect  ────▶
  │   ◀── HELLO (heartbeat_interval)
  │
  │   ───── IDENTIFY (token, intents) ────▶
  │   ◀── READY (session_id, user)
  │
  │   ─── Heartbeat cada N ms ─▶
  │   ◀── HEARTBEAT_ACK
  │
  │   ◀── MESSAGE_CREATE (un usuario escribió)
  │   ─── (rousseau procesa + envía respuesta con POST)
  │
  │   ◀── Disconnect (código 4009: sesión expirada)
  │   ─── RESUME (session_id) o re-IDENTIFY
```

El cliente rastrea `heartbeat_ack`. Si se pierde un ACK, el socket se cierra y el proceso termina; systemd o el runtime del contenedor se encargan de reiniciarlo.

## Modos de fallo

| Síntoma | Solución |
|---|---|
| El bot ve mensajes vacíos | Habilita el intent Message Content en el developer portal. |
| El Gateway se cierra con código 4004 | Token inválido. Regenéralo. |
| El bot no puede ver canales | Confirma que la invitación OAuth2 incluyó el scope `bot`. |
| 403 al enviar | El bot carece del permiso `Send Messages` en ese canal. |
| Código 4014 en Identify | Se solicitó un intent para el que tu aplicación no está aprobada (generalmente Message Content en un bot con más de 100 servidores). Verifica tu bot. |
| Código 4009 (sesión expirada) | Normal tras inactividad prolongada. Rousseau se reconecta de forma transparente. |

## Solución de problemas

### Gateway 4013 (Invalid Intents)

Estás solicitando un bit de intent que no existe. Esto usualmente indica un desajuste entre las constantes de intent de la biblioteca cliente y el mapa de intents actual de Discord. Rousseau construye la máscara de intents en `internal/transport/discord/client.go`; actualiza a la última versión si ves 4013 tras un cambio en la API de Discord.

### El bot recibe eventos pero no responde

Desajuste en la allowlist. El valor de `--allow` debe ser el ID de usuario numérico de Discord (no el nombre de usuario, ni el nombre para mostrar). Recupéralo en Discord: habilita el Modo Desarrollador en *Ajustes de Usuario &gt; Avanzado*, luego haz clic derecho sobre un usuario &gt; *Copiar ID de usuario*.

### Los DMs funcionan pero los canales de servidor no

Falta el intent `GUILD_MESSAGES`, o el bot no ha sido invitado al servidor. Los permisos de servidor son independientes de los permisos de DM: el bot debe tener el permiso `Read Messages` en el canal.

### `429 Too Many Requests` en salida

Discord impone un rate limit global de 50 req/s por bot, además de límites por canal. Bajo carga sostenida, rousseau no reintenta actualmente; quien llama debe aplicar backoff. Consulta [Guías: Rate limits](/es/guides/rate-limits/).

### El estado en línea del bot fluctúa

Discord considera a un bot fuera de línea tras aproximadamente 40 s sin heartbeat. La línea de log `discord.heartbeat_missed` indica un problema de red o un servicio con CPU insuficiente. Verifica que el contenedor tenga suficiente CPU asignada.

## Páginas relacionadas

- [Empezando: Primer transporte](/es/getting-started/first-transport/) — recorrido completo.
- [Configuración](/es/configuration/) — el bloque de configuración `discord`.
- [Transportes](/es/transports/) — transportes hermanos.
- [Guías: Auditoría y políticas de aprobación](/es/guides/audit-approval-policies/) — política para servidores de Discord.
- [Despliegue](/es/deployment/) — ejecutar Discord en un contenedor Podman.

## Lecturas adicionales

- `internal/transport/discord/client.go` — conexión al Gateway, heartbeat, bombeo de eventos.
- `internal/cli/discord.go` — cableado de la CLI.
- `internal/transport/router.go` — aplicación de la allowlist.
- [Documentación de la API de Discord: Gateway](https://discord.com/developers/docs/topics/gateway).
- [Documentación de la API de Discord: Permissions](https://discord.com/developers/docs/topics/permissions).
