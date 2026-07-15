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
description: "Every environment variable rousseau-agent reads: the ROUSSEAU_ prefix from Viper, ANTHROPIC_API_KEY, XDG paths, provider SDK variables."
keywords: "environment variables, ROUSSEAU_, ANTHROPIC_API_KEY, viper, XDG"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/reference/environment-variables/"
subtitle: "Every environment variable rousseau reads, at what layer, with what default."
tags: "reference, environment, viper, secrets"
title: "参考：环境变量"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "environment variables, ROUSSEAU_, ANTHROPIC_API_KEY, viper, XDG"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "参考：环境变量"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 51
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/reference/environment-variables/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/environment-variables/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "参考：环境变量"
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
twitter_description: "Every environment variable rousseau-agent reads: the ROUSSEAU_ prefix from Viper, ANTHROPIC_API_KEY, XDG paths, provider SDK variables."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "参考：环境变量"
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

## rousseau 如何读取环境变量

两种机制，按此顺序（参见 `internal/config/config.go` 中的 `config.Load`）：

1. **Viper 的自动 env 绑定。** `SetEnvPrefix("ROUSSEAU")` 加上 `SetEnvKeyReplacer(".", "_")` 意味着每个配置字段都可通过 `ROUSSEAU_<UPPER_SNAKE>` 触及。所以 `provider` 变为 `ROUSSEAU_PROVIDER`，`agent.approver.mode` 变为 `ROUSSEAU_AGENT_APPROVER_MODE`。
2. **显式覆盖。** `ANTHROPIC_API_KEY` 直接从环境中读取并强制填入 `anthropic.api_key`，因此标准 Anthropic SDK 约定即可直接工作。没有其他键被隐式采纳。

本页其余部分要么是 Viper 映射变量、要么是 rousseau 自身不使用但底层库使用的 SDK 管理变量、要么是用于计算默认值的 XDG 路径。

优先级仍为：**flag > env > file > default**。

## `ROUSSEAU_*` 前缀

`internal/config/config.go` 中每个 `mapstructure` 标签都可通过 `ROUSSEAU_<UPPER_SNAKE_PATH>` 触及。示例节选 —— 完整清单跟随配置 struct：

