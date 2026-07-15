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
description: "Configure OpenAI-compatible endpoints: OpenAI, OpenRouter, Ollama, self-hosted vLLM or LM Studio. BaseURL, model naming, streaming, and Ollama's not-required key."
keywords: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, base_url, chat completions, API key, streaming"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/providers/openai-compatible/"
subtitle: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, and any Chat Completions clone."
tags: "providers, openai, openrouter, ollama"
title: "Proveedor compatible con OpenAI"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, base_url, chat completions, API key, streaming"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Proveedor compatible con OpenAI"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 10
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/openai-compatible/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/openai-compatible/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Proveedor compatible con OpenAI"
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
twitter_description: "Configure OpenAI-compatible endpoints: OpenAI, OpenRouter, Ollama, self-hosted vLLM or LM Studio. BaseURL, model naming, streaming, and Ollama's not-required key."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Proveedor compatible con OpenAI"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Qué aprenderás</span><p>Cómo el proveedor <code>openai</code> de rousseau sirve seis endpoints diferentes (OpenAI, OpenRouter, Ollama, vLLM, LM Studio, LiteLLM) a través de una única implementación, el valor exacto de <code>base_url</code> y <code>model</code> para cada uno, y qué endpoints admiten uso de herramientas. Lee <code>internal/llm/openai/client.go</code> junto a esta página.</p></aside>

## Una implementación, muchos endpoints

`internal/llm/openai/` habla la API OpenAI Chat Completions. Como `base_url` es configurable, el mismo código sirve a cada endpoint compatible con OpenAI: la propia OpenAI, OpenRouter, together.ai, DeepInfra, vLLM autoalojado, el shim de OpenAI de Ollama, LM Studio y LiteLLM.

El nombre del proveedor es uno de `openai`, `openrouter` o `ollama` — cada uno corresponde a su propio bloque de configuración con un `base_url` preestablecido (consulta `setDefaults` en `internal/config/config.go`). Usa `openai` como slot genérico y sobrescribe `base_url` al apuntar a un backend autoalojado.

## Recetas de endpoints

<div class="tabs" data-tabs="openai-compat-endpoints">
  <div class="tab-list" role="tablist" aria-label="OpenAI-compatible endpoint">
    <button role="tab" aria-selected="true">OpenAI</button>
    <button role="tab" aria-selected="false">OpenRouter</button>
    <button role="tab" aria-selected="false">Ollama</button>
    <button role="tab" aria-selected="false">vLLM</button>
    <button role="tab" aria-selected="false">LM Studio</button>
    <button role="tab" aria-selected="false">LiteLLM</button>
  </div>
  <div class="tab-panel" role="tabpanel">

OpenAI directo. `api.openai.com/v1` es el valor por defecto del SDK — no se necesita sobrescribir `base_url`.

```yaml
provider: openai

openai:
  api_key: sk-...
  model: gpt-5
  max_tokens: 4096
```

Uso de herramientas: sí (array `tools` nativo). Streaming: sí (SSE).

<aside class="admonition" data-type="note"><span class="admonition-title">Nomenclatura de modelos</span><p>Los IDs de modelo siguen la propia nomenclatura de OpenAI (<code>gpt-4o</code>, <code>gpt-5</code>, <code>o1</code>, <code>o3-mini</code>). Fija IDs exactos en producción — los alias pueden cambiar bajo tus pies.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

OpenRouter agrega decenas de proveedores detrás de una sola API. Los IDs de modelo usan la convención `proveedor/modelo`:

```yaml
provider: openrouter

openrouter:
  api_key: sk-or-...
  model: anthropic/claude-sonnet-4-6
```

`base_url` por defecto es `https://openrouter.ai/api/v1`. El uso de herramientas depende del proveedor subyacente — los modelos de Anthropic y OpenAI funcionan, la mayoría de modelos de pesos abiertos no.

<aside class="admonition" data-type="tip"><span class="admonition-title">Modelos de nivel gratuito</span><p>OpenRouter expone variantes de nivel gratuito (sufijo <code>:free</code>) para experimentación. Aplican límites de tasa y cuotas diarias.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Ollama local expone un shim compatible con Chat Completions en `http://localhost:11434/v1`:

