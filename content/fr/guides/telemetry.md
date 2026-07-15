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
description: "Rousseau-agent ships zero telemetry. No analytics endpoint, no crash-report upload, no license server, no unique identifiers."
keywords: "telemetry, privacy, no phone home, no analytics, no license server"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/guides/telemetry/"
subtitle: "Zéro analytique, zéro remontée maison. Vérifiable."
tags: "guides, telemetry, privacy, security"
title: "Guide : télémétrie"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "telemetry, privacy, no phone home, no analytics, no license server"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide : télémétrie"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 40
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/telemetry/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/telemetry/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guide : télémétrie"
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
twitter_description: "Rousseau-agent ships zero telemetry. No analytics endpoint, no crash-report upload, no license server, no unique identifiers."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide : télémétrie"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Merci à chaque opérateur qui exploite son propre agent de codage."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## L'engagement

Rousseau-agent livre zéro télémétrie. La liste des choses que rousseau ne fait explicitement **pas** :

- Pas d'endpoint d'analytics. Il n'y a pas de `metrics.rousseau-agent.dev` ou équivalent.
- Pas de remontée de crash-report. Les panics atterrissent sur stderr ; rien n'est envoyé où que ce soit.
- Pas de serveur de licences. Pas de check-in périodique ni de vérification de siège.
- Pas d'identifiant d'installation unique. Le binaire est identique octet par octet sur chaque installation du même tag.
- Pas de service de feature flags. Chaque interrupteur de rousseau est dans `config.yaml` ou un flag CLI.
- Pas de ping de mise à jour. `rousseau version` est une consultation locale ; il n'y a pas d'aller-retour « vérification de mises à jour ».

## Comment vérifier

Le binaire rousseau est open source (MIT, voir `LICENSE`). Chaque appel réseau est grep-able :

```sh
grep -rn 'http.Get\|http.Post\|http.Client\|http.NewRequest\|net/http' \
  /path/to/rousseau-agent/internal/ | head
```

Chaque résultat entre dans une de ces catégories :

| Paquet | Objet |
|---|---|
| `internal/llm/anthropic/` | Appels à l'API Anthropic (via le SDK officiel). |
| `internal/llm/openai/` | Appels aux endpoints compatibles OpenAI. |
| `internal/transport/telegram/` | Bot API Telegram. |
| `internal/transport/matrix/` | API client-serveur Matrix. |
| `internal/transport/whatsapp/` | Websockets whatsmeow vers Meta. |
| `internal/transport/slack/`, `discord/` | Socket Mode / Discord Gateway. |
| `internal/transport/imessage/` | Serveur BlueBubbles (sur votre LAN). |
| `internal/transport/sms/` | Twilio / Vonage. |
| `internal/transport/email/` | IMAP + SMTP. |

Aucun n'est un endpoint d'analytics. Chacun est soit le fournisseur LLM que vous avez configuré, soit le transport que vous avez activé.

Exécutez le démon sous `strace -e network` ou surveillez-le avec `ss -tanp` — les seuls sockets que vous verrez sont vers les endpoints listés ci-dessus.

## Le logging structuré est local

Rousseau utilise `log/slog` (`internal/cli/root.go`). Par défaut, le handler écrit sur stderr, qui, sous l'unité Quadlet, atterrit dans le journal systemd. Rien n'est diffusé hors de l'hôte. Si vous voulez expédier les logs vers Loki, Datadog ou ailleurs, vous configurez ce pipeline vous-même — voir [Guides: Observability](/fr/guides/observability/).

## Comparaison

| Produit | Analytics | Remontée crash | Serveur de licences |
|---|---|---|---|
| rousseau-agent | aucun | aucune | aucun |
| Éditeur A (assistant de codage SaaS typique) | oui | oui | oui |
| Éditeur B (control plane géré) | oui | opt-out | oui |

Le modèle opérationnel de rousseau : vous apportez la clé LLM, vous hébergez le démon. Aucun morceau de rousseau ne tourne sur des serveurs contrôlés par Sebastien.

## Ce que rousseau _envoie_ aux fournisseurs LLM

Par définition, quand vous routez des messages via Anthropic, Bedrock, Vertex, OpenAI ou toute autre API, ce fournisseur voit le contenu du message. C'est inhérent au fonctionnement de l'inférence LLM — rousseau est un client, pas un adaptateur.

Deux atténuations si la gestion des données du fournisseur vous importe :

1. **Exécuter contre un modèle auto-hébergé.** Ollama, vLLM, LM Studio ou tout endpoint compatible OpenAI. Rien ne quitte votre machine. Voir [Guides: Self-hosted vLLM](/fr/guides/self-hosted-vllm/).
2. **Utiliser Bedrock ou Vertex dans une région avec un addendum de traitement des données.** AWS et GCP publient tous deux des garanties de résidence par région.

## Ce que voit le pont WhatsApp

Le protocole WhatsApp Web non officiel implémenté par whatsmeow parle aux serveurs de Meta — ce trafic est hors du contrôle de rousseau. Meta voit vos messages comme lorsque vous utilisez WhatsApp Web depuis un navigateur. Si le fait que Meta voie vos messages n'est pas acceptable, ne lancez pas le pont WhatsApp.

Le client whatsmeow est auditable publiquement — chaque paquet est documenté ; aucun appel réseau spécifique à rousseau n'est superposé.

## Voir aussi

- [Security](/fr/security/) — frontières de confiance et posture d'audit.
- [Privacy](/fr/privacy/) — la posture de confidentialité au niveau du site.
- [Providers: OpenAI-compatible](/fr/providers/openai-compatible/) — inférence auto-hébergée.
- [Guides: Self-hosted vLLM](/fr/guides/self-hosted-vllm/) — un exemple pratique.
