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
description: "Compact reference table of every rousseau-agent command mirroring the output of rousseau --help."
keywords: "cli, commands, reference, table, rousseau --help"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/reference/cli-commands/"
subtitle: "Every command tabulated."
tags: "reference, cli, commands"
title: "CLI-Befehle"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cli, commands, reference, table, rousseau --help"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "CLI-Befehle"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 50
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/cli-commands/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/cli-commands/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "CLI-Befehle"
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
twitter_description: "Compact reference table of every rousseau-agent command mirroring the output of rousseau --help."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "CLI-Befehle"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Was Sie lernen</span><p>Die vollständige <code>rousseau</code>-CLI-Oberfläche: jeder Befehl, seine Flags, die Exit-Code-Semantik und die Konfigurationsschlüssel, die jedes Flag überschreibt. Dies ist die scanfähige Referenz – siehe <a href="/de/user-guide/cli/">Benutzerleitfaden: CLI</a> für einen Durchgang mit durchgearbeiteten Beispielen.</p></aside>

## Befehlsbaum

Jeder Befehl gibt seine Hilfe über `rousseau <cmd> --help` aus. Diese Seite ist die tabellarische Zusammenfassung.

| Befehl | Beschreibung |
|---|---|
| `chat` | Öffnet die interaktive Bubble-Tea-TUI. |
| `whatsapp` | Führt die WhatsApp-Bridge aus (whatsmeow). |
| `signal` | Führt die Signal-Bridge aus (signal-cli JSON-RPC). |
| `telegram` | Führt den Telegram-Bot-API-Long-Poller aus. |
| `matrix` | Führt die Matrix-Client-Server-Bridge aus. |
| `slack` | Führt die Slack-Socket-Mode-Bridge aus. |
| `discord` | Führt die Discord-Gateway-Bridge aus. |
| `sms` | Nur ausgehende SMS über Twilio oder Vonage. |
| `imessage` | BlueBubbles-basierte iMessage-Bridge. |
| `email` | IMAP-eingehende + SMTP-ausgehende Bridge. |
| `mcp` | Startet den MCP-JSON-RPC-2.0-Server auf stdio. |
| `cron add` | Fügt einen geplanten Prompt hinzu. |
| `cron list` | Listet jeden geplanten Job auf. |
| `cron remove` | Löscht einen geplanten Job. |
| `cron enable` | Aktiviert einen deaktivierten geplanten Job. |
| `cron disable` | Deaktiviert einen aktivierten geplanten Job. |
| `session list` | Listet Sitzungen im Speicher auf, neueste zuerst. |
| `session search` | FTS5-Suche über den Nachrichteninhalt jeder Sitzung. |
| `session show` | Gibt den Nachrichtenverlauf einer Sitzung aus. |
| `session delete` | Löscht eine Sitzung. |
| `skills list` | Listet erkannte Skills aus `skills_dir` auf. |
| `skills show` | Gibt YAML-Frontmatter und Body eines Skills aus. |
| `skills lint` | Validiert Skills auf Schemakonformität. |
| `doctor` | Diagnostiziert die lokale Installation. Gibt einen Bericht aus. |
| `status` | Gibt Daemon-Status aus. |
| `init` | Schreibt eine Standardkonfiguration nach `~/.config/rousseau/`. |
| `version` | Gibt Version, Commit und Build-Datum aus. |

## Globale Flags

Jeder Befehl akzeptiert diese:

| Flag | Typ | Konfigurationsschlüssel | Hinweise |
|---|---|---|---|
| `--config` | string | — | Lädt die Konfiguration aus dieser Datei. Standard: `$XDG_CONFIG_HOME/rousseau/config.yaml`. |
| `--help`, `-h` | bool | — | Gibt Hilfe für den aktuellen Befehl aus. |

## Transport-spezifische Flags

### `rousseau whatsapp`

| Flag | Typ | Konfigurationsschlüssel | Hinweise |
|---|---|---|---|
| `--store` | string | — | Pfad zum whatsmeow-Gerätespeicher. Standard `$XDG_DATA_HOME/rousseau/whatsapp.db`. |
| `--allow` | []string | `whatsapp.allowlist` | Eingang auf diese JIDs beschränken. Wiederholbar. |

### `rousseau slack`

| Flag | Typ | Konfigurationsschlüssel |
|---|---|---|
| `--app-token` | string | `slack.app_token` |
| `--bot-token` | string | `slack.bot_token` |
| `--bot-user-id` | string | `slack.bot_user_id` |
| `--allow` | []string | `slack.allowlist` |

### `rousseau discord`

| Flag | Typ | Konfigurationsschlüssel |
|---|---|---|
| `--token` | string | `discord.token` |
| `--allow` | []string | `discord.allowlist` |

