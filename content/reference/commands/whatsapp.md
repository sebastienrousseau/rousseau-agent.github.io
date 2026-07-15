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
description: "Complete reference for rousseau whatsapp: flags, config keys, allowlist JID syntax, whatsmeow store, voice transcription, exit codes."
keywords: "whatsapp, whatsmeow, jid, allowlist, cli reference, rousseau whatsapp"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/commands/whatsapp/"
subtitle: "Complete reference for `rousseau whatsapp`."
tags: "reference, cli, whatsapp, transports"
title: "rousseau whatsapp"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "whatsapp, whatsmeow, jid, allowlist"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "rousseau whatsapp"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 61
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/commands/whatsapp/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/commands/whatsapp/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "rousseau whatsapp"
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
twitter_description: "Complete reference for rousseau whatsapp: flags, config keys, allowlist JID syntax, whatsmeow store, voice transcription, exit codes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "rousseau whatsapp"
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

## Overview

`rousseau whatsapp` runs the WhatsApp bridge in the foreground. It embeds `go.mau.fi/whatsmeow` (unofficial WhatsApp Web protocol) and speaks directly to Meta's servers. On first launch a QR code is printed to stdout; scan it from your phone under **WhatsApp > Settings > Linked devices**. Device credentials are cached to a SQLite store separate from the session database.

<aside class="admonition" data-type="warning"><span class="admonition-title">Unofficial protocol</span><p>Meta occasionally bans numbers running unofficial clients. Do not run this on a number you rely on. See <a href="/transports/whatsapp/">Transports: WhatsApp</a> for the full risk analysis.</p></aside>

Source: `internal/cli/whatsapp.go`. Transport implementation: `internal/transport/whatsapp/`.

## Synopsis

```sh
rousseau whatsapp [--store <path>] [--allow <jid>...] [--config <path>]
```

## Flags

| Flag | Type | Default | Effect |
|---|---|---|---|
| `--store` | string | `$XDG_DATA_HOME/rousseau/whatsapp.db` | Path to the whatsmeow device store (SQLite with WAL, `busy_timeout=15000`, `synchronous=NORMAL`). |
| `--allow` | []string | empty | Restrict inbound to these JIDs. Repeatable. Empty allows anyone — never do this on a public number. |
| `--config` | string | inherits from root | Path to the YAML config file. |

## Config keys respected

Read from `internal/config/config.go` `WhatsAppConfig`:

| Key | Type | Default | Effect |
|---|---|---|---|
| `whatsapp.reply_header` | string | `"💎 *Rousseau Agent*\n\n"` | Prefix prepended to every outbound message. Set to `" "` to disable. |
| `whatsapp.voice.enabled` | bool | `false` | Enable whisper-based transcription for inbound voice notes. |
| `whatsapp.voice.binary` | string | `whisper` | Whisper CLI to invoke. |
| `whatsapp.voice.model` | string | empty | Passed to `--model` (e.g. `base.en`). |
| `whatsapp.voice.model_path` | string | empty | Explicit `.bin` path; takes precedence over `model`. |
| `whatsapp.voice.language` | string | empty | Passed to `--language`; empty auto-detects. |
| `whatsapp.voice.extra_args` | []string | empty | Appended to every whisper invocation. |

## Allowlist syntax

Every allowlist entry is a WhatsApp JID (Jabber ID). The two forms in use:

<div class="tabs" data-tabs="wa-jid">
  <div class="tab-list" role="tablist" aria-label="JID kind">
    <button role="tab" aria-selected="true">Personal number</button>
    <button role="tab" aria-selected="false">Group</button>
  </div>
  <div class="tab-panel" role="tabpanel">

```text
447900123456@s.whatsapp.net
```

E.164 without a leading `+` followed by `@s.whatsapp.net`. This is the JID that identifies a single phone number.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```text
447900123456-1567890123@g.us
```

A group JID: the number of the group creator, a dash, the group creation timestamp, then `@g.us`. Groups can be added to the allowlist explicitly; individual members inside an allowed group do not need their personal JIDs listed.

  </div>
</div>

