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
description: "rousseau-agent's SMS transport is send-only. Twilio (account_sid + auth_token) or Vonage (api_key + auth_token). Inbound not supported because it requires a public webhook."
keywords: "SMS, Twilio, Vonage, Nexmo, send-only, Messaging Service SID, E.164, no webhook"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/transports/sms/"
subtitle: "Send-only SMS via Twilio or Vonage."
tags: "transports, SMS"
title: "SMS Transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "SMS, Twilio, Vonage, Nexmo, send-only, Messaging Service SID, E.164, no webhook"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "SMS Transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 19
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/sms/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/sms/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "SMS Transport"
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
twitter_description: "rousseau-agent's SMS transport is send-only. Twilio (account_sid + auth_token) or Vonage (api_key + auth_token). Inbound not supported because it requires a public webhook."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "SMS Transport"
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

## Send-only, by design

The SMS transport is **send-only**. Inbound SMS requires a public HTTP webhook that the carrier POSTs into — which directly conflicts with rousseau's zero-inbound-surface posture. If your use case needs inbound SMS, run rousseau alongside a purpose-built webhook receiver and route messages through the cron scheduler or the agent-loop embed API.

`Start` is implemented as a no-op that blocks on `ctx.Done()` so the transport still slots into the standard daemon wiring shape.

## Supported carriers

| Carrier | Config `provider` | Required fields |
|---|---|---|
| Twilio | `twilio` | `from`, `account_sid`, `auth_token` |
| Vonage (formerly Nexmo) | `vonage` | `from`, `api_key`, `auth_token` (the API secret) |

## Twilio configuration

```yaml
sms:
  provider: twilio
  from: "+15550000000"
  account_sid: "AC..."
  auth_token: "..."
```

`from` can be either an E.164 sender number or a **Twilio Messaging Service SID** (starts with `MG…`). Messaging Services handle fleet management, sticky-sender routing, and geo-based sender selection — recommended for anything more than single-country traffic.

`base_url` defaults to `https://api.twilio.com/2010-04-01` and only needs an override for regional endpoints or testing.

## Vonage configuration

```yaml
sms:
  provider: vonage
  from: "+15550000000"
  api_key: "abcd1234"
  auth_token: "efgh5678"
```

`auth_token` in the Vonage config maps to Vonage's **API secret**, not their JWT signing key — Vonage authenticates SMS submissions with a simple key/secret pair.

`base_url` defaults to `https://rest.nexmo.com`.

## Command-line

```sh
# Twilio
rousseau sms \
  --provider twilio \
  --from '+15550000000' \
  --account-sid AC... \
  --auth-token ...

# Vonage
rousseau sms \
  --provider vonage \
  --from '+15550000000' \
  --api-key abcd1234 \
  --auth-token efgh5678
```

Since there is no inbound side, `--allow` does not apply.

## Delivery API

Both providers use their respective REST endpoints:

- **Twilio.** `POST /2010-04-01/Accounts/{sid}/Messages.json` with basic-auth SID/token.
- **Vonage.** `POST /sms/json` with `api_key` + `api_secret` in the body.

Returned message IDs are logged; delivery-status webhooks are **not** consumed (again, no public HTTP surface).

## E.164 formatting

`from` and destination numbers must be in E.164 (`+<country><subscriber>`). No spaces, no dashes. Twilio Messaging Service SIDs bypass this requirement for the `from` slot only.

## Cost hygiene

- Set `max_tokens` on your provider aggressively — SMS is cheap per message but bytes multiply fast if the model generates long replies (Twilio segments at 160 chars for GSM-7 or 70 for UCS-2).
- Consider rewriting the outbound reply to be terse before handing it to the SMS transport. `agent.Options.SystemPrompt` is the right place.
