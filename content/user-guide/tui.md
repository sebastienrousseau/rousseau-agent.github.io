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
description: "Bubble Tea TUI keybindings, panels, spinner and streaming semantics for rousseau-agent's rousseau chat command."
keywords: "tui, bubble tea, keybindings, viewport, textarea, spinner, streaming, session"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/user-guide/tui/"
subtitle: "Bubble Tea keybindings, panels, streaming."
tags: "tui, bubble-tea, keybindings"
title: "TUI"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tui, bubble tea, keybindings, viewport, textarea, spinner, streaming, session"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "TUI"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/tui/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/tui/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "TUI"
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
twitter_description: "Bubble Tea TUI keybindings, panels, spinner and streaming semantics for rousseau-agent's rousseau chat command."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "TUI"
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

## Overview

`rousseau chat` opens a Bubble Tea TUI with three regions:

```
+------------------------------------------------------+
|                       Header                         |  session title
+------------------------------------------------------+
|                                                      |
|                                                      |
|                     Viewport                         |  scrollable history
|          (messages, streamed reply preview)          |
|                                                      |
|                                                      |
+------------------------------------------------------+
|                     Textarea                         |  input, Enter to send
+------------------------------------------------------+
| status: idle | spinner | streaming | error           |
+------------------------------------------------------+
```

Runs in Bubble Tea's alt-screen mode — the TUI takes over the terminal buffer and restores it on exit.

## Keybindings

Rousseau's TUI keeps the binding set small. When in doubt, standard Bubble Tea viewport / textarea shortcuts apply.

### Global

| Key | Action |
|---|---|
| `Ctrl+C` | Quit. Saves the current session, prints nothing on the way out. |
| `Esc` | Quit. Same as `Ctrl+C`. |
| `Enter` | Send the current textarea contents. No-op while the agent is busy. |

### Textarea (input)

Standard Bubble Tea textarea behaviour:

| Key | Action |
|---|---|
| Any printable character | Insert at cursor. |
| `Backspace` | Delete character before cursor. |
| `Delete` | Delete character under cursor. |
| Arrow keys | Move cursor. |
| `Home` / `End` | Jump to line start / end. |
| `Ctrl+A` / `Ctrl+E` | Jump to line start / end (Emacs bindings). |
| `Ctrl+U` | Kill to line start. |
| `Ctrl+K` | Kill to line end. |
| `Shift+Enter` | (Terminal-dependent) newline without submitting; often mapped as literal `\n`. |

The textarea grows vertically as content wraps; the viewport shrinks to accommodate.

### Viewport (history)

The viewport supports the usual Bubble Tea viewport shortcuts. Focus is on the viewport when the textarea is empty; typing routes to the textarea automatically.

| Key | Action |
|---|---|
| `PgUp` / `PgDn` | Scroll one page. |
| `↑` / `↓` | Scroll one line. |
| `Home` / `End` | Jump to top / bottom. |
| Mouse wheel | Scroll. |

## Panel semantics

### Header

`rousseau · <session title>`. The title comes from `--title` when the session was created (default: `chat YYYY-MM-DD HH:MM`).

### Viewport

Rendered history plus, while a turn is in-flight, a **streaming preview** at the bottom. The preview reflects deltas as the provider streams; when the turn finishes, the preview is replaced by the final assistant message.

Every message is prefixed by its role (`you`, `rousseau`, `tool`) so the flow is unambiguous when the model requests a tool call.

### Textarea

Placeholder text: `Ask, or press Ctrl+C to quit…`. Enter submits; the textarea resets on submit.

While the agent is busy, `Enter` is a no-op so accidental double-submits don't stack turns.

### Status line

Underneath the textarea. Content varies:

| State | Line |
|---|---|
| Idle | Empty. |
| Busy | Spinner + `thinking…`. Spinner ticks come from `bubbles/spinner`. |
| Streaming | Spinner continues; the streaming delta appears in the viewport preview. |
| Error | Error string in red. The next successful turn clears it. |

## Session persistence

Every turn is persisted to `~/.local/share/rousseau/sessions.db` via `state.Store.Save`. If the daemon crashes mid-turn:

- The user turn is already saved (it was appended before `doTurn` fires).
- The assistant reply is only saved once the turn completes.

On restart, `rousseau chat --session <id>` resumes from the last successfully saved state.

## Session commands from the CLI

The TUI does not surface every session operation. Manage sessions from a shell:

```sh
rousseau session list
rousseau session show <id>
rousseau session search "kubectl"
rousseau session delete <id>
```

## Streaming semantics

Providers that implement `StreamingProvider.ChatStream` (Anthropic, `claudecli`) stream deltas into the viewport preview. Providers that only implement `Provider.Chat` (Bedrock, Vertex, OpenAI-compatible depending on shim) deliver the reply as a single block on turn completion — the preview stays empty and the reply appears when `busy` becomes `false`.

## When things go wrong

- **The TUI hangs** — `Ctrl+C` twice. The first `Ctrl+C` signals `tea.Quit`, which flushes state. The second is captured by the OS.
- **The viewport is empty and the textarea won't accept input** — the alt-screen may have been corrupted by an escape-sequence-emitting subprocess (e.g. a tool call that prints ANSI codes). Restart the TUI.
- **The status line stays on `thinking…`** — the provider hasn't returned. Check the daemon's stderr (rousseau writes slog to stderr; if you piped it away, resurface it).

## Next

- [User Guide: CLI](/user-guide/cli/) — every command outside the TUI.
- [Concepts](/concepts/) — the agent loop underneath.
- [Compression + Recall](/user-guide/compression-recall/) — how long chats stay usable.
