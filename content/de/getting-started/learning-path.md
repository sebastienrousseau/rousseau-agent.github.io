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
description: "Recommended reading order for new rousseau-agent users, split by role: individual developer, platform operator, security reviewer."
keywords: "learning path, reading order, docs guide, individual developer, platform operator, security reviewer"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/getting-started/learning-path/"
subtitle: "What to read first, split by role."
tags: "learning-path, reading-order"
title: "Lernpfad"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "learning path, reading order, docs guide, individual developer, platform operator, security reviewer"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Lernpfad"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 22
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/learning-path/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/learning-path/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Lernpfad"
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
twitter_description: "Recommended reading order for new rousseau-agent users, split by role: individual developer, platform operator, security reviewer."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Lernpfad"
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

## Wählen Sie Ihre Rolle

Rousseaus Zielgruppe teilt sich sauber entlang dreier Achsen. Wählen Sie diejenige, die zu Ihrem Ziel passt, und lesen Sie in Reihenfolge – jeder Pfad setzt voraus, dass der vorherige Abschnitt aufgenommen wurde.

## Einzelner Entwickler

Sie möchten einen Coding-Assistenten auf Ihrem eigenen Laptop, der Sitzungen persistiert und Ihre bestehende `claude`-CLI ansteuert. Kein Team, keine gemeinsame Bereitstellung.

| # | Seite | Warum |
|---|---|---|
| 1 | [Erste Schritte](/de/getting-started/) | Installation, `rousseau chat`, Durchgang beim ersten Start. |
| 2 | [Konzepte](/de/concepts/) | Verstehen Sie die Agent-Schleife und den Sitzungsspeicher, bevor Sie etwas anpassen. |
| 3 | [Benutzerleitfaden: CLI](/de/user-guide/cli/) | Jeder Befehl, jedes Flag. |
| 4 | [Benutzerleitfaden: TUI](/de/user-guide/tui/) | Tastenbelegungen und Panel-Semantik. |
| 5 | [Benutzerleitfaden: Tools](/de/user-guide/tools/) | Was die fünf eingebauten Tools tun und was nicht. |
| 6 | [Konfiguration](/de/configuration/) | Feinjustieren Sie die Teile, die Sie angefasst haben. |
| 7 | [Skills](/de/skills/) | Wiederverwendbare Prompt-Fragmente verfassen. |

Überspringen Sie alles unter [Entwicklerleitfaden](/de/developer-guide/), es sei denn, Sie planen, die Agent-Schleife in ein anderes Binary einzubetten.

## Plattform-Operator

Sie betreiben rousseau für ein Team hinter einem Unternehmensperimeter. Verfügbarkeit, Auditierbarkeit und Least-Privilege-Haltung sind tragend.

| # | Seite | Warum |
|---|---|---|
| 1 | [Erste Schritte](/de/getting-started/) | Installation und Smoke-Test. |
| 2 | [Plattform-Unterstützung](/de/getting-started/platform-support/) | Jede Abhängigkeits-Version bestätigen. |
| 3 | [Konzepte](/de/concepts/) | Geschichtete Architektur – worauf Sie sich über Releases hinweg verlassen können. |
| 4 | [Bereitstellung](/de/deployment/) | Rootless Podman + Quadlet. Kubernetes-Hinweis. |
| 5 | [Leitfäden: Kubernetes-Bereitstellung](/de/guides/kubernetes-deployment/) | Wenn Kubernetes Ihr Ziel ist. |
| 6 | [Konfiguration](/de/configuration/) + [Referenz: Konfigurationsschema](/de/reference/config-schema/) | Jeder Knopf, strukturiert. |
| 7 | [Benutzerleitfaden: Freigaberichtlinien](/de/user-guide/approval-policies/) | Die Tool-Call-Freigabegeschichte, die Sie Auditoren präsentieren. |
| 8 | [Leitfäden: Observability](/de/guides/observability/) | slog-Ausgabe in Ihre Log-Pipeline verdrahten. |
| 9 | [Leitfäden: Audit + Freigaberichtlinien](/de/guides/audit-approval-policies/) | Durchgearbeitete Pattern-Mode-Konfiguration mit Ablehnungsregeln. |
| 10 | [Aktualisieren](/de/getting-started/updating/) | Sicher zwischen Versionen wechseln. |

## Sicherheitsprüfer

Sie prüfen rousseau vor dem Rollout oder beantworten einen Lieferantenfragebogen im Namen Ihres Teams.

| # | Seite | Warum |
|---|---|---|
| 1 | [Sicherheit](/de/security/) | Vertrauensmodell, Lieferketten-Haltung, Kryptographie-Inventar. |
| 2 | [Installation](/de/getting-started/installation/) | cosign + SHA-256-Verifikations-Rezept. |
| 3 | [Konzepte](/de/concepts/) | Geschichtete Architektur – wo die Vertrauensgrenzen liegen. |
| 4 | [Benutzerleitfaden: Freigaberichtlinien](/de/user-guide/approval-policies/) | Der Hebel zwischen dem Modell und der Shell. |
| 5 | [Leitfäden: Read-only-Modus](/de/guides/read-only-mode/) | Haltung für eine erste Inspektions-Bereitstellung. |
| 6 | [Referenz: Exit-Codes](/de/reference/exit-codes/) | Fehlermodi, die für Init-Systeme und Monitore sichtbar werden. |
| 7 | [Datenschutz](/de/privacy/) | Datenfluss-Haltung. |
| 8 | [Bereitstellung](/de/deployment/) | Laufzeit-Härtung – Podman-Flags, Capability-Drops, seccomp. |

## Übergreifende Lektüre

Jeder Leser profitiert von diesen, sobald er eine Rolle gewählt hat:

- [Fehlerbehebung](/de/troubleshooting/) — jede Diagnose, die Sie mit `rousseau doctor` erreichen können.
- [Changelog](/de/changelog/) — was sich zwischen Releases bewegt hat.
- [MCP](/de/mcp/) — wie rousseau Tools und Sitzungen anderen Agenten exponiert.
- [Cron](/de/cron/) — Prompts-auf-Zeitplan planen.

## Weiter

- [Plattform-Unterstützung](/de/getting-started/platform-support/) — was wo läuft.
- [Erster Transport](/de/getting-started/first-transport/) — durchgearbeiteter WhatsApp-Durchgang.
