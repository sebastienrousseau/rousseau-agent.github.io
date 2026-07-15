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
hreflang: "en"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "en-GB"
locale: "en_GB"
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
permalink: "https://docs.rousseau-agent.dev/guides/observability/"
subtitle: "Slog JSON into your log pipeline. OTel on the roadmap."
tags: "guides, observability, slog, loki, grafana, datadog"
title: "Guide: Observability"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "observability, slog, json logging, loki, grafana, datadog, opentelemetry"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide: Observability"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 35
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/observability/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/observability/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guide: Observability"
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
twitter_title: "Guide: Observability"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">What you'll learn</span><p>The slog attribute keys rousseau emits, the log pipelines that work well with structured JSON (Loki + Grafana, Datadog, Vector, OTel Collector), and a caller-side sketch for tracing when the OTel roadmap lands.</p></aside>

## What rousseau emits

Every daemon uses the Go standard library `log/slog` package. Choose between two handlers via `log.format`:

| Value | Handler | Use case |
|---|---|---|
| `text` (default) | `slog.NewTextHandler` | Interactive `rousseau chat`. Colours off; grep-friendly. |
| `json` | `slog.NewJSONHandler` | Any daemon in production. Every field is a JSON key. |

Levels: `debug`, `info`, `warn`, `error`.

Production config:

```yaml
log:
  level: info
  format: json
```

## Structured keys you can rely on

The following keys are load-bearing — parse them, don't rewrite them. They appear across `internal/cli/` and `internal/agent/`:

| Key | Emitted from | Fields | Meaning |
|---|---|---|---|
| `tool.execute` | `agent.runTools` | `name`, `id` | A tool call ran. |
| `tool.denied` | `agent.runTools` | `name`, `reason` | Approver blocked the call. |
| `tool.error` | `agent.runTools` | `name`, `err` | Tool ran but returned an error. |
| `agent.compressed` | `agent.Turn` | `messages` | Session compression fired. |
| `agent.compress_failed` | `agent.Turn` | `err` | Compression provider errored; loop continued. |
| `whatsapp.starting` | `cli/whatsapp.go` | `store`, `allowlist` | WhatsApp bridge booted. |
| `whatsapp.voice_enabled` | `cli/whatsapp.go` | `binary`, `model` | Voice transcription active. |
| `cron.fire` | `internal/cron/scheduler.go` | `name`, `job` | Cron job fired. |
| `cron.deliver` | `internal/cron/scheduler.go` | `name`, `target`, `bytes` | Cron reply delivered. |

Every log line carries the standard `time`, `level`, `msg` slog fields plus any attributes above.

## Log pipelines — pick your stack

<div class="tabs" data-tabs="observability-stack">
  <div class="tab-list" role="tablist" aria-label="Observability stack">
    <button role="tab" aria-selected="true">Loki + Grafana</button>
    <button role="tab" aria-selected="false">Datadog</button>
    <button role="tab" aria-selected="false">Vector</button>
    <button role="tab" aria-selected="false">OTel Collector</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Loki + Promtail + Grafana. See the systemd + Promtail config below the tabs. Query with LogQL:

```
sum by (level) (rate({job="rousseau-agent"} [5m]))
```

Alerts on approval denials:

```
count_over_time({job="rousseau-agent"} |= "tool.denied" [15m]) > 5
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Datadog Agent with the journald source; the built-in JSON parser lifts every slog attribute into a facet. See the config below the tabs.

Monitors:

- `msg:tool.denied` — every blocked tool call.
- `msg:whatsapp.logged_out` — WhatsApp lost its pairing.
- `msg:cron.delivery_failed` — cron job failed to deliver.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Vector as an aggregator with any downstream sink (S3, Kafka, Elasticsearch, etc.). See the config below the tabs. Vector's `remap` language lets you drop noisy events or add derived attributes without touching rousseau.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

The OpenTelemetry Collector accepts logs via journald and forwards to any OTLP backend:

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

Once the OTel exporter roadmap item lands in rousseau itself, this becomes end-to-end OTel with no journald hop.

  </div>
</div>

## Log pipeline: Loki + Grafana

### Systemd + Promtail

Point Promtail at the rousseau service's journal:

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

Grafana dashboards can then filter on `level=WARN` and `msg="tool.denied"` to build the "blocked tool calls" panel.

### Kubernetes

Deploy the Grafana Agent (or Loki + Alloy) as a DaemonSet. Because rousseau writes to stdout in the container, no file scraping is required.

## Log pipeline: Datadog

```
# /etc/datadog-agent/conf.d/rousseau.d/conf.yaml
logs:
  - type: journald
    include_units:
      - rousseau-agent.service
    service: rousseau-agent
    source: rousseau-agent
