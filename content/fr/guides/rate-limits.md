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
description: "How rousseau-agent handles provider rate limits: 429s, exponential backoff, prompt-cache markers, and per-provider cost notes."
keywords: "rate limits, 429, backoff, retry, prompt cache, anthropic, bedrock, cost"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/guides/rate-limits/"
subtitle: "429 handling, backoff, and cache-marker optimisation."
tags: "guides, rate limits, prompt cache, anthropic"
title: "Guide : limites de débit"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "rate limits, 429, backoff, retry, prompt cache, anthropic, bedrock, cost"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide : limites de débit"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 36
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/rate-limits/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/rate-limits/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guide : limites de débit"
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
twitter_description: "How rousseau-agent handles provider rate limits: 429s, exponential backoff, prompt-cache markers, and per-provider cost notes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide : limites de débit"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Ce que vous allez apprendre</span><p>Limites de débit fournisseur par fournisseur, coût par jeton, sémantique de retry, économie du cache et une recette de retry-avec-backoff côté appelant. Consultez la page de tarification de chaque fournisseur pour des chiffres faisant autorité — le tableau ci-dessous est un instantané.</p></aside>

## Où se produit le rate limiting

Rousseau n'implémente pas sa propre gestion des limites de débit. Chaque client de fournisseur délègue au SDK amont :

- **Anthropic direct** — `anthropic-sdk-go` gère les retries HTTP, respecte `Retry-After`, applique un backoff exponentiel sur 5xx et 429. Voir `internal/llm/anthropic/client.go`.
- **Bedrock** — `aws-sdk-go-v2` gère les erreurs de throttling avec des retries adaptatifs.
- **Vertex** — les bibliothèques d'authentification Google gèrent leurs propres retries.
- **OpenAI / OpenRouter / Ollama** — le client Go compatible OpenAI gère les 429.
- **claudecli** — le propre binaire `claude` de Claude Code gère les limites. Rousseau ne fait qu'exécuter le sous-processus.

Les requêtes en échec remontent comme événements slog `turn.failed`, `whatsapp.handler_failed` ou `cron.run_failed`. Le texte du message inclura la chaîne d'erreur du fournisseur (typiquement `429 Too Many Requests` avec un backoff suggéré).

## Quand vous atteignez vraiment une limite

Symptômes dans les logs :

```jsonl
{"level":"ERROR","msg":"whatsapp.handler_failed","err":"anthropic: complete: 429 Too Many Requests"}
```

Parce que rousseau considère un tour comme échoué sur les erreurs irrécupérables, l'opérateur voit l'échec dans la réponse du transport — le démon ne l'avale pas silencieusement. C'est intentionnel.

## Réduire la pression du rate-limiting

Trois leviers, par ordre d'impact :

### 1. Marqueurs de prompt cache (Anthropic direct)

`applyCacheMarkers` dans `internal/llm/anthropic/client.go` marque une fenêtre de tête de messages pour le cache éphémère de prompt Anthropic. Quand `CacheableMessages > 0`, le prompt système est également cache-marqué. Les jetons d'entrée en cache sont facturés à environ 10 % des tarifs d'entrée standard et les hits de cache ne consomment pas le budget standard de limite de débit d'entrée.

L'agent (`internal/agent/agent.go`) opte pour cela sur les sessions multi-tours. Si vous construisez des boucles personnalisées par-dessus l'API Go de rousseau, définissez `Request.CacheableMessages` et `Request.System` — même un hit de cache superficiel rogne à la fois le coût et la pression de rate-limit.

Les marqueurs de cache sont exclusifs à Anthropic direct aujourd'hui. Bedrock, Vertex et les fournisseurs compatibles OpenAI les ignorent.

### 2. Compression

Pour les sessions longues sur un fournisseur tarifé au jeton (Anthropic direct, Bedrock, Vertex, OpenRouter), activez la compression :

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60      # depuis la valeur par défaut de CompressionConfig
    keep_recent: 8
