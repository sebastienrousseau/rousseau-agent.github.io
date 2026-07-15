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
description: "Every environment variable rousseau-agent reads: the ROUSSEAU_ prefix from Viper, ANTHROPIC_API_KEY, XDG paths, provider SDK variables."
keywords: "environment variables, ROUSSEAU_, ANTHROPIC_API_KEY, viper, XDG"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/reference/environment-variables/"
subtitle: "Every environment variable rousseau reads, at what layer, with what default."
tags: "reference, environment, viper, secrets"
title: "Référence : variables d'environnement"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "environment variables, ROUSSEAU_, ANTHROPIC_API_KEY, viper, XDG"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Référence : variables d'environnement"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 51
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/environment-variables/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/environment-variables/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Référence : variables d'environnement"
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
twitter_description: "Every environment variable rousseau-agent reads: the ROUSSEAU_ prefix from Viper, ANTHROPIC_API_KEY, XDG paths, provider SDK variables."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Référence : variables d'environnement"
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

## Comment rousseau lit l'environnement

Deux mécanismes, dans cet ordre (voir `config.Load` dans `internal/config/config.go`) :

1. **Liaison automatique env de Viper.** `SetEnvPrefix("ROUSSEAU")` plus `SetEnvKeyReplacer(".", "_")` signifie que chaque champ de config est accessible via `ROUSSEAU_<UPPER_SNAKE>`. Ainsi `provider` devient `ROUSSEAU_PROVIDER`, `agent.approver.mode` devient `ROUSSEAU_AGENT_APPROVER_MODE`.
2. **Surcharge explicite.** `ANTHROPIC_API_KEY` est lu directement dans l'environnement et forcé dans `anthropic.api_key`, pour que la convention standard du SDK Anthropic fonctionne d'emblée. Aucune autre clé n'est captée implicitement.

Tout le reste de cette page est soit une variable mappée par Viper, soit une variable gérée par SDK que rousseau ne touche pas mais que la bibliothèque sous-jacente utilise, soit un chemin XDG servant à calculer les défauts.

La précédence reste : **flag > env > fichier > défaut**.

## Préfixe `ROUSSEAU_*`

Chaque tag `mapstructure` dans `internal/config/config.go` est accessible via `ROUSSEAU_<UPPER_SNAKE_PATH>`. Exemples sélectionnés — la liste complète suit la structure de config :

