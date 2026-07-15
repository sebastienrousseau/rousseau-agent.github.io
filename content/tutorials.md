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
description: "Full end-to-end walkthroughs: code-review bot, nightly changelog, VPS deployment, MCP integration, and approver hardening."
keywords: "tutorials, code review bot, changelog, vps deployment, mcp, approval policy"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/tutorials/"
subtitle: "Full end-to-end walkthroughs that put the pieces together."
tags: "tutorials, walkthrough, code review, changelog, deployment, mcp"
title: "Tutorials"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tutorials, code review bot, changelog, vps deployment, mcp, approval policy"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorials"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorials"
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
twitter_description: "Full end-to-end walkthroughs: code-review bot, nightly changelog, VPS deployment, MCP integration, and approver hardening."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorials"
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

## What tutorials are for

Guides answer a single "how do I…" question in isolation. Tutorials go the other way: they take a complete real-world scenario and walk you through every rousseau piece needed to ship it. Every tutorial produces something you could paste into your own workspace and expect to work.

| Tutorial | You end up with |
|---|---|
| [Build a code-review bot](/tutorials/build-a-code-review-bot/) | A Slack channel where mentioning `@rousseau` on a repo path triggers a `read` + `grep` review pass. |
| [Nightly changelog](/tutorials/nightly-changelog/) | A cron job that summarises the day's `git log` and pushes it to WhatsApp at 18:00. |
| [Deploy to a VPS](/tutorials/deploy-to-a-vps/) | A hardened rootless-Podman deployment on a fresh VPS behind systemd. |
| [Expose tools via MCP](/tutorials/expose-tools-via-mcp/) | Claude Desktop driving `rousseau_search_sessions`, `rousseau_list_sessions`, `rousseau_read_session`, `rousseau_cron_list`. |
| [Harden the approver](/tutorials/harden-approver-policy/) | A strict `pattern`-mode approver with `default: deny`, validated by the slog audit trail. |

## Prerequisites

Every tutorial assumes you have completed the [Quickstart](/quickstart/): `rousseau` is on `$PATH`, a provider is configured, and `rousseau chat` produces a response.

Beyond that, individual tutorials call out anything extra — a Slack workspace, a VPS, a WhatsApp-linked number, or `claude` desktop.

## Not a tutorial

If you want a short "how do I do X" recipe, read [Guides](/guides/). If you want the exact CLI flag or config field, jump to [Reference](/reference/cli-commands/). If you want to understand what a piece of rousseau does before wiring it up, start with [Concepts](/concepts/).
