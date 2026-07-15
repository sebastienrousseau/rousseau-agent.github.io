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
description: "rousseau-agent is self-hosted. No telemetry endpoint, no SaaS control plane. LLM providers have their own retention policies; everything else stays in the operator's infrastructure."
keywords: "privacy, telemetry, self-hosted, data handling, retention, LLM providers"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/privacy/"
subtitle: "Auto-hospedado significa autocontrolado — nada sai da sua infraestrutura, exceto a chamada ao LLM."
tags: "privacy, legal, self-hosted"
title: "Privacidade"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "privacy, telemetry, self-hosted, data handling, retention, LLM providers"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Privacidade"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "legal"
order: 30
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/privacy/index.html"
item_link: "https://docs.rousseau-agent.dev/privacy/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Privacidade"
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
twitter_description: "rousseau-agent is self-hosted. No telemetry endpoint, no SaaS control plane. LLM providers have their own retention policies; everything else stays in the operator's infrastructure."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Privacidade"
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

## Tratamento de dados

O `rousseau-agent` é auto-hospedado. Quando o operador executa o daemon em sua própria infraestrutura, **nenhum dado sai dessa infraestrutura, exceto a própria chamada ao LLM**.

Não há:

- **Nenhum endpoint de telemetria.** O rousseau não faz chamadas para `rousseau-agent.dev` nem para qualquer outro servidor controlado pelo autor em tempo de execução.
- **Nenhum control plane SaaS.** Não há servidor de licenças, nem dashboard em nuvem, nem phone-home.
- **Nenhuma analytics de uso.** O daemon não reporta quais ferramentas foram invocadas, quantos turnos rodaram, nem quais modelos foram chamados.
- **Nenhum crash reporting.** Crashes aparecem em logs locais (`journalctl --user -u rousseau-agent.service`). Nenhum stack trace é enviado a lugar nenhum.

## Onde ficam os dados de sessão

| Dados | Local | Criptografia em repouso |
|---|---|---|
| Sessões (histórico de mensagens) | `~/.local/share/rousseau/sessions.db` | Apenas no nível de filesystem (LUKS / FileVault se o operador configurou). |
| Jobs de cron | Mesmo banco SQLite | Igual. |
| Pareamento de dispositivo WhatsApp | `~/.local/share/rousseau/whatsapp.db` | Igual. |
| Saída de log | journal do systemd (tipicamente `~/.local/state/`) | Igual. |
| Arquivo de configuração | `~/.config/rousseau/config.yaml` | Igual. |
| Tokens OAuth da CLI `claude` | `~/.claude/` | Igual. |

Nenhum desses é transmitido a lugar nenhum pelo daemon.

## Provedores LLM

O provedor LLM é o único ponto de contato externo. Cada provedor tem sua própria política de tratamento de dados e retenção — nada disso é controlado pelo rousseau:

| Provedor | Política de retenção |
|---|---|
| [claudecli](/pt-BR/providers/claudecli/) | O que a CLI local `claude` estiver configurada para enviar. Tipicamente a retenção padrão da Anthropic. |
| [Anthropic direct](/pt-BR/providers/anthropic/) | Veja https://www.anthropic.com/legal/aup |
| [AWS Bedrock](/pt-BR/providers/bedrock/) | Definida por contrato; tipicamente sem retenção de longo prazo para tráfego de inferência no Bedrock. |
| [Google Vertex AI](/pt-BR/providers/vertex/) | Definida por contrato; tipicamente sem retenção de longo prazo para inferência no Vertex. |
| [Compatível com OpenAI](/pt-BR/providers/openai-compatible/) | Depende do endpoint. Ollama e vLLM auto-hospedado não retêm nada externamente; OpenAI e OpenRouter têm suas próprias políticas. |

Escolha o provedor cuja política de retenção corresponda aos seus requisitos operacionais. Para a postura mais estrita, rode contra um Ollama, vLLM ou LM Studio auto-hospedado — nenhum dado sai da sua infraestrutura.

## Dados do lado do transporte

Transportes de chat enviam mensagens pelos servidores do fornecedor (WhatsApp, Signal, Slack, Discord, etc). Cada um tem sua própria postura de tratamento de dados. O rousseau não adiciona uma camada sobre eles — o fornecedor vê o que o protocolo subjacente mostrar, o que é específico do protocolo:

- Signal e WhatsApp: criptografia ponta a ponta; o fornecedor vê metadados, mas não o conteúdo das mensagens.
- Slack, Discord: sem criptografia ponta a ponta; o fornecedor vê o conteúdo das mensagens.
- Matrix: criptografia ponta a ponta quando a sala tem E2E habilitado; do lado do servidor em outros casos.
- Email: sem criptografia ponta a ponta a menos que você coloque PGP ou S/MIME em cima (o rousseau não faz isso).
- iMessage: criptografia ponta a ponta; o BlueBubbles fica entre o rousseau e a Apple.

## Deletando uma sessão

Sessões são linhas em um banco SQLite. Delete com:

```sh
rousseau session delete <session-id>
```

Ou descarte o banco inteiro:

```sh
rm ~/.local/share/rousseau/sessions.db
```

O próximo start recria um vazio. Isso também expurga o índice FTS5 de recall entre sessões.

## Dependências de terceiros

`go.mod` lista cada dependência. Nenhuma delas está configurada para fazer phone-home. Dependências de build (linters, analisadores estáticos) rodam apenas em CI. Dependências de runtime estão enumeradas no SBOM CycloneDX anexado a cada release.
