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
hreflang: "de"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "de"
locale: "de_DE"
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
permalink: "https://docs.rousseau-agent.dev/de/reference/logs/"
subtitle: "The full vocabulary of slog messages rousseau emits."
tags: "reference, logs, slog, observability, audit"
title: "Referenz: Logs"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "slog, logs, json, text, journalctl, jq, observability"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Referenz: Logs"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 52
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/logs/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/logs/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Referenz: Logs"
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
twitter_title: "Referenz: Logs"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Danke an jeden Operator, der seinen eigenen Coding-Agenten betreibt."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Logger-Einrichtung

`internal/cli/root.go` baut einen `*slog.Logger` pro Prozess — einen `slog.NewTextHandler`, wenn `log.format` leer oder `text` ist, einen `slog.NewJSONHandler`, wenn es `json` ist. Das Level wird aus `log.level` abgebildet (`debug`, `info`, `warn`/`warning`, `error`), mit `info` als Standard. Der Handler schreibt nach stderr; jeder Daemon erbt ihn.

Für eine Produktionsbereitstellung setzen Sie immer `log.format: json`. Nachgelagerte Log-Pipelines (journald + `journalctl -o json`, Loki, Vector, Datadog Agent) parsen strukturierte Ausgabe nativ.

## Ausgabeform

### Text

```
time=2026-07-13T18:00:14.202Z level=INFO msg=tool.execute name=grep id=t_1
```

Slogs Standard-Text-Layout: `time`, `level`, `msg`, dann Schlüssel=Wert-Paare.

### JSON

```json
{"time":"2026-07-13T18:00:14.202Z","level":"INFO","msg":"tool.execute","name":"grep","id":"t_1"}
```

Dieselben Felder, JSON-kodiert. Das `msg`-Feld ist der stabile Ereignisbezeichner — filtern und alarmieren Sie darauf, nicht auf menschlichem Text.

## Nachrichten-Vokabular

Jeder Nachrichtenname, der von `internal/**/*.go` emittiert wird, ist unten mit Quellort und erwartetem Level aufgelistet. Nach Subsystem gruppiert; innerhalb einer Gruppe alphabetisiert.

### Agent-Schleife (`internal/agent/`)

| Nachricht | Level | Felder | Bedeutung |
|---|---|---|---|
| `agent.compressed` | INFO | `messages` | LLM-Compressor hat eine Sitzung neu geschrieben; die neue Nachrichtenzahl ist `messages`. |
| `agent.compress_failed` | WARN | `err` | Der Compressor hat einen Fehler zurückgegeben; die Sitzung bleibt unangetastet. |
| `tool.denied` | WARN | `name`, `reason` | Approver hat einen Tool-Aufruf blockiert. Felder aus `internal/agent/agent.go:179`. |
| `tool.execute` | INFO | `name`, `id` | Der Approver hat erlaubt und das Tool lief. |
| `tool.error` | WARN | `name`, `err` | Das Tool lief, gab aber einen Fehler zurück. |
| `turn.failed` | ERROR | `err` | Der TUI-Turn hat einen Fehler geworfen. Emittiert aus `internal/tui/model.go`. |
| `session.save_failed` | WARN | `err` | Persistieren einer Sitzung nach dem Turn ist fehlgeschlagen. |

### Cron (`internal/cron/scheduler.go`)

| Nachricht | Level | Felder | Bedeutung |
|---|---|---|---|
| `cron.started` | INFO | `poll_interval` | Scheduler-Start. |
| `cron.scheduled` | INFO | `job`, `expr` | Job zum In-Memory-Zeitplan hinzugefügt. |
| `cron.schedule_failed` | WARN | `job`, `expr`, `err` | robfig/cron/v3 hat den Ausdruck abgelehnt. |
| `cron.sync_failed` | WARN | `err` | Reconcile-Durchlauf gegen `cron_jobs` ist fehlgeschlagen. |
| `cron.firing` | INFO | `job` | Job wird gleich ausgeführt. |
| `cron.completed` | INFO | `job` | Job wurde erfolgreich beendet. |
| `cron.run_failed` | ERROR | `job`, `err` | Provider-Aufruf innerhalb des Jobs ist fehlgeschlagen. |
| `cron.delivery_failed` | ERROR | `job`, `target`, `err` | Zustellung zum Transport ist fehlgeschlagen. |
| `cron.record_failed` | WARN | `job`, `err` | Schreiben von `last_run_at` ist fehlgeschlagen. |

### MCP (`internal/mcp/server.go`)

| Nachricht | Level | Felder | Bedeutung |
|---|---|---|---|
| `mcp.encode_error` | WARN | `err` | Konnte eine Antwort nicht JSON-kodieren (selten). |
| `mcp.tool_error` | WARN | `tool`, `err` | Ein Tool-Handler hat einen Fehler zurückgegeben; dem Host mit `isError=true` präsentiert. |

