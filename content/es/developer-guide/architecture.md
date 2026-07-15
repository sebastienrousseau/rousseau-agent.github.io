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
description: "Layered architecture of rousseau-agent: agent core, provider / tool / transport interfaces, module boundaries, cyclic-dependency prevention."
keywords: "architecture, layers, agent, provider, transport, tools, module, cyclic dependency"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/developer-guide/architecture/"
subtitle: "Layered architecture and module boundaries."
tags: "developer-guide, architecture, layers"
title: "Arquitectura"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "architecture, layers, agent, provider, transport, tools, module, cyclic dependency"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Arquitectura"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 61
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/architecture/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/architecture/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Arquitectura"
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
twitter_description: "Layered architecture of rousseau-agent: agent core, provider / tool / transport interfaces, module boundaries, cyclic-dependency prevention."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Arquitectura"
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

## Vista por capas

```
+--------------------------------------------------------------------+
|                                CLI                                |
|  chat  whatsapp  slack  discord  ...  mcp  cron  skills  doctor   |
+--------------------------------+-----------------------------------+
                                 |
+--------------------------------v-----------------------------------+
|                              Router                               |
|                  (per-JID session, allowlist, dispatch)           |
+---------------+---------------+-------------------+---------------+
                |                                   |
       transport.Transport                    agent.Agent
       Start / Stop / Deliver                Turn / TurnStream
                |                                   |
     +----------+----------+              +---------+-----------+
     |  9 concrete adapters |              |    agent.Provider  |
     +---------------------+              |    5 concrete impls |
                                          +---------+-----------+
                                                    |
                                          +---------v-----------+
                                          |   tools.Registry   |
                                          |   tools.Tool iface |
                                          +---------+-----------+
                                                    |
                                          +---------v-----------+
                                          |     state.Store    |
                                          | SQLite: sessions, |
                                          | jidmap, FTS5, cron|
                                          +---------------------+
```

## Roles de los paquetes

| Paquete | Rol | Depende de |
|---|---|---|
| `internal/agent` | Session, Message, Turn, bucle del agente e interfaces Provider / Tool / Approver / Compressor / SkillsProvider / RecallProvider. | stdlib + `internal/tools` (solo interfaz). |
| `internal/tools` | Interfaz Tool + Registry seguro para concurrencia. | stdlib. |
| `internal/tools/builtin` | `read`, `write`, `edit`, `grep`, `bash`. | `internal/tools`. |
| `internal/llm/{anthropic,bedrock,claudecli,openai,vertex}` | Implementaciones concretas de `agent.Provider`. | `internal/agent`. |
| `internal/state` | Interfaz Store + tipo Summary. | stdlib. |
| `internal/state/sqlite` | Implementación SQLite, WAL, FTS5, tabla de cron y mapa de JIDs. | `internal/state`, `modernc.org/sqlite`. |
| `internal/transport` | Interfaz Transport + Router. | `internal/agent`, `internal/state`. |
| `internal/transport/{whatsapp,signal,...}` | Nueve adaptadores concretos. | `internal/transport`, `internal/agent`. |
| `internal/mcp` | Servidor JSON-RPC 2.0 sobre stdio, spec MCP 2024-11-05. | `internal/agent`, `internal/tools`, `internal/state`. |
| `internal/skills` | Cargador y composición de agentskills.io. | stdlib. |
| `internal/cron` | Goroutine planificadora robfig/cron/v3. | `internal/state`, `internal/agent`. |
| `internal/config` | Cargador de configuración basado en Viper. | stdlib + `viper`. |
| `internal/cli` | Árbol de comandos Cobra, cableado. | Todo lo anterior. |
| `internal/tui` | Modelo Bubble Tea. | `internal/agent`, `internal/state`, `bubbletea`. |
| `cmd/rousseau` | Manejo de señales + `Execute`. | `internal/cli`. |

## Invariante clave

**El paquete `agent` solo depende de las interfaces expuestas por `tools`, de sus propios tipos `Provider` y de la biblioteca estándar.**

Todo lo que puede variar — el proveedor, el store, el transporte, el approver, el compressor — se expresa como una interfaz cuya propiedad es de `agent`. Las implementaciones concretas importan `agent`; `agent` nunca las importa de vuelta. Esto hace que el bucle sea comprobable sin ningún proveedor en vivo, red en vivo ni transporte en vivo.

Si te encuentras añadiendo un import desde `agent` hacia `llm/*`, `transport/*` o `state/sqlite`, detente. El cableado pertenece a `cli`, no a `agent`.

## Prevención de dependencias cíclicas

El compilador de Go detecta ciclos de imports de paquetes en tiempo de build. La postura por capas hace que los ciclos sean prácticamente imposibles: cada capa solo conoce las capas que están por debajo. Concretamente:

- `cli` puede importar cualquier cosa.
- `transport/*`, `llm/*`, `state/*` pueden importar `agent`, `tools` y (para transports y state) sus paquetes hermanos de interfaces.
- `agent` solo puede importar `tools` (interfaces) y la biblioteca estándar.
- `tools` solo importa la biblioteca estándar.

