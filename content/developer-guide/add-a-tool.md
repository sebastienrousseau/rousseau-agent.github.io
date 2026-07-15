---

# Front Matter (YAML)

author: "sebastian.rousseau@gmail.com (Sebastien Rousseau) "
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
description: "How to add a new built-in tool to rousseau-agent: declare a JSON schema, implement Execute, register with the tool registry."
keywords: "add tool, tool registry, json schema, execute, extend, custom tool"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/developer-guide/add-a-tool/"
subtitle: "Schema, Execute, register — three moving parts."
tags: "developer-guide, tools, extend"
title: "Add a Tool"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add tool, tool registry, json schema, execute, extend, custom tool"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Add a Tool"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 64
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-tool/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-tool/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Add a Tool"
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
twitter_description: "How to add a new built-in tool to rousseau-agent: declare a JSON schema, implement Execute, register with the tool registry."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Add a Tool"
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

`internal/tools/tool.go` (paraphrased):

```go
type Tool interface {
    Name() string
    Description() string
    InputSchema() map[string]any
    Execute(ctx context.Context, input json.RawMessage) (string, error)
}
```

Four methods, no lifecycle. Tools are stateless from the loop's perspective — any state the tool needs (a compiled regex cache, an in-process index) is a private field on the concrete type.

## Skeleton for a new tool

Let's add a hypothetical **`http_get`** tool that fetches a URL and returns its body.

### Step 1 — The type

```go
package builtin

import (
    "context"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "time"

    "github.com/sebastienrousseau/rousseau-agent/internal/tools"
)

// HTTPGetTool fetches a URL over HTTPS and returns the response body.
type HTTPGetTool struct {
    Timeout time.Duration
    client  *http.Client
}

// NewHTTPGetTool constructs an HTTPGetTool. Zero timeout uses 30s.
func NewHTTPGetTool(timeout time.Duration) *HTTPGetTool {
    if timeout == 0 {
        timeout = 30 * time.Second
    }
    return &HTTPGetTool{
        Timeout: timeout,
        client:  &http.Client{Timeout: timeout},
    }
}
```

### Step 2 — Metadata

```go
// Name satisfies tools.Tool.
func (*HTTPGetTool) Name() string { return "http_get" }

// Description satisfies tools.Tool.
func (*HTTPGetTool) Description() string {
    return "Fetch an HTTPS URL and return the response body. Input: url (string). Redirects are followed up to 10 hops. Response is capped at 1 MiB."
}
```

The **description is model-facing**. It should read like a short docstring for another engineer — what the tool does, what its inputs mean, what the output shape is.

### Step 3 — Input schema

```go
// InputSchema satisfies tools.Tool.
func (*HTTPGetTool) InputSchema() map[string]any {
    return map[string]any{
        "type": "object",
        "properties": map[string]any{
            "url": map[string]any{
                "type":        "string",
                "description": "Absolute HTTPS URL to fetch.",
            },
        },
        "required": []string{"url"},
    }
}
```

Keep the schema strict. Every property gets a `description`. The `required` array is enforced by the model's tool-use validator — missing fields cause a `tool_use` retry, not a runtime error.

### Step 4 — Execute

```go
type httpGetInput struct {
    URL string `json:"url"`
}

// Execute satisfies tools.Tool.
func (t *HTTPGetTool) Execute(ctx context.Context, raw json.RawMessage) (string, error) {
    var in httpGetInput
    if err := json.Unmarshal(raw, &in); err != nil {
        return "", fmt.Errorf("http_get: parse input: %w", err)
    }
    if in.URL == "" {
        return "", fmt.Errorf("http_get: url is required")
    }
    // Refuse plaintext HTTP; refuse non-http schemes.
    if !strings.HasPrefix(in.URL, "https://") {
        return "", fmt.Errorf("http_get: only https:// URLs are permitted")
    }

    req, err := http.NewRequestWithContext(ctx, http.MethodGet, in.URL, nil)
    if err != nil {
        return "", fmt.Errorf("http_get: build request: %w", err)
    }
    req.Header.Set("user-agent", "rousseau-agent/http_get")

    resp, err := t.client.Do(req)
    if err != nil {
        return "", fmt.Errorf("http_get: transport: %w", err)
    }
    defer func() { _ = resp.Body.Close() }()

    body, err := io.ReadAll(io.LimitReader(resp.Body, 1<<20))
    if err != nil {
        return "", fmt.Errorf("http_get: read body: %w", err)
    }
    return fmt.Sprintf("HTTP %d\n%s", resp.StatusCode, string(body)), nil
}

// Compile-time interface satisfaction check.
var _ tools.Tool = (*HTTPGetTool)(nil)
```

