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
description: "Approval policy reference for rousseau-agent: allow_all, deny_all, and pattern-mode approvers with allow/deny regex rules and a configurable default."
keywords: "approval, approver, pattern mode, allow_all, deny_all, regex, safety, tool call"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/user-guide/approval-policies/"
subtitle: "Deep dive on approver modes with worked config."
tags: "approval, policy, pattern-mode, safety"
title: "Approval Policies"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approval, approver, pattern mode, allow_all, deny_all, regex, safety, tool call"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Approval Policies"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "security"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/approval-policies/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/approval-policies/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Approval Policies"
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
twitter_description: "Approval policy reference for rousseau-agent: allow_all, deny_all, and pattern-mode approvers with allow/deny regex rules and a configurable default."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Approval Policies"
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

## The contract

Every tool call passes through `Approver.Approve(ctx, ApprovalRequest)` before it executes. The interface lives in `internal/agent/approver.go`:

```go
type Decision string

const (
    DecisionAllow Decision = "allow"
    DecisionDeny  Decision = "deny"
)

type ApprovalRequest struct {
    ToolName  string
    Input     json.RawMessage
    SessionID string
}

type Approver interface {
    Approve(ctx context.Context, req ApprovalRequest) (Decision, string)
}
```

`Approve` is called synchronously on the hot path; implementations must return promptly or honour `ctx` cancellation.

A `DecisionDeny` with a non-empty reason surfaces the reason back to the model as a `tool_result` error. The model can then adapt (typically by asking the operator for clarification) instead of failing silently. This is a deliberate design decision — silent denials produce worse behaviour than annotated ones.

## Three shipped modes

### `allow_all`

Every tool call runs. This is the baseline behaviour when no approver is configured.

```yaml
agent:
  approver:
    mode: allow_all
```

Use when:

- Interactive `rousseau chat` with the `claudecli` provider (Claude Code is doing its own per-call approvals).
- Development smoke tests where you want to see exactly what the model would do.

### `deny_all`

Blocks every tool call with a single reason string.

```yaml
agent:
  approver:
    mode: deny_all
    reason: "denied by policy for this deployment"
```

Use when:

- Smoke-testing the approver wiring.
- A first-pass inspection posture where you want to see what the model *would* have tried, without letting it act.

### `pattern`

Regex allow / deny rules per tool. **Deny wins over allow.** Unmatched requests fall back to `default` (`allow` or `deny`).

```yaml
agent:
  approver:
    mode: pattern
    default: deny         # safe-by-default; unlisted requests are blocked
    reason: "denied by pattern policy"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}
    deny:
      - {tool: bash, match: "rm -rf|sudo|chmod|chown"}
```

## Rule semantics

Each `PatternRule` has two fields:

| Field | Meaning |
|---|---|
| `tool` | Tool name (`read`, `write`, `edit`, `grep`, `bash`, or any custom tool). Empty matches every tool. |
| `match` | Go RE2 regex against the raw JSON input the model produced. Empty matches every input. |

**Match order:**

1. Every deny rule is tested against the request. First match → deny.
2. Every allow rule is tested. First match → allow.
3. Fall back to `default`. Empty `default` is treated as `deny` — safe-by-default.

Deny always wins because the safer disposition is preferred. An operator adding a broad `allow` block can never accidentally unlock a category they had denied.

## Matching against raw JSON

The `match` regex runs against the **raw JSON input** the model emitted, not against parsed fields. This has two consequences:

1. **You match against the JSON shape.** For a `bash` call, that looks like `{"command":"ls /tmp"}`. Match `"command":\s*"ls\s`.
2. **You can match any field.** The `edit` tool receives `{"path":"/x","old_string":"...","new_string":"..."}`; you can match on `path`, on `old_string`, or on both.

Escape JSON-relevant characters carefully:

- Double quotes are literal in the raw JSON — match with `\"` in your regex if using YAML double-quoted strings.
- Backslashes require doubling in YAML: `\\` in the YAML file becomes `\` in the compiled regex.

## Worked matcher patterns

### Restrict edits to a directory tree

```yaml
allow:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/[^\"]*\""}
  - {tool: write, match: "\"path\":\"/workspace/repo/[^\"]*\""}
```

### Whitelist safe shell commands

```yaml
allow:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|grep|rg|find|git status|git diff|go test) "}
```

### Deny destructive commands regardless of allow

```yaml
deny:
  - {tool: bash, match: "rm\\s+-rf|sudo|:\\(\\)\\{ :\\|:& \\};:"}
