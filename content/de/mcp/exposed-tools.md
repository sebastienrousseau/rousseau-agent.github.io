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
description: "The exact tool signatures exposed by rousseau's stdio MCP server, mirroring internal/mcp/tools.go."
keywords: "mcp, rousseau_search_sessions, rousseau_list_sessions, rousseau_read_session, rousseau_cron_list"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/mcp/exposed-tools/"
subtitle: "Every tool rousseau's MCP server advertises, with schemas."
tags: "mcp, tools, sessions, cron"
title: "MCP: bereitgestellte Werkzeuge"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, rousseau_search_sessions, rousseau_list_sessions, rousseau_read_session, rousseau_cron_list"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP: bereitgestellte Werkzeuge"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "mcp"
order: 72
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/mcp/exposed-tools/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/exposed-tools/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "MCP: bereitgestellte Werkzeuge"
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
twitter_description: "The exact tool signatures exposed by rousseau's stdio MCP server, mirroring internal/mcp/tools.go."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP: bereitgestellte Werkzeuge"
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

## Registrierung

`internal/cli/mcp.go` öffnet den SQLite-Sitzungsspeicher, konstruiert einen `NewCronStore`, wickelt beide in `mcp.NewStoreBackend` ein und ruft `mcp.RegisterRousseauTools(s, backend)` auf. Die vier untenstehenden Tools werden in Einfügereihenfolge angehängt – `tools/list` liefert sie in genau dieser Reihenfolge zurück.

Jedes Tool ist schreibgeschützt. Es gibt heute keine Schreiboberfläche über MCP; das ist beabsichtigt, damit ein MCP-Host rousseaus Zustand nicht mutieren kann.

## `rousseau_search_sessions`

**Beschreibung (für Hosts sichtbar):** _Full-text search across every recorded rousseau session. Uses SQLite FTS5 syntax (phrases in double quotes, AND/OR/NOT, prefix wildcards)._

**Eingabeschema:**

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "FTS5 query"
    },
    "limit": {
      "type": "integer",
      "description": "Cap hits returned. Default 20."
    }
  },
  "required": ["query"]
}
```

**Verhalten.** Übergibt `query` wortwörtlich an SQLites FTS5-Engine (`Store.Search` in `internal/state/sqlite/search.go`). Ergebnisse werden nach BM25-Rang geordnet (niedriger = relevanter). Jeder Treffer wird als drei Zeilen dargestellt:

```
session <id> (rank 0.42)
    title:   <session title>
    snippet: <~200-char snippet with … ellipses>
```

**Fehler.** Eine leere Abfrage liefert `query is required` zurück. FTS5-Syntaxfehler steigen als SQLite-Fehler auf und werden über `isError: true` sichtbar.

## `rousseau_list_sessions`

**Beschreibung (für Hosts sichtbar):** _List rousseau sessions newest-first._

**Eingabeschema:**

```json
{
  "type": "object",
  "properties": {
    "limit": {
      "type": "integer",
      "description": "Cap rows returned. Default 20."
    }
  }
}
```

**Verhalten.** Ruft `Store.List` auf, das den Index `idx_sessions_updated_at DESC` verwendet. Jede Zeile:

```
<session-id>  <title>  msgs=<count>  updated=<iso-8601>
```

Liefert `(no sessions)` zurück, wenn der Speicher leer ist.

## `rousseau_read_session`

**Beschreibung (für Hosts sichtbar):** _Return the full transcript of a rousseau session by id._

**Eingabeschema:**

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "description": "Session id"
    }
  },
  "required": ["id"]
}
```

**Verhalten.** Ruft `Store.Load` auf, um die vollständige `agent.Session` abzurufen. Wird dargestellt als:

```
id: <session-id>
title: <session title>
created: <iso-8601>
updated: <iso-8601>
messages: <count>

[0] user
    <text content>
[1] assistant
    <text content>
    ...
```

Nur Textinhalte werden dargestellt – `tool_use`-Blöcke und `tool_result`-Blöcke werden in der MCP-Oberfläche ausgelassen (die CLI `rousseau session show` schließt sie ein; MCP absichtlich nicht).

**Fehler.** `id is required` bei leerer Eingabe. `state.ErrNotFound` bei unbekannter ID.

## `rousseau_cron_list`

**Beschreibung (für Hosts sichtbar):** _List rousseau's scheduled cron jobs (name, schedule, prompt, delivery target)._

**Eingabeschema:**

```json
{
  "type": "object",
  "properties": {}
}
```

**Verhalten.** Ruft `CronStore.List` auf – eine Zeile pro `cron_jobs`-Zeile:

```
<name> [<on|off>] <cron-expr> → <deliver-to>  prompt="<prompt>"  deliver=<deliver-to>
```

Liefert `(no jobs)` zurück, wenn die Cron-Tabelle leer ist. Liefert auch `(no jobs)` zurück, wenn der `CronStore` zum Konstruktionszeitpunkt nil ist (ein defensiver Pfad in `storeBackend.CronList`).

## Was NICHT exponiert wird

Bewusste Auslassungen:

| Oberfläche | Warum nicht |
|---|---|
| `rousseau_write_session` / `rousseau_delete_session` | Mutation über MCP würde einem nicht vertrauenswürdigen Host erlauben, rousseaus Audit-Trail umzuformen. |
| `rousseau_add_cron` | Gleicher Grund – Mutation. Fügen Sie Cron-Jobs über `rousseau cron add` hinzu. |
| Die eingebauten Tools (`read`, `write`, `edit`, `grep`, `bash`) | Diese sind agent-seitige Tools für das LLM innerhalb rousseaus eigener Schleife, nicht host-seitig. Sie zu exponieren würde dem MCP-Host die Fähigkeit geben, auf dem Host, der rousseau ausführt, eine Shell zu öffnen – genau der Vertrauensumkehr, den wir nicht wollen. |
| JID-Map-Suche | Exponiert PII (Telefonnummern). Wenn Sie sie benötigen, fragen Sie SQLite direkt auf der Maschine ab, auf der der Daemon läuft. |

## Fehleroberfläche

MCP-Handler liefern `([]Content, error)` zurück. Bei Fehlern macht der Server (`internal/mcp/server.go` `handleToolsCall`) den Fehler als `ToolsCallResult{Content: Text des Fehlers, IsError: true}` sichtbar. Dies entspricht der MCP-Konvention: Tool-Fehler fließen durch den Content-Kanal mit `isError=true`, nicht durch den JSON-RPC-`error`-Kanal. Hosts sollten den Text darstellen und fortfahren.

## Verwandt

- [MCP](/de/mcp/) — die Dachreferenz.
- [MCP: Kompatibilität](/de/mcp/compatibility/) — getestete Clients.
- [MCP: Exponierte Ressourcen](/de/mcp/exposed-resources/) — Roadmap.
- [Referenz: Tool-Schemas](/de/reference/tool-schemas/) — die andere, agent-seitige Tool-Menge.
