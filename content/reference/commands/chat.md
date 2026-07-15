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
description: "Every flag, environment variable, exit code, and session-store interaction for the rousseau chat interactive TUI subcommand."
keywords: "chat, tui, bubbletea, session, cli reference, rousseau chat"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/commands/chat/"
subtitle: "Complete reference for `rousseau chat`."
tags: "reference, cli, chat, tui"
title: "rousseau chat"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "chat, tui, session, rousseau chat"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "rousseau chat"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 60
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/commands/chat/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/commands/chat/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "rousseau chat"
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
twitter_description: "Every flag, environment variable, exit code, and session-store interaction for the rousseau chat interactive TUI subcommand."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "rousseau chat"
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

## Overview

`rousseau chat` opens the interactive Bubble Tea TUI (source: `internal/cli/chat.go` and `internal/tui/model.go`). It wires together the session store (SQLite at `state.path`), the tool registry (`read`, `write`, `edit`, `grep`, `bash`), the approval policy, and the LLM provider — then hands control to the terminal UI.

This is the primary interactive surface. It is the one subcommand that expects a real user at the keyboard; every other transport subcommand (`whatsapp`, `slack`, `discord`, and friends) is a headless daemon that reuses the same wiring underneath.

<aside class="admonition" data-type="tip"><span class="admonition-title">First-run guidance</span><p>The first invocation creates <code>~/.local/share/rousseau/sessions.db</code>. WAL mode is enabled on open, so <code>rousseau session list</code> and <code>rousseau mcp</code> can run against the same database while <code>rousseau chat</code> is open.</p></aside>

## Synopsis

```sh
rousseau chat [--session <id>] [--title <string>] [--config <path>]
```

## Flags

| Flag | Type | Default | Effect |
|---|---|---|---|
| `--session` | string | empty | Resume an existing session by id (loads via `state.Store.Load`). |
| `--title` | string | `"chat <UTC-date>"` | Title assigned when creating a new session. Ignored when `--session` is set. |
| `--config` | string | `$XDG_CONFIG_HOME/rousseau/config.yaml` | Path to the YAML config file. Persistent flag inherited from the root command. |

There are no other flags on `chat`. Everything else — provider, log level, approver — is picked up from config, environment, or hard-coded defaults.

## Environment variables

`rousseau chat` inherits every environment variable resolved by `config.Load` (see `internal/config/config.go`). The most relevant ones:

<div class="tabs" data-tabs="chat-env">
  <div class="tab-list" role="tablist" aria-label="Environment variables">
    <button role="tab" aria-selected="true">Common</button>
    <button role="tab" aria-selected="false">Provider</button>
    <button role="tab" aria-selected="false">Runtime</button>
  </div>
  <div class="tab-panel" role="tabpanel">

| Variable | Effect |
|---|---|
| `ROUSSEAU_PROVIDER` | Overrides `provider`. |
| `ROUSSEAU_LOG_LEVEL` | Overrides `log.level` (`debug`, `info`, `warn`, `error`). |
| `ROUSSEAU_LOG_FORMAT` | Overrides `log.format` (`text` or `json`). |
| `ROUSSEAU_STATE_PATH` | Overrides the SQLite session store location. |
| `XDG_CONFIG_HOME` | Config discovery base directory. |
| `XDG_DATA_HOME` | State discovery base directory. |

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

| Variable | Effect |
|---|---|
| `ANTHROPIC_API_KEY` | Read directly by `config.Load` and injected into `anthropic.api_key` regardless of provider selection. |
| `ROUSSEAU_ANTHROPIC_MODEL` | Overrides `anthropic.model`. |
| `ROUSSEAU_CLAUDECLI_BINARY` | Overrides `claudecli.binary`. |
| `AWS_PROFILE`, `AWS_REGION` | Consumed by Bedrock via the AWS credential chain. |
| `GOOGLE_APPLICATION_CREDENTIALS` | Consumed by Vertex if `vertex.credentials_file` is empty. |

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

| Variable | Effect |
|---|---|
| `TERM` | Bubble Tea uses this to select the renderer. Prefer `xterm-256color` or `screen-256color`. |
| `NO_COLOR` | Suppresses ANSI colour. |
| `HOME` | Resolves default paths for state, config, whatsapp store. |

  </div>
</div>

## Provider selection precedence

The provider is resolved in the order flag > env > file > default:

1. `--config` YAML `provider:` field.
2. `ROUSSEAU_PROVIDER` environment variable.
3. Hard-coded default `claudecli` (set in `setDefaults`).

The provider factory (`buildProvider` in `internal/cli/provider.go`) is called before the TUI starts; a misconfigured provider aborts the command with a non-zero exit code before the screen switches to alt-screen mode.

## Session-store interaction

- The store is opened at `state.path` (default `~/.local/share/rousseau/sessions.db`). Missing parent directories are created with mode `0755`.
- `--session <id>` calls `store.Load(ctx, id)`. An unknown id returns an error.
- Without `--session`, a fresh `agent.Session` is created and immediately persisted so subsequent `rousseau session list` calls see it.
- Every message committed inside the TUI is saved via `store.Save`. The store closes on TUI exit (best-effort).

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Clean exit (Ctrl+C, `:q`, or provider EOF). |
| 1 | Configuration, provider, or store error before TUI startup. |
| 130 | SIGINT while inside the TUI (Bubble Tea exits with 130 by convention). |

## Worked examples

```sh
# 1. Default: start a fresh session with an auto-generated title
rousseau chat

# 2. Resume yesterday's session (find the id with `rousseau session list`)
rousseau chat --session 3f4b1c9e-…

# 3. Named session, structured JSON logs to a file
ROUSSEAU_LOG_FORMAT=json rousseau chat --title "auth refactor" 2>chat.log

# 4. Point at a project-scoped config
rousseau chat --config ./ops/rousseau.yaml
```

## Common failure modes

<aside class="admonition" data-type="warning"><span class="admonition-title">Terminal too small</span><p>Bubble Tea requires at least ~24 lines × ~40 columns to render the viewport + textarea. Smaller terminals show a clipped UI. Resize before launching.</p></aside>

- **`claudecli: exec: "claude": executable file not found`** — the default provider needs the `claude` CLI on `$PATH`. Either install Claude Code or set `provider: anthropic` with an API key. See [Providers: claudecli](/providers/claudecli/).
- **`state: open …/sessions.db: unable to open database file`** — the parent directory is not writable. Run `rousseau doctor` for the resolved path.
- **`session not found`** — the id passed to `--session` does not exist. Use `rousseau session list` to discover valid ids.

## Related pages

- [Reference: CLI Commands](/reference/cli-commands/) — the full command tree table.
- [Reference: Config Schema](/reference/config-schema/) — every YAML key.
- [Reference: Session Store](/reference/session-store/) — the SQLite schema.
- [User Guide: TUI](/user-guide/tui/) — keybindings and interaction model.
- [User Guide: Tools](/user-guide/tools/) — the built-in tool schemas.
- [Providers: claudecli](/providers/claudecli/) — default provider setup.
