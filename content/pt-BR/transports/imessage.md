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
description: "Set up rousseau-agent's iMessage transport: BlueBubbles server on macOS, HTTP polling, poll interval, cursor deduplication, chat GUID for outbound."
keywords: "iMessage, BlueBubbles, macOS, HTTP polling, chat GUID, cursor, deduplication"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/transports/imessage/"
subtitle: "BlueBubbles HTTP polling from a macOS host."
tags: "transports, iMessage"
title: "Transporte iMessage"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "iMessage, BlueBubbles, macOS, HTTP polling, chat GUID, cursor, deduplication"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transporte iMessage"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 18
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/imessage/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/imessage/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transporte iMessage"
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
twitter_description: "Set up rousseau-agent's iMessage transport: BlueBubbles server on macOS, HTTP polling, poll interval, cursor deduplication, chat GUID for outbound."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transporte iMessage"
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

## Visão geral

O transporte iMessage (`internal/transport/imessage/`) não toca no iMessage diretamente — a Apple não fornece nenhuma API oficial voltada ao cliente. Em vez disso, ele faz polling do [BlueBubbles](https://bluebubbles.app), um daemon do lado macOS que expõe o iMessage via HTTP + Socket.IO.

O rousseau usa apenas os endpoints HTTP do BlueBubbles (Socket.IO é evitado deliberadamente para manter a pegada de dependências pequena).

## Arquitetura

```
+-----------+     iMessage      +---------+     HTTP      +-----------+
| Apple ID  | <---------------> | macOS   | <-----------> | rousseau  |
|  server   |                   | Blue    |               | daemon    |
+-----------+                   | Bubbles |               |           |
                                +---------+               +-----------+
```

O host macOS executa o BlueBubbles e permanece logado no iMessage. O rousseau faz polling do endpoint `/api/v1/message` do BlueBubbles na cadência configurada e encaminha as novas chegadas para o handler.

## Pré-requisitos

1. **Um host macOS** com o iMessage logado. Não precisa ser a mesma máquina em que o rousseau roda.
2. **Servidor BlueBubbles** instalado nesse host, escutando em uma URL que o rousseau consiga alcançar (endereço LAN, VPN ou Tailscale).
3. **Senha do BlueBubbles** obtida na GUI do servidor (Settings → Server Password).
4. **Um GUID de chat** para saída. Encontre-o na GUI do BlueBubbles ou via `GET /api/v1/chat`.

## Configuração

```yaml
imessage:
  base_url: "http://mac.internal:1234"
  password: "..."
  chat_guid: "iMessage;-;+15550001234"
  poll_interval: "5s"
  reply_header: ""
```

| Campo | Padrão | Efeito |
|---|---|---|
| `base_url` | *obrigatório* | URL do servidor BlueBubbles. |
| `password` | *obrigatório* | Senha do servidor BlueBubbles. |
| `chat_guid` | *vazio* | GUID do destino de saída. |
| `poll_interval` | `5s` | Cadência de polling contra `/api/v1/message`. |
| `reply_header` | *vazio* | Prefixado em toda mensagem enviada. |

## Linha de comando

```sh
rousseau imessage \
  --base-url http://mac.internal:1234 \
  --password ... \
  --chat-guid 'iMessage;-;+15550001234' \
  --poll-interval 5s
```

## Deduplicação por cursor

Na inicialização, o transporte inicializa seu cursor `lastID` para a mensagem existente mais recente, para que o operador não seja bombardeado com todo o histórico do iMessage. Cada polling subsequente busca as `PageSize` mensagens mais recentes (padrão 25) e encaminha apenas as mais novas que o cursor.

O cursor fica em memória. Ao reiniciar, o cursor é re-inicializado a partir do BlueBubbles — uma pequena janela de mensagens que chegaram enquanto o daemon estava fora será perdida. Este é um trade-off deliberado; uma lógica de cursor persistente exigiria outra tabela no armazenamento de estado, e os timestamps de entrega do iMessage não são monotônicos garantidos entre dispositivos.

## Alcançabilidade

O BlueBubbles precisa estar acessível pela rede a partir de onde o rousseau roda. Padrões comuns:

- **Mesma LAN.** `http://<mac-lan-ip>:1234`.
- **Tailscale.** `http://mac.tailnet.ts.net:1234`. Criptografa o link e funciona através de NAT.
- **Túnel reverso.** `http://localhost:1234` no host rousseau com um túnel SSH `-R` a partir do Mac.

Não exponha o BlueBubbles à internet pública a menos que você entenda o modelo de autenticação (uma única senha).

## Modos de falha

| Sintoma | Correção |
|---|---|
| `imessage.prime_failed` na inicialização | BlueBubbles inalcançável — verifique `base_url` e `password`. |
| Cada mensagem histórica é reproduzida | `lastID` não foi inicializado. Verifique permissões / autenticação. |
| Mensagens de saída silenciosamente descartadas | `chat_guid` errado. Consulte via `GET /api/v1/chat`. |
| Mensagens chegam com minutos de atraso | Aumente a frequência de polling do próprio BlueBubbles ou reduza `poll_interval`. |
