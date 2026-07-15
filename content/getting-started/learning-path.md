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
description: "Recommended reading order for new rousseau-agent users, split by role: individual developer, platform operator, security reviewer."
keywords: "learning path, reading order, docs guide, individual developer, platform operator, security reviewer"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/getting-started/learning-path/"
subtitle: "What to read first, split by role."
tags: "learning-path, reading-order"
title: "Learning Path"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "learning path, reading order, docs guide, individual developer, platform operator, security reviewer"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Learning Path"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 22
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/learning-path/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/learning-path/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Learning Path"
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
twitter_description: "Recommended reading order for new rousseau-agent users, split by role: individual developer, platform operator, security reviewer."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Learning Path"
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

## Pick your role

Rousseau's audience splits cleanly along three axes. Pick the one that matches your goal and read in order — every path assumes the previous section has been absorbed.

## Individual developer

You want a coding assistant on your own laptop that persists sessions and drives your existing `claude` CLI. No team, no shared deployment.

| # | Page | Why |
|---|---|---|
| 1 | [Getting Started](/getting-started/) | Install, `rousseau chat`, first-run walkthrough. |
| 2 | [Concepts](/concepts/) | Understand the agent loop and the session store before you customise anything. |
| 3 | [User Guide: CLI](/user-guide/cli/) | Every command, every flag. |
| 4 | [User Guide: TUI](/user-guide/tui/) | Keybindings and panel semantics. |
| 5 | [User Guide: Tools](/user-guide/tools/) | What the five built-in tools do and don't. |
| 6 | [Configuration](/configuration/) | Tune the pieces you touched. |
| 7 | [Skills](/skills/) | Author reusable prompt fragments. |

Skip everything under [Developer Guide](/developer-guide/) unless you plan to embed the agent loop in another binary.

## Platform operator

You are running rousseau for a team behind a corporate perimeter. Uptime, auditability, and least-privilege posture are load-bearing.

| # | Page | Why |
|---|---|---|
| 1 | [Getting Started](/getting-started/) | Install and smoke-test. |
| 2 | [Platform Support](/getting-started/platform-support/) | Confirm every dependency version. |
| 3 | [Concepts](/concepts/) | Layered architecture — what you can trust to stay stable across releases. |
| 4 | [Deployment](/deployment/) | Rootless Podman + Quadlet. Kubernetes note. |
| 5 | [Guides: Kubernetes Deployment](/guides/kubernetes-deployment/) | If Kubernetes is your target. |
| 6 | [Configuration](/configuration/) + [Reference: Config Schema](/reference/config-schema/) | Every knob, structured. |
| 7 | [User Guide: Approval Policies](/user-guide/approval-policies/) | The tool-call approval story you present to auditors. |
| 8 | [Guides: Observability](/guides/observability/) | Wire slog output into your log pipeline. |
| 9 | [Guides: Audit + Approval Policies](/guides/audit-approval-policies/) | Worked pattern-mode config with deny rules. |
| 10 | [Updating](/getting-started/updating/) | Move between versions safely. |

## Security reviewer

You are vetting rousseau before rollout, or answering a supplier-questionnaire on your team's behalf.

| # | Page | Why |
|---|---|---|
| 1 | [Security](/security/) | Trust model, supply-chain posture, cryptography inventory. |
| 2 | [Installation](/getting-started/installation/) | cosign + SHA-256 verification recipe. |
| 3 | [Concepts](/concepts/) | Layered architecture — where the trust boundaries live. |
| 4 | [User Guide: Approval Policies](/user-guide/approval-policies/) | The lever between the model and the shell. |
| 5 | [Guides: Read-only Mode](/guides/read-only-mode/) | Posture for a first-pass inspection deployment. |
| 6 | [Reference: Exit Codes](/reference/exit-codes/) | Failure modes surfaced to init systems and monitors. |
| 7 | [Privacy](/privacy/) | Data-flow posture. |
| 8 | [Deployment](/deployment/) | Runtime hardening — Podman flags, capability drops, seccomp. |

## Cross-cutting reading

Every reader benefits from these once they have picked a role:

- [Troubleshooting](/troubleshooting/) — every diagnostic you can reach with `rousseau doctor`.
- [Changelog](/changelog/) — what moved between releases.
- [MCP](/mcp/) — how rousseau exposes tools and sessions to other agents.
- [Cron](/cron/) — schedule prompt-on-a-clock.

## Next

- [Platform Support](/getting-started/platform-support/) — what runs where.
- [First transport](/getting-started/first-transport/) — worked WhatsApp walkthrough.
