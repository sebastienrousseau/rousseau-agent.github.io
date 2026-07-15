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
description: "Set up rousseau-agent's Telegram transport: BotFather token, long-polling, allowlist by numeric user ID, reply-header customisation."
keywords: "Telegram, Bot API, BotFather, long polling, getUpdates, allowlist, chat ID"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/transports/telegram/"
subtitle: "Telegram Bot API over long-polling."
tags: "transports, Telegram"
title: "Transport Telegram"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Telegram, Bot API, BotFather, long polling, getUpdates, allowlist, chat ID"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transport Telegram"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 14
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/telegram/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/telegram/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transport Telegram"
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
twitter_description: "Set up rousseau-agent's Telegram transport: BotFather token, long-polling, allowlist by numeric user ID, reply-header customisation."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transport Telegram"
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

Le transport Telegram (`internal/transport/telegram/`) communique directement avec l'API HTTP des Telegram Bots — sans SDK tiers. Long-polling `getUpdates` pour l'entrant ; `sendMessage` pour le sortant.

## Prérequis

1. **Un bot.** Sur Telegram, envoyez un message à [@BotFather](https://t.me/BotFather), envoyez `/newbot`, choisissez un nom et un identifiant se terminant par `_bot`. BotFather vous renvoie un jeton d'API HTTP qui ressemble à `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`.
2. **Les identifiants utilisateur à autoriser.** Les identifiants utilisateur Telegram sont numériques. Le bot ne peut pas résoudre `@username` en identifiant utilisateur par lui-même — l'astuce classique consiste à demander à chaque utilisateur autorisé d'envoyer `/start` au bot une fois, puis à lire le champ `from.id` dans les logs.

## Configuration

```yaml
telegram:
  token: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
  reply_header: ""
  allowlist:
    - "12345678"
    - "98765432"
```

| Champ | Défaut | Effet |
|---|---|---|
| `token` | *requis* | Jeton du bot fourni par BotFather. |
| `base_url` | `https://api.telegram.org` | À surcharger pour un serveur Bot API local. |
| `reply_header` | *vide* | Préfixé à chaque réponse sortante. |
| `allowlist` | `[]` | Identifiants utilisateur Telegram dont les messages sont traités. |

## Ligne de commande

```sh
rousseau telegram --token 123456:ABC... --allow 12345678 --allow 98765432
```

`--allow` peut être répété.

## Long-polling

Le transport appelle `getUpdates` avec un `PollTimeout` de 30 secondes par défaut (`internal/transport/telegram/client.go`). Chaque mise à jour renvoyée fait avancer un `offset` interne, de sorte que les messages ne sont jamais redélivrés, même après un redémarrage.

Il n'y a pas de webhook. Le daemon n'expose aucune surface HTTP entrante.

## Format des messages

Seuls les messages texte sont traités. Les médias, autocollants et notes vocales sont ignorés (une évolution future pourrait acheminer l'audio via le même chemin whisper.cpp que WhatsApp).

## Modes de défaillance

| Symptôme | Correctif |
|---|---|
| Aucune mise à jour ne parvient | Confirmez qu'un message a bien été envoyé au bot au moins une fois — Telegram ne délivre pas l'historique. |
| 409 Conflict sur getUpdates | Une autre instance interroge avec le même jeton. Arrêtez-la. |
| L'allowlist rejette un utilisateur légitime | Consignez le champ `from.id` ; les identifiants utilisateur sont numériques et ne correspondent pas à `@username`. |
