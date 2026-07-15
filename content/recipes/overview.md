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
description: "Index of end-to-end rousseau recipes: on-call triage, nightly summaries, code review, security audits, community bots and more."
keywords: "recipes, cookbook, oncall, cron, code review, community"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/recipes/overview/"
subtitle: "The rousseau cookbook."
tags: "recipes, cookbook"
title: "Recipes Overview"

news_genres: "Blog"
news_keywords: "recipes, cookbook"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Recipes Overview"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "recipes"
order: 10
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/recipes/overview/index.html"
item_link: "https://docs.rousseau-agent.dev/recipes/overview/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Recipes Overview"
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
twitter_description: "Index of end-to-end rousseau recipes: on-call triage, nightly summaries, code review, security audits, community bots and more."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Recipes Overview"
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

Recipes are end-to-end walkthroughs. Each one wires several rousseau primitives — transports, cron, provider, approval policies — into a shipped, tested workflow. Copy, adjust the JIDs / tokens, and run.

<aside class="admonition" data-type="tip"><span class="admonition-title">How to read a recipe</span><p>Every recipe includes: the operational problem it solves, prerequisites, config file, launch commands, verification, and the failure modes we've actually seen. Skim the "prerequisites" first — if you don't have a Slack app or a Bedrock contract, jump to another recipe.</p></aside>

## Recipe index

| Recipe | Transport | Provider | Cadence |
|---|---|---|---|
| [On-call Slack triage](/recipes/oncall-slack-triage/) | Slack Socket Mode | any | live |
| [Nightly git summary](/recipes/nightly-git-summary/) | WhatsApp | claudecli | daily 06:00 |
| [Email triage](/recipes/email-triage/) | Email (IMAP+SMTP) | anthropic | live |
| [Code review bot](/recipes/code-review-bot/) | Slack | anthropic | live |
| [Security audit cron](/recipes/security-audit-cron/) | Signal | claudecli | weekly |
| [WhatsApp pair programming](/recipes/whatsapp-pair-programming/) | WhatsApp | claudecli | live |
| [Matrix room monitor](/recipes/matrix-room-monitor/) | Matrix | anthropic | live |
| [Discord community bot](/recipes/discord-community-bot/) | Discord | anthropic | live |
| [MCP desktop integration](/recipes/mcp-desktop-integration/) | MCP (stdio) | any | on-demand |
| [Bedrock multi-account](/recipes/bedrock-multi-account/) | any | Bedrock | live |
| [Airgapped deployment](/recipes/airgapped-deployment/) | any | Ollama / vLLM | live |

## Design patterns you'll see

### Cron + transport delivery

Every recipe that produces a scheduled artefact uses `rousseau cron add` with `--deliver-to` set to a JID / user id understood by the running transport. The scheduler goroutine invokes the transport's `Deliver` method — the same code path the agent uses for reply messages.

```sh
rousseau cron add \
  --name daily-standup \
  --schedule '0 9 * * MON-FRI' \
  --prompt 'Summarise yesterday'\''s commits' \
  --deliver-to '447900123456@s.whatsapp.net'
```

### Pattern-mode approver

Most production recipes use `agent.approver.mode: pattern` with `default: deny` and specific allow-rules. This lets the agent touch the filesystem where useful (reading, grepping, editing project files) while blocking destructive shell commands.

### Skills for role-specific behaviour

`agent.skills_dir` points at a directory of Markdown files. Each file contains agentskills.io-style YAML frontmatter and a body prompt. Rousseau discovers them and composes them into the system prompt — so a "code reviewer" skill and an "SRE triage" skill can coexist without config gymnastics.

## Recipe template

If you're writing a new recipe (see [Community: Contributing](/community/contributing/)), follow this structure:

1. Overview — the operational problem in three sentences.
2. Prerequisites — transports, providers, external services.
3. Config — copy-pastable YAML.
4. Launch — the exact commands.
5. Verification — what "working" looks like.
6. Failure modes — the top three things we've seen go wrong.
7. Related pages — cross-links.

## Related pages

- [Reference: Commands: cron](/reference/commands/cron/)
- [Reference: Config: Agent](/reference/config/agent/)
- [Best Practices: Approval rules](/best-practices/approval-rules/)
- [Tutorials](/tutorials/)
