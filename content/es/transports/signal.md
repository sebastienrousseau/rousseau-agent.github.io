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
description: "Set up rousseau-agent's Signal transport: signal-cli subprocess in JSON-RPC mode, account registration out-of-band, E.164 allowlist, extra_args knob."
keywords: "Signal, signal-cli, JSON-RPC, subprocess, E.164, account registration, linked device"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/transports/signal/"
subtitle: "signal-cli subprocess in JSON-RPC daemon mode."
tags: "transports, Signal"
title: "Transporte Signal"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Signal, signal-cli, JSON-RPC, subprocess, E.164, account registration, linked device"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transporte Signal"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 13
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/signal/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/signal/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transporte Signal"
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
twitter_description: "Set up rousseau-agent's Signal transport: signal-cli subprocess in JSON-RPC mode, account registration out-of-band, E.164 allowlist, extra_args knob."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transporte Signal"
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

El transporte de Signal (`internal/transport/signal/`) delega en `signal-cli` (https://github.com/AsamK/signal-cli) en su modo daemon JSON-RPC.

`signal-cli --output=json -a <account> jsonRpc` transmite JSON-RPC 2.0 sobre stdin/stdout: las solicitudes salientes `send` entregan mensajes; las entradas llegan como notificaciones `receive`.

## Requisitos previos

Deben cumplirse dos condiciones antes de que rousseau pueda comunicarse con Signal:

1. **`signal-cli` en `$PATH`** (o un valor explícito en la configuración `binary`).
2. **Cuenta registrada o vinculada fuera de banda.**

El registro de la cuenta queda deliberadamente fuera del alcance de rousseau. Dos rutas admitidas (según la documentación de `signal-cli`):

- **Registrar un número nuevo.** `signal-cli register` inicia la verificación por SMS o voz. Complétala con `signal-cli verify <code>`. El número queda controlado por el servicio.
- **Vincular como dispositivo secundario.** `signal-cli link` imprime un URI `tsdevice://`; escanéalo en la aplicación móvil de Signal en **Ajustes → Dispositivos vinculados**. El número sigue controlado por el teléfono; el servicio actúa como secundario.

Ambos flujos persisten el estado en `~/.local/share/signal-cli/`. Móntalo en el contenedor con bind-mount si lo despliegas bajo Podman.

## Configuración

```yaml
signal:
  binary: signal-cli
  account: "+447900123456"
  extra_args:
    - --verbose
  reply_header: "*Rousseau Agent*\n\n"
  allowlist:
    - "+447900654321"
```

| Campo | Predeterminado | Efecto |
|---|---|---|
| `binary` | `signal-cli` | Ejecutable que se invoca. |
| `account` | *requerido* | Número telefónico E.164 con el que se ejecuta el servicio. |
| `extra_args` | `[]` | Se insertan entre `-a <account>` y `jsonRpc`. Útil para `--config <path>` y `--verbose`. |
| `reply_header` | *vacío* | Se antepone a cada respuesta saliente. |
| `allowlist` | `[]` | Números E.164 cuyos mensajes se procesan. Vacío acepta a todo remitente. |

## Línea de comandos

```sh
rousseau signal --account +447900123456 --allow +447900654321
```

Los flags reflejan el bloque de configuración. `--allow` puede repetirse.

## Flujo de mensajes

- **Entrada.** `signal-cli` emite una notificación JSON-RPC `receive` por cada mensaje que llega. rousseau la analiza, descarta todo lo que no esté en la allowlist y entrega el cuerpo al `Handler`.
- **Salida.** rousseau escribe una solicitud JSON-RPC `send` en el stdin de `signal-cli`. Los ACK de entrega llegan por el mismo canal.

## Tiempos de espera

El transporte no impone su propio timeout al subproceso. La capa de red de `signal-cli` gestiona las reconexiones al servidor de Signal. Si el proceso finaliza, rousseau no lo reiniciará; una directiva systemd `Restart=on-failure` (que el Quadlet de referencia ya configura) reinicia todo el servicio rousseau, arrastrando consigo a `signal-cli`.

## Modos de fallo

| Síntoma | Solución |
|---|---|
| `signal-cli` se cierra inmediatamente | La cuenta no está registrada ni vinculada. Completa el registro fuera de banda. |
| Nunca llegan notificaciones `receive` | Verifica que la cuenta no esté vinculada en otra ubicación que esté consumiendo la cola. |
| Errores de análisis JSON incorrecto | Confirma que tu versión de `signal-cli` sea 0.13 o superior. Las versiones antiguas usaban un envoltorio distinto. |
