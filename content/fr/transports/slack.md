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
description: "Set up rousseau-agent's Slack transport: Socket Mode (xapp-* app token + xoxb-* bot token), no public webhook, allowlist by user ID."
keywords: "Slack, Socket Mode, xapp, xoxb, chat.postMessage, connections:write, no webhook, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/transports/slack/"
subtitle: "Socket Mode with no public HTTP surface."
tags: "transports, Slack"
title: "Transport Slack"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Slack, Socket Mode, xapp, xoxb, chat.postMessage, connections:write, no webhook, allowlist"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transport Slack"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 16
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/slack/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/slack/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transport Slack"
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
twitter_description: "Set up rousseau-agent's Slack transport: Socket Mode (xapp-* app token + xoxb-* bot token), no public webhook, allowlist by user ID."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transport Slack"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Ce que vous allez apprendre</span><p>Le parcours complet de l'assistant app.slack.com, les scopes OAuth exacts à accorder, les abonnements d'événements à configurer, comment Socket Mode évite le besoin d'un webhook public, et comment fonctionne la prévention de boucle sur ses propres messages dans rousseau. Lisez <code>internal/transport/slack/client.go</code> en parallèle de cette page.</p></aside>

## Vue d'ensemble

Le transport Slack (`internal/transport/slack/`) utilise **Socket Mode** — un WebSocket sortant vers Slack — pour que le daemon n'ait besoin d'aucune surface HTTP publique. Les événements entrants passent par le socket ; les appels sortants visent l'API Web standard (`chat.postMessage`).

<aside class="admonition" data-type="tip"><span class="admonition-title">Pourquoi Socket Mode</span><p>L'alternative (Events API + Request URL) exige un endpoint HTTPS public avec certificat SSL. Rousseau n'expose aucune surface HTTP entrante par conception, donc Socket Mode est la seule voie d'ingress supportée.</p></aside>

## Deux jetons

Slack Socket Mode requiert deux jetons aux responsabilités disjointes :

| Jeton | Préfixe | Scope | Rôle |
|---|---|---|---|
| App-level token | `xapp-` | `connections:write` | Ouvre le WebSocket Socket Mode. |
| Bot token | `xoxb-` | `chat:write` + abonnements d'événements | Envoie les messages, s'abonne aux événements. |

## Configuration de l'app

Pas à pas complet sur https://app.slack.com/apps :

1. **Créez une nouvelle app** (« From scratch »). Choisissez un workspace.
2. **Activez Socket Mode** (Settings → Socket Mode). Générez un **app-level token** avec `connections:write`. C'est le jeton `xapp-*`.
3. **Configurez les Event Subscriptions** (Features → Event Subscriptions). Abonnez-vous à `message.channels`, `message.im`, ou aux scopes de canaux que le bot doit entendre. Vous n'avez **pas** besoin d'une Request URL car Socket Mode livre les événements par le socket.
4. **Ajoutez les bot scopes** (Features → OAuth & Permissions). Minimum : `chat:write`. Ajoutez `im:history`, `channels:history`, `groups:history` ou `mpim:history` selon vos abonnements d'événements.
5. **Installez l'app sur le workspace.** L'écran d'installation vous retourne le bot token `xoxb-*`.
6. **Notez éventuellement l'ID utilisateur propre du bot** (commence par `U…`). C'est ce que rousseau utilise pour la prévention de boucle sur ses propres messages.

## Configuration

```yaml
slack:
  app_token: "xapp-1-A0..."
  bot_token: "xoxb-1234..."
  bot_user_id: "U0123ABCD"
  reply_header: ""
  allowlist:
    - "U0ALICE"
    - "U0BOB"
```

| Champ | Défaut | Effet |
|---|---|---|
| `app_token` | *requis* | Jeton `xapp-*` de niveau app avec `connections:write`. |
| `bot_token` | *requis* | Jeton bot `xoxb-*` avec `chat:write`. |
| `bot_user_id` | *vide* | ID `U…` du bot pour la prévention de boucle sur ses propres messages. Optionnel ; à défaut, inspection du champ `bot_id`. |
| `reply_header` | *vide* | Préfixé à chaque message sortant. |
| `allowlist` | `[]` | IDs d'utilisateurs Slack dont les messages sont traités. |

## Ligne de commande

```sh
rousseau slack \
  --app-token xapp-... \
  --bot-token xoxb-... \
  --bot-user-id U0123ABCD
```

## Format wire

- **Entrant.** Slack envoie des enveloppes JSON via le WebSocket. rousseau ACK l'enveloppe, extrait le texte et l'expéditeur, et les remet au handler.
- **Sortant.** `POST https://slack.com/api/chat.postMessage` avec `{"channel": "<id>", "text": "…"}` et `Authorization: Bearer <bot_token>`.

## Explication des scopes OAuth

Chaque scope accorde une surface d'API précise. Les scopes dont rousseau a besoin, et ce qui casse sans eux :

