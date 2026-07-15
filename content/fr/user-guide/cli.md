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
description: "Full CLI reference for rousseau-agent: every command, every flag, exit codes, per-transport subcommands."
keywords: "cli, cobra, commands, flags, subcommands, exit codes"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/user-guide/cli/"
subtitle: "Every command, every flag."
tags: "cli, reference, commands"
title: "Référence CLI"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cli, cobra, commands, flags, subcommands, exit codes"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Référence CLI"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 40
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/cli/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/cli/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Référence CLI"
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
twitter_description: "Full CLI reference for rousseau-agent: every command, every flag, exit codes, per-transport subcommands."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Référence CLI"
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

## Invocation

```
rousseau [--config <path>] <command> [flags]
```

Chaque commande lit les valeurs par défaut depuis `~/.config/rousseau/config.yaml` (ou le fichier passé via `--config`). Les flags surchargent les variables d'env, les variables d'env surchargent le fichier, le fichier surcharge les valeurs codées en dur.

## Flags globaux

| Flag | Type | Défaut | Notes |
|---|---|---|---|
| `--config` | string | `$XDG_CONFIG_HOME/rousseau/config.yaml` | Charge la configuration depuis ce fichier. Absent signifie le chemin XDG par défaut. |
| `--help`, `-h` | bool | — | Affiche l'aide pour la commande actuelle. |

## Arborescence des commandes

```
rousseau
├── chat                TUI Bubble Tea
├── whatsapp            Pont WhatsApp (whatsmeow)
├── signal              Pont Signal (JSON-RPC signal-cli)
├── telegram            Long polling Telegram Bot API
├── matrix              API client-serveur Matrix
├── slack               Slack Socket Mode
├── discord             Discord Gateway
├── sms                 SMS en envoi seul (Twilio / Vonage)
├── imessage            Pont iMessage via BlueBubbles
├── email               IMAP entrant + SMTP sortant
├── mcp                 Serveur MCP JSON-RPC 2.0 sur stdio
├── cron                Gestion des prompts planifiés
├── session             Inspection / suppression du magasin de sessions
├── skills              Lister / afficher / linter les skills
├── doctor              Diagnostiquer l'installation locale
├── status              Afficher le statut du démon
├── init                Écrire une configuration par défaut dans ~/.config/rousseau/
└── version             Afficher la version, le commit, la date de build
```

## `rousseau chat`

Ouvre la TUI Bubble Tea interactive.

| Flag | Type | Défaut | Notes |
|---|---|---|---|
| `--session` | string | — | Reprend une session existante par ID. |
| `--title` | string | horodatage | Titre pour une nouvelle session. |

## `rousseau whatsapp`

Exécute le pont WhatsApp. Affiche un QR code au premier lancement.

| Flag | Type | Défaut | Notes |
|---|---|---|---|
| `--store` | string | `$XDG_DATA_HOME/rousseau/whatsapp.db` | Chemin du magasin d'appareils whatsmeow. |
| `--allow` | []string | aucun | Restreint la gestion entrante à ces JIDs. Répétable. **Ne laissez jamais vide sur un numéro public.** |

## `rousseau signal`

Exécute le pont Signal. Lance `signal-cli jsonRpc` en sous-processus.

| Flag | Type | Défaut | Notes |
|---|---|---|---|
| `--account` | string | depuis `signal.account` | Numéro E.164 sous lequel le démon opère. |
| `--binary` | string | `signal-cli` | Chemin de l'exécutable signal-cli. |
| `--allow` | []string | aucun | Restreint l'entrant à ces numéros E.164. |

## `rousseau telegram`

Exécute le long-poller de l'API Bot Telegram.

| Flag | Type | Défaut | Notes |
|---|---|---|---|
| `--token` | string | depuis `telegram.token` | Jeton BotFather. |
| `--allow` | []string | aucun | Restreint l'entrant à ces chat IDs. |

## `rousseau matrix`

Exécute le pont Matrix.

