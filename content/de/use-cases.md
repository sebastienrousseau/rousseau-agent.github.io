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
description: "Concrete deployment narratives for rousseau-agent: on-call SRE, mobile PR review, regulated-industry Bedrock deployment."
keywords: "use cases, narratives, on-call, sre, mobile review, whatsapp, bedrock, regulated"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/use-cases/"
subtitle: "Konkrete Fallgeschichten — wer rousseau einsetzt und warum."
tags: "use-cases, narratives"
title: "Anwendungsfälle"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "use cases, narratives, on-call, sre, mobile review, whatsapp, bedrock, regulated"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Anwendungsfälle"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 70
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/use-cases/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Anwendungsfälle"
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
twitter_description: "Concrete deployment narratives for rousseau-agent: on-call SRE, mobile PR review, regulated-industry Bedrock deployment."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Anwendungsfälle"
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

## Lesen Sie diese, wenn Sie ein Bild wollen, kein Handbuch

Use Cases sind kurze Erzählungen. Jede beschreibt einen plausiblen Operator, das Problem, dem er gegenübersteht, und die genaue Konfiguration, die er verwenden würde. Jeder Use Case ist eine Seite – lesen Sie den, der zu Ihrer Situation passt.

| Use Case | Persona | Problem |
|---|---|---|
| [On-Call-Buddy](/de/use-cases/oncall-buddy/) | Solo-SRE, kleines Unternehmen. | 3-Uhr-Slack-Alarm, Triage vor dem vollständigen Aufwachen. |
| [Mobile PR-Review](/de/use-cases/mobile-review/) | Einzelner Entwickler auf dem Pendelweg. | Pull Requests vom Telefon aus prüfen. |
| [Regulierte Industrie](/de/use-cases/regulated-industry/) | Team aus dem Finanzdienstleistungsbereich. | Coding-Agent innerhalb einer Bedrock-gehosteten VPC mit Pattern-Mode-Freigabe. |

Diese sind illustrativ, nicht erschöpfend – rousseaus Design verallgemeinert sich. Wenn Ihre Situation einem dieser ähnelt, beginnen Sie dort.

## Was jeder Use Case gemeinsam hat

- Ein einzelnes Go-Binary in einem rootless Container.
- Ein Transport pro Instanz (ein Slack, ein WhatsApp oder ein Signal – wählen Sie einen).
- Ein `pattern`-Mode-Approver mit sinnvollen Ablehnungsregeln.
- Sitzungszustand in SQLite, damit ein Neustart die Konversation nicht verliert.
- Keine SaaS-Steuerungsebene, kein Telemetrie-Endpunkt, kein Lizenzserver.

## Was variiert

- **Provider** — `claudecli` für einzelne Laptops, `bedrock`/`vertex` für regulierte Umgebungen, `openai`-kompatibel für selbstgehostetes vLLM.
- **Transport** — wählen Sie das Medium, das Ingenieure bereits verwenden.
- **Freigabepolitik** — strenger in hochriskanten Umgebungen; lockerer innerhalb eines abgeschotteten Containers.
- **Bereitstellungsoberfläche** — Laptop, Single-Node-Podman, Kubernetes.

## Weiter

- [On-Call-Buddy](/de/use-cases/oncall-buddy/) — die häufigste Geschichte.
- [Mobile PR-Review](/de/use-cases/mobile-review/) — der Grund, warum WhatsApp der Referenz-Transport ist.
- [Regulierte Industrie](/de/use-cases/regulated-industry/) — die Enterprise-Geschichte.
