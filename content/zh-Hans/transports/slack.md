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
description: "Set up rousseau-agent's Slack transport: Socket Mode (xapp-* app token + xoxb-* bot token), no public webhook, allowlist by user ID."
keywords: "Slack, Socket Mode, xapp, xoxb, chat.postMessage, connections:write, no webhook, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/transports/slack/"
subtitle: "Socket Mode with no public HTTP surface."
tags: "transports, Slack"
title: "Slack 传输"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Slack, Socket Mode, xapp, xoxb, chat.postMessage, connections:write, no webhook, allowlist"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Slack 传输"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 16
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/transports/slack/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/slack/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Slack 传输"
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
twitter_description: "Set up rousseau-agent's Slack transport: Socket Mode (xapp-* app token + xoxb-* bot token), no public webhook, allowlist by user ID."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Slack 传输"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">你将学到</span><p>完整的 app.slack.com 向导流程、需要授予的精确 OAuth 作用域、要配置的事件订阅、Socket Mode 如何避免公开 webhook 的需要，以及 rousseau 的自身消息循环预防如何工作。请对照阅读 <code>internal/transport/slack/client.go</code>。</p></aside>

## 概述

Slack 传输（`internal/transport/slack/`）使用 **Socket Mode**——出站到 Slack 的 WebSocket——因此守护进程无需公开 HTTP 面。入站事件流经 socket；出站调用打到标准 Web API（`chat.postMessage`）。

<aside class="admonition" data-type="tip"><span class="admonition-title">为什么用 Socket Mode</span><p>替代方案（Events API + Request URL）需要带 SSL 证书的公开 HTTPS 端点。Rousseau 按设计不提供任何入站 HTTP 面，因此 Socket Mode 是唯一支持的入口路径。</p></aside>

## 两个令牌

Slack Socket Mode 需要两个职责互不重叠的令牌：

| 令牌 | 前缀 | 作用域 | 用途 |
|---|---|---|---|
| 应用级令牌 | `xapp-` | `connections:write` | 打开 Socket Mode WebSocket。 |
| 机器人令牌 | `xoxb-` | `chat:write` + 事件订阅 | 发送消息、订阅事件。 |

## 应用设置

完整步骤位于 https://app.slack.com/apps ：

1. **创建新应用**（"从零开始"）。选择工作区。
2. **启用 Socket Mode**（Settings → Socket Mode）。生成具有 `connections:write` 权限的 **应用级令牌**。这就是 `xapp-*` 令牌。
3. **配置事件订阅**（Features → Event Subscriptions）。订阅 `message.channels`、`message.im` 或其他机器人应听的频道作用域。你**不**需要 Request URL，因为 Socket Mode 通过 socket 投递事件。
4. **添加机器人作用域**（Features → OAuth & Permissions）。最小：`chat:write`。根据事件订阅追加 `im:history`、`channels:history`、`groups:history` 或 `mpim:history`。
5. **将应用安装到工作区。** 安装页面会返回 `xoxb-*` 机器人令牌。
6. **可选地记录机器人自身的用户 ID**（以 `U…` 开头）。这是 rousseau 用于防止自身消息循环的值。

## 配置

```yaml
slack:
  app_token: "xapp-1-A0..."
  bot_token: "xoxb-1234..."
  bot_user_id: "U0123ABCD"
  reply_header: ""
  allowlist:
    - "U0ALICE"
    - "U0BOB"
```

| 字段 | 默认值 | 作用 |
|---|---|---|
| `app_token` | *必填* | 具有 `connections:write` 权限的 `xapp-*` 应用级令牌。 |
| `bot_token` | *必填* | 具有 `chat:write` 权限的 `xoxb-*` 机器人令牌。 |
| `bot_user_id` | *空* | 机器人用户的 `U…` ID，用于防止自身消息循环。可选；回退到检查 `bot_id` 字段。 |
| `reply_header` | *空* | 附加到每条出站消息前。 |
| `allowlist` | `[]` | 允许处理其消息的 Slack 用户 ID。 |

## 命令行

```sh
rousseau slack \
  --app-token xapp-... \
  --bot-token xoxb-... \
  --bot-user-id U0123ABCD
```

## 线协议格式

- **入站。** Slack 通过 WebSocket 发送 JSON 信封。rousseau 对信封 ACK、提取消息文本与发送者，然后交给处理器。
- **出站。** `POST https://slack.com/api/chat.postMessage`，负载 `{"channel": "<id>", "text": "…"}`，`Authorization: Bearer <bot_token>`。

## OAuth 作用域解读

每个作用域都授予特定的 API 面。rousseau 所需的作用域，以及缺失时会出问题的项：

