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
description: "One daemon per project vs shared: trade-offs, state isolation, blast radius, and cost accounting."
keywords: "multi-tenant, isolation, blast radius, per-project, best practices"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/best-practices/multi-tenant/"
subtitle: "One daemon per project vs one shared daemon."
tags: "best-practices, multi-tenant"
title: "Multi-Tenant Deployment"

news_genres: "Blog"
news_keywords: "multi-tenant, isolation"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Multi-Tenant Deployment"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "best-practices"
order: 15
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/best-practices/multi-tenant/index.html"
item_link: "https://docs.rousseau-agent.dev/best-practices/multi-tenant/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Multi-Tenant Deployment"
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
twitter_description: "One daemon per project vs shared: trade-offs, state isolation, blast radius, and cost accounting."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Multi-Tenant Deployment"
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

Rousseau's design makes one daemon per project the safest posture: distinct `state.path`, distinct `agent.skills_dir`, distinct provider credentials, distinct approval rules. But it's not the only option — a single daemon with multiple bind mounts also works if the trade-offs suit you.

## Options

<div class="tabs" data-tabs="mt-mode">
  <div class="tab-list" role="tablist" aria-label="Mode">
    <button role="tab" aria-selected="true">One daemon per project</button>
    <button role="tab" aria-selected="false">One shared daemon</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**Recommended for platform teams.**

Each project gets its own:

- Config file (`/etc/rousseau/projects/<slug>/config.yaml`).
- `state.path` under `/var/lib/rousseau/<slug>/`.
- Systemd unit (`rousseau-<slug>.service`).
- Provider credentials (env or LoadCredential).

Pros:

- Clean blast radius: one project's compromise does not touch another's session store.
- Per-project cost accounting: LLM spend maps cleanly.
- Independent restart cadence — upgrade one at a time.

Cons:

- More processes to monitor.
- More systemd units to templatise.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Fine for solo operators; risky for platform teams.**

One daemon, one config, one `state.path`, one workspace bind mount that contains every project.

Pros:

- Minimal footprint.
- One place to update the provider.

Cons:

- Every prompt sees every project. Approval rules must be very tight.
- Cost accounting is per-user, not per-project.
- Data-store nuking affects everyone.

  </div>
</div>

## Templatising with systemd

```ini
# /etc/systemd/system/rousseau-slack@.service
[Unit]
Description=Rousseau Slack bridge for %i
After=network-online.target

[Service]
User=rousseau
WorkingDirectory=/var/lib/rousseau/%i
EnvironmentFile=/etc/rousseau/projects/%i/secrets.env
ExecStart=/usr/local/bin/rousseau --config /etc/rousseau/projects/%i/config.yaml slack
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```sh
systemctl enable --now rousseau-slack@alpha.service
systemctl enable --now rousseau-slack@bravo.service
```

## Directory conventions

```text
/etc/rousseau/projects/<slug>/config.yaml
/etc/rousseau/projects/<slug>/secrets.env
/var/lib/rousseau/<slug>/sessions.db
/var/lib/rousseau/<slug>/whatsapp.db
```

## Verification

- [ ] `systemctl list-units 'rousseau-*.service'` shows one unit per project.
- [ ] `ls /var/lib/rousseau/*/sessions.db` shows one file per project, distinct sizes.
- [ ] A search in one project's `rousseau session search` does not return the other project's hits.

## Failure modes

- **Shared state.path** — the biggest mistake. Two units read/write the same DB; results are undefined. Enforce distinct paths in a smoke-test.
- **Skills bleed** — if you share `agent.skills_dir` across projects and one skill references project-specific paths, it will misfire.
- **Session store growth** — plan an rsync/backup rotation per project. See [Best Practices: Disaster recovery](/best-practices/disaster-recovery/).

## Related pages

- [Deployment](/deployment/)
- [Reference: Config: State](/reference/config/state/)
- [Best Practices: Disaster recovery](/best-practices/disaster-recovery/)
- [Best Practices: Cost control](/best-practices/cost-control/)
- [Recipes: Bedrock multi-account](/recipes/bedrock-multi-account/)
