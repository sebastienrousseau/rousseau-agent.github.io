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
description: "Wire rousseau into your on-call Slack channel so it answers with runbook context, cross-session recall, and safe filesystem inspection."
keywords: "oncall, slack, socket mode, triage, runbook, recipes"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/recipes/oncall-slack-triage/"
subtitle: "Rousseau in the on-call Slack channel."
tags: "recipes, slack, oncall"
title: "Recipe: On-call Slack Triage"

news_genres: "Blog"
news_keywords: "oncall, slack, triage"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Recipe: On-call Slack Triage"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "recipes"
order: 11
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/recipes/oncall-slack-triage/index.html"
item_link: "https://docs.rousseau-agent.dev/recipes/oncall-slack-triage/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Recipe: On-call Slack Triage"
last_build_date: "Mon, 13 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
ttl: "60"
type: "website"
webmaster: sebastian.rousseau@gmail.com (Sebastien Rousseau)

apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "rousseau-agent"
apple-touch-fullscreen: "yes"

msapplication-navbutton-color: "rgb(26,58,138)"

twitter_card: "summary"
twitter_creator: "rousseauagent"
twitter_description: "Wire rousseau into your on-call Slack channel so it answers with runbook context, cross-session recall, and safe filesystem inspection."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Recipe: On-call Slack Triage"
twitter_url: "https://docs.rousseau-agent.dev"

author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Overview

Deploy rousseau as a Slack bot in your on-call channel. When someone mentions the bot with an incident question, it consults the runbook directory, grep-searches the codebase, and posts a triage note — with cross-session recall so it remembers what worked in the last incident.

<aside class="admonition" data-type="tip"><span class="admonition-title">Why this works</span><p>Slack Socket Mode is a purely outbound WebSocket, so no public HTTP surface is exposed. Combined with pattern-mode approvals and a workspace bind mount, the bot can inspect but not damage.</p></aside>

## Prerequisites

- Slack workspace admin rights to create an app and install it.
- A Slack app with Socket Mode enabled, `app-level token` (`xapp-*`) with `connections:write`, and a `bot token` (`xoxb-*`) with `chat:write`, `channels:history`, `im:history`, `message.channels` event subscriptions.
- Any rousseau-supported provider — `claudecli` inheriting Claude Code auth, or `anthropic` with an API key.
- A runbook directory (`~/runbooks/`) or similar.

## Config

```yaml
provider: claudecli

state:
  path: ~/.local/share/rousseau/sessions.db

agent:
  system_prompt: |
    You are a careful on-call triage assistant. When asked about an
    incident, first grep the runbooks directory, then read matching
    files, then propose a triage plan. Never run destructive commands.
  max_iterations: 24
  skills_dir: ~/.config/rousseau/skills
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read,  match: ".*"}
      - {tool: grep,  match: ".*"}
      - {tool: bash,  match: "^(ls|cat|rg|head|tail|kubectl get|journalctl -u [a-z-]+ --since=[0-9]+m -n 200)"}
    deny:
      - {tool: bash,  match: "rm -rf|sudo|kubectl delete|kubectl scale"}

slack:
  app_token: "xapp-…"
  bot_token: "xoxb-…"
  bot_user_id: "U0ABC1234"
  reply_header: ""
  allowlist: []          # empty = anyone in a channel the bot is invited to
```

## Launch

```sh
# 1. Confirm doctor is happy
rousseau doctor

# 2. Optional: pre-populate cross-session recall by chatting once
rousseau chat --title "seed: previous SEV-2 postmortem" <<'EOF'
Read /var/postmortems/2026-07-01-payments.md and summarise root cause + mitigation.
EOF

# 3. Start the bridge (foreground for testing)
rousseau slack

# 4. Once verified, run under systemd
systemctl --user start rousseau-slack.service
journalctl --user -u rousseau-slack.service -f
```

## Systemd unit (bare-metal)

```ini
# ~/.config/systemd/user/rousseau-slack.service
[Unit]
Description=Rousseau on-call Slack triage bot
After=network-online.target

[Service]
ExecStart=%h/go/bin/rousseau slack
Restart=on-failure
RestartSec=10
Environment=ROUSSEAU_LOG_FORMAT=json

[Install]
WantedBy=default.target
```

## Verification

- [ ] `rousseau doctor` returns green.
- [ ] `journalctl --user -u rousseau-slack.service | grep slack.connected` fires within 5 s.
- [ ] `@rousseau ping` in the on-call channel produces a reply within 3 s.
- [ ] `@rousseau what happened in the payments outage last month?` produces a summary that mentions files from `/var/postmortems/`.

## Skills you'll want

Drop these in `~/.config/rousseau/skills/`:

<div class="tabs" data-tabs="oncall-skills">
  <div class="tab-list" role="tablist" aria-label="Skill">
    <button role="tab" aria-selected="true">triage.md</button>
    <button role="tab" aria-selected="false">runbook-cite.md</button>
  </div>
  <div class="tab-panel" role="tabpanel">

```markdown
---
name: triage
trigger: incident, sev, page, error
---
When the user pastes an error message or asks about an incident:
1. Search runbooks with `grep` for the key phrases.
2. If matched, `read` the top runbook.
3. Propose a triage plan as numbered steps.
4. Ask what the user has already tried before running any shell command.
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```markdown
---
name: runbook-cite
trigger: runbook, cite, source
---
Always cite runbook filenames and line numbers when quoting.
Format: `runbooks/payments.md:42–58`.
```

  </div>
</div>

## Failure modes

- **Bot answers itself in a loop** — `slack.bot_user_id` is wrong. Verify with `curl -H "Authorization: Bearer $BOT" https://slack.com/api/auth.test`.
- **Bot never sees messages** — the app is missing the Message Content-equivalent subscription, or Socket Mode is disabled.
- **Bot deletes files** — pattern approver deny-rules are missing. Every recipe MUST include a deny for `rm`, `sudo`, and destructive `kubectl` variants.

## Related pages

- [Reference: Commands: slack](/reference/commands/slack/)
- [Transports: Slack](/transports/slack/)
- [Best Practices: Approval rules](/best-practices/approval-rules/)
- [Skills](/skills/)
- [Recipes: Code review bot](/recipes/code-review-bot/)
