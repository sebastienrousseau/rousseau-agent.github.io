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
description: "Full CLI reference for rousseau-agent: every command, every flag, exit codes, per-transport subcommands."
keywords: "cli, cobra, commands, flags, subcommands, exit codes"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/user-guide/cli/"
subtitle: "Every command, every flag."
tags: "cli, reference, commands"
title: "CLI 参考"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cli, cobra, commands, flags, subcommands, exit codes"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "CLI 参考"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 40
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/user-guide/cli/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/cli/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "CLI 参考"
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
twitter_description: "Full CLI reference for rousseau-agent: every command, every flag, exit codes, per-transport subcommands."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "CLI 参考"
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

## 调用

```
rousseau [--config <path>] <command> [flags]
```

每个命令都从 `~/.config/rousseau/config.yaml`（或通过 `--config` 传入的文件）读取默认值。Flag 覆盖环境变量，环境变量覆盖文件，文件覆盖硬编码默认值。

## 全局 flag

| Flag | 类型 | 默认 | 说明 |
|---|---|---|---|
| `--config` | string | `$XDG_CONFIG_HOME/rousseau/config.yaml` | 从此文件加载配置。缺省表示默认 XDG 路径。 |
| `--help`、`-h` | bool | — | 打印当前命令的帮助。 |

## 命令树

```
rousseau
├── chat                Bubble Tea TUI
├── whatsapp            WhatsApp 桥（whatsmeow）
├── signal              Signal 桥（signal-cli JSON-RPC）
├── telegram            Telegram Bot API 长轮询
├── matrix              Matrix 客户端-服务端 API
├── slack               Slack Socket Mode
├── discord             Discord Gateway
├── sms                 SMS 仅发送（Twilio / Vonage）
├── imessage            BlueBubbles 后端的 iMessage 桥
├── email               IMAP 入站 + SMTP 出站
├── mcp                 stdio 上的 MCP JSON-RPC 2.0 服务器
├── cron                管理定时提示
├── session             检查 / 删除会话存储
├── skills              列出 / 显示 / lint skills
├── doctor              诊断本地安装
├── status              打印守护进程状态
├── init                向 ~/.config/rousseau/ 写入默认配置
└── version             打印版本、commit、构建日期
```

## `rousseau chat`

打开交互式 Bubble Tea TUI。

| Flag | 类型 | 默认 | 说明 |
|---|---|---|---|
| `--session` | string | — | 按 ID 恢复现有会话。 |
| `--title` | string | 时间戳 | 新会话的标题。 |

## `rousseau whatsapp`

运行 WhatsApp 桥。首次启动时打印 QR 码。

| Flag | 类型 | 默认 | 说明 |
|---|---|---|---|
| `--store` | string | `$XDG_DATA_HOME/rousseau/whatsapp.db` | whatsmeow 设备存储的路径。 |
| `--allow` | []string | 无 | 将入站处理限制在这些 JID。可重复。**在公开号码上绝不要留空。** |

## `rousseau signal`

运行 Signal 桥。以子进程方式启动 `signal-cli jsonRpc`。

| Flag | 类型 | 默认 | 说明 |
|---|---|---|---|
| `--account` | string | 来自 `signal.account` | 守护进程运行时使用的 E.164 电话号码。 |
| `--binary` | string | `signal-cli` | signal-cli 可执行文件的路径。 |
| `--allow` | []string | 无 | 将入站限制到这些 E.164 号码。 |

## `rousseau telegram`

运行 Telegram Bot API 长轮询器。

| Flag | 类型 | 默认 | 说明 |
|---|---|---|---|
| `--token` | string | 来自 `telegram.token` | BotFather token。 |
| `--allow` | []string | 无 | 将入站限制到这些聊天 ID。 |

## `rousseau matrix`

运行 Matrix 桥。

| Flag | 类型 | 默认 | 说明 |
|---|---|---|---|
| `--homeserver-url` | string | 来自配置 | 例如 `https://matrix.org`。 |
| `--access-token` | string | 来自配置 | 机器人的 access token。 |
| `--user-id` | string | 来自配置 | 机器人的 Matrix 用户 ID（`@bot:matrix.org`）。 |
| `--allow` | []string | 无 | 将入站限制到这些用户 ID。 |

## `rousseau slack`

运行 Slack Socket Mode 桥。

| Flag | 类型 | 默认 | 说明 |
|---|---|---|---|
| `--app-token` | string | 来自配置 | `xapp-...` Socket Mode token。 |
| `--bot-token` | string | 来自配置 | `xoxb-...` Bot User OAuth token。 |
| `--allow` | []string | 无 | 将入站限制到这些 Slack 用户 ID。 |

## `rousseau discord`

运行 Discord Gateway 桥。

| Flag | 类型 | 默认 | 说明 |
|---|---|---|---|
| `--token` | string | 来自配置 | 机器人 token。 |
| `--allow` | []string | 无 | 将入站限制到这些 Discord 用户 ID。 |

## `rousseau sms`

通过 Twilio 或 Vonage 仅发送 SMS。无入站。

| Flag | 类型 | 默认 | 说明 |
|---|---|---|---|
| `--provider` | string | 来自配置 | `twilio` 或 `vonage`。 |
| `--from` | string | 来自配置 | E.164 发送号码。 |
| `--account-sid` | string | 来自配置 | Twilio Account SID。 |
| `--auth-token` | string | 来自配置 | Twilio auth token 或 Vonage secret。 |
| `--api-key` | string | 来自配置 | Vonage API key。 |

## `rousseau imessage`

BlueBubbles 后端的 iMessage 桥。

