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
description: "rousseau-agent's SMS transport is send-only. Twilio (account_sid + auth_token) or Vonage (api_key + auth_token). Inbound not supported because it requires a public webhook."
keywords: "SMS, Twilio, Vonage, Nexmo, send-only, Messaging Service SID, E.164, no webhook"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/transports/sms/"
subtitle: "Send-only SMS via Twilio or Vonage."
tags: "transports, SMS"
title: "Transporte SMS"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "SMS, Twilio, Vonage, Nexmo, send-only, Messaging Service SID, E.164, no webhook"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transporte SMS"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 19
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/sms/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/sms/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transporte SMS"
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
twitter_description: "rousseau-agent's SMS transport is send-only. Twilio (account_sid + auth_token) or Vonage (api_key + auth_token). Inbound not supported because it requires a public webhook."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transporte SMS"
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

## Somente envio, por design

O transporte SMS é **somente envio**. SMS de entrada exige um webhook HTTP público no qual a operadora faz POST — o que conflita diretamente com a postura do rousseau de zero superfície de entrada. Se seu caso de uso precisa de SMS de entrada, execute o rousseau ao lado de um receptor de webhook dedicado e roteie mensagens pelo agendador cron ou pela API de embed do agent-loop.

`Start` é implementado como um no-op que bloqueia em `ctx.Done()` para que o transporte ainda se encaixe no formato padrão de wiring do daemon.

## Operadoras suportadas

| Operadora | `provider` na config | Campos obrigatórios |
|---|---|---|
| Twilio | `twilio` | `from`, `account_sid`, `auth_token` |
| Vonage (anteriormente Nexmo) | `vonage` | `from`, `api_key`, `auth_token` (o segredo da API) |

## Configuração Twilio

```yaml
sms:
  provider: twilio
  from: "+15550000000"
  account_sid: "AC..."
  auth_token: "..."
```

`from` pode ser um número remetente E.164 ou um **Twilio Messaging Service SID** (começa com `MG…`). Messaging Services gerenciam a frota, roteamento sticky-sender e seleção de remetente baseada em geolocalização — recomendado para qualquer tráfego além de um único país.

`base_url` tem padrão `https://api.twilio.com/2010-04-01` e só precisa de sobrescrita para endpoints regionais ou testes.

## Configuração Vonage

```yaml
sms:
  provider: vonage
  from: "+15550000000"
  api_key: "abcd1234"
  auth_token: "efgh5678"
```

`auth_token` na configuração Vonage mapeia para o **API secret** do Vonage, não para sua chave de assinatura JWT — o Vonage autentica submissões de SMS com um par chave/segredo simples.

`base_url` tem padrão `https://rest.nexmo.com`.

## Linha de comando

```sh
# Twilio
rousseau sms \
  --provider twilio \
  --from '+15550000000' \
  --account-sid AC... \
  --auth-token ...

# Vonage
rousseau sms \
  --provider vonage \
  --from '+15550000000' \
  --api-key abcd1234 \
  --auth-token efgh5678
```

Como não há lado de entrada, `--allow` não se aplica.

## API de entrega

Ambos os provedores usam seus respectivos endpoints REST:

- **Twilio.** `POST /2010-04-01/Accounts/{sid}/Messages.json` com basic-auth SID/token.
- **Vonage.** `POST /sms/json` com `api_key` + `api_secret` no corpo.

Os IDs de mensagem retornados são registrados; webhooks de status de entrega **não** são consumidos (novamente, sem superfície HTTP pública).

## Formatação E.164

`from` e os números de destino precisam estar em E.164 (`+<país><assinante>`). Sem espaços, sem hífens. Os Messaging Service SIDs do Twilio ignoram esse requisito apenas para o slot `from`.

## Higiene de custos

- Configure `max_tokens` no seu provider de forma agressiva — SMS é barato por mensagem, mas os bytes se multiplicam rápido se o modelo gerar respostas longas (o Twilio segmenta em 160 caracteres para GSM-7 ou 70 para UCS-2).
- Considere reescrever a resposta de saída para ser concisa antes de entregá-la ao transporte SMS. `agent.Options.SystemPrompt` é o lugar certo.
