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
description: "Support matrix for rousseau-agent: operating systems, CPU architectures, container runtimes, provider authentication methods, transport backing libraries."
keywords: "platform support, os matrix, architecture, container runtime, provider auth, linux, macos, windows, arm64, amd64"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/getting-started/platform-support/"
subtitle: "OS, architectures, container runtimes, provider auth methods."
tags: "platform, support, matrix"
title: "Plateformes prises en charge"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "platform support, os matrix, architecture, container runtime, provider auth, linux, macos, windows, arm64, amd64"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Plateformes prises en charge"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 23
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/platform-support/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/platform-support/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Plateformes prises en charge"
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
twitter_description: "Support matrix for rousseau-agent: operating systems, CPU architectures, container runtimes, provider authentication methods, transport backing libraries."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Plateformes prises en charge"
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

## Systèmes d'exploitation

| OS | Niveau de support | Notes |
|---|---|---|
| Linux (glibc, kernel 5.10+) | Tier 1 | La CI exécute `ubuntu-latest` à chaque push. Cible de déploiement de référence. |
| Linux (musl / Alpine) | Tier 1 | L'image de conteneur est basée sur Alpine. |
| macOS 13+ (Ventura ou plus récent) | Tier 1 | La CI exécute `macos-latest` à chaque push. TUI Bubble Tea vérifiée. |
| Windows 10 / 11 | Tier 2 | Les binaires sont compilés et livrés, mais la CI n'exécute pas la matrice complète en mode course sous Windows. Les transports chat fonctionnent ; le déploiement de référence Podman + Quadlet suppose Linux. |
| FreeBSD / OpenBSD | Best-effort | Build pur Go, mais pas de job CI. Retours de la communauté bienvenus. |

## Architectures CPU

| Architecture | Niveau de support | Nommage des releases |
|---|---|---|
| `amd64` (x86-64) | Tier 1 | `_linux_amd64`, `_darwin_amd64`, `_windows_amd64` |
| `arm64` (aarch64) | Tier 1 | `_linux_arm64`, `_darwin_arm64` (Apple Silicon) |
| `armv7` (ARM 32 bits) | Best-effort | Compilable via `GOARCH=arm GOARM=7` ; non publié. |
| `riscv64` | Best-effort | Compilable via `GOARCH=riscv64` ; non publié. |

`CGO_ENABLED=0` sur chaque cible — `modernc.org/sqlite` est pur Go, donc la compilation croisée se fait sans friction.

## Runtimes de conteneurs

| Runtime | Niveau de support | Notes |
|---|---|---|
| Podman 4.4+ (rootless) | Tier 1 | Déploiement de référence. Utilise les unités Quadlet systemd pour un durcissement déclaratif. |
| Docker 24+ | Tier 1 | Le Dockerfile fonctionne sans modification. Le durcissement à l'exécution reste de votre ressort (pas d'équivalent Quadlet). |
| containerd + `nerdctl` | Tier 2 | Même image ; nerdctl consomme le même artefact OCI. |
| Kubernetes 1.27+ | Tier 2 | Voir [Guides: Kubernetes deployment](/fr/guides/kubernetes-deployment/). |

## Méthodes d'authentification des fournisseurs

| Fournisseur | Mécanisme d'authentification | Clés de configuration |
|---|---|---|
| `claudecli` (par défaut) | Hérite des jetons OAuth de Claude Code depuis `~/.claude/`. Pas de clé dans la configuration de rousseau. | `claudecli.binary`, `claudecli.permission_mode` |
| `anthropic` | Clé API directe. | Variable d'env `ANTHROPIC_API_KEY`, ou `anthropic.api_key` |
| `openai` | Clé API OpenAI ou jeton tiers. | `OPENAI_API_KEY`, ou `openai.api_key` |
| `openrouter` | Clé API OpenRouter. Utilise le schéma OpenAI avec `openrouter.base_url` préréglé. | `openrouter.api_key` |
| `ollama` | Endpoint local, aucune clé requise (`ollama.api_key` vaut par défaut `not-required`). | `ollama.base_url` préréglé à `http://localhost:11434/v1` |
| `bedrock` | Chaîne d'identifiants AWS standard (variables d'env, `~/.aws/credentials`, IMDS, rôle IAM). | `bedrock.region`, `bedrock.profile`, `bedrock.model` |
| `vertex` | JSON de compte de service GCP, ou Application Default Credentials. | `vertex.project`, `vertex.region`, `vertex.credentials_file` |

## Bibliothèques sous-jacentes des transports

Chaque transport est un adaptateur mince par-dessus un client amont. Le support est borné par la viabilité du projet amont.

| Transport | Amont | Protocole |
|---|---|---|
| WhatsApp | `go.mau.fi/whatsmeow` | Protocole WhatsApp Web non officiel (compatible Signal). |
| Signal | Sous-processus `signal-cli` | JSON-RPC Signal. |
| Telegram | Client direct Bot API | Long polling. |
| Matrix | Client direct de l'API client-serveur | Polling HTTPS. |
| Slack | Client direct Socket Mode | WebSocket sortant. |
| Discord | Client direct Gateway | WebSocket sortant + intents. |
| iMessage | Client HTTP BlueBubbles | Polling BlueBubbles. Nécessite un hôte macOS exécutant BlueBubbles Server. |
| Email | Client standard `net/smtp` + IMAP | IMAP + SMTP sur TLS. |
| SMS | REST Twilio / Vonage direct | Sortant uniquement. |

## Dépendances runtime optionnelles

| Dépendance | Requise pour | Version |
|---|---|---|
| CLI `claude` | `provider: claudecli` (par défaut). | Dernière. |
| `signal-cli` | Transport Signal. | 0.13+. Nécessite une JVM. |
| BlueBubbles Server | Transport iMessage. | 1.9+. S'exécute sur un hôte macOS. |
| CLI `whisper.cpp` | Transcription des notes vocales WhatsApp (`whatsapp.voice.enabled: true`). | 1.5+. Non livré dans l'image de conteneur. |
| `podman` | Déploiement de référence. | 4.4+ pour le support de Quadlet. |
| `systemd` (session utilisateur) | Déploiement de référence. | 249+ pour Quadlet. |

## Compilateur et chaîne d'outils

| Composant | Version | Notes |
|---|---|---|
| Go | 1.26+ | `go.mod` fige le graphe de modules exactement. |
| golangci-lint | v2 | 18 linters, épinglages exacts dans `.golangci.yml`. |
| govulncheck | Dernière | Exécuté à chaque build CI. |
| cosign | 2.2+ | Uniquement pour vérifier les releases signées. |

## Suite

- [Installation](/fr/getting-started/installation/) — installation adaptée à votre plateforme.
- [Updating](/fr/getting-started/updating/) — passer d'une version à l'autre en toute sécurité.
