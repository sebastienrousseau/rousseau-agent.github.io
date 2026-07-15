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
description: "Rousseau-agent ships zero telemetry. No analytics endpoint, no crash-report upload, no license server, no unique identifiers."
keywords: "telemetry, privacy, no phone home, no analytics, no license server"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/guides/telemetry/"
subtitle: "Zero analytics, zero phone-home. Verifiable."
tags: "guides, telemetry, privacy, security"
title: "Guide: Telemetry"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "telemetry, privacy, no phone home, no analytics, no license server"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide: Telemetry"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 40
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/telemetry/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/telemetry/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guide: Telemetry"
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
twitter_description: "Rousseau-agent ships zero telemetry. No analytics endpoint, no crash-report upload, no license server, no unique identifiers."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide: Telemetry"
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

## The commitment

Rousseau-agent ships zero telemetry. The list of things rousseau explicitly does **not** do:

- No analytics endpoint. There is no `metrics.rousseau-agent.dev` or equivalent.
- No crash-report upload. Panics land in stderr; nothing is uploaded anywhere.
- No license server. There is no periodic check-in and no seat verification.
- No unique installation identifier. The binary is byte-identical across every install of the same tag.
- No feature-flag service. Every switch in rousseau is in `config.yaml` or a CLI flag.
- No update ping. `rousseau version` is a local lookup; there is no "checking for updates" round trip.

## How to verify

The rousseau binary is open source (MIT, see `LICENSE`). Every network call is grep-able:

```sh
grep -rn 'http.Get\|http.Post\|http.Client\|http.NewRequest\|net/http' \
  /path/to/rousseau-agent/internal/ | head
```

Every hit lands in one of these categories:

| Package | Purpose |
|---|---|
| `internal/llm/anthropic/` | Anthropic API calls (via the official SDK). |
| `internal/llm/openai/` | OpenAI-compatible endpoint calls. |
| `internal/transport/telegram/` | Telegram Bot API. |
| `internal/transport/matrix/` | Matrix client-server API. |
| `internal/transport/whatsapp/` | Whatsmeow websockets to Meta. |
| `internal/transport/slack/`, `discord/` | Socket Mode / Discord Gateway. |
| `internal/transport/imessage/` | BlueBubbles server (on your LAN). |
| `internal/transport/sms/` | Twilio / Vonage. |
| `internal/transport/email/` | IMAP + SMTP. |

None of them are analytics endpoints. Every one is either the LLM provider you configured or the transport you enabled.

Run the daemon under `strace -e network` or watch it with `ss -tanp` — the only sockets you will see are to the endpoints listed above.

## Structured logging is local

Rousseau uses `log/slog` (`internal/cli/root.go`). By default the handler writes to stderr, which under the Quadlet unit lands in the systemd journal. Nothing is streamed off-host. If you want to ship logs to Loki, Datadog, or elsewhere, you configure that pipeline yourself — see [Guides: Observability](/guides/observability/).

## Comparison

| Product | Analytics | Crash upload | License server |
|---|---|---|---|
| rousseau-agent | none | none | none |
| Vendor A (typical SaaS coding assistant) | yes | yes | yes |
| Vendor B (managed control plane) | yes | opt-out | yes |

Rousseau's operating model is: you bring the LLM key, you host the daemon. There is no piece of rousseau that runs on servers Sebastien controls.

## What rousseau _does_ send to LLM providers

By definition, when you route messages through Anthropic, Bedrock, Vertex, OpenAI, or any other API, that provider sees the message content. This is inherent to how LLM inference works — rousseau is a client, not a shim.

Two mitigations if the provider's data-handling matters to you:

1. **Run against a self-hosted model.** Ollama, vLLM, LM Studio, or any OpenAI-compatible endpoint. Nothing leaves your machine. See [Guides: Self-hosted vLLM](/guides/self-hosted-vllm/).
2. **Use Bedrock or Vertex in a region with a data-processing addendum.** Both AWS and GCP publish per-region data-residency guarantees.

## What the WhatsApp bridge sees

The unofficial WhatsApp Web protocol implemented by whatsmeow speaks to Meta's servers — that traffic is outside rousseau's control. Meta sees your messages the same way it does when you use WhatsApp Web from a browser. If Meta seeing your messages is not acceptable, do not run the WhatsApp bridge.

The whatsmeow client is publicly auditable — every packet is documented; there are no rousseau-specific network calls layered on top.

## Related

- [Security](/security/) — trust boundaries and audit posture.
- [Privacy](/privacy/) — the site-level privacy posture.
- [Providers: OpenAI-compatible](/providers/openai-compatible/) — self-hosted inference.
- [Guides: Self-hosted vLLM](/guides/self-hosted-vllm/) — a worked example.
