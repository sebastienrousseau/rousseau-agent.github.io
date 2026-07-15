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
description: "Transcribe WhatsApp voice notes to text with whisper.cpp before feeding them into the rousseau-agent agent loop. Opt-in; whisper.cpp not shipped in the container."
keywords: "voice notes, whisper.cpp, transcription, whatsapp, opt-in, audio"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/user-guide/voice-mode/"
subtitle: "Whisper-backed voice-note transcription for WhatsApp."
tags: "voice, whisper, whatsapp, transcription"
title: "Modo voz"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "voice notes, whisper.cpp, transcription, whatsapp, opt-in, audio"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Modo voz"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/voice-mode/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/voice-mode/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Modo voz"
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
twitter_description: "Transcribe WhatsApp voice notes to text with whisper.cpp before feeding them into the rousseau-agent agent loop. Opt-in; whisper.cpp not shipped in the container."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Modo voz"
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

## Qué hace el modo voz

Cuando el transporte de WhatsApp recibe una nota de voz, rousseau invoca un CLI de `whisper.cpp` instalado localmente para transcribir el audio a texto, y luego alimenta ese texto al bucle del agente como si el usuario lo hubiera tecleado. La respuesta vuelve como un mensaje de texto normal de WhatsApp.

La ruta vive en `internal/transport/whatsapp/whisper.go`. Todos los demás transportes son solo texto hoy.

**Opt-in.** El modo voz está desactivado por defecto, y `whisper.cpp` no se incluye en la imagen de contenedor de rousseau — instalas y configuras el CLI tú mismo, luego activas un único flag de configuración.

## Requisitos previos

- Un bridge `rousseau whatsapp` funcionando ([Primer transporte](/es/getting-started/first-transport/)).
- El CLI de `whisper.cpp` en el `$PATH` del demonio. Nombres de binario habituales: `whisper`, `whisper-cli`, `whisper-cpp`.
- Un archivo de modelo. `base.en` es un buen punto de partida para notas en inglés; los modelos más grandes intercambian latencia por precisión.

## Instalación de whisper.cpp

Whisper.cpp vive en [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp). Receta de build (en el host, no en el contenedor):

```sh
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp
make -j
bash ./models/download-ggml-model.sh base.en
sudo install -m 0755 main /usr/local/bin/whisper
sudo install -m 0644 models/ggml-base.en.bin /usr/local/share/whisper/ggml-base.en.bin
```

El nombre del binario tras `install` es `whisper`; la búsqueda por defecto del binario de rousseau espera ese nombre.

## Habilitar en la configuración

```yaml
whatsapp:
  reply_header: "💎 *Rousseau Agent*\n\n"
  voice:
    enabled: true
    binary: whisper                                # opcional; por defecto "whisper"
    model_path: /usr/local/share/whisper/ggml-base.en.bin
    language: en                                   # opcional; vacío auto-detecta
    extra_args: []                                 # se añaden antes del nombre del archivo de entrada
```

Cada campo en `VoiceConfig` (`internal/config/config.go`):

| Campo | Tipo | Por defecto | Notas |
|---|---|---|---|
| `enabled` | bool | `false` | Desactivado por defecto. |
| `binary` | string | `whisper` | El CLI a invocar. Puede ser `whisper-cli`, `whisper-cpp`, etc. |
| `model` | string | — | Se pasa a `--model` (p. ej. `base.en`, `small`, `medium`). Aplica la resolución por defecto de Whisper. |
| `model_path` | string | — | Ruta `.bin` explícita. **Tiene precedencia sobre `model`.** |
| `language` | string | — | Se pasa a `--language`. Vacío auto-detecta (más lento). |
| `extra_args` | []string | — | Se añaden antes del nombre del archivo de entrada. |

## Qué hace el daemon en cada nota de voz

1. WhatsApp entrega un mensaje de audio (Opus / OGG / MP3 / M4A / AAC / WAV: la extensión se infiere del mimetype).
2. Rousseau escribe el payload a un archivo temporal: `/tmp/rousseau-whisper-XXXX/input.<ext>` con permiso `0o600`.
3. Invoca:
   ```
   whisper --output-txt --output-file /tmp/rousseau-whisper-XXXX/output [--model <path>] [--language <lang>] <extra_args...> <input.ext>
   ```