The router (`internal/transport/router.go`) checks the sender's normalised JID against the allowlist. Non-matching senders are dropped with a `router.transport.rejected` log event.

## Environment variables

| Variable | Effect |
|---|---|
| `ROUSSEAU_WHATSAPP_REPLY_HEADER` | Overrides the reply header. |
| `XDG_DATA_HOME` | Base directory for the device store. |
| `ROUSSEAU_LOG_LEVEL` | Also translated into whatsmeow's log level (`DEBUG`, `INFO`, `WARN`, `ERROR`). |

Plus every provider variable — see [rousseau chat](/reference/commands/chat/#environment-variables).

## Startup sequence

1. `setUnattendedPermissionDefault(opts, "whatsapp")` — flips `claudecli.permission_mode` to `bypassPermissions` if empty, because unattended daemons cannot answer permission prompts interactively.
2. `assembleDaemon` — opens the session store, builds the provider, tool registry, approver, compressor.
3. `resolveWhatsAppDSN` — computes the SQLite DSN with WAL pragmas.
4. `whatsapp.New` — creates the whatsmeow client and (optionally) the whisper transcriber.
5. `wiring.startCron` — starts the cron scheduler with the whatsapp `Deliver` as the delivery callback, so `rousseau cron add` jobs land on the configured target JIDs.
6. `client.Start` — blocks until the context is cancelled (Ctrl+C, SIGTERM).

## Log events

| Event | Attributes | Emitted by |
|---|---|---|
| `whatsapp.qr_ready` | none | first-pairing QR code rendered to stdout |
| `whatsapp.paired` | `jid` | phone accepted the QR |
| `whatsapp.connected` | none | websocket handshake completed |
| `whatsapp.starting` | `store`, `allowlist` | pre-connect |
| `whatsapp.voice_enabled` | `binary`, `model` | when voice transcription is enabled |
| `router.transport.rejected` | `sender`, `reason` | inbound sender not on the allowlist |

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Clean context cancellation (SIGTERM). |
| 1 | Provider, store, whatsmeow, or DSN error before or during startup. |
| 130 | SIGINT interrupt. |

## Worked examples

```sh
# Personal chat with a single allowed number
rousseau whatsapp --allow 447900123456@s.whatsapp.net

# Multiple numbers plus a team group
rousseau whatsapp \
  --allow 447900123456@s.whatsapp.net \
  --allow 447900222222@s.whatsapp.net \
  --allow 447900123456-1567890123@g.us

# Explicit store path (useful in Podman with a bind-mounted volume)
rousseau whatsapp --store /var/lib/rousseau/whatsapp.db

# Voice notes with a local whisper.cpp binary
cat >> ~/.config/rousseau/config.yaml <<'EOF'
whatsapp:
  voice:
    enabled: true
    binary: /usr/local/bin/whisper
    model: base.en
EOF
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

## Common failure modes

<aside class="admonition" data-type="caution"><span class="admonition-title">QR expires quickly</span><p>WhatsApp's QR handshake is time-sensitive. Skewed container clocks (&gt;30s drift) reject valid QRs. Sync NTP before pairing.</p></aside>

- **QR displayed but never accepted** — clock drift, stale `whatsapp.db`, or Meta-invalidated number. Delete `whatsapp.db` and re-pair; check `timedatectl status`.
- **`store: locked`** — another `rousseau whatsapp` process is holding the WAL lock. WAL allows readers but only one writer.
- **Voice notes not transcribed** — `whatsapp.voice.enabled: false`, or the `whisper` binary is not on `$PATH`. `rousseau doctor` surfaces both.
- **Silent inbound drops** — the sender is not on the allowlist. Check `router.transport.rejected` in the logs.

## Related pages

- [Transports: WhatsApp](/transports/whatsapp/) — protocol, risk, operational posture.
- [Reference: Commands: cron](/reference/commands/cron/) — schedule prompts that deliver to WhatsApp JIDs.
- [Best Practices: Session hygiene](/best-practices/session-hygiene/) — when to nuke the store.
- [Deployment](/deployment/) — running under Podman.
- [Reference: Logs](/reference/logs/) — every structured log event.
