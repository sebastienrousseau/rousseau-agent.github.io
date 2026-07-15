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
changefreq: "monthly"
description: "Set up rousseau-agent's Slack transport: Socket Mode (xapp-* app token + xoxb-* bot token), no public webhook, allowlist by user ID."
keywords: "Slack, Socket Mode, xapp, xoxb, chat.postMessage, connections:write, no webhook, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/transports/slack/"
subtitle: "Socket Mode with no public HTTP surface."
tags: "transports, Slack"
title: "Slack-Transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Slack, Socket Mode, xapp, xoxb, chat.postMessage, connections:write, no webhook, allowlist"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Slack-Transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 16
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/slack/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/slack/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Slack-Transport"
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
twitter_description: "Set up rousseau-agent's Slack transport: Socket Mode (xapp-* app token + xoxb-* bot token), no public webhook, allowlist by user ID."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Slack-Transport"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Was Sie lernen</span><p>Den vollständigen Wizard-Durchlauf auf app.slack.com, welche OAuth-Scopes exakt zu vergeben sind, welche Event-Subscriptions zu konfigurieren sind, wie Socket Mode einen öffentlichen Webhook überflüssig macht und wie die Schleifen-Verhinderung eigener Nachrichten in rousseau funktioniert. Lesen Sie <code>internal/transport/slack/client.go</code> parallel zu dieser Seite.</p></aside>

## Überblick

Der Slack-Transport (`internal/transport/slack/`) nutzt **Socket Mode** – einen ausgehenden WebSocket zu Slack – weshalb der Daemon keine öffentliche HTTP-Oberfläche benötigt. Eingehende Ereignisse laufen über den Socket; ausgehende Aufrufe gehen an die Standard-Web-API (`chat.postMessage`).

<aside class="admonition" data-type="tip"><span class="admonition-title">Warum Socket Mode</span><p>Die Alternative (Events-API + Request-URL) erfordert einen öffentlichen HTTPS-Endpunkt mit SSL-Zertifikat. Rousseau exponiert konzeptionell keine eingehende HTTP-Oberfläche, weshalb Socket Mode der einzige unterstützte Ingress-Pfad ist.</p></aside>

## Zwei Tokens

Slack Socket Mode benötigt zwei Tokens mit getrennten Zuständigkeiten:

| Token | Präfix | Scope | Zweck |
|---|---|---|---|
| App-Level-Token | `xapp-` | `connections:write` | Öffnet den Socket-Mode-WebSocket. |
| Bot-Token | `xoxb-` | `chat:write` + Event-Subscriptions | Sendet Nachrichten, abonniert Ereignisse. |

## App-Einrichtung

Vollständiges Schritt-für-Schritt unter https://app.slack.com/apps :

1. **Neue App erstellen** ("From scratch"). Workspace wählen.
2. **Socket Mode aktivieren** (Settings → Socket Mode). Ein **App-Level-Token** mit `connections:write` generieren. Dies ist der `xapp-*`-Token.
3. **Event-Subscriptions konfigurieren** (Features → Event Subscriptions). Abonnieren Sie `message.channels`, `message.im` oder die Channel-Scopes, die der Bot mithören soll. Sie brauchen **keine** Request-URL, da Socket Mode Ereignisse stattdessen über den Socket zustellt.
4. **Bot-Scopes hinzufügen** (Features → OAuth & Permissions). Mindestens: `chat:write`. Ergänzen Sie `im:history`, `channels:history`, `groups:history` oder `mpim:history` passend zu Ihren Event-Subscriptions.
5. **App in den Workspace installieren.** Der Installationsbildschirm liefert den `xoxb-*`-Bot-Token zurück.
6. **Optional die eigene User-ID des Bots notieren** (beginnt mit `U…`). Diese nutzt rousseau für die Schleifen-Verhinderung eigener Nachrichten.

## Konfiguration

