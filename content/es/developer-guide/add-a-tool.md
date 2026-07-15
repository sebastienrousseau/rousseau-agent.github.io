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
description: "How to add a new built-in tool to rousseau-agent: declare a JSON schema, implement Execute, register with the tool registry."
keywords: "add tool, tool registry, json schema, execute, extend, custom tool"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/developer-guide/add-a-tool/"
subtitle: "Schema, Execute, register — three moving parts."
tags: "developer-guide, tools, extend"
title: "Añadir una herramienta"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add tool, tool registry, json schema, execute, extend, custom tool"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Añadir una herramienta"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 64
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-tool/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-tool/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Añadir una herramienta"
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
twitter_title: "Añadir una herramienta"
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

`internal/tools/tool.go` (parafraseado):

```go
type Tool interface {
    Name() string
    Description() string
    InputSchema() map[string]any
    Execute(ctx context.Context, input json.RawMessage) (string, error)
}
```

Cuatro métodos, sin ciclo de vida. Las herramientas son sin estado desde la perspectiva del bucle: cualquier estado que la herramienta necesite (un caché de regex compiladas, un índice in-process) es un campo privado del tipo concreto.

## Esqueleto para una nueva herramienta

Añadamos una herramienta hipotética **`http_get`** que obtenga una URL y devuelva su cuerpo.

### Paso 1: el tipo

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

### Paso 2: metadatos

```go
// Name satisfies tools.Tool.
func (*HTTPGetTool) Name() string { return "http_get" }

// Description satisfies tools.Tool.
func (*HTTPGetTool) Description() string {
    return "Fetch an HTTPS URL and return the response body. Input: url (string). Redirects are followed up to 10 hops. Response is capped at 1 MiB."
}
```

La **descripción está orientada al modelo**. Debe leerse como un docstring corto para otro ingeniero: qué hace la herramienta, qué significan sus entradas, cuál es la forma de la salida.

### Paso 3: esquema de entrada

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

Mantén el esquema estricto. Cada propiedad recibe una `description`. El array `required` lo aplica el validador de tool-use del modelo: los campos faltantes causan un retry de `tool_use`, no un error en runtime.

### Paso 4: Execute

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

### Paso 5: registrar

Cablealo en `internal/cli/chat.go` (y cada otro comando que construya un registro: haz grep de `registry.MustRegister` para encontrarlos):

```go
registry.MustRegister(builtin.NewHTTPGetTool(30 * time.Second))
```

Una vez registrada, la herramienta está disponible para el modelo en cada turno.

### Paso 6: tests

Sigue `internal/tools/builtin/read_test.go` para el patrón:

```go
func TestHTTPGetTool_Execute_Success(t *testing.T) {
    srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
        _, _ = w.Write([]byte("hello"))
    }))
    defer srv.Close()

    // La herramienta rechaza HTTP en texto plano; envuelve el test server con httptest.NewTLSServer
    // para un test de integración real, o expón una costura interna que permita `http://` solo en tests.
    // El esqueleto aquí es ilustrativo.
}

func TestHTTPGetTool_Execute_RejectsPlaintextHTTP(t *testing.T) {
    tool := builtin.NewHTTPGetTool(0)
    _, err := tool.Execute(context.Background(), json.RawMessage(`{"url":"http://example.com"}`))
    require.Error(t, err)
    require.Contains(t, err.Error(), "only https")
}
```

### Paso 7: política de aprobación

La herramienta ahora está disponible para el modelo, sujeta a la [política de aprobación](/es/user-guide/approval-policies/). Recomienda una regla deny en la documentación para la postura por defecto:

```yaml
deny:
  - {tool: http_get, match: "\"url\":\"https://(169\\.254|10\\.|192\\.168\\.|172\\.(1[6-9]|2[0-9]|3[01])\\.)"}
```

Esto bloquea la herramienta para que no llame al IMDS de AWS ni al espacio privado RFC1918: una petición común para herramientas que hacen fetch HTTP.

### Paso 8: docs

Añade una sección a `content/user-guide/tools.md` describiendo la nueva herramienta: esquema, semántica, notas de seguridad. Sigue la forma de las cinco herramientas existentes.

## Detalles del contrato

- **Sin estado**: `Execute` no debe llevar estado entre llamadas que no esté explícitamente privado en los campos propios de la herramienta. Dos turnos concurrentes en dos sesiones pueden llamar a la misma herramienta simultáneamente.
- **Respeto por el contexto**: `Execute` debe honrar la cancelación de `ctx`. El trabajo de larga duración debe chequear periódicamente `ctx.Err()` o enrutar el trabajo a través de una llamada de biblioteca con conciencia de contexto.
- **Sin panics**: devuelve errores en su lugar. El bucle del agente convierte un error en un `tool_result` con `IsError: true`, al que el modelo puede adaptarse.
- **Forma de retorno**: la salida es una cadena plana, retroalimentada al modelo en el siguiente turno. Incluye suficiente estructura (p. ej. números de línea, códigos de estado) para que el modelo pueda razonar sobre ella.

## Herramientas personalizadas sin tocar el código

Si no quieres forkear rousseau, integra el bucle del agente en tu propio binario y registra tus herramientas ahí:

```go
registry := tools.NewRegistry()
registry.MustRegister(builtin.NewReadTool())
registry.MustRegister(builtin.NewWriteTool())
// ...
registry.MustRegister(mypkg.NewMyTool())

ag := agent.New(provider, registry, logger, agent.Options{})
```

Consulta `examples/embed-agent/` en el árbol de código para un ejemplo completo de integración.

## Errores comunes

- **Esquema demasiado amplio.** Requerir solo `type: object` no le da ninguna ayuda al modelo. Enumera cada propiedad, describe cada campo.
- **Bloquear en I/O sin fecha límite.** Siempre usa `NewRequestWithContext`, siempre establece `http.Client{Timeout: ...}`, siempre honra `ctx`.
- **Devolver demasiado.** La salida se retroalimenta al modelo en el siguiente turno. Una respuesta de 1 MB quema tokens; acótala.
- **Efectos secundarios escapistas.** Una herramienta que muta el mundo debe registrar lo que hizo en la cadena de retorno para que el rastro de auditoría del aprobador sea completo.
- **Olvidar el chequeo de interfaz en tiempo de compilación.** `var _ tools.Tool = (*MyTool)(nil)` a nivel de paquete atrapa la deriva de interfaz en tiempo de build.

## Siguiente

- [Guía de usuario: Herramientas](/es/user-guide/tools/): las cinco herramientas integradas con esquemas.
- [Guía de usuario: Políticas de aprobación](/es/user-guide/approval-policies/): cómo restringir la nueva herramienta.
- [Pruebas](/es/developer-guide/testing/): el patrón para tests de herramientas.
