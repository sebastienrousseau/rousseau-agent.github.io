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
changefreq: "weekly"
description: "Chronological release notes for rousseau-agent. First public snapshot: 9 transports, 5 providers, MCP server, SLSA-3, 76% coverage."
keywords: "changelog, release notes, versions, snapshot"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/changelog/"
subtitle: "Notas de versão cronológicas do rousseau-agent."
tags: "changelog, reference"
title: "Registro de alterações"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "changelog, release notes, versions, snapshot"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Registro de alterações"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 28
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/changelog/index.html"
item_link: "https://docs.rousseau-agent.dev/changelog/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Registro de alterações"
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
twitter_description: "Chronological release notes for rousseau-agent. First public snapshot: 9 transports, 5 providers, MCP server, SLSA-3, 76% coverage."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Registro de alterações"
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

## Estado atual — julho de 2026

Primeiro snapshot público. Destaques do que já está disponível hoje:

- **Nove transportes de chat.** WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, Email, SMS.
- **Cinco provedores LLM.** claudecli, Anthropic direct, AWS Bedrock, Google Vertex AI, compatível com OpenAI.
- **Servidor MCP.** JSON-RPC 2.0 sobre stdio, revisão de spec 2024-11-05.
- **Procedência de build SLSA Nível 3**, checksums de release assinadas com cosign, SBOM CycloneDX.
- **76% de cobertura de testes** em todo o módulo (pacotes core ficam entre 85–100%).
- **Zero alertas Dependabot em aberto.**
- **CI completa em race mode** em `ubuntu-latest` e `macos-latest`.

## Detalhe

Para o histórico completo commit a commit, veja o git log em https://github.com/sebastienrousseau/rousseau-agent.

Cada commit usa [Conventional Commits](https://www.conventionalcommits.org/). A página de changelog receberá entradas estruturadas assim que a primeira release com tag for cortada; até lá, `git log --oneline` é a referência autoritativa.

## Política de compatibilidade

- **O formato do arquivo de configuração** é versionado por adições de campos, não por quebras de schema. Novas chaves podem ser ignoradas com segurança; renomeações e remoções virão precedidas de um aviso de descontinuação na release anterior à remoção.
- **`agent.Provider`, `agent.Message`, `agent.Session`** são exports estáveis destinados a embedders de terceiros. Mudanças que quebrem compatibilidade virão em um salto de versão major.
- **Pacotes `internal/*`** não são API estável — são internos ao projeto. Consumidores de terceiros não devem importá-los (a visibilidade `internal` do Go garante isso).

## Onde registrar feedback

- Bugs e pedidos de feature: issues no GitHub.
- Segurança: `sebastian.rousseau@gmail.com` (veja [/security/](/pt-BR/security/)).
