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
description: "Set up rousseau-agent's Slack transport: Socket Mode (xapp-* app token + xoxb-* bot token), no public webhook, allowlist by user ID."
keywords: "Slack, Socket Mode, xapp, xoxb, chat.postMessage, connections:write, no webhook, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/transports/slack/"
subtitle: "Socket Mode with no public HTTP surface."
tags: "transports, Slack"
title: "Transporte Slack"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Slack, Socket Mode, xapp, xoxb, chat.postMessage, connections:write, no webhook, allowlist"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transporte Slack"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 16
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/slack/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/slack/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transporte Slack"
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
twitter_description: "Set up rousseau-agent's Slack transport: Socket Mode (xapp-* app token + xoxb-* bot token), no public webhook, allowlist by user ID."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transporte Slack"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">O que você vai aprender</span><p>O passo a passo completo do wizard em app.slack.com, os escopos OAuth exatos a conceder, event subscriptions a configurar, como o Socket Mode evita a necessidade de um webhook público e como funciona a prevenção de loop de mensagem própria do rousseau. Leia <code>internal/transport/slack/client.go</code> junto a esta página.</p></aside>

## Visão geral

O transporte Slack (`internal/transport/slack/`) usa **Socket Mode** — um WebSocket de saída para o Slack — para que o daemon não precise de superfície HTTP pública. Eventos de entrada fluem pelo socket; chamadas de saída atingem a Web API padrão (`chat.postMessage`).

<aside class="admonition" data-type="tip"><span class="admonition-title">Por que Socket Mode</span><p>A alternativa (Events API + Request URL) requer um endpoint HTTPS público com um certificado SSL. O rousseau não entrega nenhuma superfície HTTP de entrada por design, então o Socket Mode é o único caminho de ingresso suportado.</p></aside>

## Dois tokens

O Slack Socket Mode requer dois tokens com responsabilidades disjuntas:

| Token | Prefixo | Escopo | Finalidade |
|---|---|---|---|
| Token app-level | `xapp-` | `connections:write` | Abre o WebSocket do Socket Mode. |
| Token de bot | `xoxb-` | `chat:write` + event subscriptions | Envia mensagens, se inscreve em eventos. |

## Configuração do app

Passo a passo completo em https://app.slack.com/apps :

1. **Crie um novo app** ("From scratch"). Escolha um workspace.
2. **Habilite Socket Mode** (Settings → Socket Mode). Gere um **app-level token** com `connections:write`. Este é o token `xapp-*`.
3. **Configure event subscriptions** (Features → Event Subscriptions). Inscreva-se em `message.channels`, `message.im` ou quaisquer escopos de canal que o bot deve ouvir. Você **não** precisa de uma Request URL porque o Socket Mode entrega eventos pelo socket.
4. **Adicione escopos de bot** (Features → OAuth & Permissions). Mínimo: `chat:write`. Adicione `im:history`, `channels:history`, `groups:history` ou `mpim:history` correspondentes aos seus event subscriptions.
5. **Instale o app no workspace.** A tela de instalação retorna o token de bot `xoxb-*`.
6. **Opcionalmente registre o próprio user ID do bot** (começa com `U…`). É isso que o rousseau usa para prevenção de loop de mensagens próprias.

## Configuração

```yaml
slack:
  app_token: "xapp-1-A0..."
  bot_token: "xoxb-1234..."
  bot_user_id: "U0123ABCD"
  reply_header: ""
  allowlist:
    - "U0ALICE"
    - "U0BOB"
```

| Campo | Padrão | Efeito |
|---|---|---|
| `app_token` | *obrigatório* | Token app-level `xapp-*` com `connections:write`. |
| `bot_token` | *obrigatório* | Token de bot `xoxb-*` com `chat:write`. |
| `bot_user_id` | *vazio* | ID `U…` do usuário bot para prevenção de loop de mensagem própria. Opcional; recorre à inspeção do campo `bot_id`. |
| `reply_header` | *vazio* | Anteposto a cada mensagem de saída. |
| `allowlist` | `[]` | IDs de usuário Slack cujas mensagens são tratadas. |

## Linha de comando

```sh
rousseau slack \
  --app-token xapp-... \
  --bot-token xoxb-... \
  --bot-user-id U0123ABCD
```

## Formato de wire

- **Entrada.** O Slack envia envelopes JSON pelo WebSocket. O rousseau faz ACK do envelope, extrai o texto da mensagem e o remetente, e o entrega ao handler.
- **Saída.** `POST https://slack.com/api/chat.postMessage` com `{"channel": "<id>", "text": "…"}` e `Authorization: Bearer <bot_token>`.

## Escopos OAuth explicados

Cada escopo concede uma superfície de API específica. Os escopos de que o rousseau precisa e o que quebra sem eles:

