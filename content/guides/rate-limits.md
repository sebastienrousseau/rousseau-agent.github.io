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
description: "How rousseau-agent handles provider rate limits: 429s, exponential backoff, prompt-cache markers, and per-provider cost notes."
keywords: "rate limits, 429, backoff, retry, prompt cache, anthropic, bedrock, cost"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/guides/rate-limits/"
subtitle: "429 handling, backoff, and cache-marker optimisation."
tags: "guides, rate limits, prompt cache, anthropic"
title: "Guide: Rate limits"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "rate limits, 429, backoff, retry, prompt cache, anthropic, bedrock, cost"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide: Rate limits"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 36
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/rate-limits/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/rate-limits/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guide: Rate limits"
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
twitter_title: "Guide: Rate limits"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">What you'll learn</span><p>Provider-by-provider rate limits, per-token cost, retry semantics, cache economics, and a caller-side retry-with-backoff recipe. See each provider's pricing page for authoritative numbers — the table below is a snapshot.</p></aside>

## Where rate limiting happens

Rousseau does not implement its own rate-limit handling. Every provider client delegates to the upstream SDK:

- **Anthropic direct** — `anthropic-sdk-go` handles HTTP retries, respects `Retry-After`, applies exponential backoff on 5xx and 429. See `internal/llm/anthropic/client.go`.
- **Bedrock** — `aws-sdk-go-v2` handles throttling errors with adaptive retries.
- **Vertex** — Google auth libraries handle their own retries.
- **OpenAI / OpenRouter / Ollama** — the Go OpenAI-compatible client handles 429s.
- **claudecli** — Claude Code's own `claude` binary handles limits. Rousseau just shells out.

Failed requests surface as `turn.failed`, `whatsapp.handler_failed`, or `cron.run_failed` slog events. The message text will include the provider's error string (typically `429 Too Many Requests` with a suggested backoff).

## When you actually hit a limit

Symptoms in the logs:

```jsonl
{"level":"ERROR","msg":"whatsapp.handler_failed","err":"anthropic: complete: 429 Too Many Requests"}
```

Because rousseau treats a turn as failed on unrecoverable errors, the operator sees the failure in the transport reply — the daemon does not silently swallow it. This is intentional.

## Reducing rate-limit pressure

Three levers, in order of impact:

### 1. Prompt cache markers (Anthropic direct)

`applyCacheMarkers` in `internal/llm/anthropic/client.go` marks a leading window of messages for the Anthropic ephemeral prompt cache. When `CacheableMessages > 0`, the system prompt is also cache-marked. Cached input tokens are billed at roughly 10% of standard input rates and cache hits do not consume the standard input rate-limit budget.

The agent (`internal/agent/agent.go`) opts into this on multi-turn sessions. If you build custom loops on top of rousseau's Go API, set `Request.CacheableMessages` and `Request.System` — even a shallow cache hit shaves both cost and rate-limit pressure.

Cache markers are Anthropic-direct only today. Bedrock, Vertex, and OpenAI-compat providers ignore them.

### 2. Compression

For long sessions on a pay-per-token provider (Anthropic direct, Bedrock, Vertex, OpenRouter), enable compression:

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60      # from CompressionConfig default
    keep_recent: 8
