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
description: "Session compression triggers and FTS5 cross-session recall in rousseau-agent. How the agent loop keeps long sessions inside the model's context."
keywords: "compression, recall, fts5, session, context window, summarisation, trigger_messages, keep_recent"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/user-guide/compression-recall/"
subtitle: "Session compression and FTS5 cross-session recall."
tags: "compression, recall, session, fts5"
title: "Kompression + Recall"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "compression, recall, fts5, session, context window, summarisation, trigger_messages, keep_recent"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Kompression + Recall"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "concepts"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/compression-recall/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/compression-recall/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Kompression + Recall"
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
twitter_description: "Session compression triggers and FTS5 cross-session recall in rousseau-agent. How the agent loop keeps long sessions inside the model's context."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Kompression + Recall"
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

## Zwei Probleme, zwei Mechanismen

- Eine einzelne lange Sitzung kann das Kontextfenster des Modells überwachsen. **Kompression** kollabiert alte Nachrichten zu einem Summary-Block, damit die Schleife weiter funktioniert.
- Eine neue Sitzung zu einem verwandten Thema verliert den Wert vorheriger Konversationen. **Recall** fragt den FTS5-Index sitzungsübergreifend ab und fügt Auszüge in den System-Prompt ein.

Kompression bearbeitet die aktuelle Sitzung in-place. Recall bearbeitet nie – es hängt Kontext für den aktuellen Turn an den System-Prompt an.

## Kompression

`internal/agent/compressor.go` implementiert einen LLM-gestützten Zusammenfasser. Die Agent-Schleife konsultiert ihn zu Beginn jedes `Turn`:

```go
if changed, err := a.opts.Compressor.Compress(ctx, s); err != nil {
    a.logger.Warn("agent.compress_failed", slog.String("err", err.Error()))
} else if changed {
    a.logger.Info("agent.compressed", slog.Int("messages", len(s.Messages)))
}
```

Wenn die Sitzung kurz ist, passiert nichts. Sobald die Nachrichtenanzahl `trigger_messages` überschreitet, wird der Compressor:

1. Isoliert das Ende der Sitzung – die neuesten `keep_recent` Nachrichten – und bewahrt sie wortwörtlich.
2. Speist alles Ältere an den Provider mit einem Zusammenfassungs-Prompt.
3. Ersetzt den älteren Block durch eine einzige synthetische `RoleSystem`-Nachricht mit der Zusammenfassung.
4. Markiert die Sitzung so, dass der Summary-Block im prompt-cache-fähigen Präfix beim allernächsten Provider-Aufruf sitzt.

Die Schleife läuft dann gegen die kleinere Nachrichtenliste weiter. Der Benutzer sieht die Naht nie.

### Kompression aktivieren

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60      # null → Standardwert 60
    keep_recent: 8            # null → Standardwert 8
    prompt: ""                # null → sinnvoller Standardwert
```

| Feld | Standardwert | Bedeutung |
|---|---|---|
| `enabled` | `false` | Standardmäßig aus. |
| `trigger_messages` | 60 | Nachrichtenanzahl, über der Kompression feuert. |
| `keep_recent` | 8 | Wie viele neuere Nachrichten wortwörtlich bewahrt werden. |
| `prompt` | eingebaut | Überschreibt die Zusammenfassungs-Anweisung. |

### Wann ausgeschaltet lassen

Kompression verwendet einen Provider-Roundtrip pro Feuerung. Auf einem `claudecli`-Abonnement-Konto ist dieser Trip kostenlos – frei aktivieren. Auf einer Pay-per-Token-API hat jede Feuerung Kosten, also justieren Sie `trigger_messages` nach oben oder lassen es für kurzlebige Sitzungen deaktiviert.

### Wann eingeschaltet lassen

- Langlebige Chat-Transport-Daemons, bei denen ein WhatsApp-Thread über Wochen wächst.
- Cron-geplante Prompts, deren Antworten einen Folge-Prompt speisen.
- Selbstgehostete Provider, bei denen die Token-Kosten null sind.

### Über Kompression hinweg bewahrte Semantik

- Tool-Use-/Tool-Result-Paare werden nie geteilt. Wenn ein `tool_use` im komprimierten Bereich und sein `tool_result` im bewahrten Bereich liegt, werden beide in die Zusammenfassung kollabiert.
- Der Compressor schreibt niemals den aktuellen in-flight-Benutzer-Turn um.
- Prompt-Caching (`internal/llm/anthropic` `cache_control`-Marker) wird auf den Summary-Block gesetzt, damit der nächste Aufruf ihn aus dem Cache liest.

## Recall

`internal/state/sqlite/` pflegt eine FTS5-Virtual-Table, die jede Nachricht indiziert. Ein `RecallProvider` führt eine Abfrage gegen diese Tabelle aus und liefert eine System-Prompt-Ergänzung zurück.

### Die Schnittstelle

```go
type RecallProvider interface {
    SystemAppendix(ctx context.Context, s *Session) string
}
```

Die Agent-Schleife ruft dies einmal pro Iteration auf. Wenn er nicht-leeren Text zurückgibt, wird der Text für diese Iteration an den Basis-System-Prompt angehängt.

### Der Standard-Provider

`internal/agent/recall.go` liefert eine Heuristik, die:

1. Salientes Tokens aus der letzten Benutzer-Nachricht der aktuellen Sitzung extrahiert.
2. `MATCH` gegen den FTS5-Index für diese Tokens sitzungsübergreifend ausführt.
3. Die Top-N-Auszüge als `Previously in another session:`-Block formatiert.
4. Die Ergänzung begrenzt, damit sie ein konfiguriertes Zeichenbudget nie überschreitet.

### Recall aktivieren

Recall wird bei der Agent-Konstruktion verdrahtet. Siehe `internal/cli/chat.go` und `internal/cli/*.go`, wie jeder Transport ihn verdrahtet. In Ihrer eigenen Einbettung:

```go
recall, err := sqlitestore.NewRecall(store)
if err != nil { /* ... */ }

