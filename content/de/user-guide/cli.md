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
description: "Full CLI reference for rousseau-agent: every command, every flag, exit codes, per-transport subcommands."
keywords: "cli, cobra, commands, flags, subcommands, exit codes"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/user-guide/cli/"
subtitle: "Every command, every flag."
tags: "cli, reference, commands"
title: "CLI-Referenz"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cli, cobra, commands, flags, subcommands, exit codes"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "CLI-Referenz"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 40
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/cli/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/cli/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "CLI-Referenz"
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
twitter_description: "Full CLI reference for rousseau-agent: every command, every flag, exit codes, per-transport subcommands."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "CLI-Referenz"
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

## Aufruf

```
rousseau [--config <path>] <command> [flags]
```

Jeder Befehl liest Standardwerte aus `~/.config/rousseau/config.yaml` (oder der über `--config` übergebenen Datei). Flags überschreiben Umgebungsvariablen, Umgebungsvariablen überschreiben die Datei, die Datei überschreibt hartcodierte Standardwerte.

## Globale Flags

| Flag | Typ | Standardwert | Hinweise |
|---|---|---|---|
| `--config` | string | `$XDG_CONFIG_HOME/rousseau/config.yaml` | Lädt die Konfiguration aus dieser Datei. Fehlt der Wert, wird der XDG-Standardpfad verwendet. |
| `--help`, `-h` | bool | — | Hilfe für den aktuellen Befehl ausgeben. |

## Befehlsbaum

```
rousseau
├── chat                Bubble-Tea-TUI
├── whatsapp            WhatsApp-Bridge (whatsmeow)
├── signal              Signal-Bridge (signal-cli JSON-RPC)
├── telegram            Telegram-Bot-API-Long-Polling
├── matrix              Matrix-Client-Server-API
├── slack               Slack Socket Mode
├── discord             Discord-Gateway
├── sms                 SMS nur ausgehend (Twilio / Vonage)
├── imessage            BlueBubbles-basierte iMessage-Bridge
├── email               IMAP eingehend + SMTP ausgehend
├── mcp                 MCP-JSON-RPC-2.0-Server über stdio
├── cron                Geplante Prompts verwalten
├── session             Sitzungsspeicher inspizieren / löschen
├── skills              Skills auflisten / anzeigen / linten
├── doctor              Lokale Installation diagnostizieren
├── status              Daemon-Status ausgeben
├── init                Standardkonfiguration nach ~/.config/rousseau/ schreiben
└── version             Version, Commit, Build-Datum ausgeben
```

## `rousseau chat`

Öffnet die interaktive Bubble-Tea-TUI.

| Flag | Typ | Standardwert | Hinweise |
|---|---|---|---|
| `--session` | string | — | Eine bestehende Sitzung per ID fortsetzen. |
| `--title` | string | Zeitstempel | Titel für eine neue Sitzung. |

## `rousseau whatsapp`

Führt die WhatsApp-Bridge aus. Zeigt beim ersten Start einen QR-Code an.

| Flag | Typ | Standardwert | Hinweise |
|---|---|---|---|
| `--store` | string | `$XDG_DATA_HOME/rousseau/whatsapp.db` | Pfad zum whatsmeow-Geräte-Store. |
| `--allow` | []string | keine | Beschränkt die eingehende Verarbeitung auf diese JIDs. Wiederholbar. **Lassen Sie es bei einer öffentlichen Nummer niemals leer.** |

## `rousseau signal`

Führt die Signal-Bridge aus. Startet `signal-cli jsonRpc` als Subprozess.

| Flag | Typ | Standardwert | Hinweise |
|---|---|---|---|
| `--account` | string | aus `signal.account` | E.164-Telefonnummer, unter der der Daemon läuft. |
| `--binary` | string | `signal-cli` | Pfad zur signal-cli-Executable. |
| `--allow` | []string | keine | Eingang auf diese E.164-Nummern beschränken. |

## `rousseau telegram`

Führt den Telegram-Bot-API-Long-Poller aus.

| Flag | Typ | Standardwert | Hinweise |
|---|---|---|---|
| `--token` | string | aus `telegram.token` | BotFather-Token. |
| `--allow` | []string | keine | Eingang auf diese Chat-IDs beschränken. |

## `rousseau matrix`

Führt die Matrix-Bridge aus.

