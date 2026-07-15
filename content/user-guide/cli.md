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
description: "Full CLI reference for rousseau-agent: every command, every flag, exit codes, per-transport subcommands."
keywords: "cli, cobra, commands, flags, subcommands, exit codes"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/user-guide/cli/"
subtitle: "Every command, every flag."
tags: "cli, reference, commands"
title: "CLI Reference"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cli, cobra, commands, flags, subcommands, exit codes"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "CLI Reference"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 40
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/cli/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/cli/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "CLI Reference"
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
twitter_description: "Full CLI reference for rousseau-agent: every command, every flag, exit codes, per-transport subcommands."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "CLI Reference"
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

## Invocation

```
rousseau [--config <path>] <command> [flags]
```

Every command reads defaults from `~/.config/rousseau/config.yaml` (or the file passed via `--config`). Flags override env vars, env vars override the file, the file overrides hard-coded defaults.

## Global flags

| Flag | Type | Default | Notes |
|---|---|---|---|
| `--config` | string | `$XDG_CONFIG_HOME/rousseau/config.yaml` | Load configuration from this file. Absent means the default XDG path. |
| `--help`, `-h` | bool | — | Print help for the current command. |

## Command tree

```
rousseau
├── chat                Bubble Tea TUI
├── whatsapp            WhatsApp bridge (whatsmeow)
├── signal              Signal bridge (signal-cli JSON-RPC)
├── telegram            Telegram Bot API long-polling
├── matrix              Matrix client-server API
├── slack               Slack Socket Mode
├── discord             Discord Gateway
├── sms                 SMS send-only (Twilio / Vonage)
├── imessage            BlueBubbles-backed iMessage bridge
├── email               IMAP inbound + SMTP outbound
├── mcp                 MCP JSON-RPC 2.0 server over stdio
├── cron                Manage scheduled prompts
├── session             Inspect / delete session store
├── skills              List / show / lint skills
├── doctor              Diagnose the local installation
├── status              Print daemon status
├── init                Write a default config to ~/.config/rousseau/
└── version             Print version, commit, build date
```

## `rousseau chat`

Open the interactive Bubble Tea TUI.

| Flag | Type | Default | Notes |
|---|---|---|---|
| `--session` | string | — | Resume an existing session by ID. |
| `--title` | string | timestamp | Title for a new session. |

## `rousseau whatsapp`

Run the WhatsApp bridge. Prints a QR code on first launch.

| Flag | Type | Default | Notes |
|---|---|---|---|
| `--store` | string | `$XDG_DATA_HOME/rousseau/whatsapp.db` | Path to the whatsmeow device store. |
| `--allow` | []string | none | Restrict inbound handling to these JIDs. Repeatable. **Never leave empty on a public number.** |

## `rousseau signal`

Run the Signal bridge. Spawns `signal-cli jsonRpc` as a subprocess.

| Flag | Type | Default | Notes |
|---|---|---|---|
| `--account` | string | from `signal.account` | E.164 phone number the daemon runs as. |
| `--binary` | string | `signal-cli` | Path to the signal-cli executable. |
| `--allow` | []string | none | Restrict inbound to these E.164 numbers. |

## `rousseau telegram`

Run the Telegram Bot API long-poller.

| Flag | Type | Default | Notes |
|---|---|---|---|
| `--token` | string | from `telegram.token` | BotFather token. |
| `--allow` | []string | none | Restrict inbound to these chat IDs. |

## `rousseau matrix`

Run the Matrix bridge.

| Flag | Type | Default | Notes |
|---|---|---|---|
| `--homeserver-url` | string | from config | e.g. `https://matrix.org`. |
| `--access-token` | string | from config | Bot's access token. |
| `--user-id` | string | from config | Bot's Matrix user ID (`@bot:matrix.org`). |
| `--allow` | []string | none | Restrict inbound to these user IDs. |

## `rousseau slack`

Run the Slack Socket Mode bridge.

| Flag | Type | Default | Notes |
|---|---|---|---|
| `--app-token` | string | from config | `xapp-...` Socket Mode token. |
| `--bot-token` | string | from config | `xoxb-...` Bot User OAuth token. |
| `--allow` | []string | none | Restrict inbound to these Slack user IDs. |

## `rousseau discord`

Run the Discord Gateway bridge.

| Flag | Type | Default | Notes |
|---|---|---|---|
| `--token` | string | from config | Bot token. |
| `--allow` | []string | none | Restrict inbound to these Discord user IDs. |

## `rousseau sms`

Send-only SMS via Twilio or Vonage. No inbound.

| Flag | Type | Default | Notes |
|---|---|---|---|
| `--provider` | string | from config | `twilio` or `vonage`. |
| `--from` | string | from config | E.164 sender number. |
| `--account-sid` | string | from config | Twilio Account SID. |
| `--auth-token` | string | from config | Twilio auth token or Vonage secret. |
| `--api-key` | string | from config | Vonage API key. |

## `rousseau imessage`

BlueBubbles-backed iMessage bridge.