### Router (`internal/transport/router.go`)

| Nachricht | Level | Felder | Bedeutung |
|---|---|---|---|
| `transport.rejected` | WARN | `from` | Absender nicht in der Allowlist; Nachricht verworfen. |
| `router.save_failed` | WARN | `err` | Sitzungs-Speichern nach dem Turn ist fehlgeschlagen. |
| `router.stale_mapping` | WARN | `jid`, `err` | JID→Session-Zuordnung zeigte auf eine Sitzung, die nicht mehr lädt. |

### WhatsApp (`internal/transport/whatsapp/`)

| Nachricht | Level | Felder | Bedeutung |
|---|---|---|---|
| `whatsapp.starting` | INFO | `store`, `allowlist` | Bridge startet; `store` ist die DSN. |
| `whatsapp.qr_ready` | INFO | — | QR nach stdout gerendert; scannen Sie ihn. |
| `whatsapp.qr_event` | WARN | `event` | Nicht-Erfolgs-QR-Ereignis von whatsmeow. |
| `whatsapp.paired` | INFO | — | Telefon hat den QR akzeptiert. |
| `whatsapp.connected` | INFO | — | WebSocket zu Meta ist oben. |
| `whatsapp.disconnected` | WARN | — | Socket verloren. Automatisches Wiederverbinden. |
| `whatsapp.logged_out` | ERROR | `reason` | Meta hat das Gerät ausgeloggt — meist ein Policy-Trip. |
| `whatsapp.voice_enabled` | INFO | `binary`, `model` | Voice-Note-Transkription ist an. |
| `whatsapp.incoming` | INFO | `from` | Inbound-Nachricht akzeptiert. |
| `whatsapp.skipped` | DEBUG | `reason` | Router hat eine Nachricht verworfen (Self-Echo etc). |
| `whatsapp.empty_reply` | INFO | `elapsed` | Der Agent hat in diesem Turn keinen Text produziert. |
| `whatsapp.handler_ok` | INFO | `elapsed`, `bytes` | Antwort ausgeliefert. |
| `whatsapp.handler_failed` | ERROR | `err` | Turn hat einen Fehler geworfen — meist ein Provider- oder Tool-Fehler. |
| `whatsapp.send_failed` | ERROR | `err` | Auslieferung an Meta ist fehlgeschlagen. |
| `whatsapp.presence_failed` | DEBUG | `err` | Schreiben der Typing-Presence ist fehlgeschlagen (Best-Effort). |
| `whatsapp.audio_ignored` | INFO | `size` | Sprachnotiz empfangen, aber Transkription ist deaktiviert. |
| `whatsapp.audio_downloaded` | INFO | `size` | Sprachnotiz-Bytes von Meta geladen. |
| `whatsapp.transcribed` | INFO | `elapsed` | whisper.cpp hat ein Transkript zurückgegeben. |
| `whatsapp.transcribe_failed` | ERROR | `err` | whisper-Aufruf ist fehlgeschlagen. |

### Slack (`internal/transport/slack/client.go`)

| Nachricht | Level | Felder | Bedeutung |
|---|---|---|---|
| `slack.starting` | INFO | `allowlist` | Bridge startet. |
| `slack.started` | INFO | — | Socket-Mode-Sitzung akzeptiert. |
| `slack.session_failed` | WARN | `err` | Öffnen der Socket-Mode-Sitzung fehlgeschlagen; Wiederholen. |
| `slack.frame_failed` | WARN | `err` | Fehlerhafter Frame von Slack. |
| `slack.incoming` | INFO | `from`, `channel`, `text` | Nachricht akzeptiert. |
| `slack.handler_failed` | ERROR | `err` | Turn hat einen Fehler geworfen. |

### Discord (`internal/transport/discord/client.go`)

| Nachricht | Level | Felder | Bedeutung |
|---|---|---|---|
| `discord.starting` | INFO | `allowlist` | Bridge startet. |
| `discord.ready` | INFO | `bot_id` | Discord-Gateway bereit. |
| `discord.started` | INFO | — | Sitzung oben. |
| `discord.session_failed` | WARN | `err` | Gateway-Öffnen fehlgeschlagen; Wiederholen. |
| `discord.frame_failed` | WARN | `err` | Schlechter Frame von Discord. |
| `discord.incoming` | INFO | `from`, `channel` | Nachricht akzeptiert. |
| `discord.handler_failed` | ERROR | `err` | Turn hat einen Fehler geworfen. |

### Telegram (`internal/transport/telegram/client.go`)

