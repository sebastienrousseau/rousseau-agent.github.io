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
description: "Set up rousseau-agent's WhatsApp transport: QR pairing, E.164 allowlist, LID vs phone-JID normalisation, voice-note transcription with whisper.cpp."
keywords: "WhatsApp, whatsmeow, QR pairing, JID, LID, allowlist, voice notes, whisper, transcription"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/transports/whatsapp/"
subtitle: "Whatsmeow-backed WhatsApp bridge with QR pairing."
tags: "transports, WhatsApp"
title: "Transporte WhatsApp"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "WhatsApp, whatsmeow, QR pairing, JID, LID, allowlist, voice notes, whisper, transcription"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transporte WhatsApp"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 12
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/whatsapp/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/whatsapp/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transporte WhatsApp"
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
twitter_description: "Set up rousseau-agent's WhatsApp transport: QR pairing, E.164 allowlist, LID vs phone-JID normalisation, voice-note transcription with whisper.cpp."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transporte WhatsApp"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Qué aprenderás</span><p>Cómo el transporte de WhatsApp se empareja con tu teléfono, las reglas de normalización LID vs JID de teléfono, el flujo de transcripción de notas de voz, las descargas de medios, los patrones regex de allowlist y los modos de fallo que atrapan a los operadores primerizos. Lee <code>internal/transport/whatsapp/client.go</code>, <code>resolve.go</code> y <code>dispatch.go</code> junto a esta página.</p></aside>

## Descripción general

El transporte de WhatsApp (`internal/transport/whatsapp/`) está respaldado por `go.mau.fi/whatsmeow` — un cliente multi-dispositivo de WhatsApp Web de ingeniería inversa. Meta considera esto un cliente no oficial; no lo ejecutes en un número personal del que dependas para algo importante.

Se preserva el cifrado de extremo a extremo del protocolo Signal (whatsmeow usa el mismo protocolo que la app móvil de WhatsApp). El servicio mantiene las credenciales del dispositivo en un archivo SQLite separado del almacén de sesiones, por lo que un re-enlace de dispositivo no toca el historial de conversaciones.

<aside class="admonition" data-type="caution"><span class="admonition-title">Protocolo no oficial</span><p>Meta ocasionalmente bloquea números que ejecutan clientes no oficiales. Incluso si cumples con los límites de tasa de WhatsApp y te comportas responsablemente, un número de teléfono usado con <code>whatsmeow</code> puede ser bloqueado sin aviso. Usa un número dedicado, no uno personal.</p></aside>

## Emparejamiento

Primera ejecución:

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

Un código QR se imprime a stdout vía `mdp/qrterminal/v3`. Escanéalo con la app móvil de WhatsApp (**Configuración → Dispositivos vinculados → Vincular un dispositivo**). El estado de emparejamiento se escribe en `whatsapp.db` bajo el directorio de estado (típicamente `~/.local/share/rousseau/whatsapp.db`).

Las ejecuciones subsecuentes reutilizan el dispositivo emparejado silenciosamente. Si el QR reaparece, el emparejamiento ha sido revocado desde el lado del teléfono — elimina `whatsapp.db` y empareja de nuevo.

## Allowlist

`--allow` restringe el manejo entrante. Múltiples flags se acumulan:

```sh
rousseau whatsapp \
  --allow 447900123456@s.whatsapp.net \
  --allow 442071234567@s.whatsapp.net
```

El valor es un **JID** de WhatsApp — el número de teléfono E.164 (sin `+`) seguido de `@s.whatsapp.net`. Los JIDs de grupo (`<id>@g.us`) también están soportados.

Una allowlist vacía acepta todo remitente. Para un servicio de transporte de chat siempre quieres al menos una entrada.

## Normalización LID vs JID de teléfono

WhatsApp usa dos formatos de identificador para un usuario:

| Formato | Ejemplo | Significado |
|---|---|---|
| JID de teléfono | `447900123456@s.whatsapp.net` | El número de teléfono E.164, sin `+`, seguido de `@s.whatsapp.net`. Estable en el tiempo; revela el número de teléfono. |
| LID | `1234567890@lid` | Location-Independent ID — una cadena de apariencia aleatoria que no revela el número de teléfono. También estable, pero no directamente enlazable a un número. |
| Sufijo de dispositivo | `447900123456:5@s.whatsapp.net` | Cualquier JID puede llevar un sufijo de dirección de dispositivo (`:N`). WhatsApp reporta los mensajes con el dispositivo específico que los envió. |

El handler entrante de rousseau (`ResolveInbound` en `internal/transport/whatsapp/resolve.go`) normaliza cada evento a una forma canónica antes del despacho:

