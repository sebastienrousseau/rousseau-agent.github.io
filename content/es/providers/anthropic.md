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
description: "Configure the direct Anthropic provider: ANTHROPIC_API_KEY, model IDs, max_tokens, prompt cache markers on the last messages, streaming."
keywords: "Anthropic, ANTHROPIC_API_KEY, Claude API, prompt caching, cache_control, ephemeral, streaming"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/providers/anthropic/"
subtitle: "Direct Anthropic API with ephemeral prompt-cache markers."
tags: "providers, anthropic"
title: "Proveedor Anthropic"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Anthropic, ANTHROPIC_API_KEY, Claude API, prompt caching, cache_control, ephemeral, streaming"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Proveedor Anthropic"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 7
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/anthropic/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/anthropic/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Proveedor Anthropic"
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
twitter_description: "Configure the direct Anthropic provider: ANTHROPIC_API_KEY, model IDs, max_tokens, prompt cache markers on the last messages, streaming."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Proveedor Anthropic"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Qué aprenderás</span><p>La forma exacta a nivel de cable de las solicitudes de Anthropic que envía rousseau, qué bloques de contenido reciben marcadores de caché de prompt y por qué, cómo el streaming se mapea a <code>agent.StreamingProvider</code> y los modos de fallo para respuestas 401/429/529. Lee <code>internal/llm/anthropic/client.go</code> e <code>internal/llm/anthropic/cache.go</code> junto a esta página.</p></aside>

## Cuándo usar el proveedor Anthropic

El proveedor `anthropic` directo es la elección correcta cuando:

- Tienes una clave de API de Anthropic y quieres facturación por token en `api.anthropic.com`.
- Quieres ejecución de herramientas del lado de rousseau (el `Registry` está completamente en juego).
- Quieres optar por marcadores de caché de prompt efímera en prefijos estables.
- Quieres completaciones por streaming en `rousseau chat` (actualizaciones del viewport token por token).
- Quieres límites de tasa explícitos y publicados (a diferencia del modo de suscripción `claudecli`).

## Configuración

```yaml
provider: anthropic

anthropic:
  api_key: sk-ant-...
  model: claude-sonnet-4-6
  max_tokens: 4096
```

| Campo | Por defecto | Efecto |
|---|---|---|
| `api_key` | *desde `ANTHROPIC_API_KEY`* | Bearer para `api.anthropic.com`. Se rechaza si está vacío cuando se selecciona el proveedor. |
| `model` | `claude-sonnet-4-6` | Identificador de modelo. |
| `max_tokens` | `4096` | Limita los tokens de salida por completación. |

La variable de entorno `ANTHROPIC_API_KEY` se enlaza a `anthropic.api_key` en el momento de la carga, por lo que exportarla es equivalente a configurarla. Los operadores de contenedores normalmente la exportan en la línea `Environment=` de la unidad de systemd en lugar de guardarla en `config.yaml`.

## Identificadores de modelo

`rousseau-agent` pasa `model` textualmente al SDK. Fija el ID de modelo exacto (`claude-sonnet-4-6`, `claude-opus-4-6`) en producción para que tu tráfico no cambie bajo tus pies cuando Anthropic promueva nuevos snapshots.

## Internos de caché de prompt

La caché de prompt efímera de Anthropic te permite marcar bloques de contenido con `cache_control: { type: "ephemeral" }`. La API cachea el prefijo hasta e incluyendo cualquier bloque marcado con caché; los turnos subsecuentes que carguen el mismo prefijo pagan una fracción del coste habitual de tokens de entrada (10% en el momento de escribir — consulta la documentación de Anthropic para precios actuales).

Rousseau aplica marcadores mediante `applyCacheMarkers` en `internal/llm/anthropic/cache.go`. Ocurren dos cosas cuando `CacheableMessages > 0` en la `Request` saliente:

1. **El system prompt recibe `cache_control: ephemeral`.** Sobrevive a cada turno, así que siempre vale la pena cachearlo una vez que optas por ello. Consulta las líneas 68–75 de `internal/llm/anthropic/client.go`.
2. **Los últimos `CacheableMessages` mensajes** reciben `cache_control: ephemeral` en su último bloque de texto. Esto mantiene barata una sesión creciente: a medida que se añaden nuevos turnos, el marcador flota hacia abajo del transcript, pero el prefijo hasta el marcador anterior sigue caliente.

### Qué bloques se marcan

`markLastTextBlock` recorre el contenido de un `MessageParam` hacia atrás y establece `CacheControl` en el primer bloque de texto que encuentra. Los bloques `tool_use` y `tool_result` se omiten — el SDK los modela como variantes distintas con sus propios campos opcionales `CacheControl`, y el texto es el denominador común seguro. Consulta `internal/llm/anthropic/cache.go`.

