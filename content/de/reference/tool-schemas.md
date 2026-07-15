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
description: "The exact JSON schemas for the five built-in tools rousseau ships: read, write, edit, grep, bash."
keywords: "tool schemas, read, write, edit, grep, bash, JSON Schema"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/reference/tool-schemas/"
subtitle: "JSON schemas for the five built-in tools, verbatim from internal/tools/builtin."
tags: "reference, tools, json-schema, read, write, edit, grep, bash"
title: "Referenz: Werkzeug-Schemas"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tool schemas, read, write, edit, grep, bash, JSON Schema"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Referenz: Werkzeug-Schemas"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 54
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/tool-schemas/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/tool-schemas/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Referenz: Werkzeug-Schemas"
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
twitter_description: "The exact JSON schemas for the five built-in tools rousseau ships: read, write, edit, grep, bash."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Referenz: Werkzeug-Schemas"
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

## Was diese Seite ist

Jedes eingebaute Tool in `internal/tools/builtin/*.go` veröffentlicht eine `InputSchema()`-Methode, die eine JSON-Schema-Map zurückgibt. Diese Seite reproduziert diese Schemata exakt, plus einen Absatz zum Laufzeit-Vertrag jedes Tools.

Die fünf eingebauten Tools sind: [`read`](#read), [`write`](#write), [`edit`](#edit), [`grep`](#grep), [`bash`](#bash). Alle fünf werden in der Daemon-Verdrahtung konstruiert; der Approver (`internal/agent/approver.go`) sitzt zwischen dem Tool-Aufruf des Modells und der `Execute`-Methode des Tools.

## read

Quelle: `internal/tools/builtin/read.go`.

**Beschreibung (dem Modell präsentiert):** _Read the contents of a UTF-8 text file. Input: absolute path. Returns file contents or an error._

**Input-Schema:**

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

**Vertrag.** Der `path` muss absolut sein (`filepath.IsAbs`). Das Tool liest die gesamte Datei in den Speicher und lehnt sie ab, wenn die ersten 512 Bytes ein NUL-Byte enthalten (`isLikelyText`). Gibt bei Erfolg den Dateiinhalt als String zurück; andernfalls einen Fehler. Auf Tool-Ebene wird keine Zeilenzahl- oder Größenbegrenzung durchgesetzt — Freigaberichtlinien sind der richtige Ort, um Dateigrößen zu begrenzen.

## write

Quelle: `internal/tools/builtin/write.go`.

**Beschreibung (dem Modell präsentiert):** _Write UTF-8 text to a file, replacing existing contents. Creates parent directories as needed. Input: absolute path + content._

**Input-Schema:**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "Absolute filesystem path to write."
    },
    "content": {
      "type": "string",
      "description": "The complete file contents to write."
    }
  },
  "required": ["path", "content"]
}
```

**Vertrag.** Vollständiges Datei-Überschreiben. Erstellt übergeordnete Verzeichnisse mit Modus `0o755`. Schreibt mit Modus `0o644`. Absoluter Pfad erforderlich. Gibt `"wrote N bytes to /path"` zurück. Es gibt bewusst keinen atomaren Swap-Tanz — Pattern-Modus-Approver binden das Schreibziel an einen bestimmten Verzeichnisbaum; das Tool selbst versucht nicht, in Sachen Dateisystem-Sicherheit klug zu sein.

## edit

Quelle: `internal/tools/builtin/edit.go`.

**Beschreibung (dem Modell präsentiert):** _Replace exactly one occurrence of old_string with new_string in a file. old_string must be unique in the file; if it appears zero or multiple times the edit fails. Preserve indentation exactly._

**Input-Schema:**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "Absolute filesystem path to the file to edit."
    },
    "old_string": {
      "type": "string",
      "description": "Exact text to find. Must be unique in the file."
    },
    "new_string": {
      "type": "string",
      "description": "Text to replace old_string with."
    }
  },
  "required": ["path", "old_string", "new_string"]
}
```

