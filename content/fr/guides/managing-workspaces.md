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
description: "How rousseau's session store partitions by workspace, how to switch workspaces, share sessions across machines, and drop a workspace's history."
keywords: "workspace, session store, state path, sync, rsync, XDG_DATA_HOME"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/guides/managing-workspaces/"
subtitle: "Partition state per project, share history across machines, drop history cleanly."
tags: "guides, workspace, session store, sqlite"
title: "Guide : gestion des espaces de travail"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "workspace, session store, state path, sync, rsync, XDG_DATA_HOME"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide : gestion des espaces de travail"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 38
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/managing-workspaces/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/managing-workspaces/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guide : gestion des espaces de travail"
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
twitter_description: "How rousseau's session store partitions by workspace, how to switch workspaces, share sessions across machines, and drop a workspace's history."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide : gestion des espaces de travail"
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

## La convention

Rousseau n'a pas de concept de « workspace » de première classe. Il possède un `state.path` dans `internal/config/config.go` (`StateConfig`) et pointe par défaut chaque processus vers `~/.local/share/rousseau/sessions.db`. Toutes les sessions, jobs cron, cartographies JID et l'index de recall FTS5 vivent dans ce fichier unique.

Pour la plupart des opérateurs, c'est exactement ce qu'il faut. Quand vous voulez de l'isolation — par projet, par machine, par client — vous pointez rousseau vers un fichier SQLite différent. Ce fichier **est** le workspace.

## Basculer de workspace à chaque invocation

Deux leviers, l'un ou l'autre fonctionne :

```sh
# 1. flag sur n'importe quelle commande rousseau
rousseau --config ~/.config/rousseau/acme.yaml chat

# 2. variable d'env (Viper la capte via ROUSSEAU_STATE_PATH)
ROUSSEAU_STATE_PATH=~/.local/share/rousseau/acme.db rousseau chat
```

Aucune des deux approches n'exige un redémarrage de rousseau quand vous sautez entre workspaces — chaque processus ouvre son propre fichier.

## Disposition de workspace par projet

```
~/.config/rousseau/
├── acme.yaml         # provider = anthropic, state.path = …/acme.db
├── personal.yaml     # provider = claudecli, state.path = …/personal.db
└── work.yaml         # provider = bedrock,    state.path = …/work.db
```

Chaque fichier de configuration surcharge `state.path` :

```yaml
state:
  path: /home/seb/.local/share/rousseau/acme.db
```

Puis lancez chaque session avec la bonne configuration. La TUI (`internal/tui/model.go`) affiche l'identifiant de session + le fournisseur dans sa barre de statut — confirmation visuelle que vous êtes dans le bon workspace.

## Partager l'historique entre machines

Le magasin de sessions est un unique fichier SQLite. Le journal WAL est activé par `Open()` dans `internal/state/sqlite/store.go`, donc les snapshots live sont sûrs :

```sh
# Snapshot laptop-vers-desktop (les deux au repos)
rsync -avz --partial \
  ~/.local/share/rousseau/sessions.db \
  desktop:~/.local/share/rousseau/sessions.db
```

**Un seul écrivain à la fois.** N'exécutez pas `rousseau whatsapp` sur deux machines contre le même fichier SQLite via NFS — c'est un comportement non défini. Synchronisez quand rien n'écrit, ou lancez un unique écrivain avec des répliques en lecture.

Une alternative plus sûre est le snapshot `.backup` :

```sh
sqlite3 ~/.local/share/rousseau/sessions.db ".backup '/tmp/sessions.snap.db'"
scp /tmp/sessions.snap.db desktop:~/.local/share/rousseau/sessions.db
```

`.backup` utilise l'API de backup en ligne de SQLite et produit un fichier cohérent à un instant donné.

## Migrer un workspace

Déplacez le répertoire entier ; c'est le workspace :

```sh
rsync -avz ~/.local/share/rousseau/ new-host:~/.local/share/rousseau/
```

`whatsapp.db` (identifiants d'appareil) est séparé — soit vous l'emportez aussi (l'appareil reste appairé), soit vous le laissez et rescannez le QR sur le nouvel hôte.

## Supprimer l'historique d'un workspace

```sh
rousseau session list                 # confirmer ce que vous allez perdre
rm ~/.local/share/rousseau/acme.db*   # inclut les sidecars -wal et -shm
```

Le prochain processus à ouvrir le chemin le recréera avec le schéma de `internal/state/sqlite/schema.sql`.

Si vous voulez seulement supprimer un sous-ensemble de sessions, utilisez la CLI :

```sh
rousseau session delete <id> --yes
```

`rousseau session delete` (`internal/cli/session.go`) appelle `Store.Delete`, qui cascade via les triggers FTS5 pour maintenir la cohérence de l'index de recall. Le flag `--yes` est requis — la commande refuse de s'exécuter sans lui.

## Suppression partielle via SQL

Pour le nettoyage en masse — chaque session de plus de 90 jours :

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions WHERE updated_at < datetime('now', '-90 days');
SQL
```

Les triggers FTS5 (`sessions_fts_ad` dans `internal/state/sqlite/search.go`) se déclenchent sur le DELETE et maintiennent l'index synchronisé automatiquement.

## Approbateurs par workspace

Comme le fichier de configuration et le fichier d'état sont tous deux par workspace, l'approbateur l'est aussi :

```yaml
# work.yaml — approbateur pattern strict
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

state:
  path: /home/seb/.local/share/rousseau/work.db
```

Un `personal.yaml` séparé pourrait garder `mode: allow_all` pour le travail interactif. Voir [Tutorial: Harden the approver](/fr/tutorials/harden-approver-policy/).

## Voir aussi

- [Reference: Session store](/fr/reference/session-store/) — schéma.
- [Guides: Multi-provider](/fr/guides/multi-provider/) — le motif deux-configs, deux-fournisseurs.
- [Reference: Environment Variables](/fr/reference/environment-variables/) — chaque variable d'env de chemin.
- [User Guide: CLI](/fr/user-guide/cli/) — commandes `rousseau session`.
