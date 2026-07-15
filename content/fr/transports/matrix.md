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
description: "Set up rousseau-agent's Matrix transport: homeserver URL, access token, user ID, long-polling /sync, allowlist by MXID."
keywords: "Matrix, client-server, MXID, access token, homeserver, /sync, long polling, Synapse"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/transports/matrix/"
subtitle: "Matrix client-server API with long-polling /sync."
tags: "transports, Matrix"
title: "Transport Matrix"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Matrix, client-server, MXID, access token, homeserver, /sync, long polling, Synapse"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transport Matrix"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 15
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/matrix/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/matrix/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transport Matrix"
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
twitter_description: "Set up rousseau-agent's Matrix transport: homeserver URL, access token, user ID, long-polling /sync, allowlist by MXID."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transport Matrix"
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

Le transport Matrix (`internal/transport/matrix/`) communique directement avec l'API client-server Matrix — sans SDK tiers. Long-polling `/sync` pour l'entrant ; `/rooms/{room}/send/{event_type}/{txn_id}` pour le sortant.

Compatible avec tout homeserver conforme à la spécification : Synapse, Dendrite, Conduit.

## Prérequis

1. **Un compte bot** sur l'homeserver de votre choix. Enregistrez-le via le client Matrix standard ou l'API d'administration de l'homeserver.
2. **Un jeton d'accès** pour ce compte. Connectez le bot une fois à un client Matrix classique, puis copiez le jeton depuis **Paramètres → Aide & À propos → Jeton d'accès**. Alternativement, utilisez directement l'API de connexion :

   ```sh
   curl -X POST https://matrix.org/_matrix/client/v3/login \
     -H 'Content-Type: application/json' \
     -d '{"type":"m.login.password","user":"bot","password":"..."}'
   ```

3. **Le MXID complet du bot** (par exemple `@rousseau-bot:matrix.org`) pour la suppression de l'écho des messages propres.

## Configuration

```yaml
matrix:
  homeserver_url: "https://matrix.org"
  access_token: "syt_..."
  user_id: "@rousseau-bot:matrix.org"
  reply_header: ""
  allowlist:
    - "@alice:matrix.org"
    - "@bob:example.com"
```

| Champ | Défaut | Effet |
|---|---|---|
| `homeserver_url` | *requis* | URL de base (`https://matrix.org`). |
| `access_token` | *requis* | Jeton d'accès du compte bot. |
| `user_id` | *vide* | MXID complet du compte bot. Facultatif mais recommandé (suppression de l'écho des messages propres). |
| `reply_header` | *vide* | Préfixé à chaque réponse sortante. |
| `allowlist` | `[]` | MXID dont les messages sont traités. |

## Ligne de commande

```sh
rousseau matrix \
  --homeserver-url https://matrix.org \
  --access-token syt_... \
  --user-id @rousseau-bot:matrix.org \
  --allow @alice:matrix.org
```

## Long-polling

`PollTimeout` vaut 30 secondes par défaut. Le curseur `since` de chaque réponse `/sync` est stocké en mémoire et réutilisé à l'appel suivant, de sorte que les messages ne sont jamais redélivrés pendant la vie du processus. Au redémarrage, le daemon revient au curseur le plus ancien encore valide renvoyé par l'homeserver — c'est la sémantique normale de `sync`, qui correspond à celle de tout client Matrix.

## Invitations aux salons

Le bot doit déjà être membre de tout salon dans lequel il doit répondre. Invitez-le depuis un client Matrix classique. rousseau n'accepte pas automatiquement les invitations ; l'adhésion est hors périmètre.

## Modes de défaillance

| Symptôme | Correctif |
|---|---|
| 401 sur `/sync` | Jeton d'accès expiré ou invalidé. Reconnectez-vous. |
| Le bot ne voit jamais de message | Confirmez que le bot est membre du salon, et pas seulement invité. |
| Boucle d'écho sur les messages propres | Définissez `user_id` en configuration pour que rousseau puisse filtrer ses propres messages. |
