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
hreflang: "es"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "es"
locale: "es_ES"
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
permalink: "https://docs.rousseau-agent.dev/es/tutorials/"
subtitle: "Recorridos completos de principio a fin que ensamblan todas las piezas."
tags: "tutorials, walkthrough, code review, changelog, deployment, mcp"
title: "Tutoriales"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tutorials, code review bot, changelog, vps deployment, mcp, approval policy"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutoriales"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutoriales"
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
twitter_title: "Tutoriales"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Gracias a cada operador que ejecuta su propio agente de codificación."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Para qué son los tutoriales

Las guías responden una única pregunta de "cómo hago…" de forma aislada. Los tutoriales van al contrario: toman un escenario completo del mundo real y te llevan por cada pieza de rousseau necesaria para entregarlo. Cada tutorial produce algo que podrías pegar en tu propio workspace y esperar que funcione.

| Tutorial | Con qué te quedas |
|---|---|
| [Construir un bot de code review](/es/tutorials/build-a-code-review-bot/) | Un canal de Slack donde mencionar `@rousseau` sobre una ruta de repo dispara un pase de revisión con `read` + `grep`. |
| [Changelog nocturno](/es/tutorials/nightly-changelog/) | Un cron job que resume el `git log` del día y lo envía a WhatsApp a las 18:00. |
| [Desplegar en un VPS](/es/tutorials/deploy-to-a-vps/) | Un despliegue Podman rootless endurecido en un VPS nuevo bajo systemd. |
| [Exponer herramientas vía MCP](/es/tutorials/expose-tools-via-mcp/) | Claude Desktop invocando `rousseau_search_sessions`, `rousseau_list_sessions`, `rousseau_read_session`, `rousseau_cron_list`. |
| [Endurecer el approver](/es/tutorials/harden-approver-policy/) | Un approver estricto en modo `pattern` con `default: deny`, validado por la traza de auditoría de slog. |

## Requisitos previos

Cada tutorial asume que completaste el [Quickstart](/es/quickstart/): `rousseau` está en `$PATH`, hay un proveedor configurado y `rousseau chat` produce una respuesta.

Más allá de eso, cada tutorial señala lo adicional: un workspace de Slack, un VPS, un número vinculado a WhatsApp o `claude` desktop.

## No es un tutorial

Si quieres una receta corta de "cómo hago X", lee [Guías](/es/guides/). Si quieres el flag exacto de CLI o el campo exacto de configuración, salta a [Referencia](/es/reference/cli-commands/). Si quieres entender qué hace una pieza de rousseau antes de conectarla, empieza por [Conceptos](/es/concepts/).
