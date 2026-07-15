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
changefreq: "monthly"
description: "Every environment variable rousseau-agent reads: the ROUSSEAU_ prefix from Viper, ANTHROPIC_API_KEY, XDG paths, provider SDK variables."
keywords: "environment variables, ROUSSEAU_, ANTHROPIC_API_KEY, viper, XDG"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/reference/environment-variables/"
subtitle: "Every environment variable rousseau reads, at what layer, with what default."
tags: "reference, environment, viper, secrets"
title: "Referenz: Umgebungsvariablen"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "environment variables, ROUSSEAU_, ANTHROPIC_API_KEY, viper, XDG"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Referenz: Umgebungsvariablen"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 51
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/environment-variables/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/environment-variables/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Referenz: Umgebungsvariablen"
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
twitter_title: "Referenz: Umgebungsvariablen"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Danke an jeden Operator, der seinen eigenen Coding-Agenten betreibt."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Wie rousseau die Umgebung liest

Zwei Mechanismen, in dieser Reihenfolge (siehe `config.Load` in `internal/config/config.go`):

1. **Vipers automatische Env-Bindung.** `SetEnvPrefix("ROUSSEAU")` plus `SetEnvKeyReplacer(".", "_")` bedeutet, dass jedes Konfigurationsfeld als `ROUSSEAU_<UPPER_SNAKE>` erreichbar ist. So wird `provider` zu `ROUSSEAU_PROVIDER`, `agent.approver.mode` wird zu `ROUSSEAU_AGENT_APPROVER_MODE`.
2. **Explizite Überschreibung.** `ANTHROPIC_API_KEY` wird direkt aus der Umgebung gelesen und in `anthropic.api_key` gezwungen, sodass die Standard-Anthropic-SDK-Konvention einfach funktioniert. Keine anderen Schlüssel werden implizit aufgenommen.

Alles andere auf dieser Seite ist entweder eine Viper-gemappte Variable, eine SDK-verwaltete Variable, die rousseau nicht berührt, die zugrunde liegende Bibliothek aber schon, oder ein XDG-Pfad, der zur Berechnung der Defaults verwendet wird.

Die Vorrangordnung bleibt: **Flag > Env > Datei > Default**.

## `ROUSSEAU_*`-Präfix

Jeder `mapstructure`-Tag in `internal/config/config.go` ist über `ROUSSEAU_<UPPER_SNAKE_PATH>` erreichbar. Ausgewählte Beispiele — die vollständige Liste folgt der Config-Struct:

