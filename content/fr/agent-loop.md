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
changefreq: "weekly"
description: "Embed rousseau-agent's agent loop into your own Go binary. Provider and StreamingProvider interfaces, Session/Message/Turn shapes, tool registration, approval policies, compression, FTS5 recall."
keywords: "library, embedding, agent.Provider, agent.Session, agent.Turn, tool registry, approver, compression, FTS5, recall"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/agent-loop/"
subtitle: "Contrat d'intégration en bibliothèque : Provider, Registry, Session, Turn."
tags: "library, embedding, reference"
title: "Référence de la boucle d'agent"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "library, embedding, agent.Provider, agent.Session, agent.Turn, tool registry, approver, compression, FTS5, recall"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Référence de la boucle d'agent"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 22
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/agent-loop/index.html"
item_link: "https://docs.rousseau-agent.dev/agent-loop/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Référence de la boucle d'agent"
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
twitter_description: "Embed rousseau-agent's agent loop into your own Go binary. Provider and StreamingProvider interfaces, Session/Message/Turn shapes, tool registration, approval policies, compression, FTS5 recall."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Référence de la boucle d'agent"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Ce que vous allez apprendre</span><p>L'anatomie complète d'un <code>Agent.Turn</code> : comment <code>Compressor</code>, <code>SkillsProvider</code> et <code>RecallProvider</code> composent le prompt système, comment les blocs <code>tool_use</code> du modèle traversent l'<code>Approver</code>, comment les résultats d'outils sont replacés dans la session, et comment la boucle se termine. Lisez <code>internal/agent/agent.go</code> en parallèle de cette page.</p></aside>

## rousseau en tant que bibliothèque

`rousseau-agent` est autant une bibliothèque qu'un daemon. La boucle d'agent, le registre d'outils et les abstractions de fournisseur n'ont aucune dépendance CLI. Vous pouvez les composer dans votre propre binaire sans importer `internal/cli` ni aucun package de transport.

Chaque identifiant exporté possède un commentaire godoc. `pkg.go.dev/github.com/sebastienrousseau/rousseau-agent` produit la référence complète.

## Anatomie d'un Turn

La fonction `Agent.Turn` est définie dans `internal/agent/agent.go`. En prose, un tour effectue ceci :

```
Turn(ctx, session)
  │
  ├── 1. Session guard: empty session → ErrEmptySession
  │
  ├── 2. Compressor.Compress(ctx, session)
  │     • If enabled and len(messages) > TriggerMessages, summarise older
  │       messages in place. Sets CacheableMessages on next Request.
  │
  ├── 3. registry.Definitions() → toolDefs
  │
  └── loop up to MaxIterations (default 32) times:
        │
        ├── a. Build Request{
        │       SessionID:         session.ID,
        │       System:            systemPrompt(session),
        │       Messages:          session.Messages,
        │       Tools:             toolDefs,
        │       CacheableMessages: <hint from compressor>,
        │     }
        │
        ├── b. resp = provider.Complete(ctx, req)
        │
        ├── c. session.Append(resp.Message)
        │
        ├── d. Switch on resp.StopReason:
        │       • StopEndTurn → return resp.Message (success)
        │       • StopMaxTokens / StopOther → return resp.Message
        │       • StopToolUse → continue to (e)
        │
        ├── e. runTools(ctx, resp.Message, sessionID):
        │       For each tool_use block:
        │         • registry.Get(name) → tool or ErrToolNotFound
        │         • approver.Approve(...)
        │             DecisionDeny → tool_result with is_error=true and reason
        │             DecisionAllow → tool.Execute(ctx, input)
        │               err → tool_result with is_error=true and err.Error()
        │               ok  → tool_result with output
        │
        └── f. session.Append(Message{Role: user, Content: []tool_result})
              Loop.

  MaxIterations exhausted → ErrMaxIterations
```

### Backpressure et annulation

Le `ctx` passé à `Turn` se propage partout : `Compressor.Compress`, chaque `Provider.Complete`, chaque `Tool.Execute` et chaque `Approver.Approve`. Annulez le contexte pour interrompre en cours de tour — l'appel de fournisseur de l'itération en cours retourne `context.Canceled`, la session conserve le dernier message complet du modèle ainsi que l'appel d'outil en suspens, et l'appelant peut décider de réessayer ou non.

Le `BashTool` intégré enveloppe chaque commande dans son propre `context.WithTimeout` (60 s par défaut, configurable) afin qu'une commande incontrôlée ne puisse dépasser le contexte parent.

### Composition du prompt système

`systemPrompt(ctx, session)` dans `agent.go` ligne 138 assemble jusqu'à trois parties :

```
<Options.SystemPrompt>

<SkillsProvider.SystemAppendix(session)>

<RecallProvider.SystemAppendix(ctx, session)>
```

Toute partie renvoyant une chaîne vide est omise. Le résultat est `strings.Join(parts, "\n\n")`. La composition a lieu une fois par itération (et non par tour), de sorte que skills et recall réagissent au message le plus récent — y compris les résultats d'outils intermédiaires, le cas échéant.

### Gestion de la fenêtre de contexte

