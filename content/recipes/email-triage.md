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
description: "Automated email triage with rousseau: IMAP inbound, agent inspection, SMTP reply. Runs behind a mail server you control."
keywords: "email, imap, smtp, triage, dedicated mailbox, recipes"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/recipes/email-triage/"
subtitle: "Automated email triage over IMAP + SMTP."
tags: "recipes, email"
title: "Recipe: Email Triage"

news_genres: "Blog"
news_keywords: "email, imap, smtp, triage"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Recipe: Email Triage"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "recipes"
order: 13
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/recipes/email-triage/index.html"
item_link: "https://docs.rousseau-agent.dev/recipes/email-triage/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Recipe: Email Triage"
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
twitter_description: "Automated email triage with rousseau: IMAP inbound, agent inspection, SMTP reply."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Recipe: Email Triage"
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

Point rousseau at a dedicated mailbox (`triage@example.com`). Every inbound message becomes a rousseau session; the agent inspects attached logs / patches / stack traces and replies via SMTP. Ideal for a low-volume support inbox where every message deserves a first-pass response.

## Prerequisites

- A dedicated mailbox with IMAP (port 993, TLS) and SMTP (port 465 with implicit TLS, or 587 with STARTTLS — currently 465).
- App-passwords for Gmail / Outlook, or a plain password for self-hosted Postfix + Dovecot.
- Any provider — `anthropic` recommended because prompt-cache markers cut cost on long email threads.

<aside class="admonition" data-type="caution"><span class="admonition-title">Reputation</span><p>Sending from a rousseau-hosted mailbox to unknown recipients can hurt your domain's reputation. Configure SPF, DKIM, DMARC before pointing this at a customer-facing address.</p></aside>

## Config

```yaml
provider: anthropic

anthropic:
  model: claude-sonnet-4-6
  max_tokens: 4096

agent:
  system_prompt: |
    You reply to inbound support email. Keep replies under 300 words.
    If the request needs human judgment (billing, security, legal),
    say so explicitly and set an "escalate: yes" flag at the top.
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
    deny:
      - {tool: bash, match: ".*"}

email:
  imap_addr: imap.example.com:993
  imap_username: triage@example.com
  imap_password: "$IMAP_PW"
  smtp_addr: smtp.example.com:465
  smtp_username: triage@example.com
  smtp_password: "$SMTP_PW"
  from: triage@example.com
  mailbox: INBOX
  poll_interval: 60s
  reply_header: ""
```

`bash` is denied outright — email triage should never spawn shells.

## Launch

```sh
export IMAP_PW='…' SMTP_PW='…' ANTHROPIC_API_KEY='sk-ant-…'
rousseau email
```

For production, wrap under systemd like the [on-call Slack triage](/recipes/oncall-slack-triage/#systemd-unit-bare-metal) recipe.

## Verification

- [ ] `rousseau doctor` reports the provider as `anthropic` with the key present (masked).
- [ ] Send an email to `triage@example.com` from another account.
- [ ] Within `poll_interval` seconds, a reply arrives from `triage@example.com`.
- [ ] The IMAP mailbox marks the source message as SEEN (verify via a mail client).

## Failure modes

- **Duplicate replies** — rousseau is not marking messages read. Verify with `rousseau doctor` and IMAP debug logs. Some servers require explicit UID flags.
- **Bounced replies** — SPF / DKIM misconfigured. Sending from `triage@example.com` requires the domain to authorise your SMTP host.
- **Empty replies** — the agent has nothing to say. Look at the source message; short pings ("thanks") should be dropped by a filter, not answered.

## Related pages

- [Reference: Commands: email](/reference/commands/email/)
- [Transports: Email](/transports/email/)
- [Providers: Anthropic](/providers/anthropic/)
- [Best Practices: Cost control](/best-practices/cost-control/)
