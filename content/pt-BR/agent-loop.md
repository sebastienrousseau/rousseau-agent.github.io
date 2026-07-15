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
hreflang: "pt-BR"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "pt-BR"
locale: "pt_BR"
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
permalink: "https://docs.rousseau-agent.dev/pt-BR/agent-loop/"
subtitle: "Contrato de embedding em biblioteca: Provider, Registry, Session, Turn."
tags: "library, embedding, reference"
title: "Referência do loop do agente"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "library, embedding, agent.Provider, agent.Session, agent.Turn, tool registry, approver, compression, FTS5, recall"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Referência do loop do agente"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 22
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/agent-loop/index.html"
item_link: "https://docs.rousseau-agent.dev/agent-loop/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Referência do loop do agente"
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
twitter_title: "Referência do loop do agente"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Obrigado a cada operador que executa seu próprio agente de codificação."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">O que você vai aprender</span><p>A anatomia completa de um <code>Agent.Turn</code>: como <code>Compressor</code>, <code>SkillsProvider</code> e <code>RecallProvider</code> compõem o system prompt, como os blocos <code>tool_use</code> do modelo passam pelo <code>Approver</code>, como os resultados de ferramenta são incorporados de volta à sessão, e como o loop termina. Leia <code>internal/agent/agent.go</code> junto com esta página.</p></aside>

## rousseau como biblioteca

`rousseau-agent` é tanto uma biblioteca quanto um daemon. O agent loop, o registro de ferramentas e as abstrações de provider não têm dependência da CLI. Você pode compô-los em seu próprio binário sem importar `internal/cli` ou qualquer pacote de transporte.

Todo identificador exportado possui um comentário godoc. `pkg.go.dev/github.com/sebastienrousseau/rousseau-agent` renderiza a referência completa.

## Anatomia de um Turn

A função `Agent.Turn` está definida em `internal/agent/agent.go`. Em prosa, um turn faz o seguinte:

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

### Backpressure e cancelamento

O `ctx` passado ao `Turn` se propaga por tudo: `Compressor.Compress`, todo `Provider.Complete`, todo `Tool.Execute` e todo `Approver.Approve`. Cancele o contexto para abortar no meio do turn — a chamada de provider da iteração atual retorna `context.Canceled`, a sessão fica com a última mensagem completa do modelo mais a chamada de ferramenta pendente, e os chamadores decidem se tentam novamente.

A `BashTool` nativa envolve cada comando em seu próprio `context.WithTimeout` (padrão 60s, configurável) para que um comando descontrolado não possa exceder o contexto externo.

### Composição do system prompt

`systemPrompt(ctx, session)` em `agent.go` linha 138 monta até três partes:

```
<Options.SystemPrompt>

<SkillsProvider.SystemAppendix(session)>

<RecallProvider.SystemAppendix(ctx, session)>
```

Qualquer parte que retorne vazia é omitida. O resultado é `strings.Join(parts, "\n\n")`. A composição acontece uma vez por iteração (não por turn), de modo que skills e recall reagem à mensagem mais recente — incluindo resultados intermediários de ferramenta, quando relevante.

### Gerenciamento da janela de contexto

Sessões grandes eventualmente excedem a janela de contexto do modelo. O Rousseau não trunca por conta própria — isso é trabalho do `Compressor`. O `NoopCompressor` padrão nunca reescreve, então embedders que queiram uma transcrição ilimitada em uma janela pequena precisam fornecer seu próprio compressor ou aceitar o erro do lado do modelo quando a janela encher.

`LLMCompressor` (veja abaixo) colapsa mensagens mais antigas que `KeepRecent` em um único bloco de resumo quando a contagem passa `TriggerMessages`. O resumo é gerado pelo mesmo provider que executa o turn, então custa um completion extra por ciclo de compressão.

## A interface Provider

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