| Variable | Kategorie | Default | Beschreibung |
|---|---|---|---|
| `ROUSSEAU_PROVIDER` | core | `claudecli` | Provider-Bezeichner: `claudecli`, `anthropic`, `openai`, `openrouter`, `ollama`, `bedrock`, `vertex`. |
| `ROUSSEAU_LOG_LEVEL` | logging | `info` | slog-Level: `debug`, `info`, `warn`, `error`. |
| `ROUSSEAU_LOG_FORMAT` | logging | `text` | `text` oder `json`. |
| `ROUSSEAU_STATE_PATH` | state | `$HOME/.local/share/rousseau/sessions.db` | Session-Store-DSN. |
| `ROUSSEAU_AGENT_MAX_ITERATIONS` | agent | `32` | Tool-Use-Iterationslimit pro Turn. |
| `ROUSSEAU_AGENT_APPROVER_MODE` | agent | `` | `allow_all`, `deny_all`, `pattern`. |
| `ROUSSEAU_AGENT_APPROVER_DEFAULT` | agent | `` | Für `pattern`: `allow` oder `deny` bei nicht getroffenen Aufrufen. |
| `ROUSSEAU_AGENT_COMPRESSION_ENABLED` | agent | `false` | Den LLM-Compressor einschalten. |
| `ROUSSEAU_AGENT_COMPRESSION_TRIGGER_MESSAGES` | agent | `60` | Komprimieren, sobald die Nachrichtenzahl dies übersteigt. |
| `ROUSSEAU_AGENT_COMPRESSION_KEEP_RECENT` | agent | `8` | Wie viele aktuelle Nachrichten wörtlich bewahren. |
| `ROUSSEAU_AGENT_SKILLS_DIR` | agent | `$HOME/.local/share/rousseau/skills` | Skills-Verzeichnis. |
| `ROUSSEAU_ANTHROPIC_API_KEY` | provider | — | Dasselbe wie `ANTHROPIC_API_KEY`. |
| `ROUSSEAU_ANTHROPIC_MODEL` | provider | `claude-sonnet-4-6` | Anthropic-Modell-ID. |
| `ROUSSEAU_ANTHROPIC_MAX_TOKENS` | provider | `4096` | Max Antwort-Tokens. |
| `ROUSSEAU_CLAUDECLI_BINARY` | provider | `claude` | Executable-Name für den `claudecli`-Provider. |
| `ROUSSEAU_CLAUDECLI_MODEL` | provider | — | An `claude --model` übergeben. |
| `ROUSSEAU_CLAUDECLI_PERMISSION_MODE` | provider | — | `default`, `acceptEdits`, `bypassPermissions`, `plan` etc. |
| `ROUSSEAU_OPENAI_API_KEY` | provider | — | Bearer für OpenAI-kompatible Endpunkte. |
| `ROUSSEAU_OPENAI_MODEL` | provider | — | Modell-ID. |
| `ROUSSEAU_OPENAI_BASE_URL` | provider | — | Endpunkt überschreiben. |
| `ROUSSEAU_OPENROUTER_API_KEY` | provider | — | Bearer für OpenRouter. |
| `ROUSSEAU_OPENROUTER_MODEL` | provider | — | Modell-Slug. |
| `ROUSSEAU_OPENROUTER_BASE_URL` | provider | `https://openrouter.ai/api/v1` | Endpunkt überschreiben. |
| `ROUSSEAU_OLLAMA_MODEL` | provider | — | Modell-Tag. |
| `ROUSSEAU_OLLAMA_BASE_URL` | provider | `http://localhost:11434/v1` | Lokaler Ollama-Endpunkt. |
| `ROUSSEAU_BEDROCK_REGION` | provider | — | AWS-Region. |
| `ROUSSEAU_BEDROCK_MODEL` | provider | — | Bedrock-Modell-ID. |
| `ROUSSEAU_BEDROCK_PROFILE` | provider | — | AWS-benanntes Profil. |
| `ROUSSEAU_VERTEX_PROJECT` | provider | — | GCP-Projekt. |
| `ROUSSEAU_VERTEX_REGION` | provider | — | Vertex-Region. |
| `ROUSSEAU_VERTEX_MODEL` | provider | — | Anthropic-auf-Vertex-Modell. |
| `ROUSSEAU_VERTEX_CREDENTIALS_FILE` | provider | — | Pfad zur Service-Account-JSON. |
| `ROUSSEAU_WHATSAPP_REPLY_HEADER` | transport | `💎 *Rousseau Agent*\n\n` | Vor jeder WhatsApp-Outbound-Nachricht vorangestellt. |
| `ROUSSEAU_WHATSAPP_VOICE_ENABLED` | transport | `false` | whisper-Transkription von Sprachnotizen aktivieren. |
| `ROUSSEAU_WHATSAPP_VOICE_BINARY` | transport | `whisper` | whisper.cpp-Executable. |
| `ROUSSEAU_WHATSAPP_VOICE_MODEL` | transport | — | whisper-Modellname (`base.en`, `small`). |
| `ROUSSEAU_WHATSAPP_VOICE_MODEL_PATH` | transport | — | Expliziter .bin-Pfad (hat Vorrang vor Modell). |
| `ROUSSEAU_WHATSAPP_VOICE_LANGUAGE` | transport | — | ISO-Code; leer erkennt automatisch. |
| `ROUSSEAU_SIGNAL_BINARY` | transport | `signal-cli` | signal-cli-Executable. |
| `ROUSSEAU_SIGNAL_ACCOUNT` | transport | — | E.164-Telefonnummer. |
| `ROUSSEAU_SIGNAL_REPLY_HEADER` | transport | — | Reply-Header. |
| `ROUSSEAU_TELEGRAM_TOKEN` | transport | — | Bot-API-Token. |
| `ROUSSEAU_TELEGRAM_BASE_URL` | transport | — | Bot-API-Endpunkt überschreiben. |
| `ROUSSEAU_MATRIX_HOMESERVER_URL` | transport | — | Homeserver-Basis-URL. |
| `ROUSSEAU_MATRIX_ACCESS_TOKEN` | transport | — | Matrix-Access-Token. |
| `ROUSSEAU_MATRIX_USER_ID` | transport | — | Vollständige MXID (`@bot:example.org`). |
| `ROUSSEAU_SLACK_APP_TOKEN` | transport | — | `xapp-…`-App-Level-Token. |
| `ROUSSEAU_SLACK_BOT_TOKEN` | transport | — | `xoxb-…`-Bot-Token. |
| `ROUSSEAU_SLACK_BOT_USER_ID` | transport | — | Nutzer-ID des Bots für Self-Echo-Unterdrückung. |
| `ROUSSEAU_DISCORD_TOKEN` | transport | — | Discord-Bot-Token. |
| `ROUSSEAU_SMS_PROVIDER` | transport | — | `twilio` oder `vonage`. |
| `ROUSSEAU_SMS_FROM` | transport | — | Absendernummer. |
| `ROUSSEAU_SMS_ACCOUNT_SID` | transport | — | Twilio-Account-SID. |
| `ROUSSEAU_SMS_AUTH_TOKEN` | transport | — | Twilio/Vonage-Secret. |
| `ROUSSEAU_SMS_API_KEY` | transport | — | Vonage-API-Schlüssel. |
| `ROUSSEAU_SMS_BASE_URL` | transport | — | Überschreiben für Regional-Endpunkte oder Tests. |
| `ROUSSEAU_IMESSAGE_BASE_URL` | transport | — | BlueBubbles-Server-URL. |
| `ROUSSEAU_IMESSAGE_PASSWORD` | transport | — | BlueBubbles-Passwort. |
| `ROUSSEAU_IMESSAGE_CHAT_GUID` | transport | — | Outbound-Ziel. |
| `ROUSSEAU_IMESSAGE_POLL_INTERVAL` | transport | `2s` | Duration-String. |
| `ROUSSEAU_EMAIL_IMAP_ADDR` | transport | — | IMAP-Server. |
| `ROUSSEAU_EMAIL_IMAP_USERNAME` | transport | — | IMAP-Nutzer. |
| `ROUSSEAU_EMAIL_IMAP_PASSWORD` | transport | — | IMAP-Passwort. |
| `ROUSSEAU_EMAIL_MAILBOX` | transport | — | Zu beobachtender Ordner. |
| `ROUSSEAU_EMAIL_POLL_INTERVAL` | transport | — | Duration-String. |
| `ROUSSEAU_EMAIL_SMTP_ADDR` | transport | — | SMTP-Submission-Host. |
| `ROUSSEAU_EMAIL_SMTP_USERNAME` | transport | — | SMTP-Nutzer. |
| `ROUSSEAU_EMAIL_SMTP_PASSWORD` | transport | — | SMTP-Passwort. |
| `ROUSSEAU_EMAIL_FROM` | transport | — | Absenderadresse. |

