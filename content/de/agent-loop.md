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
hreflang: "de"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "de"
locale: "de_DE"
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
permalink: "https://docs.rousseau-agent.dev/de/agent-loop/"
subtitle: "Vertrag für Library-Einbettung: Provider, Registry, Session, Turn."
tags: "library, embedding, reference"
title: "Agent-Loop-Referenz"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "library, embedding, agent.Provider, agent.Session, agent.Turn, tool registry, approver, compression, FTS5, recall"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Agent-Loop-Referenz"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 22
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/agent-loop/index.html"
item_link: "https://docs.rousseau-agent.dev/agent-loop/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Agent-Loop-Referenz"
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
twitter_title: "Agent-Loop-Referenz"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Danke an jeden Operator, der seinen eigenen Coding-Agenten betreibt."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">Was Sie lernen</span><p>Die vollständige Anatomie eines <code>Agent.Turn</code>: wie <code>Compressor</code>, <code>SkillsProvider</code> und <code>RecallProvider</code> den System-Prompt komponieren, wie die <code>tool_use</code>-Blöcke des Modells den <code>Approver</code> durchlaufen, wie Tool-Ergebnisse in die Session zurückgeführt werden und wie die Schleife terminiert. Lesen Sie <code>internal/agent/agent.go</code> begleitend zu dieser Seite.</p></aside>

## rousseau als Bibliothek

`rousseau-agent` ist ebenso Bibliothek wie Daemon. Der Agent-Loop, die Tool-Registry und die Provider-Abstraktionen haben keine CLI-Abhängigkeit. Sie können sie in Ihr eigenes Binary integrieren, ohne `internal/cli` oder ein Transport-Paket zu importieren.

Jeder exportierte Identifier trägt einen godoc-Kommentar. `pkg.go.dev/github.com/sebastienrousseau/rousseau-agent` rendert die vollständige Referenz.

## Anatomie eines Turns

Die Funktion `Agent.Turn` ist in `internal/agent/agent.go` definiert. In Prosa führt ein Turn Folgendes aus:

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

### Backpressure und Abbruch

Der an `Turn` übergebene `ctx` wird durch alles hindurchgereicht: `Compressor.Compress`, jeden `Provider.Complete`, jeden `Tool.Execute` und jeden `Approver.Approve`. Kontext abbrechen, um mitten im Turn zu terminieren — der Provider-Aufruf der aktuellen Iteration liefert `context.Canceled`, in der Session verbleiben die letzte vollständige Nachricht des Modells sowie der ausstehende Tool-Aufruf, und die Aufrufer können entscheiden, ob ein Retry erfolgt.

Das eingebaute `BashTool` umschließt jeden Befehl mit einem eigenen `context.WithTimeout` (Standard 60s, konfigurierbar), sodass ein außer Kontrolle geratener Befehl den äußeren Kontext nicht überschreiten kann.

### System-Prompt-Komposition

`systemPrompt(ctx, session)` in `agent.go`, Zeile 138, setzt bis zu drei Teile zusammen:

```
<Options.SystemPrompt>

<SkillsProvider.SystemAppendix(session)>

<RecallProvider.SystemAppendix(ctx, session)>
```

Jeder leer zurückgegebene Teil wird ausgelassen. Das Ergebnis ist `strings.Join(parts, "\n\n")`. Die Komposition erfolgt einmal pro Iteration (nicht pro Turn), sodass Skills und Recall auf die jeweils aktuellste Nachricht reagieren — einschließlich zwischenzeitlicher Tool-Ergebnisse, sofern relevant.

### Verwaltung des Kontextfensters

Große Sessions überschreiten irgendwann das Kontextfenster des Modells. Rousseau kürzt nicht von selbst — das ist Aufgabe des `Compressor`. Der Default-`NoopCompressor` schreibt niemals um; Embedder, die ein unbegrenztes Transkript in einem kleinen Fenster halten möchten, müssen entweder einen eigenen Kompressor bereitstellen oder den modellseitigen Fehler beim Vollaufen des Fensters akzeptieren.

