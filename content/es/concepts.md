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
description: "Architecture overview of rousseau-agent: agent loop, transport interface, tool registry, approval policies, SQLite session store, MCP server, cron scheduler, skills loader."
keywords: "architecture, agent loop, session, transport, tool registry, approval, MCP, cron, skills, compression, FTS5"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/concepts/"
subtitle: "Cómo encajan el bucle del agente, los transportes y el almacén de sesiones."
tags: "architecture, agent, session, mcp"
title: "Conceptos"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "architecture, agent loop, session, transport, tool registry, approval, MCP, cron, skills, compression, FTS5"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Conceptos"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "concepts"
order: 3
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/concepts/index.html"
item_link: "https://docs.rousseau-agent.dev/concepts/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Conceptos"
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
twitter_description: "Architecture overview of rousseau-agent: agent loop, transport interface, tool registry, approval policies, SQLite session store, MCP server, cron scheduler, skills loader."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Conceptos"
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

## Arquitectura por capas

```
+---------------------------------------------------------------+
|                             CLI                              |
|  chat  whatsapp  slack  discord  ...  mcp  cron  skills      |
+-------------------------+-------------------------------------+
                          |
+-------------------------v-------------------------------------+
|                          Router                              |
|          (per-JID session, allowlist, dispatch)              |
+-------------+---------------------------+---------------------+
              |                           |
     Transport interface           agent.Agent
     Start / Stop / Deliver        Turn / TurnStream
              |                           |
   +----------+----------+       +--------+--------+
   | 9 concrete adapters |       | Provider iface  |
   +---------------------+       | 5 concrete impls|
                                 +--------+--------+
                                          |
                                 +--------v--------+
                                 | Tools Registry  |
                                 | read/write/edit |
                                 | grep/bash + ext |
                                 +--------+--------+
                                          |
                                 +--------v--------+
                                 |  State (SQLite) |
                                 | sessions, cron, |
                                 | jidmap, FTS5    |
                                 +-----------------+
```

El paquete `agent` depende solo de interfaces expuestas por `tools`, de sus propios tipos `Provider` y de la biblioteca estándar. Los proveedores, almacenes y transportes concretos dependen de `agent` — nunca al revés.

## El bucle del agente

`Session → Turn → Provider → ida y vuelta de uso de herramienta`. Cada mensaje del usuario se convierte en una llamada a `Agent.Turn`:

1. **Comprobación de compresión.** El `Compressor` configurado tiene la oportunidad de reescribir la sesión antes de que se ejecute el turno. Cuando lo hace, se establece `Request.CacheableMessages` para que el bloque de resumen se cachee en el siguiente turno.
2. **Apéndice de skills.** Si hay un `SkillsProvider` configurado, inspecciona el último mensaje del usuario y devuelve texto para insertar en el system prompt.
3. **Apéndice de recuperación.** Si hay un `RecallProvider` configurado, consulta el índice FTS5 a través de sesiones anteriores y devuelve texto para insertar.
4. **Llamada al proveedor.** La implementación `Provider.Complete` devuelve un `Response` con un `StopReason`.
5. **Despacho de uso de herramienta.** Si `StopReason == StopToolUse`, cada invocación de herramienta solicitada se envía al `Approver`. Las denegaciones se convierten en errores `tool_result` para que el modelo pueda adaptarse. Las invocaciones permitidas se ejecutan contra el `Registry` y sus salidas se replayean en la siguiente iteración.
6. **Fin del turno.** Bucle hasta que `StopReason == StopEndTurn` o se alcance `MaxIterations` (32 por defecto).

`internal/agent/agent.go` es la referencia canónica.

## Transportes

Cada transporte implementa `transport.Transport`:

```go
type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

`Handler.Handle` recibe un `IncomingMessage` (`From`, `Body`, `At`) y devuelve el texto de la respuesta. El `Router` se sitúa por encima del transporte y es responsable del aislamiento de sesión por remitente, la aplicación de la allowlist y el despacho al `Agent`.

Ninguno de los transportes incluidos expone una superficie HTTP pública por defecto. Slack usa Socket Mode (WebSocket saliente). Discord usa el Gateway (WebSocket saliente). Signal es un subproceso. WhatsApp es el protocolo Web de Meta sobre TCP. Matrix, Telegram, iMessage y correo usan sondeo. SMS es solo de envío porque el lado entrante requeriría un webhook.

## Registro de herramientas

`internal/tools` define la interfaz `Tool` y un `Registry` seguro para concurrencia. Las herramientas incorporadas viven en `internal/tools/builtin/`:

- `read` — lectura de archivo.
- `write` — escritura de archivo.
- `edit` — reemplazo de cadenas con imposición de coincidencia única para prevenir reemplazos masivos accidentales.
- `grep` — búsqueda de texto.
- `bash` — ejecución de comandos. **La frontera de seguridad esencial.**

Cada herramienta declara un esquema JSON estricto. Añadir una herramienta es una sola llamada `registry.MustRegister(myTool)` en el cableado; el núcleo del agente no cambia.

## Políticas de aprobación

Cada invocación de herramienta pasa por `Approver.Approve` antes de la ejecución. Tres políticas incorporadas viven en `internal/agent/approver.go`:

| Modo | Comportamiento |
|---|---|
| `allow_all` | Cada invocación se ejecuta. Razonable con el proveedor `claudecli`, que gestiona sus propias aprobaciones. |
| `deny_all` | Cada invocación se bloquea. Útil para smoke tests y sesiones de solo lectura. |
| `pattern` | Reglas regex de permiso/denegación por herramienta. Deny gana sobre allow. Las solicitudes sin coincidencia vuelven al `Default` (`allow` o `deny`). |

Los motivos de denegación se exponen al modelo como errores `tool_result`, de modo que el modelo tenga la oportunidad de adaptarse en lugar de fallar silenciosamente.

## Almacén de sesiones

`internal/state/sqlite/` implementa la interfaz `state.Store` sobre `modernc.org/sqlite` — Go puro, sin libc, sin CGo. Características:

- **Journaling WAL** con `busy_timeout=15s`.
- **Checkpoint WAL en Close** para que el archivo principal de la base de datos se mantenga consistente para copias de seguridad.
- **Tabla FTS5 de recuperación** que indexa cada mensaje; el `RecallProvider` realiza búsquedas entre sesiones.
- **Tabla de mapa de JID** que normaliza las identidades LID de WhatsApp a JIDs de teléfono.
- **Tabla cron** que persiste tareas programadas entre reinicios.

## Servidor MCP

`internal/mcp/server.go` es un servidor JSON-RPC 2.0 sobre stdio, revisión de especificación **2024-11-05**. `rousseau mcp` lo inicia. Registra herramientas con `server.Register(mcp.ToolSpec{...})` y deja que un cliente (Claude Desktop, una extensión de IDE, otro agente) las utilice.

Los fallos de herramienta se exponen a través del canal `content` con `isError=true`, no del canal de error JSON-RPC — es lo que esperan los hosts MCP.

## Planificador cron

`internal/cron/scheduler.go` envuelve `robfig/cron/v3`. Las tareas se almacenan en SQLite para que sobrevivan a reinicios. Cada disparo llama a `Runner.RunOnce(ctx, prompt)` (un turno de agente de una sola ejecución contra una sesión nueva), luego pasa la respuesta a `Delivery` — una función agnóstica al transporte que envía el mensaje.

Las nuevas tareas añadidas mediante `rousseau cron add` se activan dentro del siguiente `PollInterval` (60s por defecto).

## Cargador de skills

`internal/skills/skills.go` escanea `skills_dir` en busca de archivos `*.md`. Cada archivo puede llevar un front-matter YAML declarando `name`, `description` y `triggers`. Cuando cualquier trigger aparece en el mensaje actual del usuario, el cuerpo del skill se inserta en el system prompt para ese turno. El formato es deliberadamente cercano a la convención de [agentskills.io](https://agentskills.io).

## Compresión

`internal/agent/compressor.go` ejecuta un resumen respaldado por LLM una vez que la sesión supera `TriggerMessages` (60 por defecto). Los `KeepRecent` mensajes más recientes (8 por defecto) sobreviven textualmente; todo lo anterior colapsa en un único bloque de resumen. Desactivado por defecto porque una cuenta de suscripción `claudecli` rara vez lo necesita; actívalo cuando ejecutes contra proveedores de pago por token.

## A dónde ir después

- [Referencia de configuración](/es/configuration/) — cada campo.
- [Referencia del bucle del agente](/es/agent-loop/) — contrato de incrustación como biblioteca.
- [MCP](/es/mcp/) — conexión del cliente.
