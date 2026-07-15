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
description: "Set up rousseau-agent's WhatsApp transport: QR pairing, E.164 allowlist, LID vs phone-JID normalisation, voice-note transcription with whisper.cpp."
keywords: "WhatsApp, whatsmeow, QR pairing, JID, LID, allowlist, voice notes, whisper, transcription"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/transports/whatsapp/"
subtitle: "Whatsmeow-backed WhatsApp bridge with QR pairing."
tags: "transports, WhatsApp"
title: "WhatsApp 传输"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "WhatsApp, whatsmeow, QR pairing, JID, LID, allowlist, voice notes, whisper, transcription"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "WhatsApp 传输"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 12
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/transports/whatsapp/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/whatsapp/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "WhatsApp 传输"
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
twitter_description: "Set up rousseau-agent's WhatsApp transport: QR pairing, E.164 allowlist, LID vs phone-JID normalisation, voice-note transcription with whisper.cpp."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "WhatsApp 传输"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">你将学到</span><p>WhatsApp 传输如何与你的手机配对、LID 与电话 JID 的规范化规则、语音消息转录流程、媒体下载、允许列表正则模式，以及初次运维人员容易踩的坑。请对照阅读 <code>internal/transport/whatsapp/client.go</code>、<code>resolve.go</code> 与 <code>dispatch.go</code>。</p></aside>

## 概述

WhatsApp 传输（`internal/transport/whatsapp/`）由 `go.mau.fi/whatsmeow` 支持——一个逆向工程的 WhatsApp Web 多设备客户端。Meta 视其为非官方客户端；请不要在你依赖用于重要事务的私人号码上运行。

Signal 协议的端到端加密得以保留（whatsmeow 使用与 WhatsApp 手机端相同的协议）。守护进程将设备凭证保存在与会话存储分离的 SQLite 文件中，因此设备重新链接不会触及对话历史。

<aside class="admonition" data-type="caution"><span class="admonition-title">非官方协议</span><p>Meta 偶尔会封禁运行非官方客户端的号码。即使你遵守 WhatsApp 的速率限制并负责任地行事，使用 <code>whatsmeow</code> 的电话号码也可能被无预警封禁。请使用专用号码而非个人号码。</p></aside>

## 配对

首次启动：

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

通过 `mdp/qrterminal/v3` 向 stdout 打印一个二维码。用 WhatsApp 手机端扫描（**设置 → 已链接的设备 → 链接设备**）。配对状态会被写入状态目录下的 `whatsapp.db`（通常为 `~/.local/share/rousseau/whatsapp.db`）。

之后的启动会静默复用已配对设备。若二维码再次出现，说明配对已在手机侧被撤销——删除 `whatsapp.db` 后重新配对。

## 允许列表

`--allow` 限制入站处理。多个选项累积生效：

```sh
rousseau whatsapp \
  --allow 447900123456@s.whatsapp.net \
  --allow 442071234567@s.whatsapp.net
```

该值是 WhatsApp 的 **JID**——E.164 电话号码（无 `+`）后接 `@s.whatsapp.net`。也支持群 JID（`<id>@g.us`）。

空允许列表接受所有发送者。对于聊天传输守护进程，你总是希望至少有一项。

## LID 与电话 JID 规范化

WhatsApp 对同一用户使用两种标识符格式：

| 格式 | 示例 | 含义 |
|---|---|---|
| 电话 JID | `447900123456@s.whatsapp.net` | 不含 `+` 的 E.164 电话号码后接 `@s.whatsapp.net`。跨时间稳定；会泄露电话号码。 |
| LID | `1234567890@lid` | Location-Independent ID——一串看似随机、不暴露电话号码的字符串。也稳定，但不直接可与号码关联。 |
| 设备后缀 | `447900123456:5@s.whatsapp.net` | 任何 JID 都可携带设备地址后缀（`:N`）。WhatsApp 报告消息时会带上发送该消息的具体设备。 |

Rousseau 的入站处理器（`internal/transport/whatsapp/resolve.go` 中的 `ResolveInbound`）在分发前将每个事件规范化为一致形式：

