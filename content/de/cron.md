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
changefreq: "weekly"
description: "rousseau-agent's cron scheduler runs stored jobs on a schedule and delivers replies through any registered transport. Backed by robfig/cron/v3 and SQLite job persistence."
keywords: "cron, robfig/cron, scheduler, scheduled jobs, delivery, transport-agnostic, SQLite persistence"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/cron/"
subtitle: "Persistente Zeitplan-Jobs, die über jeden Transport ausgeliefert werden."
tags: "cron, scheduler, reference"
title: "Cron-Planer"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, robfig/cron, scheduler, scheduled jobs, delivery, transport-agnostic, SQLite persistence"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Cron-Planer"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 24
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/cron/index.html"
item_link: "https://docs.rousseau-agent.dev/cron/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Cron-Planer"
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
twitter_description: "rousseau-agent's cron scheduler runs stored jobs on a schedule and delivers replies through any registered transport. Backed by robfig/cron/v3 and SQLite job persistence."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Cron-Planer"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Danke an jeden Operator, der seinen eigenen Coding-Agenten betreibt."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Überblick

Der Cron-Scheduler (`internal/cron/scheduler.go`) ist eine Goroutine, die gespeicherte `CronJob`-Einträge zu ihrem konfigurierten Zeitplan ausführt, den Prompt jedes Jobs durch den Agent laufen lässt und die Antwort einer transport-agnostischen `Delivery`-Funktion übergibt.

Der Scheduler läuft neben einem beliebigen Langzeit-Daemon (typischerweise `rousseau whatsapp` oder einem anderen Chat-Transport). Jobs werden in derselben SQLite-Datenbank wie die Sessions gespeichert und überleben somit Neustarts.

## Zeitplan-Syntax

Basiert auf [robfig/cron/v3](https://pkg.go.dev/github.com/robfig/cron/v3). Der Parser unterstützt:

- Standard-Cron mit 5 Feldern: `<minute> <hour> <day-of-month> <month> <day-of-week>`.
- Vordefinierte Kurzformen: `@yearly`, `@monthly`, `@weekly`, `@daily`, `@hourly`, `@every <duration>`.

Beispiel-Zeitpläne:

| Ausdruck | Feuert |
|---|---|
| `0 9 * * 1-5` | 09:00 an Werktagen |
| `*/15 * * * *` | Alle 15 Minuten |
| `@daily` | Einmal täglich um Mitternacht (Serverzeitzone) |
| `@every 30m` | Alle 30 Minuten |

## CLI

```sh
# Alle gespeicherten Jobs auflisten.
rousseau cron list

# Job hinzufügen.
rousseau cron add \
  --name morning-standup \
  --schedule '0 9 * * 1-5' \
  --prompt 'What are the top three engineering priorities today?' \
  --target '447900123456@s.whatsapp.net'

# Über Name oder ID entfernen.
rousseau cron remove morning-standup
```

## Konfiguration

Jobs liegen in der State-DB, nicht in der Konfigurationsdatei. In `~/.config/rousseau/config.yaml` gibt es nichts, um den Scheduler selbst zu konfigurieren; er verwendet den Default `PollInterval = 60s`.

## Job-Ablauf

1. Der Scheduler synchronisiert die Job-Liste alle `PollInterval` aus SQLite.
2. `robfig/cron/v3` feuert den Job zum geplanten Zeitpunkt.
3. `TurnRunner.RunOnce(ctx, job.Prompt)` führt einen **Single-Turn**-Agent-Lauf gegen eine frische Session aus (keine Historie, kein Cross-Session-Recall, sofern der Runner das nicht ausdrücklich aktiviert).
4. Der Antworttext wird an `Delivery(ctx, job.Target, replyText)` übergeben.
5. Liefert `Delivery` einen Fehler → wird geloggt; der nächste Tick versucht es erneut.

## Delivery

`Delivery` ist ein kleiner Funktionstyp:

```go
type Delivery func(ctx context.Context, target, body string) error
```

Der Scheduler importiert `internal/transport` nicht — der Zustellvertrag ist transport-agnostisch. In der Praxis verdrahten die `rousseau <transport>`-Daemons ein `Delivery`, das den Ziel-String gegen den aktiven Transport auflöst (`Deliver` am Transport-Client).

`target` ist transportspezifisch:

- WhatsApp: eine JID (`447900123456@s.whatsapp.net`).
- Telegram: eine numerische Chat-ID.
- Slack: eine Kanal-ID (`C012345`) oder Benutzer-ID (`U012345`).
- Discord: eine Kanal-ID.
- SMS: ein E.164-Ziel.
- iMessage: eine Chat-GUID.
- Signal: ein E.164-Ziel.
- Matrix: eine Room-ID.
- Email: eine vollständige RFC-5322-Adresse.

## Persistenz

Jobs werden in der Tabelle `cron_jobs` der State-Datenbank (`internal/state/sqlite/`) gespeichert. Felder: `id`, `name`, `schedule`, `prompt`, `target`, `created_at`, `updated_at`. Neustarts nehmen jeden Job beim nächsten `PollInterval` wieder auf.

Über `rousseau cron add` hinzugefügte Jobs werden innerhalb eines `PollInterval` aktiv — standardmäßig bis zu 60 Sekunden.

## Zusammenspiel mit Transports

Die `Delivery`-Closure hält eine Referenz auf den laufenden Transport. Ein einzelner Daemon betreibt typischerweise einen Transport, sodass der Cron-Scheduler über diesen Transport zustellt. Multi-Transport-Deployments betreiben je einen Daemon pro Transport, und der Operator richtet `target` jedes Cron-Jobs auf den Daemon des passenden Transports.

Cross-Transport-Zustellung (Job läuft im WhatsApp-Daemon, antwortet aber via Slack) wird derzeit nicht unterstützt — der Scheduler kennt nur das ihm übergebene `Delivery`.

## Fehlerbilder

| Symptom | Behebung |
|---|---|
| Job feuert nicht | `rousseau status` prüfen; der Scheduler loggt `cron.fired` pro Aktivierung. |
| Job feuert, es kommt aber nichts an | Zustellfehler — Logs auf `cron.delivery_failed` prüfen. |
| Job läuft, doch das Modell verweigert das Handeln | Genehmigungsrichtlinie verweigert Tool-Aufrufe. `agent.approver` lockern oder in den Modus `pattern` wechseln. |
| Zustellung geht ans falsche Ziel | Der Scheduler ist transport-agnostisch; der Daemon interpretiert `target`. Sicherstellen, dass der aktive Transport des Daemons zum Zielformat passt. |
