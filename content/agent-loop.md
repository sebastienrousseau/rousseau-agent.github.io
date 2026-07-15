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
changefreq: "weekly"
description: "Embed rousseau-agent's agent loop into your own Go binary. Provider and StreamingProvider interfaces, Session/Message/Turn shapes, tool registration, approval policies, compression, FTS5 recall."
keywords: "library, embedding, agent.Provider, agent.Session, agent.Turn, tool registry, approver, compression, FTS5, recall"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/agent-loop/"
subtitle: "Library-embedding contract: Provider, Registry, Session, Turn."
tags: "library, embedding, reference"
title: "Agent-loop Reference"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "library, embedding, agent.Provider, agent.Session, agent.Turn, tool registry, approver, compression, FTS5, recall"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Agent-loop Reference"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 22
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/agent-loop/index.html"
item_link: "https://docs.rousseau-agent.dev/agent-loop/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Agent-loop Reference"
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
twitter_description: "Embed rousseau-agent's agent loop into your own Go binary. Provider and StreamingProvider interfaces, Session/Message/Turn shapes, tool registration, approval policies, compression, FTS5 recall."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Agent-loop Reference"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">What you'll learn</span><p>The full anatomy of one <code>Agent.Turn</code>: how <code>Compressor</code>, <code>SkillsProvider</code>, and <code>RecallProvider</code> compose the system prompt, how the model's <code>tool_use</code> blocks pass through the <code>Approver</code>, how tool results are folded back into the session, and how the loop terminates. Read <code>internal/agent/agent.go</code> alongside this page.</p></aside>

## rousseau as a library

`rousseau-agent` is a library as much as it is a daemon. The agent loop, tool registry, and provider abstractions have no CLI dependency. You can compose them into your own binary without importing `internal/cli` or any transport package.

Every exported identifier has a godoc comment. `pkg.go.dev/github.com/sebastienrousseau/rousseau-agent` renders the full reference.

## Anatomy of a Turn

The `Agent.Turn` function is defined in `internal/agent/agent.go`. In prose, one turn does this:

```
Turn(ctx, session)
  │
  ├── 1. Session guard: empty session → ErrEmptySession
  │
  ├── 2. Compressor.Compress(ctx, session)
  │     • If enabled and len(messages) > TriggerMessages, summarise older
  │       messages in place. Sets CacheableMessages on next Request.
  │
  ├── 3. registry.Definitions() → toolDefs
  │
  └── loop up to MaxIterations (default 32) times:
        │
        ├── a. Build Request{
        │       SessionID:         session.ID,
        │       System:            systemPrompt(session),
        │       Messages:          session.Messages,
        │       Tools:             toolDefs,
        │       CacheableMessages: <hint from compressor>,
        │     }
        │
        ├── b. resp = provider.Complete(ctx, req)
        │
        ├── c. session.Append(resp.Message)
        │
        ├── d. Switch on resp.StopReason:
        │       • StopEndTurn → return resp.Message (success)
        │       • StopMaxTokens / StopOther → return resp.Message
        │       • StopToolUse → continue to (e)
        │
        ├── e. runTools(ctx, resp.Message, sessionID):
        │       For each tool_use block:
        │         • registry.Get(name) → tool or ErrToolNotFound
        │         • approver.Approve(...)
        │             DecisionDeny → tool_result with is_error=true and reason
        │             DecisionAllow → tool.Execute(ctx, input)
        │               err → tool_result with is_error=true and err.Error()
        │               ok  → tool_result with output
        │
        └── f. session.Append(Message{Role: user, Content: []tool_result})
              Loop.

  MaxIterations exhausted → ErrMaxIterations
```

### Backpressure and cancellation

The `ctx` passed to `Turn` propagates through everything: `Compressor.Compress`, every `Provider.Complete`, every `Tool.Execute`, and every `Approver.Approve`. Cancel the context to abort mid-turn — the current iteration's provider call returns `context.Canceled`, the session is left with the model's last complete message plus the outstanding tool call, and callers can decide whether to retry.

The built-in `BashTool` wraps each command in its own `context.WithTimeout` (default 60s, configurable) so a runaway command cannot exceed the outer context.

### System-prompt composition

`systemPrompt(ctx, session)` in `agent.go` line 138 assembles up to three parts:

```
<Options.SystemPrompt>

<SkillsProvider.SystemAppendix(session)>

<RecallProvider.SystemAppendix(ctx, session)>
```

