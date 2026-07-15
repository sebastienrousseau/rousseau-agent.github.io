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
description: "Overview of rousseau-agent's nine chat transports: WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, Email, SMS. Every transport implements Start / Stop / Deliver."
keywords: "transports, WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, email, SMS"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/transports/"
subtitle: "同一个 Transport 接口背后的九种聊天传输。"
tags: "transports, overview"
title: "传输"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "transports, WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, email, SMS"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "传输"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 11
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/transports/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "传输"
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
twitter_description: "Overview of rousseau-agent's nine chat transports: WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, Email, SMS. Every transport implements Start / Stop / Deliver."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "传输"
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

## Transport 接口

每个传输都实现一个小接口（`internal/transport/transport.go`）：

```go
type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

传输之上是 `Router`，负责按发送者查找会话、执行允许列表检查，以及分发给 `Agent`。之下是传输特定的传线代码。

默认情况下，任何随附的传输都不会暴露公共 HTTP 面。这是一个刻意的姿态选择 —— rousseau 守护进程应可在 NAT 之后安全运行，无需端口转发规则。

## 支持的传输

| 传输 | 入站 | 出站 | 底层库 / 协议 | 认证 | 一行安装 |
|---|:---:|:---:|---|---|---|
| [WhatsApp](/zh-Hans/transports/whatsapp/) | 是 | 是 | `go.mau.fi/whatsmeow` | 设备配对（QR） | `rousseau whatsapp --allow <jid>` |
| [Signal](/zh-Hans/transports/signal/) | 是 | 是 | `signal-cli` JSON-RPC | 预注册账号 | `rousseau signal --account +447900123456` |
| [Telegram](/zh-Hans/transports/telegram/) | 是 | 是 | Bot API 长轮询 | BotFather token | `rousseau telegram --token <token>` |
| [Matrix](/zh-Hans/transports/matrix/) | 是 | 是 | Client-server API `/sync` | Access token | `rousseau matrix --homeserver-url … --access-token …` |
| [Slack](/zh-Hans/transports/slack/) | 是 | 是 | Socket Mode + Web API | `xapp-*` + `xoxb-*` | `rousseau slack --app-token … --bot-token …` |
| [Discord](/zh-Hans/transports/discord/) | 是 | 是 | Gateway v10 + REST | Bot token | `rousseau discord --token <token>` |
| [iMessage](/zh-Hans/transports/imessage/) | 是 | 是 | BlueBubbles HTTP 轮询 | 服务器密码 | `rousseau imessage --base-url … --password …` |
| [Email](/zh-Hans/transports/email/) | 是 | 是 | IMAP + SMTP | 用户名 + 密码 | `rousseau email --imap-addr … --smtp-addr …` |
| [SMS](/zh-Hans/transports/sms/) | 否 | 是 | Twilio 或 Vonage REST | Account SID / API key | `rousseau sms --provider twilio --account-sid … --auth-token …` |

## 为什么没有公共 HTTP 面

两项设计选择让所列的每个传输都与公共 webhook 保持距离：

- **基于 WebSocket 的入站。** 从守护进程视角来看，Slack Socket Mode 与 Discord Gateway 仅为出站 —— 守护进程通过 TLS 拨号到供应商，消息通过同一连接到达。
- **轮询。** WhatsApp、Telegram、Matrix、iMessage 和 email 按自己的节奏拉取更新。没有供应商调入的 webhook。

SMS 是例外，rousseau 将其做成 **仅发送** 来化解。入站 SMS 需要 Twilio / Vonage webhook，而这正是本项目拒绝引入的面。

## Router 行为

router（`internal/transport/router.go`）位于每个传输与 `Agent` 之间：

- **会话隔离。** 每一个不同的 `From` 值都获得自己的 `Session`，因此并行会话不会交叉污染。WhatsApp LID 身份首先会被规范化为电话 JID（见 `internal/transport/whatsapp/resolve.go`）。
- **允许列表。** 每个支持入站的传输在其配置中都有一个 `Allowlist []string`。为空表示"接受每个发送者" —— 对守护进程而言，您总是希望至少有一条条目。
- **分发。** router 按会话串行化轮次，因此用户无法堆叠两条并发的入站消息。

## 增加第十种传输

实现 `transport.Transport`（三个方法）。在 `internal/config/` 下新增一个镜像该块布局的 `Config` 类型。在 `internal/cli/` 中接线一个 CLI 命令。这就是全部接触面 —— 代理核心保持不变。

## 各传输专属页面

- [WhatsApp](/zh-Hans/transports/whatsapp/)
- [Signal](/zh-Hans/transports/signal/)
- [Telegram](/zh-Hans/transports/telegram/)
- [Matrix](/zh-Hans/transports/matrix/)
- [Slack](/zh-Hans/transports/slack/)
- [Discord](/zh-Hans/transports/discord/)
- [iMessage](/zh-Hans/transports/imessage/)
- [Email](/zh-Hans/transports/email/)
- [SMS](/zh-Hans/transports/sms/)
