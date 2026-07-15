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
description: "Worked example: use rousseau-agent's cron scheduler + WhatsApp to run a scheduled prompt daily and deliver the result to your phone."
keywords: "cron, scheduled tasks, whatsapp, code review, robfig, daily reminder"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/guides/scheduled-tasks/"
subtitle: "Nag yourself daily via WhatsApp."
tags: "guides, cron, scheduled, whatsapp"
title: "指南：定时任务"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, scheduled tasks, whatsapp, code review, robfig, daily reminder"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "指南：定时任务"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 31
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/guides/scheduled-tasks/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/scheduled-tasks/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "指南：定时任务"
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
twitter_description: "Worked example: use rousseau-agent's cron scheduler + WhatsApp to run a scheduled prompt daily and deliver the result to your phone."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "指南：定时任务"
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

## 场景

您希望每天 09:00 通过 WhatsApp 收到提醒，询问代码评审收件箱是否有滞留的项目。代理应该读取您的本地评审队列文件，做出摘要并将摘要发送到您的手机 —— 无论您的笔记本此时是否正在处理其他任务。

组成部分：

- 一个正在运行的 `rousseau whatsapp` 守护进程。
- 通过 `rousseau cron add` 持久化到 SQLite 中的 cron 任务。
- 守护进程内的 `robfig/cron/v3` 调度器 goroutine 触发任务；回复通过同一 WhatsApp 传输发送。

## 先决条件

- 已配对且能向至少一个 JID 投递消息的 `rousseau whatsapp`（[首个传输](/zh-Hans/getting-started/first-transport/)）。
- 一份提示可以指向的文件 —— 在本演练中，是位于 `/workspace/review-queue.md` 的 Markdown 队列。

## 第 1 步 —— 注册任务

```sh
rousseau cron add \
  --name daily-review-nag \
  --schedule "0 9 * * *" \
  --prompt "Read /workspace/review-queue.md and list every PR that has been open for more than 3 days. Reply with 3 bullets max." \
  --deliver-to 447900123456@s.whatsapp.net
```

`--schedule` 是由 `robfig/cron/v3` 解析的 5 字段 POSIX 风格 cron 表达式（`min hour dom mon dow`）。Rousseau 在添加时校验表达式；无效的调度会在写入存储前快速失败。

`--deliver-to` 是接收回复的 WhatsApp JID。对于群组，使用 `@g.us` 形式。

## 第 2 步 —— 确认任务已生效

```sh
rousseau cron list
```

输出：

```
b7a3f2e1  on   daily-review-nag      0 9 * * *             last=never
    Read /workspace/review-queue.md and list every PR that has been open for more than 3 days. Reply with 3 bullets max. → 447900123456@s.whatsapp.net
```

新任务会在下一次调度器轮询间隔（默认 60 秒）内生效。无需重启。

## 第 3 步 —— 强制试运行

定时任务由运行中的 `rousseau whatsapp` 守护进程触发。要在不等到 09:00 的情况下验证接线，请临时将调度改为一分钟后运行：

```sh
rousseau cron remove daily-review-nag
rousseau cron add \
  --name daily-review-nag \
  --schedule "*/1 * * * *" \
  --prompt "..." \
  --deliver-to 447900123456@s.whatsapp.net
```

观察守护进程的日志：

```
cron.fire   name=daily-review-nag job=b7a3f2e1
tool.execute name=read id=t_1
cron.deliver name=daily-review-nag target=447900123456@s.whatsapp.net bytes=284
```

一旦您在手机上看到消息，删除每分钟版本并重新添加每日版本。

## 第 4 步 —— 停用但不删除

```sh
rousseau cron disable daily-review-nag
```

将 `enabled=false` 保留在存储中的任务上，每次触发时会跳过它。使用 `rousseau cron enable daily-review-nag` 重新启用。

## 底层发生了什么

1. `rousseau cron add` 向 `~/.local/share/rousseau/sessions.db` 中的 `cron` 表写入一行。
2. `rousseau whatsapp` 守护进程在启动时启动一个 `robfig/cron/v3` 调度器 goroutine，并每隔 `PollInterval`（默认 60 秒）轮询该表。
3. 当 cron 表达式触发时，`Runner.RunOnce(ctx, prompt)` 在一个全新的会话上运行一次单发代理轮次（不携带之前触发的历史）。
4. 回复通过 `Delivery` —— 一个与传输无关的回调，守护进程将其接线到 `client.Deliver(ctx, target, body)`。
5. `last_run_at` 在存储中更新。失败会被记录但不会停用任务。

调度器是持久的：如果守护进程在触发过程中崩溃，下次启动会拾取队列。由于 `robfig/cron/v3` 按 tick 去重，任务不会在同一分钟触发两次。

## 常见模式

| 调度 | 含义 |
|---|---|
| `0 9 * * *` | 每天 09:00。 |
| `*/15 9-17 * * 1-5` | 周一至周五 09:00–17:59 每 15 分钟。 |
| `0 * * * *` | 每小时整点。 |
| `0 0 * * 0` | 每周日午夜。 |

## 与 skills 分层

长提示令人厌烦。如果定时任务的提示不断膨胀，把样板搬到 [skill](/zh-Hans/skills/) 中，让提示引用它。skill 会在触发时拼接进系统提示。

## 注意事项

- 定时任务针对守护进程配置的 provider 运行。如果您的主 provider 是 `claudecli` 且您轮换了底层 `claude` 登录，触发会失败直到您重新认证。
- 投递目标必须属于守护进程的允许列表。即使定时任务要求，Rousseau 也不会投递到允许列表之外的 JID。
- 按设计，cron 调度器运行在 `rousseau whatsapp` 守护进程内部。同时运行 `rousseau slack` 会得到两个读取同一张表的独立调度器 —— 任务会触发两次。挑一个守护进程拥有调度权。

## 下一步

- [Cron 参考](/zh-Hans/cron/) —— 每个子命令、每个 flag。
- [Skills](/zh-Hans/skills/) —— 在任务之间共享提示样板。
- [审计 + 审批策略](/zh-Hans/guides/audit-approval-policies/) —— 锁定定时提示能做什么。
