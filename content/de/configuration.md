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
hreflang: "de"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "de"
locale: "de_DE"
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
permalink: "https://docs.rousseau-agent.dev/de/configuration/"
subtitle: "Jedes Feld in internal/config/config.go."
tags: "configuration, reference"
title: "Konfigurationsreferenz"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "configuration, config.yaml, viper, precedence, YAML, provider, transport, approver, compression"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Konfigurationsreferenz"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 4
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/configuration/index.html"
item_link: "https://docs.rousseau-agent.dev/configuration/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Konfigurationsreferenz"
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
twitter_title: "Konfigurationsreferenz"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Danke an jeden Operator, der seinen eigenen Coding-Agenten betreibt."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Rangfolge

`rousseau` löst die Konfiguration in der Reihenfolge **Flag > Env > Datei > Standard** auf. Die Datei liegt standardmässig unter `~/.config/rousseau/config.yaml`; überschreibbar mit `--config`.

Umgebungsvariablen verwenden das Präfix `ROUSSEAU_`, wobei `.` durch `_` ersetzt wird – aus `provider` wird also `ROUSSEAU_PROVIDER`, aus `anthropic.api_key` wird `ROUSSEAU_ANTHROPIC_API_KEY`. `ANTHROPIC_API_KEY` wird ebenfalls direkt berücksichtigt (es wird beim Laden an `anthropic.api_key` gebunden).

## Oberste Ebene

| Feld | Typ | Standard | Wirkung |
|---|---|---|---|
| `provider` | string | `claudecli` | LLM-Backend: `claudecli`, `anthropic`, `bedrock`, `vertex`, `openai`, `openrouter`, `ollama`. |

## `anthropic` – direkte Anthropic-API

| Feld | Typ | Standard | Wirkung |
|---|---|---|---|
| `api_key` | string | *aus `ANTHROPIC_API_KEY`* | Bearer-Token für `api.anthropic.com`. Wird abgelehnt, wenn bei ausgewähltem Provider leer. |
| `model` | string | `claude-sonnet-4-6` | Modell-ID, die an das SDK übergeben wird. |
| `max_tokens` | int64 | `4096` | Begrenzt Ausgabe-Tokens pro Completion. |

Siehe [/providers/anthropic/](/de/providers/anthropic/).

## `bedrock` – AWS Bedrock

| Feld | Typ | Standard | Wirkung |
|---|---|---|---|
| `region` | string | *erforderlich* | AWS-Region (`us-east-1`, `eu-west-2`). |
| `model` | string | *erforderlich* | Bedrock-Modell-ID (`anthropic.claude-sonnet-4-6-20260101-v1:0`). |
| `profile` | string | *leer* | Credentials-Profil aus `~/.aws/credentials`. Leer nutzt die Standard-AWS-Credential-Kette. |
| `max_tokens` | int64 | SDK-Standard | Begrenzt Ausgabe-Tokens. |

Siehe [/providers/bedrock/](/de/providers/bedrock/).

## `vertex` – Google Vertex AI

| Feld | Typ | Standard | Wirkung |
|---|---|---|---|
| `project` | string | *erforderlich* | GCP-Projekt-ID. |
| `region` | string | *erforderlich* | Vertex-Region (`us-central1`). |
| `model` | string | *erforderlich* | Anthropic-auf-Vertex-Modell-ID (`claude-sonnet-4-6@20260101`). |
| `credentials_file` | string | *leer* | Pfad zu einem Service-Account- oder Authorized-User-JSON. Leer nutzt Application Default Credentials. |
| `max_tokens` | int64 | `4096` | Begrenzt Ausgabe-Tokens. |

Siehe [/providers/vertex/](/de/providers/vertex/).

## `claudecli` – Subprozess gegen lokale `claude`-CLI

