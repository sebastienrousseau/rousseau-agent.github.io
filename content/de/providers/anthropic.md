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
description: "Configure the direct Anthropic provider: ANTHROPIC_API_KEY, model IDs, max_tokens, prompt cache markers on the last messages, streaming."
keywords: "Anthropic, ANTHROPIC_API_KEY, Claude API, prompt caching, cache_control, ephemeral, streaming"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/providers/anthropic/"
subtitle: "Direct Anthropic API with ephemeral prompt-cache markers."
tags: "providers, anthropic"
title: "Anthropic-Anbieter"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Anthropic, ANTHROPIC_API_KEY, Claude API, prompt caching, cache_control, ephemeral, streaming"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Anthropic-Anbieter"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 7
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/anthropic/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/anthropic/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Anthropic-Anbieter"
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
twitter_description: "Configure the direct Anthropic provider: ANTHROPIC_API_KEY, model IDs, max_tokens, prompt cache markers on the last messages, streaming."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Anthropic-Anbieter"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Was Sie lernen</span><p>Die exakte Wire-Level-Form der Anthropic-Requests, die rousseau sendet, welche Content-Blöcke Prompt-Cache-Markierungen erhalten und warum, wie Streaming auf <code>agent.StreamingProvider</code> abgebildet wird und die Fehlermodi für 401/429/529-Antworten. Lesen Sie <code>internal/llm/anthropic/client.go</code> und <code>internal/llm/anthropic/cache.go</code> parallel zu dieser Seite.</p></aside>

## Wann den Anthropic-Provider verwenden

Der direkte `anthropic`-Provider ist die richtige Wahl, wenn:

- Sie einen Anthropic-API-Key haben und Pro-Token-Billing auf `api.anthropic.com` wünschen.
- Sie rousseau-seitige Tool-Ausführung wollen (die `Registry` ist voll im Einsatz).
- Sie ephemere Prompt-Cache-Markierungen für stabile Präfixe nutzen wollen.
- Sie Streaming-Completions in `rousseau chat` wollen (Token-für-Token-Viewport-Updates).
- Sie explizite, veröffentlichte Rate-Limits wollen (im Gegensatz zum `claudecli`-Abonnement-Modus).

## Konfiguration

```yaml
provider: anthropic

anthropic:
  api_key: sk-ant-...
  model: claude-sonnet-4-6
  max_tokens: 4096
```

| Feld | Standard | Wirkung |
|---|---|---|
| `api_key` | *aus `ANTHROPIC_API_KEY`* | Bearer-Token für `api.anthropic.com`. Wird abgelehnt, wenn bei ausgewähltem Provider leer. |
| `model` | `claude-sonnet-4-6` | Modell-ID. |
| `max_tokens` | `4096` | Begrenzt Ausgabe-Tokens pro Completion. |

Die Umgebungsvariable `ANTHROPIC_API_KEY` wird beim Laden an `anthropic.api_key` gebunden, weshalb das Exportieren dem Konfigurieren gleichkommt. Container-Betreiber exportieren sie typischerweise in der `Environment=`-Zeile der systemd-Unit, statt sie in `config.yaml` einzuchecken.

## Modell-IDs

`rousseau-agent` übergibt `model` wortgetreu an das SDK. Pinnen Sie die exakte Modell-ID (`claude-sonnet-4-6`, `claude-opus-4-6`) in Produktion, damit Ihr Traffic sich nicht unter Ihnen verschiebt, wenn Anthropic neue Snapshots ausrollt.

## Prompt-Caching-Interna

Der ephemere Prompt-Cache von Anthropic erlaubt es, Content-Blöcke mit `cache_control: { type: "ephemeral" }` zu markieren. Die API cached das Präfix bis einschliesslich jedes cache-markierten Blocks; folgende Turns, die dasselbe Präfix mitführen, zahlen einen Bruchteil der üblichen Input-Token-Kosten (10% zum Zeitpunkt der Erstellung – prüfen Sie die Anthropic-Dokumentation für aktuelle Preise).

