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
description: "Full end-to-end walkthroughs: code-review bot, nightly changelog, VPS deployment, MCP integration, and approver hardening."
keywords: "tutorials, code review bot, changelog, vps deployment, mcp, approval policy"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/tutorials/"
subtitle: "Vollständige End-to-End-Anleitungen, die alles zusammenführen."
tags: "tutorials, walkthrough, code review, changelog, deployment, mcp"
title: "Tutorials"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tutorials, code review bot, changelog, vps deployment, mcp, approval policy"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorials"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorials"
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
twitter_description: "Full end-to-end walkthroughs: code-review bot, nightly changelog, VPS deployment, MCP integration, and approver hardening."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorials"
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

## Wofür Tutorials da sind

Leitfäden beantworten eine einzelne "Wie mache ich…"-Frage isoliert. Tutorials gehen den umgekehrten Weg: Sie nehmen ein vollständiges Praxisszenario und führen Sie durch jedes rousseau-Element, das zum Ausliefern nötig ist. Jedes Tutorial erzeugt etwas, das Sie so in Ihren Workspace übernehmen und mit dem Sie ein funktionierendes Ergebnis erwarten können.

| Tutorial | Was Sie am Ende haben |
|---|---|
| [Code-Review-Bot bauen](/de/tutorials/build-a-code-review-bot/) | Einen Slack-Kanal, in dem das Erwähnen von `@rousseau` mit einem Repo-Pfad einen `read`+`grep`-Review-Durchgang auslöst. |
| [Nightly Changelog](/de/tutorials/nightly-changelog/) | Einen Cron-Job, der den Tages-`git log` zusammenfasst und um 18:00 Uhr auf WhatsApp schickt. |
| [Auf einen VPS deployen](/de/tutorials/deploy-to-a-vps/) | Ein gehärtetes Rootless-Podman-Deployment auf einem frischen VPS hinter systemd. |
| [Tools über MCP exponieren](/de/tutorials/expose-tools-via-mcp/) | Claude Desktop steuert `rousseau_search_sessions`, `rousseau_list_sessions`, `rousseau_read_session`, `rousseau_cron_list`. |
| [Den Approver härten](/de/tutorials/harden-approver-policy/) | Einen strikten Approver im Modus `pattern` mit `default: deny`, validiert durch den slog-Audit-Trail. |

## Voraussetzungen

Jedes Tutorial setzt voraus, dass Sie den [Quickstart](/de/quickstart/) abgeschlossen haben: `rousseau` liegt in `$PATH`, ein Provider ist konfiguriert, und `rousseau chat` liefert eine Antwort.

Darüber hinaus benennt jedes Tutorial etwaige Zusatzvoraussetzungen — einen Slack-Workspace, einen VPS, eine WhatsApp-verknüpfte Rufnummer oder `claude` Desktop.

## Kein Tutorial

Für ein kurzes "Wie mache ich X"-Rezept lesen Sie [Leitfäden](/de/guides/). Für das exakte CLI-Flag oder Konfigurationsfeld springen Sie zur [Referenz](/de/reference/cli-commands/). Wenn Sie verstehen möchten, was ein rousseau-Baustein tut, bevor Sie ihn verdrahten, beginnen Sie mit [Konzepte](/de/concepts/).
