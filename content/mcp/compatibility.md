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
description: "MCP clients tested against rousseau's stdio server: Claude Desktop, Claude CLI, Continue, Codeium, plus setup snippets."
keywords: "mcp, compatibility, claude desktop, continue, codeium, stdio, claude_desktop_config"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/mcp/compatibility/"
subtitle: "Which MCP clients talk to rousseau's stdio server."
tags: "mcp, compatibility, claude, continue, stdio"
title: "MCP: Compatibility"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, compatibility, claude desktop, continue, codeium, stdio, claude_desktop_config"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP: Compatibility"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "mcp"
order: 71
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/mcp/compatibility/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/compatibility/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "MCP: Compatibility"
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
twitter_description: "MCP clients tested against rousseau's stdio server: Claude Desktop, Claude CLI, Continue, Codeium, plus setup snippets."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP: Compatibility"
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

## The protocol contract

Rousseau's MCP server (`internal/mcp/server.go`) speaks JSON-RPC 2.0 over stdio and advertises the tools declared in `internal/mcp/tools.go`. It handles these methods:

- `initialize` — returns `ServerCapabilities.Tools`.
- `initialized` — notification, no reply.
- `ping` — returns `{}`.
- `tools/list` — returns the four tools in insertion order.
- `tools/call` — invokes a tool handler, returns `ToolsCallResult` with `content` and `isError`.
- `resources/list`, `prompts/list` — return empty arrays (see roadmap notes below).
- `shutdown` — returns `{}`.

Any MCP host that speaks stdio JSON-RPC and calls the four methods above is compatible.

## Tested clients

| Client | Status | How to register |
|---|---|---|
| Claude Desktop (macOS / Windows) | Works. | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows). |
| Claude CLI (`claude`) | Works. | `--mcp-config <file>` or a `[mcp]` block in `~/.claude/config.json`. |
| Continue.dev (VS Code / JetBrains) | Works. | `~/.continue/config.json` `mcpServers` block. |
| Codeium (IDE extensions) | Works when Codeium exposes MCP host mode (recent releases). Setup varies by IDE. |
| Cursor (recent versions) | Works. Register under Cursor's own MCP settings UI. |
| Any Go / TypeScript / Python MCP host SDK | Works. Instantiate with `command: "rousseau", args: ["mcp"]`. |

Unknown / untested but likely compatible: `zed`, `windsurf`, `aider`. If your host supports the MCP stdio spec, rousseau will work.

## Claude Desktop

Edit `claude_desktop_config.json` (path above) and add:

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

Restart Claude Desktop. The four `rousseau_*` tools show up in the tool picker on the next chat session.

For per-workspace state, add an env override:

```json
{
  "mcpServers": {
    "rousseau-work": {
      "command": "/usr/local/bin/rousseau",
      "args": ["--config", "/home/seb/.config/rousseau/work.yaml", "mcp"]
    }
  }
}
```

## Claude CLI

Point the CLI at a config:

```sh
claude --mcp-config <(cat <<'JSON'
{
  "mcpServers": {
    "rousseau": {
      "command": "rousseau",
      "args": ["mcp"]
    }
  }
}
JSON
)
```

Or bake it into `~/.claude/config.json` under an `mcpServers` block using the same shape.

## Continue.dev

Add to `~/.continue/config.json`:

```json
{
  "mcpServers": [
    {
      "name": "rousseau",
      "command": "rousseau",
      "args": ["mcp"]
    }
  ]
}
```

Continue picks up the tools on the next model call.

## Cursor

Cursor exposes MCP registration in its Settings > MCP UI. Register a new server named `rousseau` with command `rousseau` and args `mcp`. No config file editing required.

## Codeium

Codeium's MCP support ships behind a feature flag in recent versions of the IDE extension. Consult the extension's docs — the registration is again a `command / args` pair.

## Environment variables and secrets

Because rousseau's MCP surface is read-only over the session store, it does not need provider credentials. `ANTHROPIC_API_KEY` and similar are unused by `rousseau mcp` — only by the transport / chat daemons that _generate_ sessions.

## Common issues

- **"Server exited immediately."** Rousseau's `mcp` command opens `state.path`. If the file isn't writable, the process exits non-zero. Run `rousseau mcp` from a shell to see the exact error.
- **"Unknown tool: rousseau_search_sessions."** The host cached an older tool list. Restart the host.
- **Duplicate registration.** If two rousseau servers are registered with the same name, only the last one wins.

## Resources and prompts

`resources/list` and `prompts/list` currently return empty. The [Exposed resources](/mcp/exposed-resources/) page tracks the roadmap for exposing sessions as MCP resources.

## Related

- [MCP](/mcp/) — the umbrella reference.
- [MCP: Exposed tools](/mcp/exposed-tools/) — every tool signature.
- [MCP: Exposed resources](/mcp/exposed-resources/) — roadmap.
- [Tutorial: Expose tools via MCP](/tutorials/expose-tools-via-mcp/) — worked example.
