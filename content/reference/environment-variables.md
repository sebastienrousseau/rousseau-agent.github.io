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
changefreq: "monthly"
description: "Every environment variable rousseau-agent reads: the ROUSSEAU_ prefix from Viper, ANTHROPIC_API_KEY, XDG paths, provider SDK variables."
keywords: "environment variables, ROUSSEAU_, ANTHROPIC_API_KEY, viper, XDG"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/environment-variables/"
subtitle: "Every environment variable rousseau reads, at what layer, with what default."
tags: "reference, environment, viper, secrets"
title: "Reference: Environment Variables"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "environment variables, ROUSSEAU_, ANTHROPIC_API_KEY, viper, XDG"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Reference: Environment Variables"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 51
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/environment-variables/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/environment-variables/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Reference: Environment Variables"
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
twitter_title: "Reference: Environment Variables"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## How rousseau reads the environment

Two mechanisms, in this order (see `config.Load` in `internal/config/config.go`):

1. **Viper's automatic env binding.** `SetEnvPrefix("ROUSSEAU")` plus `SetEnvKeyReplacer(".", "_")` means every config field is reachable as `ROUSSEAU_<UPPER_SNAKE>`. So `provider` becomes `ROUSSEAU_PROVIDER`, `agent.approver.mode` becomes `ROUSSEAU_AGENT_APPROVER_MODE`.
2. **Explicit override.** `ANTHROPIC_API_KEY` is read directly out of the environment and forced into `anthropic.api_key`, so the standard Anthropic SDK convention just works. No other keys are picked up implicitly.

Everything else on this page is either a Viper-mapped variable, an SDK-managed variable rousseau does not touch but the underlying library does, or an XDG path used to compute defaults.

Precedence stays: **flag > env > file > default**.

## `ROUSSEAU_*` prefix

Every `mapstructure` tag in `internal/config/config.go` is reachable via `ROUSSEAU_<UPPER_SNAKE_PATH>`. Selected examples — full list follows the config struct:

| Variable | Category | Default | Description |
|---|---|---|---|
| `ROUSSEAU_PROVIDER` | core | `claudecli` | Provider identifier: `claudecli`, `anthropic`, `openai`, `openrouter`, `ollama`, `bedrock`, `vertex`. |
| `ROUSSEAU_LOG_LEVEL` | logging | `info` | slog level: `debug`, `info`, `warn`, `error`. |
| `ROUSSEAU_LOG_FORMAT` | logging | `text` | `text` or `json`. |
| `ROUSSEAU_STATE_PATH` | state | `$HOME/.local/share/rousseau/sessions.db` | Session store DSN. |
| `ROUSSEAU_AGENT_MAX_ITERATIONS` | agent | `32` | Tool-use iteration cap per turn. |
| `ROUSSEAU_AGENT_APPROVER_MODE` | agent | `` | `allow_all`, `deny_all`, `pattern`. |
| `ROUSSEAU_AGENT_APPROVER_DEFAULT` | agent | `` | For `pattern`: `allow` or `deny` on unmatched calls. |
| `ROUSSEAU_AGENT_COMPRESSION_ENABLED` | agent | `false` | Turn on the LLM compressor. |
| `ROUSSEAU_AGENT_COMPRESSION_TRIGGER_MESSAGES` | agent | `60` | Compress once message count exceeds this. |
| `ROUSSEAU_AGENT_COMPRESSION_KEEP_RECENT` | agent | `8` | How many recent messages to preserve verbatim. |
| `ROUSSEAU_AGENT_SKILLS_DIR` | agent | `$HOME/.local/share/rousseau/skills` | Skills directory. |
| `ROUSSEAU_ANTHROPIC_API_KEY` | provider | — | Same as `ANTHROPIC_API_KEY`. |
| `ROUSSEAU_ANTHROPIC_MODEL` | provider | `claude-sonnet-4-6` | Anthropic model id. |
| `ROUSSEAU_ANTHROPIC_MAX_TOKENS` | provider | `4096` | Max response tokens. |
| `ROUSSEAU_CLAUDECLI_BINARY` | provider | `claude` | Executable name for the `claudecli` provider. |
| `ROUSSEAU_CLAUDECLI_MODEL` | provider | — | Passed to `claude --model`. |
| `ROUSSEAU_CLAUDECLI_PERMISSION_MODE` | provider | — | `default`, `acceptEdits`, `bypassPermissions`, `plan`, etc. |
| `ROUSSEAU_OPENAI_API_KEY` | provider | — | Bearer for OpenAI-compat endpoints. |
| `ROUSSEAU_OPENAI_MODEL` | provider | — | Model id. |
| `ROUSSEAU_OPENAI_BASE_URL` | provider | — | Override the endpoint. |
| `ROUSSEAU_OPENROUTER_API_KEY` | provider | — | Bearer for OpenRouter. |
| `ROUSSEAU_OPENROUTER_MODEL` | provider | — | Model slug. |
| `ROUSSEAU_OPENROUTER_BASE_URL` | provider | `https://openrouter.ai/api/v1` | Override endpoint. |
| `ROUSSEAU_OLLAMA_MODEL` | provider | — | Model tag. |
| `ROUSSEAU_OLLAMA_BASE_URL` | provider | `http://localhost:11434/v1` | Local Ollama endpoint. |
| `ROUSSEAU_BEDROCK_REGION` | provider | — | AWS region. |
| `ROUSSEAU_BEDROCK_MODEL` | provider | — | Bedrock model id. |
| `ROUSSEAU_BEDROCK_PROFILE` | provider | — | AWS named profile. |
| `ROUSSEAU_VERTEX_PROJECT` | provider | — | GCP project. |
| `ROUSSEAU_VERTEX_REGION` | provider | — | Vertex region. |
| `ROUSSEAU_VERTEX_MODEL` | provider | — | Anthropic-on-Vertex model. |
| `ROUSSEAU_VERTEX_CREDENTIALS_FILE` | provider | — | Path to service-account JSON. |
| `ROUSSEAU_WHATSAPP_REPLY_HEADER` | transport | `💎 *Rousseau Agent*\n\n` | Prepended to every WhatsApp outbound message. |
| `ROUSSEAU_WHATSAPP_VOICE_ENABLED` | transport | `false` | Enable whisper transcription of voice notes. |
| `ROUSSEAU_WHATSAPP_VOICE_BINARY` | transport | `whisper` | whisper.cpp executable. |
| `ROUSSEAU_WHATSAPP_VOICE_MODEL` | transport | — | whisper model name (`base.en`, `small`). |
| `ROUSSEAU_WHATSAPP_VOICE_MODEL_PATH` | transport | — | Explicit .bin path (takes precedence over model). |
| `ROUSSEAU_WHATSAPP_VOICE_LANGUAGE` | transport | — | ISO code; empty auto-detects. |
| `ROUSSEAU_SIGNAL_BINARY` | transport | `signal-cli` | signal-cli executable. |
| `ROUSSEAU_SIGNAL_ACCOUNT` | transport | — | E.164 phone number. |
| `ROUSSEAU_SIGNAL_REPLY_HEADER` | transport | — | Reply header. |
| `ROUSSEAU_TELEGRAM_TOKEN` | transport | — | Bot API token. |
| `ROUSSEAU_TELEGRAM_BASE_URL` | transport | — | Override Bot API endpoint. |
| `ROUSSEAU_MATRIX_HOMESERVER_URL` | transport | — | Homeserver base URL. |
| `ROUSSEAU_MATRIX_ACCESS_TOKEN` | transport | — | Matrix access token. |
| `ROUSSEAU_MATRIX_USER_ID` | transport | — | Full MXID (`@bot:example.org`). |
| `ROUSSEAU_SLACK_APP_TOKEN` | transport | — | `xapp-…` app-level token. |
| `ROUSSEAU_SLACK_BOT_TOKEN` | transport | — | `xoxb-…` bot token. |
| `ROUSSEAU_SLACK_BOT_USER_ID` | transport | — | Bot's user id for self-echo suppression. |
| `ROUSSEAU_DISCORD_TOKEN` | transport | — | Discord bot token. |
| `ROUSSEAU_SMS_PROVIDER` | transport | — | `twilio` or `vonage`. |
| `ROUSSEAU_SMS_FROM` | transport | — | Sender number. |
| `ROUSSEAU_SMS_ACCOUNT_SID` | transport | — | Twilio account SID. |
| `ROUSSEAU_SMS_AUTH_TOKEN` | transport | — | Twilio/Vonage secret. |
| `ROUSSEAU_SMS_API_KEY` | transport | — | Vonage API key. |
| `ROUSSEAU_SMS_BASE_URL` | transport | — | Override for regional endpoints or tests. |
| `ROUSSEAU_IMESSAGE_BASE_URL` | transport | — | BlueBubbles server URL. |
| `ROUSSEAU_IMESSAGE_PASSWORD` | transport | — | BlueBubbles password. |
| `ROUSSEAU_IMESSAGE_CHAT_GUID` | transport | — | Outbound target. |
| `ROUSSEAU_IMESSAGE_POLL_INTERVAL` | transport | `2s` | Duration string. |
| `ROUSSEAU_EMAIL_IMAP_ADDR` | transport | — | IMAP server. |
| `ROUSSEAU_EMAIL_IMAP_USERNAME` | transport | — | IMAP user. |
| `ROUSSEAU_EMAIL_IMAP_PASSWORD` | transport | — | IMAP password. |
| `ROUSSEAU_EMAIL_MAILBOX` | transport | — | Folder to watch. |
| `ROUSSEAU_EMAIL_POLL_INTERVAL` | transport | — | Duration string. |
| `ROUSSEAU_EMAIL_SMTP_ADDR` | transport | — | SMTP submission host. |
| `ROUSSEAU_EMAIL_SMTP_USERNAME` | transport | — | SMTP user. |
| `ROUSSEAU_EMAIL_SMTP_PASSWORD` | transport | — | SMTP password. |
| `ROUSSEAU_EMAIL_FROM` | transport | — | From address. |

