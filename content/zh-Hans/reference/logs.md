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
description: "rousseau-agent's slog output: message vocabulary, JSON vs text shape, and journalctl / jq recipes."
keywords: "slog, logs, json, text, journalctl, jq, observability"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/reference/logs/"
subtitle: "The full vocabulary of slog messages rousseau emits."
tags: "reference, logs, slog, observability, audit"
title: "参考：日志"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "slog, logs, json, text, journalctl, jq, observability"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "参考：日志"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 52
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/reference/logs/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/logs/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "参考：日志"
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
twitter_title: "参考：日志"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "感谢每一位运行自有编码代理的运维者。"
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Logger 装配

`internal/cli/root.go` 为每个进程构建一个 `*slog.Logger` —— 当 `log.format` 为空或 `text` 时使用 `slog.NewTextHandler`，为 `json` 时使用 `slog.NewJSONHandler`。级别从 `log.level`（`debug`、`info`、`warn`/`warning`、`error`）映射，默认 `info`。Handler 写入 stderr；每个守护进程都继承。

对于生产部署，请始终设置 `log.format: json`。下游日志管道（journald + `journalctl -o json`、Loki、Vector、Datadog Agent）能原生解析结构化输出。

## 输出形状

### Text

```
time=2026-07-13T18:00:14.202Z level=INFO msg=tool.execute name=grep id=t_1
```

Slog 的默认 text 布局：`time`、`level`、`msg`，其后为 key=value 对。

### JSON

```json
{"time":"2026-07-13T18:00:14.202Z","level":"INFO","msg":"tool.execute","name":"grep","id":"t_1"}
```

同样的字段，JSON 编码。`msg` 字段是稳定事件标识符 —— 请基于它过滤与告警，而非基于人类可读文本。

## 消息词汇

下面列出从 `internal/**/*.go` 发出的每个消息名，附带源码位置与期望级别。按子系统分组；组内按字母顺序。

### 代理循环（`internal/agent/`）

| 消息 | 级别 | 字段 | 含义 |
|---|---|---|---|
| `agent.compressed` | INFO | `messages` | LLM 压缩器重写了会话；新的消息计数为 `messages`。 |
| `agent.compress_failed` | WARN | `err` | 压缩器返回错误；会话保持不变。 |
| `tool.denied` | WARN | `name`、`reason` | 审批器阻止了一次工具调用。字段来自 `internal/agent/agent.go:179`。 |
| `tool.execute` | INFO | `name`、`id` | 审批器放行且工具已运行。 |
| `tool.error` | WARN | `name`、`err` | 工具运行但返回错误。 |
| `turn.failed` | ERROR | `err` | TUI 轮次出错。由 `internal/tui/model.go` 发出。 |
| `session.save_failed` | WARN | `err` | 轮次结束后持久化会话失败。 |

### Cron（`internal/cron/scheduler.go`）

| 消息 | 级别 | 字段 | 含义 |
|---|---|---|---|
| `cron.started` | INFO | `poll_interval` | 调度器启动。 |
| `cron.scheduled` | INFO | `job`、`expr` | 任务已加入内存调度。 |
| `cron.schedule_failed` | WARN | `job`、`expr`、`err` | robfig/cron/v3 拒绝了该表达式。 |
| `cron.sync_failed` | WARN | `err` | 对 `cron_jobs` 的对账 pass 失败。 |
| `cron.firing` | INFO | `job` | 任务即将运行。 |
| `cron.completed` | INFO | `job` | 任务成功完成。 |
| `cron.run_failed` | ERROR | `job`、`err` | 任务内的 provider 调用失败。 |
| `cron.delivery_failed` | ERROR | `job`、`target`、`err` | 向传输的投递失败。 |
| `cron.record_failed` | WARN | `job`、`err` | 写入 `last_run_at` 失败。 |

### MCP（`internal/mcp/server.go`）

| 消息 | 级别 | 字段 | 含义 |
|---|---|---|---|
| `mcp.encode_error` | WARN | `err` | 无法对响应做 JSON 编码（罕见）。 |
| `mcp.tool_error` | WARN | `tool`、`err` | 工具处理器返回错误；以 `isError=true` 呈给宿主。 |

