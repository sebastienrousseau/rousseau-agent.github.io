---

# Front Matter (YAML)

author: "sebastian.rousseau@gmail.com (Sebastien Rousseau) "
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
description: "How the LLM compressor decides what to keep, the roles of trigger_messages and keep_recent, and a before/after diagram of a compressed session."
keywords: "compression, context, keep_recent, trigger_messages, summariser, marker"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/guides/context-management/"
subtitle: "trigger_messages, keep_recent, and the compressed-marker convention."
tags: "guides, context, compression, summariser"
title: "Leitfaden: Kontextverwaltung"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "compression, context, keep_recent, trigger_messages, summariser, marker"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Leitfaden: Kontextverwaltung"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/context-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/context-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Leitfaden: Kontextverwaltung"
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
twitter_description: "How the LLM compressor decides what to keep, the roles of trigger_messages and keep_recent, and a before/after diagram of a compressed session."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Leitfaden: Kontextverwaltung"
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

## Das Problem

Eine Sitzung, die wochenlang läuft, akkumuliert Hunderte von Nachrichten. Jede einzelne wird bei jedem Turn erneut an den Provider gesendet. Kosten wachsen linear mit der Turn-Zahl; Latenz auch. Der `LLMCompressor` von rousseau (`internal/agent/compressor.go`) tauscht kleine einmalige Kosten — einen Summarisation-Aufruf pro Komprimierung — gegen permanente Einsparungen bei jedem nachfolgenden Turn.

Komprimierung ist **standardmäßig aus**, weil die Referenzbereitstellung `claudecli` auf einer Abonnementstufe verwendet, bei der die Token-Zahl nicht abgerechnet wird. Aktivieren Sie sie beim Betrieb gegen Anthropic direkt, Bedrock, Vertex oder OpenAI-kompatible Pay-per-Token-Provider.

## Die Knöpfe

Aus `CompressionConfig` in `internal/config/config.go`:

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60        # zero uses the default 60
    keep_recent: 8              # zero uses the default 8
    prompt: ""                  # overrides the default summariser prompt
```

Bedeutungen:

| Feld | Was es tut |
|---|---|
| `enabled` | Komprimierung einschalten. Bei false verwendet der Agent `NoopCompressor` und dieser gesamte Abschnitt ist ein No-Op. |
| `trigger_messages` | Komprimierung feuert, sobald `len(session.Messages) >= trigger_messages`. |
| `keep_recent` | Anzahl der jüngsten Nachrichten, die nach der Komprimierung wörtlich bewahrt werden. |
| `prompt` | Überschreibt den Standard-Summariser-Prompt. Setzen Sie nur, wenn Sie benutzerdefinierte Anweisungen benötigen (z. B. JSON-Ausgabe bewahren, immer Dateipfade zitieren). |

## Der Standard-Summariser-Prompt

```
Summarise the following conversation in <=200 words. Preserve every
commitment, TODO, credential, filename, and quoted output. Skip
pleasantries. Return only the summary — no preamble.
```

Definiert als `defaultSummaryPrompt` in `internal/agent/compressor.go`. Überschreiben mit `agent.compression.prompt` in `config.yaml`.

## Vorher / Nachher

Eine Sitzung mit 68 Nachrichten, `trigger_messages: 60`, `keep_recent: 8`:

```
Before compression:                        After compression:

┌──────────────────────────┐              ┌──────────────────────────────┐
│ msg[0]  user             │              │ msg[0]  user (synthetic)     │
│ msg[1]  assistant        │              │   [rousseau-compressed]      │
│ msg[2]  user             │              │   (summary of prior 60       │
│  …  (60 messages)        │      →       │    messages): …              │
│ msg[59] assistant        │              ├──────────────────────────────┤
├──────────────────────────┤              │ msg[1]  user       — verbatim │
│ msg[60] user   verbatim  │              │ msg[2]  assistant  — verbatim │
│ msg[61] assistant        │              │ msg[3]  user       — verbatim │
│  …                       │              │ msg[4]  assistant  — verbatim │
│ msg[67] assistant        │              │ msg[5]  user       — verbatim │
└──────────────────────────┘              │ msg[6]  assistant  — verbatim │
                                          │ msg[7]  user       — verbatim │
                                          │ msg[8]  assistant  — verbatim │
                                          └──────────────────────────────┘
