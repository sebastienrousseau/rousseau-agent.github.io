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
description: "Compact reference table of every rousseau-agent command mirroring the output of rousseau --help."
keywords: "cli, commands, reference, table, rousseau --help"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/reference/cli-commands/"
subtitle: "Every command tabulated."
tags: "reference, cli, commands"
title: "Commandes CLI"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cli, commands, reference, table, rousseau --help"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Commandes CLI"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 50
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/cli-commands/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/cli-commands/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Commandes CLI"
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
twitter_description: "Compact reference table of every rousseau-agent command mirroring the output of rousseau --help."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Commandes CLI"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Ce que vous allez apprendre</span><p>La surface complète de la CLI <code>rousseau</code> : chaque commande, ses flags, la sémantique des codes de sortie et les clés de config que chaque flag surcharge. C'est la référence scannable — voir <a href="/fr/user-guide/cli/">Guide utilisateur : CLI</a> pour une présentation avec exemples.</p></aside>

## Arborescence de commandes

Chaque commande expose son aide via `rousseau <cmd> --help`. Cette page en est le résumé tabulé.

| Commande | Description |
|---|---|
| `chat` | Ouvre la TUI Bubble Tea interactive. |
| `whatsapp` | Exécute le pont WhatsApp (whatsmeow). |
| `signal` | Exécute le pont Signal (JSON-RPC signal-cli). |
| `telegram` | Exécute le long-poller Bot API Telegram. |
| `matrix` | Exécute le pont client-server Matrix. |
| `slack` | Exécute le pont Slack Socket Mode. |
| `discord` | Exécute le pont Gateway Discord. |
| `sms` | SMS envoi seul via Twilio ou Vonage. |
| `imessage` | Pont iMessage adossé à BlueBubbles. |
| `email` | Pont IMAP entrant + SMTP sortant. |
| `mcp` | Démarre le serveur MCP JSON-RPC 2.0 sur stdio. |
| `cron add` | Ajoute un prompt planifié. |
| `cron list` | Liste chaque tâche planifiée. |
| `cron remove` | Supprime une tâche planifiée. |
| `cron enable` | Active une tâche planifiée désactivée. |
| `cron disable` | Désactive une tâche planifiée activée. |
| `session list` | Liste les sessions du magasin, plus récentes d'abord. |
| `session search` | Recherche FTS5 sur le contenu des messages de chaque session. |
| `session show` | Imprime l'historique des messages d'une session. |
| `session delete` | Supprime une session. |
| `skills list` | Liste les skills découverts dans `skills_dir`. |
| `skills show` | Imprime le front-matter YAML et le corps d'un skill. |
| `skills lint` | Valide la conformité des skills au schéma. |
| `doctor` | Diagnostique l'installation locale. Imprime un rapport. |
| `status` | Imprime le statut du démon. |
| `init` | Écrit une config par défaut dans `~/.config/rousseau/`. |
| `version` | Imprime la version, le commit et la date de build. |

## Flags globaux

Chaque commande accepte ceux-ci :

| Flag | Type | Clé de config | Notes |
|---|---|---|---|
| `--config` | string | — | Charge la configuration depuis ce fichier. Défaut : `$XDG_CONFIG_HOME/rousseau/config.yaml`. |
| `--help`, `-h` | bool | — | Imprime l'aide de la commande courante. |

## Flags par transport

### `rousseau whatsapp`

| Flag | Type | Clé de config | Notes |
|---|---|---|---|
| `--store` | string | — | Chemin du magasin d'appareils whatsmeow. Défaut `$XDG_DATA_HOME/rousseau/whatsapp.db`. |
| `--allow` | []string | `whatsapp.allowlist` | Restreint l'entrant à ces JID. Répétable. |

### `rousseau slack`

| Flag | Type | Clé de config |
|---|---|---|
| `--app-token` | string | `slack.app_token` |
| `--bot-token` | string | `slack.bot_token` |
| `--bot-user-id` | string | `slack.bot_user_id` |
| `--allow` | []string | `slack.allowlist` |

### `rousseau discord`

| Flag | Type | Clé de config |
|---|---|---|
| `--token` | string | `discord.token` |
| `--allow` | []string | `discord.allowlist` |

