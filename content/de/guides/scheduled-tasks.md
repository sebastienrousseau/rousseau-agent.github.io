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
changefreq: "monthly"
description: "Worked example: use rousseau-agent's cron scheduler + WhatsApp to run a scheduled prompt daily and deliver the result to your phone."
keywords: "cron, scheduled tasks, whatsapp, code review, robfig, daily reminder"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/guides/scheduled-tasks/"
subtitle: "Nag yourself daily via WhatsApp."
tags: "guides, cron, scheduled, whatsapp"
title: "Leitfaden: geplante Aufgaben"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, scheduled tasks, whatsapp, code review, robfig, daily reminder"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Leitfaden: geplante Aufgaben"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 31
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/scheduled-tasks/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/scheduled-tasks/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Leitfaden: geplante Aufgaben"
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
twitter_description: "Worked example: use rousseau-agent's cron scheduler + WhatsApp to run a scheduled prompt daily and deliver the result to your phone."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Leitfaden: geplante Aufgaben"
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

## Szenario

Sie möchten täglich um 09:00 Uhr eine WhatsApp-Erinnerung, die fragt, ob der Code-Review-Posteingang etwas Liegengebliebenes enthält. Der Agent soll Ihre lokale Review-Queue-Datei lesen, zusammenfassen und die Zusammenfassung an Ihr Telefon ausliefern — unabhängig davon, ob Ihr Laptop gerade mit einer anderen Aufgabe beschäftigt ist.

Die beweglichen Teile:

- Ein laufender `rousseau whatsapp`-Daemon.
- Ein via `rousseau cron add` in SQLite persistierter Cron-Job.
- Die `robfig/cron/v3`-Scheduler-Goroutine innerhalb des Daemons feuert den Job; die Antwort wird über denselben WhatsApp-Transport zugestellt.

## Voraussetzungen

- `rousseau whatsapp` gekoppelt und Nachrichten an mindestens eine JID zustellend ([Erster Transport](/de/getting-started/first-transport/)).
- Eine Datei, auf die der Prompt zeigen kann — für diese Durchgangsanleitung eine Markdown-Queue unter `/workspace/review-queue.md`.

## Schritt 1 — Job registrieren

```sh
rousseau cron add \
  --name daily-review-nag \
  --schedule "0 9 * * *" \
  --prompt "Read /workspace/review-queue.md and list every PR that has been open for more than 3 days. Reply with 3 bullets max." \
  --deliver-to 447900123456@s.whatsapp.net
```

`--schedule` ist ein 5-Feld-POSIX-artiger Cron-Ausdruck, geparst von `robfig/cron/v3` (`min hour dom mon dow`). Rousseau validiert den Ausdruck beim Hinzufügen; ein ungültiger Zeitplan schlägt sofort fehl, bevor er im Store landet.

`--deliver-to` ist die WhatsApp-JID, die die Antwort empfängt. Für Gruppen verwenden Sie die `@g.us`-Form.

## Schritt 2 — Bestätigen, dass der Job aktiv ist

```sh
rousseau cron list
```

Ausgabe:

```
b7a3f2e1  on   daily-review-nag      0 9 * * *             last=never
    Read /workspace/review-queue.md and list every PR that has been open for more than 3 days. Reply with 3 bullets max. → 447900123456@s.whatsapp.net
```

Neue Jobs werden innerhalb des nächsten Scheduler-Poll-Intervalls (Standard 60 Sekunden) aktiv. Kein Neustart erforderlich.

## Schritt 3 — Trockenlauf erzwingen

Geplante Jobs werden vom laufenden `rousseau whatsapp`-Daemon gefeuert. Um die Verdrahtung zu verifizieren, ohne bis 09:00 Uhr zu warten, ändern Sie den Zeitplan vorübergehend so, dass er in einer Minute läuft:

```sh
rousseau cron remove daily-review-nag
rousseau cron add \
  --name daily-review-nag \
  --schedule "*/1 * * * *" \
  --prompt "..." \
  --deliver-to 447900123456@s.whatsapp.net
```

