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
description: "Configure the direct Anthropic provider: ANTHROPIC_API_KEY, model IDs, max_tokens, prompt cache markers on the last messages, streaming."
keywords: "Anthropic, ANTHROPIC_API_KEY, Claude API, prompt caching, cache_control, ephemeral, streaming"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/providers/anthropic/"
subtitle: "Direct Anthropic API with ephemeral prompt-cache markers."
tags: "providers, anthropic"
title: "Fournisseur Anthropic"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Anthropic, ANTHROPIC_API_KEY, Claude API, prompt caching, cache_control, ephemeral, streaming"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Fournisseur Anthropic"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 7
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/anthropic/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/anthropic/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Fournisseur Anthropic"
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
twitter_description: "Configure the direct Anthropic provider: ANTHROPIC_API_KEY, model IDs, max_tokens, prompt cache markers on the last messages, streaming."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Fournisseur Anthropic"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Ce que vous allez apprendre</span><p>La forme exacte au niveau wire des requêtes Anthropic émises par rousseau, quels blocs de contenu reçoivent des marqueurs de cache de prompt et pourquoi, comment le streaming s'aligne sur <code>agent.StreamingProvider</code>, et les modes d'échec pour les réponses 401/429/529. Lisez <code>internal/llm/anthropic/client.go</code> et <code>internal/llm/anthropic/cache.go</code> en parallèle de cette page.</p></aside>

## Quand utiliser le provider Anthropic

Le provider `anthropic` direct est le bon choix quand :

