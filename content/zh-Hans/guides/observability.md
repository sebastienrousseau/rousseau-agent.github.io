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
hreflang: "zh-Hans"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "zh-Hans"
locale: "zh_CN"
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
permalink: "https://docs.rousseau-agent.dev/zh-Hans/guides/observability/"
subtitle: "Slog JSON into your log pipeline. OTel on the roadmap."
tags: "guides, observability, slog, loki, grafana, datadog"
title: "指南：可观测性"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "observability, slog, json logging, loki, grafana, datadog, opentelemetry"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "指南：可观测性"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 35
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/guides/observability/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/observability/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "指南：可观测性"
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
twitter_title: "指南：可观测性"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "感谢每一位运行自有编码代理的运维者。"
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">你将学到</span><p>rousseau 输出的 slog 属性键、与结构化 JSON 良好配合的日志管道（Loki + Grafana、Datadog、Vector、OTel Collector），以及在 OTel 路线图落地后调用方侧的 tracing 蓝图。</p></aside>

## rousseau 输出什么

每个守护进程都使用 Go 标准库的 `log/slog`。通过 `log.format` 在两种 handler 之间选择：

| 值 | Handler | 使用场景 |
|---|---|---|
| `text`（默认） | `slog.NewTextHandler` | 交互式 `rousseau chat`。关闭颜色；便于 grep。 |
| `json` | `slog.NewJSONHandler` | 任何生产环境中的守护进程。每个字段都是一个 JSON key。 |

级别：`debug`、`info`、`warn`、`error`。

生产配置：

```yaml
log:
  level: info
  format: json
```

## 可依赖的结构化键

以下键是关键 —— 请解析它们，不要重写。它们出现在 `internal/cli/` 与 `internal/agent/` 中：

| 键 | 输出位置 | 字段 | 含义 |
|---|---|---|---|
| `tool.execute` | `agent.runTools` | `name`、`id` | 一次工具调用已运行。 |
| `tool.denied` | `agent.runTools` | `name`、`reason` | Approver 阻止了本次调用。 |
| `tool.error` | `agent.runTools` | `name`、`err` | 工具运行但返回了错误。 |
| `agent.compressed` | `agent.Turn` | `messages` | 会话压缩被触发。 |
| `agent.compress_failed` | `agent.Turn` | `err` | 压缩 provider 报错；循环继续。 |
| `whatsapp.starting` | `cli/whatsapp.go` | `store`、`allowlist` | WhatsApp 桥启动。 |
| `whatsapp.voice_enabled` | `cli/whatsapp.go` | `binary`、`model` | 语音转写已启用。 |
| `cron.fire` | `internal/cron/scheduler.go` | `name`、`job` | Cron 作业已触发。 |
| `cron.deliver` | `internal/cron/scheduler.go` | `name`、`target`、`bytes` | Cron 回复已投递。 |

每条日志行都带有标准的 `time`、`level`、`msg` slog 字段，外加以上任意属性。

## 日志管道 —— 选择你的技术栈

<div class="tabs" data-tabs="observability-stack">
  <div class="tab-list" role="tablist" aria-label="Observability stack">
    <button role="tab" aria-selected="true">Loki + Grafana</button>
    <button role="tab" aria-selected="false">Datadog</button>
    <button role="tab" aria-selected="false">Vector</button>
    <button role="tab" aria-selected="false">OTel Collector</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Loki + Promtail + Grafana。请参见下面标签下方的 systemd + Promtail 配置。使用 LogQL 查询：

```
sum by (level) (rate({job="rousseau-agent"} [5m]))
```

对审批拒绝的告警：

```
count_over_time({job="rousseau-agent"} |= "tool.denied" [15m]) > 5
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

使用 journald 源的 Datadog Agent；内置 JSON 解析器会把每个 slog 属性提升为一个 facet。请参见下面标签下方的配置。

监控项：

- `msg:tool.denied` —— 每次被阻止的工具调用。
- `msg:whatsapp.logged_out` —— WhatsApp 失去配对。
- `msg:cron.delivery_failed` —— cron 作业投递失败。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Vector 作为聚合器，可接任何下游 sink（S3、Kafka、Elasticsearch 等）。请参见下面标签下方的配置。Vector 的 `remap` 语言允许你丢弃噪音事件或添加派生属性，而无需触碰 rousseau。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

OpenTelemetry Collector 通过 journald 接收日志，并转发到任何 OTLP 后端：

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

一旦 rousseau 自身实现了 OTel exporter 路线图，这将变成端到端的 OTel，无需 journald 中转。

  </div>
</div>

## 日志管道：Loki + Grafana

### Systemd + Promtail

将 Promtail 指向 rousseau 服务的 journal：

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

然后 Grafana 面板即可基于 `level=WARN` 和 `msg="tool.denied"` 过滤，构建"被阻止的工具调用"面板。

### Kubernetes

将 Grafana Agent（或 Loki + Alloy）作为 DaemonSet 部署。因为 rousseau 在容器中写入 stdout，无需文件采集。

## 日志管道：Datadog

```
# /etc/datadog-agent/conf.d/rousseau.d/conf.yaml
logs:
  - type: journald
    include_units:
      - rousseau-agent.service
    service: rousseau-agent
    source: rousseau-agent
