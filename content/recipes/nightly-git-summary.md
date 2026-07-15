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
description: "Daily git summary delivered to WhatsApp before your standup, powered by rousseau cron and claudecli."
keywords: "cron, git, standup, whatsapp, daily summary, recipes"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/recipes/nightly-git-summary/"
subtitle: "Automated daily-standup preview over WhatsApp."
tags: "recipes, cron, whatsapp"
title: "Recipe: Nightly Git Summary"

news_genres: "Blog"
news_keywords: "cron, git, standup, whatsapp"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Recipe: Nightly Git Summary"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "recipes"
order: 12
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/recipes/nightly-git-summary/index.html"
item_link: "https://docs.rousseau-agent.dev/recipes/nightly-git-summary/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Recipe: Nightly Git Summary"
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
twitter_description: "Daily git summary delivered to WhatsApp before your standup."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Recipe: Nightly Git Summary"
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

Every weekday at 08:30 UK, rousseau greps `git log` across a set of repositories, produces a three-bullet standup preview, and delivers it as a WhatsApp message to your personal JID. No cloud SaaS, no `curl` piped through a public bot service.

## Prerequisites

- WhatsApp paired to a phone you own (`rousseau whatsapp` completed at least once).
- A workspace directory with the repositories you care about, bind-mounted into the daemon.
- Provider that can drive tool use — `claudecli` or `anthropic` recommended.

## Config

```yaml
provider: claudecli

state:
  path: ~/.local/share/rousseau/sessions.db

agent:
  max_iterations: 12
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^git (log|diff|status|shortlog|for-each-ref|rev-parse)( |$)"}

whatsapp:
  reply_header: ""
```

Notes on the approver:

- `read` and `grep` are broad because we want the agent to inspect any repo.
- `bash` is limited to *read-only* git subcommands. No `git push`, no `git rebase`, no shell.

## Register the cron job

```sh
rousseau cron add \
  --name daily-standup \
  --schedule '30 8 * * MON-FRI' \
  --prompt 'For each git repository under /workspace, list the last 24h of commits by author. Then produce three bullets: (1) what merged, (2) what stalled, (3) what needs review before standup. Keep it under 800 characters.' \
  --deliver-to '447900123456@s.whatsapp.net'

rousseau cron list
```

## Launch

```sh
# In a Podman container per the Deployment guide, or bare-metal:
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

The cron scheduler starts *inside* the whatsapp daemon (`wiring.startCron`). No separate scheduler process.

## Verification

- [ ] `rousseau cron list` shows `daily-standup` with status `on`.
- [ ] Wait for the next 08:30 fire, or trigger manually with `rousseau chat`:
  ```sh
  rousseau chat --title 'test standup preview' <<'EOF'
  For each repo under /workspace, list yesterday's commits. Three bullets max.
  EOF
  ```
- [ ] Delivery lands on WhatsApp with the prompt's answer.

## Related pages

- [Reference: Commands: cron](/reference/commands/cron/)
- [Reference: Commands: whatsapp](/reference/commands/whatsapp/)
- [Best Practices: Approval rules](/best-practices/approval-rules/)
- [Recipes: Security audit cron](/recipes/security-audit-cron/)
