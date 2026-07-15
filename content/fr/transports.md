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
changefreq: "monthly"
description: "Overview of rousseau-agent's nine chat transports: WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, Email, SMS. Every transport implements Start / Stop / Deliver."
keywords: "transports, WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, email, SMS"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/transports/"
subtitle: "Neuf transports de messagerie derrière une seule interface Transport."
tags: "transports, overview"
title: "Transports"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "transports, WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, email, SMS"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transports"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 11
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transports"
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
twitter_title: "Transports"
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

## L'interface Transport

Chaque transport implémente une petite interface (`internal/transport/transport.go`) :

```go
type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

Au-dessus du transport se trouve le `Router`, qui gère la recherche de session par émetteur, l'application de l'allowlist et la distribution vers l'`Agent`. En dessous se trouve le code réseau spécifique au transport.

Aucun des transports livrés n'expose de surface HTTP publique par défaut. C'est un choix de posture délibéré — les démons rousseau doivent être sûrs à exécuter derrière un NAT sans règles de redirection de port.

## Transports supportés

| Transport | Entrant | Sortant | Bibliothèque / protocole | Auth | Installation en une ligne |
|---|:---:|:---:|---|---|---|
| [WhatsApp](/fr/transports/whatsapp/) | oui | oui | `go.mau.fi/whatsmeow` | Appairage d'appareil (QR) | `rousseau whatsapp --allow <jid>` |
| [Signal](/fr/transports/signal/) | oui | oui | JSON-RPC `signal-cli` | Compte pré-enregistré | `rousseau signal --account +447900123456` |
| [Telegram](/fr/transports/telegram/) | oui | oui | Long-polling Bot API | Jeton BotFather | `rousseau telegram --token <token>` |
| [Matrix](/fr/transports/matrix/) | oui | oui | Client-server API `/sync` | Jeton d'accès | `rousseau matrix --homeserver-url … --access-token …` |
| [Slack](/fr/transports/slack/) | oui | oui | Socket Mode + Web API | `xapp-*` + `xoxb-*` | `rousseau slack --app-token … --bot-token …` |
| [Discord](/fr/transports/discord/) | oui | oui | Gateway v10 + REST | Jeton de bot | `rousseau discord --token <token>` |
| [iMessage](/fr/transports/imessage/) | oui | oui | Polling HTTP BlueBubbles | Mot de passe serveur | `rousseau imessage --base-url … --password …` |
| [Email](/fr/transports/email/) | oui | oui | IMAP + SMTP | Nom d'utilisateur + mot de passe | `rousseau email --imap-addr … --smtp-addr …` |
| [SMS](/fr/transports/sms/) | non | oui | REST Twilio ou Vonage | Account SID / API key | `rousseau sms --provider twilio --account-sid … --auth-token …` |

## Pourquoi aucune surface HTTP publique

Deux choix de conception maintiennent chaque transport listé loin d'un webhook public :

- **Entrée basée sur WebSocket.** Slack Socket Mode et Discord Gateway sont sortants uniquement du point de vue du démon — le démon compose vers le fournisseur en TLS et les messages arrivent sur la même connexion.
- **Polling.** WhatsApp, Telegram, Matrix, iMessage et email récupèrent les mises à jour à leur propre cadence. Il n'y a pas de webhook que le fournisseur appelle.

SMS est l'exception, et rousseau la résout en rendant SMS **envoi seul**. Un SMS entrant nécessiterait un webhook Twilio / Vonage, ce qui est exactement la surface que ce projet refuse d'introduire.

## Comportement du routeur

Le routeur (`internal/transport/router.go`) se place entre chaque transport et l'`Agent` :

- **Isolation de session.** Chaque valeur `From` distincte reçoit sa propre `Session`, pour que les conversations parallèles ne se contaminent pas. Les identités LID WhatsApp sont d'abord normalisées en JID de téléphone (voir `internal/transport/whatsapp/resolve.go`).
- **Allowlist.** Chaque transport supportant l'entrant a une `Allowlist []string` dans sa config. Vide signifie « accepter chaque émetteur » — pour les démons vous voulez toujours au moins une entrée.
- **Distribution.** Le routeur sérialise les tours par session pour qu'un utilisateur ne puisse pas empiler deux messages entrants concurrents.

## Ajouter un dixième transport

Implémentez `transport.Transport` (trois méthodes). Ajoutez un type `Config` reflétant l'agencement de bloc sous `internal/config/`. Câblez une commande CLI dans `internal/cli/`. C'est la surface — le cœur de l'agent reste intact.

## Pages par transport

- [WhatsApp](/fr/transports/whatsapp/)
- [Signal](/fr/transports/signal/)
- [Telegram](/fr/transports/telegram/)
- [Matrix](/fr/transports/matrix/)
- [Slack](/fr/transports/slack/)
- [Discord](/fr/transports/discord/)
- [iMessage](/fr/transports/imessage/)
- [Email](/fr/transports/email/)
- [SMS](/fr/transports/sms/)
