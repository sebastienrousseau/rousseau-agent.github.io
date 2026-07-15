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
description: "Configure OpenAI-compatible endpoints: OpenAI, OpenRouter, Ollama, self-hosted vLLM or LM Studio. BaseURL, model naming, streaming, and Ollama's not-required key."
keywords: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, base_url, chat completions, API key, streaming"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/providers/openai-compatible/"
subtitle: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, and any Chat Completions clone."
tags: "providers, openai, openrouter, ollama"
title: "OpenAI-compatible Provider"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, base_url, chat completions, API key, streaming"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "OpenAI-compatible Provider"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 10
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/openai-compatible/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/openai-compatible/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "OpenAI-compatible Provider"
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
twitter_title: "OpenAI-compatible Provider"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">What you'll learn</span><p>How rousseau's <code>openai</code> provider serves six different endpoints (OpenAI, OpenRouter, Ollama, vLLM, LM Studio, LiteLLM) through a single implementation, the exact <code>base_url</code> and <code>model</code> value for each, and which endpoints support tool use. Read <code>internal/llm/openai/client.go</code> alongside this page.</p></aside>

## One implementation, many endpoints

`internal/llm/openai/` speaks the OpenAI Chat Completions API. Because `base_url` is configurable, the same code serves every OpenAI-compatible endpoint: OpenAI itself, OpenRouter, together.ai, DeepInfra, self-hosted vLLM, Ollama's OpenAI shim, LM Studio, and LiteLLM.

The provider name is one of `openai`, `openrouter`, or `ollama` — each corresponds to its own config block with a preset `base_url` (see `setDefaults` in `internal/config/config.go`). Use `openai` as the generic slot and override `base_url` when pointing at a self-hosted backend.

## Endpoint recipes

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

Direct OpenAI. `api.openai.com/v1` is the SDK default — no `base_url` override needed.

```yaml
provider: openai

openai:
  api_key: sk-...
  model: gpt-5
  max_tokens: 4096
```

Tool use: yes (native `tools` array). Streaming: yes (SSE).

<aside class="admonition" data-type="note"><span class="admonition-title">Model naming</span><p>Model IDs follow OpenAI's own naming (<code>gpt-4o</code>, <code>gpt-5</code>, <code>o1</code>, <code>o3-mini</code>). Pin exact IDs in production — aliases can shift under you.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

OpenRouter aggregates dozens of providers behind one API. Model IDs use the `provider/model` convention:

```yaml
provider: openrouter

openrouter:
  api_key: sk-or-...
  model: anthropic/claude-sonnet-4-6
```

`base_url` defaults to `https://openrouter.ai/api/v1`. Tool use depends on the underlying provider — Anthropic and OpenAI models work, most open-weights models do not.

<aside class="admonition" data-type="tip"><span class="admonition-title">Free-tier models</span><p>OpenRouter exposes free-tier variants (<code>:free</code> suffix) for experimentation. Rate limits and daily quotas apply.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Local Ollama exposes a Chat Completions-compatible shim at `http://localhost:11434/v1`:

```yaml
provider: ollama

ollama:
  model: llama3.1:8b
```

`ollama.api_key` defaults to `not-required` (the shim ignores it, but the SDK rejects empty strings — see `New` in `internal/llm/openai/client.go`). `ollama.base_url` defaults to `http://localhost:11434/v1`.

Tool use: yes as of Ollama 0.4+ (via the `tools` array in the Chat Completions request). Older builds return plain text.

<aside class="admonition" data-type="warning"><span class="admonition-title">Latency</span><p>CPU-only Ollama on a laptop can take tens of seconds per turn. Set your caller's HTTP timeout above 60s or use a GPU-backed host.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

vLLM is the production-grade self-hosted engine. Start it with `--api-key` if you want auth:

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

Tool use: yes for models with a tool-use chat template (`Hermes-2-Pro`, `Mistral-Nemo`, `Llama-3.1-8B-Instruct` and above). Streaming: yes. See [Guides: Self-hosted vLLM](/guides/self-hosted-vllm/) for the full deployment.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

LM Studio ships an OpenAI-compatible server on `http://localhost:1234/v1`:

```yaml
provider: openai

openai:
  api_key: not-required
  base_url: http://localhost:1234/v1
  model: lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF
```

Tool use: **not** supported in current builds (as of mid-2026). The endpoint accepts a `tools` array but ignores it and returns plain text. Use for chat-only workloads or wait for the feature to land.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

LiteLLM is a proxy that fronts many providers behind one API. Point rousseau at it:

```yaml
provider: openai

openai:
  api_key: sk-litellm-...
  base_url: http://litellm.internal:4000
  model: bedrock/anthropic.claude-sonnet-4-6-20260101-v1:0
```

