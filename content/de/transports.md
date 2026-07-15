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
description: "Overview of rousseau-agent's nine chat transports: WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, Email, SMS. Every transport implements Start / Stop / Deliver."
keywords: "transports, WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, email, SMS"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/transports/"
subtitle: "Neun Chat-Transporte hinter einer Transport-Schnittstelle."
tags: "transports, overview"
title: "Transporte"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "transports, WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, email, SMS"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transporte"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 11
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transporte"
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
twitter_description: "Overview of rousseau-agent's nine chat transports: WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, Email, SMS. Every transport implements Start / Stop / Deliver."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transporte"
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

## Die Transport-Schnittstelle

Jeder Transport implementiert eine kleine Schnittstelle (`internal/transport/transport.go`):

```go
type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

Über dem Transport sitzt der `Router`, der die Sitzungssuche pro Absender, die Allowlist-Durchsetzung und das Dispatch an den `Agent` übernimmt. Darunter liegt der transport-spezifische Wire-Code.

Keiner der ausgelieferten Transporte exponiert standardmäßig eine öffentliche HTTP-Oberfläche. Dies ist eine bewusste Haltungsentscheidung – rousseau-Daemons sollten sicher hinter NAT ohne Port-Forwarding-Regeln laufen können.

## Unterstützte Transporte

| Transport | Eingehend | Ausgehend | Zugrundeliegende Bibliothek / Protokoll | Auth | Ein-Zeilen-Setup |
|---|:---:|:---:|---|---|---|
| [WhatsApp](/de/transports/whatsapp/) | ja | ja | `go.mau.fi/whatsmeow` | Geräte-Kopplung (QR) | `rousseau whatsapp --allow <jid>` |
| [Signal](/de/transports/signal/) | ja | ja | `signal-cli` JSON-RPC | Vorregistriertes Konto | `rousseau signal --account +447900123456` |
| [Telegram](/de/transports/telegram/) | ja | ja | Bot-API Long-Polling | BotFather-Token | `rousseau telegram --token <token>` |
| [Matrix](/de/transports/matrix/) | ja | ja | Client-Server-API `/sync` | Access-Token | `rousseau matrix --homeserver-url … --access-token …` |
| [Slack](/de/transports/slack/) | ja | ja | Socket Mode + Web-API | `xapp-*` + `xoxb-*` | `rousseau slack --app-token … --bot-token …` |
| [Discord](/de/transports/discord/) | ja | ja | Gateway v10 + REST | Bot-Token | `rousseau discord --token <token>` |
| [iMessage](/de/transports/imessage/) | ja | ja | BlueBubbles-HTTP-Polling | Server-Passwort | `rousseau imessage --base-url … --password …` |
| [Email](/de/transports/email/) | ja | ja | IMAP + SMTP | Benutzername + Passwort | `rousseau email --imap-addr … --smtp-addr …` |
| [SMS](/de/transports/sms/) | nein | ja | Twilio- oder Vonage-REST | Account-SID / API-Key | `rousseau sms --provider twilio --account-sid … --auth-token …` |

## Warum keine öffentliche HTTP-Oberfläche

Zwei Design-Entscheidungen halten jeden aufgeführten Transport von einem öffentlichen Webhook fern:

- **WebSocket-basierte Eingänge.** Slack Socket Mode und Discord Gateway sind aus Sicht des Daemons ausschließlich ausgehend – der Daemon wählt den Anbieter über TLS an und Nachrichten kommen auf derselben Verbindung an.
- **Polling.** WhatsApp, Telegram, Matrix, iMessage und E-Mail rufen Updates in eigenem Takt ab. Es gibt keinen Webhook, den der Anbieter aufruft.

SMS ist die Ausnahme, und rousseau löst dies, indem SMS **nur ausgehend** ist. Eingehende SMS würden einen Twilio-/Vonage-Webhook erfordern, was genau die Oberfläche ist, die dieses Projekt nicht einführen will.

## Router-Verhalten

Der Router (`internal/transport/router.go`) sitzt zwischen jedem Transport und dem `Agent`:

- **Sitzungsisolation.** Jeder unterschiedliche `From`-Wert erhält seine eigene `Session`, sodass parallele Konversationen sich nicht gegenseitig kontaminieren. WhatsApp-LID-Identitäten werden zuerst zu Telefon-JIDs normalisiert (siehe `internal/transport/whatsapp/resolve.go`).
- **Allowlist.** Jeder Transport, der Eingänge unterstützt, hat eine `Allowlist []string` in seiner Konfiguration. Leer bedeutet "jeden Absender akzeptieren" – für Daemons möchten Sie immer mindestens einen Eintrag.
- **Dispatch.** Der Router serialisiert Turns pro Sitzung, sodass ein Benutzer nicht zwei gleichzeitige eingehende Nachrichten stapeln kann.

## Einen zehnten Transport hinzufügen

Implementieren Sie `transport.Transport` (drei Methoden). Fügen Sie einen `Config`-Typ hinzu, der das Blocklayout unter `internal/config/` spiegelt. Verdrahten Sie einen CLI-Befehl in `internal/cli/`. Das ist die Oberfläche – der Agent-Kern bleibt unberührt.

## Seiten pro Transport

- [WhatsApp](/de/transports/whatsapp/)
- [Signal](/de/transports/signal/)
- [Telegram](/de/transports/telegram/)
- [Matrix](/de/transports/matrix/)
- [Slack](/de/transports/slack/)
- [Discord](/de/transports/discord/)
- [iMessage](/de/transports/imessage/)
- [Email](/de/transports/email/)
- [SMS](/de/transports/sms/)
