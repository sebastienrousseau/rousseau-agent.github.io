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
description: "Overview of the five LLM provider families supported by rousseau-agent: claudecli, Anthropic, AWS Bedrock, Google Vertex AI, and any OpenAI-compatible endpoint."
keywords: "providers, LLM, Anthropic, Bedrock, Vertex, OpenAI, OpenRouter, Ollama, claudecli"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/providers/"
subtitle: "Fünf LLM-Anbieterfamilien hinter einer Provider-Schnittstelle."
tags: "providers, LLM"
title: "Anbieter"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "providers, LLM, Anthropic, Bedrock, Vertex, OpenAI, OpenRouter, Ollama, claudecli"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Anbieter"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 5
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Anbieter"
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
twitter_description: "Overview of the five LLM provider families supported by rousseau-agent: claudecli, Anthropic, AWS Bedrock, Google Vertex AI, and any OpenAI-compatible endpoint."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Anbieter"
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

## Die Provider-Schnittstelle

Jedes LLM-Backend implementiert `agent.Provider`:

```go
type Provider interface {
    Name() string
    Complete(ctx context.Context, req Request) (Response, error)
}
```

Eine `StreamingProvider`-Variante fügt `CompleteStream` für die Token-für-Token-Auslieferung hinzu. Ein sechstes Backend hinzuzufügen ist eine einzige `Complete`-Implementierung plus Verdrahtung in `internal/cli/provider.go`.

## Unterstützte Familien

| Provider | Auth-Modell | Endpunkt | Streaming | Prompt-Caching | Empfohlen für |
|---|---|---|:---:|:---:|---|
| [claudecli](/de/providers/claudecli/) | Erbt `claude`-CLI-Auth | Lokaler Subprozess | Ja | via Subprozess | Einzelne Operatoren, Claude Code auf Abonnement-Ebene |
| [Anthropic](/de/providers/anthropic/) | `ANTHROPIC_API_KEY` | `api.anthropic.com` | Ja | Ephemere Marker | Teams auf der Anthropic-API |
| [AWS Bedrock](/de/providers/bedrock/) | AWS-Credential-Chain | `bedrock-runtime.<region>.amazonaws.com` | Ja | via SDK | Unternehmen auf AWS |
| [Google Vertex AI](/de/providers/vertex/) | Service Account oder ADC | `<region>-aiplatform.googleapis.com` | Ja | via SDK | Unternehmen auf GCP |
| [OpenAI-kompatibel](/de/providers/openai-compatible/) | Bearer-Token | `api.openai.com` oder Override | Ja | Provider-abhängig | OpenAI, OpenRouter, Ollama, vLLM, LM Studio |

## Einen Provider auswählen

Setzen Sie den `provider`-Schlüssel am Anfang von `~/.config/rousseau/config.yaml`:

```yaml
provider: anthropic

anthropic:
  api_key: sk-ant-...
  model: claude-sonnet-4-6
```

Oder in der Shell überschreiben:

```sh
ROUSSEAU_PROVIDER=bedrock rousseau chat
```

`ANTHROPIC_API_KEY` wird beim Laden an `anthropic.api_key` gebunden, sodass die Übergabe über die Umgebung äquivalent ist.

## Wo jeder Provider Tool-Use ausführt

Der `claudecli`-Provider führt seine eigene Tool-Use-Schleife innerhalb des `claude`-Subprozesses aus. Auf der rousseau-`Registry` registrierte Tools werden für diesen Provider **nicht** aufgerufen; die `Response` ist immer eine einzelne Textnachricht am Ende des Turns mit der finalen Antwort von claude.

Jeder andere Provider (`anthropic`, `bedrock`, `vertex`, `openai`) verwendet die rousseau-`Registry`. Tool-Definitionen werden von jedem Provider-Paket in die vom Provider erwartete JSON-Form konvertiert.
