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
description: "Worked example: use rousseau-agent's cron scheduler + WhatsApp to run a scheduled prompt daily and deliver the result to your phone."
keywords: "cron, scheduled tasks, whatsapp, code review, robfig, daily reminder"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/guides/scheduled-tasks/"
subtitle: "Nag yourself daily via WhatsApp."
tags: "guides, cron, scheduled, whatsapp"
title: "Guia: tarefas agendadas"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, scheduled tasks, whatsapp, code review, robfig, daily reminder"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guia: tarefas agendadas"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 31
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/scheduled-tasks/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/scheduled-tasks/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guia: tarefas agendadas"
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
twitter_description: "Worked example: use rousseau-agent's cron scheduler + WhatsApp to run a scheduled prompt daily and deliver the result to your phone."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guia: tarefas agendadas"
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

## Cenário

Você quer um lembrete diário no WhatsApp às 09:00 perguntando se a caixa de entrada de code review tem algo pendente. O agente deve ler seu arquivo local de fila de revisão, resumir e entregar o resumo no seu celular — independentemente de seu laptop estar no meio de outra tarefa.

As peças móveis:

- Um daemon `rousseau whatsapp` em execução.
- Um job de cron persistido em SQLite via `rousseau cron add`.
- A goroutine do scheduler `robfig/cron/v3` dentro do daemon dispara o job; a resposta é despachada pelo mesmo transporte WhatsApp.

## Pré-requisitos

- `rousseau whatsapp` pareado e entregando mensagens para pelo menos um JID ([Primeiro transporte](/pt-BR/getting-started/first-transport/)).
- Um arquivo para o qual o prompt pode apontar — para este passo a passo, uma fila em Markdown em `/workspace/review-queue.md`.

## Passo 1 — Registrar o job

```sh
rousseau cron add \
  --name daily-review-nag \
  --schedule "0 9 * * *" \
  --prompt "Read /workspace/review-queue.md and list every PR that has been open for more than 3 days. Reply with 3 bullets max." \
  --deliver-to 447900123456@s.whatsapp.net
```

`--schedule` é uma expressão cron POSIX de 5 campos interpretada por `robfig/cron/v3` (`min hour dom mon dow`). O Rousseau valida a expressão no momento da adição; um agendamento inválido falha rapidamente antes de ir para o store.

`--deliver-to` é o JID do WhatsApp que receberá a resposta. Para grupos, use a forma `@g.us`.

## Passo 2 — Confirmar que o job está ativo

```sh
rousseau cron list
```

Saída:

```
b7a3f2e1  on   daily-review-nag      0 9 * * *             last=never
    Read /workspace/review-queue.md and list every PR that has been open for more than 3 days. Reply with 3 bullets max. → 447900123456@s.whatsapp.net
```

Novos jobs ficam ativos no próximo intervalo de poll do scheduler (padrão 60 segundos). Nenhum restart necessário.

## Passo 3 — Forçar uma execução de teste

Jobs agendados são disparados pelo daemon `rousseau whatsapp` em execução. Para verificar a fiação sem esperar até as 09:00, altere temporariamente o agendamento para rodar em um minuto:

```sh
rousseau cron remove daily-review-nag
rousseau cron add \
  --name daily-review-nag \
  --schedule "*/1 * * * *" \
  --prompt "..." \
  --deliver-to 447900123456@s.whatsapp.net
```

Observe o log do daemon:

```
cron.fire   name=daily-review-nag job=b7a3f2e1
tool.execute name=read id=t_1
cron.deliver name=daily-review-nag target=447900123456@s.whatsapp.net bytes=284
```

Assim que ver a mensagem no seu celular, apague a cópia de cada minuto e re-adicione a versão diária.

## Passo 4 — Desabilitar sem apagar

```sh
rousseau cron disable daily-review-nag
```

Alternar `enabled=false` deixa o job no store, mas o pula em cada disparo. Reative com `rousseau cron enable daily-review-nag`.

## O que acontece por baixo dos panos

1. `rousseau cron add` escreve uma linha na tabela `cron` em `~/.local/share/rousseau/sessions.db`.
2. O daemon `rousseau whatsapp` inicia uma goroutine do scheduler `robfig/cron/v3` no boot e faz poll da tabela a cada `PollInterval` (60s padrão).
3. Quando a expressão cron dispara, `Runner.RunOnce(ctx, prompt)` executa um turno de agente único contra uma sessão nova (sem histórico de disparos anteriores).
4. A resposta passa por `Delivery` — um callback agnóstico de transporte que o daemon conecta a `client.Deliver(ctx, target, body)`.
5. `last_run_at` é atualizado no store. Falhas são registradas em log, mas não desabilitam o job.

O scheduler é durável: se o daemon morrer no meio de um disparo, o próximo lançamento retoma a fila. Jobs nunca disparam duas vezes no mesmo minuto porque `robfig/cron/v3` deduplica por tick.

## Padrões comuns

| Agendamento | Significado |
|---|---|
| `0 9 * * *` | 09:00 todos os dias. |
| `*/15 9-17 * * 1-5` | A cada 15 minutos, 09:00–17:59, Seg–Sex. |
| `0 * * * *` | Início de cada hora. |
| `0 0 * * 0` | Meia-noite todo domingo. |

## Combinando com skills

Prompts longos ficam tediosos. Se o prompt de um job agendado continuar crescendo, mova o boilerplate para uma [skill](/pt-BR/skills/) e faça o prompt referenciá-la. A skill é acoplada ao system prompt no momento do disparo.

## Ressalvas

- Jobs agendados rodam contra o provider configurado do daemon. Se seu provider primário for `claudecli` e você rotacionar o login `claude` subjacente, o disparo falha até você reautenticar.
- O alvo de entrega deve pertencer à allowlist do daemon. O Rousseau não entregará a um JID fora da allowlist, mesmo que um job agendado peça.
- O scheduler de cron roda dentro do daemon `rousseau whatsapp` por design. Rodar `rousseau slack` ao lado te dá dois schedulers independentes lendo a mesma tabela — jobs vão disparar duas vezes. Escolha um daemon para ser o dono do agendamento.

## Próximo

- [Referência de cron](/pt-BR/cron/) — cada subcomando, cada flag.
- [Skills](/pt-BR/skills/) — compartilhe boilerplate de prompt entre jobs.
- [Auditoria + políticas de aprovação](/pt-BR/guides/audit-approval-policies/) — restrinja o que o prompt agendado pode fazer.
