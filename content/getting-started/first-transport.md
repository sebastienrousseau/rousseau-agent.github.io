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
description: "End-to-end walkthrough for wiring your first chat transport. Uses WhatsApp as the canonical example: pair, allowlist, send a test message, verify the reply."
keywords: "first transport, whatsapp, pairing, allowlist, e2e walkthrough, test message"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/getting-started/first-transport/"
subtitle: "End-to-end WhatsApp walkthrough: pair, allowlist, verify."
tags: "first-transport, whatsapp, walkthrough"
title: "Your First Transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "first transport, whatsapp, pairing, allowlist, e2e walkthrough, test message"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Your First Transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 25
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/first-transport/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/first-transport/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Your First Transport"
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
twitter_description: "End-to-end walkthrough for wiring your first chat transport. Uses WhatsApp as the canonical example: pair, allowlist, send a test message, verify the reply."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Your First Transport"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">What you'll learn</span><p>How to pair a chat transport with the rousseau daemon, allowlist the JID/user ID that drives it, send a first test message, and confirm the reply. WhatsApp is the canonical walkthrough because pairing is the most stringent; the tabs below show the parallel walkthroughs for Slack and Discord.</p></aside>

## Pick your first transport

Every transport is a thin adapter behind the same `transport.Transport` interface — allowlisting, session routing, and cron delivery are identical across all of them. The differences are pairing UX and the per-transport identifier format (JID, user ID, room ID). Pick whichever you can pair fastest:

<div class="tabs" data-tabs="first-transport">
  <div class="tab-list" role="tablist" aria-label="First transport">
    <button role="tab" aria-selected="true">WhatsApp</button>
    <button role="tab" aria-selected="false">Slack</button>
    <button role="tab" aria-selected="false">Discord</button>
    <button role="tab" aria-selected="false">Telegram</button>
    <button role="tab" aria-selected="false">Signal</button>
  </div>
  <div class="tab-panel" role="tabpanel">

WhatsApp is the reference — hardest to pair, easiest to test (you already have the app on your phone).

**Prerequisites:** your phone with WhatsApp, your E.164 JID (e.g. `447900123456@s.whatsapp.net`).

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

Scan the QR from **WhatsApp &gt; Settings &gt; Linked devices &gt; Link a device**. Send `hello` to yourself; rousseau replies via WhatsApp. See below for the full walkthrough.

