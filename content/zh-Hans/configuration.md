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
changefreq: "weekly"
description: "Complete configuration reference for rousseau-agent. Every provider, transport, and agent knob with type, default, and effect."
keywords: "configuration, config.yaml, viper, precedence, YAML, provider, transport, approver, compression"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/configuration/"
subtitle: "internal/config/config.go 中的每一个字段。"
tags: "configuration, reference"
title: "配置参考"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "configuration, config.yaml, viper, precedence, YAML, provider, transport, approver, compression"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "配置参考"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 4
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/configuration/index.html"
item_link: "https://docs.rousseau-agent.dev/configuration/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "配置参考"
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
twitter_description: "Complete configuration reference for rousseau-agent. Every provider, transport, and agent knob with type, default, and effect."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "配置参考"
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

## 优先级

`rousseau` 按 **flag > env > file > default** 的顺序解析配置。文件默认位于 `~/.config/rousseau/config.yaml`；可使用 `--config` 覆盖。

环境变量使用 `ROUSSEAU_` 前缀，并将 `.` 替换为 `_`——因此 `provider` 变为 `ROUSSEAU_PROVIDER`，`anthropic.api_key` 变为 `ROUSSEAU_ANTHROPIC_API_KEY`。`ANTHROPIC_API_KEY` 也会被直接识别（在加载时绑定到 `anthropic.api_key`）。

## 顶层

| 字段 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `provider` | string | `claudecli` | LLM 后端：`claudecli`、`anthropic`、`bedrock`、`vertex`、`openai`、`openrouter`、`ollama`。 |

## `anthropic` —— 直连 Anthropic API

| 字段 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `api_key` | string | *来自 `ANTHROPIC_API_KEY`* | 用于 `api.anthropic.com` 的 Bearer 令牌。选择此提供方时若为空则拒绝。 |
| `model` | string | `claude-sonnet-4-6` | 传给 SDK 的模型标识符。 |
| `max_tokens` | int64 | `4096` | 单次完成的输出 token 上限。 |

参见 [/providers/anthropic/](/zh-Hans/providers/anthropic/)。

## `bedrock` —— AWS Bedrock

| 字段 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `region` | string | *必填* | AWS 区域（`us-east-1`、`eu-west-2`）。 |
| `model` | string | *必填* | Bedrock 模型 ID（`anthropic.claude-sonnet-4-6-20260101-v1:0`）。 |
| `profile` | string | *空* | 来自 `~/.aws/credentials` 的凭证配置。为空则回退到标准 AWS 凭证链。 |
| `max_tokens` | int64 | SDK 默认值 | 输出 token 上限。 |

参见 [/providers/bedrock/](/zh-Hans/providers/bedrock/)。

## `vertex` —— Google Vertex AI

| 字段 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `project` | string | *必填* | GCP 项目 ID。 |
| `region` | string | *必填* | Vertex 区域（`us-central1`）。 |
| `model` | string | *必填* | Vertex 上的 Anthropic 模型 ID（`claude-sonnet-4-6@20260101`）。 |
| `credentials_file` | string | *空* | 服务账号或授权用户 JSON 的路径。为空则使用 Application Default Credentials。 |
| `max_tokens` | int64 | `4096` | 输出 token 上限。 |

参见 [/providers/vertex/](/zh-Hans/providers/vertex/)。

## `claudecli` —— 对本地 `claude` CLI 的子进程调用

| 字段 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `binary` | string | `claude` | 可执行文件，通过 `$PATH` 解析。 |
| `model` | string | *空* | 传给 `--model`。为空时使用 claude 默认值。 |
| `permission_mode` | string | *空* | 传给 `--permission-mode`。取值：`acceptEdits`、`auto`、`bypassPermissions`、`default`、`dontAsk`、`plan`。无人值守守护进程通常需要 `bypassPermissions`。 |
| `extra_args` | []string | `[]` | 在每次调用时插入到 `-p` 前面。对 `--add-dir`、`--allowed-tools`、`--disallowed-tools`、`--plugin-dir` 很有用。 |

参见 [/providers/claudecli/](/zh-Hans/providers/claudecli/)。

## `openai` / `openrouter` / `ollama` —— OpenAI 兼容端点

结构一致。`openrouter.base_url` 默认为 `https://openrouter.ai/api/v1`；`ollama.base_url` 默认为 `http://localhost:11434/v1`；`ollama.api_key` 默认为 `not-required`。

| 字段 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `api_key` | string | *必填* | Bearer 令牌。即使 Ollama 也必须非空（任意占位符均可）。 |
| `model` | string | *必填* | 模型标识符。跨端点没有统一的默认值。 |
| `base_url` | string | *提供方默认值* | 完整端点 URL。 |
| `max_tokens` | int64 | SDK 默认值 | 输出 token 上限。 |

参见 [/providers/openai-compatible/](/zh-Hans/providers/openai-compatible/)。

## `log`

| 字段 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `level` | string | `info` | `debug`、`info`、`warn`、`error`。 |
| `format` | string | `text` | `text`（人类可读）或 `json`（生产环境 / 日志聚合）。 |

## `state`

