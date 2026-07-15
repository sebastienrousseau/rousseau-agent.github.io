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
hreflang: "fr"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "fr"
locale: "fr_FR"
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
description: "Layered architecture of rousseau-agent: agent core, provider / tool / transport interfaces, module boundaries, cyclic-dependency prevention."
keywords: "architecture, layers, agent, provider, transport, tools, module, cyclic dependency"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/developer-guide/architecture/"
subtitle: "Layered architecture and module boundaries."
tags: "developer-guide, architecture, layers"
title: "Architecture"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "architecture, layers, agent, provider, transport, tools, module, cyclic dependency"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Architecture"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 61
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/architecture/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/architecture/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Architecture"
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
twitter_description: "Layered architecture of rousseau-agent: agent core, provider / tool / transport interfaces, module boundaries, cyclic-dependency prevention."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Architecture"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Merci à chaque opérateur qui exploite son propre agent de codage."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Layered picture

```
+--------------------------------------------------------------------+
|                                CLI                                |
|  chat  whatsapp  slack  discord  ...  mcp  cron  skills  doctor   |
+--------------------------------+-----------------------------------+
                                 |
+--------------------------------v-----------------------------------+
|                              Router                               |
|                  (per-JID session, allowlist, dispatch)           |
+---------------+---------------+-------------------+---------------+
                |                                   |
       transport.Transport                    agent.Agent
       Start / Stop / Deliver                Turn / TurnStream
                |                                   |
     +----------+----------+              +---------+-----------+
     |  9 concrete adapters |              |    agent.Provider  |
     +---------------------+              |    5 concrete impls |
                                          +---------+-----------+
                                                    |
                                          +---------v-----------+
                                          |   tools.Registry   |
                                          |   tools.Tool iface |
                                          +---------+-----------+
                                                    |
                                          +---------v-----------+
                                          |     state.Store    |
                                          | SQLite: sessions, |
                                          | jidmap, FTS5, cron|
                                          +---------------------+
```

## Package roles

| Package | Role | Depends on |
|---|---|---|
| `internal/agent` | Session, Message, Turn, agent loop, Provider / Tool / Approver / Compressor / SkillsProvider / RecallProvider interfaces. | stdlib + `internal/tools` (interface only). |
| `internal/tools` | Tool interface + concurrency-safe Registry. | stdlib. |
| `internal/tools/builtin` | `read`, `write`, `edit`, `grep`, `bash`. | `internal/tools`. |
| `internal/llm/{anthropic,bedrock,claudecli,openai,vertex}` | Concrete `agent.Provider` implementations. | `internal/agent`. |
| `internal/state` | Store interface + Summary type. | stdlib. |
| `internal/state/sqlite` | SQLite implementation, WAL, FTS5, cron table, JID map. | `internal/state`, `modernc.org/sqlite`. |
| `internal/transport` | Transport interface + Router. | `internal/agent`, `internal/state`. |
| `internal/transport/{whatsapp,signal,...}` | Nine concrete adapters. | `internal/transport`, `internal/agent`. |
| `internal/mcp` | JSON-RPC 2.0 server over stdio, MCP spec 2024-11-05. | `internal/agent`, `internal/tools`, `internal/state`. |
| `internal/skills` | agentskills.io loader + composition. | stdlib. |
| `internal/cron` | robfig/cron/v3 scheduler goroutine. | `internal/state`, `internal/agent`. |
| `internal/config` | Viper-based config loader. | stdlib + `viper`. |
| `internal/cli` | Cobra command tree, wire-up. | Everything above. |
| `internal/tui` | Bubble Tea model. | `internal/agent`, `internal/state`, `bubbletea`. |
| `cmd/rousseau` | Signal handling + `Execute`. | `internal/cli`. |

## Load-bearing invariant

**The `agent` package depends only on interfaces exposed by `tools`, on its own `Provider` types, and on the standard library.**

Everything that can vary — the provider, the store, the transport, the approver, the compressor — is expressed as an interface owned by `agent`. Concrete implementations import `agent`; `agent` never imports them back. This makes the loop testable without any live provider, live network, or live transport.

If you find yourself adding an import from `agent` into `llm/*`, `transport/*`, or `state/sqlite`, stop. The wiring belongs in `cli`, not in `agent`.

## Cyclic-dependency prevention

The Go compiler catches package import cycles at build time. The layered posture makes cycles almost impossible: each layer only knows about layers below it. Concretely:

