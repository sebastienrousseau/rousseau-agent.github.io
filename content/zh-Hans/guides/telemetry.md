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
description: "Rousseau-agent ships zero telemetry. No analytics endpoint, no crash-report upload, no license server, no unique identifiers."
keywords: "telemetry, privacy, no phone home, no analytics, no license server"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/guides/telemetry/"
subtitle: "零埋点、零回传，可自行核验。"
tags: "guides, telemetry, privacy, security"
title: "指南：遥测"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "telemetry, privacy, no phone home, no analytics, no license server"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "指南：遥测"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 40
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/guides/telemetry/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/telemetry/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "指南：遥测"
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
twitter_description: "Rousseau-agent ships zero telemetry. No analytics endpoint, no crash-report upload, no license server, no unique identifiers."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "指南：遥测"
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

## 承诺

Rousseau-agent 提供零遥测。rousseau 明确**不**做的事情清单：

- 无分析端点。没有 `metrics.rousseau-agent.dev` 或等价物。
- 无崩溃报告上传。panic 落入 stderr；没有任何东西上传到任何地方。
- 无 license 服务器。没有周期性签到，也没有座位校验。
- 无唯一安装标识。同一 tag 的每次安装二进制文件按字节相同。
- 无 feature-flag 服务。rousseau 中的每个开关都在 `config.yaml` 或 CLI flag 中。
- 无更新 ping。`rousseau version` 是本地查询；没有"检查更新"的往返。

## 如何验证

rousseau 二进制是开源的（MIT，见 `LICENSE`）。每一个网络调用都可 grep：

```sh
grep -rn 'http.Get\|http.Post\|http.Client\|http.NewRequest\|net/http' \
  /path/to/rousseau-agent/internal/ | head
```

每次命中都落到以下类别之一：

| 包 | 用途 |
|---|---|
| `internal/llm/anthropic/` | Anthropic API 调用（通过官方 SDK）。 |
| `internal/llm/openai/` | OpenAI 兼容端点调用。 |
| `internal/transport/telegram/` | Telegram Bot API。 |
| `internal/transport/matrix/` | Matrix 客户端-服务端 API。 |
| `internal/transport/whatsapp/` | 到 Meta 的 whatsmeow websocket。 |
| `internal/transport/slack/`、`discord/` | Socket Mode / Discord Gateway。 |
| `internal/transport/imessage/` | BlueBubbles 服务器（在您的 LAN 上）。 |
| `internal/transport/sms/` | Twilio / Vonage。 |
| `internal/transport/email/` | IMAP + SMTP。 |

它们没有一个是分析端点。每一个要么是您配置的 LLM provider，要么是您启用的传输。

在 `strace -e network` 下运行守护进程，或用 `ss -tanp` 观察 —— 您会看到的唯一 socket 就是通向以上端点。

## 结构化日志是本地的

Rousseau 使用 `log/slog`（`internal/cli/root.go`）。默认处理器写入 stderr，在 Quadlet 单元下会落入 systemd journal。没有任何东西流出主机。如果您想把日志转运到 Loki、Datadog 或其他地方，您自己配置该管道 —— 见 [指南：可观测性](/zh-Hans/guides/observability/)。

## 对比

| 产品 | 分析 | 崩溃上传 | License 服务器 |
|---|---|---|---|
| rousseau-agent | 无 | 无 | 无 |
| 供应商 A（典型 SaaS 编码助手） | 有 | 有 | 有 |
| 供应商 B（托管控制面） | 有 | 可选退出 | 有 |

Rousseau 的运营模型是：您提供 LLM key，您托管守护进程。没有任何一部分 rousseau 运行在 Sebastien 控制的服务器上。

## rousseau 会向 LLM provider 发送什么

按定义，当您通过 Anthropic、Bedrock、Vertex、OpenAI 或任何其他 API 路由消息时，该 provider 会看到消息内容。这是 LLM 推理工作方式的固有特性 —— rousseau 是客户端，而不是垫片。

如果 provider 的数据处理对您重要，两个缓解措施：

1. **对着自托管模型运行。** Ollama、vLLM、LM Studio 或任何 OpenAI 兼容端点。没有任何东西离开您的机器。见 [指南：自托管 vLLM](/zh-Hans/guides/self-hosted-vllm/)。
2. **在带数据处理附录的区域使用 Bedrock 或 Vertex。** AWS 与 GCP 都发布按区域的数据驻留保证。

## WhatsApp 桥看到什么

whatsmeow 实现的非官方 WhatsApp Web 协议与 Meta 的服务器通信 —— 该流量在 rousseau 控制之外。Meta 看到您消息的方式与您从浏览器使用 WhatsApp Web 时相同。如果 Meta 看到您的消息不可接受，请不要运行 WhatsApp 桥。

whatsmeow 客户端可公开审计 —— 每个数据包都有文档；上面没有 rousseau 特定的网络调用叠加。

## 相关

- [安全](/zh-Hans/security/) —— 信任边界与审计姿态。
- [隐私](/zh-Hans/privacy/) —— 站点级隐私姿态。
- [Providers：OpenAI 兼容](/zh-Hans/providers/openai-compatible/) —— 自托管推理。
- [指南：自托管 vLLM](/zh-Hans/guides/self-hosted-vllm/) —— 可行示例。
