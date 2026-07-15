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
description: "Rousseau in a Matrix room as a self-hosted community helper. Explains room commands, indexes new messages for later recall."
keywords: "matrix, room, community, synapse, dendrite, recipes"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/recipes/matrix-room-monitor/"
subtitle: "Rousseau as a self-hosted Matrix community helper."
tags: "recipes, matrix, community"
title: "Recipe: Matrix Room Monitor"

news_genres: "Blog"
news_keywords: "matrix, room, community"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Recipe: Matrix Room Monitor"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "recipes"
order: 17
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/recipes/matrix-room-monitor/index.html"
item_link: "https://docs.rousseau-agent.dev/recipes/matrix-room-monitor/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Recipe: Matrix Room Monitor"
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
twitter_description: "Rousseau in a Matrix room as a self-hosted community helper."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Recipe: Matrix Room Monitor"
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

Invite `@rousseau-bot:matrix.example` into your community room. It answers questions from documented sources, and every conversation is FTS5-indexed so future queries recall past answers.

## Prerequisites

- Self-hosted Synapse (or Dendrite / Conduwuit) with a bot user provisioned.
- Access token for the bot user.
- Docs and knowledge base bind-mounted at `/workspace/docs`.

## Config

```yaml
provider: anthropic

anthropic:
  model: claude-sonnet-4-6
  max_tokens: 4096

agent:
  system_prompt: |
    You are a community helper. Answer only from the docs directory.
    When you don't know, say so and point at a channel where a human
    can help. Keep responses under 400 words.
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

matrix:
  homeserver_url: "https://matrix.example"
  access_token: "syt_…"
  user_id: "@rousseau-bot:matrix.example"
  allowlist: []      # empty = anyone in a room the bot is invited to
```

<aside class="admonition" data-type="warning"><span class="admonition-title">Encrypted rooms not supported</span><p>The Matrix transport does not currently support end-to-end encrypted rooms. Invite the bot into an unencrypted room.</p></aside>

## Launch

```sh
rousseau matrix
```

Invite the bot from your Matrix client. It responds to any message in the room.

## Verification

- [ ] `journalctl … | grep matrix.starting` and `matrix.connected` (if emitted) at boot.
- [ ] `@rousseau-bot: how do I install?` returns a docs-anchored answer.
- [ ] Ask the same question two days later; the FTS5 recall retrieves the previous answer for consistency.

## Failure modes

- **`M_UNKNOWN_TOKEN`** — access token expired or revoked. Re-login the bot user.
- **Bot spams the room** — you forgot to set `matrix.user_id` and the bot answers its own messages.
- **Slow first response after long idle** — the `/sync` cursor rebuilds. This is one-time per restart.

## Related pages

- [Reference: Commands: matrix](/reference/commands/matrix/)
- [Transports: Matrix](/transports/matrix/)
- [Best Practices: Multi-tenant](/best-practices/multi-tenant/)
- [Recipes: Discord community bot](/recipes/discord-community-bot/)
