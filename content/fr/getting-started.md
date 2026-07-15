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
description: "Install rousseau-agent from source, go install, or a cosign-verified release. Run rousseau chat and configure the first chat transport."
keywords: "install, quickstart, rousseau chat, cosign verify, go install, systemd, podman"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/getting-started/"
subtitle: "Installer rousseau-agent et atteindre votre premier transport."
tags: "install, quickstart, getting-started"
title: "Prise en main"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "install, quickstart, rousseau chat, cosign verify, go install, systemd, podman"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Prise en main"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 2
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Prise en main"
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
twitter_description: "Install rousseau-agent from source, go install, or a cosign-verified release. Run rousseau chat and configure the first chat transport."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Prise en main"
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

## À qui s'adresse ce document

- **Développeurs individuels** qui souhaitent un assistant de codage exécuté sur leur propre machine et pilotant leur CLI `claude` existante. Aucune clé API n'est routée par la config de rousseau, aucun courtier cloud au milieu.
- **Opérateurs de plateforme** exploitant un agent de codage partagé pour une équipe derrière un périmètre d'entreprise. Rousseau est un binaire Go statique unique dans un conteneur Podman rootless avec capacités abandonnées — déployable à côté de tout autre service systemd.
- **Réviseurs sécurité** évaluant un agent avant déploiement. Provenance SLSA-3, sommes de contrôle de release signées par cosign, SBOM CycloneDX, builds reproductibles et chaque frontière de confiance sont documentés dans [Sécurité](/fr/security/).

## La voie la plus rapide

1. **Si vous avez déjà la CLI `claude` installée et authentifiée,** le démarrage le plus rapide est `rousseau chat` avec le provider `claudecli` par défaut — l'auth est héritée, aucune clé à router. Continuez avec [Première exécution](#first-run) ci-dessous.
2. **Si vous voulez une voie API directe avec votre propre clé,** définissez `ANTHROPIC_API_KEY` et basculez `provider: anthropic` dans `~/.config/rousseau/config.yaml`. Voir [Provider Anthropic](/fr/providers/anthropic/).
3. **Si vous êtes en entreprise avec AWS Bedrock ou Google Vertex,** choisissez le provider correspondant — [Bedrock](/fr/providers/bedrock/) utilise la chaîne d'identifiants AWS standard ; [Vertex](/fr/providers/vertex/) lit un JSON de compte de service. Aucun secret ne réside dans le fichier de config rousseau.
4. **Si vous êtes en air-gap ou souhaitez une inférence entièrement auto-hébergée,** pointez rousseau vers un endpoint compatible OpenAI — Ollama, vLLM, LM Studio, ou tout shim. Voir [Provider compatible OpenAI](/fr/providers/openai-compatible/).

## Ce que vous aurez à la fin

- Un binaire `rousseau` dans `$PATH` vérifié contre une signature cosign (voie release) ou construit depuis les sources (`make check` exécute les mêmes portes que la CI : 18 linters + race + govulncheck).
- Une TUI `rousseau chat` fonctionnelle, adossée au provider que vous avez choisi.
- Un magasin de sessions SQLite à `~/.local/share/rousseau/sessions.db` — chaque tour est persisté, rappel inter-sessions disponible via FTS5.
- Optionnellement : un transport de chat en direct (WhatsApp, Slack, Signal, ...) joignable depuis votre téléphone.

## Vous préférez regarder ?

Un court screencast de ce flux est prévu dans la feuille de route. En attendant, la cérémonie entière tient sur cette page — la plupart des opérateurs terminent en moins de dix minutes.

## Configuration requise

| Prérequis | Version | Notes |
|---|---|---|
| Chaîne d'outils Go | 1.26+ | `CGO_ENABLED=0` ; le binaire est entièrement statique. |
| Runtime de conteneur | Podman 4.4+ | Le déploiement de référence utilise Podman rootless + une unité Quadlet systemd. Docker fonctionne mais Quadlet est spécifique à Podman. |
| CLI `claude` | dernière | Uniquement si vous utilisez le provider `claudecli` par défaut. |
| `signal-cli` | 0.13+ | Uniquement si vous utilisez le transport Signal. |
| Serveur BlueBubbles | 1.9+ | Uniquement si vous utilisez le transport iMessage (hôte macOS requis). |
| `whisper.cpp` | 1.5+ | Uniquement si vous activez la transcription des notes vocales WhatsApp. |

## Installer

### Depuis les sources

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # produces ./bin/rousseau
./bin/rousseau version
```

`make check` exécute vet, `golangci-lint`, `go test -race` et `govulncheck` — les mêmes portes que celles imposées par la CI.

### Via `go install`

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

Le binaire embarque `modernc.org/sqlite`, donc aucune dépendance libc ou CGo à l'exécution.

### Depuis une release signée

Chaque release taguée publie une archive avec somme de contrôle, un SBOM CycloneDX, une attestation de provenance SLSA-3 et une signature cosign du fichier de sommes de contrôle. Vérifiez toujours avant d'exécuter :

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_<version>_checksums.txt.sig \
  rousseau_<version>_checksums.txt

sha256sum -c rousseau_<version>_checksums.txt
```

La regex certificate-identity est ce qui fixe l'identité du signataire ; ne l'affaiblissez pas.

## Première exécution

### Chat en terminal

```sh
rousseau chat
```

TUI Bubble Tea. Entrée pour envoyer, `Ctrl+C` pour quitter. Le provider par défaut est `claudecli`, qui hérite de l'authentification de votre installation locale de Claude Code ; aucune clé API n'est routée par la config de rousseau.

L'historique de session est persisté dans `~/.local/share/rousseau/sessions.db` (SQLite avec journalisation WAL et FTS5 pour le rappel inter-sessions).

### Premier transport de chat

WhatsApp est le transport de référence (l'UX d'appairage est la plus stricte). Appairez au premier lancement en scannant le QR depuis votre téléphone :

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

Le JID E.164 (`<digits>@s.whatsapp.net`) restreint le traitement entrant ; tout autre expéditeur est silencieusement rejeté. L'état d'appairage est stocké dans `whatsapp.db` à côté du magasin de sessions.

Les autres transports suivent la même forme :

```sh
rousseau slack   --app-token xapp-... --bot-token xoxb-...
rousseau discord --token bot-token
rousseau telegram --token 12345:ABC
rousseau matrix  --homeserver-url https://matrix.org --access-token ... --user-id @bot:matrix.org
```

Chaque `rousseau <transport> --help` liste ses flags. Les valeurs par défaut proviennent de `~/.config/rousseau/config.yaml`.

## Où l'état est stocké

| Chemin | Objectif |
|---|---|
| `~/.config/rousseau/config.yaml` | Fichier de configuration au niveau utilisateur (Viper). |
| `~/.local/share/rousseau/sessions.db` | Sessions, tâches cron, mapping JID, index de rappel FTS5. |
| `~/.local/share/rousseau/whatsapp.db` | Identifiants d'appareil Whatsmeow (séparés pour qu'un ré-appairage d'appareil ne touche pas aux conversations). |
| `~/.claude/` | Tokens OAuth de la CLI `claude`, uniquement lors de l'utilisation du provider `claudecli`. |

## Étapes suivantes

- [Concepts](/fr/concepts/) — la boucle de l'agent, magasin de sessions, MCP, cron, skills.
- [Configuration](/fr/configuration/) — chaque bouton.
- [Déploiement](/fr/deployment/) — comment exécuter le daemon sous systemd.
