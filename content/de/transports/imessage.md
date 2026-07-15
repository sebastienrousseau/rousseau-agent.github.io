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
description: "Set up rousseau-agent's iMessage transport: BlueBubbles server on macOS, HTTP polling, poll interval, cursor deduplication, chat GUID for outbound."
keywords: "iMessage, BlueBubbles, macOS, HTTP polling, chat GUID, cursor, deduplication"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/transports/imessage/"
subtitle: "BlueBubbles HTTP polling from a macOS host."
tags: "transports, iMessage"
title: "iMessage-Transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "iMessage, BlueBubbles, macOS, HTTP polling, chat GUID, cursor, deduplication"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "iMessage-Transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 18
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/imessage/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/imessage/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "iMessage-Transport"
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
twitter_description: "Set up rousseau-agent's iMessage transport: BlueBubbles server on macOS, HTTP polling, poll interval, cursor deduplication, chat GUID for outbound."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "iMessage-Transport"
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

## Überblick

Der iMessage-Transport (`internal/transport/imessage/`) greift nicht direkt auf iMessage zu — Apple stellt keine unterstützte, an Clients gerichtete API bereit. Stattdessen pollt er [BlueBubbles](https://bluebubbles.app), einen macOS-seitigen Daemon, der iMessage über HTTP + Socket.IO exponiert.

rousseau nutzt ausschließlich die HTTP-Endpunkte von BlueBubbles (Socket.IO wird bewusst gemieden, um die Abhängigkeitsfläche klein zu halten).

## Architektur

```
+-----------+     iMessage      +---------+     HTTP      +-----------+
| Apple ID  | <---------------> | macOS   | <-----------> | rousseau  |
|  server   |                   | Blue    |               | daemon    |
+-----------+                   | Bubbles |               |           |
                                +---------+               +-----------+
```

Der macOS-Host betreibt BlueBubbles und bleibt bei iMessage angemeldet. rousseau pollt den Endpunkt `/api/v1/message` von BlueBubbles im konfigurierten Takt und leitet Neueingänge an den Handler weiter.

## Voraussetzungen

1. **Ein macOS-Host** mit angemeldetem iMessage. Nicht notwendigerweise dieselbe Maschine, auf der rousseau läuft.
2. **BlueBubbles-Server** auf diesem Host installiert, erreichbar unter einer URL, die rousseau ansteuern kann (LAN-Adresse, VPN oder Tailscale).
3. **BlueBubbles-Passwort** aus der Server-GUI (Einstellungen → Server-Passwort).
4. **Eine Chat-GUID** für ausgehende Nachrichten. In der BlueBubbles-GUI oder per `GET /api/v1/chat` ermitteln.

## Konfiguration

```yaml
imessage:
  base_url: "http://mac.internal:1234"
  password: "..."
  chat_guid: "iMessage;-;+15550001234"
  poll_interval: "5s"
  reply_header: ""
```

| Feld | Standard | Wirkung |
|---|---|---|
| `base_url` | *erforderlich* | URL des BlueBubbles-Servers. |
| `password` | *erforderlich* | Passwort des BlueBubbles-Servers. |
| `chat_guid` | *leer* | GUID des ausgehenden Ziels. |
| `poll_interval` | `5s` | Poll-Takt gegen `/api/v1/message`. |
| `reply_header` | *leer* | Wird jeder ausgehenden Nachricht vorangestellt. |

## Kommandozeile

```sh
rousseau imessage \
  --base-url http://mac.internal:1234 \
  --password ... \
  --chat-guid 'iMessage;-;+15550001234' \
  --poll-interval 5s
```

## Cursor-Deduplizierung

Beim Start initialisiert der Transport seinen `lastID`-Cursor mit der neuesten vorhandenen Nachricht, damit der Operator nicht mit der gesamten iMessage-Historie überflutet wird. Jeder folgende Poll holt die neuesten `PageSize`-Nachrichten (Standard 25) und leitet nur jene weiter, die neuer als der Cursor sind.

Der Cursor liegt im Speicher. Beim Neustart wird er aus BlueBubbles neu initialisiert — ein kleines Fenster an Nachrichten, das während der Ausfallzeit des Daemons eintraf, wird verpasst. Dies ist ein bewusster Kompromiss; persistente Cursor-Logik würde eine weitere Tabelle im State Store erfordern, und iMessage-Zustellzeitstempel sind über Geräte hinweg nicht garantiert monoton.

## Erreichbarkeit

BlueBubbles muss aus der Umgebung, in der rousseau läuft, über das Netzwerk erreichbar sein. Übliche Muster:

- **Gleiches LAN.** `http://<mac-lan-ip>:1234`.
- **Tailscale.** `http://mac.tailnet.ts.net:1234`. Verschlüsselt die Verbindung und funktioniert über NAT hinweg.
- **Reverse Tunnel.** `http://localhost:1234` auf dem rousseau-Host mit einem SSH-`-R`-Tunnel vom Mac aus.

BlueBubbles nicht ins öffentliche Internet exponieren, sofern das Auth-Modell (ein einzelnes Passwort) nicht verstanden wurde.

## Fehlerbilder

| Symptom | Behebung |
|---|---|
| `imessage.prime_failed` beim Start | BlueBubbles nicht erreichbar — `base_url` und `password` prüfen. |
| Jede historische Nachricht wird erneut abgespielt | `lastID` wurde nicht initialisiert. Berechtigungen/Auth prüfen. |
| Ausgehende Nachrichten werden stillschweigend verworfen | Falsche `chat_guid`. Per `GET /api/v1/chat` nachschlagen. |
| Nachrichten treffen minutenlang verzögert ein | BlueBubbles' eigene Poll-Frequenz erhöhen oder `poll_interval` reduzieren. |
