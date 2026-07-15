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
description: "Worked example: use rousseau-agent's cron scheduler + WhatsApp to run a scheduled prompt daily and deliver the result to your phone."
keywords: "cron, scheduled tasks, whatsapp, code review, robfig, daily reminder"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/guides/scheduled-tasks/"
subtitle: "Nag yourself daily via WhatsApp."
tags: "guides, cron, scheduled, whatsapp"
title: "Guide : tâches planifiées"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, scheduled tasks, whatsapp, code review, robfig, daily reminder"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide : tâches planifiées"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 31
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/scheduled-tasks/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/scheduled-tasks/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guide : tâches planifiées"
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
twitter_description: "Worked example: use rousseau-agent's cron scheduler + WhatsApp to run a scheduled prompt daily and deliver the result to your phone."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide : tâches planifiées"
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

## Scénario

Vous voulez un rappel quotidien sur WhatsApp à 09h00 demandant si la boîte de revue de code contient quelque chose de stagnant. L'agent doit lire votre fichier local de file de revue, en faire un résumé et livrer ce résumé sur votre téléphone — indépendamment du fait que votre poste soit en pleine autre tâche.

Les pièces en mouvement :

- Un démon `rousseau whatsapp` en cours d'exécution.
- Un job cron persisté dans SQLite via `rousseau cron add`.
- La goroutine du planificateur `robfig/cron/v3` à l'intérieur du démon déclenche le job ; la réponse est distribuée via le même transport WhatsApp.

## Prérequis

- `rousseau whatsapp` appairé et livrant des messages sur au moins un JID ([First transport](/fr/getting-started/first-transport/)).
- Un fichier vers lequel le prompt peut pointer — pour cette présentation, une file Markdown à `/workspace/review-queue.md`.

## Étape 1 — Enregistrer le job

```sh
rousseau cron add \
  --name daily-review-nag \
  --schedule "0 9 * * *" \
  --prompt "Read /workspace/review-queue.md and list every PR that has been open for more than 3 days. Reply with 3 bullets max." \
  --deliver-to 447900123456@s.whatsapp.net
```

`--schedule` est une expression cron POSIX à 5 champs analysée par `robfig/cron/v3` (`min hour dom mon dow`). Rousseau valide l'expression au moment de l'ajout ; un planning invalide échoue immédiatement avant d'atterrir dans le magasin.

`--deliver-to` est le JID WhatsApp qui recevra la réponse. Pour les groupes, utilisez la forme `@g.us`.

## Étape 2 — Confirmer que le job est actif

```sh
rousseau cron list
```

Sortie :

```
b7a3f2e1  on   daily-review-nag      0 9 * * *             last=never
    Read /workspace/review-queue.md and list every PR that has been open for more than 3 days. Reply with 3 bullets max. → 447900123456@s.whatsapp.net
```

Les nouveaux jobs deviennent actifs dans l'intervalle de polling suivant du planificateur (60 secondes par défaut). Aucun redémarrage nécessaire.

## Étape 3 — Forcer un essai à vide

Les jobs planifiés sont déclenchés par le démon `rousseau whatsapp` en cours d'exécution. Pour vérifier le câblage sans attendre 09h00, changez temporairement le planning pour qu'il s'exécute dans une minute :

```sh
rousseau cron remove daily-review-nag
rousseau cron add \
  --name daily-review-nag \
  --schedule "*/1 * * * *" \
  --prompt "..." \
  --deliver-to 447900123456@s.whatsapp.net
```

Surveillez le log du démon :

```
cron.fire   name=daily-review-nag job=b7a3f2e1
tool.execute name=read id=t_1
cron.deliver name=daily-review-nag target=447900123456@s.whatsapp.net bytes=284
```

Une fois le message reçu sur votre téléphone, supprimez la copie à la minute et rajoutez la version quotidienne.

## Étape 4 — Désactiver sans supprimer

```sh
rousseau cron disable daily-review-nag
```

Basculer `enabled=false` laisse le job dans le magasin mais le saute à chaque déclenchement. Réactivez avec `rousseau cron enable daily-review-nag`.

## Ce qui se passe en interne

1. `rousseau cron add` écrit une ligne dans la table `cron` de `~/.local/share/rousseau/sessions.db`.
2. Le démon `rousseau whatsapp` démarre une goroutine de planificateur `robfig/cron/v3` au boot et interroge la table tous les `PollInterval` (60s par défaut).
3. Quand l'expression cron se déclenche, `Runner.RunOnce(ctx, prompt)` exécute un tour d'agent one-shot sur une session fraîche (pas d'historique des déclenchements précédents).
4. La réponse traverse `Delivery` — un callback agnostique du transport que le démon câble à `client.Deliver(ctx, target, body)`.
5. `last_run_at` est mis à jour dans le magasin. Les échecs sont journalisés mais ne désactivent pas le job.

Le planificateur est durable : si le démon meurt en pleine exécution, le prochain lancement reprend la file. Les jobs ne se déclenchent jamais deux fois pour la même minute car `robfig/cron/v3` déduplique par tick.

## Motifs courants

| Planning | Signification |
|---|---|
| `0 9 * * *` | 09h00 chaque jour. |
| `*/15 9-17 * * 1-5` | Toutes les 15 minutes, 09h00–17h59, lundi–vendredi. |
| `0 * * * *` | Toutes les heures pile. |
| `0 0 * * 0` | Minuit chaque dimanche. |

## Superposition avec les skills

Les prompts longs deviennent pénibles. Si le prompt d'un job planifié ne cesse de grossir, déplacez le canevas dans un [skill](/fr/skills/) et laissez le prompt le référencer. Le skill est intégré au prompt système au moment du déclenchement.

## Précautions

- Les jobs planifiés s'exécutent contre le fournisseur configuré du démon. Si votre fournisseur principal est `claudecli` et que vous faites tourner l'identifiant `claude` sous-jacent, le déclenchement échoue tant que vous ne vous êtes pas ré-authentifié.
- La cible de livraison doit figurer dans l'allowlist du démon. Rousseau ne livrera pas à un JID hors allowlist même si un job planifié le demande.
- Le planificateur cron tourne dans le démon `rousseau whatsapp` par conception. Faire tourner `rousseau slack` à côté vous donne deux planificateurs indépendants lisant la même table — les jobs se déclencheront deux fois. Choisissez un seul démon pour posséder le planning.

## Suite

- [Cron reference](/fr/cron/) — chaque sous-commande, chaque flag.
- [Skills](/fr/skills/) — partager du canevas de prompt entre jobs.
- [Audit + approval policies](/fr/guides/audit-approval-policies/) — verrouiller ce que le prompt planifié peut faire.
