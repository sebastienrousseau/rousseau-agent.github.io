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
description: "Configure the claudecli provider: PermissionMode values, model aliases, auth inheritance, and when to prefer this over the direct API."
keywords: "claudecli, claude CLI, subprocess, PermissionMode, bypassPermissions, acceptEdits, Claude Code"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/providers/claudecli/"
subtitle: "Subprocess against the local Claude Code CLI."
tags: "providers, claudecli"
title: "claudecli Provider"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "claudecli, claude CLI, subprocess, PermissionMode, bypassPermissions, acceptEdits, Claude Code"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "claudecli Provider"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 6
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/claudecli/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/claudecli/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "claudecli Provider"
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
twitter_description: "Configure the claudecli provider: PermissionMode values, model aliases, auth inheritance, and when to prefer this over the direct API."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "claudecli Provider"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">What you'll learn</span><p>How the <code>claudecli</code> provider inherits authentication from your locally-installed Claude Code, the full <code>PermissionMode</code> matrix, session correlation semantics, model aliases, and when to prefer this over the direct Anthropic API. Read <code>internal/llm/claudecli/client.go</code> alongside this page for the ground truth.</p></aside>

## When to use claudecli

`claudecli` shells out to the `claude` CLI (Claude Code) as a subprocess. It is the **default provider** and the right choice when:

- You already have Claude Code installed and authenticated locally.
- You want to reuse a subscription-tier Claude Code account rather than plumb API keys.
- You want the model to run inside `claude`'s own tool-use loop (its file-editing, thinking, and plan mode features are intact).
- You want zero secret material in rousseau's config file.

The trade-off: rousseau's tool `Registry` is **not** invoked for this provider — `claude` runs its own tools inside the subprocess. Response objects come back as a single end-of-turn text message. If you need rousseau to gate `bash`/`edit`/`write` through the approval policy, use `anthropic`, `bedrock`, `vertex`, or an OpenAI-compatible provider instead.

## Auth inheritance

The `claude` CLI holds authentication in three places:

| Location | Contents |
|---|---|
| `~/.claude/` | OAuth tokens (subscription), API-key helper output, workspace config. |
| System keychain | On macOS, `claude` may cache refresh tokens in the login keychain. |
| `ANTHROPIC_API_KEY` env | If set, `claude` uses it for API-key mode instead of OAuth. |

`claudecli` never reads these directly. Every invocation is `exec.CommandContext(binary, args...)` — the subprocess inherits the parent's environment and home directory, and looks up its own credentials. That is what makes it "zero-config" for individual operators.

<aside class="admonition" data-type="tip"><span class="admonition-title">Container binds</span><p>When running rousseau in a container, bind-mount <code>~/.claude</code> read-write into the container so <code>claude</code> can refresh cached OAuth tokens in place:</p></aside>

```ini
Volume=%h/.claude:/home/rousseau/.claude:rw,Z
```

The `Z` label is critical on SELinux hosts; see [Deployment](/deployment/) for the full Quadlet unit.

## Configuration

```yaml
provider: claudecli

claudecli:
  binary: claude
  model: sonnet
  permission_mode: bypassPermissions
  extra_args:
    - --add-dir
    - /workspace
```

| Field | Default | Effect |
|---|---|---|
| `binary` | `claude` | Executable resolved on `$PATH`. Point at an absolute path if you have multiple `claude` versions. |
| `model` | *empty* | Passed as `--model <value>`. Empty uses `claude`'s default. |
| `permission_mode` | *empty* | Passed as `--permission-mode <value>`. See table below. |
| `extra_args` | `[]` | Prepended before `-p <prompt>` on every invocation. |

Every field maps to `ClaudeCLIConfig` in `internal/config/config.go`. The subprocess command line assembled at each turn is:

```sh
claude --print --output-format json \
  --session-id <sessionID> \
  --system-prompt <systemPrompt> \
  --model <model> \
  --permission-mode <permissionMode> \
  <extra_args...> \
  <prompt>
```

