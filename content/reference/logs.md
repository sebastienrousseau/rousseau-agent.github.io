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
description: "rousseau-agent's slog output: message vocabulary, JSON vs text shape, and journalctl / jq recipes."
keywords: "slog, logs, json, text, journalctl, jq, observability"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/logs/"
subtitle: "The full vocabulary of slog messages rousseau emits."
tags: "reference, logs, slog, observability, audit"
title: "Reference: Logs"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "slog, logs, json, text, journalctl, jq, observability"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Reference: Logs"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 52
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/logs/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/logs/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Reference: Logs"
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
twitter_description: "rousseau-agent's slog output: message vocabulary, JSON vs text shape, and journalctl / jq recipes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Reference: Logs"
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

## Logger setup

`internal/cli/root.go` builds one `*slog.Logger` per process — a `slog.NewTextHandler` when `log.format` is empty or `text`, a `slog.NewJSONHandler` when it is `json`. Level maps from `log.level` (`debug`, `info`, `warn`/`warning`, `error`) with `info` as the default. Handler writes to stderr; every daemon inherits it.

For a production deployment, always set `log.format: json`. Downstream log pipelines (journald + `journalctl -o json`, Loki, Vector, Datadog Agent) parse structured output natively.

## Output shape

### Text

```
time=2026-07-13T18:00:14.202Z level=INFO msg=tool.execute name=grep id=t_1
```

Slog's default text layout: `time`, `level`, `msg`, then key=value pairs.

### JSON

```json
{"time":"2026-07-13T18:00:14.202Z","level":"INFO","msg":"tool.execute","name":"grep","id":"t_1"}
```

Same fields, JSON encoded. The `msg` field is the stable event identifier — filter and alert on it, not on human text.

## Message vocabulary

Every message name emitted from `internal/**/*.go` is listed below with source location and expected level. Grouped by subsystem; alphabetised within a group.

### Agent loop (`internal/agent/`)

| Message | Level | Fields | Meaning |
|---|---|---|---|
| `agent.compressed` | INFO | `messages` | LLM compressor rewrote a session; the new message count is `messages`. |
| `agent.compress_failed` | WARN | `err` | The compressor returned an error; the session is left untouched. |
| `tool.denied` | WARN | `name`, `reason` | Approver blocked a tool call. Fields from `internal/agent/agent.go:179`. |
| `tool.execute` | INFO | `name`, `id` | The approver allowed and the tool ran. |
| `tool.error` | WARN | `name`, `err` | The tool ran but returned an error. |
| `turn.failed` | ERROR | `err` | The TUI turn errored. Emitted from `internal/tui/model.go`. |
| `session.save_failed` | WARN | `err` | Persisting a session failed post-turn. |

### Cron (`internal/cron/scheduler.go`)

| Message | Level | Fields | Meaning |
|---|---|---|---|
| `cron.started` | INFO | `poll_interval` | Scheduler boot. |
| `cron.scheduled` | INFO | `job`, `expr` | Job added to the in-memory schedule. |
| `cron.schedule_failed` | WARN | `job`, `expr`, `err` | robfig/cron/v3 rejected the expression. |
| `cron.sync_failed` | WARN | `err` | Reconcile pass against `cron_jobs` failed. |
| `cron.firing` | INFO | `job` | Job is about to run. |
| `cron.completed` | INFO | `job` | Job finished successfully. |
| `cron.run_failed` | ERROR | `job`, `err` | Provider call inside the job failed. |
| `cron.delivery_failed` | ERROR | `job`, `target`, `err` | Delivery to the transport failed. |
| `cron.record_failed` | WARN | `job`, `err` | Writing `last_run_at` failed. |

### MCP (`internal/mcp/server.go`)

| Message | Level | Fields | Meaning |
|---|---|---|---|
| `mcp.encode_error` | WARN | `err` | Could not JSON-encode a response (rare). |
| `mcp.tool_error` | WARN | `tool`, `err` | A tool handler returned an error; surfaced to the host with `isError=true`. |