| Flag | Type | Défaut | Notes |
|---|---|---|---|
| `--homeserver-url` | string | depuis la configuration | par ex. `https://matrix.org`. |
| `--access-token` | string | depuis la configuration | Jeton d'accès du bot. |
| `--user-id` | string | depuis la configuration | ID utilisateur Matrix du bot (`@bot:matrix.org`). |
| `--allow` | []string | aucun | Restreint l'entrant à ces IDs utilisateur. |

## `rousseau slack`

Exécute le pont Slack Socket Mode.

| Flag | Type | Défaut | Notes |
|---|---|---|---|
| `--app-token` | string | depuis la configuration | Jeton Socket Mode `xapp-...`. |
| `--bot-token` | string | depuis la configuration | Jeton OAuth Bot User `xoxb-...`. |
| `--allow` | []string | aucun | Restreint l'entrant à ces IDs utilisateur Slack. |

## `rousseau discord`

Exécute le pont Discord Gateway.

| Flag | Type | Défaut | Notes |
|---|---|---|---|
| `--token` | string | depuis la configuration | Jeton du bot. |
| `--allow` | []string | aucun | Restreint l'entrant à ces IDs utilisateur Discord. |

## `rousseau sms`

SMS en envoi seul via Twilio ou Vonage. Aucun entrant.

| Flag | Type | Défaut | Notes |
|---|---|---|---|
| `--provider` | string | depuis la configuration | `twilio` ou `vonage`. |
| `--from` | string | depuis la configuration | Numéro d'envoi E.164. |
| `--account-sid` | string | depuis la configuration | Account SID Twilio. |
| `--auth-token` | string | depuis la configuration | Auth token Twilio ou secret Vonage. |
| `--api-key` | string | depuis la configuration | Clé API Vonage. |

## `rousseau imessage`

Pont iMessage via BlueBubbles.

| Flag | Type | Défaut | Notes |
|---|---|---|---|
| `--base-url` | string | `http://localhost:1234` | URL du serveur BlueBubbles. |
| `--password` | string | depuis la configuration | Mot de passe du serveur BlueBubbles. |
| `--chat-guid` | string | depuis la configuration | Cible sortante. |
| `--poll-interval` | duration | 5s | Fréquence de polling des nouveaux messages. |
| `--allow` | []string | aucun | Restreint l'entrant. |

## `rousseau email`

Pont email sur IMAP + SMTP.

| Flag | Type | Défaut | Notes |
|---|---|---|---|
| `--imap-addr` | string | depuis la configuration | par ex. `imap.example.com:993`. |
| `--imap-username`, `--imap-password` | string | depuis la configuration | Identifiants IMAP. |
| `--smtp-addr` | string | depuis la configuration | par ex. `smtp.example.com:587`. |
| `--smtp-username`, `--smtp-password` | string | depuis la configuration | Identifiants SMTP. |
| `--from` | string | depuis la configuration | Expéditeur d'enveloppe. |
| `--poll-interval` | duration | 30s | Cadence de polling IMAP. |
| `--allow` | []string | aucun | Restreint les adresses d'expéditeur entrant. |

## `rousseau mcp`

Démarre le serveur MCP sur stdio. Aucun flag — chaque paramètre vit dans `config.yaml`.

## `rousseau cron`

| Sous-commande | Description |
|---|---|
| `cron add` | Ajoute un prompt planifié. Flags : `--name`, `--schedule` (cron 5 champs), `--prompt`, `--deliver-to`. |
| `cron list` | Liste chaque job avec le statut `on/off` et l'horodatage de dernière exécution. |
| `cron remove <name-or-id>` | Supprime un job. |
| `cron enable <name-or-id>` | Active un job désactivé. |
| `cron disable <name-or-id>` | Désactive un job actif (sans le supprimer). |

## `rousseau session`

| Sous-commande | Description |
|---|---|
| `session list` | Liste les sessions du magasin, plus récentes d'abord. |
| `session search <query>` | Recherche FTS5 sur le contenu de chaque session. |
| `session show <id>` | Affiche l'historique de messages d'une session. |
| `session delete <id>` | Supprime une session. |

