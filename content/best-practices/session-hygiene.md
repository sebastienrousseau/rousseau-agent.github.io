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
description: "When to compress a session, when to start a fresh one, and when to nuke the store entirely."
keywords: "sessions, compression, hygiene, best practices"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/best-practices/session-hygiene/"
subtitle: "Compress, split, or nuke — deciding when."
tags: "best-practices, sessions"
title: "Session Hygiene"

news_genres: "Blog"
news_keywords: "sessions, compression, hygiene"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Session Hygiene"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "best-practices"
order: 13
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/best-practices/session-hygiene/index.html"
item_link: "https://docs.rousseau-agent.dev/best-practices/session-hygiene/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Session Hygiene"
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
twitter_description: "When to compress a session, when to start a fresh one, and when to nuke the store."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Session Hygiene"
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

Rousseau's session store is durable by design — nothing is ever purged automatically. That means operators own three decisions:

1. When to enable LLM-backed compression.
2. When to start a fresh session vs continue an existing one.
3. When (rarely) to delete or nuke sessions.

## When to enable compression

`agent.compression.enabled` is off by default. Turn it on when:

- You are running against a **pay-per-token provider** (Anthropic direct, OpenAI, Bedrock, Vertex).
- Your sessions routinely pass 60 messages before wrapping up (the default trigger).
- You care about latency: shorter prompts = faster responses.

Keep it off when:

- You are on `claudecli` with a subscription-tier Claude Code plan. Compression adds a summarisation-call cost you're not otherwise paying.
- You want perfect recall for audit purposes (compressed history is a summary, not the transcript).

Sensible defaults:

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60
    keep_recent: 8
```

## When to start a fresh session

- **New topic** — the model conflates unrelated threads if you keep going. Start a new session.
- **After an outage** — a fresh session with a clean context often outperforms one that carries stale state.
- **When switching providers** — history transfers cleanly, but the model's tone/style will drift; a fresh session avoids the confusion.
- **Per project** — one session per repo/feature is a good default.

Use `--title` on `rousseau chat` to name sessions distinctly. Titles show up in `rousseau session list` and MCP tool responses.

## Finding old sessions

```sh
# Newest first, 10 rows
rousseau session list --limit 10

# FTS5 search across the whole history
rousseau session search "auth refactor"
rousseau session search '"payment webhook" AND signature'
rousseau session search 'kub*'
```

## Deleting

```sh
rousseau session delete <session-id> --yes
```

<aside class="admonition" data-type="warning"><span class="admonition-title">There is no undo</span><p>SQLite <code>DELETE</code> is durable. Take a backup before mass deletion.</p></aside>

## Nuking the store

```sh
# Stop every rousseau process first
systemctl --user stop 'rousseau-*.service'

# Backup
cp -a ~/.local/share/rousseau ~/.local/share/rousseau.pre-nuke

# Nuke
rm ~/.local/share/rousseau/sessions.db*
```

Reasons to nuke:

- You want a clean slate for a new project laptop.
- The database grew unmanageably (rare — SQLite compresses well).
- A schema migration failed (`sessions.db.pre-migration` should exist as backup).

## Cross-session recall

FTS5 indexing means the agent can pull a snippet from an old session into a new one via the `rousseau_search_sessions` MCP tool. Even after compression, the raw messages remain until you delete. This lets old-session recall stay accurate while current context stays short.

## Related pages

- [Reference: Config: State](/reference/config/state/)
- [Reference: Config: Agent](/reference/config/agent/)
- [Reference: Session store](/reference/session-store/)
- [Best Practices: Disaster recovery](/best-practices/disaster-recovery/)
- [Concepts](/concepts/)
