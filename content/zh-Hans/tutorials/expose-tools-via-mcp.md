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
description: "Expose rousseau's session store and cron jobs to Claude Desktop as an MCP server that Claude can drive from its own tool interface."
keywords: "mcp, claude desktop, stdio, tools, rousseau_search_sessions, rousseau_read_session"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/tutorials/expose-tools-via-mcp/"
subtitle: "Wire rousseau mcp into Claude Desktop and let it query the session store."
tags: "tutorials, mcp, claude-desktop, stdio, sessions"
title: "教程：通过 MCP 暴露工具"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, claude desktop, stdio, tools, rousseau_search_sessions, rousseau_read_session"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "教程：通过 MCP 暴露工具"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/tutorials/expose-tools-via-mcp/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/expose-tools-via-mcp/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "教程：通过 MCP 暴露工具"
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
twitter_description: "Expose rousseau's session store and cron jobs to Claude Desktop as an MCP server that Claude can drive from its own tool interface."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "教程：通过 MCP 暴露工具"
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

## 您将构建什么

将 rousseau 作为 MCP stdio 服务器的 Claude Desktop。在 Claude Desktop 聊天内部，您可以问"找出我们讨论 retry 逻辑的会话"，Claude 会调用 `rousseau_search_sessions`，然后调用 `rousseau_read_session` 来获取完整对话稿。

预计时间：5 分钟。

## 先决条件

- 已安装 Claude Desktop（macOS 或 Windows）。Linux 使用 Claude CLI，而不是 Desktop —— 见底部的替代方案。
- Rousseau 已安装并在 `$PATH` 中。
- `~/.local/share/rousseau/sessions.db` 中有一些已有的会话历史 —— 如果文件为空，请多运行几次 `rousseau chat`。

## 第 1 步：了解暴露的内容

`rousseau mcp`（`internal/cli/mcp.go`）启动一个说 Model Context Protocol 的 stdio JSON-RPC 服务器。`RegisterRousseauTools`（`internal/mcp/tools.go`）附加四个只读工具：

| 工具 | 用途 |
|---|---|
| `rousseau_search_sessions` | 跨所有已记录会话的 FTS5 全文搜索（通过 `internal/state/sqlite/search.go`）。 |
| `rousseau_list_sessions` | 列出会话，最新在前。 |
| `rousseau_read_session` | 按 id 返回一个会话的完整对话稿。 |
| `rousseau_cron_list` | 列出 rousseau 的定时 cron 任务。 |

没有写入工具；MCP 宿主可以浏览但不能改动。确切的输入 schema 见 [MCP：暴露的工具](/zh-Hans/mcp/exposed-tools/)。

## 第 2 步：接线 Claude Desktop

Claude Desktop 读取 `claude_desktop_config.json`：

- **macOS：** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows：** `%APPDATA%\Claude\claude_desktop_config.json`

添加一个指向您的 `rousseau` 二进制的 `mcpServers` 条目：

```json
{
  "mcpServers": {
    "rousseau": {
      "command": "/usr/local/bin/rousseau",
      "args": ["mcp"]
    }
  }
}
```

重启 Claude Desktop。

## 第 3 步：核实

打开一个 Claude Desktop 聊天，检查工具选择器中是否出现这些工具。您应看到四个以 `rousseau_` 为前缀的工具。试试：

```
Use rousseau_list_sessions to show me my 5 most recent sessions,
then read the top one with rousseau_read_session.
```

Claude 会调用这两个工具，rousseau 的 MCP 服务器（`internal/mcp/server.go`）会通过 stdin/stdout 处理每个 JSON-RPC 信封。幕后：

1. Claude Desktop 调用 `initialize`，然后 `tools/list` —— rousseau 按声明的插入顺序响应四个工具。
2. Claude 挑一个工具并用参数调用 `tools/call` —— rousseau 的处理器（来自 `internal/mcp/tools.go`）查询 SQLite 并返回文本内容。
3. 出错时，rousseau 通过内容通道（`isError=true`）浮现错误，而不是作为 JSON-RPC 错误 —— MCP 宿主期望如此。

## 第 4 步：（可选）附加到 Claude CLI / 其他 MCP 宿主

stdio 协议与宿主无关。对于 Claude CLI：

```sh
claude --mcp-config <(cat <<'JSON'
{ "mcpServers": { "rousseau": { "command": "rousseau", "args": ["mcp"] } } }
JSON
)
```

对于 Continue.dev、Codeium 或其他 MCP 宿主，按它们的 MCP 服务器注册流程使用 `command: rousseau`、`args: [mcp]`。已测试客户端见 [MCP：兼容性](/zh-Hans/mcp/compatibility/)。

## 第 5 步：FTS5 语法小抄

由于 rousseau_search_sessions 是 SQLite FTS5（`internal/state/sqlite/search.go`）的薄封装，query 字段支持：

| 查询 | 含义 |
|---|---|
| `retry logic` | 任何同时包含这两个词的文档。 |
| `"retry logic"` | 精确短语。 |
| `retr*` | 前缀匹配。 |
| `retry OR backoff` | 布尔 OR。 |
| `retry NOT retries` | 排除。 |

排序使用 BM25（排名越低越相关）；`Search` 中的 `snippet()` 调用为每个命中给您 200 字符的预览。

## 故障排除

- **Claude Desktop 中"unknown tool"。** 重启应用。工具列表只在会话开始时获取。
- **服务器立即退出。** `rousseau mcp` 会打开 SQLite 状态文件；如果 `state.path` 中的路径不可写，`Open()` 会失败，进程以非零码退出。从 shell 运行它以查看错误。
- **搜索结果为空。** 确认 FTS5 索引已填充：`sqlite3 ~/.local/share/rousseau/sessions.db "SELECT count(*) FROM sessions_fts"`。`internal/state/sqlite/search.go` 中的 `EnsureSearch` 会在每次打开时回填索引，但损坏的状态文件可能需要手动重建。

## 相关

- [MCP](/zh-Hans/mcp/) —— 参考文档。
- [MCP：暴露的工具](/zh-Hans/mcp/exposed-tools/) —— 每个工具的 schema。
- [MCP：兼容性](/zh-Hans/mcp/compatibility/) —— 已测试客户端。
- [参考：会话存储](/zh-Hans/reference/session-store/) —— 工具背后的 SQLite schema。
