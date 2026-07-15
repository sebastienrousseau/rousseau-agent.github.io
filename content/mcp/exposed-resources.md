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
description: "MCP resources exposed by rousseau's stdio server today (none) and the roadmap for sessions-as-resources."
keywords: "mcp, resources, roadmap, sessions, resources/list"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/mcp/exposed-resources/"
subtitle: "What resources rousseau exposes today, and what is planned."
tags: "mcp, resources, roadmap"
title: "MCP: Exposed resources"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, resources, roadmap, sessions, resources/list"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP: Exposed resources"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "mcp"
order: 73
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/mcp/exposed-resources/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/exposed-resources/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "MCP: Exposed resources"
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
twitter_description: "MCP resources exposed by rousseau's stdio server today (none) and the roadmap for sessions-as-resources."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP: Exposed resources"
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

## Current status

Rousseau's MCP server (`internal/mcp/server.go`) declares `Tools` capability only. It returns an empty list on `resources/list`:

```
MethodResourcesList → okResponse(env.ID, map[string]any{"resources": []any{}})
```

The intent is deliberate. Every use case that would look like an MCP resource — a saved session, a cron job description — is exposed today through a tool (`rousseau_read_session`, `rousseau_cron_list`) so the host can request exactly the data it needs, when it needs it, rather than pre-listing every session.

## Why not resources today

MCP resources shine when a host wants to enumerate a modest, well-defined set of URIs (files, pages) and dereference them lazily. Rousseau's session store can grow into thousands of rows; enumerating every session on every `resources/list` call would blow up the host's context. The tool surface (search / list / read) is a better shape for high-cardinality state.

## Roadmap

Two candidates worth exposing as MCP resources, once the MCP spec supports paginated resource enumeration robustly:

### Candidate: `rousseau://sessions/<id>`

Every rousseau session as a resource. URIs would look like:

```
rousseau://sessions/1a2b3c4d-…
```

Dereferencing would return the same transcript `rousseau_read_session` returns today. This would let the host attach a specific session to a conversation as a first-class citizen ("attach session 1a2b3c…", drag-and-drop), rather than requiring the model to remember to call the tool.

Gating: a resource list would need to be paginated. Recent versions of the MCP spec propose cursor-based pagination; once that lands and hosts implement it, this becomes viable.

### Candidate: `rousseau://cron/<name>`

Every cron job as a resource. Read-only inspection of the prompt, schedule, delivery target, and last-run timestamp. Small list — probably safe to enumerate today, but not worth exposing separately from `rousseau_cron_list` until the sessions-as-resources shape is proven.

## Prompts capability

Similarly not exposed today. `MethodPromptsList` returns `{"prompts": []any{}}` in `internal/mcp/server.go` `dispatch`. Rousseau does not have a curated prompt library to expose; the skills mechanism (`internal/skills/skills.go`) is the equivalent internal concept, and it is not currently surfaced over MCP.

If the skills roadmap converges on shareable prompts, exposing them as MCP prompts is the natural next step. See [Skills](/skills/).

## How to work around the gap today

If your MCP host requires resources for a specific UI affordance (e.g. drag-and-drop of a session), the workaround is:

1. Ask the host to invoke `rousseau_list_sessions` at the start of the chat.
2. Copy the session id you want to reference.
3. Invoke `rousseau_read_session` with that id.

Not as ergonomic as native resource dereferencing, but functionally equivalent.

## Requesting a resource surface

Not every operator needs resources over MCP. If your team does, the constructive path is to file an issue with:

- The specific MCP host you're integrating with.
- The user-facing action that would be nicer with resources.
- Rough traffic expectations (how many sessions, how often).

## Related

- [MCP](/mcp/) — the umbrella reference.
- [MCP: Exposed tools](/mcp/exposed-tools/) — what is exposed today.
- [MCP: Compatibility](/mcp/compatibility/) — tested clients.
- [Skills](/skills/) — the internal concept that may become MCP prompts.
