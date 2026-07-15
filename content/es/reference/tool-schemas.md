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
description: "The exact JSON schemas for the five built-in tools rousseau ships: read, write, edit, grep, bash."
keywords: "tool schemas, read, write, edit, grep, bash, JSON Schema"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/reference/tool-schemas/"
subtitle: "JSON schemas for the five built-in tools, verbatim from internal/tools/builtin."
tags: "reference, tools, json-schema, read, write, edit, grep, bash"
title: "Referencia: esquemas de herramientas"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tool schemas, read, write, edit, grep, bash, JSON Schema"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Referencia: esquemas de herramientas"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 54
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/tool-schemas/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/tool-schemas/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Referencia: esquemas de herramientas"
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
twitter_description: "The exact JSON schemas for the five built-in tools rousseau ships: read, write, edit, grep, bash."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Referencia: esquemas de herramientas"
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

## Qué es esta página

Cada herramienta integrada en `internal/tools/builtin/*.go` publica un método `InputSchema()` que retorna un mapa JSON Schema. Esta página reproduce esos esquemas exactamente, más un párrafo sobre el contrato en tiempo de ejecución de cada herramienta.

Las cinco herramientas integradas son: [`read`](#read), [`write`](#write), [`edit`](#edit), [`grep`](#grep), [`bash`](#bash). Las cinco se construyen en el cableado del daemon; el aprobador (`internal/agent/approver.go`) se sitúa entre la llamada a herramienta del modelo y el método `Execute` de la herramienta.

## read

Fuente: `internal/tools/builtin/read.go`.

**Descripción (expuesta al modelo):** _Read the contents of a UTF-8 text file. Input: absolute path. Returns file contents or an error._

**Esquema de entrada:**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "Absolute filesystem path to the file to read."
    }
  },
  "required": ["path"]
}
```

**Contrato.** El `path` debe ser absoluto (`filepath.IsAbs`). La herramienta lee el archivo completo a memoria y lo rechaza si los primeros 512 bytes contienen un byte NUL (`isLikelyText`). Devuelve el contenido del archivo como cadena en éxito; un error en caso contrario. No se aplica límite de conteo de líneas ni de tamaño a nivel de la herramienta: las políticas de aprobación son el lugar correcto para acotar tamaños de archivo.

## write

Fuente: `internal/tools/builtin/write.go`.

**Descripción (expuesta al modelo):** _Write UTF-8 text to a file, replacing existing contents. Creates parent directories as needed. Input: absolute path + content._

**Esquema de entrada:**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "Absolute filesystem path to write."
    },
    "content": {
      "type": "string",
      "description": "The complete file contents to write."
    }
  },
  "required": ["path", "content"]
}
```

**Contrato.** Sobrescritura del archivo completo. Crea directorios padre con modo `0o755`. Escribe con modo `0o644`. Ruta absoluta requerida. Devuelve `"wrote N bytes to /path"`. Deliberadamente no hay baile de swap atómico: los aprobadores en modo pattern fijan el destino de escritura a un árbol de directorios específico; la herramienta en sí no intenta ser lista sobre seguridad del sistema de archivos.

## edit

Fuente: `internal/tools/builtin/edit.go`.

**Descripción (expuesta al modelo):** _Replace exactly one occurrence of old_string with new_string in a file. old_string must be unique in the file; if it appears zero or multiple times the edit fails. Preserve indentation exactly._

**Esquema de entrada:**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "Absolute filesystem path to the file to edit."
    },
    "old_string": {
      "type": "string",
      "description": "Exact text to find. Must be unique in the file."
    },
    "new_string": {
      "type": "string",
      "description": "Text to replace old_string with."
    }
  },
  "required": ["path", "old_string", "new_string"]
}
```

**Contrato.** Reemplazo por cadena exacta, no regex. `old_string` debe aparecer **exactamente una vez** en el archivo: cero coincidencias o múltiples coincidencias fallan con un error descriptivo, lo cual es intencional (tomado de la herramienta Edit de Claude Code). Previene el mass-replace accidental y fuerza al modelo a incluir suficiente contexto circundante para desambiguar. `old_string == new_string` también falla. Devuelve `"edited /path (1 replacement)"`.

## grep

Fuente: `internal/tools/builtin/grep.go`.

**Descripción (expuesta al modelo):** _Search files under a directory for a Go regular expression. Skips binary files and files larger than the configured limit. Returns 'path:line: matched_line' rows._

**Esquema de entrada:**

```json
{
  "type": "object",
  "properties": {
    "pattern": {
      "type": "string",
      "description": "Go RE2 regular expression to match."
    },
    "path": {
      "type": "string",
      "description": "Absolute directory to search under."
    },
    "include": {
      "type": "string",
      "description": "Optional filename glob (e.g. '*.go'). Applied to the base name."
    },
    "ignore_case": {
      "type": "boolean",
      "description": "Case-insensitive match. Defaults to false."
    }
  },
  "required": ["pattern", "path"]
}
```

**Contrato.** Regex RE2, no PCRE. Insensible a mayúsculas cuando `ignore_case: true` (implementado prefijando `(?i)`). Omite directorios llamados `.git`, `node_modules`, `vendor`, `.venv`, `__pycache__`, `dist`, `build`. Omite archivos más grandes que `MaxFileBytes` (4 MiB por defecto). Trunca la salida a `MaxMatches` (200 por defecto) y añade un pie `(truncated at N matches)` cuando alcanza el límite. Omite archivos que contienen un byte NUL en la línea actual (detección burda de binario).

## bash

Fuente: `internal/tools/builtin/bash.go`.

**Descripción (expuesta al modelo):** _Execute a shell command via `/bin/sh -c`. Returns combined stdout+stderr with exit status._

**Esquema de entrada:**

```json
{
  "type": "object",
  "properties": {
    "command": {
      "type": "string",
      "description": "The shell command to execute."
    }
  },
  "required": ["command"]
}
```

**Contrato.** `/bin/sh -c <command>`. Combinado stdout + stderr, limitado a lo que quepa en un `bytes.Buffer` (es decir, RAM). Timeout de 60 segundos por defecto (configurable en la construcción). En timeout: devuelve salida parcial más un error `bash: timed out after 60s`. **Sin sandboxing a nivel de herramienta.** El usuario de SO del daemon, la vista del sistema de archivos, la postura de red y el perfil seccomp son la contención. Los aprobadores en modo pattern son cómo restringes los comandos permitidos: consulta [Tutorial: Endurecer el aprobador](/es/tutorials/harden-approver-policy/).

## Herramientas expuestas por MCP

El servidor MCP stdio de rousseau (`rousseau mcp`) expone un conjunto **diferente** de herramientas: consultas de solo lectura contra el almacén de sesiones y trabajos cron. Consulta [MCP: Herramientas expuestas](/es/mcp/exposed-tools/) para `rousseau_search_sessions`, `rousseau_list_sessions`, `rousseau_read_session`, `rousseau_cron_list`.

## Relacionado

- [Guía de usuario: Herramientas](/es/user-guide/tools/): la vista orientada al operador.
- [Guías: Gestión de archivos](/es/guides/file-management/): cómo interactúan `write`/`edit` con bind mounts y SELinux.
- [Guías: Auditoría + políticas de aprobación](/es/guides/audit-approval-policies/): cómo las regex pattern restringen la entrada de cada herramienta.
- [Guía del desarrollador: Añadir una herramienta](/es/developer-guide/add-a-tool/): extiende este conjunto.
