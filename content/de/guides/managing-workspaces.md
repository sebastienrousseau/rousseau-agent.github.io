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
description: "How rousseau's session store partitions by workspace, how to switch workspaces, share sessions across machines, and drop a workspace's history."
keywords: "workspace, session store, state path, sync, rsync, XDG_DATA_HOME"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/guides/managing-workspaces/"
subtitle: "Partition state per project, share history across machines, drop history cleanly."
tags: "guides, workspace, session store, sqlite"
title: "Leitfaden: Arbeitsbereiche verwalten"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "workspace, session store, state path, sync, rsync, XDG_DATA_HOME"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Leitfaden: Arbeitsbereiche verwalten"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 38
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/managing-workspaces/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/managing-workspaces/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Leitfaden: Arbeitsbereiche verwalten"
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
twitter_title: "Leitfaden: Arbeitsbereiche verwalten"
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

## Die Konvention

Rousseau hat kein Erstklass-„Workspace"-Konzept. Es hat einen `state.path` in `internal/config/config.go` (`StateConfig`) und richtet standardmäßig jeden Prozess auf `~/.local/share/rousseau/sessions.db` aus. Alle Sitzungen, Cron-Jobs, JID-Zuordnungen und der FTS5-Recall-Index leben in dieser einzelnen Datei.

Für die meisten Operatoren ist das genau richtig. Wenn Sie Isolation möchten — pro Projekt, pro Maschine, pro Kunde — richten Sie rousseau auf eine andere SQLite-Datei aus. Diese Datei **ist** der Workspace.

## Workspace pro Aufruf wechseln

Zwei Knöpfe, beide funktionieren:

```sh
# 1. flag on any rousseau command
rousseau --config ~/.config/rousseau/acme.yaml chat

# 2. env var (Viper picks it up via ROUSSEAU_STATE_PATH)
ROUSSEAU_STATE_PATH=~/.local/share/rousseau/acme.db rousseau chat
```

Keiner der Ansätze erfordert einen rousseau-Neustart, wenn Sie zwischen Workspaces springen — jeder Prozess öffnet seine eigene Datei.

## Pro-Projekt-Workspace-Layout

```
~/.config/rousseau/
├── acme.yaml         # provider = anthropic, state.path = …/acme.db
├── personal.yaml     # provider = claudecli, state.path = …/personal.db
└── work.yaml         # provider = bedrock,    state.path = …/work.db
```

Jede Konfigurationsdatei überschreibt `state.path`:

```yaml
state:
  path: /home/seb/.local/share/rousseau/acme.db
```

Starten Sie dann jede Sitzung mit der richtigen Konfiguration. Das TUI (`internal/tui/model.go`) zeigt die Session-ID + Provider in seiner Statuszeile — visuelle Bestätigung, dass Sie im richtigen Workspace sind.

## Historie über Maschinen hinweg teilen

Der Session-Store ist eine einzelne SQLite-Datei. WAL-Journaling wird durch `Open()` in `internal/state/sqlite/store.go` aktiviert, sodass Live-Snapshots sicher sind:

```sh
# Snapshot laptop-to-desktop (both idle)
rsync -avz --partial \
  ~/.local/share/rousseau/sessions.db \
  desktop:~/.local/share/rousseau/sessions.db
```

**Nur ein Schreiber gleichzeitig.** Betreiben Sie `rousseau whatsapp` nicht auf zwei Maschinen gegen dieselbe SQLite-Datei über NFS — das ist undefiniert. Synchronisieren Sie, wenn nichts schreibt, oder betreiben Sie einen einzelnen Schreiber mit Read-Replikaten.

Eine sicherere Alternative ist der `.backup`-Snapshot:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db ".backup '/tmp/sessions.snap.db'"
scp /tmp/sessions.snap.db desktop:~/.local/share/rousseau/sessions.db
```

`.backup` verwendet die Online-Backup-API von SQLite und produziert eine konsistente Point-in-Time-Datei.

## Einen Workspace migrieren

Verschieben Sie das ganze Verzeichnis; das ist der Workspace:

```sh
rsync -avz ~/.local/share/rousseau/ new-host:~/.local/share/rousseau/
```

`whatsapp.db` (Gerätedaten) ist separat — Sie bringen sie entweder mit (Gerät bleibt gekoppelt) oder lassen sie zurück und scannen den QR auf dem neuen Host neu.

## Die Historie eines Workspaces verwerfen

```sh
rousseau session list                 # confirm what you're about to lose
rm ~/.local/share/rousseau/acme.db*   # includes -wal and -shm sidecars
```

Der nächste Prozess, der den Pfad öffnet, wird ihn mit dem Schema in `internal/state/sqlite/schema.sql` neu erstellen.

Wenn Sie nur einen Teil der Sitzungen verwerfen möchten, verwenden Sie die CLI:

```sh
rousseau session delete <id> --yes
```

`rousseau session delete` (`internal/cli/session.go`) ruft `Store.Delete` auf, was über die FTS5-Trigger kaskadiert, um den Recall-Index konsistent zu halten. Das `--yes`-Flag ist erforderlich — der Befehl weigert sich, ohne es zu laufen.

## Teilweise Löschung via SQL

Für Massenaufräumen — jede Sitzung, die älter als 90 Tage ist:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions WHERE updated_at < datetime('now', '-90 days');
SQL
```

Die FTS5-Trigger (`sessions_fts_ad` in `internal/state/sqlite/search.go`) feuern beim DELETE und halten den Index automatisch synchron.

## Approver pro Workspace

Weil Konfigurationsdatei und State-Datei beide pro Workspace sind, ist es auch der Approver:

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

Ein separates `personal.yaml` könnte `mode: allow_all` für interaktive Arbeit behalten. Siehe [Tutorial: Approver härten](/de/tutorials/harden-approver-policy/).

## Verwandt

- [Referenz: Session-Store](/de/reference/session-store/) — Schema.
- [Leitfäden: Multi-Provider](/de/guides/multi-provider/) — das Zwei-Konfigurations-, Zwei-Provider-Muster.
- [Referenz: Umgebungsvariablen](/de/reference/environment-variables/) — jede Pfad-Env-Var.
- [Benutzerleitfaden: CLI](/de/user-guide/cli/) — `rousseau session`-Befehle.
