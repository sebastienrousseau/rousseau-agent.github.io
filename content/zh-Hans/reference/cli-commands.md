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
description: "Compact reference table of every rousseau-agent command mirroring the output of rousseau --help."
keywords: "cli, commands, reference, table, rousseau --help"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/reference/cli-commands/"
subtitle: "Every command tabulated."
tags: "reference, cli, commands"
title: "CLI 命令"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cli, commands, reference, table, rousseau --help"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "CLI 命令"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 50
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/reference/cli-commands/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/cli-commands/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "CLI 命令"
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
twitter_description: "Compact reference table of every rousseau-agent command mirroring the output of rousseau --help."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "CLI 命令"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">您将学到</span><p>完整的 <code>rousseau</code> CLI 面：每个命令、其 flag、退出码语义，以及每个 flag 所覆盖的配置键。这是可快速浏览的参考 —— 附有可行示例的演练请见 <a href="/zh-Hans/user-guide/cli/">用户指南：CLI</a>。</p></aside>

## 命令树

每个命令都通过 `rousseau <cmd> --help` 展示其帮助。本页是表格化摘要。

| 命令 | 描述 |
|---|---|
| `chat` | 打开交互式 Bubble Tea TUI。 |
| `whatsapp` | 运行 WhatsApp 桥（whatsmeow）。 |
| `signal` | 运行 Signal 桥（signal-cli JSON-RPC）。 |
| `telegram` | 运行 Telegram Bot API 长轮询。 |
| `matrix` | 运行 Matrix client-server 桥。 |
| `slack` | 运行 Slack Socket Mode 桥。 |
| `discord` | 运行 Discord Gateway 桥。 |
| `sms` | 通过 Twilio 或 Vonage 的仅发送 SMS。 |
| `imessage` | 基于 BlueBubbles 的 iMessage 桥。 |
| `email` | IMAP 入站 + SMTP 出站桥。 |
| `mcp` | 在 stdio 上启动 MCP JSON-RPC 2.0 服务器。 |
| `cron add` | 添加一个定时提示。 |
| `cron list` | 列出所有定时任务。 |
| `cron remove` | 删除一个定时任务。 |
| `cron enable` | 启用一个已停用的定时任务。 |
| `cron disable` | 停用一个已启用的定时任务。 |
| `session list` | 列出存储中的会话，最新在前。 |
| `session search` | 跨每个会话的消息内容进行 FTS5 搜索。 |
| `session show` | 打印一个会话的消息历史。 |
| `session delete` | 删除一个会话。 |
| `skills list` | 列出从 `skills_dir` 发现的 skill。 |
| `skills show` | 打印 skill 的 YAML front-matter 与主体。 |
| `skills lint` | 校验 skill 是否符合 schema。 |
| `doctor` | 诊断本地安装。打印一份报告。 |
| `status` | 打印守护进程状态。 |
| `init` | 向 `~/.config/rousseau/` 写入默认配置。 |
| `version` | 打印版本、commit 与构建日期。 |

## 全局 flag

每个命令都接受：

| Flag | 类型 | 配置键 | 说明 |
|---|---|---|---|
| `--config` | string | — | 从该文件加载配置。默认：`$XDG_CONFIG_HOME/rousseau/config.yaml`。 |
| `--help`、`-h` | bool | — | 打印当前命令的帮助。 |

## 各传输的 flag

### `rousseau whatsapp`

| Flag | 类型 | 配置键 | 说明 |
|---|---|---|---|
| `--store` | string | — | whatsmeow 设备存储的路径。默认 `$XDG_DATA_HOME/rousseau/whatsapp.db`。 |
| `--allow` | []string | `whatsapp.allowlist` | 将入站限制到这些 JID。可重复。 |

### `rousseau slack`

| Flag | 类型 | 配置键 |
|---|---|---|
| `--app-token` | string | `slack.app_token` |
| `--bot-token` | string | `slack.bot_token` |
| `--bot-user-id` | string | `slack.bot_user_id` |
| `--allow` | []string | `slack.allowlist` |

### `rousseau discord`

