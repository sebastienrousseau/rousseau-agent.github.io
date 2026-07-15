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
description: "The exact JSON schemas for the five built-in tools rousseau ships: read, write, edit, grep, bash."
keywords: "tool schemas, read, write, edit, grep, bash, JSON Schema"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/reference/tool-schemas/"
subtitle: "JSON schemas for the five built-in tools, verbatim from internal/tools/builtin."
tags: "reference, tools, json-schema, read, write, edit, grep, bash"
title: "参考：工具模式"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tool schemas, read, write, edit, grep, bash, JSON Schema"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "参考：工具模式"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 54
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/reference/tool-schemas/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/tool-schemas/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "参考：工具模式"
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
twitter_description: "The exact JSON schemas for the five built-in tools rousseau ships: read, write, edit, grep, bash."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "参考：工具模式"
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

## 本页内容

`internal/tools/builtin/*.go` 中的每个内建工具都发布一个 `InputSchema()` 方法，返回一份 JSON Schema map。本页原样呈现这些 schema，并对每个工具的运行时契约提供一段说明。

五个内建工具是：[`read`](#read)、[`write`](#write)、[`edit`](#edit)、[`grep`](#grep)、[`bash`](#bash)。这五个都在守护进程装配中构建；审批器（`internal/agent/approver.go`）位于模型的工具调用与工具的 `Execute` 方法之间。

## read

源码：`internal/tools/builtin/read.go`。

**描述（呈给模型）：** _读取一个 UTF-8 文本文件的内容。输入：绝对路径。返回文件内容或错误。_

**输入 schema：**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "要读取文件的绝对文件系统路径。"
    }
  },
  "required": ["path"]
}
```

**契约。** `path` 必须为绝对路径（`filepath.IsAbs`）。工具将整个文件读入内存，若前 512 字节包含 NUL 字节（`isLikelyText`）则拒绝。成功时以字符串返回文件内容；否则返回错误。工具层不强制行数或大小限制 —— 审批策略才是限定文件大小的合适位置。

## write

源码：`internal/tools/builtin/write.go`。

**描述（呈给模型）：** _向文件写入 UTF-8 文本，替换现有内容。必要时创建父目录。输入：绝对路径 + 内容。_

**输入 schema：**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "要写入的绝对文件系统路径。"
    },
    "content": {
      "type": "string",
      "description": "要写入的完整文件内容。"
    }
  },
  "required": ["path", "content"]
}
```

**契约。** 整文件覆盖写入。以 `0o755` 模式创建父目录。以 `0o644` 模式写入。要求绝对路径。返回 `"wrote N bytes to /path"`。刻意不做原子交换 —— pattern 模式审批器将写入目标钉在特定目录树；工具本身不去自作聪明地处理文件系统安全。

## edit

源码：`internal/tools/builtin/edit.go`。

**描述（呈给模型）：** _在一个文件中，恰好用 new_string 替换一处 old_string。old_string 必须在文件中唯一；出现零次或多次都会导致编辑失败。请精确保留缩进。_

**输入 schema：**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "要编辑文件的绝对文件系统路径。"
    },
    "old_string": {
      "type": "string",
      "description": "要查找的精确文本。必须在文件中唯一。"
    },
    "new_string": {
      "type": "string",
      "description": "用于替换 old_string 的文本。"
    }
  },
  "required": ["path", "old_string", "new_string"]
}
```

**契约。** 精确字符串替换，非正则。`old_string` 必须在文件中 **恰好出现一次** —— 零匹配或多匹配都会以描述性错误失败，这是刻意的（借鉴自 Claude Code 的 Edit 工具）。防止意外的大规模替换，并强制模型附上足够的上下文以消除歧义。`old_string == new_string` 也会报错。返回 `"edited /path (1 replacement)"`。

## grep

源码：`internal/tools/builtin/grep.go`。

**描述（呈给模型）：** _在目录下用 Go 正则表达式搜索文件。跳过二进制文件与超过配置上限的文件。返回 'path:line: matched_line' 行。_

**输入 schema：**

```json
{
  "type": "object",
  "properties": {
    "pattern": {
      "type": "string",
      "description": "要匹配的 Go RE2 正则表达式。"
    },
    "path": {
      "type": "string",
      "description": "要搜索的绝对目录。"
    },
    "include": {
      "type": "string",
      "description": "可选的文件名 glob（例如 '*.go'）。作用于 base name。"
    },
    "ignore_case": {
      "type": "boolean",
      "description": "大小写不敏感匹配。默认 false。"
    }
  },
  "required": ["pattern", "path"]
}
```

**契约。** RE2 正则，非 PCRE。当 `ignore_case: true` 时大小写不敏感（通过前缀 `(?i)` 实现）。跳过名为 `.git`、`node_modules`、`vendor`、`.venv`、`__pycache__`、`dist`、`build` 的目录。跳过大于 `MaxFileBytes`（默认 4 MiB）的文件。在 `MaxMatches`（默认 200）处截断输出，达到上限时追加 `(truncated at N matches)` 页脚。跳过当前行包含 NUL 字节的文件（粗略的二进制检测）。

## bash

源码：`internal/tools/builtin/bash.go`。

**描述（呈给模型）：** _经由 `/bin/sh -c` 执行一条 shell 命令。返回合并后的 stdout+stderr 与退出状态。_

**输入 schema：**

```json
{
  "type": "object",
  "properties": {
    "command": {
      "type": "string",
      "description": "要执行的 shell 命令。"
    }
  },
  "required": ["command"]
}
```

**契约。** `/bin/sh -c <command>`。合并 stdout + stderr，上限为可放入 `bytes.Buffer` 的量（即受 RAM 限制）。默认 60 秒超时（构造时可配置）。超时时：返回部分输出加上一个 `bash: timed out after 60s` 错误。**工具层无沙箱。** 守护进程的操作系统用户、文件系统视图、网络姿态和 seccomp profile 才是隔离手段。pattern 模式审批器是您收窄允许命令的途径 —— 参见 [教程：加固审批器](/zh-Hans/tutorials/harden-approver-policy/)。

## MCP 暴露的工具

Rousseau 的 stdio MCP 服务器（`rousseau mcp`）暴露的是 **另一组** 工具 —— 针对会话存储与 cron 任务的只读查询。`rousseau_search_sessions`、`rousseau_list_sessions`、`rousseau_read_session`、`rousseau_cron_list` 参见 [MCP：暴露的工具](/zh-Hans/mcp/exposed-tools/)。

## 相关

- [用户指南：工具](/zh-Hans/user-guide/tools/) —— 面向运维者的视图。
- [指南：文件管理](/zh-Hans/guides/file-management/) —— `write`/`edit` 如何与 bind mount 与 SELinux 交互。
- [指南：审计 + 审批策略](/zh-Hans/guides/audit-approval-policies/) —— pattern 正则如何约束每个工具的输入。
- [开发者指南：添加工具](/zh-Hans/developer-guide/add-a-tool/) —— 扩展这组工具。
