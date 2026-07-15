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
hreflang: "de"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "de"
locale: "de_DE"
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
permalink: "https://docs.rousseau-agent.dev/de/reference/session-store/"
subtitle: "The SQLite schema at the heart of rousseau's state."
tags: "reference, sqlite, fts5, session, wal"
title: "Referenz: Session-Store"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "sqlite, fts5, session store, sessions, jid, cron, WAL, schema"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Referenz: Session-Store"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 53
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/session-store/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/session-store/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Referenz: Session-Store"
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
twitter_title: "Referenz: Session-Store"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Danke an jeden Operator, der seinen eigenen Coding-Agenten betreibt."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Ort und Treiber

Der Session-Store ist eine einzelne SQLite-Datenbank unter `state.path` (Standard `~/.local/share/rousseau/sessions.db`, siehe `internal/config/config.go` `setDefaults`).

Rousseau verwendet `modernc.org/sqlite` — einen reinen Go-SQLite-Treiber. Es gibt **keine CGO- oder libsqlite3-Abhängigkeit**. Das Go-Binary in `bin/rousseau` ist vollständig statisch.

`internal/state/sqlite/store.go` `Open()` wendet bei jedem Öffnen vier Pragmas an:

| PRAGMA | Zweck |
|---|---|
| `journal_mode=WAL` | Write-Ahead-Logging. Ermöglicht gleichzeitige Leser, sichere Live-Backups. |
| `foreign_keys=ON` | Standard-Integritätsgarantie. |
| `busy_timeout=15000` | 15-Sekunden-Wartezeit bei Sperren-Contention — kritisch, sobald mehrere Transporte gleichzeitig schreiben. |
| — | `EnsureSearch` läuft anschließend, um das FTS5-Schema zu installieren. |

Der Store wird einmal pro Prozess geöffnet. Mehrere Daemons, die auf dieselbe DB-Datei zeigen, werden dank der busy-timeout + WAL-Kombination unterstützt — die WhatsApp-Bridge, `rousseau mcp` und `rousseau session list` können die Datei sicher teilen.

## Schema-Rundgang

### Tabelle: `sessions`

Definiert in `internal/state/sqlite/schema.sql`:

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

**Payload-Form.** Die `payload`-Spalte speichert das vollständige `agent.Session`-JSON — Rollen, Content-Blöcke, Tool-Use- und Tool-Result-Blöcke, Zeitstempel. Siehe `Save`/`Load` in `internal/state/sqlite/store.go`. Die gesamte Sitzung als ein JSON-Blob zu halten, hält Schema-Migrationen selten; Abfragen gegen Interna laufen durch den FTS5-Index unten.

**Zeitstempel** sind ISO-8601 mit Millisekunden-Präzision (`2006-01-02T15:04:05.000Z` in Go-Time-Syntax), UTC.

**Ordering.** `idx_sessions_updated_at` treibt `List` und `RecentSessions` an (beide in `store.go` / `search.go`).

### Virtuelle Tabelle: `sessions_fts` (FTS5)

Installiert von `searchSchema` in `internal/state/sqlite/search.go`:

```sql
CREATE VIRTUAL TABLE IF NOT EXISTS sessions_fts USING fts5(
    session_id UNINDEXED,
    title,
    body,
    tokenize = 'porter unicode61'
);
```

Drei triggergesteuerte Schreibvorgänge halten sie mit `sessions` konsistent:

- `sessions_fts_ai` — nach INSERT auf `sessions`, spiegelt die Zeile.
- `sessions_fts_au` — nach UPDATE, löschen + neu einfügen.
- `sessions_fts_ad` — nach DELETE, FTS-Zeile entfernen.

**Backfill.** `EnsureSearch` führt bei jedem `Open()` einen `LEFT JOIN` aus, um jede `sessions`-Zeile einzufügen, die der FTS-Index noch nicht hat. Das macht den Index sicher zu einer bestehenden Datenbank hinzufügbar — keine manuelle Migration.

**Tokenisierung.** `porter unicode61` — Porter-Stemmer + Unicode-fähiges Casefolding. Case-insensitiv, handhabt englische Morphologie (`retry`/`retries`/`retried`).

**Ranking.** `Search()` ordnet nach `bm25(sessions_fts)` (niedriger = relevanter). `SearchHit.Rank` exponiert es.

