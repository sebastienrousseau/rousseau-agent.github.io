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
description: "Use case narrative: reviewing pull requests from WhatsApp on the train, driven by rousseau-agent on a home box."
keywords: "mobile review, whatsapp, pr review, commute, use case, pull request"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/use-cases/mobile-review/"
subtitle: "Reviewing PRs from your phone on the train."
tags: "use-cases, whatsapp, mobile, pr"
title: "Caso de uso: revisão de PR pelo celular"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mobile review, whatsapp, pr review, commute, use case, pull request"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Caso de uso: revisão de PR pelo celular"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 72
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/use-cases/mobile-review/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/mobile-review/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Caso de uso: revisão de PR pelo celular"
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
twitter_description: "Use case narrative: reviewing pull requests from WhatsApp on the train, driven by rousseau-agent on a home box."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Caso de uso: revisão de PR pelo celular"
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

## A história

Você é staff engineer em uma empresa de porte médio. Sua caixa de entrada tem oito PRs abertos esperando sua revisão. Você está em uma viagem de trem de 45 minutos e tem sinal mas não tem laptop. Historicamente, revisar PR pelo celular significa apertar os olhos na view de diff do GitHub e digitar comentários vazios "LGTM".

O rousseau vive no pequeno Intel NUC no seu closet. Ele tem uma conexão WhatsApp para o seu JID, `bypassPermissions` no CLI `claude` local e acesso de leitura aos seus checkouts locais dos três repos que você revisa. Você manda DM no WhatsApp:

> review PR #4821 in checkout-service

O rousseau roda `gh pr diff 4821`, lê o código e responde:

> PR #4821 adds retry-with-backoff to the Stripe webhook handler. Three observations:
>
> 1. The backoff is uncapped — if Stripe is truly down, we'll accumulate goroutines forever. Suggest a `context.WithTimeout` at the caller.
> 2. Test file adds two new tests but neither covers the timeout path.
> 3. `pkg/webhook.go:82` — the mutex is held across the network call. Minor.
>
> Should I draft a review comment stub?

Você responde:

> yes, with all three

O rousseau usa `gh pr review` com `--draft` (approver bloqueia aprovação final; um humano ainda precisa clicar em "submit review"). Quando você chega na sua mesa, o comentário draft está esperando.

## O que isso requer

### O daemon

Rousseau no NUC como um contêiner Podman rootless:

- **Provider**: `claudecli` — herda sua auth local do Claude Code.
- **Transporte**: WhatsApp — o transporte de escolha para alcance mobile.
- **Estado**: `~/.local/share/rousseau/sessions.db`.

### Config

```yaml
provider: claudecli

claudecli:
  binary: claude
  permission_mode: bypassPermissions

whatsapp:
  reply_header: "🚂 *rousseau*\n\n"

log:
  level: info
  format: text                # this is a single-user daemon; text logs are fine

agent:
  max_iterations: 32
  compression:
    enabled: true             # subscription-tier claudecli; compression is free
    trigger_messages: 60
    keep_recent: 8
  approver:
    mode: pattern
    default: deny
    reason: "denied — this daemon reviews code, it does not merge it"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(gh pr view|gh pr diff|gh pr list|gh pr review --draft|gh pr comment|git status|git diff|git log|git show) "}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(go test|go vet|go build|npm test|pnpm test|cargo check) "}
    deny:
      - {tool: bash, match: "gh pr merge|gh pr close|gh pr approve"}
      - {tool: bash, match: "git (push|reset --hard|clean)"}
      - {tool: write, match: "\"path\":\"/etc/|/root/|/var/"}
      - {tool: edit,  match: "\"path\":\"/etc/|/root/|/var/"}
```

### Os bind mounts

- `~/repos/checkout-service/` (somente leitura).
- `~/repos/payments-api/` (somente leitura).
- `~/repos/web-frontend/` (somente leitura).
- `~/.claude/` — tokens OAuth do Claude Code (leitura-escrita, mas só para refresh de token).
- `~/.config/gh/` — token OAuth do GitHub CLI (leitura-escrita, mesma razão).

Mounts somente leitura previnem o modelo de acidentalmente editar sua working copy. Revisões vão pelo GitHub, não pelo seu checkout.

### Primeiro launch

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

Você escaneia o QR code uma vez. Daí em diante o daemon vive na unidade Quadlet e inicia no restart do host. Sua allowlist é o JID do seu próprio celular pessoal.

## A postura de segurança

- **Allowlist trava o transporte.** Só seu celular pode dirigir o daemon. Qualquer outro que por acaso descubra o número de telefone é silenciosamente descartado.
- **Approver pattern bloqueia todo merge / push / close.** O rousseau revisa, faz drafts e comenta — um humano ainda precisa clicar "Merge" ou "Approve".
- **Mounts somente leitura** protegem seus checkouts de trabalho.
- **`bypassPermissions` no claudecli** só é tolerável porque o approver está fazendo o trabalho de segurança. Nunca combine `bypassPermissions` com `mode: allow_all`.

## O alcance

- **O sinal cai no metrô.** A backpressure do WhatsApp é graciosa — você envia uma pergunta, você recebe uma resposta quando o daemon tem sinal para responder. O rousseau não precisa manter uma sessão TCP ao vivo com seu celular.
- **Voice notes funcionam.** Com [modo de voz](/pt-BR/user-guide/voice-mode/) habilitado e `whisper.cpp` instalado no NUC, você pode ditar uma voice note "what's the diff on 4821" e receber uma resposta em texto. Útil quando digitar no celular num trem em movimento é irritante.
- **O daemon roda no seu hardware.** Nada sobre seu raciocínio de revisão vai para um SaaS de terceiros. A única chamada outbound é o subprocesso do CLI `claude` para a Anthropic, usando sua assinatura existente.

## O que o rousseau não faz aqui

- **Não clica em "Merge".** Essa é uma decisão humana, e o approver a reforça.
- **Não aprende seu estilo de revisão.** O próximo PR recebe a mesma checklist genérica a menos que você escreva uma [skill](/pt-BR/skills/) capturando seu estilo.
- **Não coloca revisões em fila.** Cada request é independente; não há job de background "review all my open PRs" (a menos que você conecte um via [cron](/pt-BR/guides/scheduled-tasks/)).

## O que você mudaria sob carga

- Adicione uma [skill](/pt-BR/skills/) chamada `pr-review-checklist.md` que codifica as seis coisas que você sempre checa. Skills são acopladas ao system prompt quando um trigger correspondente aparece na mensagem do usuário.
- Adicione um cron noturno: `0 8 * * 1-5 rousseau ... deliver a summary of every open PR`.
- Mude para um caminho de API paga da Anthropic se os rate limits da assinatura `claudecli` viram um gargalo. Zero mudanças de config downstream.

## Páginas relacionadas

- [Transporte WhatsApp](/pt-BR/transports/whatsapp/) — a referência do transporte.
- [Provider claudecli](/pt-BR/providers/claudecli/) — auth herdada.
- [Skills](/pt-BR/skills/) — como codificar seu estilo de revisão.
- [Modo de voz](/pt-BR/user-guide/voice-mode/) — dite revisões.
