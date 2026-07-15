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
description: "How rousseau-agent handles provider rate limits: 429s, exponential backoff, prompt-cache markers, and per-provider cost notes."
keywords: "rate limits, 429, backoff, retry, prompt cache, anthropic, bedrock, cost"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/guides/rate-limits/"
subtitle: "429 handling, backoff, and cache-marker optimisation."
tags: "guides, rate limits, prompt cache, anthropic"
title: "Leitfaden: Ratenlimits"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "rate limits, 429, backoff, retry, prompt cache, anthropic, bedrock, cost"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Leitfaden: Ratenlimits"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 36
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/rate-limits/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/rate-limits/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Leitfaden: Ratenlimits"
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
twitter_description: "How rousseau-agent handles provider rate limits: 429s, exponential backoff, prompt-cache markers, and per-provider cost notes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Leitfaden: Ratenlimits"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Was Sie lernen werden</span><p>Provider-für-Provider-Rate-Limits, Kosten pro Token, Retry-Semantik, Cache-Ökonomie und ein Caller-seitiges Retry-with-Backoff-Rezept. Autoritative Zahlen finden Sie auf der Preisseite jedes Providers — die untenstehende Tabelle ist eine Momentaufnahme.</p></aside>

## Wo Rate-Limiting stattfindet

Rousseau implementiert keine eigene Rate-Limit-Handhabung. Jeder Provider-Client delegiert an das Upstream-SDK:

- **Anthropic direkt** — `anthropic-sdk-go` handhabt HTTP-Retries, respektiert `Retry-After`, wendet exponentielles Backoff bei 5xx und 429 an. Siehe `internal/llm/anthropic/client.go`.
- **Bedrock** — `aws-sdk-go-v2` behandelt Throttling-Fehler mit adaptiven Retries.
- **Vertex** — Google-Auth-Bibliotheken übernehmen ihre eigenen Retries.
- **OpenAI / OpenRouter / Ollama** — der Go-OpenAI-kompatible Client behandelt 429s.
- **claudecli** — das eigene `claude`-Binary von Claude Code handhabt Limits. Rousseau ruft es lediglich als Subprozess auf.

Fehlgeschlagene Anfragen erscheinen als `turn.failed`-, `whatsapp.handler_failed`- oder `cron.run_failed`-slog-Ereignisse. Der Nachrichtentext enthält den Fehlerstring des Providers (typischerweise `429 Too Many Requests` mit einem empfohlenen Backoff).

## Wenn Sie tatsächlich an ein Limit stoßen

Symptome in den Logs:

```jsonl
{"level":"ERROR","msg":"whatsapp.handler_failed","err":"anthropic: complete: 429 Too Many Requests"}
```

Weil rousseau einen Turn bei nicht behebbaren Fehlern als gescheitert behandelt, sieht der Operator den Fehler in der Transport-Antwort — der Daemon schluckt ihn nicht stillschweigend. Das ist beabsichtigt.

## Rate-Limit-Druck reduzieren

Drei Hebel, nach Wirkung geordnet:

### 1. Prompt-Cache-Marker (Anthropic direkt)

`applyCacheMarkers` in `internal/llm/anthropic/client.go` markiert ein führendes Fenster von Nachrichten für den ephemeren Prompt-Cache von Anthropic. Wenn `CacheableMessages > 0`, wird auch der System-Prompt cache-markiert. Cached-Input-Tokens werden mit ungefähr 10 % der Standard-Input-Raten abgerechnet, und Cache-Treffer verbrauchen nicht das Standard-Input-Rate-Limit-Budget.

Der Agent (`internal/agent/agent.go`) meldet sich für Multi-Turn-Sitzungen dafür an. Wenn Sie eigene Schleifen auf der Go-API von rousseau bauen, setzen Sie `Request.CacheableMessages` und `Request.System` — selbst ein flacher Cache-Treffer schneidet sowohl Kosten als auch Rate-Limit-Druck.

Cache-Marker sind heute nur Anthropic-direkt. Bedrock, Vertex und OpenAI-kompatible Provider ignorieren sie.

### 2. Komprimierung

Für lange Sitzungen bei einem Pay-per-Token-Provider (Anthropic direkt, Bedrock, Vertex, OpenRouter), aktivieren Sie Komprimierung:

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60      # from CompressionConfig default
    keep_recent: 8