Any part that returns empty is omitted. The result is `strings.Join(parts, "\n\n")`. Composition happens once per iteration (not per turn) so skills and recall react to whichever message is most recent — including intermediate tool results, when relevant.

### Context-window management

Large sessions eventually exceed the model's context window. Rousseau does not truncate on its own — that is `Compressor`'s job. The default `NoopCompressor` never rewrites, so embedders who want an unbounded transcript in a small window must either provide their own compressor or accept the model-side error when the window fills.

`LLMCompressor` (see below) collapses messages older than `KeepRecent` into a single summary block once the count exceeds `TriggerMessages`. The summary is generated by the same provider that runs the turn, so it costs one extra completion per compression cycle.

## The Provider interface

`internal/agent/provider.go`:

```go
type Provider interface {
    Name() string
    Complete(ctx context.Context, req Request) (Response, error)
}

type StreamingProvider interface {
    Provider
    CompleteStream(ctx context.Context, req Request, out chan<- StreamEvent) error
}
```

`Complete` runs a single non-streaming turn. `Request` carries `SessionID`, `System`, `Messages`, `Tools`, and `CacheableMessages` (an ephemeral-cache hint). `Response` returns a single assistant `Message`, a `StopReason` (`end_turn`, `tool_use`, `max_tokens`, `other`), and `Usage` token counts.

Every shipped provider (Anthropic, Bedrock, Vertex, OpenAI-compatible, claudecli) implements `Provider`. Every one except `claudecli` implements `StreamingProvider`.

## Session, Message, Turn

`internal/agent/session.go` and `internal/agent/message.go`:

```go
type Session struct {
    ID        string
    Title     string
    Messages  []Message
    CreatedAt time.Time
    UpdatedAt time.Time
}

type Message struct {
    Role      Role     // "user", "assistant", "system"
    Content   []Content
    CreatedAt time.Time
}

type Content struct {
    Kind       ContentKind  // "text", "tool_use", "tool_result"
    Text       string
    ToolUse    *ToolUse
    ToolResult *ToolResult
}
```

A `Session` is append-only. Every user message is a call to `Agent.Turn(ctx, session)`; the agent loop mutates the session in place and returns the final assistant `Message`.

## Registering tools

`internal/tools`:

```go
registry := tools.NewRegistry()
registry.MustRegister(builtin.NewReadTool())
registry.MustRegister(builtin.NewGrepTool(0, 0))
registry.MustRegister(builtin.NewEditTool())
```

Every tool declares a strict JSON schema. Adding your own is a `Tool` implementation:

```go
type Tool interface {
    Name() string
    Description() string
    InputSchema() json.RawMessage
    Execute(ctx context.Context, input json.RawMessage) (string, error)
}
```

`MustRegister` panics on duplicate names; use `Register` and check the error if you build the registry dynamically.

## Approval policies

`internal/agent/approver.go`. Three built-in policies:

- `AllowAllApprover` — every call runs.
- `DenyAllApprover{Reason: "…"}` — every call is blocked with the given reason.
- `PatternApprover{Allow: []PatternRule, Deny: []PatternRule, Default: Decision}` — regex allow / deny per tool. Deny wins; unmatched requests use `Default` (empty → `DecisionDeny`).

Pattern rules are lazily compiled once. Compile errors surface as a `DecisionDeny` with the error string as the reason, so a malformed regex fails safe.

Custom approvers implement:

```go
type Approver interface {
    Approve(ctx context.Context, req ApprovalRequest) (Decision, string)
}
```

`ApprovalRequest` carries `ToolName`, raw `Input` JSON, and `SessionID`. Return `DecisionAllow` or `DecisionDeny` plus a reason string (surfaced back to the model as a `tool_result` error).

## Compression

`internal/agent/compressor.go`. `LLMCompressor` calls the same provider to summarise older messages once the session crosses a threshold:

```go
compressor, err := agent.NewLLMCompressor(agent.LLMCompressorConfig{
    Provider:        provider,
    TriggerMessages: 60,
    KeepRecent:      8,
})
```

The most recent `KeepRecent` messages survive verbatim; everything older collapses into a single summary block. The `Compressor` sets `CacheableMessages` on the next request so the summary is cache-hot on the very next turn.

`NoopCompressor` is the default when `Compressor` is nil.

## FTS5 cross-session recall

`internal/agent/recall.go` + `internal/state/sqlite/`. The session store's FTS5 index covers every message. `SQLiteRecall` queries against the current user message and returns the top-K most relevant snippets as a system-prompt appendix:

