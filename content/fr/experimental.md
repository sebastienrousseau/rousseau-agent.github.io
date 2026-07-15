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
description: "Off-by-default rousseau-agent behaviour: voice mode via whisper.cpp, FTS5 recall, LLM compression, and other opt-in surface."
keywords: "experimental, voice, whisper, fts5, compression, opt-in, feature flag"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/experimental/"
subtitle: "Comportements désactivés par défaut, et pourquoi."
tags: "experimental, opt-in, voice, compression, fts5"
title: "Expérimental"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "experimental, voice, whisper, fts5, compression, opt-in, feature flag"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Expérimental"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "system"
order: 60
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/experimental/index.html"
item_link: "https://docs.rousseau-agent.dev/experimental/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Expérimental"
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
twitter_description: "Off-by-default rousseau-agent behaviour: voice mode via whisper.cpp, FTS5 recall, LLM compression, and other opt-in surface."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Expérimental"
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

## Ce que signifie « expérimental » ici

La posture par défaut de rousseau est minimale : un unique binaire Go statique, un fichier SQLite, aucune dépendance externe. Toute fonctionnalité qui nécessite un runtime supplémentaire (`whisper.cpp`), un état supplémentaire (index FTS5 pour le recall) ou un coût fournisseur supplémentaire (compression pilotée par LLM) est opt-in.

Aucune n'est instable. Elles sont livrées, testées et supportées. Mais parce qu'elles modifient le coût opérationnel ou la surface, elles sont désactivées par défaut — vous activez celles dont vous avez besoin.

## Mode voix (whisper.cpp)

Désactivé par défaut car il exige que le binaire `whisper` de whisper.cpp soit installé sur l'hôte du démon.

**Activation :** `whatsapp.voice.enabled: true` dans `config.yaml`. Voir `VoiceConfig` dans `internal/config/config.go`.

**Ce qu'il fait.** Quand WhatsApp livre une note vocale, le client whatsmeow télécharge la charge utile OGG, invoque `whisper` avec le modèle configuré et traite la transcription comme le texte du message entrant. Événements de log structurés (`internal/transport/whatsapp/dispatch.go`) :

- `whatsapp.audio_downloaded size=N`
- `whatsapp.transcribed elapsed=N`

**Pourquoi désactivé.** Deux raisons : (1) une installation neuve échouerait de manière confuse quand le binaire `whisper` est manquant, (2) la transcription est une dépense CPU en temps réel que la plupart des opérateurs préfèrent activer volontairement plutôt que de la subir par surprise.

Voir [User Guide: Voice mode](/fr/user-guide/voice-mode/) pour la configuration complète.

## Recall FTS5

**Activation.** Activé par défaut, mais utilisé uniquement par les outils qui le demandent. L'index FTS5 est construit et maintenu en toutes circonstances (`EnsureSearch` dans `internal/state/sqlite/search.go`) ; le « opt-in » consiste à décider si l'agent demande au modèle de l'interroger.

**Ce qu'il fait.** Index plein texte SQLite FTS5 sur chaque session stockée. Alimenté par `rousseau session search`, l'outil MCP `rousseau_search_sessions`, et (quand l'agent est configuré avec un recall searcher) le modèle peut l'interroger en cours de tour.

**Pourquoi structuré ainsi.** L'index est peu coûteux à maintenir — les triggers dans `internal/state/sqlite/search.go` s'en occupent — mais l'exposer au modèle à chaque tour a un coût. Il n'est câblé que lorsque la boucle d'agent est construite avec un `RecallSearcher` (`internal/state/sqlite/recall.go`).

Voir [User Guide: Compression + Recall](/fr/user-guide/compression-recall/).

## Compression pilotée par LLM

Désactivée par défaut car elle consomme des jetons.

**Activation :** `agent.compression.enabled: true`. Liste complète des champs sur [Guide: Context management](/fr/guides/context-management/).

**Ce qu'il fait.** Quand une session dépasse `trigger_messages` (60 par défaut), le `LLMCompressor` (`internal/agent/compressor.go`) résume la tranche la plus ancienne en un message utilisateur synthétique unique, en préservant tels quels les `keep_recent` messages les plus récents. Chaque tour suivant est plus petit et moins coûteux.

**Pourquoi désactivé.** Le déploiement de référence exécute `claudecli` sur un palier d'abonnement où le comptage de jetons n'est pas facturé. La compression se rentabilise sur Anthropic direct, Bedrock, Vertex et les fournisseurs compatibles OpenAI.

## URLs de base OpenRouter et Ollama (préconfigurées, mais opt-in)

Pas strictement expérimentales, mais à nommer : les `setDefaults` de rousseau dans `internal/config/config.go` préconfigurent les URLs de base d'OpenRouter et d'Ollama :

- `openrouter.base_url: https://openrouter.ai/api/v1`
- `ollama.base_url: http://localhost:11434/v1`
- `ollama.api_key: not-required`

Sélectionner ces fournisseurs est opt-in via `provider: openrouter` / `provider: ollama` — les endpoints sont simplement pré-remplis pour que vous n'ayez pas à les mémoriser.

## Détection d'injection de prompt (feuille de route)

Non livrée. Voir [Guides: Prompt injection](/fr/guides/prompt-injection/) pour le modèle de menace honnête. La mitigation actuelle repose entièrement sur les approbateurs ; la détection par classifieur est un élément de la feuille de route en attente d'une recherche qui fonctionne réellement.

## Streaming vers les fournisseurs non-Anthropic (partiel)

Le fournisseur Anthropic (`internal/llm/anthropic/client.go`) supporte l'interface de streaming du SDK. Les autres adaptateurs fonctionnent actuellement en mode non-streaming. Le streaming sur chaque adaptateur est une passe d'uniformisation planifiée.

## Voir aussi

- [Configuration](/fr/configuration/) — chaque paramètre de configuration.
- [User Guide: Voice mode](/fr/user-guide/voice-mode/).
- [Guides: Context management](/fr/guides/context-management/) — plongée dans la compression.
- [Reference: Session store](/fr/reference/session-store/) — schéma FTS5.