### Cuándo compensa

<aside class="admonition" data-type="note"><span class="admonition-title">Economía del caching</span><p>El punto de equilibrio depende de cuánto se reutiliza el prefijo cacheado. Para un transporte de chat que ejecuta 20–100 turnos por sesión con un system prompt de 5–10 kB (típico con skills cargados), habilitar el caching normalmente reduce a la mitad la factura de tokens de entrada. Para una tarea cron de una sola vez que genera una única respuesta, no ahorra nada.</p></aside>

El `Compressor` establece `CacheableMessages = len(recentMessages) - 1` tras una reescritura para que el bloque de resumen fresco esté caliente en la caché en el siguiente turno. Otras rutas de código dejan `CacheableMessages = 0`, lo que significa que el caching es opt-in por solicitud. Los integradores deben establecerlo explícitamente al llamar al proveedor directamente.

### Verificar aciertos de caché

La API de Anthropic devuelve `usage.cache_read_input_tokens` y `usage.cache_creation_input_tokens` en cada respuesta. `agent.Usage` actualmente expone solo `InputTokens` y `OutputTokens`, por lo que verificar la división requiere habilitar el logging de depuración o leer la respuesta bruta del SDK — es una brecha conocida de observabilidad rastreada en `docs/GAP_ANALYSIS_2026.md`.

## Semántica de streaming

El proveedor implementa `agent.StreamingProvider`. `rousseau chat` usa streaming por defecto para que los tokens lleguen al viewport del TUI a medida que se producen. Los transportes de chat (WhatsApp, Slack, Discord, …) usan completaciones sin streaming porque los transportes orientados a mensajes agrupan la entrega de todos modos — un flujo intermedio de deltas simplemente se descartaría antes de enviar el mensaje final.

La implementación de streaming en `internal/llm/anthropic/stream.go` consume la unión `MessageStreamEvent` del SDK:

| Evento | Cómo se maneja |
|---|---|
| `message_start` | Emite `agent.StreamEvent{Kind: StreamMessageStart}`. |
| `content_block_start` | Emite `agent.StreamEvent{Kind: StreamContentStart}` con el tipo de bloque. |
| `content_block_delta` | Emite `agent.StreamEvent{Kind: StreamTextDelta, Text: delta.Text}` para texto; los eventos `input_json_delta` se acumulan en una entrada parcial de uso de herramienta. |
| `content_block_stop` | Emite `agent.StreamEvent{Kind: StreamContentStop}`. |
| `message_delta` | Lleva el motivo de parada final y el uso acumulado. |
| `message_stop` | Fin del flujo. |

El TUI Bubble Tea se suscribe a estos eventos vía `agent.StreamTurn`, que orquesta el bucle de streaming/uso de herramienta. Consulta `internal/agent/stream_turn.go`.

## Uso de herramientas

Las definiciones de herramientas del `Registry` se convierten al array `tools` de Anthropic en `toSDKTools`. Las políticas de aprobación (`agent.approver`) aplican — cada bloque `tool_use` pasa por `Approver.Approve` en el bucle del agente antes de la ejecución. Las denegaciones se exponen al modelo como bloques `tool_result` con `is_error: true`, para que el modelo pueda adaptarse (elegir una acción distinta, preguntar al usuario, rendirse con elegancia).

<aside class="admonition" data-type="warning"><span class="admonition-title">Forma del esquema</span><p>El SDK espera que el <code>input_schema</code> de la herramienta sea un objeto JSON Schema con un campo <code>properties</code> de nivel superior. El <code>tools.Definition</code> de rousseau se mapea 1:1 — consulta <code>toSDKTools</code> en <code>internal/llm/anthropic/client.go</code>. Las herramientas personalizadas que emitan esquemas que no sean de objeto fallarán en el momento de la solicitud.</p></aside>

## Manejo de rate limits

La API de Anthropic devuelve:

| Código | Significado | Comportamiento de rousseau |
|---|---|---|
| 401 | Clave incorrecta o faltante | Falla inmediatamente, sin reintento. |
| 400 | Solicitud incorrecta (esquema, codificación, prompt demasiado largo) | Falla inmediatamente con el mensaje de error del SDK. |
| 429 | Límite de tasa por minuto excedido | Se expone como error `agent`. `Complete` no reintenta. |
| 529 | Sobrecargado (capacidad transitoria) | Se expone como error `agent`. `Complete` no reintenta. |
| 5xx | Error del servidor | Se expone como error `agent`. `Complete` no reintenta. |

