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
description: "rousseau-agent's SMS transport is send-only. Twilio (account_sid + auth_token) or Vonage (api_key + auth_token). Inbound not supported because it requires a public webhook."
keywords: "SMS, Twilio, Vonage, Nexmo, send-only, Messaging Service SID, E.164, no webhook"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/transports/sms/"
subtitle: "Send-only SMS via Twilio or Vonage."
tags: "transports, SMS"
title: "Transport SMS"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "SMS, Twilio, Vonage, Nexmo, send-only, Messaging Service SID, E.164, no webhook"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transport SMS"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 19
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/sms/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/sms/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transport SMS"
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
twitter_description: "rousseau-agent's SMS transport is send-only. Twilio (account_sid + auth_token) or Vonage (api_key + auth_token). Inbound not supported because it requires a public webhook."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transport SMS"
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

## Send-only, par conception

Le transport SMS est **send-only**. Les SMS entrants exigent un webhook HTTP public dans lequel l'opérateur télécom effectue des POST — ce qui entre directement en conflit avec la posture zéro surface entrante de rousseau. Si votre cas d'usage nécessite des SMS entrants, exécutez rousseau aux côtés d'un récepteur de webhooks dédié et acheminez les messages via le planificateur cron ou l'API d'intégration agent-loop.

`Start` est implémenté comme un no-op qui bloque sur `ctx.Done()`, afin que le transport s'insère malgré tout dans la structure de câblage standard du daemon.

## Opérateurs pris en charge

| Opérateur | `provider` en configuration | Champs requis |
|---|---|---|
| Twilio | `twilio` | `from`, `account_sid`, `auth_token` |
| Vonage (anciennement Nexmo) | `vonage` | `from`, `api_key`, `auth_token` (le secret d'API) |

## Configuration Twilio

```yaml
sms:
  provider: twilio
  from: "+15550000000"
  account_sid: "AC..."
  auth_token: "..."
```

`from` peut être un numéro d'expéditeur E.164 ou un **Twilio Messaging Service SID** (commençant par `MG…`). Les Messaging Services assurent la gestion de flotte, le routage sticky-sender et la sélection d'expéditeur basée sur la géographie — recommandés pour tout trafic dépassant un seul pays.

`base_url` vaut par défaut `https://api.twilio.com/2010-04-01` et ne nécessite d'être surchargé que pour les endpoints régionaux ou les tests.

## Configuration Vonage

```yaml
sms:
  provider: vonage
  from: "+15550000000"
  api_key: "abcd1234"
  auth_token: "efgh5678"
```

Dans la configuration Vonage, `auth_token` correspond au **secret d'API** de Vonage, et non à leur clé de signature JWT — Vonage authentifie les envois SMS via une simple paire clé/secret.

`base_url` vaut par défaut `https://rest.nexmo.com`.

## Ligne de commande

```sh
# Twilio
rousseau sms \
  --provider twilio \
  --from '+15550000000' \
  --account-sid AC... \
  --auth-token ...

# Vonage
rousseau sms \
  --provider vonage \
  --from '+15550000000' \
  --api-key abcd1234 \
  --auth-token efgh5678
```

Puisqu'il n'y a pas de flux entrant, `--allow` ne s'applique pas.

## API de livraison

Les deux fournisseurs utilisent leurs endpoints REST respectifs :

- **Twilio.** `POST /2010-04-01/Accounts/{sid}/Messages.json` avec basic-auth SID/token.
- **Vonage.** `POST /sms/json` avec `api_key` + `api_secret` dans le corps.

Les identifiants de messages renvoyés sont consignés ; les webhooks de statut de livraison ne sont **pas** consommés (là encore, aucune surface HTTP publique).

## Formatage E.164

`from` et les numéros de destination doivent être au format E.164 (`+<country><subscriber>`). Sans espace, sans tiret. Les Twilio Messaging Service SID contournent cette exigence, mais uniquement pour le champ `from`.

## Hygiène des coûts

- Réglez `max_tokens` de manière agressive côté fournisseur — le SMS est peu coûteux à l'unité, mais les octets se multiplient vite si le modèle génère de longues réponses (Twilio segmente à 160 caractères en GSM-7 ou 70 en UCS-2).
- Envisagez de réécrire la réponse sortante pour la rendre concise avant de la transmettre au transport SMS. `agent.Options.SystemPrompt` est l'endroit approprié.
