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
description: "Worked example: point rousseau-agent at a self-hosted vLLM endpoint on your internal network via the OpenAI-compatible provider."
keywords: "vllm, self-hosted, openai-compatible, air-gapped, internal network, local llm"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/guides/self-hosted-vllm/"
subtitle: "Point rousseau at a vLLM endpoint on your internal network."
tags: "guides, vllm, self-hosted, openai-compatible"
title: "Leitfaden: selbstgehostetes vLLM"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "vllm, self-hosted, openai-compatible, air-gapped, internal network, local llm"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Leitfaden: selbstgehostetes vLLM"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 32
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/self-hosted-vllm/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/self-hosted-vllm/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Leitfaden: selbstgehostetes vLLM"
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
twitter_description: "Worked example: point rousseau-agent at a self-hosted vLLM endpoint on your internal network via the OpenAI-compatible provider."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Leitfaden: selbstgehostetes vLLM"
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

## Szenario

Sie haben eine vLLM-Instanz, die ein Open-Weights-Coding-Modell auf einer internen Maschine (`llm.internal:8000`) bereitstellt. Kein Inferenz-Traffic darf das Netzwerk verlassen. Richten Sie rousseau darauf aus und behandeln Sie den Endpunkt wie jedes andere OpenAI-kompatible Ziel.

vLLM implementiert das OpenAI-Chat-Completions-Schema, sodass der `openai`-Provider von rousseau unverändert funktioniert. LM Studio, Ollama und Text Generation Inference folgen demselben Muster.

## Voraussetzungen

- vLLM läuft bereits auf `http://llm.internal:8000/v1`, wobei `/v1/chat/completions` auf einen curl-Smoke-Test antwortet.
- Der Modell-Tag, mit dem Sie vLLM gestartet haben (z. B. `Qwen/Qwen3-Coder-30B`).

## Schritt 1 — vLLM bestätigen

```sh
curl -fsS http://llm.internal:8000/v1/models
curl -fsS http://llm.internal:8000/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{
    "model": "Qwen/Qwen3-Coder-30B",
    "messages": [{"role": "user", "content": "say hi"}]
  }' | jq .
```

Beide sollten fehlerfrei zurückkehren. Wenn der zweite Aufruf mit 4xx antwortet, korrigieren Sie zuerst vLLM — der Client von rousseau ist ein dünner JSON-Shim und erbt dessen Fehleroberfläche.

## Schritt 2 — rousseau an vLLM anbinden

Bearbeiten Sie `~/.config/rousseau/config.yaml`:

```yaml
provider: openai

openai:
  base_url: http://llm.internal:8000/v1
  api_key: not-required        # vLLM ignores the key but the client sends one
  model: Qwen/Qwen3-Coder-30B
  max_tokens: 4096

log:
  level: info
  format: json
```

Der `openai`-Provider teilt sich sein Schema mit `openrouter` und `ollama`; der einzige Unterschied ist die voreingestellte `base_url`. Ein explizit gesetztes `base_url` überschreibt den Standard.

## Schritt 3 — Smoke-Test im TUI

```sh
rousseau chat
```

Tippen Sie `explain the difference between goroutines and threads in two paragraphs.` und senden Sie ab. Wenn die Antwort per Streaming eintrifft, ist die Verdrahtung korrekt.

Falls nicht:

```sh
rousseau doctor
```

Die Zeile `provider.selected` zeigt `openai`; ein `fail` bei der Erreichbarkeit von `provider.openai.base_url` bedeutet, dass entweder DNS oder der interne Netzwerkpfad kaputt ist, nicht rousseau.

## Schritt 4 — Tool-Use aktivieren

Coding-Modelle variieren in Tool-Use-Treue. Die Agent-Schleife von rousseau erwartet, dass das Modell `tool_use`-Blöcke emittiert, deren JSON gegen das `InputSchema` des Tools validiert. Wenn Ihr vLLM-Modell das OpenAI-Tool-Use-Schema nicht nativ unterstützt:

