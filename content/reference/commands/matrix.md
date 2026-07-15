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
description: "Complete reference for rousseau matrix: flags, homeserver URL, MXID allowlist, sync loop, exit codes."
keywords: "matrix, mxid, homeserver, cli reference, rousseau matrix"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/commands/matrix/"
subtitle: "Complete reference for `rousseau matrix`."
tags: "reference, cli, matrix, transports"
title: "rousseau matrix"

news_genres: "Blog"
news_keywords: "matrix, mxid, homeserver"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "rousseau matrix"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 64
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/commands/matrix/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/commands/matrix/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "rousseau matrix"
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
twitter_description: "Complete reference for rousseau matrix: flags, homeserver URL, MXID allowlist, sync loop, exit codes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "rousseau matrix"
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

`rousseau matrix` runs the Matrix client-server bridge. The daemon long-polls `/sync` on a homeserver, routes each incoming `m.room.message` from a non-self sender through the agent, and posts replies via `/rooms/{room}/send/m.room.message`. Works against `matrix.org` or any self-hosted Synapse / Dendrite / Conduit / Conduwuit instance.

Source: `internal/cli/matrix.go`. Transport: `internal/transport/matrix/`.

<aside class="admonition" data-type="tip"><span class="admonition-title">Pre-provision the bot</span><p>Create a Matrix account (e.g. <code>@rousseau-bot:example.com</code>) using your homeserver's admin flow, then generate an access token via <code>/login</code>. Rousseau does not handle registration.</p></aside>

## Synopsis

```sh
rousseau matrix [--homeserver <url>] [--token <access-token>] [--user-id <mxid>] [--allow <mxid>...]
```

## Flags

| Flag | Type | Default | Effect |
|---|---|---|---|
| `--homeserver` | string | `matrix.homeserver_url` | Base URL of the homeserver, e.g. `https://matrix.org`. |
| `--token` | string | `matrix.access_token` | Bot access token. |
| `--user-id` | string | `matrix.user_id` | Bot MXID for own-message loop prevention. |
| `--allow` | []string | `matrix.allowlist` | Restrict inbound to these MXIDs. |
| `--config` | string | inherits from root | Path to the YAML config file. |

## Config keys respected

`internal/config/config.go` `MatrixConfig`:

| Key | Type | Default | Effect |
|---|---|---|---|
| `matrix.homeserver_url` | string | empty | Base URL. |
| `matrix.access_token` | string | empty | Bot access token. |
| `matrix.user_id` | string | empty | Bot MXID (`@rousseau-bot:example.com`). |
| `matrix.reply_header` | string | empty | Prefix on outbound messages. |
| `matrix.allowlist` | []string | empty | MXIDs allowed to converse. |

## Allowlist syntax

Every entry is a fully-qualified MXID:

```yaml
matrix:
  allowlist:
    - "@alice:example.com"
    - "@bob:matrix.org"
```

Room-level allowlisting is not currently supported; use user MXIDs.

## Environment variables

| Variable | Effect |
|---|---|
| `ROUSSEAU_MATRIX_HOMESERVER_URL` | Overrides homeserver URL. |
| `ROUSSEAU_MATRIX_ACCESS_TOKEN` | Overrides access token. |
| `ROUSSEAU_MATRIX_USER_ID` | Overrides bot MXID. |

## Startup sequence

1. Resolve homeserver + token; fail if either is empty.
2. Default `claudecli.permission_mode` to `bypassPermissions`.
3. Open session store; build agent wiring.
4. `matrix.New` — instantiate the client.
5. `wiring.startCron` — cron delivery via room send API.
6. `/sync` long-poll loop until context cancelled.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Clean context cancellation. |
| 1 | Missing homeserver/token, HTTP error, provider/store failure. |
| 130 | SIGINT. |

## Worked examples

```sh
# Public matrix.org bot
rousseau matrix \
  --homeserver https://matrix.org \
  --token syt_… \
  --user-id "@rousseau-bot:matrix.org" \
  --allow "@alice:matrix.org"

# Self-hosted Synapse
cat > ~/.config/rousseau/config.yaml <<'EOF'
matrix:
  homeserver_url: "https://matrix.internal.example"
  access_token: "syt_…"
  user_id: "@rousseau-bot:internal.example"
  allowlist:
    - "@alice:internal.example"
    - "@bob:internal.example"
EOF
rousseau matrix
```

## Common failure modes

<aside class="admonition" data-type="warning"><span class="admonition-title">No end-to-end encryption yet</span><p>Rousseau's Matrix transport does not currently handle encrypted rooms (Olm/Megolm). Invite the bot into unencrypted rooms only.</p></aside>

- **`M_UNKNOWN_TOKEN`** — access token expired or revoked. Re-login the bot user.
- **`M_LIMIT_EXCEEDED`** — homeserver rate-limited the sync loop. Back off.
- **Bot answers its own messages** — set `--user-id` so own-message loop prevention works.
- **Silent inbound drops** — sender MXID not on the allowlist.

## Related pages

- [Transports: Matrix](/transports/matrix/)
- [Recipes: Matrix room monitor](/recipes/matrix-room-monitor/)
- [Best Practices: Secret management](/best-practices/secret-management/)
- [Reference: Logs](/reference/logs/)
