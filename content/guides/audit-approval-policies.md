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
description: "Worked example: lock down the bash tool with a pattern-mode approver, deny rules on destructive commands, and slog-driven audit trail."
keywords: "approval policy, pattern mode, bash tool, deny rules, audit trail, slog"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/guides/audit-approval-policies/"
subtitle: "Pattern-mode approver with deny rules on the bash tool."
tags: "guides, audit, approval, pattern-mode, bash, deny"
title: "Guide: Audit + Approval Policies"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approval policy, pattern mode, bash tool, deny rules, audit trail, slog"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide: Audit + Approval Policies"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 34
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/audit-approval-policies/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/audit-approval-policies/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guide: Audit + Approval Policies"
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
twitter_description: "Worked example: lock down the bash tool with a pattern-mode approver, deny rules on destructive commands, and slog-driven audit trail."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide: Audit + Approval Policies"
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

## The problem

An unattended chat-transport daemon has no human at the terminal to approve tool calls in real time. If the model wants to run `rm -rf /workspace/*`, something has to stop it. Rousseau's `pattern`-mode approver is that lever.

The threat is not the model going rogue — it is a compromised or misaligned instruction reaching the daemon over the transport channel. A pattern-mode policy with a `default: deny` fallback makes the risk bounded and auditable.

## Approver modes

Three built-in modes ship (see `internal/agent/approver.go`):

| Mode | Behaviour | When to use |
|---|---|---|
| `allow_all` | Every tool call runs. | Interactive `rousseau chat` where the `claudecli` provider is doing its own approvals. |
| `deny_all` | Every tool call is blocked. Denial reasons are surfaced to the model as `tool_result` errors so it can adapt. | Read-only inspection posture; smoke tests. |
| `pattern` | Regex allow / deny rules per tool. **Deny wins over allow.** Unmatched requests fall back to `default`. | Any unattended daemon in production. |

## Worked config

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by pattern policy — ask the operator"
    allow:
      # Read-side tools: no restriction inside the workspace.
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

      # Edit inside /workspace only.
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}

      # Write inside /workspace only.
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}

      # Shell commands: whitelist of safe read-side utilities plus git status/diff.
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|grep|rg|find|wc|stat|file|which|pwd|env|git status|git diff|git log|go test|go vet|go build)\\b"}

    deny:
      # Absolute deny rules override any allow above.
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s|ncat"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}   # fork bomb
      - {tool: write, match: "\"path\":\"/etc/|/root/|/var/"}
      - {tool: edit, match: "\"path\":\"/etc/|/root/|/var/"}
```

Two important properties fall out of `PatternApprover.Approve`:

1. **Deny wins.** Every deny rule is checked before any allow rule. This is safer than the reverse: an operator adding a broad allow can never accidentally unlock a category they thought was denied.
2. **Unmatched → deny.** With `default: deny`, any tool call the operator forgot to enumerate is blocked. This is the safe-by-default disposition; if you want the opposite, set `default: allow`.

## Reading the audit trail

Every tool call and every denial is emitted through the slog logger:

```
INFO tool.execute name=read id=t_1
INFO tool.execute name=grep id=t_2
WARN tool.denied  name=bash reason="denied by pattern policy — ask the operator"
```

The daemon uses `slog` with configurable level and format (`log.level`, `log.format`). For production, prefer `format: json` so downstream tools (Loki, Vector, Datadog) parse cleanly. See [Guides: Observability](/guides/observability/) for the pipeline recipe.

Every denial carries a stable structured key:

- `tool.denied` — the tool call was blocked. Fields: `name` (tool identifier), `reason` (from `PatternApprover.DenyReason` or the built-in fallback).
- `tool.execute` — the tool call ran. Fields: `name`, `id` (the model-emitted call ID for correlation).
- `tool.error` — the tool ran but failed. Fields: `name`, `err`.

An `slog` filter on `tool.denied` gives you the "attempts blocked" audit view most compliance frameworks ask for.

## Testing the policy

`internal/agent/approver_test.go` in the source tree exercises the `PatternApprover` with a broad matrix. To smoke-test your own rules:

```sh
rousseau chat
> Run `rm -rf /tmp/foo` for me.
```

The model will attempt the `bash` tool call. The daemon logs `tool.denied` and returns the `reason` string to the model, which will usually pivot ("I can't run that — could you tell me what you were trying to do?").

For the reference test matrix, see `internal/agent/approver_test.go` — the same rule shapes are exercised there.

## Adding a manual override

Sometimes an operator wants to approve a single dangerous call manually. The simplest pattern:

1. Set `mode: allow_all` in `rousseau chat` (interactive TUI). The `claudecli` provider handles its own per-call approval prompts.
2. Keep `mode: pattern` in every unattended daemon.

There is no interactive per-call approval UI on the chat transports today — the safety story is entirely regex + slog.

## What the policy does not do

- **Does not sandbox the tool.** A `bash` call that survives the approver runs with the daemon's UID and its filesystem visibility. Layer a rootless container ([Deployment](/deployment/)) underneath.
- **Does not rate-limit.** Ten allowed `bash` calls per second are allowed. If you need rate limiting, wrap the tool registry.
- **Does not audit outbound network calls.** If a `bash` invocation curls something out, the approver won't see the URL — only the initial `bash` `command` string. Deny `curl` and `wget` outright at the pattern level.

## Common patterns

### Locking editing to a directory tree

```yaml
allow:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/[^\"]*\""}
  - {tool: write, match: "\"path\":\"/workspace/repo/[^\"]*\""}
deny:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/(\\.git|node_modules|vendor)/"}
```

### Read-only auditor

```yaml
mode: pattern
default: deny
allow:
  - {tool: read, match: ".*"}
  - {tool: grep, match: ".*"}