Dos reglas estructurales previenen regresiones:

1. Las interfaces viven en el paquete **consumidor**. `Provider` se define en `agent`, no en `llm/anthropic`. `Tool` se define en `tools`, no en `tools/builtin`.
2. Los dobles de prueba viven junto a su consumidor. `agent_test.go` define proveedores falsos; `transport/whatsapp/client_test.go` define conexiones WebSocket falsas.

## Interfaz Provider

```go
// Provider drives a single request/response round-trip.
type Provider interface {
    Complete(ctx context.Context, req Request) (Response, error)
}

// StreamingProvider streams response deltas.
type StreamingProvider interface {
    Provider
    CompleteStream(ctx context.Context, req Request) (StreamReader, error)
}
```

Cada adaptador de LLM satisface al menos `Provider`. El streaming es opt-in.

## Interfaz Tool

```go
// Tool is a callable capability the model can request.
type Tool interface {
    Name() string
    Description() string
    InputSchema() map[string]any
    Execute(ctx context.Context, input json.RawMessage) (string, error)
}
```

`InputSchema()` devuelve un mapa con forma de JSON Schema; su forma debe validar contra las expectativas de tool-use del modelo.

## Interfaz Transport

```go
type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

Se espera que `Start` bloquee hasta que `ctx` sea cancelado o se invoque `Stop`. La entrega de vuelta al remitente la gestiona el transporte internamente; los adaptadores normalmente exponen un método `Deliver(ctx, target, body)` usado por el planificador cron.

## Interfaz Approver

```go
type Approver interface {
    Approve(ctx context.Context, req ApprovalRequest) (Decision, string)
}
```

Se invoca en el camino crítico antes de cada llamada a herramienta. Consulta [políticas de aprobación](/es/user-guide/approval-policies/).

## Compressor y Recall

Dos interfaces adicionales que el bucle del agente consulta en cada turno:

```go
type Compressor interface {
    Compress(ctx context.Context, s *Session) (changed bool, err error)
}

