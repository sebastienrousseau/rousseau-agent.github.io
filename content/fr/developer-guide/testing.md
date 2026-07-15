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
description: "Testing pattern for rousseau-agent: dependency injection via interfaces (WSConn, IMAPClient, HTTPClient), fake generators, race + coverage thresholds."
keywords: "testing, dependency injection, fake, mock, coverage, race, go test, httptest"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/developer-guide/testing/"
subtitle: "Dependency injection, fakes, race, coverage."
tags: "developer-guide, testing, di, fakes"
title: "Tests"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "testing, dependency injection, fake, mock, coverage, race, go test, httptest"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tests"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 65
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/testing/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/testing/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Tests"
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
twitter_description: "Testing pattern for rousseau-agent: dependency injection via interfaces (WSConn, IMAPClient, HTTPClient), fake generators, race + coverage thresholds."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tests"
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

## Le motif

Chaque package qui parle au monde extérieur définit une petite interface pour sa dépendance, prend cette interface comme paramètre de constructeur, et injecte un vrai client dans `cli/*.go` (production) ou un fake dans `*_test.go` (tests).

Exemples dans l'arborescence :

| Package | Interface | Réel | Fake pour tests |
|---|---|---|---|
| `internal/transport/whatsapp` | `WSConn` | WebSocket whatsmeow | struct en mémoire avec un canal `send` |
| `internal/transport/email` | `IMAPClient` | client `emersion/go-imap` | canal scripté de messages |
| `internal/transport/whatsapp` | `Sender` | envoi direct whatsmeow | slice en mémoire pour assertion |
| `internal/llm/*` | `HTTPClient` (indirect via `http.Client`) | `http.DefaultTransport` | `httptest.NewServer` |
| `internal/state/sqlite` | `state.Store` (interface possédée par `state`) | `modernc.org/sqlite` sur disque | DSN en mémoire `:memory:` |
| `internal/agent` | `Provider`, `Approver`, `Compressor`, `RecallProvider` | types `llm/*` concrets | implémentations struct dans `_test.go` |

La règle : **interface côté consommateur, implémentation côté fournisseur.** `Provider` est défini dans `agent`, pas dans `llm/anthropic`. `Store` est défini dans `state`, pas dans `state/sqlite`.

## Exécuter le gate

```sh
make check
```

est équivalent à :

```sh
go vet ./...
golangci-lint run
go test -race -count=1 -covermode=atomic ./...
govulncheck ./...
```

La CI exécute la même commande sur `ubuntu-latest` et `macos-latest`. Si ça passe en local, ça passe en CI — sauf bugs spécifiques à la plateforme, raison pour laquelle macOS est dans la matrice.

## Race detector

`-race` n'est pas négociable. Chaque démon dans rousseau implique plusieurs goroutines (pompe de transport, boucle d'agent, planificateur cron, writer du magasin de sessions). Une race dans l'une d'elles est un vrai bug.

Si vous trouvez un test qui n'échoue que sous `-race`, c'est un bug dans le code testé, pas dans le test. Ne désactivez pas `-race`.

## Plancher de couverture

Le plancher de couverture actuel est **75 % total**. Les packages cœur (`internal/agent`, `internal/tools`, `internal/state/sqlite`) sont à 85–100 % et y sont tenus par la suite de tests préexistante ; le nouveau code dans ces packages ne doit pas les faire baisser.

Un job CI tourne après `go test -race -covermode=atomic ./... -coverprofile=coverage.out` et inspecte `coverage.out`. Rater le plancher fait échouer le build.

## Générateurs de fakes

Rousseau n'utilise pas de bibliothèque de génération de mocks. Les fakes sont des types struct écrits à la main, assez petits pour être lus d'un coup d'œil :

```go
type fakeProvider struct {
    responses []agent.Response
    calls     []agent.Request
}

func (f *fakeProvider) Complete(_ context.Context, req agent.Request) (agent.Response, error) {
    f.calls = append(f.calls, req)
    if len(f.responses) == 0 {
        return agent.Response{}, errors.New("no more canned responses")
    }
    resp := f.responses[0]
    f.responses = f.responses[1:]
    return resp, nil
}
```

Deux propriétés en découlent :