```yaml
provider: ollama

ollama:
  model: llama3.1:8b
```

`ollama.api_key` por defecto es `not-required` (el shim lo ignora, pero el SDK rechaza cadenas vacías — consulta `New` en `internal/llm/openai/client.go`). `ollama.base_url` por defecto es `http://localhost:11434/v1`.

Uso de herramientas: sí a partir de Ollama 0.4+ (mediante el array `tools` en la solicitud de Chat Completions). Los builds anteriores devuelven texto plano.

<aside class="admonition" data-type="warning"><span class="admonition-title">Latencia</span><p>Ollama solo con CPU en un portátil puede tardar decenas de segundos por turno. Establece el timeout HTTP de tu llamador por encima de 60s o usa un host con GPU.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

vLLM es el motor autoalojado de grado de producción. Arráncalo con `--api-key` si quieres autenticación:

```sh
python -m vllm.entrypoints.openai.api_server \
  --model mistralai/Mixtral-8x22B-Instruct-v0.1 \
  --host 0.0.0.0 --port 8000 \
  --api-key sk-vllm-secret
```

```yaml
provider: openai

openai:
  api_key: sk-vllm-secret
  base_url: http://vllm.internal:8000/v1
  model: mistralai/Mixtral-8x22B-Instruct-v0.1
  max_tokens: 4096
```

Uso de herramientas: sí para modelos con una plantilla de chat de uso de herramientas (`Hermes-2-Pro`, `Mistral-Nemo`, `Llama-3.1-8B-Instruct` y superiores). Streaming: sí. Consulta [Guías: vLLM autoalojado](/es/guides/self-hosted-vllm/) para el despliegue completo.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

LM Studio incluye un servidor compatible con OpenAI en `http://localhost:1234/v1`:

```yaml
provider: openai

openai:
  api_key: not-required
  base_url: http://localhost:1234/v1
  model: lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF
```

Uso de herramientas: **no** admitido en los builds actuales (a mediados de 2026). El endpoint acepta un array `tools` pero lo ignora y devuelve texto plano. Úsalo para cargas de trabajo solo de chat o espera a que llegue la funcionalidad.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

LiteLLM es un proxy que pone muchos proveedores tras una sola API. Apunta rousseau a él:

```yaml
provider: openai

openai:
  api_key: sk-litellm-...
  base_url: http://litellm.internal:4000
  model: bedrock/anthropic.claude-sonnet-4-6-20260101-v1:0
```

Nota: el puerto por defecto de LiteLLM es 4000, y su prefijo `/v1` es opcional según cómo se despliegue. Sigue la documentación de LiteLLM para tu versión.

Uso de herramientas: se pasa al proveedor subyacente. Streaming: sí. Útil para equipos que quieren un único punto de estrangulamiento para el tráfico LLM (limitación de tasa, seguimiento de presupuesto, auditoría).

  </div>
</div>

## Referencia de configuración

| Campo | Por defecto | Efecto |
|---|---|---|
| `api_key` | *requerido* | Token bearer. Usa `not-required` para endpoints locales que ignoran la autenticación. |
| `model` | *requerido* | Identificador de modelo. Sin valor por defecto universal entre endpoints. |
| `base_url` | *depende del nombre del proveedor* | Sobrescribe el endpoint. Consulta los presets en `setDefaults`. |
| `max_tokens` | por defecto del SDK | Limita los tokens de salida por completación. |

Los nombres de proveedor `openai`, `openrouter` y `ollama` cada uno se mapea a su propio bloque de configuración (`OpenAIConfig`, `OpenAIConfig`, `OpenAIConfig`); comparten la misma forma pero te permiten configurar múltiples endpoints en un `config.yaml` y cambiar entre ellos modificando `provider:`.

## Streaming

El proveedor implementa `agent.StreamingProvider` vía SSE. Todos los endpoints anteriores admiten streaming; el shim de Ollama requiere un build reciente (0.5+).

## Uso de herramientas

