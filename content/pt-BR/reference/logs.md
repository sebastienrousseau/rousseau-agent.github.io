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
description: "rousseau-agent's slog output: message vocabulary, JSON vs text shape, and journalctl / jq recipes."
keywords: "slog, logs, json, text, journalctl, jq, observability"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/reference/logs/"
subtitle: "The full vocabulary of slog messages rousseau emits."
tags: "reference, logs, slog, observability, audit"
title: "Referência: logs"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "slog, logs, json, text, journalctl, jq, observability"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Referência: logs"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 52
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/logs/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/logs/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Referência: logs"
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
twitter_description: "rousseau-agent's slog output: message vocabulary, JSON vs text shape, and journalctl / jq recipes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Referência: logs"
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

## Setup do logger

`internal/cli/root.go` constrói um `*slog.Logger` por processo — um `slog.NewTextHandler` quando `log.format` está vazio ou é `text`, um `slog.NewJSONHandler` quando é `json`. O nível mapeia de `log.level` (`debug`, `info`, `warn`/`warning`, `error`) com `info` como padrão. O handler escreve em stderr; cada daemon o herda.

Para uma implantação em produção, sempre defina `log.format: json`. Pipelines de log downstream (journald + `journalctl -o json`, Loki, Vector, Datadog Agent) fazem parse de saída estruturada nativamente.

## Formato de saída

### Text

```
time=2026-07-13T18:00:14.202Z level=INFO msg=tool.execute name=grep id=t_1
```

Layout de texto padrão do slog: `time`, `level`, `msg`, depois pares key=value.

### JSON

```json
{"time":"2026-07-13T18:00:14.202Z","level":"INFO","msg":"tool.execute","name":"grep","id":"t_1"}
```

Mesmos campos, codificados em JSON. O campo `msg` é o identificador estável de evento — filtre e crie alertas por ele, não por texto humano.

## Vocabulário de mensagens

Cada nome de mensagem emitido a partir de `internal/**/*.go` está listado abaixo com local de origem e nível esperado. Agrupados por subsistema; alfabetizados dentro de um grupo.

### Loop do agente (`internal/agent/`)

| Mensagem | Nível | Campos | Significado |
|---|---|---|---|
| `agent.compressed` | INFO | `messages` | O compressor LLM reescreveu uma sessão; a nova contagem de mensagens é `messages`. |
| `agent.compress_failed` | WARN | `err` | O compressor retornou um erro; a sessão é deixada intocada. |
| `tool.denied` | WARN | `name`, `reason` | O approver bloqueou uma tool call. Campos de `internal/agent/agent.go:179`. |
| `tool.execute` | INFO | `name`, `id` | O approver permitiu e a ferramenta rodou. |
| `tool.error` | WARN | `name`, `err` | A ferramenta rodou mas retornou um erro. |
| `turn.failed` | ERROR | `err` | O turno na TUI deu erro. Emitido de `internal/tui/model.go`. |
| `session.save_failed` | WARN | `err` | Persistir uma sessão falhou pós-turno. |

### Cron (`internal/cron/scheduler.go`)

| Mensagem | Nível | Campos | Significado |
|---|---|---|---|
| `cron.started` | INFO | `poll_interval` | Boot do scheduler. |
| `cron.scheduled` | INFO | `job`, `expr` | Job adicionado ao schedule em memória. |
| `cron.schedule_failed` | WARN | `job`, `expr`, `err` | O robfig/cron/v3 rejeitou a expressão. |
| `cron.sync_failed` | WARN | `err` | Passada de reconciliação contra `cron_jobs` falhou. |
| `cron.firing` | INFO | `job` | Job está prestes a rodar. |
| `cron.completed` | INFO | `job` | Job terminou com sucesso. |
| `cron.run_failed` | ERROR | `job`, `err` | A chamada ao provider dentro do job falhou. |
| `cron.delivery_failed` | ERROR | `job`, `target`, `err` | Entrega ao transporte falhou. |
| `cron.record_failed` | WARN | `job`, `err` | Escrita de `last_run_at` falhou. |

### MCP (`internal/mcp/server.go`)

| Mensagem | Nível | Campos | Significado |
|---|---|---|---|
| `mcp.encode_error` | WARN | `err` | Não foi possível JSON-encode uma resposta (raro). |
| `mcp.tool_error` | WARN | `tool`, `err` | Um handler de tool retornou um erro; entregue ao host com `isError=true`. |