Rousseau setzt Markierungen über `applyCacheMarkers` in `internal/llm/anthropic/cache.go`. Zwei Dinge passieren, wenn `CacheableMessages > 0` im ausgehenden `Request` ist:

1. **Der System-Prompt erhält `cache_control: ephemeral`.** Er überlebt jeden Turn, weshalb Caching sich immer lohnt, sobald Sie einsteigen. Siehe Zeilen 68–75 von `internal/llm/anthropic/client.go`.
2. **Die letzten `CacheableMessages`-Nachrichten** erhalten `cache_control: ephemeral` auf ihrem letzten Textblock. Das hält eine wachsende Sitzung günstig: Mit neuen Turns wandert die Markierung durch das Transkript, aber das Präfix bis zur vorherigen Markierung bleibt heiss.

### Welche Blöcke werden markiert

`markLastTextBlock` läuft den Content eines `MessageParam` rückwärts und setzt `CacheControl` auf dem ersten gefundenen Textblock. `tool_use`- und `tool_result`-Blöcke werden übersprungen – das SDK modelliert sie als andere Varianten mit eigenen optionalen `CacheControl`-Feldern, und Text ist der sichere gemeinsame Nenner. Siehe `internal/llm/anthropic/cache.go`.

### Wann es sich lohnt

<aside class="admonition" data-type="note"><span class="admonition-title">Caching-Ökonomie</span><p>Der Break-Even-Punkt hängt davon ab, wie oft das gecachte Präfix wiederverwendet wird. Für einen Chat-Transport mit 20–100 Turns pro Sitzung und einem 5–10 kB grossen System-Prompt (typisch mit geladenen Skills) halbiert Caching typischerweise die Input-Token-Rechnung. Für einen einmaligen Cron-Job, der eine einzelne Antwort erzeugt, spart es nichts.</p></aside>

Der `Compressor` setzt `CacheableMessages = len(recentMessages) - 1` nach einer Umschreibung, damit der frische Zusammenfassungs-Block bereits im nächsten Turn cache-heiss ist. Andere Codepfade lassen `CacheableMessages = 0`, wodurch Caching pro Request opt-in ist. Embedders sollten es explizit setzen, wenn sie den Provider direkt aufrufen.

### Cache-Treffer verifizieren

Die Anthropic-API liefert `usage.cache_read_input_tokens` und `usage.cache_creation_input_tokens` in jeder Antwort. `agent.Usage` exponiert derzeit nur `InputTokens` und `OutputTokens`, weshalb das Verifizieren des Splits entweder Debug-Logging aktivieren oder die rohe SDK-Antwort lesen erfordert – dies ist eine bekannte Observability-Lücke, die in `docs/GAP_ANALYSIS_2026.md` verfolgt wird.

## Streaming-Semantik

Der Provider implementiert `agent.StreamingProvider`. `rousseau chat` nutzt Streaming standardmässig, damit Tokens im TUI-Viewport erscheinen, sobald sie ankommen. Chat-Transports (WhatsApp, Slack, Discord, …) nutzen nicht-streamende Completions, weil nachrichtenorientierte Transports die Zustellung ohnehin bündeln – ein zwischenzeitlicher Delta-Stream würde vor dem Versand der finalen Nachricht verworfen.

Die Streaming-Implementierung in `internal/llm/anthropic/stream.go` konsumiert den `MessageStreamEvent`-Union-Typ des SDKs:

| Event | Wie behandelt |
|---|---|
| `message_start` | Emittiert `agent.StreamEvent{Kind: StreamMessageStart}`. |
| `content_block_start` | Emittiert `agent.StreamEvent{Kind: StreamContentStart}` mit dem Block-Typ. |
| `content_block_delta` | Emittiert `agent.StreamEvent{Kind: StreamTextDelta, Text: delta.Text}` für Text; `input_json_delta`-Ereignisse akkumulieren in einem partiellen Tool-Use-Input. |
| `content_block_stop` | Emittiert `agent.StreamEvent{Kind: StreamContentStop}`. |
| `message_delta` | Trägt den finalen Stop-Reason und die kumulative Nutzung. |
| `message_stop` | Ende des Streams. |