Les sessions volumineuses finissent par dépasser la fenêtre de contexte du modèle. Rousseau ne tronque pas de lui-même — c'est le rôle du `Compressor`. Le `NoopCompressor` par défaut ne réécrit jamais ; les intégrateurs qui veulent une transcription illimitée dans une petite fenêtre doivent soit fournir leur propre compresseur, soit accepter l'erreur côté modèle lorsque la fenêtre se remplit.

`LLMCompressor` (voir plus bas) condense les messages plus anciens que `KeepRecent` en un seul bloc de résumé dès que le nombre dépasse `TriggerMessages`. Le résumé est généré par le fournisseur qui exécute le tour, ce qui coûte une completion supplémentaire par cycle de compression.

## L'interface Provider

`internal/agent/provider.go` :

```go
type Provider interface {
    Name() string
    Complete(ctx context.Context, req Request) (Response, error)
}

type StreamingProvider interface {
    Provider
    CompleteStream(ctx context.Context, req Request, out chan<- StreamEvent) error
}
```

`Complete` exécute un tour unique sans streaming. `Request` transporte `SessionID`, `System`, `Messages`, `Tools` et `CacheableMessages` (un indice de cache éphémère). `Response` retourne un unique `Message` d'assistant, un `StopReason` (`end_turn`, `tool_use`, `max_tokens`, `other`) et les compteurs de tokens `Usage`.

Chaque fournisseur livré (Anthropic, Bedrock, Vertex, compatible OpenAI, claudecli) implémente `Provider`. Tous, sauf `claudecli`, implémentent `StreamingProvider`.

## Session, Message, Turn

`internal/agent/session.go` et `internal/agent/message.go` :

```go
type Session struct {
    ID        string
    Title     string
    Messages  []Message
    CreatedAt time.Time
    UpdatedAt time.Time
}

type Message struct {
    Role      Role     // "user", "assistant", "system"
    Content   []Content
    CreatedAt time.Time
}

type Content struct {
    Kind       ContentKind  // "text", "tool_use", "tool_result"
    Text       string
    ToolUse    *ToolUse
    ToolResult *ToolResult
}
```

Une `Session` est append-only. Chaque message utilisateur est un appel à `Agent.Turn(ctx, session)` ; la boucle d'agent mute la session sur place et retourne le `Message` d'assistant final.

## Enregistrer des outils

`internal/tools` :

```go
registry := tools.NewRegistry()
registry.MustRegister(builtin.NewReadTool())
registry.MustRegister(builtin.NewGrepTool(0, 0))
registry.MustRegister(builtin.NewEditTool())
```

Chaque outil déclare un schéma JSON strict. Ajouter le vôtre revient à implémenter `Tool` :

```go
type Tool interface {
    Name() string
    Description() string
    InputSchema() json.RawMessage
    Execute(ctx context.Context, input json.RawMessage) (string, error)
}
```

`MustRegister` panique sur les noms en double ; utilisez `Register` et vérifiez l'erreur si vous construisez le registre dynamiquement.

## Politiques d'approbation

`internal/agent/approver.go`. Trois politiques intégrées :

- `AllowAllApprover` — chaque appel s'exécute.
- `DenyAllApprover{Reason: "…"}` — chaque appel est bloqué avec la raison indiquée.
- `PatternApprover{Allow: []PatternRule, Deny: []PatternRule, Default: Decision}` — allow / deny par regex et par outil. Deny l'emporte ; les requêtes non appariées utilisent `Default` (vide → `DecisionDeny`).

Les règles de motif sont compilées une fois de manière paresseuse. Les erreurs de compilation remontent sous forme de `DecisionDeny` avec la chaîne d'erreur en raison, de sorte qu'une regex mal formée échoue en toute sécurité.

Les approveurs personnalisés implémentent :

```go
type Approver interface {
    Approve(ctx context.Context, req ApprovalRequest) (Decision, string)
}
```