1. **剥离设备后缀。** `447900:5@s.whatsapp.net` 变为 `447900@s.whatsapp.net`。这样，以裸用户 JID 写成的允许列表就能匹配，不论消息由哪台链接设备发送。
2. **在自聊中把 LID 替换为账户持有者的电话 JID。** 当账户持有者是发送者（`IsFromMe=true`）时，WhatsApp 报告的发送者为账户的 LID（隐私哈希），而非电话 JID。Rousseau 会替换为账户自身的 JID，让运维人员可以只把 `<phone>@s.whatsapp.net` 加入允许列表，并让自聊测试正确路由。
3. **丢弃无法解析的发送者。** 空的 `User` 或 `Server` 字段——由 `FuzzResolveInbound` 发现——无法安全路由。消息会被静默跳过，而不是以格式错误的 From 传递给处理器。

### 自聊小陷阱

当你在 WhatsApp 上向自己发消息（测试机器人）时，发送者字段以你的 LID 到达。若允许列表里是你的电话 JID，朴素查找会失配。Rousseau 的替换——`if evt.Info.IsFromMe && ownID != nil { from = ownID.ToNonAD() }`——修复了这一点。

### 循环预防

`IsFromMe=true` 也会对*该*链接设备发送的消息（rousseau 的出站回复回响）触发。当设备 ID 匹配时，传输会丢弃它们：

```go
if evt.Info.IsFromMe && ownID != nil && evt.Info.Sender.Device == ownID.Device {
    return Resolved{Skip: SkipOwnDevice}
}
```

来自账户*其他*链接设备的消息（例如主手机测试"向自己发消息"）带有 `IsFromMe=true` 但设备 ID 不同——它们会被正常处理。

## 允许列表正则模式

`--allow` 选项接受精确字符串，而非正则——rousseau 在 `router.go` 中执行大小写不敏感的相等检查。若你希望模式匹配，请使用配置文件的 `pattern` 模式（与审批策略相同）：

```yaml
whatsapp:
  allowlist:
    - "447900123456@s.whatsapp.net"
    - "447900654321@s.whatsapp.net"
```

对于群（`<hash>@g.us`），以相同方式添加。若要允许某个国家代码的所有人，你需要自定义 `Router.Allow` 实现——内置执行器按设计不做前缀匹配。

<aside class="admonition" data-type="warning"><span class="admonition-title">空允许列表</span><p>空允许列表会接受所有发送者。切勿在没有允许列表的情况下将聊天传输运行在公开号码上——任何知道该号码的人都会成为你 agent 的操作者。</p></aside>

## 回复头

每条出站消息都会加上一个前缀头，让发送者知道正在与哪个机器人交谈。默认：

```
💎 *Rousseau Agent*

<message body>
```

WhatsApp 会将 `*text*` 渲染为粗体。在配置中覆盖：

```yaml
whatsapp:
  reply_header: "🤖 *Coding bot*\n\n"
```

设为单个空格 `" "` 可完全禁用前缀。

## 语音消息转录

入站语音消息在运维人员启用时由 `whisper.cpp` 转录。默认关闭，因为需要安装 `whisper` CLI。

```yaml
whatsapp:
  voice:
    enabled: true
    binary: whisper
    model: base.en
    language: en
    extra_args:
      - --threads
      - "4"
```

| 字段 | 作用 |
|---|---|
| `enabled` | 开关。关闭时，音频消息被记录并跳过。 |
| `binary` | Whisper CLI 可执行文件。为空默认为 `whisper`。 |
| `model` | 传给 `--model`（`base.en`、`small`、`medium`）。 |
| `model_path` | 显式 `.bin` 路径。优先于 `model`。 |
| `language` | 传给 `--language`。为空则自动检测。 |
| `extra_args` | 追加到每次调用。 |

转录得到的文本会像用户键入一样交给 agent。

## 容器部署

参考的 Podman Quadlet 单元（`docker/rousseau-agent.container`）以读写方式挂载状态目录，让配对可跨重启存活：

```
Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
```

`Network=pasta` 让容器获得无 root 权限的仅出站网络栈。Whatsmeow 不需要任何提升的能力；`DropCapability=all` 是安全的。

## 语音消息转录流程

当语音消息到达时，标准解析器返回 `SkipEmptyText`（无文本内容）。`Dispatch` 会针对音频消息专门检测此情况——若配置了 `Transcriber`——按下列路径处理：

```
入站音频消息
  │
  ├── Downloader.Download(ctx, audioMsg)
  │     • bytes []byte, mimetype string, err error
  │     • 成功时记录 whatsapp.audio_downloaded
  │
  ├── Transcriber.Transcribe(ctx, audio, mimetype)
  │     • 返回纯文本转录
  │     • 记录 whatsapp.transcribed 与耗时
  │
  └── 以转录结果作为 `Body` 重新进入 handleTextMessage
```