Total messages: 68                        Total messages: 9
Input tokens: ~5000 per turn              Input tokens: ~800 per turn
```

## Der Marker

Der Compressor präfixiert die synthetische Nutzernachricht mit `[rousseau-compressed]` (Konstante `DefaultCompressorMarker` in `internal/agent/compressor.go`). Bei nachfolgenden Turns verwendet `headAlreadyCompressed()` den Marker, um ein bereits komprimiertes Präfix zu erkennen, und überspringt die Wiederkomprimierung, es sei denn, die Sitzung ist auf `2 * trigger_messages` gewachsen.

Das ist es, was die Komprimierung begrenzt hält — Sie zahlen nicht dafür, die Zusammenfassung alle 60 Nachrichten neu zusammenzufassen.

## Werte wählen

| Situation | Empfohlen |
|---|---|
| Langlaufender Transport-Daemon bei einem kostenpflichtigen Provider. | `trigger_messages: 60`, `keep_recent: 8`. Die Defaults sind dafür abgestimmt. |
| Interaktives TUI, in dem Sie alles im Kontext haben möchten. | `enabled: false`. |
| Hochtechnische Sitzungen mit viel zitiertem Code / Logs. | `trigger_messages: 40`, `keep_recent: 12`. Bewahren Sie mehr aktuellen Kontext; komprimieren Sie früher. |
| Kostenkritischer Batch-Summariser (Cron). | Jeder Cron-Lauf ist eine frische Sitzung, also feuert Komprimierung selten. Lassen Sie die Defaults aktiviert. |

## Kosten eines Komprimierungsdurchlaufs

Ein Summarisation-Aufruf pro Feuerung. Der verwendete Provider ist der, den `Config.Provider` auswählt — derselbe, den der Agent verwendet. Das bedeutet:

- Sonnet-klassiger Compressor-Aufruf: ~1–2 Sekunden, ungefähr die Kosten von ~2 Turns an Input-Tokens.
- Break-even nach ~5–10 nachfolgenden Turns, abhängig von der Sitzungsform.

Für einen günstigeren Compressor betreiben Sie rousseau im Zwei-Daemon-Multi-Provider-Muster mit einem Haiku-klassigen Modell für den Compressor-Daemon. Siehe [Leitfäden: Multi-Provider](/de/guides/multi-provider/).

## Notfall: Sitzung ist zu groß zum Laden

Wenn die Payload einer Sitzung über das Kontextfenster des Modells hinauswächst, bevor die Komprimierung feuert — selten, aber möglich bei sehr kleinem `trigger_messages` und großen Tool-Ausgaben —, wird der nächste Turn mit einem „context length exceeded"-Fehler des Providers scheitern. Wiederherstellung:

```sh
rousseau session delete <id> --yes
```

Dann frisch beginnen. Oder manuell via SQLite verkleinern:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
UPDATE sessions SET payload = json_set(payload, '$.messages',
  json_extract(payload, '$.messages[-8:]'))
WHERE id = '<session-id>';
SQL
```

Hinweis: Die genaue JSON-Pfad-Syntax hängt von der SQLite-Version ab. Bestätigen Sie zuerst mit einem `SELECT payload`.

## Verwandt

- [Benutzerleitfaden: Komprimierung + Recall](/de/user-guide/compression-recall/) — tiefere Referenz.
- [Leitfäden: Rate-Limits](/de/guides/rate-limits/) — Kostenimplikationen.
- [Leitfäden: Sitzungsverwaltung](/de/guides/session-management/) — Sitzungs-Lebenszyklus.
- [Referenz: Konfigurationsschema](/de/reference/config-schema/) — jedes Feld.