1. Le fake est inspectable — `calls` capture chaque requête, donc les assertions peuvent vérifier ce que le code testé a émis.
2. Le fake est déterministe — les réponses canned sont consommées dans l'ordre.

## `httptest` pour les fournisseurs de forme HTTP

Chaque adaptateur LLM qui parle HTTP utilise `httptest.NewServer` pour les tests :

```go
srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
    _ = json.NewEncoder(w).Encode(map[string]any{
        "role":       "assistant",
        "content":    []map[string]any{{"type": "text", "text": "hello"}},
        "stop_reason":"end_turn",
    })
}))
defer srv.Close()

p := anthropic.New(anthropic.Config{
    APIKey:  "test",
    BaseURL: srv.URL,
    Model:   "test-model",
})
```

Pour le streaming SSE, la même technique fonctionne — `http.Flusher` est disponible sur le response writer.

## Corpus fuzz

Chaque parseur a une fonction `Fuzz*`. Exécutez la batterie complète :

```sh
make fuzz
```

En CI, fuzz tourne pour une durée bornée (`-fuzztime`). En local, faites tourner plus longtemps pour amorcer le corpus.

## Tests table-driven

Les tests de Rousseau s'appuient largement sur la forme table-driven. Exemple :

```go
func TestPatternApprover_Approve(t *testing.T) {
    tests := []struct {
        name     string
        approver *agent.PatternApprover
        req      agent.ApprovalRequest
        want     agent.Decision
    }{
        {
            name:     "allow read",
            approver: &agent.PatternApprover{Allow: []agent.PatternRule{{ToolName: "read"}}},
            req:      agent.ApprovalRequest{ToolName: "read"},
            want:     agent.DecisionAllow,
        },
        {
            name:     "deny wins over allow",
            approver: &agent.PatternApprover{
                Allow: []agent.PatternRule{{ToolName: "bash"}},
                Deny:  []agent.PatternRule{{ToolName: "bash", Match: "rm"}},
            },
            req:  agent.ApprovalRequest{ToolName: "bash", Input: json.RawMessage(`{"command":"rm -rf /"}`)},
            want: agent.DecisionDeny,
        },
    }
    for _, tc := range tests {
        t.Run(tc.name, func(t *testing.T) {
            got, _ := tc.approver.Approve(context.Background(), tc.req)
            require.Equal(t, tc.want, got)
        })
    }
}
```

C'est extensible — chaque nouvelle forme de règle devient une ligne du tableau.

## Fuites de goroutines

Les tests qui lancent des goroutines doivent les joindre. Motifs courants :

- Utilisez `context.WithCancel` et `cancel()` à la fin du test.
- Utilisez un `sync.WaitGroup` et `wg.Wait()`.
- Consommez chaque canal jusqu'au `close`.

Si un test fuit une goroutine, `go test -race` peut l'attraper via une panic nil-receiver sur la goroutine fuitée après que le `main` du fichier de test soit sorti. Moins coûteux d'être discipliné dès le départ.

## Temps déterministe

Pour les tests sensibles au temps (cron, classement de récence du rappel), injectez un fournisseur de `time.Time` :

```go
type Clock interface {
    Now() time.Time
}
```

Câblez le vrai `time.Now` dans `cli/*` et un `time.Time` fake dans le test. Le planificateur `internal/cron/scheduler.go` utilise ce motif.

## Tester la TUI

`internal/tui/model_test.go` utilise le helper `TestModel` de `bubbletea`. `View()` est une fonction de chaîne pure du modèle, donc la plupart des assertions deviennent « exécute cet update, attends cette sortie de View ».

## Ce qu'il ne faut pas tester

- Les bibliothèques tierces. Rousseau ne dédouble pas les tests amont de whatsmeow ou `signal-cli`.
- La bibliothèque standard Go. `net/http` fonctionne.
- L'enregistrement des flags CLI par Cobra. Les propres tests de Cobra couvrent ça.

À la place, testez le code que vous écrivez : le câblage, le branching, les chemins d'erreur, les chemins de récupération.

## Suite

- [Ajouter un transport](/fr/developer-guide/add-a-transport/) — le motif d'injection de fake appliqué à un transport complet.
- [Ajouter un fournisseur](/fr/developer-guide/add-a-provider/) — `httptest` en action.
- [Contribuer](/fr/developer-guide/contributing/) — la checklist des PR.
