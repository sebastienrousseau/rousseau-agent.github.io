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
description: "Expose rousseau's session store and cron jobs to Claude Desktop as an MCP server that Claude can drive from its own tool interface."
keywords: "mcp, claude desktop, stdio, tools, rousseau_search_sessions, rousseau_read_session"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/tutorials/expose-tools-via-mcp/"
subtitle: "Wire rousseau mcp into Claude Desktop and let it query the session store."
tags: "tutorials, mcp, claude-desktop, stdio, sessions"
title: "Tutorial: Expose tools via MCP"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, claude desktop, stdio, tools, rousseau_search_sessions, rousseau_read_session"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorial: Expose tools via MCP"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/expose-tools-via-mcp/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/expose-tools-via-mcp/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorial: Expose tools via MCP"
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
twitter_description: "Expose rousseau's session store and cron jobs to Claude Desktop as an MCP server that Claude can drive from its own tool interface."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorial: Expose tools via MCP"
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

## What you build

Claude Desktop with rousseau as an MCP stdio server. From inside a Claude Desktop chat you can ask "find the session where we discussed the retry logic" and Claude will call `rousseau_search_sessions`, then `rousseau_read_session` to fetch the full transcript.

Estimated time: 5 minutes.

## Prerequisites

- Claude Desktop installed (macOS or Windows). Linux uses the Claude CLI, not Desktop — see the alternative at the bottom.
- Rousseau installed and on `$PATH`.
- Some existing session history in `~/.local/share/rousseau/sessions.db` — run `rousseau chat` a few times if the file is empty.

## Step 1: understand what gets exposed

`rousseau mcp` (`internal/cli/mcp.go`) starts a stdio JSON-RPC server that speaks the Model Context Protocol. `RegisterRousseauTools` (`internal/mcp/tools.go`) attaches four read-only tools:

| Tool | Purpose |
|---|---|
| `rousseau_search_sessions` | FTS5 full-text search across every recorded session (via `internal/state/sqlite/search.go`). |
| `rousseau_list_sessions` | List sessions newest-first. |
| `rousseau_read_session` | Return the full transcript of one session by id. |
| `rousseau_cron_list` | List rousseau's scheduled cron jobs. |

There are no write tools; MCP hosts can browse but not mutate. See [MCP: Exposed tools](/mcp/exposed-tools/) for the exact input schemas.

## Step 2: wire Claude Desktop

Claude Desktop reads `claude_desktop_config.json`:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add a `mcpServers` entry pointing at your `rousseau` binary:

```json
{
  "mcpServers": {
    "rousseau": {
      "command": "/usr/local/bin/rousseau",
      "args": ["mcp"]
    }
  }
}
```

Restart Claude Desktop.

## Step 3: verify

Open a Claude Desktop chat and check that the tools appear in the tool picker. You should see four tools prefixed `rousseau_`. Try:

```
Use rousseau_list_sessions to show me my 5 most recent sessions,
then read the top one with rousseau_read_session.
```

Claude will invoke both tools, and rousseau's MCP server (`internal/mcp/server.go`) will handle each JSON-RPC envelope over stdin/stdout. Behind the scenes:

1. Claude Desktop calls `initialize`, then `tools/list` — rousseau responds with the four tools declared in insertion order.
2. Claude picks a tool and calls `tools/call` with the arguments — rousseau's handler (from `internal/mcp/tools.go`) queries SQLite and returns text content.
3. On error, rousseau surfaces the error through the content channel (`isError=true`), never as a JSON-RPC error — MCP hosts expect this.

## Step 4: (optional) attach to Claude CLI / other MCP host

The stdio protocol is host-agnostic. For the Claude CLI:

```sh
claude --mcp-config <(cat <<'JSON'
{ "mcpServers": { "rousseau": { "command": "rousseau", "args": ["mcp"] } } }
JSON
)
```

For Continue.dev, Codeium, or another MCP host, follow their MCP-server registration flow with `command: rousseau`, `args: [mcp]`. See [MCP: Compatibility](/mcp/compatibility/) for the tested clients.

## Step 5: FTS5 syntax cheat-sheet

Because rousseau_search_sessions is a thin wrapper around SQLite FTS5 (`internal/state/sqlite/search.go`), the query field supports:

| Query | Meaning |
|---|---|
| `retry logic` | Any doc containing both terms. |
| `"retry logic"` | Exact phrase. |
| `retr*` | Prefix match. |
| `retry OR backoff` | Boolean OR. |
| `retry NOT retries` | Exclusion. |

Ranking uses BM25 (lower rank = more relevant); the `snippet()` call in `Search` gives you a 200-character preview per hit.

## Troubleshooting

- **"unknown tool" in Claude Desktop.** Restart the app. The tool list is only fetched on session start.
- **Server exits immediately.** `rousseau mcp` opens the SQLite state file; if the path in `state.path` isn't writable, `Open()` fails and the process exits with a non-zero code. Run it from a shell to see the error.
- **Empty search results.** Confirm the FTS5 index is populated: `sqlite3 ~/.local/share/rousseau/sessions.db "SELECT count(*) FROM sessions_fts"`. `EnsureSearch` in `internal/state/sqlite/search.go` back-fills the index on every open, but a corrupted state file may need a manual rebuild.

## Related

- [MCP](/mcp/) — the reference doc.
- [MCP: Exposed tools](/mcp/exposed-tools/) — every tool schema.
- [MCP: Compatibility](/mcp/compatibility/) — tested clients.
- [Reference: Session store](/reference/session-store/) — the SQLite schema behind the tools.
