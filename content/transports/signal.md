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
description: "Set up rousseau-agent's Signal transport: signal-cli subprocess in JSON-RPC mode, account registration out-of-band, E.164 allowlist, extra_args knob."
keywords: "Signal, signal-cli, JSON-RPC, subprocess, E.164, account registration, linked device"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/transports/signal/"
subtitle: "signal-cli subprocess in JSON-RPC daemon mode."
tags: "transports, Signal"
title: "Signal Transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Signal, signal-cli, JSON-RPC, subprocess, E.164, account registration, linked device"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Signal Transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 13
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/signal/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/signal/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Signal Transport"
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
twitter_description: "Set up rousseau-agent's Signal transport: signal-cli subprocess in JSON-RPC mode, account registration out-of-band, E.164 allowlist, extra_args knob."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Signal Transport"
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

The Signal transport (`internal/transport/signal/`) shells out to `signal-cli` (https://github.com/AsamK/signal-cli) in its JSON-RPC daemon mode.

`signal-cli --output=json -a <account> jsonRpc` streams JSON-RPC 2.0 over stdin/stdout: outbound `send` requests deliver messages; inbound arrivals arrive as `receive` notifications.

## Prerequisites

Two things must be in place before rousseau can talk to Signal:

1. **`signal-cli` on `$PATH`** (or an explicit `binary` config value).
2. **Account registered / linked out-of-band.**

Account registration is deliberately outside rousseau's scope. Two supported paths (per the `signal-cli` docs):

- **Register a new number.** `signal-cli register` starts SMS or voice verification. Complete with `signal-cli verify <code>`. The number ends up owned by the daemon.
- **Link as a secondary device.** `signal-cli link` prints a `tsdevice://` URI; scan it in the mobile Signal app under **Settings → Linked Devices**. The number stays owned by the phone; the daemon acts as a secondary.

Both flows persist state under `~/.local/share/signal-cli/`. Bind-mount that into the container if you deploy under Podman.

## Configuration

```yaml
signal:
  binary: signal-cli
  account: "+447900123456"
  extra_args:
    - --verbose
  reply_header: "*Rousseau Agent*\n\n"
  allowlist:
    - "+447900654321"
```

| Field | Default | Effect |
|---|---|---|
| `binary` | `signal-cli` | Executable to invoke. |
| `account` | *required* | E.164 phone number the daemon runs as. |
| `extra_args` | `[]` | Inserted between `-a <account>` and `jsonRpc`. Useful for `--config <path>` and `--verbose`. |
| `reply_header` | *empty* | Prepended to every outbound reply. |
| `allowlist` | `[]` | E.164 numbers whose messages are handled. Empty accepts every sender. |

## Command-line

```sh
rousseau signal --account +447900123456 --allow +447900654321
```

Flags mirror the config block. `--allow` may be repeated.

## Message flow

- **Inbound.** `signal-cli` emits a `receive` JSON-RPC notification per arriving message. rousseau parses it, drops anything not in the allowlist, and hands the body to the `Handler`.
- **Outbound.** rousseau writes a JSON-RPC `send` request to `signal-cli`'s stdin. Delivery ACKs arrive on the same channel.

## Timeouts

The transport does not impose its own timeout on the subprocess. `signal-cli`'s own network layer handles Signal server reconnects. If the process exits, rousseau will not restart it — a systemd `Restart=on-failure` (which the reference Quadlet already sets) restarts the whole rousseau daemon, taking `signal-cli` with it.

## Failure modes

| Symptom | Fix |
|---|---|
| `signal-cli` exits immediately | Account is not registered or linked. Complete registration out-of-band. |
| `receive` notifications never arrive | Check the account is not linked in another location that is consuming the queue. |
| Bad JSON parse errors | Confirm your `signal-cli` version is 0.13+. Older versions used a different envelope. |
