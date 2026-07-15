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
description: "Use case narrative: reviewing pull requests from WhatsApp on the train, driven by rousseau-agent on a home box."
keywords: "mobile review, whatsapp, pr review, commute, use case, pull request"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/use-cases/mobile-review/"
subtitle: "Reviewing PRs from your phone on the train."
tags: "use-cases, whatsapp, mobile, pr"
title: "Use Case: Mobile PR Review"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mobile review, whatsapp, pr review, commute, use case, pull request"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Use Case: Mobile PR Review"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 72
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/use-cases/mobile-review/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/mobile-review/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Use Case: Mobile PR Review"
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
twitter_description: "Use case narrative: reviewing pull requests from WhatsApp on the train, driven by rousseau-agent on a home box."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Use Case: Mobile PR Review"
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

You are a staff engineer at a mid-sized company. Your inbox has eight open PRs waiting on your review. You are on a 45-minute train ride and have signal but no laptop. Historically, PR review from the phone means squinting at GitHub's diff view and typing hollow "LGTM" comments.

Rousseau lives on the little Intel NUC in your closet. It has a WhatsApp connection to your JID, `bypassPermissions` on the local `claude` CLI, and read access to your local checkouts of the three repos you review. You DM WhatsApp:

> review PR #4821 in checkout-service

Rousseau runs `gh pr diff 4821`, reads the code, and replies:

> PR #4821 adds retry-with-backoff to the Stripe webhook handler. Three observations:
>
> 1. The backoff is uncapped — if Stripe is truly down, we'll accumulate goroutines forever. Suggest a `context.WithTimeout` at the caller.
> 2. Test file adds two new tests but neither covers the timeout path.
> 3. `pkg/webhook.go:82` — the mutex is held across the network call. Minor.
>
> Should I draft a review comment stub?

You reply:

> yes, with all three

Rousseau uses `gh pr review` under `--draft` (approver blocks final approval; a human still has to click "submit review"). By the time you're at your desk, the draft comment is waiting.

## What that requires

### The daemon

Rousseau on the NUC as a rootless Podman container:

- **Provider**: `claudecli` — inherits your local Claude Code auth.
- **Transport**: WhatsApp — the transport of choice for mobile reach.
- **State**: `~/.local/share/rousseau/sessions.db`.

### Config

```yaml
provider: claudecli

claudecli:
  binary: claude
  permission_mode: bypassPermissions

whatsapp:
  reply_header: "🚂 *rousseau*\n\n"

log:
  level: info
  format: text                # this is a single-user daemon; text logs are fine

agent:
  max_iterations: 32
  compression:
    enabled: true             # subscription-tier claudecli; compression is free
    trigger_messages: 60
    keep_recent: 8
  approver:
    mode: pattern
    default: deny
    reason: "denied — this daemon reviews code, it does not merge it"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(gh pr view|gh pr diff|gh pr list|gh pr review --draft|gh pr comment|git status|git diff|git log|git show) "}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(go test|go vet|go build|npm test|pnpm test|cargo check) "}
    deny:
      - {tool: bash, match: "gh pr merge|gh pr close|gh pr approve"}
      - {tool: bash, match: "git (push|reset --hard|clean)"}
      - {tool: write, match: "\"path\":\"/etc/|/root/|/var/"}
      - {tool: edit,  match: "\"path\":\"/etc/|/root/|/var/"}
```

### The bind mounts

- `~/repos/checkout-service/` (read-only).
- `~/repos/payments-api/` (read-only).
- `~/repos/web-frontend/` (read-only).
- `~/.claude/` — Claude Code's OAuth tokens (read-write, but only for token refresh).
- `~/.config/gh/` — GitHub CLI's OAuth token (read-write, same reason).

Read-only mounts prevent the model from accidentally editing your working copy. Reviews go through GitHub, not through your checkout.

### First launch

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

You scan the QR code once. From then on the daemon lives in the Quadlet unit and boots on host restart. Your allowlist is the JID of your own personal phone.

## The security posture

- **Allowlist locks the transport.** Only your phone can drive the daemon. Anyone else who somehow discovers the phone number gets silently dropped.
- **Pattern approver blocks every merge / push / close.** Rousseau reviews, drafts, and comments — a human still has to click "Merge" or "Approve".
- **Read-only mounts** protect your working checkouts.
- **`bypassPermissions` on claudecli** is only tolerable because the approver is doing the safety work. Never combine `bypassPermissions` with `mode: allow_all`.

## The reach

- **Signal drops on the tube.** WhatsApp's backpressure is graceful — you send a question, you get an answer when the daemon has signal to reply. Rousseau does not need to hold a live TCP session with your phone.
- **Voice notes work.** With [voice mode](/user-guide/voice-mode/) enabled and `whisper.cpp` installed on the NUC, you can dictate a voice note "what's the diff on 4821" and get a text reply. Useful when typing on a phone in a moving train is annoying.
- **The daemon runs on your hardware.** Nothing about your review reasoning goes to a third-party SaaS. The only outbound call is the `claude` CLI's subprocess to Anthropic, using your existing subscription.

## What rousseau does not do here

- **It does not click "Merge".** That's a human decision, and the approver enforces it.
- **It does not learn your review style.** The next PR gets the same generic checklist unless you author a [skill](/skills/) capturing your style.
- **It does not queue reviews.** Each request is independent; there's no "review all my open PRs" background job (unless you wire one via [cron](/guides/scheduled-tasks/)).

## What you'd change under load

- Add a [skill](/skills/) called `pr-review-checklist.md` that codifies the six things you always check. Skills are spliced into the system prompt when a matching trigger appears in the user message.
- Add a nightly cron: `0 8 * * 1-5 rousseau ... deliver a summary of every open PR`.
- Switch to a paid Anthropic API path if `claudecli` subscription rate limits become a bottleneck. Zero config changes downstream.

## Related pages

- [WhatsApp transport](/transports/whatsapp/) — the transport reference.
- [claudecli provider](/providers/claudecli/) — inherited auth.
- [Skills](/skills/) — how to codify your review style.
- [Voice mode](/user-guide/voice-mode/) — dictate reviews.
