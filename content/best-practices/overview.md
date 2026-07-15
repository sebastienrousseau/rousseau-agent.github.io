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
description: "Index of rousseau best-practice guides: secrets, egress, sessions, approvals, multi-tenant, disaster recovery, cost."
keywords: "best practices, operations, security, cost, dr"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/best-practices/overview/"
subtitle: "The rousseau operator's playbook."
tags: "best-practices, operations"
title: "Best Practices Overview"

news_genres: "Blog"
news_keywords: "best practices, operations"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Best Practices Overview"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "best-practices"
order: 10
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/best-practices/overview/index.html"
item_link: "https://docs.rousseau-agent.dev/best-practices/overview/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Best Practices Overview"
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
twitter_description: "Index of rousseau best-practice guides."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Best Practices Overview"
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

Best-practice guides in rousseau distil the operational patterns we've watched hold up under real conditions: secrets that survive a rotation, egress rules that don't accidentally block your daemon, session stores that survive an outage, cost dashboards that catch prompt-loop bugs.

<aside class="admonition" data-type="tip"><span class="admonition-title">Read order</span><p>If you're new: start with <a href="/best-practices/secret-management/">Secret management</a> and <a href="/best-practices/approval-rules/">Approval rules</a>. If you're moving to production, add <a href="/best-practices/network-egress/">Network egress</a> and <a href="/best-practices/disaster-recovery/">Disaster recovery</a>.</p></aside>

## Guide index

| Guide | Audience |
|---|---|
| [Secret management](/best-practices/secret-management/) | Every operator |
| [Network egress](/best-practices/network-egress/) | Platform / security team |
| [Session hygiene](/best-practices/session-hygiene/) | Individual operators |
| [Approval rules](/best-practices/approval-rules/) | Everyone; distinct patterns per role |
| [Multi-tenant](/best-practices/multi-tenant/) | Platform teams |
| [Disaster recovery](/best-practices/disaster-recovery/) | SREs |
| [Cost control](/best-practices/cost-control/) | Finance / platform |

## First principles

- **Never store an API key in `config.yaml` unless the file is encrypted at rest and its permissions are `0600`.** Prefer env vars, `AWS_PROFILE`, `GOOGLE_APPLICATION_CREDENTIALS`, or a secrets manager.
- **Approve tools, not conversations.** The pattern-mode approver runs before every tool invocation. Prefer narrow allow-rules over broad ones.
- **Backup `sessions.db` before every upgrade.** It's a single SQLite file — `cp` is enough.
- **Deny by default.** `agent.approver.default: deny` with explicit allow rules is safer than `default: allow` with deny exceptions.
- **Log to journalctl, not `>logs/rousseau.log`.** systemd rotation is battle-tested.

## Related pages

- [Best Practices: Secret management](/best-practices/secret-management/)
- [Best Practices: Approval rules](/best-practices/approval-rules/)
- [Best Practices: Disaster recovery](/best-practices/disaster-recovery/)
- [Deployment](/deployment/)
- [Security](/security/)
