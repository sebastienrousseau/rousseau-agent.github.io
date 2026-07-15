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
description: "Hot-swap the underlying model mid-session by editing config.yaml and restarting the daemon — the SQLite session store survives."
keywords: "model swap, hot swap, mid-session, restart, session store, sonnet, opus, haiku"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/guides/rate-model-swap/"
subtitle: "Swap Sonnet for Opus mid-session; the session store survives the restart."
tags: "guides, model, swap, restart, session"
title: "Guía: cambio de modelo en caliente"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "model swap, hot swap, mid-session, restart, session store, sonnet, opus, haiku"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guía: cambio de modelo en caliente"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/rate-model-swap/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/rate-model-swap/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guía: cambio de modelo en caliente"
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
twitter_description: "Hot-swap the underlying model mid-session by editing config.yaml and restarting the daemon — the SQLite session store survives."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guía: cambio de modelo en caliente"
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

## Por qué funciona

Rousseau lee su proveedor y modelo desde `config.yaml` una sola vez al arrancar el proceso (`config.Load` en `internal/config/config.go`). El estado de sesión vive en SQLite. Cambiar el modelo significa editar la configuración, reiniciar el daemon y dejar que el próximo mensaje entrante sea manejado por el nuevo modelo, mientras cada sesión en la que participó el modelo anterior permanece intacta en `sessions.db`.

Nada del almacén de sesiones está atado a un modelo específico. La columna `payload` (`internal/state/sqlite/schema.sql`) es un blob JSON plano de `agent.Session`; rol, contenido, bloques de tool-use. Cualquier modelo que hable la convención de bloques de contenido de Anthropic (o esté adaptado a través de los adaptadores del SDK en `internal/llm/*/client.go`) puede retomar donde el anterior lo dejó.

## Cambio dentro del mismo proveedor

El caso fácil. Edita el campo del modelo:

```yaml
# antes:
anthropic:
  model: claude-sonnet-4-6

# ahora:
anthropic:
  model: claude-opus-4-6
```

Reinicia:

```sh
systemctl --user restart rousseau-agent
# o, si ejecutas rousseau chat interactivamente, sal y relanza
```

Envía el siguiente mensaje. La respuesta viene de Opus; el contexto de sesión no ha cambiado.

## Cambio entre proveedores

Ligeramente más involucrado porque las formas de bloques de contenido varían. Los adaptadores de rousseau (`internal/llm/anthropic/client.go`, `internal/llm/openai/client.go`) hacen round-trip de valores `agent.Message` a través de los tipos nativos del SDK en cada turno. Eso significa:

- **`claudecli` → `anthropic`**: cambio limpio. Ambos usan la misma forma de bloque de contenido.
- **`claudecli` → `bedrock` / `vertex`**: cambio limpio. Anthropic-en-Bedrock y Anthropic-en-Vertex hablan el mismo formato de mensajes.
- **Familia Anthropic → `openai` / `openrouter` / `ollama`**: los bloques de tool-use se reforman al formato function-call de OpenAI. Los pares previos tool_use / tool_result en la sesión hacen round-trip por el adaptador. Debería ser fluido para texto; los casos límite (multi-tool-use en un solo turno, parciales de streaming) pueden renderizarse diferente.

Si la sesión tiene historial pesado de tool-use y cruzas familias de proveedor, prueba primero con una sesión nueva.

## Cambiar el proveedor de despliegue sin tocar el estado

Mismo almacén de sesiones, diferente configuración del daemon:

```sh
cp ~/.config/rousseau/config.yaml ~/.config/rousseau/config.yaml.bak
$EDITOR ~/.config/rousseau/config.yaml   # cambia proveedor + modelo
systemctl --user restart rousseau-agent
```

`state.path` no cambió, por lo que el mapeo JID→sesión (tabla `jid_sessions` en `internal/state/sqlite/jidmap.go`) sigue apuntando al mismo historial de conversación para cada remitente de WhatsApp / Slack / Matrix.

## Qué se preserva

| Estado | Sobrevive al reinicio | Notas |
|---|---|---|
| Transcripciones de sesión | Sí | Tabla `sessions`. |
| Índice de recall FTS5 | Sí | Tabla virtual `sessions_fts`. Retokenizada en el backfill. |
| Mapeo JID → sesión | Sí | Tabla `jid_sessions`. |
| Trabajos cron | Sí | Tabla `cron_jobs`. |
| Emparejamiento del dispositivo de WhatsApp | Sí | `whatsapp.db` (archivo separado). |
| Hit del caché de prompt de Anthropic | **No** | El caché es por endpoint. Un nuevo modelo o endpoint arranca frío. |

## Qué se pierde

Los marcadores de caché de prompt de Anthropic (`applyCacheMarkers` en `internal/llm/anthropic/client.go`) viven dentro del caché efímero del modelo: no persisten entre reinicios del modelo o proveedor. Los siguientes turnos después de un cambio pagan tokens de entrada completos; los turnos posteriores reconstruyen el caché. Vale la pena saberlo para presupuestar costos pero no para corrección.

## Cuándo cambiar vs. empezar de cero

Cambia en el lugar cuando:

- La sesión merece preservarse y el contenido es pesado en texto.
- Los modelos están en la misma familia (ambos Anthropic, o vía Bedrock/Vertex).
- Aceptas un miss de caché puntual.

Empieza de cero cuando:

- La sesión tiene contexto obsoleto que no quieres que un modelo más inteligente persiga.
- Estás cruzando familias de proveedores y quieres comportamiento determinista.
- El conteo de tokens ya está en el disparador de compresión: comprime y cambia de una vez.

## Pruebas tras un cambio

```sh
rousseau session list | head -3
rousseau session show <id> | tail -20
# en la TUI o vía un transporte:
> ¿qué acabamos de decidir sobre X?
```

Si la respuesta hace referencia a la conversación previa de forma coherente, el cambio está funcionando. Si el modelo se disculpa por "no tener contexto" o se repite, el round-trip del adaptador puede estar perdiendo metadatos de tool-use: reporta el bug o vuelve al modelo anterior.

## Relacionado

- [Proveedores](/es/providers/): cada proveedor soportado.
- [Configuración](/es/configuration/): los nombres exactos de los campos.
- [Guías: Rate limits](/es/guides/rate-limits/): discusión de marcadores de caché.
- [Guías: Gestión de sesiones](/es/guides/session-management/): ciclo de vida completo.