### Router（`internal/transport/router.go`）

| 消息 | 级别 | 字段 | 含义 |
|---|---|---|---|
| `transport.rejected` | WARN | `from` | 发送者不在允许列表；消息丢弃。 |
| `router.save_failed` | WARN | `err` | 轮次结束后会话保存失败。 |
| `router.stale_mapping` | WARN | `jid`、`err` | JID→会话映射指向已无法加载的会话。 |

### WhatsApp（`internal/transport/whatsapp/`）

| 消息 | 级别 | 字段 | 含义 |
|---|---|---|---|
| `whatsapp.starting` | INFO | `store`、`allowlist` | 桥接启动；`store` 为 DSN。 |
| `whatsapp.qr_ready` | INFO | — | QR 已渲染到 stdout；请扫描。 |
| `whatsapp.qr_event` | WARN | `event` | 来自 whatsmeow 的非成功 QR 事件。 |
| `whatsapp.paired` | INFO | — | 手机接受了 QR。 |
| `whatsapp.connected` | INFO | — | 到 Meta 的 WebSocket 已连通。 |
| `whatsapp.disconnected` | WARN | — | 丢失连接。会自动重试。 |
| `whatsapp.logged_out` | ERROR | `reason` | Meta 已注销该设备 —— 通常是触发策略。 |
| `whatsapp.voice_enabled` | INFO | `binary`、`model` | 语音笔记转写已开启。 |
| `whatsapp.incoming` | INFO | `from` | 入站消息已接受。 |
| `whatsapp.skipped` | DEBUG | `reason` | Router 丢弃了一条消息（自回显等）。 |
| `whatsapp.empty_reply` | INFO | `elapsed` | 代理本轮未产生文本。 |
| `whatsapp.handler_ok` | INFO | `elapsed`、`bytes` | 回复已投递。 |
| `whatsapp.handler_failed` | ERROR | `err` | 轮次出错 —— 通常是 provider 或工具失败。 |
| `whatsapp.send_failed` | ERROR | `err` | 向 Meta 的投递失败。 |
| `whatsapp.presence_failed` | DEBUG | `err` | typing-presence 写入失败（尽力而为）。 |
| `whatsapp.audio_ignored` | INFO | `size` | 收到语音笔记但转写被禁用。 |
| `whatsapp.audio_downloaded` | INFO | `size` | 已从 Meta 获取语音笔记字节。 |
| `whatsapp.transcribed` | INFO | `elapsed` | whisper.cpp 返回了转写。 |
| `whatsapp.transcribe_failed` | ERROR | `err` | whisper 调用失败。 |

### Slack（`internal/transport/slack/client.go`）

| 消息 | 级别 | 字段 | 含义 |
|---|---|---|---|
| `slack.starting` | INFO | `allowlist` | 桥接启动。 |
| `slack.started` | INFO | — | Socket Mode 会话已接受。 |
| `slack.session_failed` | WARN | `err` | 打开 Socket Mode 会话失败；将重试。 |
| `slack.frame_failed` | WARN | `err` | 来自 Slack 的畸形帧。 |
| `slack.incoming` | INFO | `from`、`channel`、`text` | 消息已接受。 |
| `slack.handler_failed` | ERROR | `err` | 轮次出错。 |

### Discord（`internal/transport/discord/client.go`）

| 消息 | 级别 | 字段 | 含义 |
|---|---|---|---|
| `discord.starting` | INFO | `allowlist` | 桥接启动。 |
| `discord.ready` | INFO | `bot_id` | Discord gateway 就绪。 |
| `discord.started` | INFO | — | 会话已连通。 |
| `discord.session_failed` | WARN | `err` | Gateway 打开失败；将重试。 |
| `discord.frame_failed` | WARN | `err` | 来自 Discord 的坏帧。 |
| `discord.incoming` | INFO | `from`、`channel` | 消息已接受。 |
| `discord.handler_failed` | ERROR | `err` | 轮次出错。 |

### Telegram（`internal/transport/telegram/client.go`）