```

因为 rousseau 输出 JSON，Datadog 内置的 JSON 解析器会把 `level`、`msg` 和所有属性提升为一等 facet。请在 `msg:tool.denied` 上配置监控项，作为审批策略告警。

## 日志管道：Vector

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

## 值得绘图的关键指标

目前尚无 Prometheus 端点。你想要的指标都在日志流上：

| 指标 | 如何派生 |
|---|---|
| 工具调用速率 | 统计 `msg:tool.execute` |
| 拒绝率 | 统计 `msg:tool.denied` |
| 错误率 | 统计 `msg:tool.error` |
| 压缩事件 | 统计 `msg:agent.compressed` |
| Cron 触发 | 统计 `msg:cron.fire` |
| Cron 投递字节数 | 对 `msg:cron.deliver` 处的 `bytes` 求和 |

Loki + LogQL：`sum by (name) (count_over_time({job="rousseau-agent"} |= "tool.denied" [1h]))`。

## OpenTelemetry 路线图

OpenTelemetry 集成在路线图上。发布后可预期：

- 通过 agent loop 传播 `otel.trace` 上下文（每次 `Turn` 一个 span，每次工具调用一个子 span）。
- 用于当前基于日志的相同计数器的 metric exporter。
- 通过环境变量可配置的 OTLP 端点。

在此之前，请把结构化的 slog 输出视为可观测性的基础。任何你想要作为指标或 trace 的事件都已经存在 —— 元数据是完整的，只是线协议不同。

## 无日志管道时的调试

交互式：

```sh
rousseau --config /etc/rousseau/config.yaml whatsapp \
  --allow 447900123456@s.whatsapp.net 2>&1 | jq
```

守护进程把 slog 写到 stderr；通过 `jq` 管道可以获得交互式过滤。`jq 'select(.msg == "tool.denied")'` 会显示每一次被阻止的调用。

`rousseau doctor` 是另一个可观测性杠杆 —— 它是某一时刻所有依赖和所有配置选择的快照。

## 故障排查

### `journal has no entries`

守护进程还没写入日志，或 journald 匹配规则不对。用 `journalctl --user -u rousseau-agent.service --no-pager` 确认。

### 管道中出现 JSON 解析错误

Rousseau 每个事件写一行。如果某条日志事件的 `msg` 包含换行（罕见 —— 某些传输会包含多行错误字符串），管道可能把它拆分成两条事件。请用正则过滤，或使用能保留内嵌换行的结构化解析。

### 下游属性丢失

Loki 会丢弃无法映射为 label 的属性。请在 LogQL 中使用 `line_format` 将属性投射到渲染输出中，或用 `pipeline_stages.labels` 把它们索引为 label。

### 缺少 Datadog service 标签

Datadog 使用 `service` 字段进行过滤。journald 源会根据配置设置它；请确保 `service: rousseau-agent` 存在。

### Grafana 面板没有数据

请确认 LogQL 查询与你的 label 匹配。Promtail 的默认 `job` label 由 scrape 配置设置 —— 若你改动过它，请更新每个面板的查询。

## 相关页面

- [配置](/zh-Hans/configuration/) —— `log.level` 与 `log.format`。
- [指南：审计与审批策略](/zh-Hans/guides/audit-approval-policies/) —— 你最需要的告警信号。
- [参考：退出码](/zh-Hans/reference/exit-codes/) —— 守护进程如何向 init 系统报告失败。
- [安全](/zh-Hans/security/) —— 通过 slog 的审计轨迹。
- [参考：日志](/zh-Hans/reference/logs/) —— rousseau 输出的每一个 slog 键。

## 延伸阅读

- `internal/cli/root.go` —— `newLogger` 设置 slog handler。
- `internal/agent/agent.go` —— `tool.execute`、`tool.denied`、`agent.compressed` 事件。
- `internal/transport/whatsapp/dispatch.go` —— 传输侧事件输出。
- Grafana LogQL 文档与 Datadog 日志处理文档（外部）。
