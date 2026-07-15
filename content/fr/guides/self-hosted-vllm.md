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
description: "Worked example: point rousseau-agent at a self-hosted vLLM endpoint on your internal network via the OpenAI-compatible provider."
keywords: "vllm, self-hosted, openai-compatible, air-gapped, internal network, local llm"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/guides/self-hosted-vllm/"
subtitle: "Point rousseau at a vLLM endpoint on your internal network."
tags: "guides, vllm, self-hosted, openai-compatible"
title: "Guide : vLLM auto-hébergé"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "vllm, self-hosted, openai-compatible, air-gapped, internal network, local llm"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide : vLLM auto-hébergé"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 32
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/self-hosted-vllm/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/self-hosted-vllm/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guide : vLLM auto-hébergé"
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
twitter_description: "Worked example: point rousseau-agent at a self-hosted vLLM endpoint on your internal network via the OpenAI-compatible provider."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide : vLLM auto-hébergé"
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

## Scénario

Vous disposez d'une instance vLLM servant un modèle de codage à poids ouverts sur une machine interne (`llm.internal:8000`). Aucun trafic d'inférence ne peut sortir du réseau. Pointez rousseau dessus et traitez l'endpoint comme n'importe quelle cible compatible OpenAI.

vLLM implémente le schéma OpenAI Chat Completions, donc le fournisseur `openai` de rousseau fonctionne sans modification. LM Studio, Ollama et Text Generation Inference suivent le même motif.

## Prérequis

- vLLM déjà en fonctionnement sur `http://llm.internal:8000/v1` avec `/v1/chat/completions` répondant à un test de fumée en curl.
- Le tag de modèle avec lequel vous avez lancé vLLM (par ex. `Qwen/Qwen3-Coder-30B`).

## Étape 1 — Confirmer vLLM

```sh
curl -fsS http://llm.internal:8000/v1/models
curl -fsS http://llm.internal:8000/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{
    "model": "Qwen/Qwen3-Coder-30B",
    "messages": [{"role": "user", "content": "say hi"}]
  }' | jq .
```

Les deux doivent retourner sans erreur. Si le second appel renvoie du 4xx, corrigez vLLM d'abord — le client de rousseau est un mince adaptateur JSON qui hérite de sa surface d'erreurs.

## Étape 2 — Câbler rousseau à vLLM

Éditez `~/.config/rousseau/config.yaml` :

```yaml
provider: openai

openai:
  base_url: http://llm.internal:8000/v1
  api_key: not-required        # vLLM ignore la clé mais le client en envoie une
  model: Qwen/Qwen3-Coder-30B
  max_tokens: 4096

log:
  level: info
  format: json
```

Le fournisseur `openai` partage son schéma avec `openrouter` et `ollama` ; la seule différence est le `base_url` préréglé. Définir `base_url` explicitement surcharge la valeur par défaut.

## Étape 3 — Test de fumée dans la TUI

```sh
rousseau chat
```

Tapez `explain the difference between goroutines and threads in two paragraphs.` et envoyez. Si la réponse s'affiche en streaming, le câblage est correct.

Sinon :

```sh
rousseau doctor
```

La ligne `provider.selected` affichera `openai` ; un `fail` sur l'accessibilité de `provider.openai.base_url` signifie que soit le DNS soit le chemin réseau interne est cassé, pas rousseau.

## Étape 4 — Activer l'utilisation des outils

Les modèles de codage varient dans leur fidélité tool-use. La boucle d'agent de rousseau attend que le modèle émette des blocs `tool_use` dont le JSON valide contre le `InputSchema` de l'outil. Si votre modèle vLLM ne supporte pas nativement le schéma tool-use OpenAI :

- Commencez avec `provider: openai` + un modèle qui le supporte (les variantes récentes Qwen, Mistral, Llama 3.1 8B+ l'annoncent).
- Ou enveloppez vLLM dans un adaptateur comme [l'adaptateur tool_choice compatible OpenAI de vLLM](https://docs.vllm.ai/) et vérifiez à nouveau.

Une fois le tool use fonctionnel, les outils de codage (read, write, edit, grep, bash) deviennent disponibles exactement comme avec n'importe quel autre fournisseur.

## Étape 5 — Envisager les politiques d'approbation

Les modèles auto-hébergés tendent à être moins conscients des risques que les modèles frontières. Verrouiller l'outil `bash` avec un approbateur en mode `pattern` est prudent :

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read,  match: ".*"}
      - {tool: grep,  match: ".*"}
      - {tool: edit,  match: "^./workspace/.*"}
      - {tool: bash,  match: "^(ls|cat|grep|rg|find|git status|git diff) "}
    deny:
      - {tool: bash,  match: "rm -rf|sudo|curl|wget|chmod|chown"}
```

Voir [Guides: Audit + Approval Policies](/fr/guides/audit-approval-policies/) pour une présentation plus approfondie.

## Étape 6 — Surveiller la performance

Les endpoints auto-hébergés bénéficient souvent d'un `max_iterations` plus élevé (la boucle d'agent peut nécessiter davantage d'allers-retours pour atteindre la même conclusion), et toujours d'activer la compression de session :

```yaml
agent:
  max_iterations: 48
  compression:
    enabled: true
    trigger_messages: 60
    keep_recent: 8
```

La compression est désactivée par défaut car elle utilise un tour de LLM pour résumer ; sur une API publique tarifée au jeton, cela peut être gaspilleur. Sur un endpoint auto-hébergé, le coût jeton est nul, donc laissez-la active.

## Alternatives à vLLM

La même recette s'applique à :

- **Ollama** — utilisez `provider: ollama` (préréglé `base_url` à `http://localhost:11434/v1` et `api_key` à `not-required`).
- **LM Studio** — utilisez `provider: openai` et pointez `base_url` vers le serveur LM Studio (`http://host:1234/v1`).
- **TGI (Text Generation Inference)** — utilisez `provider: openai` et pointez `base_url` vers l'endpoint de compatibilité OpenAI de TGI.
- **OpenRouter** — utilisez `provider: openrouter` (préréglé `base_url` à `https://openrouter.ai/api/v1`).

## Précautions

- rousseau ne fait pas de streaming quand le fournisseur ne fait pas de streaming. Certains builds vLLM livrent avec le streaming désactivé — activez-le pour une meilleure expérience TUI.
- Le prompt caching (`internal/llm/anthropic` utilise des marqueurs `cache_control`) est spécifique à Anthropic et ne fait rien contre vLLM. Cela compte surtout pour les sessions longues sur des fournisseurs tarifés au jeton.
- La [page du fournisseur compatible OpenAI](/fr/providers/openai-compatible/) est la référence définitive pour chaque paramètre.

## Suite

- [OpenAI-compatible provider](/fr/providers/openai-compatible/) — chaque champ de configuration.
- [Audit + approval policies](/fr/guides/audit-approval-policies/) — posture de sécurité pour les modèles moins alignés.
- [Offline](/fr/offline/) — exécuter rousseau sans internet sortant.
