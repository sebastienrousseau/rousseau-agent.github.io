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
description: "MCP clients tested against rousseau's stdio server: Claude Desktop, Claude CLI, Continue, Codeium, plus setup snippets."
keywords: "mcp, compatibility, claude desktop, continue, codeium, stdio, claude_desktop_config"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/mcp/compatibility/"
subtitle: "Which MCP clients talk to rousseau's stdio server."
tags: "mcp, compatibility, claude, continue, stdio"
title: "MCP: Kompatibilität"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, compatibility, claude desktop, continue, codeium, stdio, claude_desktop_config"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP: Kompatibilität"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "mcp"
order: 71
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/mcp/compatibility/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/compatibility/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "MCP: Kompatibilität"
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
twitter_description: "MCP clients tested against rousseau's stdio server: Claude Desktop, Claude CLI, Continue, Codeium, plus setup snippets."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP: Kompatibilität"
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

## Der Protokollvertrag

Rousseaus MCP-Server (`internal/mcp/server.go`) spricht JSON-RPC 2.0 über stdio und kündigt die in `internal/mcp/tools.go` deklarierten Tools an. Er behandelt diese Methoden:

- `initialize` — liefert `ServerCapabilities.Tools` zurück.
- `initialized` — Benachrichtigung, keine Antwort.
- `ping` — liefert `{}` zurück.
- `tools/list` — liefert die vier Tools in Einfügereihenfolge zurück.
- `tools/call` — ruft einen Tool-Handler auf, liefert `ToolsCallResult` mit `content` und `isError` zurück.
- `resources/list`, `prompts/list` — liefern leere Arrays zurück (siehe Roadmap-Hinweise unten).
- `shutdown` — liefert `{}` zurück.

Jeder MCP-Host, der stdio-JSON-RPC spricht und die vier obigen Methoden aufruft, ist kompatibel.

## Getestete Clients

| Client | Status | Wie zu registrieren |
|---|---|---|
| Claude Desktop (macOS / Windows) | Funktioniert. | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) oder `%APPDATA%\Claude\claude_desktop_config.json` (Windows). |
| Claude CLI (`claude`) | Funktioniert. | `--mcp-config <file>` oder ein `[mcp]`-Block in `~/.claude/config.json`. |
| Continue.dev (VS Code / JetBrains) | Funktioniert. | `~/.continue/config.json` `mcpServers`-Block. |
| Codeium (IDE-Erweiterungen) | Funktioniert, wenn Codeium den MCP-Host-Modus exponiert (aktuelle Versionen). Setup variiert je nach IDE. |
| Cursor (aktuelle Versionen) | Funktioniert. Registrieren Sie ihn in Cursors eigener MCP-Einstellungs-UI. |
| Jedes Go- / TypeScript- / Python-MCP-Host-SDK | Funktioniert. Mit `command: "rousseau", args: ["mcp"]` instanziieren. |

Unbekannt / ungetestet, aber wahrscheinlich kompatibel: `zed`, `windsurf`, `aider`. Wenn Ihr Host die MCP-stdio-Spezifikation unterstützt, wird rousseau funktionieren.

## Claude Desktop

Bearbeiten Sie `claude_desktop_config.json` (Pfad oben) und fügen Sie hinzu:

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

Starten Sie Claude Desktop neu. Die vier `rousseau_*`-Tools erscheinen in der nächsten Chat-Sitzung im Tool-Picker.

Für arbeitsbereich-spezifischen Zustand fügen Sie einen env-Override hinzu:

```json
{
  "mcpServers": {
    "rousseau-work": {
      "command": "/usr/local/bin/rousseau",
      "args": ["--config", "/home/seb/.config/rousseau/work.yaml", "mcp"]
    }
  }
}
```

## Claude CLI

Zeigen Sie die CLI auf eine Konfiguration:

```sh
claude --mcp-config <(cat <<'JSON'
{
  "mcpServers": {
    "rousseau": {
      "command": "rousseau",
      "args": ["mcp"]
    }
  }
}
JSON
)
```

Oder tragen Sie sie in `~/.claude/config.json` unter einem `mcpServers`-Block in derselben Form ein.

## Continue.dev

Fügen Sie zu `~/.continue/config.json` hinzu:

```json
{
  "mcpServers": [
    {
      "name": "rousseau",
      "command": "rousseau",
      "args": ["mcp"]
    }
  ]
}
```

Continue nimmt die Tools beim nächsten Modellaufruf auf.

## Cursor

Cursor exponiert die MCP-Registrierung in seiner UI unter Settings > MCP. Registrieren Sie einen neuen Server namens `rousseau` mit dem Befehl `rousseau` und den Args `mcp`. Keine Konfigurationsdatei-Bearbeitung erforderlich.

## Codeium

Codeiums MCP-Unterstützung wird in aktuellen Versionen der IDE-Erweiterung hinter einem Feature-Flag ausgeliefert. Konsultieren Sie die Dokumentation der Erweiterung – die Registrierung ist erneut ein `command / args`-Paar.

## Umgebungsvariablen und Geheimnisse

Da rousseaus MCP-Oberfläche nur lesend auf den Sitzungsspeicher zugreift, benötigt sie keine Provider-Anmeldedaten. `ANTHROPIC_API_KEY` und Ähnliches werden von `rousseau mcp` nicht verwendet – nur von den Transport-/Chat-Daemons, die Sitzungen _erzeugen_.

## Häufige Probleme

- **"Server sofort beendet."** Rousseaus `mcp`-Befehl öffnet `state.path`. Wenn die Datei nicht beschreibbar ist, endet der Prozess mit einem Wert ungleich null. Führen Sie `rousseau mcp` aus einer Shell aus, um den genauen Fehler zu sehen.
- **"Unbekanntes Tool: rousseau_search_sessions."** Der Host hat eine ältere Tool-Liste zwischengespeichert. Starten Sie den Host neu.
- **Doppelte Registrierung.** Wenn zwei rousseau-Server mit demselben Namen registriert sind, gewinnt nur der letzte.

## Ressourcen und Prompts

`resources/list` und `prompts/list` liefern derzeit leer zurück. Die Seite [Exponierte Ressourcen](/de/mcp/exposed-resources/) verfolgt die Roadmap, Sitzungen als MCP-Ressourcen zu exponieren.

## Verwandt

- [MCP](/de/mcp/) — die Dachreferenz.
- [MCP: Exponierte Tools](/de/mcp/exposed-tools/) — jede Tool-Signatur.
- [MCP: Exponierte Ressourcen](/de/mcp/exposed-resources/) — Roadmap.
- [Tutorial: Tools über MCP exponieren](/de/tutorials/expose-tools-via-mcp/) — durchgearbeitetes Beispiel.
