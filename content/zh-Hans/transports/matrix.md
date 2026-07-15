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
description: "Set up rousseau-agent's Matrix transport: homeserver URL, access token, user ID, long-polling /sync, allowlist by MXID."
keywords: "Matrix, client-server, MXID, access token, homeserver, /sync, long polling, Synapse"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/transports/matrix/"
subtitle: "Matrix client-server API with long-polling /sync."
tags: "transports, Matrix"
title: "Matrix 传输"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Matrix, client-server, MXID, access token, homeserver, /sync, long polling, Synapse"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Matrix 传输"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 15
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/transports/matrix/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/matrix/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Matrix 传输"
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
twitter_description: "Set up rousseau-agent's Matrix transport: homeserver URL, access token, user ID, long-polling /sync, allowlist by MXID."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Matrix 传输"
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

Matrix 传输（`internal/transport/matrix/`）直接使用 Matrix 客户端-服务器 API，未采用第三方 SDK。入站使用 `/sync` 长轮询；出站使用 `/rooms/{room}/send/{event_type}/{txn_id}`。

可与任何符合规范的 homeserver 一起工作：Synapse、Dendrite、Conduit。

## 先决条件

1. **一个 bot 账户**，位于你选定的 homeserver 上。可通过标准 Matrix 客户端或通过 homeserver 管理 API 注册。
2. **该账户的 access token**。先用普通 Matrix 客户端登录一次 bot，然后从 **设置 → 帮助与关于 → Access Token** 复制令牌。也可以直接使用登录 API：

   ```sh
   curl -X POST https://matrix.org/_matrix/client/v3/login \
     -H 'Content-Type: application/json' \
     -d '{"type":"m.login.password","user":"bot","password":"..."}'
   ```

3. **bot 的完整 MXID**（例如 `@rousseau-bot:matrix.org`），用于抑制自身消息回显。

## 配置

```yaml
matrix:
  homeserver_url: "https://matrix.org"
  access_token: "syt_..."
  user_id: "@rousseau-bot:matrix.org"
  reply_header: ""
  allowlist:
    - "@alice:matrix.org"
    - "@bob:example.com"
```

| 字段 | 默认值 | 作用 |
|---|---|---|
| `homeserver_url` | *必填* | 基础 URL（`https://matrix.org`）。 |
| `access_token` | *必填* | bot 用户的 access token。 |
| `user_id` | *空* | bot 用户的完整 MXID。可选但推荐（用于抑制自身消息回显）。 |
| `reply_header` | *空* | 前置到每条出站回复上。 |
| `allowlist` | `[]` | 允许处理消息的 MXID。 |

## 命令行

```sh
rousseau matrix \
  --homeserver-url https://matrix.org \
  --access-token syt_... \
  --user-id @rousseau-bot:matrix.org \
  --allow @alice:matrix.org
```

## 长轮询

`PollTimeout` 默认 30 秒。每次 `/sync` 响应中的 `since` 游标会保存在内存中，并用于下次调用，因此在进程生命周期内消息不会被重复投递。重启后，守护进程会回退到 homeserver 返回的仍然有效的最早游标 —— 这是标准的 `sync` 语义，与所有 Matrix 客户端一致。

## 房间邀请

bot 必须已是它要回复的每个房间的成员。请通过普通 Matrix 客户端进行邀请。rousseau 不会自动接受邀请；加入房间不在其职责范围内。

## 失败模式

| 现象 | 解决方式 |
|---|---|
| `/sync` 返回 401 | Access token 已过期或已失效。请重新登录。 |
| bot 从未收到消息 | 确认 bot 已经是房间成员，而不仅仅是被邀请。 |
| 自身消息回显环路 | 在配置中设置 `user_id`，让 rousseau 过滤掉自身消息。 |