**Vertrag.** Exact-String-Ersetzung, keine Regex. `old_string` muss **genau einmal** in der Datei erscheinen — null Treffer oder mehrere Treffer scheitern beide mit einem beschreibenden Fehler, was beabsichtigt ist (aus dem Edit-Tool von Claude Code entlehnt). Verhindert versehentliches Massenersetzen und zwingt das Modell, genug Umgebungskontext einzuschließen, um zu disambiguieren. `old_string == new_string` schlägt ebenfalls fehl. Gibt `"edited /path (1 replacement)"` zurück.

## grep

Quelle: `internal/tools/builtin/grep.go`.

**Beschreibung (dem Modell präsentiert):** _Search files under a directory for a Go regular expression. Skips binary files and files larger than the configured limit. Returns 'path:line: matched_line' rows._

**Input-Schema:**

```json
{
  "type": "object",
  "properties": {
    "pattern": {
      "type": "string",
      "description": "Go RE2 regular expression to match."
    },
    "path": {
      "type": "string",
      "description": "Absolute directory to search under."
    },
    "include": {
      "type": "string",
      "description": "Optional filename glob (e.g. '*.go'). Applied to the base name."
    },
    "ignore_case": {
      "type": "boolean",
      "description": "Case-insensitive match. Defaults to false."
    }
  },
  "required": ["pattern", "path"]
}
```

**Vertrag.** RE2-Regex, nicht PCRE. Case-insensitiv bei `ignore_case: true` (implementiert durch Präfix `(?i)`). Überspringt Verzeichnisse namens `.git`, `node_modules`, `vendor`, `.venv`, `__pycache__`, `dist`, `build`. Überspringt Dateien größer als `MaxFileBytes` (Standard 4 MiB). Kürzt die Ausgabe bei `MaxMatches` (Standard 200) und hängt einen `(truncated at N matches)`-Footer an, wenn die Obergrenze erreicht wird. Überspringt Dateien, die auf der aktuellen Zeile ein NUL-Byte enthalten (grobe Binärerkennung).

## bash

Quelle: `internal/tools/builtin/bash.go`.

**Beschreibung (dem Modell präsentiert):** _Execute a shell command via `/bin/sh -c`. Returns combined stdout+stderr with exit status._

**Input-Schema:**

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

**Vertrag.** `/bin/sh -c <command>`. Kombiniertes stdout + stderr, begrenzt durch das, was in einen `bytes.Buffer` (also RAM) passt. Standardmäßig 60 Sekunden Timeout (bei Konstruktion konfigurierbar). Bei Timeout: gibt die Teilausgabe plus einen `bash: timed out after 60s`-Fehler zurück. **Keine Sandbox auf Tool-Ebene.** Der OS-Nutzer des Daemons, die Dateisystem-Sicht, die Netzwerkhaltung und das seccomp-Profil sind die Einschließung. Pattern-Modus-Approver sind Ihr Werkzeug, um die erlaubten Befehle einzuengen — siehe [Tutorial: Approver härten](/de/tutorials/harden-approver-policy/).

## MCP-exponierte Tools

Der stdio-MCP-Server von rousseau (`rousseau mcp`) exponiert einen **anderen** Satz von Tools — Read-only-Abfragen gegen den Session-Store und Cron-Jobs. Siehe [MCP: Exponierte Tools](/de/mcp/exposed-tools/) für `rousseau_search_sessions`, `rousseau_list_sessions`, `rousseau_read_session`, `rousseau_cron_list`.

## Verwandt

- [Benutzerleitfaden: Tools](/de/user-guide/tools/) — die Operator-Sicht.
- [Leitfäden: Datei-Management](/de/guides/file-management/) — wie `write`/`edit` mit Bind-Mounts und SELinux interagieren.
- [Leitfäden: Audit + Freigaberichtlinien](/de/guides/audit-approval-policies/) — wie Pattern-Regexe die Eingabe jedes Tools einschränken.
- [Entwicklerleitfaden: Tool hinzufügen](/de/developer-guide/add-a-tool/) — diesen Satz erweitern.
