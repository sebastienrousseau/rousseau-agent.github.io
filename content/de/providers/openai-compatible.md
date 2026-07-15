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
description: "Configure OpenAI-compatible endpoints: OpenAI, OpenRouter, Ollama, self-hosted vLLM or LM Studio. BaseURL, model naming, streaming, and Ollama's not-required key."
keywords: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, base_url, chat completions, API key, streaming"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/providers/openai-compatible/"
subtitle: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, and any Chat Completions clone."
tags: "providers, openai, openrouter, ollama"
title: "OpenAI-kompatibler Anbieter"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, base_url, chat completions, API key, streaming"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "OpenAI-kompatibler Anbieter"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 10
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/openai-compatible/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/openai-compatible/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "OpenAI-kompatibler Anbieter"
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
twitter_description: "Configure OpenAI-compatible endpoints: OpenAI, OpenRouter, Ollama, self-hosted vLLM or LM Studio. BaseURL, model naming, streaming, and Ollama's not-required key."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "OpenAI-kompatibler Anbieter"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Was Sie lernen</span><p>Wie der <code>openai</code>-Provider von rousseau sechs verschiedene Endpunkte (OpenAI, OpenRouter, Ollama, vLLM, LM Studio, LiteLLM) durch eine einzige Implementierung bedient, die exakten <code>base_url</code>- und <code>model</code>-Werte für jeden davon und welche Endpunkte Tool-Use unterstützen. Lesen Sie <code>internal/llm/openai/client.go</code> parallel zu dieser Seite.</p></aside>

## Eine Implementierung, viele Endpunkte

`internal/llm/openai/` spricht die OpenAI Chat Completions API. Da `base_url` konfigurierbar ist, bedient derselbe Code jeden OpenAI-kompatiblen Endpunkt: OpenAI selbst, OpenRouter, together.ai, DeepInfra, selbstgehostetes vLLM, Ollamas OpenAI-Shim, LM Studio und LiteLLM.

Der Provider-Name ist einer von `openai`, `openrouter` oder `ollama` – jeder entspricht einem eigenen Config-Block mit voreingestelltem `base_url` (siehe `setDefaults` in `internal/config/config.go`). Nutzen Sie `openai` als generisches Slot und überschreiben Sie `base_url`, wenn Sie auf ein selbstgehostetes Backend zeigen.

## Endpunkt-Rezepte

<div class="tabs" data-tabs="openai-compat-endpoints">
  <div class="tab-list" role="tablist" aria-label="OpenAI-compatible endpoint">
    <button role="tab" aria-selected="true">OpenAI</button>
    <button role="tab" aria-selected="false">OpenRouter</button>
    <button role="tab" aria-selected="false">Ollama</button>
    <button role="tab" aria-selected="false">vLLM</button>
    <button role="tab" aria-selected="false">LM Studio</button>
    <button role="tab" aria-selected="false">LiteLLM</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Direktes OpenAI. `api.openai.com/v1` ist der SDK-Standard – kein `base_url`-Override nötig.

```yaml
provider: openai

openai:
  api_key: sk-...
  model: gpt-5
  max_tokens: 4096
```

Tool-Use: ja (natives `tools`-Array). Streaming: ja (SSE).

<aside class="admonition" data-type="note"><span class="admonition-title">Modell-Benennung</span><p>Modell-IDs folgen OpenAIs eigener Benennung (<code>gpt-4o</code>, <code>gpt-5</code>, <code>o1</code>, <code>o3-mini</code>). Pinnen Sie exakte IDs in Produktion – Aliase können sich unter Ihnen verschieben.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

OpenRouter aggregiert dutzende Provider hinter einer API. Modell-IDs verwenden die Konvention `provider/model`:

```yaml
provider: openrouter

openrouter:
  api_key: sk-or-...
  model: anthropic/claude-sonnet-4-6
```

`base_url` hat den Standardwert `https://openrouter.ai/api/v1`. Tool-Use hängt vom unterliegenden Provider ab – Anthropic- und OpenAI-Modelle funktionieren, die meisten Open-Weight-Modelle nicht.

<aside class="admonition" data-type="tip"><span class="admonition-title">Free-Tier-Modelle</span><p>OpenRouter bietet Free-Tier-Varianten (Suffix <code>:free</code>) zum Experimentieren an. Rate-Limits und Tages-Kontingente gelten.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Lokales Ollama exponiert einen Chat-Completions-kompatiblen Shim unter `http://localhost:11434/v1`:

```yaml
provider: ollama

ollama:
  model: llama3.1:8b
```

