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
description: "MCP clients tested against rousseau's stdio server: Claude Desktop, Claude CLI, Continue, Codeium, plus setup snippets."
keywords: "mcp, compatibility, claude desktop, continue, codeium, stdio, claude_desktop_config"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/mcp/compatibility/"
subtitle: "Which MCP clients talk to rousseau's stdio server."
tags: "mcp, compatibility, claude, continue, stdio"
title: "MCP: compatibilidad"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, compatibility, claude desktop, continue, codeium, stdio, claude_desktop_config"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP: compatibilidad"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "mcp"
order: 71
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/mcp/compatibility/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/compatibility/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "MCP: compatibilidad"
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
twitter_description: "MCP clients tested against rousseau's stdio server: Claude Desktop, Claude CLI, Continue, Codeium, plus setup snippets."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP: compatibilidad"
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

## El contrato del protocolo

El servidor MCP de rousseau (`internal/mcp/server.go`) habla JSON-RPC 2.0 sobre stdio y anuncia las herramientas declaradas en `internal/mcp/tools.go`. Maneja estos métodos:

- `initialize`: retorna `ServerCapabilities.Tools`.
- `initialized`: notificación, sin respuesta.
- `ping`: retorna `{}`.
- `tools/list`: retorna las cuatro herramientas en orden de inserción.
- `tools/call`: invoca un handler de herramienta, retorna `ToolsCallResult` con `content` y `isError`.
- `resources/list`, `prompts/list`: retornan arrays vacíos (consulta las notas de roadmap abajo).
- `shutdown`: retorna `{}`.

Cualquier host MCP que hable JSON-RPC stdio y llame a los cuatro métodos de arriba es compatible.

## Clientes probados

| Cliente | Estado | Cómo registrar |
|---|---|---|
| Claude Desktop (macOS / Windows) | Funciona. | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) o `%APPDATA%\Claude\claude_desktop_config.json` (Windows). |
| Claude CLI (`claude`) | Funciona. | `--mcp-config <file>` o un bloque `[mcp]` en `~/.claude/config.json`. |
| Continue.dev (VS Code / JetBrains) | Funciona. | Bloque `mcpServers` en `~/.continue/config.json`. |
| Codeium (extensiones IDE) | Funciona cuando Codeium expone modo host MCP (releases recientes). La configuración varía por IDE. |
| Cursor (versiones recientes) | Funciona. Regístralo bajo la UI de configuración MCP propia de Cursor. |
| Cualquier SDK de host MCP en Go / TypeScript / Python | Funciona. Instancia con `command: "rousseau", args: ["mcp"]`. |

Desconocidos / no probados pero probablemente compatibles: `zed`, `windsurf`, `aider`. Si tu host admite la spec MCP stdio, rousseau funcionará.

## Claude Desktop

Edita `claude_desktop_config.json` (ruta arriba) y añade:

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

Reinicia Claude Desktop. Las cuatro herramientas `rousseau_*` aparecen en el selector de herramientas en la siguiente sesión de chat.

Para estado por workspace, añade una sobrescritura de env:

```json
{
  "mcpServers": {
    "rousseau-work": {
      "command": "/usr/local/bin/rousseau",
      "args": ["--config", "/home/seb/.config/rousseau/work.yaml", "mcp"]
    }
  }
}
```

## CLI de Claude

Apunta el CLI a una configuración:

```sh
claude --mcp-config <(cat <<'JSON'
{
  "mcpServers": {
    "rousseau": {
      "command": "rousseau",
      "args": ["mcp"]
    }
  }
}
JSON
)
```

O consolídalo en `~/.claude/config.json` bajo un bloque `mcpServers` usando la misma forma.

## Continue.dev

Añade a `~/.continue/config.json`:

```json
{
  "mcpServers": [
    {
      "name": "rousseau",
      "command": "rousseau",
      "args": ["mcp"]
    }
  ]
}
```

Continue detecta las herramientas en la siguiente llamada al modelo.

## Cursor

Cursor expone el registro MCP en su UI Settings > MCP. Registra un nuevo servidor llamado `rousseau` con command `rousseau` y args `mcp`. Sin edición de archivos de configuración requerida.

## Codeium

El soporte MCP de Codeium se distribuye tras un feature flag en versiones recientes de la extensión IDE. Consulta la documentación de la extensión: el registro es de nuevo un par `command / args`.

## Variables de entorno y secretos

Como la superficie MCP de rousseau es de solo lectura sobre el almacén de sesiones, no necesita credenciales de proveedor. `ANTHROPIC_API_KEY` y similares no las usa `rousseau mcp`: solo los daemons de transporte / chat que _generan_ sesiones.

## Problemas comunes

- **"El servidor salió inmediatamente."** El comando `mcp` de rousseau abre `state.path`. Si el archivo no es escribible, el proceso sale con no-cero. Ejecuta `rousseau mcp` desde una shell para ver el error exacto.
- **"Unknown tool: rousseau_search_sessions."** El host cacheó una lista de herramientas más antigua. Reinicia el host.
- **Registro duplicado.** Si dos servidores rousseau se registran con el mismo nombre, solo el último gana.

## Recursos y prompts

`resources/list` y `prompts/list` actualmente retornan vacío. La página [Recursos expuestos](/es/mcp/exposed-resources/) rastrea el roadmap para exponer sesiones como recursos MCP.

## Relacionado

- [MCP](/es/mcp/): la referencia paraguas.
- [MCP: Herramientas expuestas](/es/mcp/exposed-tools/): cada firma de herramienta.
- [MCP: Recursos expuestos](/es/mcp/exposed-resources/): roadmap.
- [Tutorial: Exponer herramientas vía MCP](/es/tutorials/expose-tools-via-mcp/): ejemplo probado.