1. **Quita el sufijo de dispositivo.** `447900:5@s.whatsapp.net` se convierte en `447900@s.whatsapp.net`. Esto permite que las allowlists escritas como JIDs de usuario simples coincidan independientemente de qué dispositivo vinculado envió el mensaje.
2. **Sustituye LID por el JID de teléfono del titular de la cuenta en autoenvío.** Cuando el titular de la cuenta es el remitente (`IsFromMe=true`), WhatsApp reporta al remitente como el LID de la cuenta (un hash de privacidad), no el JID de teléfono. Rousseau sustituye el propio JID de la cuenta para que los operadores puedan incluir `<phone>@s.whatsapp.net` en la allowlist y que las pruebas de autoenvío se enruten correctamente.
3. **Descarta remitentes no parseables.** Los campos `User` o `Server` vacíos — descubiertos por `FuzzResolveInbound` — no pueden enrutarse de forma segura. El mensaje se omite silenciosamente en lugar de pasarse al handler como un From malformado.

### Gotcha de autoenvío

Cuando envías un mensaje a ti mismo en WhatsApp (para probar el bot), el campo remitente llega como tu LID. Si incluiste tu JID de teléfono en la allowlist, la búsqueda ingenua no coincidiría. La sustitución de rousseau — `if evt.Info.IsFromMe && ownID != nil { from = ownID.ToNonAD() }` — arregla esto.

### Prevención de bucles

`IsFromMe=true` también se dispara para mensajes enviados por *este* dispositivo vinculado (las respuestas salientes de rousseau haciendo eco). El transporte descarta esos cuando el ID de dispositivo coincide:

```go
if evt.Info.IsFromMe && ownID != nil && evt.Info.Sender.Device == ownID.Device {
    return Resolved{Skip: SkipOwnDevice}
}
```

Los mensajes de *otros* dispositivos vinculados de la cuenta (por ejemplo, el teléfono principal probando "envíate un mensaje a ti mismo") llevan `IsFromMe=true` pero un ID de dispositivo distinto — esos se manejan normalmente.

## Patrones regex de allowlist

El flag `--allow` toma cadenas exactas, no regex — rousseau realiza una comprobación de igualdad insensible a mayúsculas en `router.go`. Si quieres coincidencia por patrón, usa el archivo de configuración con modo `pattern` (igual que las políticas de aprobación):

```yaml
whatsapp:
  allowlist:
    - "447900123456@s.whatsapp.net"
    - "447900654321@s.whatsapp.net"
```

Para grupos (`<hash>@g.us`), añádelos de la misma manera. Para permitir a todos de un código de país dado, necesitarías una implementación personalizada de `Router.Allow` — el aplicador incorporado no hace coincidencia por prefijo por diseño.

<aside class="admonition" data-type="warning"><span class="admonition-title">Allowlist vacía</span><p>Una allowlist vacía acepta todo remitente. No ejecutes un transporte de chat sin allowlist en un número público — cualquiera que conozca el número se convierte en operador de tu agente.</p></aside>

## Header de respuesta

Cada mensaje saliente se prefija con un header para que el remitente sepa con qué bot está hablando. El por defecto:

```
💎 *Rousseau Agent*

<message body>
```

WhatsApp renderiza `*texto*` como negrita. Sobrescribe en la configuración:

```yaml
whatsapp:
  reply_header: "🤖 *Coding bot*\n\n"
```

Ponlo en un solo espacio `" "` para deshabilitar el prefijo por completo.

## Transcripción de notas de voz

Las notas de voz entrantes se transcriben vía `whisper.cpp` cuando el operador opta por ello. Desactivado por defecto porque requiere que el CLI `whisper` esté instalado.

```yaml
whatsapp:
  voice:
    enabled: true
    binary: whisper
    model: base.en
    language: en
    extra_args:
      - --threads
      - "4"
```

| Campo | Efecto |
|---|---|
| `enabled` | Interruptor. Cuando está desactivado, los mensajes de audio se registran y se omiten. |
| `binary` | Ejecutable del CLI Whisper. Vacío por defecto es `whisper`. |
| `model` | Pasado a `--model` (`base.en`, `small`, `medium`). |
| `model_path` | Ruta `.bin` explícita. Tiene precedencia sobre `model`. |
| `language` | Pasado a `--language`. Vacío autodetecta. |
| `extra_args` | Añadidos a cada invocación. |

El texto transcrito se entrega al agente como si el usuario lo hubiera escrito.

## Despliegue en contenedor

La unidad Quadlet Podman de referencia (`docker/rousseau-agent.container`) monta el directorio de estado con lectura-escritura para que el emparejamiento sobreviva a reinicios:

```
Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
```

`Network=pasta` da al contenedor una pila sin root solo de egress. Whatsmeow no necesita capacidades elevadas; `DropCapability=all` es seguro.

## Flujo de transcripción de notas de voz

Cuando llega una nota de voz, el resolvedor estándar devuelve `SkipEmptyText` (sin contenido de texto). `Dispatch` detecta esto específicamente para mensajes de audio y — si hay un `Transcriber` configurado — procede por esta ruta:

```
Mensaje de audio entrante
  │
  ├── Downloader.Download(ctx, audioMsg)
  │     • bytes []byte, mimetype string, err error
  │     • Registra whatsapp.audio_downloaded al tener éxito
  │
  ├── Transcriber.Transcribe(ctx, audio, mimetype)
  │     • Devuelve transcripción de texto plano
  │     • Registra whatsapp.transcribed con la duración
  │
  └── Vuelve a entrar en handleTextMessage con la transcripción como `Body`
```