| Flag | 类型 | 配置键 |
|---|---|---|
| `--token` | string | `discord.token` |
| `--allow` | []string | `discord.allowlist` |

### `rousseau telegram`

| Flag | 类型 | 配置键 |
|---|---|---|
| `--token` | string | `telegram.token` |
| `--allow` | []string | `telegram.allowlist` |

### `rousseau matrix`

| Flag | 类型 | 配置键 |
|---|---|---|
| `--homeserver-url` | string | `matrix.homeserver_url` |
| `--access-token` | string | `matrix.access_token` |
| `--user-id` | string | `matrix.user_id` |
| `--allow` | []string | `matrix.allowlist` |

### `rousseau signal`

| Flag | 类型 | 配置键 |
|---|---|---|
| `--account` | string | `signal.account` |
| `--binary` | string | `signal.binary` |
| `--allow` | []string | `signal.allowlist` |

### `rousseau email`

| Flag | 类型 | 配置键 |
|---|---|---|
| `--imap-addr` | string | `email.imap_addr` |
| `--imap-username` | string | `email.imap_username` |
| `--imap-password` | string | `email.imap_password` |
| `--smtp-addr` | string | `email.smtp_addr` |
| `--smtp-username` | string | `email.smtp_username` |
| `--smtp-password` | string | `email.smtp_password` |
| `--from` | string | `email.from` |
| `--mailbox` | string | `email.mailbox` |
| `--poll-interval` | string | `email.poll_interval` |

### `rousseau sms`

| Flag | 类型 | 配置键 |
|---|---|---|
| `--provider` | string | `sms.provider` |
| `--from` | string | `sms.from` |
| `--to` | string | （位置参数） |

### `rousseau imessage`

| Flag | 类型 | 配置键 |
|---|---|---|
| `--base-url` | string | `imessage.base_url` |
| `--password` | string | `imessage.password` |
| `--chat-guid` | string | `imessage.chat_guid` |

## 退出码

| 码 | 含义 |
|---|---|
| 0 | 干净退出 —— 命令已完成。对长生命周期守护进程而言并不常见（它们通常在收到信号时终止）。 |
| 1 | `Execute` 抛出的任何错误。分类参见 [参考：退出码](/zh-Hans/reference/exit-codes/)。 |

## 优先级

配置值按 **flag > env > file > default** 顺序解析（参见 `internal/config/config.go` 中的 `config.Load`）。环境变量前缀为 `ROUSSEAU_`，点号替换为下划线 —— 例如 `ROUSSEAU_ANTHROPIC_MODEL` 覆盖 `anthropic.model`。裸的 `ANTHROPIC_API_KEY` 环境变量也被认可（在 `config.Load` 中做了特殊处理）。

## 故障排除

### 在 `rousseau chat` 上出现 `unknown flag: --allow`

`--allow` 是传输作用域。`chat` 没有允许列表，因为没有入站。请改用 `rousseau whatsapp --allow …`。

### 对可重复的 flag，flag 顺序很重要

`--allow A --allow B` 是两个值，而 `--allow=A,B` 是一个恰好包含逗号的单值。请使用分离的 flag。

### 环境变量覆盖未被采纳

Rousseau 只在启动时读取环境变量。改变环境变量后请重启守护进程，或使用 `--config` 强制重新加载。

### `flag provided but not defined`

Cobra 拒绝未知 flag。若您从新版本复制了一个 flag，请以 `rousseau <cmd> --help` 检查当前拼写。

## 相关页面

- [用户指南：CLI](/zh-Hans/user-guide/cli/) —— 每个命令附带可行示例。
- [参考：退出码](/zh-Hans/reference/exit-codes/) —— 信号语义。
- [参考：配置 schema](/zh-Hans/reference/config-schema/) —— 每个配置字段。
- [参考：环境变量](/zh-Hans/reference/environment-variables/) —— 环境变量覆盖矩阵。
- [配置](/zh-Hans/configuration/) —— 完整配置文件演练。

## 延伸阅读

- `internal/cli/root.go` —— Cobra 命令树。
- `internal/cli/*.go` —— 每个子命令一个文件。
- `internal/config/config.go` —— `Load` 与默认值解析。
