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
description: "Overview of the five LLM provider families supported by rousseau-agent: claudecli, Anthropic, AWS Bedrock, Google Vertex AI, and any OpenAI-compatible endpoint."
keywords: "providers, LLM, Anthropic, Bedrock, Vertex, OpenAI, OpenRouter, Ollama, claudecli"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/providers/"
subtitle: "Cinco familias de proveedores LLM detrás de una única interfaz Provider."
tags: "providers, LLM"
title: "Proveedores"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "providers, LLM, Anthropic, Bedrock, Vertex, OpenAI, OpenRouter, Ollama, claudecli"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Proveedores"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 5
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Proveedores"
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
twitter_description: "Overview of the five LLM provider families supported by rousseau-agent: claudecli, Anthropic, AWS Bedrock, Google Vertex AI, and any OpenAI-compatible endpoint."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Proveedores"
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

## La interfaz Provider

Cada backend de LLM implementa `agent.Provider`:

```go
type Provider interface {
    Name() string
    Complete(ctx context.Context, req Request) (Response, error)
}
```

Una variante `StreamingProvider` añade `CompleteStream` para entrega token por token. Añadir un sexto backend es una única implementación de `Complete` más el cableado en `internal/cli/provider.go`.

## Familias soportadas

| Proveedor | Modelo de auth | Endpoint | Streaming | Caché de prompt | Recomendado para |
|---|---|---|:---:|:---:|---|
| [claudecli](/es/providers/claudecli/) | Hereda auth del CLI `claude` | Subproceso local | Sí | vía subproceso | Operadores individuales, Claude Code de suscripción |
| [Anthropic](/es/providers/anthropic/) | `ANTHROPIC_API_KEY` | `api.anthropic.com` | Sí | marcadores efímeros | Equipos en la API de Anthropic |
| [AWS Bedrock](/es/providers/bedrock/) | Cadena de credenciales AWS | `bedrock-runtime.<region>.amazonaws.com` | Sí | vía SDK | Empresas en AWS |
| [Google Vertex AI](/es/providers/vertex/) | Cuenta de servicio o ADC | `<region>-aiplatform.googleapis.com` | Sí | vía SDK | Empresas en GCP |
| [Compatible con OpenAI](/es/providers/openai-compatible/) | Bearer token | `api.openai.com` o sobrescritura | Sí | dependiente del proveedor | OpenAI, OpenRouter, Ollama, vLLM, LM Studio |

## Seleccionar un proveedor

Establece la clave `provider` al principio de `~/.config/rousseau/config.yaml`:

```yaml
provider: anthropic

anthropic:
  api_key: sk-ant-...
  model: claude-sonnet-4-6
```

O sobrescribe desde la shell:

```sh
ROUSSEAU_PROVIDER=bedrock rousseau chat
```

`ANTHROPIC_API_KEY` se enlaza a `anthropic.api_key` en tiempo de carga, por lo que pasarla en el entorno es equivalente.

## Dónde usa herramientas cada proveedor

El proveedor `claudecli` ejecuta su propio bucle de uso de herramientas dentro del subproceso `claude`. Las herramientas registradas en el `Registry` de rousseau **no** se invocan para este proveedor; la `Response` siempre es un único mensaje de texto de fin de turno con la respuesta final de claude.

Todos los demás proveedores (`anthropic`, `bedrock`, `vertex`, `openai`) usan el `Registry` de rousseau. Las definiciones de herramientas se convierten a la forma JSON esperada por el proveedor mediante cada paquete de proveedor.
