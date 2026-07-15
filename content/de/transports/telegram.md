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
description: "Set up rousseau-agent's Telegram transport: BotFather token, long-polling, allowlist by numeric user ID, reply-header customisation."
keywords: "Telegram, Bot API, BotFather, long polling, getUpdates, allowlist, chat ID"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/transports/telegram/"
subtitle: "Telegram Bot API over long-polling."
tags: "transports, Telegram"
title: "Telegram-Transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Telegram, Bot API, BotFather, long polling, getUpdates, allowlist, chat ID"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Telegram-Transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 14
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/telegram/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/telegram/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Telegram-Transport"
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
twitter_description: "Set up rousseau-agent's Telegram transport: BotFather token, long-polling, allowlist by numeric user ID, reply-header customisation."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Telegram-Transport"
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

Der Telegram-Transport (`internal/transport/telegram/`) spricht die Telegram Bot HTTP API direkt — ohne SDK von Drittanbietern. Long-Polling `getUpdates` für eingehende Nachrichten; `sendMessage` für ausgehende.

## Voraussetzungen

1. **Ein Bot.** Senden Sie in Telegram eine Nachricht an [@BotFather](https://t.me/BotFather), schicken Sie `/newbot`, wählen Sie einen Namen und einen Benutzernamen mit dem Suffix `_bot`. BotFather gibt ein HTTP-API-Token zurück, das etwa so aussieht: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`.
2. **Die Benutzer-IDs, die Sie autorisieren möchten.** Telegram-Benutzer-IDs sind numerisch. Der Bot kann `@username` nicht selbst in eine Benutzer-ID auflösen — üblicherweise lässt man jeden autorisierten Benutzer einmal `/start` an den Bot senden und liest anschließend `from.id` aus dem Log.

## Konfiguration

```yaml
telegram:
  token: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
  reply_header: ""
  allowlist:
    - "12345678"
    - "98765432"
```

| Feld | Standard | Wirkung |
|---|---|---|
| `token` | *erforderlich* | Bot-Token von BotFather. |
| `base_url` | `https://api.telegram.org` | Override für einen lokalen Bot-API-Server. |
| `reply_header` | *leer* | Wird jeder ausgehenden Antwort vorangestellt. |
| `allowlist` | `[]` | Telegram-Benutzer-IDs, deren Nachrichten verarbeitet werden. |

## Kommandozeile

```sh
rousseau telegram --token 123456:ABC... --allow 12345678 --allow 98765432
```

`--allow` kann mehrfach angegeben werden.

## Long-Polling

Der Transport ruft `getUpdates` standardmäßig mit einem `PollTimeout` von 30 Sekunden auf (`internal/transport/telegram/client.go`). Jedes zurückgegebene Update rückt einen internen `offset` vor, sodass Nachrichten auch über Neustarts hinweg niemals erneut zugestellt werden.

Es gibt keinen Webhook. Der Daemon benötigt keine eingehende HTTP-Fläche.

## Nachrichtenstruktur

Es werden ausschließlich Textnachrichten verarbeitet. Medien, Sticker und Sprachnotizen werden ignoriert (ein künftiges Upgrade könnte Audio über denselben whisper.cpp-Pfad wie WhatsApp leiten).

## Fehlerbilder

| Symptom | Behebung |
|---|---|
| Keine Updates treffen ein | Sicherstellen, dass der Bot mindestens einmal angeschrieben wurde — Telegram liefert keine historischen Nachrichten aus. |
| 409 Conflict bei getUpdates | Eine andere Instanz pollt mit demselben Token. Die andere beenden. |
| Allowlist weist einen echten Benutzer ab | Feld `from.id` loggen; Benutzer-IDs sind numerisch und entsprechen nicht `@username`. |