`Complete` executa um único turn não-streaming. `Request` carrega `SessionID`, `System`, `Messages`, `Tools` e `CacheableMessages` (uma dica de cache efêmero). `Response` retorna uma única `Message` do assistant, um `StopReason` (`end_turn`, `tool_use`, `max_tokens`, `other`) e contagens de tokens `Usage`.

Todo provider incluído (Anthropic, Bedrock, Vertex, compatível com OpenAI, claudecli) implementa `Provider`. Todos exceto `claudecli` implementam `StreamingProvider`.

## Session, Message, Turn

`internal/agent/session.go` e `internal/agent/message.go`:

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

Uma `Session` é append-only. Cada mensagem do usuário é uma chamada a `Agent.Turn(ctx, session)`; o agent loop muta a sessão in loco e retorna a `Message` final do assistant.

## Registrando ferramentas

`internal/tools`:

```go
registry := tools.NewRegistry()
registry.MustRegister(builtin.NewReadTool())
registry.MustRegister(builtin.NewGrepTool(0, 0))
registry.MustRegister(builtin.NewEditTool())
```

Toda ferramenta declara um schema JSON estrito. Adicionar a sua é uma implementação de `Tool`:

```go
type Tool interface {
    Name() string
    Description() string
    InputSchema() json.RawMessage
    Execute(ctx context.Context, input json.RawMessage) (string, error)
}
```

`MustRegister` faz panic em caso de nomes duplicados; use `Register` e verifique o erro se você monta o registro dinamicamente.

## Políticas de aprovação

`internal/agent/approver.go`. Três políticas nativas:

- `AllowAllApprover` — toda chamada roda.
- `DenyAllApprover{Reason: "…"}` — toda chamada é bloqueada com a razão informada.
- `PatternApprover{Allow: []PatternRule, Deny: []PatternRule, Default: Decision}` — allow/deny por regex e ferramenta. Deny vence; requisições sem match usam `Default` (vazio → `DecisionDeny`).

As regras por padrão são compiladas preguiçosamente uma vez. Erros de compilação aparecem como `DecisionDeny` com a string de erro como razão, então uma regex malformada falha de forma segura.

Approvers customizados implementam:

```go
type Approver interface {
    Approve(ctx context.Context, req ApprovalRequest) (Decision, string)
}
```

`ApprovalRequest` carrega `ToolName`, o JSON bruto de `Input` e `SessionID`. Retorne `DecisionAllow` ou `DecisionDeny` mais uma string de razão (exposta de volta ao modelo como um erro `tool_result`).

## Compressão

`internal/agent/compressor.go`. `LLMCompressor` chama o mesmo provider para resumir mensagens mais antigas quando a sessão cruza um limite:

```go
compressor, err := agent.NewLLMCompressor(agent.LLMCompressorConfig{
    Provider:        provider,
    TriggerMessages: 60,
    KeepRecent:      8,
})
```

As `KeepRecent` mensagens mais recentes sobrevivem literais; tudo mais antigo colapsa em um único bloco de resumo. O `Compressor` define `CacheableMessages` na próxima requisição para que o resumo esteja cache-hot logo no turn seguinte.

`NoopCompressor` é o padrão quando `Compressor` é nil.

## Recall entre sessões via FTS5

`internal/agent/recall.go` + `internal/state/sqlite/`. O índice FTS5 do session store cobre cada mensagem. `SQLiteRecall` consulta contra a mensagem atual do usuário e retorna os top-K trechos mais relevantes como um apêndice do system prompt:

```go
recall := recall.NewSQLiteRecall(store, 5)
```

Habilite definindo `Options.RecallProvider = recall`. Resultados vazios são seguros — o loop segue normalmente.

