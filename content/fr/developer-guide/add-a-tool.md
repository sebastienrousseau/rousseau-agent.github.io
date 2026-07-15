---

# Front Matter (YAML)

author: "sebastian.rousseau@gmail.com (Sebastien Rousseau) "
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
description: "How to add a new built-in tool to rousseau-agent: declare a JSON schema, implement Execute, register with the tool registry."
keywords: "add tool, tool registry, json schema, execute, extend, custom tool"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/developer-guide/add-a-tool/"
subtitle: "Schema, Execute, register — three moving parts."
tags: "developer-guide, tools, extend"
title: "Ajouter un outil"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add tool, tool registry, json schema, execute, extend, custom tool"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Ajouter un outil"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 64
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-tool/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-tool/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Ajouter un outil"
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
twitter_description: "How to add a new built-in tool to rousseau-agent: declare a JSON schema, implement Execute, register with the tool registry."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Ajouter un outil"
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

`internal/tools/tool.go` (paraphrasé) :

```go
type Tool interface {
    Name() string
    Description() string
    InputSchema() map[string]any
    Execute(ctx context.Context, input json.RawMessage) (string, error)
}
```

Quatre méthodes, pas de cycle de vie. Les outils sont sans état du point de vue de la boucle — tout état dont l'outil a besoin (un cache de regex compilées, un index en mémoire) est un champ privé sur le type concret.

## Squelette pour un nouvel outil

Ajoutons un outil hypothétique **`http_get`** qui récupère une URL et renvoie son corps.

### Étape 1 — Le type

```go
package builtin

import (
    "context"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "time"

    "github.com/sebastienrousseau/rousseau-agent/internal/tools"
)

// HTTPGetTool fetches a URL over HTTPS and returns the response body.
type HTTPGetTool struct {
    Timeout time.Duration
    client  *http.Client
}

// NewHTTPGetTool constructs an HTTPGetTool. Zero timeout uses 30s.
func NewHTTPGetTool(timeout time.Duration) *HTTPGetTool {
    if timeout == 0 {
        timeout = 30 * time.Second
    }
    return &HTTPGetTool{
        Timeout: timeout,
        client:  &http.Client{Timeout: timeout},
    }
}
```

### Étape 2 — Métadonnées

```go
// Name satisfies tools.Tool.
func (*HTTPGetTool) Name() string { return "http_get" }

// Description satisfies tools.Tool.
func (*HTTPGetTool) Description() string {
    return "Fetch an HTTPS URL and return the response body. Input: url (string). Redirects are followed up to 10 hops. Response is capped at 1 MiB."
}
```

La **description est destinée au modèle**. Elle doit se lire comme une courte docstring pour un autre ingénieur — ce que fait l'outil, ce que signifient ses entrées, quelle est la forme de la sortie.

### Étape 3 — Schéma d'entrée

```go
// InputSchema satisfies tools.Tool.
func (*HTTPGetTool) InputSchema() map[string]any {
    return map[string]any{
        "type": "object",
        "properties": map[string]any{
            "url": map[string]any{
                "type":        "string",
                "description": "Absolute HTTPS URL to fetch.",
            },
        },
        "required": []string{"url"},
    }
}
```

Gardez le schéma strict. Chaque propriété reçoit une `description`. Le tableau `required` est imposé par le validateur tool-use du modèle — les champs manquants provoquent un retry `tool_use`, pas une erreur runtime.

### Étape 4 — Execute

```go
type httpGetInput struct {
    URL string `json:"url"`
}

// Execute satisfies tools.Tool.
func (t *HTTPGetTool) Execute(ctx context.Context, raw json.RawMessage) (string, error) {
    var in httpGetInput
    if err := json.Unmarshal(raw, &in); err != nil {
        return "", fmt.Errorf("http_get: parse input: %w", err)
    }
    if in.URL == "" {
        return "", fmt.Errorf("http_get: url is required")
    }
    // Refuse plaintext HTTP; refuse non-http schemes.
    if !strings.HasPrefix(in.URL, "https://") {
        return "", fmt.Errorf("http_get: only https:// URLs are permitted")
    }

    req, err := http.NewRequestWithContext(ctx, http.MethodGet, in.URL, nil)
    if err != nil {
        return "", fmt.Errorf("http_get: build request: %w", err)
    }
    req.Header.Set("user-agent", "rousseau-agent/http_get")

    resp, err := t.client.Do(req)
    if err != nil {
        return "", fmt.Errorf("http_get: transport: %w", err)
    }
    defer func() { _ = resp.Body.Close() }()

    body, err := io.ReadAll(io.LimitReader(resp.Body, 1<<20))
    if err != nil {
        return "", fmt.Errorf("http_get: read body: %w", err)
    }
    return fmt.Sprintf("HTTP %d\n%s", resp.StatusCode, string(body)), nil
}

// Compile-time interface satisfaction check.
var _ tools.Tool = (*HTTPGetTool)(nil)
```

