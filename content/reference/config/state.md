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
description: "Every state config field: state.path, session store location and permissions."
keywords: "config, state, sqlite, session store"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/config/state/"
subtitle: "State store configuration."
tags: "reference, config, state"
title: "Config: State"

news_genres: "Blog"
news_keywords: "config, state, sqlite"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Config: State"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 82
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/config/state/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/config/state/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Config: State"
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
twitter_description: "Every state config field: state.path, session store location and permissions."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Config: State"
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

The `state.*` block picks where rousseau persists everything: sessions, messages, cron jobs, JID map, claude cache, FTS5 recall index. Concrete implementation: `internal/state/sqlite/store.go`.

<aside class="admonition" data-type="tip"><span class="admonition-title">Single database</span><p>Every table (<code>sessions</code>, <code>messages</code>, <code>cron_jobs</code>, <code>jid_map</code>, <code>claude_cache</code>, <code>fts_index</code>) lives in the single SQLite file at <code>state.path</code>. WAL mode is enabled on open; multiple rousseau processes can read concurrently but only one writes at a time.</p></aside>

## `state.*`

| Field | Type | Default | Required | Description | Source |
|---|---|---|---|---|---|
| `state.path` | string | `$XDG_DATA_HOME/rousseau/sessions.db` (defaults to `~/.local/share/rousseau/sessions.db`) | no | Absolute path to the SQLite database. Parent directories are created with mode `0755`. | `StateConfig.Path` in `internal/config/config.go`; default injected in `setDefaults` |

That's the only key. Everything else is fixed by the SQLite pragmas applied in `sqlitestore.Open`:

| Pragma | Value | Rationale |
|---|---|---|
| `journal_mode` | `WAL` | Concurrent readers, single writer, safe under crashes. |
| `busy_timeout` | `15000` | 15s wait before returning `SQLITE_BUSY`. |
| `foreign_keys` | `1` | Cascading deletes when a session is removed. |
| `synchronous` | `NORMAL` | Durability + speed compromise (WAL truncates on checkpoint). |

## Environment variables

| Variable | Effect |
|---|---|
| `ROUSSEAU_STATE_PATH` | Overrides `state.path`. |
| `XDG_DATA_HOME` | Base directory when `state.path` is unset. |

## Worked examples

<div class="tabs" data-tabs="state-ex">
  <div class="tab-list" role="tablist" aria-label="Deployment">
    <button role="tab" aria-selected="true">Default</button>
    <button role="tab" aria-selected="false">Container</button>
    <button role="tab" aria-selected="false">Multi-tenant</button>
  </div>
  <div class="tab-panel" role="tabpanel">

```yaml
# No override needed
```

Rousseau creates `~/.local/share/rousseau/sessions.db` on first launch.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```yaml
state:
  path: /var/lib/rousseau/sessions.db
```

Combined with the Quadlet unit's `Volume=%h/.local/share/rousseau:/var/lib/rousseau:rw,Z`, the container writes to a persistent bind mount. See [Deployment](/deployment/).

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```yaml
# per-project config
state:
  path: /projects/webapp/rousseau/sessions.db
```

Each project gets its own database, isolating conversation history and FTS5 recall. See [Best Practices: Multi-tenant](/best-practices/multi-tenant/).

  </div>
</div>

## Migration paths

- **Bare-metal → container**: copy the file, adjust `Volume=` in the Quadlet unit, restart. WAL/SHM files can travel with the main DB but will be recreated at first open.
- **Move to a bigger disk**: stop rousseau, `cp -a sessions.db* /new/location/`, update `state.path`, restart.
- **Reset**: `rm ~/.local/share/rousseau/sessions.db*` — you lose all conversation history and cron jobs. Consider `rousseau session delete <id> --yes` for targeted removal.

See [Migrations: Container migration](/migrations/container-migration/) and [Best Practices: Disaster recovery](/best-practices/disaster-recovery/).

## Related pages

- [Reference: Session store](/reference/session-store/)
- [Best Practices: Disaster recovery](/best-practices/disaster-recovery/)
- [Migrations: Container migration](/migrations/container-migration/)
- [Reference: Config: Agent](/reference/config/agent/)