```yaml
slack:
  app_token: "xapp-1-A0..."
  bot_token: "xoxb-1234..."
  bot_user_id: "U0123ABCD"
  reply_header: ""
  allowlist:
    - "U0ALICE"
    - "U0BOB"
```

| Feld | Standard | Wirkung |
|---|---|---|
| `app_token` | *erforderlich* | `xapp-*`-App-Level-Token mit `connections:write`. |
| `bot_token` | *erforderlich* | `xoxb-*`-Bot-Token mit `chat:write`. |
| `bot_user_id` | *leer* | `U…`-ID des Bot-Benutzers zur Schleifen-Verhinderung eigener Nachrichten. Optional; fällt sonst auf die Prüfung des `bot_id`-Feldes zurück. |
| `reply_header` | *leer* | Wird jeder ausgehenden Nachricht vorangestellt. |
| `allowlist` | `[]` | Slack-User-IDs, deren Nachrichten verarbeitet werden. |

## Befehlszeile

```sh
rousseau slack \
  --app-token xapp-... \
  --bot-token xoxb-... \
  --bot-user-id U0123ABCD
```

## Wire-Format

- **Inbound.** Slack sendet JSON-Envelopes über den WebSocket. rousseau bestätigt das Envelope (ACK), extrahiert Nachrichtentext und Absender und übergibt beides an den Handler.
- **Outbound.** `POST https://slack.com/api/chat.postMessage` mit `{"channel": "<id>", "text": "…"}` und `Authorization: Bearer <bot_token>`.

## OAuth-Scopes erklärt

Jeder Scope gewährt eine spezifische API-Oberfläche. Die Scopes, die rousseau benötigt, und was ohne sie bricht:

| Scope | Genutzter Endpunkt | Bricht ohne |
|---|---|---|
| `connections:write` | `apps.connections.open` (Socket-Mode-WebSocket) | Der Socket kann nicht geöffnet werden. **Erforderlich.** |
| `chat:write` | `chat.postMessage` | Auf keine Nachricht kann geantwortet werden. **Erforderlich.** |
| `im:history` | `conversations.history` für DMs (indirekt über Events) | Der Bot sieht keine DM-Inhalte in Events. |
| `im:read` | `im.list`, DM-Metadaten | Offene DMs können nicht aufgelistet werden. |
| `im:write` | `conversations.open` | Neue DMs können nicht eröffnet werden (nur relevant, wenn der Bot jemanden unaufgefordert per DM anschreiben soll). |
| `mpim:history`, `channels:history`, `groups:history` | Multi-Party-IMs / Channels / private Channels | Der Bot sieht keine Nachrichteninhalte ausserhalb von DMs. |

Setzen Sie die Scopes unter *OAuth &amp; Permissions &gt; Bot Token Scopes*. Fügen Sie nur Scopes hinzu, die Sie tatsächlich benötigen – Slack zeigt zur Installationszeit für jeden Scope eine Warnung an, und Endnutzer installieren eher einen Bot mit schmaler Berechtigungsfläche.

## Schleifen-Verhinderung eigener Nachrichten

Ohne Schutz sieht ein Bot, der auf Nachrichten antwortet, seine eigenen Antworten als eingehende Ereignisse – was zu Endlos-Schleifen führt. Rousseau löst dies über `bot_user_id`:

```go
// Vereinfacht – die tatsächliche Logik in internal/transport/slack/client.go
if msg.User == cfg.BotUserID {
    continue // Überspringen: das ist unsere eigene ausgehende Nachricht, die zurückkommt.
}
```

Ermitteln Sie die User-ID Ihres Bots einmalig via:

```sh
curl -H "Authorization: Bearer xoxb-your-token" \
  https://slack.com/api/auth.test
```

Die Antwort enthält `user_id`. Tragen Sie sie in `slack.bot_user_id` in der Config ein oder übergeben Sie sie via `--bot-user-id`.

