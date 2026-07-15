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
description: "Set up rousseau-agent's Discord transport: Gateway v10 WebSocket, bot token, Message Content intent, allowlist by user ID."
keywords: "Discord, Gateway v10, WebSocket, bot token, Message Content intent, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/transports/discord/"
subtitle: "Discord Gateway v10 over WebSocket."
tags: "transports, Discord"
title: "Discord 传输"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Discord, Gateway v10, WebSocket, bot token, Message Content intent, allowlist"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Discord 传输"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 17
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/transports/discord/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/discord/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Discord 传输"
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
twitter_description: "Set up rousseau-agent's Discord transport: Gateway v10 WebSocket, bot token, Message Content intent, allowlist by user ID."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Discord 传输"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">你将学到</span><p>Discord Developer Portal 的操作步骤、rousseau 需要哪些 Gateway intents 以及原因、权限位计算方法，以及常见配置错误的失败模式。请配合 <code>internal/transport/discord/client.go</code> 一起阅读本页。</p></aside>

## 概述

Discord 传输（`internal/transport/discord/`）直接使用 Discord Gateway v10 协议，未采用第三方 SDK。入站使用 WebSocket（`Identify → Ready → Heartbeat/Ack → Dispatch(MESSAGE_CREATE)`）；出站使用 REST（`POST /channels/{id}/messages`）。

## 先决条件

1. **一个带 Bot 用户的 Discord 应用。** 在 https://discord.com/developers/applications 创建 → **New Application** → **Bot** 选项卡 → **Add Bot**。
2. **一个 bot 令牌**（Bot 选项卡 → **Reset Token** → 复制令牌 —— 仅显示一次）。
3. **启用 Message Content intent**（Bot 选项卡 → **Privileged Gateway Intents**）。若未启用，Gateway 会从每个事件中剥离消息文本，rousseau 将只能看到空正文。
4. **bot 已被邀请到至少一个服务器**（或已启用 DM）。在 **OAuth2 → URL Generator** 下生成邀请 URL，勾选 `bot` scope 以及 `Send Messages` 和 `Read Message History` 权限。

## 配置

```yaml
discord:
  token: "Bot MTIz..."
  reply_header: ""
  allowlist:
    - "123456789012345678"
```

| 字段 | 默认值 | 作用 |
|---|---|---|
| `token` | *必填* | 来自 Developer Portal 的 bot 令牌。 |
| `reply_header` | *空* | 前置到每条出站回复上。 |
| `allowlist` | `[]` | 允许处理消息的 Discord 用户 ID。 |

## 命令行

```sh
rousseau discord --token 'MTIz...' --allow 123456789012345678
```

## Gateway intents

rousseau 请求三个 intent（`internal/transport/discord/client.go`）：

| Intent | Bit | 用途 |
|---|---|---|
| `GUILD_MESSAGES` | `1 << 9` | 服务器频道中的消息。 |
| `DIRECT_MESSAGES` | `1 << 12` | 发给 bot 的私信。 |
| `MESSAGE_CONTENT` | `1 << 15` | 填充 `content` 字段。**必须在 portal 中启用。** |

若未启用 Message Content intent，`MESSAGE_CREATE` 事件到达时 `content` 为空，rousseau 将记录 `discord.empty_body`。

## 心跳

该传输遵守 Gateway 通过 Hello opcode 下发的 `heartbeat_interval`，发送 Heartbeat 并跟踪 `heartbeat_ack`。丢失 ack 会关闭套接字，并让 systemd 重启进程。

## 回复前缀

Discord 将 `**text**` 渲染为粗体，并不要求特定的前缀格式。可根据需要覆盖：

```yaml
discord:
  reply_header: "**Rousseau Agent**\n"
```

## 权限位计算器

Discord 使用位掩码来编码 bot 的频道权限。每个权限是 2 的幂。rousseau 常用的权限：

| 权限 | Bit |
|---|---|
| Read Messages / View Channels | `1 << 10` = `1024` |
| Send Messages | `1 << 11` = `2048` |
| Send Messages in Threads | `1 << 38` = `274877906944` |
| Read Message History | `1 << 16` = `65536` |
| Add Reactions | `1 << 6` = `64` |

要授予多个权限，将这些位按位或，并把结果整数粘贴到 OAuth2 URL Generator 的 `permissions=` 参数中：

