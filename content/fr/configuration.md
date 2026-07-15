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
description: "Complete configuration reference for rousseau-agent. Every provider, transport, and agent knob with type, default, and effect."
keywords: "configuration, config.yaml, viper, precedence, YAML, provider, transport, approver, compression"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/configuration/"
subtitle: "Chaque champ de internal/config/config.go."
tags: "configuration, reference"
title: "Référence de configuration"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "configuration, config.yaml, viper, precedence, YAML, provider, transport, approver, compression"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Référence de configuration"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 4
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/configuration/index.html"
item_link: "https://docs.rousseau-agent.dev/configuration/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Référence de configuration"
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
twitter_description: "Complete configuration reference for rousseau-agent. Every provider, transport, and agent knob with type, default, and effect."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Référence de configuration"
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

## Précédence

`rousseau` résout la configuration dans l'ordre **flag > env > fichier > défaut**. Le fichier réside par défaut à `~/.config/rousseau/config.yaml` ; surchargez-le avec `--config`.

Les variables d'environnement utilisent le préfixe `ROUSSEAU_` avec les `.` remplacés par `_` — ainsi `provider` devient `ROUSSEAU_PROVIDER`, `anthropic.api_key` devient `ROUSSEAU_ANTHROPIC_API_KEY`. `ANTHROPIC_API_KEY` est également reconnu directement (lié à `anthropic.api_key` au chargement).

## Racine

| Champ | Type | Défaut | Effet |
|---|---|---|---|
| `provider` | string | `claudecli` | Backend LLM : `claudecli`, `anthropic`, `bedrock`, `vertex`, `openai`, `openrouter`, `ollama`. |

## `anthropic` — API Anthropic directe

| Champ | Type | Défaut | Effet |
|---|---|---|---|
| `api_key` | string | *depuis `ANTHROPIC_API_KEY`* | Bearer pour `api.anthropic.com`. Rejeté si vide lorsque le fournisseur est sélectionné. |
| `model` | string | `claude-sonnet-4-6` | Identifiant du modèle transmis au SDK. |
| `max_tokens` | int64 | `4096` | Limite les tokens de sortie par complétion. |

Voir [/providers/anthropic/](/fr/providers/anthropic/).

## `bedrock` — AWS Bedrock

| Champ | Type | Défaut | Effet |
|---|---|---|---|
| `region` | string | *requis* | Région AWS (`us-east-1`, `eu-west-2`). |
| `model` | string | *requis* | ID de modèle Bedrock (`anthropic.claude-sonnet-4-6-20260101-v1:0`). |
| `profile` | string | *vide* | Profil de credentials depuis `~/.aws/credentials`. Vide, utilise la chaîne d'authentification AWS standard. |
| `max_tokens` | int64 | défaut SDK | Limite les tokens de sortie. |

Voir [/providers/bedrock/](/fr/providers/bedrock/).

## `vertex` — Google Vertex AI

| Champ | Type | Défaut | Effet |
|---|---|---|---|
| `project` | string | *requis* | ID du projet GCP. |
| `region` | string | *requis* | Région Vertex (`us-central1`). |
| `model` | string | *requis* | ID de modèle Anthropic-on-Vertex (`claude-sonnet-4-6@20260101`). |
| `credentials_file` | string | *vide* | Chemin vers le JSON de compte de service ou d'utilisateur autorisé. Vide, utilise Application Default Credentials. |
| `max_tokens` | int64 | `4096` | Limite les tokens de sortie. |

Voir [/providers/vertex/](/fr/providers/vertex/).

## `claudecli` — sous-processus vers la CLI `claude` locale

| Champ | Type | Défaut | Effet |
|---|---|---|---|
| `binary` | string | `claude` | Exécutable, résolu via `$PATH`. |
| `model` | string | *vide* | Transmis à `--model`. Vide, utilise le défaut de claude. |
| `permission_mode` | string | *vide* | Transmis à `--permission-mode`. Valeurs : `acceptEdits`, `auto`, `bypassPermissions`, `default`, `dontAsk`, `plan`. Les daemons non supervisés requièrent généralement `bypassPermissions`. |
| `extra_args` | []string | `[]` | Ajouté avant `-p` à chaque invocation. Utile pour `--add-dir`, `--allowed-tools`, `--disallowed-tools`, `--plugin-dir`. |

