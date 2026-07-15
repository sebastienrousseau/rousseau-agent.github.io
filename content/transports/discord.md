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
description: "Set up rousseau-agent's Discord transport: Gateway v10 WebSocket, bot token, Message Content intent, allowlist by user ID."
keywords: "Discord, Gateway v10, WebSocket, bot token, Message Content intent, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/transports/discord/"
subtitle: "Discord Gateway v10 over WebSocket."
tags: "transports, Discord"
title: "Discord Transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Discord, Gateway v10, WebSocket, bot token, Message Content intent, allowlist"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Discord Transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 17
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/discord/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/discord/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Discord Transport"
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
twitter_description: "Set up rousseau-agent's Discord transport: Gateway v10 WebSocket, bot token, Message Content intent, allowlist by user ID."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Discord Transport"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">What you'll learn</span><p>The Discord Developer Portal walkthrough, which Gateway intents rousseau needs and why, the permissions bit calculator explained, and the failure modes for common misconfigurations. Read <code>internal/transport/discord/client.go</code> alongside this page.</p></aside>

## Overview

The Discord transport (`internal/transport/discord/`) speaks the Discord Gateway v10 protocol directly — no third-party SDK. WebSocket for inbound (`Identify → Ready → Heartbeat/Ack → Dispatch(MESSAGE_CREATE)`); REST for outbound (`POST /channels/{id}/messages`).

## Prerequisites

1. **A Discord Application with a Bot user.** Create at https://discord.com/developers/applications → **New Application** → **Bot** tab → **Add Bot**.
2. **A bot token** (Bot tab → **Reset Token** → copy the token — you only see it once).
3. **Message Content intent enabled** (Bot tab → **Privileged Gateway Intents**). Without this, the Gateway strips message text from every event and rousseau will see empty bodies.
4. **The bot invited to at least one server** (or DMs enabled). Generate the invite URL under **OAuth2 → URL Generator** with the `bot` scope and `Send Messages` + `Read Message History` permissions.

## Configuration

```yaml
discord:
  token: "Bot MTIz..."
  reply_header: ""
  allowlist:
    - "123456789012345678"
```

| Field | Default | Effect |
|---|---|---|
| `token` | *required* | Bot token from the Developer Portal. |
| `reply_header` | *empty* | Prepended to every outbound reply. |
| `allowlist` | `[]` | Discord user IDs whose messages are handled. |

## Command-line

```sh
rousseau discord --token 'MTIz...' --allow 123456789012345678
```

## Gateway intents

rousseau requests three intents (`internal/transport/discord/client.go`):

| Intent | Bit | Purpose |
|---|---|---|
| `GUILD_MESSAGES` | `1 << 9` | Messages in server channels. |
| `DIRECT_MESSAGES` | `1 << 12` | DMs to the bot. |
| `MESSAGE_CONTENT` | `1 << 15` | Populates the `content` field. **Must be enabled in the portal.** |

Without the Message Content intent, `MESSAGE_CREATE` events arrive with empty `content` and rousseau will log `discord.empty_body`.

## Heartbeat

The transport honours the Gateway's `heartbeat_interval` from the Hello opcode, sending Heartbeat + tracking `heartbeat_ack`. Missed acks close the socket and let systemd restart the process.

## Reply header

Discord renders `**text**` as bold and does not require any specific header shape. Override as needed:

```yaml
discord:
  reply_header: "**Rousseau Agent**\n"
```

## Permissions bit calculator

Discord uses a bitmask to encode a bot's channel permissions. Each permission is a power of 2. Common ones for rousseau:

| Permission | Bit |
|---|---|
| Read Messages / View Channels | `1 << 10` = `1024` |
| Send Messages | `1 << 11` = `2048` |
| Send Messages in Threads | `1 << 38` = `274877906944` |
| Read Message History | `1 << 16` = `65536` |
| Add Reactions | `1 << 6` = `64` |

