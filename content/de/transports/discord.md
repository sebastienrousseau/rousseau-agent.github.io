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
description: "Set up rousseau-agent's Discord transport: Gateway v10 WebSocket, bot token, Message Content intent, allowlist by user ID."
keywords: "Discord, Gateway v10, WebSocket, bot token, Message Content intent, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/transports/discord/"
subtitle: "Discord Gateway v10 over WebSocket."
tags: "transports, Discord"
title: "Discord-Transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Discord, Gateway v10, WebSocket, bot token, Message Content intent, allowlist"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Discord-Transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 17
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/discord/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/discord/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Discord-Transport"
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
twitter_description: "Set up rousseau-agent's Discord transport: Gateway v10 WebSocket, bot token, Message Content intent, allowlist by user ID."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Discord-Transport"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Was Sie lernen</span><p>Die Anleitung durch das Discord Developer Portal, welche Gateway-Intents rousseau benötigt und warum, den Permissions-Bit-Rechner in verständlicher Form sowie die Fehlerbilder häufiger Fehlkonfigurationen. Lesen Sie <code>internal/transport/discord/client.go</code> begleitend zu dieser Seite.</p></aside>

## Überblick

Der Discord-Transport (`internal/transport/discord/`) spricht das Discord Gateway v10-Protokoll direkt — ohne SDK von Drittanbietern. WebSocket für eingehende Nachrichten (`Identify → Ready → Heartbeat/Ack → Dispatch(MESSAGE_CREATE)`); REST für ausgehende (`POST /channels/{id}/messages`).

## Voraussetzungen

1. **Eine Discord-Anwendung mit Bot-Benutzer.** Erstellen unter https://discord.com/developers/applications → **New Application** → Tab **Bot** → **Add Bot**.
2. **Ein Bot-Token** (Tab Bot → **Reset Token** → Token kopieren — es ist nur einmal sichtbar).
3. **Message-Content-Intent aktiviert** (Tab Bot → **Privileged Gateway Intents**). Ohne diesen entfernt das Gateway den Nachrichtentext aus jedem Event, und rousseau sieht leere Inhalte.
4. **Der Bot ist auf mindestens einem Server eingeladen** (oder DMs aktiviert). Die Einladungs-URL wird unter **OAuth2 → URL Generator** mit dem Scope `bot` und den Berechtigungen `Send Messages` + `Read Message History` erzeugt.

## Konfiguration

```yaml
discord:
  token: "Bot MTIz..."
  reply_header: ""
  allowlist:
    - "123456789012345678"
```

| Feld | Standard | Wirkung |
|---|---|---|
| `token` | *erforderlich* | Bot-Token aus dem Developer Portal. |
| `reply_header` | *leer* | Wird jeder ausgehenden Antwort vorangestellt. |
| `allowlist` | `[]` | Discord-Benutzer-IDs, deren Nachrichten verarbeitet werden. |

## Kommandozeile

```sh
rousseau discord --token 'MTIz...' --allow 123456789012345678
```

## Gateway-Intents

rousseau fordert drei Intents an (`internal/transport/discord/client.go`):

| Intent | Bit | Zweck |
|---|---|---|
| `GUILD_MESSAGES` | `1 << 9` | Nachrichten in Server-Kanälen. |
| `DIRECT_MESSAGES` | `1 << 12` | Direktnachrichten an den Bot. |
| `MESSAGE_CONTENT` | `1 << 15` | Füllt das `content`-Feld. **Muss im Portal aktiviert sein.** |

Ohne den Message-Content-Intent treffen `MESSAGE_CREATE`-Events mit leerem `content` ein, und rousseau protokolliert `discord.empty_body`.

## Heartbeat

Der Transport respektiert das `heartbeat_interval` des Gateways aus dem Hello-Opcode, sendet Heartbeat + verfolgt `heartbeat_ack`. Ausbleibende ACKs schließen den Socket und lassen systemd den Prozess neu starten.

## Reply-Header

Discord rendert `**text**` als Fettschrift und erfordert kein spezielles Header-Format. Bei Bedarf überschreiben:

```yaml
discord:
  reply_header: "**Rousseau Agent**\n"
```

## Permissions-Bit-Rechner

Discord kodiert die Kanalberechtigungen eines Bots als Bitmaske. Jede Berechtigung ist eine Zweierpotenz. Häufige für rousseau:

| Berechtigung | Bit |
|---|---|
| Read Messages / View Channels | `1 << 10` = `1024` |
| Send Messages | `1 << 11` = `2048` |
| Send Messages in Threads | `1 << 38` = `274877906944` |
| Read Message History | `1 << 16` = `65536` |
| Add Reactions | `1 << 6` = `64` |

Um mehrere Berechtigungen zu erteilen, verknüpfen Sie die Bits mit OR und fügen die resultierende Ganzzahl in den Parameter `permissions=` des OAuth2 URL Generators ein:

```
Read Messages (1024) OR Send Messages (2048) OR Read Message History (65536) = 68608
```

