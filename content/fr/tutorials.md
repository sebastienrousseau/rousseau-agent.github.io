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
hreflang: "fr"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "fr"
locale: "fr_FR"
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
permalink: "https://docs.rousseau-agent.dev/fr/tutorials/"
subtitle: "Guides pas à pas complets qui assemblent toutes les pièces."
tags: "tutorials, walkthrough, code review, changelog, deployment, mcp"
title: "Tutoriels"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tutorials, code review bot, changelog, vps deployment, mcp, approval policy"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutoriels"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutoriels"
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
twitter_title: "Tutoriels"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Merci à chaque opérateur qui exploite son propre agent de codage."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## À quoi servent les tutoriels

Les guides répondent à une seule question du type « comment faire pour… » de manière isolée. Les tutoriels font l'inverse : ils partent d'un scénario réel complet et vous accompagnent à travers chaque brique rousseau nécessaire pour le mettre en production. Chaque tutoriel produit quelque chose que vous pourriez coller dans votre propre espace de travail et voir fonctionner.

| Tutoriel | Ce que vous obtenez |
|---|---|
| [Construire un bot de revue de code](/fr/tutorials/build-a-code-review-bot/) | Un canal Slack où mentionner `@rousseau` sur un chemin de dépôt déclenche une passe de revue `read` + `grep`. |
| [Changelog nocturne](/fr/tutorials/nightly-changelog/) | Une tâche cron qui résume le `git log` de la journée et le pousse sur WhatsApp à 18:00. |
| [Déployer sur un VPS](/fr/tutorials/deploy-to-a-vps/) | Un déploiement Podman rootless durci sur un VPS neuf, derrière systemd. |
| [Exposer des outils via MCP](/fr/tutorials/expose-tools-via-mcp/) | Claude Desktop pilotant `rousseau_search_sessions`, `rousseau_list_sessions`, `rousseau_read_session`, `rousseau_cron_list`. |
| [Durcir l'approver](/fr/tutorials/harden-approver-policy/) | Un approver strict en mode `pattern` avec `default: deny`, validé par la piste d'audit slog. |

## Prérequis

Chaque tutoriel suppose que vous avez terminé le [Quickstart](/fr/quickstart/) : `rousseau` est dans le `$PATH`, un fournisseur est configuré et `rousseau chat` produit une réponse.

Au-delà de cela, chaque tutoriel précise ce qui est requis en plus — un workspace Slack, un VPS, un numéro lié à WhatsApp, ou `claude` desktop.

## Ce qui n'est pas un tutoriel

Pour une recette courte du type « comment faire X », lisez les [Guides](/fr/guides/). Pour le flag CLI ou le champ de configuration exact, allez à la [Référence](/fr/reference/cli-commands/). Pour comprendre ce qu'un composant de rousseau fait avant de le brancher, commencez par les [Concepts](/fr/concepts/).
