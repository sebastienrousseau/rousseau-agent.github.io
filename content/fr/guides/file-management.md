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
description: "How rousseau's write and edit tools interact with the workspace bind mount, SELinux :Z labels, container UID mapping, and safe editing outside /workspace."
keywords: "workspace, bind mount, SELinux, :Z, UserNS, write, edit, permissions"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/guides/file-management/"
subtitle: "Workspace bind mount, SELinux :Z, UID mapping, and safe file edits."
tags: "guides, files, container, selinux, workspace"
title: "Guide : gestion des fichiers"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "workspace, bind mount, SELinux, :Z, UserNS, write, edit, permissions"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide : gestion des fichiers"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 37
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/file-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/file-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guide : gestion des fichiers"
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
twitter_description: "How rousseau's write and edit tools interact with the workspace bind mount, SELinux :Z labels, container UID mapping, and safe editing outside /workspace."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide : gestion des fichiers"
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

## Les deux outils

Deux outils modifient le système de fichiers :

- [`write`](/fr/reference/tool-schemas/#write) — écrasement complet du fichier. `internal/tools/builtin/write.go` écrit avec le mode `0o644` et `MkdirAll(dir, 0o755)`.
- [`edit`](/fr/reference/tool-schemas/#edit) — remplacement de chaîne exacte unique à l'intérieur d'un fichier existant. `internal/tools/builtin/edit.go`.

Les deux exigent un **chemin absolu** (ils appellent `filepath.IsAbs`). Les deux ne font pas de bascule atomique — ils utilisent `os.WriteFile` directement.

## La vue du monde depuis le conteneur

L'unité Quadlet de référence dans `docker/rousseau-agent.container` monte trois répertoires hôtes dans le conteneur :

```
Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
Volume=%h/.claude:/home/rousseau/.claude:rw,Z
Volume=%h/team-rousseau-workspace:/workspace:rw,Z
```

Rien d'autre sur l'hôte n'est visible. Depuis l'intérieur du conteneur, un appel d'outil `edit` sur `/workspace/repos/foo/main.go` se résout à `~/team-rousseau-workspace/repos/foo/main.go` sur l'hôte.

### `:Z` — l'étiquette SELinux

Le flag `:Z` sur chaque `Volume=` indique à Podman de ré-étiqueter le montage avec une catégorie SELinux MCS **privée au conteneur**. Sans lui, sur un système avec SELinux en mode enforcing :

- Les lectures fonctionnent la plupart du temps (`container_file_t` est largement lisible).
- Les écritures échouent avec `EACCES` et `avc: denied { write }` dans le log d'audit.

Si vous remplacez le flag par `:z` (minuscule), Podman ré-étiquette avec une catégorie **partagée** — plus sûr pour les hôtes que vous partagez entre plusieurs utilisateurs de conteneurs, mais pas la valeur par défaut.

Sur les systèmes sans SELinux (Debian, Ubuntu non durci), `:Z` est un no-op silencieux.

### `UserNS=keep-id` — cartographie d'UID

Le conteneur s'exécute en UID/GID 1000. Sans cartographie d'espace de noms utilisateur, Podman rootless remappe 1000 dans la plage subuid (typiquement `100000+`), et les fichiers écrits depuis l'intérieur du conteneur appartiendraient à cet UID mappé sur l'hôte — inutilisables pour l'opérateur.

`UserNS=keep-id` mappe l'UID 1000 du conteneur à l'UID de l'utilisateur hôte (également 1000 dans le setup de référence). Les fichiers écrits dans `/workspace` finissent possédés par `seb:seb` sur l'hôte — exactement ce que vous voulez.

Si votre utilisateur hôte n'est pas UID 1000, la cartographie fonctionne toujours ; `keep-id` utilise l'UID réel de l'utilisateur appelant.

## Édition hors de `/workspace`

Parce que les bind mounts sont la seule vue du conteneur sur le système de fichiers hôte, `write` ou `edit` contre `/etc/nginx/nginx.conf` échouera avec une erreur de chemin introuvable — le chemin n'existe simplement pas dans le conteneur. C'est une **fonctionnalité** : cela signifie que la politique d'approbation de l'opérateur peut faire confiance à la frontière du conteneur.

Si vous devez vraiment que le démon touche un chemin hôte différent :

1. **Préféré :** ajoutez une nouvelle ligne `Volume=` à l'unité Quadlet. Faites le choix le moins permissif : `:ro` pour lecture seule, `:Z` pour un étiquetage SELinux privé.
2. **Ne lancez pas** rousseau hors du conteneur pour contourner la frontière — vous perdez seccomp, le retrait de capacités et le système de fichiers racine en lecture seule.

## Édition hors du conteneur

Si vous exécutez rousseau directement sur l'hôte (sans conteneur), les outils opèrent contre la vue du processus démon — tout ce qui se trouve sous le HOME de l'utilisateur par défaut. L'approbateur est la seule couche de confinement. Voir [Guides: Audit + approval policies](/fr/guides/audit-approval-policies/) pour la recette pattern-mode + `default: deny`.

## `write` vs `edit` — quand utiliser lequel

| Situation | Utiliser |
|---|---|
| Créer un nouveau fichier. | `write`. |
| Réécrire un fichier en entier. | `write`. |
| Modifier une section d'un grand fichier. | `edit`. Il échoue proprement quand `old_string` n'est pas unique. |
| Renommer un symbole dans tout le fichier. | Plusieurs appels `edit` avec de plus en plus de contexte environnant, ou un unique `write` avec le contenu entièrement réécrit. N'utilisez pas `edit` avec une sémantique de type `replace_all` — l'outil refuse. |

La contrainte d'unicité exacte sur `edit` est délibérée. Elle est empruntée directement à l'outil Edit de Claude Code. Cherchez dans `internal/tools/builtin/edit.go` le bloc de commentaire qui l'explique.

## Modes de défaillance courants

| Symptôme | Cause | Correction |
|---|---|---|
| `edit: path must be absolute, got "…"` | Le modèle a passé un chemin relatif. | Rejeter ou réécrire dans l'approbateur ; demander au modèle d'utiliser des chemins absolus. |
| `edit: old_string not found in …` | Le fichier a changé depuis la dernière lecture du modèle, ou le modèle a halluciné le contexte environnant. | Le modèle relira typiquement et réessayera. |
| `edit: old_string is not unique in … (found 3 occurrences)` | La même chaîne apparaît plusieurs fois. | Le modèle doit fournir davantage de lignes environnantes pour lever l'ambiguïté. |
| `write: permission denied` | Mauvaise étiquette SELinux ou mauvaise cartographie d'UID. | Vérifier `:Z` sur le volume et `UserNS=keep-id` sur le conteneur. |
| `read: does not look like UTF-8 text` | Le fichier contient des octets NUL dans les 512 premiers octets (`isLikelyText` dans `read.go`). | Refuser les lectures binaires au niveau approbateur ; utiliser l'outil `bash` avec `file` si l'identification est nécessaire. |

## Sauvegardes avant grosses réécritures

Les outils ne créent pas de copies `.bak`. Pour les changements à haut risque, apprenez au modèle à écrire d'abord vers un chemin voisin, faire un diff avec `bash`, puis basculer. Alternativement, tout passer par une branche git — rousseau laisse `git` complètement hors de son chemin d'exécution, donc tout versionnage se fait via votre flux de travail habituel.

## Voir aussi

- [Reference: Tool schemas](/fr/reference/tool-schemas/) — schémas d'entrée exacts.
- [User Guide: Tools](/fr/user-guide/tools/).
- [Deployment](/fr/deployment/) — l'unité Quadlet qui définit les bind mounts.
- [Guides: Audit + approval policies](/fr/guides/audit-approval-policies/) — restreindre les écritures à une arborescence de répertoires.
