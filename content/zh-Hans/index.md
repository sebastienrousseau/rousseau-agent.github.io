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
changefreq: "weekly"
description: "自托管的编码代理，支持 9 种聊天传输、5 类 LLM 提供方、MCP 服务器、SLSA-3 来源证明与 cosign 签名的发布。"
keywords: "rousseau-agent, coding agent, self-hosted, container-native, MCP, SLSA-3, cosign, SBOM, LLM, WhatsApp, Signal, Slack"
layout: "index"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/"
subtitle: "自托管、容器原生、MCP 原生的编码代理。"
tags: "overview, self-hosted, mcp, security"
title: "rousseau-agent"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "rousseau-agent, coding agent, self-hosted, container-native, MCP, SLSA-3, cosign, SBOM, LLM, WhatsApp, Signal, Slack"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "rousseau-agent"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "welcome"
order: 1
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/index.html"
item_link: "https://docs.rousseau-agent.dev/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "rousseau-agent"
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
twitter_description: "自托管的编码代理，支持 9 种聊天传输、5 类 LLM 提供方、MCP 服务器、SLSA-3 来源证明与 cosign 签名的发布。"
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "rousseau-agent"
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

## 自托管、容器原生、MCP 原生的编码代理

**rousseau-agent** 是一个用 Go 编写的编码助手，运行在你代码所在的位置。守护进程、认证凭据以及与模型之间的通信，全都留在运维方掌控的硬件上。**9 种传输 · 5 类 LLM 提供方 · SLSA-3 · cosign · SBOM。**

```sh
rousseau chat
```

这一条命令即可启动一个 Bubble Tea 编写的 TUI，背后接入你所配置的 LLM 提供方。除对提供方的调用本身外，没有任何数据会越出你的网络边界。

## 三大支柱

### 面向企业的加固

- 通过 `slsa-framework/slsa-github-generator` 提供 **SLSA 等级 3** 构建来源。
- 每个发布的 checksum 文件均带有 **cosign** 无密钥签名，可通过 Sigstore 透明日志验证。
- 每个版本随附 **CycloneDX** JSON SBOM。
- 在 CI 中基于干净 checkout 验证的 **可复现构建**。
- 无 root 权限的 Podman，配合 `ReadOnly=true`、`DropCapability=all`、`NoNewPrivileges=true`、默认 seccomp 过滤器、非 root UID 1000 与 `keep-id` 用户命名空间映射。
- 由 18 个 linter 组成的 `golangci-lint` v2 门禁、CodeQL（Go）、每次 CI 运行的 `govulncheck`，以及针对 `gomod` 与 `github-actions` 的 Dependabot。

### 多模态覆盖

一个守护进程背后运行九种聊天传输：

- [WhatsApp](/zh-Hans/transports/whatsapp/) （`go.mau.fi/whatsmeow`，兼容 Signal 协议）
- [Signal](/zh-Hans/transports/signal/) （`signal-cli` 的 JSON-RPC 子进程）
- [Telegram](/zh-Hans/transports/telegram/) （Bot API 长轮询）
- [Matrix](/zh-Hans/transports/matrix/) （客户端-服务器 API）
- [Slack](/zh-Hans/transports/slack/) （Socket Mode，无公开 HTTP 端点）
- [Discord](/zh-Hans/transports/discord/) （Gateway v10）
- [iMessage](/zh-Hans/transports/imessage/) （BlueBubbles 的 HTTP 轮询）
- [Email](/zh-Hans/transports/email/) （IMAP + SMTP）
- [SMS](/zh-Hans/transports/sms/) （Twilio 或 Vonage，仅发送）

### 模型无关

五类 LLM 提供方族，同一套 `agent.Provider` 接口：

- [claudecli](/zh-Hans/providers/claudecli/) —— 调用本地 `claude` CLI 的子进程，沿用其认证。
- [Anthropic](/zh-Hans/providers/anthropic/) —— 直连 API，带有临时的提示缓存标记。
- [AWS Bedrock](/zh-Hans/providers/bedrock/) —— 标准 AWS 凭据链。
- [Google Vertex AI](/zh-Hans/providers/vertex/) —— 服务账号 JSON 或 ADC。
- [OpenAI 兼容](/zh-Hans/providers/openai-compatible/) —— OpenAI、OpenRouter、Ollama、vLLM、LM Studio。

## 下一步

- [快速入门](/zh-Hans/getting-started/) —— 安装、首次运行与首个传输。
- [配置](/zh-Hans/configuration/) —— `internal/config/config.go` 中的每一个字段。
- [部署](/zh-Hans/deployment/) —— 无 root Podman + Quadlet，以及 Kubernetes 说明。
- [安全](/zh-Hans/security/) —— 供应链姿态、信任模型与 cosign 使用示例。
- [核心概念](/zh-Hans/concepts/) —— agent 循环、会话存储、MCP、cron 与技能。
