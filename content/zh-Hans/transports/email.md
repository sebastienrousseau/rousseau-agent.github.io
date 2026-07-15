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
description: "Set up rousseau-agent's email transport: IMAP inbound polling, SMTP submission, both over full TLS, PlainAuth on 587, UTF-8 RFC 5322 output."
keywords: "email, IMAP, SMTP, TLS, PlainAuth, INBOX, poll interval, RFC 5322, UTF-8"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/transports/email/"
subtitle: "IMAP inbound plus SMTP outbound over TLS."
tags: "transports, email"
title: "电子邮件传输"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "email, IMAP, SMTP, TLS, PlainAuth, INBOX, poll interval, RFC 5322, UTF-8"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "电子邮件传输"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 20
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/transports/email/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/email/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "电子邮件传输"
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
twitter_description: "Set up rousseau-agent's email transport: IMAP inbound polling, SMTP submission, both over full TLS, PlainAuth on 587, UTF-8 RFC 5322 output."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "电子邮件传输"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">你将学到</span><p>Gmail 应用密码演练、如何为 Fastmail / Google Workspace / 自托管邮件服务器配置传输、从仅支持 STARTTLS 的服务器迁移的路径，以及纯文本 vs HTML 渲染的取舍。请对照阅读 <code>internal/transport/email/client.go</code>。</p></aside>

## 概述

邮件传输（`internal/transport/email/`）是一对：**IMAP 入站**（通过 `github.com/emersion/go-imap/v2`）与 **SMTP 出站**（通过 Go 标准库 `net/smtp`）。

它轮询 INBOX 中的 `UNSEEN` 消息，交给处理器后将其标记为 `SEEN`，并通过 `net/smtp.SendMail` 回复。

## TLS 姿态

**两端均为完全 TLS。** 传输在 IMAP 侧使用 `imapclient.DialTLS`，在 SMTP 侧使用 `smtp.SendMail` 配合已封装 TLS 的连接上的 `PlainAuth`。目前**不支持**仅 STARTTLS 的 IMAP 或 SMTP 服务器——守护进程拒绝在未加密 socket 上发送明文凭证。

标准 TLS 端口：

- IMAP：`993`
- SMTP 提交：`465`（隐式 TLS）——完全 TLS。**除非你的提供方在 587 上也提供隐式 TLS，否则不要使用 `587`。**

一些提供方（Google Workspace、Fastmail）在 `465` 上以隐式 TLS 接受 SMTP 提交。请在配置前确认你的提供方。

## 配置

```yaml
email:
  imap_addr: "imap.example.com:993"
  imap_username: "bot@example.com"
  imap_password: "..."
  mailbox: "INBOX"
  poll_interval: "30s"

  smtp_addr: "smtp.example.com:465"
  smtp_username: "bot@example.com"
  smtp_password: "..."

  from: "bot@example.com"
  reply_header: ""
```

| 字段 | 默认值 | 作用 |
|---|---|---|
| `imap_addr` | *必填* | 用于 TLS IMAP 的 `host:port`。 |
| `imap_username` | *必填* | IMAP 用户名。 |
| `imap_password` | *必填* | IMAP 密码。 |
| `mailbox` | `INBOX` | 要轮询的邮箱。 |
| `poll_interval` | `30s` | 查找 UNSEEN 邮件的频率。 |
| `smtp_addr` | *必填* | 用于 SMTP 提交的 `host:port`。 |
| `smtp_username` | *必填* | SMTP 用户名。 |
| `smtp_password` | *必填* | SMTP 密码。 |
| `from` | *必填* | 信封 + 首部 `From` 地址。 |
| `reply_header` | *空* | 附加到每条出站消息正文前。 |

## 命令行

```sh
rousseau email \
  --imap-addr imap.example.com:993 \
  --imap-username bot@example.com \
  --imap-password ... \
  --smtp-addr smtp.example.com:465 \
  --smtp-username bot@example.com \
  --smtp-password ... \
  --from bot@example.com
```

## 出站消息结构

回复符合 RFC 5322。rousseau 写入：

