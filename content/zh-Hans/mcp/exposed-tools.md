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
description: "The exact tool signatures exposed by rousseau's stdio MCP server, mirroring internal/mcp/tools.go."
keywords: "mcp, rousseau_search_sessions, rousseau_list_sessions, rousseau_read_session, rousseau_cron_list"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/mcp/exposed-tools/"
subtitle: "Every tool rousseau's MCP server advertises, with schemas."
tags: "mcp, tools, sessions, cron"
title: "MCP：暴露的工具"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, rousseau_search_sessions, rousseau_list_sessions, rousseau_read_session, rousseau_cron_list"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP：暴露的工具"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "mcp"
order: 72
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/mcp/exposed-tools/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/exposed-tools/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "MCP：暴露的工具"
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
twitter_description: "The exact tool signatures exposed by rousseau's stdio MCP server, mirroring internal/mcp/tools.go."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP：暴露的工具"
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

## 注册

`internal/cli/mcp.go` 打开 SQLite 会话存储，构造一个 `NewCronStore`，把二者都包装在 `mcp.NewStoreBackend` 中，然后调用 `mcp.RegisterRousseauTools(s, backend)`。以下四个工具按插入顺序附加 —— `tools/list` 按这个精确顺序返回它们。

每个工具都是只读的。今天在 MCP 上没有写入面；这是有意为之，让 MCP 宿主不能改动 rousseau 的状态。

## `rousseau_search_sessions`

**描述（表面给宿主）：** _跨每条已记录 rousseau 会话的全文搜索。使用 SQLite FTS5 语法（双引号内短语、AND/OR/NOT、前缀通配符）。_

**输入 schema：**

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "FTS5 query"
    },
    "limit": {
      "type": "integer",
      "description": "Cap hits returned. Default 20."
    }
  },
  "required": ["query"]
}
```

**行为。** 把 `query` 原样传递给 SQLite 的 FTS5 引擎（`internal/state/sqlite/search.go` 中的 `Store.Search`）。结果按 BM25 排名排序（越低越相关）。每个命中渲染为三行：

```
session <id> (rank 0.42)
    title:   <session title>
    snippet: <约 200 字符的片段，带 … 省略号>
```

**错误。** 空查询返回 `query is required`。FTS5 语法错误作为 SQLite 错误冒泡，通过 `isError: true` 浮现。

## `rousseau_list_sessions`

**描述（表面给宿主）：** _列出 rousseau 会话，最新在前。_

**输入 schema：**

```json
{
  "type": "object",
  "properties": {
    "limit": {
      "type": "integer",
      "description": "Cap rows returned. Default 20."
    }
  }
}
```

**行为。** 调用使用 `idx_sessions_updated_at DESC` 索引的 `Store.List`。每一行：

```
<session-id>  <title>  msgs=<count>  updated=<iso-8601>
```

存储为空时返回 `(no sessions)`。

## `rousseau_read_session`

**描述（表面给宿主）：** _按 id 返回一个 rousseau 会话的完整对话稿。_

**输入 schema：**

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "description": "Session id"
    }
  },
  "required": ["id"]
}
```

**行为。** 调用 `Store.Load` 取回完整的 `agent.Session`。渲染为：

```
id: <session-id>
title: <session title>
created: <iso-8601>
updated: <iso-8601>
messages: <count>

[0] user
    <text content>
[1] assistant
    <text content>
    ...
```

只渲染文本内容 —— tool_use 块与 tool_result 块在 MCP 面上被省略（CLI `rousseau session show` 包含它们；MCP 有意不包含）。

**错误。** 空输入返回 `id is required`。未知 id 返回 `state.ErrNotFound`。

## `rousseau_cron_list`

**描述（表面给宿主）：** _列出 rousseau 的定时 cron 任务（名称、调度、提示、投递目标）。_

**输入 schema：**

```json
{
  "type": "object",
  "properties": {}
}
```

**行为。** 调用 `CronStore.List` —— 每个 `cron_jobs` 行一行：

```
<name> [<on|off>] <cron-expr> → <deliver-to>  prompt="<prompt>"  deliver=<deliver-to>
```

cron 表为空时返回 `(no jobs)`。如果构造时 `CronStore` 为 nil，也返回 `(no jobs)`（`storeBackend.CronList` 中的防御路径）。

## 没有暴露的

有意的省略：

| 面 | 为什么不 |
|---|---|
| `rousseau_write_session` / `rousseau_delete_session` | MCP 上的改动会让不受信任的宿主重塑 rousseau 的审计轨迹。 |
| `rousseau_add_cron` | 同样原因 —— 改动。通过 `rousseau cron add` 添加 cron 任务。 |
| 内置工具（`read`、`write`、`edit`、`grep`、`bash`） | 这些是 rousseau 自己循环内部面向 LLM 的代理工具，不是面向宿主的。暴露它们会赋予 MCP 宿主在运行 rousseau 的主机上 shell 出的能力 —— 恰是我们不想要的信任翻转。 |
| JID 映射查询 | 暴露 PII（电话号码）。如果您需要，就在运行守护进程的机器上直接查询 SQLite。 |

## 错误面

MCP 处理器返回 `([]Content, error)`。出错时，服务器（`internal/mcp/server.go` 的 `handleToolsCall`）以 `ToolsCallResult{Content: text of err, IsError: true}` 浮现错误。这遵循 MCP 约定：工具失败通过带 `isError=true` 的内容通道流动，而不是通过 JSON-RPC `error` 通道。宿主应渲染文本并继续。

## 相关

- [MCP](/zh-Hans/mcp/) —— 综合参考。
- [MCP：兼容性](/zh-Hans/mcp/compatibility/) —— 已测试客户端。
- [MCP：暴露的资源](/zh-Hans/mcp/exposed-resources/) —— 路线图。
- [参考：工具 schema](/zh-Hans/reference/tool-schemas/) —— 不同的面向代理的工具集。
