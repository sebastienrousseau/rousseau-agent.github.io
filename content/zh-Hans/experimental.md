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
description: "Off-by-default rousseau-agent behaviour: voice mode via whisper.cpp, FTS5 recall, LLM compression, and other opt-in surface."
keywords: "experimental, voice, whisper, fts5, compression, opt-in, feature flag"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/experimental/"
subtitle: "默认关闭的行为及其原因。"
tags: "experimental, opt-in, voice, compression, fts5"
title: "实验特性"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "experimental, voice, whisper, fts5, compression, opt-in, feature flag"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "实验特性"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "system"
order: 60
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/experimental/index.html"
item_link: "https://docs.rousseau-agent.dev/experimental/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "实验特性"
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
twitter_description: "Off-by-default rousseau-agent behaviour: voice mode via whisper.cpp, FTS5 recall, LLM compression, and other opt-in surface."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "实验特性"
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

## 这里的"实验性"意味着什么

Rousseau 的默认姿态是极简的：一个静态 Go 二进制、一个 SQLite 文件、没有外部依赖。任何需要额外运行时（`whisper.cpp`）、额外状态（用于召回的 FTS5 索引）或额外 provider 成本（基于 LLM 的压缩）的特性都是选择性开启的。

它们都不是不稳定的。它们已发布、有测试、受支持。但因为它们改变了运维成本或接触面，所以默认关闭 —— 您只开启需要的那些。

## 语音模式（whisper.cpp）

默认关闭，因为它需要在守护进程宿主上安装来自 whisper.cpp 的 `whisper` 二进制。

**开关：** 在 `config.yaml` 中设置 `whatsapp.voice.enabled: true`。参见 `internal/config/config.go` 中的 `VoiceConfig`。

**它做什么。** 当 WhatsApp 送达语音笔记时，whatsmeow 客户端下载 OGG 负载，使用配置的模型调用 `whisper`，并将转写文本视为入站消息文本。结构化日志事件（`internal/transport/whatsapp/dispatch.go`）：

- `whatsapp.audio_downloaded size=N`
- `whatsapp.transcribed elapsed=N`

**为何关闭。** 两个原因：（1）在 `whisper` 二进制缺失时，全新安装会以令人困惑的方式失败；（2）转写是实时的 CPU 开销，大多数运维者宁愿主动开启也不愿被意外。

完整安装参见 [用户指南：语音模式](/zh-Hans/user-guide/voice-mode/)。

## FTS5 召回

**开关。** 默认开启，但仅由请求它的工具使用。无论如何 FTS5 索引都会被构建和维护（`internal/state/sqlite/search.go` 中的 `EnsureSearch`）；"选择性开启"指的是代理是否让模型去搜索它。

**它做什么。** 对每个已存储会话建立 SQLite FTS5 全文索引。通过 `rousseau session search`、MCP 工具 `rousseau_search_sessions` 供能；（当代理配置了 recall searcher 时）模型可以在轮次中间对其发起查询。

**为何这样构造。** 索引的维护成本很低 —— 由 `internal/state/sqlite/search.go` 中的触发器处理 —— 但把它暴露给每一轮的模型是有成本的。它只在代理循环由 `RecallSearcher`（`internal/state/sqlite/recall.go`）构造时才接线。

参见 [用户指南：压缩 + 召回](/zh-Hans/user-guide/compression-recall/)。

## 基于 LLM 的压缩

默认关闭，因为它会消耗 token。

**开关：** `agent.compression.enabled: true`。字段完整列表见 [指南：上下文管理](/zh-Hans/guides/context-management/)。

**它做什么。** 当会话增长超过 `trigger_messages`（默认 60）时，`LLMCompressor`（`internal/agent/compressor.go`）会将最早的切片摘要为一条合成的用户消息，并逐字保留最新的 `keep_recent` 条消息。之后每一轮都更小、更便宜。

**为何关闭。** 参考部署使用订阅制的 `claudecli`，token 计数不计费。压缩在 Anthropic 直连、Bedrock、Vertex 和 OpenAI 兼容 provider 上会自负盈亏。

## OpenRouter 与 Ollama 基础 URL（预配置，仍是选择性开启）

严格说不算实验性，但值得点名：rousseau 在 `internal/config/config.go` 中的 `setDefaults` 预先配置了 OpenRouter 与 Ollama 的 base URL：

- `openrouter.base_url: https://openrouter.ai/api/v1`
- `ollama.base_url: http://localhost:11434/v1`
- `ollama.api_key: not-required`

选择这些 provider 通过 `provider: openrouter` / `provider: ollama` 进行开启 —— 端点只是被预先填好，让您不必记忆。

## 提示注入检测（路线图）

尚未发布。诚实的威胁模型参见 [指南：提示注入](/zh-Hans/guides/prompt-injection/)。目前的缓解完全基于审批器；基于分类器的检测是一个路线图项目，等待真正有效的研究成果。

## 到非 Anthropic provider 的流式（部分）

Anthropic provider（`internal/llm/anthropic/client.go`）支持 SDK 的流式接口。其他适配器目前以非流式模式运行。跨每个适配器的流式是一次计划中的一致化 pass。

## 相关

- [配置](/zh-Hans/configuration/) —— 每个配置旋钮。
- [用户指南：语音模式](/zh-Hans/user-guide/voice-mode/)。
- [指南：上下文管理](/zh-Hans/guides/context-management/) —— 压缩的深入解析。
- [参考：会话存储](/zh-Hans/reference/session-store/) —— FTS5 schema。