```
From: bot@example.com
To: sender@example.com
Subject: Re: <inbound subject>
Content-Type: text/plain; charset=utf-8
MIME-Version: 1.0

<reply_header><body>
```

UTF-8 是无条件的。HTML 输出不在范围内；未接入模板引擎。

## 入站消息结构

`UNSEEN` 消息被解析为 `IncomingMessage`，其中：

- `From` = 解析后的 `From` 首部地址。
- `Body` = 拼接后的 `text/plain` 部分。
- `At` = 来自 IMAP 的 `INTERNALDATE`。

附件、`text/html` 和内嵌图片会被忽略。

## 邮箱选择

`mailbox: "INBOX"` 是默认值。可指向 Gmail 标签（`"[Gmail]/label"`）或 Fastmail 文件夹以做更细的筛选——IMAP 服务器暴露的任何位置都可用。

## 提供方专属设置

<div class="tabs" data-tabs="email-provider">
  <div class="tab-list" role="tablist" aria-label="Email provider">
    <button role="tab" aria-selected="true">Gmail / Workspace</button>
    <button role="tab" aria-selected="false">Fastmail</button>
    <button role="tab" aria-selected="false">Outlook / M365</button>
    <button role="tab" aria-selected="false">自托管</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**Gmail 应用密码演练。** 启用 2FA 后，常规 Gmail 密码无法通过 IMAP/SMTP 认证。请生成应用密码：

1. 访问 https://myaccount.google.com/security 。确认 **两步验证** 已开启。
2. 点击 **应用密码**（仅在启用 2FA 时可见）。
3. 将应用命名为 "rousseau-agent"，生成。复制 16 字符密码（空格可选）。

配置：

```yaml
email:
  imap_addr: imap.gmail.com:993
  imap_username: your.address@gmail.com
  imap_password: "aaaa bbbb cccc dddd"

  smtp_addr: smtp.gmail.com:465
  smtp_username: your.address@gmail.com
  smtp_password: "aaaa bbbb cccc dddd"

  from: your.address@gmail.com
```

<aside class="admonition" data-type="warning"><span class="admonition-title">Google Workspace 管理员锁定</span><p>某些 Workspace 管理员在组织范围内禁用应用密码。如果你的安全页面缺少 <em>应用密码</em>，请让管理员允许"不太安全的应用访问权限"或配置 OAuth——rousseau 尚不支持 Gmail OAuth（路线图中）。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Fastmail 在 *Settings &gt; Password &amp; Security &gt; App passwords* 支持应用密码。创建作用域为 *Mail (IMAP/POP/SMTP)* 的密码：

```yaml
email:
  imap_addr: imap.fastmail.com:993
  imap_username: your.address@fastmail.com
  imap_password: "..."

  smtp_addr: smtp.fastmail.com:465
  smtp_username: your.address@fastmail.com
  smtp_password: "..."

  from: your.address@fastmail.com
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Microsoft 365 已对大多数租户弃用基本认证（用户名 + 密码）。Rousseau 尚不支持 Modern Auth / OAuth（路线图中）。选项：

1. 在 M365 管理中心按邮箱启用 *Authenticated SMTP*（部分租户可行）。
2. 使用中继：让 rousseau 对接自托管 IMAP+SMTP，后者通过 SMTP 加应用密码转发到 M365。
3. 等待 OAuth 支持落地。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

任何在 993 上以 TLS 承载 IMAP、并在 465 上以隐式 TLS 承载 SMTP 提交的自托管邮件服务器都可开箱即用。Postfix + Dovecot 加上 465 端口的 `smtpd_tls_wrappermode=yes` 是经典配置。

```yaml
email:
  imap_addr: mail.internal:993
  imap_username: rousseau
  imap_password: "..."

  smtp_addr: mail.internal:465
  smtp_username: rousseau
  smtp_password: "..."

  from: rousseau@internal
