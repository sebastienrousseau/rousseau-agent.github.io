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
description: "Wire rousseau-agent to a Slack channel that runs read and grep over the workspace whenever an operator asks."
keywords: "slack, code review, socket mode, read tool, grep tool, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/tutorials/build-a-code-review-bot/"
subtitle: "A Slack channel that lets rousseau review a repo on demand."
tags: "tutorials, slack, code review, socket mode, read, grep"
title: "Tutorial: construir um bot de revisão de código"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "slack, code review, socket mode, read tool, grep tool, allowlist"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorial: construir um bot de revisão de código"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 42
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/build-a-code-review-bot/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/build-a-code-review-bot/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorial: construir um bot de revisão de código"
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
twitter_description: "Wire rousseau-agent to a Slack channel that runs read and grep over the workspace whenever an operator asks."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorial: construir um bot de revisão de código"
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

## O que você constrói

Um canal Slack privado onde membros da equipe mencionam `@rousseau` com um caminho de repositório e uma pergunta. O Rousseau navega pelo workspace, executa `read` e `grep` de `internal/tools/builtin/` e posta uma resposta com referências de linha citadas. Sem superfície HTTP pública — o Slack Socket Mode dirige tudo pelo WebSocket de saída.

Tempo estimado: 20 minutos, assumindo que você já tenha acesso de admin no Slack a um workspace.

## Pré-requisitos

- Rousseau instalado e um provider configurado (veja [Quickstart](/pt-BR/quickstart/)).
- Admin do workspace Slack.
- Um repositório já clonado em algum caminho sob seu `$HOME` — esse se torna o "workspace" sobre o qual o bot pode fazer `read`/`grep`.

## Passo 1: criar um app Slack

O Socket Mode do Slack é o que torna esse bot possível: seu daemon abre um WebSocket de saída para o Slack, sem ingress necessário.

1. Vá para <https://api.slack.com/apps> e crie um novo app **do zero**.
2. Em **Socket Mode**, habilite-o e gere um **app-level token** com `connections:write`. Copie o valor `xapp-...`.
3. Em **OAuth & Permissions**, adicione estes **Bot Token Scopes**:
   - `chat:write`
   - `app_mentions:read`
   - `channels:history` (ou `groups:history` para canais privados)
4. Instale o app no seu workspace. Copie o **Bot User OAuth Token** — o valor `xoxb-...`.
5. Em **Event Subscriptions**, habilite eventos e inscreva o bot em `app_mention` e `message.channels` (ou `message.groups`).
6. Convide o bot para o canal de review: `/invite @rousseau`.

## Passo 2: configurar o rousseau

Adicione a `~/.config/rousseau/config.yaml`. Os campos relevantes vêm de `SlackConfig` em `internal/config/config.go`:

```yaml
provider: claudecli           # ou anthropic — o que você definiu no Quickstart

slack:
  app_token:  xapp-1-…
  bot_token:  xoxb-…
  bot_user_id: U0ROUSSEAU     # de https://api.slack.com/methods/auth.test
  reply_header: "*rousseau-agent*\n\n"
  allowlist:
    - U01ABC…                 # seus IDs de usuário Slack

agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
    # sem bash, sem write, sem edit — reviewer somente leitura
```

O `allowlist` restringe de quem o router aceita mensagens. O router em `internal/transport/router.go` emite `transport.rejected` para qualquer outro remetente.

## Passo 3: executar a bridge

```sh
rousseau slack \
  --app-token "$SLACK_APP_TOKEN" \
  --bot-token "$SLACK_BOT_TOKEN" \
  --bot-user-id "$SLACK_BOT_USER_ID"
```

`--bot-user-id` impede que o bot responda às próprias mensagens. Logs estruturados de `internal/transport/slack/client.go` vão mostrar:

```
INFO slack.started
INFO slack.incoming from=U01ABC channel=C01REVIEW text="…"
INFO tool.execute name=read id=t_1
INFO tool.execute name=grep id=t_2
```

## Passo 4: teste

No canal de review:

```
@rousseau look under /home/seb/repos/acme-api and tell me
where request logging is set up
```

O provider `claudecli` (ou Anthropic — o que você escolheu) vai chamar `read` e `grep` de `internal/tools/builtin/` contra o bind mount do workspace. Como o approver está em modo `pattern` com apenas `read` e `grep` em allowlist, o modelo não pode escrever nem sair para o shell — mesmo que um prompt comprometido peça.

## Passo 5: endurecer

Approvers em modo pattern são **regex sobre o JSON de input da ferramenta**. Para restringir `read` e `grep` a uma árvore de projeto específica:

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: "\"path\":\"/home/seb/repos/acme-api/[^\"]*\""}
      - {tool: grep, match: "\"path\":\"/home/seb/repos/acme-api\""}
```

Veja [Tutorial: Endurecer o approver](/pt-BR/tutorials/harden-approver-policy/) para o passo a passo completo de `default: deny` + auditoria.

## Implantando via systemd

Para qualquer coisa além de uma sessão de laptop, execute a bridge Slack sob a unit Quadlet do Podman em `docker/rousseau-agent.container` — troque `Exec=whatsapp --allow …` por `Exec=slack --app-token … --bot-token …`. Veja [Implantação](/pt-BR/deployment/) para a unit completa.

## Relacionado

- [Transportes: Slack](/pt-BR/transports/slack/)
- [Guia do usuário: Políticas de aprovação](/pt-BR/user-guide/approval-policies/)
- [Guia do usuário: Ferramentas](/pt-BR/user-guide/tools/)
- [Tutorial: Endurecer o approver](/pt-BR/tutorials/harden-approver-policy/)
