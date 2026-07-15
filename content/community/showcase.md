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
description: "A placeholder for real rousseau-agent deployments across on-call, community bots, code review, and airgapped operators."
keywords: "showcase, deployments, users, community"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/community/showcase/"
subtitle: "Real deployments."
tags: "community, showcase"
title: "Showcase"

news_genres: "Blog"
news_keywords: "showcase, deployments"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Showcase"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "community"
order: 11
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/community/showcase/index.html"
item_link: "https://docs.rousseau-agent.dev/community/showcase/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Showcase"
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
twitter_description: "A placeholder for real rousseau-agent deployments."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Showcase"
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

This is a curated list of real rousseau-agent deployments. It exists so newcomers can see representative shapes: solo operators, small teams, community bots, and airgapped shops.

<aside class="admonition" data-type="tip"><span class="admonition-title">Add yours</span><p>Open a PR against <code>content/community/showcase.md</code> with a short paragraph. See <a href="/community/contributing/">Contributing</a>. Anonymity is fine — say "a fintech in the EU" rather than a company name if that's easier.</p></aside>

## Deployment shapes we know exist

<div class="tabs" data-tabs="showcase-shape">
  <div class="tab-list" role="tablist" aria-label="Shape">
    <button role="tab" aria-selected="true">Solo operator</button>
    <button role="tab" aria-selected="false">Small team</button>
    <button role="tab" aria-selected="false">Community bot</button>
    <button role="tab" aria-selected="false">Airgapped</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**One developer, one workstation.** WhatsApp transport pointed at their own number. `claudecli` inheriting Claude Code auth. Uses `rousseau chat` at the desk, WhatsApp on the go. Cron jobs for nightly git summaries. Session store on the local disk, backed up nightly.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**5–10 engineers, one shared daemon per project.** Slack Socket Mode in an on-call channel, Discord in a community channel, WhatsApp for individual pair-programming sessions. Provider: Bedrock via a scoped AWS profile per project. Rootless Podman under systemd Quadlet.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Public Discord server for an OSS project.** Answers doc questions with citations. Provider: `anthropic` with prompt-cache markers. `agent.approver.mode: pattern` with only `read`/`grep`. Cost is a rounding error thanks to caching.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**A regulated shop with strict egress rules.** No calls leave the internal network. Provider: `ollama` on an internal GPU box, `llama3.1:70b-instruct`. Transport: self-hosted Matrix (Synapse). No public WebSocket transports. Tool-use quality noticeably lower than Anthropic but acceptable for their workflow.

  </div>
</div>

## Wanted

If you're running rousseau in production and want to be added, we specifically want to hear:

- Your provider + transport combination.
- Rough scale (messages/day, sessions/week).
- Whether you're on bare-metal, Podman, Kubernetes, or something else.
- One thing that surprised you (good or bad).

Open a PR with a short markdown block; no company logos, no marketing copy.

## Related pages

- [Community: Contributing](/community/contributing/)
- [Community: Overview](/community/overview/)
- [Recipes](/recipes/overview/) — the recipe catalogue mirrors what showcased users are doing.
- [Deployment](/deployment/)
