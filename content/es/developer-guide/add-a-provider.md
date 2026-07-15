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
description: "How to add a sixth LLM provider to rousseau-agent: implement Provider.Complete and optionally StreamingProvider.CompleteStream."
keywords: "add provider, llm, chat completion, streaming, agent provider, extend"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/developer-guide/add-a-provider/"
subtitle: "Provider.Complete and StreamingProvider.CompleteStream."
tags: "developer-guide, provider, llm, extend"
title: "Añadir un proveedor"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add provider, llm, chat completion, streaming, agent provider, extend"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Añadir un proveedor"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 63
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-provider/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-provider/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Añadir un proveedor"
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
twitter_title: "Añadir un proveedor"
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

## La interfaz

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

// Provider dirige un único round-trip.
type Provider interface {
    Complete(ctx context.Context, req Request) (Response, error)
}

// StreamingProvider transmite deltas de respuesta según llegan.
type StreamingProvider interface {
    Provider
    CompleteStream(ctx context.Context, req Request) (StreamReader, error)
}
```

Cada adaptador de LLM satisface al menos `Provider`. `StreamingProvider` es opcional: la TUI y los handlers de transporte de chat harán fallback al camino no-streaming cuando un proveedor no lo implemente.

`StopReason` es uno de `StopEndTurn`, `StopToolUse`, `StopMaxTokens`. El bucle del agente trata `StopEndTurn` como terminal y `StopToolUse` como "el modelo quiere una llamada a herramienta".

## Esqueleto para un nuevo proveedor

Añadamos un proveedor hipotético **Cohere Command R**.

### Paso 1: directorio

```
internal/llm/cohere/
├── client.go        # Config, New
├── complete.go      # Provider.Complete
├── stream.go        # StreamingProvider.CompleteStream (optional)
└── *_test.go
```

### Paso 2: `client.go`

```go
// El paquete cohere implementa el proveedor Cohere Command R.
package cohere

import (
    "net/http"
    "time"
)

// Config configura el proveedor Cohere.
type Config struct {
    APIKey    string
    Model     string
    BaseURL   string
    MaxTokens int64
}

// Provider es el adaptador de Cohere.
type Provider struct {
    cfg    Config
    client *http.Client
}

// New construye un Provider.
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

### Paso 3: `complete.go`

Implementa `Complete`:

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

Los cuerpos `encodeRequest`, `decodeResponse` y la forma `cohereResponse` son específicos de Cohere: traducen los tipos `agent.Request` y `agent.Response` agnósticos al proveedor de rousseau desde y hacia el formato de cable de Cohere.

### Paso 4: streaming (opcional)

Si Cohere admite streaming estilo SSE, implementa `CompleteStream`. Sáltatelo en una primera pasada; el bucle del agente hace fallback a no-streaming automáticamente.

### Paso 5: superficie de configuración

Añade `CohereConfig` a `internal/config/config.go`:

```go
type CohereConfig struct {
    APIKey    string `mapstructure:"api_key"`
    Model     string `mapstructure:"model"`
    BaseURL   string `mapstructure:"base_url"`
    MaxTokens int64  `mapstructure:"max_tokens"`
}
```

Añade un campo a `Config`:

```go
Cohere CohereConfig `mapstructure:"cohere"`
```

Extiende `setDefaults` con un default de modelo sensato:

```go
v.SetDefault("cohere.model", "command-r-plus")
```

### Paso 6: cableado CLI

En `internal/cli/provider.go`, extiende `buildProvider(cfg *config.Config)`:

```go
func buildProvider(cfg *config.Config) (agent.Provider, error) {
    switch cfg.Provider {
    // ...casos existentes...
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

Extiende `rousseau doctor` (`internal/cli/doctor.go`) para añadir un bloque de chequeo `provider.cohere.*` cuando `cfg.Provider == "cohere"`. Replica los chequeos existentes de anthropic.

## Detalles del contrato que asume el bucle del agente

- **`Complete` respeta `ctx`.** Las solicitudes HTTP largas deben honrar la cancelación de contexto, o el apagado por `SIGTERM` del daemon se colgará.
- **Round-trip de tool-use.** Cuando el modelo emite bloques `tool_use`, el `StopReason` de la respuesta debe ser `StopToolUse` y el contenido del mensaje debe incluir `Content{Kind: ContentToolUse, ToolUse: &ToolUse{Name, Input, ID}}` para cada llamada solicitada. El bucle del agente enruta cada una al `Registry`, la ejecuta y canaliza los resultados de vuelta en la siguiente llamada a `Complete`.
- **Manejo de `tool_result`.** En la siguiente llamada, `req.Messages` contiene un mensaje de usuario cuyo contenido incluye `Content{Kind: ContentToolResult, ToolResult: &ToolResult{ToolUseID, Output, IsError}}` para cada llamada ejecutada. El proveedor debe renderizar estos a la forma que espere la API upstream.
- **Chequeo de interfaz en tiempo de compilación.** `var _ agent.Provider = (*Provider)(nil)` a nivel de paquete atrapa la deriva de interfaz en tiempo de build.

## Contrato de streaming

Si implementas `StreamingProvider`:

```go
type StreamReader interface {
    Next(ctx context.Context) (StreamChunk, error)
    Close() error
}

type StreamChunk struct {
    Delta     string       // delta de texto parcial
    Done      bool         // chunk final
    Response  *Response    // Response final, no-nil solo en Done
}
```

La TUI y los handlers de transporte de chat leen deltas según llegan; la `Response` final se usa para añadir el mensaje del asistente completamente formado a la sesión.

## Caché de prompts

`internal/llm/anthropic` coloca marcadores `cache_control` en los dos últimos mensajes de la solicitud. Si tu proveedor admite caché de prompt, haz lo mismo: convierte compresión + recall (consulta [Compresión + Recall](/es/user-guide/compression-recall/)) de un patrón hambriento de tokens a uno barato.

## Pruebas

Usa `httptest.NewServer` para levantar un upstream fake. `internal/llm/anthropic/*_test.go` es la referencia. El patrón:

1. Inicia `httptest.NewServer` con un handler que retorne JSON enlatado.
2. Construye el proveedor apuntando `BaseURL` al test server.
3. Llama a `Complete` con un `Request` enlatado.
4. Asegúrate en la forma del `Response` retornado.

Para streaming, `httptest` también admite Server-Sent Events: consulta `internal/llm/anthropic/stream.go`.

## Docs

Añade `content/providers/cohere.md` en este sitio de docs. Sigue la forma de `content/providers/anthropic.md`: descripción, superficie de configuración, detalles de auth, advertencias específicas del proveedor.

## Errores comunes

- **Reescribir silenciosamente `Messages`.** El bucle del agente es la fuente de verdad para el estado de conversación. Los proveedores deben traducir la forma sin mutar la semántica.
- **Perder IDs de tool-use.** Cada `ToolUse.ID` en una respuesta debe coincidir con un `ToolResult.ToolUseID` en la siguiente solicitud. Si tu proveedor asigna sus propios IDs, tradúcelos con cuidado.
- **Ignorar `MaxTokens`.** Algunos proveedores rechazan solicitudes sin un límite explícito. Establece un default sensato en `New`.
- **Bloquear el bucle con políticas de retry.** Los reintentos pertenecen al adaptador de proveedor, no al bucle del agente. Acótalos; fallar rápido es mejor que colgarse.

## Siguiente

- [Pruebas](/es/developer-guide/testing/): cómo escribir el `_test.go` del proveedor.
- [Añadir una herramienta](/es/developer-guide/add-a-tool/): el punto de extensión más pequeño.
- [Configuración](/es/configuration/): la superficie de configuración que cada proveedor expone.
