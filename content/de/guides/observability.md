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
hreflang: "de"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "de"
locale: "de_DE"
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
permalink: "https://docs.rousseau-agent.dev/de/guides/observability/"
subtitle: "Slog JSON into your log pipeline. OTel on the roadmap."
tags: "guides, observability, slog, loki, grafana, datadog"
title: "Leitfaden: Observability"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "observability, slog, json logging, loki, grafana, datadog, opentelemetry"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Leitfaden: Observability"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 35
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/observability/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/observability/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Leitfaden: Observability"
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
twitter_title: "Leitfaden: Observability"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Danke an jeden Operator, der seinen eigenen Coding-Agenten betreibt."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">Was Sie lernen</span><p>Welche slog-Attribut-Keys rousseau emittiert, welche Log-Pipelines gut mit strukturiertem JSON zusammenarbeiten (Loki + Grafana, Datadog, Vector, OTel Collector), sowie eine Skizze für aufruferseitiges Tracing, sobald die OTel-Roadmap greift.</p></aside>

## Was rousseau emittiert

Jeder Daemon nutzt das Standardbibliothekspaket `log/slog` von Go. Wahl zwischen zwei Handlern über `log.format`:

| Wert | Handler | Anwendungsfall |
|---|---|---|
| `text` (Default) | `slog.NewTextHandler` | Interaktives `rousseau chat`. Ohne Farben; grep-freundlich. |
| `json` | `slog.NewJSONHandler` | Jeder Daemon in Produktion. Jedes Feld ist ein JSON-Schlüssel. |

Level: `debug`, `info`, `warn`, `error`.

Produktionskonfiguration:

```yaml
log:
  level: info
  format: json
```

## Strukturierte Keys, auf die Sie sich verlassen können

Die folgenden Keys sind tragend — sie parsen, nicht umbenennen. Sie erscheinen in `internal/cli/` und `internal/agent/`:

| Key | Emittiert von | Felder | Bedeutung |
|---|---|---|---|
| `tool.execute` | `agent.runTools` | `name`, `id` | Ein Tool-Aufruf lief. |
| `tool.denied` | `agent.runTools` | `name`, `reason` | Der Approver blockierte den Aufruf. |
| `tool.error` | `agent.runTools` | `name`, `err` | Tool lief, lieferte aber einen Fehler. |
| `agent.compressed` | `agent.Turn` | `messages` | Session-Kompression wurde ausgeführt. |
| `agent.compress_failed` | `agent.Turn` | `err` | Kompressions-Provider warf einen Fehler; Schleife fuhr fort. |
| `whatsapp.starting` | `cli/whatsapp.go` | `store`, `allowlist` | WhatsApp-Bridge gebootet. |
| `whatsapp.voice_enabled` | `cli/whatsapp.go` | `binary`, `model` | Sprachtranskription aktiv. |
| `cron.fire` | `internal/cron/scheduler.go` | `name`, `job` | Cron-Job feuerte. |
| `cron.deliver` | `internal/cron/scheduler.go` | `name`, `target`, `bytes` | Cron-Antwort zugestellt. |

Jede Log-Zeile trägt die Standard-slog-Felder `time`, `level`, `msg` sowie die oben genannten Attribute.

## Log-Pipelines — Stack auswählen

<div class="tabs" data-tabs="observability-stack">
  <div class="tab-list" role="tablist" aria-label="Observability stack">
    <button role="tab" aria-selected="true">Loki + Grafana</button>
    <button role="tab" aria-selected="false">Datadog</button>
    <button role="tab" aria-selected="false">Vector</button>
    <button role="tab" aria-selected="false">OTel Collector</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Loki + Promtail + Grafana. Die systemd- + Promtail-Konfiguration steht unterhalb der Tabs. Abfrage mit LogQL:

```
sum by (level) (rate({job="rousseau-agent"} [5m]))
```

Alerts auf Genehmigungsverweigerungen:

```
count_over_time({job="rousseau-agent"} |= "tool.denied" [15m]) > 5
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Datadog Agent mit der journald-Quelle; der eingebaute JSON-Parser hebt jedes slog-Attribut in eine Facette. Die Konfiguration steht unterhalb der Tabs.

Monitore:

- `msg:tool.denied` — jeder blockierte Tool-Aufruf.
- `msg:whatsapp.logged_out` — WhatsApp hat sein Pairing verloren.
- `msg:cron.delivery_failed` — Cron-Job scheiterte bei der Zustellung.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Vector als Aggregator mit beliebigem Downstream-Sink (S3, Kafka, Elasticsearch usw.). Die Konfiguration steht unterhalb der Tabs. Die `remap`-Sprache von Vector erlaubt es, laute Events zu verwerfen oder abgeleitete Attribute hinzuzufügen, ohne rousseau anzufassen.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Der OpenTelemetry Collector nimmt Logs über journald entgegen und leitet sie an ein beliebiges OTLP-Backend weiter:

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

Sobald das OTel-Exporter-Roadmap-Item in rousseau selbst landet, wird daraus End-to-End-OTel ohne journald-Zwischenstation.

  </div>
</div>

## Log-Pipeline: Loki + Grafana

### Systemd + Promtail

Promtail auf das Journal des rousseau-Dienstes ausrichten:

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

Grafana-Dashboards können anschließend auf `level=WARN` und `msg="tool.denied"` filtern, um das Panel "blockierte Tool-Aufrufe" zu bauen.

### Kubernetes

Grafana Agent (oder Loki + Alloy) als DaemonSet ausrollen. Da rousseau im Container auf stdout schreibt, ist kein Datei-Scraping erforderlich.

## Log-Pipeline: Datadog

```
# /etc/datadog-agent/conf.d/rousseau.d/conf.yaml
logs:
  - type: journald
    include_units:
      - rousseau-agent.service
    service: rousseau-agent
    source: rousseau-agent
