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
description: "Exit codes and signal semantics for the rousseau-agent binary. What init systems can rely on."
keywords: "exit codes, signals, sigterm, sigint, systemd, restart policy"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/reference/exit-codes/"
subtitle: "Exit codes and signal semantics."
tags: "reference, exit-codes, signals"
title: "Codes de sortie"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "exit codes, signals, sigterm, sigint, systemd, restart policy"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Codes de sortie"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 51
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/exit-codes/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/exit-codes/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Codes de sortie"
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
twitter_description: "Exit codes and signal semantics for the rousseau-agent binary. What init systems can rely on."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Codes de sortie"
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

## Codes de sortie

La CLI de Rousseau est délibérément conservatrice — deux codes de sortie couvrent tous les chemins.

| Code | Émis par | Signification |
|---|---|---|
| 0 | `cmd/rousseau/main.go` via `cli.Execute` | Commande terminée avec succès. Les démons sortent 0 lors d'un arrêt propre (SIGINT / SIGTERM). |
| 1 | `cmd/rousseau/main.go` via `cli.Execute` | Commande échouée. La chaîne d'erreur est imprimée sur stderr. Chaque échec — erreur de parsing config, échec d'authentification fournisseur, panic de transport, erreur de câblage d'outil — retombe sur ce code. |

`rousseau doctor` suit la même convention : exit 0 quand chaque contrôle passe, exit 1 quand un contrôle est `fail`. Les avertissements et les lignes de niveau info n'affectent pas le code de sortie.

Les versions futures pourront séparer les échecs en codes distincts (config vs runtime vs réseau). Aujourd'hui, traitez toute sortie non nulle comme réessayable mais nécessitant une inspection des logs.

## Gestion des signaux

`cmd/rousseau/main.go` installe un gestionnaire de signaux qui annule le `context.Context` racine sur `SIGINT` et `SIGTERM`. Chaque composant longue durée (boucle d'agent, transport, planificateur cron, serveur MCP) honore l'annulation de contexte, donc le chemin d'arrêt est :

1. `SIGINT` / `SIGTERM` reçu.
2. Le contexte racine est annulé.
3. Les transports appellent `Stop()` sur eux-mêmes, flushant les messages en vol.
4. Le planificateur cron cesse d'accepter de nouveaux déclenchements ; les déclenchements en cours se terminent.
5. `Close()` du magasin de sessions est appelé via `defer`, en checkpointant le WAL.
6. `Execute` retourne 0.

`SIGKILL` ne peut pas être capté. Si le démon est `kill -9` en pleine session, le WAL du magasin protège de la corruption mais le tour en vol n'est pas persisté. Le prochain lancement reprend depuis le dernier état sauvegardé.

## Politique de redémarrage systemd

Pour l'unité Quadlet de référence :

```
[Service]
Restart=on-failure
RestartSec=10
```

`on-failure` redémarre sur toute sortie non nulle ; combiné à la convention de codes de sortie de rousseau cela signifie : exit 0 (`SIGTERM` depuis `systemctl stop`) ne redémarre pas, exit 1 redémarre.

Pour les démons qui rencontrent des erreurs persistantes (mauvaise config, mauvaise auth fournisseur), `on-failure` va s'emballer. Consultez `journalctl` pour la raison de l'échec avant de supposer que la boucle de retry va récupérer.

## Sémantique des probes Kubernetes

Rousseau ne livre aucun endpoint HTTP liveness/readiness par conception. Les probes Kubernetes doivent être soit :

- Des probes `exec` exécutant `rousseau doctor --config /etc/rousseau/config.yaml` (retourne 0 en bonne santé, 1 en échec), soit
- Absentes, le pod s'appuyant sur `restartPolicy: Always` et la gestion d'erreurs propre au démon.

`rousseau doctor` est bon marché (~50 ms) donc c'est une bonne probe de liveness. Ne l'utilisez pas comme readiness probe — un `fail` sur `provider.claudecli.binary` ne devrait pas retirer le pod de la rotation si l'échec ne va pas se réparer tout seul.

## Erreurs gérées

Les erreurs qui produisent le code de sortie 1 via la surface d'erreur de la CLI incluent :

- **Échec de chargement config** — erreur de parsing YAML, champ inconnu, type invalide.
- **Échec d'authentification fournisseur** — clé API manquante, identifiants invalides, région Bedrock / Vertex invalide.
- **Échec de démarrage de transport** — jeton manquant, hôte IMAP/SMTP injoignable, erreur de protocole whatsmeow.
- **Échec d'ouverture du magasin** — permission refusée sur `~/.local/share/rousseau/`, disque plein.
- **Échec de contrôle doctor** — toute ligne `fail` fait retourner exit 1 à doctor.
- **Échec de parsing d'expression cron** — `rousseau cron add` valide avant persistance.

## Panics non gérées

`go test -race` est exécuté à chaque build CI, donc les panics sont extrêmement rares. Quand elles se produisent, le runtime Go imprime la panic + la stack trace sur stderr et sort avec un code non nul depuis le runtime — typiquement 2, mais c'est la convention de Go et pas quelque chose que rousseau contrôle.

Pour la production, encadrez le démon d'un superviseur qui capture stderr en cas de sortie anormale et remonte la trace.

## Suite

- [Guide utilisateur : CLI](/fr/user-guide/cli/) — chaque commande.
- [Guides : Observabilité](/fr/guides/observability/) — remonter le signal slog au-delà du code de sortie.
- [Troubleshooting](/fr/troubleshooting/) — que faire quand le code de sortie ne suffit pas.
