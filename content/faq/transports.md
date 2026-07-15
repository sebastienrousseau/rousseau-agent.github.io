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
description: "Fifteen transport-specific questions about WhatsApp, Signal, Telegram, Matrix, Slack, Discord, Email, SMS, iMessage."
keywords: "faq, transports, whatsapp, slack, discord, matrix, signal, telegram, email, sms, imessage"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/faq/transports/"
subtitle: "Transport-specific FAQ."
tags: "faq, transports"
title: "FAQ: Transports"

news_genres: "Blog"
news_keywords: "faq, transports"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "FAQ: Transports"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "faq"
order: 13
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/faq/transports/index.html"
item_link: "https://docs.rousseau-agent.dev/faq/transports/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "FAQ: Transports"
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
twitter_description: "Fifteen transport-specific questions."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "FAQ: Transports"
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

Fifteen questions about the nine transport bridges — the operational subset that tends to bite people in production.

## Questions

### 1. Do any transports open inbound HTTP ports?

No. Every inbound transport uses either an outbound WebSocket (Slack Socket Mode, Discord Gateway) or long polling (Telegram, Matrix `/sync`, email IMAP, iMessage). SMS is send-only for exactly this reason.

### 2. Can I run more than one transport at once?

Yes. Run each as its own subcommand (e.g. under separate systemd units). They share the session store.

### 3. Is the WhatsApp integration official?

No. It uses the whatsmeow library which speaks the unofficial WhatsApp Web protocol. Meta can and does ban numbers using unofficial clients.

### 4. Can I lose access to my WhatsApp number?

Yes. Do not run this bridge on a number you rely on. See [Transports: WhatsApp](/transports/whatsapp/).

### 5. Do I need signal-cli for Signal?

Yes. Rousseau does not embed the Signal protocol; it drives `signal-cli` via JSON-RPC over a subprocess.

### 6. How does the Matrix bridge handle encrypted rooms?

It doesn't. Encrypted (Olm/Megolm) rooms are unsupported today. Invite the bot into unencrypted rooms.

### 7. Why is SMS outbound-only?

Inbound SMS requires a public HTTP webhook. That conflicts with rousseau's zero-inbound-surface posture. Use SMS with cron or from other scripts.

### 8. Can iMessage work without a Mac?

No. Apple has no public API. Rousseau polls a locally installed BlueBubbles server on a Mac.

### 9. Does email support STARTTLS?

Not currently. Direct TLS on port 993 (IMAP) and port 465 (SMTP) only.

### 10. Does the Slack bridge need a public webhook URL?

No. Socket Mode is a purely outbound WebSocket, so no public endpoint is required.

### 11. Does the Discord bridge need extra intents?

Yes, the Message Content privileged intent. Enable it in the Developer Portal.

### 12. How do allowlists work?

Every transport reads a list of IDs / JIDs / numbers. Only messages from listed senders enter the router. Empty allowlist = everyone (do not use in production).

### 13. Can I add a tenth transport?

Yes. Implement the `transport.Transport` interface (`Start`, `Stop`, `Deliver`) under `internal/transport/<name>/`, wire it in `internal/cli/<name>.go`, add a config block. See [Community: Contributing](/community/contributing/).

### 14. Do cron jobs work with every transport?

Yes. Every transport gets a `Deliver` method, and `wiring.startCron` runs inside the transport daemon. The cron `--deliver-to` value is transport-specific (JID for WhatsApp, snowflake for Discord, etc.).

### 15. Where do transport-level failures show up?

Structured events like `whatsapp.error`, `slack.error`, `matrix.disconnected`. See [Reference: Logs](/reference/logs/).

## Related pages

- [Transports](/transports/)
- [Reference: Config: Transports](/reference/config/transports/)
- [Reference: Commands: whatsapp](/reference/commands/whatsapp/) — and every other per-command page
- [FAQ: General](/faq/general/)
- [FAQ: Security](/faq/security/)