Die Bubble-Tea-TUI abonniert diese Ereignisse über `agent.StreamTurn`, das die Stream-/Tool-Use-Schleife orchestriert. Siehe `internal/agent/stream_turn.go`.

## Tool-Use

Tool-Definitionen aus der `Registry` werden in `toSDKTools` in Anthropics `tools`-Array konvertiert. Approval-Richtlinien (`agent.approver`) greifen – jeder `tool_use`-Block durchläuft `Approver.Approve` in der Agent-Schleife vor der Ausführung. Ablehnungen werden dem Modell als `tool_result`-Blöcke mit `is_error: true` zurückgemeldet, damit es reagieren kann (andere Aktion wählen, Benutzer fragen, gepflegt aufgeben).

<aside class="admonition" data-type="warning"><span class="admonition-title">Schema-Form</span><p>Das SDK erwartet, dass das <code>input_schema</code> des Tools ein JSON-Schema-Objekt mit einem Top-Level-Feld <code>properties</code> ist. Die <code>tools.Definition</code> von rousseau bildet 1:1 darauf ab – siehe <code>toSDKTools</code> in <code>internal/llm/anthropic/client.go</code>. Custom-Tools, die keine Objekt-Schemas emittieren, schlagen zur Request-Zeit fehl.</p></aside>

## Rate-Limit-Behandlung

Die Anthropic-API gibt zurück:

| Code | Bedeutung | rousseaus Verhalten |
|---|---|---|
| 401 | Falscher oder fehlender Key | Schlägt sofort fehl, kein Retry. |
| 400 | Ungültige Anfrage (Schema, Encoding, Prompt zu lang) | Schlägt sofort mit der Fehlermeldung des SDKs fehl. |
| 429 | Pro-Minute-Rate-Limit überschritten | Wird als `agent`-Fehler gemeldet. `Complete` wiederholt nicht. |
| 529 | Überlastet (transiente Kapazität) | Wird als `agent`-Fehler gemeldet. `Complete` wiederholt nicht. |
| 5xx | Serverfehler | Wird als `agent`-Fehler gemeldet. `Complete` wiederholt nicht. |

**Retries liegen in der Verantwortung des Aufrufers.** Die `rousseau chat`-TUI und der Transport-`RouterHandler` implementieren derzeit keinen Backoff – ein 429 beendet den Turn. Dies ist eine bewusste Design-Entscheidung: Retries interagieren mit Tool-Use-Semantik (partielle Tool-Aufrufe, Idempotenz), und der Aufrufer hat den Kontext, die richtige Entscheidung zu treffen. Siehe `docs/GAP_ANALYSIS_2026.md` für den geplanten Retry-Helper.

<aside class="admonition" data-type="tip"><span class="admonition-title">429 in einem Chat-Transport behandeln</span><p>Kapseln Sie den Transport-<code>RouterHandler</code> in einer aufruferseitigen Retry-Schleife mit exponentiellem Backoff und Jitter. Der <a href="/de/guides/rate-limits/">Rate-Limits-Guide</a> zeigt ein durchgearbeitetes Beispiel.</p></aside>

## Kosten-Hygiene

- **`max_tokens` niedrig setzen** (2048–4096) für Chat-Transports, in denen Antworten selten mehr als ein paar Absätze benötigen. `max_tokens` ist ein Deckel, kein Ziel – Sie zahlen nur für tatsächlich erzeugten Output.
- **`agent.compression` aktivieren**, um alte Nachrichten zu komprimieren, sobald das Transkript `trigger_messages` (Standard 60) überschreitet. Die Zusammenfassung ist deutlich billiger als das rohe Transkript.
- **`CacheableMessages > 0` nutzen**, wenn Sie die Agent-Bibliothek einbetten – die direkte API ist der Ort, an dem sich Prompt-Caching am meisten auszahlt.
- **Sonnet für Tool-Use-Schleifen bevorzugen.** Opus ist teurer und langsamer; solange Sie keine gemessenen Vorteile für Ihre spezifische Aufgabe haben, ist Sonnet aus gutem Grund der Standard.
- **Achten Sie auf Abrechnung bei Stream-Abbrüchen.** Wenn ein Stream mitten in der Antwort abgebrochen wird, berechnet die API dennoch die bis zum Abbruch erzeugten Tokens. Setzen Sie im Aufrufer eine Timeout-Obergrenze.

