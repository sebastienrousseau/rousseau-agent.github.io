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
description: "Testing pattern for rousseau-agent: dependency injection via interfaces (WSConn, IMAPClient, HTTPClient), fake generators, race + coverage thresholds."
keywords: "testing, dependency injection, fake, mock, coverage, race, go test, httptest"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/developer-guide/testing/"
subtitle: "Dependency injection, fakes, race, coverage."
tags: "developer-guide, testing, di, fakes"
title: "Testes"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "testing, dependency injection, fake, mock, coverage, race, go test, httptest"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Testes"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 65
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/testing/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/testing/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Testes"
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
twitter_title: "Testes"
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

## O padrão

Cada pacote que fala com o mundo externo define uma pequena interface para sua dependência, toma essa interface como parâmetro de construtor e injeta um cliente real em `cli/*.go` (produção) ou um fake em `*_test.go` (testes).

Exemplos na árvore:

| Pacote | Interface | Real | Fake para testes |
|---|---|---|---|
| `internal/transport/whatsapp` | `WSConn` | WebSocket do whatsmeow | struct em memória com um canal `send` |
| `internal/transport/email` | `IMAPClient` | cliente `emersion/go-imap` | canal roteirizado de mensagens |
| `internal/transport/whatsapp` | `Sender` | send direto do whatsmeow | slice em memória para assertion |
| `internal/llm/*` | `HTTPClient` (indireto via `http.Client`) | `http.DefaultTransport` | `httptest.NewServer` |
| `internal/state/sqlite` | `state.Store` (interface dona do `state`) | `modernc.org/sqlite` em disco | DSN em memória `:memory:` |
| `internal/agent` | `Provider`, `Approver`, `Compressor`, `RecallProvider` | tipos concretos `llm/*` | implementações struct em `_test.go` |

A regra: **interface com o consumidor, implementação com o provedor.** `Provider` é definida em `agent`, não em `llm/anthropic`. `Store` é definida em `state`, não em `state/sqlite`.

## Rodando o gate

```sh
make check
```

é equivalente a:

```sh
go vet ./...
golangci-lint run
go test -race -count=1 -covermode=atomic ./...
govulncheck ./...
```

O CI roda o mesmo comando em `ubuntu-latest` e `macos-latest`. Se passa localmente, passa no CI — exceto bugs específicos de plataforma, razão pela qual macOS está na matriz.

## Race detector

`-race` é inegociável. Cada daemon no rousseau envolve múltiplas goroutines (pump de transporte, agent loop, cron scheduler, escritor do session store). Uma race em qualquer uma delas é um bug real.

Se você achar um teste que só falha sob `-race`, isso é um bug no código sob teste, não no teste. Não desabilite `-race`.

## Floor de cobertura

O floor atual de cobertura é **75% total**. Pacotes core (`internal/agent`, `internal/tools`, `internal/state/sqlite`) ficam em 85–100% e são mantidos ali pela suíte de teste pré-existente; novo código nesses pacotes não deve abaixá-los.

Um job de CI roda após `go test -race -covermode=atomic ./... -coverprofile=coverage.out` e inspeciona `coverage.out`. Falhar o floor falha o build.

## Geradores de fake

O rousseau não usa uma biblioteca de geração de mocks. Fakes são tipos struct escritos à mão, pequenos o suficiente para ler de um olhar:

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

Duas propriedades caem daí:

1. O fake é inspecionável — `calls` captura cada request, então assertions podem checar o que o código sob teste emitiu.
2. O fake é determinístico — respostas canned são consumidas em ordem.

## `httptest` para providers em forma HTTP

Cada adapter de LLM que fala HTTP usa `httptest.NewServer` para testes:

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

Para streaming estilo SSE, a mesma técnica funciona — `http.Flusher` está disponível no response writer.

## Corpus de fuzz

Cada parser tem uma função `Fuzz*`. Rode a bateria completa:

```sh
make fuzz
```

Sob o CI, fuzz roda por um tempo limitado (`-fuzztime`). Localmente, rode mais tempo para semear o corpus.

## Testes table-driven

Os testes do rousseau se apoiam pesadamente na forma table-driven. Formato de exemplo:

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

Isso escala — cada nova forma de regra vira uma linha de tabela.

## Vazamento de goroutines

Testes que fazem spawn de goroutines devem juntá-las. Padrões comuns:

- Use `context.WithCancel` e `cancel()` no final do teste.
- Use um `sync.WaitGroup` e `wg.Wait()`.
- Consuma cada canal até `close`.

Se um teste vaza uma goroutine, `go test -race` pode pegar via um nil-receiver panic na goroutine vazada depois que o `main` do arquivo de teste saiu. Mais barato ser disciplinado desde o início.

## Tempo determinístico

Para testes sensíveis a tempo (cron, ranqueamento de recência de recall), injete um provider de `time.Time`:

```go
type Clock interface {
    Now() time.Time
}
```

Conecte o `time.Now` real em `cli/*` e um `time.Time` fake no teste. O scheduler `internal/cron/scheduler.go` usa esse padrão.

## Testando a TUI

`internal/tui/model_test.go` usa o helper `TestModel` do `bubbletea`. `View()` é uma função pura de string do modelo, então a maioria das assertions vira "rode este update, espere esta saída de View".

## O que não testar

- Bibliotecas de terceiros. O rousseau não sombreia os testes upstream do whatsmeow ou `signal-cli`.
- A standard library do Go. `net/http` funciona.
- Registro de flag CLI pelo Cobra. Os próprios testes do Cobra cobrem isso.

Ao invés disso, teste o código que você escreve: o wire-up, o branching, os caminhos de erro, os caminhos de recuperação.

## Próximo

- [Adicionar um transporte](/pt-BR/developer-guide/add-a-transport/) — o padrão de injeção de fake aplicado a um transporte completo.
- [Adicionar um provider](/pt-BR/developer-guide/add-a-provider/) — `httptest` em ação.
- [Contribuindo](/pt-BR/developer-guide/contributing/) — o checklist de PR.
