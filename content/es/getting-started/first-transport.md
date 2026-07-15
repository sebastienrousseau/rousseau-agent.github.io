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
description: "End-to-end walkthrough for wiring your first chat transport. Uses WhatsApp as the canonical example: pair, allowlist, send a test message, verify the reply."
keywords: "first transport, whatsapp, pairing, allowlist, e2e walkthrough, test message"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/getting-started/first-transport/"
subtitle: "End-to-end WhatsApp walkthrough: pair, allowlist, verify."
tags: "first-transport, whatsapp, walkthrough"
title: "Tu primer transporte"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "first transport, whatsapp, pairing, allowlist, e2e walkthrough, test message"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tu primer transporte"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 25
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/first-transport/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/first-transport/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Tu primer transporte"
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
twitter_description: "End-to-end walkthrough for wiring your first chat transport. Uses WhatsApp as the canonical example: pair, allowlist, send a test message, verify the reply."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tu primer transporte"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Qué aprenderás</span><p>Cómo emparejar un transporte de chat con el servicio rousseau, incluir en la allowlist el JID/ID de usuario que lo controla, enviar un primer mensaje de prueba y confirmar la respuesta. WhatsApp es el recorrido canónico porque el emparejamiento es el más estricto; las pestañas a continuación muestran los recorridos paralelos para Slack y Discord.</p></aside>

## Elige tu primer transporte

Cada transporte es un adaptador ligero detrás de la misma interfaz `transport.Transport` — la allowlist, el enrutamiento de sesión y la entrega cron son idénticos en todos ellos. Las diferencias son la UX de emparejamiento y el formato de identificador por transporte (JID, ID de usuario, ID de sala). Elige el que puedas emparejar más rápido:

<div class="tabs" data-tabs="first-transport">
  <div class="tab-list" role="tablist" aria-label="First transport">
    <button role="tab" aria-selected="true">WhatsApp</button>
    <button role="tab" aria-selected="false">Slack</button>
    <button role="tab" aria-selected="false">Discord</button>
    <button role="tab" aria-selected="false">Telegram</button>
    <button role="tab" aria-selected="false">Signal</button>
  </div>
  <div class="tab-panel" role="tabpanel">

WhatsApp es la referencia — el más difícil de emparejar, el más fácil de probar (ya tienes la app en tu teléfono).

**Requisitos previos:** tu teléfono con WhatsApp, tu JID E.164 (por ejemplo `447900123456@s.whatsapp.net`).

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

Escanea el QR desde **WhatsApp &gt; Configuración &gt; Dispositivos vinculados &gt; Vincular un dispositivo**. Envía `hello` a ti mismo; rousseau responde vía WhatsApp. Consulta a continuación el recorrido completo.

