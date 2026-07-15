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
description: "Every transport config field grouped into one page: whatsapp, signal, telegram, matrix, slack, discord, email, sms, imessage."
keywords: "config, transports, whatsapp, signal, telegram, matrix, slack, discord, email, sms, imessage"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/config/transports/"
subtitle: "Every knob for the nine transport blocks."
tags: "reference, config, transports"
title: "Config: Transports"

news_genres: "Blog"
news_keywords: "config, transports, whatsapp, signal, telegram, matrix, slack, discord, email, sms, imessage"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Config: Transports"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 84
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/config/transports/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/config/transports/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Config: Transports"
last_build_date: "Mon, 13 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
ttl: "60"
type: "website"
webmaster: sebastian.rousseau@gmail.com (Sebastien Rousseau)

apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "rousseau-agent"
apple-touch-fullscreen: "yes"

msapplication-navbutton-color: "rgb(26,58,138)"

twitter_card: "summary"
twitter_creator: "rousseauagent"
twitter_description: "Every transport config field grouped into one page: whatsapp, signal, telegram, matrix, slack, discord, email, sms, imessage."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Config: Transports"
twitter_url: "https://docs.rousseau-agent.dev"

author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Overview

Nine transport blocks live at the top of `Config` in `internal/config/config.go`. Each has its own struct (`WhatsAppConfig`, `SignalConfig`, and so on). Every field below cites the concrete struct field.

<aside class="admonition" data-type="tip"><span class="admonition-title">Naming</span><p>YAML keys follow <code>mapstructure</code> tags: <code>snake_case</code>. Env vars follow <code>ROUSSEAU_&lt;SECTION&gt;_&lt;KEY&gt;</code>.</p></aside>

## `whatsapp.*`

`WhatsAppConfig` + nested `VoiceConfig`.

| Field | Type | Default | Description | Source |
|---|---|---|---|---|
| `whatsapp.reply_header` | string | `"💎 *Rousseau Agent*\n\n"` (built-in) | Prepended to every outbound message. Set to `" "` to disable. | `WhatsAppConfig.ReplyHeader` |
| `whatsapp.voice.enabled` | bool | `false` | Enable whisper-based transcription. | `VoiceConfig.Enabled` |
| `whatsapp.voice.binary` | string | `whisper` | Whisper CLI. | `VoiceConfig.Binary` |
| `whatsapp.voice.model` | string | empty | `--model` value. | `VoiceConfig.Model` |
| `whatsapp.voice.model_path` | string | empty | Explicit `.bin` path, takes precedence over `model`. | `VoiceConfig.ModelPath` |
| `whatsapp.voice.language` | string | empty (auto) | `--language`. | `VoiceConfig.Language` |
| `whatsapp.voice.extra_args` | []string | empty | Appended to every whisper invocation. | `VoiceConfig.ExtraArgs` |

Note: WhatsApp has no `allowlist` on the config struct — it is a CLI flag only. See [rousseau whatsapp](/reference/commands/whatsapp/).

## `signal.*`

| Field | Type | Default | Description | Source |
|---|---|---|---|---|
| `signal.binary` | string | `signal-cli` | Path to executable. | `SignalConfig.Binary` |
| `signal.account` | string | empty (required) | E.164 phone number. | `SignalConfig.Account` |
| `signal.extra_args` | []string | empty | Inserted between `-a <acct>` and `jsonRpc`. | `SignalConfig.ExtraArgs` |
| `signal.reply_header` | string | empty | Prefix on outbound. | `SignalConfig.ReplyHeader` |
| `signal.allowlist` | []string | empty | E.164 numbers permitted. | `SignalConfig.Allowlist` |

## `telegram.*`

| Field | Type | Default | Description | Source |
|---|---|---|---|---|
| `telegram.token` | string | empty (required) | Bot token. | `TelegramConfig.Token` |
| `telegram.base_url` | string | `https://api.telegram.org` | Override endpoint. | `TelegramConfig.BaseURL` |
| `telegram.reply_header` | string | empty | Prefix on outbound. | `TelegramConfig.ReplyHeader` |
| `telegram.allowlist` | []string | empty | Chat ids as strings. | `TelegramConfig.Allowlist` |

## `matrix.*`

| Field | Type | Default | Description | Source |
|---|---|---|---|---|
| `matrix.homeserver_url` | string | empty (required) | Homeserver base URL. | `MatrixConfig.HomeserverURL` |
| `matrix.access_token` | string | empty (required) | Bot access token. | `MatrixConfig.AccessToken` |
| `matrix.user_id` | string | empty | Bot MXID. | `MatrixConfig.UserID` |
| `matrix.reply_header` | string | empty | Prefix on outbound. | `MatrixConfig.ReplyHeader` |
| `matrix.allowlist` | []string | empty | MXIDs permitted. | `MatrixConfig.Allowlist` |

## `slack.*`

