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
description: "Set up rousseau-agent's Telegram transport: BotFather token, long-polling, allowlist by numeric user ID, reply-header customisation."
keywords: "Telegram, Bot API, BotFather, long polling, getUpdates, allowlist, chat ID"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/transports/telegram/"
subtitle: "Telegram Bot API over long-polling."
tags: "transports, Telegram"
title: "Transporte Telegram"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Telegram, Bot API, BotFather, long polling, getUpdates, allowlist, chat ID"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transporte Telegram"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 14
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/telegram/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/telegram/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transporte Telegram"
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
twitter_description: "Set up rousseau-agent's Telegram transport: BotFather token, long-polling, allowlist by numeric user ID, reply-header customisation."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transporte Telegram"
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

O transporte Telegram (`internal/transport/telegram/`) fala diretamente com a API HTTP do Bot do Telegram — sem SDK de terceiros. Long-polling em `getUpdates` para entrada; `sendMessage` para saída.

## Pré-requisitos

1. **Um bot.** No Telegram, envie mensagem para [@BotFather](https://t.me/BotFather), envie `/newbot`, escolha um nome e um nome de usuário com sufixo `_bot`. O BotFather devolve um token da API HTTP que se parece com `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`.
2. **Os IDs de usuário que você quer autorizar.** IDs de usuário do Telegram são numéricos. O bot não consegue resolver `@username` para um ID por conta própria — o truque padrão é fazer com que cada usuário autorizado envie `/start` ao bot uma vez, e então ler o `from.id` no log.

## Configuração

```yaml
telegram:
  token: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
  reply_header: ""
  allowlist:
    - "12345678"
    - "98765432"
```

| Campo | Padrão | Efeito |
|---|---|---|
| `token` | *obrigatório* | Token do bot do BotFather. |
| `base_url` | `https://api.telegram.org` | Sobrescreve para um servidor local da Bot API. |
| `reply_header` | *vazio* | Prefixado em toda resposta enviada. |
| `allowlist` | `[]` | IDs de usuário do Telegram cujas mensagens são tratadas. |

## Linha de comando

```sh
rousseau telegram --token 123456:ABC... --allow 12345678 --allow 98765432
```

`--allow` pode ser repetido.

## Long-polling

O transporte chama `getUpdates` com um `PollTimeout` de 30 segundos por padrão (`internal/transport/telegram/client.go`). Cada atualização retornada avança um `offset` interno, de modo que as mensagens nunca são entregues novamente, mesmo entre reinicializações.

Não há webhook. O daemon não precisa de nenhuma superfície HTTP de entrada.

## Formato das mensagens

Apenas mensagens de texto são tratadas. Mídia, figurinhas e notas de voz são ignoradas (uma futura atualização poderia rotear áudio pelo mesmo caminho whisper.cpp do WhatsApp).

## Modos de falha

| Sintoma | Correção |
|---|---|
| Nenhuma atualização chega | Confirme que o bot recebeu ao menos uma mensagem — o Telegram não entrega mensagens históricas. |
| 409 Conflict em getUpdates | Outra instância está fazendo polling com o mesmo token. Pare a outra. |
| Allowlist rejeita um usuário real | Registre o campo `from.id`; IDs de usuário são numéricos e não correspondem a `@username`. |