<aside class="admonition" data-type="note"><span class="admonition-title">Hilfe im Portal</span><p>Der <em>OAuth2 URL Generator</em> im Developer Portal erlaubt das Ankreuzen von Berechtigungs-Checkboxen und berechnet die Ganzzahl automatisch. Speichern Sie die generierte URL als Lesezeichen — sie erlaubt Server-Administratoren, den Bot auf beliebige Discord-Server einzuladen.</p></aside>

## Gateway-Lebenszyklus

Das Gateway ist zustandsbehaftet:

```
Client                        Discord Gateway
  │
  │   ────  Connect  ────▶
  │   ◀── HELLO (heartbeat_interval)
  │
  │   ───── IDENTIFY (token, intents) ────▶
  │   ◀── READY (session_id, user)
  │
  │   ─── Heartbeat every N ms ─▶
  │   ◀── HEARTBEAT_ACK
  │
  │   ◀── MESSAGE_CREATE (a user typed)
  │   ─── (rousseau handles + POSTs reply)
  │
  │   ◀── Disconnect (code 4009: session timed out)
  │   ─── RESUME (session_id) or re-IDENTIFY
```

Der Client verfolgt `heartbeat_ack`. Bleibt ein ACK aus, wird der Socket geschlossen und der Prozess beendet — systemd oder die Container-Runtime starten ihn neu.

## Fehlerbilder

| Symptom | Behebung |
|---|---|
| Der Bot sieht leere Nachrichten | Message-Content-Intent im Developer Portal aktivieren. |
| Gateway schließt mit Code 4004 | Ungültiges Token. Neu generieren. |
| Der Bot sieht keine Kanäle | Sicherstellen, dass die OAuth2-Einladung den Scope `bot` enthielt. |
| 403 beim Senden | Dem Bot fehlt die Berechtigung `Send Messages` in diesem Kanal. |
| Code 4014 auf Identify | Angeforderter Intent ist für Ihre App nicht freigegeben (meist Message Content bei einem Bot auf 100+ Servern). Bot verifizieren. |
| Code 4009 (Session Timeout) | Normal nach langer Inaktivität. Rousseau verbindet sich transparent neu. |

## Troubleshooting

### Gateway 4013 (Invalid Intents)

Sie fordern ein Intent-Bit an, das nicht existiert. Meist ein Mismatch zwischen den Intent-Konstanten der Client-Bibliothek und Discords aktueller Intent-Map. Rousseau baut die Intent-Bitmaske in `internal/transport/discord/client.go`; auf die neueste Version aktualisieren, falls 4013 nach einer Discord-API-Änderung auftritt.

### Der Bot empfängt Events, antwortet aber nicht

Allowlist-Mismatch. Der Wert für `--allow` muss die numerische Discord-Benutzer-ID sein (nicht Benutzername, nicht Anzeigename). In Discord ermitteln: Developer Mode unter *User Settings &gt; Advanced* aktivieren, dann Rechtsklick auf einen Benutzer &gt; *Copy User ID*.

### DMs funktionieren, Gilden-Kanäle nicht

Fehlender Intent `GUILD_MESSAGES` oder Bot ist nicht in die Gilde eingeladen. Gilden-Berechtigungen sind unabhängig von DM-Berechtigungen — der Bot benötigt die Berechtigung `Read Messages` für den Kanal.

### `429 Too Many Requests` beim Senden

Discord erzwingt ein globales Rate Limit von 50 req/s pro Bot sowie pro-Kanal-Limits. Unter Dauerlast wiederholt rousseau derzeit nicht — der Aufrufer muss zurückfahren. Siehe [Leitfäden: Rate Limits](/de/guides/rate-limits/).

### Der Online-Status des Bots flappt

Discord betrachtet einen Bot nach ca. 40 s ohne Heartbeat als offline. Die Log-Zeile `discord.heartbeat_missed` deutet auf ein Netzwerkproblem oder einen CPU-limitierten Daemon hin. Prüfen, ob dem Container ausreichend CPU zugewiesen ist.

## Verwandte Seiten

- [Erste Schritte: Erster Transport](/de/getting-started/first-transport/) — vollständiger End-to-End-Durchlauf.
- [Konfiguration](/de/configuration/) — der `discord`-Konfigurationsblock.
- [Transports](/de/transports/) — verwandte Transports.
- [Leitfäden: Audit- &amp; Genehmigungsrichtlinien](/de/guides/audit-approval-policies/) — Richtlinien für Discord-Server.
- [Deployment](/de/deployment/) — Discord in einem Podman-Container betreiben.

## Weiterführende Literatur

- `internal/transport/discord/client.go` — Gateway-Verbindung, Heartbeat, Event-Pump.
- `internal/cli/discord.go` — CLI-Verdrahtung.
- `internal/transport/router.go` — Durchsetzung der Allowlist.
- [Discord-API-Dokumentation: Gateway](https://discord.com/developers/docs/topics/gateway).
- [Discord-API-Dokumentation: Permissions](https://discord.com/developers/docs/topics/permissions).
