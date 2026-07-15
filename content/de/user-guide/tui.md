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
description: "Bubble Tea TUI keybindings, panels, spinner and streaming semantics for rousseau-agent's rousseau chat command."
keywords: "tui, bubble tea, keybindings, viewport, textarea, spinner, streaming, session"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/user-guide/tui/"
subtitle: "Bubble Tea keybindings, panels, streaming."
tags: "tui, bubble-tea, keybindings"
title: "TUI"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tui, bubble tea, keybindings, viewport, textarea, spinner, streaming, session"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "TUI"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/tui/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/tui/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "TUI"
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
twitter_description: "Bubble Tea TUI keybindings, panels, spinner and streaming semantics for rousseau-agent's rousseau chat command."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "TUI"
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

## Übersicht

`rousseau chat` öffnet eine Bubble-Tea-TUI mit drei Regionen:

```
+------------------------------------------------------+
|                       Header                         |  Sitzungstitel
+------------------------------------------------------+
|                                                      |
|                                                      |
|                     Viewport                         |  scrollbarer Verlauf
|          (Nachrichten, Streaming-Antwort-Vorschau)   |
|                                                      |
|                                                      |
+------------------------------------------------------+
|                     Textarea                         |  Eingabe, Enter zum Senden
+------------------------------------------------------+
| Status: idle | Spinner | streaming | error           |
+------------------------------------------------------+
```

Läuft in Bubble Teas Alt-Screen-Modus – die TUI übernimmt den Terminal-Puffer und stellt ihn beim Beenden wieder her.

## Tastenbelegungen

Rousseaus TUI hält die Belegungsmenge klein. Im Zweifel gelten die Standard-Shortcuts von Bubble-Tea-Viewport / -Textarea.

### Global

| Taste | Aktion |
|---|---|
| `Ctrl+C` | Beenden. Speichert die aktuelle Sitzung, gibt beim Verlassen nichts aus. |
| `Esc` | Beenden. Wie `Ctrl+C`. |
| `Enter` | Aktuellen Textarea-Inhalt senden. No-op, während der Agent beschäftigt ist. |

### Textarea (Eingabe)

Standard-Bubble-Tea-Textarea-Verhalten:

| Taste | Aktion |
|---|---|
| Beliebiges druckbares Zeichen | An Cursor-Position einfügen. |
| `Backspace` | Zeichen vor Cursor löschen. |
| `Delete` | Zeichen unter Cursor löschen. |
| Pfeiltasten | Cursor bewegen. |
| `Home` / `End` | Zum Zeilenanfang / -ende springen. |
| `Ctrl+A` / `Ctrl+E` | Zum Zeilenanfang / -ende springen (Emacs-Bindungen). |
| `Ctrl+U` | Bis zum Zeilenanfang löschen. |
| `Ctrl+K` | Bis zum Zeilenende löschen. |
| `Shift+Enter` | (Terminal-abhängig) Zeilenumbruch ohne Senden; oft als literales `\n` gemappt. |

Die Textarea wächst vertikal, während Inhalte umbrechen; der Viewport schrumpft entsprechend.

### Viewport (Verlauf)

Der Viewport unterstützt die üblichen Bubble-Tea-Viewport-Shortcuts. Der Fokus liegt auf dem Viewport, wenn die Textarea leer ist; das Tippen wird automatisch an die Textarea geleitet.

| Taste | Aktion |
|---|---|
| `PgUp` / `PgDn` | Eine Seite scrollen. |
| `↑` / `↓` | Eine Zeile scrollen. |
| `Home` / `End` | Zum Anfang / Ende springen. |
| Mausrad | Scrollen. |

## Panel-Semantik

### Header

`rousseau · <Sitzungstitel>`. Der Titel kommt aus `--title` beim Anlegen der Sitzung (Standard: `chat YYYY-MM-DD HH:MM`).

### Viewport

Gerenderter Verlauf plus, während ein Turn in Bearbeitung ist, eine **Streaming-Vorschau** am unteren Rand. Die Vorschau reflektiert Deltas, während der Provider streamt; wenn der Turn endet, wird die Vorschau durch die finale Assistenten-Nachricht ersetzt.

Jede Nachricht wird durch ihre Rolle vorangestellt (`you`, `rousseau`, `tool`), sodass der Fluss unmissverständlich ist, wenn das Modell einen Tool-Aufruf anfordert.

### Textarea

Platzhaltertext: `Ask, or press Ctrl+C to quit…`. Enter sendet ab; die Textarea setzt sich beim Absenden zurück.

Während der Agent beschäftigt ist, ist `Enter` ein No-op, damit versehentliche Doppel-Sends keine Turns stapeln.

### Statuszeile

Unter der Textarea. Der Inhalt variiert:

| Zustand | Zeile |
|---|---|
| Idle | Leer. |
| Beschäftigt | Spinner + `thinking…`. Spinner-Ticks stammen von `bubbles/spinner`. |
| Streaming | Spinner läuft weiter; das Streaming-Delta erscheint in der Viewport-Vorschau. |
| Fehler | Fehlerstring in Rot. Der nächste erfolgreiche Turn löscht ihn. |

## Sitzungspersistenz

Jeder Turn wird über `state.Store.Save` in `~/.local/share/rousseau/sessions.db` persistiert. Wenn der Daemon mitten im Turn abstürzt:

- Der Benutzer-Turn ist bereits gespeichert (er wurde angehängt, bevor `doTurn` gefeuert hat).
- Die Assistenten-Antwort wird erst nach Abschluss des Turns gespeichert.

Beim Neustart setzt `rousseau chat --session <id>` vom letzten erfolgreich gespeicherten Zustand fort.

## Sitzungsbefehle aus der CLI

Die TUI exponiert nicht jede Sitzungsoperation. Verwalten Sie Sitzungen aus einer Shell:

```sh
rousseau session list
rousseau session show <id>
rousseau session search "kubectl"
rousseau session delete <id>
```

## Streaming-Semantik

Provider, die `StreamingProvider.ChatStream` implementieren (Anthropic, `claudecli`), streamen Deltas in die Viewport-Vorschau. Provider, die nur `Provider.Chat` implementieren (Bedrock, Vertex, OpenAI-kompatibel je nach Shim), liefern die Antwort als einen einzigen Block bei Turn-Abschluss – die Vorschau bleibt leer und die Antwort erscheint, wenn `busy` zu `false` wird.

## Wenn Dinge schiefgehen

- **Die TUI hängt** — `Ctrl+C` zweimal drücken. Das erste `Ctrl+C` signalisiert `tea.Quit`, das den Zustand flushed. Das zweite wird vom OS erfasst.
- **Der Viewport ist leer und die Textarea akzeptiert keine Eingabe** — der Alt-Screen könnte durch einen Subprozess mit Escape-Sequenzen (z. B. ein Tool-Aufruf, der ANSI-Codes ausgibt) beschädigt worden sein. Starten Sie die TUI neu.
- **Die Statuszeile bleibt auf `thinking…`** — der Provider ist nicht zurückgekehrt. Prüfen Sie stderr des Daemons (rousseau schreibt slog auf stderr; wenn Sie es umgeleitet haben, machen Sie es wieder sichtbar).

## Weiter

- [Benutzerleitfaden: CLI](/de/user-guide/cli/) — jeder Befehl außerhalb der TUI.
- [Konzepte](/de/concepts/) — die Agent-Schleife darunter.
- [Kompression + Recall](/de/user-guide/compression-recall/) — wie lange Chats nutzbar bleiben.
