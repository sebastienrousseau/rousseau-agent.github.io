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
description: "Schedule a rousseau cron job that summarises git log every evening and posts the result to WhatsApp."
keywords: "cron, git log, changelog, whatsapp, scheduled prompt, deliver-to"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/tutorials/nightly-changelog/"
subtitle: "A daily 18:00 cron job that pushes a git-log summary to WhatsApp."
tags: "tutorials, cron, changelog, whatsapp, git"
title: "Tutorial: changelog noturno"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, git log, changelog, whatsapp, scheduled prompt, deliver-to"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorial: changelog noturno"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/nightly-changelog/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/nightly-changelog/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorial: changelog noturno"
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
twitter_description: "Schedule a rousseau cron job that summarises git log every evening and posts the result to WhatsApp."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorial: changelog noturno"
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

Um job de cron armazenado no próprio estado SQLite do rousseau (tabela `cron_jobs`, schema em `internal/state/sqlite/cron.go`) que dispara às 18:00 horário local em dias úteis. Ele roda um prompt que pede ao modelo para resumir `git log --since=today` e entrega o resultado no seu celular pelo WhatsApp.

Tempo estimado: 10 minutos.

## Pré-requisitos

- Bridge de WhatsApp já pareado (veja [Quickstart](/pt-BR/quickstart/) passo 4 ou [Transportes: WhatsApp](/pt-BR/transports/whatsapp/)).
- O daemon `rousseau whatsapp` rodando — o scheduler de cron em `internal/cron/scheduler.go` é inicializado pelos daemons de transporte via `wiring.startCron()`, não pelo `rousseau chat`.
- Um workspace contendo o repo git que você quer resumido, bind-mountado no contêiner (ou no host se você roda rousseau fora de um contêiner).

## Como o cron do rousseau funciona

`rousseau cron add` escreve uma linha na tabela `cron_jobs` (`internal/state/sqlite/cron.go`). A cada ~15 segundos, `scheduler.sync` relê a tabela e reconcilia o schedule em memória do robfig/cron/v3. Quando um job dispara, o scheduler emite `cron.firing`, roda o prompt pelo provider configurado e entrega o resultado a `deliver_to` via o bridge de transporte que é dono do processo (WhatsApp neste tutorial).

Nomes de log estruturado que você verá (de `internal/cron/scheduler.go`):

- `cron.started` — scheduler inicializado com `poll_interval=…`.
- `cron.scheduled` — um job foi aceito.
- `cron.firing` — um job está prestes a rodar.
- `cron.completed` — um job terminou com sucesso.
- `cron.run_failed`, `cron.delivery_failed`, `cron.record_failed` — modos de falha.

## Passo 1: adicione o job

```sh
rousseau cron add \
  --name        nightly-changelog \
  --schedule    "0 18 * * 1-5" \
  --prompt      "Summarise git log --since=yesterday under /workspace/rousseau-agent as a Slack-style bullet list. Keep it under 200 words. If nothing changed, reply with a single line 'no commits'." \
  --deliver-to  447900123456@s.whatsapp.net
```

A expressão cron é interpretada por `robfig/cron/v3` em `newCronAddCmd` (`internal/cli/cron.go`). Expressões inválidas são rejeitadas antes da escrita. O valor `--deliver-to` é o JID E.164 para WhatsApp (`<dígitos>@s.whatsapp.net`); o formato do alvo de entrega é específico do transporte.

## Passo 2: verifique

```sh
rousseau cron list
```

Formato da saída (de `newCronListCmd`):

```
NAME               STATUS SCHEDULE       PROMPT                       DELIVER-TO
nightly-changelog  on     0 18 * * 1-5   Summarise git log …          447900123456@s.whatsapp.net
```

A lista também é exposta via MCP como `rousseau_cron_list` (veja `internal/mcp/tools.go`).

## Passo 3: dry-run

Não há trigger embutido de "disparar agora". Para smoke-test, agende temporariamente o job um minuto no futuro:

```sh
rousseau cron remove nightly-changelog
rousseau cron add --name test --schedule "*/1 * * * *" --prompt "say hi" --deliver-to "$JID"
journalctl --user -u rousseau-agent -f | grep cron.
```

Sequência de log esperada:

```
INFO cron.scheduled  job=test expr=*/1 * * * *
INFO cron.firing     job=test
INFO cron.completed  job=test
```

Remova o job de teste e re-adicione o real quando terminar.

## Passo 4: aperte o prompt

Os melhores prompts de cron são autocontidos: o modelo não tem memória de execuções anteriores. Inclua o caminho do repo, o formato de saída esperado e um fallback para o caso vazio. Exemplo de segunda iteração:

```
Summarise commits authored since 07:00 UTC today under
/workspace/rousseau-agent. Use this format:

- <short type>: <one-line summary> — <sha>

Group by author. If no commits landed, reply exactly: no commits.
```

## Alternando e removendo

```sh
rousseau cron disable nightly-changelog   # keeps the row, stops firing
rousseau cron enable  nightly-changelog
rousseau cron remove  nightly-changelog   # deletes the row
```

`SetEnabled` e `Delete` de `internal/state/sqlite/cron.go` são o que estes chamam.

## Relacionado

- [Cron](/pt-BR/cron/) — referência para o scheduler.
- [Guias: Tarefas agendadas](/pt-BR/guides/scheduled-tasks/) — discussão mais profunda.
- [Transportes: WhatsApp](/pt-BR/transports/whatsapp/) — como o delivery-to funciona.
- [Referência: Comandos CLI](/pt-BR/reference/cli-commands/) — cada flag de `rousseau cron`.
