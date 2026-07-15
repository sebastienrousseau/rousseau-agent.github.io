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
hreflang: "en"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "en-GB"
locale: "en_GB"
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
permalink: "https://docs.rousseau-agent.dev/configuration/"
subtitle: "Every field in internal/config/config.go."
tags: "configuration, reference"
title: "Configuration Reference"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "configuration, config.yaml, viper, precedence, YAML, provider, transport, approver, compression"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Configuration Reference"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 4
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/configuration/index.html"
item_link: "https://docs.rousseau-agent.dev/configuration/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Configuration Reference"
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
twitter_title: "Configuration Reference"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Precedence

`rousseau` resolves configuration in the order **flag > env > file > default**. The file lives at `~/.config/rousseau/config.yaml` by default; override with `--config`.

Environment variables use the prefix `ROUSSEAU_` with `.` replaced by `_` — so `provider` becomes `ROUSSEAU_PROVIDER`, `anthropic.api_key` becomes `ROUSSEAU_ANTHROPIC_API_KEY`. `ANTHROPIC_API_KEY` is also honoured directly (it is bound to `anthropic.api_key` at load time).

## Top-level

| Field | Type | Default | Effect |
|---|---|---|---|
| `provider` | string | `claudecli` | LLM backend: `claudecli`, `anthropic`, `bedrock`, `vertex`, `openai`, `openrouter`, `ollama`. |

## `anthropic` — direct Anthropic API

| Field | Type | Default | Effect |
|---|---|---|---|
| `api_key` | string | *from `ANTHROPIC_API_KEY`* | Bearer for `api.anthropic.com`. Rejected if empty when the provider is selected. |
| `model` | string | `claude-sonnet-4-6` | Model identifier passed to the SDK. |
| `max_tokens` | int64 | `4096` | Caps output tokens per completion. |

See [/providers/anthropic/](/providers/anthropic/).

## `bedrock` — AWS Bedrock

| Field | Type | Default | Effect |
|---|---|---|---|
| `region` | string | *required* | AWS region (`us-east-1`, `eu-west-2`). |
| `model` | string | *required* | Bedrock model ID (`anthropic.claude-sonnet-4-6-20260101-v1:0`). |
| `profile` | string | *empty* | Credentials profile from `~/.aws/credentials`. Empty falls through the standard AWS credential chain. |
| `max_tokens` | int64 | SDK default | Caps output tokens. |

See [/providers/bedrock/](/providers/bedrock/).

## `vertex` — Google Vertex AI

| Field | Type | Default | Effect |
|---|---|---|---|
| `project` | string | *required* | GCP project ID. |
| `region` | string | *required* | Vertex region (`us-central1`). |
| `model` | string | *required* | Anthropic-on-Vertex model ID (`claude-sonnet-4-6@20260101`). |
| `credentials_file` | string | *empty* | Path to service-account or authorized-user JSON. Empty uses Application Default Credentials. |
| `max_tokens` | int64 | `4096` | Caps output tokens. |

See [/providers/vertex/](/providers/vertex/).

## `claudecli` — subprocess against local `claude` CLI

| Field | Type | Default | Effect |
|---|---|---|---|
| `binary` | string | `claude` | Executable, resolved on `$PATH`. |
| `model` | string | *empty* | Passed to `--model`. Empty uses claude's default. |
| `permission_mode` | string | *empty* | Passed to `--permission-mode`. Values: `acceptEdits`, `auto`, `bypassPermissions`, `default`, `dontAsk`, `plan`. Unattended daemons typically need `bypassPermissions`. |
| `extra_args` | []string | `[]` | Prepended before `-p` on every invocation. Useful for `--add-dir`, `--allowed-tools`, `--disallowed-tools`, `--plugin-dir`. |

See [/providers/claudecli/](/providers/claudecli/).

## `openai` / `openrouter` / `ollama` — OpenAI-compatible endpoints

Shared shape. `openrouter.base_url` defaults to `https://openrouter.ai/api/v1`; `ollama.base_url` defaults to `http://localhost:11434/v1`; `ollama.api_key` defaults to `not-required`.

