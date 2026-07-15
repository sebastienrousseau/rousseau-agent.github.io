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
description: "Complete reference for rousseau signal: flags, allowlist syntax, signal-cli integration, exit codes, and failure modes."
keywords: "signal, signal-cli, jsonrpc, allowlist, cli reference, rousseau signal"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/commands/signal/"
subtitle: "Complete reference for `rousseau signal`."
tags: "reference, cli, signal, transports"
title: "rousseau signal"

news_genres: "Blog"
news_keywords: "signal, signal-cli, allowlist"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "rousseau signal"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 62
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/commands/signal/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/commands/signal/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "rousseau signal"
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
twitter_description: "Complete reference for rousseau signal: flags, allowlist syntax, signal-cli integration, exit codes, and failure modes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "rousseau signal"
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

`rousseau signal` runs the Signal bridge by shelling out to a locally installed `signal-cli` (https://github.com/AsamK/signal-cli) in `jsonRpc` mode. The daemon pumps JSON-RPC messages between the account and the agent loop. This is the most privacy-preserving transport in the tree because Signal is end-to-end encrypted and does not require any provider-hosted infrastructure.

Source: `internal/cli/signal.go`. Transport: `internal/transport/signal/`.

<aside class="admonition" data-type="tip"><span class="admonition-title">Prerequisite</span><p>You must install <code>signal-cli</code> and either register a new number (<code>signal-cli -a +NUMBER register</code>) or link it as a device (<code>signal-cli link</code>). Rousseau does not handle account setup.</p></aside>

## Synopsis

```sh
rousseau signal [--account <e164>] [--binary <path>] [--allow <e164>...] [--config <path>]
```

## Flags

| Flag | Type | Default | Effect |
|---|---|---|---|
| `--account` | string | `signal.account` | E.164 phone number the daemon runs as. Passed to `signal-cli -a`. |
| `--binary` | string | `signal.binary` or `signal-cli` on `$PATH` | Path to the signal-cli executable. |
| `--allow` | []string | `signal.allowlist` | Restrict inbound to these E.164 numbers. Repeatable. |
| `--config` | string | inherits from root | Path to the YAML config file. |

## Config keys respected

`internal/config/config.go` `SignalConfig`:

| Key | Type | Default | Effect |
|---|---|---|---|
| `signal.binary` | string | `signal-cli` | Executable name/path. |
| `signal.account` | string | empty | E.164 the daemon runs as. Required. |
| `signal.extra_args` | []string | empty | Inserted between `-a <account>` and `jsonRpc`. |
| `signal.reply_header` | string | empty | Prefix prepended to every outbound message. |
| `signal.allowlist` | []string | empty | E.164 numbers permitted to send inbound messages. |

## Allowlist syntax

Every entry is an E.164 phone number with the leading `+`:

```yaml
signal:
  account: "+447900123456"
  allowlist:
    - "+447900123456"
    - "+447900222222"
```

The router matches inbound sender numbers exactly against the list. Empty allowlist allows every sender — do not use this posture in production.

## Environment variables

| Variable | Effect |
|---|---|
| `ROUSSEAU_SIGNAL_ACCOUNT` | Overrides `signal.account`. |
| `ROUSSEAU_SIGNAL_BINARY` | Overrides `signal.binary`. |
| `PATH` | Used to locate `signal-cli` when `signal.binary` is unset. |

## Startup sequence

1. Resolve and validate the account (either flag, env, or config).
2. Default `claudecli.permission_mode` to `bypassPermissions` because signal-cli JSON-RPC is unattended.
3. Open the session store.
4. `signal.New` — spawn `signal-cli -a <account> [extra_args] jsonRpc` as a subprocess.
5. Pump JSON-RPC over the subprocess stdio.
6. `wiring.startCron` — wire cron delivery through Signal.
7. Block on `client.Start` until context cancellation.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Clean context cancellation. |
| 1 | Missing `--account`, subprocess spawn failure, provider/store setup failure. |
| 130 | SIGINT. |

If `signal-cli` itself dies, the wrapper returns a non-zero code that surfaces as `1`.

## Worked examples

```sh
# Basic
rousseau signal --account +447900123456 --allow +447900222222

# Custom signal-cli path (e.g. flatpak install)
rousseau signal \
  --binary /var/lib/flatpak/exports/bin/org.asamk.signal.SignalCli \
  --account +447900123456

# Multiple allowlist entries from config
cat > ~/.config/rousseau/config.yaml <<'EOF'
signal:
  account: "+447900123456"
  allowlist:
    - "+447900123456"
    - "+447900222222"
EOF
rousseau signal
```

## Common failure modes

<aside class="admonition" data-type="note"><span class="admonition-title">Registration first</span><p>signal-cli must already be registered/linked. If you see <code>User is not registered</code>, run <code>signal-cli -a +NUMBER register</code> or <code>signal-cli link</code> first.</p></aside>

- **`exec: "signal-cli": executable file not found`** — install signal-cli or set `signal.binary`.
- **`Failed to send message: RateLimit`** — Signal rate-limits new accounts. Wait, then retry.
- **`Invalid recipient`** — E.164 must include the leading `+`.
- **Silent inbound drops** — sender not on the allowlist. Grep for `router.transport.rejected`.

## Related pages

- [Transports: Signal](/transports/signal/)
- [Best Practices: Secret management](/best-practices/secret-management/)
- [Reference: Commands: cron](/reference/commands/cron/)
- [Reference: Logs](/reference/logs/)
