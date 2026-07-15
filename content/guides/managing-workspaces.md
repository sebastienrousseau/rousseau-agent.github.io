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
description: "How rousseau's session store partitions by workspace, how to switch workspaces, share sessions across machines, and drop a workspace's history."
keywords: "workspace, session store, state path, sync, rsync, XDG_DATA_HOME"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/guides/managing-workspaces/"
subtitle: "Partition state per project, share history across machines, drop history cleanly."
tags: "guides, workspace, session store, sqlite"
title: "Guide: Managing workspaces"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "workspace, session store, state path, sync, rsync, XDG_DATA_HOME"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide: Managing workspaces"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 38
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/managing-workspaces/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/managing-workspaces/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guide: Managing workspaces"
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
twitter_description: "How rousseau's session store partitions by workspace, how to switch workspaces, share sessions across machines, and drop a workspace's history."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide: Managing workspaces"
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

## The convention

Rousseau does not have a first-class "workspace" concept. It has one `state.path` in `internal/config/config.go` (`StateConfig`) and by default points every process at `~/.local/share/rousseau/sessions.db`. All sessions, cron jobs, JID mappings, and the FTS5 recall index live in that single file.

For most operators that's exactly right. When you want isolation — per project, per machine, per client — you point rousseau at a different SQLite file. That file **is** the workspace.

## Switch workspace per invocation

Two knobs, either works:

```sh
# 1. flag on any rousseau command
rousseau --config ~/.config/rousseau/acme.yaml chat

# 2. env var (Viper picks it up via ROUSSEAU_STATE_PATH)
ROUSSEAU_STATE_PATH=~/.local/share/rousseau/acme.db rousseau chat
```

Neither approach requires a rousseau restart when you jump between workspaces — each process opens its own file.

## Per-project workspace layout

```
~/.config/rousseau/
├── acme.yaml         # provider = anthropic, state.path = …/acme.db
├── personal.yaml     # provider = claudecli, state.path = …/personal.db
└── work.yaml         # provider = bedrock,    state.path = …/work.db
```

Each config file overrides `state.path`:

```yaml
state:
  path: /home/seb/.local/share/rousseau/acme.db
```

Then launch each session with the right config. The TUI (`internal/tui/model.go`) surfaces the session id + provider in its status bar — visual confirmation you're in the right workspace.

## Sharing history across machines

The session store is a single SQLite file. WAL journaling is enabled by `Open()` in `internal/state/sqlite/store.go`, so live snapshots are safe:

```sh
# Snapshot laptop-to-desktop (both idle)
rsync -avz --partial \
  ~/.local/share/rousseau/sessions.db \
  desktop:~/.local/share/rousseau/sessions.db
```

**Only one writer at a time.** Do not run `rousseau whatsapp` on two machines against the same SQLite file over NFS — that is undefined. Sync when nothing is writing, or run a single writer with read replicas.

A safer alternative is the `.backup` snapshot:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db ".backup '/tmp/sessions.snap.db'"
scp /tmp/sessions.snap.db desktop:~/.local/share/rousseau/sessions.db
```

`.backup` uses SQLite's online backup API and produces a consistent point-in-time file.

## Migrating a workspace

Move the whole directory; that's the workspace:

```sh
rsync -avz ~/.local/share/rousseau/ new-host:~/.local/share/rousseau/
```

`whatsapp.db` (device credentials) is separate — you either bring it too (device stays paired) or leave it behind and re-scan the QR on the new host.

## Dropping a workspace's history

```sh
rousseau session list                 # confirm what you're about to lose
rm ~/.local/share/rousseau/acme.db*   # includes -wal and -shm sidecars
```

The next process to open the path will re-create it with the schema in `internal/state/sqlite/schema.sql`.

If you only want to drop a subset of sessions, use the CLI:

```sh
rousseau session delete <id> --yes
```

`rousseau session delete` (`internal/cli/session.go`) calls `Store.Delete`, which cascades through the FTS5 triggers to keep the recall index consistent. The `--yes` flag is required — the command refuses to run without it.

## Partial deletion via SQL

For bulk cleanup — every session older than 90 days:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions WHERE updated_at < datetime('now', '-90 days');
SQL
```

The FTS5 triggers (`sessions_fts_ad` in `internal/state/sqlite/search.go`) fire on the DELETE and keep the index in sync automatically.

## Per-workspace approvers

Because config file and state file are both per-workspace, so is the approver:

```yaml
# work.yaml — strict pattern approver
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

state:
  path: /home/seb/.local/share/rousseau/work.db
```

A separate `personal.yaml` might keep `mode: allow_all` for interactive work. See [Tutorial: Harden the approver](/tutorials/harden-approver-policy/).

## Related

- [Reference: Session store](/reference/session-store/) — schema.
- [Guides: Multi-provider](/guides/multi-provider/) — the two-config, two-provider pattern.
- [Reference: Environment Variables](/reference/environment-variables/) — every path env var.
- [User Guide: CLI](/user-guide/cli/) — `rousseau session` commands.