`ollama.api_key` hat den Standardwert `not-required` (der Shim ignoriert ihn, aber das SDK lehnt leere Strings ab – siehe `New` in `internal/llm/openai/client.go`). `ollama.base_url` hat den Standardwert `http://localhost:11434/v1`.

Tool-Use: Ja ab Ollama 0.4+ (über das `tools`-Array im Chat-Completions-Request). Ältere Builds liefern Klartext.

<aside class="admonition" data-type="warning"><span class="admonition-title">Latenz</span><p>Reines CPU-Ollama auf einem Laptop kann pro Turn zehn Sekunden und mehr benötigen. Setzen Sie den HTTP-Timeout Ihres Aufrufers über 60s oder nutzen Sie einen GPU-Host.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

vLLM ist die produktionsreife selbstgehostete Engine. Starten Sie sie mit `--api-key`, wenn Sie Auth wünschen:

```sh
python -m vllm.entrypoints.openai.api_server \
  --model mistralai/Mixtral-8x22B-Instruct-v0.1 \
  --host 0.0.0.0 --port 8000 \
  --api-key sk-vllm-secret
```

```yaml
provider: openai

openai:
  api_key: sk-vllm-secret
  base_url: http://vllm.internal:8000/v1
  model: mistralai/Mixtral-8x22B-Instruct-v0.1
  max_tokens: 4096
```

Tool-Use: Ja für Modelle mit einem Tool-Use-Chat-Template (`Hermes-2-Pro`, `Mistral-Nemo`, `Llama-3.1-8B-Instruct` und höher). Streaming: Ja. Siehe [Guides: Selbstgehostetes vLLM](/de/guides/self-hosted-vllm/) für die vollständige Bereitstellung.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

LM Studio liefert einen OpenAI-kompatiblen Server unter `http://localhost:1234/v1`:

```yaml
provider: openai

openai:
  api_key: not-required
  base_url: http://localhost:1234/v1
  model: lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF
```

Tool-Use: In aktuellen Builds (Stand Mitte 2026) **nicht** unterstützt. Der Endpunkt akzeptiert ein `tools`-Array, ignoriert es aber und liefert Klartext. Nutzen Sie ihn für reine Chat-Workloads oder warten Sie, bis das Feature eintrifft.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

LiteLLM ist ein Proxy, der viele Provider hinter einer API zusammenführt. Zeigen Sie rousseau darauf:

```yaml
provider: openai

openai:
  api_key: sk-litellm-...
  base_url: http://litellm.internal:4000
  model: bedrock/anthropic.claude-sonnet-4-6-20260101-v1:0
```

Hinweis: Der Standard-Port von LiteLLM ist 4000, und sein `/v1`-Präfix ist je nach Bereitstellung optional. Folgen Sie der LiteLLM-Dokumentation Ihrer Version.

Tool-Use: Wird an den unterliegenden Provider durchgereicht. Streaming: Ja. Nützlich für Teams, die einen einzigen Engpass für LLM-Traffic wollen (Rate-Limiting, Budget-Tracking, Audit).

  </div>
</div>

## Konfigurationsreferenz

| Feld | Standard | Wirkung |
|---|---|---|
| `api_key` | *erforderlich* | Bearer-Token. Nutzen Sie `not-required` für lokale Endpunkte, die Auth ignorieren. |
| `model` | *erforderlich* | Modell-ID. Kein universeller Standard über die Endpunkte hinweg. |
| `base_url` | *hängt vom Provider-Namen ab* | Überschreibt den Endpunkt. Siehe Presets in `setDefaults`. |
| `max_tokens` | SDK-Standard | Begrenzt Ausgabe-Tokens pro Completion. |

Die Provider-Namen `openai`, `openrouter` und `ollama` bilden jeweils auf einen eigenen Config-Block ab (`OpenAIConfig`, `OpenAIConfig`, `OpenAIConfig`); sie teilen sich die Form, ermöglichen aber, mehrere Endpunkte in einer `config.yaml` zu konfigurieren und durch Ändern von `provider:` umzuschalten.

## Streaming

Der Provider implementiert `agent.StreamingProvider` über SSE. Jeder Endpunkt oben unterstützt Streaming; der Shim von Ollama erfordert einen aktuellen Build (0.5+).

## Tool-Use

Tool-Definitionen aus der `Registry` werden in `internal/llm/openai/client.go` in OpenAIs `tools`-Array konvertiert. Nicht jeder OpenAI-kompatible Endpunkt unterstützt Tool-Use – prüfen Sie Ihr Backend vor der Aktivierung. Ollama unterstützt es ab 0.4; ältere LM-Studio-Builds nicht.