```

Combined with `provider.claudecli.permission_mode: plan`, this yields a read-only inspection posture — see [Guides: Read-only Mode](/guides/read-only-mode/).

### Git-first workflows

```yaml
allow:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"git (status|diff|log|show|branch|stash|fetch|pull --ff-only)\\b"}
deny:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"git (push|reset --hard|clean -fd|checkout --)\\b"}
```

## Five reference rulesets

<div class="tabs" data-tabs="approval-rulesets">
  <div class="tab-list" role="tablist" aria-label="Reference ruleset">
    <button role="tab" aria-selected="true">Dev laptop</button>
    <button role="tab" aria-selected="false">Staging</button>
    <button role="tab" aria-selected="false">Production</button>
    <button role="tab" aria-selected="false">Oncall bot</button>
    <button role="tab" aria-selected="false">Read-only</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**Dev laptop.** Permissive by default, deny the truly dangerous. Assumes an attended terminal.

```yaml
agent:
  approver:
    mode: pattern
    default: allow
    deny:
      - {tool: bash, match: "rm\\s+-rf\\s+/"}
      - {tool: bash, match: "sudo(?!\\s+-n)"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}
      - {tool: write, match: "\"path\":\"/etc/|/root/"}
      - {tool: edit, match: "\"path\":\"/etc/|/root/"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Staging.** Explicit allow list for the workspace, deny everything outside. Suitable for a shared staging daemon with limited blast radius.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by staging policy — ping #platform for exceptions"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: bash, match: "^\\{\"command\":\"git (status|diff|log|show|branch|fetch|pull --ff-only)\\b"}
      - {tool: bash, match: "^\\{\"command\":\"(ls|cat|grep|rg|find)\\s"}
    deny:
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s"}
      - {tool: edit, match: "\"path\":\"/workspace/(\\.git|node_modules|vendor)/"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Production.** Deny-first. Every allowed command is explicitly enumerated. Suitable for a production daemon that answers customer-facing questions.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by production policy — this daemon is read-mostly"
    allow:
      - {tool: read, match: "\"path\":\"/workspace/(runbooks|docs|src)/"}
      - {tool: grep, match: "\"path\":\"/workspace/(runbooks|docs|src)/"}
      - {tool: bash, match: "^\\{\"command\":\"(ls|cat|rg)\\s"}
    deny:
      # Layered denies just in case.
      - {tool: write, match: ".*"}
      - {tool: edit, match: ".*"}
      - {tool: bash, match: "\\b(rm|mv|cp|dd|mkfs|kill|killall)\\b"}
      - {tool: bash, match: "\\b(curl|wget|nc|ncat|ssh|scp|rsync)\\b"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Oncall bot.** Can query monitoring, tail logs, but not restart services or edit code. Suitable for a Slack-facing incident-response helper.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied — oncall bot can query, not mutate"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\{\"command\":\"(kubectl|helm|argocd) (get|describe|logs|top|status)\\b"}
      - {tool: bash, match: "^\\{\"command\":\"(curl|http|wget) -[gsL]* https?://monitoring\\."}
      - {tool: bash, match: "^\\{\"command\":\"(pg_dump|psql -c 'SELECT|redis-cli GET)\\b"}
    deny:
      - {tool: write, match: ".*"}
      - {tool: edit, match: ".*"}
      - {tool: bash, match: "\\b(kubectl (apply|delete|edit|scale)|helm (install|upgrade|uninstall))\\b"}
      - {tool: bash, match: "\\b(systemctl (start|stop|restart|reload))\\b"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Read-only auditor.** No writes, no shell. Suitable for a code-review bot or a docs-explainer daemon.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "read-only auditor — no side effects permitted"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
```

Combine with `provider.claudecli.permission_mode: plan` and `provider.claudecli.extra_args: ["--allowed-tools", "read,grep"]` for belt-and-braces enforcement — the model literally cannot request other tools.

  </div>
</div>

## Troubleshooting

### Every call is denied even though I have allow rules

Deny wins over allow. Check whether one of your deny rules matches unintentionally. Log line `tool.denied name=<X> reason=<Y>` includes the exact reason.

### Pattern regex compile error

`PatternApprover` lazily compiles rules on first use. A compile error becomes a `DecisionDeny` with reason `approver: pattern compile: <err>`. Fix the regex; regex101.com with the Go flavour selected is your friend.

### Regex matches JSON literally, not semantically

The `match` regex runs against the raw JSON input of the tool call. Escape quotes and backslashes appropriately: `"\"path\":\"/workspace/"` matches the `path` field of an `edit` or `write` call.

### `deny_all` is not blocking anything

Confirm `mode: deny_all` (not `mode: deny`). The valid modes are `allow_all`, `deny_all`, `pattern`. `allow` and `deny` alone are treated as aliases for the `_all` variants but exact strings are safer.

### Allow rule for `bash` never matches

The `bash` input is JSON like `{"command":"ls -la"}`. Match against that JSON literal, not just the shell command string. Use a pattern like `^\\{\"command\":\"ls`.

## Related pages

- [User Guide: Approval Policies](/user-guide/approval-policies/) — deeper reference and worked examples.
- [User Guide: Tools](/user-guide/tools/) — every built-in tool's schema.
- [Guides: Observability](/guides/observability/) — surface the audit trail.
- [Guides: Read-only mode](/guides/read-only-mode/) — belt-and-braces enforcement.
- [Security](/security/) — trust model overview.

## Further reading

- `internal/agent/approver.go` — `PatternApprover`, `AllowAllApprover`, `DenyAllApprover`.
- `internal/agent/approver_test.go` — test matrix.
- `internal/cli/approver.go` — config → approver translation.
- `internal/config/config.go` — `ApproverConfig`, `PatternEntry`.