`LLMCompressor` (siehe unten) fasst Nachrichten, die älter als `KeepRecent` sind, in einem einzigen Summary-Block zusammen, sobald die Anzahl `TriggerMessages` überschreitet. Die Zusammenfassung wird vom selben Provider erzeugt, der den Turn ausführt, und kostet somit pro Kompressionszyklus eine zusätzliche Completion.

## Das Provider-Interface

`internal/agent/provider.go`:

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

`Complete` führt einen einzelnen, nicht streamenden Turn aus. `Request` trägt `SessionID`, `System`, `Messages`, `Tools` und `CacheableMessages` (ein Ephemeral-Cache-Hinweis). `Response` liefert eine einzelne Assistant-`Message`, einen `StopReason` (`end_turn`, `tool_use`, `max_tokens`, `other`) und `Usage`-Tokenzahlen.

Jeder ausgelieferte Provider (Anthropic, Bedrock, Vertex, OpenAI-kompatibel, claudecli) implementiert `Provider`. Jeder außer `claudecli` implementiert `StreamingProvider`.

## Session, Message, Turn

`internal/agent/session.go` und `internal/agent/message.go`:

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

Eine `Session` ist append-only. Jede Benutzernachricht ist ein Aufruf von `Agent.Turn(ctx, session)`; der Agent-Loop verändert die Session in-place und liefert die abschließende Assistant-`Message` zurück.

## Tools registrieren

`internal/tools`:

```go
registry := tools.NewRegistry()
registry.MustRegister(builtin.NewReadTool())
registry.MustRegister(builtin.NewGrepTool(0, 0))
registry.MustRegister(builtin.NewEditTool())
```

Jedes Tool deklariert ein striktes JSON-Schema. Ein eigenes Tool anzulegen bedeutet, eine `Tool`-Implementierung bereitzustellen:

```go
type Tool interface {
    Name() string
    Description() string
    InputSchema() json.RawMessage
    Execute(ctx context.Context, input json.RawMessage) (string, error)
}
```

`MustRegister` panict bei doppelten Namen; wenn Sie die Registry dynamisch aufbauen, `Register` verwenden und den Fehler auswerten.

## Genehmigungsrichtlinien

`internal/agent/approver.go`. Drei eingebaute Richtlinien:

- `AllowAllApprover` — jeder Aufruf wird ausgeführt.
- `DenyAllApprover{Reason: "…"}` — jeder Aufruf wird mit dem angegebenen Grund blockiert.
- `PatternApprover{Allow: []PatternRule, Deny: []PatternRule, Default: Decision}` — Regex-Allow/Deny pro Tool. Deny gewinnt; nicht gematchte Anfragen nutzen `Default` (leer → `DecisionDeny`).

Pattern-Regeln werden einmalig lazy kompiliert. Kompilierfehler werden als `DecisionDeny` mit der Fehlermeldung als Grund weitergereicht, sodass ein fehlerhaftes Regex fail-safe ausfällt.

Eigene Approver implementieren:

```go
type Approver interface {
    Approve(ctx context.Context, req ApprovalRequest) (Decision, string)
}
```

`ApprovalRequest` trägt `ToolName`, das rohe `Input`-JSON und `SessionID`. Rückgabe: `DecisionAllow` oder `DecisionDeny` plus ein Grund-String (wird dem Modell als `tool_result`-Fehler zurückgegeben).

## Kompression

`internal/agent/compressor.go`. `LLMCompressor` ruft denselben Provider auf, um ältere Nachrichten zusammenzufassen, sobald die Session einen Schwellwert überschreitet:

```go
compressor, err := agent.NewLLMCompressor(agent.LLMCompressorConfig{
    Provider:        provider,
    TriggerMessages: 60,
    KeepRecent:      8,
})
```

Die neuesten `KeepRecent` Nachrichten überleben unverändert; alles Ältere wird zu einem einzigen Summary-Block zusammengefasst. Der `Compressor` setzt `CacheableMessages` beim nächsten Request, sodass die Zusammenfassung bereits im nächsten Turn cache-heiß ist.

`NoopCompressor` ist der Default, wenn `Compressor` `nil` ist.

## FTS5-Recall über Sessions hinweg

`internal/agent/recall.go` + `internal/state/sqlite/`. Der FTS5-Index des Session-Stores erfasst jede Nachricht. `SQLiteRecall` sucht gegen die aktuelle Benutzernachricht und liefert die Top-K relevantesten Snippets als System-Prompt-Anhang:

```go
recall := recall.NewSQLiteRecall(store, 5)
```

Aktivieren durch Setzen von `Options.RecallProvider = recall`. Leere Ergebnisse sind unproblematisch — die Schleife läuft normal weiter.

## Vollständiges Embedding-Beispiel

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

Ein lauffähiges Exemplar liegt im Source-Tree unter `examples/embed-agent`.

## Troubleshooting

### `agent: max iterations exceeded`

Das Modell forderte fortlaufend Tool-Aufrufe an, ohne jemals `end_turn` auszugeben. Häufige Ursachen: ein Tool, das immer fehlschlägt (das Modell wiederholt mit Variationen), oder ein für eine tatsächlich komplexe Aufgabe zu niedriger `MaxIterations`-Wert. Standard ist 32 — für große Refactorings auf 64 erhöhen. `MaxIterations: 0` verwendet den Default.

### `agent: tool not found: <name>`

Das Modell emittierte einen `tool_use`-Block mit einem Tool-Namen, der nicht in der Registry steht. Deutet meist auf einen veralteten System-Prompt (Tool entfernt, aber vom Modell noch erinnert) oder ein halluziniertes Tool hin. Rousseau meldet dies dem Aufrufer als Fehler; das Modell erhält keine Gelegenheit zur Anpassung. Für eine sanfte Degradation den Registry-Lookup in einen eigenen Tool-Dispatcher verpacken.

### Provider lieferte `end_turn` mit leerer Nachricht

Manche Provider geben `stop_reason=end_turn` ohne Content-Blöcke zurück — etwa, wenn das Modell schweigen wollte. Rousseau liefert die leere `Message`; der Aufrufer entscheidet, ob "leer" ein gültiges Ergebnis für die eigene UI ist. Die Chat-Transport-Handler loggen `whatsapp.empty_reply`, `slack.empty_reply` usw.

### Tool-Ergebnis ist abgeschnitten

`Content.ToolResult.Output` ist ein einfacher Go-String. Manche Tool-Implementierungen (insbesondere `read` auf einer sehr großen Datei) liefern mehr Ausgabe zurück, als das Modell verarbeiten kann. Die Ausgabe im Tool selbst begrenzen — das eingebaute `read`-Tool kürzt bei 200 KB.

### Kompression läuft, aber die Zusammenfassung ergibt keinen Sinn

Der Default-Compression-Prompt bittet um eine Bullet-Liste. Fehlen in den Zusammenfassungen wichtige Fakten, entweder `KeepRecent` erhöhen (damit mehr Nachrichten unverändert erhalten bleiben) oder `CompressionConfig.Prompt` mit einer aufgabenspezifischen Anweisung überschreiben. Die Anweisung ist der Hebel des Operators — der Kompressor lenkt das Modell ansonsten nicht.

## Verwandte Seiten

- [Konzepte](/de/concepts/) — Überblick über jedes Subsystem.
- [Benutzerhandbuch: Genehmigungsrichtlinien](/de/user-guide/approval-policies/) — vollständige Richtlinien-Semantik.
- [Benutzerhandbuch: Tools](/de/user-guide/tools/) — Schemata der eingebauten Tools.
- [Benutzerhandbuch: Kompression &amp; Recall](/de/user-guide/compression-recall/) — Interna des Kompressors und des FTS5-Recall.
- [MCP](/de/mcp/) — die Tools des Agents externen Hosts zugänglich machen.

## Weiterführende Literatur

- `internal/agent/agent.go` — `Turn`, `runTools`, `systemPrompt`.
- `internal/agent/approver.go` — `PatternApprover`, `AllowAllApprover`, `DenyAllApprover`.
- `internal/agent/compressor.go` — `LLMCompressor` und `NoopCompressor`.
- `internal/agent/recall.go` — `SQLiteRecall` und die FTS5-Query-Struktur.
- `internal/agent/stream_turn.go` — Streaming-Variante, die Token-für-Token-Fortschritt sichtbar macht.
- `internal/tools/tool.go` — das `Tool`-Interface.
- `examples/embed-agent/main.go` — lauffähiges Embedding-Beispiel.
