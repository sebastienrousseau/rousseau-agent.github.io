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
description: "Worked examples for rousseau-agent: scheduled tasks, self-hosted vLLM, Kubernetes deployment, approval-policy audits, observability, read-only mode."
keywords: "guides, tutorials, worked examples, vllm, kubernetes, audit, observability, read-only"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/guides/"
subtitle: "Praxisbeispiele mit lauffähiger Konfiguration."
tags: "guides, tutorials"
title: "Leitfäden"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "guides, tutorials, worked examples, vllm, kubernetes, audit, observability, read-only"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Leitfäden"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 30
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Leitfäden"
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
twitter_description: "Worked examples for rousseau-agent: scheduled tasks, self-hosted vLLM, Kubernetes deployment, approval-policy audits, observability, read-only mode."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Leitfäden"
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

## Was hier zu finden ist

Leitfäden sind ausgearbeitete Beispiele mit lauffähiger Konfiguration. Jeder Leitfaden beantwortet eine einzelne "Wie mache ich…"-Frage end-to-end.

| Leitfaden | Beantwortet |
|---|---|
| [Zeitgesteuerte Aufgaben](/de/guides/scheduled-tasks/) | Wie lasse ich mich von rousseau nach Zeitplan per WhatsApp erinnern? |
| [Self-hosted vLLM](/de/guides/self-hosted-vllm/) | Wie richte ich rousseau auf einen vLLM-Endpunkt in meinem internen Netz aus? |
| [Kubernetes-Bereitstellung](/de/guides/kubernetes-deployment/) | Wie betreibe ich rousseau als Kubernetes-`Deployment`? |
| [Audit- + Genehmigungsrichtlinien](/de/guides/audit-approval-policies/) | Wie schränke ich das `bash`-Tool ein und lasse den Agent trotzdem sinnvoll arbeiten? |
| [Observability](/de/guides/observability/) | Wie bringe ich die slog-Ausgabe von rousseau in Loki / Grafana / Datadog? |
| [Read-Only-Modus](/de/guides/read-only-mode/) | Wie betreibe ich rousseau als Read-Only-Inspektionsagent, der den Workspace nie verändert? |

## Wann Leitfäden, wann Konzepte, wann Referenz

- **[Konzepte](/de/concepts/)** — Sie wollen verstehen, wie der Agent-Loop funktioniert.
- **Leitfäden** — Sie wollen ein konkretes operatives Problem lösen.
- **[Referenz](/de/reference/cli-commands/)** — Sie wollen die exakte Signatur eines Flags.

## Weiter

- [Zeitgesteuerte Aufgaben](/de/guides/scheduled-tasks/) — häufig der erste Leitfaden, zu dem Operatoren greifen.
