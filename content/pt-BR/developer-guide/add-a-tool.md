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
description: "How to add a new built-in tool to rousseau-agent: declare a JSON schema, implement Execute, register with the tool registry."
keywords: "add tool, tool registry, json schema, execute, extend, custom tool"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/developer-guide/add-a-tool/"
subtitle: "Schema, Execute, register — three moving parts."
tags: "developer-guide, tools, extend"
title: "Adicionar uma ferramenta"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add tool, tool registry, json schema, execute, extend, custom tool"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Adicionar uma ferramenta"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 64
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-tool/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-tool/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Adicionar uma ferramenta"
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
twitter_title: "Adicionar uma ferramenta"
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

`internal/tools/tool.go` (parafraseado):

```go
type Tool interface {
    Name() string
    Description() string
    InputSchema() map[string]any
    Execute(ctx context.Context, input json.RawMessage) (string, error)
}
```

Quatro métodos, sem ciclo de vida. Ferramentas são stateless da perspectiva do loop — qualquer estado que a ferramenta precisa (um cache de regex compilada, um índice in-process) é um campo privado no tipo concreto.

## Skeleton para uma nova ferramenta

Vamos adicionar uma ferramenta **`http_get`** hipotética que faz fetch de uma URL e retorna seu body.

### Passo 1 — O tipo

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

### Passo 2 — Metadata

```go
// Name satisfies tools.Tool.
func (*HTTPGetTool) Name() string { return "http_get" }

// Description satisfies tools.Tool.
func (*HTTPGetTool) Description() string {
    return "Fetch an HTTPS URL and return the response body. Input: url (string). Redirects are followed up to 10 hops. Response is capped at 1 MiB."
}
```

A **description é voltada ao modelo**. Deve se ler como uma docstring curta para outro engenheiro — o que a ferramenta faz, o que as entradas significam, qual a forma da saída.

### Passo 3 — Schema de entrada

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

Mantenha o schema estrito. Cada property recebe uma `description`. O array `required` é reforçado pelo validador de tool-use do modelo — campos faltantes causam um retry de `tool_use`, não um erro de runtime.

### Passo 4 — Execute

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

### Passo 5 — Registro

Conecte em `internal/cli/chat.go` (e cada outro comando que constrói um registry — faça grep por `registry.MustRegister` para encontrá-los):

```go
registry.MustRegister(builtin.NewHTTPGetTool(30 * time.Second))
```

Uma vez registrada, a ferramenta fica disponível ao modelo em cada turno.

### Passo 6 — Testes

Siga `internal/tools/builtin/read_test.go` para o padrão:

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

### Passo 7 — Política de aprovação

A ferramenta agora está disponível ao modelo, sujeita à [política de aprovação](/pt-BR/user-guide/approval-policies/). Recomende uma regra de deny nos docs para a postura padrão:

```yaml
deny:
  - {tool: http_get, match: "\"url\":\"https://(169\\.254|10\\.|192\\.168\\.|172\\.(1[6-9]|2[0-9]|3[01])\\.)"}
```

Isso bloqueia a ferramenta de chamar AWS IMDS ou espaço privado RFC1918 — um pedido comum para ferramentas de HTTP fetching.

### Passo 8 — Docs

Adicione uma seção a `content/user-guide/tools.md` descrevendo a nova ferramenta: schema, semântica, notas de segurança. Siga a forma das cinco ferramentas existentes.

## Detalhes do contrato

- **Statelessness**: `Execute` não deve carregar estado entre calls que não seja explicitamente privado aos campos da própria ferramenta. Dois turnos concorrentes em duas sessões podem chamar a mesma ferramenta simultaneamente.
- **Respeito ao context**: `Execute` deve honrar o cancelamento de `ctx`. Trabalho de longa duração deve checar `ctx.Err()` periodicamente ou rotear o trabalho por uma chamada de biblioteca ciente de context.
- **Sem panics**: retorne erros no lugar. O agent loop converte um erro em um `tool_result` com `IsError: true`, ao qual o modelo pode se adaptar.
- **Formato de retorno**: a saída é uma string simples, alimentada de volta ao modelo no próximo turno. Inclua estrutura suficiente (por exemplo, números de linha, códigos de status) para o modelo raciocinar sobre ela.

## Ferramentas customizadas sem tocar no source

Se você não quer fazer fork do rousseau, embuta o agent loop no seu próprio binário e registre suas ferramentas ali:

```go
registry := tools.NewRegistry()
registry.MustRegister(builtin.NewReadTool())
registry.MustRegister(builtin.NewWriteTool())
// ...
registry.MustRegister(mypkg.NewMyTool())

ag := agent.New(provider, registry, logger, agent.Options{})
```

Veja `examples/embed-agent/` na árvore de código para um exemplo de embedding completo.

## Armadilhas comuns

- **Schema muito amplo.** Exigir apenas `type: object` não dá ajuda ao modelo. Enumere cada property, descreva cada campo.
- **Bloquear em I/O sem um deadline.** Sempre use `NewRequestWithContext`, sempre defina um `http.Client{Timeout: ...}`, sempre honre `ctx`.
- **Retornar demais.** A saída é alimentada de volta ao modelo no próximo turno. Uma resposta de 1 MB queima tokens; limite.
- **Efeitos colaterais escapando.** Uma ferramenta que muta o mundo deve logar o que fez na string de retorno para que a trilha de auditoria do approver seja completa.
- **Esquecer a checagem de interface em compile time.** `var _ tools.Tool = (*MyTool)(nil)` no escopo do pacote pega interface drift em build time.

## Próximo

- [Guia do usuário: Tools](/pt-BR/user-guide/tools/) — as cinco ferramentas embutidas com schemas.
- [Guia do usuário: Políticas de Aprovação](/pt-BR/user-guide/approval-policies/) — como controlar a nova ferramenta.
- [Testing](/pt-BR/developer-guide/testing/) — o padrão para testes de ferramenta.