| 作用域 | 使用的端点 | 缺失时的影响 |
|---|---|---|
| `connections:write` | `apps.connections.open`（Socket Mode WebSocket） | 无法打开 socket。**必需。** |
| `chat:write` | `chat.postMessage` | 无法回复任何消息。**必需。** |
| `im:history` | 用于 DM 的 `conversations.history`（通过事件间接） | 机器人在事件中看不到 DM 内容。 |
| `im:read` | `im.list`、DM 元数据 | 无法列出打开的 DM。 |
| `im:write` | `conversations.open` | 无法打开新 DM（仅当希望机器人主动 DM 某人时相关）。 |
| `mpim:history`、`channels:history`、`groups:history` | 多方 IM / 频道 / 私有频道 | 机器人看不到 DM 以外的消息内容。 |

在 *OAuth &amp; Permissions &gt; Bot Token Scopes* 下设置作用域。只添加你确实需要的作用域——Slack 在安装时会对每个作用域给出警告，用户更愿意安装权限面较窄的机器人。

## 自身消息循环预防

没有保护时，回复消息的机器人也会把自己的回复作为入站事件看到——导致失控循环。Rousseau 通过 `bot_user_id` 处理：

```go
// 简化——实际逻辑在 internal/transport/slack/client.go 中
if msg.User == cfg.BotUserID {
    continue // 跳过：这是我们自己的出站消息回响。
}
```

一次性获取机器人用户 ID：

```sh
curl -H "Authorization: Bearer xoxb-your-token" \
  https://slack.com/api/auth.test
```

响应包含 `user_id`。将其粘贴到配置中的 `slack.bot_user_id`，或通过 `--bot-user-id` 传入。

<aside class="admonition" data-type="warning"><span class="admonition-title">回退式循环预防</span><p>即使不设置 <code>bot_user_id</code>，传输也会忽略 <code>bot_message</code> 子类型事件。但仅依赖子类型比较脆弱——生产中请设置 <code>bot_user_id</code>。</p></aside>

## 线程

Slack 消息在作为线程回复时携带 `thread_ts`。当入站事件带有它时，rousseau 的出站调用也会包含 `thread_ts`，使机器人回复保持在同一线程。顶层消息仅在用户开启新线程时才成为新线程。

## 失败模式

| 症状 | 修复 |
|---|---|
| socket 打开时 `invalid_auth` | `app_token` 错误或缺少 `connections:write`。重新生成。 |
| 入站事件从未到达 | 请确认 **Event Subscriptions** 已启用且订阅了相关的 `message.*` 事件。 |
| 机器人回复自己的消息 | 在配置中设置 `bot_user_id`。 |
| 发送时 `not_in_channel` | 请把机器人邀请到频道（`/invite @rousseau-bot`）。 |
| DM 可用但频道不可用 | 缺少 `channels:history` 作用域，或机器人未被邀请到该频道。 |

## 故障排查

### socket 打开时 `invalid_auth`

`xapp-…` 令牌错误或作用域丢失。从 *Basic Information &gt; App-Level Tokens* 重新生成，并确保新令牌具有 `connections:write`。

### `chat.postMessage` 时 `not_authed`

机器人令牌（`xoxb-…`）缺失或错误。从 *OAuth &amp; Permissions &gt; Bot User OAuth Token* 重新生成。

### 事件到达但 rousseau 没有回复任何一个

检查允许列表。在 `pattern` 模式并设 `default: deny` 时，未列出的用户会被静默丢弃。请在日志中查找 `router.transport.rejected`。

### 出站时 `channel_not_found`

Slack 频道 ID（`C…`）已变——例如频道被归档并重建。请更新任何硬编码的频道 ID。Rousseau 通常使用入站事件中的频道，因此这仅在向固定频道进行 cron 投递时出现。

### 机器人在 Slack 中显示为离线

Socket Mode 每 ~30 秒空闲检查 WebSocket。若 Slack 显示机器人离线，请确认：(1) 守护进程运行中（`systemctl --user status`），(2) WebSocket 已连接（日志行 `slack.connected`），(3) 机器时钟在真实时间 30 秒内。

## 相关页面

- [快速入门：第一个传输](/zh-Hans/getting-started/first-transport/)——端到端演练。
- [配置](/zh-Hans/configuration/)——`slack` 配置块。
- [传输](/zh-Hans/transports/)——同类传输。
- [部署](/zh-Hans/deployment/)——在 Podman 容器中运行 Slack。
- [指南：审计与审批策略](/zh-Hans/guides/audit-approval-policies/)——用于共享 Slack 工作区的策略规则集。

## 延伸阅读

- `internal/transport/slack/client.go`——Socket Mode 连接、事件泵、`chat.postMessage`。
- `internal/cli/slack.go`——CLI 装配。
- `internal/transport/router.go`——允许列表强制执行。
- [Slack API 文档：Socket Mode](https://api.slack.com/apis/socket-mode)。
