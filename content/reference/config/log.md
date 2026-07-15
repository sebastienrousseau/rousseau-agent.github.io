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
description: "Every log config field: log.level, log.format, plus per-transport log conventions."
keywords: "config, log, slog, json, level"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/config/log/"
subtitle: "Structured logging configuration."
tags: "reference, config, log"
title: "Config: Log"

news_genres: "Blog"
news_keywords: "config, log, slog"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Config: Log"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 83
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/config/log/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/config/log/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Config: Log"
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
twitter_description: "Every log config field: log.level, log.format, plus per-transport log conventions."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Config: Log"
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

Rousseau uses Go's standard library `log/slog` for all structured logging. The `log.*` block picks the level and format; concrete handler construction lives in `internal/cli/root.go:newLogger`.

Logs go to **stderr** by default. `rousseau mcp` requires this because stdout is reserved for the JSON-RPC transport.

## `log.*`

| Field | Type | Default | Required | Description | Source |
|---|---|---|---|---|---|
| `log.level` | string | `info` | no | One of `debug`, `info`, `warn`, `warning`, `error`. Case-insensitive. Unknown values fall back to `info`. | `LogConfig.Level` in `internal/config/config.go`; parsed by `newLogger` |
| `log.format` | string | `text` | no | `text` = `slog.TextHandler`, `json` = `slog.JSONHandler`. Anything else defaults to text. | `LogConfig.Format` |

## Level semantics

<div class="tabs" data-tabs="log-level">
  <div class="tab-list" role="tablist" aria-label="Log level">
    <button role="tab" aria-selected="true">debug</button>
    <button role="tab" aria-selected="false">info</button>
    <button role="tab" aria-selected="false">warn</button>
    <button role="tab" aria-selected="false">error</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Every request/response, every tool-call, every whatsmeow protocol frame. Use in development only — extremely verbose.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

One-liner per meaningful event: session created, transport connected, cron fired, provider called. Recommended for production.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Recoverable anomalies: rate limits, retries, expired auth tokens.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Non-recoverable per-request failures. Structured errors with attributes like `err`, `event`, `session_id`, `sender`.

  </div>
</div>

## Log formats

- **`text`** — human-friendly `key=value` pairs. Good for `journalctl -f` on a workstation.
- **`json`** — one JSON object per line. Ship to Loki, Datadog, ELK, or any log aggregator with a JSON parser. Recommended in production.

## Standard log-event names

Rousseau uses dot-separated event names as the `msg` field:

| Prefix | Emitted by |
|---|---|
| `whatsapp.*` | `internal/transport/whatsapp/` |
| `signal.*` | `internal/transport/signal/` |
| `telegram.*` | `internal/transport/telegram/` |
| `matrix.*` | `internal/transport/matrix/` |
| `slack.*` | `internal/transport/slack/` |
| `discord.*` | `internal/transport/discord/` |
| `email.*` | `internal/transport/email/` |
| `sms.*` | `internal/transport/sms/` |
| `imessage.*` | `internal/transport/imessage/` |
| `router.transport.*` | `internal/transport/router.go` |
| `agent.*` | `internal/agent/` |
| `cron.*` | `internal/cron/` |
| `mcp.*` | `internal/mcp/` |

See [Reference: Logs](/reference/logs/) for the full event catalogue.

## Whatsmeow log-level mapping

The whatsmeow library needs its own log level; rousseau translates from `log.level` via `whatsappLogLevel` in `internal/cli/whatsapp.go`:

| `log.level` | Whatsmeow level |
|---|---|
| `debug` | `DEBUG` |
| `info` (default) | `INFO` |
| `warn`, `warning` | `WARN` |
| `error` | `ERROR` |

## Environment variables

| Variable | Effect |
|---|---|
| `ROUSSEAU_LOG_LEVEL` | Overrides `log.level`. |
| `ROUSSEAU_LOG_FORMAT` | Overrides `log.format`. |

## Worked examples

```yaml
# Development
log:
  level: debug
  format: text
```

```yaml
# Production (containerised)
log:
  level: info
  format: json
```

```sh
# One-off debug run without touching the config file
ROUSSEAU_LOG_LEVEL=debug ROUSSEAU_LOG_FORMAT=text rousseau whatsapp 2>debug.log
```

## Related pages

- [Reference: Logs](/reference/logs/) — the event catalogue.
- [Best Practices: Cost control](/best-practices/cost-control/) — logs feed cost dashboards.
- [Deployment](/deployment/) — journalctl + Quadlet.
- [Reference: Config: State](/reference/config/state/)
