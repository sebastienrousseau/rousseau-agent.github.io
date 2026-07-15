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
changefreq: "weekly"
description: "Embed rousseau-agent's agent loop into your own Go binary. Provider and StreamingProvider interfaces, Session/Message/Turn shapes, tool registration, approval policies, compression, FTS5 recall."
keywords: "library, embedding, agent.Provider, agent.Session, agent.Turn, tool registry, approver, compression, FTS5, recall"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/agent-loop/"
subtitle: "Contrato para embeber la biblioteca: Provider, Registry, Session, Turn."
tags: "library, embedding, reference"
title: "Referencia del bucle del agente"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "library, embedding, agent.Provider, agent.Session, agent.Turn, tool registry, approver, compression, FTS5, recall"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Referencia del bucle del agente"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 22
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/agent-loop/index.html"
item_link: "https://docs.rousseau-agent.dev/agent-loop/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Referencia del bucle del agente"
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
twitter_title: "Referencia del bucle del agente"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Lo que aprenderás</span><p>La anatomía completa de un <code>Agent.Turn</code>: cómo <code>Compressor</code>, <code>SkillsProvider</code> y <code>RecallProvider</code> componen el system prompt, cómo los bloques <code>tool_use</code> del modelo pasan por el <code>Approver</code>, cómo los resultados de herramientas se pliegan de vuelta en la sesión y cómo termina el bucle. Lee <code>internal/agent/agent.go</code> junto con esta página.</p></aside>

## rousseau como biblioteca

`rousseau-agent` es tanto una biblioteca como un servicio. El bucle del agente, el registro de herramientas y las abstracciones de proveedor no dependen de la CLI. Puedes componerlos en tu propio binario sin importar `internal/cli` ni ningún paquete de transporte.

Cada identificador exportado tiene un comentario godoc. `pkg.go.dev/github.com/sebastienrousseau/rousseau-agent` renderiza la referencia completa.

## Anatomía de un Turn

La función `Agent.Turn` está definida en `internal/agent/agent.go`. En prosa, un turno hace lo siguiente:

```
Turn(ctx, session)
  │
  ├── 1. Guardia de sesión: sesión vacía → ErrEmptySession
  │
  ├── 2. Compressor.Compress(ctx, session)
  │     • Si está habilitado y len(messages) > TriggerMessages, resume los
  │       mensajes más antiguos in situ. Fija CacheableMessages en la próxima Request.
  │
  ├── 3. registry.Definitions() → toolDefs
  │
  └── bucle hasta MaxIterations (32 por defecto) veces:
        │
        ├── a. Construye Request{
        │       SessionID:         session.ID,
        │       System:            systemPrompt(session),
        │       Messages:          session.Messages,
        │       Tools:             toolDefs,
        │       CacheableMessages: <pista del compressor>,
        │     }
        │
        ├── b. resp = provider.Complete(ctx, req)
        │
        ├── c. session.Append(resp.Message)
        │
        ├── d. Switch sobre resp.StopReason:
        │       • StopEndTurn → devuelve resp.Message (éxito)
        │       • StopMaxTokens / StopOther → devuelve resp.Message
        │       • StopToolUse → continúa a (e)
        │
        ├── e. runTools(ctx, resp.Message, sessionID):
        │       Por cada bloque tool_use:
        │         • registry.Get(name) → tool o ErrToolNotFound
        │         • approver.Approve(...)
        │             DecisionDeny → tool_result con is_error=true y razón
        │             DecisionAllow → tool.Execute(ctx, input)
        │               err → tool_result con is_error=true y err.Error()
        │               ok  → tool_result con la salida
        │
        └── f. session.Append(Message{Role: user, Content: []tool_result})
              Bucle.

  MaxIterations agotadas → ErrMaxIterations
```

### Contrapresión y cancelación

El `ctx` que se pasa a `Turn` se propaga a todo: `Compressor.Compress`, cada `Provider.Complete`, cada `Tool.Execute` y cada `Approver.Approve`. Cancela el contexto para abortar a mitad de un turno; la llamada al proveedor de la iteración actual devuelve `context.Canceled`, la sesión queda con el último mensaje completo del modelo más la llamada de herramienta pendiente, y quien llama decide si reintenta.

La herramienta integrada `BashTool` envuelve cada comando en su propio `context.WithTimeout` (60 s por defecto, configurable), para que un comando descontrolado no pueda exceder el contexto externo.

