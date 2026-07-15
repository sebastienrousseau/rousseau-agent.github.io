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
hreflang: "es"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "es"
locale: "es_ES"
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
permalink: "https://docs.rousseau-agent.dev/es/developer-guide/testing/"
subtitle: "Dependency injection, fakes, race, coverage."
tags: "developer-guide, testing, di, fakes"
title: "Pruebas"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "testing, dependency injection, fake, mock, coverage, race, go test, httptest"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Pruebas"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 65
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/testing/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/testing/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Pruebas"
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
twitter_title: "Pruebas"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Gracias a cada operador que ejecuta su propio agente de codificación."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## El patrón

Cada paquete que habla con el mundo exterior define una interfaz pequeña para su dependencia, toma esa interfaz como parámetro del constructor e inyecta un cliente real en `cli/*.go` (producción) o un fake en `*_test.go` (tests).

Ejemplos en el árbol:

| Paquete | Interfaz | Real | Fake para tests |
|---|---|---|---|
| `internal/transport/whatsapp` | `WSConn` | WebSocket de whatsmeow | struct en memoria con un canal `send` |
| `internal/transport/email` | `IMAPClient` | Cliente `emersion/go-imap` | Canal scripted de mensajes |
| `internal/transport/whatsapp` | `Sender` | Envío directo con whatsmeow | Slice en memoria para aserción |
| `internal/llm/*` | `HTTPClient` (indirecto vía `http.Client`) | `http.DefaultTransport` | `httptest.NewServer` |
| `internal/state/sqlite` | `state.Store` (interfaz propiedad de `state`) | `modernc.org/sqlite` en disco | DSN en memoria `:memory:` |
| `internal/agent` | `Provider`, `Approver`, `Compressor`, `RecallProvider` | tipos concretos de `llm/*` | Implementaciones struct en `_test.go` |

La regla: **la interfaz con el consumidor, la implementación con el proveedor.** `Provider` se define en `agent`, no en `llm/anthropic`. `Store` se define en `state`, no en `state/sqlite`.

## Ejecutar el gate

```sh
make check
```

es equivalente a:

```sh
go vet ./...
golangci-lint run
go test -race -count=1 -covermode=atomic ./...
govulncheck ./...
```

CI ejecuta el mismo comando en `ubuntu-latest` y `macos-latest`. Si pasa localmente, pasa en CI, salvo bugs específicos de plataforma, por eso macOS está en la matriz.

## Detector de race

`-race` no es negociable. Cada daemon en rousseau involucra múltiples goroutines (bomba de transporte, bucle del agente, planificador cron, escritor del almacén de sesiones). Una race en cualquiera de ellas es un bug real.

Si encuentras un test que solo falla bajo `-race`, ese es un bug en el código bajo prueba, no en el test. No deshabilites `-race`.

## Piso de cobertura

El piso de cobertura actual es **75% total**. Los paquetes centrales (`internal/agent`, `internal/tools`, `internal/state/sqlite`) están entre 85–100% y se mantienen ahí por la suite de tests preexistente; el código nuevo en esos paquetes no debe bajarlos.

Un job de CI se ejecuta tras `go test -race -covermode=atomic ./... -coverprofile=coverage.out` e inspecciona `coverage.out`. Fallar el piso hace fallar el build.

## Generadores de fakes

Rousseau no usa una biblioteca de generación de mocks. Los fakes son tipos struct escritos a mano, lo suficientemente pequeños para leer de un vistazo:

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

Se desprenden dos propiedades:

1. El fake es inspeccionable: `calls` captura cada solicitud, para que las aserciones puedan chequear qué emitió el código bajo prueba.
2. El fake es determinista: las respuestas enlatadas se consumen en orden.

## `httptest` para proveedores con forma HTTP

Cada adaptador de LLM que habla HTTP usa `httptest.NewServer` para los tests:

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

Para streaming estilo SSE, la misma técnica funciona: `http.Flusher` está disponible en el response writer.

## Corpus de fuzz

Cada parser tiene una función `Fuzz*`. Ejecuta la batería completa:

```sh
make fuzz
```

Bajo CI, fuzz se ejecuta por un tiempo acotado (`-fuzztime`). Localmente, ejecuta más tiempo para sembrar el corpus.

## Tests dirigidos por tablas

Los tests de rousseau se apoyan fuertemente en la forma dirigida por tablas. Forma de ejemplo:

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

Esto escala: cada nueva forma de regla se convierte en una fila de la tabla.

## Fugas de goroutines

Los tests que lanzan goroutines deben unirlas. Patrones comunes:

- Usa `context.WithCancel` y `cancel()` al final del test.
- Usa un `sync.WaitGroup` y `wg.Wait()`.
- Consume cada canal hasta `close`.

Si un test filtra una goroutine, `go test -race` puede atraparla vía un panic de receptor nil en la goroutine filtrada después de que el `main` del archivo del test haya salido. Más barato ser disciplinado desde el principio.

## Tiempo determinista

Para tests sensibles al tiempo (cron, ranking de reciente en recall), inyecta un proveedor `time.Time`:

```go
type Clock interface {
    Now() time.Time
}
```

Cablea el `time.Now` real en `cli/*` y un `time.Time` fake en el test. El planificador `internal/cron/scheduler.go` usa este patrón.

## Testear la TUI

`internal/tui/model_test.go` usa el helper `TestModel` de `bubbletea`. `View()` es una función pura de cadena del modelo, por lo que la mayoría de aserciones se vuelven "ejecuta este update, espera esta salida de View".

## Qué no testear

- Bibliotecas de terceros. Rousseau no duplica los tests upstream de whatsmeow o `signal-cli`.
- La biblioteca estándar de Go. `net/http` funciona.
- Registro de flags CLI por Cobra. Los propios tests de Cobra lo cubren.

En su lugar, testea el código que escribes: el cableado, la ramificación, los caminos de error, los caminos de recuperación.

## Siguiente

- [Añadir un transporte](/es/developer-guide/add-a-transport/): el patrón de inyección de fake aplicado a un transporte completo.
- [Añadir un proveedor](/es/developer-guide/add-a-provider/): `httptest` en acción.
- [Contribuir](/es/developer-guide/contributing/): la lista de verificación de PR.