## Exemplo de embed completo

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
            SystemPrompt: "Você é um assistente de codificação cauteloso e conciso.",
            Approver: &agent.PatternApprover{
                Allow: []agent.PatternRule{
                    {ToolName: "read", Match: ".*"},
                    {ToolName: "grep", Match: ".*"},
                },
                Default: agent.DecisionDeny,
            },
        })

    session := agent.NewSession("hello")
    session.Append(agent.NewUserText("O que o main.go faz?"))

    reply, err := ag.Turn(context.Background(), session)
    if err != nil {
        fmt.Fprintf(os.Stderr, "turn: %v\n", err)
        os.Exit(1)
    }
    fmt.Println(reply.Content[0].Text)
}
```

Uma cópia executável está em `examples/embed-agent` na árvore de código.

## Solução de problemas

### `agent: max iterations exceeded`

O modelo continuou pedindo chamadas de ferramenta sem nunca emitir `end_turn`. Causas comuns: uma ferramenta que sempre falha (o modelo continua tentando variações), ou um valor de `MaxIterations` baixo demais para uma tarefa genuinamente complexa. O padrão é 32 — aumente para 64 em refatorações grandes. Defina `MaxIterations: 0` para usar o padrão.

### `agent: tool not found: <name>`

O modelo emitiu um bloco `tool_use` nomeando uma ferramenta que não está no registro. Geralmente indica um system prompt desatualizado (a ferramenta foi removida mas o modelo ainda a lembra), ou uma ferramenta alucinada. O Rousseau expõe isso como erro ao chamador; o modelo não recebe chance de se adaptar. Se você quiser degradação graciosa, encapsule a busca no registro em seu próprio dispatcher de ferramentas.

### Provider retornou `end_turn` com uma mensagem vazia

Alguns providers retornam `stop_reason=end_turn` sem blocos de conteúdo — por exemplo, quando o modelo escolheu ficar em silêncio. O Rousseau retorna a `Message` vazia; o chamador decide se "vazio" é um resultado válido para sua UI. Os handlers de transportes de chat registram `whatsapp.empty_reply`, `slack.empty_reply`, etc.

### O resultado da ferramenta está truncado

`Content.ToolResult.Output` é uma string Go simples. Algumas implementações de ferramenta (notadamente `read` em um arquivo enorme) retornam saída maior do que o modelo consegue absorver. Limite a saída na própria ferramenta — a ferramenta `read` nativa trunca em 200 KB.

### A compressão dispara, mas o resumo não faz sentido

O prompt de compressão padrão pede um resumo em bullets. Se os resumos do modelo estão perdendo fatos importantes, aumente `KeepRecent` para que mais mensagens sobrevivam literais, ou sobrescreva `CompressionConfig.Prompt` com uma instrução específica da tarefa. A instrução é a alavanca do operador — o compressor não guia o modelo de outra forma.

## Páginas relacionadas

- [Conceitos](/pt-BR/concepts/) — visão geral de cada subsistema.
- [Guia do usuário: Políticas de aprovação](/pt-BR/user-guide/approval-policies/) — semântica completa das políticas.
- [Guia do usuário: Ferramentas](/pt-BR/user-guide/tools/) — schemas das ferramentas nativas.
- [Guia do usuário: Compressão &amp; Recall](/pt-BR/user-guide/compression-recall/) — internals do compressor e do recall FTS5.
- [MCP](/pt-BR/mcp/) — expondo as ferramentas do agente para hosts externos.

## Leitura adicional

- `internal/agent/agent.go` — `Turn`, `runTools`, `systemPrompt`.
- `internal/agent/approver.go` — `PatternApprover`, `AllowAllApprover`, `DenyAllApprover`.
- `internal/agent/compressor.go` — `LLMCompressor` e `NoopCompressor`.
- `internal/agent/recall.go` — `SQLiteRecall` e o formato da consulta FTS5.
- `internal/agent/stream_turn.go` — variante em streaming que expõe progresso token a token.
- `internal/tools/tool.go` — a interface `Tool`.
- `examples/embed-agent/main.go` — exemplo executável de embedding.
