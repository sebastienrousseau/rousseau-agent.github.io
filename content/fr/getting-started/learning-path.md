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
description: "Recommended reading order for new rousseau-agent users, split by role: individual developer, platform operator, security reviewer."
keywords: "learning path, reading order, docs guide, individual developer, platform operator, security reviewer"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/getting-started/learning-path/"
subtitle: "What to read first, split by role."
tags: "learning-path, reading-order"
title: "Parcours d'apprentissage"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "learning path, reading order, docs guide, individual developer, platform operator, security reviewer"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Parcours d'apprentissage"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 22
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/learning-path/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/learning-path/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Parcours d'apprentissage"
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
twitter_title: "Parcours d'apprentissage"
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

## Choisir son rôle

Le public de Rousseau se répartit clairement selon trois axes. Choisissez celui qui correspond à votre objectif et lisez dans l'ordre — chaque parcours suppose que la section précédente a été assimilée.

## Développeur individuel

Vous voulez un assistant de codage sur votre propre poste de travail qui persiste les sessions et pilote votre CLI `claude` existante. Pas d'équipe, pas de déploiement partagé.

| # | Page | Pourquoi |
|---|---|---|
| 1 | [Getting Started](/fr/getting-started/) | Installation, `rousseau chat`, présentation du premier lancement. |
| 2 | [Concepts](/fr/concepts/) | Comprendre la boucle d'agent et le magasin de sessions avant toute personnalisation. |
| 3 | [User Guide: CLI](/fr/user-guide/cli/) | Chaque commande, chaque option. |
| 4 | [User Guide: TUI](/fr/user-guide/tui/) | Raccourcis clavier et sémantique des panneaux. |
| 5 | [User Guide: Tools](/fr/user-guide/tools/) | Ce que les cinq outils intégrés font et ne font pas. |
| 6 | [Configuration](/fr/configuration/) | Régler les éléments que vous avez modifiés. |
| 7 | [Skills](/fr/skills/) | Rédiger des fragments de prompt réutilisables. |

Ignorez tout ce qui se trouve dans le [Developer Guide](/fr/developer-guide/) sauf si vous prévoyez d'intégrer la boucle d'agent dans un autre binaire.

## Opérateur de plateforme

Vous exécutez rousseau pour une équipe derrière un périmètre d'entreprise. La disponibilité, l'auditabilité et la posture du moindre privilège sont critiques.

| # | Page | Pourquoi |
|---|---|---|
| 1 | [Getting Started](/fr/getting-started/) | Installation et test de fumée. |
| 2 | [Platform Support](/fr/getting-started/platform-support/) | Confirmer chaque version de dépendance. |
| 3 | [Concepts](/fr/concepts/) | Architecture en couches — ce qui reste stable entre les versions. |
| 4 | [Deployment](/fr/deployment/) | Podman rootless + Quadlet. Note Kubernetes. |
| 5 | [Guides: Kubernetes Deployment](/fr/guides/kubernetes-deployment/) | Si Kubernetes est votre cible. |
| 6 | [Configuration](/fr/configuration/) + [Reference: Config Schema](/fr/reference/config-schema/) | Chaque paramètre, structuré. |
| 7 | [User Guide: Approval Policies](/fr/user-guide/approval-policies/) | Le récit d'approbation des appels d'outils à présenter aux auditeurs. |
| 8 | [Guides: Observability](/fr/guides/observability/) | Brancher la sortie slog dans votre pipeline de logs. |
| 9 | [Guides: Audit + Approval Policies](/fr/guides/audit-approval-policies/) | Configuration éprouvée en mode motif avec règles de refus. |
| 10 | [Updating](/fr/getting-started/updating/) | Passer d'une version à l'autre en toute sécurité. |

## Auditeur sécurité

Vous évaluez rousseau avant déploiement, ou vous répondez à un questionnaire fournisseur pour le compte de votre équipe.

| # | Page | Pourquoi |
|---|---|---|
| 1 | [Security](/fr/security/) | Modèle de confiance, posture chaîne d'approvisionnement, inventaire cryptographique. |
| 2 | [Installation](/fr/getting-started/installation/) | Recette de vérification cosign + SHA-256. |
| 3 | [Concepts](/fr/concepts/) | Architecture en couches — où se situent les frontières de confiance. |
| 4 | [User Guide: Approval Policies](/fr/user-guide/approval-policies/) | Le levier entre le modèle et le shell. |
| 5 | [Guides: Read-only Mode](/fr/guides/read-only-mode/) | Posture pour un déploiement d'inspection en première passe. |
| 6 | [Reference: Exit Codes](/fr/reference/exit-codes/) | Modes de défaillance exposés aux systèmes d'init et aux moniteurs. |
| 7 | [Privacy](/fr/privacy/) | Posture des flux de données. |
| 8 | [Deployment](/fr/deployment/) | Durcissement à l'exécution — flags Podman, retraits de capacités, seccomp. |

## Lectures transverses

Chaque lecteur bénéficie de ces pages une fois son rôle choisi :

- [Troubleshooting](/fr/troubleshooting/) — tous les diagnostics accessibles via `rousseau doctor`.
- [Changelog](/fr/changelog/) — ce qui a bougé entre les versions.
- [MCP](/fr/mcp/) — comment rousseau expose les outils et les sessions aux autres agents.
- [Cron](/fr/cron/) — planifier un prompt à l'horloge.

## Suite

- [Platform Support](/fr/getting-started/platform-support/) — ce qui tourne où.
- [First transport](/fr/getting-started/first-transport/) — présentation pratique de WhatsApp.
