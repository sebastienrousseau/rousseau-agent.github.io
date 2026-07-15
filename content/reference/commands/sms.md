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
description: "Complete reference for rousseau sms: outbound-only Twilio or Vonage, credentials, exit codes."
keywords: "sms, twilio, vonage, outbound only, cli reference, rousseau sms"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/commands/sms/"
subtitle: "Complete reference for `rousseau sms`."
tags: "reference, cli, sms, transports"
title: "rousseau sms"

news_genres: "Blog"
news_keywords: "sms, twilio, vonage"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "rousseau sms"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 69
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/commands/sms/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/commands/sms/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "rousseau sms"
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
twitter_description: "Complete reference for rousseau sms: outbound-only Twilio or Vonage, credentials, exit codes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "rousseau sms"
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

`rousseau sms` is a **send-only** SMS bridge backed by Twilio or Vonage. Inbound SMS requires a public HTTP webhook, which conflicts with rousseau's zero-inbound-surface posture — so rousseau does not accept inbound SMS. Use this transport with `rousseau cron` or from other code paths that need to text a number.

Source: `internal/cli/sms.go`. Transport: `internal/transport/sms/`.

<aside class="admonition" data-type="note"><span class="admonition-title">Outbound only</span><p>If you need inbound SMS, put a small webhook in front (e.g. Twilio → your load balancer → a message queue) and have that queue drive <code>rousseau chat</code> or the MCP server directly. Rousseau will not open an inbound HTTP port.</p></aside>

## Synopsis

```sh
rousseau sms [--provider twilio|vonage] [--from <e164|MG…>] \
             [--account-sid AC…] [--auth-token <secret>] [--api-key <key>]
```

## Flags

| Flag | Type | Default | Effect |
|---|---|---|---|
| `--provider` | string | `sms.provider` | `twilio` or `vonage`. |
| `--from` | string | `sms.from` | E.164 sending number, or a Twilio Messaging Service SID (`MG…`). |
| `--account-sid` | string | `sms.account_sid` | Twilio `AC…` AccountSID. |
| `--auth-token` | string | `sms.auth_token` | Twilio auth token or Vonage API secret. |
| `--api-key` | string | `sms.api_key` | Vonage API key. |
| `--config` | string | inherits from root | Path to the YAML config file. |

## Config keys respected

`internal/config/config.go` `SMSConfig`:

| Key | Type | Default | Effect |
|---|---|---|---|
| `sms.provider` | string | empty | Required. `twilio` or `vonage`. |
| `sms.from` | string | empty | Required. E.164 or MG SID. |
| `sms.account_sid` | string | empty | Twilio only. |
| `sms.auth_token` | string | empty | Both providers. |
| `sms.api_key` | string | empty | Vonage only. |
| `sms.base_url` | string | empty | Override for regional endpoints or test doubles. |
| `sms.reply_header` | string | empty | Prefix on outbound messages. |

## Environment variables

| Variable | Effect |
|---|---|
| `ROUSSEAU_SMS_PROVIDER` | Override provider. |
| `ROUSSEAU_SMS_FROM` | Override from. |
| `ROUSSEAU_SMS_ACCOUNT_SID` | Override Twilio SID. |
| `ROUSSEAU_SMS_AUTH_TOKEN` | Override auth token. |
| `ROUSSEAU_SMS_API_KEY` | Override Vonage API key. |

## Startup sequence

1. Resolve provider + from; fail if either is empty.
2. Default `claudecli.permission_mode` to `bypassPermissions`.
3. Open session store, build agent wiring (no inbound router used).
4. `sms.New` — HTTP client.
5. `wiring.startCron` — cron delivery via REST.
6. Block on `client.Start` (a no-op for send-only; keeps the process alive).

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Clean context cancellation. |
| 1 | Missing provider/from, HTTP failure, provider/store error. |
| 130 | SIGINT. |

## Worked examples

<div class="tabs" data-tabs="sms-provider">
  <div class="tab-list" role="tablist" aria-label="SMS provider">
    <button role="tab" aria-selected="true">Twilio</button>
    <button role="tab" aria-selected="false">Vonage</button>
  </div>
  <div class="tab-panel" role="tabpanel">

```sh
rousseau sms \
  --provider twilio \
  --from "+15550001111" \
  --account-sid "$TWILIO_SID" \
  --auth-token "$TWILIO_TOKEN"
```

For a Messaging Service, replace `--from "+1555…"` with `--from "MG…"`.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```sh
rousseau sms \
  --provider vonage \
  --from "RousseauBot" \
  --api-key "$VONAGE_KEY" \
  --auth-token "$VONAGE_SECRET"
```

Vonage `from` can be an alphanumeric sender id in supported regions.

  </div>
</div>

## Common failure modes

- **Twilio `21606` "The 'From' phone number is not a valid message-capable Twilio phone number"** — buy a proper SMS-capable number in the console.
- **Vonage `Non-Whitelisted Destination`** — free-trial accounts can only send to verified numbers.
- **Long messages truncated** — SMS is 160 GSM-7 characters per segment; both providers concatenate but charge per segment.
- **Delivery reports** — rousseau does not consume delivery-status webhooks. Monitor them on Twilio/Vonage directly.

## Related pages

- [Transports: SMS](/transports/sms/)
- [Reference: Commands: cron](/reference/commands/cron/)
- [Best Practices: Cost control](/best-practices/cost-control/)
- [Reference: Logs](/reference/logs/)