| Field | Type | Default | Effect |
|---|---|---|---|
| `api_key` | string | *required* | Bearer token. Non-empty even for Ollama (any placeholder works). |
| `model` | string | *required* | Model identifier. There is no universal default across endpoints. |
| `base_url` | string | *provider default* | Full endpoint URL. |
| `max_tokens` | int64 | SDK default | Caps output tokens. |

See [/providers/openai-compatible/](/providers/openai-compatible/).

## `log`

| Field | Type | Default | Effect |
|---|---|---|---|
| `level` | string | `info` | `debug`, `info`, `warn`, `error`. |
| `format` | string | `text` | `text` (human) or `json` (production / log aggregation). |

## `state`

| Field | Type | Default | Effect |
|---|---|---|---|
| `path` | string | `~/.local/share/rousseau/sessions.db` | SQLite database path (WAL mode, `busy_timeout=15s`). |

## `agent`

| Field | Type | Default | Effect |
|---|---|---|---|
| `system_prompt` | string | *empty* | Overrides the built-in default. |
| `max_iterations` | int | `32` | Caps model round-trips per `Turn`. |
| `skills_dir` | string | *empty* | Directory of `*.md` skill files. Empty disables skills. |

### `agent.compression`

| Field | Type | Default | Effect |
|---|---|---|---|
| `enabled` | bool | `false` | Enables LLM-backed session compression. |
| `trigger_messages` | int | `60` | Message count above which compression fires. |
| `keep_recent` | int | `8` | Recent messages preserved verbatim. |
| `prompt` | string | *built-in* | Overrides the default summarisation instruction. |

### `agent.approver`

| Field | Type | Default | Effect |
|---|---|---|---|
| `mode` | string | `allow_all` | `allow_all`, `deny_all`, or `pattern`. |
| `reason` | string | *empty* | Denial reason surfaced to the model. |
| `default` | string | `deny` | Fallback when no `allow` or `deny` rule matches (pattern mode). |
| `allow` | []PatternEntry | `[]` | Regex allow rules per tool. |
| `deny` | []PatternEntry | `[]` | Regex deny rules per tool. Deny wins over allow. |

Each `PatternEntry` is `{tool: <name>, match: <regex>}`. `tool: ""` matches every tool; `match: ""` matches every input.

## Transport blocks

### `whatsapp`

| Field | Type | Default | Effect |
|---|---|---|---|
| `reply_header` | string | `💎 *Rousseau Agent*\n\n` | Prepended to every outbound message. Set to `" "` to disable. |
| `voice.enabled` | bool | `false` | Whisper-based transcription for inbound voice notes. |
| `voice.binary` | string | `whisper` | Whisper CLI executable. |
| `voice.model` | string | *empty* | Passed to `--model` (`base.en`, `small`). |
| `voice.model_path` | string | *empty* | Explicit `.bin` path, takes precedence over `model`. |
| `voice.language` | string | *empty* | Passed to `--language`. Empty auto-detects. |
| `voice.extra_args` | []string | `[]` | Appended to every whisper invocation. |

### `signal`

| Field | Type | Default | Effect |
|---|---|---|---|
| `binary` | string | `signal-cli` | Executable to invoke in JSON-RPC daemon mode. |
| `account` | string | *required* | E.164 phone number the daemon runs as. |
| `extra_args` | []string | `[]` | Inserted between `-a <account>` and `jsonRpc`. |
| `reply_header` | string | *empty* | Prepended to every outbound message. |
| `allowlist` | []string | `[]` | E.164 numbers whose messages are handled. Empty accepts every sender. |

### `telegram`

| Field | Type | Default | Effect |
|---|---|---|---|
| `token` | string | *required* | Bot token from BotFather. |
| `base_url` | string | `https://api.telegram.org` | Override for a local Bot API server. |
| `reply_header` | string | *empty* | Prepended to every outbound reply. |
| `allowlist` | []string | `[]` | Telegram user IDs whose messages are handled. |

### `matrix`

| Field | Type | Default | Effect |
|---|---|---|---|
| `homeserver_url` | string | *required* | Base URL, e.g. `https://matrix.org`. |
| `access_token` | string | *required* | Bot user's access token. |
| `user_id` | string | *empty* | Bot user's full MXID (`@bot:matrix.org`). Optional but recommended (own-message echo suppression). |
| `reply_header` | string | *empty* | Prepended to every outbound reply. |
| `allowlist` | []string | `[]` | Matrix IDs whose messages are handled. |