**Allowlist-Arrays** (`ROUSSEAU_SLACK_ALLOWLIST`, `ROUSSEAU_DISCORD_ALLOWLIST`, `ROUSSEAU_TELEGRAM_ALLOWLIST`, …) werden von Viper unterstützt, aber das kommagetrennte Env-String-Parsing ist knifflig — bevorzugen Sie, diese in `config.yaml` zu setzen.

## Explizite Env-Vars (außerhalb des ROUSSEAU_-Präfixes)

| Variable | Quelle | Zweck |
|---|---|---|
| `ANTHROPIC_API_KEY` | `config.Load` (`internal/config/config.go` Zeile 275) | Befüllt `anthropic.api_key`. Standard-Anthropic-SDK-Konvention. |
| `HOME` | `internal/cli/init.go` | Wird von `rousseau init` verwendet, um den Standard-State-Pfad zu berechnen. |

## SDK-eigene Variablen, die rousseau nicht berührt

Einige Provider-Bibliotheken nehmen ihre eigene Umgebung auf. Rousseau liest diese nicht selbst, aber sie beeinflussen das Verhalten, wenn der entsprechende Provider ausgewählt ist:

| Variable | Konsument | Anmerkungen |
|---|---|---|
| `AWS_PROFILE`, `AWS_REGION`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`, `AWS_WEB_IDENTITY_TOKEN_FILE` | `aws-sdk-go-v2` (Bedrock) | Die Standard-Credential-Chain. Bevorzugen Sie IRSA oder profilbasierte Credentials gegenüber statischen Schlüsseln. |
| `GOOGLE_APPLICATION_CREDENTIALS` | Google-Auth-Bibliotheken (Vertex) | Pfad zu einer Service-Account-JSON. Wird durch `vertex.credentials_file` in `config.yaml` überschrieben, falls gesetzt. |
| `OPENAI_API_KEY` | Die Upstream-Go-OpenAI-Clients lesen dies typischerweise | Rousseau verdrahtet den Schlüssel explizit über `openai.api_key`; nichts Implizites. |
| `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY` | Go net/http | Universelle Go-Proxy-Variablen. Nützlich für unternehmensweite Egress-Pfade. |

## XDG-Pfad-Variablen

Rousseau folgt der XDG-Base-Directory-Spezifikation für State und Config, mit zwei Fallbacks:

| Variable | Wirkung |
|---|---|
| `XDG_CONFIG_HOME` | `$XDG_CONFIG_HOME/rousseau/config.yaml` ist der Standard-Konfigurationspfad (referenziert in `internal/cli/root.go`). |
| `XDG_DATA_HOME` | Standard-State-Pfad `$XDG_DATA_HOME/rousseau/sessions.db` (referenziert von `whatsapp.go`, `skills.go`, `init.go`). |
| `HOME` | Fallback, wenn die XDG-Variablen unset sind; rousseau verwendet `os.UserHomeDir()` in `internal/config/config.go`. |

Die Container-Quadlet-Unit unter `docker/rousseau-agent.container` setzt sowohl `HOME=/home/rousseau` als auch `XDG_DATA_HOME=/home/rousseau/.local/share`.

## Secret-Hygiene

Speichern Sie Secrets an einem von drei Orten:

1. **Ein systemd-Unit-`EnvironmentFile=`** — `chmod 0600`, root- oder nutzerseitig, je nach Angemessenheit. Von der Quadlet-Unit referenziert — siehe das [VPS-Bereitstellungs-Tutorial](/de/tutorials/deploy-to-a-vps/).
2. **Eine von Ihrer Shell geladene `.env`-Datei.** Nur für Desktop-Nutzung; halten Sie sie aus der Versionskontrolle heraus.
3. **Ein Secret-Manager.** AWS Secrets Manager, HashiCorp Vault oder `pass`/`gopass`. Leiten Sie den Wert beim Start in den Prozess.

Committen Sie Secrets niemals in `config.yaml`. `config.yaml` ist der richtige Ort für Allowlists, Base-URLs und nicht-geheime Konfiguration; es ist der falsche Ort für API-Schlüssel und Bot-Tokens.

## Fehlerbehebung

### `ROUSSEAU_...` gesetzt, aber rousseau verwendet weiterhin den Default

Env-Vars werden beim Start gelesen. Starten Sie den Daemon nach dem Export neu. Verifizieren Sie auch die Transformationsregel: Punkte im Config-Schlüssel werden zu Unterstrichen, und das Präfix ist `ROUSSEAU_` (Großbuchstaben, exakt).

### `ANTHROPIC_API_KEY` scheinbar ignoriert

Die Env-Var wird nur konsultiert, wenn `provider: anthropic` aktiv ist. Unter `provider: claudecli` liest die `claude`-CLI ihre eigenen Credentials.

### Unterschiedliche Werte auf unterschiedlichen Hosts

Die Vorrangordnung ist **Flag &gt; Env &gt; Datei &gt; Default**. Wenn ein Flag gesetzt ist (z. B. vom `ExecStart` der systemd-Unit), gewinnt es sowohl gegen Env als auch Datei.

### `GOOGLE_APPLICATION_CREDENTIALS` innerhalb des Containers nicht lesbar

Stellen Sie sicher, dass die Datei read-only in den Container bind-gemountet ist und die Container-UID (1000 per Default) sie lesen kann.

## Verwandte Seiten

- [Konfiguration](/de/configuration/) — jedes Konfigurationsfeld mit Default.
- [Referenz: Konfigurationsschema](/de/reference/config-schema/) — die YAML-Struktur.
- [Referenz: CLI-Befehle](/de/reference/cli-commands/) — Per-Transport-Flags.
- [Leitfäden: Enterprise-Onboarding](/de/guides/enterprise-onboarding/) — Secret-Handling in Produktion.
- [Bereitstellung](/de/deployment/) — Optionen zum Secret-Management.

## Weiterführende Lektüre

- `internal/config/config.go` — `Load` setzt das Env-Präfix und den Punkt-Unterstrich-Schlüssel-Ersetzer.
- `internal/cli/root.go` — wo `Load` aufgerufen wird.