## `rousseau skills`

| Sous-commande | Description |
|---|---|
| `skills list` | Liste les skills découverts depuis `skills_dir`. |
| `skills show <name>` | Affiche le front-matter YAML et le corps d'un skill. |
| `skills lint` | Valide la conformité des skills au schéma. |

## `rousseau doctor`

Parcourt chaque dépendance runtime et chaque choix de configuration. Affiche un rapport de statut avec des lignes étiquetées `ok`, `warn`, `fail`, `info`. Code de sortie 1 si une ligne est `fail`.

Aucun flag aujourd'hui ; étendez via `--config` au niveau global.

## `rousseau status`

Affiche un résumé compact du statut du démon — fournisseur, nombre de sessions, jobs cron. En lecture seule.

## `rousseau init`

Écrit un `config.yaml` par défaut dans `~/.config/rousseau/`. Refuse d'écraser un fichier existant sauf si `--force` est passé.

| Flag | Type | Défaut | Notes |
|---|---|---|---|
| `--force` | bool | false | Écrase une configuration existante. |

## `rousseau version`

Affiche la version, le hash de commit et la date de build. Estampillés à la compilation via `-ldflags`.

## Codes de sortie

| Code | Signification |
|---|---|
| 0 | La commande s'est terminée avec succès. |
| 1 | La commande a échoué. L'erreur est affichée sur stderr. |

Voir [Reference: Exit Codes](/fr/reference/exit-codes/) pour la sémantique des signaux du démon.

## Variables d'environnement

Chaque champ de configuration peut être surchargé par une variable d'environnement en utilisant le préfixe `ROUSSEAU_` et `_` comme séparateur de section : `ROUSSEAU_LOG_LEVEL=debug`, `ROUSSEAU_ANTHROPIC_API_KEY=sk-ant-...`, etc.

Le cas spécial est `ANTHROPIC_API_KEY` (sans préfixe) — elle est reprise directement par le chargeur de configuration par convention.

## Dépannage

### `unknown command` lors du passage d'une sous-commande

Les sous-commandes de rousseau sont déclarées dans `internal/cli/root.go`. Si `rousseau <cmd>` renvoie inconnu, soit le flag est mal orthographié soit vous êtes sur un binaire plus ancien. `rousseau version` montre ce que vous avez.

### Les flags répétables nécessitent plusieurs invocations

`--allow` accepte un JID par flag. Répétez le flag pour plusieurs valeurs : `--allow A --allow B`, pas `--allow A,B`.

### Les variables d'env sont ignorées silencieusement

Rousseau utilise le préfixe `ROUSSEAU_` + un séparateur de section underscore : `anthropic.model` devient `ROUSSEAU_ANTHROPIC_MODEL`. La casse compte.

### `rousseau chat` n'affiche qu'un écran blanc

La TUI Bubble Tea a besoin d'un terminal ANSI-compatible. Définissez `TERM=xterm-256color` et exécutez de manière interactive (pas sous `nohup` ni derrière un pipe).

### La commande sort en 0 immédiatement

Certains flags (`--help`, variantes `--version`) court-circuitent. Si votre commande ne s'exécute pas, vérifiez les flags passés.

## Pages liées

- [User Guide: TUI](/fr/user-guide/tui/) — raccourcis dans `rousseau chat`.
- [User Guide: Tools](/fr/user-guide/tools/) — schéma JSON de chaque outil intégré.
- [Reference: CLI Commands](/fr/reference/cli-commands/) — table des commandes.
- [Reference: Environment Variables](/fr/reference/environment-variables/) — matrice de surcharge.
- [Configuration](/fr/configuration/) — le fichier de configuration derrière chaque commande.

## Lecture complémentaire

- `internal/cli/root.go` — l'arbre Cobra.
- `internal/cli/chat.go`, `internal/cli/whatsapp.go`, `internal/cli/slack.go`, … — un fichier par sous-commande.
- `internal/config/config.go` — résolution variable d'env / flag.
