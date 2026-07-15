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
description: "Bubble Tea TUI keybindings, panels, spinner and streaming semantics for rousseau-agent's rousseau chat command."
keywords: "tui, bubble tea, keybindings, viewport, textarea, spinner, streaming, session"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/user-guide/tui/"
subtitle: "Bubble Tea keybindings, panels, streaming."
tags: "tui, bubble-tea, keybindings"
title: "TUI"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tui, bubble tea, keybindings, viewport, textarea, spinner, streaming, session"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "TUI"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/user-guide/tui/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/tui/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "TUI"
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
twitter_description: "Bubble Tea TUI keybindings, panels, spinner and streaming semantics for rousseau-agent's rousseau chat command."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "TUI"
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

## 概览

`rousseau chat` 打开一个带三个区域的 Bubble Tea TUI：

```
+------------------------------------------------------+
|                       Header                         |  会话标题
+------------------------------------------------------+
|                                                      |
|                                                      |
|                     Viewport                         |  可滚动历史
|          （消息、流式回复预览）                        |
|                                                      |
|                                                      |
+------------------------------------------------------+
|                     Textarea                         |  输入，Enter 发送
+------------------------------------------------------+
| status: idle | spinner | streaming | error           |
+------------------------------------------------------+
```

在 Bubble Tea 的 alt-screen 模式下运行 —— TUI 接管终端缓冲区并在退出时恢复。

## 键位映射

Rousseau 的 TUI 保持键位集合较小。有疑问时，标准的 Bubble Tea viewport / textarea 快捷键适用。

### 全局

| 键 | 动作 |
|---|---|
| `Ctrl+C` | 退出。保存当前会话，退出时不打印任何东西。 |
| `Esc` | 退出。与 `Ctrl+C` 相同。 |
| `Enter` | 发送当前 textarea 内容。代理繁忙时为 no-op。 |

### Textarea（输入）

标准 Bubble Tea textarea 行为：

| 键 | 动作 |
|---|---|
| 任意可打印字符 | 在光标处插入。 |
| `Backspace` | 删除光标前的字符。 |
| `Delete` | 删除光标下的字符。 |
| 方向键 | 移动光标。 |
| `Home` / `End` | 跳到行首 / 行尾。 |
| `Ctrl+A` / `Ctrl+E` | 跳到行首 / 行尾（Emacs 键位）。 |
| `Ctrl+U` | 剪切到行首。 |
| `Ctrl+K` | 剪切到行尾。 |
| `Shift+Enter` | （视终端而定）不提交的换行；通常映射为字面 `\n`。 |

textarea 随内容换行竖向增长；viewport 相应缩小。

### Viewport（历史）

viewport 支持常用的 Bubble Tea viewport 快捷键。textarea 为空时焦点在 viewport 上；打字会自动路由到 textarea。

| 键 | 动作 |
|---|---|
| `PgUp` / `PgDn` | 滚动一页。 |
| `↑` / `↓` | 滚动一行。 |
| `Home` / `End` | 跳到顶部 / 底部。 |
| 鼠标滚轮 | 滚动。 |

## 面板语义

### Header

`rousseau · <session title>`。标题来自会话创建时的 `--title`（默认：`chat YYYY-MM-DD HH:MM`）。

### Viewport

渲染的历史加上，当一次轮次进行中时，底部的**流式预览**。预览在 provider 流式过程中反映增量；轮次结束时，预览被最终的助手消息取代。

每条消息都以其角色（`you`、`rousseau`、`tool`）为前缀，因此当模型请求工具调用时流程也清晰。

### Textarea

占位文本：`Ask, or press Ctrl+C to quit…`。Enter 提交；textarea 在提交时重置。

当代理繁忙时，`Enter` 是 no-op，避免意外双击提交把轮次堆叠。

### 状态行

在 textarea 下方。内容各异：

| 状态 | 行 |
|---|---|
| Idle | 空。 |
| Busy | Spinner + `thinking…`。Spinner tick 来自 `bubbles/spinner`。 |
| Streaming | Spinner 继续；流式增量出现在 viewport 预览。 |
| Error | 红色错误字符串。下一次成功轮次清除它。 |

## 会话持久化

每一轮通过 `state.Store.Save` 持久化到 `~/.local/share/rousseau/sessions.db`。如果守护进程在轮次中崩溃：

- 用户轮次已经保存（它在 `doTurn` 触发之前追加）。
- 助手回复只在轮次完成时保存。

重启后，`rousseau chat --session <id>` 从最后一次成功保存的状态恢复。

## 从 CLI 使用会话命令

TUI 不表面每一项会话操作。从 shell 管理会话：

```sh
rousseau session list
rousseau session show <id>
rousseau session search "kubectl"
rousseau session delete <id>
```

## 流式语义

实现 `StreamingProvider.ChatStream` 的 provider（Anthropic、`claudecli`）会把增量流入 viewport 预览。只实现 `Provider.Chat` 的 provider（Bedrock、Vertex、视 shim 而定的 OpenAI 兼容）在轮次完成时一次性交付回复 —— 预览保持为空，`busy` 变为 `false` 时回复出现。

## 出问题时

- **TUI 挂起** —— 按两次 `Ctrl+C`。第一次 `Ctrl+C` 发出 `tea.Quit` 信号，会刷盘状态。第二次由操作系统捕获。
- **viewport 为空且 textarea 不接受输入** —— alt-screen 可能被一个发出转义序列的子进程破坏（例如一个打印 ANSI 代码的工具调用）。重启 TUI。
- **状态行停在 `thinking…`** —— provider 没有返回。检查守护进程的 stderr（rousseau 把 slog 写到 stderr；如果您把它管道走了，请重新浮现）。

## 下一步

- [用户指南：CLI](/zh-Hans/user-guide/cli/) —— TUI 之外的每个命令。
- [概念](/zh-Hans/concepts/) —— 底下的代理循环。
- [压缩 + 回忆](/zh-Hans/user-guide/compression-recall/) —— 长聊天如何保持可用。
