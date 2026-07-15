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
description: "Configure the direct Anthropic provider: ANTHROPIC_API_KEY, model IDs, max_tokens, prompt cache markers on the last messages, streaming."
keywords: "Anthropic, ANTHROPIC_API_KEY, Claude API, prompt caching, cache_control, ephemeral, streaming"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/providers/anthropic/"
subtitle: "Direct Anthropic API with ephemeral prompt-cache markers."
tags: "providers, anthropic"
title: "Anthropic 提供方"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Anthropic, ANTHROPIC_API_KEY, Claude API, prompt caching, cache_control, ephemeral, streaming"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Anthropic 提供方"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 7
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/providers/anthropic/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/anthropic/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Anthropic 提供方"
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
twitter_description: "Configure the direct Anthropic provider: ANTHROPIC_API_KEY, model IDs, max_tokens, prompt cache markers on the last messages, streaming."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Anthropic 提供方"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">你将学到</span><p>rousseau 发出的 Anthropic 请求的精确线级形状、哪些内容块会收到提示缓存标记及其原因、流式如何映射到 <code>agent.StreamingProvider</code>，以及 401/429/529 响应的失败模式。请对照阅读 <code>internal/llm/anthropic/client.go</code> 与 <code>internal/llm/anthropic/cache.go</code>。</p></aside>

## 何时使用 Anthropic 提供方

直连的 `anthropic` 提供方在以下场景是正确选择：

- 你拥有 Anthropic API 密钥并希望在 `api.anthropic.com` 上按 token 计费。
- 你希望在 rousseau 侧执行工具（`Registry` 全面参与）。
- 你希望在稳定前缀上启用临时提示缓存标记。
- 你希望在 `rousseau chat` 中使用流式完成（按 token 更新视口）。
- 你希望有明确、公开的速率限制（不同于 `claudecli` 订阅模式）。

## 配置

```yaml
provider: anthropic

anthropic:
  api_key: sk-ant-...
  model: claude-sonnet-4-6
  max_tokens: 4096
```

| 字段 | 默认值 | 作用 |
|---|---|---|
| `api_key` | *来自 `ANTHROPIC_API_KEY`* | 用于 `api.anthropic.com` 的 Bearer 令牌。选择此提供方时若为空则拒绝。 |
| `model` | `claude-sonnet-4-6` | 模型标识符。 |
| `max_tokens` | `4096` | 单次完成的输出 token 上限。 |

环境变量 `ANTHROPIC_API_KEY` 在加载时绑定到 `anthropic.api_key`，因此导出它等同于在配置中设置它。容器运维人员通常在 systemd 单元的 `Environment=` 行导出它，而不是写入 `config.yaml`。

## 模型标识符

`rousseau-agent` 将 `model` 原样传递给 SDK。在生产环境中固定精确的模型 ID（`claude-sonnet-4-6`、`claude-opus-4-6`），这样当 Anthropic 升级新快照时你的流量不会随之偏移。

## 提示缓存内部机制

Anthropic 的临时提示缓存允许你用 `cache_control: { type: "ephemeral" }` 标记内容块。API 会缓存直到并包含任一带缓存标记的块的前缀；带有相同前缀的后续轮次只需支付通常输入 token 成本的一小部分（撰写本文时为 10%——请查看 Anthropic 文档获取当前定价）。

Rousseau 通过 `internal/llm/anthropic/cache.go` 中的 `applyCacheMarkers` 应用标记。当出站 `Request` 中 `CacheableMessages > 0` 时会发生两件事：

1. **系统提示获得 `cache_control: ephemeral`。** 它跨每一轮保留，因此一旦启用就总值得缓存。参见 `internal/llm/anthropic/client.go` 第 68–75 行。
2. **最后 `CacheableMessages` 条消息**在其最后一个文本块上获得 `cache_control: ephemeral`。这让不断增长的会话保持廉价：随着新轮次附加，标记会沿文本流下移，但直到上一个标记的前缀仍然热。

### 哪些块会被标记