```

Der `LLMCompressor` (`internal/agent/compressor.go`) fasst den ältesten Ausschnitt der Sitzung in eine einzelne synthetische Nutzernachricht zusammen, sobald die Nachrichtenzahl `trigger_messages` überschreitet, und bewahrt die letzten `keep_recent` Nachrichten wörtlich. Weniger Tokens pro Turn = weniger Rate-Limit-Druck.

Komprimierung ist standardmäßig ausgeschaltet, weil die Referenzbereitstellung `claudecli` auf einer Abonnementstufe verwendet, bei der die Token-Anzahl nicht abgerechnet wird.

### 3. Langsamere Cron-Kadenz

Für reine Hintergrund-Daemons halbiert eine halbierte Cron-Kadenz die Anfragen. `rousseau cron`-Kadenzen sind Cron-Ausdrücke — gehen Sie von alle 15 Minuten auf jede Stunde, wenn die Aktualitätsanforderung es erlaubt.

## Ungefähre Kosten pro Provider

Rate-Limits und Kosten pro Token bewegen sich unabhängig voneinander, sind aber in der Regel korreliert (kostenpflichtige Stufen haben höhere Limits). Grober Leitfaden Stand 2026-07:

| Provider | Input $/MTok (Sonnet-Klasse) | Output $/MTok | Cache-Read $/MTok |
|---|---|---|---|
| `anthropic` direkt | ~3 | ~15 | ~0,30 |
| `bedrock` (Sonnet-4.6) | ~3 | ~15 | Cache: zum Zeitpunkt der Erstellung nicht verfügbar |
| `vertex` (Anthropic auf Vertex) | ~3 | ~15 | Cache: zum Zeitpunkt der Erstellung nicht verfügbar |
| `openrouter` | modellabhängig | modellabhängig | providerabhängig |
| `ollama` selbst gehostet | $0 | $0 | $0 (Sie zahlen Compute) |
| `claudecli` | Abrechnung nach Abonnementstufe | inklusive | N/A |

Aktuelle Zahlen erhalten Sie von der Preisseite jedes Providers.

## Wenn das SDK die Retries erschöpft

Wenn das SDK des Providers aufgibt, gibt rousseau den finalen Fehler weiter. Der Turn ist verloren — es gibt keine Warteschlange und keinen On-Disk-Retry. Zwei Abhilfen:

- **Nachricht an den Operator über denselben Kanal.** Der Turn-Fehler ist in der Transport-Antwort sichtbar; der Operator kann umformulieren.
- **Manueller Fallback auf einen zweiten Provider.** Siehe [Leitfäden: Multi-Provider](/de/guides/multi-provider/) für das Zwei-Daemon-Muster.

Automatisches Cross-Provider-Failover ist ein Roadmap-Punkt.

## Rate-Limit-Probleme debuggen

1. Setzen Sie `log.level: debug` in `config.yaml`. Die SDK-Debug-Ausgabe zeigt den genauen `Retry-After`-Wert.
2. Suchen Sie im Journal nach `turn.failed`, `whatsapp.handler_failed`, `cron.run_failed`.
3. Prüfen Sie das Provider-Dashboard (Anthropic Console, AWS CloudWatch, GCP Cloud Monitoring) auf tatsächlichen Kontingentverbrauch.
4. Wenn Sie auf einer Abonnementstufe sind, achten Sie auf tägliche Kontingent-Resets — der SDK-Fehler enthält meist die Reset-Zeit.

## Provider-für-Provider-Kurzreferenz

<aside class="admonition" data-type="warning"><span class="admonition-title">Zitieren Sie Ihre Quellen</span><p>Preise und Limits ändern sich ohne Vorankündigung. Die Zahlen in dieser Tabelle stammen von Mitte 2026 und sind illustrativ. Verlinken Sie stets die aktuelle Preisseite des Providers für autoritative Werte.</p></aside>

| Provider | Retry-Verhalten | Rate-Signal | Kosten pro 1 Mio. Input | Kosten pro 1 Mio. Output | Cache-Read-Kosten |
|---|---|---|---|---|---|
| `anthropic` direkt | SDK retried 5xx; 429 mit `Retry-After` respektiert | `429 Too Many Requests`-Header trägt Reset-Zeit | ~$3 (Sonnet) | ~$15 (Sonnet) | ~$0,30 |
| `bedrock` | AWS-SDK adaptive Retry | `ThrottlingException` | ~$3 (Sonnet) | ~$15 (Sonnet) | noch nicht |
| `vertex` | Google-SDK exponentielle Retry | `429 RESOURCE_EXHAUSTED` | ~$3 (Sonnet) | ~$15 (Sonnet) | noch nicht |
| `openai` | SDK retried 5xx; 429 respektiert | `429 Too Many Requests` | modellspezifisch | modellspezifisch | modellspezifisch |
| `openrouter` | Passthrough zum darunterliegenden Provider | providerabhängig | modellspezifisch | modellspezifisch | providerabhängig |
| `ollama` | SDK retried; lokal, feuert also selten | keines | $0 (Compute-Kosten) | $0 (Compute-Kosten) | N/A |
| `claudecli` | Subprozess-Fehler tauchen auf; kein rousseau-seitiger Retry | opak | Abonnement | Abonnement | opak |

Autoritative Quellen:

- [Anthropic-Preise](https://www.anthropic.com/pricing)
- [AWS-Bedrock-Preise](https://aws.amazon.com/bedrock/pricing/)
- [Vertex-AI-Preise](https://cloud.google.com/vertex-ai/generative-ai/pricing)
- [OpenAI-Preise](https://openai.com/pricing)
- [OpenRouter-Modellliste](https://openrouter.ai/models)

## Caller-seitiges Retry-Rezept

Rousseau retried nicht innerhalb von `Complete`. Wenn Sie die Agent-Bibliothek einbetten, wickeln Sie `Turn` in Ihre eigene Retry-Schleife mit exponentiellem Backoff und Jitter:

```go
func retryTurn(ctx context.Context, ag *agent.Agent, sess *agent.Session, maxRetries int) (agent.Message, error) {
    var lastErr error
    for attempt := 0; attempt < maxRetries; attempt++ {
        m, err := ag.Turn(ctx, sess)
        if err == nil {
            return m, nil
        }
        if !isRateLimit(err) {
            return agent.Message{}, err // non-retryable
        }
        lastErr = err
        // Exponential backoff with jitter: 1s, 2s, 4s, 8s, ...
        backoff := time.Duration(1<<attempt) * time.Second
        jitter := time.Duration(rand.Int63n(int64(backoff / 2)))
        select {
        case <-time.After(backoff + jitter):
        case <-ctx.Done():
            return agent.Message{}, ctx.Err()
        }
    }
    return agent.Message{}, fmt.Errorf("giving up after %d retries: %w", maxRetries, lastErr)
}