### Router (`internal/transport/router.go`)

| Mensagem | Nível | Campos | Significado |
|---|---|---|---|
| `transport.rejected` | WARN | `from` | Remetente não está na allowlist; mensagem descartada. |
| `router.save_failed` | WARN | `err` | Save de sessão pós-turno falhou. |
| `router.stale_mapping` | WARN | `jid`, `err` | O mapeamento JID→sessão apontava para uma sessão que não carrega mais. |

### WhatsApp (`internal/transport/whatsapp/`)

| Mensagem | Nível | Campos | Significado |
|---|---|---|---|
| `whatsapp.starting` | INFO | `store`, `allowlist` | Bridge dando boot; `store` é o DSN. |
| `whatsapp.qr_ready` | INFO | — | QR renderizado em stdout; escaneie. |
| `whatsapp.qr_event` | WARN | `event` | Evento de QR sem sucesso do whatsmeow. |
| `whatsapp.paired` | INFO | — | Telefone aceitou o QR. |
| `whatsapp.connected` | INFO | — | WebSocket para a Meta está ativo. |
| `whatsapp.disconnected` | WARN | — | Perdeu o socket. Tenta reconectar automaticamente. |
| `whatsapp.logged_out` | ERROR | `reason` | A Meta deslogou o dispositivo — geralmente uma penalidade de política. |
| `whatsapp.voice_enabled` | INFO | `binary`, `model` | Transcrição de mensagens de voz ligada. |
| `whatsapp.incoming` | INFO | `from` | Mensagem de entrada aceita. |
| `whatsapp.skipped` | DEBUG | `reason` | O router descartou uma mensagem (self-echo, etc). |
| `whatsapp.empty_reply` | INFO | `elapsed` | O agente não produziu texto neste turno. |
| `whatsapp.handler_ok` | INFO | `elapsed`, `bytes` | Resposta entregue. |
| `whatsapp.handler_failed` | ERROR | `err` | Turno deu erro — geralmente falha de provider ou de ferramenta. |
| `whatsapp.send_failed` | ERROR | `err` | Entrega para a Meta falhou. |
| `whatsapp.presence_failed` | DEBUG | `err` | Escrita de presence de digitação falhou (best-effort). |
| `whatsapp.audio_ignored` | INFO | `size` | Mensagem de voz recebida mas transcrição desabilitada. |
| `whatsapp.audio_downloaded` | INFO | `size` | Bytes da mensagem de voz baixados da Meta. |
| `whatsapp.transcribed` | INFO | `elapsed` | whisper.cpp retornou uma transcrição. |
| `whatsapp.transcribe_failed` | ERROR | `err` | Invocação do whisper falhou. |

### Slack (`internal/transport/slack/client.go`)

| Mensagem | Nível | Campos | Significado |
|---|---|---|---|
| `slack.starting` | INFO | `allowlist` | Bridge dando boot. |
| `slack.started` | INFO | — | Sessão de Socket Mode aceita. |
| `slack.session_failed` | WARN | `err` | Falha ao abrir a sessão Socket Mode; retry. |
| `slack.frame_failed` | WARN | `err` | Frame malformado do Slack. |
| `slack.incoming` | INFO | `from`, `channel`, `text` | Mensagem aceita. |
| `slack.handler_failed` | ERROR | `err` | Turno deu erro. |

### Discord (`internal/transport/discord/client.go`)

| Mensagem | Nível | Campos | Significado |
|---|---|---|---|
| `discord.starting` | INFO | `allowlist` | Bridge dando boot. |
| `discord.ready` | INFO | `bot_id` | Discord gateway pronto. |
| `discord.started` | INFO | — | Sessão ativa. |
| `discord.session_failed` | WARN | `err` | Abertura do gateway falhou; retry. |
| `discord.frame_failed` | WARN | `err` | Frame ruim do Discord. |
| `discord.incoming` | INFO | `from`, `channel` | Mensagem aceita. |
| `discord.handler_failed` | ERROR | `err` | Turno deu erro. |

### Telegram (`internal/transport/telegram/client.go`)

