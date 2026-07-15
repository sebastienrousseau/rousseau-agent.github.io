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
description: "Expose rousseau's session store to Claude Desktop and Cursor via the built-in MCP server so your desktop agent recalls WhatsApp conversations."
keywords: "mcp, claude desktop, cursor, stdio, recall, recipes"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/recipes/mcp-desktop-integration/"
subtitle: "Expose rousseau's history to Claude Desktop / Cursor."
tags: "recipes, mcp, desktop"
title: "Recipe: MCP Desktop Integration"

news_genres: "Blog"
news_keywords: "mcp, claude desktop, cursor"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Recipe: MCP Desktop Integration"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "recipes"
order: 19
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/recipes/mcp-desktop-integration/index.html"
item_link: "https://docs.rousseau-agent.dev/recipes/mcp-desktop-integration/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Recipe: MCP Desktop Integration"
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
twitter_description: "Expose rousseau's session store to Claude Desktop and Cursor via the built-in MCP server."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Recipe: MCP Desktop Integration"
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

Register `rousseau mcp` as a stdio MCP server in Claude Desktop or Cursor. Your desktop agent gains four tools: `rousseau_search_sessions`, `rousseau_list_sessions`, `rousseau_read_session`, `rousseau_cron_list`. This lets it recall a WhatsApp conversation from three days ago while you plan a new feature at your desk.

## Prerequisites

- Rousseau installed (`rousseau version` prints a real version).
- Claude Desktop 0.7+ or Cursor with MCP support.
- A `sessions.db` with some content — start from `rousseau chat` at least once.

## Wiring

<div class="tabs" data-tabs="mcp-recipe">
  <div class="tab-list" role="tablist" aria-label="MCP host">
    <button role="tab" aria-selected="true">Claude Desktop</button>
    <button role="tab" aria-selected="false">Cursor</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "rousseau": {
      "command": "rousseau",
      "args": ["mcp"]
    }
  }
}
```

Restart Claude Desktop. The tools appear under the tool picker.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

In Cursor Settings → MCP Servers → Add:

```json
{
  "mcpServers": {
    "rousseau": {
      "command": "/usr/local/bin/rousseau",
      "args": ["mcp"],
      "env": {
        "ROUSSEAU_STATE_PATH": "/home/you/.local/share/rousseau/sessions.db"
      }
    }
  }
}
```

Use absolute paths — Cursor's PATH may differ from your shell.

  </div>
</div>

## Verification

- [ ] Claude Desktop tool picker lists `rousseau_search_sessions`, `rousseau_list_sessions`, `rousseau_read_session`, `rousseau_cron_list`.
- [ ] Prompt: "Search my rousseau sessions for 'payments outage' and summarise." — the agent invokes `rousseau_search_sessions` and the results appear inline.
- [ ] Prompt: "Show my three most recent sessions." — the agent invokes `rousseau_list_sessions`.

## Failure modes

- **Host reports "server exited immediately"** — permission on `state.path`. `ls -l ~/.local/share/rousseau/sessions.db`.
- **Tools present but always return empty** — you pointed at an empty `sessions.db`. Run `rousseau chat` once.
- **Absolute vs relative path** — GUI apps do not inherit shell PATH. Use `/usr/local/bin/rousseau` or wherever `which rousseau` reports.

## Related pages

- [Reference: Commands: mcp](/reference/commands/mcp/)
- [MCP](/mcp/)
- [Reference: Session store](/reference/session-store/)
- [Best Practices: Session hygiene](/best-practices/session-hygiene/)
