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
changefreq: "weekly"
description: "rousseau-agent's cron scheduler runs stored jobs on a schedule and delivers replies through any registered transport. Backed by robfig/cron/v3 and SQLite job persistence."
keywords: "cron, robfig/cron, scheduler, scheduled jobs, delivery, transport-agnostic, SQLite persistence"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/cron/"
subtitle: "可通过任意传输触发的持久化定时任务。"
tags: "cron, scheduler, reference"
title: "Cron 调度器"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, robfig/cron, scheduler, scheduled jobs, delivery, transport-agnostic, SQLite persistence"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Cron 调度器"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 24
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/cron/index.html"
item_link: "https://docs.rousseau-agent.dev/cron/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Cron 调度器"
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
twitter_title: "Cron 调度器"
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

## 概述

cron 调度器（`internal/cron/scheduler.go`）是一个 goroutine，它按照配置的时间表运行保存的 `CronJob` 条目，通过 agent 执行每个作业的提示词，并把回复交给一个与传输无关的 `Delivery` 函数。

调度器与任何长期运行的守护进程共同运行（通常是 `rousseau whatsapp` 或其他聊天传输）。作业保存在与会话相同的 SQLite 数据库中，因此可以跨重启保留。

## 调度语法

底层由 [robfig/cron/v3](https://pkg.go.dev/github.com/robfig/cron/v3) 支持。解析器支持：

- 标准 5 字段 cron：`<minute> <hour> <day-of-month> <month> <day-of-week>`。
- 预定义快捷方式：`@yearly`、`@monthly`、`@weekly`、`@daily`、`@hourly`、`@every <duration>`。

示例调度：

| 表达式 | 触发时间 |
|---|---|
| `0 9 * * 1-5` | 工作日 09:00 |
| `*/15 * * * *` | 每 15 分钟 |
| `@daily` | 每天午夜一次（服务器时区） |
| `@every 30m` | 每 30 分钟 |

## CLI

```sh
# 列出所有已保存的作业。
rousseau cron list

# 添加一个作业。
rousseau cron add \
  --name morning-standup \
  --schedule '0 9 * * 1-5' \
  --prompt 'What are the top three engineering priorities today?' \
  --target '447900123456@s.whatsapp.net'

# 按名称或 ID 移除。
rousseau cron remove morning-standup
```

## 配置

作业保存在状态数据库中，而非配置文件里。`~/.config/rousseau/config.yaml` 中没有任何配置调度器自身的项；它使用默认 `PollInterval = 60s`。

## 作业流程

1. 调度器每隔 `PollInterval` 从 SQLite 重新同步作业列表。
2. `robfig/cron/v3` 在其计划时间触发作业。
3. `TurnRunner.RunOnce(ctx, job.Prompt)` 针对一个全新会话执行一次**单 turn** 的 agent 运行（除非 runner 显式选择，否则没有历史、没有跨会话召回）。
4. 回复文本被传入 `Delivery(ctx, job.Target, replyText)`。
5. `Delivery` 返回错误 → 记录日志；下一次 tick 时重试。

## 投递

`Delivery` 是一个小的函数类型：

```go
type Delivery func(ctx context.Context, target, body string) error
```

调度器不导入 `internal/transport` —— 投递契约与传输无关。实际上，`rousseau <transport>` 守护进程会布线一个 `Delivery`，它根据当前活动的传输来解析 target 字符串（传输客户端上的 `Deliver`）。

`target` 视传输而定：

- WhatsApp：一个 JID（`447900123456@s.whatsapp.net`）。
- Telegram：数字 chat ID。
- Slack：频道 ID（`C012345`）或用户 ID（`U012345`）。
- Discord：频道 ID。
- SMS：E.164 目标号码。
- iMessage：chat GUID。
- Signal：E.164 目标号码。
- Matrix：房间 ID。
- Email：完整的 RFC 5322 地址。

## 持久化

作业保存在状态数据库（`internal/state/sqlite/`）的 `cron_jobs` 表中。字段：`id`、`name`、`schedule`、`prompt`、`target`、`created_at`、`updated_at`。重启后会在下一次 `PollInterval` 时载入所有作业。

通过 `rousseau cron add` 新增的作业将在一个 `PollInterval` 内生效 —— 默认最多 60 秒。

## 与传输的交互

`Delivery` 闭包捕获对当前运行传输的引用。通常一个守护进程运行一个传输，因此 cron 调度器通过该传输投递。多传输部署为每个传输运行一个守护进程，运维者把每个 cron 作业的 `target` 指向匹配的传输守护进程。

跨传输投递（作业在 WhatsApp 守护进程中运行、通过 Slack 回复）目前不支持 —— 调度器只知道它被赋予的那个 `Delivery`。

## 失败模式

| 现象 | 解决方式 |
|---|---|
| 作业未触发 | 检查 `rousseau status`；调度器每次激活会记录 `cron.fired` 日志。 |
| 作业触发但没有消息到达 | 投递错误 —— 检查日志中的 `cron.delivery_failed`。 |
| 作业运行但模型拒绝执行 | 审批策略拒绝了工具调用。放宽 `agent.approver`，或切换到 `pattern` 模式。 |
| 投递到了错误的目标 | 调度器与传输无关；由守护进程解释 `target`。请确认你运行的传输匹配 target 格式。 |
