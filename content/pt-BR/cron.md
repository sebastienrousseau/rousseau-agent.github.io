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
changefreq: "weekly"
description: "rousseau-agent's cron scheduler runs stored jobs on a schedule and delivers replies through any registered transport. Backed by robfig/cron/v3 and SQLite job persistence."
keywords: "cron, robfig/cron, scheduler, scheduled jobs, delivery, transport-agnostic, SQLite persistence"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/cron/"
subtitle: "Tarefas agendadas persistentes que disparam por qualquer transporte."
tags: "cron, scheduler, reference"
title: "Agendador cron"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, robfig/cron, scheduler, scheduled jobs, delivery, transport-agnostic, SQLite persistence"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Agendador cron"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 24
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/cron/index.html"
item_link: "https://docs.rousseau-agent.dev/cron/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Agendador cron"
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
twitter_description: "rousseau-agent's cron scheduler runs stored jobs on a schedule and delivers replies through any registered transport. Backed by robfig/cron/v3 and SQLite job persistence."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Agendador cron"
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

O scheduler cron (`internal/cron/scheduler.go`) é uma goroutine que executa entradas `CronJob` armazenadas em seu agendamento configurado, executa o prompt de cada job pelo agente e entrega a resposta a uma função `Delivery` agnóstica ao transporte.

O scheduler roda ao lado de qualquer daemon de longa duração (tipicamente `rousseau whatsapp` ou outro transporte de chat). Os jobs são armazenados no mesmo banco SQLite das sessões, então sobrevivem a reinicializações.

## Sintaxe do agendamento

Baseado em [robfig/cron/v3](https://pkg.go.dev/github.com/robfig/cron/v3). O parser suporta:

- Cron padrão de 5 campos: `<minuto> <hora> <dia-do-mês> <mês> <dia-da-semana>`.
- Atalhos predefinidos: `@yearly`, `@monthly`, `@weekly`, `@daily`, `@hourly`, `@every <duração>`.

Exemplos de agendamento:

| Expressão | Dispara |
|---|---|
| `0 9 * * 1-5` | 09:00 em dias úteis |
| `*/15 * * * *` | A cada 15 minutos |
| `@daily` | Uma vez por dia à meia-noite (fuso do servidor) |
| `@every 30m` | A cada 30 minutos |

## CLI

```sh
# Lista todos os jobs armazenados.
rousseau cron list

# Adiciona um job.
rousseau cron add \
  --name morning-standup \
  --schedule '0 9 * * 1-5' \
  --prompt 'What are the top three engineering priorities today?' \
  --target '447900123456@s.whatsapp.net'

# Remove por nome ou ID.
rousseau cron remove morning-standup
```

## Configuração

Os jobs são armazenados no banco de estado, não no arquivo de config. Não há nada em `~/.config/rousseau/config.yaml` para configurar o scheduler em si; ele usa `PollInterval = 60s` por padrão.

## Fluxo de job

1. O scheduler re-sincroniza a lista de jobs do SQLite a cada `PollInterval`.
2. `robfig/cron/v3` dispara o job no horário agendado.
3. `TurnRunner.RunOnce(ctx, job.Prompt)` executa um agente em **turn único** contra uma sessão nova (sem histórico, sem recall entre sessões, a menos que o runner opte por isso).
4. O texto da resposta é passado para `Delivery(ctx, job.Target, replyText)`.
5. Se `Delivery` retornar erro → é registrado; o próximo tick tenta novamente.

## Entrega

`Delivery` é um tipo de função pequeno:

```go
type Delivery func(ctx context.Context, target, body string) error
```

O scheduler não importa `internal/transport` — o contrato de entrega é agnóstico ao transporte. Na prática, os daemons `rousseau <transport>` conectam um `Delivery` que resolve a string de target contra o transporte ativo (`Deliver` no cliente do transporte).

`target` é específico do transporte:

- WhatsApp: um JID (`447900123456@s.whatsapp.net`).
- Telegram: um ID de chat numérico.
- Slack: um ID de canal (`C012345`) ou ID de usuário (`U012345`).
- Discord: um ID de canal.
- SMS: um destino E.164.
- iMessage: um GUID de chat.
- Signal: um destino E.164.
- Matrix: um ID de sala.
- Email: um endereço RFC 5322 completo.

## Persistência

Os jobs são armazenados na tabela `cron_jobs` do banco de estado (`internal/state/sqlite/`). Campos: `id`, `name`, `schedule`, `prompt`, `target`, `created_at`, `updated_at`. Reinicializações captam cada job no próximo `PollInterval`.

Jobs novos adicionados via `rousseau cron add` ficam ativos em até um `PollInterval` — no máximo 60 segundos por padrão.

## Interação com transportes

A closure `Delivery` captura uma referência ao transporte em execução. Um único daemon tipicamente roda um transporte, então o scheduler cron entrega através desse transporte. Implantações multi-transporte rodam um daemon por transporte, e o operador aponta o `target` de cada job cron para o daemon do transporte correspondente.

Entrega entre transportes (o job roda no daemon WhatsApp, mas responde via Slack) não é suportada hoje — o scheduler só conhece o `Delivery` que recebeu.

## Modos de falha

| Sintoma | Correção |
|---|---|
| Job não dispara | Verifique `rousseau status`; o scheduler registra `cron.fired` por ativação. |
| Job dispara mas nada chega | Erro de entrega — verifique os logs por `cron.delivery_failed`. |
| Job roda mas o modelo se recusa a agir | Política de aprovação negando chamadas de ferramenta. Afrouxe `agent.approver` ou migre para o modo `pattern`. |
| A entrega vai para o alvo errado | O scheduler é agnóstico ao transporte; o daemon interpreta `target`. Confirme que o transporte rodando no seu daemon corresponde ao formato do target. |