- Starten Sie mit `provider: openai` + einem Modell, das es unterstützt (aktuelle Qwen-, Mistral-, Llama-3.1-8B+-Varianten bewerben dies).
- Oder wickeln Sie vLLM in einen Shim wie [vLLMs OpenAI-kompatiblen tool_choice-Adapter](https://docs.vllm.ai/) und verifizieren Sie erneut.

Sobald Tool-Use funktioniert, sind die Coding-Tools (read, write, edit, grep, bash) genauso verfügbar wie bei jedem anderen Provider.

## Schritt 5 — Freigaberichtlinien in Betracht ziehen

Selbst gehostete Modelle sind tendenziell weniger risikobewusst als Frontier-Modelle. Das `bash`-Tool mit einem Approver im `pattern`-Modus zu sperren ist ratsam:

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read,  match: ".*"}
      - {tool: grep,  match: ".*"}
      - {tool: edit,  match: "^./workspace/.*"}
      - {tool: bash,  match: "^(ls|cat|grep|rg|find|git status|git diff) "}
    deny:
      - {tool: bash,  match: "rm -rf|sudo|curl|wget|chmod|chown"}
```

Siehe [Leitfäden: Audit + Freigaberichtlinien](/de/guides/audit-approval-policies/) für eine tiefergehende Durchgangsanleitung.

## Schritt 6 — Performance beobachten

Selbst gehostete Endpunkte profitieren häufig von höherem `max_iterations` (die Agent-Schleife braucht möglicherweise mehr Round-Trips, um zur gleichen Schlussfolgerung zu kommen) und stets vom Aktivieren der Sitzungs-Komprimierung:

```yaml
agent:
  max_iterations: 48
  compression:
    enabled: true
    trigger_messages: 60
    keep_recent: 8
```

Komprimierung ist standardmäßig ausgeschaltet, weil sie einen LLM-Turn für die Zusammenfassung verbraucht; auf einer Pay-per-Token-Public-API kann das verschwenderisch sein. Auf einem selbst gehosteten Endpunkt sind die Token-Kosten null, also lassen Sie sie aktiviert.

## Alternativen zu vLLM

Dasselbe Rezept gilt für:

- **Ollama** — verwenden Sie `provider: ollama` (`base_url` standardmäßig `http://localhost:11434/v1`, `api_key` standardmäßig `not-required`).
- **LM Studio** — verwenden Sie `provider: openai` und richten Sie `base_url` auf den LM-Studio-Server (`http://host:1234/v1`).
- **TGI (Text Generation Inference)** — verwenden Sie `provider: openai` und richten Sie `base_url` auf den OpenAI-Kompatibilitäts-Endpunkt von TGI.
- **OpenRouter** — verwenden Sie `provider: openrouter` (`base_url` standardmäßig `https://openrouter.ai/api/v1`).

## Vorbehalte

- rousseau streamt nicht, wenn der Provider nicht streamt. Manche vLLM-Builds werden mit deaktiviertem Streaming ausgeliefert — aktivieren Sie es für ein besseres TUI-Erlebnis.
- Prompt Caching (`internal/llm/anthropic` verwendet `cache_control`-Marker) ist Anthropic-spezifisch und wirkt sich gegen vLLM nicht aus. Das ist vor allem für langlebige Sitzungen bei Pay-per-Token-Providern relevant.
- Die Seite [OpenAI-kompatibler Provider](/de/providers/openai-compatible/) ist die definitive Referenz für jeden Knopf.

## Weiter

- [OpenAI-kompatibler Provider](/de/providers/openai-compatible/) — jedes Konfigurationsfeld.
- [Audit + Freigaberichtlinien](/de/guides/audit-approval-policies/) — Sicherheitshaltung für weniger ausgerichtete Modelle.
- [Offline](/de/offline/) — rousseau ohne ausgehende Internetverbindung betreiben.
