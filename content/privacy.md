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
description: "rousseau-agent is self-hosted. No telemetry endpoint, no SaaS control plane. LLM providers have their own retention policies; everything else stays in the operator's infrastructure."
keywords: "privacy, telemetry, self-hosted, data handling, retention, LLM providers"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/privacy/"
subtitle: "Self-hosted means self-controlled — nothing leaves your infrastructure except the LLM call."
tags: "privacy, legal, self-hosted"
title: "Privacy"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "privacy, telemetry, self-hosted, data handling, retention, LLM providers"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Privacy"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "legal"
order: 30
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/privacy/index.html"
item_link: "https://docs.rousseau-agent.dev/privacy/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Privacy"
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
twitter_description: "rousseau-agent is self-hosted. No telemetry endpoint, no SaaS control plane. LLM providers have their own retention policies; everything else stays in the operator's infrastructure."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Privacy"
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

## Data handling

`rousseau-agent` is self-hosted. When the operator runs the daemon on their own infrastructure, **no data leaves that infrastructure except the LLM call itself**.

There is:

- **No telemetry endpoint.** rousseau makes no calls to `rousseau-agent.dev` or any other author-controlled server at runtime.
- **No SaaS control plane.** There is no license server, no cloud dashboard, no phone-home.
- **No usage analytics.** The daemon does not report which tools were invoked, how many turns ran, or what models were called.
- **No crash reporting.** Crashes surface in local logs (`journalctl --user -u rousseau-agent.service`). No stack traces are shipped anywhere.

## Where session data lives

| Data | Location | Encryption at rest |
|---|---|---|
| Sessions (message history) | `~/.local/share/rousseau/sessions.db` | Filesystem-level only (LUKS / FileVault if the operator configured it). |
| Cron jobs | Same SQLite database | Same. |
| WhatsApp device pairing | `~/.local/share/rousseau/whatsapp.db` | Same. |
| Log output | systemd journal (typically `~/.local/state/`) | Same. |
| Config file | `~/.config/rousseau/config.yaml` | Same. |
| `claude` CLI OAuth tokens | `~/.claude/` | Same. |

None of these are transmitted anywhere by the daemon.

## LLM providers

The LLM provider is the one external touchpoint. Every provider has its own data-handling and retention policy — none of which rousseau controls:

| Provider | Retention policy |
|---|---|
| [claudecli](/providers/claudecli/) | Whatever the local `claude` CLI is configured to send. Typically Anthropic's standard retention. |
| [Anthropic direct](/providers/anthropic/) | See https://www.anthropic.com/legal/aup |
| [AWS Bedrock](/providers/bedrock/) | Contract-defined; typically no long-term retention for inference traffic on Bedrock. |
| [Google Vertex AI](/providers/vertex/) | Contract-defined; typically no long-term retention for Vertex inference. |
| [OpenAI-compatible](/providers/openai-compatible/) | Depends on the endpoint. Ollama and self-hosted vLLM retain nothing external; OpenAI and OpenRouter have their own policies. |

Choose the provider whose retention policy matches your operational requirements. For the strictest posture, run against a self-hosted Ollama, vLLM, or LM Studio — no data leaves your infrastructure.

## Transport-side data

Chat transports send messages through the vendor's servers (WhatsApp, Signal, Slack, Discord, etc). Each has its own data-handling posture. rousseau does not add a layer on top of them — the vendor sees whatever the underlying protocol shows them, which is protocol-specific:

- Signal and WhatsApp: end-to-end encrypted; the vendor sees metadata but not message content.
- Slack, Discord: not end-to-end encrypted; the vendor sees message content.
- Matrix: end-to-end encrypted when the room is E2E-enabled; server-side otherwise.
- Email: not end-to-end encrypted unless you layer PGP or S/MIME on top (rousseau does not).
- iMessage: end-to-end encrypted; BlueBubbles sits between rousseau and Apple.

## Deleting a session

Sessions are rows in a SQLite database. Delete with:

```sh
rousseau session delete <session-id>
```

Or drop the entire database:

```sh
rm ~/.local/share/rousseau/sessions.db
```

The next startup will re-create an empty one. This also purges the FTS5 cross-session recall index.

## Third-party dependencies

`go.mod` lists every dependency. None of them are configured to phone home. Build-time dependencies (linters, static analysers) run in CI only. Runtime dependencies are enumerated in the CycloneDX SBOM attached to every release.