```go
recall := recall.NewSQLiteRecall(store, 5)
```

Enable by setting `Options.RecallProvider = recall`. Empty results are safe — the loop proceeds normally.

## Complete embed example

```go
package main

import (
    "context"
    "fmt"
    "log/slog"
    "os"

    "github.com/sebastienrousseau/rousseau-agent/internal/agent"
    "github.com/sebastienrousseau/rousseau-agent/internal/llm/claudecli"
    "github.com/sebastienrousseau/rousseau-agent/internal/tools"
    "github.com/sebastienrousseau/rousseau-agent/internal/tools/builtin"
)

func main() {
    provider := claudecli.New(claudecli.Config{
        PermissionMode: "bypassPermissions",
    })

    registry := tools.NewRegistry()
    registry.MustRegister(builtin.NewReadTool())
    registry.MustRegister(builtin.NewGrepTool(0, 0))

    ag := agent.New(provider, registry,
        slog.New(slog.NewJSONHandler(os.Stdout, nil)),
        agent.Options{
            SystemPrompt: "You are a careful, concise coding assistant.",
            Approver: &agent.PatternApprover{
                Allow: []agent.PatternRule{
                    {ToolName: "read", Match: ".*"},
                    {ToolName: "grep", Match: ".*"},
                },
                Default: agent.DecisionDeny,
            },
        })

    session := agent.NewSession("hello")
    session.Append(agent.NewUserText("What does main.go do?"))

    reply, err := ag.Turn(context.Background(), session)
    if err != nil {
        fmt.Fprintf(os.Stderr, "turn: %v\n", err)
        os.Exit(1)
    }
    fmt.Println(reply.Content[0].Text)
}
```

A runnable copy lives in `examples/embed-agent` in the source tree.

## Troubleshooting

### `agent: max iterations exceeded`

The model kept requesting tool calls without ever emitting `end_turn`. Common causes: a tool that always errors (the model keeps retrying with variations), or a `MaxIterations` value that is too low for a genuinely complex task. Default is 32 — bump to 64 for large refactors. Set `MaxIterations: 0` to use the default.

### `agent: tool not found: <name>`

The model emitted a `tool_use` block naming a tool that is not in the registry. Usually indicates a stale system prompt (the tool was removed but the model still remembers it), or a hallucinated tool. Rousseau surfaces this as an error to the caller; the model is not given a chance to adapt. If you want graceful degradation, wrap the registry lookup in your own tool dispatcher.

### Provider returned `end_turn` with an empty message

Some providers return `stop_reason=end_turn` with no content blocks — for example, when the model chose to remain silent. Rousseau returns the empty `Message`; the caller decides whether "empty" is a valid outcome for their UI. The chat transport handlers log `whatsapp.empty_reply`, `slack.empty_reply`, etc.

### Tool result is truncated

`Content.ToolResult.Output` is a plain Go string. Some tool implementations (notably `read` on a huge file) return output larger than the model can absorb. Cap the output in the tool itself — the built-in `read` tool truncates at 200 KB.

### Compression fires but the summary is nonsensical

The default compression prompt asks for a bullet-list summary. If the model's summaries are missing key facts, either raise `KeepRecent` so more messages survive verbatim, or override `CompressionConfig.Prompt` with a task-specific instruction. The instruction is the operator's lever — the compressor does not otherwise steer the model.

## Related pages

- [Concepts](/concepts/) — overview of every subsystem.
- [User Guide: Approval Policies](/user-guide/approval-policies/) — full policy semantics.
- [User Guide: Tools](/user-guide/tools/) — built-in tool schemas.
- [User Guide: Compression &amp; Recall](/user-guide/compression-recall/) — the compressor and FTS5 recall internals.
- [MCP](/mcp/) — exposing the agent's tools to external hosts.

## Further reading

- `internal/agent/agent.go` — `Turn`, `runTools`, `systemPrompt`.
- `internal/agent/approver.go` — `PatternApprover`, `AllowAllApprover`, `DenyAllApprover`.
- `internal/agent/compressor.go` — `LLMCompressor` and `NoopCompressor`.
- `internal/agent/recall.go` — `SQLiteRecall` and the FTS5 query shape.
- `internal/agent/stream_turn.go` — streaming variant that surfaces token-by-token progress.
- `internal/tools/tool.go` — the `Tool` interface.
- `examples/embed-agent/main.go` — runnable embedding example.
