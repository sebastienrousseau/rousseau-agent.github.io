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
description: "Architecture overview of rousseau-agent: agent loop, transport interface, tool registry, approval policies, SQLite session store, MCP server, cron scheduler, skills loader."
keywords: "architecture, agent loop, session, transport, tool registry, approval, MCP, cron, skills, compression, FTS5"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/concepts/"
subtitle: "How the agent loop, transports, and session store fit together."
tags: "architecture, agent, session, mcp"
title: "Concepts"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "architecture, agent loop, session, transport, tool registry, approval, MCP, cron, skills, compression, FTS5"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Concepts"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "concepts"
order: 3
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/concepts/index.html"
item_link: "https://docs.rousseau-agent.dev/concepts/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Concepts"
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
twitter_description: "Architecture overview of rousseau-agent: agent loop, transport interface, tool registry, approval policies, SQLite session store, MCP server, cron scheduler, skills loader."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Concepts"
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

<figure class="arch-diagram" role="figure" aria-label="rousseau-agent turn dispatch across transport, agent, provider, tools">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 300" role="img" style="max-width:100%;height:auto;background:var(--bg-elev);border:1px solid var(--border);border-radius:12px;padding:18px 0">
  <title>Turn dispatch flow</title>
  <desc>A message enters at the transport, is routed to the Agent, which calls the Provider, potentially issues tool calls, and returns a reply.</desc>
  <style>
    .box{fill:#7aa4ff;stroke:#1a3a8a;stroke-width:2;rx:8}
    .txt{font-family:'Inter',system-ui,sans-serif;font-size:14px;fill:#fff;text-anchor:middle;font-weight:600}
    .txt-sub{font-family:'Inter',system-ui,sans-serif;font-size:10px;fill:#e5e7eb;text-anchor:middle}
    .arrow{stroke:#4b5563;stroke-width:2;fill:none;marker-end:url(#arw)}
    .dot{fill:#41d1ff;r:5}
    @keyframes fly{
      0%,10%{cx:60;opacity:0}
      15%{opacity:1}
      30%{cx:200;cy:60}
      50%{cx:360;cy:150}
      65%{cx:520;cy:150}
      75%{cx:520;cy:220}
      85%{cx:360;cy:220}
      95%{cx:200;cy:220}
      100%{cx:60;opacity:0}
    }
    @media (prefers-reduced-motion:reduce){.dot{animation:none;opacity:.6}}
    .dot-animated{animation:fly 6s ease-in-out infinite}
  </style>
  <defs>
    <marker id="arw" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M0,0 L10,5 L0,10 Z" fill="#4b5563"/>
    </marker>
  </defs>

  <!-- Boxes -->
  <rect class="box" x="20" y="35" width="120" height="50"/>
  <text class="txt" x="80" y="60">Transport</text>
  <text class="txt-sub" x="80" y="76">slack · whatsapp · …</text>

  <rect class="box" x="160" y="35" width="120" height="50" style="fill:#41d1ff"/>
  <text class="txt" x="220" y="60" style="fill:#0f1424">Router</text>
  <text class="txt-sub" x="220" y="76" style="fill:#1a3a8a">allowlist · session</text>

  <rect class="box" x="300" y="125" width="120" height="50"/>
  <text class="txt" x="360" y="150">Agent loop</text>
  <text class="txt-sub" x="360" y="166">Session · Turn</text>

  <rect class="box" x="460" y="125" width="120" height="50" style="fill:#a4c1ff"/>
  <text class="txt" x="520" y="150" style="fill:#122a63">Provider</text>
  <text class="txt-sub" x="520" y="166" style="fill:#122a63">claudecli · anthropic</text>

  <rect class="box" x="460" y="195" width="120" height="50" style="fill:#f0abfc"/>
  <text class="txt" x="520" y="220" style="fill:#4a044e">Tool call</text>
  <text class="txt-sub" x="520" y="236" style="fill:#4a044e">read · edit · bash</text>

  <rect class="box" x="300" y="195" width="120" height="50" style="fill:#a5d6ff"/>
  <text class="txt" x="360" y="220" style="fill:#0b5e93">Session store</text>
  <text class="txt-sub" x="360" y="236" style="fill:#0b5e93">SQLite + FTS5</text>

  <rect class="box" x="140" y="195" width="120" height="50" style="fill:#7ce38b"/>
  <text class="txt" x="200" y="220" style="fill:#065f46">Reply</text>
  <text class="txt-sub" x="200" y="236" style="fill:#065f46">to transport</text>

  <!-- Arrows -->
  <path class="arrow" d="M140 60 L160 60"/>
  <path class="arrow" d="M220 90 Q220 120 300 150"/>
  <path class="arrow" d="M420 150 L460 150"/>
  <path class="arrow" d="M520 175 L520 195"/>
  <path class="arrow" d="M460 220 L420 220"/>
  <path class="arrow" d="M300 220 L260 220"/>
  <path class="arrow" d="M140 210 Q80 180 80 90"/>

  <!-- Animated packet -->
  <circle class="dot dot-animated" cx="60" cy="60" r="5"/>
</svg>
<figcaption style="text-align:center;color:var(--fg-muted);font-size:13.5px;margin-top:8px">A user message travels through the transport, agent loop, provider, tool, and back — animated at 6 s / cycle.</figcaption>
</figure>


## Layered architecture

```
+---------------------------------------------------------------+
|                             CLI                              |
|  chat  whatsapp  slack  discord  ...  mcp  cron  skills      |
+-------------------------+-------------------------------------+
                          |
+-------------------------v-------------------------------------+
|                          Router                              |
|          (per-JID session, allowlist, dispatch)              |
+-------------+---------------------------+---------------------+
              |                           |
     Transport interface           agent.Agent
     Start / Stop / Deliver        Turn / TurnStream
              |                           |
   +----------+----------+       +--------+--------+
   | 9 concrete adapters |       | Provider iface  |
   +---------------------+       | 5 concrete impls|
                                 +--------+--------+
                                          |
                                 +--------v--------+
                                 | Tools Registry  |
                                 | read/write/edit |
                                 | grep/bash + ext |
                                 +--------+--------+
                                          |
                                 +--------v--------+
                                 |  State (SQLite) |
                                 | sessions, cron, |
                                 | jidmap, FTS5    |
                                 +-----------------+
```

The `agent` package depends only on interfaces exposed by `tools`, on its own `Provider` types, and on the standard library. Concrete providers, stores, and transports depend on `agent` — never the reverse.

## The agent loop

`Session → Turn → Provider → tool-use round trip`. Every user message becomes a call to `Agent.Turn`:

1. **Compression check.** The configured `Compressor` gets a chance to rewrite the session before the turn runs. When it does, `Request.CacheableMessages` is set so the summary block is cached on the very next turn.
2. **Skills appendix.** If a `SkillsProvider` is configured, it inspects the last user message and returns text to splice into the system prompt.
3. **Recall appendix.** If a `RecallProvider` is configured, it queries the FTS5 index across prior sessions and returns text to splice.
4. **Provider call.** The `Provider.Complete` implementation returns a `Response` with a `StopReason`.
5. **Tool-use dispatch.** If `StopReason == StopToolUse`, each requested tool call is sent to the `Approver`. Denials become `tool_result` errors so the model can adapt. Allowed calls are executed against the `Registry` and their outputs replayed on the next iteration.
6. **End of turn.** Loop until `StopReason == StopEndTurn` or `MaxIterations` is reached (default 32).

`internal/agent/agent.go` is the canonical reference.

## Transports

Every transport implements `transport.Transport`:

```go
type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

`Handler.Handle` receives an `IncomingMessage` (`From`, `Body`, `At`) and returns the reply text. The `Router` sits above the transport and is responsible for per-sender session isolation, allowlist enforcement, and dispatching to the `Agent`.

None of the shipped transports expose a public HTTP surface by default. Slack uses Socket Mode (outbound WebSocket). Discord uses the Gateway (outbound WebSocket). Signal is a subprocess. WhatsApp is Meta's Web protocol over TCP. Matrix, Telegram, iMessage, and email use polling. SMS is send-only because the inbound side would require a webhook.

## Tool registry

`internal/tools` defines the `Tool` interface and a concurrency-safe `Registry`. Built-in tools live in `internal/tools/builtin/`:

- `read` — file read.
- `write` — file write.
- `edit` — string replace with unique-match enforcement to prevent accidental mass-replacement.
- `grep` — text search.
- `bash` — command execution. **The load-bearing security boundary.**

Every tool declares a strict JSON schema. Adding a tool is a single `registry.MustRegister(myTool)` call at wire-up; the agent core does not change.

## Approval policies

Every tool call goes through `Approver.Approve` before execution. Three built-in policies live in `internal/agent/approver.go`:

| Mode | Behaviour |
|---|---|
| `allow_all` | Every call runs. Sensible with the `claudecli` provider, which handles its own approvals. |
| `deny_all` | Every call is blocked. Useful for smoke tests and read-only sessions. |
| `pattern` | Regex allow / deny rules per tool. Deny wins over allow. Unmatched requests fall back to `Default` (`allow` or `deny`). |

Deny reasons are surfaced back to the model as `tool_result` errors, so the model gets a chance to adapt instead of failing silently.

## Session store

`internal/state/sqlite/` implements the `state.Store` interface on `modernc.org/sqlite` — pure Go, no libc, no CGo. Features:

- **WAL journaling** with `busy_timeout=15s`.
- **WAL checkpoint on Close** so the primary database file stays consistent for backups.
- **FTS5 recall** table indexes every message; the `RecallProvider` performs cross-session lookups.
- **JID map** table normalises WhatsApp LID identities to phone JIDs.
- **Cron table** persists scheduled jobs across restarts.

## MCP server

`internal/mcp/server.go` is a JSON-RPC 2.0 server over stdio, spec revision **2024-11-05**. `rousseau mcp` starts it. Register tools with `server.Register(mcp.ToolSpec{...})` and let a client (Claude Desktop, an IDE extension, another agent) drive them.

Tool failures are surfaced through the `content` channel with `isError=true`, not the JSON-RPC error channel — this is what MCP hosts expect.

## Cron scheduler

`internal/cron/scheduler.go` wraps `robfig/cron/v3`. Jobs are stored in SQLite so they survive restarts. Each fire calls `Runner.RunOnce(ctx, prompt)` (a one-shot agent turn against a fresh session), then hands the reply to `Delivery` — a transport-agnostic function that ships the message.

New jobs added via `rousseau cron add` become live within the next `PollInterval` (default 60s).

## Skills loader

`internal/skills/skills.go` scans `skills_dir` for `*.md` files. Each file may carry YAML front-matter declaring `name`, `description`, and `triggers`. When any trigger appears in the current user message, the skill body is spliced into the system prompt for that turn. Format is deliberately close to the [agentskills.io](https://agentskills.io) convention.

## Compression

`internal/agent/compressor.go` runs LLM-backed summarisation once the session crosses `TriggerMessages` (default 60). The most recent `KeepRecent` messages (default 8) survive verbatim; everything older collapses into a single summary block. Disabled by default because a subscription-tier `claudecli` account rarely needs it; turn it on when running against pay-per-token providers.

## Where to go next

- [Configuration reference](/configuration/) — every field.
- [Agent-loop reference](/agent-loop/) — library-embedding contract.
- [MCP](/mcp/) — client wire-up.