| 字段 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `path` | string | `~/.local/share/rousseau/sessions.db` | SQLite 数据库路径（WAL 模式，`busy_timeout=15s`）。 |

## `agent`

| 字段 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `system_prompt` | string | *空* | 覆盖内置默认值。 |
| `max_iterations` | int | `32` | 每个 `Turn` 内的模型往返上限。 |
| `skills_dir` | string | *空* | `*.md` 技能文件的目录。为空则禁用技能。 |

### `agent.compression`

| 字段 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `enabled` | bool | `false` | 启用基于 LLM 的会话压缩。 |
| `trigger_messages` | int | `60` | 消息数超过此值时触发压缩。 |
| `keep_recent` | int | `8` | 逐字保留的最近消息数。 |
| `prompt` | string | *内置* | 覆盖默认摘要指令。 |

### `agent.approver`

| 字段 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `mode` | string | `allow_all` | `allow_all`、`deny_all` 或 `pattern`。 |
| `reason` | string | *空* | 呈现给模型的拒绝理由。 |
| `default` | string | `deny` | 无 `allow` 或 `deny` 规则匹配时的兜底（pattern 模式）。 |
| `allow` | []PatternEntry | `[]` | 每个工具的正则允许规则。 |
| `deny` | []PatternEntry | `[]` | 每个工具的正则拒绝规则。deny 优先于 allow。 |

每一个 `PatternEntry` 形如 `{tool: <name>, match: <regex>}`。`tool: ""` 匹配所有工具；`match: ""` 匹配所有输入。

## 传输配置块

### `whatsapp`

| 字段 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `reply_header` | string | `💎 *Rousseau Agent*\n\n` | 附加到每条出站消息前。设为 `" "` 可禁用。 |
| `voice.enabled` | bool | `false` | 使用 Whisper 转录入站语音消息。 |
| `voice.binary` | string | `whisper` | Whisper CLI 可执行文件。 |
| `voice.model` | string | *空* | 传给 `--model`（`base.en`、`small`）。 |
| `voice.model_path` | string | *空* | 显式 `.bin` 路径，优先于 `model`。 |
| `voice.language` | string | *空* | 传给 `--language`。为空则自动检测。 |
| `voice.extra_args` | []string | `[]` | 追加到每次 whisper 调用后。 |

### `signal`

| 字段 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `binary` | string | `signal-cli` | 以 JSON-RPC 守护进程模式调用的可执行文件。 |
| `account` | string | *必填* | 守护进程运行时使用的 E.164 电话号码。 |
| `extra_args` | []string | `[]` | 插入到 `-a <account>` 和 `jsonRpc` 之间。 |
| `reply_header` | string | *空* | 附加到每条出站消息前。 |
| `allowlist` | []string | `[]` | 允许处理其消息的 E.164 号码。为空则接受所有发送者。 |

### `telegram`

| 字段 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `token` | string | *必填* | 来自 BotFather 的 Bot 令牌。 |
| `base_url` | string | `https://api.telegram.org` | 用于本地 Bot API 服务器的覆盖值。 |
| `reply_header` | string | *空* | 附加到每条出站回复前。 |
| `allowlist` | []string | `[]` | 允许处理其消息的 Telegram 用户 ID。 |

### `matrix`

| 字段 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `homeserver_url` | string | *必填* | 基础 URL，例如 `https://matrix.org`。 |
| `access_token` | string | *必填* | 机器人用户的访问令牌。 |
| `user_id` | string | *空* | 机器人用户的完整 MXID（`@bot:matrix.org`）。可选但建议填写（用于抑制自身消息回响）。 |
| `reply_header` | string | *空* | 附加到每条出站回复前。 |
| `allowlist` | []string | `[]` | 允许处理其消息的 Matrix ID。 |

### `slack`

| 字段 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `app_token` | string | *必填* | 具有 `connections:write` 权限的 `xapp-*` 应用级令牌。 |
| `bot_token` | string | *必填* | 具有 `chat:write` 权限的 `xoxb-*` 机器人令牌。 |
| `bot_user_id` | string | *空* | 机器人自身的 `U…` ID，用于防止自身消息回环。 |
| `reply_header` | string | *空* | 附加到每条出站消息前。 |
| `allowlist` | []string | `[]` | 允许处理其消息的 Slack 用户 ID。 |

### `discord`

| 字段 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `token` | string | *必填* | 来自开发者门户的 Bot 令牌。 |
| `reply_header` | string | *空* | 附加到每条出站回复前。 |
| `allowlist` | []string | `[]` | 允许处理其消息的 Discord 用户 ID。 |

### `sms`

| 字段 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `provider` | string | *必填* | `twilio` 或 `vonage`。 |
| `from` | string | *必填* | E.164 发送者或 Twilio Messaging Service SID。 |
| `account_sid` | string | *twilio 必填* | Twilio 账户 SID（`AC…`）。 |
| `auth_token` | string | *必填* | Twilio 认证令牌或 Vonage API secret。 |
| `api_key` | string | *vonage 必填* | Vonage API key。 |
| `base_url` | string | *提供方默认值* | 用于区域或测试端点的覆盖值。 |
| `reply_header` | string | *空* | 附加到每条出站消息前。 |

