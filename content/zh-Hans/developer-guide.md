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
description: "Landing page for the rousseau-agent developer guide: architecture, how to add a transport, provider, or tool, testing pattern, contributing."
keywords: "developer guide, architecture, add transport, add provider, add tool, testing, contributing"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/developer-guide/"
subtitle: "架构、扩展点、测试与贡献。"
tags: "developer-guide, architecture, extend"
title: "开发者指南"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "developer guide, architecture, add transport, add provider, add tool, testing, contributing"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "开发者指南"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 60
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/developer-guide/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "开发者指南"
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
twitter_description: "Landing page for the rousseau-agent developer guide: architecture, how to add a transport, provider, or tool, testing pattern, contributing."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "开发者指南"
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

## 面向贡献者与集成者

开发者指南涵盖修改 rousseau 或将其代理循环嵌入到您自己二进制中所需的一切。如果您只想运行 rousseau，请改读 [用户指南](/zh-Hans/user-guide/cli/)。

## 页面

| 页面 | 主题 |
|---|---|
| [架构](/zh-Hans/developer-guide/architecture/) | 分层架构：agent、provider、tools、transport、cli。模块边界。 |
| [添加传输](/zh-Hans/developer-guide/add-a-transport/) | 实现 `transport.Transport` 并将其注册到 CLI 中。 |
| [添加 provider](/zh-Hans/developer-guide/add-a-provider/) | 实现 `agent.Provider`（以及可选的 `agent.StreamingProvider`）。 |
| [添加工具](/zh-Hans/developer-guide/add-a-tool/) | 实现 `tools.Tool` 并接线到 registry。 |
| [测试](/zh-Hans/developer-guide/testing/) | 通过接口进行依赖注入、fake 生成器、覆盖率阈值。 |
| [贡献](/zh-Hans/developer-guide/contributing/) | PR 清单、提交风格、质量门禁。 |

## 仓库布局

```
cmd/rousseau/                 Entry point (signal handling + Execute)
internal/agent/               Session, Message, Turn, agent loop, Provider interfaces, compression
internal/cli/                 Cobra command tree (chat, per-transport commands, doctor, status, cron, mcp, skills, init, version)
internal/config/              Viper-based; flag > env > file > default precedence
internal/cron/                robfig/cron/v3 scheduler goroutine with durable job storage
internal/llm/anthropic/       Direct Anthropic API provider with cache markers
internal/llm/bedrock/         AWS Bedrock provider
internal/llm/claudecli/       Subprocess provider (claude CLI + JSON parser)
internal/llm/openai/          OpenAI-compatible provider
internal/llm/vertex/          Google Vertex AI provider
internal/mcp/                 MCP server (JSON-RPC 2.0 over stdio, spec 2024-11-05)
internal/skills/              agentskills.io-style skill loader + composition
internal/state/               Store interface + Summary type
internal/state/sqlite/        SQLite implementation (WAL, JIDMap, claude cache, FTS5 recall, cron table)
internal/tools/               Tool interface + concurrency-safe Registry
internal/tools/builtin/       read, write, edit, grep, bash
internal/transport/           Transport interface + Router
internal/transport/{whatsapp,signal,telegram,matrix,slack,discord,sms,imessage,email}/
                              Nine transport adapters
internal/tui/                 Bubble Tea model
docker/                       Dockerfile, Podman Quadlet unit
docs/                         Roadmap, gap analysis
examples/embed-agent/         Minimal library-embedding example
```

## 依赖方向

`agent` 仅依赖于 `tools` 暴露的接口、其自身的 `Provider` 类型以及标准库。具体的 provider、store 和 transport 依赖 `agent` —— 反过来则绝对不会。

这由约定与 CI lint 门禁强制执行。若您发现自己需要从 `agent` 中导入某个具体 provider，说明您正在做分层不允许的事情；请退回一步。

## 质量门禁

每次提交都必须在本地与 CI 中通过：

- `go vet ./...`
- `golangci-lint run`（18 个 linter，精确 pin 位于 `.golangci.yml`）
- `go test -race -count=1 -covermode=atomic ./...`，在 Linux 与 macOS 上
- 覆盖率底线（当前整体 75%；核心 package 位于 85–100%）
- `govulncheck ./...`
- CodeQL 静态分析（Go）
- 可复现构建校验

使用 `make check` 在本地运行门禁。

## 下一步

- [架构](/zh-Hans/developer-guide/architecture/) —— 地图。
- [贡献](/zh-Hans/developer-guide/contributing/) —— 流程。