## Fehlerbehebung

### `anthropic: complete: 401 unauthorized`

Ihr `ANTHROPIC_API_KEY` fehlt, wurde widerrufen oder ist für einen Workspace/eine Organisation gesetzt, auf die Sie keinen Zugriff mehr haben. Verifizieren mit `curl -H "x-api-key: $ANTHROPIC_API_KEY" https://api.anthropic.com/v1/messages`.

### `anthropic: complete: 400 messages: too many messages`

Das Transkript ist über das Kontextfenster hinausgewachsen. Aktivieren Sie `agent.compression.enabled: true` (Standardwerte sind meist gut) und wiederholen. Wenn Kompression aktiv ist und dennoch feuert, senken Sie `trigger_messages` oder erhöhen Sie `keep_recent`, damit der Kompressor früher auslöst.

### `anthropic: unsupported content block <type>`

Das SDK hat einen Content-Block-Typ zurückgegeben, den rousseau nicht modelliert – derzeit werden nur `text` und `tool_use` unterstützt (siehe `fromSDKResponse`). Dies kann passieren, wenn das Modell `thinking`-Blöcke emittiert (Extended-Thinking-Modus). rousseau exponiert diese noch nicht; deaktivieren Sie Extended Thinking in Ihrer Provider-Config, bis Unterstützung eintrifft.

### 429s unter Dauerlast

Sie erreichen das pro-Minute-Output-Token-Rate-Limit. Optionen: (1) Anfrage einer Limit-Erhöhung bei Anthropic, (2) Turns im Aufrufer serialisiert in eine Warteschlange, (3) Wechsel zu Bedrock oder Vertex, wo Enterprise-Quoten meist höher sind.

### Prompt-Cache-Misses trotz `CacheableMessages > 0`

Anthropic invalidiert den Cache, wenn sich das Präfix ändert. Häufige Ursachen: Der System-Prompt wird pro Turn neu generiert (Skills, die sich mit jeder Benutzernachricht verschieben), die Modell-ID hat sich geändert oder `MaxTokens` unterscheidet sich. Loggen Sie den Request-Payload und diff'en Sie über zwei Turns, um dies zu isolieren.

## Verwandte Seiten

- [Providers: claudecli](/de/providers/claudecli/) – Subprozess vs. direkte API im Trade-off.
- [Providers: Bedrock](/de/providers/bedrock/) – AWS-verwaltetes Claude mit Enterprise-Quoten.
- [Guides: Rate-Limits](/de/guides/rate-limits/) – der Retry-und-Backoff-Playbook.
- [Agent-Loop](/de/agent-loop/) – wie Streaming und Tool-Use komponiert werden.
- [Benutzerhandbuch: Kompression &amp; Recall](/de/user-guide/compression-recall/) – der Mechanismus, der Input-Token-Zahlen im Rahmen hält.

## Weiterführende Lektüre

- `internal/llm/anthropic/client.go` – `Complete`, Nachrichtenkonvertierung, Tool-Schema.
- `internal/llm/anthropic/stream.go` – Streaming-Implementierung.
- `internal/llm/anthropic/cache.go` – Helfer für Cache-Marker.
- `internal/agent/stream_turn.go` – wie die Agent-Schleife Streaming-Ereignisse konsumiert.
- `internal/agent/compressor.go` – wie der Kompressor `CacheableMessages` vorbereitet.
