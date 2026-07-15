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
description: "Worked example: point rousseau-agent at a self-hosted vLLM endpoint on your internal network via the OpenAI-compatible provider."
keywords: "vllm, self-hosted, openai-compatible, air-gapped, internal network, local llm"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/guides/self-hosted-vllm/"
subtitle: "Point rousseau at a vLLM endpoint on your internal network."
tags: "guides, vllm, self-hosted, openai-compatible"
title: "Guía: vLLM autoalojado"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "vllm, self-hosted, openai-compatible, air-gapped, internal network, local llm"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guía: vLLM autoalojado"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 32
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/self-hosted-vllm/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/self-hosted-vllm/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guía: vLLM autoalojado"
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
twitter_description: "Worked example: point rousseau-agent at a self-hosted vLLM endpoint on your internal network via the OpenAI-compatible provider."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guía: vLLM autoalojado"
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

## Escenario

Tienes una instancia de vLLM sirviendo un modelo de codificación de pesos abiertos en un equipo interno (`llm.internal:8000`). No puede salir tráfico de inferencia de la red. Apunta rousseau a él y trata el endpoint como cualquier otro objetivo compatible con OpenAI.

vLLM implementa el esquema OpenAI Chat Completions, por lo que el proveedor `openai` de rousseau funciona sin cambios. LM Studio, Ollama y Text Generation Inference siguen el mismo patrón.

## Requisitos previos

- vLLM ya activo en `http://llm.internal:8000/v1` con `/v1/chat/completions` respondiendo a una prueba con curl.
- La etiqueta del modelo con el que lanzaste vLLM (p. ej. `Qwen/Qwen3-Coder-30B`).

## Paso 1: Confirmar vLLM

```sh
curl -fsS http://llm.internal:8000/v1/models
curl -fsS http://llm.internal:8000/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{
    "model": "Qwen/Qwen3-Coder-30B",
    "messages": [{"role": "user", "content": "say hi"}]
  }' | jq .
```

Ambas deben retornar sin error. Si la segunda llamada devuelve 4xx, arregla vLLM primero: el cliente de rousseau es una capa JSON delgada y hereda su superficie de error.

## Paso 2: Conectar rousseau con vLLM

Edita `~/.config/rousseau/config.yaml`:

```yaml
provider: openai

openai:
  base_url: http://llm.internal:8000/v1
  api_key: not-required        # vLLM ignora la clave pero el cliente envía una
  model: Qwen/Qwen3-Coder-30B
  max_tokens: 4096

log:
  level: info
  format: json
```

El proveedor `openai` comparte su esquema con `openrouter` y `ollama`; la única diferencia es el `base_url` preconfigurado. Establecer `base_url` explícitamente sobrescribe el valor por defecto.

## Paso 3: Prueba en la TUI

```sh
rousseau chat
```

Escribe `explica la diferencia entre goroutines e hilos en dos párrafos.` y envía. Si la respuesta llega en streaming, el cableado es correcto.

Si no:

```sh
rousseau doctor
```

La fila `provider.selected` mostrará `openai`; un `fail` en la alcanzabilidad de `provider.openai.base_url` significa que DNS o la ruta de red interna están rotos, no rousseau.

## Paso 4: Activar el uso de herramientas

Los modelos de codificación varían en fidelidad de uso de herramientas. El bucle del agente de rousseau espera que el modelo emita bloques `tool_use` cuyo JSON valide contra el `InputSchema` de la herramienta. Si tu modelo en vLLM no admite nativamente el esquema de uso de herramientas de OpenAI:

- Comienza con `provider: openai` + un modelo que lo admita (variantes recientes de Qwen, Mistral, Llama 3.1 8B+ lo anuncian).
- O envuelve vLLM en un adaptador como [vLLM's OpenAI-compatible tool_choice adapter](https://docs.vllm.ai/) y vuelve a verificar.

Una vez que el uso de herramientas funciona, las herramientas de codificación (read, write, edit, grep, bash) quedan disponibles exactamente como con cualquier otro proveedor.

## Paso 5: Considerar políticas de aprobación

Los modelos autohospedados tienden a ser menos conscientes del riesgo que los modelos de frontera. Bloquear la herramienta `bash` con un aprobador en modo `pattern` es prudente:

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read,  match: ".*"}
      - {tool: grep,  match: ".*"}
      - {tool: edit,  match: "^./workspace/.*"}
      - {tool: bash,  match: "^(ls|cat|grep|rg|find|git status|git diff) "}
    deny:
      - {tool: bash,  match: "rm -rf|sudo|curl|wget|chmod|chown"}
```

Consulta [Guías: Auditoría + Políticas de aprobación](/es/guides/audit-approval-policies/) para un recorrido más profundo.

## Paso 6: Observar el rendimiento

Los endpoints autohospedados suelen beneficiarse de un `max_iterations` más alto (el bucle del agente puede necesitar más idas y vueltas para llegar a la misma conclusión) y siempre de habilitar la compresión de sesión:

```yaml
agent:
  max_iterations: 48
  compression:
    enabled: true
    trigger_messages: 60
    keep_recent: 8
```

La compresión está desactivada por defecto porque usa un turno de LLM para resumir; en una API pública por token esto puede ser un desperdicio. En un endpoint autohospedado el costo por token es cero, así que déjala activada.

## Alternativas a vLLM

La misma receta aplica a:

- **Ollama**: usa `provider: ollama` (por defecto `base_url` es `http://localhost:11434/v1` y `api_key` es `not-required`).
- **LM Studio**: usa `provider: openai` y apunta `base_url` al servidor de LM Studio (`http://host:1234/v1`).
- **TGI (Text Generation Inference)**: usa `provider: openai` y apunta `base_url` al endpoint de compatibilidad OpenAI de TGI.
- **OpenRouter**: usa `provider: openrouter` (por defecto `base_url` es `https://openrouter.ai/api/v1`).

## Advertencias

- rousseau no hace streaming cuando el proveedor no lo hace. Algunos builds de vLLM se distribuyen con streaming desactivado: actívalo para una mejor experiencia en la TUI.
- El caché de prompts (`internal/llm/anthropic` usa marcadores `cache_control`) es específico de Anthropic y no hace nada contra vLLM. Esto importa mayormente para sesiones de larga duración en proveedores de pago por token.
- La [página del proveedor compatible con OpenAI](/es/providers/openai-compatible/) es la referencia definitiva para cada perilla.

## Siguiente

- [Proveedor compatible con OpenAI](/es/providers/openai-compatible/): cada campo de configuración.
- [Auditoría + políticas de aprobación](/es/guides/audit-approval-policies/): postura de seguridad para modelos menos alineados.
- [Offline](/es/offline/): ejecutar rousseau sin internet saliente.