```

Le `LLMCompressor` (`internal/agent/compressor.go`) résume la tranche la plus ancienne de la session en un unique message utilisateur synthétique quand le nombre de messages dépasse `trigger_messages`, et préserve les `keep_recent` derniers messages tels quels. Moins de jetons par tour = moins de pression rate-limit.

La compression est désactivée par défaut parce que le déploiement de référence utilise `claudecli` sur un palier d'abonnement, où le compte de jetons n'est pas facturé.

### 3. Cadence cron plus lente

Pour les démons purement d'arrière-plan, réduire de moitié la cadence cron réduit de moitié les requêtes. Les cadences `rousseau cron` sont des expressions cron — passez de toutes les 15 minutes à toutes les heures si l'exigence de fraîcheur le permet.

## Coût approximatif par fournisseur

Les limites de débit et le coût par jeton bougent indépendamment, mais les deux sont généralement corrélés (les paliers payants ont des limites plus élevées). Guide approximatif au 2026-07 :

| Fournisseur | Entrée $/MTok (classe Sonnet) | Sortie $/MTok | Lecture cache $/MTok |
|---|---|---|---|
| `anthropic` direct | ~3 | ~15 | ~0,30 |
| `bedrock` (Sonnet-4.6) | ~3 | ~15 | Cache : N/A à la rédaction |
| `vertex` (Anthropic on Vertex) | ~3 | ~15 | Cache : N/A à la rédaction |
| `openrouter` | dépend du modèle | dépend du modèle | dépend du fournisseur |
| `ollama` auto-hébergé | 0 $ | 0 $ | 0 $ (vous payez le compute) |
| `claudecli` | facturation au palier d'abonnement | inclus | N/A |

Récupérez les chiffres actuels sur la page de tarification de chaque fournisseur.

## Quand le SDK épuise ses retries

Si le SDK du fournisseur abandonne, rousseau expose l'erreur finale. Le tour est perdu — pas de file d'attente ni de retry sur disque. Deux atténuations :

- **Signaler à l'opérateur via le même canal.** L'échec de tour est visible dans la réponse du transport ; l'opérateur peut reformuler.
- **Basculer sur un second fournisseur à la main.** Voir [Guides: Multi-provider](/fr/guides/multi-provider/) pour le motif à deux démons.

Le failover automatique entre fournisseurs est un élément de feuille de route.

## Déboguer les problèmes de rate-limit

1. Réglez `log.level: debug` dans `config.yaml`. La sortie debug du SDK montre la valeur exacte de `Retry-After`.
2. Cherchez `turn.failed`, `whatsapp.handler_failed`, `cron.run_failed` dans le journal.
3. Consultez le tableau de bord du fournisseur (Anthropic Console, AWS CloudWatch, GCP Cloud Monitoring) pour la consommation réelle de quota.
4. Si vous êtes sur un palier d'abonnement, surveillez les réinitialisations de quota journalier — l'erreur du SDK inclut habituellement l'heure de reset.

## Référence rapide par fournisseur

<aside class="admonition" data-type="warning"><span class="admonition-title">Citez vos sources</span><p>Les tarifs et limites changent sans préavis. Les chiffres de ce tableau datent de mi-2026 et sont illustratifs. Renvoyez toujours à la page de tarification actuelle du fournisseur pour des valeurs faisant autorité.</p></aside>

| Fournisseur | Comportement retry | Signal de rate | Coût par 1M entrée | Coût par 1M sortie | Coût lecture cache |
|---|---|---|---|---|---|
| `anthropic` direct | SDK retry 5xx ; 429 avec `Retry-After` respecté | l'en-tête `429 Too Many Requests` porte l'heure de reset | ~3 $ (Sonnet) | ~15 $ (Sonnet) | ~0,30 $ |
| `bedrock` | Retry adaptatif SDK AWS | `ThrottlingException` | ~3 $ (Sonnet) | ~15 $ (Sonnet) | pas encore |
| `vertex` | Retry exponentiel SDK Google | `429 RESOURCE_EXHAUSTED` | ~3 $ (Sonnet) | ~15 $ (Sonnet) | pas encore |
| `openai` | SDK retry 5xx ; 429 respecté | `429 Too Many Requests` | spécifique au modèle | spécifique au modèle | spécifique au modèle |
| `openrouter` | passthrough vers le fournisseur sous-jacent | dépend du fournisseur | spécifique au modèle | spécifique au modèle | dépend du fournisseur |
| `ollama` | SDK retry ; local donc rare | aucun | 0 $ (coût compute) | 0 $ (coût compute) | N/A |
| `claudecli` | les erreurs de sous-processus remontent ; pas de retry côté rousseau | opaque | abonnement | abonnement | opaque |

Sources faisant autorité :

- [Tarifs Anthropic](https://www.anthropic.com/pricing)
- [Tarifs AWS Bedrock](https://aws.amazon.com/bedrock/pricing/)
- [Tarifs Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/pricing)
- [Tarifs OpenAI](https://openai.com/pricing)
- [Liste des modèles OpenRouter](https://openrouter.ai/models)

## Recette de retry côté appelant

Rousseau ne retry pas dans `Complete`. Si vous embarquez la bibliothèque d'agent, enveloppez `Turn` dans votre propre boucle de retry avec backoff exponentiel et jitter :

```go
func retryTurn(ctx context.Context, ag *agent.Agent, sess *agent.Session, maxRetries int) (agent.Message, error) {
    var lastErr error
    for attempt := 0; attempt < maxRetries; attempt++ {
        m, err := ag.Turn(ctx, sess)
        if err == nil {
            return m, nil
        }
        if !isRateLimit(err) {
            return agent.Message{}, err // non-retriable
        }
        lastErr = err
        // Exponential backoff with jitter: 1s, 2s, 4s, 8s, ...
        backoff := time.Duration(1<<attempt) * time.Second
        jitter := time.Duration(rand.Int63n(int64(backoff / 2)))
        select {
        case <-time.After(backoff + jitter):
        case <-ctx.Done():
            return agent.Message{}, ctx.Err()
        }
    }
    return agent.Message{}, fmt.Errorf("giving up after %d retries: %w", maxRetries, lastErr)
}

