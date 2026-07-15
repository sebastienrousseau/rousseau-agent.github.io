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
description: "Rousseau-agent ships zero telemetry. No analytics endpoint, no crash-report upload, no license server, no unique identifiers."
keywords: "telemetry, privacy, no phone home, no analytics, no license server"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/guides/telemetry/"
subtitle: "Zero analytics, zero telemetria. Verificável."
tags: "guides, telemetry, privacy, security"
title: "Guia: telemetria"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "telemetry, privacy, no phone home, no analytics, no license server"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guia: telemetria"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 40
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/telemetry/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/telemetry/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guia: telemetria"
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
twitter_description: "Rousseau-agent ships zero telemetry. No analytics endpoint, no crash-report upload, no license server, no unique identifiers."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guia: telemetria"
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

## O compromisso

O rousseau-agent envia zero telemetria. A lista de coisas que o rousseau explicitamente **não** faz:

- Sem endpoint de analytics. Não existe `metrics.rousseau-agent.dev` ou equivalente.
- Sem upload de crash-report. Panics vão para stderr; nada é enviado para lugar nenhum.
- Sem servidor de licença. Não há check-in periódico e nem verificação de seat.
- Sem identificador único de instalação. O binário é byte-idêntico em cada install da mesma tag.
- Sem serviço de feature-flag. Cada switch no rousseau está em `config.yaml` ou em uma flag CLI.
- Sem ping de update. `rousseau version` é um lookup local; não há round trip de "checking for updates".

## Como verificar

O binário do rousseau é open source (MIT, veja `LICENSE`). Cada chamada de rede é grepável:

```sh
grep -rn 'http.Get\|http.Post\|http.Client\|http.NewRequest\|net/http' \
  /path/to/rousseau-agent/internal/ | head
```

Cada hit cai em uma dessas categorias:

| Pacote | Propósito |
|---|---|
| `internal/llm/anthropic/` | Calls da API Anthropic (via o SDK oficial). |
| `internal/llm/openai/` | Calls de endpoint compatível com OpenAI. |
| `internal/transport/telegram/` | Telegram Bot API. |
| `internal/transport/matrix/` | Matrix client-server API. |
| `internal/transport/whatsapp/` | Websockets whatsmeow para a Meta. |
| `internal/transport/slack/`, `discord/` | Socket Mode / Discord Gateway. |
| `internal/transport/imessage/` | Servidor BlueBubbles (na sua LAN). |
| `internal/transport/sms/` | Twilio / Vonage. |
| `internal/transport/email/` | IMAP + SMTP. |

Nenhum deles é endpoint de analytics. Cada um é o provider de LLM que você configurou ou o transporte que você habilitou.

Rode o daemon sob `strace -e network` ou observe com `ss -tanp` — os únicos sockets que você verá são para os endpoints listados acima.

## Logging estruturado é local

O rousseau usa `log/slog` (`internal/cli/root.go`). Por padrão o handler escreve para stderr, o que sob a unidade Quadlet vai para o journal do systemd. Nada é streamado para fora do host. Se você quer enviar logs para Loki, Datadog ou outro lugar, você configura esse pipeline por conta própria — veja [Guias: Observabilidade](/pt-BR/guides/observability/).

## Comparação

| Produto | Analytics | Upload de crash | Servidor de licença |
|---|---|---|---|
| rousseau-agent | nenhum | nenhum | nenhum |
| Vendor A (assistente de codificação SaaS típico) | sim | sim | sim |
| Vendor B (control plane gerenciado) | sim | opt-out | sim |

O modelo operacional do rousseau é: você traz a chave do LLM, você hospeda o daemon. Não há nenhuma parte do rousseau que roda em servidores que o Sebastien controla.

## O que o rousseau _envia_ para providers de LLM

Por definição, quando você roteia mensagens por Anthropic, Bedrock, Vertex, OpenAI ou qualquer outra API, aquele provider vê o conteúdo da mensagem. Isso é inerente a como a inferência de LLM funciona — o rousseau é um cliente, não um shim.

Duas mitigações se o handling de dados do provider importa para você:

1. **Rode contra um modelo self-hosted.** Ollama, vLLM, LM Studio ou qualquer endpoint compatível com OpenAI. Nada sai da sua máquina. Veja [Guias: vLLM self-hosted](/pt-BR/guides/self-hosted-vllm/).
2. **Use Bedrock ou Vertex em uma região com um adendo de processamento de dados.** Tanto AWS quanto GCP publicam garantias de residência de dados por região.

## O que o bridge do WhatsApp vê

O protocolo não oficial do WhatsApp Web implementado por whatsmeow fala com os servidores da Meta — esse tráfego está fora do controle do rousseau. A Meta vê suas mensagens da mesma forma que quando você usa o WhatsApp Web pelo navegador. Se a Meta ver suas mensagens não é aceitável, não rode o bridge do WhatsApp.

O cliente whatsmeow é publicamente auditável — cada pacote é documentado; não há chamadas de rede específicas do rousseau sobrepostas.

## Relacionado

- [Segurança](/pt-BR/security/) — fronteiras de confiança e postura de auditoria.
- [Privacidade](/pt-BR/privacy/) — a postura de privacidade em nível de site.
- [Providers: OpenAI-compatible](/pt-BR/providers/openai-compatible/) — inferência self-hosted.
- [Guias: vLLM self-hosted](/pt-BR/guides/self-hosted-vllm/) — um exemplo trabalhado.
