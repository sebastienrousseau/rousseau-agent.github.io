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
description: "Set up rousseau-agent's iMessage transport: BlueBubbles server on macOS, HTTP polling, poll interval, cursor deduplication, chat GUID for outbound."
keywords: "iMessage, BlueBubbles, macOS, HTTP polling, chat GUID, cursor, deduplication"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/transports/imessage/"
subtitle: "BlueBubbles HTTP polling from a macOS host."
tags: "transports, iMessage"
title: "iMessage Transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "iMessage, BlueBubbles, macOS, HTTP polling, chat GUID, cursor, deduplication"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "iMessage Transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 18
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/imessage/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/imessage/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "iMessage Transport"
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
twitter_description: "Set up rousseau-agent's iMessage transport: BlueBubbles server on macOS, HTTP polling, poll interval, cursor deduplication, chat GUID for outbound."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "iMessage Transport"
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

The iMessage transport (`internal/transport/imessage/`) does not touch iMessage directly — Apple provides no supported client-facing API. Instead it polls [BlueBubbles](https://bluebubbles.app), a macOS-side daemon that exposes iMessage via HTTP + Socket.IO.

rousseau uses BlueBubbles's HTTP endpoints only (Socket.IO is deliberately avoided to keep the dependency footprint small).

## Architecture

```
+-----------+     iMessage      +---------+     HTTP      +-----------+
| Apple ID  | <---------------> | macOS   | <-----------> | rousseau  |
|  server   |                   | Blue    |               | daemon    |
+-----------+                   | Bubbles |               |           |
                                +---------+               +-----------+
```

The macOS host runs BlueBubbles and stays signed into iMessage. rousseau polls BlueBubbles's `/api/v1/message` endpoint on the configured cadence and forwards new arrivals to the handler.

## Prerequisites

1. **A macOS host** with iMessage signed in. Not necessarily the same machine rousseau runs on.
2. **BlueBubbles server** installed on that host, listening on a URL rousseau can reach (LAN address, VPN, or Tailscale).
3. **BlueBubbles password** from the server GUI (Settings → Server Password).
4. **A chat GUID** for outbound. Find it in BlueBubbles's GUI or via `GET /api/v1/chat`.

## Configuration

```yaml
imessage:
  base_url: "http://mac.internal:1234"
  password: "..."
  chat_guid: "iMessage;-;+15550001234"
  poll_interval: "5s"
  reply_header: ""
```

| Field | Default | Effect |
|---|---|---|
| `base_url` | *required* | BlueBubbles server URL. |
| `password` | *required* | BlueBubbles server password. |
| `chat_guid` | *empty* | Outbound target GUID. |
| `poll_interval` | `5s` | Poll cadence against `/api/v1/message`. |
| `reply_header` | *empty* | Prepended to every outbound message. |

## Command-line

```sh
rousseau imessage \
  --base-url http://mac.internal:1234 \
  --password ... \
  --chat-guid 'iMessage;-;+15550001234' \
  --poll-interval 5s
```

## Cursor deduplication

On startup, the transport primes its `lastID` cursor to the newest existing message so the operator does not get spammed with the entire iMessage history. Every subsequent poll fetches the newest `PageSize` messages (default 25) and only forwards those newer than the cursor.

The cursor is in-memory. On restart, the cursor is re-primed from BlueBubbles — a small window of messages that arrived while the daemon was down will be missed. This is a deliberate trade-off; persistent cursor logic would require another table in the state store and iMessage delivery timestamps are not guaranteed monotonic across devices.

## Reachability

BlueBubbles must be network-reachable from wherever rousseau runs. Common patterns:

- **Same LAN.** `http://<mac-lan-ip>:1234`.
- **Tailscale.** `http://mac.tailnet.ts.net:1234`. Encrypts the link and works across NAT.
- **Reverse tunnel.** `http://localhost:1234` on the rousseau host with an SSH `-R` tunnel from the Mac.

Do not expose BlueBubbles to the public internet unless you understand the auth model (a single password).

## Failure modes

| Symptom | Fix |
|---|---|
| `imessage.prime_failed` on startup | BlueBubbles unreachable — check `base_url` and `password`. |
| Every historic message replays | `lastID` did not prime. Check permissions / auth. |
| Outbound messages silently dropped | Wrong `chat_guid`. Look it up via `GET /api/v1/chat`. |
| Messages arrive minutes late | Increase BlueBubbles's own polling frequency or lower `poll_interval`. |
