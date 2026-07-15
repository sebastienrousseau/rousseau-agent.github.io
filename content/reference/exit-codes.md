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
description: "Exit codes and signal semantics for the rousseau-agent binary. What init systems can rely on."
keywords: "exit codes, signals, sigterm, sigint, systemd, restart policy"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/exit-codes/"
subtitle: "Exit codes and signal semantics."
tags: "reference, exit-codes, signals"
title: "Exit Codes"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "exit codes, signals, sigterm, sigint, systemd, restart policy"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Exit Codes"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 51
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/exit-codes/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/exit-codes/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Exit Codes"
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
twitter_description: "Exit codes and signal semantics for the rousseau-agent binary. What init systems can rely on."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Exit Codes"
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

## Exit codes

Rousseau's CLI is deliberately conservative — two exit codes cover every path.

| Code | Emitted by | Meaning |
|---|---|---|
| 0 | `cmd/rousseau/main.go` via `cli.Execute` | Command completed successfully. Daemons exit 0 on graceful shutdown (SIGINT / SIGTERM). |
| 1 | `cmd/rousseau/main.go` via `cli.Execute` | Command failed. The error string is printed to stderr. Every failure — config parse error, provider auth failure, transport panic, tool wiring error — maps to this code. |

`rousseau doctor` follows the same convention: exit 0 when every check passes, exit 1 when any check is `fail`. Warnings and info-level rows do not affect the exit code.

Future releases may split failures into distinct codes (config vs runtime vs network). Today, treat any non-zero exit as retryable but requiring log inspection.

## Signal handling

`cmd/rousseau/main.go` installs a signal handler that cancels the root `context.Context` on `SIGINT` and `SIGTERM`. Every long-lived component (agent loop, transport, cron scheduler, MCP server) honours context cancellation, so the shutdown path is:

1. `SIGINT` / `SIGTERM` received.
2. Root context is cancelled.
3. Transports call `Stop()` on themselves, flushing in-flight messages.
4. Cron scheduler stops accepting new fires; running fires complete.
5. Session store `Close()` is called via `defer`, checkpointing the WAL.
6. `Execute` returns 0.

`SIGKILL` cannot be caught. If the daemon is `kill -9`'d mid-turn, the session store's WAL protects against corruption but the in-flight turn is not persisted. The next launch resumes from the last saved state.

## systemd restart policy

For the reference Quadlet unit:

```
[Service]
Restart=on-failure
RestartSec=10
```

`on-failure` restarts on any non-zero exit; combined with rousseau's exit code convention this means: exit 0 (`SIGTERM` from `systemctl stop`) does not restart, exit 1 does.

For daemons that hit persistent errors (bad config, wrong provider auth), `on-failure` will thrash. Watch `journalctl` for the failure reason before assuming the retry loop will recover.

## Kubernetes probe semantics

Rousseau ships no HTTP liveness/readiness endpoint by design. Kubernetes probes must be either:

- `exec` probes running `rousseau doctor --config /etc/rousseau/config.yaml` (returns 0 on healthy, 1 on failure), or
- Absent, with the pod relying on `restartPolicy: Always` and the daemon's own error handling.

`rousseau doctor` is cheap (~50ms) so it is a fine liveness probe. Do not use it as a readiness probe — a `fail` on `provider.claudecli.binary` shouldn't take the pod out of rotation if the failure will not self-heal.

## Handled errors

Errors that produce exit code 1 by way of the CLI error surface include:

- **Config load failure** — YAML parse error, unknown field, invalid type.
- **Provider auth failure** — missing API key, invalid credentials, invalid Bedrock / Vertex region.
- **Transport startup failure** — missing token, unreachable IMAP/SMTP host, whatsmeow protocol error.
- **Store open failure** — permission denied on `~/.local/share/rousseau/`, disk full.
- **Doctor check failure** — any `fail` row makes doctor return exit 1.
- **Cron cron-expression parse failure** — `rousseau cron add` validates before persisting.

## Unhandled panics

`go test -race` is run on every CI build, so panics are extremely rare. When they do happen, the Go runtime prints the panic + stack trace to stderr and exits with a non-zero code from the runtime — typically 2, but this is Go's convention and not something rousseau controls.

For production, wrap the daemon in a supervisor that captures stderr on abnormal exit and reports the trace.

## Next

- [User Guide: CLI](/user-guide/cli/) — every command.
- [Guides: Observability](/guides/observability/) — surface the slog signal beyond the exit code.
- [Troubleshooting](/troubleshooting/) — what to do when the exit code is not enough.