```

若你的服务器仅支持 STARTTLS（587 端口 SMTP 提交），rousseau 会拒绝认证——传输不发送明文凭证。参见下方迁移章节。

  </div>
</div>

## 从仅 STARTTLS 服务器迁移

Rousseau 在 IMAP（993）和 SMTP（465）上均使用隐式 TLS。若你现有的邮件基础设施仅在 143（IMAP）或 587（SMTP 提交）上提供 STARTTLS，你有三种选项：

1. **在你的服务器上启用隐式 TLS。** Postfix 支持将 `smtpd_tls_wrappermode=yes` 绑定到 465 端口。Dovecot 开箱即用地支持 993 端口上的 `imaps` 服务。
2. **在服务器前放置 TLS 终止代理。** `stunnel` 可以在 465 上接受隐式 TLS，并在 587 上以 STARTTLS 转发。
3. **等待 STARTTLS 支持。** 路线图项；参见 `docs/GAP_ANALYSIS_2026.md`。

## 纯文本 vs HTML 渲染

出站为 `text/plain; charset=utf-8`。无 HTML 模板。这是刻意为之——纯文本可通用渲染，不嵌入跟踪像素，且在纯文本邮件客户端中永不失败。若你希望 HTML 输出，请封装传输并重写 `SendMail`：

```go
// 发出 multipart/alternative 的自定义传输。
type MyEmailClient struct{ email.Client }

func (c *MyEmailClient) Deliver(ctx context.Context, to, body string) error {
    html := markdown.ToHTML([]byte(body), nil, nil)
    // ... 构造 multipart/alternative 消息，调用 net/smtp.SendMail ...
}
```

Rousseau 的核心保持纯文本；HTML 是调用方的关切点。

## 失败模式

| 症状 | 修复 |
|---|---|
| `imapclient.DialTLS` 错误 | 确认 993 端口出站可通，TLS 证书有效。 |
| `SMTP AUTH failed` | `PlainAuth` 要求认证服务器主机名与 `smtp_addr` 匹配。带负载均衡的提供方可能呈现不同名称。 |
| 消息未被标记为 SEEN | 处理器返回错误。请解决根本问题；rousseau 不会无限重试。 |
| 回复重复 | 两个 rousseau 实例针对同一邮箱运行；只应运行一个。 |
| `AUTHENTICATE failed: Application-specific password required` | Gmail 启用了 2FA，却使用了账户密码而非应用密码。参见上文 Gmail 演练。 |

## 故障排查

### `dial tcp: connect: connection refused`

端口错误。请确保 `imap_addr` 使用 `:993`（而非 `:143`），`smtp_addr` 使用 `:465`（而非仅 STARTTLS 服务器的 `:587`）。

### 机器人回复垃圾邮件

INBOX 中任何 `UNSEEN` 消息都会被处理。请在邮箱层面过滤垃圾邮件（服务器端规则、Gmail 垃圾邮件过滤器），或配置一个不同于 INBOX 的 `mailbox:` 并用服务器端规则将邮件路由至其中。

### `SendMail` 成功但消息从未到达

检查 SMTP 服务器的邮件日志。常见原因：DKIM 签名失败（`From:` 域与服务器可签署的域不匹配）、反向 DNS 不匹配、接收方域的 SPF 阻止你的 IP。

### 消息正文中的 Unicode 显示为 `?????`

路径上某处剥离了 UTF-8。请确认发送消息中包含 `Content-Type: text/plain; charset=utf-8`（rousseau 总是设置它），并且没有中继在转码。

### 修改配置后 poll 仍需数秒

`poll_interval` 仅在守护进程启动时读取。请重启以获取新值。

## 相关页面

- [快速入门：第一个传输](/zh-Hans/getting-started/first-transport/)——端到端演练。
- [配置](/zh-Hans/configuration/)——`email` 配置块。
- [传输](/zh-Hans/transports/)——同类传输。
- [部署](/zh-Hans/deployment/)——在 Podman 容器中运行 Email。
- [Cron](/zh-Hans/cron/)——通过邮件发送定时摘要。

## 延伸阅读

- `internal/transport/email/client.go`——IMAP 轮询、SMTP 发送、消息解析。
- `internal/cli/email.go`——CLI 装配。
- `internal/config/config.go`——`EmailConfig` 结构体。
- [emersion/go-imap 文档](https://github.com/emersion/go-imap)——IMAP 库。
