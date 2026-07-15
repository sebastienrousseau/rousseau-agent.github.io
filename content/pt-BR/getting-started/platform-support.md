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
description: "Support matrix for rousseau-agent: operating systems, CPU architectures, container runtimes, provider authentication methods, transport backing libraries."
keywords: "platform support, os matrix, architecture, container runtime, provider auth, linux, macos, windows, arm64, amd64"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/getting-started/platform-support/"
subtitle: "OS, architectures, container runtimes, provider auth methods."
tags: "platform, support, matrix"
title: "Plataformas suportadas"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "platform support, os matrix, architecture, container runtime, provider auth, linux, macos, windows, arm64, amd64"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Plataformas suportadas"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 23
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/platform-support/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/platform-support/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Plataformas suportadas"
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
twitter_description: "Support matrix for rousseau-agent: operating systems, CPU architectures, container runtimes, provider authentication methods, transport backing libraries."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Plataformas suportadas"
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

## Sistemas operacionais

| SO | Tier de suporte | Notas |
|---|---|---|
| Linux (glibc, kernel 5.10+) | Tier 1 | O CI roda `ubuntu-latest` em todo push. Alvo de implantação de referência. |
| Linux (musl / Alpine) | Tier 1 | A imagem de contêiner é baseada em Alpine. |
| macOS 13+ (Ventura ou mais novo) | Tier 1 | O CI roda `macos-latest` em todo push. TUI Bubble Tea verificada. |
| Windows 10 / 11 | Tier 2 | Binários são compilados e distribuídos, mas o CI não roda a matriz completa em race no Windows. Transportes de chat funcionam; a implantação de referência com Podman + Quadlet assume Linux. |
| FreeBSD / OpenBSD | Best-effort | Build em Go puro, mas sem job de CI. Relatos da comunidade são bem-vindos. |

## Arquiteturas de CPU

| Arquitetura | Tier de suporte | Nomenclatura de release |
|---|---|---|
| `amd64` (x86-64) | Tier 1 | `_linux_amd64`, `_darwin_amd64`, `_windows_amd64` |
| `arm64` (aarch64) | Tier 1 | `_linux_arm64`, `_darwin_arm64` (Apple Silicon) |
| `armv7` (ARM 32 bits) | Best-effort | Buildável via `GOARCH=arm GOARM=7`; não distribuída. |
| `riscv64` | Best-effort | Buildável via `GOARCH=riscv64`; não distribuída. |

`CGO_ENABLED=0` em cada alvo — `modernc.org/sqlite` é Go puro, então cross-compilação é sem atrito.

## Runtimes de contêiner

| Runtime | Tier de suporte | Notas |
|---|---|---|
| Podman 4.4+ (rootless) | Tier 1 | Implantação de referência. Usa unidades Quadlet do systemd para endurecimento declarativo. |
| Docker 24+ | Tier 1 | O Dockerfile funciona sem alterações. O endurecimento de runtime é responsabilidade sua (não há equivalente do Quadlet). |
| containerd + `nerdctl` | Tier 2 | Mesma imagem; o nerdctl consome o mesmo artefato OCI. |
| Kubernetes 1.27+ | Tier 2 | Veja [Guias: Implantação no Kubernetes](/pt-BR/guides/kubernetes-deployment/). |

## Métodos de autenticação dos providers

| Provider | Mecanismo de autenticação | Chaves de configuração |
|---|---|---|
| `claudecli` (padrão) | Herda os tokens OAuth do Claude Code de `~/.claude/`. Sem chave na config do rousseau. | `claudecli.binary`, `claudecli.permission_mode` |
| `anthropic` | Chave direta de API. | Variável de ambiente `ANTHROPIC_API_KEY`, ou `anthropic.api_key` |
| `openai` | Chave OpenAI ou token de terceiro. | `OPENAI_API_KEY`, ou `openai.api_key` |
| `openrouter` | Chave de API do OpenRouter. Usa schema OpenAI com `openrouter.base_url` pré-configurada. | `openrouter.api_key` |
| `ollama` | Endpoint local, sem chave necessária (`ollama.api_key` tem padrão `not-required`). | `ollama.base_url` pré-configurada para `http://localhost:11434/v1` |
| `bedrock` | Cadeia padrão de credenciais AWS (variáveis de ambiente, `~/.aws/credentials`, IMDS, IAM role). | `bedrock.region`, `bedrock.profile`, `bedrock.model` |
| `vertex` | JSON de service account do GCP, ou Application Default Credentials. | `vertex.project`, `vertex.region`, `vertex.credentials_file` |

## Bibliotecas de apoio dos transportes

Cada transporte é um adaptador fino sobre um cliente upstream. O suporte é limitado pela viabilidade do projeto upstream.

| Transporte | Upstream | Protocolo |
|---|---|---|
| WhatsApp | `go.mau.fi/whatsmeow` | Protocolo não oficial do WhatsApp Web (compatível com Signal). |
| Signal | Subprocesso `signal-cli` | Signal JSON-RPC. |
| Telegram | Cliente direto da Bot API | Long polling. |
| Matrix | Cliente direto da API cliente-servidor | Polling HTTPS. |
| Slack | Cliente direto de Socket Mode | WebSocket outbound. |
| Discord | Cliente direto do Gateway | WebSocket outbound + intents. |
| iMessage | Cliente HTTP do BlueBubbles | Polling do BlueBubbles. Requer um host macOS rodando o BlueBubbles Server. |
| Email | Cliente padrão `net/smtp` + IMAP | IMAP + SMTP sobre TLS. |
| SMS | REST direto de Twilio / Vonage | Apenas outbound. |

## Dependências opcionais de runtime

| Dependência | Necessária para | Versão |
|---|---|---|
| CLI `claude` | `provider: claudecli` (padrão). | Latest. |
| `signal-cli` | Transporte Signal. | 0.13+. Requer uma JVM. |
| BlueBubbles Server | Transporte iMessage. | 1.9+. Roda em um host macOS. |
| CLI `whisper.cpp` | Transcrição de mensagens de voz do WhatsApp (`whatsapp.voice.enabled: true`). | 1.5+. Não incluída na imagem de contêiner. |
| `podman` | Implantação de referência. | 4.4+ para suporte a Quadlet. |
| `systemd` (sessão de usuário) | Implantação de referência. | 249+ para Quadlet. |

## Compilador e toolchain

| Componente | Versão | Notas |
|---|---|---|
| Go | 1.26+ | O `go.mod` fixa o grafo de módulos com exatidão. |
| golangci-lint | v2 | 18 linters, pins exatos em `.golangci.yml`. |
| govulncheck | Latest | Rodado em cada build de CI. |
| cosign | 2.2+ | Apenas para verificar releases assinadas. |

## Próximo

- [Instalação](/pt-BR/getting-started/installation/) — instale conforme sua plataforma.
- [Atualizando](/pt-BR/getting-started/updating/) — mude entre versões com segurança.
