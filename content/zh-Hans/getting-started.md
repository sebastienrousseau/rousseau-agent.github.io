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
description: "Install rousseau-agent from source, go install, or a cosign-verified release. Run rousseau chat and configure the first chat transport."
keywords: "install, quickstart, rousseau chat, cosign verify, go install, systemd, podman"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/getting-started/"
subtitle: "安装 rousseau-agent 并接入你的第一个传输。"
tags: "install, quickstart, getting-started"
title: "快速入门"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "install, quickstart, rousseau chat, cosign verify, go install, systemd, podman"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "快速入门"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 2
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/getting-started/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "快速入门"
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
twitter_description: "Install rousseau-agent from source, go install, or a cosign-verified release. Run rousseau chat and configure the first chat transport."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "快速入门"
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

## 适用人群

- **个人开发者**——希望在自己的笔记本电脑上运行一个编码助手，并驱动其现有的 `claude` CLI。无需在 rousseau 的配置中传递 API 密钥，中间也没有云端中转。
- **平台运维人员**——在企业边界内为团队运行一个共享的编码代理。Rousseau 是一个部署在无 root 权限 Podman 容器内并已剥离权限的静态 Go 单文件二进制——可以与任何其他 systemd 服务并列部署。
- **安全审查人员**——在推广前审核代理。SLSA-3 溯源、cosign 签名的发布校验和、CycloneDX SBOM、可复现构建，所有信任边界均在[安全](/zh-Hans/security/)中记录。

## 最快路径

1. **如果你已经安装并认证了 `claude` CLI，** 最快的开始方式是使用默认 `claudecli` 提供方运行 `rousseau chat`——认证被继承，无需传递密钥。继续查看下面的[首次运行](#first-run)。
2. **如果你希望使用自己的密钥直连 API，** 请设置 `ANTHROPIC_API_KEY` 并在 `~/.config/rousseau/config.yaml` 中切换为 `provider: anthropic`。参见 [Anthropic 提供方](/zh-Hans/providers/anthropic/)。
3. **如果你所在的企业使用 AWS Bedrock 或 Google Vertex，** 请选择对应的提供方——[Bedrock](/zh-Hans/providers/bedrock/) 使用标准 AWS 凭证链；[Vertex](/zh-Hans/providers/vertex/) 读取服务账号 JSON。rousseau 的配置文件中不存放任何机密。
4. **如果你处于气隙环境或希望完全自托管推理，** 请将 rousseau 指向一个 OpenAI 兼容端点——Ollama、vLLM、LM Studio 或任意兼容层。参见 [OpenAI 兼容提供方](/zh-Hans/providers/openai-compatible/)。

## 完成后你将拥有

- 一个位于 `$PATH` 上的 `rousseau` 二进制，可通过 cosign 签名（发布路径）验证，或从源码构建（`make check` 执行与 CI 相同的 18 个 linter + race + govulncheck 门槛）。
- 一个可用的 `rousseau chat` TUI，由你所选择的提供方支撑。
- 一个位于 `~/.local/share/rousseau/sessions.db` 的 SQLite 会话存储——每一轮对话都会被持久化，可通过 FTS5 进行跨会话检索。
- 可选：一个可从你手机访问的实时聊天传输（WhatsApp、Slack、Signal 等）。

## 更愿意观看视频？

上述流程的简短录屏已列入路线图。在此之前，整个流程都在本页——大多数运维人员可在十分钟内完成。

## 系统要求

| 要求 | 版本 | 说明 |
|---|---|---|
| Go 工具链 | 1.26+ | `CGO_ENABLED=0`；二进制完全静态。 |
| 容器运行时 | Podman 4.4+ | 参考部署使用无 root 权限 Podman + systemd Quadlet 单元。Docker 也可运行，但 Quadlet 是 Podman 专属。 |
| `claude` CLI | 最新版 | 仅在使用默认 `claudecli` 提供方时需要。 |
| `signal-cli` | 0.13+ | 仅在使用 Signal 传输时需要。 |
| BlueBubbles 服务器 | 1.9+ | 仅在使用 iMessage 传输时需要（需 macOS 主机）。 |
| `whisper.cpp` | 1.5+ | 仅在启用 WhatsApp 语音消息转录时需要。 |

## 安装

### 从源码构建

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # produces ./bin/rousseau
./bin/rousseau version
```

`make check` 会运行 vet、`golangci-lint`、`go test -race` 与 `govulncheck`——与 CI 执行的门槛完全一致。

### 通过 `go install`

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

该二进制内嵌 `modernc.org/sqlite`，因此运行时不依赖 libc 或 CGo。

### 从签名发布安装

每一个打标签的发布都会发布带校验和的归档、CycloneDX SBOM、SLSA-3 溯源证明以及对校验和文件的 cosign 签名。运行前请务必验证：

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_<version>_checksums.txt.sig \
  rousseau_<version>_checksums.txt

sha256sum -c rousseau_<version>_checksums.txt
```

certificate-identity 正则用于锁定签名者身份；不要将其放宽。

## 首次运行

### 终端聊天

```sh
rousseau chat
```

Bubble Tea TUI。回车发送，`Ctrl+C` 退出。默认提供方为 `claudecli`，它会继承本地 Claude Code 安装的认证；rousseau 的配置中不会传递任何 API 密钥。

会话历史被持久化到 `~/.local/share/rousseau/sessions.db`（启用 WAL 日志与 FTS5 的 SQLite，用于跨会话检索）。

### 第一个聊天传输

WhatsApp 是参考传输（其配对 UX 最为严格）。首次启动时通过手机扫描 QR 完成配对：

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

E.164 JID（`<digits>@s.whatsapp.net`）用于限制入站消息处理；其他发送者会被静默丢弃。配对状态与会话存储一起保存在 `whatsapp.db` 中。

其他传输遵循相同的形式：

```sh
rousseau slack   --app-token xapp-... --bot-token xoxb-...
rousseau discord --token bot-token
rousseau telegram --token 12345:ABC
rousseau matrix  --homeserver-url https://matrix.org --access-token ... --user-id @bot:matrix.org
```

每个 `rousseau <transport> --help` 都会列出该传输的选项。默认值来自 `~/.config/rousseau/config.yaml`。

## 状态存储位置

| 路径 | 用途 |
|---|---|
| `~/.config/rousseau/config.yaml` | 用户级配置文件（Viper）。 |
| `~/.local/share/rousseau/sessions.db` | 会话、定时任务、JID 映射、FTS5 检索索引。 |
| `~/.local/share/rousseau/whatsapp.db` | Whatsmeow 设备凭证（单独保存，以便设备重新链接不影响会话）。 |
| `~/.claude/` | `claude` CLI OAuth 令牌，仅在使用 `claudecli` 提供方时相关。 |

## 后续步骤

- [核心概念](/zh-Hans/concepts/)——agent 循环、会话存储、MCP、cron、技能。
- [配置](/zh-Hans/configuration/)——每一个配置项。
- [部署](/zh-Hans/deployment/)——如何在 systemd 下运行守护进程。
