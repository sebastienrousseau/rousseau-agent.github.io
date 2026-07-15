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
description: "Worked example: use rousseau-agent's cron scheduler + WhatsApp to run a scheduled prompt daily and deliver the result to your phone."
keywords: "cron, scheduled tasks, whatsapp, code review, robfig, daily reminder"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/guides/scheduled-tasks/"
subtitle: "Nag yourself daily via WhatsApp."
tags: "guides, cron, scheduled, whatsapp"
title: "Guide: Scheduled Tasks"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, scheduled tasks, whatsapp, code review, robfig, daily reminder"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide: Scheduled Tasks"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 31
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/scheduled-tasks/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/scheduled-tasks/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guide: Scheduled Tasks"
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
twitter_description: "Worked example: use rousseau-agent's cron scheduler + WhatsApp to run a scheduled prompt daily and deliver the result to your phone."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide: Scheduled Tasks"
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

## Scenario

You want a daily nudge on WhatsApp at 09:00 asking whether the code-review inbox has anything stale. The agent should read your local review-queue file, summarise, and deliver the summary to your phone — no matter whether your laptop is in the middle of another task.

The moving parts:

- A running `rousseau whatsapp` daemon.
- A cron job persisted in SQLite via `rousseau cron add`.
- The `robfig/cron/v3` scheduler goroutine inside the daemon fires the job; the reply is dispatched through the same WhatsApp transport.

## Prerequisites

- `rousseau whatsapp` paired and delivering messages to at least one JID ([First transport](/getting-started/first-transport/)).
- A file the prompt can point at — for this walkthrough, a Markdown queue at `/workspace/review-queue.md`.

## Step 1 — Register the job

```sh
rousseau cron add \
  --name daily-review-nag \
  --schedule "0 9 * * *" \
  --prompt "Read /workspace/review-queue.md and list every PR that has been open for more than 3 days. Reply with 3 bullets max." \
  --deliver-to 447900123456@s.whatsapp.net
```

`--schedule` is a 5-field POSIX-style cron expression parsed by `robfig/cron/v3` (`min hour dom mon dow`). Rousseau validates the expression at add time; an invalid schedule fails fast before it lands in the store.

`--deliver-to` is the WhatsApp JID that will receive the reply. For groups, use the `@g.us` form.

## Step 2 — Confirm the job is live

```sh
rousseau cron list
```

Output:

```
b7a3f2e1  on   daily-review-nag      0 9 * * *             last=never
    Read /workspace/review-queue.md and list every PR that has been open for more than 3 days. Reply with 3 bullets max. → 447900123456@s.whatsapp.net
```

New jobs become live within the next scheduler poll interval (default 60 seconds). No restart required.

## Step 3 — Force a dry run

Scheduled jobs are fired by the running `rousseau whatsapp` daemon. To verify the wiring without waiting until 09:00, temporarily change the schedule to run one minute from now:

```sh
rousseau cron remove daily-review-nag
rousseau cron add \
  --name daily-review-nag \
  --schedule "*/1 * * * *" \
  --prompt "..." \
  --deliver-to 447900123456@s.whatsapp.net
```

Watch the daemon's log:

```
cron.fire   name=daily-review-nag job=b7a3f2e1
tool.execute name=read id=t_1
cron.deliver name=daily-review-nag target=447900123456@s.whatsapp.net bytes=284
```

Once you see the message on your phone, delete the every-minute copy and re-add the daily version.

## Step 4 — Disable without deleting

```sh
rousseau cron disable daily-review-nag
```

Toggling `enabled=false` leaves the job in the store but skips it on every fire. Re-enable with `rousseau cron enable daily-review-nag`.

## What happens under the hood

1. `rousseau cron add` writes a row to the `cron` table in `~/.local/share/rousseau/sessions.db`.
2. The `rousseau whatsapp` daemon starts a `robfig/cron/v3` scheduler goroutine at boot and polls the table every `PollInterval` (60s default).
3. When the cron expression fires, `Runner.RunOnce(ctx, prompt)` runs a one-shot agent turn against a fresh session (no history from prior fires).
4. The reply passes through `Delivery` — a transport-agnostic callback the daemon wires to `client.Deliver(ctx, target, body)`.
5. `last_run_at` is updated in the store. Failures are logged but do not disable the job.

The scheduler is durable: if the daemon dies mid-fire, the next launch picks up the queue. Jobs never fire twice for the same minute because `robfig/cron/v3` deduplicates by tick.

## Common patterns

| Schedule | Meaning |
|---|---|
| `0 9 * * *` | 09:00 every day. |
| `*/15 9-17 * * 1-5` | Every 15 minutes, 09:00–17:59, Mon–Fri. |
| `0 * * * *` | Top of every hour. |
| `0 0 * * 0` | Midnight every Sunday. |

## Layering with skills

Long prompts get tedious. If a scheduled job's prompt keeps growing, move the boilerplate into a [skill](/skills/) and let the prompt reference it. The skill is spliced into the system prompt at fire time.

## Caveats

- Scheduled jobs run against the daemon's configured provider. If your primary provider is `claudecli` and you rotate the underlying `claude` login, the fire fails until you re-authenticate.
- The delivery target must belong to the daemon's allowlist. Rousseau will not deliver to an out-of-allowlist JID even if a scheduled job asks it to.
- The cron scheduler runs inside the `rousseau whatsapp` daemon by design. Running `rousseau slack` alongside gives you two independent schedulers reading the same table — jobs will fire twice. Pick one daemon to own the schedule.

## Next

- [Cron reference](/cron/) — every subcommand, every flag.
- [Skills](/skills/) — share prompt boilerplate across jobs.
- [Audit + approval policies](/guides/audit-approval-policies/) — lock down what the scheduled prompt can do.
