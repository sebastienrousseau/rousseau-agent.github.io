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
description: "Expose rousseau's session store and cron jobs to Claude Desktop as an MCP server that Claude can drive from its own tool interface."
keywords: "mcp, claude desktop, stdio, tools, rousseau_search_sessions, rousseau_read_session"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/tutorials/expose-tools-via-mcp/"
subtitle: "Wire rousseau mcp into Claude Desktop and let it query the session store."
tags: "tutorials, mcp, claude-desktop, stdio, sessions"
title: "Tutorial: exponer herramientas mediante MCP"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, claude desktop, stdio, tools, rousseau_search_sessions, rousseau_read_session"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorial: exponer herramientas mediante MCP"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/expose-tools-via-mcp/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/expose-tools-via-mcp/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorial: exponer herramientas mediante MCP"
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
twitter_description: "Expose rousseau's session store and cron jobs to Claude Desktop as an MCP server that Claude can drive from its own tool interface."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorial: exponer herramientas mediante MCP"
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

## Qué construyes

Claude Desktop con rousseau como servidor MCP stdio. Desde dentro de un chat de Claude Desktop puedes preguntar "encuentra la sesión donde discutimos la lógica de reintentos" y Claude llamará a `rousseau_search_sessions`, luego a `rousseau_read_session` para obtener la transcripción completa.

Tiempo estimado: 5 minutos.

## Requisitos previos

- Claude Desktop instalado (macOS o Windows). Linux usa el CLI de Claude, no Desktop: consulta la alternativa al final.
- Rousseau instalado y en `$PATH`.
- Historial de sesiones existente en `~/.local/share/rousseau/sessions.db`: ejecuta `rousseau chat` unas cuantas veces si el archivo está vacío.

## Paso 1: entender qué se expone

`rousseau mcp` (`internal/cli/mcp.go`) inicia un servidor JSON-RPC stdio que habla el Model Context Protocol. `RegisterRousseauTools` (`internal/mcp/tools.go`) adjunta cuatro herramientas de solo lectura:

| Herramienta | Propósito |
|---|---|
| `rousseau_search_sessions` | Búsqueda full-text FTS5 en cada sesión registrada (vía `internal/state/sqlite/search.go`). |
| `rousseau_list_sessions` | Lista las sesiones, las más recientes primero. |
| `rousseau_read_session` | Devuelve la transcripción completa de una sesión por id. |
| `rousseau_cron_list` | Lista los trabajos cron programados de rousseau. |

No hay herramientas de escritura; los hosts MCP pueden explorar pero no mutar. Consulta [MCP: Herramientas expuestas](/es/mcp/exposed-tools/) para los esquemas de entrada exactos.

## Paso 2: conectar Claude Desktop

Claude Desktop lee `claude_desktop_config.json`:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Añade una entrada `mcpServers` apuntando a tu binario `rousseau`:

```json
{
  "mcpServers": {
    "rousseau": {
      "command": "/usr/local/bin/rousseau",
      "args": ["mcp"]
    }
  }
}
```

Reinicia Claude Desktop.

## Paso 3: verificar

Abre un chat de Claude Desktop y comprueba que las herramientas aparecen en el selector de herramientas. Deberías ver cuatro herramientas con prefijo `rousseau_`. Prueba:

```
Use rousseau_list_sessions to show me my 5 most recent sessions,
then read the top one with rousseau_read_session.
```

Claude invocará ambas herramientas, y el servidor MCP de rousseau (`internal/mcp/server.go`) manejará cada envelope JSON-RPC por stdin/stdout. Detrás de escena:

1. Claude Desktop llama a `initialize`, luego a `tools/list`: rousseau responde con las cuatro herramientas declaradas en orden de inserción.
2. Claude elige una herramienta y llama a `tools/call` con los argumentos: el handler de rousseau (de `internal/mcp/tools.go`) consulta SQLite y devuelve contenido de texto.
3. En caso de error, rousseau expone el error a través del canal de contenido (`isError=true`), nunca como un error JSON-RPC: los hosts MCP esperan esto.

## Paso 4: (opcional) conectar con el CLI de Claude u otro host MCP

El protocolo stdio es agnóstico al host. Para el CLI de Claude:

```sh
claude --mcp-config <(cat <<'JSON'
{ "mcpServers": { "rousseau": { "command": "rousseau", "args": ["mcp"] } } }
JSON
)
```

Para Continue.dev, Codeium u otro host MCP, sigue su flujo de registro de servidor MCP con `command: rousseau`, `args: [mcp]`. Consulta [MCP: Compatibilidad](/es/mcp/compatibility/) para los clientes probados.

## Paso 5: chuleta de sintaxis FTS5

Como rousseau_search_sessions es un envoltorio delgado sobre SQLite FTS5 (`internal/state/sqlite/search.go`), el campo de consulta admite:

| Consulta | Significado |
|---|---|
| `retry logic` | Cualquier documento que contenga ambos términos. |
| `"retry logic"` | Frase exacta. |
| `retr*` | Coincidencia por prefijo. |
| `retry OR backoff` | OR booleano. |
| `retry NOT retries` | Exclusión. |

El ranking usa BM25 (rank menor = más relevante); la llamada `snippet()` en `Search` te da una vista previa de 200 caracteres por resultado.

## Solución de problemas

- **"unknown tool" en Claude Desktop.** Reinicia la aplicación. La lista de herramientas solo se obtiene al iniciar la sesión.
- **El servidor sale inmediatamente.** `rousseau mcp` abre el archivo de estado SQLite; si la ruta en `state.path` no es escribible, `Open()` falla y el proceso sale con un código distinto de cero. Ejecútalo desde un shell para ver el error.
- **Resultados de búsqueda vacíos.** Confirma que el índice FTS5 está poblado: `sqlite3 ~/.local/share/rousseau/sessions.db "SELECT count(*) FROM sessions_fts"`. `EnsureSearch` en `internal/state/sqlite/search.go` rellena el índice en cada open, pero un archivo de estado corrupto podría necesitar una reconstrucción manual.

## Relacionado

- [MCP](/es/mcp/): el documento de referencia.
- [MCP: Herramientas expuestas](/es/mcp/exposed-tools/): cada esquema de herramienta.
- [MCP: Compatibilidad](/es/mcp/compatibility/): clientes probados.
- [Referencia: Almacén de sesiones](/es/reference/session-store/): el esquema SQLite detrás de las herramientas.