| 变量 | 类别 | 默认值 | 描述 |
|---|---|---|---|
| `ROUSSEAU_PROVIDER` | core | `claudecli` | Provider 标识：`claudecli`、`anthropic`、`openai`、`openrouter`、`ollama`、`bedrock`、`vertex`。 |
| `ROUSSEAU_LOG_LEVEL` | logging | `info` | slog 级别：`debug`、`info`、`warn`、`error`。 |
| `ROUSSEAU_LOG_FORMAT` | logging | `text` | `text` 或 `json`。 |
| `ROUSSEAU_STATE_PATH` | state | `$HOME/.local/share/rousseau/sessions.db` | 会话存储 DSN。 |
| `ROUSSEAU_AGENT_MAX_ITERATIONS` | agent | `32` | 每轮工具调用迭代上限。 |
| `ROUSSEAU_AGENT_APPROVER_MODE` | agent | `` | `allow_all`、`deny_all`、`pattern`。 |
| `ROUSSEAU_AGENT_APPROVER_DEFAULT` | agent | `` | 用于 `pattern`：对未匹配调用的 `allow` 或 `deny`。 |
| `ROUSSEAU_AGENT_COMPRESSION_ENABLED` | agent | `false` | 开启 LLM 压缩器。 |
| `ROUSSEAU_AGENT_COMPRESSION_TRIGGER_MESSAGES` | agent | `60` | 消息数超过此值时压缩。 |
| `ROUSSEAU_AGENT_COMPRESSION_KEEP_RECENT` | agent | `8` | 逐字保留多少条最近消息。 |
| `ROUSSEAU_AGENT_SKILLS_DIR` | agent | `$HOME/.local/share/rousseau/skills` | Skills 目录。 |
| `ROUSSEAU_ANTHROPIC_API_KEY` | provider | — | 等同于 `ANTHROPIC_API_KEY`。 |
| `ROUSSEAU_ANTHROPIC_MODEL` | provider | `claude-sonnet-4-6` | Anthropic 模型 id。 |
| `ROUSSEAU_ANTHROPIC_MAX_TOKENS` | provider | `4096` | 最大响应 token。 |
| `ROUSSEAU_CLAUDECLI_BINARY` | provider | `claude` | `claudecli` provider 的可执行文件名。 |
| `ROUSSEAU_CLAUDECLI_MODEL` | provider | — | 传给 `claude --model`。 |
| `ROUSSEAU_CLAUDECLI_PERMISSION_MODE` | provider | — | `default`、`acceptEdits`、`bypassPermissions`、`plan` 等。 |
| `ROUSSEAU_OPENAI_API_KEY` | provider | — | OpenAI 兼容端点的 bearer。 |
| `ROUSSEAU_OPENAI_MODEL` | provider | — | 模型 id。 |
| `ROUSSEAU_OPENAI_BASE_URL` | provider | — | 覆盖端点。 |
| `ROUSSEAU_OPENROUTER_API_KEY` | provider | — | OpenRouter 的 bearer。 |
| `ROUSSEAU_OPENROUTER_MODEL` | provider | — | 模型 slug。 |
| `ROUSSEAU_OPENROUTER_BASE_URL` | provider | `https://openrouter.ai/api/v1` | 覆盖端点。 |
| `ROUSSEAU_OLLAMA_MODEL` | provider | — | 模型 tag。 |
| `ROUSSEAU_OLLAMA_BASE_URL` | provider | `http://localhost:11434/v1` | 本地 Ollama 端点。 |
| `ROUSSEAU_BEDROCK_REGION` | provider | — | AWS 区域。 |
| `ROUSSEAU_BEDROCK_MODEL` | provider | — | Bedrock 模型 id。 |
| `ROUSSEAU_BEDROCK_PROFILE` | provider | — | AWS named profile。 |
| `ROUSSEAU_VERTEX_PROJECT` | provider | — | GCP project。 |
| `ROUSSEAU_VERTEX_REGION` | provider | — | Vertex 区域。 |
| `ROUSSEAU_VERTEX_MODEL` | provider | — | Anthropic-on-Vertex 模型。 |
| `ROUSSEAU_VERTEX_CREDENTIALS_FILE` | provider | — | service account JSON 的路径。 |
| `ROUSSEAU_WHATSAPP_REPLY_HEADER` | transport | `💎 *Rousseau Agent*\n\n` | 附加到每条 WhatsApp 出站消息之前。 |
| `ROUSSEAU_WHATSAPP_VOICE_ENABLED` | transport | `false` | 启用语音笔记的 whisper 转写。 |
| `ROUSSEAU_WHATSAPP_VOICE_BINARY` | transport | `whisper` | whisper.cpp 可执行文件。 |
| `ROUSSEAU_WHATSAPP_VOICE_MODEL` | transport | — | whisper 模型名（`base.en`、`small`）。 |
| `ROUSSEAU_WHATSAPP_VOICE_MODEL_PATH` | transport | — | 显式 .bin 路径（优先于 model）。 |
| `ROUSSEAU_WHATSAPP_VOICE_LANGUAGE` | transport | — | ISO 代码；为空则自动检测。 |
| `ROUSSEAU_SIGNAL_BINARY` | transport | `signal-cli` | signal-cli 可执行文件。 |
| `ROUSSEAU_SIGNAL_ACCOUNT` | transport | — | E.164 电话号码。 |
| `ROUSSEAU_SIGNAL_REPLY_HEADER` | transport | — | 回复 header。 |
| `ROUSSEAU_TELEGRAM_TOKEN` | transport | — | Bot API token。 |
| `ROUSSEAU_TELEGRAM_BASE_URL` | transport | — | 覆盖 Bot API 端点。 |
| `ROUSSEAU_MATRIX_HOMESERVER_URL` | transport | — | Homeserver base URL。 |
| `ROUSSEAU_MATRIX_ACCESS_TOKEN` | transport | — | Matrix access token。 |
| `ROUSSEAU_MATRIX_USER_ID` | transport | — | 完整 MXID（`@bot:example.org`）。 |
| `ROUSSEAU_SLACK_APP_TOKEN` | transport | — | `xapp-…` 应用级 token。 |
| `ROUSSEAU_SLACK_BOT_TOKEN` | transport | — | `xoxb-…` bot token。 |
| `ROUSSEAU_SLACK_BOT_USER_ID` | transport | — | Bot 的用户 id，用于自回显抑制。 |
| `ROUSSEAU_DISCORD_TOKEN` | transport | — | Discord bot token。 |
| `ROUSSEAU_SMS_PROVIDER` | transport | — | `twilio` 或 `vonage`。 |
| `ROUSSEAU_SMS_FROM` | transport | — | 发送号码。 |
| `ROUSSEAU_SMS_ACCOUNT_SID` | transport | — | Twilio account SID。 |
| `ROUSSEAU_SMS_AUTH_TOKEN` | transport | — | Twilio/Vonage 秘密。 |
| `ROUSSEAU_SMS_API_KEY` | transport | — | Vonage API 密钥。 |
| `ROUSSEAU_SMS_BASE_URL` | transport | — | 用于区域端点或测试的覆盖。 |
| `ROUSSEAU_IMESSAGE_BASE_URL` | transport | — | BlueBubbles 服务器 URL。 |
| `ROUSSEAU_IMESSAGE_PASSWORD` | transport | — | BlueBubbles 密码。 |
| `ROUSSEAU_IMESSAGE_CHAT_GUID` | transport | — | 出站目标。 |
| `ROUSSEAU_IMESSAGE_POLL_INTERVAL` | transport | `2s` | Duration 字符串。 |
| `ROUSSEAU_EMAIL_IMAP_ADDR` | transport | — | IMAP 服务器。 |
| `ROUSSEAU_EMAIL_IMAP_USERNAME` | transport | — | IMAP 用户。 |
| `ROUSSEAU_EMAIL_IMAP_PASSWORD` | transport | — | IMAP 密码。 |
| `ROUSSEAU_EMAIL_MAILBOX` | transport | — | 要监视的文件夹。 |
| `ROUSSEAU_EMAIL_POLL_INTERVAL` | transport | — | Duration 字符串。 |
| `ROUSSEAU_EMAIL_SMTP_ADDR` | transport | — | SMTP 提交主机。 |
| `ROUSSEAU_EMAIL_SMTP_USERNAME` | transport | — | SMTP 用户。 |
| `ROUSSEAU_EMAIL_SMTP_PASSWORD` | transport | — | SMTP 密码。 |
| `ROUSSEAU_EMAIL_FROM` | transport | — | From 地址。 |

