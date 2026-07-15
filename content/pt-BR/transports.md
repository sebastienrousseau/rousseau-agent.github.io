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
description: "Overview of rousseau-agent's nine chat transports: WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, Email, SMS. Every transport implements Start / Stop / Deliver."
keywords: "transports, WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, email, SMS"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/transports/"
subtitle: "Nove transportes de chat por trás de uma única interface Transport."
tags: "transports, overview"
title: "Transportes"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "transports, WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, email, SMS"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transportes"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 11
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transportes"
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
twitter_description: "Overview of rousseau-agent's nine chat transports: WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, Email, SMS. Every transport implements Start / Stop / Deliver."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transportes"
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

## A interface Transport

Cada transporte implementa uma pequena interface (`internal/transport/transport.go`):

```go
type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

Acima do transporte fica o `Router`, que trata do lookup de sessão por remetente, aplicação da allowlist e despacho para o `Agent`. Abaixo fica o código de wire específico do transporte.

Nenhum dos transportes distribuídos expõe uma superfície HTTP pública por padrão. É uma escolha deliberada de postura — daemons rousseau devem ser seguros para rodar atrás de NAT sem regras de port-forwarding.

## Transportes suportados

| Transporte | Inbound | Outbound | Biblioteca / protocolo de apoio | Autenticação | Setup em uma linha |
|---|:---:|:---:|---|---|---|
| [WhatsApp](/pt-BR/transports/whatsapp/) | sim | sim | `go.mau.fi/whatsmeow` | Pareamento de dispositivo (QR) | `rousseau whatsapp --allow <jid>` |
| [Signal](/pt-BR/transports/signal/) | sim | sim | `signal-cli` JSON-RPC | Conta pré-registrada | `rousseau signal --account +447900123456` |
| [Telegram](/pt-BR/transports/telegram/) | sim | sim | Long-polling da Bot API | Token do BotFather | `rousseau telegram --token <token>` |
| [Matrix](/pt-BR/transports/matrix/) | sim | sim | API cliente-servidor `/sync` | Access token | `rousseau matrix --homeserver-url … --access-token …` |
| [Slack](/pt-BR/transports/slack/) | sim | sim | Socket Mode + Web API | `xapp-*` + `xoxb-*` | `rousseau slack --app-token … --bot-token …` |
| [Discord](/pt-BR/transports/discord/) | sim | sim | Gateway v10 + REST | Bot token | `rousseau discord --token <token>` |
| [iMessage](/pt-BR/transports/imessage/) | sim | sim | Polling HTTP do BlueBubbles | Senha do servidor | `rousseau imessage --base-url … --password …` |
| [Email](/pt-BR/transports/email/) | sim | sim | IMAP + SMTP | Usuário + senha | `rousseau email --imap-addr … --smtp-addr …` |
| [SMS](/pt-BR/transports/sms/) | não | sim | REST do Twilio ou Vonage | Account SID / API key | `rousseau sms --provider twilio --account-sid … --auth-token …` |

## Por que não há superfície HTTP pública

Duas escolhas de design mantêm cada transporte listado longe de um webhook público:

- **Inbound baseado em WebSocket.** Slack Socket Mode e Discord Gateway são, do ponto de vista do daemon, apenas outbound — o daemon disca até o fornecedor sobre TLS e as mensagens chegam pela mesma conexão.
- **Polling.** WhatsApp, Telegram, Matrix, iMessage e email buscam atualizações em sua própria cadência. Não há webhook para o fornecedor chamar.

SMS é a exceção, e o rousseau resolve isso tornando o SMS **apenas de envio**. SMS de entrada exigiria um webhook Twilio / Vonage, que é exatamente a superfície que este projeto se recusa a introduzir.

## Comportamento do router

O router (`internal/transport/router.go`) fica entre cada transporte e o `Agent`:

- **Isolamento de sessão.** Cada valor distinto de `From` recebe sua própria `Session`, para que conversas paralelas não se contaminem. Identidades LID do WhatsApp são primeiro normalizadas para JIDs de telefone (veja `internal/transport/whatsapp/resolve.go`).
- **Allowlist.** Cada transporte que suporta inbound tem um `Allowlist []string` em sua config. Vazio significa "aceite todo remetente" — para daemons, você sempre quer pelo menos uma entrada.
- **Despacho.** O router serializa turnos por sessão para que um usuário não consiga empilhar duas mensagens de entrada concorrentes.

## Adicionando um décimo transporte

Implemente `transport.Transport` (três métodos). Adicione um tipo `Config` espelhando o layout de bloco sob `internal/config/`. Conecte um comando CLI em `internal/cli/`. Essa é a superfície — o core do agente permanece intocado.

## Páginas por transporte

- [WhatsApp](/pt-BR/transports/whatsapp/)
- [Signal](/pt-BR/transports/signal/)
- [Telegram](/pt-BR/transports/telegram/)
- [Matrix](/pt-BR/transports/matrix/)
- [Slack](/pt-BR/transports/slack/)
- [Discord](/pt-BR/transports/discord/)
- [iMessage](/pt-BR/transports/imessage/)
- [Email](/pt-BR/transports/email/)
- [SMS](/pt-BR/transports/sms/)