| Field | Type | Default | Description | Source |
|---|---|---|---|---|
| `slack.app_token` | string | empty (required) | `xapp-*`. | `SlackConfig.AppToken` |
| `slack.bot_token` | string | empty (required) | `xoxb-*`. | `SlackConfig.BotToken` |
| `slack.bot_user_id` | string | empty | Bot user id for loop prevention. | `SlackConfig.BotUserID` |
| `slack.reply_header` | string | empty | Prefix on outbound. | `SlackConfig.ReplyHeader` |
| `slack.allowlist` | []string | empty | Slack user IDs permitted. | `SlackConfig.Allowlist` |

## `discord.*`

| Field | Type | Default | Description | Source |
|---|---|---|---|---|
| `discord.token` | string | empty (required) | Bot token. | `DiscordConfig.Token` |
| `discord.reply_header` | string | empty | Prefix on outbound. | `DiscordConfig.ReplyHeader` |
| `discord.allowlist` | []string | empty | User snowflakes permitted. | `DiscordConfig.Allowlist` |

## `email.*`

| Field | Type | Default | Description | Source |
|---|---|---|---|---|
| `email.imap_addr` | string | empty (required) | `host:port`. | `EmailConfig.IMAPAddr` |
| `email.imap_username` | string | empty (required) | IMAP user. | `EmailConfig.IMAPUsername` |
| `email.imap_password` | string | empty (required) | IMAP password. | `EmailConfig.IMAPPassword` |
| `email.mailbox` | string | `INBOX` | Polled mailbox. | `EmailConfig.Mailbox` |
| `email.poll_interval` | duration string | `30s` | Cadence. | `EmailConfig.PollInterval` |
| `email.smtp_addr` | string | empty (required) | `host:port`. | `EmailConfig.SMTPAddr` |
| `email.smtp_username` | string | empty (required) | SMTP user. | `EmailConfig.SMTPUsername` |
| `email.smtp_password` | string | empty (required) | SMTP password. | `EmailConfig.SMTPPassword` |
| `email.from` | string | empty (required) | `From:` address. | `EmailConfig.From` |
| `email.reply_header` | string | empty | Prefix on outbound. | `EmailConfig.ReplyHeader` |

## `sms.*`

| Field | Type | Default | Description | Source |
|---|---|---|---|---|
| `sms.provider` | string | empty (required) | `twilio` or `vonage`. | `SMSConfig.Provider` |
| `sms.from` | string | empty (required) | E.164 or MG SID. | `SMSConfig.From` |
| `sms.account_sid` | string | empty | Twilio AccountSID. | `SMSConfig.AccountSID` |
| `sms.auth_token` | string | empty | Twilio auth token or Vonage secret. | `SMSConfig.AuthToken` |
| `sms.api_key` | string | empty | Vonage API key. | `SMSConfig.APIKey` |
| `sms.base_url` | string | empty | Override for testing / regional. | `SMSConfig.BaseURL` |
| `sms.reply_header` | string | empty | Prefix on outbound. | `SMSConfig.ReplyHeader` |

## `imessage.*`

| Field | Type | Default | Description | Source |
|---|---|---|---|---|
| `imessage.base_url` | string | empty (required) | BlueBubbles URL. | `IMessageConfig.BaseURL` |
| `imessage.password` | string | empty (required) | BlueBubbles password. | `IMessageConfig.Password` |
| `imessage.chat_guid` | string | empty | Outbound target chat GUID. | `IMessageConfig.ChatGUID` |
| `imessage.poll_interval` | duration string | `5s` | Cadence. | `IMessageConfig.PollInterval` |
| `imessage.reply_header` | string | empty | Prefix on outbound. | `IMessageConfig.ReplyHeader` |

## Full example

```yaml
whatsapp:
  reply_header: "💎 *Rousseau Agent*\n\n"
  voice:
    enabled: true
    model: base.en

signal:
  account: "+447900123456"
  allowlist:
    - "+447900222222"

telegram:
  token: "7000000000:AAE…"
  allowlist:
    - "123456789"

matrix:
  homeserver_url: "https://matrix.internal.example"
  access_token: "syt_…"
  user_id: "@rousseau-bot:internal.example"
  allowlist:
    - "@alice:internal.example"

slack:
  app_token: "xapp-…"
  bot_token: "xoxb-…"
  bot_user_id: "U0ABC1234"
  allowlist: ["U0XYZ5678"]

discord:
  token: "MTIz…"
  allowlist: ["123456789012345678"]

email:
  imap_addr: imap.example.com:993
  imap_username: bot@example.com
  imap_password: "$IMAP_PW"
  smtp_addr: smtp.example.com:465
  smtp_username: bot@example.com
  smtp_password: "$SMTP_PW"
  from: bot@example.com
  poll_interval: 30s

sms:
  provider: twilio
  from: "+15550001111"
  account_sid: "$TWILIO_SID"
  auth_token: "$TWILIO_TOKEN"

imessage:
  base_url: http://localhost:1234
  password: "$BLUEBUBBLES_PW"
  poll_interval: 5s
```

## Related pages

- [Reference: Commands: whatsapp](/reference/commands/whatsapp/) — and every other per-command page
- [Transports](/transports/) — protocol-level detail per transport
- [Reference: Config: Provider](/reference/config/provider/)
- [Best Practices: Secret management](/best-practices/secret-management/)
