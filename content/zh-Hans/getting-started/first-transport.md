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
description: "End-to-end walkthrough for wiring your first chat transport. Uses WhatsApp as the canonical example: pair, allowlist, send a test message, verify the reply."
keywords: "first transport, whatsapp, pairing, allowlist, e2e walkthrough, test message"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/getting-started/first-transport/"
subtitle: "End-to-end WhatsApp walkthrough: pair, allowlist, verify."
tags: "first-transport, whatsapp, walkthrough"
title: "你的第一个传输"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "first transport, whatsapp, pairing, allowlist, e2e walkthrough, test message"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "你的第一个传输"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 25
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/getting-started/first-transport/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/first-transport/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "你的第一个传输"
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
twitter_description: "End-to-end walkthrough for wiring your first chat transport. Uses WhatsApp as the canonical example: pair, allowlist, send a test message, verify the reply."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "你的第一个传输"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">你将学到</span><p>如何将一个聊天传输与 rousseau 守护进程配对，将驱动它的 JID/用户 ID 加入允许列表，发送第一条测试消息，并确认回复。WhatsApp 是标准演练，因为其配对最为严格；下方标签页展示 Slack 和 Discord 的并行演练。</p></aside>

## 选择你的第一个传输

每个传输都是同一个 `transport.Transport` 接口下的薄适配器——允许列表、会话路由和定时投递在所有传输中都相同。差异在于配对 UX 和每种传输的标识符格式（JID、用户 ID、房间 ID）。选择你能最快配对的那个：

<div class="tabs" data-tabs="first-transport">
  <div class="tab-list" role="tablist" aria-label="First transport">
    <button role="tab" aria-selected="true">WhatsApp</button>
    <button role="tab" aria-selected="false">Slack</button>
    <button role="tab" aria-selected="false">Discord</button>
    <button role="tab" aria-selected="false">Telegram</button>
    <button role="tab" aria-selected="false">Signal</button>
  </div>
  <div class="tab-panel" role="tabpanel">

WhatsApp 是参考——配对最难，测试最容易（你手机上已经有该 app）。

**先决条件：** 装有 WhatsApp 的手机、你的 E.164 JID（例如 `447900123456@s.whatsapp.net`）。

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

从 **WhatsApp &gt; 设置 &gt; 已链接的设备 &gt; 链接设备** 扫描二维码。向自己发送 `hello`；rousseau 会通过 WhatsApp 回复。完整演练见下方。