**Los reintentos son responsabilidad del llamador.** El TUI `rousseau chat` y el `RouterHandler` del transporte actualmente no implementan backoff — un 429 mata el turno. Esta es una elección de diseño deliberada: los reintentos interactúan con la semántica de tool_use (llamadas parciales a herramientas, idempotencia), y el llamador tiene el contexto para tomar la decisión correcta. Consulta `docs/GAP_ANALYSIS_2026.md` para el helper de reintento planificado.

<aside class="admonition" data-type="tip"><span class="admonition-title">Manejo de 429 en un transporte de chat</span><p>Envuelve el <code>RouterHandler</code> del transporte en un bucle de reintento a nivel del llamador con backoff exponencial y jitter. La <a href="/es/guides/rate-limits/">guía de límites de tasa</a> muestra un ejemplo trabajado.</p></aside>

## Higiene de costes

- **Establece `max_tokens` bajo** (2048–4096) para transportes de chat donde las respuestas rara vez necesitan superar unos pocos párrafos. `max_tokens` es un tope, no un objetivo — solo pagas por la salida realmente generada.
- **Habilita `agent.compression`** para colapsar mensajes antiguos una vez que el transcript supere `trigger_messages` (60 por defecto). El resumen es mucho más barato que el transcript en bruto.
- **Usa `CacheableMessages > 0`** al incrustar la biblioteca del agente — la API directa es donde el caching de prompt más compensa.
- **Prefiere Sonnet para bucles de uso de herramientas.** Opus es más caro y más lento; a menos que hayas medido victorias en tu tarea concreta, Sonnet es el por defecto por una razón.
- **Cuidado con la facturación por aborto de flujo.** Si un flujo se cancela a mitad de la respuesta, la API aún factura por los tokens generados hasta el punto de cancelación. Establece un tope de timeout en tu llamador.

## Solución de problemas

### `anthropic: complete: 401 unauthorized`

Tu `ANTHROPIC_API_KEY` está ausente, revocada o establecida a un workspace/organización al que ya no tienes acceso. Verifica con `curl -H "x-api-key: $ANTHROPIC_API_KEY" https://api.anthropic.com/v1/messages`.

### `anthropic: complete: 400 messages: too many messages`

El transcript creció más allá de la ventana de contexto. Habilita `agent.compression.enabled: true` (los valores por defecto suelen estar bien) y vuelve a ejecutar. Si la compresión está activada y aún se dispara, baja `trigger_messages` o aumenta `keep_recent` para que el compresor se active antes.

### `anthropic: unsupported content block <type>`

El SDK devolvió un tipo de bloque de contenido que rousseau no modela — actualmente solo se admiten `text` y `tool_use` (consulta `fromSDKResponse`). Esto puede ocurrir si el modelo emite bloques `thinking` (modo de pensamiento extendido). rousseau aún no los expone; deshabilita el pensamiento extendido en tu configuración de proveedor hasta que aterrice el soporte.

### 429 bajo carga sostenida

Estás alcanzando el límite de tasa de tokens de salida por minuto. Opciones: (1) solicitar un aumento de límite a Anthropic, (2) encolar turnos en el llamador y procesarlos en serie, (3) cambiar a Bedrock o Vertex donde las cuotas empresariales suelen ser mayores.

### Fallos de caché de prompt a pesar de `CacheableMessages > 0`

Anthropic invalida la caché cuando el prefijo cambia. Causas comunes: el system prompt se regenera por turno (skills que cambian con cada mensaje del usuario), el ID del modelo cambió, o `MaxTokens` difiere. Registra el payload de la solicitud y compáralo entre dos turnos para aislar.

## Páginas relacionadas

- [Proveedores: claudecli](/es/providers/claudecli/) — contrapartidas entre subproceso y API directa.
- [Proveedores: Bedrock](/es/providers/bedrock/) — Claude gestionado por AWS con cuotas empresariales.
- [Guías: Límites de tasa](/es/guides/rate-limits/) — el manual de reintento y backoff.
- [Bucle del agente](/es/agent-loop/) — cómo se componen el streaming y el uso de herramientas.
- [Guía de usuario: Compresión y recuperación](/es/user-guide/compression-recall/) — el mecanismo que mantiene sano el recuento de tokens de entrada.

## Lectura adicional

- `internal/llm/anthropic/client.go` — `Complete`, conversión de mensajes, esquema de herramientas.
- `internal/llm/anthropic/stream.go` — implementación de streaming.
- `internal/llm/anthropic/cache.go` — helper de marcador de caché.
- `internal/agent/stream_turn.go` — cómo el bucle del agente consume eventos de streaming.
- `internal/agent/compressor.go` — cómo el compresor prepara `CacheableMessages`.