| Escopo | Endpoint usado | Quebra sem |
|---|---|---|
| `connections:write` | `apps.connections.open` (WebSocket do Socket Mode) | Não consegue abrir o socket. **Obrigatório.** |
| `chat:write` | `chat.postMessage` | Não consegue responder a nenhuma mensagem. **Obrigatório.** |
| `im:history` | `conversations.history` para DMs (indireto via eventos) | O bot não verá o conteúdo de DMs em eventos. |
| `im:read` | `im.list`, metadata de DM | Não consegue listar DMs abertas. |
| `im:write` | `conversations.open` | Não consegue abrir uma nova DM (só relevante se você quer que o bot envie DM a alguém sem prompt). |
| `mpim:history`, `channels:history`, `groups:history` | IMs multi-party / canais / canais privados | O bot não verá conteúdo de mensagem fora de DMs. |

Defina os escopos em *OAuth &amp; Permissions &gt; Bot Token Scopes*. Adicione apenas escopos que você realmente precisa — o Slack mostra um aviso no momento da instalação sobre cada escopo, e usuários finais são mais propensos a instalar um bot com uma superfície de permissão estreita.

## Prevenção de loop de mensagem própria

Sem proteção, um bot que responde a mensagens também verá suas próprias respostas como eventos de entrada — levando a loops descontrolados. O rousseau trata disso via `bot_user_id`:

```go
// Simplified — actual logic in internal/transport/slack/client.go
if msg.User == cfg.BotUserID {
    continue // Skip: this is our own outbound message echoing back.
}
```

Recupere o user ID do seu bot uma vez via:

```sh
curl -H "Authorization: Bearer xoxb-your-token" \
  https://slack.com/api/auth.test
```

A resposta inclui `user_id`. Cole em `slack.bot_user_id` na configuração, ou passe com `--bot-user-id`.

<aside class="admonition" data-type="warning"><span class="admonition-title">Prevenção de loop de fallback</span><p>Mesmo sem <code>bot_user_id</code>, o transporte ignora eventos do subtipo <code>bot_message</code>. Mas depender apenas do subtipo é frágil — defina <code>bot_user_id</code> em produção.</p></aside>

## Threading

Mensagens Slack carregam um `thread_ts` quando são respostas em uma thread. As chamadas de saída do rousseau incluem `thread_ts` quando o evento de entrada tinha um, para que respostas do bot permaneçam em thread. Mensagens de nível superior se tornam novas threads apenas quando o usuário inicia uma.

## Modos de falha

| Sintoma | Correção |
|---|---|
| `invalid_auth` na abertura do socket | O `app_token` está errado ou perdeu `connections:write`. Regenere. |
| Eventos de entrada nunca chegam | Verifique se **Event Subscriptions** está habilitado e os eventos `message.*` relevantes estão inscritos. |
| O bot responde às próprias mensagens | Defina `bot_user_id` na configuração. |
| `not_in_channel` no envio | Convide o bot para o canal (`/invite @rousseau-bot`). |
| DM funciona mas canal não | Escopo `channels:history` ausente, ou o bot não foi convidado para o canal. |

## Solução de problemas

### `invalid_auth` na abertura do socket

O token `xapp-…` está errado ou perdeu seu escopo. Regenere em *Basic Information &gt; App-Level Tokens*, garanta que `connections:write` está no novo token.

### `not_authed` no `chat.postMessage`

Token de bot (`xoxb-…`) ausente ou errado. Regenere em *OAuth &amp; Permissions &gt; Bot User OAuth Token*.

### Eventos chegam mas o rousseau não responde a nenhum

Verifique a allowlist. No modo `pattern` com `default: deny`, usuários não listados são silenciosamente descartados. Procure por `router.transport.rejected` nos logs.

### `channel_not_found` na saída

O ID do canal Slack (`C…`) mudou — por exemplo, um canal foi arquivado e recriado. Atualize quaisquer IDs de canal hardcoded. O rousseau normalmente usa o canal do evento de entrada, então isso só acontece com entrega de cron para um canal fixo.

### O bot aparece offline no Slack

O Socket Mode deixa o WebSocket ocioso a cada ~30s. Se o Slack mostra o bot como offline, verifique: (1) o daemon está rodando (`systemctl --user status`), (2) o WebSocket está conectado (linha de log `slack.connected`), (3) o relógio da máquina está dentro de 30s do tempo verdadeiro.

## Páginas relacionadas

- [Começando: Seu primeiro transporte](/pt-BR/getting-started/first-transport/) — passo a passo de ponta a ponta.
- [Configuração](/pt-BR/configuration/) — o bloco de configuração `slack`.
- [Transportes](/pt-BR/transports/) — transportes irmãos.
- [Implantação](/pt-BR/deployment/) — executando o Slack em um contêiner Podman.
- [Guias: Auditoria e Políticas de aprovação](/pt-BR/guides/audit-approval-policies/) — conjuntos de regras de política para um workspace Slack compartilhado.

## Leitura complementar

- `internal/transport/slack/client.go` — conexão Socket Mode, event pump, `chat.postMessage`.
- `internal/cli/slack.go` — wiring do CLI.
- `internal/transport/router.go` — imposição da allowlist.
- [Docs da API Slack: Socket Mode](https://api.slack.com/apis/socket-mode).
