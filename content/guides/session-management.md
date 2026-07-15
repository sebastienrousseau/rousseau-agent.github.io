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
description: "Full session lifecycle: list, search, show, delete, compression triggers, and restoration from the SQLite session store."
keywords: "session, lifecycle, list, search, delete, compression, sqlite"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/guides/session-management/"
subtitle: "List, search, delete, compress, restore."
tags: "guides, session, sqlite, compression"
title: "Guide: Session management"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "session, lifecycle, list, search, delete, compression, sqlite"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide: Session management"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 42
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/session-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/session-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guide: Session management"
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
twitter_description: "Full session lifecycle: list, search, show, delete, compression triggers, and restoration from the SQLite session store."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide: Session management"
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

## Session lifecycle

A session is one `agent.Session` value persisted as a row in the `sessions` table (`internal/state/sqlite/schema.sql`). It has an `id`, a `title`, a chronologically-ordered slice of `Message` values, and timestamps. Once created, it exists until you delete it.

Sessions are created on-demand by every entry point:

- `rousseau chat` — one session per TUI session (a new one on each `chat` invocation; you'd have to build a session-picker to reuse an existing one).
- Every transport (`whatsapp`, `slack`, …) — one session per JID, via the JID map (`internal/state/sqlite/jidmap.go`).
- `rousseau cron` — each fire is a one-shot session bounded to that run.

## Enumerate

```sh
rousseau session list --limit 10
```

Output (from `newSessionListCmd` in `internal/cli/session.go`):

```
<short-id>  <messages>  <updated_at>  <title>
```

`--limit 0` returns unlimited rows.

## Search

FTS5 across every recorded message:

```sh
rousseau session search 'retry logic'
rousseau session search '"exponential backoff" AND anthropic'
rousseau session search 'retr*'                # prefix
```

The command wraps `Store.Search` (`internal/state/sqlite/search.go`) with `SearchOptions{Limit: N}`. Ranking is BM25; snippets are trimmed to ~200 characters.

## Show

```sh
rousseau session show <session-id>
```

Prints the full transcript with `→ tool_use(name, input)` and `← tool_result` markers between assistant messages. Useful for auditing an unattended daemon's session.

## Delete

```sh
rousseau session delete <session-id> --yes
```

The `--yes` flag is required (`newSessionDeleteCmd`). Deletion cascades through the FTS5 triggers so the recall index stays consistent.

## Compression triggers

When `agent.compression.enabled: true` in `config.yaml`, the `LLMCompressor` (`internal/agent/compressor.go`) checks two conditions before each turn:

- `len(s.Messages) >= trigger_messages` (default 60).
- `len(s.Messages) > keep_recent` (default 8).

If both hold, the compressor summarises the oldest slice into one synthetic user message prefixed with the marker `[rousseau-compressed]`, then keeps the last `keep_recent` messages verbatim. The rewritten session replaces the original in memory and is persisted on the next `Store.Save`.

A second compression on an already-compressed session is skipped unless the session has grown to more than `2 * trigger_messages` — this bounds runaway growth without paying to re-summarise every turn.

Log line:

```
INFO agent.compressed messages=68
```

## Restoration

Sessions restore automatically. The transport router (`internal/transport/router.go`) looks up the JID → session id mapping on inbound, then `Store.Load` unmarshals the JSON payload back into an `agent.Session`. No manual step.

If a mapping is stale — session id exists in `jid_sessions` but not in `sessions` — you'll see `router.stale_mapping` (WARN), and the router creates a fresh session. Legacy artefact from a partial delete; safe to ignore.

## Manual restoration from a backup

To roll back the entire session store from a `.backup` snapshot:

```sh
systemctl --user stop rousseau-agent
cp /backup/sessions.db.2026-07-12.bak ~/.local/share/rousseau/sessions.db
rm -f ~/.local/share/rousseau/sessions.db-wal ~/.local/share/rousseau/sessions.db-shm
systemctl --user start rousseau-agent
```

The `-wal` and `-shm` files must be dropped alongside the primary; SQLite reconstructs them on next open.

## Bulk deletion by age

There is no built-in "delete sessions older than X" CLI. Drop through SQLite:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions WHERE updated_at < datetime('now', '-90 days');
SQL
```

FTS5 triggers keep the recall index consistent.

## Preserving privacy

Since session content is stored plaintext in a JSON blob, treat `sessions.db` as sensitive. Options:

- **Filesystem-level encryption.** LUKS on Linux, FileVault on macOS.
- **Encrypted backups.** `restic` and `borg` both encrypt at rest.
- **Delete-on-completion for one-shot sessions.** For cron-driven daemons, a post-run hook could `rousseau session delete` the just-completed session id. Not built-in today; see [Guides: Enterprise Onboarding](/guides/enterprise-onboarding/) for the review.

## Full `rousseau session` command reference

<div class="tabs" data-tabs="session-commands">
  <div class="tab-list" role="tablist" aria-label="Session subcommand">
    <button role="tab" aria-selected="true">list</button>
    <button role="tab" aria-selected="false">show</button>
    <button role="tab" aria-selected="false">search</button>
    <button role="tab" aria-selected="false">delete</button>
    <button role="tab" aria-selected="false">export</button>
  </div>
  <div class="tab-panel" role="tabpanel">

List sessions, newest first:

```sh
rousseau session list
rousseau session list --limit 100
rousseau session list --json
```

Columns: `ID`, `Title`, `Messages`, `UpdatedAt`. The `--json` flag emits one object per line for scripted consumers.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Print a session's full transcript:

```sh
rousseau session show <session-id>
rousseau session show <session-id> --raw
```

`--raw` prints the JSON as stored (useful for debugging). Without `--raw`, tool calls render as `→ tool_use(name, input)` and results as `← tool_result`.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Full-text search across every session:

```sh
rousseau session search "refactor login"
rousseau session search "TODO" --limit 10
```

Uses the FTS5 index (see `internal/state/sqlite/`). Results are ranked by relevance and include a snippet with the matched terms highlighted.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Delete a session and its FTS5 entries:

```sh
rousseau session delete <session-id> --yes
```

The `--yes` flag is required — no interactive confirmation. Deletion cascades via SQL triggers so the recall index stays consistent.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Export a session as JSON:

```sh
rousseau session export <session-id> > session.json
```

The exported format matches the on-disk JSON blob; re-import is not yet supported (roadmap).

  </div>
</div>

## Troubleshooting

### `session not found`

The ID you passed does not exist. Case-sensitive. Use `rousseau session list` to see valid IDs.

### FTS5 search returns nothing

The index might be out of date on legacy sessions imported before FTS5 was wired. Rebuild by running any content-mutating operation (a delete triggers reindex), or reindex manually via SQLite.

### `database is locked` on read

Another daemon is holding a WAL write lock. Use a read-only DSN (`?mode=ro`) if you only need to read.

### Session store growing too fast

Enable compression (`agent.compression.enabled: true`) and periodically `VACUUM` the SQLite file to reclaim space.

### Restore from backup produces stale state

Ensure you dropped `-wal` and `-shm` before starting the daemon. SQLite will replay the WAL if `-wal` is present, potentially undoing your restore.

## Related pages

- [Reference: Session store](/reference/session-store/) — schema and DDL.
- [Guides: Managing workspaces](/guides/managing-workspaces/) — per-workspace stores.
- [Guides: Context management](/guides/context-management/) — how compression decides what to keep.
- [User Guide: CLI](/user-guide/cli/) — command signatures.
- [User Guide: Compression &amp; Recall](/user-guide/compression-recall/) — internals of the compressor and FTS5 recall.

## Further reading

- `internal/cli/session.go` — CLI wiring.
- `internal/state/sqlite/store.go` — DSN, WAL, indexes.
- `internal/agent/session.go` — the `Session` struct.
- `internal/agent/compressor.go` — `LLMCompressor`.
- `internal/agent/recall.go` — `SQLiteRecall`.
