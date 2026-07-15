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
description: "Bubble Tea TUI keybindings, panels, spinner and streaming semantics for rousseau-agent's rousseau chat command."
keywords: "tui, bubble tea, keybindings, viewport, textarea, spinner, streaming, session"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/user-guide/tui/"
subtitle: "Bubble Tea keybindings, panels, streaming."
tags: "tui, bubble-tea, keybindings"
title: "TUI"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tui, bubble tea, keybindings, viewport, textarea, spinner, streaming, session"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "TUI"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/tui/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/tui/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "TUI"
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
twitter_description: "Bubble Tea TUI keybindings, panels, spinner and streaming semantics for rousseau-agent's rousseau chat command."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "TUI"
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

`rousseau chat` abre una TUI de Bubble Tea con tres regiones:

```
+------------------------------------------------------+
|                       Encabezado                     |  título de sesión
+------------------------------------------------------+
|                                                      |
|                                                      |
|                     Viewport                         |  historial con scroll
|      (mensajes, vista previa de respuesta streaming) |
|                                                      |
|                                                      |
+------------------------------------------------------+
|                     Textarea                         |  entrada, Enter para enviar
+------------------------------------------------------+
| estado: idle | spinner | streaming | error           |
+------------------------------------------------------+
```

Se ejecuta en modo alt-screen de Bubble Tea: la TUI toma el buffer de la terminal y lo restaura al salir.

## Atajos de teclado

La TUI de rousseau mantiene el conjunto de bindings pequeño. Ante la duda, aplican los atajos estándar de viewport / textarea de Bubble Tea.

### Globales

| Tecla | Acción |
|---|---|
| `Ctrl+C` | Salir. Guarda la sesión actual, no imprime nada al salir. |
| `Esc` | Salir. Igual que `Ctrl+C`. |
| `Enter` | Envía el contenido actual del textarea. No-op mientras el agente está ocupado. |

### Textarea (entrada)

Comportamiento estándar del textarea de Bubble Tea:

| Tecla | Acción |
|---|---|
| Cualquier carácter imprimible | Inserta en el cursor. |
| `Backspace` | Elimina el carácter antes del cursor. |
| `Delete` | Elimina el carácter bajo el cursor. |
| Flechas | Mueven el cursor. |
| `Home` / `End` | Salta al inicio / fin de línea. |
| `Ctrl+A` / `Ctrl+E` | Salta al inicio / fin de línea (bindings estilo Emacs). |
| `Ctrl+U` | Elimina hasta el inicio de línea. |
| `Ctrl+K` | Elimina hasta el fin de línea. |
| `Shift+Enter` | (Depende del terminal) salto de línea sin enviar; a menudo mapeado como `\n` literal. |

El textarea crece verticalmente conforme el contenido se ajusta; el viewport se encoge para acomodar.

### Viewport (historial)

El viewport soporta los atajos usuales de viewport de Bubble Tea. El foco está en el viewport cuando el textarea está vacío; escribir enruta al textarea automáticamente.

| Tecla | Acción |
|---|---|
| `PgUp` / `PgDn` | Scroll de una página. |
| `↑` / `↓` | Scroll de una línea. |
| `Home` / `End` | Salta al inicio / final. |
| Rueda del ratón | Scroll. |

## Semántica de paneles

### Encabezado

`rousseau · <título de sesión>`. El título viene de `--title` cuando se creó la sesión (por defecto: `chat YYYY-MM-DD HH:MM`).

### Viewport

Historial renderizado más, mientras un turno está en vuelo, una **vista previa en streaming** en la parte inferior. La vista previa refleja los deltas mientras el proveedor hace streaming; cuando el turno termina, la vista previa se reemplaza por el mensaje final del asistente.

Cada mensaje está prefijado por su rol (`tú`, `rousseau`, `tool`) para que el flujo sea inequívoco cuando el modelo solicita una llamada a herramienta.

### Textarea

Texto placeholder: `Ask, or press Ctrl+C to quit…`. Enter envía; el textarea se reinicia al enviar.

Mientras el agente está ocupado, `Enter` es un no-op para que los envíos dobles accidentales no apilen turnos.

### Línea de estado

Debajo del textarea. El contenido varía:

| Estado | Línea |
|---|---|
| Idle | Vacía. |
| Ocupado | Spinner + `thinking…`. Los ticks del spinner vienen de `bubbles/spinner`. |
| Streaming | El spinner continúa; el delta de streaming aparece en la vista previa del viewport. |
| Error | Cadena de error en rojo. El siguiente turno exitoso la limpia. |

## Persistencia de sesión

Cada turno se persiste en `~/.local/share/rousseau/sessions.db` vía `state.Store.Save`. Si el daemon se cae a mitad de turno:

- El turno del usuario ya está guardado (se añadió antes de que se disparara `doTurn`).
- La respuesta del asistente solo se guarda una vez que el turno se completa.

Al reiniciar, `rousseau chat --session <id>` retoma desde el último estado guardado exitosamente.

## Comandos de sesión desde el CLI

La TUI no expone cada operación de sesión. Gestiona sesiones desde una shell:

```sh
rousseau session list
rousseau session show <id>
rousseau session search "kubectl"
rousseau session delete <id>
```

## Semántica de streaming

Los proveedores que implementan `StreamingProvider.ChatStream` (Anthropic, `claudecli`) hacen streaming de deltas a la vista previa del viewport. Los proveedores que solo implementan `Provider.Chat` (Bedrock, Vertex, compatible con OpenAI dependiendo del shim) entregan la respuesta como un único bloque al completarse el turno: la vista previa queda vacía y la respuesta aparece cuando `busy` se vuelve `false`.

## Cuando las cosas van mal

- **La TUI se cuelga**: `Ctrl+C` dos veces. El primer `Ctrl+C` señaliza `tea.Quit`, que flushea el estado. El segundo lo captura el SO.
- **El viewport está vacío y el textarea no acepta entrada**: la alt-screen puede haber sido corrompida por un subproceso que emite secuencias de escape (p. ej. una llamada a herramienta que imprime códigos ANSI). Reinicia la TUI.
- **La línea de estado se queda en `thinking…`**: el proveedor no ha retornado. Revisa el stderr del daemon (rousseau escribe slog a stderr; si lo redirigiste, hazlo visible de nuevo).

## Siguiente

- [Guía de usuario: CLI](/es/user-guide/cli/): cada comando fuera de la TUI.
- [Conceptos](/es/concepts/): el bucle del agente subyacente.
- [Compresión + Recall](/es/user-guide/compression-recall/): cómo se mantienen usables los chats largos.