**Query-Syntax.** Wird wortwörtlich an FTS5 übergeben. Siehe [Tutorial: Tools via MCP exponieren](/de/tutorials/expose-tools-via-mcp/) für den Operator-Spickzettel.

### Tabelle: `jid_sessions`

Persistiert Plattform-Absender-zu-Session-ID-Zuordnungen; installiert von `NewJIDMap` in `internal/state/sqlite/jidmap.go`:

```sql
CREATE TABLE IF NOT EXISTS jid_sessions (
    jid         TEXT PRIMARY KEY,
    session_id  TEXT NOT NULL,
    created_at  TEXT NOT NULL
);
```

Jeder langlaufende Transport verwendet die JID-Map, damit dieselbe Telefonnummer, derselbe Matrix-Nutzer oder Slack-Nutzer über Neustarts hinweg dieselbe Konversation aufnimmt. `Router.Handle` (`internal/transport/router.go`) schlägt sie beim Inbound nach; `Put` schreibt sie nach `Save`.

Der JID-Raum ist transportspezifisch — `447900123456@s.whatsapp.net` für WhatsApp, `@user:matrix.org` für Matrix, `U01ABC…` für Slack. Der Transport ist für die Kanonisierung verantwortlich.

### Tabelle: `cron_jobs`

Installiert von `NewCronStore` in `internal/state/sqlite/cron.go`:

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

`UNIQUE(name)` verhindert Duplikate. `rousseau cron add/list/remove/enable/disable` (aus `internal/cli/cron.go`) laufen alle durch diese Tabelle. Der Scheduler in `internal/cron/scheduler.go` gleicht daraus alle `poll_interval` ab. MCP exponiert sie read-only via `rousseau_cron_list`.

## Concurrency-Haltung

- **WAL** erlaubt unbegrenzt gleichzeitige Leser neben einem einzelnen Schreiber.
- **`busy_timeout=15000`** bedeutet, dass ein Schreiber, der auf Contention trifft, bis zu 15 s wartet, statt schnell zu scheitern. In der Praxis hält die WhatsApp-Bridge die Schreiber-Rolle, während `rousseau mcp` und `rousseau session list` read-only-Besucher sind.
- Der Store ist nicht für Cross-Maschinen-Concurrency ausgelegt. Zwei Hosts, die über NFS in dieselbe Datei schreiben, ist undefiniertes Verhalten — verwenden Sie einen einzelnen Schreiber und rsync-en Sie die DB anderswohin für Read-Replikate.

## Sichern

Der sicherste Ansatz ist ein Live-`sqlite3 .backup`:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db ".backup '/backup/sessions.db.$(date -I).bak'"
```

`.backup` verwendet die Online-Backup-API von SQLite und funktioniert, während in die Primärdatei geschrieben wird. `restic`- / `borg`-Snapshots auf der Rohdatei sind wegen WAL ebenfalls sicher — das Backup erhält einen konsistenten Snapshot zum Zeitpunkt, an dem die Datei gelesen wurde.

Die `whatsapp.db`-Datei (whatsmeow-Gerätedaten) ist eine separate Datenbank; sichern Sie sie auf dieselbe Weise, wenn Sie ein erneutes Pairing nach einer Wiederherstellung vermeiden möchten.

## Den FTS-Index neu aufbauen

Wenn der FTS5-Index aus der Synchronisation gerät (extrem selten — die Trigger halten ihn konsistent), bauen Sie ihn neu:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions_fts;
INSERT INTO sessions_fts (session_id, title, body)
SELECT id, title, payload FROM sessions;
SQL
```

`EnsureSearch` von rousseau wird dies nicht rückgängig machen; die Trigger setzen einfach von einem sauberen Zustand aus fort.

## Verwandt

- [Konzepte](/de/concepts/) — wo der Store in der Gesamtarchitektur sitzt.
- [Benutzerleitfaden: Komprimierung + Recall](/de/user-guide/compression-recall/) — wie der FTS-Index dem Modell exponiert wird.
- [MCP: Exponierte Tools](/de/mcp/exposed-tools/) — die Read-only-Oberfläche über diesem Schema.
- [Leitfäden: Workspaces verwalten](/de/guides/managing-workspaces/) — den Store über Maschinen teilen / partitionieren.
