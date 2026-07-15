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
description: "Complete reference for rousseau imessage: BlueBubbles URL/password, poll interval, exit codes, macOS requirement."
keywords: "imessage, bluebubbles, macos, cli reference, rousseau imessage"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/commands/imessage/"
subtitle: "Complete reference for `rousseau imessage`."
tags: "reference, cli, imessage, transports"
title: "rousseau imessage"

news_genres: "Blog"
news_keywords: "imessage, bluebubbles, macos"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "rousseau imessage"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 68
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/commands/imessage/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/commands/imessage/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "rousseau imessage"
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
twitter_description: "Complete reference for rousseau imessage: BlueBubbles URL/password, poll interval, exit codes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "rousseau imessage"
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

`rousseau imessage` runs the iMessage bridge by polling a locally installed [BlueBubbles](https://bluebubbles.app) server. BlueBubbles is a macOS-only helper that exposes iMessage over an HTTP + WebSocket API. Rousseau does not send iMessages directly (Apple does not offer a public API) — it goes through BlueBubbles.

Source: `internal/cli/imessage.go`. Transport: `internal/transport/imessage/`.

<aside class="admonition" data-type="warning"><span class="admonition-title">Requires a Mac</span><p>You must run a BlueBubbles server on a Mac signed into an Apple ID. Rousseau then talks to that Mac over the LAN or a tunnel. Non-Apple hosts cannot originate iMessages.</p></aside>

## Synopsis

```sh
rousseau imessage [--base-url http://host:port] [--password <pw>] [--poll-interval 5s]
```

## Flags

| Flag | Type | Default | Effect |
|---|---|---|---|
| `--base-url` | string | `imessage.base_url` | BlueBubbles server URL, e.g. `http://localhost:1234`. |
| `--password` | string | `imessage.password` | BlueBubbles server password. |
| `--poll-interval` | duration string | `imessage.poll_interval` | Cadence for `/api/v1/message`. |
| `--config` | string | inherits from root | Path to the YAML config file. |

## Config keys respected

`internal/config/config.go` `IMessageConfig`:

| Key | Type | Default | Effect |
|---|---|---|---|
| `imessage.base_url` | string | empty | Required. |
| `imessage.password` | string | empty | Required. |
| `imessage.chat_guid` | string | empty | Outbound target chat GUID (optional). |
| `imessage.poll_interval` | duration | `5s` | Poll cadence. |
| `imessage.reply_header` | string | empty | Prefix on outbound messages. |

## Allowlist syntax

iMessage has no `--allow` flag today. Filtering must happen at the BlueBubbles server side (its own contact allowlist), or use the `chat_guid` config to constrain outbound to a single conversation.

## Environment variables

| Variable | Effect |
|---|---|
| `ROUSSEAU_IMESSAGE_BASE_URL` | Override BlueBubbles URL. |
| `ROUSSEAU_IMESSAGE_PASSWORD` | Override BlueBubbles password. |

## Startup sequence

1. Resolve URL and password; fail if either is empty.
2. Default `claudecli.permission_mode` to `bypassPermissions`.
3. Parse `poll_interval`.
4. Open session store, build agent wiring.
5. `imessage.New` — instantiate the HTTP client.
6. `wiring.startCron` — cron delivery via BlueBubbles POST.
7. Poll loop until context cancelled.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Clean context cancellation. |
| 1 | Missing URL/password, HTTP failure, provider/store error. |
| 130 | SIGINT. |

## Worked examples

```sh
# Local BlueBubbles on the same Mac
rousseau imessage \
  --base-url http://localhost:1234 \
  --password "$BLUEBUBBLES_PW"

# Remote Mac via SSH tunnel
ssh -N -L 1234:localhost:1234 mac.internal &
rousseau imessage \
  --base-url http://localhost:1234 \
  --password "$BLUEBUBBLES_PW" \
  --poll-interval 3s
```

## Common failure modes

- **`401 Unauthorized`** — wrong password.
- **`Connection refused`** — BlueBubbles server not running or wrong port.
- **No inbound messages** — verify the BlueBubbles UI shows recent conversations; enable Full Disk Access in macOS for BlueBubbles.
- **Delayed replies** — reduce `poll_interval`; the default 5s is a compromise between latency and CPU.

## Related pages

- [Transports: iMessage](/transports/imessage/)
- [Best Practices: Secret management](/best-practices/secret-management/)
- [Reference: Logs](/reference/logs/)
