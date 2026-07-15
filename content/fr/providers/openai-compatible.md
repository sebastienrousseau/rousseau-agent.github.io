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
description: "Configure OpenAI-compatible endpoints: OpenAI, OpenRouter, Ollama, self-hosted vLLM or LM Studio. BaseURL, model naming, streaming, and Ollama's not-required key."
keywords: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, base_url, chat completions, API key, streaming"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/providers/openai-compatible/"
subtitle: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, and any Chat Completions clone."
tags: "providers, openai, openrouter, ollama"
title: "Fournisseur compatible OpenAI"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, base_url, chat completions, API key, streaming"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Fournisseur compatible OpenAI"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 10
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/openai-compatible/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/openai-compatible/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Fournisseur compatible OpenAI"
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
twitter_description: "Configure OpenAI-compatible endpoints: OpenAI, OpenRouter, Ollama, self-hosted vLLM or LM Studio. BaseURL, model naming, streaming, and Ollama's not-required key."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Fournisseur compatible OpenAI"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Ce que vous allez apprendre</span><p>Comment le provider <code>openai</code> de rousseau sert six endpoints différents (OpenAI, OpenRouter, Ollama, vLLM, LM Studio, LiteLLM) via une seule implémentation, la valeur exacte de <code>base_url</code> et <code>model</code> pour chacun, et quels endpoints supportent l'utilisation d'outils. Lisez <code>internal/llm/openai/client.go</code> en parallèle de cette page.</p></aside>

## Une implémentation, plusieurs endpoints

`internal/llm/openai/` parle l'API OpenAI Chat Completions. Parce que `base_url` est configurable, le même code sert chaque endpoint compatible OpenAI : OpenAI lui-même, OpenRouter, together.ai, DeepInfra, vLLM auto-hébergé, le shim OpenAI d'Ollama, LM Studio et LiteLLM.

Le nom de provider est l'un de `openai`, `openrouter` ou `ollama` — chacun correspond à son propre bloc de config avec un `base_url` préréglé (voir `setDefaults` dans `internal/config/config.go`). Utilisez `openai` comme emplacement générique et surchargez `base_url` en pointant vers un backend auto-hébergé.

## Recettes par endpoint

<div class="tabs" data-tabs="openai-compat-endpoints">
  <div class="tab-list" role="tablist" aria-label="OpenAI-compatible endpoint">
    <button role="tab" aria-selected="true">OpenAI</button>
    <button role="tab" aria-selected="false">OpenRouter</button>
    <button role="tab" aria-selected="false">Ollama</button>
    <button role="tab" aria-selected="false">vLLM</button>
    <button role="tab" aria-selected="false">LM Studio</button>
    <button role="tab" aria-selected="false">LiteLLM</button>
  </div>
  <div class="tab-panel" role="tabpanel">

OpenAI direct. `api.openai.com/v1` est le défaut du SDK — aucune surcharge de `base_url` nécessaire.

```yaml
provider: openai

openai:
  api_key: sk-...
  model: gpt-5
  max_tokens: 4096
```

Utilisation d'outils : oui (tableau `tools` natif). Streaming : oui (SSE).

<aside class="admonition" data-type="note"><span class="admonition-title">Nommage des modèles</span><p>Les IDs de modèles suivent le nommage propre d'OpenAI (<code>gpt-4o</code>, <code>gpt-5</code>, <code>o1</code>, <code>o3-mini</code>). Figez les IDs exacts en production — les alias peuvent se déplacer.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

OpenRouter agrège des dizaines de fournisseurs derrière une seule API. Les IDs de modèles suivent la convention `provider/model` :

```yaml
provider: openrouter

openrouter:
  api_key: sk-or-...
  model: anthropic/claude-sonnet-4-6
```

`base_url` vaut par défaut `https://openrouter.ai/api/v1`. L'utilisation d'outils dépend du fournisseur sous-jacent — les modèles Anthropic et OpenAI fonctionnent, la plupart des modèles open-weights non.

<aside class="admonition" data-type="tip"><span class="admonition-title">Modèles free-tier</span><p>OpenRouter expose des variantes free-tier (suffixe <code>:free</code>) pour l'expérimentation. Limites de débit et quotas quotidiens s'appliquent.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Ollama local expose un shim compatible Chat Completions sur `http://localhost:11434/v1` :

