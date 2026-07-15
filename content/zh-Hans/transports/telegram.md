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
description: "Set up rousseau-agent's Telegram transport: BotFather token, long-polling, allowlist by numeric user ID, reply-header customisation."
keywords: "Telegram, Bot API, BotFather, long polling, getUpdates, allowlist, chat ID"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/transports/telegram/"
subtitle: "Telegram Bot API over long-polling."
tags: "transports, Telegram"
title: "Telegram 传输"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Telegram, Bot API, BotFather, long polling, getUpdates, allowlist, chat ID"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Telegram 传输"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 14
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/transports/telegram/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/telegram/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Telegram 传输"
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
twitter_description: "Set up rousseau-agent's Telegram transport: BotFather token, long-polling, allowlist by numeric user ID, reply-header customisation."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Telegram 传输"
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

Telegram 传输（`internal/transport/telegram/`）直接使用 Telegram Bot HTTP API，未采用第三方 SDK。入站通过 `getUpdates` 长轮询；出站通过 `sendMessage`。

## 先决条件

1. **一个 bot。** 在 Telegram 中给 [@BotFather](https://t.me/BotFather) 发送 `/newbot`，选择名称以及以 `_bot` 为后缀的用户名。BotFather 会返回一个 HTTP API 令牌，形如 `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`。
2. **要授权的用户 ID。** Telegram 用户 ID 是数字。bot 自身无法将 `@username` 解析为用户 ID —— 常用做法是让每位被授权的用户先向 bot 发送一次 `/start`，然后从日志读取 `from.id`。

## 配置

```yaml
telegram:
  token: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
  reply_header: ""
  allowlist:
    - "12345678"
    - "98765432"
```

| 字段 | 默认值 | 作用 |
|---|---|---|
| `token` | *必填* | 来自 BotFather 的 bot 令牌。 |
| `base_url` | `https://api.telegram.org` | 用于覆盖为本地 Bot API 服务器。 |
| `reply_header` | *空* | 前置到每条出站回复上。 |
| `allowlist` | `[]` | 允许处理消息的 Telegram 用户 ID。 |

## 命令行

```sh
rousseau telegram --token 123456:ABC... --allow 12345678 --allow 98765432
```

`--allow` 可重复使用。

## 长轮询

该传输默认以 30 秒的 `PollTimeout` 调用 `getUpdates`（`internal/transport/telegram/client.go`）。每次返回的更新都会推进内部 `offset`，因此即使跨重启也不会重复投递消息。

不需要 webhook。守护进程无需暴露入站 HTTP 接口。

## 消息形态

仅处理文本消息。媒体、贴纸和语音消息会被忽略（未来版本可能通过与 WhatsApp 相同的 whisper.cpp 路径来处理音频）。

## 失败模式

| 现象 | 解决方式 |
|---|---|
| 没有收到任何更新 | 确认至少已向 bot 发送过一条消息 —— Telegram 不会投递历史消息。 |
| getUpdates 返回 409 Conflict | 另一个实例正在使用同一个令牌轮询。停止另一个实例。 |
| 允许列表拒绝了一个真实用户 | 查看日志中的 `from.id` 字段；用户 ID 是数字，不会匹配 `@username`。 |