`ApprovalRequest` transporte `ToolName`, l'`Input` JSON brut et `SessionID`. Retournez `DecisionAllow` ou `DecisionDeny` accompagné d'une chaîne de raison (renvoyée au modèle sous forme d'erreur `tool_result`).

## Compression

`internal/agent/compressor.go`. `LLMCompressor` appelle le même fournisseur pour résumer les messages plus anciens dès que la session franchit un seuil :

```go
compressor, err := agent.NewLLMCompressor(agent.LLMCompressorConfig{
    Provider:        provider,
    TriggerMessages: 60,
    KeepRecent:      8,
})
```

Les `KeepRecent` messages les plus récents survivent tels quels ; tout ce qui est plus ancien est condensé en un unique bloc de résumé. Le `Compressor` positionne `CacheableMessages` sur la requête suivante afin que le résumé soit chaud dans le cache dès le tour suivant.

`NoopCompressor` est utilisé par défaut lorsque `Compressor` est nil.

## Rappel inter-sessions FTS5

`internal/agent/recall.go` + `internal/state/sqlite/`. L'index FTS5 du store de sessions couvre chaque message. `SQLiteRecall` interroge à partir du message utilisateur courant et retourne les K extraits les plus pertinents en annexe du prompt système :

```go
recall := recall.NewSQLiteRecall(store, 5)
```

Activez en positionnant `Options.RecallProvider = recall`. Des résultats vides sont sans danger — la boucle continue normalement.

## Exemple d'intégration complet

```go
package main

import (
    "context"
    "fmt"
    "log/slog"
    "os"

    "github.com/sebastienrousseau/rousseau-agent/internal/agent"
    "github.com/sebastienrousseau/rousseau-agent/internal/llm/claudecli"
    "github.com/sebastienrousseau/rousseau-agent/internal/tools"
    "github.com/sebastienrousseau/rousseau-agent/internal/tools/builtin"
)

func main() {
    provider := claudecli.New(claudecli.Config{
        PermissionMode: "bypassPermissions",
    })

    registry := tools.NewRegistry()
    registry.MustRegister(builtin.NewReadTool())
    registry.MustRegister(builtin.NewGrepTool(0, 0))

    ag := agent.New(provider, registry,
        slog.New(slog.NewJSONHandler(os.Stdout, nil)),
        agent.Options{
            SystemPrompt: "You are a careful, concise coding assistant.",
            Approver: &agent.PatternApprover{
                Allow: []agent.PatternRule{
                    {ToolName: "read", Match: ".*"},
                    {ToolName: "grep", Match: ".*"},
                },
                Default: agent.DecisionDeny,
            },
        })

    session := agent.NewSession("hello")
    session.Append(agent.NewUserText("What does main.go do?"))

    reply, err := ag.Turn(context.Background(), session)
    if err != nil {
        fmt.Fprintf(os.Stderr, "turn: %v\n", err)
        os.Exit(1)
    }
    fmt.Println(reply.Content[0].Text)
}
```

Une copie exécutable se trouve dans `examples/embed-agent` dans l'arborescence des sources.

## Dépannage

### `agent: max iterations exceeded`

Le modèle a continué à demander des appels d'outils sans jamais émettre `end_turn`. Causes fréquentes : un outil qui échoue systématiquement (le modèle réessaie avec des variantes), ou une valeur `MaxIterations` trop faible pour une tâche réellement complexe. La valeur par défaut est 32 — passez à 64 pour les gros refactorings. Positionnez `MaxIterations: 0` pour utiliser la valeur par défaut.

### `agent: tool not found: <name>`

Le modèle a émis un bloc `tool_use` nommant un outil absent du registre. Cela signale généralement un prompt système obsolète (l'outil a été retiré mais le modèle s'en souvient encore) ou un outil halluciné. Rousseau remonte cela comme une erreur à l'appelant ; le modèle n'a pas l'occasion de s'adapter. Pour une dégradation gracieuse, encapsulez la recherche dans votre propre dispatcher d'outils.

### Le fournisseur a retourné `end_turn` avec un message vide

Certains fournisseurs retournent `stop_reason=end_turn` sans bloc de contenu — par exemple, lorsque le modèle a choisi de rester silencieux. Rousseau retourne le `Message` vide ; l'appelant décide si « vide » est un résultat valide pour son interface. Les handlers des transports de chat consignent `whatsapp.empty_reply`, `slack.empty_reply`, etc.

### Le résultat d'un outil est tronqué

`Content.ToolResult.Output` est une simple chaîne Go. Certaines implémentations d'outils (notamment `read` sur un très gros fichier) renvoient une sortie plus grande que ce que le modèle peut absorber. Plafonnez la sortie dans l'outil lui-même — l'outil `read` intégré tronque à 200 Ko.

### La compression se déclenche mais le résumé est incohérent

Le prompt de compression par défaut demande un résumé sous forme de liste à puces. Si les résumés du modèle omettent des faits clés, augmentez `KeepRecent` afin que plus de messages survivent tels quels, ou surchargez `CompressionConfig.Prompt` par une instruction propre à la tâche. L'instruction est le levier de l'opérateur — le compresseur ne pilote pas autrement le modèle.

## Pages liées

- [Concepts](/fr/concepts/) — vue d'ensemble de chaque sous-système.
- [Guide utilisateur : Politiques d'approbation](/fr/user-guide/approval-policies/) — sémantique complète des politiques.
- [Guide utilisateur : Outils](/fr/user-guide/tools/) — schémas des outils intégrés.
- [Guide utilisateur : Compression &amp; Rappel](/fr/user-guide/compression-recall/) — internes du compresseur et du rappel FTS5.
- [MCP](/fr/mcp/) — exposer les outils de l'agent aux hôtes externes.

## Lectures complémentaires

- `internal/agent/agent.go` — `Turn`, `runTools`, `systemPrompt`.
- `internal/agent/approver.go` — `PatternApprover`, `AllowAllApprover`, `DenyAllApprover`.
- `internal/agent/compressor.go` — `LLMCompressor` et `NoopCompressor`.
- `internal/agent/recall.go` — `SQLiteRecall` et la forme des requêtes FTS5.
- `internal/agent/stream_turn.go` — variante streaming qui expose la progression token par token.
- `internal/tools/tool.go` — l'interface `Tool`.
- `examples/embed-agent/main.go` — exemple d'intégration exécutable.
