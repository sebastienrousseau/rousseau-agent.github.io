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
description: "Rousseau as a Discord community helper: FAQ answers, docs citations, per-channel approval scoping."
keywords: "discord, community, gateway, faq, recipes"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/recipes/discord-community-bot/"
subtitle: "Rousseau as a Discord community helper."
tags: "recipes, discord, community"
title: "Recipe: Discord Community Bot"

news_genres: "Blog"
news_keywords: "discord, community, gateway"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Recipe: Discord Community Bot"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "recipes"
order: 18
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/recipes/discord-community-bot/index.html"
item_link: "https://docs.rousseau-agent.dev/recipes/discord-community-bot/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Recipe: Discord Community Bot"
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
twitter_description: "Rousseau as a Discord community helper: FAQ answers, docs citations, per-channel approval scoping."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Recipe: Discord Community Bot"
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

Rousseau in a Discord server, answering FAQ questions with docs citations. Scoped to specific channels through user-id allowlisting on the transport side (rousseau does not filter by channel today; add the bot to specific channels only, and set the allowlist to the user IDs of the community managers if you want to lock it down further).

## Prerequisites

- Discord bot token; Message Content intent enabled.
- Docs directory bind-mounted at `/workspace/docs`.
- Any provider with tool-use.

## Config

```yaml
provider: anthropic

anthropic:
  model: claude-sonnet-4-6
  max_tokens: 4096

agent:
  system_prompt: |
    Answer community questions from the docs directory only.
    When unsure, say "I don't know — try #help".
    Keep responses to under 5 sentences. Cite `docs/<file>.md` when quoting.
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

discord:
  token: "MTIz…"
  allowlist: []       # empty = anyone in the channels the bot is in
```

## Launch

```sh
rousseau discord
```

Invite the bot to your Discord server with a scoped invite URL (Bot permissions: Read Messages, Send Messages, Read Message History).

## Verification

- [ ] Post a common question; the bot answers within 3 s with a citation.
- [ ] Ask something outside the docs; the bot says it doesn't know and points to `#help`.
- [ ] `rousseau session list --limit 5` shows one session per Discord user.

## Failure modes

- **Bot answers `Disallowed intents`** — the bot's invite lacks the Message Content intent scope. Regenerate with the correct intents.
- **Rate-limited** — Discord 429s on burst posts. The transport retries with backoff.
- **Cost spike** — set the allowlist tightly or `max_tokens` lower.

## Related pages

- [Reference: Commands: discord](/reference/commands/discord/)
- [Transports: Discord](/transports/discord/)
- [Best Practices: Cost control](/best-practices/cost-control/)
- [Recipes: Matrix room monitor](/recipes/matrix-room-monitor/)
