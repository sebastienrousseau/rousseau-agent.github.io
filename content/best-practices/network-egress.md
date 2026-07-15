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
description: "Lock down rousseau's outbound traffic with nftables and a hardened Podman quadlet: only the LLM endpoint and enabled transports."
keywords: "nftables, firewall, egress, podman, quadlet, best practices"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/best-practices/network-egress/"
subtitle: "nftables + Podman for locked-down egress."
tags: "best-practices, security, network"
title: "Network Egress"

news_genres: "Blog"
news_keywords: "nftables, firewall, egress"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Network Egress"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "best-practices"
order: 12
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/best-practices/network-egress/index.html"
item_link: "https://docs.rousseau-agent.dev/best-practices/network-egress/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Network Egress"
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
twitter_description: "Lock down rousseau's outbound traffic with nftables and a hardened Podman quadlet."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Network Egress"
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

Rousseau exposes zero inbound HTTP surface. All traffic is outbound: LLM calls, transport WebSockets, cron scheduler side effects. This guide walks through the egress-only firewall posture we recommend for production, using nftables on the host and Podman `Network=pasta` inside the container.

<aside class="admonition" data-type="tip"><span class="admonition-title">Reference nft ships in-tree</span><p>The rousseau-agent repo ships an example ruleset at <code>docker/nftables.example.nft</code>. Adapt to your provider/transport mix.</p></aside>

## Domains rousseau might reach

| Purpose | Endpoint |
|---|---|
| Anthropic | `api.anthropic.com` |
| AWS Bedrock | `bedrock-runtime.<region>.amazonaws.com`, STS |
| GCP Vertex | `<region>-aiplatform.googleapis.com`, IAM |
| OpenAI-compatible | as configured (`openai.base_url`) |
| Ollama | `localhost:11434` |
| WhatsApp | `web.whatsapp.com` and `mmg.whatsapp.net` |
| Signal | signal.org services (via `signal-cli`) |
| Telegram | `api.telegram.org` |
| Matrix | your homeserver |
| Slack | `slack.com`, `wss.slack.com` |
| Discord | `discord.com`, `gateway.discord.gg` |
| Email | your IMAP + SMTP hosts |
| Cosign / SLSA / govulncheck (if run inside) | Sigstore, GitHub, Go proxy |

Anything not in this list should be blocked.

## nftables ruleset (host)

```text
table inet rousseau {
  chain output {
    type filter hook output priority 0; policy drop;

    # Loopback + established
    oifname lo accept
    ct state established,related accept

    # DNS to internal resolver only
    ip daddr 10.42.0.1 udp dport 53 accept
    ip daddr 10.42.0.1 tcp dport 53 accept

    # Anthropic (adjust to Bedrock / Vertex / self-hosted)
    ip daddr { 160.79.104.0/23 } tcp dport 443 accept

    # Slack Socket Mode WebSocket
    ip daddr { slack-ip-set } tcp dport 443 accept

    # Log-and-drop everything else
    log prefix "[rousseau blocked] " counter drop
  }
}
```

Verify with `sudo nft list ruleset`.

## Podman quadlet posture

The reference `docker/rousseau-agent.container` unit uses `Network=pasta` (rootless), no `PublishPort=`. From inside the container:

```sh
podman exec rousseau-agent ss -tulwn
# expect: no LISTEN sockets
```

## Verification

- [ ] `curl -m 3 https://api.anthropic.com` succeeds from the daemon host.
- [ ] `curl -m 3 https://example.com` fails / times out.
- [ ] `ss -tulwn` inside the container shows no LISTEN sockets.
- [ ] `nft list ruleset` shows the rousseau table active.

## Common pitfalls

- **DNS leaks**: the container inherits `/etc/resolv.conf`. Point at an internal resolver, or use CoreDNS with a custom zone.
- **cosign `verify-blob` fails during upgrade**: the Sigstore endpoints (`rekor.sigstore.dev`, `fulcio.sigstore.dev`) must be reachable when verifying. Add them to the ruleset when performing releases.
- **STS token refresh fails on Bedrock/Vertex**: the STS/GCP IAM endpoints must be reachable.

## Related pages

- [Security](/security/)
- [Deployment](/deployment/)
- [Recipes: Airgapped deployment](/recipes/airgapped-deployment/)
- [Best Practices: Secret management](/best-practices/secret-management/)
