---

# Front Matter (YAML)

author: "sebastian.rousseau@gmail.com (Sebastien Rousseau) "
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
description: "How the LLM compressor decides what to keep, the roles of trigger_messages and keep_recent, and a before/after diagram of a compressed session."
keywords: "compression, context, keep_recent, trigger_messages, summariser, marker"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/guides/context-management/"
subtitle: "trigger_messages, keep_recent, and the compressed-marker convention."
tags: "guides, context, compression, summariser"
title: "指南：上下文管理"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "compression, context, keep_recent, trigger_messages, summariser, marker"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "指南：上下文管理"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/guides/context-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/context-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "指南：上下文管理"
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
twitter_description: "How the LLM compressor decides what to keep, the roles of trigger_messages and keep_recent, and a before/after diagram of a compressed session."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "指南：上下文管理"
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

## 问题

一个持续数周的会话会积累数百条消息。每一条在每一轮都被重新发送到 provider。成本随轮次数量线性增长；延迟也随之增长。Rousseau 的 `LLMCompressor`（`internal/agent/compressor.go`）用一次小小的一次性成本 —— 每次压缩一次摘要调用 —— 换取后续每一轮的永久节省。

压缩**默认关闭**，因为参考部署在订阅层使用 `claudecli`，那里不按 token 计费。当您对着 Anthropic direct、Bedrock、Vertex 或 OpenAI 兼容的按 token 计费 provider 运行时，把它打开。

## 旋钮

来自 `internal/config/config.go` 的 `CompressionConfig`：

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60        # 零则使用默认 60
    keep_recent: 8              # 零则使用默认 8
    prompt: ""                  # 覆盖默认摘要提示
```

含义：

| 字段 | 作用 |
|---|---|
| `enabled` | 打开压缩。为 false 时，代理使用 `NoopCompressor`，整节都是 no-op。 |
| `trigger_messages` | 一旦 `len(session.Messages) >= trigger_messages` 就触发压缩。 |
| `keep_recent` | 压缩后原样保留的最新消息数量。 |
| `prompt` | 覆盖默认摘要提示。仅在您需要自定义指令时设置（例如保留 JSON 输出、始终引用文件路径）。 |

## 默认摘要提示

```
Summarise the following conversation in <=200 words. Preserve every
commitment, TODO, credential, filename, and quoted output. Skip
pleasantries. Return only the summary — no preamble.
```

在 `internal/agent/compressor.go` 中定义为 `defaultSummaryPrompt`。用 `config.yaml` 中的 `agent.compression.prompt` 覆盖。

## 之前 / 之后

一个 68 条消息的会话，`trigger_messages: 60`、`keep_recent: 8`：

```
压缩前：                                    压缩后：

┌──────────────────────────┐              ┌──────────────────────────────┐
│ msg[0]  user             │              │ msg[0]  user（合成）         │
│ msg[1]  assistant        │              │   [rousseau-compressed]      │
│ msg[2]  user             │              │   （前 60 条消息的摘要）：… │
│  …  （60 条消息）        │      →       │                              │
│ msg[59] assistant        │              ├──────────────────────────────┤
├──────────────────────────┤              │ msg[1]  user       —— 原样   │
│ msg[60] user   原样      │              │ msg[2]  assistant  —— 原样   │
│ msg[61] assistant        │              │ msg[3]  user       —— 原样   │
│  …                       │              │ msg[4]  assistant  —— 原样   │
│ msg[67] assistant        │              │ msg[5]  user       —— 原样   │
└──────────────────────────┘              │ msg[6]  assistant  —— 原样   │
                                          │ msg[7]  user       —— 原样   │
                                          │ msg[8]  assistant  —— 原样   │
                                          └──────────────────────────────┘
总消息数：68                              总消息数：9
每轮输入 token：~5000                     每轮输入 token：~800
```

## 标记

压缩器给合成用户消息加前缀 `[rousseau-compressed]`（`internal/agent/compressor.go` 中的常量 `DefaultCompressorMarker`）。在后续轮次，`headAlreadyCompressed()` 用该标记检测已压缩前缀，除非会话增长到 `2 * trigger_messages`，否则跳过重复压缩。

正是这一点让压缩有界 —— 您不必每 60 条消息就为重新摘要摘要付费。

## 选择值

| 场景 | 推荐 |
|---|---|
| 付费 provider 上的长运行传输守护进程。 | `trigger_messages: 60`、`keep_recent: 8`。默认为此调优。 |
| 想把一切都留在上下文中的交互式 TUI。 | `enabled: false`。 |
| 大量引用代码 / 日志的高技术性会话。 | `trigger_messages: 40`、`keep_recent: 12`。保留更多近期上下文；更早压缩。 |
| 成本关键的批量摘要（cron）。 | 每次 cron 运行都是新会话，所以压缩很少触发。保持默认打开。 |

## 一次压缩通行的成本

每次触发一次摘要调用。所用 provider 就是 `Config.Provider` 选择的那个 —— 与代理所用相同。这意味着：

- Sonnet 级压缩器调用：~1-2 秒，大约相当于 ~2 轮的输入 token 成本。
- 视会话形状，~5-10 轮后回本。

要更便宜的压缩器，用双守护进程多 provider 模式运行 rousseau，压缩器守护进程使用 Haiku 级模型。见 [指南：多 provider](/zh-Hans/guides/multi-provider/)。

## 紧急：会话大到无法加载

如果会话的负载在压缩触发之前就超过模型的上下文窗口 —— 罕见但在 `trigger_messages` 非常小且工具输出很大时可能 —— 下一轮将以 provider 的"上下文长度超限"错误失败。恢复：

```sh
rousseau session delete <id> --yes
```

然后重新开始。或通过 SQLite 手动缩减：

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
UPDATE sessions SET payload = json_set(payload, '$.messages',
  json_extract(payload, '$.messages[-8:]'))
WHERE id = '<session-id>';
SQL
```

注意：确切的 JSON 路径语法视 SQLite 版本而异。先用 `SELECT payload` 确认。

## 相关

- [用户指南：压缩 + 回忆](/zh-Hans/user-guide/compression-recall/) —— 更深入的参考。
- [指南：速率限制](/zh-Hans/guides/rate-limits/) —— 成本影响。
- [指南：会话管理](/zh-Hans/guides/session-management/) —— 会话生命周期。
- [参考：配置 schema](/zh-Hans/reference/config-schema/) —— 每个字段。
