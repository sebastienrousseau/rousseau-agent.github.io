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
changefreq: "weekly"
description: "Agent de codage auto-hébergé avec 9 transports de messagerie, 5 fournisseurs LLM, serveur MCP, provenance SLSA-3, versions signées avec cosign."
keywords: "rousseau-agent, agent de codage, auto-hébergé, natif conteneur, MCP, SLSA-3, cosign, SBOM, LLM, WhatsApp, Signal, Slack"
layout: "index"
permalink: "https://docs.rousseau-agent.dev/fr/"
subtitle: "Agent de codage auto-hébergé, natif conteneur, natif MCP."
tags: "vue d'ensemble, auto-hébergé, mcp, sécurité"
title: "rousseau-agent"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "rousseau-agent, agent de codage, auto-hébergé, natif conteneur, MCP, SLSA-3, cosign, SBOM, LLM, WhatsApp, Signal, Slack"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "rousseau-agent"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "welcome"
order: 1
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/index.html"
item_link: "https://docs.rousseau-agent.dev/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "rousseau-agent"
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
twitter_description: "Agent de codage auto-hébergé avec 9 transports de messagerie, 5 fournisseurs LLM, serveur MCP, provenance SLSA-3, versions signées avec cosign."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "rousseau-agent"
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

## Agent de codage auto-hébergé, natif conteneur, natif MCP

**rousseau-agent** est un assistant de codage en Go qui s'exécute là où votre code s'exécute. Le démon, les identifiants d'authentification et le trafic vers le modèle restent sur du matériel contrôlé par l'opérateur. **9 transports · 5 fournisseurs LLM · SLSA-3 · cosign · SBOM.**

```sh
rousseau chat
```

Cette seule commande lance une interface TUI Bubble Tea adossée au fournisseur LLM que vous avez configuré. Rien ne franchit le périmètre réseau, à l'exception de l'appel au fournisseur lui-même.

## Trois piliers

### Durci pour l'entreprise

- Provenance de build **SLSA niveau 3** via `slsa-framework/slsa-github-generator`.
- Signatures **cosign** sans clé sur chaque fichier de somme de contrôle publié, vérifiables contre le journal de transparence Sigstore.
- SBOM **CycloneDX** JSON joint à chaque version.
- **Builds reproductibles** vérifiés en CI sur un checkout neuf.
- Podman rootless avec `ReadOnly=true`, `DropCapability=all`, `NoNewPrivileges=true`, filtre seccomp par défaut, UID 1000 non-root, mapping d'espace de noms utilisateur `keep-id`.
- Passerelle 18 linters `golangci-lint` v2, CodeQL (Go), `govulncheck` à chaque exécution CI, Dependabot pour `gomod` et `github-actions`.

### Portée multi-modale

Neuf transports de messagerie derrière un seul démon :

- [WhatsApp](/fr/transports/whatsapp/) (`go.mau.fi/whatsmeow`, compatible avec le protocole Signal)
- [Signal](/fr/transports/signal/) (sous-processus JSON-RPC `signal-cli`)
- [Telegram](/fr/transports/telegram/) (long-polling de l'API Bot)
- [Matrix](/fr/transports/matrix/) (API client-serveur)
- [Slack](/fr/transports/slack/) (Socket Mode, aucune surface HTTP publique)
- [Discord](/fr/transports/discord/) (Gateway v10)
- [iMessage](/fr/transports/imessage/) (interrogation HTTP BlueBubbles)
- [Email](/fr/transports/email/) (IMAP + SMTP)
- [SMS](/fr/transports/sms/) (Twilio ou Vonage, envoi seul)

### Indépendant du modèle

Cinq familles de fournisseurs LLM, une seule interface `agent.Provider` :

- [claudecli](/fr/providers/claudecli/) — sous-processus s'appuyant sur votre CLI `claude` locale, hérite de son authentification.
- [Anthropic](/fr/providers/anthropic/) — API directe avec marqueurs de cache de prompt éphémères.
- [AWS Bedrock](/fr/providers/bedrock/) — chaîne d'identifiants AWS standard.
- [Google Vertex AI](/fr/providers/vertex/) — JSON de compte de service ou ADC.
- [Compatible OpenAI](/fr/providers/openai-compatible/) — OpenAI, OpenRouter, Ollama, vLLM, LM Studio.

## Pour aller plus loin

- [Prise en main](/fr/getting-started/) — installation, première exécution, premier transport.
- [Configuration](/fr/configuration/) — chaque champ de `internal/config/config.go`.
- [Déploiement](/fr/deployment/) — Podman rootless + Quadlet, note Kubernetes.
- [Sécurité](/fr/security/) — posture de la chaîne d'approvisionnement, modèle de confiance, recette cosign.
- [Concepts](/fr/concepts/) — boucle d'agent, magasin de sessions, MCP, cron, compétences.
