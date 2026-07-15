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
description: "Overview of the five LLM provider families supported by rousseau-agent: claudecli, Anthropic, AWS Bedrock, Google Vertex AI, and any OpenAI-compatible endpoint."
keywords: "providers, LLM, Anthropic, Bedrock, Vertex, OpenAI, OpenRouter, Ollama, claudecli"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/providers/"
subtitle: "Cinq familles de fournisseurs LLM derrière une seule interface Provider."
tags: "providers, LLM"
title: "Fournisseurs"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "providers, LLM, Anthropic, Bedrock, Vertex, OpenAI, OpenRouter, Ollama, claudecli"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Fournisseurs"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 5
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Fournisseurs"
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
twitter_description: "Overview of the five LLM provider families supported by rousseau-agent: claudecli, Anthropic, AWS Bedrock, Google Vertex AI, and any OpenAI-compatible endpoint."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Fournisseurs"
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

## L'interface Provider

Chaque backend LLM implémente `agent.Provider` :

```go
type Provider interface {
    Name() string
    Complete(ctx context.Context, req Request) (Response, error)
}
```

Une variante `StreamingProvider` ajoute `CompleteStream` pour la livraison jeton par jeton. Ajouter un sixième backend équivaut à une seule implémentation de `Complete` plus le câblage dans `internal/cli/provider.go`.

## Familles supportées

| Fournisseur | Modèle d'auth | Endpoint | Streaming | Cache de prompt | Recommandé pour |
|---|---|---|:---:|:---:|---|
| [claudecli](/fr/providers/claudecli/) | Hérite de l'auth de la CLI `claude` | Sous-processus local | Oui | via sous-processus | Opérateurs individuels, abonnement Claude Code |
| [Anthropic](/fr/providers/anthropic/) | `ANTHROPIC_API_KEY` | `api.anthropic.com` | Oui | marqueurs éphémères | Équipes sur l'API Anthropic |
| [AWS Bedrock](/fr/providers/bedrock/) | Chaîne d'identifiants AWS | `bedrock-runtime.<region>.amazonaws.com` | Oui | via SDK | Entreprises sur AWS |
| [Google Vertex AI](/fr/providers/vertex/) | Compte de service ou ADC | `<region>-aiplatform.googleapis.com` | Oui | via SDK | Entreprises sur GCP |
| [Compatible OpenAI](/fr/providers/openai-compatible/) | Bearer token | `api.openai.com` ou surcharge | Oui | dépend du fournisseur | OpenAI, OpenRouter, Ollama, vLLM, LM Studio |

## Choisir un fournisseur

Définissez la clé `provider` en tête de `~/.config/rousseau/config.yaml` :

```yaml
provider: anthropic

anthropic:
  api_key: sk-ant-...
  model: claude-sonnet-4-6
```

Ou surchargez depuis le shell :

```sh
ROUSSEAU_PROVIDER=bedrock rousseau chat
```

`ANTHROPIC_API_KEY` est lié à `anthropic.api_key` au chargement, donc passer cette variable d'environnement est équivalent.

## Où chaque fournisseur fait du tool-use

Le fournisseur `claudecli` exécute sa propre boucle tool-use à l'intérieur du sous-processus `claude`. Les outils enregistrés dans le `Registry` de rousseau **ne sont pas** invoqués pour ce fournisseur ; la `Response` est toujours un unique message texte de fin de tour avec la réponse finale de claude.

Chaque autre fournisseur (`anthropic`, `bedrock`, `vertex`, `openai`) utilise le `Registry` de rousseau. Les définitions d'outils sont converties dans la forme JSON attendue par le fournisseur par chaque package fournisseur.