```

Because rousseau emits JSON, Datadog's built-in JSON parser lifts `level`, `msg`, and every attribute into first-class facets. Configure a monitor on `msg:tool.denied` for approval-policy alerts.

## Log pipeline: Vector

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

## Key metrics to graph

There is no Prometheus endpoint today. The metrics you want ride on the log stream:

| Metric | How to derive |
|---|---|
| Tool-call rate | count `msg:tool.execute` |
| Denial rate | count `msg:tool.denied` |
| Error rate | count `msg:tool.error` |
| Compression events | count `msg:agent.compressed` |
| Cron fires | count `msg:cron.fire` |
| Cron delivery bytes | sum `bytes` where `msg:cron.deliver` |

Loki + LogQL: `sum by (name) (count_over_time({job="rousseau-agent"} |= "tool.denied" [1h]))`.

## OpenTelemetry roadmap

An OpenTelemetry integration is on the roadmap. When it ships, expect:

- `otel.trace` context propagation through the agent loop (one span per `Turn`, child spans per tool call).
- Metric exporter for the same counters that today ride on logs.
- Configurable OTLP endpoint via env vars.

Until then, treat the structured slog output as the observability substrate. Every event you would want a metric or a trace for is already there — the metadata is complete, only the wire format is different.

## Debugging without a log pipeline

Interactive:

```sh
rousseau --config /etc/rousseau/config.yaml whatsapp \
  --allow 447900123456@s.whatsapp.net 2>&1 | jq
```

The daemon writes slog to stderr; piping through `jq` gives an interactive filter. `jq 'select(.msg == "tool.denied")'` shows every blocked call.

`rousseau doctor` is the other observability lever — a snapshot of every dependency and every config choice at a moment in time.

## Troubleshooting

### `journal has no entries`

The daemon wrote nothing yet, or the journald matcher is wrong. Confirm with `journalctl --user -u rousseau-agent.service --no-pager`.

### JSON parsing errors in the pipeline

Rousseau logs one line per event. If a log event's `msg` contains a newline (rare — some transports include multi-line error strings), the pipeline may split it into two events. Filter with a regex or use structured parsing that respects embedded newlines.

### Missing attributes downstream

Loki drops attributes it cannot map to labels. Use `line_format` in LogQL to project attributes into the rendered output, or index them as labels with `pipeline_stages.labels`.

### Datadog service tag is missing

Datadog uses the `service` field for filtering. The journald source sets it from the config; ensure `service: rousseau-agent` is present.

### Grafana dashboards show no data

Verify the LogQL query matches your labels. Promtail's default `job` label is set by the scrape config — if you changed it, update every dashboard query.

## Related pages

- [Configuration](/configuration/) — `log.level` and `log.format`.
- [Guides: Audit &amp; Approval Policies](/guides/audit-approval-policies/) — the alert signals you most want.
- [Reference: Exit codes](/reference/exit-codes/) — how the daemon signals failure to init systems.
- [Security](/security/) — audit trail via slog.
- [Reference: Logs](/reference/logs/) — every slog key rousseau emits.

## Further reading

- `internal/cli/root.go` — `newLogger` sets the slog handler.
- `internal/agent/agent.go` — `tool.execute`, `tool.denied`, `agent.compressed` events.
- `internal/transport/whatsapp/dispatch.go` — transport-side event emission.
- Grafana LogQL docs and Datadog log processing docs (external).