### `slack`

| Field | Type | Default | Effect |
|---|---|---|---|
| `app_token` | string | *required* | `xapp-*` app-level token with `connections:write`. |
| `bot_token` | string | *required* | `xoxb-*` bot token with `chat:write`. |
| `bot_user_id` | string | *empty* | Bot user's own `U…` ID for own-message loop prevention. |
| `reply_header` | string | *empty* | Prepended to every outbound message. |
| `allowlist` | []string | `[]` | Slack user IDs whose messages are handled. |

### `discord`

| Field | Type | Default | Effect |
|---|---|---|---|
| `token` | string | *required* | Bot token from the Developer Portal. |
| `reply_header` | string | *empty* | Prepended to every outbound reply. |
| `allowlist` | []string | `[]` | Discord user IDs whose messages are handled. |

### `sms`

| Field | Type | Default | Effect |
|---|---|---|---|
| `provider` | string | *required* | `twilio` or `vonage`. |
| `from` | string | *required* | E.164 sender or Twilio Messaging Service SID. |
| `account_sid` | string | *required for twilio* | Twilio account SID (`AC…`). |
| `auth_token` | string | *required* | Twilio auth token or Vonage API secret. |
| `api_key` | string | *required for vonage* | Vonage API key. |
| `base_url` | string | *provider default* | Override for regional or test endpoints. |
| `reply_header` | string | *empty* | Prepended to every outbound message. |

### `imessage`

| Field | Type | Default | Effect |
|---|---|---|---|
| `base_url` | string | *required* | BlueBubbles server URL (`http://localhost:1234`). |
| `password` | string | *required* | BlueBubbles server password. |
| `chat_guid` | string | *empty* | Outbound target GUID. |
| `poll_interval` | duration | `5s` | Poll cadence against `/api/v1/message`. |
| `reply_header` | string | *empty* | Prepended to every outbound message. |

### `email`

| Field | Type | Default | Effect |
|---|---|---|---|
| `imap_addr` | string | *required* | `host:port` for TLS-wrapped IMAP (typically `:993`). |
| `imap_username` | string | *required* | IMAP username. |
| `imap_password` | string | *required* | IMAP password. |
| `mailbox` | string | `INBOX` | Mailbox to poll. |
| `poll_interval` | duration | `30s` | How often to look for UNSEEN mail. |
| `smtp_addr` | string | *required* | `host:port` for SMTP submission (typically `:587`). |
| `smtp_username` | string | *required* | SMTP username. |
| `smtp_password` | string | *required* | SMTP password. |
| `from` | string | *required* | Envelope + header `From` address. |
| `reply_header` | string | *empty* | Prepended to every outbound message body. |

## Complete example

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

## Troubleshooting

### `config: unmarshal: 1 error(s) decoding: ...`

The YAML is valid but a field has the wrong type. The error message names the field — check the type in `internal/config/config.go`.

### Env var override not picked up

Rousseau prefixes env vars with `ROUSSEAU_` and replaces dots with underscores. `anthropic.model` becomes `ROUSSEAU_ANTHROPIC_MODEL`. `ANTHROPIC_API_KEY` is a special case wired directly to `anthropic.api_key`.

### `config: read: yaml: line X: found character that cannot start any token`

Tab indentation. YAML requires spaces.

### Changes to `config.yaml` do not take effect

Rousseau reads config once at startup. Restart the daemon.

### Two config values seem to be in effect

Precedence is **flag > env > file > default**. Enable `log.level: debug` and grep for `config.loaded` to see the resolved value.

## Related pages

- [Reference: Config Schema](/reference/config-schema/) — every field.
- [Reference: Environment Variables](/reference/environment-variables/) — override matrix.
- [Reference: CLI Commands](/reference/cli-commands/) — per-transport flags.
- [Providers](/providers/) — provider-specific stanzas.
- [Transports](/transports/) — transport-specific stanzas.

## Further reading

- `internal/config/config.go` — the authoritative struct.
- `internal/cli/root.go` — where config is loaded.
- `internal/config/config_test.go` — the loading semantics test matrix.