| Nachricht | Level | Felder | Bedeutung |
|---|---|---|---|
| `telegram.starting` | INFO | `allowlist` | Bridge startet. |
| `telegram.started` | INFO | — | Erster Long-Poll erfolgreich. |
| `telegram.poll_failed` | WARN | `err` | Long-Poll-HTTP ist fehlgeschlagen. |
| `telegram.incoming` | INFO | `from` | Nachricht akzeptiert. |
| `telegram.handler_failed` | ERROR | `err` | Turn hat einen Fehler geworfen. |
| `telegram.send_failed` | ERROR | `err` | Outbound-HTTP ist fehlgeschlagen. |

### Matrix (`internal/transport/matrix/client.go`)

| Nachricht | Level | Felder | Bedeutung |
|---|---|---|---|
| `matrix.starting` | INFO | `homeserver`, `allowlist` | Bridge startet. |
| `matrix.started` | INFO | `homeserver` | Erstes `/sync` akzeptiert. |
| `matrix.sync_failed` | WARN | `err` | `/sync`-HTTP ist fehlgeschlagen. |
| `matrix.incoming` | INFO | `from`, `room` | Nachricht akzeptiert. |
| `matrix.handler_failed` | ERROR | `err` | Turn hat einen Fehler geworfen. |
| `matrix.send_failed` | ERROR | `err` | Outbound-HTTP ist fehlgeschlagen. |

### Signal (`internal/transport/signal/`)

| Nachricht | Level | Felder | Bedeutung |
|---|---|---|---|
| `signal.starting` | INFO | `account`, `allowlist` | signal-cli-JSON-RPC-Subprozess startet. |
| `signal.started` | INFO | — | Subprozess hat Bereitschaft gemeldet. |
| `signal.frame_failed` | WARN | `err` | Fehlerhafter JSON-Frame von signal-cli. |
| `signal.stderr` | WARN | `line` | Passthrough von signal-cli-stderr. |
| `signal.incoming` | INFO | `from` | Nachricht akzeptiert. |
| `signal.handler_failed` | ERROR | `err` | Turn hat einen Fehler geworfen. |

### iMessage (`internal/transport/imessage/client.go`)

| Nachricht | Level | Felder | Bedeutung |
|---|---|---|---|
| `imessage.starting` | INFO | `base` | BlueBubbles-Server-URL geloggt. |
| `imessage.started` | INFO | `server` | Erster Poll erfolgreich. |
| `imessage.prime_failed` | WARN | `err` | Priming-State-Abruf fehlgeschlagen; Wiederholen. |
| `imessage.poll_failed` | WARN | `err` | Poll-HTTP ist fehlgeschlagen. |
| `imessage.incoming` | INFO | `from` | Nachricht akzeptiert. |
| `imessage.handler_failed` | ERROR | `err` | Turn hat einen Fehler geworfen. |
| `imessage.send_failed` | ERROR | `err` | Outbound-HTTP ist fehlgeschlagen. |

### E-Mail + SMS (`internal/transport/email/`, `internal/transport/sms/`)

Folgt derselben `<transport>.starting / .started / .poll_failed / .incoming / .handler_failed / .send_failed`-Form wie die pollenden Transporte oben.

## Rezepte

### Zeige jeden fehlgeschlagenen Tool-Aufruf von heute

```sh
journalctl --user -u rousseau-agent --since today -o json \
  | jq -c 'select(.MESSAGE | fromjson? | .msg == "tool.denied")'
```

### Einer einzelnen Transport-Sitzung live folgen

```sh
journalctl --user -u rousseau-agent -f -o cat \
  | grep -E 'whatsapp\.|tool\.|cron\.'
```

### Alarm bei Cron-Fehlern

Prometheus/alertmanager-Regel-Skizze (via die `promtail` → Loki → Alert-Pipeline in [Leitfäden: Observability](/de/guides/observability/)):

```yaml
- alert: RousseauCronFailure
  expr: |
    sum by (job) (
      count_over_time({app="rousseau-agent"} |= "cron.run_failed" [5m])
    ) > 0
```

### Redaktion

`slog` redigiert standardmäßig nicht. Konfigurieren Sie einen nachgelagerten Prozessor, der `err`-Felder bei `whatsapp.send_failed`, `tool.error` etc. redigiert — Provider-Fehler können gelegentlich Prompt-Fragmente enthalten. Siehe [Leitfäden: Observability](/de/guides/observability/) für die Pipeline.

## Verwandt

- [Benutzerleitfaden: Freigaberichtlinien](/de/user-guide/approval-policies/) — die Quelle von `tool.denied`.
- [Leitfäden: Observability](/de/guides/observability/) — vollständiges Pipeline-Rezept.
- [Leitfäden: Audit + Freigaberichtlinien](/de/guides/audit-approval-policies/) — behandeln Sie diese Logs als Audit-Trail.
