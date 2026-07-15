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
changefreq: "monthly"
description: "Overview of rousseau-agent's nine chat transports: WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, Email, SMS. Every transport implements Start / Stop / Deliver."
keywords: "transports, WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, email, SMS"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/transports/"
subtitle: "Nine chat transports behind one Transport interface."
tags: "transports, overview"
title: "Transports"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "transports, WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, email, SMS"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transports"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 11
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transports"
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
twitter_description: "Overview of rousseau-agent's nine chat transports: WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, Email, SMS. Every transport implements Start / Stop / Deliver."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transports"
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

## The Transport interface

Every transport implements one small interface (`internal/transport/transport.go`):

```go
type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

Above the transport sits the `Router`, which handles per-sender session lookup, allowlist enforcement, and dispatch to the `Agent`. Below sits the transport-specific wire code.

None of the shipped transports expose a public HTTP surface by default. This is a deliberate posture choice — rousseau daemons should be safe to run behind NAT with no port-forwarding rules.

## Supported transports

| Transport | Inbound | Outbound | Backing library / protocol | Auth | One-line setup |
|---|:---:|:---:|---|---|---|
| [WhatsApp](/transports/whatsapp/) | yes | yes | `go.mau.fi/whatsmeow` | Device pair (QR) | `rousseau whatsapp --allow <jid>` |
| [Signal](/transports/signal/) | yes | yes | `signal-cli` JSON-RPC | Pre-registered account | `rousseau signal --account +447900123456` |
| [Telegram](/transports/telegram/) | yes | yes | Bot API long-polling | BotFather token | `rousseau telegram --token <token>` |
| [Matrix](/transports/matrix/) | yes | yes | Client-server API `/sync` | Access token | `rousseau matrix --homeserver-url … --access-token …` |
| [Slack](/transports/slack/) | yes | yes | Socket Mode + Web API | `xapp-*` + `xoxb-*` | `rousseau slack --app-token … --bot-token …` |
| [Discord](/transports/discord/) | yes | yes | Gateway v10 + REST | Bot token | `rousseau discord --token <token>` |
| [iMessage](/transports/imessage/) | yes | yes | BlueBubbles HTTP polling | Server password | `rousseau imessage --base-url … --password …` |
| [Email](/transports/email/) | yes | yes | IMAP + SMTP | Username + password | `rousseau email --imap-addr … --smtp-addr …` |
| [SMS](/transports/sms/) | no | yes | Twilio or Vonage REST | Account SID / API key | `rousseau sms --provider twilio --account-sid … --auth-token …` |

## Why no public HTTP surface

Two design choices keep every listed transport away from a public webhook:

- **WebSocket-based inbound.** Slack Socket Mode and Discord Gateway are outbound-only from the daemon's perspective — the daemon dials the vendor over TLS and messages arrive on the same connection.
- **Polling.** WhatsApp, Telegram, Matrix, iMessage, and email pull for updates on their own cadence. There is no webhook the vendor calls into.

SMS is the exception, and rousseau resolves it by making SMS **send-only**. Inbound SMS would require a Twilio / Vonage webhook, which is exactly the surface this project refuses to introduce.

## Router behaviour

The router (`internal/transport/router.go`) sits between every transport and the `Agent`:

- **Session isolation.** Every distinct `From` value gets its own `Session`, so parallel conversations do not cross-contaminate. WhatsApp LID identities are normalised to phone JIDs first (see `internal/transport/whatsapp/resolve.go`).
- **Allowlist.** Every transport that supports inbound has an `Allowlist []string` in its config. Empty means "accept every sender" — for daemons you always want at least one entry.
- **Dispatch.** The router serialises turns per session so a user cannot stack two concurrent inbound messages.

## Adding a tenth transport

Implement `transport.Transport` (three methods). Add a `Config` type mirroring the block layout under `internal/config/`. Wire a CLI command in `internal/cli/`. That is the surface — the agent core stays untouched.

## Per-transport pages

- [WhatsApp](/transports/whatsapp/)
- [Signal](/transports/signal/)
- [Telegram](/transports/telegram/)
- [Matrix](/transports/matrix/)
- [Slack](/transports/slack/)
- [Discord](/transports/discord/)
- [iMessage](/transports/imessage/)
- [Email](/transports/email/)
- [SMS](/transports/sms/)
