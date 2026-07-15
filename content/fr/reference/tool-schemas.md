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
description: "The exact JSON schemas for the five built-in tools rousseau ships: read, write, edit, grep, bash."
keywords: "tool schemas, read, write, edit, grep, bash, JSON Schema"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/reference/tool-schemas/"
subtitle: "JSON schemas for the five built-in tools, verbatim from internal/tools/builtin."
tags: "reference, tools, json-schema, read, write, edit, grep, bash"
title: "Référence : schémas des outils"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tool schemas, read, write, edit, grep, bash, JSON Schema"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Référence : schémas des outils"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 54
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/tool-schemas/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/tool-schemas/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Référence : schémas des outils"
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
twitter_description: "The exact JSON schemas for the five built-in tools rousseau ships: read, write, edit, grep, bash."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Référence : schémas des outils"
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

## Ce qu'est cette page

Chaque outil intégré dans `internal/tools/builtin/*.go` publie une méthode `InputSchema()` qui retourne une map JSON Schema. Cette page reproduit ces schémas exactement, plus un paragraphe sur le contrat d'exécution de chaque outil.

Les cinq outils intégrés sont : [`read`](#read), [`write`](#write), [`edit`](#edit), [`grep`](#grep), [`bash`](#bash). Tous les cinq sont construits dans le câblage du démon ; l'approbateur (`internal/agent/approver.go`) se place entre l'appel d'outil du modèle et la méthode `Execute` de l'outil.

## read

Source : `internal/tools/builtin/read.go`.

**Description (exposée au modèle) :** _Read the contents of a UTF-8 text file. Input: absolute path. Returns file contents or an error._

**Schéma d'entrée :**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "Absolute filesystem path to the file to read."
    }
  },
  "required": ["path"]
}
```

**Contrat.** Le `path` doit être absolu (`filepath.IsAbs`). L'outil lit tout le fichier en mémoire et le rejette si les 512 premiers octets contiennent un octet NUL (`isLikelyText`). Retourne le contenu du fichier sous forme de chaîne en cas de succès ; une erreur sinon. Aucune limite de nombre de lignes ou de taille n'est imposée au niveau de l'outil — les politiques d'approbation sont le bon endroit pour borner la taille des fichiers.

## write

Source : `internal/tools/builtin/write.go`.

**Description (exposée au modèle) :** _Write UTF-8 text to a file, replacing existing contents. Creates parent directories as needed. Input: absolute path + content._

**Schéma d'entrée :**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "Absolute filesystem path to write."
    },
    "content": {
      "type": "string",
      "description": "The complete file contents to write."
    }
  },
  "required": ["path", "content"]
}
```

**Contrat.** Réécriture complète du fichier. Crée les répertoires parents avec le mode `0o755`. Écrit avec le mode `0o644`. Chemin absolu requis. Retourne `"wrote N bytes to /path"`. Il n'y a délibérément pas de danse d'atomic-swap — les approbateurs en mode pattern épinglent la cible d'écriture à une arborescence spécifique ; l'outil lui-même ne cherche pas à être malin sur la sécurité du système de fichiers.

## edit

Source : `internal/tools/builtin/edit.go`.

**Description (exposée au modèle) :** _Replace exactly one occurrence of old_string with new_string in a file. old_string must be unique in the file; if it appears zero or multiple times the edit fails. Preserve indentation exactly._

**Schéma d'entrée :**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "Absolute filesystem path to the file to edit."
    },
    "old_string": {
      "type": "string",
      "description": "Exact text to find. Must be unique in the file."
    },
    "new_string": {
      "type": "string",
      "description": "Text to replace old_string with."
    }
  },
  "required": ["path", "old_string", "new_string"]
}
```

**Contrat.** Remplacement exact de chaîne, pas regex. `old_string` doit apparaître **exactement une fois** dans le fichier — zéro correspondance ou plusieurs correspondances échouent toutes deux avec une erreur descriptive, ce qui est intentionnel (emprunté à l'outil Edit de Claude Code). Empêche le remplacement en masse accidentel et force le modèle à inclure suffisamment de contexte environnant pour désambiguïser. `old_string == new_string` échoue aussi. Retourne `"edited /path (1 replacement)"`.

## grep

Source : `internal/tools/builtin/grep.go`.

**Description (exposée au modèle) :** _Search files under a directory for a Go regular expression. Skips binary files and files larger than the configured limit. Returns 'path:line: matched_line' rows._

**Schéma d'entrée :**

```json
{
  "type": "object",
  "properties": {
    "pattern": {
      "type": "string",
      "description": "Go RE2 regular expression to match."
    },
    "path": {
      "type": "string",
      "description": "Absolute directory to search under."
    },
    "include": {
      "type": "string",
      "description": "Optional filename glob (e.g. '*.go'). Applied to the base name."
    },
    "ignore_case": {
      "type": "boolean",
      "description": "Case-insensitive match. Defaults to false."
    }
  },
  "required": ["pattern", "path"]
}
```

**Contrat.** Regex RE2, pas PCRE. Insensible à la casse quand `ignore_case: true` (implémenté en préfixant par `(?i)`). Saute les répertoires nommés `.git`, `node_modules`, `vendor`, `.venv`, `__pycache__`, `dist`, `build`. Saute les fichiers plus grands que `MaxFileBytes` (défaut 4 Mio). Tronque la sortie à `MaxMatches` (défaut 200) et ajoute un pied de page `(truncated at N matches)` quand il atteint le plafond. Saute les fichiers qui contiennent un octet NUL sur la ligne courante (détection binaire grossière).

## bash

Source : `internal/tools/builtin/bash.go`.

**Description (exposée au modèle) :** _Execute a shell command via `/bin/sh -c`. Returns combined stdout+stderr with exit status._

**Schéma d'entrée :**

```json
{
  "type": "object",
  "properties": {
    "command": {
      "type": "string",
      "description": "The shell command to execute."
    }
  },
  "required": ["command"]
}
```

**Contrat.** `/bin/sh -c <command>`. stdout + stderr combinés, plafonnés à ce qui tient dans un `bytes.Buffer` (c.-à-d. la RAM). Timeout de 60 secondes par défaut (configurable à la construction). En cas de timeout : retourne la sortie partielle plus une erreur `bash: timed out after 60s`. **Aucun sandboxing au niveau de l'outil.** L'utilisateur OS du démon, la vue du système de fichiers, la posture réseau et le profil seccomp sont la ceinture. Les approbateurs en mode pattern sont la manière de restreindre les commandes autorisées — voir [Tutoriel : durcir l'approbateur](/fr/tutorials/harden-approver-policy/).

## Outils exposés via MCP

Le serveur MCP stdio de Rousseau (`rousseau mcp`) expose un ensemble **différent** d'outils — requêtes en lecture seule sur le magasin de sessions et les tâches cron. Voir [MCP : outils exposés](/fr/mcp/exposed-tools/) pour `rousseau_search_sessions`, `rousseau_list_sessions`, `rousseau_read_session`, `rousseau_cron_list`.

## Voir aussi

- [Guide utilisateur : outils](/fr/user-guide/tools/) — la vue orientée opérateur.
- [Guides : gestion des fichiers](/fr/guides/file-management/) — comment `write`/`edit` interagissent avec les montages et SELinux.
- [Guides : Audit + politiques d'approbation](/fr/guides/audit-approval-policies/) — comment les regex de pattern contraignent l'entrée de chaque outil.
- [Guide développeur : ajouter un outil](/fr/developer-guide/add-a-tool/) — étendre cet ensemble.
