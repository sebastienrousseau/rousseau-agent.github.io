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
description: "Full session lifecycle: list, search, show, delete, compression triggers, and restoration from the SQLite session store."
keywords: "session, lifecycle, list, search, delete, compression, sqlite"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/guides/session-management/"
subtitle: "List, search, delete, compress, restore."
tags: "guides, session, sqlite, compression"
title: "Leitfaden: Sitzungsverwaltung"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "session, lifecycle, list, search, delete, compression, sqlite"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Leitfaden: Sitzungsverwaltung"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 42
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/session-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/session-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Leitfaden: Sitzungsverwaltung"
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
twitter_title: "Leitfaden: Sitzungsverwaltung"
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

## Sitzungs-Lebenszyklus

Eine Sitzung ist ein `agent.Session`-Wert, der als Zeile in der `sessions`-Tabelle (`internal/state/sqlite/schema.sql`) persistiert wird. Sie hat eine `id`, einen `title`, eine chronologisch geordnete Sequenz von `Message`-Werten und Zeitstempel. Einmal erstellt, existiert sie, bis Sie sie löschen.

Sitzungen werden von jedem Einstiegspunkt bei Bedarf erstellt:

- `rousseau chat` — eine Sitzung pro TUI-Sitzung (bei jedem `chat`-Aufruf eine neue; um eine bestehende wiederzuverwenden, müssten Sie einen Session-Picker bauen).
- Jeder Transport (`whatsapp`, `slack`, …) — eine Sitzung pro JID, über die JID-Map (`internal/state/sqlite/jidmap.go`).
- `rousseau cron` — jedes Feuern ist eine One-Shot-Sitzung, begrenzt auf diesen Lauf.

## Aufzählen

```sh
rousseau session list --limit 10
```

Ausgabe (aus `newSessionListCmd` in `internal/cli/session.go`):

```
<short-id>  <messages>  <updated_at>  <title>
```

`--limit 0` liefert unbegrenzt Zeilen.

## Suchen

FTS5 über jede aufgezeichnete Nachricht:

```sh
rousseau session search 'retry logic'
rousseau session search '"exponential backoff" AND anthropic'
rousseau session search 'retr*'                # prefix
```

Der Befehl umhüllt `Store.Search` (`internal/state/sqlite/search.go`) mit `SearchOptions{Limit: N}`. Ranking ist BM25; Snippets werden auf ~200 Zeichen gekürzt.

## Anzeigen

```sh
rousseau session show <session-id>
```

Gibt das vollständige Transkript mit `→ tool_use(name, input)`- und `← tool_result`-Markern zwischen Assistenten-Nachrichten aus. Nützlich zum Auditieren der Sitzung eines unbeaufsichtigten Daemons.

## Löschen

```sh
rousseau session delete <session-id> --yes
```

Das `--yes`-Flag ist erforderlich (`newSessionDeleteCmd`). Löschung kaskadiert über die FTS5-Trigger, sodass der Recall-Index konsistent bleibt.

## Komprimierungs-Auslöser

Wenn `agent.compression.enabled: true` in `config.yaml` gesetzt ist, prüft der `LLMCompressor` (`internal/agent/compressor.go`) vor jedem Turn zwei Bedingungen:

- `len(s.Messages) >= trigger_messages` (Standard 60).
- `len(s.Messages) > keep_recent` (Standard 8).

Wenn beide zutreffen, fasst der Compressor den ältesten Ausschnitt in eine synthetische Nutzernachricht zusammen, präfixiert mit dem Marker `[rousseau-compressed]`, und behält dann die letzten `keep_recent` Nachrichten wörtlich. Die umgeschriebene Sitzung ersetzt das Original im Speicher und wird beim nächsten `Store.Save` persistiert.

Eine zweite Komprimierung einer bereits komprimierten Sitzung wird übersprungen, es sei denn, die Sitzung ist über `2 * trigger_messages` gewachsen — dies begrenzt unkontrolliertes Wachstum, ohne für die Neuzusammenfassung jedes Turns zu bezahlen.

Log-Zeile:

```
INFO agent.compressed messages=68
```

## Wiederherstellung

Sitzungen werden automatisch wiederhergestellt. Der Transport-Router (`internal/transport/router.go`) schlägt beim eingehenden Verkehr die JID-→-Session-ID-Zuordnung nach, dann unmarshalt `Store.Load` die JSON-Payload zurück in eine `agent.Session`. Kein manueller Schritt.

Wenn eine Zuordnung veraltet ist — Session-ID existiert in `jid_sessions`, aber nicht in `sessions` — sehen Sie `router.stale_mapping` (WARN), und der Router erstellt eine frische Sitzung. Legacy-Artefakt aus einem Teillöschen; kann ignoriert werden.

## Manuelle Wiederherstellung aus einem Backup

Um den gesamten Session-Store aus einem `.backup`-Snapshot zurückzurollen:

```sh
systemctl --user stop rousseau-agent
cp /backup/sessions.db.2026-07-12.bak ~/.local/share/rousseau/sessions.db
rm -f ~/.local/share/rousseau/sessions.db-wal ~/.local/share/rousseau/sessions.db-shm
systemctl --user start rousseau-agent
```

Die `-wal`- und `-shm`-Dateien müssen zusammen mit der Hauptdatei entfernt werden; SQLite rekonstruiert sie beim nächsten Öffnen.

