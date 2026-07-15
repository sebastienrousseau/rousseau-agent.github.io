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
description: "Weekly security audit that runs govulncheck, npm audit, and secret-scanning across a workspace and delivers the digest to a Signal chat."
keywords: "security, audit, cron, govulncheck, signal, weekly digest, recipes"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/recipes/security-audit-cron/"
subtitle: "Weekly security audit delivered over Signal."
tags: "recipes, security, cron, signal"
title: "Recipe: Weekly Security Audit"

news_genres: "Blog"
news_keywords: "security, audit, cron, signal"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Recipe: Weekly Security Audit"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "recipes"
order: 15
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/recipes/security-audit-cron/index.html"
item_link: "https://docs.rousseau-agent.dev/recipes/security-audit-cron/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Recipe: Weekly Security Audit"
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
twitter_description: "Weekly security audit delivered over Signal."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Recipe: Weekly Security Audit"
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

Once a week at Sunday 07:00 UK, rousseau runs `govulncheck`, `npm audit`, and a `grep` pass for common secret patterns across every repository under the workspace mount. It produces a digest and delivers it as a Signal message. Signal is chosen because the audit report should stay end-to-end encrypted in transit.

## Prerequisites

- Signal transport working (`rousseau signal --account +…` completes handshake).
- `govulncheck` and `npm` installed in the container image.
- A workspace mount containing your repos.

## Config

```yaml
provider: claudecli

agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^(govulncheck ./...|npm audit --json|rg --hidden -e 'AWS_SECRET_ACCESS_KEY|-----BEGIN [A-Z]+ PRIVATE KEY-----|sk-[a-zA-Z0-9-]+' /workspace)"}
    deny:
      - {tool: bash, match: "rm |sudo|git push"}

signal:
  account: "+447900123456"
  allowlist:
    - "+447900222222"
```

The `bash` allow list is deliberately narrow — the exact commands the audit needs, no more.

## Register the cron job

```sh
rousseau cron add \
  --name weekly-security-audit \
  --schedule '0 7 * * SUN' \
  --prompt 'For every repo under /workspace: (1) run govulncheck if it is a Go module, (2) run npm audit --json if package.json exists, (3) rg for common secret patterns. Summarise: total findings, top 5 by severity, any secret hits (with file:line). Under 1500 chars.' \
  --deliver-to '+447900123456'

rousseau cron list
```

## Launch

```sh
rousseau signal --account +447900123456 --allow +447900222222
```

The scheduler starts inside the signal daemon.

## Verification

- [ ] Trigger the prompt manually via `rousseau chat` and confirm the tool calls run in the expected order.
- [ ] Wait for the next Sunday fire, or temporarily set `--schedule '*/5 * * * *'` to smoke-test.
- [ ] A Signal message lands at `+447900222222`.

## Failure modes

- **`govulncheck: command not found`** — install `go install golang.org/x/vuln/cmd/govulncheck@latest` inside the container image.
- **`npm audit` slow or hangs on private registries** — pin the registry URL with `npm config set registry` in the image build.
- **False positives in secret grep** — refine the regex to your project's key formats, and consider `truffleHog` as a heavier alternative.

## Related pages

- [Reference: Commands: signal](/reference/commands/signal/)
- [Reference: Commands: cron](/reference/commands/cron/)
- [Best Practices: Secret management](/best-practices/secret-management/)
- [Security](/security/)