Approval-Richtlinien greifen bei Endpunkten, die tatsächlich `tool_calls` zurückgeben. Endpunkte ohne Tool-Use-Support liefern Klartext, und die `Registry` wird nicht konsultiert.

## Fallstricke

- **Modell-Benennung.** Jeder Endpunkt hat seine eigene Konvention: OpenAI (`gpt-5`), OpenRouter (`anthropic/claude-sonnet-4-6`), Ollama (`llama3.1:8b`), vLLM (der HuggingFace-Name). Es gibt keine anbieterübergreifende Portabilität.
- **Leerer API-Key.** Das SDK lehnt leere Strings ab; übergeben Sie `not-required` (oder einen beliebigen Platzhalter) für lokale Endpunkte, die keine Auth benötigen.
- **Trailing-Slash in BaseURL.** Enthalten Sie das Pfadsegment `/v1`. Kein abschliessender Slash.
- **Timeouts.** Lokales Ollama auf einer CPU kann pro Turn zehn Sekunden und mehr benötigen – erhöhen Sie das HTTP-Client-Timeout, wenn Sie den Provider selbst wrappen. `rousseau` nutzt den SDK-Standard.
- **Tool-Use-Varianz.** OpenAI und Anthropic-hinter-OpenRouter unterstützen Tools zuverlässig. Ollama benötigt einen aktuellen Build und ein Modell mit Tool-Use-Chat-Template. LM Studio unterstützt keine Tools. Kommen `tool_calls` als Klartext an, wird die `Registry` nicht konsultiert.
- **Reasoning-Modelle.** OpenAIs o1-/o3-Serie verhält sich anders: `max_tokens` wird durch `max_completion_tokens` ersetzt, und System-Prompts sind eingeschränkt. Das SDK erledigt dies, jedoch mit höherer Pro-Turn-Latenz.

## Fehlerbehebung

### `openai: complete: 401 Unauthorized`

Falscher oder fehlender API-Key. Für OpenRouter nutzen Sie den `sk-or-…`-Token. Für lokale Endpunkte stellen Sie sicher, dass `api_key` nicht leer ist, selbst wenn der Endpunkt ihn ignoriert.

### `openai: complete: 404 model not found`

Der `model`-String passt zu nichts, was der Endpunkt kennt. Für OpenRouter schliessen Sie das Provider-Präfix ein (`anthropic/claude-sonnet-4-6`, nicht `claude-sonnet-4-6`). Für Ollama stellen Sie sicher, dass das Modell gepullt wurde (`ollama pull llama3.1:8b`).

### Das Modell ignoriert meine `tools`

Der Endpunkt unterstützt Tool-Use für dieses Modell nicht. Verifizieren Sie durch Zeigen auf dasselbe Modell über einen bekannt-funktionierenden Endpunkt (OpenAI, Anthropic direkt, OpenRouter mit einem Anthropic-Modell). Siehe die Tool-Use-Spalte in den Rezepten oben.

### `context deadline exceeded` bei lokalem Ollama

CPU-Inferenz ist langsam. Optionen: (1) Timeout des Aufrufers erhöhen, (2) Ollama auf einem GPU-Host betreiben, (3) auf ein kleineres Modell wechseln (`llama3.1:8b` vs. `70b`).

### Streaming stockt mitten in einer Antwort

Einige Proxies (LiteLLM, Unternehmens-Egress-Proxies) puffern SSE. Konfigurieren Sie den Proxy so, dass Buffering für `text/event-stream` deaktiviert ist, oder betreiben Sie rousseau im selben Netzwerksegment wie den Endpunkt.

## Verwandte Seiten

- [Guides: Selbstgehostetes vLLM](/de/guides/self-hosted-vllm/) – Produktions-Bereitstellung.
- [Providers: Anthropic](/de/providers/anthropic/) – die direkte API als Alternative für Claude.
- [Guides: Multi-Provider](/de/guides/multi-provider/) – unterschiedliche Provider pro Transport betreiben.
- [Guides: Rate-Limits](/de/guides/rate-limits/) – Retry-Playbook pro Provider.
- [Konfiguration](/de/configuration/) – die Blöcke `openai`/`openrouter`/`ollama` im Kontext.

## Weiterführende Lektüre

- `internal/llm/openai/client.go` – `Complete`, Nachrichtenkonvertierung, Tool-Schema.
- `internal/llm/openai/client.go` – Streaming-Implementierung.
- `internal/config/config.go` – `OpenAIConfig`-Struktur, `setDefaults` für `base_url`-Presets.
