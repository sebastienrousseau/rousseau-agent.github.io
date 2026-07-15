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
description: "The exact tool signatures exposed by rousseau's stdio MCP server, mirroring internal/mcp/tools.go."
keywords: "mcp, rousseau_search_sessions, rousseau_list_sessions, rousseau_read_session, rousseau_cron_list"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/mcp/exposed-tools/"
subtitle: "Every tool rousseau's MCP server advertises, with schemas."
tags: "mcp, tools, sessions, cron"
title: "MCP: Exposed tools"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, rousseau_search_sessions, rousseau_list_sessions, rousseau_read_session, rousseau_cron_list"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP: Exposed tools"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "mcp"
order: 72
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/mcp/exposed-tools/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/exposed-tools/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "MCP: Exposed tools"
last_build_date: "Mon, 13 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
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
twitter_description: "The exact tool signatures exposed by rousseau's stdio MCP server, mirroring internal/mcp/tools.go."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP: Exposed tools"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Registration

`internal/cli/mcp.go` opens the SQLite session store, constructs a `NewCronStore`, wraps both in `mcp.NewStoreBackend`, and calls `mcp.RegisterRousseauTools(s, backend)`. The four tools below are attached in insertion order — `tools/list` returns them in this exact order.

Every tool is read-only. There is no write surface over MCP today; that is by design so an MCP host cannot mutate rousseau's state.

## `rousseau_search_sessions`

**Description (surfaced to hosts):** _Full-text search across every recorded rousseau session. Uses SQLite FTS5 syntax (phrases in double quotes, AND/OR/NOT, prefix wildcards)._

**Input schema:**

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "FTS5 query"
    },
    "limit": {
      "type": "integer",
      "description": "Cap hits returned. Default 20."
    }
  },
  "required": ["query"]
}
```

**Behaviour.** Passes `query` verbatim to SQLite's FTS5 engine (`Store.Search` in `internal/state/sqlite/search.go`). Results are ordered by BM25 rank (lower = more relevant). Each hit renders as three lines:

```
session <id> (rank 0.42)
    title:   <session title>
    snippet: <~200-char snippet with … ellipses>
```

**Errors.** An empty query returns `query is required`. FTS5 syntax errors bubble up as SQLite errors and surface via `isError: true`.

## `rousseau_list_sessions`

**Description (surfaced to hosts):** _List rousseau sessions newest-first._

**Input schema:**

```json
{
  "type": "object",
  "properties": {
    "limit": {
      "type": "integer",
      "description": "Cap rows returned. Default 20."
    }
  }
}
```

**Behaviour.** Calls `Store.List` which uses the `idx_sessions_updated_at DESC` index. Each row:

```
<session-id>  <title>  msgs=<count>  updated=<iso-8601>
```

Returns `(no sessions)` when the store is empty.

## `rousseau_read_session`

**Description (surfaced to hosts):** _Return the full transcript of a rousseau session by id._

**Input schema:**

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "description": "Session id"
    }
  },
  "required": ["id"]
}
```

**Behaviour.** Calls `Store.Load` to fetch the full `agent.Session`. Renders as:

```
id: <session-id>
title: <session title>
created: <iso-8601>
updated: <iso-8601>
messages: <count>

[0] user
    <text content>
[1] assistant
    <text content>
    ...
```

Only text content is rendered — tool_use blocks and tool_result blocks are elided in the MCP surface (the CLI `rousseau session show` includes them; MCP intentionally does not).

**Errors.** `id is required` on empty input. `state.ErrNotFound` on unknown id.

## `rousseau_cron_list`

**Description (surfaced to hosts):** _List rousseau's scheduled cron jobs (name, schedule, prompt, delivery target)._

**Input schema:**

```json
{
  "type": "object",
  "properties": {}
}
```

**Behaviour.** Calls `CronStore.List` — one row per `cron_jobs` row:

```
<name> [<on|off>] <cron-expr> → <deliver-to>  prompt="<prompt>"  deliver=<deliver-to>
```

Returns `(no jobs)` when the cron table is empty. Also returns `(no jobs)` if the `CronStore` is nil at construction time (a defensive path in `storeBackend.CronList`).

## What is NOT exposed

Deliberate omissions:

| Surface | Why not |
|---|---|
| `rousseau_write_session` / `rousseau_delete_session` | Mutation over MCP would let an untrusted host reshape rousseau's audit trail. |
| `rousseau_add_cron` | Same reason — mutation. Add cron jobs via `rousseau cron add`. |
| The built-in tools (`read`, `write`, `edit`, `grep`, `bash`) | These are agent-facing tools for the LLM inside rousseau's own loop, not host-facing. Exposing them would give the MCP host the ability to shell out on the host running rousseau — precisely the trust flip we don't want. |
| JID map lookup | Exposes PII (phone numbers). If you need it, query SQLite directly on the machine where the daemon runs. |

## Error surface

MCP handlers return `([]Content, error)`. On error, the server (`internal/mcp/server.go` `handleToolsCall`) surfaces the error as `ToolsCallResult{Content: text of err, IsError: true}`. This is per the MCP convention: tool failures flow through the content channel with `isError=true`, not through the JSON-RPC `error` channel. Hosts should render the text and continue.

## Related

- [MCP](/mcp/) — the umbrella reference.
- [MCP: Compatibility](/mcp/compatibility/) — tested clients.
- [MCP: Exposed resources](/mcp/exposed-resources/) — roadmap.
- [Reference: Tool schemas](/reference/tool-schemas/) — the different agent-facing tool set.