### `rousseau telegram`

| Flag | Type | Clé de config |
|---|---|---|
| `--token` | string | `telegram.token` |
| `--allow` | []string | `telegram.allowlist` |

### `rousseau matrix`

| Flag | Type | Clé de config |
|---|---|---|
| `--homeserver-url` | string | `matrix.homeserver_url` |
| `--access-token` | string | `matrix.access_token` |
| `--user-id` | string | `matrix.user_id` |
| `--allow` | []string | `matrix.allowlist` |

### `rousseau signal`

| Flag | Type | Clé de config |
|---|---|---|
| `--account` | string | `signal.account` |
| `--binary` | string | `signal.binary` |
| `--allow` | []string | `signal.allowlist` |

### `rousseau email`

| Flag | Type | Clé de config |
|---|---|---|
| `--imap-addr` | string | `email.imap_addr` |
| `--imap-username` | string | `email.imap_username` |
| `--imap-password` | string | `email.imap_password` |
| `--smtp-addr` | string | `email.smtp_addr` |
| `--smtp-username` | string | `email.smtp_username` |
| `--smtp-password` | string | `email.smtp_password` |
| `--from` | string | `email.from` |
| `--mailbox` | string | `email.mailbox` |
| `--poll-interval` | string | `email.poll_interval` |

### `rousseau sms`

| Flag | Type | Clé de config |
|---|---|---|
| `--provider` | string | `sms.provider` |
| `--from` | string | `sms.from` |
| `--to` | string | (positionnel) |

### `rousseau imessage`

| Flag | Type | Clé de config |
|---|---|---|
| `--base-url` | string | `imessage.base_url` |
| `--password` | string | `imessage.password` |
| `--chat-guid` | string | `imessage.chat_guid` |

## Codes de sortie

| Code | Signification |
|---|---|
| 0 | Sortie propre — commande terminée. Pas typique pour les démons longue durée (ils se terminent généralement sur signal). |
| 1 | Toute erreur remontée par `Execute`. Voir [Référence : codes de sortie](/fr/reference/exit-codes/) pour la classification. |

## Précédence

Les valeurs de config sont résolues dans l'ordre **flag &gt; env &gt; fichier &gt; défaut** (voir `config.Load` dans `internal/config/config.go`). Les variables d'environnement sont préfixées `ROUSSEAU_` avec les points remplacés par des underscores — par ex. `ROUSSEAU_ANTHROPIC_MODEL` surcharge `anthropic.model`. La variable `ANTHROPIC_API_KEY` nue est également honorée (cas spécial dans `config.Load`).

## Dépannage

### `unknown flag: --allow` sur `rousseau chat`

`--allow` est propre au transport. `chat` n'a pas d'allowlist car il n'y a pas d'ingress. Utilisez `rousseau whatsapp --allow …` à la place.

### L'ordre des flags compte pour les flags répétables

`--allow A --allow B` fait deux valeurs, mais `--allow=A,B` fait une valeur qui contient une virgule. Préférez des flags séparés.

### Surcharge env non prise en compte

Rousseau lit env uniquement au démarrage. Redémarrez le démon après avoir modifié les variables d'environnement, ou utilisez `--config` pour forcer un rechargement.

### `flag provided but not defined`

Cobra rejette les flags inconnus. Si vous copiez un flag d'une version plus récente, vérifiez `rousseau <cmd> --help` pour l'orthographe courante.

## Pages associées

- [Guide utilisateur : CLI](/fr/user-guide/cli/) — chaque commande avec exemples.
- [Référence : codes de sortie](/fr/reference/exit-codes/) — sémantique des signaux.
- [Référence : schéma de config](/fr/reference/config-schema/) — chaque champ de configuration.
- [Référence : variables d'environnement](/fr/reference/environment-variables/) — matrice de surcharges env.
- [Configuration](/fr/configuration/) — présentation complète du fichier de config.

## Pour aller plus loin

- `internal/cli/root.go` — arborescence de commandes Cobra.
- `internal/cli/*.go` — un fichier par sous-commande.
- `internal/config/config.go` — `Load` et résolution des défauts.