| Feld | Typ | Standard | Wirkung |
|---|---|---|---|
| `binary` | string | `claude` | Ausführbare Datei, aufgelöst über `$PATH`. |
| `model` | string | *leer* | An `--model` übergeben. Leer nutzt Claudes Standardmodell. |
| `permission_mode` | string | *leer* | An `--permission-mode` übergeben. Werte: `acceptEdits`, `auto`, `bypassPermissions`, `default`, `dontAsk`, `plan`. Unbeaufsichtigte Daemons benötigen typischerweise `bypassPermissions`. |
| `extra_args` | []string | `[]` | Vor `-p` bei jedem Aufruf vorangestellt. Nützlich für `--add-dir`, `--allowed-tools`, `--disallowed-tools`, `--plugin-dir`. |

Siehe [/providers/claudecli/](/de/providers/claudecli/).

## `openai` / `openrouter` / `ollama` – OpenAI-kompatible Endpunkte

Gemeinsame Struktur. `openrouter.base_url` hat den Standardwert `https://openrouter.ai/api/v1`; `ollama.base_url` hat den Standardwert `http://localhost:11434/v1`; `ollama.api_key` hat den Standardwert `not-required`.

| Feld | Typ | Standard | Wirkung |
|---|---|---|---|
| `api_key` | string | *erforderlich* | Bearer-Token. Auch für Ollama nicht leer (jeder Platzhalter funktioniert). |
| `model` | string | *erforderlich* | Modell-ID. Es gibt keinen universellen Standard über alle Endpunkte hinweg. |
| `base_url` | string | *Provider-Standard* | Vollständige Endpunkt-URL. |
| `max_tokens` | int64 | SDK-Standard | Begrenzt Ausgabe-Tokens. |

Siehe [/providers/openai-compatible/](/de/providers/openai-compatible/).

## `log`

| Feld | Typ | Standard | Wirkung |
|---|---|---|---|
| `level` | string | `info` | `debug`, `info`, `warn`, `error`. |
| `format` | string | `text` | `text` (menschenlesbar) oder `json` (Produktion / Log-Aggregation). |

## `state`

| Feld | Typ | Standard | Wirkung |
|---|---|---|---|
| `path` | string | `~/.local/share/rousseau/sessions.db` | Pfad zur SQLite-Datenbank (WAL-Modus, `busy_timeout=15s`). |

## `agent`

| Feld | Typ | Standard | Wirkung |
|---|---|---|---|
| `system_prompt` | string | *leer* | Überschreibt den eingebauten Standard. |
| `max_iterations` | int | `32` | Begrenzt Modell-Round-Trips pro `Turn`. |
| `skills_dir` | string | *leer* | Verzeichnis mit `*.md`-Skill-Dateien. Leer deaktiviert Skills. |

### `agent.compression`

| Feld | Typ | Standard | Wirkung |
|---|---|---|---|
| `enabled` | bool | `false` | Aktiviert LLM-basierte Sitzungskompression. |
| `trigger_messages` | int | `60` | Nachrichtenanzahl, ab der die Kompression ausgelöst wird. |
| `keep_recent` | int | `8` | Aktuelle Nachrichten, die wortgetreu erhalten bleiben. |
| `prompt` | string | *eingebaut* | Überschreibt die Standard-Zusammenfassungsanweisung. |

### `agent.approver`

| Feld | Typ | Standard | Wirkung |
|---|---|---|---|
| `mode` | string | `allow_all` | `allow_all`, `deny_all` oder `pattern`. |
| `reason` | string | *leer* | Ablehnungsgrund, der dem Modell übermittelt wird. |
| `default` | string | `deny` | Fallback, wenn keine `allow`- oder `deny`-Regel passt (Pattern-Modus). |
| `allow` | []PatternEntry | `[]` | Regex-Erlaubnisregeln pro Tool. |
| `deny` | []PatternEntry | `[]` | Regex-Verbotsregeln pro Tool. Verbot schlägt Erlaubnis. |

Jeder `PatternEntry` hat die Form `{tool: <name>, match: <regex>}`. `tool: ""` passt auf jedes Tool; `match: ""` passt auf jede Eingabe.

## Transport-Blöcke

### `whatsapp`

