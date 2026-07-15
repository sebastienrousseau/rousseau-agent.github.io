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
description: "Wire rousseau-agent to a Slack channel that runs read and grep over the workspace whenever an operator asks."
keywords: "slack, code review, socket mode, read tool, grep tool, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/tutorials/build-a-code-review-bot/"
subtitle: "A Slack channel that lets rousseau review a repo on demand."
tags: "tutorials, slack, code review, socket mode, read, grep"
title: "Tutoriel : construire un bot de revue de code"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "slack, code review, socket mode, read tool, grep tool, allowlist"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutoriel : construire un bot de revue de code"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 42
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/build-a-code-review-bot/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/build-a-code-review-bot/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutoriel : construire un bot de revue de code"
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
twitter_description: "Wire rousseau-agent to a Slack channel that runs read and grep over the workspace whenever an operator asks."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutoriel : construire un bot de revue de code"
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

## Ce que vous construisez

Un canal Slack privé où les membres de l'équipe mentionnent `@rousseau` avec un chemin de dépôt et une question. Rousseau parcourt l'espace de travail, exécute `read` et `grep` depuis `internal/tools/builtin/` et publie une réponse avec des références de lignes citées. Aucune surface HTTP publique — le Socket Mode de Slack orchestre tout via un WebSocket sortant.

Temps estimé : 20 minutes, en supposant que vous disposez déjà d'un accès administrateur à un workspace Slack.

## Prérequis

- Rousseau installé et un fournisseur configuré (voir [Quickstart](/fr/quickstart/)).
- Administrateur du workspace Slack.
- Un dépôt déjà cloné quelque part sous votre `$HOME` — il devient l'« espace de travail » sur lequel le bot pourra faire `read`/`grep`.

## Étape 1 : créer une application Slack

Le Socket Mode de Slack est ce qui rend ce bot possible : votre daemon ouvre un WebSocket sortant vers Slack, aucun ingress n'est requis.

1. Rendez-vous sur <https://api.slack.com/apps> et créez une nouvelle application **from scratch**.
2. Sous **Socket Mode**, activez-le et générez un **app-level token** avec `connections:write`. Copiez la valeur `xapp-...`.
3. Sous **OAuth & Permissions**, ajoutez ces **Bot Token Scopes** :
   - `chat:write`
   - `app_mentions:read`
   - `channels:history` (ou `groups:history` pour les canaux privés)
4. Installez l'application sur votre workspace. Copiez le **Bot User OAuth Token** — la valeur `xoxb-...`.
5. Sous **Event Subscriptions**, activez les événements et abonnez le bot à `app_mention` et `message.channels` (ou `message.groups`).
6. Invitez le bot dans le canal de revue : `/invite @rousseau`.

## Étape 2 : configurer rousseau

Ajoutez dans `~/.config/rousseau/config.yaml`. Les champs pertinents proviennent de `SlackConfig` dans `internal/config/config.go` :

```yaml
provider: claudecli           # ou anthropic — celui que vous avez défini dans le Quickstart

slack:
  app_token:  xapp-1-…
  bot_token:  xoxb-…
  bot_user_id: U0ROUSSEAU     # via https://api.slack.com/methods/auth.test
  reply_header: "*rousseau-agent*\n\n"
  allowlist:
    - U01ABC…                 # vos identifiants utilisateur Slack

agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
    # pas de bash, pas de write, pas d'edit — reviewer en lecture seule
```

L'`allowlist` restreint les expéditeurs dont le routeur accepte les messages. Le routeur `internal/transport/router.go` émet `transport.rejected` pour tout autre expéditeur.

## Étape 3 : exécuter le bridge

```sh
rousseau slack \
  --app-token "$SLACK_APP_TOKEN" \
  --bot-token "$SLACK_BOT_TOKEN" \
  --bot-user-id "$SLACK_BOT_USER_ID"
```

`--bot-user-id` empêche le bot de répondre à ses propres messages. Les logs structurés issus de `internal/transport/slack/client.go` afficheront :

```
INFO slack.started
INFO slack.incoming from=U01ABC channel=C01REVIEW text="…"
INFO tool.execute name=read id=t_1
INFO tool.execute name=grep id=t_2
```

## Étape 4 : essayer

Dans le canal de revue :

```
@rousseau look under /home/seb/repos/acme-api and tell me
where request logging is set up
```

Le fournisseur `claudecli` (ou Anthropic — selon votre choix) appellera `read` et `grep` depuis `internal/tools/builtin/` sur le bind mount de l'espace de travail. Puisque l'approver fonctionne en mode `pattern` avec seulement `read` et `grep` autorisés, le modèle ne peut ni écrire ni ouvrir un shell — même si un prompt compromis le lui demande.

## Étape 5 : durcir

Les approvers en mode pattern sont des **regex sur l'entrée JSON de l'outil**. Pour restreindre `read` et `grep` à une arborescence de projet spécifique :

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: "\"path\":\"/home/seb/repos/acme-api/[^\"]*\""}
      - {tool: grep, match: "\"path\":\"/home/seb/repos/acme-api\""}
```

Voir [Tutoriel : Durcir l'approver](/fr/tutorials/harden-approver-policy/) pour le parcours complet de `default: deny` + audit.

## Déployer sous systemd

Pour tout ce qui dépasse une session sur portable, exécutez le bridge Slack via l'unité Quadlet Podman de `docker/rousseau-agent.container` — remplacez `Exec=whatsapp --allow …` par `Exec=slack --app-token … --bot-token …`. Voir [Déploiement](/fr/deployment/) pour l'unité complète.

## Voir aussi

- [Transports : Slack](/fr/transports/slack/)
- [Guide utilisateur : Politiques d'approbation](/fr/user-guide/approval-policies/)
- [Guide utilisateur : Outils](/fr/user-guide/tools/)
- [Tutoriel : Durcir l'approver](/fr/tutorials/harden-approver-policy/)
