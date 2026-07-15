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
description: "Set up rousseau-agent's Discord transport: Gateway v10 WebSocket, bot token, Message Content intent, allowlist by user ID."
keywords: "Discord, Gateway v10, WebSocket, bot token, Message Content intent, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/transports/discord/"
subtitle: "Discord Gateway v10 over WebSocket."
tags: "transports, Discord"
title: "Transport Discord"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Discord, Gateway v10, WebSocket, bot token, Message Content intent, allowlist"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transport Discord"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 17
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/discord/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/discord/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transport Discord"
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
twitter_description: "Set up rousseau-agent's Discord transport: Gateway v10 WebSocket, bot token, Message Content intent, allowlist by user ID."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transport Discord"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Ce que vous allez apprendre</span><p>Le guide pas à pas du Discord Developer Portal, quels intents Gateway rousseau utilise et pourquoi, l'explication du calculateur de bits de permissions, et les modes de défaillance liés aux erreurs de configuration courantes. Lisez <code>internal/transport/discord/client.go</code> en parallèle de cette page.</p></aside>

## Vue d'ensemble

Le transport Discord (`internal/transport/discord/`) communique directement avec le protocole Discord Gateway v10 — sans SDK tiers. WebSocket pour l'entrant (`Identify → Ready → Heartbeat/Ack → Dispatch(MESSAGE_CREATE)`) ; REST pour le sortant (`POST /channels/{id}/messages`).

## Prérequis

