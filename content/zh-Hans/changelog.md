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
description: "Chronological release notes for rousseau-agent. First public snapshot: 9 transports, 5 providers, MCP server, SLSA-3, 76% coverage."
keywords: "changelog, release notes, versions, snapshot"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/changelog/"
subtitle: "rousseau-agent 的按时间顺序排列的发布说明。"
tags: "changelog, reference"
title: "变更日志"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "changelog, release notes, versions, snapshot"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "变更日志"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 28
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/changelog/index.html"
item_link: "https://docs.rousseau-agent.dev/changelog/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "变更日志"
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
twitter_description: "Chronological release notes for rousseau-agent. First public snapshot: 9 transports, 5 providers, MCP server, SLSA-3, 76% coverage."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "变更日志"
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

## 当前状态 —— 2026 年 7 月

首次公开快照。今日发布的亮点：

- **九种聊天传输。** WhatsApp、Signal、Telegram、Matrix、Slack、Discord、iMessage、Email、SMS。
- **五种 LLM provider。** claudecli、Anthropic 直连、AWS Bedrock、Google Vertex AI、OpenAI 兼容。
- **MCP 服务器。** 基于 stdio 的 JSON-RPC 2.0，规范版本 2024-11-05。
- **SLSA Level 3** 构建溯源、cosign 签名的 release checksums、CycloneDX SBOM。
- **模块整体 76% 测试覆盖率**（核心 package 位于 85–100%）。
- **零未处理的 Dependabot 告警。**
- **完整 race-mode CI**，在 `ubuntu-latest` 与 `macos-latest` 上执行。

## 详情

要查看逐次提交的完整历史，请查阅 https://github.com/sebastienrousseau/rousseau-agent 的 git log。

每次提交都使用 [Conventional Commits](https://www.conventionalcommits.org/)。首个打标签的 release 发布后，changelog 页面会呈现结构化条目；在此之前，`git log --oneline` 是权威参考。

## 兼容性策略

- **配置文件格式** 通过字段追加而非 schema 破坏来演进。新增键可以安全忽略；重命名与移除会在移除之前的一个 release 中先以弃用警告出现。
- **`agent.Provider`、`agent.Message`、`agent.Session`** 是面向第三方嵌入者的稳定导出。破坏性变更将随大版本号跃迁一同发布。
- **`internal/*` package** 不是稳定 API —— 它们是项目内部的。第三方消费者不应导入它们（Go 的 `internal` 可见性会强制这一点）。

## 反馈提交地址

- Bug 与功能请求：GitHub issues。
- 安全：`sebastian.rousseau@gmail.com`（见 [/security/](/zh-Hans/security/)）。