- Vous avez une clé API Anthropic et voulez une facturation au token sur `api.anthropic.com`.
- Vous voulez l'exécution d'outils côté rousseau (le `Registry` est pleinement en jeu).
- Vous voulez opter pour les marqueurs de cache de prompt éphémère sur les préfixes stables.
- Vous voulez des complétions en streaming dans `rousseau chat` (mise à jour du viewport token par token).
- Vous voulez des limites de débit explicites, publiées (contrairement au mode d'abonnement `claudecli`).

## Configuration

```yaml
provider: anthropic

anthropic:
  api_key: sk-ant-...
  model: claude-sonnet-4-6
  max_tokens: 4096
```

| Champ | Défaut | Effet |
|---|---|---|
| `api_key` | *depuis `ANTHROPIC_API_KEY`* | Bearer pour `api.anthropic.com`. Rejeté si vide lorsque le provider est sélectionné. |
| `model` | `claude-sonnet-4-6` | Identifiant de modèle. |
| `max_tokens` | `4096` | Plafonne les tokens de sortie par complétion. |

La variable d'environnement `ANTHROPIC_API_KEY` est liée à `anthropic.api_key` au chargement, donc l'exporter équivaut à la configurer. Les opérateurs de conteneur l'exportent typiquement dans la ligne `Environment=` de l'unité systemd plutôt que dans `config.yaml`.

## Identifiants de modèles

`rousseau-agent` transmet `model` tel quel au SDK. Figez l'ID de modèle exact (`claude-sonnet-4-6`, `claude-opus-4-6`) en production pour que votre trafic ne change pas quand Anthropic promeut de nouveaux snapshots.

## Internes du cache de prompt

Le cache de prompt éphémère d'Anthropic permet de marquer les blocs de contenu par `cache_control: { type: "ephemeral" }`. L'API met en cache le préfixe jusqu'au bloc marqué inclus ; les tours suivants qui portent le même préfixe paient une fraction du coût habituel en tokens d'entrée (10 % à l'heure de rédaction — vérifiez la doc Anthropic pour les tarifs en vigueur).

Rousseau applique les marqueurs via `applyCacheMarkers` dans `internal/llm/anthropic/cache.go`. Deux choses se produisent quand `CacheableMessages > 0` dans la `Request` sortante :

1. **Le system prompt reçoit `cache_control: ephemeral`.** Il survit à chaque tour, donc il vaut toujours la peine de le mettre en cache dès qu'on active la fonctionnalité. Voir lignes 68–75 de `internal/llm/anthropic/client.go`.
2. **Les `CacheableMessages` derniers messages** reçoivent `cache_control: ephemeral` sur leur dernier bloc texte. Cela maintient une session en croissance peu coûteuse : à mesure que de nouveaux tours sont ajoutés, le marqueur descend dans le transcript, mais le préfixe jusqu'au marqueur précédent reste chaud.

### Quels blocs sont marqués

`markLastTextBlock` parcourt le contenu d'un `MessageParam` à l'envers et positionne `CacheControl` sur le premier bloc texte rencontré. Les blocs `tool_use` et `tool_result` sont ignorés — le SDK les modélise comme des variantes distinctes avec leurs propres champs `CacheControl` optionnels, et le texte est le dénominateur commun sûr. Voir `internal/llm/anthropic/cache.go`.

### Quand cela devient rentable

<aside class="admonition" data-type="note"><span class="admonition-title">Économie du cache</span><p>Le seuil de rentabilité dépend de la fréquence de réutilisation du préfixe caché. Pour un transport de chat qui exécute 20 à 100 tours par session avec un system prompt de 5 à 10 kB (typique avec des skills chargés), activer le cache divise généralement par deux la facture en tokens d'entrée. Pour un job cron one-shot qui génère une seule réponse, cela n'économise rien.</p></aside>

Le `Compressor` positionne `CacheableMessages = len(recentMessages) - 1` après une réécriture pour que le bloc de résumé neuf soit chaud dès le tour suivant. Les autres chemins de code laissent `CacheableMessages = 0`, ce qui signifie que le cache est opt-in par requête. Les intégrateurs devraient le positionner explicitement lorsqu'ils appellent le provider directement.

### Vérifier les hits de cache

L'API Anthropic retourne `usage.cache_read_input_tokens` et `usage.cache_creation_input_tokens` à chaque réponse. `agent.Usage` n'expose actuellement que `InputTokens` et `OutputTokens`, donc vérifier la répartition impose soit d'activer le logging debug, soit de lire la réponse SDK brute — c'est un manque d'observabilité connu, suivi dans `docs/GAP_ANALYSIS_2026.md`.

## Sémantique du streaming

Le provider implémente `agent.StreamingProvider`. `rousseau chat` utilise le streaming par défaut pour que les tokens s'affichent dans le viewport TUI au fil de leur arrivée. Les transports de chat (WhatsApp, Slack, Discord, …) utilisent des complétions non-streaming car les transports orientés messages regroupent la livraison de toute façon — un flux de deltas intermédiaire serait juste jeté avant l'envoi du message final.

L'implémentation streaming dans `internal/llm/anthropic/stream.go` consomme l'union `MessageStreamEvent` du SDK :

| Événement | Traitement |
|---|---|
| `message_start` | Émet `agent.StreamEvent{Kind: StreamMessageStart}`. |
| `content_block_start` | Émet `agent.StreamEvent{Kind: StreamContentStart}` avec le type de bloc. |
| `content_block_delta` | Émet `agent.StreamEvent{Kind: StreamTextDelta, Text: delta.Text}` pour le texte ; les événements `input_json_delta` s'accumulent dans une entrée de tool-use partielle. |
| `content_block_stop` | Émet `agent.StreamEvent{Kind: StreamContentStop}`. |
| `message_delta` | Porte la raison d'arrêt finale et l'usage cumulatif. |
| `message_stop` | Fin de flux. |

Le TUI Bubble Tea souscrit à ces événements via `agent.StreamTurn`, qui orchestre la boucle stream/tool-use. Voir `internal/agent/stream_turn.go`.

## Utilisation d'outils

Les définitions d'outils issues du `Registry` sont converties dans le tableau `tools` d'Anthropic via `toSDKTools`. Les politiques d'approbation (`agent.approver`) s'appliquent — chaque bloc `tool_use` passe par `Approver.Approve` dans la boucle d'agent avant exécution. Les refus reviennent au modèle sous forme de blocs `tool_result` avec `is_error: true`, ce qui permet au modèle de s'adapter (choisir une autre action, demander à l'utilisateur, abandonner proprement).

<aside class="admonition" data-type="warning"><span class="admonition-title">Forme du schéma</span><p>Le SDK attend que l'<code>input_schema</code> de l'outil soit un objet JSON Schema avec un champ <code>properties</code> au premier niveau. La <code>tools.Definition</code> de rousseau correspond 1:1 — voir <code>toSDKTools</code> dans <code>internal/llm/anthropic/client.go</code>. Les outils personnalisés émettant des schémas non-objet échoueront au moment de la requête.</p></aside>

## Gestion des limites de débit

L'API Anthropic retourne :

| Code | Signification | Comportement de rousseau |
|---|---|---|
| 401 | Clé absente ou invalide | Échec immédiat, sans retry. |
| 400 | Mauvaise requête (schéma, encodage, prompt trop long) | Échec immédiat avec le message d'erreur du SDK. |
| 429 | Limite de débit par minute dépassée | Remonte comme erreur `agent`. `Complete` ne retente pas. |
| 529 | Surchargé (capacité transitoire) | Remonte comme erreur `agent`. `Complete` ne retente pas. |
| 5xx | Erreur serveur | Remonte comme erreur `agent`. `Complete` ne retente pas. |

**Les retries sont à la charge de l'appelant.** Le TUI `rousseau chat` et le `RouterHandler` de transport n'implémentent pas de backoff actuellement — un 429 tue le tour. C'est un choix de conception délibéré : les retries interagissent avec la sémantique tool_use (appels d'outils partiels, idempotence), et l'appelant a le contexte pour prendre la bonne décision. Voir `docs/GAP_ANALYSIS_2026.md` pour l'assistant de retry prévu.

<aside class="admonition" data-type="tip"><span class="admonition-title">Gérer les 429 dans un transport de chat</span><p>Enveloppez le <code>RouterHandler</code> de transport dans une boucle de retry côté appelant avec backoff exponentiel et jitter. Le <a href="/fr/guides/rate-limits/">guide des limites de débit</a> présente un exemple travaillé.</p></aside>

## Hygiène de coût

- **Réglez `max_tokens` bas** (2048–4096) pour les transports de chat où les réponses dépassent rarement quelques paragraphes. `max_tokens` est un plafond, pas une cible — vous ne payez que pour la sortie réellement générée.
- **Activez `agent.compression`** pour condenser les anciens messages une fois que le transcript dépasse `trigger_messages` (60 par défaut). Le résumé est bien moins coûteux que le transcript brut.
- **Utilisez `CacheableMessages > 0`** quand vous embarquez la bibliothèque agent — c'est sur l'API directe que le cache de prompt paie le plus.
- **Préférez Sonnet pour les boucles tool-use.** Opus est plus cher et plus lent ; à moins d'avoir mesuré des gains sur votre tâche, Sonnet est le défaut pour une raison.
- **Attention à la facturation lors d'un abandon de stream.** Si un flux est annulé en cours de réponse, l'API facture toujours les tokens générés jusqu'au point d'annulation. Positionnez un plafond de timeout côté appelant.

## Dépannage

### `anthropic: complete: 401 unauthorized`

Votre `ANTHROPIC_API_KEY` est absente, révoquée ou attachée à un workspace/organisation auquel vous n'avez plus accès. Vérifiez avec `curl -H "x-api-key: $ANTHROPIC_API_KEY" https://api.anthropic.com/v1/messages`.

### `anthropic: complete: 400 messages: too many messages`

Le transcript a dépassé la fenêtre de contexte. Activez `agent.compression.enabled: true` (les défauts conviennent généralement) et rejouez. Si la compression est active et se déclenche quand même, baissez `trigger_messages` ou augmentez `keep_recent` pour que le compresseur se déclenche plus tôt.

### `anthropic: unsupported content block <type>`

Le SDK a retourné un type de bloc de contenu que rousseau ne modélise pas — seuls `text` et `tool_use` sont actuellement supportés (voir `fromSDKResponse`). Cela peut arriver si le modèle émet des blocs `thinking` (mode extended thinking). rousseau ne les remonte pas encore ; désactivez extended thinking dans votre config provider en attendant.

### 429 sous charge soutenue

Vous atteignez la limite de débit par minute en tokens de sortie. Options : (1) demandez un relèvement de limite à Anthropic, (2) mettez les tours en file côté appelant et traitez-les en série, (3) basculez vers Bedrock ou Vertex où les quotas entreprise sont généralement plus élevés.

### Cache miss malgré `CacheableMessages > 0`

Anthropic invalide le cache quand le préfixe change. Causes fréquentes : le system prompt est régénéré à chaque tour (skills qui varient à chaque message utilisateur), l'ID de modèle a changé, ou `MaxTokens` diffère. Loguez la payload de requête et comparez-la sur deux tours pour isoler.

## Pages liées

- [Fournisseurs : claudecli](/fr/providers/claudecli/) — arbitrages sous-processus vs API directe.
- [Fournisseurs : Bedrock](/fr/providers/bedrock/) — Claude géré par AWS avec des quotas entreprise.
- [Guides : Limites de débit](/fr/guides/rate-limits/) — le playbook retry + backoff.
- [Boucle d'agent](/fr/agent-loop/) — comment se composent streaming et tool use.
- [Guide utilisateur : Compression &amp; Rappel](/fr/user-guide/compression-recall/) — le mécanisme qui garde les tokens d'entrée sous contrôle.

## Pour aller plus loin

- `internal/llm/anthropic/client.go` — `Complete`, conversion de messages, schéma d'outils.
- `internal/llm/anthropic/stream.go` — implémentation du streaming.
- `internal/llm/anthropic/cache.go` — helper de marqueur de cache.
- `internal/agent/stream_turn.go` — comment la boucle d'agent consomme les événements de streaming.
- `internal/agent/compressor.go` — comment le compresseur amorce `CacheableMessages`.
