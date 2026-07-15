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
description: "Pair-program with rousseau over WhatsApp: voice-note transcription, workspace editing, safe bash execution."
keywords: "whatsapp, pair programming, voice, whisper, recipes"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/recipes/whatsapp-pair-programming/"
subtitle: "Pair-program with rousseau while you're away from the desk."
tags: "recipes, whatsapp, voice"
title: "Recipe: WhatsApp Pair Programming"

news_genres: "Blog"
news_keywords: "whatsapp, pair programming, voice"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Recipe: WhatsApp Pair Programming"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "recipes"
order: 16
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/recipes/whatsapp-pair-programming/index.html"
item_link: "https://docs.rousseau-agent.dev/recipes/whatsapp-pair-programming/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Recipe: WhatsApp Pair Programming"
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
twitter_description: "Pair-program with rousseau over WhatsApp: voice-note transcription, workspace editing, safe bash execution."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Recipe: WhatsApp Pair Programming"
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

You're on a train, you had an idea, you dictate a voice note. Rousseau transcribes it with whisper, edits the file on your workstation via the bind-mounted workspace, and replies with a summary. Session picks up where you left it thanks to `--session`.

## Prerequisites

- WhatsApp paired and confirmed (`rousseau whatsapp` at least once).
- `whisper` (whisper.cpp CLI) installed on the daemon host.
- Workspace bind mount (`/workspace`) with the repo you're editing.
- Any provider that handles tool-use — `claudecli` if you have Claude Code, `anthropic` otherwise.

## Config

```yaml
provider: claudecli

agent:
  max_iterations: 40
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read,  match: ".*"}
      - {tool: grep,  match: ".*"}
      - {tool: edit,  match: "^/workspace/.*"}
      - {tool: write, match: "^/workspace/.*"}
      - {tool: bash,  match: "^(git (log|diff|status|add [^&|;`$]+|commit -m)|go test ./...|npm test)"}
    deny:
      - {tool: bash,  match: "rm|sudo|git push"}

whatsapp:
  reply_header: ""
  voice:
    enabled: true
    binary: /usr/local/bin/whisper
    model: base.en
    language: en
```

The approver:

- `edit`/`write` scoped to `/workspace` — the container sees nothing else.
- `bash` limited to safe git + test invocations.
- `git push` explicitly denied — pushing decisions belong to a human.

## Launch

```sh
# In the Podman quadlet, or bare metal:
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

## Verification

- [ ] Send a text: "Read /workspace/README.md and give me a one-line summary." — reply lands within 5 s.
- [ ] Send a voice note: "Add a docstring to the main function in server.go" — whisper transcribes, the file is edited, git status shows the change.
- [ ] `rousseau session list --limit 3` shows the pair session.

## Failure modes

- **Voice notes silently dropped** — `whatsapp.voice.enabled: false` or `whisper` binary missing. `rousseau doctor` catches both.
- **Edits fail with "unique-string constraint violated"** — the built-in `edit` tool refuses when the search string appears more than once (a safety rail). Include more surrounding context.
- **Transcription in the wrong language** — set `whatsapp.voice.language` explicitly instead of relying on auto-detect.

## Related pages

- [Reference: Commands: whatsapp](/reference/commands/whatsapp/)
- [Transports: WhatsApp](/transports/whatsapp/)
- [Best Practices: Approval rules](/best-practices/approval-rules/)
- [Best Practices: Session hygiene](/best-practices/session-hygiene/)