<aside class="admonition" data-type="warning"><span class="admonition-title">非官方协议</span><p>WhatsApp 支持使用 <code>whatsmeow</code>——一个逆向工程客户端。Meta 偶尔会封禁运行非官方客户端的号码。请不要在你依赖的号码上运行它。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**先决条件：** Slack 工作区管理员权限、在 [api.slack.com/apps](https://api.slack.com/apps) 创建的应用、已启用 Socket Mode。

1. 创建一个 Slack 应用，在 <em>Settings &gt; Socket Mode</em> 下启用 **Socket Mode**。
2. 创建一个具有 `connections:write` 权限的 **应用级令牌**——即 `xapp-…` 令牌。
3. 在 <em>OAuth &amp; Permissions</em> 下添加机器人作用域 `chat:write`、`im:history`、`im:read`、`im:write`、`mpim:history`、`mpim:read`。安装到工作区以获取 `xoxb-…` 机器人令牌。
4. 在 <em>Event Subscriptions</em> 下订阅 `message.im`（DM）以及任何你需要的频道事件。

```sh
rousseau slack --app-token xapp-... --bot-token xoxb-... --allow U01234567
```

在 Slack 中对机器人发送 DM；rousseau 在同一 DM 中回复。完整演练与 OAuth 作用域理由参见 [传输：Slack](/zh-Hans/transports/slack/)。

<aside class="admonition" data-type="tip"><span class="admonition-title">无需公开 HTTP</span><p>Socket Mode 意味着守护进程出站连接 Slack 的 WebSocket。你无需公开 webhook、ngrok 或 ingress。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**先决条件：** 在 [discord.com/developers/applications](https://discord.com/developers/applications) 创建的 Discord 应用、一个机器人用户、在 <em>Bot</em> 下启用 **Message Content Intent**。

1. 创建应用、添加机器人、复制机器人令牌。
2. 在 <em>Bot &gt; Privileged Gateway Intents</em> 下启用 **Message Content Intent**。若不启用，消息文本会为空。
3. 通过 <em>OAuth2 &gt; URL Generator</em> 邀请机器人——作用域 `bot`，权限 `Send Messages`、`Read Message History`。

```sh
rousseau discord --token <bot-token> --allow 234567890123456789
```

给机器人发 DM；rousseau 回复。权限与 intent 深入解析参见 [传输：Discord](/zh-Hans/transports/discord/)。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**先决条件：** 通过 [@BotFather](https://t.me/BotFather) 创建的 Telegram 机器人。

1. 私聊 `@BotFather`，发送 `/newbot`，按提示操作。复制令牌。
2. 与你的机器人交流至少一次以便 Telegram 创建会话。

```sh
rousseau telegram --token 1234567890:AA... --allow 987654321
```

`--allow` 的值是 Telegram 的数字用户 ID（而非用户名）。通过给 [@userinfobot](https://t.me/userinfobot) 发消息获取。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**先决条件：** 已安装 `signal-cli` 并链接到 Signal 账户。配对流程参见 [signal-cli 文档](https://github.com/AsamK/signal-cli)。

```sh
rousseau signal --account +447900123456 --allow +447900654321
```

Rousseau 将 `signal-cli` 作为子进程启动（见 `internal/cli/signal.go`）并通过 JSON-RPC 与它通信。参见 [传输：Signal](/zh-Hans/transports/signal/)。

  </div>
</div>

## 为什么用 WhatsApp 演练

本页其余部分以 WhatsApp 为标准示例——只要你在这里理解了模式，其他每一种传输都是它的变体（把一个稳定 ID 加入允许列表，跑一次配对 UX，发一条测试消息，确认回复）。如果你已经拿到令牌，可以直接跳到对应传输页：

- [Slack](/zh-Hans/transports/slack/)——Socket Mode 令牌与事件订阅。
- [Discord](/zh-Hans/transports/discord/)——机器人令牌、intent、权限整数。
- [Telegram](/zh-Hans/transports/telegram/)——BotFather 令牌。
- [Signal](/zh-Hans/transports/signal/)——signal-cli 子进程。
- [Matrix](/zh-Hans/transports/matrix/)——homeserver URL + 访问令牌。

## 先决条件

- `rousseau` 位于 `$PATH` 中（参见 [安装](/zh-Hans/getting-started/installation/)）。
- 一个可用的提供方——默认为继承 Claude Code 认证的 `claudecli`；其他都需要先填好配置（参见 [配置](/zh-Hans/configuration/)）。
- 装有 WhatsApp 的手机。你的 E.164 电话 JID（例如 `447900123456@s.whatsapp.net`）。

## 第 1 步 —— 选择驱动守护进程的 JID

Rousseau 使用允许列表把入站处理限制到一组固定的 JID。其他发送者会被静默丢弃。这一点至关重要：没有允许列表，任何知道该号码的人都能驱动 agent。

你的 E.164 JID 就是你的电话号码，只保留数字，后接 `@s.whatsapp.net`：

```
447900123456@s.whatsapp.net
```

群 JID 以 `@g.us` 结尾；守护进程也支持，但请先从个人 JID 开始。

## 第 2 步 —— 首次启动与配对

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

首次启动时，一个二维码会打印到 stdout。在手机上打开 WhatsApp，进入 **设置 → 已链接的设备 → 链接设备**，扫描二维码。

守护进程会打印类似内容：

```
whatsapp.starting store=file:/home/you/.local/share/rousseau/whatsapp.db?_pragma=... allowlist=1
```

扫描后，whatsmeow 会把设备凭证持久化到 `whatsapp.db`。此后的启动都会静默连接——不再出现二维码。

## 第 3 步 —— 发送测试消息

在手机上向自己发送 `hello`。守护进程会记录入站事件、分发到 agent，并按配置的 header 通过 WhatsApp 回复：

```
💎 *Rousseau Agent*

Hello — what would you like to work on?
```

回复 header 可通过 `whatsapp.reply_header` 配置。设为单个空格即可禁用前缀。

## 第 4 步 —— 设置 `config.yaml` 从而不必使用长选项

创建 `~/.config/rousseau/config.yaml`：

```yaml
provider: claudecli

claudecli:
  binary: claude
  permission_mode: bypassPermissions

whatsapp:
  reply_header: "💎 *Rousseau Agent*\n\n"
```

现在 `rousseau whatsapp --allow 447900123456@s.whatsapp.net` 会自动读取 header。每个传输都从同一个文件读取自己的配置块——完整列表参见 [配置](/zh-Hans/configuration/)。

`bypassPermissions` 是无人值守守护进程的默认值，因为终端另一端没有人可以交互式批准工具调用。在将守护进程指向你在意的任何目标之前，**请先设置好审批策略**（[用户指南：审批策略](/zh-Hans/user-guide/approval-policies/)）。

## 第 5 步 —— 端到端确认

在手机上发送一个编码问题：

```
Read the file at /workspace/README.md and summarise it in 3 bullets.
```

守护进程会执行一次 `read` 工具调用、把文件喂给模型，并把摘要通过消息回复给你。你刚刚闭合了整个回路：

- 手机 → WhatsApp → whatsmeow WebSocket
- rousseau-agent → agent 循环 → 工具调用 → 提供方调用
- 回复 → whatsmeow → WhatsApp → 手机

除提供方调用外没有任何流量越过你的网络边界——如果提供方是本地 Claude Code 上的 `claudecli`，连这一步也没有。

## 使用 `rousseau doctor` 验证

```sh
rousseau doctor
```

WhatsApp 路径上的每一项检查都覆盖：

- `provider.claudecli.binary`、`provider.claudecli.version`——LLM 路径。
- `state.path`、`state.db_size`、`state.sessions`——SQLite 会话存储。
- `whatsapp.store`、`whatsapp.paired`——设备凭证。
- `whatsapp.voice`——语音消息转录姿态。

`fail` 行意味着硬性中止；`warn` 行值得在上线前调查。

## 故障排查

### 二维码打印出来但手机拒绝

三种常见原因。第一，此前部分完成的配对让 `whatsapp.db` 处于 whatsmeow 无法复用的状态——删除 `~/.local/share/rousseau/whatsapp.db` 后重新扫描。第二，时钟偏差超过 30 秒（在没有可用 NTP 客户端的容器中常见）——WhatsApp 的握手对时间敏感。第三，较旧的 `whatsmeow` 版本可能错过 Meta 的协议更新；升级 rousseau。

### 我发了消息但守护进程记录 `router.transport.rejected`

你的 JID 与允许列表不匹配。传给 `--allow` 的值必须与 WhatsApp 报告的发送者 JID 完全一致（`447900123456@s.whatsapp.net`，不含 `+`、不含空格）。请注意，自聊测试可以工作，因为 rousseau 会把账户自身的 JID 替换为 LID 隐私哈希（见 `internal/transport/whatsapp/resolve.go`）。

### 未打印二维码且守护进程以 `no rows` 退出

whatsmeow 存储从未初始化。请确保父目录（`~/.local/share/rousseau/`）存在且可写。`rousseau doctor` 会在 `whatsapp.store` 下报告此问题。

### Rousseau 回复但模型输出为空

在 `rousseau doctor` 中检查 `provider.claudecli.binary` 与 `provider.claudecli.version`。最常见的空回复原因是 `claudecli` 调用返回 `is_error: true`——守护进程会以 `warn` 级别记录截断的错误。将提供方切换为 `anthropic` 或 `bedrock` 以隔离子进程。

### Slack/Discord："invalid_auth" 或 "401 Unauthorized"

对于 Slack，`xapp-…`（应用令牌）与 `xoxb-…`（机器人令牌）不同——弄混会产生 `invalid_auth`。对于 Discord，<em>Bot &gt; Reset Token</em> 中显示的令牌只显示一次；若你复制过一次然后丢失，只能再次重置。

## 相关页面

- [传输](/zh-Hans/transports/)——每一种传输、其线路协议以及允许列表格式。
- [用户指南：CLI](/zh-Hans/user-guide/cli/)——每个命令与选项。
- [用户指南：审批策略](/zh-Hans/user-guide/approval-policies/)——主要的安全杠杆。
- [部署](/zh-Hans/deployment/)——从前台 `rousseau whatsapp` 交接到 systemd 单元。
- [语音模式](/zh-Hans/user-guide/voice-mode/)——把 WhatsApp 语音消息变成 agent 轮次。

## 延伸阅读

- `internal/transport/whatsapp/client.go`——连接、二维码、事件泵。
- `internal/transport/whatsapp/resolve.go`——LID/JID 规范化与自聊处理。
- `internal/cli/whatsapp.go`——CLI 装配、存储 DSN、转录器选择。
- `internal/cli/slack.go`、`internal/cli/discord.go`——同类传输 CLI。
- `internal/transport/router.go`——允许列表强制执行。