### Step 5 — Register

Wire it up in `internal/cli/chat.go` (and every other command that constructs a registry — grep for `registry.MustRegister` to find them):

```go
registry.MustRegister(builtin.NewHTTPGetTool(30 * time.Second))
```

Once registered, the tool is available to the model on every turn.

### Step 6 — Tests

Follow `internal/tools/builtin/read_test.go` for the pattern:

```go
func TestHTTPGetTool_Execute_Success(t *testing.T) {
    srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
        _, _ = w.Write([]byte("hello"))
    }))
    defer srv.Close()

    // The tool refuses plaintext HTTP; wrap the test server behind httptest.NewTLSServer instead
    // for a real integration test, or expose an internal seam that permits `http://` in tests only.
    // The skeleton here is illustrative.
}

func TestHTTPGetTool_Execute_RejectsPlaintextHTTP(t *testing.T) {
    tool := builtin.NewHTTPGetTool(0)
    _, err := tool.Execute(context.Background(), json.RawMessage(`{"url":"http://example.com"}`))
    require.Error(t, err)
    require.Contains(t, err.Error(), "only https")
}
```

### Step 7 — Approval policy

The tool is now available to the model, subject to the [approval policy](/user-guide/approval-policies/). Recommend a deny rule in the docs for the default posture:

```yaml
deny:
  - {tool: http_get, match: "\"url\":\"https://(169\\.254|10\\.|192\\.168\\.|172\\.(1[6-9]|2[0-9]|3[01])\\.)"}
```

This blocks the tool from calling AWS IMDS or private RFC1918 space — a common ask for HTTP-fetching tools.

### Step 8 — Docs

Add a section to `content/user-guide/tools.md` describing the new tool: schema, semantics, safety notes. Follow the shape of the existing five tools.

## Contract details

- **Statelessness**: `Execute` must not carry state between calls that isn't explicitly private to the tool's own fields. Two concurrent turns on two sessions may call the same tool simultaneously.
- **Context respect**: `Execute` must honour `ctx` cancellation. Long-running work should periodically check `ctx.Err()` or route the work through a context-aware library call.
- **No panics**: return errors instead. The agent loop converts an error into a `tool_result` with `IsError: true`, which the model can adapt to.
- **Return shape**: the output is a plain string, fed back to the model on the next turn. Include enough structure (e.g. line numbers, status codes) for the model to reason about it.

## Custom tools without touching the source

If you don't want to fork rousseau, embed the agent loop in your own binary and register your tools there:

```go
registry := tools.NewRegistry()
registry.MustRegister(builtin.NewReadTool())
registry.MustRegister(builtin.NewWriteTool())
// ...
registry.MustRegister(mypkg.NewMyTool())

ag := agent.New(provider, registry, logger, agent.Options{})
```

See `examples/embed-agent/` in the source tree for a complete embedding example.

## Common pitfalls

- **Over-broad schema.** Requiring only `type: object` gives the model no help. Enumerate every property, describe every field.
- **Blocking on I/O without a deadline.** Always use `NewRequestWithContext`, always set an `http.Client{Timeout: ...}`, always honour `ctx`.
- **Returning too much.** The output is fed back to the model in the next turn. A 1 MB response burns tokens; cap it.
- **Escaping side effects.** A tool that mutates the world should log what it did in the return string so the approver's audit trail is complete.
- **Forgetting the compile-time interface check.** `var _ tools.Tool = (*MyTool)(nil)` at package scope catches interface drift at build time.

## Next

- [User Guide: Tools](/user-guide/tools/) — the five built-in tools with schemas.
- [User Guide: Approval Policies](/user-guide/approval-policies/) — how to gate the new tool.
- [Testing](/developer-guide/testing/) — the pattern for tool tests.