### Étape 5 — Enregistrement

Câblez-le dans `internal/cli/chat.go` (et chaque autre commande qui construit un registry — grepez `registry.MustRegister` pour les trouver) :

```go
registry.MustRegister(builtin.NewHTTPGetTool(30 * time.Second))
```

Une fois enregistré, l'outil est disponible pour le modèle à chaque tour.

### Étape 6 — Tests

Suivez `internal/tools/builtin/read_test.go` pour le motif :

```go
func TestHTTPGetTool_Execute_Success(t *testing.T) {
    srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
        _, _ = w.Write([]byte("hello"))
    }))
    defer srv.Close()

    // The tool refuses plaintext HTTP; wrap the test server behind httptest.NewTLSServer instead
    // for a real integration test, or expose an internal seam that permits `http://` in tests only.
    // The skeleton here is illustrative.
}

func TestHTTPGetTool_Execute_RejectsPlaintextHTTP(t *testing.T) {
    tool := builtin.NewHTTPGetTool(0)
    _, err := tool.Execute(context.Background(), json.RawMessage(`{"url":"http://example.com"}`))
    require.Error(t, err)
    require.Contains(t, err.Error(), "only https")
}
```

### Étape 7 — Politique d'approbation

L'outil est maintenant disponible pour le modèle, soumis à la [politique d'approbation](/fr/user-guide/approval-policies/). Recommandez une règle deny dans la doc pour la posture par défaut :

```yaml
deny:
  - {tool: http_get, match: "\"url\":\"https://(169\\.254|10\\.|192\\.168\\.|172\\.(1[6-9]|2[0-9]|3[01])\\.)"}
```

Cela empêche l'outil d'appeler AWS IMDS ou l'espace privé RFC1918 — une demande courante pour les outils de fetch HTTP.

### Étape 8 — Documentation

Ajoutez une section à `content/user-guide/tools.md` décrivant le nouvel outil : schéma, sémantique, notes de sécurité. Suivez la forme des cinq outils existants.

## Détails du contrat

- **Sans état** : `Execute` ne doit pas transporter d'état entre appels qui ne soit pas explicitement privé aux champs propres de l'outil. Deux tours concurrents sur deux sessions peuvent appeler le même outil simultanément.
- **Respect du contexte** : `Execute` doit honorer l'annulation de `ctx`. Le travail long doit périodiquement vérifier `ctx.Err()` ou passer par un appel de bibliothèque conscient du contexte.
- **Pas de panics** : retournez des erreurs à la place. La boucle d'agent convertit une erreur en `tool_result` avec `IsError: true`, auquel le modèle peut s'adapter.
- **Forme de retour** : la sortie est une chaîne, réinjectée au modèle au tour suivant. Incluez assez de structure (par ex. numéros de ligne, codes de statut) pour que le modèle puisse raisonner dessus.

## Outils personnalisés sans toucher au code source

Si vous ne voulez pas forker rousseau, embarquez la boucle d'agent dans votre propre binaire et enregistrez-y vos outils :

```go
registry := tools.NewRegistry()
registry.MustRegister(builtin.NewReadTool())
registry.MustRegister(builtin.NewWriteTool())
// ...
registry.MustRegister(mypkg.NewMyTool())

ag := agent.New(provider, registry, logger, agent.Options{})
```

Voir `examples/embed-agent/` dans l'arborescence source pour un exemple d'embedding complet.

## Pièges courants

- **Schéma trop large.** N'exiger que `type: object` n'aide pas le modèle. Énumérez chaque propriété, décrivez chaque champ.
- **Bloquer sur I/O sans deadline.** Utilisez toujours `NewRequestWithContext`, réglez toujours `http.Client{Timeout: ...}`, honorez toujours `ctx`.
- **Retourner trop.** La sortie est réinjectée au modèle au tour suivant. Une réponse de 1 Mo brûle des jetons ; plafonnez-la.
- **Effets de bord discrets.** Un outil qui mute le monde doit journaliser ce qu'il a fait dans la chaîne de retour pour que la piste d'audit de l'approbateur soit complète.
- **Oublier le check d'interface à la compilation.** `var _ tools.Tool = (*MyTool)(nil)` au niveau du package attrape le drift d'interface au build.

## Suite

- [Guide utilisateur : outils](/fr/user-guide/tools/) — les cinq outils intégrés avec schémas.
- [Guide utilisateur : politiques d'approbation](/fr/user-guide/approval-policies/) — comment filtrer le nouvel outil.
- [Testing](/fr/developer-guide/testing/) — le motif pour les tests d'outils.