Note: LiteLLM's default port is 4000, and its `/v1` prefix is optional depending on how it is deployed. Follow the LiteLLM docs for your version.

Tool use: passes through to the underlying provider. Streaming: yes. Useful for teams that want a single choke-point for LLM traffic (rate limiting, budget tracking, audit).

  </div>
</div>

## Configuration reference

| Field | Default | Effect |
|---|---|---|
| `api_key` | *required* | Bearer token. Use `not-required` for local endpoints that ignore auth. |
| `model` | *required* | Model identifier. No universal default across endpoints. |
| `base_url` | *depends on provider name* | Overrides the endpoint. See presets in `setDefaults`. |
| `max_tokens` | SDK default | Caps output tokens per completion. |

The `openai`, `openrouter`, and `ollama` provider names each map to their own config block (`OpenAIConfig`, `OpenAIConfig`, `OpenAIConfig`); they share the same shape but let you configure multiple endpoints in one `config.yaml` and switch between them by changing `provider:`.

## Streaming

The provider implements `agent.StreamingProvider` via SSE. Every endpoint above supports streaming; Ollama's shim requires a recent build (0.5+).

## Tool use

Tool definitions from the `Registry` are converted to OpenAI's `tools` array in `internal/llm/openai/client.go`. Not every OpenAI-compatible endpoint supports tool use — check your backend before enabling. Ollama supports it as of 0.4; older LM Studio builds do not.

Approval policies apply for endpoints that do return `tool_calls`. Endpoints without tool-use support will return plain text and the `Registry` will not be consulted.

## Gotchas

- **Model naming.** Every endpoint has its own convention: OpenAI (`gpt-5`), OpenRouter (`anthropic/claude-sonnet-4-6`), Ollama (`llama3.1:8b`), vLLM (the HuggingFace name). There is no cross-endpoint portability.
- **Empty API key.** The SDK rejects empty strings; pass `not-required` (or any placeholder) for local endpoints that do not need auth.
- **BaseURL trailing slash.** Include the `/v1` path segment. Do not include a trailing slash.
- **Timeouts.** Local Ollama on a CPU can take tens of seconds per turn — increase your HTTP client timeout if you wrap the provider yourself. `rousseau` uses the SDK default.
- **Tool use variance.** OpenAI and Anthropic-behind-OpenRouter reliably support tools. Ollama needs a recent build and a model with a tool-use chat template. LM Studio does not support tools. If tool_calls arrive as plain text, the `Registry` is not consulted.
- **Reasoning models.** OpenAI o1/o3 series behave differently: `max_tokens` is replaced by `max_completion_tokens` and system prompts are limited. The SDK handles this, but expect longer per-turn latency.

## Troubleshooting

### `openai: complete: 401 Unauthorized`

Wrong or missing API key. For OpenRouter, use the `sk-or-…` token. For local endpoints, ensure `api_key` is non-empty even if the endpoint ignores it.

### `openai: complete: 404 model not found`

The `model` string does not match anything the endpoint recognises. For OpenRouter, include the provider prefix (`anthropic/claude-sonnet-4-6`, not `claude-sonnet-4-6`). For Ollama, ensure the model is pulled (`ollama pull llama3.1:8b`).

### The model ignores my `tools`

The endpoint does not support tool use for this model. Verify by pointing at the same model via a known-good endpoint (OpenAI, Anthropic direct, OpenRouter with an Anthropic model). See the tool-use column in the recipes above.

### `context deadline exceeded` on local Ollama

CPU inference is slow. Options: (1) increase your caller's timeout, (2) run Ollama on a GPU host, (3) switch to a smaller model (`llama3.1:8b` vs `70b`).

### Streaming stalls halfway through a response

Some proxies (LiteLLM, corporate egress proxies) buffer SSE. Set the proxy to disable buffering for `text/event-stream` or run rousseau on the same network segment as the endpoint.

## Related pages

- [Guides: Self-hosted vLLM](/guides/self-hosted-vllm/) — production deployment.
- [Providers: Anthropic](/providers/anthropic/) — the direct API alternative for Claude.
- [Guides: Multi-provider](/guides/multi-provider/) — running different providers per transport.
- [Guides: Rate limits](/guides/rate-limits/) — provider-by-provider retry playbook.
- [Configuration](/configuration/) — the `openai`/`openrouter`/`ollama` stanzas in context.

## Further reading

- `internal/llm/openai/client.go` — `Complete`, message conversion, tool schema.
- `internal/llm/openai/client.go` — streaming implementation.
- `internal/config/config.go` — `OpenAIConfig` struct, `setDefaults` for `base_url` presets.