Las definiciones de herramientas del `Registry` se convierten al array `tools` de OpenAI en `internal/llm/openai/client.go`. No todo endpoint compatible con OpenAI admite uso de herramientas — revisa tu backend antes de habilitar. Ollama lo admite a partir de 0.4; los builds anteriores de LM Studio no.

Las políticas de aprobación aplican para endpoints que sí devuelven `tool_calls`. Los endpoints sin soporte de uso de herramientas devolverán texto plano y no se consultará el `Registry`.

## Gotchas

- **Nomenclatura de modelos.** Cada endpoint tiene su propia convención: OpenAI (`gpt-5`), OpenRouter (`anthropic/claude-sonnet-4-6`), Ollama (`llama3.1:8b`), vLLM (el nombre de HuggingFace). No hay portabilidad entre endpoints.
- **Clave de API vacía.** El SDK rechaza cadenas vacías; pasa `not-required` (o cualquier marcador de posición) para endpoints locales que no necesitan autenticación.
- **Barra final en BaseURL.** Incluye el segmento de ruta `/v1`. No incluyas una barra final.
- **Timeouts.** Ollama local en un CPU puede tardar decenas de segundos por turno — aumenta el timeout de tu cliente HTTP si envuelves el proveedor tú mismo. `rousseau` usa el valor por defecto del SDK.
- **Varianza en el uso de herramientas.** OpenAI y Anthropic detrás de OpenRouter admiten herramientas de forma fiable. Ollama necesita un build reciente y un modelo con una plantilla de chat de uso de herramientas. LM Studio no admite herramientas. Si los tool_calls llegan como texto plano, no se consulta el `Registry`.
- **Modelos de razonamiento.** Las series o1/o3 de OpenAI se comportan diferente: `max_tokens` se reemplaza por `max_completion_tokens` y los system prompts están limitados. El SDK gestiona esto, pero espera latencia por turno más larga.

## Solución de problemas

### `openai: complete: 401 Unauthorized`

Clave de API incorrecta o faltante. Para OpenRouter, usa el token `sk-or-…`. Para endpoints locales, asegúrate de que `api_key` no esté vacío incluso si el endpoint lo ignora.

### `openai: complete: 404 model not found`

La cadena `model` no coincide con nada que el endpoint reconozca. Para OpenRouter, incluye el prefijo del proveedor (`anthropic/claude-sonnet-4-6`, no `claude-sonnet-4-6`). Para Ollama, asegúrate de que el modelo esté descargado (`ollama pull llama3.1:8b`).

### El modelo ignora mis `tools`

El endpoint no admite uso de herramientas para este modelo. Verifica apuntando al mismo modelo vía un endpoint conocido como bueno (OpenAI, Anthropic directo, OpenRouter con un modelo de Anthropic). Consulta la columna de uso de herramientas en las recetas anteriores.

### `context deadline exceeded` en Ollama local

La inferencia por CPU es lenta. Opciones: (1) aumenta el timeout de tu llamador, (2) ejecuta Ollama en un host con GPU, (3) cambia a un modelo más pequeño (`llama3.1:8b` vs `70b`).

### El streaming se detiene a mitad de una respuesta

Algunos proxies (LiteLLM, proxies corporativos de egress) hacen buffering de SSE. Configura el proxy para deshabilitar el buffering para `text/event-stream` o ejecuta rousseau en el mismo segmento de red que el endpoint.

## Páginas relacionadas

- [Guías: vLLM autoalojado](/es/guides/self-hosted-vllm/) — despliegue de producción.
- [Proveedores: Anthropic](/es/providers/anthropic/) — la alternativa de API directa para Claude.
- [Guías: Multi-proveedor](/es/guides/multi-provider/) — ejecutar proveedores distintos por transporte.
- [Guías: Límites de tasa](/es/guides/rate-limits/) — manual de reintento por proveedor.
- [Configuración](/es/configuration/) — los bloques `openai`/`openrouter`/`ollama` en contexto.

## Lectura adicional

- `internal/llm/openai/client.go` — `Complete`, conversión de mensajes, esquema de herramientas.
- `internal/llm/openai/client.go` — implementación de streaming.
- `internal/config/config.go` — struct `OpenAIConfig`, `setDefaults` para presets de `base_url`.
