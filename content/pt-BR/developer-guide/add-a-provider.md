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
changefreq: "monthly"
description: "How to add a sixth LLM provider to rousseau-agent: implement Provider.Complete and optionally StreamingProvider.CompleteStream."
keywords: "add provider, llm, chat completion, streaming, agent provider, extend"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/developer-guide/add-a-provider/"
subtitle: "Provider.Complete and StreamingProvider.CompleteStream."
tags: "developer-guide, provider, llm, extend"
title: "Adicionar um provedor"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add provider, llm, chat completion, streaming, agent provider, extend"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Adicionar um provedor"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 63
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-provider/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-provider/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Adicionar um provedor"
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
twitter_title: "Adicionar um provedor"
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

## A interface

`internal/agent/provider.go` (parafraseado):

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

Cada adapter de LLM satisfaz pelo menos `Provider`. `StreamingProvider` é opt-in — a TUI e os handlers de chat-transport fazem fallback para o caminho não-streaming quando um provider não o implementa.

`StopReason` é um de `StopEndTurn`, `StopToolUse`, `StopMaxTokens`. O agent loop trata `StopEndTurn` como terminal e `StopToolUse` como "o modelo quer uma tool call".

## Skeleton para um novo provider

Vamos adicionar um provider hipotético **Cohere Command R**.

### Passo 1 — Diretório

```
internal/llm/cohere/
├── client.go        # Config, New
├── complete.go      # Provider.Complete
├── stream.go        # StreamingProvider.CompleteStream (optional)
└── *_test.go
```

### Passo 2 — `client.go`

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

### Passo 3 — `complete.go`

Implemente `Complete`:

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

Os corpos `encodeRequest`, `decodeResponse` e o formato `cohereResponse` são específicos do Cohere — eles traduzem os tipos agnósticos de provider `agent.Request` e `agent.Response` do rousseau de e para o wire format do Cohere.

### Passo 4 — Streaming (opcional)

Se o Cohere suporta streaming estilo SSE, implemente `CompleteStream`. Pule na primeira passada; o agent loop faz fallback para não-streaming automaticamente.

### Passo 5 — Superfície de config

Adicione `CohereConfig` a `internal/config/config.go`:

```go
type CohereConfig struct {
    APIKey    string `mapstructure:"api_key"`
    Model     string `mapstructure:"model"`
    BaseURL   string `mapstructure:"base_url"`
    MaxTokens int64  `mapstructure:"max_tokens"`
}
```

Adicione um campo a `Config`:

```go
Cohere CohereConfig `mapstructure:"cohere"`
```

Estenda `setDefaults` com um padrão sensato de modelo:

```go
v.SetDefault("cohere.model", "command-r-plus")
```

### Passo 6 — Wire-up de CLI

Em `internal/cli/provider.go`, estenda `buildProvider(cfg *config.Config)`:

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

Estenda `rousseau doctor` (`internal/cli/doctor.go`) para adicionar um bloco de checagem `provider.cohere.*` quando `cfg.Provider == "cohere"`. Espelhe as checagens existentes de anthropic.

## Detalhes do contrato que o agent loop assume

- **`Complete` respeita `ctx`.** Requests HTTP longos devem honrar o cancelamento de context, ou o shutdown de `SIGTERM` do daemon vai travar.
- **Round-trip de tool-use.** Quando o modelo emite blocos `tool_use`, o `StopReason` da resposta deve ser `StopToolUse` e o conteúdo da mensagem deve incluir `Content{Kind: ContentToolUse, ToolUse: &ToolUse{Name, Input, ID}}` para cada call solicitada. O agent loop roteia cada uma para o `Registry`, executa, e faz pipe dos resultados de volta na próxima call `Complete`.
- **Manejo de `tool_result`.** Na próxima call, `req.Messages` contém uma mensagem de usuário cujo conteúdo inclui `Content{Kind: ContentToolResult, ToolResult: &ToolResult{ToolUseID, Output, IsError}}` para cada call executada. O provider deve renderizar essas na forma que a API upstream espera.
- **Checagem de interface em compile time.** `var _ agent.Provider = (*Provider)(nil)` no escopo do pacote pega interface drift em build time.

## Contrato de streaming

Se você implementa `StreamingProvider`:

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

A TUI e os handlers de chat-transport leem deltas conforme chegam; a `Response` final é usada para anexar a mensagem de assistente completamente formada à sessão.

## Prompt caching

`internal/llm/anthropic` coloca marcadores `cache_control` nas duas últimas mensagens do request. Se seu provider suporta prompt caching, faça o mesmo — transforma compressão + recall (veja [Compressão + Recall](/pt-BR/user-guide/compression-recall/)) de um padrão que consome tokens para um barato.

## Testing

Use `httptest.NewServer` para levantar um upstream fake. `internal/llm/anthropic/*_test.go` é a referência. O padrão:

1. Inicie `httptest.NewServer` com um handler que retorna JSON canned.
2. Construa o provider apontando `BaseURL` para o test server.
3. Chame `Complete` com um `Request` canned.
4. Faça assert no formato de `Response` retornado.

Para streaming, `httptest` também suporta Server-Sent Events — veja `internal/llm/anthropic/stream.go`.

## Docs

Adicione `content/providers/cohere.md` neste docs site. Siga a forma de `content/providers/anthropic.md` — descrição, superfície de config, detalhes de auth, ressalvas específicas do provider.

## Armadilhas comuns

- **Reescrever `Messages` silenciosamente.** O agent loop é a fonte da verdade para o estado da conversa. Providers devem traduzir a forma sem mutar a semântica.
- **Perder IDs de tool-use.** Cada `ToolUse.ID` em uma resposta deve casar com um `ToolResult.ToolUseID` no próximo request. Se seu provider atribui seus próprios IDs, traduza com cuidado.
- **Ignorar `MaxTokens`.** Alguns providers rejeitam requests sem um limite explícito. Defina um padrão sensato em `New`.
- **Bloquear o loop com políticas de retry.** Retries pertencem ao adapter do provider, não ao agent loop. Limite; falhar rápido é melhor que travar.

## Próximo

- [Testing](/pt-BR/developer-guide/testing/) — como escrever o `_test.go` do provider.
- [Adicionar uma ferramenta](/pt-BR/developer-guide/add-a-tool/) — o menor ponto de extensão.
- [Configuração](/pt-BR/configuration/) — a superfície de config que cada provider expõe.
