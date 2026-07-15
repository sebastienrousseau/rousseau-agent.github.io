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
description: "Fifteen security questions answered: sandbox, supply chain, secrets, trust boundaries, disclosure."
keywords: "faq, security, supply chain, secrets, disclosure"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/faq/security/"
subtitle: "Security-related FAQ."
tags: "faq, security"
title: "FAQ: Security"

news_genres: "Blog"
news_keywords: "faq, security"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "FAQ: Security"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "faq"
order: 11
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/faq/security/index.html"
item_link: "https://docs.rousseau-agent.dev/faq/security/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "FAQ: Security"
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
twitter_description: "Fifteen security questions answered."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "FAQ: Security"
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

Fifteen questions about rousseau's security posture, supply chain, trust boundaries, and disclosure process.

<aside class="admonition" data-type="warning"><span class="admonition-title">Disclose privately</span><p>Do not open a public issue for a suspected vulnerability. Email <code>sebastian.rousseau@gmail.com</code> with details. Acknowledgement within 72 hours.</p></aside>

## Questions

### 1. Does rousseau run arbitrary shell commands?

Yes — via the built-in `bash` tool. Approval policies (`agent.approver.mode: pattern`) with a `default: deny` fallback are the primary defence. See [Best Practices: Approval rules](/best-practices/approval-rules/).

### 2. Is there a sandbox for the `bash` tool?

Not inside rousseau — the OS is the sandbox. The reference Podman quadlet drops all capabilities, sets `NoNewPrivileges=true`, applies seccomp, and runs as UID 1000. That's the security perimeter.

### 3. How are releases signed?

`cosign` (keyless, GitHub Actions OIDC) signs the checksums file. Verify with the incantation in the [Quickstart](/quickstart/#5-verify-supply-chain).

### 4. What's the SLSA level?

SLSA Level 3 via `slsa-framework/slsa-github-generator`. Every tagged release ships an `intoto.jsonl` provenance attestation.

### 5. Is there an SBOM?

Yes — CycloneDX 1.5, published per release as `rousseau_<v>_sbom.cdx.json`.

### 6. Are dependencies pinned?

Yes. `go.mod` uses exact versions; `go.sum` is frozen. `govulncheck` runs on every CI build and blocks known-vulnerable transitives.

### 7. Where do you store my API keys?

Nowhere by default. If you put them in `config.yaml`, they live wherever you save that file. Prefer env vars. See [Best Practices: Secret management](/best-practices/secret-management/).

### 8. Is the session store encrypted at rest?

No. SQLite files are not encrypted. If your host has full-disk encryption, that's your protection. Otherwise, restrict `state.path` to a mount with the encryption you need.

### 9. Does rousseau send my code to Anthropic / OpenAI / …?

Only the parts you or the agent choose to send in tool inputs or system-prompt context. Rousseau doesn't ship your entire workspace by default.

### 10. Does rousseau have a phone-home feature?

No. There is no telemetry, no crash reporter, no analytics.

### 11. What about the `claude` CLI subprocess?

The `claude` CLI has its own trust boundary — see Anthropic's docs. When you use `provider: claudecli`, rousseau shells out to `claude` and inherits its behaviour.

### 12. How do I audit what tools were called?

Every tool invocation logs a structured event. Look for `agent.tool.called` and `agent.tool.result` in the logs.

### 13. What's the fuzz coverage?

Every parser (whatsapp binary XML, signal JSON-RPC, MCP JSON-RPC, config YAML, cron expressions, tool schemas) has a Fuzz function. `make fuzz` runs the full battery.

### 14. Do you have a security policy?

Yes, [`SECURITY.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/SECURITY.md) in the source tree and mirrored at [Security](/security/).

### 15. What's the vulnerability disclosure timeline?

Acknowledgement within 72h. Reasonable time for a fix (aim: 30 days for high, 90 days for medium). Public disclosure after a fix is released.

## Related pages

- [Security](/security/)
- [FAQ: General](/faq/general/)
- [Best Practices: Secret management](/best-practices/secret-management/)
- [Best Practices: Approval rules](/best-practices/approval-rules/)
- [Best Practices: Network egress](/best-practices/network-egress/)
