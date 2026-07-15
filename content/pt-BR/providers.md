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
hreflang: "pt-BR"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "pt-BR"
locale: "pt_BR"
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
permalink: "https://docs.rousseau-agent.dev/pt-BR/providers/"
subtitle: "Cinco famílias de provedores LLM por trás de uma única interface Provider."
tags: "providers, LLM"
title: "Provedores"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "providers, LLM, Anthropic, Bedrock, Vertex, OpenAI, OpenRouter, Ollama, claudecli"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Provedores"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 5
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Provedores"
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
twitter_title: "Provedores"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Obrigado a cada operador que executa seu próprio agente de codificação."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## A interface Provider

Todo backend LLM implementa `agent.Provider`:

```go
type Provider interface {
    Name() string
    Complete(ctx context.Context, req Request) (Response, error)
}
```

Uma variante `StreamingProvider` adiciona `CompleteStream` para entrega token a token. Adicionar um sexto backend é uma única implementação de `Complete` mais a conexão em `internal/cli/provider.go`.

## Famílias suportadas

| Provider | Modelo de autenticação | Endpoint | Streaming | Prompt caching | Recomendado para |
|---|---|---|:---:|:---:|---|
| [claudecli](/pt-BR/providers/claudecli/) | Herda a autenticação da CLI `claude` | Subprocesso local | Sim | via subprocesso | Operadores individuais, Claude Code no tier por assinatura |
| [Anthropic](/pt-BR/providers/anthropic/) | `ANTHROPIC_API_KEY` | `api.anthropic.com` | Sim | marcadores efêmeros | Times na API da Anthropic |
| [AWS Bedrock](/pt-BR/providers/bedrock/) | Cadeia de credenciais AWS | `bedrock-runtime.<region>.amazonaws.com` | Sim | via SDK | Empresas na AWS |
| [Google Vertex AI](/pt-BR/providers/vertex/) | Service account ou ADC | `<region>-aiplatform.googleapis.com` | Sim | via SDK | Empresas no GCP |
| [Compatível com OpenAI](/pt-BR/providers/openai-compatible/) | Bearer token | `api.openai.com` ou override | Sim | dependente do provider | OpenAI, OpenRouter, Ollama, vLLM, LM Studio |

## Selecionando um provider

Defina a chave `provider` no topo de `~/.config/rousseau/config.yaml`:

```yaml
provider: anthropic

anthropic:
  api_key: sk-ant-...
  model: claude-sonnet-4-6
```

Ou sobrescreva no shell:

```sh
ROUSSEAU_PROVIDER=bedrock rousseau chat
```

`ANTHROPIC_API_KEY` é bindada a `anthropic.api_key` no momento do load, então passá-la no ambiente é equivalente.

## Onde cada provider faz tool-use

O provider `claudecli` roda seu próprio loop de tool-use dentro do subprocesso `claude`. Ferramentas registradas no `Registry` do rousseau **não** são invocadas para esse provider; a `Response` é sempre uma única mensagem de texto de fim de turno com a resposta final do claude.

Todos os outros providers (`anthropic`, `bedrock`, `vertex`, `openai`) usam o `Registry` do rousseau. Definições de ferramenta são convertidas para o formato JSON esperado pelo provider por cada pacote de provider.
