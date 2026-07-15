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
description: "Complete reference for rousseau cron: add, list, remove, enable, disable scheduled prompts. Cron expression grammar and delivery targets."
keywords: "cron, robfig cron, scheduler, cli reference, rousseau cron"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/commands/cron/"
subtitle: "Complete reference for `rousseau cron`."
tags: "reference, cli, cron, scheduler"
title: "rousseau cron"

news_genres: "Blog"
news_keywords: "cron, scheduler, robfig"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "rousseau cron"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 71
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/commands/cron/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/commands/cron/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "rousseau cron"
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
twitter_description: "Complete reference for rousseau cron: add, list, remove, enable, disable scheduled prompts. Cron expression grammar and delivery targets."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "rousseau cron"
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

`rousseau cron` is a **subcommand tree** that manages scheduled prompts. Jobs live in the `cron_jobs` table inside `sessions.db`. A running transport daemon (any of `whatsapp`, `slack`, `discord`, `telegram`, `matrix`, `signal`, `sms`, `imessage`, `email`) picks up the jobs at startup and fires them via the configured provider, delivering the result to the target address.

Source: `internal/cli/cron.go`. Scheduler: `internal/cron/`. Storage: `internal/state/sqlite/` (`CronStore`).

<aside class="admonition" data-type="note"><span class="admonition-title">Daemon required</span><p>Adding a job persists it but does not run it. Only a transport daemon with <code>startCron</code> in its wiring actually executes jobs. Standalone <code>rousseau cron add</code> does not start a scheduler.</p></aside>

## Command tree

```text
rousseau cron
├── add       Add a scheduled prompt
├── list      List every scheduled job
├── remove    Delete a scheduled job (alias for `rm` in some places)
├── enable    Enable a scheduled job
└── disable   Disable a scheduled job
```

## `cron add`

```sh
rousseau cron add \
  --name <unique-name> \
  --schedule '<5-field cron expression>' \
  --prompt '<prompt text>' \
  --deliver-to <target>
```

| Flag | Type | Required | Effect |
|---|---|---|---|
| `--name` | string | yes | Unique name across jobs. |
| `--schedule` | string | yes | 5-field cron expression (min hour dom mon dow). Validated with `cron.ParseStandard`. |
| `--prompt` | string | yes | Prompt to run at each fire. |
| `--deliver-to` | string | no | Delivery target — a JID for WhatsApp, a Slack channel/user id, etc. Interpreted by the running transport. |

## Cron expression grammar

Rousseau uses [robfig/cron/v3](https://pkg.go.dev/github.com/robfig/cron/v3)'s standard parser. Five fields:

| Field | Range | Example |
|---|---|---|
| minute | 0–59 | `*/5` |
| hour | 0–23 | `9` |
| day of month | 1–31 | `1` |
| month | 1–12 or JAN–DEC | `*` |
| day of week | 0–6 or SUN–SAT | `MON-FRI` |

Common recipes:

```text
0 9 * * MON-FRI    # every weekday at 09:00
*/15 * * * *       # every 15 minutes
0 */6 * * *        # every 6 hours on the hour
30 8 1 * *         # 08:30 on the 1st of every month
```

## `cron list`

```sh
rousseau cron list
```

Prints one row per job:

```text
<short-id>  <on|off>  <name>           <cron_expr>            last=<time-or-never>
    <prompt> → <deliver-to>
```

## `cron remove`

```sh
rousseau cron remove <name-or-id>
```

Matches by full or short (8-char) id, or by exact name.

## `cron enable` / `cron disable`

```sh
rousseau cron enable <name-or-id>
rousseau cron disable <name-or-id>
```

Toggles the `enabled` flag without deleting. Disabled jobs are skipped by the scheduler but survive restarts.

## Environment variables

Inherits every env var from `config.Load`. The most relevant for cron is `ROUSSEAU_STATE_PATH` — every cron subcommand opens the same SQLite store as `chat`.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Successful add/list/remove/toggle. |
| 1 | Missing required flags, invalid cron expression, store error, unknown job. |

## Worked examples

<div class="tabs" data-tabs="cron-examples">
  <div class="tab-list" role="tablist" aria-label="Recipe">
    <button role="tab" aria-selected="true">Daily standup</button>
    <button role="tab" aria-selected="false">Weekly digest</button>
    <button role="tab" aria-selected="false">Hourly probe</button>
  </div>
  <div class="tab-panel" role="tabpanel">

```sh
rousseau cron add \
  --name daily-standup \
  --schedule '0 9 * * MON-FRI' \
  --prompt 'Summarise yesterday'\''s git activity in team-rousseau-workspace and post it as three bullets.' \
  --deliver-to '447900123456@s.whatsapp.net'
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```sh
rousseau cron add \
  --name weekly-digest \
  --schedule '0 17 * * FRI' \
  --prompt 'Read the CHANGELOG and produce a one-paragraph digest for stakeholders.' \
  --deliver-to '#eng-updates'
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```sh
rousseau cron add \
  --name log-health \
  --schedule '0 * * * *' \
  --prompt 'Grep for ERROR in the last hour of journalctl output; if any, list them.' \
  --deliver-to '447900123456@s.whatsapp.net'
```

  </div>
</div>

## Common failure modes

- **`invalid cron expression`** — five whitespace-separated fields expected. Six-field notation with seconds is not supported.
- **`unique constraint failed`** — name already exists. `remove` first or use a different name.
- **Job never fires** — no transport daemon is running. Start `rousseau whatsapp` / `slack` / etc.
- **`deliver-to` ignored** — some transports (email, sms) require a specific address shape. The default `whatsapp` interpretation is a JID.

## Related pages

- [Concepts: Cron](/cron/)
- [Recipes: Nightly git summary](/recipes/nightly-git-summary/)
- [Recipes: Security audit cron](/recipes/security-audit-cron/)
- [Reference: Session store](/reference/session-store/)
- [Reference: Commands: chat](/reference/commands/chat/)