<aside class="admonition" data-type="warning"><span class="admonition-title">Protocolo no oficial</span><p>El soporte de WhatsApp usa <code>whatsmeow</code> — un cliente de ingeniería inversa. Meta ocasionalmente bloquea números que ejecutan clientes no oficiales. No lo ejecutes en un número del que dependas.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Requisitos previos:** administrador en un workspace de Slack, una app creada en [api.slack.com/apps](https://api.slack.com/apps), Socket Mode habilitado.

1. Crea una app de Slack, habilita **Socket Mode** en <em>Settings &gt; Socket Mode</em>.
2. Crea un **App-Level Token** con `connections:write` — este es el token `xapp-…`.
3. En <em>OAuth &amp; Permissions</em>, añade los scopes de bot `chat:write`, `im:history`, `im:read`, `im:write`, `mpim:history`, `mpim:read`. Instala en el workspace para obtener el token de bot `xoxb-…`.
4. En <em>Event Subscriptions</em>, suscríbete a `message.im` (DMs) y a cualquier evento de canal que desees.

```sh
rousseau slack --app-token xapp-... --bot-token xoxb-... --allow U01234567
```

Envía un DM al bot en Slack; rousseau responde en el mismo DM. Consulta [Transportes: Slack](/es/transports/slack/) para el recorrido completo con la justificación de los scopes de OAuth.

<aside class="admonition" data-type="tip"><span class="admonition-title">Sin HTTP público</span><p>Socket Mode significa que el servicio se conecta de forma saliente al WebSocket de Slack. No necesitas un webhook público, ngrok ni ingress.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Requisitos previos:** una aplicación de Discord en [discord.com/developers/applications](https://discord.com/developers/applications), un usuario bot, la opción **Message Content Intent** habilitada en <em>Bot</em>.

1. Crea una aplicación, añade un bot, copia el token del bot.
2. En <em>Bot &gt; Privileged Gateway Intents</em>, habilita **Message Content Intent**. Sin esto, el texto de los mensajes llega vacío.
3. Invita al bot mediante <em>OAuth2 &gt; URL Generator</em> — scope `bot`, permisos `Send Messages`, `Read Message History`.

```sh
rousseau discord --token <bot-token> --allow 234567890123456789
```

Envía un DM al bot; rousseau responde. Consulta [Transportes: Discord](/es/transports/discord/) para un análisis profundo de permisos e intents.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Requisitos previos:** un bot de Telegram de [@BotFather](https://t.me/BotFather).

1. Envía mensaje a `@BotFather`, `/newbot`, sigue las indicaciones. Copia el token.
2. Habla con tu bot al menos una vez para que Telegram cree un chat.

```sh
rousseau telegram --token 1234567890:AA... --allow 987654321
```

El valor de `--allow` es el ID numérico de usuario de Telegram (no el nombre de usuario). Obtenlo enviando un mensaje a [@userinfobot](https://t.me/userinfobot).

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Requisitos previos:** `signal-cli` instalado y enlazado a una cuenta de Signal. Consulta la [documentación de signal-cli](https://github.com/AsamK/signal-cli) para el flujo de emparejamiento.

```sh
rousseau signal --account +447900123456 --allow +447900654321
```

Rousseau lanza `signal-cli` como subproceso (consulta `internal/cli/signal.go`) y se comunica con él vía JSON-RPC. Consulta [Transportes: Signal](/es/transports/signal/).

  </div>
</div>

## Por qué el recorrido de WhatsApp

El resto de esta página usa WhatsApp como ejemplo canónico — si captas el patrón aquí, cada otro transporte es una variación (incluir un ID estable en la allowlist, ejecutar una UX de emparejamiento una vez, enviar una prueba, verificar la respuesta). Salta a la página del transporte hermano si ya tienes un token a mano:

- [Slack](/es/transports/slack/) — tokens de Socket Mode y suscripciones a eventos.
- [Discord](/es/transports/discord/) — token de bot, intents, enteros de permisos.
- [Telegram](/es/transports/telegram/) — token de BotFather.
- [Signal](/es/transports/signal/) — subproceso signal-cli.
- [Matrix](/es/transports/matrix/) — URL de homeserver + token de acceso.

## Requisitos previos

- `rousseau` en `$PATH` (consulta [Instalación](/es/getting-started/installation/)).
- Un proveedor funcional — `claudecli` heredando la autenticación de Claude Code es el por defecto; cualquier otro necesita su configuración cumplimentada primero ([Configuración](/es/configuration/)).
- Tu teléfono con WhatsApp instalado. Tu JID de teléfono E.164 (por ejemplo `447900123456@s.whatsapp.net`).

## Paso 1 — Elige el JID que controlará el servicio

Rousseau usa una allowlist para restringir el manejo entrante a un conjunto fijo de JIDs. Cualquier otro remitente se descarta silenciosamente. Esto es esencial: sin una allowlist, cualquiera que conozca el número podría controlar el agente.

Tu JID E.164 es tu número de teléfono, solo dígitos, seguido de `@s.whatsapp.net`:

```
447900123456@s.whatsapp.net
```

Los JIDs de grupo terminan en `@g.us`; el servicio también los admite, pero empieza con un JID personal.

## Paso 2 — Primera ejecución y emparejamiento

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

En la primera ejecución, se imprime un código QR a stdout. Abre WhatsApp en tu teléfono, ve a **Configuración → Dispositivos vinculados → Vincular un dispositivo**, y escanea el QR.

El servicio imprime algo como:

```
whatsapp.starting store=file:/home/you/.local/share/rousseau/whatsapp.db?_pragma=... allowlist=1
```

Una vez escanees, whatsmeow persiste las credenciales del dispositivo en `whatsapp.db`. Las ejecuciones subsecuentes se conectan silenciosamente — sin más QR.

## Paso 3 — Envía un mensaje de prueba

Desde tu teléfono, envía `hello` a ti mismo. El servicio registra el evento entrante, lo despacha al agente y entrega la respuesta de vuelta a través de WhatsApp con el header configurado:

```
💎 *Rousseau Agent*

Hello — what would you like to work on?
```

El header de respuesta se configura mediante `whatsapp.reply_header`. Ponlo en un solo espacio para deshabilitar el prefijo.

## Paso 4 — Configura un `config.yaml` para no necesitar flags largos

Crea `~/.config/rousseau/config.yaml`:

```yaml
provider: claudecli

claudecli:
  binary: claude
  permission_mode: bypassPermissions

whatsapp:
  reply_header: "💎 *Rousseau Agent*\n\n"
```

Ahora `rousseau whatsapp --allow 447900123456@s.whatsapp.net` toma el header automáticamente. Cada transporte lee su bloque del mismo archivo — consulta [Configuración](/es/configuration/) para la lista completa.

`bypassPermissions` es el valor por defecto para servicios no supervisados porque no hay un humano al otro lado del terminal para aprobar invocaciones de herramientas de forma interactiva. **Configura una política de aprobación** ([Guía de usuario: Políticas de aprobación](/es/user-guide/approval-policies/)) antes de apuntar el servicio a algo que te importe.

## Paso 5 — Confirma de principio a fin

Envía una pregunta de código desde tu teléfono:

```
Lee el archivo en /workspace/README.md y resúmelo en 3 viñetas.
```

El servicio ejecuta una invocación de herramienta `read`, alimenta el archivo al modelo y te envía el resumen. Acabas de cerrar el bucle:

- Teléfono → WhatsApp → WebSocket whatsmeow
- rousseau-agent → bucle del agente → invocación de herramienta → llamada al proveedor
- respuesta → whatsmeow → WhatsApp → teléfono

Nada cruzó tu perímetro de red excepto la llamada al proveedor — y si el proveedor era `claudecli` en tu instalación local de Claude Code, ni siquiera eso.

## Verificar con `rousseau doctor`

```sh
rousseau doctor
```

Cada comprobación para la ruta de WhatsApp está cubierta:

- `provider.claudecli.binary`, `provider.claudecli.version` — la ruta LLM.
- `state.path`, `state.db_size`, `state.sessions` — almacén de sesiones SQLite.
- `whatsapp.store`, `whatsapp.paired` — credenciales de dispositivo.
- `whatsapp.voice` — postura de transcripción de notas de voz.

Una fila `fail` es un bloqueo total; una fila `warn` merece la pena investigar antes del despliegue.

## Solución de problemas

### El código QR se imprime pero el teléfono lo rechaza

Tres causas comunes. Primero, un emparejamiento previo parcialmente completado dejó `whatsapp.db` en un estado que whatsmeow no puede reutilizar — elimina `~/.local/share/rousseau/whatsapp.db` y vuelve a escanear. Segundo, el reloj está desviado más de 30 segundos (común en contenedores sin un cliente NTP funcional) — el handshake de WhatsApp es sensible al tiempo. Tercero, una versión antigua de `whatsmeow` puede haber perdido una actualización de protocolo de Meta; actualiza rousseau.

### Envié un mensaje pero el servicio registra `router.transport.rejected`

Tu JID no coincide con la allowlist. El valor pasado a `--allow` debe ser el JID del remitente exactamente como WhatsApp lo reporta (`447900123456@s.whatsapp.net`, sin `+`, sin espacios). Ten en cuenta que las pruebas de autoenvío funcionan porque rousseau sustituye el JID propio de la cuenta por el hash de privacidad LID (consulta `internal/transport/whatsapp/resolve.go`).

### No se imprime QR y el servicio sale con `no rows`

El almacén de whatsmeow nunca se inicializó. Asegúrate de que el directorio padre (`~/.local/share/rousseau/`) exista y sea modificable. `rousseau doctor` reporta esto bajo `whatsapp.store`.

### Rousseau responde pero la salida del modelo está vacía

Comprueba `provider.claudecli.binary` y `provider.claudecli.version` en `rousseau doctor`. La causa más común de respuestas vacías es una invocación de `claudecli` devolviendo `is_error: true` — el servicio registra el error truncado en nivel `warn`. Cambia el proveedor a `anthropic` o `bedrock` para aislar el subproceso.

### Slack/Discord: "invalid_auth" o "401 Unauthorized"

Para Slack, `xapp-…` (app token) y `xoxb-…` (bot token) son diferentes — mezclarlos produce `invalid_auth`. Para Discord, el token mostrado en <em>Bot &gt; Reset Token</em> es de una sola vez; si lo copiaste una vez y lo perdiste, debes resetear de nuevo.

## Páginas relacionadas

- [Transportes](/es/transports/) — cada transporte, su protocolo de cable y su formato de allowlist.
- [Guía de usuario: CLI](/es/user-guide/cli/) — cada comando y flag.
- [Guía de usuario: Políticas de aprobación](/es/user-guide/approval-policies/) — la palanca de seguridad principal.
- [Despliegue](/es/deployment/) — traspaso desde `rousseau whatsapp` en primer plano a una unidad de systemd.
- [Modo voz](/es/user-guide/voice-mode/) — convierte notas de voz de WhatsApp en turnos del agente.

## Lectura adicional

- `internal/transport/whatsapp/client.go` — conexión, QR, bombeo de eventos.
- `internal/transport/whatsapp/resolve.go` — normalización LID/JID y manejo de autoenvío.
- `internal/cli/whatsapp.go` — cableado de CLI, DSN del almacén, selección de transcriptor.
- `internal/cli/slack.go`, `internal/cli/discord.go` — CLIs de transportes hermanos.
- `internal/transport/router.go` — aplicación de allowlist.
