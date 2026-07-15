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
description: "rousseau-agent's MCP server exposes its tools and sessions over stdio JSON-RPC. Compatible with Claude Desktop and any MCP host."
keywords: "MCP, Model Context Protocol, JSON-RPC, stdio, Claude Desktop, tools, sessions"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/mcp/"
subtitle: "JSON-RPC 2.0 sobre stdio, revisión de spec 2024-11-05."
tags: "MCP, reference"
title: "Servidor MCP"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "MCP, Model Context Protocol, JSON-RPC, stdio, Claude Desktop, tools, sessions"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Servidor MCP"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 21
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/mcp/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Servidor MCP"
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
twitter_description: "rousseau-agent's MCP server exposes its tools and sessions over stdio JSON-RPC. Compatible with Claude Desktop and any MCP host."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Servidor MCP"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Lo que aprenderás</span><p>El formato de cable JSON-RPC 2.0 completo que habla rousseau, todos los métodos que implementa el servidor MCP de rousseau con pares de solicitud/respuesta de ejemplo, la semántica de los códigos de error, y cómo configurar hosts MCP de Claude Desktop / Cursor / IDE para alcanzar el servidor. Lee <code>internal/mcp/protocol.go</code> y <code>internal/mcp/server.go</code> junto con esta página.</p></aside>

## Formato de cable

