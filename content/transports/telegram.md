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
description: "Set up rousseau-agent's Telegram transport: BotFather token, long-polling, allowlist by numeric user ID, reply-header customisation."
keywords: "Telegram, Bot API, BotFather, long polling, getUpdates, allowlist, chat ID"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/transports/telegram/"
subtitle: "Telegram Bot API over long-polling."
tags: "transports, Telegram"
title: "Telegram Transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Telegram, Bot API, BotFather, long polling, getUpdates, allowlist, chat ID"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Telegram Transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 14
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/telegram/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/telegram/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Telegram Transport"
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
twitter_description: "Set up rousseau-agent's Telegram transport: BotFather token, long-polling, allowlist by numeric user ID, reply-header customisation."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Telegram Transport"
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

## Overview

The Telegram transport (`internal/transport/telegram/`) speaks the Telegram Bot HTTP API directly — no third-party SDK. Long-polling `getUpdates` for inbound; `sendMessage` for outbound.

## Prerequisites

1. **A bot.** In Telegram, message [@BotFather](https://t.me/BotFather), send `/newbot`, choose a name and a `_bot`-suffixed username. BotFather hands back an HTTP API token that looks like `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`.
2. **The user IDs you want to authorise.** Telegram user IDs are numeric. The bot cannot resolve `@username` to a user ID by itself — the standard trick is to have every authorised user send `/start` to the bot once, then read the `from.id` from the log.

## Configuration

```yaml
telegram:
  token: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
  reply_header: ""
  allowlist:
    - "12345678"
    - "98765432"
```

| Field | Default | Effect |
|---|---|---|
| `token` | *required* | Bot token from BotFather. |
| `base_url` | `https://api.telegram.org` | Override for a local Bot API server. |
| `reply_header` | *empty* | Prepended to every outbound reply. |
| `allowlist` | `[]` | Telegram user IDs whose messages are handled. |

## Command-line

```sh
rousseau telegram --token 123456:ABC... --allow 12345678 --allow 98765432
```

`--allow` may be repeated.

## Long-polling

The transport calls `getUpdates` with a 30-second `PollTimeout` by default (`internal/transport/telegram/client.go`). Every returned update advances an internal `offset`, so messages are never redelivered even across restarts.

There is no webhook. The daemon needs no inbound HTTP surface.

## Message shape

Only text messages are handled. Media, stickers, and voice notes are ignored (a future upgrade could route audio through the same whisper.cpp path as WhatsApp).

## Failure modes

| Symptom | Fix |
|---|---|
| No updates arrive | Confirm the bot has been messaged at least once — Telegram does not deliver historic messages. |
| 409 Conflict on getUpdates | Another instance is polling with the same token. Stop the other one. |
| Allowlist rejects a real user | Log the `from.id` field; user IDs are numeric and do not match `@username`. |
