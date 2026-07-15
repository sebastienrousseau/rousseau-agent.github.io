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
description: "Go from bypassPermissions to a pattern-mode approver with default: deny and validate the audit trail through slog."
keywords: "approver, pattern mode, default deny, tool denied, audit, slog"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/tutorials/harden-approver-policy/"
subtitle: "From bypassPermissions to default-deny with slog-audited rule matching."
tags: "tutorials, approver, pattern-mode, security, audit"
title: "Tutorial: Harden the approver"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approver, pattern mode, default deny, tool denied, audit, slog"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorial: Harden the approver"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 46
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/harden-approver-policy/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/harden-approver-policy/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorial: Harden the approver"
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
twitter_description: "Go from bypassPermissions to a pattern-mode approver with default: deny and validate the audit trail through slog."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorial: Harden the approver"
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

## What you build

A rousseau daemon that started out running the `claudecli` provider in `bypassPermissions` mode (the unattended default) ends up under a `pattern`-mode rousseau-agent approver with `default: deny`. Every tool call is either explicitly allowlisted or blocked; every denial produces a `tool.denied` slog event you can audit.

Estimated time: 30 minutes for a proper rules pass with tests.

## Prerequisites

- Rousseau installed with any transport bridge running (WhatsApp, Slack, Signal — anything unattended).
- Basic Go regex familiarity — approver rules are Go RE2 regexes over the JSON tool-input.

## Where the approver lives

Two independent layers can approve tool calls:

1. **The provider's own permission mode.** The `claudecli` provider (`internal/llm/claudecli/client.go`) delegates to `claude --permission-mode`. Values documented in `ClaudeCLIConfig.PermissionMode` (`internal/config/config.go`): `acceptEdits`, `auto`, `bypassPermissions`, `default`, `dontAsk`, `plan`. Unattended daemons pin `bypassPermissions` in `setUnattendedPermissionDefault`.
2. **Rousseau's own approver.** Configured under `agent.approver` (`internal/config/config.go` `ApproverConfig`; implementation in `internal/agent/approver.go`). Three modes: `allow_all`, `deny_all`, `pattern`. **Deny wins over allow, and unmatched calls fall back to `default`.**

For an unattended daemon, the rousseau approver is the mitigation you configure by hand. `claudecli`'s own mode is the seatbelt.

## Step 1: baseline audit

Before writing rules, run a few realistic sessions with `mode: allow_all` and `log.format: json`. Every tool call emits `tool.execute` (`internal/agent/agent.go`):

```sh
jq -c 'select(.msg == "tool.execute") | {name, input: .input}' \
  < /var/log/rousseau.jsonl \
  | sort | uniq -c | sort -rn | head
```

You now have an empirical distribution of which tools the agent uses and against which paths. That's the seed for the allowlist.

## Step 2: draft a pattern policy

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by pattern policy — ask the operator to loosen the rules"
    allow:
      # Read side: unrestricted within the daemon's filesystem view.
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

      # Editing pinned to /workspace.
      - {tool: edit,  match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}

      # Shell: whitelist of read-only utilities plus git status/diff/log.
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|grep|rg|find|wc|stat|file|which|pwd|env|git status|git diff|git log|go test|go vet|go build)\\b"}

    deny:
      # Absolute denies override any allow above.
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s|ncat"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}    # fork bomb
      - {tool: write, match: "\"path\":\"/etc/|/root/|/var/"}
      - {tool: edit,  match: "\"path\":\"/etc/|/root/|/var/"}
```

Deploy and watch the slog stream. The relevant events (`internal/agent/agent.go`):

- `tool.execute` — the call ran. Fields: `name`, `id`.
- `tool.denied` — the approver blocked it. Fields: `name`, `reason`.
- `tool.error` — it ran and failed. Fields: `name`, `err`.

## Step 3: iterate

The first day surfaces false positives: legitimate tool calls the approver blocked. Grep for them:

```sh
jq -c 'select(.msg == "tool.denied") | {name, input}' \
  < /var/log/rousseau.jsonl \
  | sort | uniq -c | sort -rn | head
```

Every recurring `tool.denied` deserves a decision:

- **Genuinely needed** — extend the allow rule. Prefer narrow (path pinned) over broad (open-ended regex).
- **Not needed** — leave denied. The model will pivot to a different approach.

Do not weaken `default: deny`. That is the property that makes an unforgotten tool safe.

## Step 4: audit-log excerpt

A production run with an unfamiliar prompt looked like this:

```jsonl
{"time":"2026-07-13T18:00:12Z","level":"INFO", "msg":"whatsapp.incoming","from":"447900123456@s.whatsapp.net"}
{"time":"2026-07-13T18:00:14Z","level":"INFO", "msg":"tool.execute","name":"grep","id":"t_1"}
{"time":"2026-07-13T18:00:15Z","level":"INFO", "msg":"tool.execute","name":"read","id":"t_2"}
{"time":"2026-07-13T18:00:17Z","level":"WARN", "msg":"tool.denied","name":"bash","reason":"denied by pattern policy — ask the operator to loosen the rules"}
{"time":"2026-07-13T18:00:18Z","level":"INFO", "msg":"tool.execute","name":"read","id":"t_3"}
{"time":"2026-07-13T18:00:20Z","level":"INFO", "msg":"whatsapp.handler_ok","elapsed":"7.4s"}
```

The one `tool.denied` here was `bash: "curl https://…"`. The deny rule caught it, the model degraded to `read` + `grep`, and the reply still went through.

## Step 5: bake it in

Once the false-positive rate settles, freeze the config, commit it to source control (secrets excluded — see [Guides: Enterprise Onboarding](/guides/enterprise-onboarding/)), and gate config changes behind a code review. `internal/agent/approver_test.go` in the source tree is your model for how to write tests against the ruleset — copy its shape into an internal package if you want CI to catch a broken policy.

## What the policy still does not do

Even with the tightest pattern rules:

- **No sandboxing.** An allowed `bash` call still runs with the daemon's UID and filesystem visibility. Layer a rootless container ([Deployment](/deployment/)) under it.
- **No rate limiting.** Ten allowed calls per second are all allowed. Wrap the tool registry if you need this.
- **No outbound network audit.** The approver sees the initial `bash` `command` string, not what it curls. Deny `curl` and `wget` outright — the sample deny rules do this.

See [Guides: Audit + approval policies](/guides/audit-approval-policies/) for the deeper discussion.

## Related

- [User Guide: Approval Policies](/user-guide/approval-policies/) — reference for every mode.
- [User Guide: Tools](/user-guide/tools/) — tool schemas, useful for writing regex.
- [Guides: Observability](/guides/observability/) — pipe `tool.denied` to Loki/Datadog.
- [Reference: Logs](/reference/logs/) — every well-known slog message.
