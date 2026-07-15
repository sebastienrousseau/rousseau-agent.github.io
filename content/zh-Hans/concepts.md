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
description: "Architecture overview of rousseau-agent: agent loop, transport interface, tool registry, approval policies, SQLite session store, MCP server, cron scheduler, skills loader."
keywords: "architecture, agent loop, session, transport, tool registry, approval, MCP, cron, skills, compression, FTS5"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/concepts/"
subtitle: "Agent 循环、传输和会话存储如何协同工作。"
tags: "architecture, agent, session, mcp"
title: "核心概念"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "architecture, agent loop, session, transport, tool registry, approval, MCP, cron, skills, compression, FTS5"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "核心概念"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "concepts"
order: 3
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/concepts/index.html"
item_link: "https://docs.rousseau-agent.dev/concepts/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "核心概念"
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
twitter_description: "Architecture overview of rousseau-agent: agent loop, transport interface, tool registry, approval policies, SQLite session store, MCP server, cron scheduler, skills loader."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "核心概念"
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

## 分层架构

```
+---------------------------------------------------------------+
|                             CLI                              |
|  chat  whatsapp  slack  discord  ...  mcp  cron  skills      |
+-------------------------+-------------------------------------+
                          |
+-------------------------v-------------------------------------+
|                          Router                              |
|          (per-JID session, allowlist, dispatch)              |
+-------------+---------------------------+---------------------+
              |                           |
     Transport interface           agent.Agent
     Start / Stop / Deliver        Turn / TurnStream
              |                           |
   +----------+----------+       +--------+--------+
   | 9 concrete adapters |       | Provider iface  |
   +---------------------+       | 5 concrete impls|
                                 +--------+--------+
                                          |
                                 +--------v--------+
                                 | Tools Registry  |
                                 | read/write/edit |
                                 | grep/bash + ext |
                                 +--------+--------+
                                          |
                                 +--------v--------+
                                 |  State (SQLite) |
                                 | sessions, cron, |
                                 | jidmap, FTS5    |
                                 +-----------------+
```

`agent` 包只依赖 `tools` 暴露的接口、它自身的 `Provider` 类型以及标准库。具体的提供方、存储和传输依赖 `agent`——绝不反向。

## agent 循环

`Session → Turn → Provider → tool-use 往返`。每条用户消息都会调用 `Agent.Turn`：

1. **压缩检查。** 配置的 `Compressor` 有机会在本轮运行前重写会话。当它这样做时，`Request.CacheableMessages` 被设置，以便摘要块在紧接着的下一轮被缓存。
2. **技能追加。** 若配置了 `SkillsProvider`，它会检查最后一条用户消息并返回要拼接到系统提示中的文本。
3. **检索追加。** 若配置了 `RecallProvider`，它会跨先前会话查询 FTS5 索引并返回要拼接的文本。
4. **提供方调用。** `Provider.Complete` 实现返回一个带有 `StopReason` 的 `Response`。
5. **工具调用分发。** 若 `StopReason == StopToolUse`，每次请求的工具调用都会送往 `Approver`。拒绝会成为 `tool_result` 错误，让模型可以适应。允许的调用会针对 `Registry` 执行，其输出在下一次迭代中回放。
6. **本轮结束。** 循环直到 `StopReason == StopEndTurn` 或达到 `MaxIterations`（默认 32）。

`internal/agent/agent.go` 是权威参考。

## 传输

每个传输都实现 `transport.Transport`：

