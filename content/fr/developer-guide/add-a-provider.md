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
description: "How to add a sixth LLM provider to rousseau-agent: implement Provider.Complete and optionally StreamingProvider.CompleteStream."
keywords: "add provider, llm, chat completion, streaming, agent provider, extend"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/developer-guide/add-a-provider/"
subtitle: "Provider.Complete and StreamingProvider.CompleteStream."
tags: "developer-guide, provider, llm, extend"
title: "Ajouter un fournisseur"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add provider, llm, chat completion, streaming, agent provider, extend"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Ajouter un fournisseur"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 63
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-provider/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-provider/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Ajouter un fournisseur"
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
twitter_description: "How to add a sixth LLM provider to rousseau-agent: implement Provider.Complete and optionally StreamingProvider.CompleteStream."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Ajouter un fournisseur"
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

## L'interface

`internal/agent/provider.go` (paraphrasé) :

```go
type Request struct {
    SessionID string
    System    string
    Messages  []Message
    Tools     []ToolDefinition
}

type Response struct {
    Message    Message
    StopReason StopReason
}

// Provider drives a single round-trip.
type Provider interface {
    Complete(ctx context.Context, req Request) (Response, error)
}

// StreamingProvider streams response deltas as they arrive.
type StreamingProvider interface {
    Provider
    CompleteStream(ctx context.Context, req Request) (StreamReader, error)
}
```

Chaque adaptateur LLM satisfait au moins `Provider`. `StreamingProvider` est opt-in — la TUI et les handlers de transport chat retombent sur le chemin non-streaming quand un fournisseur ne l'implémente pas.

`StopReason` est l'une de `StopEndTurn`, `StopToolUse`, `StopMaxTokens`. La boucle d'agent traite `StopEndTurn` comme terminal et `StopToolUse` comme « le modèle veut un appel d'outil ».

## Squelette pour un nouveau fournisseur

Ajoutons un fournisseur **Cohere Command R** hypothétique.

### Étape 1 — Répertoire

```
internal/llm/cohere/
├── client.go        # Config, New
├── complete.go      # Provider.Complete
├── stream.go        # StreamingProvider.CompleteStream (optional)
└── *_test.go
```

### Étape 2 — `client.go`

```go
// Package cohere implements the Cohere Command R provider.
package cohere

import (
    "net/http"
    "time"
)

// Config configures the Cohere provider.
type Config struct {
    APIKey    string
    Model     string
    BaseURL   string
    MaxTokens int64
}

// Provider is the Cohere adapter.
type Provider struct {
    cfg    Config
    client *http.Client
}

// New constructs a Provider.
func New(cfg Config) *Provider {
    if cfg.BaseURL == "" {
        cfg.BaseURL = "https://api.cohere.com/v1"
    }
    if cfg.MaxTokens == 0 {
        cfg.MaxTokens = 4096
    }
    return &Provider{
        cfg:    cfg,
        client: &http.Client{Timeout: 120 * time.Second},
    }
}
```

### Étape 3 — `complete.go`

Implémentez `Complete` :

```go
package cohere

import (
    "bytes"
    "context"
    "encoding/json"
    "fmt"
    "net/http"

    "github.com/sebastienrousseau/rousseau-agent/internal/agent"
)

// Complete satisfies agent.Provider.
func (p *Provider) Complete(ctx context.Context, req agent.Request) (agent.Response, error) {
    body, err := p.encodeRequest(req)
    if err != nil {
        return agent.Response{}, fmt.Errorf("cohere: encode: %w", err)
    }

    httpReq, err := http.NewRequestWithContext(ctx, http.MethodPost, p.cfg.BaseURL+"/chat", bytes.NewReader(body))
    if err != nil {
        return agent.Response{}, err
    }
    httpReq.Header.Set("content-type", "application/json")
    httpReq.Header.Set("authorization", "Bearer "+p.cfg.APIKey)

    httpResp, err := p.client.Do(httpReq)
    if err != nil {
        return agent.Response{}, fmt.Errorf("cohere: transport: %w", err)
    }
    defer httpResp.Body.Close()

    if httpResp.StatusCode >= 400 {
        return agent.Response{}, fmt.Errorf("cohere: HTTP %d", httpResp.StatusCode)
    }

    var raw cohereResponse
    if err := json.NewDecoder(httpResp.Body).Decode(&raw); err != nil {
        return agent.Response{}, fmt.Errorf("cohere: decode: %w", err)
    }
    return p.decodeResponse(raw), nil
}

// Compile-time interface check.
var _ agent.Provider = (*Provider)(nil)
```

Les corps de `encodeRequest`, `decodeResponse` et la forme `cohereResponse` sont spécifiques à Cohere — ils traduisent les types agnostiques `agent.Request` et `agent.Response` de rousseau vers et depuis le format réseau de Cohere.

### Étape 4 — Streaming (optionnel)

Si Cohere supporte le streaming SSE, implémentez `CompleteStream`. Sautez-le pour une première passe ; la boucle d'agent retombe automatiquement sur le non-streaming.

### Étape 5 — Surface de config

Ajoutez `CohereConfig` à `internal/config/config.go` :