func isRateLimit(err error) bool {
    s := err.Error()
    return strings.Contains(s, "429") || strings.Contains(s, "rate limit") || strings.Contains(s, "ThrottlingException")
}
```

## Fehlerbehebung

### `429 Too Many Requests` bei jeder Anfrage

Sie sind auf einer niedrigen Stufe, oder eine andere Workload verbraucht das Kontingent. Optionen: (1) eine Limit-Erhöhung anfordern, (2) Last auf Provider aufteilen, (3) `claudecli` für Abonnement-only-Workloads betreiben.

### `529 Overloaded` intermittierend

Das System von Anthropic ist an der Kapazitätsgrenze. Kein per-Account-Throttling — die gesamte Region ist ausgelastet. Retry mit Backoff.

### Cache-Marker gesetzt, aber keine sichtbare Kostenersparnis

Verifizieren Sie, dass `CacheableMessages` tatsächlich gesetzt ist. `applyCacheMarkers` in `internal/llm/anthropic/cache.go` ist bei null ein No-Op. Verifizieren Sie auch, dass das Präfix stabil ist — ein System-Prompt, der pro Turn neu generiert wird, unterläuft das Caching.

### `ThrottlingException` bei Bedrock mit geringem Volumen

Das Bedrock-Kontingent ist pro Account, pro Modell und pro Region. Einige Modelle haben standardmäßig sehr niedrige Kontingente (2–5 Anfragen pro Minute). Fordern Sie eine Erhöhung in der Service-Quotas-Konsole an.

### Langsame API-Antworten trotz geringer Nutzung

Einige Provider depriorisieren Konten niedriger Stufen unter globaler Last. Die `x-ratelimit-*`-Response-Header von Anthropic zeigen den aktuellen Bucket-Zustand — inspizieren Sie sie, wenn Sie SDK-Zugriff haben.

## Verwandte Seiten

- [Provider: Anthropic](/de/providers/anthropic/) — Cache-Marker-Details.
- [Konfiguration](/de/configuration/) — jeder Komprimierungsknopf.
- [Benutzerleitfaden: Komprimierung + Recall](/de/user-guide/compression-recall/) — tiefere Komprimierungsdiskussion.
- [Leitfäden: Multi-Provider](/de/guides/multi-provider/) — Last auf Endpunkte aufteilen.
- [Leitfäden: Rate/Modell-Swap](/de/guides/rate-model-swap/) — Provider bei Ausfall hot-swappen.

## Weiterführende Lektüre

- `internal/llm/anthropic/client.go` — SDK-Aufruf.
- `internal/llm/anthropic/cache.go` — Cache-Marker-Helfer.
- `internal/agent/agent.go` — wo Turn-Fehler zutage treten.
- Provider-Preisseiten oben verlinkt.
