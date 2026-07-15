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
description: "Schedule a rousseau cron job that summarises git log every evening and posts the result to WhatsApp."
keywords: "cron, git log, changelog, whatsapp, scheduled prompt, deliver-to"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/tutorials/nightly-changelog/"
subtitle: "A daily 18:00 cron job that pushes a git-log summary to WhatsApp."
tags: "tutorials, cron, changelog, whatsapp, git"
title: "Tutoriel : changelog nocturne"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, git log, changelog, whatsapp, scheduled prompt, deliver-to"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutoriel : changelog nocturne"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/nightly-changelog/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/nightly-changelog/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutoriel : changelog nocturne"
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
twitter_description: "Schedule a rousseau cron job that summarises git log every evening and posts the result to WhatsApp."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutoriel : changelog nocturne"
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

Une tâche cron stockée dans l'état SQLite de rousseau (table `cron_jobs`, schéma dans `internal/state/sqlite/cron.go`) qui se déclenche à 18h00 heure locale du lundi au vendredi. Elle exécute un prompt qui demande au modèle de résumer `git log --since=today` et livre le résultat sur votre téléphone via WhatsApp.

Temps estimé : 10 minutes.

## Prérequis

- Pont WhatsApp déjà appairé (voir l'étape 4 du [Quickstart](/fr/quickstart/) ou [Transports : WhatsApp](/fr/transports/whatsapp/)).
- Le démon `rousseau whatsapp` en cours d'exécution — le planificateur cron dans `internal/cron/scheduler.go` est démarré par les démons de transport via `wiring.startCron()`, pas par `rousseau chat`.
- Un espace de travail contenant le dépôt git à résumer, monté dans le conteneur (ou sur l'hôte si vous exécutez rousseau hors conteneur).

## Fonctionnement du cron rousseau

`rousseau cron add` écrit une ligne dans la table `cron_jobs` (`internal/state/sqlite/cron.go`). Toutes les ~15 secondes, `scheduler.sync` relit la table et réconcilie le planning en mémoire de robfig/cron/v3. Quand une tâche se déclenche, le planificateur émet `cron.firing`, exécute le prompt via le fournisseur configuré et livre le résultat à `deliver_to` via le pont de transport qui possède le processus (WhatsApp dans ce tutoriel).

Noms de logs structurés que vous verrez (depuis `internal/cron/scheduler.go`) :

- `cron.started` — planificateur démarré avec `poll_interval=…`.
- `cron.scheduled` — une tâche a été acceptée.
- `cron.firing` — une tâche va s'exécuter.
- `cron.completed` — une tâche s'est terminée avec succès.
- `cron.run_failed`, `cron.delivery_failed`, `cron.record_failed` — modes de défaillance.

## Étape 1 : ajouter la tâche

```sh
rousseau cron add \
  --name        nightly-changelog \
  --schedule    "0 18 * * 1-5" \
  --prompt      "Summarise git log --since=yesterday under /workspace/rousseau-agent as a Slack-style bullet list. Keep it under 200 words. If nothing changed, reply with a single line 'no commits'." \
  --deliver-to  447900123456@s.whatsapp.net
```

L'expression cron est analysée par `robfig/cron/v3` dans `newCronAddCmd` (`internal/cli/cron.go`). Les expressions invalides sont rejetées avant écriture. La valeur `--deliver-to` est le JID au format E.164 pour WhatsApp (`<chiffres>@s.whatsapp.net`) ; le format de la cible de livraison dépend du transport.

## Étape 2 : vérifier

```sh
rousseau cron list
```

Forme de la sortie (depuis `newCronListCmd`) :

```
NAME               STATUS SCHEDULE       PROMPT                       DELIVER-TO
nightly-changelog  on     0 18 * * 1-5   Summarise git log …          447900123456@s.whatsapp.net
```

La liste est également exposée via MCP sous `rousseau_cron_list` (voir `internal/mcp/tools.go`).

## Étape 3 : essai à blanc

Il n'existe pas de déclencheur « exécuter maintenant » intégré. Pour un test de fumée, planifiez temporairement la tâche une minute dans le futur :

```sh
rousseau cron remove nightly-changelog
rousseau cron add --name test --schedule "*/1 * * * *" --prompt "say hi" --deliver-to "$JID"
journalctl --user -u rousseau-agent -f | grep cron.
```

Séquence de logs attendue :

```
INFO cron.scheduled  job=test expr=*/1 * * * *
INFO cron.firing     job=test
INFO cron.completed  job=test
```

Supprimez la tâche de test et rajoutez la vraie une fois terminé.

## Étape 4 : affiner le prompt

Les meilleurs prompts cron sont autonomes : le modèle n'a aucune mémoire des exécutions précédentes. Incluez le chemin du dépôt, le format de sortie attendu et un repli pour le cas vide. Exemple de deuxième itération :

```
Summarise commits authored since 07:00 UTC today under
/workspace/rousseau-agent. Use this format:

- <short type>: <one-line summary> — <sha>

Group by author. If no commits landed, reply exactly: no commits.
```

## Activation et suppression

```sh
rousseau cron disable nightly-changelog   # conserve la ligne, stoppe les déclenchements
rousseau cron enable  nightly-changelog
rousseau cron remove  nightly-changelog   # supprime la ligne
```

`SetEnabled` et `Delete` de `internal/state/sqlite/cron.go` sont ce que ces commandes appellent.

## Voir aussi

- [Cron](/fr/cron/) — référence du planificateur.
- [Guides : Tâches planifiées](/fr/guides/scheduled-tasks/) — discussion approfondie.
- [Transports : WhatsApp](/fr/transports/whatsapp/) — fonctionnement de deliver-to.
- [Référence : commandes CLI](/fr/reference/cli-commands/) — chaque flag `rousseau cron`.