**允许列表数组**（`ROUSSEAU_SLACK_ALLOWLIST`、`ROUSSEAU_DISCORD_ALLOWLIST`、`ROUSSEAU_TELEGRAM_ALLOWLIST`……）由 Viper 支持，但逗号分隔的 env-string 解析较为脆弱 —— 优先在 `config.yaml` 中设置。

## 显式环境变量（在 ROUSSEAU_ 前缀之外）

| 变量 | 来源 | 用途 |
|---|---|---|
| `ANTHROPIC_API_KEY` | `config.Load`（`internal/config/config.go` 第 275 行） | 填充 `anthropic.api_key`。Anthropic SDK 的标准约定。 |
| `HOME` | `internal/cli/init.go` | 供 `rousseau init` 计算默认 state 路径。 |

## SDK 拥有、rousseau 不使用的变量

某些 provider 库会读取自己的环境变量。Rousseau 自身不读取这些，但当选中相应 provider 时它们会影响行为：

| 变量 | 消费者 | 说明 |
|---|---|---|
| `AWS_PROFILE`、`AWS_REGION`、`AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY`、`AWS_SESSION_TOKEN`、`AWS_WEB_IDENTITY_TOKEN_FILE` | `aws-sdk-go-v2`（Bedrock） | 标准凭据链。相比静态密钥，优先选择 IRSA 或基于 profile 的凭据。 |
| `GOOGLE_APPLICATION_CREDENTIALS` | Google 认证库（Vertex） | service account JSON 的路径。若设置了 `config.yaml` 中的 `vertex.credentials_file`，则被后者覆盖。 |
| `OPENAI_API_KEY` | 上游 Go OpenAI 客户端通常会读取此变量 | Rousseau 显式通过 `openai.api_key` 接线；不做任何隐式操作。 |
| `HTTP_PROXY`、`HTTPS_PROXY`、`NO_PROXY` | Go net/http | 通用 Go 代理变量。适用于企业出口路径。 |

