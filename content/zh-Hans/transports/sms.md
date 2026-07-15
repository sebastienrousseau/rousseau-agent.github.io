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
description: "rousseau-agent's SMS transport is send-only. Twilio (account_sid + auth_token) or Vonage (api_key + auth_token). Inbound not supported because it requires a public webhook."
keywords: "SMS, Twilio, Vonage, Nexmo, send-only, Messaging Service SID, E.164, no webhook"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/transports/sms/"
subtitle: "Send-only SMS via Twilio or Vonage."
tags: "transports, SMS"
title: "SMS 传输"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "SMS, Twilio, Vonage, Nexmo, send-only, Messaging Service SID, E.164, no webhook"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "SMS 传输"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 19
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/transports/sms/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/sms/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "SMS 传输"
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
twitter_description: "rousseau-agent's SMS transport is send-only. Twilio (account_sid + auth_token) or Vonage (api_key + auth_token). Inbound not supported because it requires a public webhook."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "SMS 传输"
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

## 设计上仅支持发送

SMS 传输是**仅发送**的。入站 SMS 需要一个由运营商 POST 请求的公开 HTTP webhook —— 这与 rousseau 的零入站接口理念直接冲突。如果你的用例需要接收 SMS，请在 rousseau 旁边运行一个专用的 webhook 接收器，并通过 cron 调度器或 agent-loop 嵌入 API 路由消息。

`Start` 被实现为一个阻塞在 `ctx.Done()` 上的 no-op，因此该传输仍可套入标准的守护进程布线结构。

## 支持的运营商

| 运营商 | 配置 `provider` | 必填字段 |
|---|---|---|
| Twilio | `twilio` | `from`、`account_sid`、`auth_token` |
| Vonage（原 Nexmo） | `vonage` | `from`、`api_key`、`auth_token`（即 API secret） |

## Twilio 配置

```yaml
sms:
  provider: twilio
  from: "+15550000000"
  account_sid: "AC..."
  auth_token: "..."
```

`from` 既可以是 E.164 发件号码，也可以是 **Twilio Messaging Service SID**（以 `MG…` 开头）。Messaging Services 处理号码池管理、粘性发件人路由和基于地理位置的发件人选择 —— 对超出单国流量的场景推荐使用。

`base_url` 默认为 `https://api.twilio.com/2010-04-01`，仅在使用区域端点或测试时才需要覆盖。

## Vonage 配置

```yaml
sms:
  provider: vonage
  from: "+15550000000"
  api_key: "abcd1234"
  auth_token: "efgh5678"
```

Vonage 配置中的 `auth_token` 对应 Vonage 的 **API secret**，而不是他们的 JWT 签名密钥 —— Vonage 使用简单的 key/secret 对来鉴权 SMS 提交。

`base_url` 默认为 `https://rest.nexmo.com`。

## 命令行

```sh
# Twilio
rousseau sms \
  --provider twilio \
  --from '+15550000000' \
  --account-sid AC... \
  --auth-token ...

# Vonage
rousseau sms \
  --provider vonage \
  --from '+15550000000' \
  --api-key abcd1234 \
  --auth-token efgh5678
```

由于没有入站方向，`--allow` 不适用。

## 投递 API

两个供应商均使用各自的 REST 端点：

- **Twilio。** `POST /2010-04-01/Accounts/{sid}/Messages.json`，使用 SID/token 的 basic-auth。
- **Vonage。** `POST /sms/json`，请求体中带 `api_key` + `api_secret`。

返回的消息 ID 会被记录；投递状态 webhook **不会**被消费（同样，因为不暴露公开 HTTP 接口）。

## E.164 格式

`from` 与目标号码必须使用 E.164 格式（`+<country><subscriber>`）。不含空格，不含短横线。Twilio Messaging Service SID 仅在 `from` 字段绕过此要求。

## 成本管理

- 在你的供应商上激进地设置 `max_tokens` —— 单条 SMS 便宜，但如果模型生成较长回复，字节数会迅速累加（Twilio 对 GSM-7 每 160 字符分段，对 UCS-2 每 70 字符分段）。
- 考虑在把出站回复交给 SMS 传输之前先重写得简洁一些。合适的位置是 `agent.Options.SystemPrompt`。
