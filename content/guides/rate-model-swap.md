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
description: "Hot-swap the underlying model mid-session by editing config.yaml and restarting the daemon — the SQLite session store survives."
keywords: "model swap, hot swap, mid-session, restart, session store, sonnet, opus, haiku"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/guides/rate-model-swap/"
subtitle: "Swap Sonnet for Opus mid-session; the session store survives the restart."
tags: "guides, model, swap, restart, session"
title: "Guide: Hot-swap the model"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "model swap, hot swap, mid-session, restart, session store, sonnet, opus, haiku"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide: Hot-swap the model"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/rate-model-swap/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/rate-model-swap/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guide: Hot-swap the model"
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
twitter_description: "Hot-swap the underlying model mid-session by editing config.yaml and restarting the daemon — the SQLite session store survives."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide: Hot-swap the model"
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

## Why it works

Rousseau reads its provider and model from `config.yaml` once at process start (`config.Load` in `internal/config/config.go`). The session state lives in SQLite. Changing the model means editing the config, restarting the daemon, and letting the next inbound message be handled by the new model — while every session the previous model participated in remains intact in `sessions.db`.

Nothing about the session store is tied to a specific model. The `payload` column (`internal/state/sqlite/schema.sql`) is a plain JSON blob of `agent.Session`; role, content, tool-use blocks. Any model that speaks the Anthropic content-block convention (or is adapted through the SDK adapters in `internal/llm/*/client.go`) can pick up where the previous one left off.

## Swap within the same provider

The easy case. Edit the model field:

```yaml
# was:
anthropic:
  model: claude-sonnet-4-6

# now:
anthropic:
  model: claude-opus-4-6
```

Restart:

```sh
systemctl --user restart rousseau-agent
# or, if you're running rousseau chat interactively, quit and relaunch
```

Send the next message. The reply comes from Opus; the session context is unchanged.

## Swap across providers

Slightly more involved because content-block shapes vary. Rousseau's adapters (`internal/llm/anthropic/client.go`, `internal/llm/openai/client.go`) round-trip `agent.Message` values through the SDK's native types on each turn. That means:

- **`claudecli` → `anthropic`** — clean swap. Both use the same content-block shape.
- **`claudecli` → `bedrock` / `vertex`** — clean swap. Anthropic-on-Bedrock and Anthropic-on-Vertex speak the same messages format.
- **Anthropic-family → `openai` / `openrouter` / `ollama`** — Tool-use blocks are re-shaped to OpenAI's function-call format. Prior tool_use / tool_result pairs in the session round-trip through the adapter. Should be seamless for text; edge cases (multi-tool-use in a single turn, streaming partials) may render differently.

If the session has heavy tool-use history and you're crossing provider families, test with a fresh session first.

## Swap the deployment provider without touching state

Same session store, different daemon config:

```sh
cp ~/.config/rousseau/config.yaml ~/.config/rousseau/config.yaml.bak
$EDITOR ~/.config/rousseau/config.yaml   # change provider + model
systemctl --user restart rousseau-agent
```

`state.path` did not change, so the JID→session mapping (`jid_sessions` table in `internal/state/sqlite/jidmap.go`) still points at the same conversation history for every WhatsApp / Slack / Matrix sender.

## What is preserved

| State | Survives restart | Notes |
|---|---|---|
| Session transcripts | Yes | `sessions` table. |
| FTS5 recall index | Yes | `sessions_fts` virtual table. Re-tokenised on backfill. |
| JID → session mapping | Yes | `jid_sessions` table. |
| Cron jobs | Yes | `cron_jobs` table. |
| WhatsApp device pairing | Yes | `whatsapp.db` (separate file). |
| Anthropic prompt cache hit | **No** | The cache is per-endpoint. A new model or endpoint starts cold. |

## What is lost

The Anthropic prompt-cache markers (`applyCacheMarkers` in `internal/llm/anthropic/client.go`) live inside the model's ephemeral cache — they don't persist across restarts of the model or provider. The next few turns after a swap pay full input tokens; subsequent turns rebuild the cache. This is worth knowing for cost budgeting but not for correctness.

## When to swap vs. start fresh

Swap in place when:

- The session is worth preserving and the content is text-heavy.
- The models are in the same family (both Anthropic, or via Bedrock/Vertex).
- You accept a one-time cache miss.

Start fresh when:

- The session has stale context you don't want a smarter model chasing.
- You're crossing provider families and want deterministic behaviour.
- The token count is at the compression trigger anyway — compress and swap in one go.

## Testing after a swap

```sh
rousseau session list | head -3
rousseau session show <id> | tail -20
# in TUI or via a transport:
> what did we just decide about X?
```

If the reply references the prior conversation coherently, the swap is working. If the model apologises for "not having context" or repeats itself, the adapter round-trip may be losing tool-use metadata — file a bug or fall back to the previous model.

## Related

- [Providers](/providers/) — every supported provider.
- [Configuration](/configuration/) — the exact field names.
- [Guides: Rate limits](/guides/rate-limits/) — cache-marker discussion.
- [Guides: Session management](/guides/session-management/) — full lifecycle.
