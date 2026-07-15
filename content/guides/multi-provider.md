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
description: "Run two rousseau daemons with different providers side-by-side — e.g. claudecli for interactive chat and Bedrock for scheduled reports."
keywords: "multi provider, claudecli, bedrock, config precedence, XDG_CONFIG_HOME"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/guides/multi-provider/"
subtitle: "Two daemons, two providers, one operator."
tags: "guides, providers, multi-provider, deployment"
title: "Guide: Multi-provider"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "multi provider, claudecli, bedrock, config precedence, XDG_CONFIG_HOME"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide: Multi-provider"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 35
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/multi-provider/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/multi-provider/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guide: Multi-provider"
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
twitter_description: "Run two rousseau daemons with different providers side-by-side — e.g. claudecli for interactive chat and Bedrock for scheduled reports."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide: Multi-provider"
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

## Why you might want this

Rousseau's `provider` field is a single scalar (`internal/config/config.go` `Config.Provider`). A single rousseau process talks to exactly one provider. When you want more than one — most commonly, `claudecli` for interactive TUI use because it inherits an OAuth session, and a paid API provider (Bedrock, Anthropic direct, Vertex) for background daemons where subscription-tier `claude` OAuth is inconvenient — you run **two rousseau processes** with different config files.

Reasonable pairings:

| Interactive | Unattended | Why |
|---|---|---|
| `claudecli` | `anthropic` or `bedrock` | OAuth for laptop chat, API key for a VPS daemon. |
| `claudecli` | `vertex` | Same, on GCP. |
| `anthropic` | `openai` or `ollama` | Compare answers, or fall back to a cheaper/local model for cron. |
| `claudecli` | `openai` (OpenRouter) | Claude in TUI, cheap OpenRouter model for scheduled summaries. |

## How rousseau resolves config

`config.Load` (in `internal/config/config.go`) applies flag > env > file > default. The file it reads defaults to `~/.config/rousseau/config.yaml`, but the `--config` persistent flag on the root command (`internal/cli/root.go`) overrides it. That gives you a clean split.

## Two-config layout

```sh
mkdir -p ~/.config/rousseau
cat > ~/.config/rousseau/chat.yaml <<'YAML'
provider: claudecli
claudecli:
  binary: claude
log:
  level: info
  format: text
YAML

cat > ~/.config/rousseau/cron.yaml <<'YAML'
provider: bedrock
bedrock:
  region: eu-west-2
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
log:
  level: info
  format: json
YAML
```

Run each command with the right file:

```sh
rousseau --config ~/.config/rousseau/chat.yaml chat
rousseau --config ~/.config/rousseau/cron.yaml whatsapp --allow YOUR_JID@s.whatsapp.net
```

## Shared vs partitioned state

Both processes point at the same SQLite session store by default (`~/.local/share/rousseau/sessions.db`) — and that's usually what you want, so the WhatsApp bridge and your TUI chat share history.

To fully partition state, override `state.path` per config:

```yaml
state:
  path: /home/seb/.local/share/rousseau/chat.db
```

Cross-process SQLite access is safe because of WAL journaling and the 15-second `busy_timeout` set by `Open()` in `internal/state/sqlite/store.go`.

## systemd wiring

Two Quadlet units, one per config. Each unit's `Exec=` includes `--config /home/rousseau/.config/rousseau/<name>.yaml`:

```ini
Exec=--config /home/rousseau/.config/rousseau/cron.yaml whatsapp --allow ...
```

See [Deployment](/deployment/) for the base unit.

## Approver policies per config

Different providers deserve different approvals. Interactive `claudecli` can safely stay in `mode: allow_all` because Claude Code has its own per-call approval UI. The Bedrock/Anthropic daemon should run `mode: pattern` with `default: deny`. Put each under its own YAML.

## Testing

Confirm each process talks to the right endpoint:

```sh
# Interactive shows the claudecli subprocess path in strace / lsof
lsof -c rousseau | grep -E 'claude|CLAUDE'

# Background shows outbound HTTPS to bedrock-runtime.<region>.amazonaws.com
ss -tanp | grep rousseau
```

## What this does NOT give you

- **Not per-request routing.** Rousseau will not fall back from one provider to another inside a single turn. Failure of the configured provider surfaces as `whatsapp.handler_failed` / `turn.failed` and the model does not retry against a different provider. That is a roadmap item.
- **Not shared caching.** The Anthropic prompt cache (see `applyCacheMarkers` in `internal/llm/anthropic/client.go`) is per-endpoint. A hit under Anthropic direct is not a hit against Bedrock, even for the same model family.

## Related

- [Providers](/providers/) — comparison of all five provider types.
- [Configuration](/configuration/) — every knob.
- [Reference: Environment Variables](/reference/environment-variables/) — env-based overrides.
- [Guides: Production Deployment](/guides/production-deployment/).
