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
description: "Overview of the five LLM provider families supported by rousseau-agent: claudecli, Anthropic, AWS Bedrock, Google Vertex AI, and any OpenAI-compatible endpoint."
keywords: "providers, LLM, Anthropic, Bedrock, Vertex, OpenAI, OpenRouter, Ollama, claudecli"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/providers/"
subtitle: "同一个 Provider 接口背后的五类 LLM 提供方。"
tags: "providers, LLM"
title: "提供方"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "providers, LLM, Anthropic, Bedrock, Vertex, OpenAI, OpenRouter, Ollama, claudecli"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "提供方"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 5
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/providers/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "提供方"
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
twitter_description: "Overview of the five LLM provider families supported by rousseau-agent: claudecli, Anthropic, AWS Bedrock, Google Vertex AI, and any OpenAI-compatible endpoint."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "提供方"
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

## Provider 接口

每个 LLM 后端都实现 `agent.Provider`：

```go
type Provider interface {
    Name() string
    Complete(ctx context.Context, req Request) (Response, error)
}
```

`StreamingProvider` 变体额外提供 `CompleteStream` 以支持逐 token 传输。新增第六个后端只需一个 `Complete` 实现，再加上在 `internal/cli/provider.go` 中的接线。

## 支持的家族

| Provider | 认证模型 | 端点 | 流式 | 提示缓存 | 推荐场景 |
|---|---|---|:---:|:---:|---|
| [claudecli](/zh-Hans/providers/claudecli/) | 继承 `claude` CLI 认证 | 本地子进程 | 是 | 通过子进程 | 个人运维者、订阅制 Claude Code |
| [Anthropic](/zh-Hans/providers/anthropic/) | `ANTHROPIC_API_KEY` | `api.anthropic.com` | 是 | ephemeral 标记 | 使用 Anthropic API 的团队 |
| [AWS Bedrock](/zh-Hans/providers/bedrock/) | AWS 凭据链 | `bedrock-runtime.<region>.amazonaws.com` | 是 | 通过 SDK | AWS 上的企业 |
| [Google Vertex AI](/zh-Hans/providers/vertex/) | Service account 或 ADC | `<region>-aiplatform.googleapis.com` | 是 | 通过 SDK | GCP 上的企业 |
| [OpenAI 兼容](/zh-Hans/providers/openai-compatible/) | Bearer token | `api.openai.com` 或自定义 | 是 | 依 provider 而定 | OpenAI、OpenRouter、Ollama、vLLM、LM Studio |

## 选择 provider

在 `~/.config/rousseau/config.yaml` 顶部设置 `provider` 键：

```yaml
provider: anthropic

anthropic:
  api_key: sk-ant-...
  model: claude-sonnet-4-6
```

或在 shell 中覆盖：

```sh
ROUSSEAU_PROVIDER=bedrock rousseau chat
```

`ANTHROPIC_API_KEY` 在加载时绑定到 `anthropic.api_key`，因此通过环境变量传入具有等价效果。

## 每个 provider 在何处进行工具调用

`claudecli` provider 在 `claude` 子进程内运行其自身的工具调用循环。为该 provider **不会** 调用注册在 rousseau `Registry` 上的工具；`Response` 始终是一条包含 claude 最终回答的、结束轮次的文本消息。

其他所有 provider（`anthropic`、`bedrock`、`vertex`、`openai`）使用 rousseau 的 `Registry`。工具定义会由各 provider 的 package 转换为该 provider 期望的 JSON 形态。
