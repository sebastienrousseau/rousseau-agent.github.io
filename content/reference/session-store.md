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
description: "Rousseau's SQLite session store: sessions table, FTS5 recall index, JID mapping table, cron jobs, and WAL journaling."
keywords: "sqlite, fts5, session store, sessions, jid, cron, WAL, schema"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/session-store/"
subtitle: "The SQLite schema at the heart of rousseau's state."
tags: "reference, sqlite, fts5, session, wal"
title: "Reference: Session Store"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "sqlite, fts5, session store, sessions, jid, cron, WAL, schema"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Reference: Session Store"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 53
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/session-store/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/session-store/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Reference: Session Store"
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
twitter_description: "Rousseau's SQLite session store: sessions table, FTS5 recall index, JID mapping table, cron jobs, and WAL journaling."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Reference: Session Store"
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

## Location and driver

The session store is a single SQLite database at `state.path` (defaults to `~/.local/share/rousseau/sessions.db`, see `internal/config/config.go` `setDefaults`).

Rousseau uses `modernc.org/sqlite` — a pure-Go SQLite driver. There is **no CGO or libsqlite3 dependency**. The Go binary in `bin/rousseau` is fully static.

`internal/state/sqlite/store.go` `Open()` applies four pragmas on every open:

| PRAGMA | Purpose |
|---|---|
| `journal_mode=WAL` | Write-ahead logging. Enables concurrent readers, safe live backups. |
| `foreign_keys=ON` | Standard integrity guarantee. |
| `busy_timeout=15000` | 15-second wait on lock contention — critical once multiple transports write concurrently. |
| — | `EnsureSearch` runs afterwards to install the FTS5 schema. |

The store is opened once per process. Multiple daemons pointing at the same DB file are supported because of the busy-timeout + WAL combination — the WhatsApp bridge, `rousseau mcp`, and `rousseau session list` can share the file safely.

## Schema tour

### Table: `sessions`

Defined in `internal/state/sqlite/schema.sql`:

```sql
CREATE TABLE IF NOT EXISTS sessions (
    id             TEXT PRIMARY KEY,
    title          TEXT NOT NULL,
    payload        TEXT NOT NULL,        -- JSON blob of the full agent.Session
    message_count  INTEGER NOT NULL DEFAULT 0,
    created_at     TEXT NOT NULL,
    updated_at     TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sessions_updated_at
    ON sessions(updated_at DESC);
```

**Payload shape.** The `payload` column stores the full `agent.Session` JSON — roles, content blocks, tool-use and tool-result blocks, timestamps. See `Save`/`Load` in `internal/state/sqlite/store.go`. Keeping the whole session as one JSON blob keeps schema migrations rare; queries against internals go through the FTS5 index below.

**Timestamps** are ISO-8601 with millisecond precision (`2006-01-02T15:04:05.000Z` in Go time syntax), UTC.

**Ordering.** `idx_sessions_updated_at` powers `List` and `RecentSessions` (both in `store.go` / `search.go`).

### Virtual table: `sessions_fts` (FTS5)

Installed by `searchSchema` in `internal/state/sqlite/search.go`:

```sql
CREATE VIRTUAL TABLE IF NOT EXISTS sessions_fts USING fts5(
    session_id UNINDEXED,
    title,
    body,
    tokenize = 'porter unicode61'
);
```

Three trigger-driven writes keep it consistent with `sessions`:

- `sessions_fts_ai` — after INSERT on `sessions`, mirror the row.
- `sessions_fts_au` — after UPDATE, delete + reinsert.
- `sessions_fts_ad` — after DELETE, drop the FTS row.

**Backfill.** `EnsureSearch` runs a `LEFT JOIN` on every `Open()` to insert any `sessions` rows the FTS index doesn't already have. This makes the index safe to add to an existing database — no manual migration.

**Tokenisation.** `porter unicode61` — Porter stemmer + Unicode-aware casefolding. Case-insensitive, handles English morphology (`retry`/`retries`/`retried`).

**Ranking.** `Search()` orders by `bm25(sessions_fts)` (lower is more relevant). `SearchHit.Rank` exposes it.

**Query syntax.** Passed to FTS5 verbatim. See [Tutorial: Expose tools via MCP](/tutorials/expose-tools-via-mcp/) for the operator cheat sheet.

### Table: `jid_sessions`

Persists platform-sender-to-session-id mappings; installed by `NewJIDMap` in `internal/state/sqlite/jidmap.go`:

```sql
CREATE TABLE IF NOT EXISTS jid_sessions (
    jid         TEXT PRIMARY KEY,
    session_id  TEXT NOT NULL,
    created_at  TEXT NOT NULL
);
```

Every long-running transport uses the JID map so the same phone number, Matrix user, or Slack user picks up the same conversation across restarts. `Router.Handle` (`internal/transport/router.go`) looks it up on inbound; `Put` writes it after `Save`.

The JID space is transport-specific — `447900123456@s.whatsapp.net` for WhatsApp, `@user:matrix.org` for Matrix, `U01ABC…` for Slack. The transport is responsible for canonicalising.

### Table: `cron_jobs`

Installed by `NewCronStore` in `internal/state/sqlite/cron.go`:

```sql
CREATE TABLE IF NOT EXISTS cron_jobs (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    cron_expr   TEXT NOT NULL,
    prompt      TEXT NOT NULL,
    deliver_to  TEXT NOT NULL,
    enabled     INTEGER NOT NULL DEFAULT 1,
    created_at  TEXT NOT NULL,
    last_run_at TEXT
);
```

`UNIQUE(name)` prevents duplicates. `rousseau cron add/list/remove/enable/disable` (from `internal/cli/cron.go`) all round-trip through this table. The scheduler in `internal/cron/scheduler.go` reconciles from it every `poll_interval`. MCP exposes it read-only via `rousseau_cron_list`.

## Concurrency posture

- **WAL** allows unlimited concurrent readers alongside a single writer.
- **`busy_timeout=15000`** means a writer that hits contention waits up to 15 s rather than failing fast. In practice the WhatsApp bridge holds the writer role while `rousseau mcp` and `rousseau session list` are read-only visitors.
- The store is not designed for cross-machine concurrency. Two hosts writing to the same file over NFS is undefined behaviour — use a single writer and rsync the DB elsewhere for read replicas.

## Backing up

The safest approach is a live `sqlite3 .backup`:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db ".backup '/backup/sessions.db.$(date -I).bak'"
```

`.backup` uses SQLite's online backup API and works while the primary is being written to. `restic` / `borg` snapshots on the raw file are also safe because of WAL — the backup gets a consistent snapshot as of the moment the file was read.

The `whatsapp.db` file (whatsmeow device credentials) is a separate database; back it up the same way if you want to avoid re-pairing after a restore.

## Rebuilding the FTS index

If the FTS5 index goes out of sync (extremely rare — the triggers keep it consistent), rebuild it:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions_fts;
INSERT INTO sessions_fts (session_id, title, body)
SELECT id, title, payload FROM sessions;
SQL
```

Rousseau's `EnsureSearch` will not undo this; the triggers just resume from a clean state.

## Related

- [Concepts](/concepts/) — where the store sits in the overall architecture.
- [User Guide: Compression + Recall](/user-guide/compression-recall/) — how the FTS index is exposed to the model.
- [MCP: Exposed tools](/mcp/exposed-tools/) — the read-only surface over this schema.
- [Guides: Managing workspaces](/guides/managing-workspaces/) — sharing / partitioning the store across machines.
