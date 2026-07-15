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
description: "Twenty of the most-asked general questions about rousseau-agent: what it is, what it isn't, how it compares, how to run it."
keywords: "faq, general, questions, rousseau"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/faq/general/"
subtitle: "General frequently-asked questions."
tags: "faq, general"
title: "FAQ: General"

news_genres: "Blog"
news_keywords: "faq, general"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "FAQ: General"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "faq"
order: 10
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/faq/general/index.html"
item_link: "https://docs.rousseau-agent.dev/faq/general/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "FAQ: General"
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
twitter_description: "Twenty of the most-asked general questions about rousseau-agent."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "FAQ: General"
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

Twenty of the most-asked general questions about rousseau-agent. See also [FAQ: Security](/faq/security/), [FAQ: Providers](/faq/providers/), [FAQ: Transports](/faq/transports/).

<aside class="admonition" data-type="tip"><span class="admonition-title">Search first</span><p>Use the docs search or <code>rousseau session search</code> against your own history before asking. Half the time, the answer is one Ctrl+K away.</p></aside>

## Questions

### 1. What is rousseau-agent?

A self-hosted coding assistant that runs as a single static Go binary. It ships a Bubble Tea TUI, a SQLite session store, nine chat transports, five LLM providers, an MCP server, and a cron scheduler.

### 2. What isn't it?

- Not a SaaS product.
- Not a wrapper around a hosted broker.
- Not a chatbot framework — the agent loop, tool registry, and approver are load-bearing.

### 3. Who is it for?

Operators who need the workspace, auth material, and model traffic to stay on a machine they control. Regulated environments, airgapped shops, individual operators who want IDE-optional coding.

### 4. Do I need a Kubernetes cluster?

No. The reference deployment is rootless Podman + a systemd Quadlet unit on a single host. There's a Deployment shape for Kubernetes if you want it, but there's no operator or CRD.

### 5. What LLM does it use?

Any of five backends: `claudecli` (default, inherits Claude Code auth), `anthropic`, `bedrock`, `vertex`, or an OpenAI-compatible endpoint (`openai`, `openrouter`, `ollama`).

### 6. Does it require an API key?

Not with the default `claudecli` provider — that inherits your local `claude` CLI's OAuth. For the other providers, yes: an API key or cloud credential.

### 7. What OSes are supported?

Rousseau runs natively on macOS, Linux, and Windows. The Podman reference deployment is Linux-first; on Windows use WSL 2.

### 8. Does it phone home?

No. There is no telemetry endpoint, no license server, no crash reporter. `govulncheck` at build time is the closest thing.

### 9. How do I install it?

Three paths: `go install`, from source (`make build`), or a signed release archive. See [Quickstart](/quickstart/#1-install-rousseau).

### 10. Where's the config file?

`~/.config/rousseau/config.yaml` by default. Override with `--config` or `XDG_CONFIG_HOME`.

### 11. Where's the state stored?

`~/.local/share/rousseau/sessions.db` (SQLite). WhatsApp pairing lives in `whatsapp.db` next to it.

### 12. Can I run more than one transport at once?

Yes. Each transport is a separate subcommand — run them under separate systemd units, they all share the session store. WhatsApp and Slack can run in parallel.

### 13. Does it support voice notes?

WhatsApp only, via optional whisper.cpp integration. Set `whatsapp.voice.enabled: true` and install `whisper`.

### 14. How does the session store work?

SQLite with WAL. Every message is persisted immediately. Cross-session recall uses SQLite FTS5. See [Reference: Session store](/reference/session-store/).

### 15. Can I embed the agent loop as a library?

Yes. `agent.New(provider, registry, logger, opts).Turn(ctx, session)` is stable. See the embedding example in `examples/embed-agent`.

### 16. How do I upgrade?

For minor releases: `go install …@vX.Y.Z` or replace the binary with a signed release. See [Migrations: Overview](/migrations/overview/).

### 17. How do I downgrade?

Reinstall the previous version. If the new schema was written, restore `sessions.db` from backup.

### 18. Is there a UI?

The Bubble Tea TUI (`rousseau chat`) and the transports themselves. There's no web dashboard.

### 19. Where do I ask questions?

[GitHub Discussions](https://github.com/sebastienrousseau/rousseau-agent/discussions).

### 20. How do I report a bug?

[GitHub Issues](https://github.com/sebastienrousseau/rousseau-agent/issues) with `rousseau version` + `rousseau doctor` output.

## Related pages

- [FAQ: Security](/faq/security/)
- [FAQ: Providers](/faq/providers/)
- [FAQ: Transports](/faq/transports/)
- [Quickstart](/quickstart/)
- [Community: Contributing](/community/contributing/)
