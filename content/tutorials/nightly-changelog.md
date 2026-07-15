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
description: "Schedule a rousseau cron job that summarises git log every evening and posts the result to WhatsApp."
keywords: "cron, git log, changelog, whatsapp, scheduled prompt, deliver-to"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/tutorials/nightly-changelog/"
subtitle: "A daily 18:00 cron job that pushes a git-log summary to WhatsApp."
tags: "tutorials, cron, changelog, whatsapp, git"
title: "Tutorial: Nightly changelog"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, git log, changelog, whatsapp, scheduled prompt, deliver-to"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorial: Nightly changelog"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/nightly-changelog/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/nightly-changelog/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorial: Nightly changelog"
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
twitter_description: "Schedule a rousseau cron job that summarises git log every evening and posts the result to WhatsApp."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorial: Nightly changelog"
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

A cron job stored in rousseau's own SQLite state (`cron_jobs` table, schema in `internal/state/sqlite/cron.go`) that fires at 18:00 local time on weekdays. It runs a prompt that asks the model to summarise `git log --since=today` and delivers the result to your phone over WhatsApp.

Estimated time: 10 minutes.

## Prerequisites

- WhatsApp bridge already paired (see [Quickstart](/quickstart/) step 4 or [Transports: WhatsApp](/transports/whatsapp/)).
- The `rousseau whatsapp` daemon running — the cron scheduler in `internal/cron/scheduler.go` is booted by transport daemons via `wiring.startCron()`, not by `rousseau chat`.
- A workspace containing the git repo you want summarised, bind-mounted into the container (or on the host if you run rousseau outside a container).

## How rousseau cron works

`rousseau cron add` writes a row to the `cron_jobs` table (`internal/state/sqlite/cron.go`). Every ~15 seconds, `scheduler.sync` re-reads the table and reconciles the robfig/cron/v3 in-memory schedule. When a job fires, the scheduler emits `cron.firing`, runs the prompt through the configured provider, and delivers the result to `deliver_to` via the transport bridge that owns the process (WhatsApp in this tutorial).

Structured log names you'll see (from `internal/cron/scheduler.go`):

- `cron.started` — scheduler booted with `poll_interval=…`.
- `cron.scheduled` — a job was accepted.
- `cron.firing` — a job is about to run.
- `cron.completed` — a job finished successfully.
- `cron.run_failed`, `cron.delivery_failed`, `cron.record_failed` — failure modes.

## Step 1: add the job

```sh
rousseau cron add \
  --name        nightly-changelog \
  --schedule    "0 18 * * 1-5" \
  --prompt      "Summarise git log --since=yesterday under /workspace/rousseau-agent as a Slack-style bullet list. Keep it under 200 words. If nothing changed, reply with a single line 'no commits'." \
  --deliver-to  447900123456@s.whatsapp.net
```

The cron expression is parsed by `robfig/cron/v3` in `newCronAddCmd` (`internal/cli/cron.go`). Invalid expressions are rejected before write. The `--deliver-to` value is the E.164 JID for WhatsApp (`<digits>@s.whatsapp.net`); the delivery target format is transport-specific.

## Step 2: verify

```sh
rousseau cron list
```

Output shape (from `newCronListCmd`):

```
NAME               STATUS SCHEDULE       PROMPT                       DELIVER-TO
nightly-changelog  on     0 18 * * 1-5   Summarise git log …          447900123456@s.whatsapp.net
```

The list is also exposed over MCP as `rousseau_cron_list` (see `internal/mcp/tools.go`).

## Step 3: dry-run

There is no built-in "fire now" trigger. To smoke-test, temporarily schedule the job one minute in the future:

```sh
rousseau cron remove nightly-changelog
rousseau cron add --name test --schedule "*/1 * * * *" --prompt "say hi" --deliver-to "$JID"
journalctl --user -u rousseau-agent -f | grep cron.
```

Expected log sequence:

```
INFO cron.scheduled  job=test expr=*/1 * * * *
INFO cron.firing     job=test
INFO cron.completed  job=test
```

Remove the test job and re-add the real one when you're done.

## Step 4: tighten the prompt

The best cron prompts are self-contained: the model has no memory of previous runs. Include the repo path, expected output format, and a fallback for the empty case. Example second iteration:

```
Summarise commits authored since 07:00 UTC today under
/workspace/rousseau-agent. Use this format:

- <short type>: <one-line summary> — <sha>

Group by author. If no commits landed, reply exactly: no commits.
```

## Toggling and removing

```sh
rousseau cron disable nightly-changelog   # keeps the row, stops firing
rousseau cron enable  nightly-changelog
rousseau cron remove  nightly-changelog   # deletes the row
```

`SetEnabled` and `Delete` from `internal/state/sqlite/cron.go` are what these call.

## Related

- [Cron](/cron/) — reference for the scheduler.
- [Guides: Scheduled tasks](/guides/scheduled-tasks/) — deeper discussion.
- [Transports: WhatsApp](/transports/whatsapp/) — how delivery-to works.
- [Reference: CLI Commands](/reference/cli-commands/) — every `rousseau cron` flag.