| Flag | Typ | Standardwert | Hinweise |
|---|---|---|---|
| `--homeserver-url` | string | aus config | z. B. `https://matrix.org`. |
| `--access-token` | string | aus config | Access-Token des Bots. |
| `--user-id` | string | aus config | Matrix-User-ID des Bots (`@bot:matrix.org`). |
| `--allow` | []string | keine | Eingang auf diese User-IDs beschränken. |

## `rousseau slack`

Führt die Slack-Socket-Mode-Bridge aus.

| Flag | Typ | Standardwert | Hinweise |
|---|---|---|---|
| `--app-token` | string | aus config | `xapp-...` Socket-Mode-Token. |
| `--bot-token` | string | aus config | `xoxb-...` Bot-User-OAuth-Token. |
| `--allow` | []string | keine | Eingang auf diese Slack-User-IDs beschränken. |

## `rousseau discord`

Führt die Discord-Gateway-Bridge aus.

| Flag | Typ | Standardwert | Hinweise |
|---|---|---|---|
| `--token` | string | aus config | Bot-Token. |
| `--allow` | []string | keine | Eingang auf diese Discord-User-IDs beschränken. |

## `rousseau sms`

Nur ausgehende SMS über Twilio oder Vonage. Kein Eingang.

| Flag | Typ | Standardwert | Hinweise |
|---|---|---|---|
| `--provider` | string | aus config | `twilio` oder `vonage`. |
| `--from` | string | aus config | E.164-Absendernummer. |
| `--account-sid` | string | aus config | Twilio-Account-SID. |
| `--auth-token` | string | aus config | Twilio-Auth-Token oder Vonage-Secret. |
| `--api-key` | string | aus config | Vonage-API-Key. |

## `rousseau imessage`

BlueBubbles-basierte iMessage-Bridge.

| Flag | Typ | Standardwert | Hinweise |
|---|---|---|---|
| `--base-url` | string | `http://localhost:1234` | BlueBubbles-Server-URL. |
| `--password` | string | aus config | BlueBubbles-Server-Passwort. |
| `--chat-guid` | string | aus config | Ausgangs-Ziel. |
| `--poll-interval` | duration | 5s | Wie oft nach neuen Nachrichten gepollt wird. |
| `--allow` | []string | keine | Eingang beschränken. |

## `rousseau email`

E-Mail-Bridge über IMAP + SMTP.

| Flag | Typ | Standardwert | Hinweise |
|---|---|---|---|
| `--imap-addr` | string | aus config | z. B. `imap.example.com:993`. |
| `--imap-username`, `--imap-password` | string | aus config | IMAP-Zugangsdaten. |
| `--smtp-addr` | string | aus config | z. B. `smtp.example.com:587`. |
| `--smtp-username`, `--smtp-password` | string | aus config | SMTP-Zugangsdaten. |
| `--from` | string | aus config | Envelope-Absender. |
| `--poll-interval` | duration | 30s | IMAP-Poll-Takt. |
| `--allow` | []string | keine | Eingehende Absenderadressen beschränken. |

## `rousseau mcp`

Startet den MCP-Server auf stdio. Keine Flags – jeder Knopf lebt in `config.yaml`.

## `rousseau cron`

| Unterbefehl | Beschreibung |
|---|---|
| `cron add` | Einen geplanten Prompt hinzufügen. Flags: `--name`, `--schedule` (5-Feld-cron), `--prompt`, `--deliver-to`. |
| `cron list` | Jeden Job mit `on/off`-Status und letztem Ausführungszeitstempel auflisten. |
| `cron remove <name-or-id>` | Einen Job löschen. |
| `cron enable <name-or-id>` | Einen deaktivierten Job aktivieren. |
| `cron disable <name-or-id>` | Einen aktivierten Job deaktivieren (ohne Löschen). |

## `rousseau session`

| Unterbefehl | Beschreibung |
|---|---|
| `session list` | Sitzungen im Store auflisten, neueste zuerst. |
| `session search <query>` | FTS5-Suche über den Nachrichteninhalt jeder Sitzung. |
| `session show <id>` | Den Nachrichtenverlauf einer Sitzung ausgeben. |
| `session delete <id>` | Eine Sitzung löschen. |

## `rousseau skills`

| Unterbefehl | Beschreibung |
|---|---|
| `skills list` | Aus `skills_dir` erkannte Skills auflisten. |
| `skills show <name>` | YAML-Frontmatter und Body eines Skills ausgeben. |
| `skills lint` | Skills auf Schemakonformität validieren. |