Voir [/providers/claudecli/](/fr/providers/claudecli/).

## `openai` / `openrouter` / `ollama` — endpoints compatibles OpenAI

Forme partagée. `openrouter.base_url` vaut par défaut `https://openrouter.ai/api/v1` ; `ollama.base_url` vaut par défaut `http://localhost:11434/v1` ; `ollama.api_key` vaut par défaut `not-required`.

| Champ | Type | Défaut | Effet |
|---|---|---|---|
| `api_key` | string | *requis* | Bearer token. Non vide, même pour Ollama (n'importe quelle valeur convient). |
| `model` | string | *requis* | Identifiant du modèle. Aucun défaut universel selon les endpoints. |
| `base_url` | string | *défaut fournisseur* | URL complète de l'endpoint. |
| `max_tokens` | int64 | défaut SDK | Limite les tokens de sortie. |

Voir [/providers/openai-compatible/](/fr/providers/openai-compatible/).

## `log`

| Champ | Type | Défaut | Effet |
|---|---|---|---|
| `level` | string | `info` | `debug`, `info`, `warn`, `error`. |
| `format` | string | `text` | `text` (humain) ou `json` (production / agrégation de logs). |

## `state`

| Champ | Type | Défaut | Effet |
|---|---|---|---|
| `path` | string | `~/.local/share/rousseau/sessions.db` | Chemin de la base SQLite (mode WAL, `busy_timeout=15s`). |

## `agent`

| Champ | Type | Défaut | Effet |
|---|---|---|---|
| `system_prompt` | string | *vide* | Surcharge le défaut intégré. |
| `max_iterations` | int | `32` | Plafonne les allers-retours du modèle par `Turn`. |
| `skills_dir` | string | *vide* | Répertoire de fichiers `*.md` de skills. Vide, désactive les skills. |

### `agent.compression`

| Champ | Type | Défaut | Effet |
|---|---|---|---|
| `enabled` | bool | `false` | Active la compression de session par LLM. |
| `trigger_messages` | int | `60` | Nombre de messages au-delà duquel la compression se déclenche. |
| `keep_recent` | int | `8` | Messages récents conservés tels quels. |
| `prompt` | string | *intégré* | Surcharge l'instruction de synthèse par défaut. |

### `agent.approver`

| Champ | Type | Défaut | Effet |
|---|---|---|---|
| `mode` | string | `allow_all` | `allow_all`, `deny_all` ou `pattern`. |
| `reason` | string | *vide* | Motif de refus renvoyé au modèle. |
| `default` | string | `deny` | Repli lorsqu'aucune règle `allow` ou `deny` ne correspond (mode pattern). |
| `allow` | []PatternEntry | `[]` | Règles regex d'autorisation par outil. |
| `deny` | []PatternEntry | `[]` | Règles regex de refus par outil. Le refus l'emporte sur l'autorisation. |

Chaque `PatternEntry` s'écrit `{tool: <nom>, match: <regex>}`. `tool: ""` correspond à tous les outils ; `match: ""` correspond à toutes les entrées.

## Blocs de transport

### `whatsapp`

| Champ | Type | Défaut | Effet |
|---|---|---|---|
| `reply_header` | string | `💎 *Rousseau Agent*\n\n` | Préfixe chaque message sortant. Mettre `" "` pour désactiver. |
| `voice.enabled` | bool | `false` | Transcription via Whisper des notes vocales entrantes. |
| `voice.binary` | string | `whisper` | Exécutable CLI Whisper. |
| `voice.model` | string | *vide* | Transmis à `--model` (`base.en`, `small`). |
| `voice.model_path` | string | *vide* | Chemin `.bin` explicite, prioritaire sur `model`. |
| `voice.language` | string | *vide* | Transmis à `--language`. Vide, détection automatique. |
| `voice.extra_args` | []string | `[]` | Ajouté à chaque invocation whisper. |

### `signal`

| Champ | Type | Défaut | Effet |
|---|---|---|---|
| `binary` | string | `signal-cli` | Exécutable à invoquer en mode daemon JSON-RPC. |
| `account` | string | *requis* | Numéro E.164 sous lequel le daemon opère. |
| `extra_args` | []string | `[]` | Inséré entre `-a <account>` et `jsonRpc`. |
| `reply_header` | string | *vide* | Préfixe chaque message sortant. |
| `allowlist` | []string | `[]` | Numéros E.164 dont les messages sont traités. Vide, tous les expéditeurs sont acceptés. |

### `telegram`

| Champ | Type | Défaut | Effet |
|---|---|---|---|
| `token` | string | *requis* | Jeton de bot issu de BotFather. |
| `base_url` | string | `https://api.telegram.org` | Surcharge pour un serveur Bot API local. |
| `reply_header` | string | *vide* | Préfixe chaque réponse sortante. |
| `allowlist` | []string | `[]` | IDs d'utilisateurs Telegram dont les messages sont traités. |

### `matrix`

| Champ | Type | Défaut | Effet |
|---|---|---|---|
| `homeserver_url` | string | *requis* | URL de base, ex. `https://matrix.org`. |
| `access_token` | string | *requis* | Jeton d'accès du bot. |
| `user_id` | string | *vide* | MXID complet du bot (`@bot:matrix.org`). Facultatif mais recommandé (suppression de l'écho des propres messages). |
| `reply_header` | string | *vide* | Préfixe chaque réponse sortante. |
| `allowlist` | []string | `[]` | IDs Matrix dont les messages sont traités. |

### `slack`

| Champ | Type | Défaut | Effet |
|---|---|---|---|
| `app_token` | string | *requis* | Jeton `xapp-*` de niveau app avec `connections:write`. |
| `bot_token` | string | *requis* | Jeton bot `xoxb-*` avec `chat:write`. |
| `bot_user_id` | string | *vide* | ID `U…` du bot pour éviter la boucle sur ses propres messages. |
| `reply_header` | string | *vide* | Préfixe chaque message sortant. |
| `allowlist` | []string | `[]` | IDs d'utilisateurs Slack dont les messages sont traités. |

### `discord`

| Champ | Type | Défaut | Effet |
|---|---|---|---|
| `token` | string | *requis* | Jeton de bot depuis le Developer Portal. |
| `reply_header` | string | *vide* | Préfixe chaque réponse sortante. |
| `allowlist` | []string | `[]` | IDs d'utilisateurs Discord dont les messages sont traités. |

### `sms`

| Champ | Type | Défaut | Effet |
|---|---|---|---|
| `provider` | string | *requis* | `twilio` ou `vonage`. |
| `from` | string | *requis* | Expéditeur E.164 ou Messaging Service SID Twilio. |
| `account_sid` | string | *requis pour twilio* | SID de compte Twilio (`AC…`). |
| `auth_token` | string | *requis* | Auth token Twilio ou API secret Vonage. |
| `api_key` | string | *requis pour vonage* | Clé API Vonage. |
| `base_url` | string | *défaut fournisseur* | Surcharge pour endpoints régionaux ou de test. |
| `reply_header` | string | *vide* | Préfixe chaque message sortant. |

### `imessage`

| Champ | Type | Défaut | Effet |
|---|---|---|---|
| `base_url` | string | *requis* | URL du serveur BlueBubbles (`http://localhost:1234`). |
| `password` | string | *requis* | Mot de passe du serveur BlueBubbles. |
| `chat_guid` | string | *vide* | GUID de cible sortante. |
| `poll_interval` | duration | `5s` | Cadence de sondage sur `/api/v1/message`. |
| `reply_header` | string | *vide* | Préfixe chaque message sortant. |

### `email`

| Champ | Type | Défaut | Effet |
|---|---|---|---|
| `imap_addr` | string | *requis* | `host:port` pour IMAP encapsulé en TLS (généralement `:993`). |
| `imap_username` | string | *requis* | Nom d'utilisateur IMAP. |
| `imap_password` | string | *requis* | Mot de passe IMAP. |
| `mailbox` | string | `INBOX` | Boîte à sonder. |
| `poll_interval` | duration | `30s` | Fréquence de recherche des mails UNSEEN. |
| `smtp_addr` | string | *requis* | `host:port` pour la soumission SMTP (généralement `:587`). |
| `smtp_username` | string | *requis* | Nom d'utilisateur SMTP. |
| `smtp_password` | string | *requis* | Mot de passe SMTP. |
| `from` | string | *requis* | Adresse `From` en enveloppe et en en-tête. |
| `reply_header` | string | *vide* | Préfixe le corps de chaque message sortant. |

## Exemple complet

```yaml
provider: claudecli

anthropic:
  api_key: sk-ant-...
  model: claude-sonnet-4-6
  max_tokens: 4096

bedrock:
  region: us-east-1
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
  profile: default

vertex:
  project: my-gcp-project
  region: us-central1
  model: claude-sonnet-4@20260101
  credentials_file: ~/.config/gcloud/vertex-key.json

claudecli:
  binary: claude
  model: sonnet
  permission_mode: bypassPermissions
  extra_args: []

log:
  level: info
  format: json

state:
  path: ~/.local/share/rousseau/sessions.db

agent:
  system_prompt: ""
  max_iterations: 32
  skills_dir: ~/.local/share/rousseau/skills
  compression:
    enabled: true
    trigger_messages: 60
    keep_recent: 8
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "^./workspace/.*"}
    deny:
      - {tool: bash, match: "rm -rf|sudo|:\\(\\)\\{ :\\|:& \\};:"}

whatsapp:
  reply_header: "💎 *Rousseau Agent*\n\n"
  voice:
    enabled: false

signal:
  account: "+447900123456"
  allowlist: ["+447900654321"]

telegram:
  token: "123:ABC"
  allowlist: ["12345678"]

matrix:
  homeserver_url: "https://matrix.org"
  access_token: "syt_..."
  user_id: "@bot:matrix.org"
  allowlist: ["@alice:matrix.org"]

slack:
  app_token: "xapp-..."
  bot_token: "xoxb-..."
  bot_user_id: "U0123ABCD"

discord:
  token: "bot-token"
  allowlist: ["123456789012345678"]

sms:
  provider: twilio
  from: "+15550000000"
  account_sid: "AC..."
  auth_token: "..."

imessage:
  base_url: "http://localhost:1234"
  password: "..."
  poll_interval: "5s"

email:
  imap_addr: "imap.example.com:993"
  imap_username: "bot@example.com"
  imap_password: "..."
  smtp_addr: "smtp.example.com:587"
  smtp_username: "bot@example.com"
  smtp_password: "..."
  from: "bot@example.com"
  poll_interval: "30s"
```

## Dépannage

### `config: unmarshal: 1 error(s) decoding: ...`

Le YAML est valide mais un champ a un type incorrect. Le message d'erreur nomme le champ — vérifiez son type dans `internal/config/config.go`.

### La surcharge par variable d'environnement n'est pas prise en compte

Rousseau préfixe les variables d'environnement par `ROUSSEAU_` et remplace les points par des underscores. `anthropic.model` devient `ROUSSEAU_ANTHROPIC_MODEL`. `ANTHROPIC_API_KEY` est un cas particulier câblé directement sur `anthropic.api_key`.

### `config: read: yaml: line X: found character that cannot start any token`

Indentation par tabulations. YAML exige des espaces.

### Les modifications de `config.yaml` ne prennent pas effet

Rousseau lit la configuration une seule fois au démarrage. Redémarrez le daemon.

### Deux valeurs de configuration semblent actives

L'ordre de précédence est **flag > env > fichier > défaut**. Activez `log.level: debug` et cherchez `config.loaded` pour visualiser la valeur résolue.

## Pages liées

- [Référence : Schéma de configuration](/fr/reference/config-schema/) — chaque champ.
- [Référence : Variables d'environnement](/fr/reference/environment-variables/) — matrice de surcharge.
- [Référence : Commandes CLI](/fr/reference/cli-commands/) — flags par transport.
- [Fournisseurs](/fr/providers/) — sections spécifiques aux fournisseurs.
- [Transports](/fr/transports/) — sections spécifiques aux transports.

## Pour aller plus loin

- `internal/config/config.go` — la structure de référence.
- `internal/cli/root.go` — où la configuration est chargée.
- `internal/config/config_test.go` — matrice de tests de la sémantique de chargement.