4. Lee `/tmp/rousseau-whisper-XXXX/output.txt` (con fallback a `<input>.txt` para variantes de whisper.cpp que escriben junto al input).
5. Alimenta el texto transcrito al bucle del agente como el turno del usuario.
6. El directorio temporal se limpia con `os.RemoveAll` (diferido).

## Verificar con `rousseau doctor`

```sh
rousseau doctor
```

Busca:

```
✔ whatsapp.voice.binary     /usr/local/bin/whisper
```

o cuando está desactivado:

```
· whatsapp.voice           disabled
```

Un `fail` en `whatsapp.voice.binary` significa `enabled: true` pero el CLI no está en el `$PATH` del daemon. Arregla la instalación o desactívalo.

## Prueba end-to-end

1. Habilita voice en la configuración, reinicia `rousseau whatsapp`.
2. Desde tu teléfono, graba una nota de voz corta ("¿qué hace el archivo main.go?") y envíala.
3. Observa el log del daemon:
   ```
   whatsapp.voice_enabled binary=whisper model=/usr/local/share/whisper/ggml-base.en.bin
   ```
4. El daemon responde con una respuesta de texto a la pregunta transcrita.

## Notas de latencia

Whisper es CPU-bound por defecto. Latencias aproximadas para una nota de voz de 10 segundos en una laptop moderna:

| Modelo | Latencia CPU aprox. |
|---|---|
| `tiny.en` | ~1s |
| `base.en` | ~3s |
| `small.en` | ~8s |
| `medium.en` | ~25s |

Si compilas whisper.cpp con `WHISPER_COREML=1` (macOS) o `WHISPER_CUBLAS=1` (Linux + NVIDIA), la transcripción puede ser 2–10x más rápida. A rousseau no le importa: solo hace shell out.

## Advertencias sobre contenedores

La imagen de contenedor de rousseau (`docker/Dockerfile`) **no** incluye `whisper.cpp`. Si quieres modo voz dentro del contenedor, extiende la imagen:

```dockerfile
# Añadir sobre el Dockerfile de referencia
RUN apk add --no-cache build-base git && \
    git clone https://github.com/ggerganov/whisper.cpp /tmp/whisper && \
    make -C /tmp/whisper -j && \
    mkdir -p /usr/local/share/whisper && \
    /tmp/whisper/models/download-ggml-model.sh base.en /usr/local/share/whisper && \
    install -m 0755 /tmp/whisper/main /usr/local/bin/whisper && \
    rm -rf /tmp/whisper
```

O haz bind-mount de `whisper` y el modelo desde el host en la unidad Quadlet.

## Errores expuestos a slog

| Evento | Significado |
|---|---|
| `whisper: empty audio payload` | El transporte entregó un mensaje de audio de cero bytes. Omitido. |
| `whisper: temp dir: <err>` | `/tmp` no es escribible. Comprueba el mount `Tmpfs=/tmp:rw` del contenedor. |
| `whisper: write audio: <err>` | Disco lleno o permiso denegado. |
| `whisper: run <binary>: <err>: <stderr excerpt>` | El CLI salió con no-cero. El extracto se trunca a 400 caracteres. |
| `whisper: read transcript: <err>` | Whisper se ejecutó pero no produjo el archivo `.txt` esperado. A menudo una variante de whisper.cpp que escribe en una ruta diferente. |

## Notas de privacidad

La transcripción se ejecuta **completamente en el host**. El audio nunca sale del daemon. Si intercambias el CLI por un servicio de transcripción hospedado (fuera del alcance del código distribuido), asumes el flujo de datos de ese proveedor: verifica contra tu propia [postura de privacidad](/es/privacy/).

## Siguiente

- [Transporte WhatsApp](/es/transports/whatsapp/): la referencia del transporte.
- [Configuración](/es/configuration/): cada campo en `internal/config/config.go`.
- [Despliegue](/es/deployment/): cómo hacer bind-mount de whisper en el contenedor.