`rousseau mcp` inicia un servidor MCP que habla JSON-RPC 2.0 sobre stdio, según la especificación [Model Context Protocol](https://modelcontextprotocol.io) revisión **2024-11-05** (declarada en `ProtocolVersion` en `internal/mcp/protocol.go`).

- Una solicitud por línea en stdin (`bufio.Scanner` lee hasta 8 MiB por línea).
- Una respuesta por línea en stdout (`json.NewEncoder` emite JSON delimitado por saltos de línea).
- El servidor se bloquea hasta que stdin se cierre o `ctx` sea cancelado.

### Envoltura JSON-RPC 2.0

Cada solicitud, notificación y respuesta usa esta envoltura (de `internal/mcp/protocol.go` línea 38):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

Los campos presentes dependen del tipo de envoltura:

| Campo | Solicitud | Notificación | Respuesta |
|---|:---:|:---:|:---:|
| `jsonrpc` | siempre `"2.0"` | siempre `"2.0"` | siempre `"2.0"` |
| `id` | requerido | ausente | reflejado desde la solicitud |
| `method` | requerido | requerido | ausente |
| `params` | opcional | opcional | ausente |
| `result` | ausente | ausente | solo en éxito |
| `error` | ausente | ausente | solo en fallo |

Las notificaciones no llevan `id` y no reciben respuesta. rousseau solo recibe una notificación (`notifications/initialized`), que se acepta silenciosamente.

### Referencia de métodos

`Server.dispatch` de rousseau (`internal/mcp/server.go` línea 112) enruta estos métodos:

| Método | Propósito | Respuesta |
|---|---|---|
| `initialize` | Handshake. El cliente declara la versión del protocolo y las capacidades. | `InitializeResult` |
| `notifications/initialized` | El cliente confirma que está listo. | (notificación, sin respuesta) |
| `ping` | Sondeo de vida. | `{}` |
| `tools/list` | Enumera las herramientas registradas. | `ToolsListResult` |
| `tools/call` | Invoca una herramienta. | `ToolsCallResult` |
| `resources/list` | Marcador de posición. Hoy devuelve `{ "resources": [] }`. | `{"resources": []}` |
| `prompts/list` | Marcador de posición. Devuelve `{ "prompts": [] }`. | `{"prompts": []}` |
| `shutdown` | Cierre iniciado por el cliente. | `{}` |

<aside class="admonition" data-type="note"><span class="admonition-title">Métodos faltantes</span><p><code>resources/list</code> y <code>prompts/list</code> devuelven arrays vacíos para que los hosts que los sondean no fallen. El soporte completo de recursos/prompts está en el roadmap; consulta <code>docs/GAP_ANALYSIS_2026.md</code>.</p></aside>

## Ejemplos de solicitud/respuesta

### 1. `initialize`

El cliente envía:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","clientInfo":{"name":"claude-desktop","version":"0.7.0"}}}
```

El servidor responde:

```json
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05","serverInfo":{"name":"rousseau","version":"0.6.0"},"capabilities":{"tools":{"listChanged":false}}}}
```

`listChanged: false` porque el conjunto de herramientas de rousseau es estático al inicio del proceso: no hay añadidos ni eliminaciones en tiempo de ejecución.

### 2. `tools/list`

```json
{"jsonrpc":"2.0","id":2,"method":"tools/list"}
```

El servidor responde con las herramientas registradas en el orden de inserción:

```json
{"jsonrpc":"2.0","id":2,"result":{"tools":[
  {"name":"read","description":"Read a file...","inputSchema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
  {"name":"grep","description":"Search for a regex...","inputSchema":{"type":"object","properties":{"pattern":{"type":"string"},"path":{"type":"string"}},"required":["pattern"]}},
  {"name":"bash","description":"Execute a shell command...","inputSchema":{"type":"object","properties":{"command":{"type":"string"}},"required":["command"]}}
]}}
```

### 3. `tools/call`

```json
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"read","arguments":{"path":"/etc/hostname"}}}
```

Éxito:

```json
{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"my-host.example.com\n"}]}}
```

Fallo a nivel de handler (surge como contenido, no como un error JSON-RPC; es convención de MCP):

```json
{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"read: open /nope: no such file or directory"}],"isError":true}}
```

### 4. `ping`

```json
{"jsonrpc":"2.0","id":4,"method":"ping"}
```

```json
{"jsonrpc":"2.0","id":4,"result":{}}
```

## Códigos de error

Rousseau usa el rango estándar de errores JSON-RPC 2.0 más una extensión de MCP:

| Código | Constante | Significado | Cuándo se emite |
|---|---|---|---|
| -32700 | `CodeParseError` | JSON inválido en la envoltura. | La envoltura falló en `json.Unmarshal`. |
| -32600 | `CodeInvalidRequest` | La forma de la envoltura es incorrecta. | El campo `jsonrpc` no es `"2.0"`. |
| -32601 | `CodeMethodNotFound` | Método no implementado. | El dispatch cayó en el caso predeterminado. |
| -32602 | `CodeInvalidParams` | Los parámetros no se pudieron decodificar. | `params` no se deserializó a la forma esperada. |
| -32603 | `CodeInternalError` | Algo falló al serializar la respuesta. | Raro; indica un bug. |
| -32000 | `CodeToolNotFound` | El nombre de la herramienta no está registrado. | `tools/call` con un `name` desconocido. |

<aside class="admonition" data-type="warning"><span class="admonition-title">Errores de herramienta vs. errores JSON-RPC</span><p>Los fallos a nivel de handler —un comando <code>bash</code> que sale con código distinto de cero, un <code>read</code> contra un archivo inexistente— se retornan mediante <code>result.content</code> con <code>isError: true</code>, NO a través del campo <code>error</code> de JSON-RPC. Solo los fallos a nivel de protocolo usan <code>error</code>. Los hosts que tratan ambos canales como equivalentes clasificarán mal los fallos recuperables.</p></aside>

## Qué se expone

Dos superficies:

- **Herramientas.** Cada `mcp.ToolSpec` registrado antes de `Serve` se anuncia en `tools/list` y puede invocarse vía `tools/call`. rousseau conecta las mismas implementaciones de herramientas que usa el bucle del agente local: `read`, `write`, `edit`, `grep`, `bash`.
- **Sesiones.** El almacén de sesiones SQLite de rousseau se expone para que un host MCP pueda enumerar y leer conversaciones pasadas. `resources/list` devuelve una entrada por sesión.

Los fallos de herramientas se emergen a través del canal `content` con `isError=true`, no por el canal de error JSON-RPC. Es la convención de MCP.

## Configuración del cliente — Claude Desktop

Añade a `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) o el equivalente en tu plataforma:

```json
{
  "mcpServers": {
    "rousseau": {
      "command": "rousseau",
      "args": ["mcp"],
      "env": {
        "HOME": "/Users/you"
      }
    }
  }
}
```

Reinicia Claude Desktop. `rousseau` aparecerá en la paleta de herramientas; toda herramienta registrada se puede invocar.

Para un rousseau empaquetado en una imagen Podman, la entrada queda así:

```json
{
  "mcpServers": {
    "rousseau": {
      "command": "podman",
      "args": [
        "run", "--rm", "-i",
        "-v", "/Users/you/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z",
        "localhost/rousseau-agent:local",
        "mcp"
      ]
    }
  }
}
```

Monta con bind-mount el directorio de estado para que el host MCP vea las mismas sesiones que el servicio.

## Registrar una herramienta personalizada

Integrando el servidor MCP en tu propio binario:

