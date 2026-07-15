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
description: "Support routing for rousseau-agent. GitHub issues for bugs and features. sebastian.rousseau@gmail.com for security reports."
keywords: "contact, support, GitHub issues, security disclosure, email"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/contact/"
subtitle: "Où adresser les bugs, les demandes de fonctionnalités et les signalements de sécurité."
tags: "contact, support"
title: "Contact"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "contact, support, GitHub issues, security disclosure, email"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Contact"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "support"
order: 29
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/contact/index.html"
item_link: "https://docs.rousseau-agent.dev/contact/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Contact"
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
twitter_description: "Support routing for rousseau-agent. GitHub issues for bugs and features. sebastian.rousseau@gmail.com for security reports."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Contact"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Merci à chaque opérateur qui exploite son propre agent de codage."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Bugs et fonctionnalités

Ouvrez un ticket à https://github.com/sebastienrousseau/rousseau-agent/issues. Incluez :

- La sortie de `rousseau version`.
- Version de Go, OS, runtime conteneur.
- Reproduction minimale — idéalement un test en échec.
- Extrait de log avec `ROUSSEAU_LOG_LEVEL=debug`, rédigé pour les secrets.

## Divulgation de sécurité

**N'**ouvrez **pas** de ticket public pour les rapports touchant à la sécurité. Écrivez à :

**sebastian.rousseau@gmail.com**

SLA d'accusé de réception : 72 heures. La table complète des SLA de divulgation vit sur la [page Security](/fr/security/).

Incluez un vecteur CVSS 3.1 si vous en avez un, le composant affecté (chemin de fichier et plage de lignes ou module de dépendance), une reproduction minimale et tout calendrier de divulgation coordonnée que vous devez respecter.

La politique complète est dans `SECURITY.md` dans le dépôt source.

## Commercial / conseil

`rousseau-agent` est un projet open source sous licence MIT. Il n'y a pas de niveau de support commercial. Les prestations de conseil sont ponctuelles — contactez le mainteneur à l'adresse ci-dessus.
