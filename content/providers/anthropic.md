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
description: "Configure the direct Anthropic provider: ANTHROPIC_API_KEY, model IDs, max_tokens, prompt cache markers on the last messages, streaming."
keywords: "Anthropic, ANTHROPIC_API_KEY, Claude API, prompt caching, cache_control, ephemeral, streaming"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/providers/anthropic/"
subtitle: "Direct Anthropic API with ephemeral prompt-cache markers."
tags: "providers, anthropic"
title: "Anthropic Provider"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Anthropic, ANTHROPIC_API_KEY, Claude API, prompt caching, cache_control, ephemeral, streaming"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Anthropic Provider"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 7
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/anthropic/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/anthropic/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Anthropic Provider"
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
twitter_title: "Anthropic Provider"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">What you'll learn</span><p>The exact wire-level shape of Anthropic requests rousseau sends, which content blocks receive prompt-cache markers and why, how streaming maps to <code>agent.StreamingProvider</code>, and the failure modes for 401/429/529 responses. Read <code>internal/llm/anthropic/client.go</code> and <code>internal/llm/anthropic/cache.go</code> alongside this page.</p></aside>

## When to use the Anthropic provider

The direct `anthropic` provider is the right choice when:

- You have an Anthropic API key and want per-token billing on `api.anthropic.com`.
- You want rousseau-side tool execution (the `Registry` is fully in play).
- You want to opt into ephemeral prompt-cache markers on stable prefixes.
- You want streaming completions in `rousseau chat` (token-by-token viewport updates).
- You want explicit, published rate limits (unlike `claudecli` subscription mode).

## Configuration

```yaml
provider: anthropic

anthropic:
  api_key: sk-ant-...
  model: claude-sonnet-4-6
  max_tokens: 4096
```

| Field | Default | Effect |
|---|---|---|
| `api_key` | *from `ANTHROPIC_API_KEY`* | Bearer for `api.anthropic.com`. Rejected if empty when the provider is selected. |
| `model` | `claude-sonnet-4-6` | Model identifier. |
| `max_tokens` | `4096` | Caps output tokens per completion. |

The environment variable `ANTHROPIC_API_KEY` is bound to `anthropic.api_key` at load time, so exporting it is equivalent to configuring it. Container operators typically export it in the systemd unit's `Environment=` line rather than checking it into `config.yaml`.

## Model identifiers

`rousseau-agent` passes `model` verbatim to the SDK. Pin the exact model ID (`claude-sonnet-4-6`, `claude-opus-4-6`) in production so your traffic does not shift under you when Anthropic promotes new snapshots.

## Prompt caching internals

Anthropic's ephemeral prompt cache lets you mark content blocks with `cache_control: { type: "ephemeral" }`. The API caches the prefix up to and including any cache-marked block; subsequent turns that carry the same prefix pay a fraction of the usual input-token cost (10% at the time of writing — check the Anthropic docs for current pricing).

Rousseau applies markers via `applyCacheMarkers` in `internal/llm/anthropic/cache.go`. Two things happen when `CacheableMessages > 0` in the outgoing `Request`:

1. **The system prompt gets `cache_control: ephemeral`.** It survives every turn, so it is always worth caching once you opt in. See lines 68–75 of `internal/llm/anthropic/client.go`.
2. **The last `CacheableMessages` messages** get `cache_control: ephemeral` on their last text block. This keeps a growing session cheap: as new turns are appended, the marker floats down the transcript, but the prefix up to the previous marker is still hot.

### Which blocks get marked

`markLastTextBlock` walks a `MessageParam`'s content backwards and sets `CacheControl` on the first text block it finds. `tool_use` and `tool_result` blocks are skipped — the SDK models them as different variants with their own optional `CacheControl` fields, and text is the safe common denominator. See `internal/llm/anthropic/cache.go`.

### When it pays off

<aside class="admonition" data-type="note"><span class="admonition-title">Caching economics</span><p>The break-even point depends on how much the cached prefix is reused. For a chat transport that runs 20–100 turns per session with a 5–10 kB system prompt (typical with skills loaded), enabling caching typically halves the input-token bill. For a one-shot cron job that generates a single reply, it saves nothing.</p></aside>

The `Compressor` sets `CacheableMessages = len(recentMessages) - 1` after a rewrite so the fresh summary block is cache-hot on the very next turn. Other code paths leave `CacheableMessages = 0`, meaning caching is opt-in per request. Embedders should set it explicitly when calling the provider directly.

### Verifying cache hits

The Anthropic API returns `usage.cache_read_input_tokens` and `usage.cache_creation_input_tokens` on every response. `agent.Usage` currently exposes only `InputTokens` and `OutputTokens`, so verifying the split requires either enabling debug logging or reading the raw SDK response — this is a known observability gap tracked in `docs/GAP_ANALYSIS_2026.md`.

## Streaming semantics

The provider implements `agent.StreamingProvider`. `rousseau chat` uses streaming by default so tokens land in the TUI viewport as they arrive. Chat transports (WhatsApp, Slack, Discord, …) use non-streaming completions because message-oriented transports batch delivery anyway — an intermediate delta stream would just be discarded before the final message is sent.

The streaming implementation in `internal/llm/anthropic/stream.go` consumes the SDK's `MessageStreamEvent` union:

| Event | Handled how |
|---|---|
| `message_start` | Emits `agent.StreamEvent{Kind: StreamMessageStart}`. |
| `content_block_start` | Emits `agent.StreamEvent{Kind: StreamContentStart}` with the block type. |
| `content_block_delta` | Emits `agent.StreamEvent{Kind: StreamTextDelta, Text: delta.Text}` for text; `input_json_delta` events accumulate into a partial tool-use input. |
| `content_block_stop` | Emits `agent.StreamEvent{Kind: StreamContentStop}`. |
| `message_delta` | Carries the final stop reason and cumulative usage. |
| `message_stop` | End of stream. |