1. **Une application Discord avec un utilisateur Bot.** Créez-la sur https://discord.com/developers/applications → **New Application** → onglet **Bot** → **Add Bot**.
2. **Un jeton de bot** (onglet Bot → **Reset Token** → copiez le jeton — vous ne le voyez qu'une fois).
3. **L'intent Message Content activé** (onglet Bot → **Privileged Gateway Intents**). Sans cela, la Gateway retire le texte des messages de chaque événement et rousseau ne verra que des corps vides.
4. **Le bot invité sur au moins un serveur** (ou messages privés activés). Générez l'URL d'invitation sous **OAuth2 → URL Generator** avec le scope `bot` et les permissions `Send Messages` + `Read Message History`.

## Configuration

```yaml
discord:
  token: "Bot MTIz..."
  reply_header: ""
  allowlist:
    - "123456789012345678"
```

| Champ | Défaut | Effet |
|---|---|---|
| `token` | *requis* | Jeton de bot fourni par le Developer Portal. |
| `reply_header` | *vide* | Préfixé à chaque réponse sortante. |
| `allowlist` | `[]` | Identifiants utilisateur Discord dont les messages sont traités. |

## Ligne de commande

```sh
rousseau discord --token 'MTIz...' --allow 123456789012345678
```

## Intents Gateway

rousseau demande trois intents (`internal/transport/discord/client.go`) :

| Intent | Bit | Rôle |
|---|---|---|
| `GUILD_MESSAGES` | `1 << 9` | Messages dans les canaux serveur. |
| `DIRECT_MESSAGES` | `1 << 12` | Messages privés au bot. |
| `MESSAGE_CONTENT` | `1 << 15` | Alimente le champ `content`. **Doit être activé dans le portail.** |

Sans l'intent Message Content, les événements `MESSAGE_CREATE` arrivent avec un `content` vide et rousseau consignera `discord.empty_body`.

## Heartbeat

Le transport respecte le `heartbeat_interval` de la Gateway émis dans l'opcode Hello, en envoyant Heartbeat + en suivant `heartbeat_ack`. Les ack manqués ferment la socket et laissent systemd redémarrer le processus.

## En-tête de réponse

Discord affiche `**text**` en gras et n'impose aucune forme d'en-tête particulière. Surchargez selon vos besoins :

```yaml
discord:
  reply_header: "**Rousseau Agent**\n"
```

## Calculateur de bits de permissions

Discord utilise un bitmask pour encoder les permissions d'un bot sur un canal. Chaque permission est une puissance de 2. Les plus courantes pour rousseau :

| Permission | Bit |
|---|---|
| Read Messages / View Channels | `1 << 10` = `1024` |
| Send Messages | `1 << 11` = `2048` |
| Send Messages in Threads | `1 << 38` = `274877906944` |
| Read Message History | `1 << 16` = `65536` |
| Add Reactions | `1 << 6` = `64` |

Pour accorder plusieurs permissions, combinez les bits par OU logique et collez l'entier obtenu dans le paramètre `permissions=` de l'OAuth2 URL Generator :

```
Read Messages (1024) OR Send Messages (2048) OR Read Message History (65536) = 68608
```

<aside class="admonition" data-type="note"><span class="admonition-title">Aide du portail</span><p>L'<em>OAuth2 URL Generator</em> du developer portal vous permet de cocher les cases de permissions et calcule l'entier à votre place. Ajoutez l'URL générée à vos favoris — elle permet aux administrateurs de serveur d'inviter le bot sur n'importe quel serveur Discord.</p></aside>

## Cycle de vie de la Gateway

La Gateway est à état :

```
Client                        Discord Gateway
  │
  │   ────  Connect  ────▶
  │   ◀── HELLO (heartbeat_interval)
  │
  │   ───── IDENTIFY (token, intents) ────▶
  │   ◀── READY (session_id, user)
  │
  │   ─── Heartbeat every N ms ─▶
  │   ◀── HEARTBEAT_ACK
  │
  │   ◀── MESSAGE_CREATE (a user typed)
  │   ─── (rousseau handles + POSTs reply)
  │
  │   ◀── Disconnect (code 4009: session timed out)
  │   ─── RESUME (session_id) or re-IDENTIFY
```

Le client suit `heartbeat_ack`. Si un ack est manqué, la socket se ferme et le processus se termine — systemd ou le runtime de conteneur redémarre.

## Modes de défaillance

| Symptôme | Correctif |
|---|---|
| Le bot ne voit que des messages vides | Activez l'intent Message Content dans le developer portal. |
| La Gateway se ferme avec le code 4004 | Jeton invalide. Régénérez-le. |
| Le bot ne voit aucun canal | Confirmez que l'invitation OAuth2 incluait le scope `bot`. |
| 403 à l'envoi | Le bot n'a pas la permission `Send Messages` sur ce canal. |
| Code 4014 sur Identify | Vous demandez un intent pour lequel votre application n'est pas approuvée (généralement Message Content sur un bot présent sur plus de 100 serveurs). Faites vérifier votre bot. |
| Code 4009 (session timed out) | Normal après une longue inactivité. Rousseau se reconnecte de manière transparente. |

## Dépannage

### Gateway 4013 (Invalid Intents)

Vous demandez un bit d'intent qui n'existe pas. Cela traduit généralement une incohérence entre les constantes d'intent de la bibliothèque cliente et la carte d'intents actuelle de Discord. Rousseau construit le bitmask d'intents dans `internal/transport/discord/client.go` ; mettez à jour vers la dernière version si vous voyez 4013 après un changement d'API Discord.

### Le bot reçoit les événements mais ne répond pas

Décalage d'allowlist. La valeur `--allow` doit être l'identifiant utilisateur Discord numérique (pas le nom d'utilisateur, pas le nom d'affichage). Récupérez-le dans Discord : activez le mode développeur dans *Paramètres utilisateur &gt; Avancés*, puis clic droit sur un utilisateur &gt; *Copier l'identifiant utilisateur*.

### Les MP fonctionnent, mais pas les canaux de serveur

Intent `GUILD_MESSAGES` manquant, ou bot non invité sur le serveur. Les permissions serveur sont distinctes des permissions MP — le bot doit disposer de la permission `Read Messages` sur le canal.

### `429 Too Many Requests` en sortie

Discord applique une limite globale de 50 req/s par bot, en plus des limites par canal. Sous charge soutenue, rousseau ne retente pas actuellement — l'appelant doit se retirer. Voir [Guides : Rate limits](/fr/guides/rate-limits/).

### Le statut en ligne du bot fluctue

Discord considère un bot hors-ligne après environ 40 s sans heartbeat. La ligne de log `discord.heartbeat_missed` indique un problème réseau ou un daemon à court de CPU. Vérifiez que le conteneur dispose d'assez de CPU alloué.

## Pages liées

- [Prise en main : Premier transport](/fr/getting-started/first-transport/) — parcours de bout en bout.
- [Configuration](/fr/configuration/) — le bloc de configuration `discord`.
- [Transports](/fr/transports/) — transports voisins.
- [Guides : Politiques d'audit &amp; d'approbation](/fr/guides/audit-approval-policies/) — politique pour les serveurs Discord.
- [Déploiement](/fr/deployment/) — exécution de Discord dans un conteneur Podman.

## Lectures complémentaires

- `internal/transport/discord/client.go` — connexion Gateway, heartbeat, pompe d'événements.
- `internal/cli/discord.go` — câblage CLI.
- `internal/transport/router.go` — application de l'allowlist.
- [Documentation de l'API Discord : Gateway](https://discord.com/developers/docs/topics/gateway).
- [Documentation de l'API Discord : Permissions](https://discord.com/developers/docs/topics/permissions).