<aside class="admonition" data-type="warning"><span class="admonition-title">Fallback-Schleifen-Verhinderung</span><p>Auch ohne <code>bot_user_id</code> ignoriert der Transport <code>bot_message</code>-Subtype-Ereignisse. Sich allein auf den Subtype zu verlassen, ist jedoch fragil – setzen Sie <code>bot_user_id</code> in Produktion.</p></aside>

## Threading

Slack-Nachrichten tragen ein `thread_ts`, wenn sie Antworten in einem Thread sind. Rousseaus ausgehende Aufrufe enthalten `thread_ts`, wenn das eingehende Ereignis eines hatte, damit Bot-Antworten im Thread bleiben. Top-Level-Nachrichten werden nur dann zu neuen Threads, wenn der Benutzer einen startet.

## Fehlermodi

| Symptom | Lösung |
|---|---|
| `invalid_auth` beim Socket-Öffnen | `app_token` ist falsch oder ohne `connections:write`. Neu generieren. |
| Eingehende Ereignisse treffen nie ein | Prüfen, ob **Event Subscriptions** aktiv sind und die relevanten `message.*`-Events abonniert sind. |
| Bot antwortet auf eigene Nachrichten | `bot_user_id` in der Config setzen. |
| `not_in_channel` beim Senden | Bot in den Channel einladen (`/invite @rousseau-bot`). |
| DM funktioniert, Channel nicht | Fehlender `channels:history`-Scope, oder der Bot wurde nicht in den Channel eingeladen. |

## Fehlerbehebung

### `invalid_auth` beim Socket-Öffnen

Der `xapp-…`-Token ist falsch oder hat seinen Scope verloren. Neu generieren unter *Basic Information &gt; App-Level Tokens*, `connections:write` auf dem neuen Token sicherstellen.

### `not_authed` bei `chat.postMessage`

Bot-Token (`xoxb-…`) fehlt oder ist falsch. Neu generieren unter *OAuth &amp; Permissions &gt; Bot User OAuth Token*.

### Ereignisse treffen ein, aber rousseau antwortet auf keines

Prüfen Sie die Allowlist. Im `pattern`-Modus mit `default: deny` werden nicht gelistete Benutzer stillschweigend verworfen. Suchen Sie in den Logs nach `router.transport.rejected`.

### `channel_not_found` beim Senden

Die Slack-Channel-ID (`C…`) hat sich geändert – z.B. wurde ein Channel archiviert und neu angelegt. Aktualisieren Sie fest hinterlegte Channel-IDs. Rousseau nutzt normalerweise den Channel aus dem eingehenden Ereignis, weshalb dies nur bei Cron-Zustellung an einen festen Channel auftritt.

### Bot erscheint in Slack offline

Socket Mode idled den WebSocket alle ~30s. Zeigt Slack den Bot als offline, prüfen Sie: (1) Läuft der Daemon (`systemctl --user status`), (2) ist der WebSocket verbunden (Log-Zeile `slack.connected`), (3) ist die Uhr der Maschine innerhalb von 30s der echten Zeit.

## Verwandte Seiten

- [Getting Started: Erster Transport](/de/getting-started/first-transport/) – End-to-End-Durchlauf.
- [Konfiguration](/de/configuration/) – der `slack`-Config-Block.
- [Transports](/de/transports/) – Geschwister-Transports.
- [Bereitstellung](/de/deployment/) – Slack in einem Podman-Container betreiben.
- [Guides: Audit &amp; Approval-Richtlinien](/de/guides/audit-approval-policies/) – Policy-Regelwerke für einen geteilten Slack-Workspace.

## Weiterführende Lektüre

- `internal/transport/slack/client.go` – Socket-Mode-Verbindung, Event-Pump, `chat.postMessage`.
- `internal/cli/slack.go` – CLI-Verdrahtung.
- `internal/transport/router.go` – Durchsetzung der Allowlist.
- [Slack-API-Dokumentation: Socket Mode](https://api.slack.com/apis/socket-mode).
