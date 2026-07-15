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
hreflang: "es"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "es"
locale: "es_ES"
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
permalink: "https://docs.rousseau-agent.dev/es/guides/observability/"
subtitle: "Slog JSON into your log pipeline. OTel on the roadmap."
tags: "guides, observability, slog, loki, grafana, datadog"
title: "Guía: observabilidad"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "observability, slog, json logging, loki, grafana, datadog, opentelemetry"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guía: observabilidad"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 35
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/observability/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/observability/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guía: observabilidad"
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
twitter_title: "Guía: observabilidad"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Gracias a cada operador que ejecuta su propio agente de codificación."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">Lo que aprenderás</span><p>Las claves de atributos de slog que emite rousseau, los pipelines de logs que funcionan bien con JSON estructurado (Loki + Grafana, Datadog, Vector, OTel Collector), y un boceto del lado del cliente para el tracing cuando se implemente el roadmap de OTel.</p></aside>

## Qué emite rousseau

Cada servicio usa el paquete `log/slog` de la biblioteca estándar de Go. Elige entre dos handlers vía `log.format`:

| Valor | Handler | Caso de uso |
|---|---|---|
| `text` (predeterminado) | `slog.NewTextHandler` | `rousseau chat` interactivo. Sin colores; compatible con grep. |
| `json` | `slog.NewJSONHandler` | Cualquier servicio en producción. Cada campo es una clave JSON. |

Niveles: `debug`, `info`, `warn`, `error`.

Configuración de producción:

```yaml
log:
  level: info
  format: json
```

## Claves estructuradas confiables

Las siguientes claves son fundamentales: parséalas, no las reescribas. Aparecen a lo largo de `internal/cli/` e `internal/agent/`:

| Clave | Emitida desde | Campos | Significado |
|---|---|---|---|
| `tool.execute` | `agent.runTools` | `name`, `id` | Se ejecutó una llamada a herramienta. |
| `tool.denied` | `agent.runTools` | `name`, `reason` | El approver bloqueó la llamada. |
| `tool.error` | `agent.runTools` | `name`, `err` | La herramienta se ejecutó pero devolvió error. |
| `agent.compressed` | `agent.Turn` | `messages` | Se disparó la compresión de sesión. |
| `agent.compress_failed` | `agent.Turn` | `err` | El proveedor de compresión falló; el bucle continuó. |
| `whatsapp.starting` | `cli/whatsapp.go` | `store`, `allowlist` | El puente WhatsApp arrancó. |
| `whatsapp.voice_enabled` | `cli/whatsapp.go` | `binary`, `model` | Transcripción de voz activa. |
| `cron.fire` | `internal/cron/scheduler.go` | `name`, `job` | Job cron disparado. |
| `cron.deliver` | `internal/cron/scheduler.go` | `name`, `target`, `bytes` | Respuesta de cron entregada. |

Cada línea de log lleva los campos estándar de slog `time`, `level`, `msg` más cualquier atributo anterior.

## Pipelines de logs — elige tu stack

<div class="tabs" data-tabs="observability-stack">
  <div class="tab-list" role="tablist" aria-label="Observability stack">
    <button role="tab" aria-selected="true">Loki + Grafana</button>
    <button role="tab" aria-selected="false">Datadog</button>
    <button role="tab" aria-selected="false">Vector</button>
    <button role="tab" aria-selected="false">OTel Collector</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Loki + Promtail + Grafana. Consulta la configuración de systemd + Promtail debajo de las pestañas. Consulta con LogQL:

```
sum by (level) (rate({job="rousseau-agent"} [5m]))
```

Alertas sobre denegaciones de aprobación:

```
count_over_time({job="rousseau-agent"} |= "tool.denied" [15m]) > 5
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Datadog Agent con la fuente journald; el parser JSON integrado eleva cada atributo slog a una facet. Consulta la configuración debajo de las pestañas.

Monitores:

- `msg:tool.denied` — cada llamada a herramienta bloqueada.
- `msg:whatsapp.logged_out` — WhatsApp perdió su emparejamiento.
- `msg:cron.delivery_failed` — un cron job no pudo entregar.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Vector como agregador con cualquier sink posterior (S3, Kafka, Elasticsearch, etc.). Consulta la configuración debajo de las pestañas. El lenguaje `remap` de Vector permite descartar eventos ruidosos o añadir atributos derivados sin tocar rousseau.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

El OpenTelemetry Collector acepta logs vía journald y los reenvía a cualquier backend OTLP:

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

Cuando el ítem del roadmap del exportador OTel se implemente en rousseau, esto se convierte en OTel de extremo a extremo sin salto por journald.

  </div>
</div>

## Pipeline de logs: Loki + Grafana

### Systemd + Promtail

Apunta Promtail al journal del servicio rousseau:

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

Los dashboards de Grafana pueden entonces filtrar por `level=WARN` y `msg="tool.denied"` para construir el panel de "llamadas a herramientas bloqueadas".

### Kubernetes

Despliega el Grafana Agent (o Loki + Alloy) como un DaemonSet. Como rousseau escribe a stdout en el contenedor, no se requiere scraping de archivos.

## Pipeline de logs: Datadog

```
# /etc/datadog-agent/conf.d/rousseau.d/conf.yaml
logs:
  - type: journald
    include_units:
      - rousseau-agent.service
    service: rousseau-agent
    source: rousseau-agent
