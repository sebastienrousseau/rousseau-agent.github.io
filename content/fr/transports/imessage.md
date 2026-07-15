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
description: "Set up rousseau-agent's iMessage transport: BlueBubbles server on macOS, HTTP polling, poll interval, cursor deduplication, chat GUID for outbound."
keywords: "iMessage, BlueBubbles, macOS, HTTP polling, chat GUID, cursor, deduplication"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/transports/imessage/"
subtitle: "BlueBubbles HTTP polling from a macOS host."
tags: "transports, iMessage"
title: "Transport iMessage"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "iMessage, BlueBubbles, macOS, HTTP polling, chat GUID, cursor, deduplication"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transport iMessage"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 18
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/imessage/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/imessage/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transport iMessage"
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
twitter_description: "Set up rousseau-agent's iMessage transport: BlueBubbles server on macOS, HTTP polling, poll interval, cursor deduplication, chat GUID for outbound."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transport iMessage"
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

## Vue d'ensemble

Le transport iMessage (`internal/transport/imessage/`) ne dialogue pas directement avec iMessage — Apple ne fournit aucune API client officielle. Il interroge à la place [BlueBubbles](https://bluebubbles.app), un daemon côté macOS qui expose iMessage via HTTP + Socket.IO.

rousseau n'utilise que les endpoints HTTP de BlueBubbles (Socket.IO est délibérément évité pour minimiser l'empreinte des dépendances).

## Architecture

```
+-----------+     iMessage      +---------+     HTTP      +-----------+
| Apple ID  | <---------------> | macOS   | <-----------> | rousseau  |
|  server   |                   | Blue    |               | daemon    |
+-----------+                   | Bubbles |               |           |
                                +---------+               +-----------+
```

L'hôte macOS exécute BlueBubbles et reste connecté à iMessage. rousseau interroge l'endpoint `/api/v1/message` de BlueBubbles selon la cadence configurée et transmet les nouveaux messages au handler.

## Prérequis

1. **Un hôte macOS** connecté à iMessage. Pas nécessairement la même machine que celle sur laquelle tourne rousseau.
2. **Serveur BlueBubbles** installé sur cet hôte, à l'écoute sur une URL joignable par rousseau (adresse LAN, VPN ou Tailscale).
3. **Mot de passe BlueBubbles** depuis l'interface du serveur (Settings → Server Password).
4. **Un GUID de conversation** pour l'envoi. Retrouvez-le dans l'interface BlueBubbles ou via `GET /api/v1/chat`.

## Configuration

```yaml
imessage:
  base_url: "http://mac.internal:1234"
  password: "..."
  chat_guid: "iMessage;-;+15550001234"
  poll_interval: "5s"
  reply_header: ""
```

| Champ | Défaut | Effet |
|---|---|---|
| `base_url` | *requis* | URL du serveur BlueBubbles. |
| `password` | *requis* | Mot de passe du serveur BlueBubbles. |
| `chat_guid` | *vide* | GUID de la conversation cible en sortie. |
| `poll_interval` | `5s` | Cadence d'interrogation de `/api/v1/message`. |
| `reply_header` | *vide* | Préfixé à chaque message sortant. |

## Ligne de commande

```sh
rousseau imessage \
  --base-url http://mac.internal:1234 \
  --password ... \
  --chat-guid 'iMessage;-;+15550001234' \
  --poll-interval 5s
```

## Déduplication par curseur

Au démarrage, le transport initialise son curseur `lastID` au message existant le plus récent, afin d'éviter d'inonder l'opérateur avec tout l'historique iMessage. Chaque poll ultérieur récupère les `PageSize` messages les plus récents (25 par défaut) et ne transmet que ceux plus récents que le curseur.

Le curseur est en mémoire. Au redémarrage, il est réinitialisé depuis BlueBubbles — une petite fenêtre de messages arrivés pendant l'indisponibilité du daemon sera perdue. Il s'agit d'un compromis délibéré ; une logique de curseur persistante nécessiterait une table supplémentaire dans le state store, et les horodatages de livraison iMessage ne sont pas garantis monotones entre appareils.

## Accessibilité réseau

BlueBubbles doit être joignable via le réseau depuis l'endroit où rousseau s'exécute. Schémas courants :

- **Même LAN.** `http://<mac-lan-ip>:1234`.
- **Tailscale.** `http://mac.tailnet.ts.net:1234`. Chiffre la liaison et fonctionne à travers le NAT.
- **Tunnel inversé.** `http://localhost:1234` sur l'hôte rousseau, avec un tunnel SSH `-R` depuis le Mac.

N'exposez pas BlueBubbles sur l'Internet public à moins de comprendre son modèle d'authentification (un simple mot de passe).

## Modes de défaillance

| Symptôme | Correctif |
|---|---|
| `imessage.prime_failed` au démarrage | BlueBubbles injoignable — vérifiez `base_url` et `password`. |
| Chaque message historique est rejoué | `lastID` n'a pas été initialisé. Vérifiez les permissions / l'authentification. |
| Les messages sortants sont silencieusement écartés | `chat_guid` incorrect. Retrouvez-le via `GET /api/v1/chat`. |
| Les messages arrivent avec plusieurs minutes de retard | Augmentez la fréquence de polling propre à BlueBubbles ou réduisez `poll_interval`. |