### Composición del system prompt

`systemPrompt(ctx, session)` en `agent.go` línea 138 ensambla hasta tres partes:

```
<Options.SystemPrompt>

<SkillsProvider.SystemAppendix(session)>

<RecallProvider.SystemAppendix(ctx, session)>
```

Cualquier parte que devuelva vacío se omite. El resultado es `strings.Join(parts, "\n\n")`. La composición ocurre una vez por iteración (no por turno), de modo que las skills y el recall reaccionan al mensaje más reciente, incluyendo resultados intermedios de herramientas cuando corresponda.

### Gestión de la ventana de contexto

Las sesiones grandes eventualmente exceden la ventana de contexto del modelo. Rousseau no trunca por sí mismo; ese es el trabajo del `Compressor`. El `NoopCompressor` por defecto nunca reescribe, así que quienes integren y quieran una transcripción ilimitada en una ventana pequeña deben proveer su propio compresor o aceptar el error del lado del modelo cuando la ventana se llene.

`LLMCompressor` (ver abajo) colapsa los mensajes anteriores a `KeepRecent` en un único bloque de resumen una vez que el conteo excede `TriggerMessages`. El resumen lo genera el mismo proveedor que ejecuta el turno, por lo que cuesta una completación extra por ciclo de compresión.

## La interfaz Provider

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

`Complete` ejecuta un único turno no-streaming. `Request` lleva `SessionID`, `System`, `Messages`, `Tools` y `CacheableMessages` (una pista para el caché efímero). `Response` devuelve un único `Message` del asistente, un `StopReason` (`end_turn`, `tool_use`, `max_tokens`, `other`) y los conteos de tokens en `Usage`.

Cada proveedor incluido (Anthropic, Bedrock, Vertex, compatible con OpenAI, claudecli) implementa `Provider`. Todos excepto `claudecli` implementan `StreamingProvider`.

## Session, Message, Turn

`internal/agent/session.go` y `internal/agent/message.go`:

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

Una `Session` es solo de anexión. Cada mensaje de usuario es una llamada a `Agent.Turn(ctx, session)`; el bucle del agente muta la sesión in situ y devuelve el `Message` final del asistente.

## Registro de herramientas

`internal/tools`:

```go
registry := tools.NewRegistry()
registry.MustRegister(builtin.NewReadTool())
registry.MustRegister(builtin.NewGrepTool(0, 0))
registry.MustRegister(builtin.NewEditTool())
```

Cada herramienta declara un esquema JSON estricto. Añadir la tuya es una implementación de `Tool`:

```go
type Tool interface {
    Name() string
    Description() string
    InputSchema() json.RawMessage
    Execute(ctx context.Context, input json.RawMessage) (string, error)
}
```

`MustRegister` produce panic ante nombres duplicados; usa `Register` y verifica el error si construyes el registro dinámicamente.

## Políticas de aprobación

`internal/agent/approver.go`. Tres políticas integradas:

- `AllowAllApprover` — todas las llamadas se ejecutan.
- `DenyAllApprover{Reason: "…"}` — toda llamada se bloquea con la razón indicada.
- `PatternApprover{Allow: []PatternRule, Deny: []PatternRule, Default: Decision}` — regex de permitir/denegar por herramienta. Denegar gana; las solicitudes sin coincidencia usan `Default` (vacío → `DecisionDeny`).

Las reglas de patrones se compilan de manera perezosa una sola vez. Los errores de compilación aparecen como un `DecisionDeny` con la cadena de error como razón, de modo que una regex malformada falla de manera segura.

Los approvers personalizados implementan:

```go
type Approver interface {
    Approve(ctx context.Context, req ApprovalRequest) (Decision, string)
}
```

`ApprovalRequest` lleva `ToolName`, el JSON bruto de `Input` y `SessionID`. Devuelve `DecisionAllow` o `DecisionDeny` más una cadena con la razón (que se emerge al modelo como un error de `tool_result`).

## Compresión

`internal/agent/compressor.go`. `LLMCompressor` llama al mismo proveedor para resumir mensajes antiguos una vez que la sesión cruza un umbral:

```go
compressor, err := agent.NewLLMCompressor(agent.LLMCompressorConfig{
    Provider:        provider,
    TriggerMessages: 60,
    KeepRecent:      8,
})
```

