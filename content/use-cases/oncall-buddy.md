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
description: "Use case narrative: a solo SRE running rousseau-agent over Slack to triage a 3 a.m. page from the couch, then hand off to full incident response."
keywords: "on-call, sre, slack, incident, page, triage, use case"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/use-cases/oncall-buddy/"
subtitle: "Triaging a 3 a.m. page from the couch over Slack."
tags: "use-cases, on-call, slack, sre"
title: "Use Case: On-call Buddy"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "on-call, sre, slack, incident, page, triage, use case"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Use Case: On-call Buddy"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 71
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/use-cases/oncall-buddy/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/oncall-buddy/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Use Case: On-call Buddy"
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
twitter_description: "Use case narrative: a solo SRE running rousseau-agent over Slack to triage a 3 a.m. page from the couch, then hand off to full incident response."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Use Case: On-call Buddy"
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

## The story

It's 3 a.m. Your pager fires. PagerDuty says the checkout service is throwing 502s. You are one of two SREs at a small company, your co-lead is on holiday, and getting to your laptop means finding your glasses, walking downstairs, and unlocking a VPN. Before all of that, you want a first-pass answer: what dashboards look bad, what changed in the last 24 hours, what runbook applies.

Rousseau lives on the ops box in your closet. It has read-only credentials to your logging stack, read-only kubectl in one namespace, and a Slack Socket Mode connection into `#incident-oncall`. You tap the DM notification on your phone:

> what changed in checkout in the last 24h?

Rousseau reads the git log for the checkout service repo, cross-references against your deploy log (from a bind-mounted directory), and replies:

> Two changes: PR #4821 (payment retry logic, deployed 21:14 UTC) and a Helm value bump on `checkout-web` at 22:03 UTC. The payment retry change is the more suspicious — it touches the same code path the current 502s originate from.

You ask:

> pull the last 100 error lines from checkout-web

Rousseau runs `kubectl logs -n checkout deploy/checkout-web --tail=100 --previous` under its read-only kubeconfig, and pastes back the salient lines. You spot a null-pointer trace. You DM back:

> revert PR #4821 in staging first — call me when it's confirmed green

Rousseau posts to `#incident-oncall` with a plan, opens a revert PR against staging, and pings back once staging is green. You get up and get to your laptop.

## What that requires

### The daemon

Rousseau runs as a rootless Podman container on the ops box:

- **Provider**: `bedrock` — your company already has a Bedrock spend commitment; no per-user API keys required.
- **Transport**: Slack Socket Mode — no inbound HTTP surface, WebSocket outbound only.
- **State**: `~/.local/share/rousseau/sessions.db`, on a LUKS-encrypted disk.

### Config

```yaml
provider: bedrock

bedrock:
  region: us-east-1
  profile: rousseau-oncall
  model: anthropic.claude-sonnet-4-6-20250101-v1:0

log:
  level: info
  format: json

state:
  path: /var/lib/rousseau/sessions.db

agent:
  max_iterations: 32
  approver:
    mode: pattern
    default: deny
    reason: "read-only on-call posture — ask an operator to widen the scope"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(kubectl get|kubectl describe|kubectl logs|git log|git diff|git show|cat|grep|rg|head|tail|wc) "}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"gh pr (view|list|diff) "}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"gh pr create --draft "}   # allows opening a draft revert
    deny:
      - {tool: bash, match: "kubectl (delete|apply|edit|scale|rollout undo|exec)"}
      - {tool: bash, match: "gh pr merge|gh pr close --delete-branch"}

slack:
  app_token: xapp-<...>
  bot_token: xoxb-<...>
  allowlist:
    - U012ABCXYZ    # your Slack user ID
    - U012DEFGHI    # your co-lead's Slack user ID
```

### The bind mounts

- Repo checkouts under `/workspace/repos/` (read-only).
- Deploy log under `/workspace/deploys/` (read-only).
- kubeconfig at `/home/rousseau/.kube/config` — mounted read-only, service account has read-only cluster role in the `checkout` namespace.
- AWS credentials via IAM Role for Service Accounts (IRSA) if on EKS, or via a mounted `~/.aws/` for on-prem.

### The systemd Quadlet unit

The reference `docker/rousseau-agent.container` with:

- `ReadOnly=true`
- `DropCapability=all`
- `NoNewPrivileges=true`
- `Restart=on-failure`

Boots on host restart. Journal available via `journalctl --user -u rousseau-agent.service`.

## The security posture

- **Slack allowlist** ensures only you and your co-lead can drive the daemon. Every other DM is silently dropped.
- **Pattern approver with `default: deny`** blocks anything outside the whitelist. If the model wants to run `kubectl delete pod`, it gets a `tool_result` error explaining the block and reroutes to a plan document.
- **Read-only kubeconfig + read-only repo mounts** mean the daemon *cannot* mutate production even if the approver failed open.
- **Belt, braces, and a second belt** — each layer fails safely.

## What rousseau does not do here

- **It does not page you.** PagerDuty is the source of truth for who is on-call.
- **It does not merge PRs.** The approver blocks `gh pr merge`. Rousseau can open a draft revert; a human still has to confirm.
- **It does not run `kubectl exec`.** Any command that could mutate cluster state is denied.
- **It does not learn from the incident.** Cross-session recall via FTS5 means the next incident's rousseau will find keywords from tonight's session; the semantic conclusions are still the operator's job.

## What you'd change under load

If two 3 a.m. pages a month become two a week:

- Consider promoting more `bash` matchers into `allow` as you gain confidence.
- Wire the slog output into [Loki](/guides/observability/) so post-mortem reviews can cite the exact tool calls rousseau made.
- Add [scheduled tasks](/guides/scheduled-tasks/) so rousseau runs a nightly digest of open incidents into your morning Slack.

## Related pages

- [Guides: Audit + Approval Policies](/guides/audit-approval-policies/) — the safety lever.
- [Guides: Read-only Mode](/guides/read-only-mode/) — the strictest posture.
- [Slack transport](/transports/slack/) — Socket Mode wiring.
- [Bedrock provider](/providers/bedrock/) — auth chain.
