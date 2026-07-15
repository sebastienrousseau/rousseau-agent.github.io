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
description: "Complete reference for rousseau email: IMAP inbound + SMTP outbound, poll interval, mailbox, exit codes."
keywords: "email, imap, smtp, poll interval, cli reference, rousseau email"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/commands/email/"
subtitle: "Complete reference for `rousseau email`."
tags: "reference, cli, email, transports"
title: "rousseau email"

news_genres: "Blog"
news_keywords: "email, imap, smtp"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "rousseau email"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 67
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/commands/email/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/commands/email/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "rousseau email"
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
twitter_description: "Complete reference for rousseau email: IMAP inbound + SMTP outbound, poll interval, mailbox, exit codes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "rousseau email"
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

`rousseau email` runs the email bridge: IMAP for inbound polling, SMTP for outbound sending. It polls `INBOX` (or another mailbox) for `UNSEEN` messages, routes each into the agent, and sends the reply via SMTP. Both connections use TLS. IMAP IDLE is not yet supported — set `poll_interval` accordingly.

Source: `internal/cli/email.go`. Transport: `internal/transport/email/`.

<aside class="admonition" data-type="caution"><span class="admonition-title">STARTTLS not supported</span><p>Rousseau requires direct TLS on both IMAP (port 993) and SMTP (port 465 or 587 with implicit TLS). STARTTLS-only servers do not currently work.</p></aside>

## Synopsis

```sh
rousseau email [--imap-addr host:port] [--imap-username u] [--imap-password p] \
               [--smtp-addr host:port] [--smtp-username u] [--smtp-password p] \
               [--from addr] [--mailbox INBOX] [--poll-interval 30s]
```

## Flags

| Flag | Type | Default | Effect |
|---|---|---|---|
| `--imap-addr` | string | `email.imap_addr` | IMAP `host:port`. |
| `--imap-username` | string | `email.imap_username` | IMAP username. |
| `--imap-password` | string | `email.imap_password` | IMAP password. Prefer env vars. |
| `--smtp-addr` | string | `email.smtp_addr` | SMTP `host:port`. |
| `--smtp-username` | string | `email.smtp_username` | SMTP username. |
| `--smtp-password` | string | `email.smtp_password` | SMTP password. Prefer env vars. |
| `--from` | string | `email.from` | `From:` address. |
| `--mailbox` | string | `email.mailbox` (defaults to `INBOX`) | IMAP mailbox to poll. |
| `--poll-interval` | duration string | `email.poll_interval` (built-in default `30s`) | Poll cadence. |

## Config keys respected

`internal/config/config.go` `EmailConfig`:

| Key | Type | Default | Effect |
|---|---|---|---|
| `email.imap_addr` | string | empty | Required. |
| `email.imap_username` | string | empty | Required. |
| `email.imap_password` | string | empty | Required. |
| `email.smtp_addr` | string | empty | Required. |
| `email.smtp_username` | string | empty | Required. |
| `email.smtp_password` | string | empty | Required. |
| `email.from` | string | empty | Required. |
| `email.mailbox` | string | `INBOX` | Polled mailbox. |
| `email.poll_interval` | duration | `30s` | Cadence. |
| `email.reply_header` | string | empty | Prefix on outbound messages. |

## Allowlist syntax

Email has no `--allow` flag — the whole point of the `From:`/`Reply-To:` model is that anyone can send. Filtering happens at the mail-server side (postfix ACLs, Gmail filters, etc.), not in the router.

## Environment variables

| Variable | Effect |
|---|---|
| `ROUSSEAU_EMAIL_IMAP_ADDR` | Override IMAP address. |
| `ROUSSEAU_EMAIL_IMAP_USERNAME` | Override IMAP username. |
| `ROUSSEAU_EMAIL_IMAP_PASSWORD` | Override IMAP password. |
| `ROUSSEAU_EMAIL_SMTP_ADDR` | Override SMTP address. |
| `ROUSSEAU_EMAIL_SMTP_USERNAME` | Override SMTP username. |
| `ROUSSEAU_EMAIL_SMTP_PASSWORD` | Override SMTP password. |
| `ROUSSEAU_EMAIL_FROM` | Override From address. |

## Startup sequence

1. Validate IMAP and SMTP settings; fail if any required field is empty.
2. Default `claudecli.permission_mode` to `bypassPermissions`.
3. Parse `poll_interval` duration.
4. Open session store, build agent wiring.
5. `email.New` — instantiate the transport.
6. `wiring.startCron` — cron delivery via SMTP.
7. IMAP poll loop until context cancelled.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Clean context cancellation. |
| 1 | Missing IMAP/SMTP settings, invalid duration, TLS failure, provider/store error. |
| 130 | SIGINT. |

## Worked examples

```sh
# Gmail app password + implicit TLS
rousseau email \
  --imap-addr imap.gmail.com:993 \
  --imap-username bot@example.com \
  --imap-password "$IMAP_APP_PW" \
  --smtp-addr smtp.gmail.com:465 \
  --smtp-username bot@example.com \
  --smtp-password "$SMTP_APP_PW" \
  --from bot@example.com

# From config, poll every 2 minutes
cat > ~/.config/rousseau/config.yaml <<'EOF'
email:
  imap_addr: imap.example.com:993
  imap_username: bot@example.com
  imap_password: "$IMAP_APP_PW"
  smtp_addr: smtp.example.com:465
  smtp_username: bot@example.com
  smtp_password: "$SMTP_APP_PW"
  from: bot@example.com
  mailbox: INBOX
  poll_interval: 2m
EOF
rousseau email
```

## Common failure modes

- **`AUTHENTICATIONFAILED`** — bad IMAP credentials or missing app-password (Gmail, Outlook require app-passwords).
- **`STARTTLS is not supported`** — the server offers only STARTTLS; not implemented.
- **Duplicate replies** — the bot is not marking messages read; verify mail is flagged `SEEN` after processing.
- **SMTP `550 5.7.1 relay denied`** — SMTP host requires authenticated SMTP; verify username/password.

## Related pages

- [Transports: Email](/transports/email/)
- [Recipes: Email triage](/recipes/email-triage/)
- [Best Practices: Secret management](/best-practices/secret-management/)
- [Reference: Logs](/reference/logs/)
