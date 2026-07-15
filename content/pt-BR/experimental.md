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
description: "Off-by-default rousseau-agent behaviour: voice mode via whisper.cpp, FTS5 recall, LLM compression, and other opt-in surface."
keywords: "experimental, voice, whisper, fts5, compression, opt-in, feature flag"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/experimental/"
subtitle: "Comportamentos desativados por padrão, e por quê."
tags: "experimental, opt-in, voice, compression, fts5"
title: "Experimental"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "experimental, voice, whisper, fts5, compression, opt-in, feature flag"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Experimental"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "system"
order: 60
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/experimental/index.html"
item_link: "https://docs.rousseau-agent.dev/experimental/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Experimental"
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
twitter_description: "Off-by-default rousseau-agent behaviour: voice mode via whisper.cpp, FTS5 recall, LLM compression, and other opt-in surface."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Experimental"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Obrigado a cada operador que executa seu próprio agente de codificação."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## O que "experimental" significa aqui

A postura padrão do Rousseau é minimalista: um binário Go estático, um arquivo SQLite, nenhuma dependência externa. Qualquer feature que exija um runtime extra (`whisper.cpp`), estado extra (índice FTS5 para recall) ou custo extra de provedor (compressão apoiada em LLM) é opt-in.

Nenhuma delas é instável. Elas estão disponíveis, têm testes, são suportadas. Mas como mudam o custo ou a superfície operacional, o padrão é desligado — você liga as que precisa.

## Voice mode (whisper.cpp)

Desligado por padrão porque exige que o binário `whisper` do whisper.cpp esteja instalado no host do daemon.

**Toggle:** `whatsapp.voice.enabled: true` no `config.yaml`. Veja `VoiceConfig` em `internal/config/config.go`.

**O que faz.** Quando o WhatsApp entrega uma mensagem de voz, o cliente whatsmeow baixa o payload OGG, invoca `whisper` com o modelo configurado e trata a transcrição como o texto da mensagem de entrada. Eventos de log estruturado (`internal/transport/whatsapp/dispatch.go`):

- `whatsapp.audio_downloaded size=N`
- `whatsapp.transcribed elapsed=N`

**Por que fica desligado.** Duas razões: (1) uma instalação nova falharia de forma confusa quando o binário `whisper` estivesse ausente, (2) transcrição é um gasto de CPU em tempo real que a maioria dos operadores prefere optar por adotar do que ser surpreendida.

Veja [Guia do usuário: Voice mode](/pt-BR/user-guide/voice-mode/) para o setup completo.

## Recall FTS5

**Toggle.** Ligado por padrão, mas usado apenas por ferramentas que pedem por ele. O índice FTS5 é construído e mantido independentemente (`EnsureSearch` em `internal/state/sqlite/search.go`); o "opt-in" é se o agente pede ao modelo para pesquisar nele.

**O que faz.** Índice full-text FTS5 do SQLite sobre cada sessão armazenada. Alimentado por `rousseau session search`, pela ferramenta MCP `rousseau_search_sessions` e (quando o agente está configurado com um recall searcher) o modelo pode consultá-lo no meio do turno.

**Por que é estruturado assim.** O índice é barato de manter — os triggers em `internal/state/sqlite/search.go` cuidam disso — mas expô-lo ao modelo a cada turno tem um custo. Ele só é conectado quando o loop do agente é construído com um `RecallSearcher` (`internal/state/sqlite/recall.go`).

Veja [Guia do usuário: Compressão + Recall](/pt-BR/user-guide/compression-recall/).

## Compressão apoiada em LLM

Desligada por padrão porque custa tokens.

**Toggle:** `agent.compression.enabled: true`. Lista completa de campos em [Guia: Gerenciamento de contexto](/pt-BR/guides/context-management/).

**O que faz.** Quando uma sessão cresce além de `trigger_messages` (padrão 60), o `LLMCompressor` (`internal/agent/compressor.go`) sumariza a fatia mais antiga em uma única mensagem sintética de usuário, preservando na íntegra as `keep_recent` mensagens mais recentes. Cada turno subsequente é menor e mais barato.

**Por que fica desligada.** A implantação de referência roda `claudecli` em um tier por assinatura em que a contagem de tokens não é cobrada. A compressão se paga em provedores Anthropic direct, Bedrock, Vertex e compatíveis com OpenAI.

## Base URLs de OpenRouter e Ollama (pré-configuradas, ainda opt-in)

Não estritamente experimental, mas vale nomear: o `setDefaults` do rousseau em `internal/config/config.go` pré-configura as base URLs de OpenRouter e Ollama:

- `openrouter.base_url: https://openrouter.ai/api/v1`
- `ollama.base_url: http://localhost:11434/v1`
- `ollama.api_key: not-required`

Selecionar esses provedores é opt-in via `provider: openrouter` / `provider: ollama` — os endpoints já estão preenchidos para você não precisar lembrar deles.

## Detecção de prompt injection (roadmap)

Não distribuída. Veja [Guias: Prompt injection](/pt-BR/guides/prompt-injection/) para o modelo de ameaça honesto. Hoje a mitigação é inteiramente baseada em approver; detecção via classificador é um item de roadmap dependendo de pesquisa que realmente funcione.

## Streaming para provedores não-Anthropic (parcial)

O provedor Anthropic (`internal/llm/anthropic/client.go`) suporta a interface de streaming do SDK. Outros adaptadores atualmente rodam em modo não-streaming. Streaming em todos os adaptadores é uma passada de uniformização planejada.

## Relacionados

- [Configuração](/pt-BR/configuration/) — cada botão de config.
- [Guia do usuário: Voice mode](/pt-BR/user-guide/voice-mode/).
- [Guias: Gerenciamento de contexto](/pt-BR/guides/context-management/) — aprofundamento em compressão.
- [Referência: Session store](/pt-BR/reference/session-store/) — schema FTS5.
