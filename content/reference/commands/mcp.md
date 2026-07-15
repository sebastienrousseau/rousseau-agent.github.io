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
description: "Complete reference for rousseau mcp: stdio JSON-RPC 2.0 server, exposed tools, MCP host wiring, exit codes."
keywords: "mcp, jsonrpc, stdio, claude desktop, cli reference, rousseau mcp"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/commands/mcp/"
subtitle: "Complete reference for `rousseau mcp`."
tags: "reference, cli, mcp"
title: "rousseau mcp"

news_genres: "Blog"
news_keywords: "mcp, jsonrpc, stdio"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "rousseau mcp"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 70
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/commands/mcp/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/commands/mcp/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "rousseau mcp"
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
twitter_description: "Complete reference for rousseau mcp: stdio JSON-RPC 2.0 server, exposed tools, MCP host wiring, exit codes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "rousseau mcp"
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

`rousseau mcp` starts a stdio Model Context Protocol server (spec revision 2024-11-05). It publishes rousseau's session store and cron jobs as MCP tools so any MCP host (Claude Desktop, Cursor, IDE extensions, other agents) can search, list, and read your rousseau history.

Source: `internal/cli/mcp.go`. Server implementation: `internal/mcp/`.

<aside class="admonition" data-type="tip"><span class="admonition-title">Read-only from the MCP side</span><p>The exposed tools are read-only queries into rousseau's session store and cron table. The MCP server does not accept new prompts or run the agent loop — for that, use <code>rousseau chat</code> or a transport.</p></aside>

## Synopsis

```sh
rousseau mcp [--config <path>]
```

There are no MCP-specific flags. Communication is over stdin/stdout; the MCP host launches rousseau as a subprocess.

## Exposed tools

| Tool | Purpose | Returns |
|---|---|---|
| `rousseau_search_sessions` | FTS5 search across every recorded conversation | ranked list of `{session_id, title, snippet, rank}` |
| `rousseau_list_sessions` | List recent sessions newest-first | `{id, title, message_count, updated_at}` rows |
| `rousseau_read_session` | Fetch the full transcript of one session | ordered messages with role + content |
| `rousseau_cron_list` | List every scheduled prompt | `{id, name, cron_expr, enabled, last_run_at, ...}` |

These tools are registered by `mcp.RegisterRousseauTools(s, mcp.NewStoreBackend(concrete, cronStore))`.

## Environment variables

`rousseau mcp` inherits every environment variable resolved by `config.Load`. The most relevant:

| Variable | Effect |
|---|---|
| `ROUSSEAU_STATE_PATH` | Override the SQLite session store location. |
| `ROUSSEAU_LOG_LEVEL` | Log level for the MCP server itself (writes to stderr; stdout is reserved for JSON-RPC). |
| `ROUSSEAU_LOG_FORMAT` | Log format (`text` or `json`). |

<aside class="admonition" data-type="warning"><span class="admonition-title">stderr for logs</span><p>MCP hosts pipe stdout to their JSON-RPC parser. Ensure any structured logs go to stderr — rousseau does this by default via <code>internal/cli/root.go</code>'s <code>newLogger</code>.</p></aside>

## Wiring into an MCP host

<div class="tabs" data-tabs="mcp-host">
  <div class="tab-list" role="tablist" aria-label="MCP host">
    <button role="tab" aria-selected="true">Claude Desktop</button>
    <button role="tab" aria-selected="false">Cursor</button>
    <button role="tab" aria-selected="false">Generic</button>
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

Cursor honours the same `mcpServers` shape in its settings JSON. Set the command to the absolute path of your rousseau binary if it isn't on Cursor's PATH.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Any MCP host that follows the stdio transport spec can attach to `rousseau mcp` by spawning the subprocess and pumping JSON-RPC over stdio.

  </div>
</div>

## Startup sequence

1. Open the SQLite session store at `state.path`.
2. Instantiate the cron store.
3. Construct `mcp.NewServer("rousseau", version, logger)`.
4. Register the four tools.
5. `s.Serve(ctx, os.Stdin, os.Stdout)` — blocks reading JSON-RPC from stdin.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | stdin closed (host disconnected). |
| 1 | Store or server startup error. |
| 130 | SIGINT. |

## Worked examples

```sh
# Manual smoke-test: send an `initialize` request over stdin
printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","clientInfo":{"name":"probe","version":"0"},"capabilities":{}}}' | rousseau mcp
```

You should see a JSON-RPC response containing `serverInfo` with `"name":"rousseau"`.

## Common failure modes

- **Host says "server exited immediately"** — a permission error opening `state.path`. Check `ls -l ~/.local/share/rousseau/sessions.db`.
- **Nothing shows up in Claude Desktop** — the config JSON syntax is wrong. Validate with `jq . claude_desktop_config.json`.
- **`FTS5 syntax error`** — search queries must use FTS5 grammar (phrases in double quotes, `AND`/`OR`/`NOT`, prefix `foo*`).

## Related pages

- [MCP](/mcp/) — protocol overview.
- [Recipes: MCP desktop integration](/recipes/mcp-desktop-integration/)
- [Reference: Session store](/reference/session-store/)
- [Reference: Commands: chat](/reference/commands/chat/)