### Router (`internal/transport/router.go`)

| Message | Level | Fields | Meaning |
|---|---|---|---|
| `transport.rejected` | WARN | `from` | Sender not in the allowlist; message dropped. |
| `router.save_failed` | WARN | `err` | Post-turn session save failed. |
| `router.stale_mapping` | WARN | `jid`, `err` | JID→session mapping pointed at a session that no longer loads. |

### WhatsApp (`internal/transport/whatsapp/`)

| Message | Level | Fields | Meaning |
|---|---|---|---|
| `whatsapp.starting` | INFO | `store`, `allowlist` | Bridge booting; `store` is the DSN. |
| `whatsapp.qr_ready` | INFO | — | QR rendered to stdout; scan it. |
| `whatsapp.qr_event` | WARN | `event` | Non-success QR event from whatsmeow. |
| `whatsapp.paired` | INFO | — | Phone accepted the QR. |
| `whatsapp.connected` | INFO | — | WebSocket to Meta is up. |
| `whatsapp.disconnected` | WARN | — | Lost the socket. Retries automatically. |
| `whatsapp.logged_out` | ERROR | `reason` | Meta logged the device out — usually a policy trip. |
| `whatsapp.voice_enabled` | INFO | `binary`, `model` | Voice-note transcription is on. |
| `whatsapp.incoming` | INFO | `from` | Inbound message accepted. |
| `whatsapp.skipped` | DEBUG | `reason` | Router discarded a message (self-echo, etc). |
| `whatsapp.empty_reply` | INFO | `elapsed` | The agent produced no text this turn. |
| `whatsapp.handler_ok` | INFO | `elapsed`, `bytes` | Reply delivered. |
| `whatsapp.handler_failed` | ERROR | `err` | Turn errored — usually a provider or tool failure. |
| `whatsapp.send_failed` | ERROR | `err` | Delivery to Meta failed. |
| `whatsapp.presence_failed` | DEBUG | `err` | Typing-presence write failed (best-effort). |
| `whatsapp.audio_ignored` | INFO | `size` | Voice note received but transcription is disabled. |
| `whatsapp.audio_downloaded` | INFO | `size` | Voice-note bytes fetched from Meta. |
| `whatsapp.transcribed` | INFO | `elapsed` | whisper.cpp returned a transcript. |
| `whatsapp.transcribe_failed` | ERROR | `err` | whisper invocation failed. |

### Slack (`internal/transport/slack/client.go`)

| Message | Level | Fields | Meaning |
|---|---|---|---|
| `slack.starting` | INFO | `allowlist` | Bridge booting. |
| `slack.started` | INFO | — | Socket Mode session accepted. |
| `slack.session_failed` | WARN | `err` | Failed to open the Socket Mode session; retry. |
| `slack.frame_failed` | WARN | `err` | Malformed frame from Slack. |
| `slack.incoming` | INFO | `from`, `channel`, `text` | Message accepted. |
| `slack.handler_failed` | ERROR | `err` | Turn errored. |

### Discord (`internal/transport/discord/client.go`)

| Message | Level | Fields | Meaning |
|---|---|---|---|
| `discord.starting` | INFO | `allowlist` | Bridge booting. |
| `discord.ready` | INFO | `bot_id` | Discord gateway ready. |
| `discord.started` | INFO | — | Session up. |
| `discord.session_failed` | WARN | `err` | Gateway open failed; retry. |
| `discord.frame_failed` | WARN | `err` | Bad frame from Discord. |
| `discord.incoming` | INFO | `from`, `channel` | Message accepted. |
| `discord.handler_failed` | ERROR | `err` | Turn errored. |

### Telegram (`internal/transport/telegram/client.go`)

