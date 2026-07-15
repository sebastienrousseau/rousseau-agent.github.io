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
description: "Wire rousseau-agent's slog JSON output to Loki, Grafana, Datadog, or any log pipeline. OpenTelemetry roadmap notes."
keywords: "observability, slog, json logging, loki, grafana, datadog, opentelemetry"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/guides/observability/"
subtitle: "Slog JSON into your log pipeline. OTel on the roadmap."
tags: "guides, observability, slog, loki, grafana, datadog"
title: "Guia: observabilidade"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "observability, slog, json logging, loki, grafana, datadog, opentelemetry"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guia: observabilidade"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 35
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/observability/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/observability/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guia: observabilidade"
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
twitter_description: "Wire rousseau-agent's slog JSON output to Loki, Grafana, Datadog, or any log pipeline. OpenTelemetry roadmap notes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guia: observabilidade"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">O que você vai aprender</span><p>As chaves de atributo slog que o rousseau emite, os pipelines de log que funcionam bem com JSON estruturado (Loki + Grafana, Datadog, Vector, OTel Collector) e um esboço do lado do chamador para tracing quando o item OTel do roadmap for concluído.</p></aside>

## O que o rousseau emite

Todo daemon usa o pacote `log/slog` da biblioteca padrão Go. Escolha entre dois handlers via `log.format`:

| Valor | Handler | Caso de uso |
|---|---|---|
| `text` (padrão) | `slog.NewTextHandler` | `rousseau chat` interativo. Sem cores; amigável a grep. |
| `json` | `slog.NewJSONHandler` | Qualquer daemon em produção. Cada campo é uma chave JSON. |

Níveis: `debug`, `info`, `warn`, `error`.

Configuração de produção:

```yaml
log:
  level: info
  format: json
```

## Chaves estruturadas com as quais você pode contar

As chaves a seguir são carga útil — dê parse nelas, não as reescreva. Elas aparecem em `internal/cli/` e `internal/agent/`:

| Chave | Emitida em | Campos | Significado |
|---|---|---|---|
| `tool.execute` | `agent.runTools` | `name`, `id` | Uma chamada de ferramenta foi executada. |
| `tool.denied` | `agent.runTools` | `name`, `reason` | Approver bloqueou a chamada. |
| `tool.error` | `agent.runTools` | `name`, `err` | A ferramenta rodou mas retornou erro. |
| `agent.compressed` | `agent.Turn` | `messages` | Compressão de sessão disparou. |
| `agent.compress_failed` | `agent.Turn` | `err` | Provider de compressão falhou; o loop continuou. |
| `whatsapp.starting` | `cli/whatsapp.go` | `store`, `allowlist` | Bridge do WhatsApp iniciou. |
| `whatsapp.voice_enabled` | `cli/whatsapp.go` | `binary`, `model` | Transcrição de voz ativa. |
| `cron.fire` | `internal/cron/scheduler.go` | `name`, `job` | Job cron disparou. |
| `cron.deliver` | `internal/cron/scheduler.go` | `name`, `target`, `bytes` | Resposta cron entregue. |

Toda linha de log carrega os campos slog padrão `time`, `level`, `msg` mais qualquer atributo acima.

## Pipelines de log — escolha sua stack

<div class="tabs" data-tabs="observability-stack">
  <div class="tab-list" role="tablist" aria-label="Observability stack">
    <button role="tab" aria-selected="true">Loki + Grafana</button>
    <button role="tab" aria-selected="false">Datadog</button>
    <button role="tab" aria-selected="false">Vector</button>
    <button role="tab" aria-selected="false">OTel Collector</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Loki + Promtail + Grafana. Veja a configuração systemd + Promtail abaixo das abas. Consulte com LogQL:

```
sum by (level) (rate({job="rousseau-agent"} [5m]))
```

Alertas em negações de aprovação:

```
count_over_time({job="rousseau-agent"} |= "tool.denied" [15m]) > 5
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Datadog Agent com a fonte journald; o parser JSON nativo eleva cada atributo slog a uma faceta. Veja a config abaixo das abas.

Monitores:

- `msg:tool.denied` — toda chamada de ferramenta bloqueada.
- `msg:whatsapp.logged_out` — WhatsApp perdeu o pareamento.
- `msg:cron.delivery_failed` — job cron falhou ao entregar.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Vector como agregador com qualquer sink downstream (S3, Kafka, Elasticsearch, etc.). Veja a config abaixo das abas. A linguagem `remap` do Vector permite descartar eventos ruidosos ou adicionar atributos derivados sem tocar no rousseau.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

O OpenTelemetry Collector aceita logs via journald e encaminha para qualquer backend OTLP:

```yaml
# otel-collector-config.yaml
receivers:
  journald:
    units: [rousseau-agent.service]

processors:
  transform:
    log_statements:
      - context: log
        statements:
          - merge_maps(cache, ParseJSON(body), "insert")

exporters:
  otlphttp:
    endpoint: https://otel-backend.internal:4318

service:
  pipelines:
    logs:
      receivers: [journald]
      processors: [transform]
      exporters: [otlphttp]
```

Assim que o item do exportador OTel do roadmap chegar no próprio rousseau, isso se torna OTel de ponta a ponta sem o hop no journald.

  </div>
</div>

## Pipeline de log: Loki + Grafana

### Systemd + Promtail

Aponte o Promtail para o journal do serviço rousseau:

```yaml
# /etc/promtail/promtail.yaml
scrape_configs:
  - job_name: rousseau-agent
    journal:
      matches: _SYSTEMD_USER_UNIT=rousseau-agent.service
      labels: { job: rousseau-agent }
    relabel_configs:
      - source_labels: [__journal__systemd_user_unit]
        target_label: unit
    pipeline_stages:
      - json:
          expressions: { level: level, msg: msg }
      - labels: { level: "" }
