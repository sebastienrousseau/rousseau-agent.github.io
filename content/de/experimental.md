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
description: "Off-by-default rousseau-agent behaviour: voice mode via whisper.cpp, FTS5 recall, LLM compression, and other opt-in surface."
keywords: "experimental, voice, whisper, fts5, compression, opt-in, feature flag"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/experimental/"
subtitle: "Verhalten, das standardmäßig deaktiviert ist — und warum."
tags: "experimental, opt-in, voice, compression, fts5"
title: "Experimentell"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "experimental, voice, whisper, fts5, compression, opt-in, feature flag"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Experimentell"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "system"
order: 60
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/experimental/index.html"
item_link: "https://docs.rousseau-agent.dev/experimental/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Experimentell"
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
twitter_description: "Off-by-default rousseau-agent behaviour: voice mode via whisper.cpp, FTS5 recall, LLM compression, and other opt-in surface."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Experimentell"
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

## Was "experimentell" hier bedeutet

Rousseaus Standardhaltung ist minimal: ein statisches Go-Binary, eine SQLite-Datei, keine externen Abhängigkeiten. Jedes Feature, das eine zusätzliche Laufzeit (`whisper.cpp`), zusätzlichen Zustand (FTS5-Index für Recall) oder zusätzliche Provider-Kosten (LLM-gestützte Kompression) benötigt, ist Opt-in.

Keines davon ist instabil. Sie werden ausgeliefert, haben Tests und werden unterstützt. Aber weil sie die Betriebskosten oder die Angriffsfläche ändern, sind sie standardmäßig aus – Sie schalten diejenigen ein, die Sie benötigen.

## Sprachmodus (whisper.cpp)

Standardmäßig aus, weil er die Installation des `whisper`-Binaries aus whisper.cpp auf dem Daemon-Host erfordert.

**Umschalter:** `whatsapp.voice.enabled: true` in `config.yaml`. Siehe `VoiceConfig` in `internal/config/config.go`.

**Was es tut.** Wenn WhatsApp eine Sprachnachricht liefert, lädt der whatsmeow-Client die OGG-Nutzlast herunter, ruft `whisper` mit dem konfigurierten Modell auf und behandelt das Transkript als Text der eingehenden Nachricht. Strukturierte Log-Ereignisse (`internal/transport/whatsapp/dispatch.go`):

- `whatsapp.audio_downloaded size=N`
- `whatsapp.transcribed elapsed=N`

**Warum es aus ist.** Zwei Gründe: (1) eine frische Installation würde verwirrend fehlschlagen, wenn das `whisper`-Binary fehlt, (2) Transkription ist eine Echtzeit-CPU-Ausgabe, die die meisten Operatoren aktiv wählen würden, statt sie überraschend zu erhalten.

Siehe [Benutzerleitfaden: Sprachmodus](/de/user-guide/voice-mode/) für die vollständige Einrichtung.

## FTS5-Recall

**Umschalter.** Standardmäßig aktiviert, aber nur von Tools genutzt, die danach fragen. Der FTS5-Index wird unabhängig davon aufgebaut und gepflegt (`EnsureSearch` in `internal/state/sqlite/search.go`); das "Opt-in" ist, ob der Agent das Modell auffordert, ihn zu durchsuchen.

**Was es tut.** SQLite-FTS5-Volltextindex über jede gespeicherte Sitzung. Angetrieben durch `rousseau session search`, das MCP-Tool `rousseau_search_sessions`, und (wenn der Agent mit einem Recall-Searcher konfiguriert ist) kann das Modell ihn mitten im Turn abfragen.

**Warum es so strukturiert ist.** Der Index ist günstig zu pflegen – die Trigger in `internal/state/sqlite/search.go` erledigen das –, aber ihn dem Modell bei jedem Turn zu exponieren hat einen Preis. Er wird nur eingebunden, wenn die Agent-Schleife mit einem `RecallSearcher` (`internal/state/sqlite/recall.go`) konstruiert wird.

Siehe [Benutzerleitfaden: Kompression + Recall](/de/user-guide/compression-recall/).

## LLM-gestützte Kompression

Standardmäßig aus, weil sie Tokens kostet.

**Umschalter:** `agent.compression.enabled: true`. Vollständige Feldliste im [Leitfaden: Kontext-Verwaltung](/de/guides/context-management/).

**Was es tut.** Wenn eine Sitzung über `trigger_messages` (Standard 60) hinauswächst, fasst der `LLMCompressor` (`internal/agent/compressor.go`) den ältesten Abschnitt in einer synthetischen Benutzernachricht zusammen und behält die neuesten `keep_recent` Nachrichten wortwörtlich bei. Jeder nachfolgende Turn ist kleiner und günstiger.

**Warum es aus ist.** Die Referenzbereitstellung führt `claudecli` auf einer Abonnement-Ebene aus, bei der die Token-Anzahl nicht abgerechnet wird. Kompression zahlt sich bei Anthropic direkt, Bedrock, Vertex und OpenAI-kompatiblen Providern aus.

## OpenRouter- und Ollama-Basis-URLs (vorkonfiguriert, weiterhin Opt-in)

Nicht streng experimentell, aber erwähnenswert: Rousseaus `setDefaults` in `internal/config/config.go` konfiguriert die Basis-URLs von OpenRouter und Ollama vor:

- `openrouter.base_url: https://openrouter.ai/api/v1`
- `ollama.base_url: http://localhost:11434/v1`
- `ollama.api_key: not-required`

Die Auswahl dieser Provider ist Opt-in via `provider: openrouter` / `provider: ollama` – die Endpunkte sind nur vorbelegt, damit Sie sie nicht auswendig lernen müssen.

## Prompt-Injection-Erkennung (Roadmap)

Nicht ausgeliefert. Siehe [Leitfäden: Prompt Injection](/de/guides/prompt-injection/) für das ehrliche Bedrohungsmodell. Die Abwehr ist heute vollständig approver-basiert; klassifikatorbasierte Erkennung ist ein Roadmap-Punkt, der auf Forschung wartet, die tatsächlich funktioniert.

## Streaming zu Nicht-Anthropic-Providern (teilweise)

Der Anthropic-Provider (`internal/llm/anthropic/client.go`) unterstützt die Streaming-Schnittstelle des SDK. Andere Adapter laufen derzeit im Non-Streaming-Modus. Streaming über alle Adapter hinweg ist ein geplanter Vereinheitlichungsdurchgang.

## Verwandt

- [Konfiguration](/de/configuration/) — jeder Konfigurationsknopf.
- [Benutzerleitfaden: Sprachmodus](/de/user-guide/voice-mode/).
- [Leitfäden: Kontext-Verwaltung](/de/guides/context-management/) — Kompressions-Tiefeneinblick.
- [Referenz: Sitzungsspeicher](/de/reference/session-store/) — FTS5-Schema.