<aside class="admonition" data-type="warning"><span class="admonition-title">STDOUT parsing</span><p>Rousseau expects <code>claude</code> to emit a JSON envelope on stdout. If you wrap <code>claude</code> in a shell script (for auditing, redaction, or ratelimiting) the wrapper must forward stdout unmodified. The parser tolerates a leading log line before the first <code>{</code> — see <code>parseResult</code> in <code>internal/llm/claudecli/client.go</code> — but garbage after the JSON envelope will fail.</p></aside>

## PermissionMode matrix

The `PermissionMode` flag mirrors `claude`'s own `--permission-mode`. The subprocess enforces the value; rousseau does not double-check.

<div class="tabs" data-tabs="claudecli-permission-modes">
  <div class="tab-list" role="tablist" aria-label="PermissionMode selector">
    <button role="tab" aria-selected="true">Attended</button>
    <button role="tab" aria-selected="false">Unattended</button>
    <button role="tab" aria-selected="false">Read-only</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Interactive TUI sessions where a human sits at the terminal and can approve tool calls.

| Mode | Behaviour |
|---|---|
| `default` | Claude Code prompts interactively for every tool call. Best for exploratory sessions. |
| `acceptEdits` | File edits proceed without prompting; other tools still prompt. Good when you trust the edit surface. |
| `auto` | Automatic based on the tool. Use when you want claude's built-in heuristic to decide. |

```yaml
claudecli:
  permission_mode: acceptEdits
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Chat transports (WhatsApp, Slack, Discord, Signal, …) have no human at the terminal to answer prompts.

| Mode | Behaviour |
|---|---|
| `bypassPermissions` | Every tool call runs without prompting. Accepts full blast radius. |
| `dontAsk` | Alias treated similarly to bypass. |

```yaml
claudecli:
  permission_mode: bypassPermissions
```

The CLI sets `bypassPermissions` automatically for unattended daemons if the operator did not specify one — see `setUnattendedPermissionDefault` in `internal/cli`.

<aside class="admonition" data-type="caution"><span class="admonition-title">Blast radius</span><p><code>bypassPermissions</code> gives the model direct <code>bash</code> access with the daemon's privileges. Combine it with (a) a hardened container, (b) an allowlist, and (c) a pattern-mode approver on rousseau's side — or use a non-<code>claudecli</code> provider that lets rousseau enforce approvals before the tool runs.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Exploration mode for large refactors or code reviews where you do not want any writes.

| Mode | Behaviour |
|---|---|
| `plan` | Planner mode. Reads and grep are allowed; writes are inhibited. |

```yaml
claudecli:
  permission_mode: plan
```

Pair with rousseau's own read-only mode (see [Guides: Read-only mode](/guides/read-only-mode/)) for belt-and-braces enforcement.

  </div>
</div>

## Session correlation

`claudecli` maintains conversation state inside the subprocess. Rousseau correlates its own session IDs with `claude`'s via two flags:

- `claude -p --session-id <uuid>` creates a new session. If the UUID already exists, `claude` errors with `already in use`.
- `claude -p --resume <uuid>` resumes an existing session. If unknown, `claude` errors.

Rousseau picks the flag using an in-memory `SessionCache` (`InMemorySessionCache` by default). On a cold-start cache miss where `claude` already has state from a previous rousseau run, the provider optimistically tries `--session-id`, catches the `already in use` error, and retries with `--resume`. See the comment on `(*Provider).Complete` in `internal/llm/claudecli/client.go`.

Callers embedding the provider can swap in a persistent cache via `provider.WithCache(store)` — the `state.sqlite` store implements the same interface and survives daemon restarts, avoiding the cold-start roundtrip on the first turn after a reboot.

## Model aliases

`claude`'s model aliases are honoured by the subprocess unchanged:

| Alias | Points at |
|---|---|
| `sonnet` | The current default Sonnet-tier model. |
| `opus` | The current default Opus-tier model. |
| `haiku` | The current default Haiku-tier model. |

For reproducibility across daemon restarts (skill benchmarks, cron jobs, batch runs), pin an exact model ID:

```yaml
claudecli:
  model: claude-sonnet-4-6
```

<aside class="admonition" data-type="note"><span class="admonition-title">Aliases follow releases</span><p>Aliases move when Anthropic ships a new model. The <code>sonnet</code> alias in July 2026 does not point at the same weights the <code>sonnet</code> alias pointed at in April 2026. If your workflow depends on a specific behaviour, pin the exact ID.</p></aside>

## Combining with skills

`claudecli` sends the system prompt via `--system-prompt` on session creation. `claude` honours it verbatim and ignores subsequent `--system-prompt` values on `--resume` — which matches how rousseau uses it. The `SkillsProvider` output is spliced in before the invocation:

```
<agent.SystemPrompt>

<skill 1 markdown>

<skill 2 markdown>

<RecallProvider appendix>
```

See `internal/agent/agent.go` `systemPrompt()`. Skills work identically across every provider; the mechanics of the composition happen in `agent.Agent`, not the provider.

<aside class="admonition" data-type="tip"><span class="admonition-title">Prompt caching</span><p>The Anthropic direct provider marks the system prompt for the ephemeral prompt cache (see <code>internal/llm/anthropic/cache.go</code>). <code>claudecli</code> does not — <code>claude</code> owns its own cache internally. If you want measurable prompt-cache savings, use <code>provider: anthropic</code>.</p></aside>

## Gotchas

- **No cross-provider portability.** A session created against `claudecli` is not portable to `anthropic` — model-side state lives inside `claude`. Switching providers midway forces a new session.
- **Tool registry is not invoked.** `bash`, `edit`, `write`, `grep`, `read` are executed by `claude`, not by `rousseau`. Rousseau's `agent.Approver` cannot gate those calls. Use a non-`claudecli` provider if you need rousseau-side approval enforcement.
- **`--add-dir` scoping.** By default `claude` refuses to read outside its own workspace. Pass `--add-dir /workspace` (or wherever your source lives) via `extra_args` to widen it. Combine with rousseau's approval policy at the transport level if you want to compensate for the loss of control.
- **Streaming.** `claudecli` uses `claude -p --output-format json` (non-streaming). The streaming path in `internal/llm/claudecli/stream.go` reads `--output-format stream-json`; opt in by using `StreamingProvider` from an embedding integration.
- **Environment leakage.** The subprocess inherits every environment variable of the parent. If `ANTHROPIC_API_KEY` is set in rousseau's environment, `claude` will prefer it over cached OAuth. That is usually fine, but it changes billing.

## Troubleshooting

### `claudecli: run: exec: "claude": executable file not found in $PATH`

`claude` is not on `PATH` (or the container image does not ship it). Two fixes:

1. Set `claudecli.binary` to an absolute path.
2. Add Claude Code to the container's runtime layer — the reference `docker/Dockerfile` uses `node:22-alpine` for this reason.

### `claudecli: model error: session id already in use`

You are running two rousseau processes against the same session ID against the same `claude` install, or the in-memory cache dropped a session that `claude` still remembers. The optimistic retry described above handles the second case; the first means you have concurrent daemons stepping on each other.

### `claudecli: no JSON in output`

`claude` printed non-JSON to stdout, or exited before emitting the envelope. Common causes: an invalid API key on the Claude Code side, a `claude` version that predates `--output-format json`, or a shell wrapper writing progress markers. Run `claude -p --output-format json 'hello'` directly to isolate.

### The reply cuts off mid-sentence

`claude`'s output is capped by `--max-turns` and its own internal token budget. Rousseau does not set `--max-turns`; if you set it via `extra_args`, raise it. For long generations, consider a direct API provider where you control `MaxTokens` from `internal/llm/anthropic/client.go`.

### Subscription plan is rate-limited but the API is fine

The `claude` CLI on a subscription plan has hidden per-conversation and per-window limits. If you hit them, switch to `provider: anthropic` with an API key — the direct API has explicit, published limits (see [Guides: Rate limits](/guides/rate-limits/)).

## Related pages

- [Providers: Anthropic](/providers/anthropic/) — direct API with prompt caching and streaming.
- [Providers: Bedrock](/providers/bedrock/) — AWS-managed Claude.
- [User Guide: Approval Policies](/user-guide/approval-policies/) — how to gate tool calls at the rousseau layer.
- [Skills](/skills/) — how the system-prompt appendix is composed.
- [Configuration](/configuration/) — the `claudecli` stanza in context.

## Further reading

- `internal/llm/claudecli/client.go` — subprocess invocation, session correlation, JSON parsing.
- `internal/llm/claudecli/stream.go` — streaming variant using `--output-format stream-json`.
- `internal/config/config.go` — `ClaudeCLIConfig` struct.
- `internal/cli/root.go` — how `setUnattendedPermissionDefault` picks `bypassPermissions` for chat transports.