| Feld | Typ | Standard | Wirkung |
|---|---|---|---|
| `reply_header` | string | `💎 *Rousseau Agent*\n\n` | Wird jeder ausgehenden Nachricht vorangestellt. Zum Deaktivieren auf `" "` setzen. |
| `voice.enabled` | bool | `false` | Whisper-basierte Transkription für eingehende Sprachnachrichten. |
| `voice.binary` | string | `whisper` | Whisper-CLI-Executable. |
| `voice.model` | string | *leer* | An `--model` übergeben (`base.en`, `small`). |
| `voice.model_path` | string | *leer* | Expliziter `.bin`-Pfad, hat Vorrang vor `model`. |
| `voice.language` | string | *leer* | An `--language` übergeben. Leer erkennt automatisch. |
| `voice.extra_args` | []string | `[]` | Wird an jeden Whisper-Aufruf angehängt. |

### `signal`

| Feld | Typ | Standard | Wirkung |
|---|---|---|---|
| `binary` | string | `signal-cli` | Ausführbare Datei, aufgerufen im JSON-RPC-Daemon-Modus. |
| `account` | string | *erforderlich* | E.164-Telefonnummer, unter der der Daemon läuft. |
| `extra_args` | []string | `[]` | Zwischen `-a <account>` und `jsonRpc` eingefügt. |
| `reply_header` | string | *leer* | Wird jeder ausgehenden Nachricht vorangestellt. |
| `allowlist` | []string | `[]` | E.164-Nummern, deren Nachrichten verarbeitet werden. Leer akzeptiert jeden Absender. |

### `telegram`

| Feld | Typ | Standard | Wirkung |
|---|---|---|---|
| `token` | string | *erforderlich* | Bot-Token vom BotFather. |
| `base_url` | string | `https://api.telegram.org` | Override für einen lokalen Bot-API-Server. |
| `reply_header` | string | *leer* | Wird jeder ausgehenden Antwort vorangestellt. |
| `allowlist` | []string | `[]` | Telegram-Benutzer-IDs, deren Nachrichten verarbeitet werden. |

### `matrix`

| Feld | Typ | Standard | Wirkung |
|---|---|---|---|
| `homeserver_url` | string | *erforderlich* | Basis-URL, z.B. `https://matrix.org`. |
| `access_token` | string | *erforderlich* | Access-Token des Bot-Benutzers. |
| `user_id` | string | *leer* | Vollständige MXID des Bot-Benutzers (`@bot:matrix.org`). Optional, aber empfohlen (Unterdrückung von Eigen-Nachrichten-Echos). |
| `reply_header` | string | *leer* | Wird jeder ausgehenden Antwort vorangestellt. |
| `allowlist` | []string | `[]` | Matrix-IDs, deren Nachrichten verarbeitet werden. |

### `slack`

| Feld | Typ | Standard | Wirkung |
|---|---|---|---|
| `app_token` | string | *erforderlich* | `xapp-*`-App-Level-Token mit `connections:write`. |
| `bot_token` | string | *erforderlich* | `xoxb-*`-Bot-Token mit `chat:write`. |
| `bot_user_id` | string | *leer* | Eigene `U…`-ID des Bot-Benutzers zur Verhinderung von Eigen-Nachrichten-Schleifen. |
| `reply_header` | string | *leer* | Wird jeder ausgehenden Nachricht vorangestellt. |
| `allowlist` | []string | `[]` | Slack-Benutzer-IDs, deren Nachrichten verarbeitet werden. |

### `discord`

| Feld | Typ | Standard | Wirkung |
|---|---|---|---|
| `token` | string | *erforderlich* | Bot-Token aus dem Developer Portal. |
| `reply_header` | string | *leer* | Wird jeder ausgehenden Antwort vorangestellt. |
| `allowlist` | []string | `[]` | Discord-Benutzer-IDs, deren Nachrichten verarbeitet werden. |

### `sms`

