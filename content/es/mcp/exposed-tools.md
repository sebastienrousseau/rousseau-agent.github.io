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
date: "July 13, 2026"
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
description: "The exact tool signatures exposed by rousseau's stdio MCP server, mirroring internal/mcp/tools.go."
keywords: "mcp, rousseau_search_sessions, rousseau_list_sessions, rousseau_read_session, rousseau_cron_list"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/mcp/exposed-tools/"
subtitle: "Every tool rousseau's MCP server advertises, with schemas."
tags: "mcp, tools, sessions, cron"
title: "MCP: herramientas expuestas"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, rousseau_search_sessions, rousseau_list_sessions, rousseau_read_session, rousseau_cron_list"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP: herramientas expuestas"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "mcp"
order: 72
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/mcp/exposed-tools/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/exposed-tools/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "MCP: herramientas expuestas"
last_build_date: "Mon, 13 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
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
twitter_description: "The exact tool signatures exposed by rousseau's stdio MCP server, mirroring internal/mcp/tools.go."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP: herramientas expuestas"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Gracias a cada operador que ejecuta su propio agente de codificación."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Registro

`internal/cli/mcp.go` abre el almacén de sesiones SQLite, construye un `NewCronStore`, envuelve ambos en `mcp.NewStoreBackend` y llama a `mcp.RegisterRousseauTools(s, backend)`. Las cuatro herramientas siguientes se adjuntan en orden de inserción: `tools/list` las retorna en este orden exacto.

Cada herramienta es de solo lectura. No hay superficie de escritura por MCP hoy; es por diseño para que un host MCP no pueda mutar el estado de rousseau.

## `rousseau_search_sessions`

**Descripción (expuesta a los hosts):** _Full-text search across every recorded rousseau session. Uses SQLite FTS5 syntax (phrases in double quotes, AND/OR/NOT, prefix wildcards)._

**Esquema de entrada:**

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Consulta FTS5"
    },
    "limit": {
      "type": "integer",
      "description": "Límite de resultados. Por defecto 20."
    }
  },
  "required": ["query"]
}
```

**Comportamiento.** Pasa `query` textualmente al motor FTS5 de SQLite (`Store.Search` en `internal/state/sqlite/search.go`). Los resultados se ordenan por rank BM25 (menor = más relevante). Cada resultado se renderiza como tres líneas:

```
session <id> (rank 0.42)
    title:   <session title>
    snippet: <snippet de ~200 caracteres con … puntos suspensivos>
```

**Errores.** Una consulta vacía retorna `query is required`. Los errores de sintaxis FTS5 burbujean como errores de SQLite y se muestran vía `isError: true`.

## `rousseau_list_sessions`

**Descripción (expuesta a los hosts):** _List rousseau sessions newest-first._

**Esquema de entrada:**

```json
{
  "type": "object",
  "properties": {
    "limit": {
      "type": "integer",
      "description": "Límite de filas retornadas. Por defecto 20."
    }
  }
}
```

**Comportamiento.** Llama a `Store.List` que usa el índice `idx_sessions_updated_at DESC`. Cada fila:

```
<session-id>  <title>  msgs=<count>  updated=<iso-8601>
```

Retorna `(no sessions)` cuando el almacén está vacío.

## `rousseau_read_session`

**Descripción (expuesta a los hosts):** _Return the full transcript of a rousseau session by id._

**Esquema de entrada:**

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "description": "ID de sesión"
    }
  },
  "required": ["id"]
}
```

**Comportamiento.** Llama a `Store.Load` para obtener el `agent.Session` completo. Se renderiza como:

```
id: <session-id>
title: <session title>
created: <iso-8601>
updated: <iso-8601>
messages: <count>

[0] user
    <text content>
[1] assistant
    <text content>
    ...
```

Solo se renderiza contenido de texto: los bloques tool_use y tool_result se eliden en la superficie MCP (el CLI `rousseau session show` los incluye; MCP intencionalmente no).

**Errores.** `id is required` en entrada vacía. `state.ErrNotFound` en id desconocido.

## `rousseau_cron_list`

**Descripción (expuesta a los hosts):** _List rousseau's scheduled cron jobs (name, schedule, prompt, delivery target)._

**Esquema de entrada:**

```json
{
  "type": "object",
  "properties": {}
}
```

**Comportamiento.** Llama a `CronStore.List`: una fila por fila de `cron_jobs`:

```
<name> [<on|off>] <cron-expr> → <deliver-to>  prompt="<prompt>"  deliver=<deliver-to>
```

Retorna `(no jobs)` cuando la tabla cron está vacía. También retorna `(no jobs)` si el `CronStore` es nil en tiempo de construcción (una ruta defensiva en `storeBackend.CronList`).

## Lo que NO se expone

Omisiones deliberadas:

| Superficie | Por qué no |
|---|---|
| `rousseau_write_session` / `rousseau_delete_session` | Mutación por MCP permitiría a un host no confiable reformar el rastro de auditoría de rousseau. |
| `rousseau_add_cron` | Misma razón: mutación. Añade trabajos cron vía `rousseau cron add`. |
| Las herramientas integradas (`read`, `write`, `edit`, `grep`, `bash`) | Estas son herramientas orientadas al agente para el LLM dentro del bucle propio de rousseau, no orientadas al host. Exponerlas daría al host MCP la capacidad de hacer shell out en el host que ejecuta rousseau: precisamente el flip de confianza que no queremos. |
| Búsqueda del mapa JID | Expone PII (números de teléfono). Si lo necesitas, consulta SQLite directamente en la máquina donde se ejecuta el daemon. |

## Superficie de errores

Los handlers MCP retornan `([]Content, error)`. En caso de error, el servidor (`internal/mcp/server.go` `handleToolsCall`) expone el error como `ToolsCallResult{Content: texto del err, IsError: true}`. Esto es por la convención MCP: las fallas de herramientas fluyen por el canal de contenido con `isError=true`, no por el canal `error` de JSON-RPC. Los hosts deben renderizar el texto y continuar.

## Relacionado

- [MCP](/es/mcp/): la referencia paraguas.
- [MCP: Compatibilidad](/es/mcp/compatibility/): clientes probados.
- [MCP: Recursos expuestos](/es/mcp/exposed-resources/): roadmap.
- [Referencia: Esquemas de herramientas](/es/reference/tool-schemas/): el conjunto diferente de herramientas orientadas al agente.
