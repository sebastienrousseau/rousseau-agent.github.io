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
description: "Set up rousseau-agent's Matrix transport: homeserver URL, access token, user ID, long-polling /sync, allowlist by MXID."
keywords: "Matrix, client-server, MXID, access token, homeserver, /sync, long polling, Synapse"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/transports/matrix/"
subtitle: "Matrix client-server API with long-polling /sync."
tags: "transports, Matrix"
title: "Matrix-Transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Matrix, client-server, MXID, access token, homeserver, /sync, long polling, Synapse"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Matrix-Transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 15
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/matrix/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/matrix/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Matrix-Transport"
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
twitter_description: "Set up rousseau-agent's Matrix transport: homeserver URL, access token, user ID, long-polling /sync, allowlist by MXID."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Matrix-Transport"
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

Der Matrix-Transport (`internal/transport/matrix/`) spricht die Matrix Client-Server-API direkt — ohne SDK von Drittanbietern. `/sync`-Long-Polling für eingehende Nachrichten; `/rooms/{room}/send/{event_type}/{txn_id}` für ausgehende.

Funktioniert mit jedem spezifikationskonformen Homeserver: Synapse, Dendrite, Conduit.

## Voraussetzungen

1. **Ein Bot-Konto** auf dem Homeserver Ihrer Wahl. Registrierung über einen üblichen Matrix-Client oder die Admin-API des Homeservers.
2. **Ein Access Token** für dieses Konto. Melden Sie den Bot einmal an einem gewöhnlichen Matrix-Client an und kopieren Sie das Token aus **Einstellungen → Hilfe & Info → Access Token**. Alternativ nutzen Sie die Login-API direkt:

   ```sh
   curl -X POST https://matrix.org/_matrix/client/v3/login \
     -H 'Content-Type: application/json' \
     -d '{"type":"m.login.password","user":"bot","password":"..."}'
   ```

3. **Die vollständige MXID des Bots** (z. B. `@rousseau-bot:matrix.org`) für die Echo-Unterdrückung eigener Nachrichten.

## Konfiguration

```yaml
matrix:
  homeserver_url: "https://matrix.org"
  access_token: "syt_..."
  user_id: "@rousseau-bot:matrix.org"
  reply_header: ""
  allowlist:
    - "@alice:matrix.org"
    - "@bob:example.com"
```

| Feld | Standard | Wirkung |
|---|---|---|
| `homeserver_url` | *erforderlich* | Basis-URL (`https://matrix.org`). |
| `access_token` | *erforderlich* | Access Token des Bot-Benutzers. |
| `user_id` | *leer* | Vollständige MXID des Bot-Benutzers. Optional, aber empfohlen (Echo-Unterdrückung eigener Nachrichten). |
| `reply_header` | *leer* | Wird jeder ausgehenden Antwort vorangestellt. |
| `allowlist` | `[]` | MXIDs, deren Nachrichten verarbeitet werden. |

## Kommandozeile

```sh
rousseau matrix \
  --homeserver-url https://matrix.org \
  --access-token syt_... \
  --user-id @rousseau-bot:matrix.org \
  --allow @alice:matrix.org
```

## Long-Polling

`PollTimeout` beträgt standardmäßig 30 Sekunden. Der `since`-Cursor jeder `/sync`-Antwort wird im Speicher gehalten und beim nächsten Aufruf verwendet, sodass Nachrichten während der Prozesslaufzeit nie erneut zugestellt werden. Beim Neustart spult der Daemon auf den frühesten noch gültigen Cursor zurück, den der Homeserver liefert — dies ist die übliche `sync`-Semantik und entspricht dem Verhalten jedes Matrix-Clients.

## Raum-Einladungen

Der Bot muss bereits Mitglied jedes Raums sein, in dem er antworten soll. Laden Sie ihn aus einem gewöhnlichen Matrix-Client ein. rousseau akzeptiert Einladungen nicht automatisch; der Beitritt liegt außerhalb des Scopes.

## Fehlerbilder

| Symptom | Behebung |
|---|---|
| 401 auf `/sync` | Access Token abgelaufen oder ungültig. Erneut anmelden. |
| Der Bot sieht keine Nachricht | Sicherstellen, dass der Bot Mitglied des Raums ist, nicht nur eingeladen. |
| Echo-Schleife eigener Nachrichten | `user_id` in der Konfiguration setzen, damit rousseau eigene Nachrichten filtern kann. |