```

Como rousseau emite JSON, el parser JSON integrado de Datadog eleva `level`, `msg` y cada atributo a facets de primer nivel. Configura un monitor sobre `msg:tool.denied` para alertas de política de aprobación.

## Pipeline de logs: Vector

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

## Métricas clave a graficar

Hoy no hay endpoint de Prometheus. Las métricas que buscas viajan sobre el flujo de logs:

| Métrica | Cómo derivarla |
|---|---|
| Tasa de llamadas a herramientas | contar `msg:tool.execute` |
| Tasa de denegación | contar `msg:tool.denied` |
| Tasa de errores | contar `msg:tool.error` |
| Eventos de compresión | contar `msg:agent.compressed` |
| Disparos de cron | contar `msg:cron.fire` |
| Bytes de entrega de cron | sumar `bytes` donde `msg:cron.deliver` |

Loki + LogQL: `sum by (name) (count_over_time({job="rousseau-agent"} |= "tool.denied" [1h]))`.

## Roadmap de OpenTelemetry

Una integración con OpenTelemetry está en el roadmap. Cuando se publique, espera:

- Propagación del contexto `otel.trace` a través del bucle del agente (un span por `Turn`, spans hijos por cada llamada a herramienta).
- Exportador de métricas para los mismos contadores que hoy viajan en logs.
- Endpoint OTLP configurable mediante variables de entorno.

Hasta entonces, trata la salida estructurada de slog como el sustrato de observabilidad. Cada evento del que quisieras una métrica o un trace ya está ahí; los metadatos están completos, solo cambia el formato de cable.

## Depuración sin un pipeline de logs

Interactiva:

```sh
rousseau --config /etc/rousseau/config.yaml whatsapp \
  --allow 447900123456@s.whatsapp.net 2>&1 | jq
```

El servicio escribe slog a stderr; canalizar por `jq` proporciona un filtro interactivo. `jq 'select(.msg == "tool.denied")'` muestra cada llamada bloqueada.

`rousseau doctor` es la otra palanca de observabilidad: una instantánea de cada dependencia y cada elección de configuración en un momento dado.

## Solución de problemas

### `journal has no entries`

El servicio aún no escribió nada, o el matcher de journald es incorrecto. Confirma con `journalctl --user -u rousseau-agent.service --no-pager`.

### Errores de análisis JSON en el pipeline

Rousseau registra una línea por evento. Si el `msg` de un evento de log contiene un salto de línea (raro; algunos transportes incluyen cadenas de error multilínea), el pipeline puede dividirlo en dos eventos. Filtra con una regex o usa parseo estructurado que respete saltos de línea embebidos.

### Faltan atributos aguas abajo

Loki descarta atributos que no puede mapear a labels. Usa `line_format` en LogQL para proyectar atributos en la salida renderizada, o indexálos como labels con `pipeline_stages.labels`.

### Falta el tag de servicio en Datadog

Datadog usa el campo `service` para filtrar. La fuente journald lo fija desde la configuración; asegúrate de que `service: rousseau-agent` esté presente.

### Los dashboards de Grafana no muestran datos

Verifica que la consulta LogQL coincida con tus labels. La label `job` por defecto de Promtail se fija en la configuración de scrape; si la cambiaste, actualiza cada consulta del dashboard.

## Páginas relacionadas

- [Configuración](/es/configuration/) — `log.level` y `log.format`.
- [Guías: Auditoría y políticas de aprobación](/es/guides/audit-approval-policies/) — las señales de alerta más útiles.
- [Referencia: Códigos de salida](/es/reference/exit-codes/) — cómo el servicio señala fallos a los sistemas de init.
- [Seguridad](/es/security/) — traza de auditoría vía slog.
- [Referencia: Logs](/es/reference/logs/) — cada clave slog que emite rousseau.

## Lecturas adicionales

- `internal/cli/root.go` — `newLogger` configura el handler de slog.
- `internal/agent/agent.go` — eventos `tool.execute`, `tool.denied`, `agent.compressed`.
- `internal/transport/whatsapp/dispatch.go` — emisión de eventos del lado del transporte.
- Documentación de Grafana LogQL y de procesamiento de logs de Datadog (externas).