To grant multiple permissions, OR the bits together and paste the resulting integer into the OAuth2 URL Generator's `permissions=` parameter:

```
Read Messages (1024) OR Send Messages (2048) OR Read Message History (65536) = 68608
```

<aside class="admonition" data-type="note"><span class="admonition-title">Portal helper</span><p>The developer portal's <em>OAuth2 URL Generator</em> lets you tick permission checkboxes and computes the integer for you. Bookmark the generated URL — it lets server admins invite the bot to any Discord server.</p></aside>

## Gateway lifecycle

The Gateway is stateful:

```
Client                        Discord Gateway
  │
  │   ────  Connect  ────▶
  │   ◀── HELLO (heartbeat_interval)
  │
  │   ───── IDENTIFY (token, intents) ────▶
  │   ◀── READY (session_id, user)
  │
  │   ─── Heartbeat every N ms ─▶
  │   ◀── HEARTBEAT_ACK
  │
  │   ◀── MESSAGE_CREATE (a user typed)
  │   ─── (rousseau handles + POSTs reply)
  │
  │   ◀── Disconnect (code 4009: session timed out)
  │   ─── RESUME (session_id) or re-IDENTIFY
```

The client tracks `heartbeat_ack`. If an ack is missed, the socket closes and the process exits — systemd or the container runtime restarts.

## Failure modes

| Symptom | Fix |
|---|---|
| Bot sees empty messages | Enable Message Content intent in the developer portal. |
| Gateway closes with code 4004 | Invalid token. Regenerate. |
| Bot cannot see any channels | Confirm the OAuth2 invite included the `bot` scope. |
| 403 on send | Bot lacks `Send Messages` permission in that channel. |
| Code 4014 on Identify | Requested an intent your app is not approved for (usually Message Content on a 100+ server bot). Verify your bot. |
| Code 4009 (session timed out) | Normal after long idle. Rousseau reconnects transparently. |

## Troubleshooting

### Gateway 4013 (Invalid Intents)

You are requesting an intent bit that does not exist. This usually means a mismatch between the client library's intent constants and Discord's current intent map. Rousseau builds the intent bitmask in `internal/transport/discord/client.go`; upgrade to the latest release if you see 4013 after a Discord API change.

### Bot receives events but does not respond

Allowlist mismatch. The `--allow` value must be the numeric Discord user ID (not username, not display name). Retrieve it in Discord: enable Developer Mode in *User Settings &gt; Advanced*, then right-click a user &gt; *Copy User ID*.

### DMs work but guild channels do not

Missing `GUILD_MESSAGES` intent, or the bot has not been invited to the guild. Guild permissions are separate from DM permissions — the bot must have the `Read Messages` permission for the channel.

### `429 Too Many Requests` on outbound

Discord enforces a global 50 req/s rate limit per bot, plus per-channel limits. Under sustained load, rousseau does not currently retry — the caller must back off. See [Guides: Rate limits](/guides/rate-limits/).

### Bot online status flaps

Discord considers a bot offline after ~40s without a heartbeat. Log line `discord.heartbeat_missed` indicates a network problem or CPU-starved daemon. Verify the container has enough CPU allocated.

## Related pages

- [Getting Started: First Transport](/getting-started/first-transport/) — end-to-end walkthrough.
- [Configuration](/configuration/) — the `discord` config block.
- [Transports](/transports/) — sibling transports.
- [Guides: Audit &amp; Approval Policies](/guides/audit-approval-policies/) — policy for Discord servers.
- [Deployment](/deployment/) — running Discord in a Podman container.

## Further reading

- `internal/transport/discord/client.go` — Gateway connection, heartbeat, event pump.
- `internal/cli/discord.go` — CLI wiring.
- `internal/transport/router.go` — allowlist enforcement.
- [Discord API docs: Gateway](https://discord.com/developers/docs/topics/gateway).
- [Discord API docs: Permissions](https://discord.com/developers/docs/topics/permissions).