- `cli` is allowed to import everything.
- `transport/*`, `llm/*`, `state/*` are allowed to import `agent`, `tools`, and (for transports and state) their sibling interface packages.
- `agent` is only allowed to import `tools` (interfaces) and the standard library.
- `tools` imports only the standard library.

Two structural rules prevent regressions:

1. Interfaces live in the **consumer** package. `Provider` is defined in `agent`, not in `llm/anthropic`. `Tool` is defined in `tools`, not in `tools/builtin`.
2. Test doubles live alongside their consumer. `agent_test.go` defines fake providers; `transport/whatsapp/client_test.go` defines fake WebSocket connections.

## Provider interface

```go
// Provider drives a single request/response round-trip.
type Provider interface {
    Complete(ctx context.Context, req Request) (Response, error)
}

// StreamingProvider streams response deltas.
type StreamingProvider interface {
    Provider
    CompleteStream(ctx context.Context, req Request) (StreamReader, error)
}
```

Every LLM adapter satisfies at least `Provider`. Streaming is opt-in.

## Tool interface

```go
// Tool is a callable capability the model can request.
type Tool interface {
    Name() string
    Description() string
    InputSchema() map[string]any
    Execute(ctx context.Context, input json.RawMessage) (string, error)
}
```

`InputSchema()` returns JSON-Schema-shaped map; the shape must validate against the model's tool-use expectations.

## Transport interface

```go
type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

`Start` is expected to block until `ctx` is cancelled or `Stop` is called. Delivery back to the sender is handled by the transport internally; adapters typically expose a `Deliver(ctx, target, body)` method used by the cron scheduler.

## Approver interface

```go
type Approver interface {
    Approve(ctx context.Context, req ApprovalRequest) (Decision, string)
}
```

Called on the hot path before every tool call. See [Approval Policies](/fr/user-guide/approval-policies/).

## Compressor and Recall

Two more interfaces the agent loop consults each turn:

```go
type Compressor interface {
    Compress(ctx context.Context, s *Session) (changed bool, err error)
}

