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
description: "Beyond the Quadlet reference: log shipping, session-store backup, health checks, rolling restarts, and multi-transport coexistence."
keywords: "production, log shipping, backup, health check, rolling restart, systemd"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/guides/production-deployment/"
subtitle: "Everything the Quadlet reference doesn't already cover."
tags: "guides, production, deployment, backup, logs, health check"
title: "Guide : déploiement en production"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "production, log shipping, backup, health check, rolling restart, systemd"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide : déploiement en production"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/production-deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/production-deployment/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guide : déploiement en production"
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
twitter_description: "Beyond the Quadlet reference: log shipping, session-store backup, health checks, rolling restarts, and multi-transport coexistence."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide : déploiement en production"
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

## À lire après

L'unité Quadlet de référence dans `docker/rousseau-agent.container` couvre le « comment lancer rousseau ». Ce guide couvre ce que vous ajoutez autour avant de l'appeler production : logs, sauvegardes, santé, hygiène de processus.

## Expédition des logs

Rousseau écrit des logs structurés sur stderr via `log/slog` (`internal/cli/root.go`). Quand vous l'exécutez sous systemd, ce stderr atterrit dans le journal. Options pour l'expédier hors de l'hôte :

| Outil | Adaptation | Notes |
|---|---|---|
| Vector (`vector.dev`) | Meilleur défaut. | Source `journald` + un filtre écartant DEBUG. Expédier vers Loki, Datadog, S3, ce que vous voulez. |
| Promtail + Loki | Si vous exécutez déjà Grafana. | La source `journal` de Loki fonctionne directement contre `journalctl -o json`. |
| Agent Datadog | Si Datadog est le standard de l'entreprise. | L'agent DD a une queue journald. Le JSON structuré se parse nativement. |
| Fluent Bit | Alternative à faible empreinte. | Définissez `log.format: json` dans `config.yaml` ; l'entrée `systemd` de Fluent Bit le parse. |

Configurez `log.format: json` (`internal/config/config.go` `LogConfig.Format`) sans condition en production. La sortie texte est conçue pour `less`, pas pour l'analyse machine.

Voir [Guides: Observability](/fr/guides/observability/) pour une recette complète de pipeline Loki.

## Sauvegarde du magasin de sessions

Le répertoire d'état `~/.local/share/rousseau/` est le seul état durable que possède rousseau. Sauvegardez-le chaque nuit.

Deux approches :

**1. `.backup` SQLite (recommandé).**

```sh
sqlite3 ~/.local/share/rousseau/sessions.db \
  ".backup '/backup/sessions.db.$(date +%Y%m%d).bak'"
sqlite3 ~/.local/share/rousseau/whatsapp.db \
  ".backup '/backup/whatsapp.db.$(date +%Y%m%d).bak'"
restic backup /backup
```

`.backup` utilise l'API en ligne de SQLite — sûr même pendant que le démon écrit. Voir [Reference: Session store](/fr/reference/session-store/).

**2. Snapshot du système de fichiers.**

Comme le journal WAL est activé (`Open()` dans `internal/state/sqlite/store.go`), `restic` et `borg` peuvent snapshotter les fichiers bruts pendant que le démon tourne. WAL garantit une image cohérente à un instant donné.

À ne pas faire :

- Copier le fichier `.db` avec `cp` pendant que le démon tourne sans copier aussi `-wal` et `-shm`.
- Stocker les sauvegardes sur le même disque.
- Sauter le fichier d'identifiants d'appareil WhatsApp — le perdre implique de rescanner le QR.

## Health checks

`rousseau status` (`internal/cli/status.go`) sort en 0 quand sain, non-zéro en cas de problème. Utilisez-le comme sonde de santé systemd :

```ini
[Service]
ExecStartPost=/usr/bin/timeout 30 podman exec rousseau-agent rousseau status
```

Pour une sonde plus riche, scriptez une vérification qui :

1. Exécute `rousseau status`.
2. Confirme que la dernière écriture du magasin de sessions est récente (`stat sessions.db -c %Y` comparé à maintenant).
3. Vérifie l'uptime du conteneur via `podman inspect`.

Rousseau n'expose pas de `/healthz` HTTP. Si votre plateforme en exige un (sondes readiness Kubernetes), voir [Guides: Kubernetes deployment](/fr/guides/kubernetes-deployment/) — vous enveloppez rousseau dans un petit side-car ami de `curl`.

## Redémarrage roulant

Comme l'état est un unique fichier SQLite, le démon est véritablement mono-instance. Un redémarrage roulant est : arrêter, remplacer l'image, démarrer. Pas de préchauffage requis.

```sh
podman pull localhost/rousseau-agent:local     # or rebuild locally
systemctl --user restart rousseau-agent
podman logs -n 50 rousseau-agent | grep -E 'starting|connected'
```

Séquence de logs attendue (depuis `internal/transport/whatsapp/client.go`) :

```
INFO whatsapp.starting store=… allowlist=1
INFO whatsapp.connected
```

Si le démon n'émet pas `whatsapp.connected` dans les ~15 secondes, effectuez un rollback.

## Plusieurs transports sur un hôte

Vous pouvez vouloir que le même magasin de sessions soit partagé par WhatsApp et Slack. Deux moyens :

- **Plusieurs unités Quadlet** — une par transport, chacune pointant sur le même `state.path`. WAL + `busy_timeout` (voir `Open()` dans `internal/state/sqlite/store.go`) rend les écrivains concurrents sûrs.
- **Un binaire, un transport par invocation.** Les commandes de transport de rousseau sont mono-transport (`whatsapp`, `slack`, `signal`, …). Pour exécuter deux transports vous exécutez deux processus.

## Changements de configuration sans interruption

Rousseau ne recharge pas `config.yaml` à chaud. Les changements de configuration exigent un redémarrage. `SIGHUP` n'est pas câblé pour un rechargement.

Flux pratique :

1. Éditer `~/.config/rousseau/config.yaml`.
2. `systemctl --user restart rousseau-agent`.
3. Vérifier depuis les logs.

Pour la plupart des transports, la reconnexion est rapide (~1-3 secondes). La pause principale est sur WhatsApp, où whatsmeow rétablit le websocket.

## Rétention des logs

La rétention `journald` est fixée par `SystemMaxUse=` dans `/etc/systemd/journald.conf`. Pour un déploiement ami de l'audit, expédiez les logs hors hôte et réglez journald sur une rétention plus courte sur le disque local (par ex. 7 jours) afin que la piste d'audit vive dans Loki/S3, pas sur un système de fichiers qu'un intrus pourrait rotater.

## Cycle de vie de l'image de conteneur

Reconstruisez l'image à chaque release rousseau que vous voulez adopter :

```sh
cd ~/rousseau-agent
git pull
podman build -t rousseau-agent:local -f docker/Dockerfile .
systemctl --user restart rousseau-agent
```

La ligne `AutoUpdate=disabled` du Quadlet (dans `docker/rousseau-agent.container`) empêche `podman auto-update` de toucher au conteneur. Vous contrôlez la cadence de mise à jour.

## Voir aussi

- [Deployment](/fr/deployment/) — l'unité Quadlet de référence.
- [Tutorial: Deploy to a VPS](/fr/tutorials/deploy-to-a-vps/) — exemple pratique.
- [Guides: Observability](/fr/guides/observability/) — pipeline de logs.
- [Guides: Enterprise Onboarding](/fr/guides/enterprise-onboarding/) — checklist complète.