```go
srv := mcp.NewServer("rousseau", "0.1.0", logger)

srv.MustRegister(mcp.ToolSpec{
    Name:        "count_files",
    Description: "Count files under a path.",
    InputSchema: json.RawMessage(`{
      "type": "object",
      "properties": {"path": {"type": "string"}},
      "required": ["path"]
    }`),
    Handler: func(ctx context.Context, args json.RawMessage) ([]mcp.Content, error) {
        var in struct{ Path string }
        if err := json.Unmarshal(args, &in); err != nil {
            return nil, fmt.Errorf("bad input: %w", err)
        }
        // ... count files ...
        return []mcp.Content{{Type: "text", Text: fmt.Sprintf("%d", n)}}, nil
    },
})

_ = srv.Serve(ctx, os.Stdin, os.Stdout)
```

Las registros duplicados devuelven un error; `MustRegister` produce panic ante duplicados (reservado para el cableado en `main`).

## Concurrencia

`Serve` puede llamarse de forma concurrente sobre transportes independientes (stdin/stdout para el host MCP, más un canal de control si lo deseas). El mapa de herramientas del servidor está protegido por un RWMutex; la ejecución de los handlers no se serializa: las implementaciones deben ser seguras para uso concurrente.

## Depuración

Cada envoltura de solicitud/respuesta se registra a nivel `debug` por defecto. Habilita con:

```yaml
log:
  level: debug
  format: text
```

O:

```sh
ROUSSEAU_LOG_LEVEL=debug rousseau mcp 2>/tmp/mcp.log
```

El host MCP consume stdout; mantén el flujo de logs en stderr.

## Solución de problemas

### Claude Desktop / Cursor nunca muestra las herramientas de rousseau

Casi siempre es un error de cableado, no un problema de rousseau. Verifica: (1) que `command` y `args` en la configuración del host invocan `rousseau mcp` (no `rousseau chat`); (2) que el archivo de configuración se guardó y el host se reinició; (3) que `rousseau mcp </dev/null` desde una shell no falla; si lo hace, corrige eso primero.

### `parse error` en el primer mensaje

El host no envía JSON delimitado por líneas. Algunas implementaciones tempranas de MCP envían mensajes enmarcados (`Content-Length: N\r\n\r\n<body>`); rousseau espera delimitación con `\n`. Actualiza el host a una versión que use enmarcado stdio (todos los hosts principales actuales lo hacen).

### `method not found: <foo>`

El host llama a un método que rousseau no implementa. Los `resources/list` y `prompts/list` vacíos se proveen como no-ops para las sondas comunes; cualquier otro método devuelve `-32601`. Consulta `dispatch()` en `internal/mcp/server.go` para la lista completa de métodos.

### Las llamadas a herramientas tienen éxito pero el host las reporta como errores

El handler de la herramienta devolvió el error de forma incorrecta. Los handlers deben devolver `[]Content{{Type: "text", Text: err.Error()}}, err != nil`; rousseau captura el error y lo envuelve en `isError: true`. No devuelvas el error por el canal `error` de JSON-RPC salvo que sea un fallo a nivel de protocolo.

### El MCP basado en contenedor falla con `permission denied` en el directorio de estado

La invocación `podman run` desde Claude Desktop debe incluir un `-v` para el directorio de estado con la etiqueta SELinux correcta. Usa `:Z` (privada) a menos que el contenedor se comparta con otras cargas de trabajo Podman. Verifica también que el UID del host dentro del contenedor coincida con la propiedad de los archivos.

## Páginas relacionadas

- [MCP: Herramientas expuestas](/es/mcp/exposed-tools/) — el conjunto de herramientas que rousseau publica.
- [MCP: Recursos expuestos](/es/mcp/exposed-resources/) — enumeración y lectura de sesiones.
- [MCP: Compatibilidad](/es/mcp/compatibility/) — matriz de hosts probados.
- [Tutoriales: Exponer herramientas vía MCP](/es/tutorials/expose-tools-via-mcp/) — recorrido completo.
- [Bucle del agente](/es/agent-loop/) — cómo se usan las mismas herramientas dentro de rousseau.

## Lecturas adicionales

- `internal/mcp/protocol.go` — envoltura, nombres de métodos, códigos de error.
- `internal/mcp/server.go` — `Serve`, `dispatch`, registro de herramientas.
- `internal/mcp/tools.go` — ayudantes para registrar las herramientas integradas de rousseau.
- `internal/cli/mcp.go` — cableado del comando `rousseau mcp`.
- [Especificación de Model Context Protocol](https://modelcontextprotocol.io) — referencia externa.
