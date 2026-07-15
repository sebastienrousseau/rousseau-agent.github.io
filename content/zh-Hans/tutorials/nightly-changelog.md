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
description: "Schedule a rousseau cron job that summarises git log every evening and posts the result to WhatsApp."
keywords: "cron, git log, changelog, whatsapp, scheduled prompt, deliver-to"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/tutorials/nightly-changelog/"
subtitle: "A daily 18:00 cron job that pushes a git-log summary to WhatsApp."
tags: "tutorials, cron, changelog, whatsapp, git"
title: "教程：夜间生成变更日志"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, git log, changelog, whatsapp, scheduled prompt, deliver-to"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "教程：夜间生成变更日志"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/tutorials/nightly-changelog/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/nightly-changelog/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "教程：夜间生成变更日志"
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
twitter_title: "教程：夜间生成变更日志"
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

## 您将构建什么

一个存储在 rousseau 自身 SQLite 状态（`cron_jobs` 表，schema 见 `internal/state/sqlite/cron.go`）中的 cron 任务，在工作日本地时间 18:00 触发。它运行一个提示要求模型总结 `git log --since=today`，并通过 WhatsApp 将结果送到您的手机。

预计时间：10 分钟。

## 先决条件

- WhatsApp 桥接已配对（见 [快速开始](/zh-Hans/quickstart/) 第 4 步或 [传输：WhatsApp](/zh-Hans/transports/whatsapp/)）。
- `rousseau whatsapp` 守护进程正在运行 —— `internal/cron/scheduler.go` 中的 cron 调度器由传输守护进程通过 `wiring.startCron()` 启动，而不是由 `rousseau chat`。
- 一个包含您希望被总结的 git 仓库的工作区，bind-mount 到容器内（或如果您在容器外运行 rousseau，则在主机上）。

## rousseau cron 的工作方式

`rousseau cron add` 向 `cron_jobs` 表（`internal/state/sqlite/cron.go`）写入一行。每隔约 15 秒，`scheduler.sync` 重新读取该表并调和 robfig/cron/v3 的内存中调度。当一个任务触发时，调度器发出 `cron.firing`，通过配置的 provider 运行提示，并通过拥有该进程的传输桥（在本教程中是 WhatsApp）将结果投递到 `deliver_to`。

您会看到的结构化日志名称（来自 `internal/cron/scheduler.go`）：

- `cron.started` —— 调度器以 `poll_interval=…` 启动。
- `cron.scheduled` —— 一个任务已被接受。
- `cron.firing` —— 一个任务即将运行。
- `cron.completed` —— 一个任务成功完成。
- `cron.run_failed`、`cron.delivery_failed`、`cron.record_failed` —— 失败模式。

## 第 1 步：添加任务

```sh
rousseau cron add \
  --name        nightly-changelog \
  --schedule    "0 18 * * 1-5" \
  --prompt      "Summarise git log --since=yesterday under /workspace/rousseau-agent as a Slack-style bullet list. Keep it under 200 words. If nothing changed, reply with a single line 'no commits'." \
  --deliver-to  447900123456@s.whatsapp.net
```

cron 表达式由 `newCronAddCmd`（`internal/cli/cron.go`）中的 `robfig/cron/v3` 解析。无效表达式在写入前被拒绝。`--deliver-to` 值是 WhatsApp 的 E.164 JID（`<digits>@s.whatsapp.net`）；投递目标格式随传输而异。

## 第 2 步：核实

```sh
rousseau cron list
```

输出形状（来自 `newCronListCmd`）：

```
NAME               STATUS SCHEDULE       PROMPT                       DELIVER-TO
nightly-changelog  on     0 18 * * 1-5   Summarise git log …          447900123456@s.whatsapp.net
```

该列表也通过 MCP 以 `rousseau_cron_list` 暴露（见 `internal/mcp/tools.go`）。

## 第 3 步：试运行

没有内置的"立即触发"触发器。要冒烟测试，把任务临时安排在未来一分钟：

```sh
rousseau cron remove nightly-changelog
rousseau cron add --name test --schedule "*/1 * * * *" --prompt "say hi" --deliver-to "$JID"
journalctl --user -u rousseau-agent -f | grep cron.
```

预期日志序列：

```
INFO cron.scheduled  job=test expr=*/1 * * * *
INFO cron.firing     job=test
INFO cron.completed  job=test
```

完成后删除测试任务并重新添加真正的任务。

## 第 4 步：收紧提示

最好的 cron 提示是自足的：模型对之前的运行没有记忆。包含仓库路径、期望的输出格式，以及针对空情况的兜底。示例第二次迭代：

```
Summarise commits authored since 07:00 UTC today under
/workspace/rousseau-agent. Use this format:

- <short type>: <one-line summary> — <sha>

Group by author. If no commits landed, reply exactly: no commits.
```

## 开关与删除

```sh
rousseau cron disable nightly-changelog   # 保留该行，停止触发
rousseau cron enable  nightly-changelog
rousseau cron remove  nightly-changelog   # 删除该行
```

这些调用的是 `internal/state/sqlite/cron.go` 中的 `SetEnabled` 与 `Delete`。

## 相关

- [Cron](/zh-Hans/cron/) —— 调度器参考。
- [指南：定时任务](/zh-Hans/guides/scheduled-tasks/) —— 更深入的讨论。
- [传输：WhatsApp](/zh-Hans/transports/whatsapp/) —— delivery-to 的工作方式。
- [参考：CLI 命令](/zh-Hans/reference/cli-commands/) —— 每个 `rousseau cron` flag。