```yaml
provider: ollama

ollama:
  model: llama3.1:8b
```

`ollama.api_key` vaut par défaut `not-required` (le shim l'ignore, mais le SDK refuse les chaînes vides — voir `New` dans `internal/llm/openai/client.go`). `ollama.base_url` vaut par défaut `http://localhost:11434/v1`.

Utilisation d'outils : oui à partir d'Ollama 0.4 (via le tableau `tools` dans la requête Chat Completions). Les builds antérieurs retournent du texte simple.

<aside class="admonition" data-type="warning"><span class="admonition-title">Latence</span><p>Ollama CPU-only sur laptop peut prendre des dizaines de secondes par tour. Positionnez le timeout HTTP de votre appelant au-dessus de 60 s, ou utilisez un hôte avec GPU.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

vLLM est le moteur auto-hébergé de production. Démarrez-le avec `--api-key` si vous voulez de l'auth :

```sh
python -m vllm.entrypoints.openai.api_server \
  --model mistralai/Mixtral-8x22B-Instruct-v0.1 \
  --host 0.0.0.0 --port 8000 \
  --api-key sk-vllm-secret
```

```yaml
provider: openai

openai:
  api_key: sk-vllm-secret
  base_url: http://vllm.internal:8000/v1
  model: mistralai/Mixtral-8x22B-Instruct-v0.1
  max_tokens: 4096
```

Utilisation d'outils : oui pour les modèles disposant d'un chat template tool-use (`Hermes-2-Pro`, `Mistral-Nemo`, `Llama-3.1-8B-Instruct` et supérieurs). Streaming : oui. Voir [Guides : vLLM auto-hébergé](/fr/guides/self-hosted-vllm/) pour le déploiement complet.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

LM Studio embarque un serveur compatible OpenAI sur `http://localhost:1234/v1` :

```yaml
provider: openai

openai:
  api_key: not-required
  base_url: http://localhost:1234/v1
  model: lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF
```

Utilisation d'outils : **non** supportée dans les builds actuels (à mi-2026). L'endpoint accepte un tableau `tools` mais l'ignore et retourne du texte simple. À utiliser pour les charges de travail chat-only, ou en attendant l'arrivée de la fonctionnalité.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

LiteLLM est un proxy qui expose plusieurs fournisseurs derrière une seule API. Faites pointer rousseau dessus :

```yaml
provider: openai

openai:
  api_key: sk-litellm-...
  base_url: http://litellm.internal:4000
  model: bedrock/anthropic.claude-sonnet-4-6-20260101-v1:0
```

Note : le port par défaut de LiteLLM est 4000, et son préfixe `/v1` est optionnel selon la manière dont il est déployé. Suivez la doc LiteLLM pour votre version.

Utilisation d'outils : transmise au fournisseur sous-jacent. Streaming : oui. Utile pour les équipes qui veulent un point d'entrée unique pour le trafic LLM (rate limiting, suivi budgétaire, audit).

  </div>
</div>

## Référence de configuration

| Champ | Défaut | Effet |
|---|---|---|
| `api_key` | *requis* | Bearer token. Utilisez `not-required` pour les endpoints locaux qui ignorent l'auth. |
| `model` | *requis* | Identifiant de modèle. Aucun défaut universel entre endpoints. |
| `base_url` | *dépend du nom de provider* | Surcharge l'endpoint. Voir les presets dans `setDefaults`. |
| `max_tokens` | défaut SDK | Plafonne les tokens de sortie par complétion. |

Les noms de provider `openai`, `openrouter` et `ollama` correspondent chacun à leur propre bloc de config (`OpenAIConfig`, `OpenAIConfig`, `OpenAIConfig`) ; ils partagent la même forme mais vous permettent de configurer plusieurs endpoints dans un seul `config.yaml` et de basculer entre eux en changeant `provider:`.

## Streaming

Le provider implémente `agent.StreamingProvider` via SSE. Chaque endpoint ci-dessus supporte le streaming ; le shim d'Ollama requiert un build récent (0.5+).

## Utilisation d'outils

Les définitions d'outils issues du `Registry` sont converties dans le tableau `tools` d'OpenAI via `internal/llm/openai/client.go`. Tous les endpoints compatibles OpenAI ne supportent pas les outils — vérifiez votre backend avant d'activer. Ollama le supporte à partir de 0.4 ; les anciens builds de LM Studio non.

Les politiques d'approbation s'appliquent pour les endpoints qui retournent réellement des `tool_calls`. Les endpoints sans support tool-use retournent du texte simple et le `Registry` n'est pas consulté.

## Points de vigilance

- **Nommage des modèles.** Chaque endpoint a sa propre convention : OpenAI (`gpt-5`), OpenRouter (`anthropic/claude-sonnet-4-6`), Ollama (`llama3.1:8b`), vLLM (le nom HuggingFace). Aucune portabilité inter-endpoints.
- **Clé API vide.** Le SDK refuse les chaînes vides ; passez `not-required` (ou un placeholder) pour les endpoints locaux sans auth.
- **Slash final dans BaseURL.** Incluez le segment `/v1`. N'incluez pas de slash final.
- **Timeouts.** Ollama local sur CPU peut prendre des dizaines de secondes par tour — augmentez le timeout de votre client HTTP si vous encapsulez le provider. `rousseau` utilise le défaut du SDK.
- **Variance de tool-use.** OpenAI et Anthropic-derrière-OpenRouter supportent les outils de manière fiable. Ollama nécessite un build récent et un modèle avec un chat template tool-use. LM Studio ne supporte pas les outils. Si des tool_calls arrivent sous forme de texte simple, le `Registry` n'est pas consulté.
- **Modèles de raisonnement.** Les séries OpenAI o1/o3 se comportent différemment : `max_tokens` est remplacé par `max_completion_tokens` et les system prompts sont limités. Le SDK gère cela, mais attendez-vous à une latence par tour plus élevée.

## Dépannage

### `openai: complete: 401 Unauthorized`

Clé API absente ou incorrecte. Pour OpenRouter, utilisez le jeton `sk-or-…`. Pour les endpoints locaux, assurez-vous que `api_key` est non vide même si l'endpoint l'ignore.

### `openai: complete: 404 model not found`

La chaîne `model` ne correspond à rien de reconnu par l'endpoint. Pour OpenRouter, incluez le préfixe de fournisseur (`anthropic/claude-sonnet-4-6`, pas `claude-sonnet-4-6`). Pour Ollama, assurez-vous que le modèle est pullé (`ollama pull llama3.1:8b`).

### Le modèle ignore mes `tools`

L'endpoint ne supporte pas les outils pour ce modèle. Vérifiez en pointant vers le même modèle via un endpoint connu comme fonctionnel (OpenAI, Anthropic direct, OpenRouter avec un modèle Anthropic). Voir la colonne tool-use dans les recettes ci-dessus.

### `context deadline exceeded` sur Ollama local

L'inférence CPU est lente. Options : (1) augmentez le timeout côté appelant, (2) faites tourner Ollama sur un hôte GPU, (3) basculez sur un modèle plus petit (`llama3.1:8b` vs `70b`).

### Le streaming s'arrête au milieu d'une réponse

Certains proxies (LiteLLM, proxies egress d'entreprise) bufferisent SSE. Configurez le proxy pour désactiver la bufferisation pour `text/event-stream`, ou faites tourner rousseau sur le même segment réseau que l'endpoint.

## Pages liées

- [Guides : vLLM auto-hébergé](/fr/guides/self-hosted-vllm/) — déploiement de production.
- [Fournisseurs : Anthropic](/fr/providers/anthropic/) — l'alternative API directe pour Claude.
- [Guides : Multi-fournisseur](/fr/guides/multi-provider/) — plusieurs fournisseurs par transport.
- [Guides : Limites de débit](/fr/guides/rate-limits/) — playbook de retry fournisseur par fournisseur.
- [Configuration](/fr/configuration/) — les sections `openai`/`openrouter`/`ollama` en contexte.

## Pour aller plus loin

- `internal/llm/openai/client.go` — `Complete`, conversion de messages, schéma d'outils.
- `internal/llm/openai/client.go` — implémentation du streaming.
- `internal/config/config.go` — struct `OpenAIConfig`, `setDefaults` pour les presets de `base_url`.