| 消息 | 级别 | 字段 | 含义 |
|---|---|---|---|
| `telegram.starting` | INFO | `allowlist` | 桥接启动。 |
| `telegram.started` | INFO | — | 首次长轮询成功。 |
| `telegram.poll_failed` | WARN | `err` | 长轮询 HTTP 失败。 |
| `telegram.incoming` | INFO | `from` | 消息已接受。 |
| `telegram.handler_failed` | ERROR | `err` | 轮次出错。 |
| `telegram.send_failed` | ERROR | `err` | 出站 HTTP 失败。 |

### Matrix（`internal/transport/matrix/client.go`）

| 消息 | 级别 | 字段 | 含义 |
|---|---|---|---|
| `matrix.starting` | INFO | `homeserver`、`allowlist` | 桥接启动。 |
| `matrix.started` | INFO | `homeserver` | 首个 `/sync` 已接受。 |
| `matrix.sync_failed` | WARN | `err` | `/sync` HTTP 失败。 |
| `matrix.incoming` | INFO | `from`、`room` | 消息已接受。 |
| `matrix.handler_failed` | ERROR | `err` | 轮次出错。 |
| `matrix.send_failed` | ERROR | `err` | 出站 HTTP 失败。 |

### Signal（`internal/transport/signal/`）

| 消息 | 级别 | 字段 | 含义 |
|---|---|---|---|
| `signal.starting` | INFO | `account`、`allowlist` | signal-cli JSON-RPC 子进程启动。 |
| `signal.started` | INFO | — | 子进程报告就绪。 |
| `signal.frame_failed` | WARN | `err` | 来自 signal-cli 的畸形 JSON 帧。 |
| `signal.stderr` | WARN | `line` | signal-cli stderr 的透传。 |
| `signal.incoming` | INFO | `from` | 消息已接受。 |
| `signal.handler_failed` | ERROR | `err` | 轮次出错。 |

### iMessage（`internal/transport/imessage/client.go`）

| 消息 | 级别 | 字段 | 含义 |
|---|---|---|---|
| `imessage.starting` | INFO | `base` | BlueBubbles 服务器 URL 已记录。 |
| `imessage.started` | INFO | `server` | 首次轮询成功。 |
| `imessage.prime_failed` | WARN | `err` | 预热状态抓取失败；将重试。 |
| `imessage.poll_failed` | WARN | `err` | 轮询 HTTP 失败。 |
| `imessage.incoming` | INFO | `from` | 消息已接受。 |
| `imessage.handler_failed` | ERROR | `err` | 轮次出错。 |
| `imessage.send_failed` | ERROR | `err` | 出站 HTTP 失败。 |

### Email + SMS（`internal/transport/email/`、`internal/transport/sms/`）

遵循与上方轮询传输相同的 `<transport>.starting / .started / .poll_failed / .incoming / .handler_failed / .send_failed` 形态。

## 配方

### 显示今日所有失败的工具调用

```sh
journalctl --user -u rousseau-agent --since today -o json \
  | jq -c 'select(.MESSAGE | fromjson? | .msg == "tool.denied")'
```

### 实时跟踪单一传输会话

```sh
journalctl --user -u rousseau-agent -f -o cat \
  | grep -E 'whatsapp\.|tool\.|cron\.'
```

### 对 cron 失败告警

Prometheus/alertmanager 规则草图（经由 [指南：可观测性](/zh-Hans/guides/observability/) 中的 `promtail` → Loki → alert 管道）：

```yaml
- alert: RousseauCronFailure
  expr: |
    sum by (job) (
      count_over_time({app="rousseau-agent"} |= "cron.run_failed" [5m])
    ) > 0
```

### 脱敏

`slog` 默认不做脱敏。请配置下游处理器对 `whatsapp.send_failed`、`tool.error` 等的 `err` 字段脱敏 —— provider 错误偶尔可能包含提示片段。管道见 [指南：可观测性](/zh-Hans/guides/observability/)。

## 相关

- [用户指南：审批策略](/zh-Hans/user-guide/approval-policies/) —— `tool.denied` 的源头。
- [指南：可观测性](/zh-Hans/guides/observability/) —— 完整管道配方。
- [指南：审计 + 审批策略](/zh-Hans/guides/audit-approval-policies/) —— 将这些日志视为审计线索。
