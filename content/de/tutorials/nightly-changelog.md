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
description: "Schedule a rousseau cron job that summarises git log every evening and posts the result to WhatsApp."
keywords: "cron, git log, changelog, whatsapp, scheduled prompt, deliver-to"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/tutorials/nightly-changelog/"
subtitle: "A daily 18:00 cron job that pushes a git-log summary to WhatsApp."
tags: "tutorials, cron, changelog, whatsapp, git"
title: "Tutorial: nächtliches Changelog"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, git log, changelog, whatsapp, scheduled prompt, deliver-to"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorial: nächtliches Changelog"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/nightly-changelog/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/nightly-changelog/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorial: nächtliches Changelog"
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
twitter_description: "Schedule a rousseau cron job that summarises git log every evening and posts the result to WhatsApp."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorial: nächtliches Changelog"
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

## Was Sie bauen

Ein Cron-Job, gespeichert im eigenen SQLite-Zustand von rousseau (Tabelle `cron_jobs`, Schema in `internal/state/sqlite/cron.go`), der werktags um 18:00 Uhr lokaler Zeit feuert. Er führt einen Prompt aus, der das Modell auffordert, `git log --since=today` zusammenzufassen, und liefert das Ergebnis über WhatsApp an Ihr Telefon.

Geschätzte Zeit: 10 Minuten.

## Voraussetzungen

- WhatsApp-Bridge bereits gekoppelt (siehe [Schnellstart](/de/quickstart/) Schritt 4 oder [Transporte: WhatsApp](/de/transports/whatsapp/)).
- Der `rousseau whatsapp`-Daemon läuft — der Cron-Scheduler in `internal/cron/scheduler.go` wird von Transport-Daemons via `wiring.startCron()` gestartet, nicht von `rousseau chat`.
- Ein Workspace, der das git-Repo enthält, das Sie zusammenfassen möchten, in den Container bind-gemountet (oder auf dem Host, wenn Sie rousseau außerhalb eines Containers betreiben).

## Wie rousseau cron funktioniert

`rousseau cron add` schreibt eine Zeile in die Tabelle `cron_jobs` (`internal/state/sqlite/cron.go`). Alle ~15 Sekunden liest `scheduler.sync` die Tabelle erneut und gleicht den robfig/cron/v3-In-Memory-Zeitplan ab. Wenn ein Job feuert, emittiert der Scheduler `cron.firing`, führt den Prompt über den konfigurierten Provider aus und liefert das Ergebnis über die Transport-Bridge, die den Prozess besitzt (WhatsApp in diesem Tutorial), an `deliver_to` aus.

Strukturierte Log-Namen, die Sie sehen werden (aus `internal/cron/scheduler.go`):

- `cron.started` — Scheduler mit `poll_interval=…` gestartet.
- `cron.scheduled` — ein Job wurde akzeptiert.
- `cron.firing` — ein Job wird gleich ausgeführt.
- `cron.completed` — ein Job wurde erfolgreich beendet.
- `cron.run_failed`, `cron.delivery_failed`, `cron.record_failed` — Fehlermodi.

## Schritt 1: Job hinzufügen

```sh
rousseau cron add \
  --name        nightly-changelog \
  --schedule    "0 18 * * 1-5" \
  --prompt      "Summarise git log --since=yesterday under /workspace/rousseau-agent as a Slack-style bullet list. Keep it under 200 words. If nothing changed, reply with a single line 'no commits'." \
  --deliver-to  447900123456@s.whatsapp.net
```

Der Cron-Ausdruck wird von `robfig/cron/v3` in `newCronAddCmd` (`internal/cli/cron.go`) geparst. Ungültige Ausdrücke werden vor dem Schreiben abgelehnt. Der `--deliver-to`-Wert ist die E.164-JID für WhatsApp (`<digits>@s.whatsapp.net`); das Zustellzielformat ist transportspezifisch.

## Schritt 2: verifizieren

```sh
rousseau cron list
```

Ausgabeform (aus `newCronListCmd`):

```
NAME               STATUS SCHEDULE       PROMPT                       DELIVER-TO
nightly-changelog  on     0 18 * * 1-5   Summarise git log …          447900123456@s.whatsapp.net
```

Die Liste wird auch über MCP als `rousseau_cron_list` (siehe `internal/mcp/tools.go`) exponiert.

## Schritt 3: Trockenlauf

Es gibt keinen eingebauten „jetzt feuern"-Trigger. Zum Smoke-Test planen Sie den Job vorübergehend eine Minute in der Zukunft:

```sh
rousseau cron remove nightly-changelog
rousseau cron add --name test --schedule "*/1 * * * *" --prompt "say hi" --deliver-to "$JID"
journalctl --user -u rousseau-agent -f | grep cron.
```

Erwartete Log-Sequenz:

```
INFO cron.scheduled  job=test expr=*/1 * * * *
INFO cron.firing     job=test
INFO cron.completed  job=test
```

Entfernen Sie den Test-Job und fügen Sie den echten wieder hinzu, wenn Sie fertig sind.

## Schritt 4: Prompt schärfen

Die besten Cron-Prompts sind eigenständig: Das Modell hat keine Erinnerung an vorherige Läufe. Fügen Sie den Repo-Pfad, das erwartete Ausgabeformat und einen Fallback für den leeren Fall ein. Beispielhafte zweite Iteration:

```
Summarise commits authored since 07:00 UTC today under
/workspace/rousseau-agent. Use this format:

- <short type>: <one-line summary> — <sha>

Group by author. If no commits landed, reply exactly: no commits.
```

## Umschalten und Entfernen

```sh
rousseau cron disable nightly-changelog   # keeps the row, stops firing
rousseau cron enable  nightly-changelog
rousseau cron remove  nightly-changelog   # deletes the row
```

`SetEnabled` und `Delete` aus `internal/state/sqlite/cron.go` sind das, was diese aufrufen.

## Verwandt

- [Cron](/de/cron/) — Referenz für den Scheduler.
- [Leitfäden: Geplante Aufgaben](/de/guides/scheduled-tasks/) — tiefere Diskussion.
- [Transporte: WhatsApp](/de/transports/whatsapp/) — wie delivery-to funktioniert.
- [Referenz: CLI-Befehle](/de/reference/cli-commands/) — jedes `rousseau cron`-Flag.
