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
description: "Worked example: point rousseau-agent at a self-hosted vLLM endpoint on your internal network via the OpenAI-compatible provider."
keywords: "vllm, self-hosted, openai-compatible, air-gapped, internal network, local llm"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/guides/self-hosted-vllm/"
subtitle: "Point rousseau at a vLLM endpoint on your internal network."
tags: "guides, vllm, self-hosted, openai-compatible"
title: "Guide: Self-hosted vLLM"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "vllm, self-hosted, openai-compatible, air-gapped, internal network, local llm"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide: Self-hosted vLLM"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 32
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/self-hosted-vllm/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/self-hosted-vllm/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guide: Self-hosted vLLM"
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
twitter_title: "Guide: Self-hosted vLLM"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Scenario

You have a vLLM instance serving an open-weights coding model on an internal box (`llm.internal:8000`). No inference traffic can leave the network. Point rousseau at it and treat the endpoint like any other OpenAI-compatible target.

vLLM implements the OpenAI Chat Completions schema, so rousseau's `openai` provider works unchanged. LM Studio, Ollama, and Text Generation Inference are the same pattern.

## Prerequisites

- vLLM already up on `http://llm.internal:8000/v1` with `/v1/chat/completions` responding to a curl smoke test.
- The model tag you launched vLLM with (e.g. `Qwen/Qwen3-Coder-30B`).

## Step 1 — Confirm vLLM

```sh
curl -fsS http://llm.internal:8000/v1/models
curl -fsS http://llm.internal:8000/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{
    "model": "Qwen/Qwen3-Coder-30B",
    "messages": [{"role": "user", "content": "say hi"}]
  }' | jq .
```

Both should return without error. If the second call 4xx's, fix vLLM first — rousseau's client is a thin JSON shim and inherits its error surface.

## Step 2 — Wire rousseau to vLLM

Edit `~/.config/rousseau/config.yaml`:

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

The `openai` provider shares its schema with `openrouter` and `ollama`; the only difference is the preset `base_url`. Setting `base_url` explicitly overrides the default.

## Step 3 — Smoke-test in the TUI

```sh
rousseau chat
```

Type `explain the difference between goroutines and threads in two paragraphs.` and send. If the reply streams in, the wiring is correct.

If it doesn't:

```sh
rousseau doctor
```

The `provider.selected` row will show `openai`; a `fail` on `provider.openai.base_url` reachability means either DNS or the internal network path is broken, not rousseau.

## Step 4 — Turn on tool use

Coding models vary in tool-use fidelity. The rousseau agent loop expects the model to emit `tool_use` blocks whose JSON validates against the tool's `InputSchema`. If your vLLM model does not natively support the OpenAI tool-use schema:

- Start with `provider: openai` + a model that supports it (recent Qwen, Mistral, Llama 3.1 8B+ variants advertise this).
- Or wrap vLLM in a shim like [vLLM's OpenAI-compatible tool_choice adapter](https://docs.vllm.ai/) and re-verify.

Once tool use works, the coding tools (read, write, edit, grep, bash) become available exactly as they do with any other provider.

## Step 5 — Consider approval policies

Self-hosted models tend to be less risk-aware than frontier models. Locking the `bash` tool with a `pattern`-mode approver is prudent:

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

See [Guides: Audit + Approval Policies](/guides/audit-approval-policies/) for a deeper walkthrough.

## Step 6 — Watch performance

Self-hosted endpoints often benefit from higher `max_iterations` (the agent loop may need more round-trips to hit the same conclusion), and always from enabling session compression:

```yaml
agent:
  max_iterations: 48
  compression:
    enabled: true
    trigger_messages: 60
    keep_recent: 8
```

Compression is off by default because it uses an LLM turn to summarise; on a pay-per-token public API this can be wasteful. On a self-hosted endpoint the token cost is zero, so leave it on.

## Alternatives to vLLM

Same recipe applies to:

- **Ollama** — use `provider: ollama` (defaults `base_url` to `http://localhost:11434/v1` and `api_key` to `not-required`).
- **LM Studio** — use `provider: openai` and point `base_url` at the LM Studio server (`http://host:1234/v1`).
- **TGI (Text Generation Inference)** — use `provider: openai` and point `base_url` at the TGI OpenAI compatibility endpoint.
- **OpenRouter** — use `provider: openrouter` (defaults `base_url` to `https://openrouter.ai/api/v1`).

## Caveats

- rousseau does not stream when the provider does not stream. Some vLLM builds ship streaming disabled — turn it on for a better TUI experience.
- Prompt caching (`internal/llm/anthropic` uses `cache_control` markers) is Anthropic-specific and does nothing against vLLM. This mostly matters for long-lived sessions on pay-per-token providers.
- The [openai-compatible provider page](/providers/openai-compatible/) is the definitive reference for every knob.

## Next

- [OpenAI-compatible provider](/providers/openai-compatible/) — every config field.
- [Audit + approval policies](/guides/audit-approval-policies/) — safety posture for less-aligned models.
- [Offline](/offline/) — running rousseau with no outbound internet.
