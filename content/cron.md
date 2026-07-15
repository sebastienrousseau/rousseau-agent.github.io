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
changefreq: "weekly"
description: "rousseau-agent's cron scheduler runs stored jobs on a schedule and delivers replies through any registered transport. Backed by robfig/cron/v3 and SQLite job persistence."
keywords: "cron, robfig/cron, scheduler, scheduled jobs, delivery, transport-agnostic, SQLite persistence"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/cron/"
subtitle: "Persistent scheduled jobs that fire through any transport."
tags: "cron, scheduler, reference"
title: "Cron Scheduler"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, robfig/cron, scheduler, scheduled jobs, delivery, transport-agnostic, SQLite persistence"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Cron Scheduler"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 24
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/cron/index.html"
item_link: "https://docs.rousseau-agent.dev/cron/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Cron Scheduler"
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
twitter_description: "rousseau-agent's cron scheduler runs stored jobs on a schedule and delivers replies through any registered transport. Backed by robfig/cron/v3 and SQLite job persistence."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Cron Scheduler"
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

## Overview

The cron scheduler (`internal/cron/scheduler.go`) is a goroutine that runs stored `CronJob` entries on their configured schedule, executes each job's prompt through the agent, and hands the reply to a transport-agnostic `Delivery` function.

The scheduler runs alongside any long-running daemon (typically `rousseau whatsapp` or another chat transport). Jobs are stored in the same SQLite database as sessions, so they survive restarts.

## Schedule syntax

Backed by [robfig/cron/v3](https://pkg.go.dev/github.com/robfig/cron/v3). The parser supports:

- Standard 5-field cron: `<minute> <hour> <day-of-month> <month> <day-of-week>`.
- Predefined shortcuts: `@yearly`, `@monthly`, `@weekly`, `@daily`, `@hourly`, `@every <duration>`.

Example schedules:

| Expression | Fires |
|---|---|
| `0 9 * * 1-5` | 09:00 on weekdays |
| `*/15 * * * *` | Every 15 minutes |
| `@daily` | Once a day at midnight (server timezone) |
| `@every 30m` | Every 30 minutes |

## CLI

```sh
# List all stored jobs.
rousseau cron list

# Add a job.
rousseau cron add \
  --name morning-standup \
  --schedule '0 9 * * 1-5' \
  --prompt 'What are the top three engineering priorities today?' \
  --target '447900123456@s.whatsapp.net'

# Remove by name or ID.
rousseau cron remove morning-standup
```

## Configuration

Jobs are stored in the state DB, not the config file. There is nothing in `~/.config/rousseau/config.yaml` to configure the scheduler itself; it uses default `PollInterval = 60s`.

## Job flow

1. Scheduler re-syncs the job list from SQLite every `PollInterval`.
2. `robfig/cron/v3` fires the job at its scheduled time.
3. `TurnRunner.RunOnce(ctx, job.Prompt)` executes a **single-turn** agent run against a fresh session (no history, no cross-session recall unless the runner opts in).
4. The reply text is passed to `Delivery(ctx, job.Target, replyText)`.
5. `Delivery` returns error → logged; the next tick retries.

## Delivery

`Delivery` is a small function type:

```go
type Delivery func(ctx context.Context, target, body string) error
```

The scheduler does not import `internal/transport` — the delivery contract is transport-agnostic. In practice, `rousseau <transport>` daemons wire a `Delivery` that resolves the target string against the active transport (`Deliver` on the transport client).

`target` is transport-specific:

- WhatsApp: a JID (`447900123456@s.whatsapp.net`).
- Telegram: a numeric chat ID.
- Slack: a channel ID (`C012345`) or user ID (`U012345`).
- Discord: a channel ID.
- SMS: an E.164 destination.
- iMessage: a chat GUID.
- Signal: an E.164 destination.
- Matrix: a room ID.
- Email: a full RFC 5322 address.

## Persistence

Jobs are stored in the `cron_jobs` table of the state database (`internal/state/sqlite/`). Fields: `id`, `name`, `schedule`, `prompt`, `target`, `created_at`, `updated_at`. Restarts pick up every job on the next `PollInterval`.

New jobs added via `rousseau cron add` become live within one `PollInterval` — up to 60 seconds by default.

## Interaction with transports

The `Delivery` closure captures a reference to the running transport. A single daemon typically runs one transport, so the cron scheduler delivers through that transport. Multi-transport deployments run one daemon per transport, and the operator points each cron job's `target` at the matching transport's daemon.

Cross-transport delivery (job runs in the WhatsApp daemon, replies via Slack) is not supported today — the scheduler only knows about the `Delivery` it was given.

## Failure modes

| Symptom | Fix |
|---|---|
| Job doesn't fire | Check `rousseau status`; the scheduler logs `cron.fired` per activation. |
| Job fires but nothing arrives | Delivery error — check logs for `cron.delivery_failed`. |
| Job runs but the model refuses to act | Approval policy denying tool calls. Loosen `agent.approver` or move to `pattern` mode. |
| Delivery goes to wrong target | The scheduler is transport-agnostic; the daemon interprets `target`. Confirm the transport your daemon is running matches the target format. |
