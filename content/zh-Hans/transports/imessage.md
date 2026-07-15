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
description: "Set up rousseau-agent's iMessage transport: BlueBubbles server on macOS, HTTP polling, poll interval, cursor deduplication, chat GUID for outbound."
keywords: "iMessage, BlueBubbles, macOS, HTTP polling, chat GUID, cursor, deduplication"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/transports/imessage/"
subtitle: "BlueBubbles HTTP polling from a macOS host."
tags: "transports, iMessage"
title: "iMessage 传输"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "iMessage, BlueBubbles, macOS, HTTP polling, chat GUID, cursor, deduplication"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "iMessage 传输"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 18
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/transports/imessage/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/imessage/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "iMessage 传输"
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
twitter_description: "Set up rousseau-agent's iMessage transport: BlueBubbles server on macOS, HTTP polling, poll interval, cursor deduplication, chat GUID for outbound."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "iMessage 传输"
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

iMessage 传输（`internal/transport/imessage/`）不会直接接触 iMessage —— Apple 没有提供受支持的面向客户端的 API。它通过轮询 [BlueBubbles](https://bluebubbles.app) 实现，这是一个运行在 macOS 上的守护进程，通过 HTTP + Socket.IO 暴露 iMessage。

rousseau 仅使用 BlueBubbles 的 HTTP 端点（刻意避免使用 Socket.IO，以保持依赖体积精简）。

## 架构

```
+-----------+     iMessage      +---------+     HTTP      +-----------+
| Apple ID  | <---------------> | macOS   | <-----------> | rousseau  |
|  server   |                   | Blue    |               | daemon    |
+-----------+                   | Bubbles |               |           |
                                +---------+               +-----------+
```

macOS 主机运行 BlueBubbles 并保持登录 iMessage。rousseau 按配置的频率轮询 BlueBubbles 的 `/api/v1/message` 端点，将新到达的消息转发给处理程序。

## 先决条件

1. **一台已登录 iMessage 的 macOS 主机。** 不必与运行 rousseau 的机器相同。
2. **BlueBubbles 服务器**已安装在该主机上，并在 rousseau 可以访问的 URL（LAN 地址、VPN 或 Tailscale）上监听。
3. **BlueBubbles 密码**，来自服务器 GUI（Settings → Server Password）。
4. **一个用于出站的 chat GUID**。可在 BlueBubbles 的 GUI 中找到，或通过 `GET /api/v1/chat` 获取。

## 配置

```yaml
imessage:
  base_url: "http://mac.internal:1234"
  password: "..."
  chat_guid: "iMessage;-;+15550001234"
  poll_interval: "5s"
  reply_header: ""
```

| 字段 | 默认值 | 作用 |
|---|---|---|
| `base_url` | *必填* | BlueBubbles 服务器 URL。 |
| `password` | *必填* | BlueBubbles 服务器密码。 |
| `chat_guid` | *空* | 出站目标 GUID。 |
| `poll_interval` | `5s` | 对 `/api/v1/message` 的轮询频率。 |
| `reply_header` | *空* | 前置到每条出站消息上。 |

## 命令行

```sh
rousseau imessage \
  --base-url http://mac.internal:1234 \
  --password ... \
  --chat-guid 'iMessage;-;+15550001234' \
  --poll-interval 5s
```

## 游标去重

启动时，传输会将其 `lastID` 游标初始化为最新的现有消息，以免运维者被整段 iMessage 历史消息轰炸。随后的每次轮询会获取最新的 `PageSize` 条消息（默认 25），只转发比游标更新的那些。

游标只保存在内存中。重启后，游标会从 BlueBubbles 重新初始化 —— 守护进程停机期间到达的一小段消息将被漏掉。这是一种有意的取舍；持久化游标逻辑需要在状态存储中新增一张表，而且 iMessage 的投递时间戳在不同设备间无法保证单调递增。

## 可达性

无论 rousseau 在何处运行，BlueBubbles 必须在网络上可达。常见方案：

- **同一 LAN。** `http://<mac-lan-ip>:1234`。
- **Tailscale。** `http://mac.tailnet.ts.net:1234`。加密连接，可跨 NAT 使用。
- **反向隧道。** 在 rousseau 主机上使用 `http://localhost:1234`，从 Mac 建立 SSH `-R` 隧道。

除非你充分理解其鉴权模型（仅一个密码），否则不要将 BlueBubbles 暴露到公网。

## 失败模式

| 现象 | 解决方式 |
|---|---|
| 启动时 `imessage.prime_failed` | BlueBubbles 不可达 —— 请检查 `base_url` 和 `password`。 |
| 所有历史消息被重放 | `lastID` 没有正确初始化。请检查权限 / 鉴权。 |
| 出站消息被静默丢弃 | `chat_guid` 错误。请通过 `GET /api/v1/chat` 查找。 |
| 消息延迟数分钟到达 | 提高 BlueBubbles 自身的轮询频率，或降低 `poll_interval`。 |