| Feld | Typ | Standard | Wirkung |
|---|---|---|---|
| `provider` | string | *erforderlich* | `twilio` oder `vonage`. |
| `from` | string | *erforderlich* | E.164-Absender oder Twilio-Messaging-Service-SID. |
| `account_sid` | string | *erforderlich für twilio* | Twilio-Account-SID (`AC…`). |
| `auth_token` | string | *erforderlich* | Twilio-Auth-Token oder Vonage-API-Secret. |
| `api_key` | string | *erforderlich für vonage* | Vonage-API-Key. |
| `base_url` | string | *Provider-Standard* | Override für regionale oder Test-Endpunkte. |
| `reply_header` | string | *leer* | Wird jeder ausgehenden Nachricht vorangestellt. |

### `imessage`

| Feld | Typ | Standard | Wirkung |
|---|---|---|---|
| `base_url` | string | *erforderlich* | BlueBubbles-Server-URL (`http://localhost:1234`). |
| `password` | string | *erforderlich* | BlueBubbles-Server-Passwort. |
| `chat_guid` | string | *leer* | Ausgehende Ziel-GUID. |
| `poll_interval` | duration | `5s` | Poll-Frequenz gegen `/api/v1/message`. |
| `reply_header` | string | *leer* | Wird jeder ausgehenden Nachricht vorangestellt. |

### `email`

| Feld | Typ | Standard | Wirkung |
|---|---|---|---|
| `imap_addr` | string | *erforderlich* | `host:port` für TLS-umhülltes IMAP (typischerweise `:993`). |
| `imap_username` | string | *erforderlich* | IMAP-Benutzername. |
| `imap_password` | string | *erforderlich* | IMAP-Passwort. |
| `mailbox` | string | `INBOX` | Zu pollende Mailbox. |
| `poll_interval` | duration | `30s` | Wie oft nach UNSEEN-Mails gesucht wird. |
| `smtp_addr` | string | *erforderlich* | `host:port` für SMTP-Übermittlung (typischerweise `:587`). |
| `smtp_username` | string | *erforderlich* | SMTP-Benutzername. |
| `smtp_password` | string | *erforderlich* | SMTP-Passwort. |
| `from` | string | *erforderlich* | Envelope- und Header-Absenderadresse (`From`). |
| `reply_header` | string | *leer* | Wird dem Body jeder ausgehenden Nachricht vorangestellt. |

## Vollständiges Beispiel

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

## Fehlerbehebung

### `config: unmarshal: 1 error(s) decoding: ...`

Das YAML ist gültig, aber ein Feld hat den falschen Typ. Die Fehlermeldung nennt das Feld – prüfen Sie den Typ in `internal/config/config.go`.

### Env-Var-Override wird nicht übernommen

Rousseau setzt Env-Variablen das Präfix `ROUSSEAU_` voran und ersetzt Punkte durch Unterstriche. Aus `anthropic.model` wird `ROUSSEAU_ANTHROPIC_MODEL`. `ANTHROPIC_API_KEY` ist ein Sonderfall, der direkt an `anthropic.api_key` gebunden ist.

### `config: read: yaml: line X: found character that cannot start any token`

Tab-Einrückung. YAML erfordert Leerzeichen.

### Änderungen an `config.yaml` werden nicht wirksam

Rousseau liest die Konfiguration einmalig beim Start. Starten Sie den Daemon neu.

### Zwei Konfigurationswerte scheinen aktiv zu sein

Die Rangfolge ist **Flag > Env > Datei > Standard**. Aktivieren Sie `log.level: debug` und suchen Sie mit grep nach `config.loaded`, um den aufgelösten Wert zu sehen.

## Verwandte Seiten

- [Referenz: Config-Schema](/de/reference/config-schema/) – jedes Feld.
- [Referenz: Umgebungsvariablen](/de/reference/environment-variables/) – Override-Matrix.
- [Referenz: CLI-Befehle](/de/reference/cli-commands/) – Flags pro Transport.
- [Provider](/de/providers/) – Provider-spezifische Blöcke.
- [Transports](/de/transports/) – Transport-spezifische Blöcke.

## Weiterführende Lektüre

- `internal/config/config.go` – die massgebliche Struktur.
- `internal/cli/root.go` – wo die Konfiguration geladen wird.
- `internal/config/config_test.go` – die Test-Matrix der Lade-Semantik.
