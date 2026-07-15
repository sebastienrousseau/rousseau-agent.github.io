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
description: "Session compression triggers and FTS5 cross-session recall in rousseau-agent. How the agent loop keeps long sessions inside the model's context."
keywords: "compression, recall, fts5, session, context window, summarisation, trigger_messages, keep_recent"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/user-guide/compression-recall/"
subtitle: "Session compression and FTS5 cross-session recall."
tags: "compression, recall, session, fts5"
title: "压缩与召回"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "compression, recall, fts5, session, context window, summarisation, trigger_messages, keep_recent"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "压缩与召回"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "concepts"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/user-guide/compression-recall/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/compression-recall/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "压缩与召回"
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
twitter_description: "Session compression triggers and FTS5 cross-session recall in rousseau-agent. How the agent loop keeps long sessions inside the model's context."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "压缩与召回"
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

## 两个问题，两种机制

- 单个长会话可能超出模型的上下文窗口。**压缩** 把旧消息折叠成摘要块，让循环持续运行。
- 关联话题上的新会话失去了先前对话的价值。**回忆** 跨会话查询 FTS5 索引，并把摘录拼接进系统提示。

压缩就地编辑当前会话。回忆从不编辑 —— 它为当前轮次向系统提示追加上下文。

## 压缩

`internal/agent/compressor.go` 实现了一个由 LLM 支撑的摘要器。代理循环在每次 `Turn` 开始时咨询它：

```go
if changed, err := a.opts.Compressor.Compress(ctx, s); err != nil {
    a.logger.Warn("agent.compress_failed", slog.String("err", err.Error()))
} else if changed {
    a.logger.Info("agent.compressed", slog.Int("messages", len(s.Messages)))
}
```

如果会话较短，什么也不发生。一旦消息计数越过 `trigger_messages`，压缩器：

1. 隔离会话的尾部 —— 最近 `keep_recent` 条消息 —— 并原样保留。
2. 把更早的所有内容连同一个摘要提示喂给 provider。
3. 用一条包含摘要的合成 `RoleSystem` 消息替换更早的块。
4. 标记该会话，让摘要块在下一次 provider 调用时位于符合提示缓存条件的前缀中。

循环随后针对更短的消息列表继续。用户永远看不到接缝。

### 启用压缩

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60      # 零 → 默认 60
    keep_recent: 8            # 零 → 默认 8
    prompt: ""                # 零 → 合理默认值
```

| 字段 | 默认 | 含义 |
|---|---|---|
| `enabled` | `false` | 默认关闭。 |
| `trigger_messages` | 60 | 消息计数超过此值时压缩触发。 |
| `keep_recent` | 8 | 原样保留的最近消息数量。 |
| `prompt` | 内置 | 覆盖摘要指令。 |

### 何时关闭

压缩每次触发使用一次 provider 往返。在订阅层的 `claudecli` 账户上，那次往返是免费的 —— 放心启用。在按 token 计费的 API 上，每次触发都有成本，请把 `trigger_messages` 调高，或在短寿命会话中保持禁用。

### 何时开启

- 长寿命的聊天传输守护进程，其中的 WhatsApp 线程持续数周增长。
- 回复喂给后续提示的 cron 定时提示。
- token 成本为零的自托管 provider。

### 压缩前后保留的语义

- tool-use / tool-result 对永不拆分。如果一个 `tool_use` 处于被压缩区域而其 `tool_result` 处于保留区域，两者都会被折叠进摘要。
- 压缩器绝不重写当前进行中的用户轮次。
- 提示缓存（`internal/llm/anthropic` 的 `cache_control` 标记）被放在摘要块上，以便下一次调用从缓存读取它。

## 回忆

`internal/state/sqlite/` 维护一个索引每条消息的 FTS5 虚拟表。`RecallProvider` 针对该表运行查询，并返回一个系统提示附录。

### 接口

```go
type RecallProvider interface {
    SystemAppendix(ctx context.Context, s *Session) string
}
```

代理循环每次迭代调用此方法一次。当它返回非空文本时，文本会被追加到该迭代的基础系统提示。

### 默认 provider

`internal/agent/recall.go` 提供一个启发式：

1. 从当前会话最后一条用户消息中提取显著 token。
2. 在其他会话的 FTS5 索引上对这些 token 运行 `MATCH`。
3. 把 top N 摘录格式化为 `Previously in another session:` 块。
4. 限定附录以永不超出所配置的字符预算。

### 启用回忆

回忆在代理构造时接线。见 `internal/cli/chat.go` 与 `internal/cli/*.go` 了解每个传输如何接线它。在您自己的嵌入中：

```go
recall, err := sqlitestore.NewRecall(store)
if err != nil { /* ... */ }

ag := agent.New(provider, registry, logger, agent.Options{
    RecallProvider: recall,
})
```

### 与审批器的交互

回忆从会话存储读取；它从不触发工具调用。不咨询审批器。存储内容本身就是信任边界。

### 从 CLI 做会话搜索

回忆是面向机器的功能。对人类而言，同一份 FTS5 索引支撑：

```sh
rousseau session search "kubectl"
rousseau session search "PVC not binding"
```

同一查询引擎、同样的结果，只是没有真正的 RecallProvider 可能添加的 LLM 重排。

## 与 skills 的交互

Skills（[Skills](/zh-Hans/skills/)）和回忆都往系统提示中添加内容。它们按固定顺序组合：

1. 基础系统提示（来自 `agent.system_prompt` 或默认值）。
2. Skills 附录（如果有）。
3. 回忆附录（如果有）。

一切以两个换行分隔。若无需添加内容，基础提示原封不动通过。

## 摘要块的语义

合成摘要消息以 `RoleSystem` 发出。它不是用户或助手消息，因此在 `rousseau session show` 中不会作为对话轮次出现 —— 它以 `[compressed summary]` 元数据的形式显示。

如果您用 `rousseau chat --session <id>` 恢复一个已压缩会话，摘要会被保留。通过假想的 schema 编辑删除摘要块是不安全的：模型可能引用只通过它才知晓的事实。

## 核实压缩正在触发

```
INFO agent.compressed messages=12
```

`messages` 是摘要块替换被压缩前缀之后的新会话长度。`WARN agent.compress_failed err=...` 意味着摘要 provider 出错；循环针对未压缩会话继续。

## 注意事项

- 压缩是有损的。摘要是模型生成的文本；重要细节可能被丢弃。对于审计轨迹，请在存储中保留完整会话 —— 压缩只影响模型看到的内容，不影响 SQLite 持久化的内容。
- 回忆需要 FTS5 SQLite 扩展。`modernc.org/sqlite` 默认将其编译进去；如果您替换存储实现，请确保 FTS5 可用。
- 两项功能都假定 UTF-8 文本。语音笔记转写（见 [语音模式](/zh-Hans/user-guide/voice-mode/)）一旦转写就算作常规用户消息。

## 下一步

- [概念](/zh-Hans/concepts/) —— 代理循环概览。
- [配置](/zh-Hans/configuration/) —— 每个 `agent.compression.*` 旋钮。
- [Skills](/zh-Hans/skills/) —— 第三个系统提示输入。