## XDG 路径变量

Rousseau 对 state 与 config 遵循 XDG Base Directory 规范，并有两个回退：

| 变量 | 影响 |
|---|---|
| `XDG_CONFIG_HOME` | `$XDG_CONFIG_HOME/rousseau/config.yaml` 是默认配置路径（在 `internal/cli/root.go` 中引用）。 |
| `XDG_DATA_HOME` | 默认 state 路径 `$XDG_DATA_HOME/rousseau/sessions.db`（被 `whatsapp.go`、`skills.go`、`init.go` 引用）。 |
| `HOME` | 当 XDG 变量未设置时的回退；rousseau 在 `internal/config/config.go` 中使用 `os.UserHomeDir()`。 |

`docker/rousseau-agent.container` 的容器 Quadlet 单元同时设置 `HOME=/home/rousseau` 与 `XDG_DATA_HOME=/home/rousseau/.local/share`。

## 密钥卫生

将密钥保存在以下三处之一：

1. **systemd 单元 `EnvironmentFile=`** —— `chmod 0600`，视情况归 root 或用户所有。由 Quadlet 单元引用 —— 参见 [VPS 部署教程](/zh-Hans/tutorials/deploy-to-a-vps/)。
2. **由 shell 加载的 `.env` 文件。** 仅供桌面使用；请将其排除在版本控制之外。
3. **密钥管理器。** AWS Secrets Manager、HashiCorp Vault，或 `pass`/`gopass`。在启动时将其值管道传入进程。

绝不要把密钥提交到 `config.yaml`。`config.yaml` 适合放允许列表、base URL 与非密钥配置；不适合放 API 密钥与 bot token。

## 故障排除

### 已设置 `ROUSSEAU_...` 但 rousseau 仍使用默认值

环境变量只在启动时被读取。请在 export 后重启守护进程。同时校验转换规则：配置键中的点号变为下划线，前缀为 `ROUSSEAU_`（大写，精确）。

### `ANTHROPIC_API_KEY` 似乎被忽略

该环境变量只在 `provider: anthropic` 激活时才被查询。在 `provider: claudecli` 下，`claude` CLI 会读取自己的凭据。

### 不同主机上值不同

优先级为 **flag > env > file > default**。若已设置 flag（例如来自 systemd 单元的 `ExecStart`），它会同时优先于 env 和 file。

### 容器内无法读取 `GOOGLE_APPLICATION_CREDENTIALS`

请确保该文件以只读方式 bind mount 到容器中，并且容器 UID（默认 1000）可读。

## 相关页面

- [配置](/zh-Hans/configuration/) —— 每个配置字段及默认值。
- [参考：配置 schema](/zh-Hans/reference/config-schema/) —— YAML 结构。
- [参考：CLI 命令](/zh-Hans/reference/cli-commands/) —— 各传输的 flag。
- [指南：企业入门](/zh-Hans/guides/enterprise-onboarding/) —— 生产环境中的密钥处理。
- [部署](/zh-Hans/deployment/) —— 密钥管理选项。

## 延伸阅读

- `internal/config/config.go` —— `Load` 设置 env 前缀与点号-下划线键替换。
- `internal/cli/root.go` —— `Load` 的调用点。