type RecallProvider interface {
    SystemAppendix(ctx context.Context, s *Session) string
}
```

Consulta [Compresión + Recall](/es/user-guide/compression-recall/).

## Cableado en `cli`

`internal/cli/chat.go` es el ejemplo canónico de cableado. Sus pasos:

1. Carga la configuración.
2. Construye un proveedor (`buildProvider(cfg)`).
3. Abre el store SQLite (`openStore`).
4. Crea un registro de herramientas y registra las herramientas integradas.
5. Construye un approver a partir de `cfg.Agent.Approver`.
6. Construye un compressor a partir de `cfg.Agent.Compression`.
7. Construye `agent.New(...)`.
8. Entrega el agente al modelo de Bubble Tea.

Cada uno de los demás comandos sigue el mismo patrón — las partes específicas del demonio son solo el constructor del transporte y su invocación de `Start`.

## Patrón de pruebas

Las interfaces de cada capa permiten probar en aislamiento:

- `agent_test.go` usa un `Provider` falso que devuelve valores `Response` predefinidos.
- `transport/whatsapp/client_test.go` usa un `WSConn` falso y un `Sender` falso.
- `state/sqlite/*_test.go` usa un SQLite en memoria (`file::memory:`).
- `tools/builtin/*_test.go` usa `testing/fstest.MapFS` (donde corresponda) y archivos temporales.

Consulta [Pruebas](/es/developer-guide/testing/) para conocer el patrón de inyección.

## Grafo de dependencias de paquetes

```
cmd/rousseau/               (entry point)
    │
    ▼
internal/cli/               (Cobra command tree)
    │
    ├───▶ internal/config/  (Viper-driven config)
    ├───▶ internal/agent/   (Turn loop, session, provider iface, approver, compressor)
    │        │
    │        └───▶ internal/tools/           (Tool iface + Registry)
    │                    │
    │                    └───▶ internal/tools/builtin/   (read, write, edit, grep, bash)
    │
    ├───▶ internal/llm/anthropic/  ─────┐
    ├───▶ internal/llm/bedrock/    ─────┤
    ├───▶ internal/llm/claudecli/  ─────┼─▶ implements agent.Provider
    ├───▶ internal/llm/openai/     ─────┤
    ├───▶ internal/llm/vertex/     ─────┘
    │
    ├───▶ internal/transport/           (Transport iface + Router)
    │        │
    │        ├───▶ whatsapp/    (whatsmeow)
    │        ├───▶ slack/       (Socket Mode)
    │        ├───▶ discord/     (Gateway v10)
    │        ├───▶ telegram/    (Bot API)
    │        ├───▶ matrix/      (Client-Server)
    │        ├───▶ signal/      (signal-cli JSON-RPC)
    │        ├───▶ email/       (IMAP + SMTP)
    │        ├───▶ sms/         (Twilio / Vonage REST)
    │        └───▶ imessage/    (BlueBubbles)
    │
    ├───▶ internal/cron/        (scheduled prompts)
    ├───▶ internal/mcp/         (JSON-RPC 2.0 server)
    ├───▶ internal/skills/      (agentskills.io loader)
    ├───▶ internal/state/       (Store iface)
    │        │
    │        └───▶ internal/state/sqlite/   (WAL, FTS5)
    │
    └───▶ internal/tui/         (Bubble Tea model)
```

Propiedad clave: `internal/agent` depende únicamente de la biblioteca estándar, de `internal/tools` (a través de su interfaz reducida) y de sus propios subpaquetes. Cada proveedor, cada store y cada transporte dependen de `agent` — nunca al revés.

## Justificación estilo ADR

Decisiones de frontera seleccionadas y por qué existen:

### ADR-1: Provider es una interfaz, no un plugin

Consideramos un modelo de plugins (`plugin.Open` o `hashicorp/go-plugin`). Se rechazó porque:

- Los builds estáticos son más fáciles de firmar, reproducir y distribuir.
- Las ABIs de plugin son frágiles entre versiones de Go.
- Cada proveedor que nos importa es lo bastante pequeño como para vendorizarlo.

Contrapartida: añadir un proveedor requiere una recompilación. Es aceptable.

### ADR-2: Las herramientas viven en `internal/tools/builtin`, no en un `pkg/tools`

Consideramos exportar el registro de herramientas públicamente. Se rechazó porque:

- `internal/` desalienta el acoplamiento accidental.
- Quien embeba el agente puede seguir registrando sus propias herramientas mediante la interfaz `Registry` exportada — simplemente lo hace a través del paquete `tools` en lugar de importar una builtin.

Contrapartida: los usuarios no pueden importar `rousseau/tools/builtin` directamente. Importan `rousseau/agent` y `rousseau/tools` y construyen su propio registro, que es lo que demuestra `examples/embed-agent`.

### ADR-3: SQLite vía `modernc.org/sqlite`, no `mattn/go-sqlite3`

`modernc.org/sqlite` es un port en Go puro; `mattn/go-sqlite3` usa cgo. Elegido porque:

- `CGO_ENABLED=0` mantiene el binario estático.
- Los binarios estáticos son más fáciles de firmar, reproducir y distribuir.
- El job de CI para builds reproducibles sería mucho más difícil con cgo.

Contrapartida: `modernc.org/sqlite` es más lento en cargas con muchas escrituras. Aceptable — rousseau no es una base de datos con carga intensiva de escritura.

### ADR-4: El servidor MCP es minimalista, no el SDK oficial

El paquete `internal/mcp/` son ~200 líneas de JSON-RPC hechas a mano. Elegido porque:

- La superficie de MCP que rousseau necesita es pequeña (initialize, tools/list, tools/call, ping, shutdown).
- El SDK oficial de Go aún no era estable cuando se escribió el código.
- Mantener la superficie pequeña hace que el cambio al SDK sea indoloro cuando este se estabilice.

Contrapartida: algunas funcionalidades de MCP (resources, prompts, notificaciones de list-changed) son stubs. Está en la hoja de ruta.

### ADR-5: El proveedor `claudecli` no usa el registro de herramientas de rousseau

El subproceso de `claude` ejecuta su propio bucle de tool-use. Por tanto, el approver de rousseau no puede ver las llamadas a herramientas. Es una aceptación deliberada:

- El proveedor `claudecli` existe para permitir a los suscriptores usar su autenticación de Claude Code sin una API key.
- Si rousseau interceptase el bucle de herramientas, tendríamos que canalizar cada entrada y salida a través del límite del subproceso — lento y propenso a errores.
- Quienes quieran aprobación del lado de rousseau usan un proveedor distinto a `claudecli`.

Contrapartida: los usuarios de `claudecli` deben confiar en el modelo de permisos de `claude`. Documentado en [Proveedores: claudecli](/es/providers/claudecli/).

## Siguiente

- [Añadir un transporte](/es/developer-guide/add-a-transport/) — cómo se ve un nuevo implementador de la interfaz.
- [Añadir un proveedor](/es/developer-guide/add-a-provider/) — mismo patrón, distinta interfaz.
- [Añadir una herramienta](/es/developer-guide/add-a-tool/) — el punto de extensión más pequeño.

## Páginas relacionadas

- [Conceptos](/es/concepts/) — recorrido de alto nivel.
- [Bucle del agente](/es/agent-loop/) — la forma en tiempo de ejecución.
- [MCP](/es/mcp/) — exposición externa de herramientas.
- [Configuración](/es/configuration/) — la superficie de configuración de la que lee cada interfaz.

## Lecturas adicionales

- `README.md` — posicionamiento a nivel de repositorio y matriz de capacidades.
- `internal/agent/agent.go` — el bucle central.
- `internal/agent/provider.go` — las interfaces `Provider` y `StreamingProvider`.
- `internal/transport/transport.go` — la interfaz `Transport`.
- `internal/tools/registry.go` — la interfaz `Tool` y `Registry`.
