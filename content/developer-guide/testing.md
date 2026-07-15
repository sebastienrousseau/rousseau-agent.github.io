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
description: "Testing pattern for rousseau-agent: dependency injection via interfaces (WSConn, IMAPClient, HTTPClient), fake generators, race + coverage thresholds."
keywords: "testing, dependency injection, fake, mock, coverage, race, go test, httptest"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/developer-guide/testing/"
subtitle: "Dependency injection, fakes, race, coverage."
tags: "developer-guide, testing, di, fakes"
title: "Testing"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "testing, dependency injection, fake, mock, coverage, race, go test, httptest"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Testing"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 65
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/testing/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/testing/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Testing"
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
twitter_description: "Testing pattern for rousseau-agent: dependency injection via interfaces (WSConn, IMAPClient, HTTPClient), fake generators, race + coverage thresholds."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Testing"
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

## The pattern

Every package that talks to the outside world defines a small interface for its dependency, takes that interface as a constructor parameter, and injects a real client in `cli/*.go` (production) or a fake in `*_test.go` (tests).

Examples in the tree:

| Package | Interface | Real | Fake for tests |
|---|---|---|---|
| `internal/transport/whatsapp` | `WSConn` | whatsmeow's WebSocket | in-memory struct with a `send` channel |
| `internal/transport/email` | `IMAPClient` | `emersion/go-imap` client | scripted channel of messages |
| `internal/transport/whatsapp` | `Sender` | direct whatsmeow send | in-memory slice for assertion |
| `internal/llm/*` | `HTTPClient` (indirect via `http.Client`) | `http.DefaultTransport` | `httptest.NewServer` |
| `internal/state/sqlite` | `state.Store` (interface owned by `state`) | `modernc.org/sqlite` on-disk | in-memory `:memory:` DSN |
| `internal/agent` | `Provider`, `Approver`, `Compressor`, `RecallProvider` | concrete `llm/*` types | struct implementations in `_test.go` |

The rule: **interface with the consumer, implementation with the provider.** `Provider` is defined in `agent`, not in `llm/anthropic`. `Store` is defined in `state`, not in `state/sqlite`.

## Running the gate

```sh
make check
```

is equivalent to:

```sh
go vet ./...
golangci-lint run
go test -race -count=1 -covermode=atomic ./...
govulncheck ./...
```

CI runs the same command on `ubuntu-latest` and `macos-latest`. If it passes locally, it passes in CI — barring platform-specific bugs, which is why macOS is in the matrix.

## Race detector

`-race` is non-negotiable. Every daemon in rousseau involves multiple goroutines (transport pump, agent loop, cron scheduler, session-store writer). A race in any one of them is a real bug.

If you find a test that only fails under `-race`, that is a bug in the code under test, not in the test. Do not disable `-race`.

## Coverage floor

The current coverage floor is **75% total**. Core packages (`internal/agent`, `internal/tools`, `internal/state/sqlite`) sit at 85–100% and are held there by the pre-existing test suite; new code in those packages should not lower them.

A CI job runs after `go test -race -covermode=atomic ./... -coverprofile=coverage.out` and inspects `coverage.out`. Failing the floor fails the build.

## Fake generators

Rousseau does not use a mock-generation library. Fakes are hand-written struct types, small enough to read at a glance:

```go
type fakeProvider struct {
    responses []agent.Response
    calls     []agent.Request
}

func (f *fakeProvider) Complete(_ context.Context, req agent.Request) (agent.Response, error) {
    f.calls = append(f.calls, req)
    if len(f.responses) == 0 {
        return agent.Response{}, errors.New("no more canned responses")
    }
    resp := f.responses[0]
    f.responses = f.responses[1:]
    return resp, nil
}
```

Two properties fall out:

1. The fake is inspectable — `calls` captures every request, so assertions can check what the code under test emitted.
2. The fake is deterministic — canned responses are consumed in order.

## `httptest` for HTTP-shaped providers

Every LLM adapter that talks HTTP uses `httptest.NewServer` for tests:

```go
srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
    _ = json.NewEncoder(w).Encode(map[string]any{
        "role":       "assistant",
        "content":    []map[string]any{{"type": "text", "text": "hello"}},
        "stop_reason":"end_turn",
    })
}))
defer srv.Close()

p := anthropic.New(anthropic.Config{
    APIKey:  "test",
    BaseURL: srv.URL,
    Model:   "test-model",
})
```

For SSE-style streaming, the same technique works — `http.Flusher` is available on the response writer.

## Fuzz corpus

Every parser has a `Fuzz*` function. Run the full battery:

```sh
make fuzz
```

Under CI, fuzz runs for a bounded time (`-fuzztime`). Locally, run longer to seed the corpus.

## Table-driven tests

Rousseau's tests lean heavily on table-driven form. Example shape:

```go
func TestPatternApprover_Approve(t *testing.T) {
    tests := []struct {
        name     string
        approver *agent.PatternApprover
        req      agent.ApprovalRequest
        want     agent.Decision
    }{
        {
            name:     "allow read",
            approver: &agent.PatternApprover{Allow: []agent.PatternRule{{ToolName: "read"}}},
            req:      agent.ApprovalRequest{ToolName: "read"},
            want:     agent.DecisionAllow,
        },
        {
            name:     "deny wins over allow",
            approver: &agent.PatternApprover{
                Allow: []agent.PatternRule{{ToolName: "bash"}},
                Deny:  []agent.PatternRule{{ToolName: "bash", Match: "rm"}},
            },
            req:  agent.ApprovalRequest{ToolName: "bash", Input: json.RawMessage(`{"command":"rm -rf /"}`)},
            want: agent.DecisionDeny,
        },
    }
    for _, tc := range tests {
        t.Run(tc.name, func(t *testing.T) {
            got, _ := tc.approver.Approve(context.Background(), tc.req)
            require.Equal(t, tc.want, got)
        })
    }
}
```

This scales — every new rule shape becomes one table row.

## Goroutine leaks

Tests that spawn goroutines must join them. Common patterns:

- Use `context.WithCancel` and `cancel()` at the end of the test.
- Use a `sync.WaitGroup` and `wg.Wait()`.
- Consume every channel to `close`.

If a test leaks a goroutine, `go test -race` may catch it via a nil-receiver panic on the leaked goroutine after the test file's `main` has exited. Cheaper to be disciplined up front.

## Deterministic time

For time-sensitive tests (cron, recall recency ranking), inject a `time.Time` provider:

```go
type Clock interface {
    Now() time.Time
}
```

Wire the real `time.Now` in `cli/*` and a fake `time.Time` in the test. The `internal/cron/scheduler.go` scheduler uses this pattern.

## Testing the TUI

`internal/tui/model_test.go` uses `bubbletea`'s `TestModel` helper. `View()` is a pure string function of the model, so most assertions become "run this update, expect this View output".

## What not to test

- Third-party libraries. Rousseau does not shadow whatsmeow's or `signal-cli`'s upstream tests.
- The Go standard library. `net/http` works.
- CLI flag registration by Cobra. Cobra's own tests cover that.

Instead, test the code you write: the wire-up, the branching, the error paths, the recovery paths.

## Next

- [Add a transport](/developer-guide/add-a-transport/) — the fake-injection pattern applied to a full transport.
- [Add a provider](/developer-guide/add-a-provider/) — `httptest` in action.
- [Contributing](/developer-guide/contributing/) — the PR checklist.
