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
hreflang: "en"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "en-GB"
locale: "en_GB"
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
description: "Fifteen provider-specific questions about claudecli, Anthropic, Bedrock, Vertex, OpenAI-compatible, Ollama."
keywords: "faq, providers, claudecli, anthropic, bedrock, vertex, ollama"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/faq/providers/"
subtitle: "Provider-specific FAQ."
tags: "faq, providers"
title: "FAQ: Providers"

news_genres: "Blog"
news_keywords: "faq, providers"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "FAQ: Providers"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "faq"
order: 12
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/faq/providers/index.html"
item_link: "https://docs.rousseau-agent.dev/faq/providers/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "FAQ: Providers"
last_build_date: "Mon, 13 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
ttl: "60"
type: "website"
webmaster: sebastian.rousseau@gmail.com (Sebastien Rousseau)

apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "rousseau-agent"
apple-touch-fullscreen: "yes"

msapplication-navbutton-color: "rgb(26,58,138)"

twitter_card: "summary"
twitter_creator: "rousseauagent"
twitter_description: "Fifteen provider-specific questions."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "FAQ: Providers"
twitter_url: "https://docs.rousseau-agent.dev"

author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Overview

Fifteen provider-focused questions covering all five LLM backends.

## Questions

### 1. Which provider is default?

`claudecli`. See `setDefaults` in `internal/config/config.go`.

### 2. Do I need an API key for the default?

No. `claudecli` shells out to the local `claude` binary and inherits its auth.

### 3. How do I switch to Anthropic API directly?

Set `provider: anthropic` and export `ANTHROPIC_API_KEY`. See [Migrations: Provider migration](/migrations/provider-migration/).

### 4. Does Bedrock need explicit keys in the config?

No. Rousseau uses the standard AWS credential chain: env vars, `~/.aws/credentials`, IMDS, IRSA. Set `bedrock.profile` for a named profile.

### 5. Does Vertex work with Application Default Credentials?

Yes. Leave `vertex.credentials_file` empty and set `GOOGLE_APPLICATION_CREDENTIALS`, or run `gcloud auth application-default login`.

### 6. Which OpenAI-compatible endpoints work?

Any that speak the Chat Completions shape. Tested: OpenRouter, Ollama, LM Studio, vLLM. `openai.base_url` is the knob.

### 7. Does Ollama need an API key?

No. `setDefaults` seeds `ollama.api_key: not-required`.

### 8. Does prompt caching work?

Yes on `anthropic`. The client writes cache markers on the last two messages. Other providers depend on their own caching layer.

### 9. What model do you recommend?

- `claudecli`: whatever `claude` is configured to use.
- `anthropic`: `claude-sonnet-4-6` (the default).
- `bedrock`: `anthropic.claude-sonnet-4-6-20250101-v1:0`.
- `vertex`: `claude-sonnet-4-6@20250101`.
- Local: `llama3.1:70b-instruct` minimum for reliable tool-use.

### 10. Can I switch providers mid-session?

Yes — providers don't leak model-specific state into the session. Edit `config.yaml`, restart. History is preserved.

### 11. Which provider is cheapest?

Depends on scale. `claudecli` with a subscription plan is flat-rate. Ollama is free after model download. Pay-per-token providers vary; enable prompt caching + compression to reduce spend.

### 12. Which provider is fastest?

Anthropic direct usually wins on TTFT. Ollama depends on your GPU. Bedrock/Vertex add STS/IAM latency but stream fine.

### 13. Does tool-use work on all providers?

Anthropic / claudecli / Bedrock / Vertex: excellent. OpenAI-compatible: depends on the model — GPT-class is fine, small local models often fail structured tool inputs.

### 14. Can I use two providers simultaneously?

Not from one config. Run two rousseau processes with distinct configs and state paths.

### 15. Where do provider errors show up?

Structured logs with `err` attribute. Grep `journalctl … | grep 'provider.error'` or the equivalent event name for your provider.

## Related pages

- [Providers](/providers/)
- [Reference: Config: Provider](/reference/config/provider/)
- [Migrations: Provider migration](/migrations/provider-migration/)
- [FAQ: General](/faq/general/)
- [FAQ: Transports](/faq/transports/)