```

Da rousseau JSON emittiert, hebt der eingebaute JSON-Parser von Datadog `level`, `msg` und jedes Attribut in First-Class-Facetten. Einen Monitor auf `msg:tool.denied` einrichten, um Alerts zu Genehmigungsrichtlinien zu erhalten.

## Log-Pipeline: Vector

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

## Wichtige Kennzahlen zum Visualisieren

Es gibt heute keinen Prometheus-Endpunkt. Die gewünschten Metriken reisen über den Log-Stream:

| Metrik | Ableitung |
|---|---|
| Tool-Aufrufrate | zählen `msg:tool.execute` |
| Ablehnungsrate | zählen `msg:tool.denied` |
| Fehlerrate | zählen `msg:tool.error` |
| Kompressions-Ereignisse | zählen `msg:agent.compressed` |
| Cron-Feuerungen | zählen `msg:cron.fire` |
| Cron-Zustell-Bytes | summieren `bytes`, wobei `msg:cron.deliver` |

Loki + LogQL: `sum by (name) (count_over_time({job="rousseau-agent"} |= "tool.denied" [1h]))`.

## OpenTelemetry-Roadmap

Eine OpenTelemetry-Integration steht auf der Roadmap. Zu erwarten, sobald sie ausgeliefert ist:

- `otel.trace`-Kontextpropagierung durch den Agent-Loop (ein Span pro `Turn`, Child-Spans pro Tool-Aufruf).
- Metrik-Exporter für dieselben Zähler, die heute per Log transportiert werden.
- Konfigurierbarer OTLP-Endpunkt über Umgebungsvariablen.

Bis dahin die strukturierte slog-Ausgabe als Observability-Substrat behandeln. Jedes Ereignis, für das Sie eine Metrik oder einen Trace wünschen, ist bereits vorhanden — die Metadaten sind vollständig, lediglich das Wire-Format unterscheidet sich.

## Debugging ohne Log-Pipeline

Interaktiv:

```sh
rousseau --config /etc/rousseau/config.yaml whatsapp \
  --allow 447900123456@s.whatsapp.net 2>&1 | jq
```

Der Daemon schreibt slog auf stderr; Piping durch `jq` liefert einen interaktiven Filter. `jq 'select(.msg == "tool.denied")'` zeigt jeden blockierten Aufruf.

`rousseau doctor` ist der weitere Observability-Hebel — ein Snapshot jeder Abhängigkeit und jeder Konfigurationsentscheidung zu einem bestimmten Zeitpunkt.

## Troubleshooting

### `journal has no entries`

Der Daemon hat noch nichts geschrieben, oder der journald-Matcher ist falsch. Mit `journalctl --user -u rousseau-agent.service --no-pager` bestätigen.

### JSON-Parsing-Fehler in der Pipeline

Rousseau loggt eine Zeile pro Event. Enthält das `msg` eines Log-Events einen Zeilenumbruch (selten — manche Transports enthalten mehrzeilige Fehlerstrings), kann die Pipeline es in zwei Events aufteilen. Mit einem Regex filtern oder strukturiertes Parsing verwenden, das eingebettete Zeilenumbrüche respektiert.

### Fehlende Attribute downstream

Loki verwirft Attribute, die es nicht auf Labels mappen kann. In LogQL `line_format` verwenden, um Attribute in die gerenderte Ausgabe zu projizieren, oder sie als Labels über `pipeline_stages.labels` indizieren.

### Datadog-`service`-Tag fehlt

Datadog nutzt das `service`-Feld zum Filtern. Die journald-Quelle setzt es aus der Konfiguration; sicherstellen, dass `service: rousseau-agent` vorhanden ist.

### Grafana-Dashboards zeigen keine Daten

Prüfen, dass die LogQL-Query zu Ihren Labels passt. Promtails Default-Label `job` wird von der Scrape-Konfiguration gesetzt — bei Änderungen jede Dashboard-Query aktualisieren.

## Verwandte Seiten

- [Konfiguration](/de/configuration/) — `log.level` und `log.format`.
- [Leitfäden: Audit- &amp; Genehmigungsrichtlinien](/de/guides/audit-approval-policies/) — die wichtigsten Alert-Signale.
- [Referenz: Exit-Codes](/de/reference/exit-codes/) — wie der Daemon Init-Systemen einen Fehler signalisiert.
- [Sicherheit](/de/security/) — Audit-Trail über slog.
- [Referenz: Logs](/de/reference/logs/) — jeder slog-Key, den rousseau emittiert.

## Weiterführende Literatur

- `internal/cli/root.go` — `newLogger` setzt den slog-Handler.
- `internal/agent/agent.go` — `tool.execute`-, `tool.denied`-, `agent.compressed`-Events.
- `internal/transport/whatsapp/dispatch.go` — Event-Emission auf Transportseite.
- Grafana-LogQL-Docs und Datadog-Log-Processing-Docs (extern).
