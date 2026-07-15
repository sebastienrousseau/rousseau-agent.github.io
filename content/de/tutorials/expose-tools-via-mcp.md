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
description: "Expose rousseau's session store and cron jobs to Claude Desktop as an MCP server that Claude can drive from its own tool interface."
keywords: "mcp, claude desktop, stdio, tools, rousseau_search_sessions, rousseau_read_session"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/tutorials/expose-tools-via-mcp/"
subtitle: "Wire rousseau mcp into Claude Desktop and let it query the session store."
tags: "tutorials, mcp, claude-desktop, stdio, sessions"
title: "Tutorial: Werkzeuge über MCP bereitstellen"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, claude desktop, stdio, tools, rousseau_search_sessions, rousseau_read_session"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorial: Werkzeuge über MCP bereitstellen"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/expose-tools-via-mcp/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/expose-tools-via-mcp/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorial: Werkzeuge über MCP bereitstellen"
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
twitter_description: "Expose rousseau's session store and cron jobs to Claude Desktop as an MCP server that Claude can drive from its own tool interface."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorial: Werkzeuge über MCP bereitstellen"
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

## Was Sie bauen

Claude Desktop mit rousseau als MCP-stdio-Server. Aus einem Claude-Desktop-Chat heraus können Sie „finde die Sitzung, in der wir die Retry-Logik besprochen haben" fragen, und Claude wird `rousseau_search_sessions` aufrufen, dann `rousseau_read_session`, um das vollständige Transkript zu holen.

Geschätzte Zeit: 5 Minuten.

## Voraussetzungen

- Claude Desktop installiert (macOS oder Windows). Linux verwendet die Claude-CLI, nicht Desktop — siehe die Alternative am Ende.
- Rousseau installiert und in `$PATH`.
- Etwas vorhandene Sitzungshistorie in `~/.local/share/rousseau/sessions.db` — führen Sie `rousseau chat` einige Male aus, wenn die Datei leer ist.

## Schritt 1: verstehen, was exponiert wird

`rousseau mcp` (`internal/cli/mcp.go`) startet einen stdio-JSON-RPC-Server, der das Model Context Protocol spricht. `RegisterRousseauTools` (`internal/mcp/tools.go`) hängt vier Read-only-Tools an:

| Tool | Zweck |
|---|---|
| `rousseau_search_sessions` | FTS5-Volltextsuche über jede aufgezeichnete Sitzung (via `internal/state/sqlite/search.go`). |
| `rousseau_list_sessions` | Sitzungen auflisten, neueste zuerst. |
| `rousseau_read_session` | Das vollständige Transkript einer Sitzung nach ID zurückgeben. |
| `rousseau_cron_list` | Die geplanten Cron-Jobs von rousseau auflisten. |

Es gibt keine Schreib-Tools; MCP-Hosts können browsen, aber nichts mutieren. Siehe [MCP: Exponierte Tools](/de/mcp/exposed-tools/) für die genauen Input-Schemata.

## Schritt 2: Claude Desktop verdrahten

Claude Desktop liest `claude_desktop_config.json`:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Fügen Sie einen `mcpServers`-Eintrag hinzu, der auf Ihr `rousseau`-Binary zeigt:

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

Starten Sie Claude Desktop neu.

## Schritt 3: verifizieren

Öffnen Sie einen Claude-Desktop-Chat und prüfen Sie, dass die Tools im Tool-Picker erscheinen. Sie sollten vier Tools mit dem Präfix `rousseau_` sehen. Versuchen Sie:

```
Use rousseau_list_sessions to show me my 5 most recent sessions,
then read the top one with rousseau_read_session.
```

Claude ruft beide Tools auf, und der MCP-Server von rousseau (`internal/mcp/server.go`) behandelt jeden JSON-RPC-Umschlag über stdin/stdout. Hinter den Kulissen:

1. Claude Desktop ruft `initialize`, dann `tools/list` auf — rousseau antwortet mit den vier Tools in Einfügungsreihenfolge.
2. Claude wählt ein Tool und ruft `tools/call` mit den Argumenten auf — der Handler von rousseau (aus `internal/mcp/tools.go`) queryt SQLite und gibt Text-Content zurück.
3. Bei Fehler zeigt rousseau den Fehler über den Content-Kanal (`isError=true`), nie als JSON-RPC-Fehler — MCP-Hosts erwarten das.

## Schritt 4: (optional) an die Claude-CLI / einen anderen MCP-Host anhängen

Das stdio-Protokoll ist host-agnostisch. Für die Claude-CLI:

```sh
claude --mcp-config <(cat <<'JSON'
{ "mcpServers": { "rousseau": { "command": "rousseau", "args": ["mcp"] } } }
JSON
)
```

Für Continue.dev, Codeium oder einen anderen MCP-Host folgen Sie deren MCP-Server-Registrierungsablauf mit `command: rousseau`, `args: [mcp]`. Siehe [MCP: Kompatibilität](/de/mcp/compatibility/) für die getesteten Clients.

## Schritt 5: FTS5-Syntax-Spickzettel

Da rousseau_search_sessions ein dünner Wrapper um SQLite FTS5 (`internal/state/sqlite/search.go`) ist, unterstützt das Query-Feld:

| Query | Bedeutung |
|---|---|
| `retry logic` | Jedes Dokument, das beide Terme enthält. |
| `"retry logic"` | Exakte Phrase. |
| `retr*` | Präfix-Match. |
| `retry OR backoff` | Boolesches OR. |
| `retry NOT retries` | Ausschluss. |

Ranking verwendet BM25 (niedriger Rang = relevanter); der `snippet()`-Aufruf in `Search` gibt Ihnen eine 200-Zeichen-Vorschau pro Treffer.

## Fehlerbehebung

- **„unknown tool" in Claude Desktop.** Starten Sie die App neu. Die Tool-Liste wird nur beim Sitzungsstart abgerufen.
- **Server beendet sich sofort.** `rousseau mcp` öffnet die SQLite-Statusdatei; wenn der Pfad in `state.path` nicht beschreibbar ist, schlägt `Open()` fehl und der Prozess beendet sich mit einem Nicht-Null-Code. Führen Sie es aus einer Shell aus, um den Fehler zu sehen.
- **Leere Suchergebnisse.** Bestätigen Sie, dass der FTS5-Index gefüllt ist: `sqlite3 ~/.local/share/rousseau/sessions.db "SELECT count(*) FROM sessions_fts"`. `EnsureSearch` in `internal/state/sqlite/search.go` füllt den Index bei jedem Öffnen nach, aber eine korrupte Statusdatei benötigt möglicherweise einen manuellen Neuaufbau.

## Verwandt

- [MCP](/de/mcp/) — das Referenzdokument.
- [MCP: Exponierte Tools](/de/mcp/exposed-tools/) — jedes Tool-Schema.
- [MCP: Kompatibilität](/de/mcp/compatibility/) — getestete Clients.
- [Referenz: Session-Store](/de/reference/session-store/) — das SQLite-Schema hinter den Tools.