### `rousseau telegram`

| Flag | Typ | Konfigurationsschlüssel |
|---|---|---|
| `--token` | string | `telegram.token` |
| `--allow` | []string | `telegram.allowlist` |

### `rousseau matrix`

| Flag | Typ | Konfigurationsschlüssel |
|---|---|---|
| `--homeserver-url` | string | `matrix.homeserver_url` |
| `--access-token` | string | `matrix.access_token` |
| `--user-id` | string | `matrix.user_id` |
| `--allow` | []string | `matrix.allowlist` |

### `rousseau signal`

| Flag | Typ | Konfigurationsschlüssel |
|---|---|---|
| `--account` | string | `signal.account` |
| `--binary` | string | `signal.binary` |
| `--allow` | []string | `signal.allowlist` |

### `rousseau email`

| Flag | Typ | Konfigurationsschlüssel |
|---|---|---|
| `--imap-addr` | string | `email.imap_addr` |
| `--imap-username` | string | `email.imap_username` |
| `--imap-password` | string | `email.imap_password` |
| `--smtp-addr` | string | `email.smtp_addr` |
| `--smtp-username` | string | `email.smtp_username` |
| `--smtp-password` | string | `email.smtp_password` |
| `--from` | string | `email.from` |
| `--mailbox` | string | `email.mailbox` |
| `--poll-interval` | string | `email.poll_interval` |

### `rousseau sms`

| Flag | Typ | Konfigurationsschlüssel |
|---|---|---|
| `--provider` | string | `sms.provider` |
| `--from` | string | `sms.from` |
| `--to` | string | (positional) |

### `rousseau imessage`

| Flag | Typ | Konfigurationsschlüssel |
|---|---|---|
| `--base-url` | string | `imessage.base_url` |
| `--password` | string | `imessage.password` |
| `--chat-guid` | string | `imessage.chat_guid` |

## Exit-Codes

| Code | Bedeutung |
|---|---|
| 0 | Sauberer Exit – Befehl abgeschlossen. Für langlaufende Daemons nicht typisch (sie enden meist per Signal). |
| 1 | Jeder aus `Execute` gemeldete Fehler. Siehe [Referenz: Exit-Codes](/de/reference/exit-codes/) für die Klassifizierung. |

## Rangfolge

Konfigurationswerte werden in der Reihenfolge **flag &gt; env &gt; file &gt; default** aufgelöst (siehe `config.Load` in `internal/config/config.go`). Umgebungsvariablen sind mit `ROUSSEAU_` präfixiert und Punkte durch Unterstriche ersetzt – z. B. überschreibt `ROUSSEAU_ANTHROPIC_MODEL` `anthropic.model`. Die reine `ANTHROPIC_API_KEY`-Umgebungsvariable wird ebenfalls berücksichtigt (Sonderfall in `config.Load`).

## Fehlerbehebung

### `unknown flag: --allow` bei `rousseau chat`

`--allow` ist transport-spezifisch. `chat` hat keine Allowlist, weil es keinen Eingang gibt. Verwenden Sie stattdessen `rousseau whatsapp --allow …`.

### Die Flag-Reihenfolge zählt bei wiederholbaren Flags

`--allow A --allow B` sind zwei Werte, aber `--allow=A,B` ist ein Wert, der zufällig ein Komma enthält. Bevorzugen Sie separate Flags.

### Env-Override wird nicht aufgenommen

Rousseau liest Env nur beim Start. Starten Sie den Daemon nach dem Ändern von Env-Variablen neu, oder verwenden Sie `--config`, um ein Neuladen zu erzwingen.

### `flag provided but not defined`

Cobra weist unbekannte Flags ab. Wenn Sie ein Flag aus einer neueren Version kopieren, prüfen Sie `rousseau <cmd> --help` für die aktuelle Schreibweise.

## Verwandte Seiten

- [Benutzerleitfaden: CLI](/de/user-guide/cli/) — jeder Befehl mit durchgearbeiteten Beispielen.
- [Referenz: Exit-Codes](/de/reference/exit-codes/) — Signal-Semantik.
- [Referenz: Konfigurationsschema](/de/reference/config-schema/) — jedes Konfigurationsfeld.
- [Referenz: Umgebungsvariablen](/de/reference/environment-variables/) — Env-Override-Matrix.
- [Konfiguration](/de/configuration/) — der vollständige Konfigurationsdatei-Durchgang.

## Weiterführende Lektüre

- `internal/cli/root.go` — Cobra-Befehlsbaum.
- `internal/cli/*.go` — eine Datei pro Unterbefehl.
- `internal/config/config.go` — `Load` und Standardwert-Auflösung.
