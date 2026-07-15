---

# Front Matter (YAML)

author: "sebastian.rousseau@gmail.com (Sebastien Rousseau) "
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
description: "How the LLM compressor decides what to keep, the roles of trigger_messages and keep_recent, and a before/after diagram of a compressed session."
keywords: "compression, context, keep_recent, trigger_messages, summariser, marker"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/guides/context-management/"
subtitle: "trigger_messages, keep_recent, and the compressed-marker convention."
tags: "guides, context, compression, summariser"
title: "Guide: Context management"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "compression, context, keep_recent, trigger_messages, summariser, marker"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide: Context management"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/context-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/context-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guide: Context management"
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
twitter_description: "How the LLM compressor decides what to keep, the roles of trigger_messages and keep_recent, and a before/after diagram of a compressed session."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide: Context management"
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

## The problem

A session that runs for weeks accumulates hundreds of messages. Every one is re-sent to the provider on every turn. Cost grows linearly with turn count; latency grows too. Rousseau's `LLMCompressor` (`internal/agent/compressor.go`) trades a small one-off cost — one summarisation call per compression — for permanent savings on every subsequent turn.

Compression is **off by default** because the reference deployment uses `claudecli` on a subscription tier, where token count is not billed. Turn it on when running against Anthropic direct, Bedrock, Vertex, or OpenAI-compatible pay-per-token providers.

## The knobs

From `CompressionConfig` in `internal/config/config.go`:

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60        # zero uses the default 60
    keep_recent: 8              # zero uses the default 8
    prompt: ""                  # overrides the default summariser prompt
```

Meanings:

| Field | What it does |
|---|---|
| `enabled` | Turn compression on. When false, the agent uses `NoopCompressor` and this whole section is a no-op. |
| `trigger_messages` | Compression fires once `len(session.Messages) >= trigger_messages`. |
| `keep_recent` | Number of most-recent messages preserved verbatim after compression. |
| `prompt` | Overrides the default summariser prompt. Set only if you need custom instructions (e.g. preserve JSON output, always cite file paths). |

## The default summariser prompt

```
Summarise the following conversation in <=200 words. Preserve every
commitment, TODO, credential, filename, and quoted output. Skip
pleasantries. Return only the summary — no preamble.
```

Defined as `defaultSummaryPrompt` in `internal/agent/compressor.go`. Override with `agent.compression.prompt` in `config.yaml`.

## Before / after

A session of 68 messages, `trigger_messages: 60`, `keep_recent: 8`:

```
Before compression:                        After compression:

┌──────────────────────────┐              ┌──────────────────────────────┐
│ msg[0]  user             │              │ msg[0]  user (synthetic)     │
│ msg[1]  assistant        │              │   [rousseau-compressed]      │
│ msg[2]  user             │              │   (summary of prior 60       │
│  …  (60 messages)        │      →       │    messages): …              │
│ msg[59] assistant        │              ├──────────────────────────────┤
├──────────────────────────┤              │ msg[1]  user       — verbatim │
│ msg[60] user   verbatim  │              │ msg[2]  assistant  — verbatim │
│ msg[61] assistant        │              │ msg[3]  user       — verbatim │
│  …                       │              │ msg[4]  assistant  — verbatim │
│ msg[67] assistant        │              │ msg[5]  user       — verbatim │
└──────────────────────────┘              │ msg[6]  assistant  — verbatim │
                                          │ msg[7]  user       — verbatim │
                                          │ msg[8]  assistant  — verbatim │
                                          └──────────────────────────────┘
Total messages: 68                        Total messages: 9
Input tokens: ~5000 per turn              Input tokens: ~800 per turn
```

## The marker

The compressor prefixes the synthetic user message with `[rousseau-compressed]` (constant `DefaultCompressorMarker` in `internal/agent/compressor.go`). On subsequent turns, `headAlreadyCompressed()` uses the marker to detect an already-compressed prefix and skips repeat compression unless the session has grown to `2 * trigger_messages`.

This is what keeps compression bounded — you don't pay to re-summarise the summary every 60 messages.

## Choosing values

| Situation | Recommended |
|---|---|
| Long-running transport daemon on a paid provider. | `trigger_messages: 60`, `keep_recent: 8`. Defaults are tuned for this. |
| Interactive TUI where you want everything in context. | `enabled: false`. |
| Highly technical sessions with lots of quoted code / logs. | `trigger_messages: 40`, `keep_recent: 12`. Preserve more recent context; compress sooner. |
| Cost-critical batch summariser (cron). | Each cron run is a fresh session, so compression rarely triggers. Leave defaults on. |

## Cost of a compression pass

One summarisation call per firing. The Provider used is whatever `Config.Provider` selects — the same one the agent uses. That means:

- Sonnet-class compressor call: ~1-2 seconds, roughly the cost of ~2 turns' worth of input tokens.
- Break-even after ~5-10 subsequent turns depending on session shape.

For a cheaper compressor, run rousseau in the two-daemon multi-provider pattern with a Haiku-class model for the compressor daemon. See [Guides: Multi-provider](/guides/multi-provider/).

## Emergency: session is too large to load

If a session's payload grows past the model's context window before compression fires — rare but possible with a very small `trigger_messages` and large tool outputs — the next turn will fail with a provider "context length exceeded" error. Recovery:

```sh
rousseau session delete <id> --yes
```

Then start fresh. Or manually shrink via SQLite:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
UPDATE sessions SET payload = json_set(payload, '$.messages',
  json_extract(payload, '$.messages[-8:]'))
WHERE id = '<session-id>';
SQL
```

Note: the exact JSON path syntax depends on SQLite version. Confirm with a `SELECT payload` first.

## Related

- [User Guide: Compression + Recall](/user-guide/compression-recall/) — deeper reference.
- [Guides: Rate limits](/guides/rate-limits/) — cost implications.
- [Guides: Session management](/guides/session-management/) — session lifecycle.
- [Reference: Config schema](/reference/config-schema/) — every field.