```go
type CohereConfig struct {
    APIKey    string `mapstructure:"api_key"`
    Model     string `mapstructure:"model"`
    BaseURL   string `mapstructure:"base_url"`
    MaxTokens int64  `mapstructure:"max_tokens"`
}
```

Ajoutez un champ à `Config` :

```go
Cohere CohereConfig `mapstructure:"cohere"`
```

Étendez `setDefaults` avec un défaut de modèle raisonnable :

```go
v.SetDefault("cohere.model", "command-r-plus")
```

### Étape 6 — Câblage CLI

Dans `internal/cli/provider.go`, étendez `buildProvider(cfg *config.Config)` :

```go
func buildProvider(cfg *config.Config) (agent.Provider, error) {
    switch cfg.Provider {
    // ...existing cases...
    case "cohere":
        return cohere.New(cohere.Config{
            APIKey:    cfg.Cohere.APIKey,
            Model:     cfg.Cohere.Model,
            BaseURL:   cfg.Cohere.BaseURL,
            MaxTokens: cfg.Cohere.MaxTokens,
        }), nil
    default:
        return nil, fmt.Errorf("unknown provider %q", cfg.Provider)
    }
}
```

Étendez `rousseau doctor` (`internal/cli/doctor.go`) pour ajouter un bloc de contrôles `provider.cohere.*` quand `cfg.Provider == "cohere"`. Reflétez les contrôles anthropic existants.

## Détails de contrat que la boucle d'agent suppose

- **`Complete` respecte `ctx`.** Les longues requêtes HTTP doivent honorer l'annulation de contexte, sinon l'arrêt `SIGTERM` du démon se figera.
- **Aller-retour tool-use.** Quand le modèle émet des blocs `tool_use`, le `StopReason` de la réponse doit être `StopToolUse` et le contenu du message doit inclure `Content{Kind: ContentToolUse, ToolUse: &ToolUse{Name, Input, ID}}` pour chaque appel demandé. La boucle d'agent en route chacun vers le `Registry`, l'exécute et repasse les résultats dans l'appel `Complete` suivant.
- **Gestion des `tool_result`.** À l'appel suivant, `req.Messages` contient un message utilisateur dont le contenu inclut `Content{Kind: ContentToolResult, ToolResult: &ToolResult{ToolUseID, Output, IsError}}` pour chaque appel exécuté. Le fournisseur doit les rendre dans la forme attendue par l'API amont.
- **Check d'interface à la compilation.** `var _ agent.Provider = (*Provider)(nil)` au niveau du package attrape le drift d'interface au build.

## Contrat de streaming

Si vous implémentez `StreamingProvider` :

```go
type StreamReader interface {
    Next(ctx context.Context) (StreamChunk, error)
    Close() error
}

type StreamChunk struct {
    Delta     string       // partial text delta
    Done      bool         // final chunk
    Response  *Response    // final Response, non-nil only on Done
}
```

La TUI et les handlers de transport chat lisent les deltas au fur et à mesure ; la `Response` finale sert à ajouter le message assistant complètement formé à la session.

## Cache de prompt

`internal/llm/anthropic` place des marqueurs `cache_control` sur les deux derniers messages de la requête. Si votre fournisseur supporte le cache de prompt, faites de même — cela transforme la compression + rappel (voir [Compression + Rappel](/fr/user-guide/compression-recall/)) d'un motif gourmand en jetons en un motif bon marché.

## Tests

Utilisez `httptest.NewServer` pour monter un amont factice. `internal/llm/anthropic/*_test.go` est la référence. Le motif :

1. Démarrez `httptest.NewServer` avec un handler qui retourne du JSON canned.
2. Construisez le fournisseur en pointant `BaseURL` vers le serveur de test.
3. Appelez `Complete` avec un `Request` canned.
4. Assertez sur la forme de la `Response` retournée.

Pour le streaming, `httptest` supporte aussi les Server-Sent Events — voir `internal/llm/anthropic/stream.go`.

## Documentation

Ajoutez `content/providers/cohere.md` dans ce site de doc. Suivez la forme de `content/providers/anthropic.md` — description, surface de config, détails d'auth, précautions spécifiques au fournisseur.

## Pièges courants

- **Réécrire silencieusement `Messages`.** La boucle d'agent est la source de vérité pour l'état conversationnel. Les fournisseurs doivent traduire la forme sans muter la sémantique.
- **Perdre les IDs tool-use.** Chaque `ToolUse.ID` dans une réponse doit correspondre à un `ToolResult.ToolUseID` sur la requête suivante. Si votre fournisseur assigne ses propres IDs, traduisez soigneusement.
- **Ignorer `MaxTokens`.** Certains fournisseurs rejettent les requêtes sans limite explicite. Réglez un défaut raisonnable dans `New`.
- **Bloquer la boucle avec des politiques de retry.** Les retries appartiennent à l'adaptateur du fournisseur, pas à la boucle d'agent. Bornez-les ; échouer rapidement vaut mieux que se figer.

## Suite

- [Testing](/fr/developer-guide/testing/) — comment écrire le `_test.go` du fournisseur.
- [Ajouter un outil](/fr/developer-guide/add-a-tool/) — le plus petit point d'extension.
- [Configuration](/fr/configuration/) — la surface de config que chaque fournisseur expose.