```

Os dashboards do Grafana podem então filtrar por `level=WARN` e `msg="tool.denied"` para montar o painel "chamadas de ferramenta bloqueadas".

### Kubernetes

Faça deploy do Grafana Agent (ou Loki + Alloy) como um DaemonSet. Como o rousseau escreve na stdout no contêiner, não é necessário coletar arquivos.

## Pipeline de log: Datadog

```
# /etc/datadog-agent/conf.d/rousseau.d/conf.yaml
logs:
  - type: journald
    include_units:
      - rousseau-agent.service
    service: rousseau-agent
    source: rousseau-agent
```

Como o rousseau emite JSON, o parser JSON nativo do Datadog eleva `level`, `msg` e cada atributo a facetas de primeira classe. Configure um monitor em `msg:tool.denied` para alertas de política de aprovação.

## Pipeline de log: Vector

```toml
# /etc/vector/vector.toml
[sources.rousseau_journal]
type = "journald"
include_units = ["rousseau-agent.service"]

[transforms.rousseau_parse]
type = "remap"
inputs = ["rousseau_journal"]
source = '''
. = merge(., parse_json(.message) ?? {})
'''

[sinks.loki]
type = "loki"
inputs = ["rousseau_parse"]
endpoint = "https://loki.internal:3100"
labels = { job = "rousseau-agent", level = "{{ level }}" }
```

## Métricas-chave para plotar

Hoje não há endpoint Prometheus. As métricas que você quer viajam no stream de log:

| Métrica | Como derivar |
|---|---|
| Taxa de chamadas de ferramenta | contar `msg:tool.execute` |
| Taxa de negação | contar `msg:tool.denied` |
| Taxa de erro | contar `msg:tool.error` |
| Eventos de compressão | contar `msg:agent.compressed` |
| Disparos de cron | contar `msg:cron.fire` |
| Bytes de entrega cron | somar `bytes` onde `msg:cron.deliver` |

Loki + LogQL: `sum by (name) (count_over_time({job="rousseau-agent"} |= "tool.denied" [1h]))`.

## Roadmap OpenTelemetry

Uma integração OpenTelemetry está no roadmap. Quando for lançada, espere:

- Propagação de contexto `otel.trace` através do agent loop (um span por `Turn`, spans filhos por chamada de ferramenta).
- Exportador de métricas para os mesmos contadores que hoje viajam nos logs.
- Endpoint OTLP configurável via variáveis de ambiente.

Até lá, trate a saída slog estruturada como o substrato de observabilidade. Todo evento para o qual você gostaria de uma métrica ou um trace já está lá — os metadados estão completos, só o formato de wire é diferente.

## Depurando sem um pipeline de log

Interativo:

```sh
rousseau --config /etc/rousseau/config.yaml whatsapp \
  --allow 447900123456@s.whatsapp.net 2>&1 | jq
```

O daemon escreve slog na stderr; passar por `jq` dá um filtro interativo. `jq 'select(.msg == "tool.denied")'` mostra toda chamada bloqueada.

`rousseau doctor` é a outra alavanca de observabilidade — um snapshot de cada dependência e cada escolha de configuração em um momento no tempo.

## Solução de problemas

### `journal has no entries`

O daemon ainda não escreveu nada, ou o matcher do journald está errado. Confirme com `journalctl --user -u rousseau-agent.service --no-pager`.

### Erros de parsing JSON no pipeline

O Rousseau registra uma linha por evento. Se o `msg` de um evento de log contiver uma newline (raro — alguns transportes incluem strings de erro em múltiplas linhas), o pipeline pode dividi-lo em dois eventos. Filtre com regex ou use parsing estruturado que respeite newlines embutidas.

### Atributos ausentes no destino

O Loki descarta atributos que não consegue mapear a labels. Use `line_format` no LogQL para projetar atributos na saída renderizada, ou indexe-os como labels com `pipeline_stages.labels`.

### Tag de service faltando no Datadog

O Datadog usa o campo `service` para filtragem. A fonte journald a define a partir da config; garanta que `service: rousseau-agent` esteja presente.

### Dashboards do Grafana não mostram dados

Verifique se a consulta LogQL corresponde às suas labels. A label `job` padrão do Promtail é definida pelo scrape config — se você a mudou, atualize toda consulta de dashboard.

## Páginas relacionadas

- [Configuração](/pt-BR/configuration/) — `log.level` e `log.format`.
- [Guias: Auditoria &amp; Políticas de aprovação](/pt-BR/guides/audit-approval-policies/) — os sinais de alerta que você mais quer.
- [Referência: Exit codes](/pt-BR/reference/exit-codes/) — como o daemon sinaliza falha aos sistemas de init.
- [Segurança](/pt-BR/security/) — trilha de auditoria via slog.
- [Referência: Logs](/pt-BR/reference/logs/) — cada chave slog que o rousseau emite.

## Leitura adicional

- `internal/cli/root.go` — `newLogger` define o handler slog.
- `internal/agent/agent.go` — eventos `tool.execute`, `tool.denied`, `agent.compressed`.
- `internal/transport/whatsapp/dispatch.go` — emissão de eventos do lado do transporte.
- Documentação do LogQL do Grafana e docs de processamento de logs do Datadog (externo).
