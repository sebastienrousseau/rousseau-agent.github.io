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
description: "Compact reference table of every rousseau-agent command mirroring the output of rousseau --help."
keywords: "cli, commands, reference, table, rousseau --help"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/cli-commands/"
subtitle: "Every command tabulated."
tags: "reference, cli, commands"
title: "CLI Commands"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cli, commands, reference, table, rousseau --help"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "CLI Commands"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 50
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/cli-commands/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/cli-commands/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "CLI Commands"
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
twitter_description: "Compact reference table of every rousseau-agent command mirroring the output of rousseau --help."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "CLI Commands"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">What you'll learn</span><p>The complete <code>rousseau</code> CLI surface: every command, its flags, exit-code semantics, and the config keys each flag overrides. This is the scannable reference — see <a href="/user-guide/cli/">User Guide: CLI</a> for a walkthrough with worked examples.</p></aside>

## Command tree

Every command surfaces its help via `rousseau <cmd> --help`. This page is the tabulated summary.

| Command | Description |
|---|---|
| `chat` | Open the interactive Bubble Tea TUI. |
| `whatsapp` | Run the WhatsApp bridge (whatsmeow). |
| `signal` | Run the Signal bridge (signal-cli JSON-RPC). |
| `telegram` | Run the Telegram Bot API long-poller. |
| `matrix` | Run the Matrix client-server bridge. |
| `slack` | Run the Slack Socket Mode bridge. |
| `discord` | Run the Discord Gateway bridge. |
| `sms` | Send-only SMS via Twilio or Vonage. |
| `imessage` | BlueBubbles-backed iMessage bridge. |
| `email` | IMAP inbound + SMTP outbound bridge. |
| `mcp` | Start the MCP JSON-RPC 2.0 server on stdio. |
| `cron add` | Add a scheduled prompt. |
| `cron list` | List every scheduled job. |
| `cron remove` | Delete a scheduled job. |
| `cron enable` | Enable a disabled scheduled job. |
| `cron disable` | Disable an enabled scheduled job. |
| `session list` | List sessions in the store, newest first. |
| `session search` | FTS5 search across every session's message content. |
| `session show` | Print a session's message history. |
| `session delete` | Delete a session. |
| `skills list` | List discovered skills from `skills_dir`. |
| `skills show` | Print a skill's YAML front-matter and body. |
| `skills lint` | Validate skills for schema conformance. |
| `doctor` | Diagnose the local installation. Prints a report. |
| `status` | Print daemon status. |
| `init` | Write a default config to `~/.config/rousseau/`. |
| `version` | Print version, commit, and build date. |

## Global flags

Every command accepts these:

| Flag | Type | Config key | Notes |
|---|---|---|---|
| `--config` | string | — | Load configuration from this file. Default: `$XDG_CONFIG_HOME/rousseau/config.yaml`. |
| `--help`, `-h` | bool | — | Print help for the current command. |

## Per-transport flags

### `rousseau whatsapp`

| Flag | Type | Config key | Notes |
|---|---|---|---|
| `--store` | string | — | Path to the whatsmeow device store. Default `$XDG_DATA_HOME/rousseau/whatsapp.db`. |
| `--allow` | []string | `whatsapp.allowlist` | Restrict inbound to these JIDs. Repeatable. |

### `rousseau slack`

| Flag | Type | Config key |
|---|---|---|
| `--app-token` | string | `slack.app_token` |
| `--bot-token` | string | `slack.bot_token` |
| `--bot-user-id` | string | `slack.bot_user_id` |
| `--allow` | []string | `slack.allowlist` |

### `rousseau discord`

| Flag | Type | Config key |
|---|---|---|
| `--token` | string | `discord.token` |
| `--allow` | []string | `discord.allowlist` |

### `rousseau telegram`

| Flag | Type | Config key |
|---|---|---|
| `--token` | string | `telegram.token` |
| `--allow` | []string | `telegram.allowlist` |

### `rousseau matrix`

| Flag | Type | Config key |
|---|---|---|
| `--homeserver-url` | string | `matrix.homeserver_url` |
| `--access-token` | string | `matrix.access_token` |
| `--user-id` | string | `matrix.user_id` |
| `--allow` | []string | `matrix.allowlist` |

### `rousseau signal`

| Flag | Type | Config key |
|---|---|---|
| `--account` | string | `signal.account` |
| `--binary` | string | `signal.binary` |
| `--allow` | []string | `signal.allowlist` |

### `rousseau email`

| Flag | Type | Config key |
|---|---|---|
| `--imap-addr` | string | `email.imap_addr` |
| `--imap-username` | string | `email.imap_username` |
| `--imap-password` | string | `email.imap_password` |
| `--smtp-addr` | string | `email.smtp_addr` |
| `--smtp-username` | string | `email.smtp_username` |
| `--smtp-password` | string | `email.smtp_password` |
| `--from` | string | `email.from` |
| `--mailbox` | string | `email.mailbox` |
| `--poll-interval` | string | `email.poll_interval` |

### `rousseau sms`

| Flag | Type | Config key |
|---|---|---|
| `--provider` | string | `sms.provider` |
| `--from` | string | `sms.from` |
| `--to` | string | (positional) |

### `rousseau imessage`

| Flag | Type | Config key |
|---|---|---|
| `--base-url` | string | `imessage.base_url` |
| `--password` | string | `imessage.password` |
| `--chat-guid` | string | `imessage.chat_guid` |

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Clean exit — command completed. Not typical for long-running daemons (they usually terminate on signal). |
| 1 | Any error surfaced from `Execute`. See [Reference: Exit codes](/reference/exit-codes/) for the classification. |

## Precedence

Config values are resolved in the order **flag &gt; env &gt; file &gt; default** (see `config.Load` in `internal/config/config.go`). Env vars are prefixed `ROUSSEAU_` with dots replaced by underscores — e.g. `ROUSSEAU_ANTHROPIC_MODEL` overrides `anthropic.model`. The bare `ANTHROPIC_API_KEY` env var is also honoured (special-cased in `config.Load`).

## Troubleshooting

### `unknown flag: --allow` on `rousseau chat`

`--allow` is transport-scoped. `chat` has no allowlist because there is no ingress. Use `rousseau whatsapp --allow …` instead.

### Flag order matters for repeatable flags

`--allow A --allow B` is two values, but `--allow=A,B` is one value that happens to contain a comma. Prefer separate flags.

### Env override not picked up

Rousseau reads env at start only. Restart the daemon after changing env vars, or use `--config` to force a reload.

### `flag provided but not defined`

Cobra rejects unknown flags. If you copy a flag from a newer version, check `rousseau <cmd> --help` for the current spelling.

## Related pages

- [User Guide: CLI](/user-guide/cli/) — every command with worked examples.
- [Reference: Exit codes](/reference/exit-codes/) — signal semantics.
- [Reference: Config schema](/reference/config-schema/) — every configuration field.
- [Reference: Environment variables](/reference/environment-variables/) — env override matrix.
- [Configuration](/configuration/) — the full config file walkthrough.

## Further reading

- `internal/cli/root.go` — Cobra command tree.
- `internal/cli/*.go` — one file per subcommand.
- `internal/config/config.go` — `Load` and default resolution.