Los `KeepRecent` mensajes más recientes sobreviven textualmente; todo lo anterior se colapsa en un único bloque de resumen. El `Compressor` fija `CacheableMessages` en la próxima solicitud para que el resumen esté caliente en caché en el siguiente turno.

`NoopCompressor` es el predeterminado cuando `Compressor` es nil.

## Recall entre sesiones con FTS5

`internal/agent/recall.go` + `internal/state/sqlite/`. El índice FTS5 del almacén de sesiones cubre cada mensaje. `SQLiteRecall` consulta contra el mensaje actual del usuario y devuelve los K fragmentos más relevantes como un apéndice del system prompt:

```go
recall := recall.NewSQLiteRecall(store, 5)
```

Habilítalo asignando `Options.RecallProvider = recall`. Los resultados vacíos son seguros; el bucle continúa normalmente.

## Ejemplo completo de integración

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

Existe una copia ejecutable en `examples/embed-agent` dentro del árbol de código.

## Solución de problemas

### `agent: max iterations exceeded`

El modelo siguió solicitando llamadas a herramientas sin emitir `end_turn`. Causas comunes: una herramienta que siempre falla (el modelo sigue reintentando con variaciones), o un valor de `MaxIterations` demasiado bajo para una tarea genuinamente compleja. El valor por defecto es 32; súbelo a 64 para refactorizaciones grandes. Fija `MaxIterations: 0` para usar el predeterminado.

### `agent: tool not found: <name>`

El modelo emitió un bloque `tool_use` con el nombre de una herramienta que no está en el registro. Suele indicar un system prompt desactualizado (la herramienta se eliminó pero el modelo aún la recuerda), o una herramienta alucinada. Rousseau lo emerge como un error a quien llama; al modelo no se le da la oportunidad de adaptarse. Si quieres degradación elegante, envuelve la búsqueda en el registro dentro de tu propio despachador de herramientas.

### El proveedor devolvió `end_turn` con un mensaje vacío

Algunos proveedores devuelven `stop_reason=end_turn` sin bloques de contenido; por ejemplo, cuando el modelo eligió permanecer en silencio. Rousseau devuelve el `Message` vacío; quien llama decide si "vacío" es un resultado válido para su UI. Los handlers de transporte de chat registran `whatsapp.empty_reply`, `slack.empty_reply`, etc.

### El resultado de la herramienta está truncado

`Content.ToolResult.Output` es una cadena Go simple. Algunas implementaciones de herramientas (notablemente `read` sobre un archivo enorme) devuelven una salida mayor de la que el modelo puede absorber. Limita la salida en la propia herramienta; la herramienta integrada `read` trunca en 200 KB.

### La compresión se dispara pero el resumen es incoherente

El prompt de compresión por defecto solicita un resumen en forma de lista. Si a los resúmenes del modelo les faltan hechos clave, aumenta `KeepRecent` para que sobrevivan más mensajes textualmente, o sobrescribe `CompressionConfig.Prompt` con una instrucción específica a la tarea. La instrucción es la palanca del operador; el compresor no dirige al modelo de otra manera.

## Páginas relacionadas

- [Conceptos](/es/concepts/) — panorama de cada subsistema.
- [Guía del usuario: Políticas de aprobación](/es/user-guide/approval-policies/) — semántica completa de políticas.
- [Guía del usuario: Herramientas](/es/user-guide/tools/) — esquemas de herramientas integradas.
- [Guía del usuario: Compresión y recall](/es/user-guide/compression-recall/) — internos del compresor y del recall FTS5.
- [MCP](/es/mcp/) — exponer las herramientas del agente a hosts externos.

## Lecturas adicionales

- `internal/agent/agent.go` — `Turn`, `runTools`, `systemPrompt`.
- `internal/agent/approver.go` — `PatternApprover`, `AllowAllApprover`, `DenyAllApprover`.
- `internal/agent/compressor.go` — `LLMCompressor` y `NoopCompressor`.
- `internal/agent/recall.go` — `SQLiteRecall` y la forma de consulta FTS5.
- `internal/agent/stream_turn.go` — variante streaming que expone progreso token a token.
- `internal/tools/tool.go` — la interfaz `Tool`.
- `examples/embed-agent/main.go` — ejemplo de integración ejecutable.
