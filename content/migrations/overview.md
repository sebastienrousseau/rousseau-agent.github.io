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
description: "Overview of every migration path: version upgrades, container migration, provider switching. Structure and downgrade discipline."
keywords: "migrations, upgrade, downgrade, container, provider"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/migrations/overview/"
subtitle: "Migration index and structure."
tags: "migrations, upgrade"
title: "Migrations Overview"

news_genres: "Blog"
news_keywords: "migrations, upgrade, downgrade"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Migrations Overview"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "migrations"
order: 10
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/migrations/overview/index.html"
item_link: "https://docs.rousseau-agent.dev/migrations/overview/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Migrations Overview"
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
twitter_description: "Overview of every migration path: version upgrades, container migration, provider switching. Structure and downgrade discipline."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Migrations Overview"
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

Migration guides in rousseau-agent cover three axes:

1. **Version upgrades** — moving between tagged releases.
2. **Deployment mode changes** — bare-metal to containerised, single-host to multi-host.
3. **Provider or transport swaps** — switching LLM backends or chat channels mid-project without losing conversation history.

Every migration guide follows the same structure so operators can skim to the section they need.

<aside class="admonition" data-type="tip"><span class="admonition-title">Pre-flight discipline</span><p>Before any migration: (1) back up <code>~/.local/share/rousseau/sessions.db</code>; (2) note the current version with <code>rousseau version</code>; (3) run <code>rousseau doctor</code> and save its output. See <a href="/best-practices/disaster-recovery/">Best Practices: Disaster recovery</a> for the full backup playbook.</p></aside>

## Guide structure

Each migration page contains, in order:

1. **What changed** — the concrete diff at the config / CLI / data-store level. Never a philosophical summary.
2. **Config diff** — a before/after YAML block. Copy-pastable.
3. **Data-store compatibility** — whether `sessions.db` opens as-is, requires a schema migration, or must be exported/reimported.
4. **Downgrade path** — the reverse recipe. Rousseau follows a "one release backward" downgrade promise; further back requires the sessions.db backup.
5. **Verification** — the commands that prove the migration succeeded (`rousseau doctor`, `rousseau session list`, `rousseau version`).

## Available guides

| Guide | When to read |
|---|---|
| [0.4 → 0.5](/migrations/0.4-to-0.5/) | Upgrading from an early single-transport release. |
| [0.5 → 0.6](/migrations/0.5-to-0.6/) | Upgrading to the current line-up of nine transports and five providers. |
| [Container migration](/migrations/container-migration/) | Moving from `go install` on bare metal to rootless Podman + systemd Quadlet. |
| [Provider migration](/migrations/provider-migration/) | Switching LLM backend without losing conversation history. |

## Versioning discipline

Rousseau uses semver: `MAJOR.MINOR.PATCH`.

- **PATCH** — bug fixes, no config-file changes, no data-store schema changes.
- **MINOR** — new fields with sensible defaults, additive tables. Backwards-compatible with a `PATCH` release. Downgrade allowed.
- **MAJOR** — renamed fields, removed subcommands, or a data-store migration. Requires reading the migration guide.

Every release ships:

- Signed checksums (`cosign verify-blob`).
- CycloneDX SBOM (`rousseau_<v>_sbom.cdx.json`).
- SLSA-3 provenance (`rousseau_<v>_provenance.intoto.jsonl`).

Verify the signature before any upgrade — see [Security](/security/) for the trust root.

## Change types you might encounter

<div class="tabs" data-tabs="mig-change">
  <div class="tab-list" role="tablist" aria-label="Change type">
    <button role="tab" aria-selected="true">Config renames</button>
    <button role="tab" aria-selected="false">CLI flags</button>
    <button role="tab" aria-selected="false">Schema migrations</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Old key deprecated but honoured for two MINOR releases with a `WARN`-level log message. New key wins if both present. Env-var counterparts follow the same policy.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

New flags are additive with defaults. Removed flags are only removed at MAJOR bumps and are documented in the migration guide with the replacement.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau runs schema migrations automatically at startup (`sqlitestore.Open` executes `PRAGMA user_version` checks and DDL). Downgrade requires either an older binary that understands the newer schema (rare) or a restore from backup.

  </div>
</div>

## Related pages

- [Migrations: 0.4 → 0.5](/migrations/0.4-to-0.5/)
- [Migrations: 0.5 → 0.6](/migrations/0.5-to-0.6/)
- [Migrations: Container migration](/migrations/container-migration/)
- [Migrations: Provider migration](/migrations/provider-migration/)
- [Best Practices: Disaster recovery](/best-practices/disaster-recovery/)
- [Changelog](/changelog/)