**Allowlist arrays** (`ROUSSEAU_SLACK_ALLOWLIST`, `ROUSSEAU_DISCORD_ALLOWLIST`, `ROUSSEAU_TELEGRAM_ALLOWLIST`, …) are supported by Viper but comma-separated env-string parsing is finicky — prefer setting these in `config.yaml`.

## Explicit env vars (outside the ROUSSEAU_ prefix)

| Variable | Source | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | `config.Load` (`internal/config/config.go` line 275) | Populates `anthropic.api_key`. Standard Anthropic SDK convention. |
| `HOME` | `internal/cli/init.go` | Used by `rousseau init` to compute the default state path. |

## SDK-owned variables rousseau does not touch

Some provider libraries pick up their own environment. Rousseau does not read these itself, but they influence behaviour when the corresponding provider is selected:

| Variable | Consumer | Notes |
|---|---|---|
| `AWS_PROFILE`, `AWS_REGION`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`, `AWS_WEB_IDENTITY_TOKEN_FILE` | `aws-sdk-go-v2` (Bedrock) | The standard credential chain. Prefer IRSA or profile-based creds over static keys. |
| `GOOGLE_APPLICATION_CREDENTIALS` | Google auth libraries (Vertex) | Path to a service-account JSON. Superseded by `vertex.credentials_file` in `config.yaml` if set. |
| `OPENAI_API_KEY` | The upstream Go OpenAI clients typically read this | Rousseau explicitly wires the key through `openai.api_key`; nothing implicit. |
| `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY` | Go net/http | Universal Go proxy variables. Useful for corporate egress paths. |

## XDG path variables

Rousseau follows the XDG Base Directory Specification for state and config, with two fallbacks:

| Variable | Effect |
|---|---|
| `XDG_CONFIG_HOME` | `$XDG_CONFIG_HOME/rousseau/config.yaml` is the default config path (referenced in `internal/cli/root.go`). |
| `XDG_DATA_HOME` | Default state path `$XDG_DATA_HOME/rousseau/sessions.db` (referenced by `whatsapp.go`, `skills.go`, `init.go`). |
| `HOME` | Fallback when the XDG variables are unset; rousseau uses `os.UserHomeDir()` in `internal/config/config.go`. |

The container Quadlet unit at `docker/rousseau-agent.container` sets both `HOME=/home/rousseau` and `XDG_DATA_HOME=/home/rousseau/.local/share`.

## Secret hygiene

Store secrets in one of three places:

1. **A systemd unit `EnvironmentFile=`** — `chmod 0600`, root-owned or user-owned as appropriate. Referenced from the Quadlet unit — see the [VPS deployment tutorial](/tutorials/deploy-to-a-vps/).
2. **A `.env` file loaded by your shell.** For desktop use only; keep it out of source control.
3. **A secret manager.** AWS Secrets Manager, HashiCorp Vault, or `pass`/`gopass`. Pipe the value into the process at start.

Never commit secrets to `config.yaml`. `config.yaml` is the right place for allowlists, base URLs, and non-secret configuration; it is the wrong place for API keys and bot tokens.

## Troubleshooting

### `ROUSSEAU_...` set but rousseau still uses the default

Env vars are read at start. Restart the daemon after export. Also verify the transformation rule: dots in the config key become underscores, and the prefix is `ROUSSEAU_` (uppercase, exact).

### `ANTHROPIC_API_KEY` seemingly ignored

The env var is only consulted when `provider: anthropic` is active. Under `provider: claudecli`, the `claude` CLI reads its own credentials.

### Different value on different hosts

The precedence is **flag &gt; env &gt; file &gt; default**. If a flag is set (from the systemd unit's `ExecStart` for example), it wins over both env and file.

### `GOOGLE_APPLICATION_CREDENTIALS` unreadable inside the container

Ensure the file is bind-mounted read-only into the container and the container UID (1000 by default) can read it.

## Related pages

- [Configuration](/configuration/) — every config field with default.
- [Reference: Config schema](/reference/config-schema/) — the YAML structure.
- [Reference: CLI Commands](/reference/cli-commands/) — per-transport flags.
- [Guides: Enterprise Onboarding](/guides/enterprise-onboarding/) — secret handling in production.
- [Deployment](/deployment/) — secrets management options.

## Further reading

- `internal/config/config.go` — `Load` sets the env prefix and dot-underscore key replacer.
- `internal/cli/root.go` — where `Load` is called.
