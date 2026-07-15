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
description: "Set up rousseau-agent's Signal transport: signal-cli subprocess in JSON-RPC mode, account registration out-of-band, E.164 allowlist, extra_args knob."
keywords: "Signal, signal-cli, JSON-RPC, subprocess, E.164, account registration, linked device"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/transports/signal/"
subtitle: "signal-cli subprocess in JSON-RPC daemon mode."
tags: "transports, Signal"
title: "Transport Signal"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Signal, signal-cli, JSON-RPC, subprocess, E.164, account registration, linked device"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transport Signal"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 13
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/signal/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/signal/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transport Signal"
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
twitter_description: "Set up rousseau-agent's Signal transport: signal-cli subprocess in JSON-RPC mode, account registration out-of-band, E.164 allowlist, extra_args knob."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transport Signal"
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

Le transport Signal (`internal/transport/signal/`) délègue à `signal-cli` (https://github.com/AsamK/signal-cli) exécuté en mode daemon JSON-RPC.

`signal-cli --output=json -a <account> jsonRpc` diffuse du JSON-RPC 2.0 sur stdin/stdout : les requêtes sortantes `send` délivrent les messages ; les arrivées entrantes se présentent sous forme de notifications `receive`.

## Prérequis

Deux éléments doivent être en place avant que rousseau puisse dialoguer avec Signal :

1. **`signal-cli` dans le `$PATH`** (ou une valeur `binary` explicite en configuration).
2. **Compte enregistré / lié hors-bande.**

L'enregistrement du compte est délibérément hors du périmètre de rousseau. Deux voies sont prises en charge (selon la documentation `signal-cli`) :

- **Enregistrer un nouveau numéro.** `signal-cli register` déclenche la vérification par SMS ou appel vocal. Finalisez avec `signal-cli verify <code>`. Le numéro devient la propriété du daemon.
- **Lier en tant que périphérique secondaire.** `signal-cli link` affiche une URI `tsdevice://` ; scannez-la dans l'application mobile Signal sous **Paramètres → Périphériques liés**. Le numéro reste rattaché au téléphone ; le daemon agit en secondaire.

Les deux flux persistent l'état sous `~/.local/share/signal-cli/`. Effectuez un bind-mount de ce répertoire dans le conteneur si vous déployez sous Podman.

## Configuration

```yaml
signal:
  binary: signal-cli
  account: "+447900123456"
  extra_args:
    - --verbose
  reply_header: "*Rousseau Agent*\n\n"
  allowlist:
    - "+447900654321"
```

| Champ | Défaut | Effet |
|---|---|---|
| `binary` | `signal-cli` | Exécutable à invoquer. |
| `account` | *requis* | Numéro de téléphone E.164 sous lequel le daemon fonctionne. |
| `extra_args` | `[]` | Inséré entre `-a <account>` et `jsonRpc`. Utile pour `--config <path>` et `--verbose`. |
| `reply_header` | *vide* | Préfixé à chaque réponse sortante. |
| `allowlist` | `[]` | Numéros E.164 dont les messages sont traités. Vide accepte tous les expéditeurs. |

## Ligne de commande

```sh
rousseau signal --account +447900123456 --allow +447900654321
```

Les options en ligne de commande reflètent le bloc de configuration. `--allow` peut être répété.

## Flux des messages

- **Entrant.** `signal-cli` émet une notification JSON-RPC `receive` pour chaque message reçu. rousseau la parse, écarte ce qui n'est pas dans l'allowlist et transmet le corps au `Handler`.
- **Sortant.** rousseau écrit une requête JSON-RPC `send` sur l'entrée standard de `signal-cli`. Les accusés de livraison arrivent sur le même canal.

## Timeouts

Le transport n'impose pas son propre timeout sur le sous-processus. La couche réseau propre à `signal-cli` gère les reconnexions au serveur Signal. Si le processus se termine, rousseau ne le relance pas — un `Restart=on-failure` systemd (déjà configuré dans le Quadlet de référence) redémarre l'ensemble du daemon rousseau, entraînant `signal-cli` avec lui.

## Modes de défaillance

| Symptôme | Correctif |
|---|---|
| `signal-cli` se termine immédiatement | Le compte n'est ni enregistré ni lié. Effectuez l'enregistrement hors-bande. |
| Les notifications `receive` n'arrivent jamais | Vérifiez que le compte n'est pas lié à un autre emplacement qui consomme la file. |
| Erreurs de parsing JSON | Confirmez que votre version de `signal-cli` est 0.13+. Les versions plus anciennes utilisaient une enveloppe différente. |