| Message | Level | Fields | Meaning |
|---|---|---|---|
| `telegram.starting` | INFO | `allowlist` | Bridge booting. |
| `telegram.started` | INFO | — | First long-poll succeeded. |
| `telegram.poll_failed` | WARN | `err` | Long-poll HTTP failed. |
| `telegram.incoming` | INFO | `from` | Message accepted. |
| `telegram.handler_failed` | ERROR | `err` | Turn errored. |
| `telegram.send_failed` | ERROR | `err` | Outbound HTTP failed. |

### Matrix (`internal/transport/matrix/client.go`)

| Message | Level | Fields | Meaning |
|---|---|---|---|
| `matrix.starting` | INFO | `homeserver`, `allowlist` | Bridge booting. |
| `matrix.started` | INFO | `homeserver` | First `/sync` accepted. |
| `matrix.sync_failed` | WARN | `err` | `/sync` HTTP failed. |
| `matrix.incoming` | INFO | `from`, `room` | Message accepted. |
| `matrix.handler_failed` | ERROR | `err` | Turn errored. |
| `matrix.send_failed` | ERROR | `err` | Outbound HTTP failed. |

### Signal (`internal/transport/signal/`)

| Message | Level | Fields | Meaning |
|---|---|---|---|
| `signal.starting` | INFO | `account`, `allowlist` | signal-cli JSON-RPC subprocess starting. |
| `signal.started` | INFO | — | Subprocess reported ready. |
| `signal.frame_failed` | WARN | `err` | Malformed JSON frame from signal-cli. |
| `signal.stderr` | WARN | `line` | Passthrough of signal-cli stderr. |
| `signal.incoming` | INFO | `from` | Message accepted. |
| `signal.handler_failed` | ERROR | `err` | Turn errored. |

### iMessage (`internal/transport/imessage/client.go`)

| Message | Level | Fields | Meaning |
|---|---|---|---|
| `imessage.starting` | INFO | `base` | BlueBubbles server URL logged. |
| `imessage.started` | INFO | `server` | First poll succeeded. |
| `imessage.prime_failed` | WARN | `err` | Priming state fetch failed; retries. |
| `imessage.poll_failed` | WARN | `err` | Poll HTTP failed. |
| `imessage.incoming` | INFO | `from` | Message accepted. |
| `imessage.handler_failed` | ERROR | `err` | Turn errored. |
| `imessage.send_failed` | ERROR | `err` | Outbound HTTP failed. |

### Email + SMS (`internal/transport/email/`, `internal/transport/sms/`)

Follows the same `<transport>.starting / .started / .poll_failed / .incoming / .handler_failed / .send_failed` shape as the polling transports above.

## Recipes

### Show every failed tool call today

```sh
journalctl --user -u rousseau-agent --since today -o json \
  | jq -c 'select(.MESSAGE | fromjson? | .msg == "tool.denied")'
```

### Follow a single transport session live

```sh
journalctl --user -u rousseau-agent -f -o cat \
  | grep -E 'whatsapp\.|tool\.|cron\.'
```

### Alert on cron failures

Prometheus/alertmanager rule sketch (via the `promtail` → Loki → alert pipeline in [Guides: Observability](/guides/observability/)):

```yaml
- alert: RousseauCronFailure
  expr: |
    sum by (job) (
      count_over_time({app="rousseau-agent"} |= "cron.run_failed" [5m])
    ) > 0
```

### Redacting

`slog` does not redact by default. Configure a downstream processor to redact `err` fields on `whatsapp.send_failed`, `tool.error`, etc. — provider errors can occasionally include prompt fragments. See [Guides: Observability](/guides/observability/) for the pipeline.

## Related

- [User Guide: Approval Policies](/user-guide/approval-policies/) — the source of `tool.denied`.
- [Guides: Observability](/guides/observability/) — full pipeline recipe.
- [Guides: Audit + approval policies](/guides/audit-approval-policies/) — treat these logs as an audit trail.