ag := agent.New(provider, registry, logger, agent.Options{
    RecallProvider: recall,
})
```

### Interaktion mit dem Approver

Recall liest aus dem Sitzungsspeicher; er feuert nie einen Tool-Aufruf. Der Approver wird nicht konsultiert. Die Store-Inhalte selbst sind die Vertrauensgrenze.

### Sitzungssuche aus der CLI

Recall ist ein maschinenseitiges Feature. Für Menschen wird derselbe FTS5-Index angetrieben von:

```sh
rousseau session search "kubectl"
rousseau session search "PVC not binding"
```

Gleiche Abfrage-Engine, gleiche Ergebnisse, minus das LLM-Re-Ranking, das ein richtiger RecallProvider hinzufügen könnte.

## Interaktion mit Skills

Skills ([Skills](/de/skills/)) und Recall fügen beide dem System-Prompt etwas hinzu. Sie werden in einer festen Reihenfolge zusammengesetzt:

1. Basis-System-Prompt (aus `agent.system_prompt` oder dem Standardwert).
2. Skills-Ergänzung (falls vorhanden).
3. Recall-Ergänzung (falls vorhanden).

Alles wird durch zwei Zeilenumbrüche getrennt. Wenn nichts hinzugefügt werden muss, geht der Basis-Prompt unverändert durch.

## Semantik des Summary-Blocks

Die synthetische Zusammenfassungs-Nachricht wird mit `RoleSystem` ausgegeben. Sie ist keine Benutzer- oder Assistenten-Nachricht, sodass sie in `rousseau session show` nie als Konversations-Turn erscheint – sie zeigt sich als `[compressed summary]`-Metadaten.

Wenn Sie eine komprimierte Sitzung mit `rousseau chat --session <id>` fortsetzen, bleibt die Zusammenfassung erhalten. Das Löschen des Summary-Blocks über eine hypothetische Schema-Bearbeitung ist unsicher: Das Modell könnte auf Fakten verweisen, die nur durch ihn bekannt sind.

## Verifizieren, dass Kompression feuert

```
INFO agent.compressed messages=12
```

`messages` ist die neue Sitzungslänge, nachdem der Summary-Block das komprimierte Präfix ersetzt hat. Ein `WARN agent.compress_failed err=...` bedeutet, dass der Zusammenfassungs-Provider einen Fehler hatte; die Schleife setzte gegen die unkomprimierte Sitzung fort.

## Vorbehalte

- Kompression ist verlustbehaftet. Die Zusammenfassung ist modell-generierter Text; wichtige Details können wegfallen. Für Audit-Trails behalten Sie die vollständige Sitzung im Speicher – Kompression betrifft nur, was das Modell sieht, nicht, was SQLite persistiert.
- Recall benötigt die FTS5-SQLite-Erweiterung. `modernc.org/sqlite` baut sie standardmäßig ein; wenn Sie die Store-Implementierung austauschen, stellen Sie sicher, dass FTS5 verfügbar ist.
- Beide Features setzen UTF-8-Text voraus. Sprachnachrichten-Transkripte (siehe [Sprachmodus](/de/user-guide/voice-mode/)) zählen nach der Transkription als reguläre Benutzer-Nachrichten.

## Weiter

- [Konzepte](/de/concepts/) — die Übersicht der Agent-Schleife.
- [Konfiguration](/de/configuration/) — jeder `agent.compression.*`-Knopf.
- [Skills](/de/skills/) — die dritte System-Prompt-Eingabe.