## Massenlöschung nach Alter

Es gibt keine eingebaute „Sitzungen älter als X löschen"-CLI. Direkt via SQLite:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions WHERE updated_at < datetime('now', '-90 days');
SQL
```

FTS5-Trigger halten den Recall-Index konsistent.

## Datenschutz bewahren

Da Sitzungsinhalte als Klartext in einem JSON-Blob gespeichert sind, behandeln Sie `sessions.db` als sensibel. Optionen:

- **Verschlüsselung auf Dateisystem-Ebene.** LUKS unter Linux, FileVault unter macOS.
- **Verschlüsselte Backups.** `restic` und `borg` verschlüsseln beide at rest.
- **Delete-on-completion für One-Shot-Sitzungen.** Für Cron-gesteuerte Daemons könnte ein Post-Run-Hook die soeben abgeschlossene Session-ID `rousseau session delete`n. Heute nicht eingebaut; siehe [Leitfäden: Enterprise-Onboarding](/de/guides/enterprise-onboarding/) für die Prüfung.

## Vollständige `rousseau session`-Befehlsreferenz

<div class="tabs" data-tabs="session-commands">
  <div class="tab-list" role="tablist" aria-label="Session subcommand">
    <button role="tab" aria-selected="true">list</button>
    <button role="tab" aria-selected="false">show</button>
    <button role="tab" aria-selected="false">search</button>
    <button role="tab" aria-selected="false">delete</button>
    <button role="tab" aria-selected="false">export</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Sitzungen auflisten, neueste zuerst:

```sh
rousseau session list
rousseau session list --limit 100
rousseau session list --json
```

Spalten: `ID`, `Title`, `Messages`, `UpdatedAt`. Das `--json`-Flag emittiert ein Objekt pro Zeile für skriptbare Konsumenten.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Vollständiges Transkript einer Sitzung ausgeben:

```sh
rousseau session show <session-id>
rousseau session show <session-id> --raw
```

`--raw` gibt das JSON wie gespeichert aus (nützlich zum Debuggen). Ohne `--raw` werden Tool-Aufrufe als `→ tool_use(name, input)` und Ergebnisse als `← tool_result` gerendert.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Volltextsuche über jede Sitzung:

```sh
rousseau session search "refactor login"
rousseau session search "TODO" --limit 10
```

Verwendet den FTS5-Index (siehe `internal/state/sqlite/`). Ergebnisse werden nach Relevanz gerankt und enthalten ein Snippet mit hervorgehobenen Treffertermini.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Eine Sitzung und ihre FTS5-Einträge löschen:

```sh
rousseau session delete <session-id> --yes
```

Das `--yes`-Flag ist erforderlich — keine interaktive Bestätigung. Löschung kaskadiert über SQL-Trigger, sodass der Recall-Index konsistent bleibt.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Eine Sitzung als JSON exportieren:

```sh
rousseau session export <session-id> > session.json
```

Das Exportformat entspricht dem On-Disk-JSON-Blob; ein Re-Import wird noch nicht unterstützt (Roadmap).

  </div>
</div>

## Fehlerbehebung

### `session not found`

Die übergebene ID existiert nicht. Groß-/Kleinschreibung beachten. Nutzen Sie `rousseau session list`, um gültige IDs zu sehen.

### FTS5-Suche liefert nichts

Der Index könnte bei Legacy-Sitzungen, die vor der Verdrahtung von FTS5 importiert wurden, veraltet sein. Neu aufbauen, indem Sie eine inhaltsmutierende Operation ausführen (ein Delete löst Reindex aus), oder manuell via SQLite reindizieren.

### `database is locked` beim Lesen

Ein anderer Daemon hält eine WAL-Schreibsperre. Verwenden Sie eine Read-only-DSN (`?mode=ro`), wenn Sie nur lesen müssen.

### Session-Store wächst zu schnell

Aktivieren Sie Komprimierung (`agent.compression.enabled: true`) und `VACUUM`en Sie die SQLite-Datei periodisch, um Platz zurückzugewinnen.

### Wiederherstellung aus Backup erzeugt veralteten Zustand

Stellen Sie sicher, dass Sie `-wal` und `-shm` vor dem Start des Daemons entfernt haben. SQLite wird das WAL wiederabspielen, wenn `-wal` vorhanden ist, und potenziell Ihre Wiederherstellung rückgängig machen.

## Verwandte Seiten

- [Referenz: Session-Store](/de/reference/session-store/) — Schema und DDL.
- [Leitfäden: Workspaces verwalten](/de/guides/managing-workspaces/) — Per-Workspace-Stores.
- [Leitfäden: Kontext-Management](/de/guides/context-management/) — wie Komprimierung entscheidet, was behalten wird.
- [Benutzerleitfaden: CLI](/de/user-guide/cli/) — Befehlssignaturen.
- [Benutzerleitfaden: Komprimierung &amp; Recall](/de/user-guide/compression-recall/) — Interna des Compressors und der FTS5-Recall.

## Weiterführende Lektüre

- `internal/cli/session.go` — CLI-Verdrahtung.
- `internal/state/sqlite/store.go` — DSN, WAL, Indizes.
- `internal/agent/session.go` — die `Session`-Struktur.
- `internal/agent/compressor.go` — `LLMCompressor`.
- `internal/agent/recall.go` — `SQLiteRecall`.