Si no hay un transcriptor configurado, el servicio registra `whatsapp.audio_ignored reason=transcriber_not_configured` y descarta el mensaje. Las notas de voz nunca disparan una respuesta de "silencio" — un mensaje entrante vacío produce un mensaje saliente vacío.

## Descargas de medios

La interfaz `Downloader` es pequeña a propósito:

```go
type Downloader interface {
    Download(ctx context.Context, msg DownloadableAudio) (bytes []byte, mimetype string, err error)
}
```

Actualmente solo está cableada la descarga de audio. Las descargas de imagen y video están en la hoja de ruta — llegan como `waProto.ImageMessage` / `VideoMessage` y necesitarían una interfaz `DownloadableMedia` correspondiente. Sigue el plan en [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md).

## Indicadores de escritura

El handler envuelve cada respuesta en llamadas `SendPresence(Composing, Paused)` para que el remitente vea el indicador "…está escribiendo" mientras el modelo piensa. Ambas llamadas tienen un timeout de 5 segundos y son "best-effort" — un fallo de presencia nunca bloquea la propia respuesta.

## Modos de fallo

| Síntoma | Corrección |
|---|---|
| El QR se reimprime en cada reinicio | El emparejamiento fue revocado desde el teléfono; elimina `whatsapp.db` y empareja de nuevo. |
| Bucle de reconexión de WhatsApp | Comprueba la desviación de reloj contra `pool.ntp.org` — el handshake de whatsmeow es sensible al tiempo. |
| Mensajes entrantes ignorados | Verifica que el remitente esté en la lista `--allow`; revisa los logs para `router.transport.rejected`. |
| Meta bloquea el número | No lo ejecutes en un número personal. El protocolo es no oficial. |
| El "hello" de autoenvío no se enruta | El autoenvío usa LID; rousseau sustituye al JID de teléfono para la coincidencia de allowlist. Verifica que `ownID` esté inicializado — el servicio registra `whatsapp.connected` cuando lo está. |
| Notas de voz silenciosamente descartadas | O bien `whatsapp.voice.enabled: false` o falta el binario `whisper`. Línea de log: `whatsapp.audio_ignored`. |
| Cada respuesta me vuelve dos veces | La prevención de bucles está desactivada. Asegúrate de estar ejecutando un build reciente; la corrección aterrizó en `ResolveInbound` al principio del despliegue multi-dispositivo de whatsmeow. |

## Solución de problemas

### El QR se imprime pero la app del teléfono lo rechaza

Tres causas comunes: (1) un emparejamiento previo parcialmente completado dejó `whatsapp.db` en un estado que whatsmeow no puede reutilizar — elimina el archivo y vuelve a escanear; (2) el reloj está desviado más de 30 segundos (común en contenedores sin NTP) — comprueba con `timedatectl status`; (3) una versión antigua de `whatsmeow` puede haber perdido una actualización de protocolo de Meta.

### `whatsapp.connected` luego `whatsapp.disconnected` en bucle

Desviación de reloj, o Meta ha invalidado el emparejamiento. Comprueba los eventos `whatsapp.logged_out` en el log — esa es la señal definitiva.

### Las notas de voz llegan pero nunca se transcriben

El binario del transcriptor no es resolvible. Comprueba `whatsapp.voice.binary` y `whatsapp.voice.model_path` — ambos deben apuntar a archivos reales (o `binary` debe estar en `PATH`).

### El regex de la allowlist no coincide

La allowlist de rousseau es de cadena exacta, no regex. Para coincidir con un rango de remitentes, lista cada uno explícitamente o añade un router personalizado.

### El header de respuesta aparece como caracteres `*` literales

El cliente del destinatario no renderiza el Markdown de WhatsApp. Este es un problema de renderizado del lado del cliente; usa texto plano si tus destinatarios usan clientes antiguos.

## Páginas relacionadas

- [Primeros pasos: Tu primer transporte](/es/getting-started/first-transport/) — recorrido de principio a fin.
- [Guía de usuario: Modo voz](/es/user-guide/voice-mode/) — análisis profundo de notas de voz.
- [Configuración](/es/configuration/) — el bloque de configuración `whatsapp`.
- [Transportes](/es/transports/) — los otros ocho transportes.
- [Despliegue](/es/deployment/) — ejecutar WhatsApp en un contenedor Podman.

## Lectura adicional

- `internal/transport/whatsapp/client.go` — conexión, emparejamiento QR, bombeo de eventos.
- `internal/transport/whatsapp/resolve.go` — normalización LID/JID y manejo de autoenvío.
- `internal/transport/whatsapp/dispatch.go` — despacho de mensajes entrantes con ramificación de notas de voz.
- `internal/transport/whatsapp/whisper.go` — transcriptor whisper-cpp de referencia.
- `internal/cli/whatsapp.go` — cableado de CLI, DSN del almacén, selección de transcriptor.
