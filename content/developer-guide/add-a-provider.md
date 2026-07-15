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
description: "How to add a sixth LLM provider to rousseau-agent: implement Provider.Complete and optionally StreamingProvider.CompleteStream."
keywords: "add provider, llm, chat completion, streaming, agent provider, extend"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/developer-guide/add-a-provider/"
subtitle: "Provider.Complete and StreamingProvider.CompleteStream."
tags: "developer-guide, provider, llm, extend"
title: "Add a Provider"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add provider, llm, chat completion, streaming, agent provider, extend"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Add a Provider"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 63
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-provider/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-provider/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Add a Provider"
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
twitter_description: "How to add a sixth LLM provider to rousseau-agent: implement Provider.Complete and optionally StreamingProvider.CompleteStream."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Add a Provider"
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

## The interface

`internal/agent/provider.go` (paraphrased):

```go
type Request struct {
    SessionID string
    System    string
    Messages  []Message
    Tools     []ToolDefinition
}

type Response struct {
    Message    Message
    StopReason StopReason
}

// Provider drives a single round-trip.
type Provider interface {
    Complete(ctx context.Context, req Request) (Response, error)
}

// StreamingProvider streams response deltas as they arrive.
type StreamingProvider interface {
    Provider
    CompleteStream(ctx context.Context, req Request) (StreamReader, error)
}
```

Every LLM adapter satisfies at least `Provider`. `StreamingProvider` is opt-in — the TUI and chat-transport handlers will fall back to the non-streaming path when a provider does not implement it.

`StopReason` is one of `StopEndTurn`, `StopToolUse`, `StopMaxTokens`. The agent loop treats `StopEndTurn` as terminal and `StopToolUse` as "the model wants a tool call".

## Skeleton for a new provider

Let's add a hypothetical **Cohere Command R** provider.

### Step 1 — Directory

```
internal/llm/cohere/
├── client.go        # Config, New
├── complete.go      # Provider.Complete
├── stream.go        # StreamingProvider.CompleteStream (optional)
└── *_test.go
```

### Step 2 — `client.go`

```go
// Package cohere implements the Cohere Command R provider.
package cohere

import (
    "net/http"
    "time"
)

// Config configures the Cohere provider.
type Config struct {
    APIKey    string
    Model     string
    BaseURL   string
    MaxTokens int64
}

// Provider is the Cohere adapter.
type Provider struct {
    cfg    Config
    client *http.Client
}

// New constructs a Provider.
func New(cfg Config) *Provider {
    if cfg.BaseURL == "" {
        cfg.BaseURL = "https://api.cohere.com/v1"
    }
    if cfg.MaxTokens == 0 {
        cfg.MaxTokens = 4096
    }
    return &Provider{
        cfg:    cfg,
        client: &http.Client{Timeout: 120 * time.Second},
    }
}
```

### Step 3 — `complete.go`

Implement `Complete`:

```go
package cohere

import (
    "bytes"
    "context"
    "encoding/json"
    "fmt"
    "net/http"

    "github.com/sebastienrousseau/rousseau-agent/internal/agent"
)

// Complete satisfies agent.Provider.
func (p *Provider) Complete(ctx context.Context, req agent.Request) (agent.Response, error) {
    body, err := p.encodeRequest(req)
    if err != nil {
        return agent.Response{}, fmt.Errorf("cohere: encode: %w", err)
    }

    httpReq, err := http.NewRequestWithContext(ctx, http.MethodPost, p.cfg.BaseURL+"/chat", bytes.NewReader(body))
    if err != nil {
        return agent.Response{}, err
    }
    httpReq.Header.Set("content-type", "application/json")
    httpReq.Header.Set("authorization", "Bearer "+p.cfg.APIKey)

    httpResp, err := p.client.Do(httpReq)
    if err != nil {
        return agent.Response{}, fmt.Errorf("cohere: transport: %w", err)
    }
    defer httpResp.Body.Close()

    if httpResp.StatusCode >= 400 {
        return agent.Response{}, fmt.Errorf("cohere: HTTP %d", httpResp.StatusCode)
    }

    var raw cohereResponse
    if err := json.NewDecoder(httpResp.Body).Decode(&raw); err != nil {
        return agent.Response{}, fmt.Errorf("cohere: decode: %w", err)
    }
    return p.decodeResponse(raw), nil
}

// Compile-time interface check.
var _ agent.Provider = (*Provider)(nil)
```

The bodies `encodeRequest`, `decodeResponse`, and the `cohereResponse` shape are Cohere-specific — they translate rousseau's provider-agnostic `agent.Request` and `agent.Response` types to and from Cohere's wire format.

### Step 4 — Streaming (optional)