```
Read Messages (1024) OR Send Messages (2048) OR Read Message History (65536) = 68608
```

<aside class="admonition" data-type="note"><span class="admonition-title">Portal 辅助工具</span><p>Developer portal 的 <em>OAuth2 URL Generator</em> 让你勾选权限复选框并为你计算整数。将生成的 URL 加入书签 —— 服务器管理员可用它把 bot 邀请到任何 Discord 服务器。</p></aside>

## Gateway 生命周期

Gateway 是有状态的：

```
Client                        Discord Gateway
  │
  │   ────  Connect  ────▶
  │   ◀── HELLO (heartbeat_interval)
  │
  │   ───── IDENTIFY (token, intents) ────▶
  │   ◀── READY (session_id, user)
  │
  │   ─── Heartbeat every N ms ─▶
  │   ◀── HEARTBEAT_ACK
  │
  │   ◀── MESSAGE_CREATE (a user typed)
  │   ─── (rousseau handles + POSTs reply)
  │
  │   ◀── Disconnect (code 4009: session timed out)
  │   ─── RESUME (session_id) or re-IDENTIFY
```

客户端会跟踪 `heartbeat_ack`。若某次 ack 丢失，套接字会关闭，进程随之退出 —— 由 systemd 或容器运行时重启。

## 失败模式

| 现象 | 解决方式 |
|---|---|
| bot 看到的都是空消息 | 在 developer portal 中启用 Message Content intent。 |
| Gateway 以 4004 关闭 | 令牌无效。请重新生成。 |
| bot 看不到任何频道 | 确认 OAuth2 邀请包含了 `bot` scope。 |
| 发送时 403 | bot 在该频道缺少 `Send Messages` 权限。 |
| Identify 时 4014 | 请求了应用未获准的 intent（通常是 100+ 服务器的 bot 请求 Message Content）。请为你的 bot 完成认证。 |
| 4009（会话超时） | 长时间空闲后属正常现象。Rousseau 会透明重连。 |

## 故障排查

### Gateway 4013（Invalid Intents）

你请求了一个不存在的 intent 位。这通常意味着客户端库的 intent 常量与 Discord 当前的 intent 映射不一致。Rousseau 在 `internal/transport/discord/client.go` 中构建 intent 位掩码；若在 Discord API 变更后出现 4013，请升级到最新版本。

### bot 收到事件但未响应

允许列表不匹配。`--allow` 的值必须是数字型 Discord 用户 ID（不是用户名，也不是显示名）。在 Discord 中获取方式：在 *用户设置 > 高级* 里启用开发者模式，然后右键某用户 > *复制用户 ID*。

### DM 正常但服务器频道不行

缺少 `GUILD_MESSAGES` intent，或 bot 尚未被邀请到该服务器。服务器权限与 DM 权限是分开的 —— bot 必须对该频道拥有 `Read Messages` 权限。

### 出站消息返回 `429 Too Many Requests`

Discord 对每个 bot 实施全局 50 req/s 速率限制，并有每频道限制。在持续高负载下，rousseau 目前不会重试 —— 调用方必须自行退避。参见 [指南：速率限制](/zh-Hans/guides/rate-limits/)。

### bot 在线状态频繁波动

Discord 在约 40 秒没有心跳后会将 bot 视为离线。日志中的 `discord.heartbeat_missed` 表示网络问题或 CPU 资源不足。请确认容器分配了足够的 CPU。

## 相关页面

- [入门：第一个传输](/zh-Hans/getting-started/first-transport/) —— 端到端演练。
- [配置](/zh-Hans/configuration/) —— `discord` 配置块。
- [传输](/zh-Hans/transports/) —— 同类传输。
- [指南：审计与审批策略](/zh-Hans/guides/audit-approval-policies/) —— 针对 Discord 服务器的策略。
- [部署](/zh-Hans/deployment/) —— 在 Podman 容器中运行 Discord。

## 延伸阅读

- `internal/transport/discord/client.go` —— Gateway 连接、心跳、事件泵。
- `internal/cli/discord.go` —— CLI 布线。
- `internal/transport/router.go` —— 允许列表强制执行。
- [Discord API 文档：Gateway](https://discord.com/developers/docs/topics/gateway)。
- [Discord API 文档：Permissions](https://discord.com/developers/docs/topics/permissions)。