func isRateLimit(err error) bool {
    s := err.Error()
    return strings.Contains(s, "429") || strings.Contains(s, "rate limit") || strings.Contains(s, "ThrottlingException")
}
```

## Dépannage

### `429 Too Many Requests` à chaque requête

Vous êtes sur un palier bas ou une autre charge de travail consomme le quota. Options : (1) demander une augmentation de limite, (2) répartir la charge entre fournisseurs, (3) utiliser `claudecli` pour les charges de travail réservées à l'abonnement.

### `529 Overloaded` par intermittence

Le système Anthropic est à capacité. Pas un throttling par compte — la région entière est chargée. Réessayez avec backoff.

### Marqueurs de cache posés mais aucune économie visible

Vérifiez que `CacheableMessages` est bien défini. `applyCacheMarkers` dans `internal/llm/anthropic/cache.go` est un no-op à zéro. Vérifiez aussi que le préfixe est stable — un prompt système régénéré à chaque tour défait la mise en cache.

### `ThrottlingException` sur Bedrock avec faible volume

Le quota Bedrock est par compte, par modèle, par région. Certains modèles ont des quotas par défaut très bas (2–5 requêtes par minute). Demandez une augmentation dans la console Service Quotas.

### Réponses API lentes malgré une faible utilisation

Certains fournisseurs déprioritisent les comptes bas palier sous charge globale. Les en-têtes de réponse `x-ratelimit-*` d'Anthropic indiquent l'état actuel du bucket — inspectez-les si vous avez accès au SDK.

## Pages liées

- [Providers: Anthropic](/fr/providers/anthropic/) — détails des marqueurs de cache.
- [Configuration](/fr/configuration/) — chaque paramètre de compression.
- [User Guide: Compression + Recall](/fr/user-guide/compression-recall/) — discussion approfondie sur la compression.
- [Guides: Multi-provider](/fr/guides/multi-provider/) — répartir la charge entre endpoints.
- [Guides: Rate/Model Swap](/fr/guides/rate-model-swap/) — bascule à chaud de fournisseur en cas d'échec.

## Lecture complémentaire

- `internal/llm/anthropic/client.go` — invocation du SDK.
- `internal/llm/anthropic/cache.go` — helper de marquage de cache.
- `internal/agent/agent.go` — où les échecs de tour remontent.
- Pages de tarification des fournisseurs liées ci-dessus.