`markLastTextBlock` 反向遍历 `MessageParam` 的内容，将 `CacheControl` 设置在它找到的第一个文本块上。`tool_use` 与 `tool_result` 块被跳过——SDK 将它们建模为具有各自可选 `CacheControl` 字段的不同变体，而文本是安全的公共分母。参见 `internal/llm/anthropic/cache.go`。

### 何时值得启用

<aside class="admonition" data-type="note"><span class="admonition-title">缓存经济学</span><p>盈亏平衡点取决于缓存前缀的复用程度。对于每次会话运行 20–100 轮、系统提示为 5–10 kB 的聊天传输（加载技能时的典型情况），启用缓存通常可将输入 token 账单减半。对于只生成单条回复的一次性定时任务，则毫无节省。</p></aside>

`Compressor` 在重写后设置 `CacheableMessages = len(recentMessages) - 1`，使新的摘要块在紧接着的下一轮就是缓存热的。其他代码路径将 `CacheableMessages = 0`，意味着缓存按请求可选。嵌入者在直接调用提供方时应显式设置它。

### 验证缓存命中

Anthropic API 在每个响应上返回 `usage.cache_read_input_tokens` 与 `usage.cache_creation_input_tokens`。`agent.Usage` 目前只暴露 `InputTokens` 与 `OutputTokens`，因此验证明细要么启用 debug 日志，要么读取原始 SDK 响应——这是一个已知的可观测性缺口，在 `docs/GAP_ANALYSIS_2026.md` 中跟踪。

## 流式语义

该提供方实现了 `agent.StreamingProvider`。`rousseau chat` 默认使用流式，让 token 到达时落入 TUI 视口。聊天传输（WhatsApp、Slack、Discord 等）使用非流式完成，因为消息导向的传输本就批量投递——中间的 delta 流在最终消息发送前只会被丢弃。

`internal/llm/anthropic/stream.go` 中的流式实现消费 SDK 的 `MessageStreamEvent` 联合类型：

| 事件 | 处理方式 |
|---|---|
| `message_start` | 发出 `agent.StreamEvent{Kind: StreamMessageStart}`。 |
| `content_block_start` | 发出 `agent.StreamEvent{Kind: StreamContentStart}` 以及块类型。 |
| `content_block_delta` | 对文本发出 `agent.StreamEvent{Kind: StreamTextDelta, Text: delta.Text}`；`input_json_delta` 事件累积为部分 tool-use 输入。 |
| `content_block_stop` | 发出 `agent.StreamEvent{Kind: StreamContentStop}`。 |
| `message_delta` | 携带最终停止原因与累计用量。 |
| `message_stop` | 流结束。 |

Bubble Tea TUI 通过 `agent.StreamTurn` 订阅这些事件，`StreamTurn` 编排流 / tool-use 循环。参见 `internal/agent/stream_turn.go`。

## 工具使用

来自 `Registry` 的工具定义在 `toSDKTools` 中转换为 Anthropic 的 `tools` 数组。审批策略（`agent.approver`）生效——每一个 `tool_use` 块在执行前都会在 agent 循环中经过 `Approver.Approve`。拒绝以带 `is_error: true` 的 `tool_result` 块反馈给模型，让模型可以适应（选择不同动作、询问用户、优雅放弃）。

<aside class="admonition" data-type="warning"><span class="admonition-title">Schema 形状</span><p>SDK 期望工具的 <code>input_schema</code> 是一个具有顶层 <code>properties</code> 字段的 JSON Schema 对象。Rousseau 的 <code>tools.Definition</code> 1:1 映射——参见 <code>internal/llm/anthropic/client.go</code> 中的 <code>toSDKTools</code>。发出非对象 schema 的自定义工具会在请求时失败。</p></aside>

## 速率限制处理

Anthropic API 返回：

| 代码 | 含义 | rousseau 的行为 |
|---|---|---|
| 401 | 密钥错误或缺失 | 立即失败，不重试。 |
| 400 | 请求错误（schema、编码、提示过长） | 携带 SDK 错误信息立即失败。 |
| 429 | 每分钟速率限制超限 | 作为 `agent` 错误呈现。`Complete` 不重试。 |
| 529 | 过载（临时容量不足） | 作为 `agent` 错误呈现。`Complete` 不重试。 |
| 5xx | 服务器错误 | 作为 `agent` 错误呈现。`Complete` 不重试。 |

