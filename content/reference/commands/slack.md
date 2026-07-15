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
description: "Complete reference for rousseau slack: Socket Mode tokens, allowlist syntax, bot user id, exit codes."
keywords: "slack, socket mode, xapp, xoxb, cli reference, rousseau slack"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/commands/slack/"
subtitle: "Complete reference for `rousseau slack`."
tags: "reference, cli, slack, transports"
title: "rousseau slack"

news_genres: "Blog"
news_keywords: "slack, socket mode, xapp, xoxb"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "rousseau slack"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 65
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/commands/slack/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/commands/slack/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "rousseau slack"
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
twitter_description: "Complete reference for rousseau slack: Socket Mode tokens, allowlist syntax, bot user id, exit codes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "rousseau slack"
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

`rousseau slack` runs the Slack bridge in Socket Mode. Slack Socket Mode is a bidirectional outbound WebSocket — the daemon dials Slack, Slack sends event payloads down the socket, the daemon replies via `chat.postMessage`. No public HTTP surface is exposed, which is why this transport works in Podman/Quadlet with `Network=pasta` and no port bindings.

Source: `internal/cli/slack.go`. Transport: `internal/transport/slack/`.

<aside class="admonition" data-type="tip"><span class="admonition-title">Two tokens, one app</span><p>Create a Slack app at <a href="https://api.slack.com/apps">api.slack.com/apps</a>. Enable Socket Mode. You need an <strong>app-level token</strong> (<code>xapp-*</code>) with <code>connections:write</code> and a <strong>bot token</strong> (<code>xoxb-*</code>) with <code>chat:write</code> + message event subscriptions.</p></aside>

## Synopsis

```sh
rousseau slack [--app-token <xapp>] [--bot-token <xoxb>] [--bot-user-id <UXXX>] [--allow <UXXX>...]
```

## Flags

| Flag | Type | Default | Effect |
|---|---|---|---|
| `--app-token` | string | `slack.app_token` | `xapp-*` app-level token (Socket Mode WebSocket). |
| `--bot-token` | string | `slack.bot_token` | `xoxb-*` bot token (posting). |
| `--bot-user-id` | string | `slack.bot_user_id` | Bot user ID (e.g. `U0ABC123`) for own-message loop prevention. |
| `--allow` | []string | `slack.allowlist` | Restrict inbound to these Slack user IDs. |
| `--config` | string | inherits from root | Path to the YAML config file. |

## Config keys respected

`internal/config/config.go` `SlackConfig`:

| Key | Type | Default | Effect |
|---|---|---|---|
| `slack.app_token` | string | empty | `xapp-*` app-level token. |
| `slack.bot_token` | string | empty | `xoxb-*` bot token. |
| `slack.bot_user_id` | string | empty | Bot user id. |
| `slack.reply_header` | string | empty | Prefix on outbound messages. |
| `slack.allowlist` | []string | empty | Slack user IDs permitted. |

## Allowlist syntax

Slack user IDs (`U…` for humans, `W…` for enterprise/grid, `B…` for bots) as strings:

```yaml
slack:
  allowlist:
    - "U0ABC1234"
    - "U0XYZ5678"
```

Channel allowlisting is not implemented — filter by the sender's user id instead.

## Environment variables

| Variable | Effect |
|---|---|
| `ROUSSEAU_SLACK_APP_TOKEN` | Overrides app token. |
| `ROUSSEAU_SLACK_BOT_TOKEN` | Overrides bot token. |
| `ROUSSEAU_SLACK_BOT_USER_ID` | Overrides bot user id. |

## Startup sequence

1. Resolve tokens from flag/env/config; fail if either app or bot token is empty.
2. Default `claudecli.permission_mode` to `bypassPermissions`.
3. Open session store, build agent wiring.
4. `slack.New` — Socket Mode client.
5. `wiring.startCron` — cron deliveries via `chat.postMessage`.
6. WebSocket loop until context cancelled.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Clean context cancellation. |
| 1 | Missing tokens, WebSocket failure, provider/store error. |
| 130 | SIGINT. |

## Worked examples

```sh
# From flags
rousseau slack \
  --app-token "xapp-1-…" \
  --bot-token "xoxb-2-…" \
  --bot-user-id "U0ABC1234" \
  --allow "U0XYZ5678"

# From config
cat > ~/.config/rousseau/config.yaml <<'EOF'
slack:
  app_token: "xapp-1-…"
  bot_token: "xoxb-2-…"
  bot_user_id: "U0ABC1234"
  allowlist:
    - "U0XYZ5678"
EOF
rousseau slack
```

## Common failure modes

- **`invalid_auth`** — token typo or wrong scope. Verify with `curl -H "Authorization: Bearer $token" https://slack.com/api/auth.test`.
- **`missing_scope`** — bot token is missing `chat:write`. Update in the app manifest.
- **`socket_mode_disabled`** — Socket Mode is off. Enable it in the app config.
- **Bot answers itself** — set `--bot-user-id` correctly.
- **Silent inbound drops** — sender user id not on the allowlist.

## Related pages

- [Transports: Slack](/transports/slack/)
- [Recipes: On-call Slack triage](/recipes/oncall-slack-triage/)
- [Reference: Commands: cron](/reference/commands/cron/)
- [Best Practices: Secret management](/best-practices/secret-management/)