| Flag | 类型 | 默认 | 说明 |
|---|---|---|---|
| `--base-url` | string | `http://localhost:1234` | BlueBubbles 服务器 URL。 |
| `--password` | string | 来自配置 | BlueBubbles 服务器密码。 |
| `--chat-guid` | string | 来自配置 | 出站目标。 |
| `--poll-interval` | duration | 5s | 轮询新消息的频率。 |
| `--allow` | []string | 无 | 限制入站。 |

## `rousseau email`

通过 IMAP + SMTP 的 Email 桥。

| Flag | 类型 | 默认 | 说明 |
|---|---|---|---|
| `--imap-addr` | string | 来自配置 | 例如 `imap.example.com:993`。 |
| `--imap-username`、`--imap-password` | string | 来自配置 | IMAP 凭据。 |
| `--smtp-addr` | string | 来自配置 | 例如 `smtp.example.com:587`。 |
| `--smtp-username`、`--smtp-password` | string | 来自配置 | SMTP 凭据。 |
| `--from` | string | 来自配置 | 信封发送方。 |
| `--poll-interval` | duration | 30s | IMAP 轮询频率。 |
| `--allow` | []string | 无 | 限制入站发件地址。 |

## `rousseau mcp`

在 stdio 上启动 MCP 服务器。无 flag —— 所有旋钮都在 `config.yaml` 中。

## `rousseau cron`

| 子命令 | 说明 |
|---|---|
| `cron add` | 添加定时提示。Flag：`--name`、`--schedule`（5 字段 cron）、`--prompt`、`--deliver-to`。 |
| `cron list` | 列出每个任务，带 `on/off` 状态与最后运行时间戳。 |
| `cron remove <name-or-id>` | 删除任务。 |
| `cron enable <name-or-id>` | 启用一个已停用的任务。 |
| `cron disable <name-or-id>` | 停用一个已启用的任务（不删除）。 |

## `rousseau session`

| 子命令 | 说明 |
|---|---|
| `session list` | 列出存储中的会话，最新在前。 |
| `session search <query>` | 跨每个会话消息内容的 FTS5 搜索。 |
| `session show <id>` | 打印一个会话的消息历史。 |
| `session delete <id>` | 删除一个会话。 |

## `rousseau skills`

| 子命令 | 说明 |
|---|---|
| `skills list` | 列出从 `skills_dir` 发现的 skills。 |
| `skills show <name>` | 打印一个 skill 的 YAML 前置元数据与正文。 |
| `skills lint` | 校验 skills 是否符合 schema。 |

## `rousseau doctor`

走一遍每个运行时依赖与每项配置选择。打印带 `ok`、`warn`、`fail`、`info` 标签的状态报告。如果任一行为 `fail`，退出码为 1。

目前无 flag；通过全局层面的 `--config` 扩展。

## `rousseau status`

打印一份精简的守护进程状态摘要 —— provider、会话数量、cron 任务。只读。

## `rousseau init`

向 `~/.config/rousseau/` 写入默认 `config.yaml`。除非传入 `--force`，否则拒绝覆盖已有文件。

| Flag | 类型 | 默认 | 说明 |
|---|---|---|---|
| `--force` | bool | false | 覆盖现有配置。 |

## `rousseau version`

打印版本、commit 哈希与构建日期。通过 `-ldflags` 在构建时打戳。

## 退出码

| 码 | 含义 |
|---|---|
| 0 | 命令成功完成。 |
| 1 | 命令失败。错误打印到 stderr。 |

守护进程信号语义见 [参考：退出码](/zh-Hans/reference/exit-codes/)。

## 环境变量

每个配置字段都可以通过环境变量覆盖，前缀为 `ROUSSEAU_`，以 `_` 作为节分隔符：`ROUSSEAU_LOG_LEVEL=debug`、`ROUSSEAU_ANTHROPIC_API_KEY=sk-ant-...` 等。

特殊情况是 `ANTHROPIC_API_KEY`（不带前缀）—— 为遵循惯例，配置加载器会直接拾取它。

## 故障排除

### 传子命令时出现 `unknown command`

Rousseau 的子命令在 `internal/cli/root.go` 中声明。如果 `rousseau <cmd>` 报告 unknown，要么是 flag 拼错，要么您使用的是较旧的二进制。`rousseau version` 显示您手上的版本。

### 可重复 flag 需要多次调用

`--allow` 每个 flag 接受一个 JID。要传多个值就重复该 flag：`--allow A --allow B`，而不是 `--allow A,B`。

### 环境变量被静默忽略

Rousseau 使用 `ROUSSEAU_` 前缀 + 下划线节分隔符：`anthropic.model` 变成 `ROUSSEAU_ANTHROPIC_MODEL`。区分大小写。

### `rousseau chat` 只显示空白屏幕

Bubble Tea TUI 需要一个支持 ANSI 的终端。设置 `TERM=xterm-256color` 并交互式运行（不要在 `nohup` 或管道下运行）。

### 命令立即以 0 退出

一些 flag（`--help`、`--version` 变体）会短路。如果您的命令没有运行，检查您传的 flag。

## 相关页面

- [用户指南：TUI](/zh-Hans/user-guide/tui/) —— `rousseau chat` 内的键位映射。
- [用户指南：工具](/zh-Hans/user-guide/tools/) —— 每个内置工具的 JSON schema。
- [参考：CLI 命令](/zh-Hans/reference/cli-commands/) —— 命令表。
- [参考：环境变量](/zh-Hans/reference/environment-variables/) —— 覆盖矩阵。
- [配置](/zh-Hans/configuration/) —— 支撑每个命令的配置文件。

## 延伸阅读

- `internal/cli/root.go` —— Cobra 树。
- `internal/cli/chat.go`、`internal/cli/whatsapp.go`、`internal/cli/slack.go`、…… —— 每个子命令一个文件。
- `internal/config/config.go` —— 环境变量 / flag 解析。