**重试是调用方的责任。** `rousseau chat` TUI 与传输 `RouterHandler` 目前未实现退避——429 会让本轮失败。这是刻意的设计选择：重试涉及 tool_use 语义（部分工具调用、幂等性），而调用方掌握做出正确决定的上下文。规划中的重试助手参见 `docs/GAP_ANALYSIS_2026.md`。

<aside class="admonition" data-type="tip"><span class="admonition-title">在聊天传输中处理 429</span><p>用调用方级别、带指数退避与抖动的重试循环包装传输的 <code>RouterHandler</code>。<a href="/zh-Hans/guides/rate-limits/">速率限制指南</a> 提供了完整示例。</p></aside>

## 成本控制

- **将 `max_tokens` 设低**（2048–4096），适用于回复很少需要超过几段的聊天传输。`max_tokens` 是上限而非目标——你只为实际生成的输出付费。
- **启用 `agent.compression`**，在文本超过 `trigger_messages`（默认 60）后折叠旧消息。摘要远比原文本便宜。
- **在嵌入 agent 库时使用 `CacheableMessages > 0`**——直连 API 是提示缓存最能发挥作用的地方。
- **对 tool-use 循环优先选择 Sonnet。** Opus 更贵、更慢；除非你在具体任务上有可量化的收益，Sonnet 是默认之选是有原因的。
- **警惕流中止计费。** 如果流在响应中途被取消，API 仍会为取消点之前生成的 token 计费。请在调用方设置超时上限。

## 故障排查

### `anthropic: complete: 401 unauthorized`

`ANTHROPIC_API_KEY` 缺失、被吊销，或指向你已无权访问的工作区/组织。用 `curl -H "x-api-key: $ANTHROPIC_API_KEY" https://api.anthropic.com/v1/messages` 验证。

### `anthropic: complete: 400 messages: too many messages`

文本超过上下文窗口。启用 `agent.compression.enabled: true`（默认值通常够用）并重试。若已启用压缩仍触发，请降低 `trigger_messages` 或提高 `keep_recent`，让压缩器更早触发。

### `anthropic: unsupported content block <type>`

SDK 返回了 rousseau 未建模的内容块类型——目前仅支持 `text` 和 `tool_use`（见 `fromSDKResponse`）。当模型发出 `thinking` 块（扩展思考模式）时可能出现。rousseau 尚未呈现这些；请在提供方配置中禁用扩展思考，直到支持落地。

### 持续负载下出现 429

你触及了每分钟输出 token 速率限制。选项：(1) 向 Anthropic 请求提升限额，(2) 在调用方排队并串行处理各轮，(3) 切换到 Bedrock 或 Vertex，那里的企业配额通常更高。

### 尽管 `CacheableMessages > 0` 仍然缓存未命中

Anthropic 在前缀变化时使缓存失效。常见原因：系统提示每轮重新生成（技能随每条用户消息变化）、模型 ID 变更或 `MaxTokens` 不同。记录请求负载并跨两轮做 diff 以定位。

## 相关页面

- [提供方：claudecli](/zh-Hans/providers/claudecli/)——子进程 vs 直连 API 的权衡。
- [提供方：Bedrock](/zh-Hans/providers/bedrock/)——具有企业配额的 AWS 托管 Claude。
- [指南：速率限制](/zh-Hans/guides/rate-limits/)——重试与退避操作手册。
- [Agent 循环](/zh-Hans/agent-loop/)——流式与工具使用如何组合。
- [用户指南：压缩与检索](/zh-Hans/user-guide/compression-recall/)——保持输入 token 数量合理的机制。

## 延伸阅读

- `internal/llm/anthropic/client.go`——`Complete`、消息转换、工具 schema。
- `internal/llm/anthropic/stream.go`——流式实现。
- `internal/llm/anthropic/cache.go`——缓存标记助手。
- `internal/agent/stream_turn.go`——agent 循环如何消费流式事件。
- `internal/agent/compressor.go`——压缩器如何预置 `CacheableMessages`。
