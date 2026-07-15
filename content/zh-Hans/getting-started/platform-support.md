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
description: "Support matrix for rousseau-agent: operating systems, CPU architectures, container runtimes, provider authentication methods, transport backing libraries."
keywords: "platform support, os matrix, architecture, container runtime, provider auth, linux, macos, windows, arm64, amd64"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/getting-started/platform-support/"
subtitle: "OS, architectures, container runtimes, provider auth methods."
tags: "platform, support, matrix"
title: "平台支持"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "platform support, os matrix, architecture, container runtime, provider auth, linux, macos, windows, arm64, amd64"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "平台支持"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 23
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/getting-started/platform-support/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/platform-support/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "平台支持"
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
twitter_description: "Support matrix for rousseau-agent: operating systems, CPU architectures, container runtimes, provider authentication methods, transport backing libraries."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "平台支持"
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

## 操作系统

| 操作系统 | 支持等级 | 说明 |
|---|---|---|
| Linux（glibc，内核 5.10+） | Tier 1 | 每次推送 CI 都会运行 `ubuntu-latest`。参考部署目标。 |
| Linux（musl / Alpine） | Tier 1 | 容器镜像基于 Alpine。 |
| macOS 13+（Ventura 或更新） | Tier 1 | 每次推送 CI 都会运行 `macos-latest`。Bubble Tea TUI 已验证。 |
| Windows 10 / 11 | Tier 2 | 二进制会构建并发布，但 CI 不会在 Windows 上运行完整的 race matrix。聊天传输可工作；Podman + Quadlet 参考部署假定为 Linux。 |
| FreeBSD / OpenBSD | 尽力支持 | 纯 Go 构建，但没有 CI 任务。欢迎社区反馈。 |

## CPU 架构

| 架构 | 支持等级 | Release 命名 |
|---|---|---|
| `amd64`（x86-64） | Tier 1 | `_linux_amd64`、`_darwin_amd64`、`_windows_amd64` |
| `arm64`（aarch64） | Tier 1 | `_linux_arm64`、`_darwin_arm64`（Apple Silicon） |
| `armv7`（32 位 ARM） | 尽力支持 | 可通过 `GOARCH=arm GOARM=7` 构建；不发布。 |
| `riscv64` | 尽力支持 | 可通过 `GOARCH=riscv64` 构建；不发布。 |

在每个目标上 `CGO_ENABLED=0` —— `modernc.org/sqlite` 是纯 Go，因此交叉编译毫无摩擦。

## 容器运行时

| 运行时 | 支持等级 | 说明 |
|---|---|---|
| Podman 4.4+（rootless） | Tier 1 | 参考部署。使用 systemd Quadlet 单元进行声明式加固。 |
| Docker 24+ | Tier 1 | Dockerfile 无需修改即可工作。运行时加固由您负责（无 Quadlet 等价物）。 |
| containerd + `nerdctl` | Tier 2 | 同一镜像；nerdctl 消费同一 OCI 制品。 |
| Kubernetes 1.27+ | Tier 2 | 参见 [指南：Kubernetes 部署](/zh-Hans/guides/kubernetes-deployment/)。 |

## Provider 认证方式

| Provider | 认证机制 | 配置键 |
|---|---|---|
| `claudecli`（默认） | 继承 Claude Code 位于 `~/.claude/` 的 OAuth token。rousseau 配置中无密钥。 | `claudecli.binary`、`claudecli.permission_mode` |
| `anthropic` | 直接 API 密钥。 | `ANTHROPIC_API_KEY` 环境变量，或 `anthropic.api_key` |
| `openai` | OpenAI API 密钥或第三方 token。 | `OPENAI_API_KEY`，或 `openai.api_key` |
| `openrouter` | OpenRouter API 密钥。使用 OpenAI schema 并预设 `openrouter.base_url`。 | `openrouter.api_key` |
| `ollama` | 本地端点，无需密钥（`ollama.api_key` 默认 `not-required`）。 | `ollama.base_url` 预设为 `http://localhost:11434/v1` |
| `bedrock` | 标准 AWS 凭据链（环境变量、`~/.aws/credentials`、IMDS、IAM role）。 | `bedrock.region`、`bedrock.profile`、`bedrock.model` |
| `vertex` | GCP service account JSON，或 Application Default Credentials。 | `vertex.project`、`vertex.region`、`vertex.credentials_file` |

## 传输底层库

每种传输都是对上游客户端的薄适配器。支持受限于上游项目的可用性。

| 传输 | 上游 | 协议 |
|---|---|---|
| WhatsApp | `go.mau.fi/whatsmeow` | 非官方 WhatsApp Web 协议（Signal 兼容）。 |
| Signal | `signal-cli` 子进程 | Signal JSON-RPC。 |
| Telegram | 直接 Bot API 客户端 | 长轮询。 |
| Matrix | 直接 client-server API 客户端 | HTTPS 轮询。 |
| Slack | 直接 Socket Mode 客户端 | 出站 WebSocket。 |
| Discord | 直接 Gateway 客户端 | 出站 WebSocket + intents。 |
| iMessage | BlueBubbles HTTP 客户端 | BlueBubbles 轮询。需要运行 BlueBubbles Server 的 macOS 宿主。 |
| Email | 标准 `net/smtp` + IMAP 客户端 | 基于 TLS 的 IMAP + SMTP。 |
| SMS | 直接 Twilio / Vonage REST | 仅出站。 |

## 可选运行时依赖

| 依赖 | 用途 | 版本 |
|---|---|---|
| `claude` CLI | `provider: claudecli`（默认）。 | 最新。 |
| `signal-cli` | Signal 传输。 | 0.13+。需要 JVM。 |
| BlueBubbles Server | iMessage 传输。 | 1.9+。运行在 macOS 宿主。 |
| `whisper.cpp` CLI | WhatsApp 语音笔记转写（`whatsapp.voice.enabled: true`）。 | 1.5+。容器镜像中未包含。 |
| `podman` | 参考部署。 | 4.4+ 以支持 Quadlet。 |
| `systemd`（用户会话） | 参考部署。 | 249+ 以支持 Quadlet。 |

## 编译器与工具链

| 组件 | 版本 | 说明 |
|---|---|---|
| Go | 1.26+ | `go.mod` 精确锁定模块图。 |
| golangci-lint | v2 | 18 个 linter，精确 pin 位于 `.golangci.yml`。 |
| govulncheck | 最新 | 在每次 CI 构建时运行。 |
| cosign | 2.2+ | 仅用于校验已签名的 release。 |

## 下一步

- [安装](/zh-Hans/getting-started/installation/) —— 按您的平台安装。
- [更新](/zh-Hans/getting-started/updating/) —— 在版本间安全迁移。