### `imessage`

| 字段 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `base_url` | string | *必填* | BlueBubbles 服务器 URL（`http://localhost:1234`）。 |
| `password` | string | *必填* | BlueBubbles 服务器密码。 |
| `chat_guid` | string | *空* | 出站目标 GUID。 |
| `poll_interval` | duration | `5s` | 轮询 `/api/v1/message` 的节奏。 |
| `reply_header` | string | *空* | 附加到每条出站消息前。 |

### `email`

| 字段 | 类型 | 默认值 | 作用 |
|---|---|---|---|
| `imap_addr` | string | *必填* | 用于 TLS 封装 IMAP 的 `host:port`（通常为 `:993`）。 |
| `imap_username` | string | *必填* | IMAP 用户名。 |
| `imap_password` | string | *必填* | IMAP 密码。 |
| `mailbox` | string | `INBOX` | 要轮询的邮箱。 |
| `poll_interval` | duration | `30s` | 查找 UNSEEN 邮件的频率。 |
| `smtp_addr` | string | *必填* | 用于 SMTP 提交的 `host:port`（通常为 `:587`）。 |
| `smtp_username` | string | *必填* | SMTP 用户名。 |
| `smtp_password` | string | *必填* | SMTP 密码。 |
| `from` | string | *必填* | 信封 + 首部 `From` 地址。 |
| `reply_header` | string | *空* | 附加到每条出站消息正文前。 |

## 完整示例

```yaml
provider: claudecli

anthropic:
  api_key: sk-ant-...
  model: claude-sonnet-4-6
  max_tokens: 4096

bedrock:
  region: us-east-1
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
  profile: default

vertex:
  project: my-gcp-project
  region: us-central1
  model: claude-sonnet-4@20260101
  credentials_file: ~/.config/gcloud/vertex-key.json

claudecli:
  binary: claude
  model: sonnet
  permission_mode: bypassPermissions
  extra_args: []

log:
  level: info
  format: json

state:
  path: ~/.local/share/rousseau/sessions.db

agent:
  system_prompt: ""
  max_iterations: 32
  skills_dir: ~/.local/share/rousseau/skills
  compression:
    enabled: true
    trigger_messages: 60
    keep_recent: 8
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "^./workspace/.*"}
    deny:
      - {tool: bash, match: "rm -rf|sudo|:\\(\\)\\{ :\\|:& \\};:"}

whatsapp:
  reply_header: "💎 *Rousseau Agent*\n\n"
  voice:
    enabled: false

signal:
  account: "+447900123456"
  allowlist: ["+447900654321"]

telegram:
  token: "123:ABC"
  allowlist: ["12345678"]

matrix:
  homeserver_url: "https://matrix.org"
  access_token: "syt_..."
  user_id: "@bot:matrix.org"
  allowlist: ["@alice:matrix.org"]

slack:
  app_token: "xapp-..."
  bot_token: "xoxb-..."
  bot_user_id: "U0123ABCD"

discord:
  token: "bot-token"
  allowlist: ["123456789012345678"]

sms:
  provider: twilio
  from: "+15550000000"
  account_sid: "AC..."
  auth_token: "..."

imessage:
  base_url: "http://localhost:1234"
  password: "..."
  poll_interval: "5s"

email:
  imap_addr: "imap.example.com:993"
  imap_username: "bot@example.com"
  imap_password: "..."
  smtp_addr: "smtp.example.com:587"
  smtp_username: "bot@example.com"
  smtp_password: "..."
  from: "bot@example.com"
  poll_interval: "30s"
```

## 故障排查

### `config: unmarshal: 1 error(s) decoding: ...`

YAML 有效但某字段类型错误。错误信息会指出字段名——请到 `internal/config/config.go` 检查类型。

### 环境变量覆盖未生效

Rousseau 为环境变量添加 `ROUSSEAU_` 前缀并把点替换为下划线。`anthropic.model` 变为 `ROUSSEAU_ANTHROPIC_MODEL`。`ANTHROPIC_API_KEY` 是特例，直接绑定到 `anthropic.api_key`。

### `config: read: yaml: line X: found character that cannot start any token`

制表符缩进。YAML 要求使用空格。

### 对 `config.yaml` 的修改不生效

Rousseau 只在启动时读取一次配置。请重启守护进程。

### 似乎有两个配置值都生效

优先级为 **flag > env > file > default**。启用 `log.level: debug` 并搜索 `config.loaded` 以查看已解析的值。

## 相关页面

- [参考：配置架构](/zh-Hans/reference/config-schema/)——所有字段。
- [参考：环境变量](/zh-Hans/reference/environment-variables/)——覆盖矩阵。
- [参考：CLI 命令](/zh-Hans/reference/cli-commands/)——各传输的选项。
- [提供方](/zh-Hans/providers/)——各提供方专属配置块。
- [传输](/zh-Hans/transports/)——各传输专属配置块。

## 延伸阅读

- `internal/config/config.go`——权威结构体。
- `internal/cli/root.go`——配置加载位置。
- `internal/config/config_test.go`——加载语义测试矩阵。