| Variable | Catégorie | Défaut | Description |
|---|---|---|---|
| `ROUSSEAU_PROVIDER` | core | `claudecli` | Provider identifier: `claudecli`, `anthropic`, `openai`, `openrouter`, `ollama`, `bedrock`, `vertex`. |
| `ROUSSEAU_LOG_LEVEL` | logging | `info` | slog level: `debug`, `info`, `warn`, `error`. |
| `ROUSSEAU_LOG_FORMAT` | logging | `text` | `text` or `json`. |
| `ROUSSEAU_STATE_PATH` | state | `$HOME/.local/share/rousseau/sessions.db` | Session store DSN. |
| `ROUSSEAU_AGENT_MAX_ITERATIONS` | agent | `32` | Tool-use iteration cap per turn. |
| `ROUSSEAU_AGENT_APPROVER_MODE` | agent | `` | `allow_all`, `deny_all`, `pattern`. |
| `ROUSSEAU_AGENT_APPROVER_DEFAULT` | agent | `` | For `pattern`: `allow` or `deny` on unmatched calls. |
| `ROUSSEAU_AGENT_COMPRESSION_ENABLED` | agent | `false` | Turn on the LLM compressor. |
| `ROUSSEAU_AGENT_COMPRESSION_TRIGGER_MESSAGES` | agent | `60` | Compress once message count exceeds this. |
| `ROUSSEAU_AGENT_COMPRESSION_KEEP_RECENT` | agent | `8` | How many recent messages to preserve verbatim. |
| `ROUSSEAU_AGENT_SKILLS_DIR` | agent | `$HOME/.local/share/rousseau/skills` | Skills directory. |
| `ROUSSEAU_ANTHROPIC_API_KEY` | provider | — | Same as `ANTHROPIC_API_KEY`. |
| `ROUSSEAU_ANTHROPIC_MODEL` | provider | `claude-sonnet-4-6` | Anthropic model id. |
| `ROUSSEAU_ANTHROPIC_MAX_TOKENS` | provider | `4096` | Max response tokens. |
| `ROUSSEAU_CLAUDECLI_BINARY` | provider | `claude` | Executable name for the `claudecli` provider. |
| `ROUSSEAU_CLAUDECLI_MODEL` | provider | — | Passed to `claude --model`. |
| `ROUSSEAU_CLAUDECLI_PERMISSION_MODE` | provider | — | `default`, `acceptEdits`, `bypassPermissions`, `plan`, etc. |
| `ROUSSEAU_OPENAI_API_KEY` | provider | — | Bearer for OpenAI-compat endpoints. |
| `ROUSSEAU_OPENAI_MODEL` | provider | — | Model id. |
| `ROUSSEAU_OPENAI_BASE_URL` | provider | — | Override the endpoint. |
| `ROUSSEAU_OPENROUTER_API_KEY` | provider | — | Bearer for OpenRouter. |
| `ROUSSEAU_OPENROUTER_MODEL` | provider | — | Model slug. |
| `ROUSSEAU_OPENROUTER_BASE_URL` | provider | `https://openrouter.ai/api/v1` | Override endpoint. |
| `ROUSSEAU_OLLAMA_MODEL` | provider | — | Model tag. |
| `ROUSSEAU_OLLAMA_BASE_URL` | provider | `http://localhost:11434/v1` | Local Ollama endpoint. |
| `ROUSSEAU_BEDROCK_REGION` | provider | — | AWS region. |
| `ROUSSEAU_BEDROCK_MODEL` | provider | — | Bedrock model id. |
| `ROUSSEAU_BEDROCK_PROFILE` | provider | — | AWS named profile. |
| `ROUSSEAU_VERTEX_PROJECT` | provider | — | GCP project. |
| `ROUSSEAU_VERTEX_REGION` | provider | — | Vertex region. |
| `ROUSSEAU_VERTEX_MODEL` | provider | — | Anthropic-on-Vertex model. |
| `ROUSSEAU_VERTEX_CREDENTIALS_FILE` | provider | — | Path to service-account JSON. |
| `ROUSSEAU_WHATSAPP_REPLY_HEADER` | transport | `💎 *Rousseau Agent*\n\n` | Prepended to every WhatsApp outbound message. |
| `ROUSSEAU_WHATSAPP_VOICE_ENABLED` | transport | `false` | Enable whisper transcription of voice notes. |
| `ROUSSEAU_WHATSAPP_VOICE_BINARY` | transport | `whisper` | whisper.cpp executable. |
| `ROUSSEAU_WHATSAPP_VOICE_MODEL` | transport | — | whisper model name (`base.en`, `small`). |
| `ROUSSEAU_WHATSAPP_VOICE_MODEL_PATH` | transport | — | Explicit .bin path (takes precedence over model). |
| `ROUSSEAU_WHATSAPP_VOICE_LANGUAGE` | transport | — | ISO code; empty auto-detects. |
| `ROUSSEAU_SIGNAL_BINARY` | transport | `signal-cli` | signal-cli executable. |
| `ROUSSEAU_SIGNAL_ACCOUNT` | transport | — | E.164 phone number. |
| `ROUSSEAU_SIGNAL_REPLY_HEADER` | transport | — | Reply header. |
| `ROUSSEAU_TELEGRAM_TOKEN` | transport | — | Bot API token. |
| `ROUSSEAU_TELEGRAM_BASE_URL` | transport | — | Override Bot API endpoint. |
| `ROUSSEAU_MATRIX_HOMESERVER_URL` | transport | — | Homeserver base URL. |
| `ROUSSEAU_MATRIX_ACCESS_TOKEN` | transport | — | Matrix access token. |
| `ROUSSEAU_MATRIX_USER_ID` | transport | — | Full MXID (`@bot:example.org`). |
| `ROUSSEAU_SLACK_APP_TOKEN` | transport | — | `xapp-…` app-level token. |
| `ROUSSEAU_SLACK_BOT_TOKEN` | transport | — | `xoxb-…` bot token. |
| `ROUSSEAU_SLACK_BOT_USER_ID` | transport | — | Bot's user id for self-echo suppression. |
| `ROUSSEAU_DISCORD_TOKEN` | transport | — | Discord bot token. |
| `ROUSSEAU_SMS_PROVIDER` | transport | — | `twilio` or `vonage`. |
| `ROUSSEAU_SMS_FROM` | transport | — | Sender number. |
| `ROUSSEAU_SMS_ACCOUNT_SID` | transport | — | Twilio account SID. |
| `ROUSSEAU_SMS_AUTH_TOKEN` | transport | — | Twilio/Vonage secret. |
| `ROUSSEAU_SMS_API_KEY` | transport | — | Vonage API key. |
| `ROUSSEAU_SMS_BASE_URL` | transport | — | Override for regional endpoints or tests. |
| `ROUSSEAU_IMESSAGE_BASE_URL` | transport | — | BlueBubbles server URL. |
| `ROUSSEAU_IMESSAGE_PASSWORD` | transport | — | BlueBubbles password. |
| `ROUSSEAU_IMESSAGE_CHAT_GUID` | transport | — | Outbound target. |
| `ROUSSEAU_IMESSAGE_POLL_INTERVAL` | transport | `2s` | Duration string. |
| `ROUSSEAU_EMAIL_IMAP_ADDR` | transport | — | IMAP server. |
| `ROUSSEAU_EMAIL_IMAP_USERNAME` | transport | — | IMAP user. |
| `ROUSSEAU_EMAIL_IMAP_PASSWORD` | transport | — | IMAP password. |
| `ROUSSEAU_EMAIL_MAILBOX` | transport | — | Folder to watch. |
| `ROUSSEAU_EMAIL_POLL_INTERVAL` | transport | — | Duration string. |
| `ROUSSEAU_EMAIL_SMTP_ADDR` | transport | — | SMTP submission host. |
| `ROUSSEAU_EMAIL_SMTP_USERNAME` | transport | — | SMTP user. |
| `ROUSSEAU_EMAIL_SMTP_PASSWORD` | transport | — | SMTP password. |
| `ROUSSEAU_EMAIL_FROM` | transport | — | From address. |

