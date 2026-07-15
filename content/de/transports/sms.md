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
description: "rousseau-agent's SMS transport is send-only. Twilio (account_sid + auth_token) or Vonage (api_key + auth_token). Inbound not supported because it requires a public webhook."
keywords: "SMS, Twilio, Vonage, Nexmo, send-only, Messaging Service SID, E.164, no webhook"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/transports/sms/"
subtitle: "Send-only SMS via Twilio or Vonage."
tags: "transports, SMS"
title: "SMS-Transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "SMS, Twilio, Vonage, Nexmo, send-only, Messaging Service SID, E.164, no webhook"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "SMS-Transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 19
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/sms/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/sms/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "SMS-Transport"
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
twitter_description: "rousseau-agent's SMS transport is send-only. Twilio (account_sid + auth_token) or Vonage (api_key + auth_token). Inbound not supported because it requires a public webhook."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "SMS-Transport"
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

## Nur ausgehend, per Design

Der SMS-Transport ist **nur ausgehend (send-only)**. Eingehende SMS erfordern einen öffentlichen HTTP-Webhook, in den der Carrier POSTet — was direkt der Zero-Inbound-Surface-Haltung von rousseau widerspricht. Wenn Ihr Anwendungsfall eingehende SMS benötigt, betreiben Sie rousseau parallel zu einem zweckgebauten Webhook-Receiver und leiten Nachrichten über den Cron-Scheduler oder die Embed-API des Agent-Loops.

`Start` ist als No-Op implementiert, der auf `ctx.Done()` blockiert, sodass sich der Transport dennoch in die Standard-Verdrahtung des Daemons einfügt.

## Unterstützte Carrier

| Carrier | Konfigurations-`provider` | Pflichtfelder |
|---|---|---|
| Twilio | `twilio` | `from`, `account_sid`, `auth_token` |
| Vonage (früher Nexmo) | `vonage` | `from`, `api_key`, `auth_token` (das API-Secret) |

## Twilio-Konfiguration

```yaml
sms:
  provider: twilio
  from: "+15550000000"
  account_sid: "AC..."
  auth_token: "..."
```

`from` kann entweder eine E.164-Absendernummer oder eine **Twilio Messaging Service SID** (beginnt mit `MG…`) sein. Messaging Services übernehmen Flottenmanagement, Sticky-Sender-Routing und geobasierte Absenderauswahl — empfohlen für alles jenseits von Verkehr innerhalb eines einzelnen Landes.

`base_url` ist standardmäßig `https://api.twilio.com/2010-04-01` und muss nur für regionale Endpunkte oder Tests überschrieben werden.

## Vonage-Konfiguration

```yaml
sms:
  provider: vonage
  from: "+15550000000"
  api_key: "abcd1234"
  auth_token: "efgh5678"
```

`auth_token` in der Vonage-Konfiguration entspricht dem **API-Secret** von Vonage, nicht dem JWT-Signaturschlüssel — Vonage authentifiziert SMS-Einreichungen mit einem einfachen Key/Secret-Paar.

`base_url` ist standardmäßig `https://rest.nexmo.com`.

## Kommandozeile

```sh
# Twilio
rousseau sms \
  --provider twilio \
  --from '+15550000000' \
  --account-sid AC... \
  --auth-token ...

# Vonage
rousseau sms \
  --provider vonage \
  --from '+15550000000' \
  --api-key abcd1234 \
  --auth-token efgh5678
```

Da es keine Empfangsseite gibt, ist `--allow` nicht anwendbar.

## Zustell-API

Beide Provider nutzen ihre jeweiligen REST-Endpunkte:

- **Twilio.** `POST /2010-04-01/Accounts/{sid}/Messages.json` mit Basic Auth SID/Token.
- **Vonage.** `POST /sms/json` mit `api_key` + `api_secret` im Body.

Zurückgegebene Nachrichten-IDs werden geloggt; Zustellstatus-Webhooks werden **nicht** konsumiert (auch hier: keine öffentliche HTTP-Fläche).

## E.164-Formatierung

`from`- und Zielrufnummern müssen im E.164-Format vorliegen (`+<land><teilnehmer>`). Keine Leerzeichen, keine Bindestriche. Twilio Messaging Service SIDs umgehen diese Vorgabe nur für den `from`-Slot.

## Kosten-Hygiene

- Setzen Sie `max_tokens` beim Provider aggressiv — SMS ist pro Nachricht günstig, aber Bytes vervielfachen sich schnell, wenn das Modell lange Antworten erzeugt (Twilio segmentiert bei 160 Zeichen für GSM-7 bzw. 70 für UCS-2).
- Erwägen Sie, die ausgehende Antwort vor Übergabe an den SMS-Transport knapper zu formulieren. Der richtige Ort dafür ist `agent.Options.SystemPrompt`.