若未配置转录器，守护进程会记录 `whatsapp.audio_ignored reason=transcriber_not_configured` 并丢弃消息。语音消息不会触发"静默"回复——空入站产生空出站。

## 媒体下载

`Downloader` 接口刻意保持小巧：

```go
type Downloader interface {
    Download(ctx context.Context, msg DownloadableAudio) (bytes []byte, mimetype string, err error)
}
```

目前只接入了音频下载。图片和视频下载在路线图上——它们以 `waProto.ImageMessage` / `VideoMessage` 到达，需要相应的 `DownloadableMedia` 接口。计划请跟踪 [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md)。

## 打字指示

处理器将每条回复包装在 `SendPresence(Composing, Paused)` 调用中，让发送者在模型思考时看到"…正在输入"指示。两次调用都有 5 秒超时且尽力而为——presence 失败绝不会阻塞回复本身。

## 失败模式

| 症状 | 修复 |
|---|---|
| 每次重启都重新打印二维码 | 配对已从手机侧被撤销；删除 `whatsapp.db` 后重新配对。 |
| WhatsApp 重连循环 | 对照 `pool.ntp.org` 检查时钟偏差——whatsmeow 的握手对时间敏感。 |
| 入站消息被忽略 | 确认发送者在 `--allow` 列表中；查看日志中的 `router.transport.rejected`。 |
| Meta 封禁了号码 | 请勿运行于个人号码。该协议是非官方的。 |
| 自聊 "hello" 未路由 | 自聊使用 LID；rousseau 会替换为电话 JID 以匹配允许列表。请确认 `ownID` 已初始化——守护进程会在初始化时记录 `whatsapp.connected`。 |
| 语音消息被静默丢弃 | 要么 `whatsapp.voice.enabled: false`，要么缺少 `whisper` 二进制。日志行：`whatsapp.audio_ignored`。 |
| 每条回复重复出现 | 循环预防未开启。请确保运行的是较新构建；相关修复在 whatsmeow 多设备铺开初期即已落地于 `ResolveInbound`。 |

## 故障排查

### 二维码已打印但手机 app 拒绝

三种常见原因：(1) 此前部分完成的配对让 `whatsapp.db` 处于 whatsmeow 无法复用的状态——删除该文件后重新扫描；(2) 时钟偏差超过 30 秒（在无 NTP 的容器中常见）——用 `timedatectl status` 检查；(3) 较旧的 `whatsmeow` 版本可能错过 Meta 的协议更新。

### `whatsapp.connected` 与 `whatsapp.disconnected` 循环

时钟偏差，或 Meta 已使配对失效。查看日志中的 `whatsapp.logged_out` 事件——这是决定性信号。

### 语音消息到达但未被转录

转录器二进制无法解析。检查 `whatsapp.voice.binary` 与 `whatsapp.voice.model_path`——两者都必须指向真实文件（或 `binary` 位于 `PATH` 中）。

### 允许列表正则未匹配

Rousseau 的允许列表是精确字符串而非正则。若要匹配一组发送者，请逐一列出或添加自定义路由器。

### 回复头显示为字面 `*` 字符

接收方客户端未渲染 WhatsApp Markdown。这是客户端渲染问题；若你的接收方使用较旧客户端，请改用纯文本。

## 相关页面

- [快速入门：第一个传输](/zh-Hans/getting-started/first-transport/)——端到端演练。
- [用户指南：语音模式](/zh-Hans/user-guide/voice-mode/)——语音消息深入解析。
- [配置](/zh-Hans/configuration/)——`whatsapp` 配置块。
- [传输](/zh-Hans/transports/)——其他八种传输。
- [部署](/zh-Hans/deployment/)——在 Podman 容器中运行 WhatsApp。

## 延伸阅读

- `internal/transport/whatsapp/client.go`——连接、二维码配对、事件泵。
- `internal/transport/whatsapp/resolve.go`——LID/JID 规范化与自聊处理。
- `internal/transport/whatsapp/dispatch.go`——带语音消息分支的入站消息分发。
- `internal/transport/whatsapp/whisper.go`——参考的 whisper-cpp 转录器。
- `internal/cli/whatsapp.go`——CLI 装配、存储 DSN、转录器选择。