If Cohere supports SSE-style streaming, implement `CompleteStream`. Skip it for a first pass; the agent loop falls back to non-streaming automatically.

### Step 5 — Config surface

Add `CohereConfig` to `internal/config/config.go`:

```go
type CohereConfig struct {
    APIKey    string `mapstructure:"api_key"`
    Model     string `mapstructure:"model"`
    BaseURL   string `mapstructure:"base_url"`
    MaxTokens int64  `mapstructure:"max_tokens"`
}
```

Add a field to `Config`:

```go
Cohere CohereConfig `mapstructure:"cohere"`
```

Extend `setDefaults` with a sensible model default:

```go
v.SetDefault("cohere.model", "command-r-plus")
```

### Step 6 — CLI wire-up

In `internal/cli/provider.go`, extend `buildProvider(cfg *config.Config)`:

```go
func buildProvider(cfg *config.Config) (agent.Provider, error) {
    switch cfg.Provider {
    // ...existing cases...
    case "cohere":
        return cohere.New(cohere.Config{
            APIKey:    cfg.Cohere.APIKey,
            Model:     cfg.Cohere.Model,
            BaseURL:   cfg.Cohere.BaseURL,
            MaxTokens: cfg.Cohere.MaxTokens,
        }), nil
    default:
        return nil, fmt.Errorf("unknown provider %q", cfg.Provider)
    }
}
```

Extend `rousseau doctor` (`internal/cli/doctor.go`) to add a `provider.cohere.*` check block when `cfg.Provider == "cohere"`. Mirror the existing anthropic checks.

## Contract details the agent loop assumes

- **`Complete` respects `ctx`.** Long HTTP requests must honour context cancellation, or the daemon's `SIGTERM` shutdown will hang.
- **Tool-use round-trip.** When the model emits `tool_use` blocks, the response `StopReason` must be `StopToolUse` and the message content must include `Content{Kind: ContentToolUse, ToolUse: &ToolUse{Name, Input, ID}}` for each requested call. The agent loop routes each to the `Registry`, executes it, and pipes the results back in the next `Complete` call.
- **`tool_result` handling.** On the next call, `req.Messages` contains a user message whose content includes `Content{Kind: ContentToolResult, ToolResult: &ToolResult{ToolUseID, Output, IsError}}` for each executed call. The provider must render these into whatever shape the upstream API expects.
- **Compile-time interface check.** `var _ agent.Provider = (*Provider)(nil)` at package scope catches interface drift at build time.

## Streaming contract

If you implement `StreamingProvider`:

```go
type StreamReader interface {
    Next(ctx context.Context) (StreamChunk, error)
    Close() error
}

type StreamChunk struct {
    Delta     string       // partial text delta
    Done      bool         // final chunk
    Response  *Response    // final Response, non-nil only on Done
}
```

The TUI and the chat-transport handlers read deltas as they arrive; the final `Response` is used to append the fully-formed assistant message to the session.

## Prompt caching

`internal/llm/anthropic` places `cache_control` markers on the last two messages of the request. If your provider supports prompt caching, do the same — it turns compression + recall (see [Compression + Recall](/user-guide/compression-recall/)) from a token-hungry pattern into a cheap one.

## Testing

Use `httptest.NewServer` to stand up a fake upstream. `internal/llm/anthropic/*_test.go` is the reference. The pattern:

1. Start `httptest.NewServer` with a handler that returns canned JSON.
2. Construct the provider pointing `BaseURL` at the test server.
3. Call `Complete` with a canned `Request`.
4. Assert on the returned `Response` shape.

For streaming, `httptest` supports Server-Sent Events too — see `internal/llm/anthropic/stream.go`.

## Docs

Add `content/providers/cohere.md` in this docs site. Follow the shape of `content/providers/anthropic.md` — description, config surface, auth details, provider-specific caveats.

## Common pitfalls

- **Silently rewriting `Messages`.** The agent loop is the source of truth for conversation state. Providers must translate the shape without mutating the semantics.
- **Losing tool-use IDs.** Every `ToolUse.ID` in a response must match a `ToolResult.ToolUseID` on the next request. If your provider assigns its own IDs, translate carefully.
- **Ignoring `MaxTokens`.** Some providers reject requests without an explicit limit. Set a sane default in `New`.
- **Blocking the loop with retry policies.** Retries belong in the provider adapter, not in the agent loop. Bound them; failing fast is better than hanging.

## Next

- [Testing](/developer-guide/testing/) — how to write the provider's `_test.go`.
- [Add a tool](/developer-guide/add-a-tool/) — the smallest extension point.
- [Configuration](/configuration/) — the config surface every provider exposes.
