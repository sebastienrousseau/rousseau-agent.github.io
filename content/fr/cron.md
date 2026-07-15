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
changefreq: "weekly"
description: "rousseau-agent's cron scheduler runs stored jobs on a schedule and delivers replies through any registered transport. Backed by robfig/cron/v3 and SQLite job persistence."
keywords: "cron, robfig/cron, scheduler, scheduled jobs, delivery, transport-agnostic, SQLite persistence"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/cron/"
subtitle: "Tâches planifiées persistantes déclenchées via n'importe quel transport."
tags: "cron, scheduler, reference"
title: "Planificateur cron"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, robfig/cron, scheduler, scheduled jobs, delivery, transport-agnostic, SQLite persistence"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Planificateur cron"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 24
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/cron/index.html"
item_link: "https://docs.rousseau-agent.dev/cron/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Planificateur cron"
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
twitter_description: "rousseau-agent's cron scheduler runs stored jobs on a schedule and delivers replies through any registered transport. Backed by robfig/cron/v3 and SQLite job persistence."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Planificateur cron"
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

Le planificateur cron (`internal/cron/scheduler.go`) est une goroutine qui exécute les entrées `CronJob` stockées selon leur planning configuré, exécute le prompt de chaque tâche via l'agent et transmet la réponse à une fonction `Delivery` indépendante du transport.

Le planificateur s'exécute aux côtés de n'importe quel daemon long-running (typiquement `rousseau whatsapp` ou un autre transport de chat). Les tâches sont stockées dans la même base SQLite que les sessions, elles survivent donc aux redémarrages.

## Syntaxe de planification

Fondée sur [robfig/cron/v3](https://pkg.go.dev/github.com/robfig/cron/v3). Le parseur prend en charge :

- Le cron standard à 5 champs : `<minute> <heure> <jour-du-mois> <mois> <jour-de-la-semaine>`.
- Les raccourcis prédéfinis : `@yearly`, `@monthly`, `@weekly`, `@daily`, `@hourly`, `@every <duration>`.

Exemples de plannings :

| Expression | Déclenchement |
|---|---|
| `0 9 * * 1-5` | 09:00 en semaine |
| `*/15 * * * *` | Toutes les 15 minutes |
| `@daily` | Une fois par jour à minuit (fuseau horaire du serveur) |
| `@every 30m` | Toutes les 30 minutes |

## CLI

```sh
# Lister toutes les tâches enregistrées.
rousseau cron list

# Ajouter une tâche.
rousseau cron add \
  --name morning-standup \
  --schedule '0 9 * * 1-5' \
  --prompt 'What are the top three engineering priorities today?' \
  --target '447900123456@s.whatsapp.net'

# Supprimer par nom ou par ID.
rousseau cron remove morning-standup
```

## Configuration

Les tâches sont stockées dans la base d'état, pas dans le fichier de configuration. Il n'y a rien dans `~/.config/rousseau/config.yaml` pour configurer le planificateur lui-même ; il utilise le `PollInterval = 60s` par défaut.

## Flux d'exécution d'une tâche

1. Le planificateur resynchronise la liste des tâches depuis SQLite toutes les `PollInterval`.
2. `robfig/cron/v3` déclenche la tâche à l'heure planifiée.
3. `TurnRunner.RunOnce(ctx, job.Prompt)` exécute un **tour unique** de l'agent sur une session neuve (pas d'historique, pas de rappel inter-session sauf si le runner l'active explicitement).
4. Le texte de réponse est passé à `Delivery(ctx, job.Target, replyText)`.
5. Si `Delivery` retourne une erreur → journalisée ; le prochain tick réessaie.

## Livraison

`Delivery` est un petit type fonctionnel :

```go
type Delivery func(ctx context.Context, target, body string) error
```

Le planificateur n'importe pas `internal/transport` — le contrat de livraison est indépendant du transport. En pratique, les daemons `rousseau <transport>` câblent un `Delivery` qui résout la chaîne cible via le transport actif (`Deliver` sur le client de transport).

`target` est spécifique au transport :

- WhatsApp : un JID (`447900123456@s.whatsapp.net`).
- Telegram : un identifiant de conversation numérique.
- Slack : un identifiant de canal (`C012345`) ou d'utilisateur (`U012345`).
- Discord : un identifiant de canal.
- SMS : une destination E.164.
- iMessage : un GUID de conversation.
- Signal : une destination E.164.
- Matrix : un identifiant de salon.
- Email : une adresse complète RFC 5322.

## Persistance

Les tâches sont stockées dans la table `cron_jobs` de la base d'état (`internal/state/sqlite/`). Champs : `id`, `name`, `schedule`, `prompt`, `target`, `created_at`, `updated_at`. Les redémarrages récupèrent chaque tâche au prochain `PollInterval`.

Les nouvelles tâches ajoutées via `rousseau cron add` deviennent actives dans un délai maximum d'un `PollInterval` — jusqu'à 60 secondes par défaut.

## Interaction avec les transports

La closure `Delivery` capture une référence au transport en cours d'exécution. Un daemon exécute généralement un seul transport, de sorte que le planificateur cron livre via ce transport. Les déploiements multi-transports exécutent un daemon par transport, et l'opérateur fait pointer le `target` de chaque tâche cron vers le daemon du transport correspondant.

La livraison inter-transports (tâche exécutée dans le daemon WhatsApp, réponse via Slack) n'est pas prise en charge aujourd'hui — le planificateur ne connaît que le `Delivery` qu'on lui a fourni.

## Modes de défaillance

| Symptôme | Correctif |
|---|---|
| La tâche ne se déclenche pas | Vérifiez `rousseau status` ; le planificateur consigne `cron.fired` à chaque activation. |
| La tâche se déclenche mais rien n'arrive | Erreur de livraison — recherchez `cron.delivery_failed` dans les logs. |
| La tâche s'exécute mais le modèle refuse d'agir | Politique d'approbation refusant les appels d'outils. Assouplissez `agent.approver` ou passez en mode `pattern`. |
| La livraison va vers la mauvaise cible | Le planificateur est indépendant du transport ; le daemon interprète `target`. Confirmez que le transport exécuté par votre daemon correspond au format de la cible. |