```

### Deny writes to system directories

```yaml
deny:
  - {tool: write, match: "\"path\":\"/(etc|root|var|usr)/"}
  - {tool: edit,  match: "\"path\":\"/(etc|root|var|usr)/"}
```

## The `Default` field

`default: deny` is the safer disposition and the recommended value for any unattended daemon. `default: allow` inverts the model — every unlisted call runs, and `deny` rules become the primary lever.

When to use `default: allow`:

- The daemon is running inside a heavily locked-down container ([Deployment](/deployment/)) and the container is your primary boundary.
- You are experimenting and want to see the model's behaviour before deciding what to block.

Everywhere else, prefer `default: deny`.

## The `Reason` field

`reason` is the string returned to the model on every denial (or `default: deny` fallback). Empty falls back to `denied by pattern policy` (or `denied by policy` for `deny_all`).

Setting a helpful reason improves model recovery — instead of `denied by pattern policy`, try `denied — this deployment only allows reads inside /workspace; ask the operator to widen the scope` and watch the model reply with an actionable clarification.

## Interaction with `claudecli`

When `provider: claudecli`, Claude Code is running the tool calls, and its own permission-mode (`bypassPermissions`, `plan`, `default`) also gates every action. Effective behaviour is the intersection: **both** the rousseau approver and Claude Code's approver must permit the call for it to run.

Prefer to keep both aligned:

- Unattended: `bypassPermissions` on Claude Code, `mode: pattern` + `default: deny` on rousseau.
- Read-only inspection: `plan` on Claude Code, `mode: pattern` allowing only `read`/`grep` on rousseau. See [Guides: Read-only Mode](/guides/read-only-mode/).

## Audit trail

Every approver decision is emitted through slog:

| Event | Meaning |
|---|---|
| `tool.execute` (INFO) | Call approved, running. |
| `tool.denied` (WARN) | Call blocked. Includes tool name and reason. |
| `tool.error` (WARN) | Call ran but failed. |

See [Guides: Observability](/guides/observability/) for pipeline recipes.

## Custom approvers

Any type satisfying `Approver` works. Wire your own in when embedding the agent loop:

```go
myApprover := agent.ApproverFunc(func(ctx context.Context, req agent.ApprovalRequest) (agent.Decision, string) {
    // Consult an external policy engine, prompt the operator, ...
    return agent.DecisionAllow, ""
})

ag := agent.New(provider, registry, logger, agent.Options{Approver: myApprover})
```

The interface is deliberately minimal (`Approve` is the only method) so integrating with an external policy engine (OPA, Cedar, or a bespoke rules engine) is a small adapter.

## Troubleshooting

### Every call denied even with a matching allow

Deny wins over allow. `PatternApprover.Approve` in `internal/agent/approver.go` line 152 iterates deny rules first. Look for the exact `reason` string in `tool.denied` logs.

### Regex compile error at start

`PatternApprover` compiles regexes lazily on first `Approve`. A compile error results in `DecisionDeny` with reason `approver: pattern compile: <err>`. Test regexes at [regex101.com](https://regex101.com) with the Go flavour.

### `mode: pattern` but `default:` is ignored

Only `allow` and `deny` are valid values for `default:`. Empty or unknown values fall back to `DecisionDeny` (safe default) and print no warning.

### Allow rule matches the JSON literally

The regex runs against the raw tool-call input JSON. To match a `path` field, escape quotes: `"\"path\":\"/workspace/"`.

### Denied calls do not appear in logs

They do — as `tool.denied` at `warn` level. If you filter by level, ensure `warn` is included.

## Related pages

- [Guides: Audit + Approval Policies](/guides/audit-approval-policies/) — worked example with slog audit trail.
- [Guides: Read-only Mode](/guides/read-only-mode/) — the inspection posture.
- [User Guide: Tools](/user-guide/tools/) — the tools the approver gates.
- [Security](/security/) — trust boundaries overview.
- [Agent loop](/agent-loop/) — where the approver is called.

## Further reading

- `internal/agent/approver.go` — `PatternApprover`, `AllowAllApprover`, `DenyAllApprover`.
- `internal/agent/approver_test.go` — the test matrix.
- `internal/cli/approver.go` — config → approver translation.
- `internal/config/config.go` — `ApproverConfig`, `PatternEntry`.
