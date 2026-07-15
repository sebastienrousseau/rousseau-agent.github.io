---

# Front Matter (YAML)

author: "sebastian.rousseau@gmail.com (Sebastien Rousseau) "
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
description: "How the LLM compressor decides what to keep, the roles of trigger_messages and keep_recent, and a before/after diagram of a compressed session."
keywords: "compression, context, keep_recent, trigger_messages, summariser, marker"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/guides/context-management/"
subtitle: "trigger_messages, keep_recent, and the compressed-marker convention."
tags: "guides, context, compression, summariser"
title: "Guía: gestión de contexto"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "compression, context, keep_recent, trigger_messages, summariser, marker"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guía: gestión de contexto"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/context-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/context-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guía: gestión de contexto"
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
twitter_description: "How the LLM compressor decides what to keep, the roles of trigger_messages and keep_recent, and a before/after diagram of a compressed session."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guía: gestión de contexto"
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

## El problema

Una sesión que se ejecuta durante semanas acumula cientos de mensajes. Cada uno se reenvía al proveedor en cada turno. El costo crece linealmente con la cantidad de turnos; la latencia también crece. El `LLMCompressor` de rousseau (`internal/agent/compressor.go`) intercambia un pequeño costo puntual (una llamada de resumen por compresión) por ahorros permanentes en cada turno posterior.

La compresión está **desactivada por defecto** porque el despliegue de referencia usa `claudecli` en un nivel de suscripción, donde no se factura el conteo de tokens. Actívala cuando ejecutes contra Anthropic direct, Bedrock, Vertex o proveedores compatibles con OpenAI de pago por token.

## Las perillas

De `CompressionConfig` en `internal/config/config.go`:

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60        # cero usa el default 60
    keep_recent: 8              # cero usa el default 8
    prompt: ""                  # sobrescribe el prompt de resumen por defecto
```

Significados:

| Campo | Qué hace |
|---|---|
| `enabled` | Activa la compresión. Cuando es false, el agente usa `NoopCompressor` y toda esta sección es un no-op. |
| `trigger_messages` | La compresión se dispara una vez que `len(session.Messages) >= trigger_messages`. |
| `keep_recent` | Número de mensajes más recientes preservados textualmente tras la compresión. |
| `prompt` | Sobrescribe el prompt de resumen por defecto. Ajústalo solo si necesitas instrucciones personalizadas (p. ej. preservar salida JSON, siempre citar rutas de archivos). |

## El prompt de resumen por defecto

```
Summarise the following conversation in <=200 words. Preserve every
commitment, TODO, credential, filename, and quoted output. Skip
pleasantries. Return only the summary — no preamble.
```

Definido como `defaultSummaryPrompt` en `internal/agent/compressor.go`. Sobrescribe con `agent.compression.prompt` en `config.yaml`.

## Antes / después

Una sesión de 68 mensajes, `trigger_messages: 60`, `keep_recent: 8`:

```
Antes de la compresión:                    Después de la compresión:

┌──────────────────────────┐              ┌──────────────────────────────┐
│ msg[0]  user             │              │ msg[0]  user (sintético)     │
│ msg[1]  assistant        │              │   [rousseau-compressed]      │
│ msg[2]  user             │              │   (resumen de los 60         │
│  …  (60 mensajes)        │      →       │    mensajes previos): …      │
│ msg[59] assistant        │              ├──────────────────────────────┤
├──────────────────────────┤              │ msg[1]  user       — literal │
│ msg[60] user   literal   │              │ msg[2]  assistant  — literal │
│ msg[61] assistant        │              │ msg[3]  user       — literal │
│  …                       │              │ msg[4]  assistant  — literal │
│ msg[67] assistant        │              │ msg[5]  user       — literal │
└──────────────────────────┘              │ msg[6]  assistant  — literal │
                                          │ msg[7]  user       — literal │
                                          │ msg[8]  assistant  — literal │
                                          └──────────────────────────────┘
Total de mensajes: 68                     Total de mensajes: 9
Tokens de entrada: ~5000 por turno        Tokens de entrada: ~800 por turno
```

## El marcador

El compresor prefija el mensaje sintético del usuario con `[rousseau-compressed]` (constante `DefaultCompressorMarker` en `internal/agent/compressor.go`). En turnos posteriores, `headAlreadyCompressed()` usa el marcador para detectar un prefijo ya comprimido y salta la recompresión salvo que la sesión haya crecido a `2 * trigger_messages`.

Esto es lo que mantiene la compresión acotada: no pagas por re-resumir el resumen cada 60 mensajes.

## Elección de valores

| Situación | Recomendado |
|---|---|
| Daemon de transporte de larga duración en un proveedor de pago. | `trigger_messages: 60`, `keep_recent: 8`. Los defaults están afinados para esto. |
| TUI interactiva donde quieres todo en contexto. | `enabled: false`. |
| Sesiones altamente técnicas con mucho código / logs citados. | `trigger_messages: 40`, `keep_recent: 12`. Preserva más contexto reciente; comprime antes. |
| Resumidor batch crítico en costo (cron). | Cada ejecución cron es una sesión nueva, por lo que la compresión rara vez se dispara. Deja los defaults activados. |

## Costo de una pasada de compresión

Una llamada de resumen por disparo. El Provider usado es el que selecciona `Config.Provider`: el mismo que usa el agente. Eso significa:

- Llamada de compresor clase Sonnet: ~1-2 segundos, aproximadamente el costo de ~2 turnos de tokens de entrada.
- Punto de equilibrio tras ~5-10 turnos posteriores dependiendo de la forma de la sesión.

Para un compresor más barato, ejecuta rousseau en el patrón multi-proveedor de dos daemons con un modelo clase Haiku para el daemon compresor. Consulta [Guías: Multi-proveedor](/es/guides/multi-provider/).

## Emergencia: la sesión es demasiado grande para cargar

Si el payload de una sesión crece más allá de la ventana de contexto del modelo antes de que se dispare la compresión (raro pero posible con un `trigger_messages` muy pequeño y salidas de herramientas grandes), el siguiente turno fallará con un error "context length exceeded" del proveedor. Recuperación:

```sh
rousseau session delete <id> --yes
```

Luego empieza de nuevo. O reduce manualmente vía SQLite:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
UPDATE sessions SET payload = json_set(payload, '$.messages',
  json_extract(payload, '$.messages[-8:]'))
WHERE id = '<session-id>';
SQL
```

Nota: la sintaxis exacta de rutas JSON depende de la versión de SQLite. Confirma con un `SELECT payload` primero.

## Relacionado

- [Guía de usuario: Compresión + Recall](/es/user-guide/compression-recall/): referencia más profunda.
- [Guías: Rate limits](/es/guides/rate-limits/): implicaciones de costo.
- [Guías: Gestión de sesiones](/es/guides/session-management/): ciclo de vida de sesión.
- [Referencia: Esquema de configuración](/es/reference/config-schema/): cada campo.