type RecallProvider interface {
    SystemAppendix(ctx context.Context, s *Session) string
}
```

See [Compression + Recall](/fr/user-guide/compression-recall/).

## Wire-up in `cli`

`internal/cli/chat.go` is the canonical wire-up example. It:

1. Loads config.
2. Builds a provider (`buildProvider(cfg)`).
3. Opens the SQLite store (`openStore`).
4. Creates a tool registry and registers the built-in tools.
5. Builds an approver from `cfg.Agent.Approver`.
6. Builds a compressor from `cfg.Agent.Compression`.
7. Constructs `agent.New(...)`.
8. Hands the agent to the Bubble Tea model.

Every other command follows the same pattern — the daemon-specific parts are just the transport constructor and its `Start` invocation.

## Testing pattern

Every layer's interfaces make it possible to test in isolation:

- `agent_test.go` uses a fake `Provider` that returns canned `Response` values.
- `transport/whatsapp/client_test.go` uses a fake `WSConn` and a fake `Sender`.
- `state/sqlite/*_test.go` uses an in-memory SQLite (`file::memory:`).
- `tools/builtin/*_test.go` uses `testing/fstest.MapFS` (where relevant) and temp files.

See [Testing](/fr/developer-guide/testing/) for the injection pattern.

## Package dependency graph

```
cmd/rousseau/               (entry point)
    │
    ▼
internal/cli/               (Cobra command tree)
    │
    ├───▶ internal/config/  (Viper-driven config)
    ├───▶ internal/agent/   (Turn loop, session, provider iface, approver, compressor)
    │        │
    │        └───▶ internal/tools/           (Tool iface + Registry)
    │                    │
    │                    └───▶ internal/tools/builtin/   (read, write, edit, grep, bash)
    │
    ├───▶ internal/llm/anthropic/  ─────┐
    ├───▶ internal/llm/bedrock/    ─────┤
    ├───▶ internal/llm/claudecli/  ─────┼─▶ implements agent.Provider
    ├───▶ internal/llm/openai/     ─────┤
    ├───▶ internal/llm/vertex/     ─────┘
    │
    ├───▶ internal/transport/           (Transport iface + Router)
    │        │
    │        ├───▶ whatsapp/    (whatsmeow)
    │        ├───▶ slack/       (Socket Mode)
    │        ├───▶ discord/     (Gateway v10)
    │        ├───▶ telegram/    (Bot API)
    │        ├───▶ matrix/      (Client-Server)
    │        ├───▶ signal/      (signal-cli JSON-RPC)
    │        ├───▶ email/       (IMAP + SMTP)
    │        ├───▶ sms/         (Twilio / Vonage REST)
    │        └───▶ imessage/    (BlueBubbles)
    │
    ├───▶ internal/cron/        (scheduled prompts)
    ├───▶ internal/mcp/         (JSON-RPC 2.0 server)
    ├───▶ internal/skills/      (agentskills.io loader)
    ├───▶ internal/state/       (Store iface)
    │        │
    │        └───▶ internal/state/sqlite/   (WAL, FTS5)
    │
    └───▶ internal/tui/         (Bubble Tea model)
```

Load-bearing property: `internal/agent` depends only on the standard library, `internal/tools` (through its narrow interface), and its own subpackages. Every provider, every store, and every transport depends on `agent` — never the reverse.

## ADR-style rationale

Selected boundary decisions and why they exist:

### ADR-1: Provider is an interface, not a plugin

We considered a plugin model (`plugin.Open` or `hashicorp/go-plugin`). Rejected because:

- Static builds are easier to sign, reproduce, and distribute.
- Plugin ABIs are fragile across Go versions.
- Every provider we care about is small enough to vendor.

Trade-off: adding a provider requires a rebuild. Acceptable.

### ADR-2: Tools live in `internal/tools/builtin`, not a `pkg/tools`

We considered exporting the tool registry publicly. Rejected because:

- `internal/` discourages accidental coupling.
- Callers embedding the agent can still register their own tools via the exported `Registry` interface — they just do it through the `tools` package rather than importing a builtin.

Trade-off: users cannot import `rousseau/tools/builtin` directly. They import `rousseau/agent` and `rousseau/tools` and build their own registry, which is what `examples/embed-agent` demonstrates.

### ADR-3: SQLite via `modernc.org/sqlite`, not `mattn/go-sqlite3`

`modernc.org/sqlite` is a pure-Go port; `mattn/go-sqlite3` uses cgo. Chosen because:

- `CGO_ENABLED=0` keeps the binary static.
- Static binaries are easier to sign, reproduce, and distribute.
- The reproducible-build CI job would be much harder with cgo.

Trade-off: `modernc.org/sqlite` is slower for write-heavy workloads. Acceptable — rousseau is not a write-heavy database.

### ADR-4: MCP server is minimal, not the official SDK

The `internal/mcp/` package is ~200 lines of hand-rolled JSON-RPC. Chosen because:

- The MCP surface rousseau needs is small (initialize, tools/list, tools/call, ping, shutdown).
- The official Go SDK was not yet stable when the code was written.
- Keeping the surface small makes the swap-in painless when the SDK stabilises.

Trade-off: some MCP features (resources, prompts, list-changed notifications) are stubs. Roadmap.

### ADR-5: `claudecli` provider does not use rousseau's tool registry

`claude`'s subprocess runs its own tool-use loop. Rousseau's approver, therefore, cannot see the tool calls. This is a deliberate acceptance:

- The `claudecli` provider exists to let subscribers use their Claude Code auth without an API key.
- If rousseau intercepted the tool loop, we would have to pipe every input and output through the subprocess boundary — slow and error-prone.
- Users who want rousseau-side approval use a non-`claudecli` provider.

Trade-off: `claudecli` users must trust `claude`'s permission model. Documented in [Providers: claudecli](/fr/providers/claudecli/).

## Next

- [Add a transport](/fr/developer-guide/add-a-transport/) — how a new interface implementer looks.
- [Add a provider](/fr/developer-guide/add-a-provider/) — same pattern, different interface.
- [Add a tool](/fr/developer-guide/add-a-tool/) — the smallest extension point.

## Related pages

- [Concepts](/fr/concepts/) — high-level tour.
- [Agent loop](/fr/agent-loop/) — the runtime shape.
- [MCP](/fr/mcp/) — external tool exposure.
- [Configuration](/fr/configuration/) — the config surface each interface reads from.

## Further reading

- `README.md` — repository-level positioning and capability matrix.
- `internal/agent/agent.go` — the core loop.
- `internal/agent/provider.go` — the `Provider` and `StreamingProvider` interfaces.
- `internal/transport/transport.go` — the `Transport` interface.
- `internal/tools/registry.go` — the `Tool` interface and `Registry`.
