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
hreflang: "pt-BR"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "pt-BR"
locale: "pt_BR"
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
permalink: "https://docs.rousseau-agent.dev/pt-BR/tutorials/"
subtitle: "Passo a passo completo que une todas as peças."
tags: "tutorials, walkthrough, code review, changelog, deployment, mcp"
title: "Tutoriais"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tutorials, code review bot, changelog, vps deployment, mcp, approval policy"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutoriais"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutoriais"
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
twitter_title: "Tutoriais"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Obrigado a cada operador que executa seu próprio agente de codificação."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Para que servem os tutoriais

Guias respondem a uma única pergunta "como faço para…" de forma isolada. Tutoriais vão pelo caminho oposto: eles pegam um cenário completo do mundo real e te conduzem por cada peça do rousseau necessária para colocá-lo em produção. Todo tutorial produz algo que você poderia colar no seu próprio workspace e esperar que funcione.

| Tutorial | Você acaba com |
|---|---|
| [Construir um bot de code review](/pt-BR/tutorials/build-a-code-review-bot/) | Um canal Slack onde mencionar `@rousseau` num caminho de repositório dispara uma passagem de review com `read` + `grep`. |
| [Changelog noturno](/pt-BR/tutorials/nightly-changelog/) | Um job cron que resume o `git log` do dia e envia para o WhatsApp às 18:00. |
| [Implantar em um VPS](/pt-BR/tutorials/deploy-to-a-vps/) | Uma implantação Podman rootless endurecida em um VPS novo por trás do systemd. |
| [Expor ferramentas via MCP](/pt-BR/tutorials/expose-tools-via-mcp/) | Claude Desktop dirigindo `rousseau_search_sessions`, `rousseau_list_sessions`, `rousseau_read_session`, `rousseau_cron_list`. |
| [Endurecer o approver](/pt-BR/tutorials/harden-approver-policy/) | Um approver estrito em modo `pattern` com `default: deny`, validado pela trilha de auditoria slog. |

## Pré-requisitos

Todo tutorial assume que você concluiu o [Quickstart](/pt-BR/quickstart/): `rousseau` está no `$PATH`, um provider está configurado e `rousseau chat` produz uma resposta.

Além disso, cada tutorial destaca o que for extra — um workspace Slack, um VPS, um número vinculado ao WhatsApp, ou `claude` desktop.

## Não é um tutorial

Se você quer uma receita curta de "como faço X", leia os [Guias](/pt-BR/guides/). Se quer a flag exata da CLI ou o campo de configuração, vá para [Referência](/pt-BR/reference/cli-commands/). Se quer entender o que uma peça do rousseau faz antes de conectá-la, comece pelos [Conceitos](/pt-BR/concepts/).
