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
date: "July 12, 2026"
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
description: "The five built-in tools shipped with rousseau-agent: read, write, edit, grep, bash. JSON schemas, execution semantics, safety notes."
keywords: "tools, read, write, edit, grep, bash, json schema, tool registry"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/user-guide/tools/"
subtitle: "The five built-in tools, with schemas and safety notes."
tags: "tools, reference, read, write, edit, grep, bash"
title: "Eingebaute Werkzeuge"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tools, read, write, edit, grep, bash, json schema, tool registry"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Eingebaute Werkzeuge"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 42
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/tools/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/tools/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Eingebaute Werkzeuge"
last_build_date: "Sun, 12 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
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
twitter_description: "The five built-in tools shipped with rousseau-agent: read, write, edit, grep, bash. JSON schemas, execution semantics, safety notes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Eingebaute Werkzeuge"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Danke an jeden Operator, der seinen eigenen Coding-Agenten betreibt."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Was ausgeliefert wird

`internal/tools/builtin/` stellt die fünf Tools bereit, die jeder rousseau-Daemon standardmäßig verdrahtet (siehe `internal/cli/chat.go` für die Verdrahtung):

| Tool | Zweck | Mutiert? |
|---|---|:---:|
| `read` | UTF-8-Textdatei lesen. | Nein |
| `write` | UTF-8-Textdatei überschreiben. Erstellt übergeordnete Verzeichnisse. | Ja |
| `edit` | Exakte String-Ersetzung, eindeutiger Treffer erforderlich. | Ja |
| `grep` | RE2-Regex-Suche unter einem Verzeichnis. | Nein |
| `bash` | `/bin/sh -c <cmd>` mit Timeout. | Ja |

Jedes wird über `registry.MustRegister(builtin.NewXTool())` registriert. Registrieren Sie zusätzliche Tools, ohne den Agent-Kern zu berühren – siehe [Entwicklerleitfaden: Tool hinzufügen](/de/developer-guide/add-a-tool/).

## `read`

Liest eine UTF-8-Textdatei aus dem lokalen Dateisystem.

