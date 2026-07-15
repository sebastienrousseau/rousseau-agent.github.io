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
description: "Set up rousseau-agent's Slack transport: Socket Mode (xapp-* app token + xoxb-* bot token), no public webhook, allowlist by user ID."
keywords: "Slack, Socket Mode, xapp, xoxb, chat.postMessage, connections:write, no webhook, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/transports/slack/"
subtitle: "Socket Mode with no public HTTP surface."
tags: "transports, Slack"
title: "Slack Transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Slack, Socket Mode, xapp, xoxb, chat.postMessage, connections:write, no webhook, allowlist"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Slack Transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 16
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/slack/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/slack/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Slack Transport"
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
twitter_description: "Set up rousseau-agent's Slack transport: Socket Mode (xapp-* app token + xoxb-* bot token), no public webhook, allowlist by user ID."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Slack Transport"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">What you'll learn</span><p>The full app.slack.com wizard walkthrough, exact OAuth scopes to grant, event subscriptions to configure, how Socket Mode avoids the need for a public webhook, and how rousseau's own-message loop prevention works. Read <code>internal/transport/slack/client.go</code> alongside this page.</p></aside>

## Overview

The Slack transport (`internal/transport/slack/`) uses **Socket Mode** — an outbound WebSocket to Slack — so the daemon needs no public HTTP surface. Inbound events flow over the socket; outbound calls hit the standard Web API (`chat.postMessage`).

<aside class="admonition" data-type="tip"><span class="admonition-title">Why Socket Mode</span><p>The alternative (Events API + Request URL) requires a public HTTPS endpoint with an SSL certificate. Rousseau does not ship any inbound HTTP surface by design, so Socket Mode is the only supported ingress path.</p></aside>

## Two tokens

Slack Socket Mode requires two tokens with disjoint responsibilities:

| Token | Prefix | Scope | Purpose |
|---|---|---|---|
| App-level token | `xapp-` | `connections:write` | Opens the Socket Mode WebSocket. |
| Bot token | `xoxb-` | `chat:write` + event subscriptions | Sends messages, subscribes to events. |

## App setup

Full step-by-step at https://app.slack.com/apps :

1. **Create a new app** ("From scratch"). Pick a workspace.
2. **Enable Socket Mode** (Settings → Socket Mode). Generate an **app-level token** with `connections:write`. This is the `xapp-*` token.
3. **Configure event subscriptions** (Features → Event Subscriptions). Subscribe to `message.channels`, `message.im`, or whichever channel scopes the bot should hear. You do **not** need a Request URL because Socket Mode delivers events over the socket instead.
4. **Add bot scopes** (Features → OAuth & Permissions). Minimum: `chat:write`. Add `im:history`, `channels:history`, `groups:history`, or `mpim:history` matching your event subscriptions.
5. **Install the app to the workspace.** The install screen hands back the `xoxb-*` bot token.
6. **Optionally record the bot's own user ID** (starts with `U…`). This is what rousseau uses for own-message loop prevention.

## Configuration

```yaml
slack:
  app_token: "xapp-1-A0..."
  bot_token: "xoxb-1234..."
  bot_user_id: "U0123ABCD"
  reply_header: ""
  allowlist:
    - "U0ALICE"
    - "U0BOB"
```

| Field | Default | Effect |
|---|---|---|
| `app_token` | *required* | `xapp-*` app-level token with `connections:write`. |
| `bot_token` | *required* | `xoxb-*` bot token with `chat:write`. |
| `bot_user_id` | *empty* | Bot user's `U…` ID for own-message loop prevention. Optional; falls back to inspecting the `bot_id` field. |
| `reply_header` | *empty* | Prepended to every outbound message. |
| `allowlist` | `[]` | Slack user IDs whose messages are handled. |

## Command-line

```sh
rousseau slack \
  --app-token xapp-... \
  --bot-token xoxb-... \
  --bot-user-id U0123ABCD
```

## Wire format

- **Inbound.** Slack sends JSON envelopes over the WebSocket. rousseau ACKs the envelope, extracts the message text and sender, and hands it to the handler.
- **Outbound.** `POST https://slack.com/api/chat.postMessage` with `{"channel": "<id>", "text": "…"}` and `Authorization: Bearer <bot_token>`.

## OAuth scopes explained

Every scope grants a specific API surface. The scopes rousseau needs, and what breaks without them:

| Scope | Endpoint used | Broken without |
|---|---|---|
| `connections:write` | `apps.connections.open` (Socket Mode WebSocket) | Cannot open the socket. **Required.** |
| `chat:write` | `chat.postMessage` | Cannot reply to any message. **Required.** |
| `im:history` | `conversations.history` for DMs (indirect via events) | Bot won't see DM contents in events. |
| `im:read` | `im.list`, DM metadata | Cannot list open DMs. |
| `im:write` | `conversations.open` | Cannot open a new DM (only relevant if you want the bot to DM someone unprompted). |
| `mpim:history`, `channels:history`, `groups:history` | Multi-party IMs / channels / private channels | Bot won't see message contents outside DMs. |

Set the scopes under *OAuth &amp; Permissions &gt; Bot Token Scopes*. Only add scopes you actually need — Slack shows a warning at install time about each scope, and end users are more likely to install a bot with a narrow permission surface.

## Own-message loop prevention

Without protection, a bot that replies to messages will also see its own replies as inbound events — leading to runaway loops. Rousseau handles this via `bot_user_id`:

```go
// Simplified — actual logic in internal/transport/slack/client.go
if msg.User == cfg.BotUserID {
    continue // Skip: this is our own outbound message echoing back.
}
```

Retrieve your bot's user ID once via:

```sh
curl -H "Authorization: Bearer xoxb-your-token" \
  https://slack.com/api/auth.test
```

The response includes `user_id`. Paste it into `slack.bot_user_id` in config, or pass with `--bot-user-id`.

<aside class="admonition" data-type="warning"><span class="admonition-title">Fallback loop prevention</span><p>Even without <code>bot_user_id</code>, the transport ignores <code>bot_message</code> subtype events. But relying on subtype alone is fragile — set <code>bot_user_id</code> in production.</p></aside>

## Threading

Slack messages carry a `thread_ts` when they are replies in a thread. Rousseau's outbound calls include `thread_ts` when the inbound event had one, so bot replies stay threaded. Top-level messages become new threads only when the user starts one.

## Failure modes

| Symptom | Fix |
|---|---|
| `invalid_auth` on socket open | `app_token` is wrong or missing `connections:write`. Regenerate. |
| Inbound events never arrive | Verify **Event Subscriptions** are enabled and the relevant `message.*` events are subscribed. |
| Bot replies to its own messages | Set `bot_user_id` in config. |
| `not_in_channel` on send | Invite the bot to the channel (`/invite @rousseau-bot`). |
| DM works but channel does not | Missing `channels:history` scope, or the bot has not been invited to the channel. |

## Troubleshooting

### `invalid_auth` on socket open

The `xapp-…` token is wrong or lost its scope. Regenerate from *Basic Information &gt; App-Level Tokens*, ensure `connections:write` is on the new token.

### `not_authed` on `chat.postMessage`

Bot token (`xoxb-…`) missing or wrong. Regenerate from *OAuth &amp; Permissions &gt; Bot User OAuth Token*.

### Events arrive but rousseau responds to none of them

Check the allowlist. In `pattern` mode with `default: deny`, unlisted users get silently dropped. Look for `router.transport.rejected` in the logs.

### `channel_not_found` on outbound

The Slack channel ID (`C…`) has changed — for example, a channel was archived and recreated. Update any hardcoded channel IDs. Rousseau normally uses the channel from the inbound event, so this only happens with cron delivery to a fixed channel.

### Bot appears offline in Slack

Socket Mode idles the WebSocket every ~30s. If Slack shows the bot as offline, verify: (1) the daemon is running (`systemctl --user status`), (2) the WebSocket is connected (log line `slack.connected`), (3) the machine's clock is within 30s of true time.

## Related pages

- [Getting Started: First Transport](/getting-started/first-transport/) — end-to-end walkthrough.
- [Configuration](/configuration/) — the `slack` config block.
- [Transports](/transports/) — sibling transports.
- [Deployment](/deployment/) — running Slack in a Podman container.
- [Guides: Audit &amp; Approval Policies](/guides/audit-approval-policies/) — policy rulesets for a shared Slack workspace.

## Further reading

- `internal/transport/slack/client.go` — Socket Mode connection, event pump, `chat.postMessage`.
- `internal/cli/slack.go` — CLI wiring.
- `internal/transport/router.go` — allowlist enforcement.
- [Slack API docs: Socket Mode](https://api.slack.com/apis/socket-mode).
