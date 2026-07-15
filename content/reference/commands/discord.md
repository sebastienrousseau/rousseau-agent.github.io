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
description: "Complete reference for rousseau discord: bot token, Gateway intents, allowlist syntax, exit codes."
keywords: "discord, gateway, intents, allowlist, cli reference, rousseau discord"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/commands/discord/"
subtitle: "Complete reference for `rousseau discord`."
tags: "reference, cli, discord, transports"
title: "rousseau discord"

news_genres: "Blog"
news_keywords: "discord, gateway, intents"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "rousseau discord"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 66
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/commands/discord/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/commands/discord/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "rousseau discord"
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
twitter_description: "Complete reference for rousseau discord: bot token, Gateway intents, allowlist syntax, exit codes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "rousseau discord"
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

`rousseau discord` runs the Discord Gateway bridge. It connects to Discord's Gateway v10 WebSocket, subscribes to `MESSAGE_CREATE` events with the Message Content intent, and posts replies via the REST API. Outbound WebSocket only — no public HTTP surface.

Source: `internal/cli/discord.go`. Transport: `internal/transport/discord/`.

<aside class="admonition" data-type="tip"><span class="admonition-title">Enable Message Content intent</span><p>In the Discord Developer Portal, under Bot settings, enable the <strong>Message Content</strong> privileged intent. Without it, the bot only sees mentions.</p></aside>

## Synopsis

```sh
rousseau discord [--token <bot-token>] [--allow <user-id>...] [--config <path>]
```

## Flags

| Flag | Type | Default | Effect |
|---|---|---|---|
| `--token` | string | `discord.token` | Bot token from the Developer Portal. |
| `--allow` | []string | `discord.allowlist` | Restrict inbound to these Discord user IDs. |
| `--config` | string | inherits from root | Path to the YAML config file. |

## Config keys respected

`internal/config/config.go` `DiscordConfig`:

| Key | Type | Default | Effect |
|---|---|---|---|
| `discord.token` | string | empty | Bot token. |
| `discord.reply_header` | string | empty | Prefix on outbound messages. |
| `discord.allowlist` | []string | empty | Discord user IDs (snowflakes as strings). |

## Allowlist syntax

Discord user IDs are 17–20 digit snowflakes:

```yaml
discord:
  allowlist:
    - "123456789012345678"
    - "987654321098765432"
```

To find your own id, enable Developer Mode in Discord settings, then right-click your name and pick "Copy User ID". Or read `router.transport.received` in the logs with an empty allowlist.

## Environment variables

| Variable | Effect |
|---|---|
| `ROUSSEAU_DISCORD_TOKEN` | Overrides `discord.token`. |

## Startup sequence

1. Resolve token from flag/env/config; fail if empty.
2. Default `claudecli.permission_mode` to `bypassPermissions`.
3. Open session store, build agent wiring.
4. `discord.New` — Gateway client with required intents.
5. `wiring.startCron` — cron delivery via REST.
6. Gateway WebSocket loop until context cancelled.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Clean context cancellation. |
| 1 | Missing token, WebSocket failure, provider/store error. |
| 130 | SIGINT. |

## Worked examples

```sh
# Ad-hoc bot for one user
rousseau discord --token "MTIz…" --allow "123456789012345678"

# From config
cat > ~/.config/rousseau/config.yaml <<'EOF'
discord:
  token: "MTIz…"
  allowlist:
    - "123456789012345678"
EOF
rousseau discord
```

## Common failure modes

- **`401 Unauthorized`** — invalid token. Regenerate in the Developer Portal.
- **Bot sees no message content** — Message Content intent not enabled.
- **`Sharding required`** — the bot joined 2500+ guilds. Rousseau does not shard; use a smaller deployment.
- **Silent inbound drops** — sender snowflake not on the allowlist.

## Related pages

- [Transports: Discord](/transports/discord/)
- [Recipes: Discord community bot](/recipes/discord-community-bot/)
- [Best Practices: Secret management](/best-practices/secret-management/)
- [Reference: Logs](/reference/logs/)