Les **tableaux allowlist** (`ROUSSEAU_SLACK_ALLOWLIST`, `ROUSSEAU_DISCORD_ALLOWLIST`, `ROUSSEAU_TELEGRAM_ALLOWLIST`, …) sont supportés par Viper, mais le parsing de chaînes env séparées par virgule est capricieux — préférez les définir dans `config.yaml`.

## Variables env explicites (hors préfixe ROUSSEAU_)

| Variable | Source | Objectif |
|---|---|---|
| `ANTHROPIC_API_KEY` | `config.Load` (`internal/config/config.go` ligne 275) | Remplit `anthropic.api_key`. Convention standard du SDK Anthropic. |
| `HOME` | `internal/cli/init.go` | Utilisé par `rousseau init` pour calculer le chemin d'état par défaut. |

## Variables détenues par les SDK que rousseau ne touche pas

Certaines bibliothèques de fournisseur récupèrent leur propre environnement. Rousseau ne les lit pas lui-même, mais elles influencent le comportement quand le fournisseur correspondant est sélectionné :

| Variable | Consommateur | Notes |
|---|---|---|
| `AWS_PROFILE`, `AWS_REGION`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`, `AWS_WEB_IDENTITY_TOKEN_FILE` | `aws-sdk-go-v2` (Bedrock) | La chaîne d'identifiants standard. Préférez IRSA ou les creds basés sur profil aux clés statiques. |
| `GOOGLE_APPLICATION_CREDENTIALS` | Bibliothèques d'auth Google (Vertex) | Chemin vers un JSON de service-account. Supplantée par `vertex.credentials_file` dans `config.yaml` si défini. |
| `OPENAI_API_KEY` | Les clients Go OpenAI amont la lisent typiquement | Rousseau câble explicitement la clé via `openai.api_key` ; rien d'implicite. |
| `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY` | Go net/http | Variables de proxy Go universelles. Utiles pour les chemins d'egress d'entreprise. |

## Variables de chemins XDG

Rousseau suit la spécification XDG Base Directory pour l'état et la config, avec deux replis :

| Variable | Effet |
|---|---|
| `XDG_CONFIG_HOME` | `$XDG_CONFIG_HOME/rousseau/config.yaml` est le chemin de config par défaut (référencé dans `internal/cli/root.go`). |
| `XDG_DATA_HOME` | Chemin d'état par défaut `$XDG_DATA_HOME/rousseau/sessions.db` (référencé par `whatsapp.go`, `skills.go`, `init.go`). |
| `HOME` | Repli quand les variables XDG ne sont pas définies ; rousseau utilise `os.UserHomeDir()` dans `internal/config/config.go`. |

L'unité Quadlet conteneur `docker/rousseau-agent.container` définit à la fois `HOME=/home/rousseau` et `XDG_DATA_HOME=/home/rousseau/.local/share`.

## Hygiène des secrets

Stockez les secrets à l'un de ces trois endroits :

1. **Un `EnvironmentFile=` d'unité systemd** — `chmod 0600`, appartenant à root ou à l'utilisateur selon les cas. Référencé depuis l'unité Quadlet — voir le [tutoriel de déploiement sur VPS](/fr/tutorials/deploy-to-a-vps/).
2. **Un fichier `.env` chargé par votre shell.** Pour usage desktop uniquement ; gardez-le hors contrôle de source.
3. **Un gestionnaire de secrets.** AWS Secrets Manager, HashiCorp Vault, ou `pass`/`gopass`. Pipez la valeur dans le processus au démarrage.

Ne commitez jamais de secrets dans `config.yaml`. `config.yaml` est le bon endroit pour les allowlists, les URL de base et la configuration non secrète ; c'est le mauvais endroit pour les clés API et les jetons de bot.

## Dépannage

### `ROUSSEAU_...` défini mais rousseau utilise toujours le défaut

Les variables d'environnement sont lues au démarrage. Redémarrez le démon après export. Vérifiez également la règle de transformation : les points dans la clé de config deviennent des underscores, et le préfixe est `ROUSSEAU_` (majuscules, exact).

### `ANTHROPIC_API_KEY` apparemment ignorée

La variable d'environnement n'est consultée que quand `provider: anthropic` est actif. Sous `provider: claudecli`, la CLI `claude` lit ses propres identifiants.

### Valeur différente sur différents hôtes

La précédence est **flag &gt; env &gt; fichier &gt; défaut**. Si un flag est défini (depuis le `ExecStart` de l'unité systemd par exemple), il l'emporte sur env et fichier.

### `GOOGLE_APPLICATION_CREDENTIALS` illisible dans le conteneur

Assurez-vous que le fichier est monté en lecture seule dans le conteneur et que l'UID du conteneur (1000 par défaut) peut le lire.

## Pages associées

- [Configuration](/fr/configuration/) — chaque champ de config avec défaut.
- [Référence : schéma de config](/fr/reference/config-schema/) — la structure YAML.
- [Référence : commandes CLI](/fr/reference/cli-commands/) — flags par transport.
- [Guides : Enterprise Onboarding](/fr/guides/enterprise-onboarding/) — gestion des secrets en production.
- [Deployment](/fr/deployment/) — options de gestion des secrets.

## Pour aller plus loin

- `internal/config/config.go` — `Load` définit le préfixe env et le remplaceur point-underscore.
- `internal/cli/root.go` — où `Load` est appelé.
