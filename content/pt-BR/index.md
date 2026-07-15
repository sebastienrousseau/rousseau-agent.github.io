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
description: "Agente de codificação auto-hospedado com 9 transportes de chat, 5 provedores LLM, servidor MCP, procedência SLSA-3 e releases assinadas com cosign."
keywords: "rousseau-agent, coding agent, self-hosted, container-native, MCP, SLSA-3, cosign, SBOM, LLM, WhatsApp, Signal, Slack"
layout: "index"
permalink: "https://docs.rousseau-agent.dev/pt-BR/"
subtitle: "Agente de codificação auto-hospedado, nativo em contêiner e nativo em MCP."
tags: "overview, self-hosted, mcp, security"
title: "rousseau-agent"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "rousseau-agent, coding agent, self-hosted, container-native, MCP, SLSA-3, cosign, SBOM, LLM, WhatsApp, Signal, Slack"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "rousseau-agent"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "welcome"
order: 1
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/index.html"
item_link: "https://docs.rousseau-agent.dev/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "rousseau-agent"
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
twitter_description: "Agente de codificação auto-hospedado com 9 transportes de chat, 5 provedores LLM, servidor MCP, procedência SLSA-3 e releases assinadas com cosign."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "rousseau-agent"
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

## Agente de codificação auto-hospedado, nativo em contêiner e nativo em MCP

**rousseau-agent** é um assistente de codificação em Go que roda onde seu código roda. O daemon, o material de autenticação e o tráfego para o modelo permanecem em hardware controlado pelo operador. **9 transportes · 5 provedores LLM · SLSA-3 · cosign · SBOM.**

```sh
rousseau chat
```

Esse único comando abre uma TUI Bubble Tea apoiada pelo provedor LLM que você tiver configurado. Nada cruza o perímetro da sua rede a não ser a chamada ao próprio provedor.

## Três pilares

### Endurecido para empresa

- Procedência de build **SLSA Nível 3** via `slsa-framework/slsa-github-generator`.
- Assinaturas **cosign** sem chave em cada arquivo de checksums das releases, verificáveis contra o log de transparência do Sigstore.
- SBOM **CycloneDX** em JSON anexado a cada release.
- **Builds reprodutíveis** verificados em CI a partir de um checkout limpo.
- Podman rootless com `ReadOnly=true`, `DropCapability=all`, `NoNewPrivileges=true`, filtro seccomp padrão, UID 1000 sem privilégios e mapeamento de user namespace `keep-id`.
- Portão de 18 linters no `golangci-lint` v2, CodeQL (Go), `govulncheck` em cada execução de CI, Dependabot para `gomod` e `github-actions`.

### Alcance multimodal

Nove transportes de chat por trás de um único daemon:

- [WhatsApp](/pt-BR/transports/whatsapp/) (`go.mau.fi/whatsmeow`, compatível com o protocolo Signal)
- [Signal](/pt-BR/transports/signal/) (subprocesso `signal-cli` em JSON-RPC)
- [Telegram](/pt-BR/transports/telegram/) (long-polling da Bot API)
- [Matrix](/pt-BR/transports/matrix/) (API cliente-servidor)
- [Slack](/pt-BR/transports/slack/) (Socket Mode, sem superfície HTTP pública)
- [Discord](/pt-BR/transports/discord/) (Gateway v10)
- [iMessage](/pt-BR/transports/imessage/) (polling HTTP do BlueBubbles)
- [Email](/pt-BR/transports/email/) (IMAP + SMTP)
- [SMS](/pt-BR/transports/sms/) (Twilio ou Vonage, apenas envio)

### Agnóstico ao modelo

Cinco famílias de provedores LLM, uma única interface `agent.Provider`:

- [claudecli](/pt-BR/providers/claudecli/) — subprocesso apoiado na sua CLI local `claude`, herda a autenticação dela.
- [Anthropic](/pt-BR/providers/anthropic/) — API direta com marcadores efêmeros de cache de prompt.
- [AWS Bedrock](/pt-BR/providers/bedrock/) — cadeia padrão de credenciais AWS.
- [Google Vertex AI](/pt-BR/providers/vertex/) — JSON de service account ou ADC.
- [Compatível com OpenAI](/pt-BR/providers/openai-compatible/) — OpenAI, OpenRouter, Ollama, vLLM, LM Studio.

## Para onde ir agora

- [Começando](/pt-BR/getting-started/) — instalação, primeira execução, primeiro transporte.
- [Configuração](/pt-BR/configuration/) — cada campo de `internal/config/config.go`.
- [Implantação](/pt-BR/deployment/) — Podman rootless + Quadlet, nota sobre Kubernetes.
- [Segurança](/pt-BR/security/) — postura de cadeia de suprimentos, modelo de confiança, receita cosign.
- [Conceitos](/pt-BR/concepts/) — loop do agente, armazenamento de sessões, MCP, cron, skills.