```go
type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

`Handler.Handle` 接收一个 `IncomingMessage`（`From`、`Body`、`At`）并返回回复文本。`Router` 位于传输之上，负责按发送者隔离会话、执行允许列表以及分发给 `Agent`。

默认情况下所有随附的传输都不暴露公开 HTTP 面。Slack 使用 Socket Mode（出站 WebSocket）。Discord 使用 Gateway（出站 WebSocket）。Signal 是子进程。WhatsApp 是 Meta 基于 TCP 的 Web 协议。Matrix、Telegram、iMessage 和 email 使用轮询。SMS 是只发送的，因为入站侧需要 webhook。

## 工具注册表

`internal/tools` 定义 `Tool` 接口和并发安全的 `Registry`。内置工具位于 `internal/tools/builtin/`：

- `read`——读取文件。
- `write`——写入文件。
- `edit`——字符串替换，强制唯一匹配以防止意外的大规模替换。
- `grep`——文本搜索。
- `bash`——命令执行。**承载安全的关键边界。**

每个工具都声明严格的 JSON schema。添加一个工具只需在装配时调用一次 `registry.MustRegister(myTool)`；agent 核心不变。

## 审批策略

每次工具调用在执行前都会经过 `Approver.Approve`。`internal/agent/approver.go` 中提供三种内置策略：

| 模式 | 行为 |
|---|---|
| `allow_all` | 每次调用都会运行。使用 `claudecli` 提供方时合适，它会自行处理审批。 |
| `deny_all` | 每次调用都被阻止。适用于冒烟测试与只读会话。 |
| `pattern` | 按工具的正则允许 / 拒绝规则。deny 优先于 allow。未匹配的请求回落到 `Default`（`allow` 或 `deny`）。 |

拒绝理由会作为 `tool_result` 错误反馈给模型，使模型有机会适应，而不是静默失败。

## 会话存储

`internal/state/sqlite/` 在 `modernc.org/sqlite` 上实现 `state.Store` 接口——纯 Go，无 libc，无 CGo。特性：

- **WAL 日志**，`busy_timeout=15s`。
- **关闭时执行 WAL 检查点**，让主数据库文件在备份时保持一致。
- **FTS5 检索**表为每条消息建立索引；`RecallProvider` 执行跨会话查询。
- **JID 映射**表将 WhatsApp LID 身份规范化为电话 JID。
- **Cron 表**跨重启持久化计划任务。

## MCP 服务器

`internal/mcp/server.go` 是基于 stdio 的 JSON-RPC 2.0 服务器，规范版本为 **2024-11-05**。`rousseau mcp` 启动它。通过 `server.Register(mcp.ToolSpec{...})` 注册工具，让客户端（Claude Desktop、IDE 扩展、另一个代理）驱动它们。

工具失败通过 `content` 通道以 `isError=true` 呈现，而非 JSON-RPC 错误通道——这正是 MCP 主机所期望的。

## Cron 调度器

`internal/cron/scheduler.go` 封装 `robfig/cron/v3`。任务存储在 SQLite 中，可跨重启存活。每次触发都会调用 `Runner.RunOnce(ctx, prompt)`（针对全新会话的一次性 agent 轮次），然后将回复交给 `Delivery`——一个与传输无关的函数，用于投递消息。

通过 `rousseau cron add` 添加的新任务会在下一个 `PollInterval`（默认 60 秒）内生效。

## 技能加载器

`internal/skills/skills.go` 扫描 `skills_dir` 下的 `*.md` 文件。每个文件可携带 YAML front-matter，声明 `name`、`description` 与 `triggers`。当任一触发词出现在当前用户消息中时，技能正文会拼接到该轮的系统提示中。格式刻意贴近 [agentskills.io](https://agentskills.io) 约定。

## 压缩

`internal/agent/compressor.go` 在会话超过 `TriggerMessages`（默认 60）时运行基于 LLM 的摘要。最近的 `KeepRecent`（默认 8）条消息按原样保留；更旧的一切被折叠为单个摘要块。默认关闭，因为订阅制的 `claudecli` 账号很少需要；在针对按 token 计费的提供方运行时开启。

## 下一步

- [配置参考](/zh-Hans/configuration/)——每一个字段。
- [Agent 循环参考](/zh-Hans/agent-loop/)——库嵌入契约。
- [MCP](/zh-Hans/mcp/)——客户端接入。
