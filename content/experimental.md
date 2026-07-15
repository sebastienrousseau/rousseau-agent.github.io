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
description: "Off-by-default rousseau-agent behaviour: voice mode via whisper.cpp, FTS5 recall, LLM compression, and other opt-in surface."
keywords: "experimental, voice, whisper, fts5, compression, opt-in, feature flag"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/experimental/"
subtitle: "Behaviour that is off by default and why."
tags: "experimental, opt-in, voice, compression, fts5"
title: "Experimental"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "experimental, voice, whisper, fts5, compression, opt-in, feature flag"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Experimental"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "system"
order: 60
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/experimental/index.html"
item_link: "https://docs.rousseau-agent.dev/experimental/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Experimental"
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
twitter_title: "Experimental"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## What "experimental" means here

Rousseau's default posture is minimal: one static Go binary, one SQLite file, no external dependencies. Any feature that requires an extra runtime (`whisper.cpp`), extra state (FTS5 index for recall), or extra provider cost (LLM-backed compression) is opt-in.

None of these are unstable. They ship, they have tests, they're supported. But because they change the operational cost or surface, they default to off — you turn on the ones you need.

## Voice mode (whisper.cpp)

Off by default because it requires the `whisper` binary from whisper.cpp to be installed on the daemon host.

**Toggle:** `whatsapp.voice.enabled: true` in `config.yaml`. See `VoiceConfig` in `internal/config/config.go`.

**What it does.** When WhatsApp delivers a voice note, the whatsmeow client downloads the OGG payload, invokes `whisper` with the configured model, and treats the transcript as the inbound message text. Structured log events (`internal/transport/whatsapp/dispatch.go`):

- `whatsapp.audio_downloaded size=N`
- `whatsapp.transcribed elapsed=N`

**Why it's off.** Two reasons: (1) a fresh install would fail confusingly when the `whisper` binary is missing, (2) transcription is a real-time CPU spend most operators would opt into rather than surprise.

See [User Guide: Voice mode](/user-guide/voice-mode/) for the full setup.

## FTS5 recall

**Toggle.** On by default, but only used by tools that ask for it. The FTS5 index is built and maintained regardless (`EnsureSearch` in `internal/state/sqlite/search.go`); the "opt-in" is whether the agent asks the model to search it.

**What it does.** SQLite FTS5 full-text index over every stored session. Powered through `rousseau session search`, the MCP tool `rousseau_search_sessions`, and (when the agent is configured with a recall searcher) the model can query it mid-turn.

**Why it's structured this way.** The index is cheap to maintain — the triggers in `internal/state/sqlite/search.go` handle it — but exposing it to the model on every turn has a cost. It gets wired only when the agent loop is constructed with a `RecallSearcher` (`internal/state/sqlite/recall.go`).

See [User Guide: Compression + Recall](/user-guide/compression-recall/).

## LLM-backed compression

Off by default because it costs tokens.

**Toggle:** `agent.compression.enabled: true`. Full field list on the [Guide: Context management](/guides/context-management/).

**What it does.** When a session grows past `trigger_messages` (default 60), the `LLMCompressor` (`internal/agent/compressor.go`) summarises the oldest slice into one synthetic user message, preserving the most recent `keep_recent` messages verbatim. Every subsequent turn is smaller and cheaper.

**Why it's off.** The reference deployment runs `claudecli` on a subscription tier where token count is not billed. Compression pays for itself on Anthropic direct, Bedrock, Vertex, and OpenAI-compatible providers.

## OpenRouter and Ollama base URLs (pre-configured, still opt-in)

Not strictly experimental, but worth naming: rousseau's `setDefaults` in `internal/config/config.go` pre-configures OpenRouter and Ollama base URLs:

- `openrouter.base_url: https://openrouter.ai/api/v1`
- `ollama.base_url: http://localhost:11434/v1`
- `ollama.api_key: not-required`

Selecting these providers is opt-in via `provider: openrouter` / `provider: ollama` — the endpoints are just pre-filled so you don't have to remember them.

## Prompt-injection detection (roadmap)

Not shipped. See [Guides: Prompt injection](/guides/prompt-injection/) for the honest threat model. Mitigation today is entirely approver-based; classifier-based detection is a roadmap item pending research that actually works.

## Streaming to non-Anthropic providers (partial)

The Anthropic provider (`internal/llm/anthropic/client.go`) supports the SDK's streaming interface. Other adapters currently run in non-streaming mode. Streaming across every adapter is a planned uniformity pass.

## Related

- [Configuration](/configuration/) — every config knob.
- [User Guide: Voice mode](/user-guide/voice-mode/).
- [Guides: Context management](/guides/context-management/) — compression deep-dive.
- [Reference: Session store](/reference/session-store/) — FTS5 schema.
