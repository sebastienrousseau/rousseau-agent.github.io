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
description: "Wire rousseau-agent to a Slack channel that runs read and grep over the workspace whenever an operator asks."
keywords: "slack, code review, socket mode, read tool, grep tool, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/tutorials/build-a-code-review-bot/"
subtitle: "A Slack channel that lets rousseau review a repo on demand."
tags: "tutorials, slack, code review, socket mode, read, grep"
title: "教程：构建代码审查机器人"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "slack, code review, socket mode, read tool, grep tool, allowlist"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "教程：构建代码审查机器人"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 42
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/tutorials/build-a-code-review-bot/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/build-a-code-review-bot/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "教程：构建代码审查机器人"
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
twitter_description: "Wire rousseau-agent to a Slack channel that runs read and grep over the workspace whenever an operator asks."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "教程：构建代码审查机器人"
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

## 你要构建什么

一个私有 Slack 频道，团队成员在其中 @ `@rousseau` 并附上仓库路径和问题。Rousseau 会检出工作区，运行 `internal/tools/builtin/` 中的 `read` 和 `grep`，并回复带引用行号的答复。没有公开的 HTTP 接口 —— Slack Socket Mode 通过出站 WebSocket 驱动一切。

预计耗时：20 分钟，前提是你已经拥有 Slack 工作区的管理员权限。

## 先决条件

- 已安装 Rousseau 并配置了 provider（参见 [Quickstart](/zh-Hans/quickstart/)）。
- 具备 Slack 工作区管理员权限。
- 已在 `$HOME` 下某路径检出的仓库 —— 它将成为 bot 可以 `read`/`grep` 的“工作区”。

## 步骤 1：创建一个 Slack 应用

Slack 的 Socket Mode 是让此 bot 成为可能的关键：你的守护进程向 Slack 打开一个出站 WebSocket，无需入站接口。

1. 前往 <https://api.slack.com/apps>，选择 **from scratch** 新建一个应用。
2. 在 **Socket Mode** 中启用它，并生成一个具有 `connections:write` 的 **app-level token**。复制 `xapp-...` 值。
3. 在 **OAuth & Permissions** 下，添加以下 **Bot Token Scopes**：
   - `chat:write`
   - `app_mentions:read`
   - `channels:history`（私有频道使用 `groups:history`）
4. 将应用安装到你的工作区。复制 **Bot User OAuth Token** —— 即 `xoxb-...` 值。
5. 在 **Event Subscriptions** 下启用事件，并为 bot 订阅 `app_mention` 与 `message.channels`（或 `message.groups`）。
6. 将 bot 邀请到评审频道：`/invite @rousseau`。

## 步骤 2：配置 rousseau

添加到 `~/.config/rousseau/config.yaml`。相关字段来自 `internal/config/config.go` 中的 `SlackConfig`：

```yaml
provider: claudecli           # or anthropic — whatever you set in Quickstart

slack:
  app_token:  xapp-1-…
  bot_token:  xoxb-…
  bot_user_id: U0ROUSSEAU     # from https://api.slack.com/methods/auth.test
  reply_header: "*rousseau-agent*\n\n"
  allowlist:
    - U01ABC…                 # your Slack user IDs

agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
    # no bash, no write, no edit — read-only reviewer
```

`allowlist` 限制路由器会接受哪些发送者的消息。`internal/transport/router.go` 中的路由器会对其他任何发送者输出 `transport.rejected`。

## 步骤 3：运行桥

```sh
rousseau slack \
  --app-token "$SLACK_APP_TOKEN" \
  --bot-token "$SLACK_BOT_TOKEN" \
  --bot-user-id "$SLACK_BOT_USER_ID"
```

`--bot-user-id` 可防止 bot 回复自身消息。`internal/transport/slack/client.go` 输出的结构化日志会显示：

```
INFO slack.started
INFO slack.incoming from=U01ABC channel=C01REVIEW text="…"
INFO tool.execute name=read id=t_1
INFO tool.execute name=grep id=t_2
```

## 步骤 4：试用

在评审频道中：

```
@rousseau look under /home/seb/repos/acme-api and tell me
where request logging is set up
```

`claudecli` provider（或 Anthropic —— 无论你选哪个）会针对工作区绑定挂载调用 `internal/tools/builtin/` 中的 `read` 和 `grep`。因为审批器运行在 `pattern` 模式且只有 `read` 和 `grep` 被放行，即使被污染的提示词要求，模型也无法写入或调用 shell。

## 步骤 5：加固

pattern 模式的审批器是**对 JSON 工具输入的正则匹配**。要将 `read` 与 `grep` 限制到某个具体的项目树：

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: "\"path\":\"/home/seb/repos/acme-api/[^\"]*\""}
      - {tool: grep, match: "\"path\":\"/home/seb/repos/acme-api\""}
```

关于 `default: deny` + 审计的完整演练，请参见 [教程：加固审批器](/zh-Hans/tutorials/harden-approver-policy/)。

## 通过 systemd 部署

超出笔记本会话的任何场景，都应在位于 `docker/rousseau-agent.container` 的 Podman Quadlet 单元下运行 Slack 桥 —— 把 `Exec=whatsapp --allow …` 换成 `Exec=slack --app-token … --bot-token …`。完整 unit 见 [部署](/zh-Hans/deployment/)。

## 相关

- [传输：Slack](/zh-Hans/transports/slack/)
- [用户指南：审批策略](/zh-Hans/user-guide/approval-policies/)
- [用户指南：工具](/zh-Hans/user-guide/tools/)
- [教程：加固审批器](/zh-Hans/tutorials/harden-approver-policy/)