Beobachten Sie das Log des Daemons:

```
cron.fire   name=daily-review-nag job=b7a3f2e1
tool.execute name=read id=t_1
cron.deliver name=daily-review-nag target=447900123456@s.whatsapp.net bytes=284
```

Sobald Sie die Nachricht auf Ihrem Telefon sehen, löschen Sie die Jede-Minute-Kopie und fügen Sie die tägliche Version erneut hinzu.

## Schritt 4 — Deaktivieren, ohne zu löschen

```sh
rousseau cron disable daily-review-nag
```

Das Umschalten von `enabled=false` belässt den Job im Store, überspringt ihn aber bei jedem Feuer. Reaktivieren mit `rousseau cron enable daily-review-nag`.

## Was unter der Haube passiert

1. `rousseau cron add` schreibt eine Zeile in die `cron`-Tabelle in `~/.local/share/rousseau/sessions.db`.
2. Der `rousseau whatsapp`-Daemon startet beim Booten eine `robfig/cron/v3`-Scheduler-Goroutine und pollt die Tabelle alle `PollInterval` (60 s Standard).
3. Wenn der Cron-Ausdruck feuert, führt `Runner.RunOnce(ctx, prompt)` einen One-Shot-Agent-Turn gegen eine frische Sitzung aus (keine Historie aus vorherigen Feuerungen).
4. Die Antwort läuft durch `Delivery` — einen transport-agnostischen Callback, den der Daemon an `client.Deliver(ctx, target, body)` verdrahtet.
5. `last_run_at` wird im Store aktualisiert. Fehler werden protokolliert, deaktivieren den Job aber nicht.

Der Scheduler ist dauerhaft: Wenn der Daemon mitten im Feuern stirbt, nimmt der nächste Start die Warteschlange auf. Jobs feuern nie zweimal für dieselbe Minute, da `robfig/cron/v3` per Tick dedupliziert.

## Gebräuchliche Muster

| Zeitplan | Bedeutung |
|---|---|
| `0 9 * * *` | 09:00 Uhr täglich. |
| `*/15 9-17 * * 1-5` | Alle 15 Minuten, 09:00–17:59, Mo–Fr. |
| `0 * * * *` | Zur vollen Stunde. |
| `0 0 * * 0` | Mitternacht jeden Sonntag. |

## Schichtung mit Skills

Lange Prompts werden mühsam. Wenn der Prompt eines geplanten Jobs immer weiter wächst, verschieben Sie den Boilerplate in einen [Skill](/de/skills/) und lassen Sie den Prompt darauf verweisen. Der Skill wird beim Feuern in den System-Prompt eingespleißt.

## Vorbehalte

- Geplante Jobs laufen gegen den vom Daemon konfigurierten Provider. Wenn Ihr primärer Provider `claudecli` ist und Sie das zugrunde liegende `claude`-Login rotieren, schlägt das Feuern fehl, bis Sie sich erneut authentifizieren.
- Das Zustellziel muss zur Allowlist des Daemons gehören. Rousseau wird nicht an eine außerhalb der Allowlist liegende JID zustellen, selbst wenn ein geplanter Job dies verlangt.
- Der Cron-Scheduler läuft konstruktionsbedingt innerhalb des `rousseau whatsapp`-Daemons. Wenn Sie parallel `rousseau slack` laufen lassen, erhalten Sie zwei unabhängige Scheduler, die dieselbe Tabelle lesen — Jobs feuern doppelt. Wählen Sie einen Daemon, der den Zeitplan besitzt.

## Weiter

- [Cron-Referenz](/de/cron/) — jeder Subbefehl, jedes Flag.
- [Skills](/de/skills/) — Prompt-Boilerplate über Jobs hinweg teilen.
- [Audit + Freigaberichtlinien](/de/guides/audit-approval-policies/) — einschränken, was der geplante Prompt tun darf.