| Flag | Type | Default | Notes |
|---|---|---|---|
| `--base-url` | string | `http://localhost:1234` | BlueBubbles server URL. |
| `--password` | string | from config | BlueBubbles server password. |
| `--chat-guid` | string | from config | Outbound target. |
| `--poll-interval` | duration | 5s | How often to poll for new messages. |
| `--allow` | []string | none | Restrict inbound. |

## `rousseau email`

Email bridge over IMAP + SMTP.

| Flag | Type | Default | Notes |
|---|---|---|---|
| `--imap-addr` | string | from config | e.g. `imap.example.com:993`. |
| `--imap-username`, `--imap-password` | string | from config | IMAP credentials. |
| `--smtp-addr` | string | from config | e.g. `smtp.example.com:587`. |
| `--smtp-username`, `--smtp-password` | string | from config | SMTP credentials. |
| `--from` | string | from config | Envelope sender. |
| `--poll-interval` | duration | 30s | IMAP poll cadence. |
| `--allow` | []string | none | Restrict inbound sender addresses. |

## `rousseau mcp`

Start the MCP server on stdio. No flags — every knob lives in `config.yaml`.

## `rousseau cron`

| Subcommand | Description |
|---|---|
| `cron add` | Add a scheduled prompt. Flags: `--name`, `--schedule` (5-field cron), `--prompt`, `--deliver-to`. |
| `cron list` | List every job with `on/off` status and last-run timestamp. |
| `cron remove <name-or-id>` | Delete a job. |
| `cron enable <name-or-id>` | Enable a disabled job. |
| `cron disable <name-or-id>` | Disable an enabled job (without deleting). |

## `rousseau session`

| Subcommand | Description |
|---|---|
| `session list` | List sessions in the store, newest first. |
| `session search <query>` | FTS5 search across every session's message content. |
| `session show <id>` | Print a session's message history. |
| `session delete <id>` | Delete a session. |

## `rousseau skills`

| Subcommand | Description |
|---|---|
| `skills list` | List discovered skills from `skills_dir`. |
| `skills show <name>` | Print a skill's YAML front-matter and body. |
| `skills lint` | Validate skills for schema conformance. |

## `rousseau doctor`

Walk every runtime dependency and every config choice. Prints a status report with rows tagged `ok`, `warn`, `fail`, `info`. Exit code 1 if any row is `fail`.

No flags today; extend via `--config` at the global level.

## `rousseau status`

Print a compact daemon-status summary — provider, session count, cron jobs. Read-only.

## `rousseau init`

Write a default `config.yaml` to `~/.config/rousseau/`. Refuses to overwrite an existing file unless `--force` is passed.

| Flag | Type | Default | Notes |
|---|---|---|---|
| `--force` | bool | false | Overwrite an existing config. |

## `rousseau version`

Print version, commit hash, and build date. Stamped at build time via `-ldflags`.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Command completed successfully. |
| 1 | Command failed. Error is printed to stderr. |

See [Reference: Exit Codes](/reference/exit-codes/) for the daemon signal semantics.

## Environment variables

Every config field can be overridden by an environment variable using the `ROUSSEAU_` prefix and `_` as the section separator: `ROUSSEAU_LOG_LEVEL=debug`, `ROUSSEAU_ANTHROPIC_API_KEY=sk-ant-...`, etc.

The special case is `ANTHROPIC_API_KEY` (without prefix) — it is picked up directly by the config loader to match convention.

## Troubleshooting

### `unknown command` when passing a subcommand

Rousseau's subcommands are declared in `internal/cli/root.go`. If `rousseau <cmd>` reports unknown, either the flag is misspelled or you are on an older binary. `rousseau version` shows what you have.

### Repeatable flags need multiple invocations

`--allow` accepts one JID per flag. Repeat the flag for multiple values: `--allow A --allow B`, not `--allow A,B`.

### Env vars silently ignored

Rousseau uses `ROUSSEAU_` prefix + underscore section separator: `anthropic.model` becomes `ROUSSEAU_ANTHROPIC_MODEL`. Case matters.

### `rousseau chat` shows only a blank screen

The Bubble Tea TUI needs an ANSI-capable terminal. Set `TERM=xterm-256color` and run interactively (not under `nohup` or a pipe).

### Command exits 0 immediately

Some flags (`--help`, `--version` variants) short-circuit. If your command doesn't run, check the flags you passed.

## Related pages

- [User Guide: TUI](/user-guide/tui/) — keybindings inside `rousseau chat`.
- [User Guide: Tools](/user-guide/tools/) — every built-in tool's JSON schema.
- [Reference: CLI Commands](/reference/cli-commands/) — command table.
- [Reference: Environment Variables](/reference/environment-variables/) — override matrix.
- [Configuration](/configuration/) — the config file backing every command.

## Further reading

- `internal/cli/root.go` — the Cobra tree.
- `internal/cli/chat.go`, `internal/cli/whatsapp.go`, `internal/cli/slack.go`, … — one file per subcommand.
- `internal/config/config.go` — env var / flag resolution.