<aside class="admonition" data-type="warning"><span class="admonition-title">Unofficial protocol</span><p>WhatsApp support uses <code>whatsmeow</code> — a reverse-engineered client. Meta occasionally bans numbers running unofficial clients. Do not run this on a number you rely on.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Prerequisites:** admin on a Slack workspace, an app created at [api.slack.com/apps](https://api.slack.com/apps), Socket Mode enabled.

1. Create a Slack app, enable **Socket Mode** under <em>Settings &gt; Socket Mode</em>.
2. Create an **App-Level Token** with `connections:write` — this is the `xapp-…` token.
3. Under <em>OAuth &amp; Permissions</em>, add bot scopes `chat:write`, `im:history`, `im:read`, `im:write`, `mpim:history`, `mpim:read`. Install to the workspace to get the `xoxb-…` bot token.
4. Under <em>Event Subscriptions</em>, subscribe to `message.im` (DMs) and any channel event you want.

```sh
rousseau slack --app-token xapp-... --bot-token xoxb-... --allow U01234567
```

DM the bot in Slack; rousseau replies in the same DM. See [Transports: Slack](/transports/slack/) for the full walkthrough with OAuth scope rationale.

<aside class="admonition" data-type="tip"><span class="admonition-title">No public HTTP</span><p>Socket Mode means the daemon connects outbound to Slack's WebSocket. You do not need a public webhook, ngrok, or ingress.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Prerequisites:** a Discord application at [discord.com/developers/applications](https://discord.com/developers/applications), a bot user, the **Message Content Intent** enabled under <em>Bot</em>.

1. Create an application, add a bot, copy the bot token.
2. Under <em>Bot &gt; Privileged Gateway Intents</em>, enable **Message Content Intent**. Without this, message text arrives empty.
3. Invite the bot via <em>OAuth2 &gt; URL Generator</em> — scope `bot`, permissions `Send Messages`, `Read Message History`.

```sh
rousseau discord --token <bot-token> --allow 234567890123456789
```

DM the bot; rousseau replies. See [Transports: Discord](/transports/discord/) for permissions and intents deep dive.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Prerequisites:** a Telegram bot from [@BotFather](https://t.me/BotFather).

1. Message `@BotFather`, `/newbot`, follow prompts. Copy the token.
2. Talk to your bot at least once so Telegram creates a chat.

```sh
rousseau telegram --token 1234567890:AA... --allow 987654321
```

The `--allow` value is the Telegram numeric user ID (not username). Get it by messaging [@userinfobot](https://t.me/userinfobot).

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Prerequisites:** `signal-cli` installed and linked to a Signal account. See the [signal-cli docs](https://github.com/AsamK/signal-cli) for the pairing flow.

```sh
rousseau signal --account +447900123456 --allow +447900654321
```

Rousseau spawns `signal-cli` as a subprocess (see `internal/cli/signal.go`) and communicates with it via JSON-RPC. See [Transports: Signal](/transports/signal/).

  </div>
</div>

## Why the WhatsApp walkthrough

The rest of this page uses WhatsApp as the canonical example — if you get the pattern here, every other transport is a variation on it (allowlist a stable ID, run a pairing UX once, send a test, verify the reply). Skip to the sibling transport page if you already have a token in hand:

- [Slack](/transports/slack/) — Socket Mode tokens and event subscriptions.
- [Discord](/transports/discord/) — bot token, intents, permission integers.
- [Telegram](/transports/telegram/) — BotFather token.
- [Signal](/transports/signal/) — signal-cli subprocess.
- [Matrix](/transports/matrix/) — homeserver URL + access token.

## Prerequisites

- `rousseau` on `$PATH` (see [Installation](/getting-started/installation/)).
- A working provider — `claudecli` inheriting Claude Code auth is the default; anything else needs its config filled in first ([Configuration](/configuration/)).
- Your phone with WhatsApp installed. Your E.164 phone JID (e.g. `447900123456@s.whatsapp.net`).

## Step 1 — Choose the JID that will drive the daemon

Rousseau uses an allowlist to restrict inbound handling to a fixed set of JIDs. Every other sender is silently dropped. This is load-bearing: without an allowlist, anyone who knows the number could drive the agent.

Your E.164 JID is your phone number, digits only, followed by `@s.whatsapp.net`:

```
447900123456@s.whatsapp.net
```

Group JIDs end in `@g.us`; the daemon supports those too, but start with a personal JID.

## Step 2 — First launch and pairing

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

On first launch, a QR code is printed to stdout. Open WhatsApp on your phone, go to **Settings → Linked devices → Link a device**, and scan the QR.

The daemon prints something like:

```
whatsapp.starting store=file:/home/you/.local/share/rousseau/whatsapp.db?_pragma=... allowlist=1
```

Once you scan, whatsmeow persists device credentials to `whatsapp.db`. Subsequent launches connect silently — no more QR.

## Step 3 — Send a test message

From your phone, send `hello` to yourself. The daemon logs the inbound event, dispatches to the agent, and delivers the reply back through WhatsApp with the configured header:

```
💎 *Rousseau Agent*

Hello — what would you like to work on?
```

The reply header is configurable via `whatsapp.reply_header`. Set it to a single space to disable the prefix.

## Step 4 — Set up a `config.yaml` so you don't need long flags

Create `~/.config/rousseau/config.yaml`:

```yaml
provider: claudecli

claudecli:
  binary: claude
  permission_mode: bypassPermissions

whatsapp:
  reply_header: "💎 *Rousseau Agent*\n\n"
```

Now `rousseau whatsapp --allow 447900123456@s.whatsapp.net` picks up the header automatically. Every transport reads its stanza from the same file — see [Configuration](/configuration/) for the full list.

`bypassPermissions` is the default for unattended daemons because there is no human on the other end of the terminal to approve tool calls interactively. **Set up an approval policy** ([User Guide: Approval Policies](/user-guide/approval-policies/)) before you point the daemon at anything you care about.

## Step 5 — Confirm end-to-end

Send a coding question from your phone:

```
Read the file at /workspace/README.md and summarise it in 3 bullets.
```

The daemon runs a `read` tool call, feeds the file to the model, and messages you back with the summary. You have just closed the loop:

- Phone → WhatsApp → whatsmeow WebSocket
- rousseau-agent → agent loop → tool call → provider call
- reply → whatsmeow → WhatsApp → phone

Nothing crossed your network perimeter except the provider call — and if the provider was `claudecli` on your local Claude Code install, not even that.

## Verifying with `rousseau doctor`

```sh
rousseau doctor
```

Every check for the WhatsApp path is covered:

- `provider.claudecli.binary`, `provider.claudecli.version` — the LLM path.
- `state.path`, `state.db_size`, `state.sessions` — SQLite session store.
- `whatsapp.store`, `whatsapp.paired` — device credentials.
- `whatsapp.voice` — voice-note transcription posture.

A `fail` row is a hard stop; a `warn` row is worth investigating before rolling out.

## Troubleshooting

### QR code prints but the phone rejects it

Three common causes. First, a partially-completed prior pairing left `whatsapp.db` in a state whatsmeow cannot reuse — delete `~/.local/share/rousseau/whatsapp.db` and re-scan. Second, the clock is skewed by more than 30 seconds (common in containers without a working NTP client) — WhatsApp's handshake is time-sensitive. Third, an older `whatsmeow` version can miss a Meta protocol update; upgrade rousseau.

### I sent a message but the daemon logs `router.transport.rejected`

Your JID does not match the allowlist. The value passed to `--allow` must be the sender's JID exactly as WhatsApp reports it (`447900123456@s.whatsapp.net`, no `+`, no spaces). Note that self-chat testing works because rousseau substitutes the account's own JID for the LID privacy hash (see `internal/transport/whatsapp/resolve.go`).

### No QR code prints and the daemon exits with `no rows`

The whatsmeow store was never initialised. Ensure the parent directory (`~/.local/share/rousseau/`) exists and is writable. `rousseau doctor` reports this under `whatsapp.store`.

### Rousseau replies but the model output is empty

Check `provider.claudecli.binary` and `provider.claudecli.version` in `rousseau doctor`. The most common empty-reply cause is a `claudecli` invocation returning `is_error: true` — the daemon logs the truncated error at `warn` level. Switch provider to `anthropic` or `bedrock` to isolate the subprocess.

### Slack/Discord: "invalid_auth" or "401 Unauthorized"

For Slack, `xapp-…` (app token) and `xoxb-…` (bot token) are different — mixing them up produces `invalid_auth`. For Discord, the token displayed on <em>Bot &gt; Reset Token</em> is one-shot; if you copied it once and lost it, you must reset again.

## Related pages

- [Transports](/transports/) — every transport, its wire protocol, and its allowlist format.
- [User Guide: CLI](/user-guide/cli/) — every command and flag.
- [User Guide: Approval Policies](/user-guide/approval-policies/) — the primary safety lever.
- [Deployment](/deployment/) — hand off from foreground `rousseau whatsapp` to a systemd unit.
- [Voice mode](/user-guide/voice-mode/) — turn WhatsApp voice notes into agent turns.

## Further reading

- `internal/transport/whatsapp/client.go` — connect, QR, event pump.
- `internal/transport/whatsapp/resolve.go` — LID/JID normalisation and self-chat handling.
- `internal/cli/whatsapp.go` — CLI wiring, store DSN, transcriber selection.
- `internal/cli/slack.go`, `internal/cli/discord.go` — sibling transport CLIs.
- `internal/transport/router.go` — allowlist enforcement.
