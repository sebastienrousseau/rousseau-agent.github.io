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
description: "Complete reference for rousseau telegram: flags, BotFather token, chat-id allowlist, long-polling behaviour, exit codes."
keywords: "telegram, botfather, bot api, cli reference, rousseau telegram"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/commands/telegram/"
subtitle: "Complete reference for `rousseau telegram`."
tags: "reference, cli, telegram, transports"
title: "rousseau telegram"

news_genres: "Blog"
news_keywords: "telegram, botfather, allowlist"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "rousseau telegram"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 63
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/commands/telegram/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/commands/telegram/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "rousseau telegram"
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
twitter_description: "Complete reference for rousseau telegram: flags, BotFather token, chat-id allowlist, long-polling behaviour, exit codes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "rousseau telegram"
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

`rousseau telegram` runs a Telegram Bot API long-poller. The daemon repeatedly calls `getUpdates`, routes each incoming private message through the agent, and replies via `sendMessage`. No public HTTP surface is exposed — long polling is a purely outbound HTTPS connection.

Source: `internal/cli/telegram.go`. Transport: `internal/transport/telegram/`.

<aside class="admonition" data-type="tip"><span class="admonition-title">Get a bot token</span><p>Talk to <a href="https://t.me/BotFather">@BotFather</a> on Telegram. Send <code>/newbot</code>, follow the prompts, and copy the <code>xxxxxxx:yyyy…</code> token.</p></aside>

## Synopsis

```sh
rousseau telegram [--token <bot-token>] [--allow <chat-id>...] [--config <path>]
```

## Flags

| Flag | Type | Default | Effect |
|---|---|---|---|
| `--token` | string | `telegram.token` | Bot token from @BotFather. |
| `--allow` | []string | `telegram.allowlist` | Restrict inbound to these chat ids. Repeatable. |
| `--config` | string | inherits from root | Path to the YAML config file. |

## Config keys respected

`internal/config/config.go` `TelegramConfig`:

| Key | Type | Default | Effect |
|---|---|---|---|
| `telegram.token` | string | empty | Bot token. |
| `telegram.base_url` | string | `https://api.telegram.org` | Override Bot API endpoint (self-hosted `telegram-bot-api` or proxy). |
| `telegram.reply_header` | string | empty | Prefix prepended to outbound messages. |
| `telegram.allowlist` | []string | empty | Chat ids permitted. Strings. |

## Allowlist syntax

Telegram chat ids are integers as returned by `chat.id` in Bot API updates. Rousseau treats them as strings for allowlist matching:

<div class="tabs" data-tabs="tg-id">
  <div class="tab-list" role="tablist" aria-label="Chat id kind">
    <button role="tab" aria-selected="true">Personal</button>
    <button role="tab" aria-selected="false">Group</button>
    <button role="tab" aria-selected="false">Channel</button>
  </div>
  <div class="tab-panel" role="tabpanel">

```yaml
telegram:
  allowlist:
    - "123456789"    # positive integer for private chats
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```yaml
telegram:
  allowlist:
    - "-987654321"   # negative integer for groups
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```yaml
telegram:
  allowlist:
    - "-1001234567890"  # -100... prefix for channels/supergroups
```

  </div>
</div>

To discover a chat id, message the bot once with an empty allowlist and grep the logs for the `router.transport.received` event; the `sender` attribute is the id.

## Environment variables

| Variable | Effect |
|---|---|
| `ROUSSEAU_TELEGRAM_TOKEN` | Overrides `telegram.token`. |
| `ROUSSEAU_TELEGRAM_BASE_URL` | Overrides the Bot API endpoint. |

## Startup sequence

1. Resolve token from flag, env, or config; fail if empty.
2. Default `claudecli.permission_mode` to `bypassPermissions`.
3. Open session store, build provider, tool registry, approver, compressor.
4. `telegram.New` — instantiate the Bot API client.
5. `wiring.startCron` — cron deliveries land via `sendMessage`.
6. Long-poll loop until context cancelled.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Clean context cancellation. |
| 1 | Missing token, HTTP transport error, provider/store failure. |
| 130 | SIGINT. |

## Worked examples

```sh
# Ad-hoc single-user bot
rousseau telegram --token 7000000000:AAE… --allow 123456789

# From config, no flags
cat > ~/.config/rousseau/config.yaml <<'EOF'
telegram:
  token: "7000000000:AAE…"
  allowlist:
    - "123456789"
    - "-987654321"
EOF
rousseau telegram
```

## Common failure modes

- **`Unauthorized`** — invalid or revoked bot token. Regenerate with @BotFather.
- **`Conflict: terminated by other getUpdates request`** — two rousseau instances polling the same token. Only one Bot API long-poll at a time.
- **`Forbidden: bot was blocked by the user`** — user blocked the bot; outbound messages to that chat fail permanently.
- **Silent inbound drops** — the sender's chat id is not on the allowlist. Check `router.transport.rejected`.

## Related pages

- [Transports: Telegram](/transports/telegram/)
- [Reference: Commands: cron](/reference/commands/cron/)
- [Best Practices: Secret management](/best-practices/secret-management/)
- [Reference: Logs](/reference/logs/)