| Scope | Endpoint utilisé | Cassé sans |
|---|---|---|
| `connections:write` | `apps.connections.open` (WebSocket Socket Mode) | Impossible d'ouvrir le socket. **Requis.** |
| `chat:write` | `chat.postMessage` | Impossible de répondre à un message. **Requis.** |
| `im:history` | `conversations.history` pour les DM (indirect via événements) | Le bot ne verra pas le contenu des DM dans les événements. |
| `im:read` | `im.list`, métadonnées DM | Impossible de lister les DM ouverts. |
| `im:write` | `conversations.open` | Impossible d'ouvrir un nouveau DM (utile uniquement si le bot doit DM quelqu'un sans invitation). |
| `mpim:history`, `channels:history`, `groups:history` | IM multi-partie / canaux / canaux privés | Le bot ne verra pas le contenu hors DM. |

Positionnez les scopes sous *OAuth &amp; Permissions &gt; Bot Token Scopes*. N'ajoutez que ceux dont vous avez réellement besoin — Slack affiche un avertissement au moment de l'installation pour chaque scope, et les utilisateurs finaux installent plus volontiers un bot à surface de permissions étroite.

## Prévention de boucle sur ses propres messages

Sans protection, un bot qui répond aux messages voit aussi ses propres réponses comme événements entrants — d'où des boucles incontrôlées. Rousseau gère cela via `bot_user_id` :

```go
// Simplified — actual logic in internal/transport/slack/client.go
if msg.User == cfg.BotUserID {
    continue // Skip: this is our own outbound message echoing back.
}
```

Récupérez l'ID utilisateur de votre bot une fois via :

```sh
curl -H "Authorization: Bearer xoxb-your-token" \
  https://slack.com/api/auth.test
```

La réponse contient `user_id`. Collez-le dans `slack.bot_user_id` en config, ou passez-le avec `--bot-user-id`.

<aside class="admonition" data-type="warning"><span class="admonition-title">Prévention de boucle de repli</span><p>Même sans <code>bot_user_id</code>, le transport ignore les événements de sous-type <code>bot_message</code>. Mais s'appuyer sur le sous-type seul est fragile — positionnez <code>bot_user_id</code> en production.</p></aside>

## Threads

Les messages Slack portent un `thread_ts` lorsqu'ils sont des réponses dans un thread. Les appels sortants de rousseau incluent `thread_ts` quand l'événement entrant en avait un, pour que les réponses du bot restent dans le thread. Les messages de premier niveau ne deviennent de nouveaux threads que quand l'utilisateur en démarre un.

## Modes d'échec

| Symptôme | Correctif |
|---|---|
| `invalid_auth` à l'ouverture du socket | `app_token` erroné ou sans `connections:write`. Régénérez. |
| Les événements entrants n'arrivent jamais | Vérifiez que les **Event Subscriptions** sont activées et que les événements `message.*` pertinents sont abonnés. |
| Le bot répond à ses propres messages | Renseignez `bot_user_id` en config. |
| `not_in_channel` à l'envoi | Invitez le bot dans le canal (`/invite @rousseau-bot`). |
| Les DM fonctionnent mais pas le canal | Scope `channels:history` manquant, ou le bot n'a pas été invité au canal. |

## Dépannage

### `invalid_auth` à l'ouverture du socket

Le jeton `xapp-…` est incorrect ou a perdu son scope. Régénérez depuis *Basic Information &gt; App-Level Tokens*, en veillant à ce que `connections:write` figure sur le nouveau jeton.

### `not_authed` sur `chat.postMessage`

Bot token (`xoxb-…`) absent ou incorrect. Régénérez depuis *OAuth &amp; Permissions &gt; Bot User OAuth Token*.

### Les événements arrivent mais rousseau ne répond à aucun

Vérifiez l'allowlist. En mode `pattern` avec `default: deny`, les utilisateurs non listés sont silencieusement rejetés. Cherchez `router.transport.rejected` dans les logs.

### `channel_not_found` en sortant

L'ID de canal Slack (`C…`) a changé — par exemple, un canal archivé puis recréé. Mettez à jour les IDs de canaux codés en dur. Rousseau utilise normalement le canal issu de l'événement entrant, donc cela n'arrive qu'avec une livraison cron vers un canal fixé.

### Le bot apparaît hors ligne dans Slack

Socket Mode fait tourner le WebSocket toutes les ~30 s. Si Slack affiche le bot hors ligne, vérifiez : (1) le daemon tourne (`systemctl --user status`), (2) le WebSocket est connecté (ligne de log `slack.connected`), (3) l'horloge de la machine est à moins de 30 s de l'heure exacte.

## Pages liées

- [Prise en main : Premier transport](/fr/getting-started/first-transport/) — parcours de bout en bout.
- [Configuration](/fr/configuration/) — le bloc de config `slack`.
- [Transports](/fr/transports/) — transports voisins.
- [Déploiement](/fr/deployment/) — exécuter Slack dans un conteneur Podman.
- [Guides : Audit &amp; Politiques d'approbation](/fr/guides/audit-approval-policies/) — jeux de règles pour un workspace Slack partagé.

## Pour aller plus loin

- `internal/transport/slack/client.go` — connexion Socket Mode, pompe d'événements, `chat.postMessage`.
- `internal/cli/slack.go` — câblage CLI.
- `internal/transport/router.go` — application de l'allowlist.
- [Docs API Slack : Socket Mode](https://api.slack.com/apis/socket-mode).