## `rousseau doctor`

Geht jede Laufzeit-Abhängigkeit und jede Konfigurationswahl durch. Gibt einen Statusbericht mit Zeilen aus, die mit `ok`, `warn`, `fail`, `info` markiert sind. Exit-Code 1, wenn eine Zeile `fail` ist.

Heute keine Flags; erweitern Sie über `--config` auf globaler Ebene.

## `rousseau status`

Gibt eine kompakte Daemon-Status-Zusammenfassung aus – Provider, Sitzungsanzahl, Cron-Jobs. Nur lesend.

## `rousseau init`

Schreibt eine Standard-`config.yaml` nach `~/.config/rousseau/`. Weigert sich, eine bestehende Datei zu überschreiben, sofern nicht `--force` übergeben wird.

| Flag | Typ | Standardwert | Hinweise |
|---|---|---|---|
| `--force` | bool | false | Eine bestehende Konfiguration überschreiben. |

## `rousseau version`

Gibt Version, Commit-Hash und Build-Datum aus. Zur Bauzeit über `-ldflags` gestempelt.

## Exit-Codes

| Code | Bedeutung |
|---|---|
| 0 | Befehl erfolgreich abgeschlossen. |
| 1 | Befehl fehlgeschlagen. Fehler wird auf stderr ausgegeben. |

Siehe [Referenz: Exit-Codes](/de/reference/exit-codes/) für die Daemon-Signal-Semantik.

## Umgebungsvariablen

Jedes Konfigurationsfeld kann durch eine Umgebungsvariable überschrieben werden, die das Präfix `ROUSSEAU_` und `_` als Abschnitts-Trennzeichen verwendet: `ROUSSEAU_LOG_LEVEL=debug`, `ROUSSEAU_ANTHROPIC_API_KEY=sk-ant-...`, etc.

Der Sonderfall ist `ANTHROPIC_API_KEY` (ohne Präfix) – es wird direkt vom Konfigurations-Loader konventionsgemäß aufgenommen.

## Fehlerbehebung

### `unknown command` beim Übergeben eines Unterbefehls

Rousseaus Unterbefehle sind in `internal/cli/root.go` deklariert. Wenn `rousseau <cmd>` unbekannt meldet, ist entweder das Flag falsch geschrieben oder Sie sind auf einem älteren Binary. `rousseau version` zeigt, was Sie haben.

### Wiederholbare Flags benötigen mehrere Aufrufe

`--allow` akzeptiert eine JID pro Flag. Wiederholen Sie das Flag für mehrere Werte: `--allow A --allow B`, nicht `--allow A,B`.

### Env-Variablen werden still ignoriert

Rousseau verwendet das `ROUSSEAU_`-Präfix + Unterstrich als Abschnitts-Trennzeichen: `anthropic.model` wird zu `ROUSSEAU_ANTHROPIC_MODEL`. Groß-/Kleinschreibung ist wichtig.

### `rousseau chat` zeigt nur einen leeren Bildschirm

Die Bubble-Tea-TUI benötigt ein ANSI-fähiges Terminal. Setzen Sie `TERM=xterm-256color` und führen Sie interaktiv aus (nicht unter `nohup` oder einer Pipe).

### Befehl beendet sofort mit 0

Einige Flags (`--help`, `--version`-Varianten) kurzschließen. Wenn Ihr Befehl nicht läuft, prüfen Sie die übergebenen Flags.

## Verwandte Seiten

- [Benutzerleitfaden: TUI](/de/user-guide/tui/) — Tastenbelegungen innerhalb von `rousseau chat`.
- [Benutzerleitfaden: Tools](/de/user-guide/tools/) — das JSON-Schema jedes eingebauten Tools.
- [Referenz: CLI-Befehle](/de/reference/cli-commands/) — Befehlstabelle.
- [Referenz: Umgebungsvariablen](/de/reference/environment-variables/) — Override-Matrix.
- [Konfiguration](/de/configuration/) — die Konfigurationsdatei, die jedem Befehl zugrunde liegt.

## Weiterführende Lektüre

- `internal/cli/root.go` — der Cobra-Baum.
- `internal/cli/chat.go`, `internal/cli/whatsapp.go`, `internal/cli/slack.go`, … — eine Datei pro Unterbefehl.
- `internal/config/config.go` — Env-Variable-/Flag-Auflösung.