| Mensagem | Nível | Campos | Significado |
|---|---|---|---|
| `telegram.starting` | INFO | `allowlist` | Bridge dando boot. |
| `telegram.started` | INFO | — | Primeiro long-poll teve sucesso. |
| `telegram.poll_failed` | WARN | `err` | HTTP de long-poll falhou. |
| `telegram.incoming` | INFO | `from` | Mensagem aceita. |
| `telegram.handler_failed` | ERROR | `err` | Turno deu erro. |
| `telegram.send_failed` | ERROR | `err` | HTTP outbound falhou. |

### Matrix (`internal/transport/matrix/client.go`)

| Mensagem | Nível | Campos | Significado |
|---|---|---|---|
| `matrix.starting` | INFO | `homeserver`, `allowlist` | Bridge dando boot. |
| `matrix.started` | INFO | `homeserver` | Primeiro `/sync` aceito. |
| `matrix.sync_failed` | WARN | `err` | HTTP de `/sync` falhou. |
| `matrix.incoming` | INFO | `from`, `room` | Mensagem aceita. |
| `matrix.handler_failed` | ERROR | `err` | Turno deu erro. |
| `matrix.send_failed` | ERROR | `err` | HTTP outbound falhou. |

### Signal (`internal/transport/signal/`)

| Mensagem | Nível | Campos | Significado |
|---|---|---|---|
| `signal.starting` | INFO | `account`, `allowlist` | Subprocesso JSON-RPC do signal-cli iniciando. |
| `signal.started` | INFO | — | Subprocesso reportou pronto. |
| `signal.frame_failed` | WARN | `err` | Frame JSON malformado do signal-cli. |
| `signal.stderr` | WARN | `line` | Passthrough do stderr do signal-cli. |
| `signal.incoming` | INFO | `from` | Mensagem aceita. |
| `signal.handler_failed` | ERROR | `err` | Turno deu erro. |

### iMessage (`internal/transport/imessage/client.go`)

| Mensagem | Nível | Campos | Significado |
|---|---|---|---|
| `imessage.starting` | INFO | `base` | URL do servidor BlueBubbles logada. |
| `imessage.started` | INFO | `server` | Primeiro poll teve sucesso. |
| `imessage.prime_failed` | WARN | `err` | Fetch de priming de estado falhou; retries. |
| `imessage.poll_failed` | WARN | `err` | HTTP de poll falhou. |
| `imessage.incoming` | INFO | `from` | Mensagem aceita. |
| `imessage.handler_failed` | ERROR | `err` | Turno deu erro. |
| `imessage.send_failed` | ERROR | `err` | HTTP outbound falhou. |

### Email + SMS (`internal/transport/email/`, `internal/transport/sms/`)

Seguem o mesmo formato `<transport>.starting / .started / .poll_failed / .incoming / .handler_failed / .send_failed` dos transportes de polling acima.

## Receitas

### Mostrar cada tool call falhada hoje

```sh
journalctl --user -u rousseau-agent --since today -o json \
  | jq -c 'select(.MESSAGE | fromjson? | .msg == "tool.denied")'
```

### Seguir ao vivo uma única sessão de transporte

```sh
journalctl --user -u rousseau-agent -f -o cat \
  | grep -E 'whatsapp\.|tool\.|cron\.'
```

### Alertar sobre falhas de cron

Rascunho de regra Prometheus/alertmanager (via o pipeline `promtail` → Loki → alerta em [Guias: Observabilidade](/pt-BR/guides/observability/)):

```yaml
- alert: RousseauCronFailure
  expr: |
    sum by (job) (
      count_over_time({app="rousseau-agent"} |= "cron.run_failed" [5m])
    ) > 0
```

### Redação

O `slog` não redige por padrão. Configure um processador downstream para redigir os campos `err` em `whatsapp.send_failed`, `tool.error`, etc. — erros de provider ocasionalmente incluem fragmentos de prompt. Veja [Guias: Observabilidade](/pt-BR/guides/observability/) para o pipeline.

## Relacionados

- [Guia do usuário: Políticas de aprovação](/pt-BR/user-guide/approval-policies/) — a origem de `tool.denied`.
- [Guias: Observabilidade](/pt-BR/guides/observability/) — receita completa de pipeline.
- [Guias: Auditoria + políticas de aprovação](/pt-BR/guides/audit-approval-policies/) — trate esses logs como uma trilha de auditoria.