```

The `LLMCompressor` (`internal/agent/compressor.go`) summarises the oldest slice of the session into a single synthetic user message when message count crosses `trigger_messages`, and preserves the last `keep_recent` messages verbatim. Fewer tokens per turn = less rate-limit pressure.

Compression is off by default because the reference deployment uses `claudecli` on a subscription tier, where token count is not billed.

### 3. Slower cron cadence

For pure background daemons, halving the cron cadence halves the requests. `rousseau cron` cadences are cron expressions — go from every 15 minutes to every hour if the freshness requirement allows it.

## Approximate cost by provider

Rate limits and per-token cost move independently, but the two are usually correlated (paid tiers have higher limits). Rough guide as of 2026-07:

| Provider | Input $/MTok (Sonnet-class) | Output $/MTok | Cache read $/MTok |
|---|---|---|---|
| `anthropic` direct | ~3 | ~15 | ~0.30 |
| `bedrock` (Sonnet-4.6) | ~3 | ~15 | Cache: N/A at time of writing |
| `vertex` (Anthropic on Vertex) | ~3 | ~15 | Cache: N/A at time of writing |
| `openrouter` | model-dependent | model-dependent | provider-dependent |
| `ollama` self-hosted | $0 | $0 | $0 (you pay compute) |
| `claudecli` | subscription-tier billing | included | N/A |

Get the current numbers from each provider's pricing page.

## When the SDK exhausts retries

If the provider's SDK gives up, rousseau surfaces the final error. The turn is lost — there is no queue and no on-disk retry. Two mitigations:

- **Message the operator through the same channel.** The turn failure is visible in the transport reply; the operator can rephrase.
- **Fall back to a second provider by hand.** See [Guides: Multi-provider](/guides/multi-provider/) for the two-daemon pattern.

Automatic cross-provider failover is a roadmap item.

## Debugging rate-limit trouble

1. Set `log.level: debug` in `config.yaml`. The SDK debug output shows the exact `Retry-After` value.
2. Look for `turn.failed`, `whatsapp.handler_failed`, `cron.run_failed` in the journal.
3. Check the provider dashboard (Anthropic Console, AWS CloudWatch, GCP Cloud Monitoring) for actual quota consumption.
4. If you're on a subscription tier, watch for daily-quota resets — the SDK error usually includes the reset time.

## Provider-by-provider quick reference

<aside class="admonition" data-type="warning"><span class="admonition-title">Cite your sources</span><p>Pricing and limits change without notice. The numbers in this table are as of mid-2026 and are illustrative. Always link to the provider's current pricing page for authoritative values.</p></aside>

| Provider | Retry behaviour | Rate signal | Cost per 1M input | Cost per 1M output | Cache read cost |
|---|---|---|---|---|---|
| `anthropic` direct | SDK retries 5xx; 429 with `Retry-After` respected | `429 Too Many Requests` header carries reset time | ~$3 (Sonnet) | ~$15 (Sonnet) | ~$0.30 |
| `bedrock` | AWS SDK adaptive retry | `ThrottlingException` | ~$3 (Sonnet) | ~$15 (Sonnet) | not yet |
| `vertex` | Google SDK exponential retry | `429 RESOURCE_EXHAUSTED` | ~$3 (Sonnet) | ~$15 (Sonnet) | not yet |
| `openai` | SDK retries 5xx; 429 respected | `429 Too Many Requests` | model-specific | model-specific | model-specific |
| `openrouter` | passthrough to underlying provider | provider-dependent | model-specific | model-specific | provider-dependent |
| `ollama` | SDK retries; local so rarely fires | none | $0 (compute cost) | $0 (compute cost) | N/A |
| `claudecli` | subprocess errors surface; no rousseau-side retry | opaque | subscription | subscription | opaque |

Authoritative sources:

- [Anthropic pricing](https://www.anthropic.com/pricing)
- [AWS Bedrock pricing](https://aws.amazon.com/bedrock/pricing/)
- [Vertex AI pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)
- [OpenAI pricing](https://openai.com/pricing)
- [OpenRouter model list](https://openrouter.ai/models)

## Caller-side retry recipe

Rousseau does not retry inside `Complete`. If you embed the agent library, wrap `Turn` in your own retry loop with exponential backoff and jitter:

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

## Troubleshooting

### `429 Too Many Requests` every request

You are on a low tier or another workload is consuming the quota. Options: (1) request a limit increase, (2) split load across providers, (3) run `claudecli` for subscription-only workloads.

### `529 Overloaded` intermittently

Anthropic's system is at capacity. Not per-account throttling — the whole region is loaded. Retry with backoff.

### Cache markers set but no visible cost saving

Verify that `CacheableMessages` is actually being set. `applyCacheMarkers` in `internal/llm/anthropic/cache.go` is a no-op for zero. Also verify the prefix is stable — a system prompt that regenerates per turn defeats caching.

### `ThrottlingException` on Bedrock with low volume

Bedrock quota is per-account-per-model-per-region. Some models default to very low quotas (2–5 requests per minute). Request an increase in the Service Quotas console.

### Slow API responses despite low usage

Some providers de-prioritise low-tier accounts under global load. Anthropic's `x-ratelimit-*` response headers indicate current bucket state — inspect them if you have SDK access.

## Related pages

- [Providers: Anthropic](/providers/anthropic/) — cache-marker details.
- [Configuration](/configuration/) — every compression knob.
- [User Guide: Compression + Recall](/user-guide/compression-recall/) — deeper compression discussion.
- [Guides: Multi-provider](/guides/multi-provider/) — split load across endpoints.
- [Guides: Rate/Model Swap](/guides/rate-model-swap/) — hot-swap providers on failure.

## Further reading

- `internal/llm/anthropic/client.go` — SDK invocation.
- `internal/llm/anthropic/cache.go` — cache-marker helper.
- `internal/agent/agent.go` — where turn failures surface.
- Provider pricing pages linked above.
