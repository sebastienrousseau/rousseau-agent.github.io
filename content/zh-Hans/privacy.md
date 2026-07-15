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
description: "rousseau-agent is self-hosted. No telemetry endpoint, no SaaS control plane. LLM providers have their own retention policies; everything else stays in the operator's infrastructure."
keywords: "privacy, telemetry, self-hosted, data handling, retention, LLM providers"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/privacy/"
subtitle: "自托管即自控——除了对 LLM 的调用外，不会有任何数据离开你的基础设施。"
tags: "privacy, legal, self-hosted"
title: "隐私"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "privacy, telemetry, self-hosted, data handling, retention, LLM providers"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "隐私"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "legal"
order: 30
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/privacy/index.html"
item_link: "https://docs.rousseau-agent.dev/privacy/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "隐私"
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
twitter_description: "rousseau-agent is self-hosted. No telemetry endpoint, no SaaS control plane. LLM providers have their own retention policies; everything else stays in the operator's infrastructure."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "隐私"
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

## 数据处理

`rousseau-agent` 是自托管的。当运维者在自己的基础设施上运行守护进程时，**除 LLM 调用本身外，没有任何数据离开该基础设施**。

不存在：

- **遥测端点。** rousseau 在运行时不会调用 `rousseau-agent.dev` 或任何其他作者控制的服务器。
- **SaaS 控制面。** 没有许可服务器、没有云端仪表盘、没有回传。
- **使用情况分析。** 守护进程不会报告调用了哪些工具、运行了多少轮次或调用了哪些模型。
- **崩溃上报。** 崩溃只出现在本地日志（`journalctl --user -u rousseau-agent.service`）。没有堆栈跟踪被发送到任何地方。

## 会话数据的存放位置

| 数据 | 位置 | 静态加密 |
|---|---|---|
| 会话（消息历史） | `~/.local/share/rousseau/sessions.db` | 仅文件系统层面（若运维者已配置 LUKS / FileVault）。 |
| Cron 任务 | 同一 SQLite 数据库 | 同上。 |
| WhatsApp 设备配对 | `~/.local/share/rousseau/whatsapp.db` | 同上。 |
| 日志输出 | systemd journal（通常在 `~/.local/state/`） | 同上。 |
| 配置文件 | `~/.config/rousseau/config.yaml` | 同上。 |
| `claude` CLI OAuth token | `~/.claude/` | 同上。 |

守护进程不会将其中任何一项传输到任何地方。

## LLM providers

LLM provider 是唯一的外部接触点。每个 provider 有其自己的数据处理与保留策略 —— rousseau 无法控制其中任何一项：

| Provider | 保留策略 |
|---|---|
| [claudecli](/zh-Hans/providers/claudecli/) | 取决于本地 `claude` CLI 被配置发送什么。通常为 Anthropic 的标准保留策略。 |
| [Anthropic 直连](/zh-Hans/providers/anthropic/) | 见 https://www.anthropic.com/legal/aup |
| [AWS Bedrock](/zh-Hans/providers/bedrock/) | 合同定义；Bedrock 上的推理流量通常不会长期保留。 |
| [Google Vertex AI](/zh-Hans/providers/vertex/) | 合同定义；Vertex 推理通常不会长期保留。 |
| [OpenAI 兼容](/zh-Hans/providers/openai-compatible/) | 取决于端点。Ollama 和自托管 vLLM 不会外部保留任何内容；OpenAI 和 OpenRouter 各有其策略。 |

请选择保留策略与您运维需求匹配的 provider。若追求最严格姿态，请对接自托管 Ollama、vLLM 或 LM Studio —— 数据不会离开您的基础设施。

## 传输侧数据

聊天传输通过供应商的服务器发送消息（WhatsApp、Signal、Slack、Discord 等）。每一种都有其自身的数据处理姿态。rousseau 不会在其上叠加额外层 —— 供应商能看到底层协议向它们展示的内容，这是协议相关的：

- Signal 与 WhatsApp：端到端加密；供应商可见元数据但不可见消息内容。
- Slack、Discord：非端到端加密；供应商可见消息内容。
- Matrix：当房间启用 E2E 时端到端加密；否则为服务端可见。
- Email：除非您在其上叠加 PGP 或 S/MIME（rousseau 不会），否则非端到端加密。
- iMessage：端到端加密；BlueBubbles 位于 rousseau 与 Apple 之间。

## 删除会话

会话是 SQLite 数据库中的行。删除方式：

```sh
rousseau session delete <session-id>
```

或删除整个数据库：

```sh
rm ~/.local/share/rousseau/sessions.db
```

下次启动时会重新创建一个空数据库。此操作同时会清空 FTS5 跨会话召回索引。

## 第三方依赖

`go.mod` 列出了每一个依赖项。没有任何一个被配置为回传。构建期依赖（linter、静态分析器）仅在 CI 中运行。运行期依赖列于随每次 release 附带的 CycloneDX SBOM 中。