**Eingabeschema:**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "Absolute filesystem path to the file to read."
    }
  },
  "required": ["path"]
}
```

**Semantik:**

- `path` muss absolut sein; relative Pfade werden abgelehnt.
- Lehnt binären Inhalt über einen `\x00`-Sniff auf den ersten 512 Byte ab.
- Gibt den Dateiinhalt wortwörtlich als String zurück.

**Fehler:** fehlender Pfad, relativer Pfad, nicht lesbare Datei, nicht-textueller Inhalt.

## `write`

Schreibt UTF-8-Text in eine Datei und ersetzt den bestehenden Inhalt. Erstellt bei Bedarf übergeordnete Verzeichnisse.

**Eingabeschema:**

```json
{
  "type": "object",
  "properties": {
    "path":    { "type": "string", "description": "Absolute filesystem path to write." },
    "content": { "type": "string", "description": "The complete file contents to write." }
  },
  "required": ["path", "content"]
}
```

**Semantik:**

- Überschreibt die Datei (kein Anhängen). Verwenden Sie `edit` für inkrementelle Änderungen.
- `MkdirAll(dir, 0o755)` auf dem übergeordneten Verzeichnis.
- Datei mit Berechtigung `0o644` geschrieben.
- Gibt `wrote <n> bytes to <path>` bei Erfolg zurück.

**Fehler:** fehlender Pfad, relativer Pfad, mkdir-Fehlschlag, Schreib-Fehlschlag.

## `edit`

Exakte String-Ersetzung mit einer **Eindeutigkeits-Bedingung**. Entlehnt aus Claude Codes Edit-Tool.

**Eingabeschema:**

```json
{
  "type": "object",
  "properties": {
    "path":       { "type": "string", "description": "Absolute filesystem path to the file to edit." },
    "old_string": { "type": "string", "description": "Exact text to find. Must be unique in the file." },
    "new_string": { "type": "string", "description": "Text to replace old_string with." }
  },
  "required": ["path", "old_string", "new_string"]
}
```

**Semantik:**

- `old_string` muss **genau einmal** in der Datei erscheinen. Null Vorkommen → Fehler. Zwei oder mehr → Fehler (fordert das Modell auf, mehr Kontext zu liefern).
- `old_string == new_string` → Fehler (No-op-Edits werden abgelehnt).
- Behält Einrückung und Whitespace wortwörtlich bei.
- Gibt `edited <path> (1 replacement)` bei Erfolg zurück.

Die Eindeutigkeits-Regel ist Absicht: Sie verhindert, dass das Modell versehentliche Massen-Ersetzungen durchführt. Wenn das Modell jedes Vorkommen ändern will, muss es mehrere `edit`-Aufrufe verfassen, jeweils mit genug umgebendem Kontext zur Disambiguierung.

**Fehler:** fehlender / relativer Pfad, fehlendes `old_string`, kein Treffer, nicht-eindeutiger Treffer, identische Strings, Lese-/Schreib-Fehlschlag.

## `grep`

Regex-Suche unter einem Verzeichnis. Bewusst einfacher als ripgrep – keine Abhängigkeit, läuft in-process.

**Eingabeschema:**

```json
{
  "type": "object",
  "properties": {
    "pattern":     { "type": "string",  "description": "Go RE2 regular expression to match." },
    "path":        { "type": "string",  "description": "Absolute directory to search under." },
    "include":     { "type": "string",  "description": "Optional filename glob (e.g. '*.go'). Applied to the base name." },
    "ignore_case": { "type": "boolean", "description": "Case-insensitive match. Defaults to false." }
  },
  "required": ["pattern", "path"]
}
```

**Semantik:**

- Go-[RE2](https://github.com/google/re2/wiki/Syntax)-Syntax – keine Backreferences, keine Lookaround.
- Läuft rekursiv durch `path`. Überspringt `.git`, `node_modules`, `vendor`, `.venv`, `__pycache__`, `dist`, `build`.
- Überspringt Dateien größer als `MaxFileBytes` (Standard 4 MiB) und binären Inhalt.
- Begrenzt die Ausgabe auf `MaxMatches` (Standard 200); Kürzung wird inline annotiert.
- Gibt `<path>:<line>: <matching-line>`-Zeilen zurück.
- Gibt den String `no matches` zurück, wenn nichts übereinstimmt.

**Fehler:** fehlendes Pattern / Pfad, relativer Pfad, ungültiger Regex, ungültiger Include-Glob.

## `bash`

Führt einen Shell-Befehl über `/bin/sh -c` aus. **Die tragende Sicherheitsgrenze.**

**Eingabeschema:**

```json
{
  "type": "object",
  "properties": {
    "command": {
      "type": "string",
      "description": "The shell command to execute."
    }
  },
  "required": ["command"]
}
```

**Semantik:**

- Läuft unter `/bin/sh -c <command>`. Nicht bash-spezifisch – POSIX-Shell.
- Kombiniertes stdout+stderr wird zurückgegeben.
- Standard-Timeout: 60 Sekunden. Konfigurierbar bei der Registrierung über `NewBashTool(timeout)`.
- Timeout gibt einen `bash: timed out after <duration>`-Fehler zurück, zusammen mit jeder Ausgabe, die vor der Deadline produziert wurde.
- Ein Exit ungleich null liefert einen Fehler, dessen String den Exit-Status umschließt; die Ausgabe wird trotzdem zurückgegeben, damit das Modell sie inspizieren kann.

**Sicherheit:**

- Das Tool hat keine eingebaute Allowlist. Der [Approver](/de/user-guide/approval-policies/) ist das tragende Gate. Aktivieren Sie bei unbeaufsichtigten Daemons **immer** die Pattern-Mode-Freigabe.
- Der Befehl läuft mit der UID und Dateisystem-Sichtbarkeit des Daemons. Legen Sie einen rootless Container darunter ([Bereitstellung](/de/deployment/)).

## Tool-Fehler und die Schleife

Wenn ein Tool einen Fehler zurückgibt, wandelt der Agent ihn in einen `tool_result`-Block mit `isError: true` um und speist ihn in der nächsten Iteration an das Modell zurück:

```
[user] mach die Änderung
[assistant] tool_use: edit {"path": "/tmp/foo", "old_string": "x", "new_string": "y"}
[user]      tool_result: "edit: old_string not found in /tmp/foo" (isError=true)
[assistant] Ich konnte "x" in /tmp/foo nicht finden. Können Sie den Pfad bestätigen?
```

Dies ist derselbe Kanal, der für Approver-Ablehnungen verwendet wird – siehe [Freigaberichtlinien](/de/user-guide/approval-policies/).

## Zusätzliche Tools registrieren

```go
registry := tools.NewRegistry()
registry.MustRegister(builtin.NewReadTool())
registry.MustRegister(builtin.NewWriteTool())
registry.MustRegister(builtin.NewEditTool())
registry.MustRegister(builtin.NewGrepTool(0, 0))    // null → Standardwerte
registry.MustRegister(builtin.NewBashTool(60 * time.Second))
registry.MustRegister(myCustomTool)                  // beliebiges tools.Tool
```

`tools.Registry` ist concurrency-sicher; die Registrierung ist thread-sicher.

## Sicherheitsimplikationen auf einen Blick

| Tool | Blast-Radius | Wann NICHT verwenden |
|---|---|---|
| `read` | Liest Dateien mit der FS-Sichtbarkeit des Daemons. Kann jede lesbare Datei exfiltrieren. | Wenn irgendein geheimes Material auf Disk im Arbeitsbereich liegt. Über Approver-`match`-Regex einschränken. |
| `grep` | Wie read plus Regex-CPU-Kosten. | Beim Matchen nicht vertrauenswürdiger Patterns – ReDoS ist mit pathologischen Regexes möglich. |
| `edit` | Modifiziert Dateiinhalte in-place. | Wenn die FS-Sichtbarkeit des Daemons über den beabsichtigten Arbeitsbereich hinausgeht. Kombinieren Sie mit einem Container-Bind-Mount. |
| `write` | Erstellt/überschreibt Dateien. | Wie edit, plus kann Dateien überall erstellen, wo der Daemon schreiben kann. |
| `bash` | Beliebige Befehlsausführung. | Auf jedem unbeaufsichtigten Daemon ohne einen Pattern-Mode-Approver. **Die primäre Sicherheitsgrenze.** |

## Fehlerbehebung

### `read: read /path: is a directory`

Das `read`-Tool ist datei-only. Verwenden Sie `grep` mit einem Path-Pattern oder `bash` (mit `ls`), wenn Sie Verzeichnisinhalte benötigen.

### `edit: old_string not found`

Das vom Modell vorgeschlagene `old_string` stimmte nicht Byte für Byte mit dem Dateiinhalt überein. Häufige Ursachen: Whitespace-/Zeilenumbruch-Drift, falscher Zeilenendstil, die Datei wurde zwischen dem Lesen des Modells und dem edit-Aufruf bearbeitet.

### `edit: old_string is not unique`

Rousseaus `edit`-Tool weigert sich, mehrdeutige Bearbeitungen durchzuführen – das Modell muss genug umgebenden Kontext einschließen, damit `old_string` ein eindeutiger Teilstring ist. Dies verhindert versehentliche Multi-Site-Ersetzungen.

### `bash: timed out after 1m0s`

Standard-Timeout von 60s. Langlaufende Befehle (Build, Test) werden fehlschlagen. Entweder erhöhen Sie das Timeout mit `NewBashTool(2*time.Minute)` beim Einbetten oder teilen Sie in schnellere Schritte auf.

### `grep` liefert nichts, obwohl das Pattern definitiv vorhanden ist

Rousseaus `grep` verwendet Gos `regexp`-Paket (RE2), das nicht alle PCRE-Features unterstützt. Backreferences und Lookarounds schlagen still fehl. Schreiben Sie das Pattern für RE2 um.

## Verwandte Seiten

- [Benutzerleitfaden: Freigaberichtlinien](/de/user-guide/approval-policies/) — das Gate auf jedem Tool-Aufruf.
- [Entwicklerleitfaden: Tool hinzufügen](/de/developer-guide/add-a-tool/) — bauen Sie Ihr eigenes.
- [Konzepte](/de/concepts/) — wie Tools in die Agent-Schleife passen.
- [Agent-Schleife](/de/agent-loop/) — wie Tool-Ergebnisse in den nächsten Turn zurückfließen.
- [Referenz: Tool-Schemas](/de/reference/tool-schemas/) — maschinenlesbare Schemas.

## Weiterführende Lektüre

- `internal/tools/builtin/read.go` — Dateilesen mit Kürzung.
- `internal/tools/builtin/write.go` — Dateischreiben.
- `internal/tools/builtin/edit.go` — der Eindeutigkeits-Constraint-Enforcer.
- `internal/tools/builtin/grep.go` — rekursive Regex-Suche.
- `internal/tools/builtin/bash.go` — `/bin/sh -c` Shell-Wrapper.