The Bubble Tea TUI subscribes to these events via `agent.StreamTurn`, which orchestrates the stream/tool-use loop. See `internal/agent/stream_turn.go`.

## Tool use

Tool definitions from the `Registry` are converted to Anthropic's `tools` array in `toSDKTools`. Approval policies (`agent.approver`) apply — every `tool_use` block goes through `Approver.Approve` in the agent loop before execution. Denials surface back to the model as `tool_result` blocks with `is_error: true`, so the model can adapt (pick a different action, ask the user, give up gracefully).

<aside class="admonition" data-type="warning"><span class="admonition-title">Schema shape</span><p>The SDK expects the tool's <code>input_schema</code> to be a JSON Schema object with a top-level <code>properties</code> field. Rousseau's <code>tools.Definition</code> maps 1:1 — see <code>toSDKTools</code> in <code>internal/llm/anthropic/client.go</code>. Custom tools that emit non-object schemas will fail at request time.</p></aside>

## Rate-limit handling

The Anthropic API returns:

| Code | Meaning | rousseau's behaviour |
|---|---|---|
| 401 | Bad or missing key | Fails immediately, no retry. |
| 400 | Bad request (schema, encoding, prompt too long) | Fails immediately with the SDK's error message. |
| 429 | Per-minute rate limit exceeded | Surfaces as an `agent` error. `Complete` does not retry. |
| 529 | Overloaded (transient capacity) | Surfaces as an `agent` error. `Complete` does not retry. |
| 5xx | Server error | Surfaces as an `agent` error. `Complete` does not retry. |

**Retries are the caller's responsibility.** The `rousseau chat` TUI and the transport `RouterHandler` currently do not implement backoff — a 429 kills the turn. This is a deliberate design choice: retries interact with tool_use semantics (partial tool calls, idempotency), and the caller has the context to make the right decision. See `docs/GAP_ANALYSIS_2026.md` for the planned retry helper.

<aside class="admonition" data-type="tip"><span class="admonition-title">Handling 429 in a chat transport</span><p>Wrap the transport <code>RouterHandler</code> in a caller-level retry loop with exponential backoff and jitter. The <a href="/guides/rate-limits/">rate-limits guide</a> shows a worked example.</p></aside>

## Cost hygiene

- **Set `max_tokens` low** (2048–4096) for chat transports where replies rarely need to exceed a few paragraphs. `max_tokens` is a cap, not a target — you pay only for the output actually generated.
- **Enable `agent.compression`** to collapse old messages once the transcript is past `trigger_messages` (default 60). The summary is much cheaper than the raw transcript.
- **Use `CacheableMessages > 0`** when embedding the agent library — the direct API is where prompt caching pays off most.
- **Prefer Sonnet for tool-use loops.** Opus is more expensive and slower; unless you have measured wins on your particular task, Sonnet is the default for a reason.
- **Watch out for stream-abort billing.** If a stream is cancelled mid-response, the API still bills for tokens generated up to the cancellation point. Set a timeout ceiling in your caller.

## Troubleshooting

### `anthropic: complete: 401 unauthorized`

Your `ANTHROPIC_API_KEY` is missing, revoked, or set to a workspace/organisation you no longer have access to. Verify with `curl -H "x-api-key: $ANTHROPIC_API_KEY" https://api.anthropic.com/v1/messages`.

### `anthropic: complete: 400 messages: too many messages`

The transcript grew past the context window. Enable `agent.compression.enabled: true` (defaults are usually fine) and rerun. If compression is on and still fires, lower `trigger_messages` or increase `keep_recent` so the compressor triggers earlier.

### `anthropic: unsupported content block <type>`

The SDK returned a content block type rousseau does not model — currently only `text` and `tool_use` are supported (see `fromSDKResponse`). This can happen if the model emits `thinking` blocks (extended thinking mode). rousseau does not surface those yet; disable extended thinking in your provider config until support lands.

### 429s under sustained load

You are hitting the per-minute output-token rate limit. Options: (1) request a limit increase from Anthropic, (2) queue turns in the caller and process them serially, (3) switch to Bedrock or Vertex where enterprise quotas are usually higher.

### Prompt cache misses despite `CacheableMessages > 0`

Anthropic invalidates the cache when the prefix changes. Common causes: the system prompt is regenerated per turn (skills that shift with each user message), the model ID changed, or `MaxTokens` differs. Log the request payload and diff it across two turns to isolate.

## Related pages

- [Providers: claudecli](/providers/claudecli/) — subprocess vs direct API trade-offs.
- [Providers: Bedrock](/providers/bedrock/) — AWS-managed Claude with enterprise quotas.
- [Guides: Rate limits](/guides/rate-limits/) — the retry-and-backoff playbook.
- [Agent loop](/agent-loop/) — how streaming and tool use compose.
- [User Guide: Compression &amp; Recall](/user-guide/compression-recall/) — the mechanism that keeps input token counts sane.

## Further reading

- `internal/llm/anthropic/client.go` — `Complete`, message conversion, tool schema.
- `internal/llm/anthropic/stream.go` — streaming implementation.
- `internal/llm/anthropic/cache.go` — cache-marker helper.
- `internal/agent/stream_turn.go` — how the agent loop consumes streaming events.
- `internal/agent/compressor.go` — how the compressor primes `CacheableMessages`.
