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
description: "The five built-in tools shipped with rousseau-agent: read, write, edit, grep, bash. JSON schemas, execution semantics, safety notes."
keywords: "tools, read, write, edit, grep, bash, json schema, tool registry"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/user-guide/tools/"
subtitle: "The five built-in tools, with schemas and safety notes."
tags: "tools, reference, read, write, edit, grep, bash"
title: "Herramientas integradas"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tools, read, write, edit, grep, bash, json schema, tool registry"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Herramientas integradas"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 42
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/tools/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/tools/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Herramientas integradas"
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
twitter_description: "The five built-in tools shipped with rousseau-agent: read, write, edit, grep, bash. JSON schemas, execution semantics, safety notes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Herramientas integradas"
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

## Qué se incluye

`internal/tools/builtin/` proporciona las cinco herramientas que todo daemon de rousseau conecta por defecto (consulta `internal/cli/chat.go` para el cableado):

| Herramienta | Propósito | ¿Muta? |
|---|---|:---:|
| `read` | Lectura de archivo de texto UTF-8. | No |
| `write` | Sobrescritura de archivo de texto UTF-8. Crea directorios padre. | Sí |
| `edit` | Reemplazo por cadena exacta, se requiere coincidencia única. | Sí |
| `grep` | Búsqueda regex RE2 bajo un directorio. | No |
| `bash` | `/bin/sh -c <cmd>` con un timeout. | Sí |

Cada una se registra vía `registry.MustRegister(builtin.NewXTool())`. Registra herramientas adicionales sin tocar el núcleo del agente: consulta [Guía del desarrollador: Añadir una herramienta](/es/developer-guide/add-a-tool/).

## `read`

Lee un archivo de texto UTF-8 desde el sistema de archivos local.

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

**Semántica:**

- `path` debe ser absoluto; las rutas relativas se rechazan.
- Rechaza contenido binario mediante una detección de `\x00` sobre los primeros 512 bytes.
- Devuelve el contenido del archivo textualmente como una cadena.

**Errores:** ruta faltante, ruta relativa, archivo no legible, contenido no de texto.

## `write`

Escribe texto UTF-8 en un archivo, reemplazando el contenido existente. Crea directorios padre según sea necesario.

**Esquema de entrada:**

```json
{
  "type": "object",
  "properties": {
    "path":    { "type": "string", "description": "Absolute filesystem path to write." },
    "content": { "type": "string", "description": "The complete file contents to write." }
  },
  "required": ["path", "content"]
}
```

**Semántica:**

- Sobrescribe el archivo (no anexa). Usa `edit` para cambios incrementales.
- `MkdirAll(dir, 0o755)` en el directorio padre.
- El archivo se escribe con permiso `0o644`.
- Devuelve `wrote <n> bytes to <path>` en caso de éxito.

**Errores:** ruta faltante, ruta relativa, fallo de mkdir, fallo de escritura.

## `edit`

Reemplazo por cadena exacta con una **restricción de coincidencia única**. Tomado de la herramienta Edit de Claude Code.

**Esquema de entrada:**

```json
{
  "type": "object",
  "properties": {
    "path":       { "type": "string", "description": "Absolute filesystem path to the file to edit." },
    "old_string": { "type": "string", "description": "Exact text to find. Must be unique in the file." },
    "new_string": { "type": "string", "description": "Text to replace old_string with." }
  },
  "required": ["path", "old_string", "new_string"]
}
```

**Semántica:**

- `old_string` debe aparecer **exactamente una vez** en el archivo. Cero ocurrencias → error. Dos o más → error (pide al modelo que proporcione más contexto circundante).
- `old_string == new_string` → error (las ediciones sin operación se rechazan).
- Preserva la indentación y los espacios en blanco textualmente.
- Devuelve `edited <path> (1 replacement)` en caso de éxito.

La regla de coincidencia única es deliberada: impide que el modelo realice un reemplazo masivo accidental. Cuando el modelo quiere cambiar cada ocurrencia, tiene que crear múltiples llamadas `edit`, cada una con suficiente contexto circundante para desambiguar.

**Errores:** ruta faltante / relativa, `old_string` faltante, sin coincidencia, coincidencia no única, cadenas idénticas, fallo de lectura / escritura.

## `grep`

Búsqueda regex bajo un directorio. Deliberadamente más simple que ripgrep: sin dependencia, se ejecuta in-process.

**Esquema de entrada:**

```json
{
  "type": "object",
  "properties": {
    "pattern":     { "type": "string",  "description": "Go RE2 regular expression to match." },
    "path":        { "type": "string",  "description": "Absolute directory to search under." },
    "include":     { "type": "string",  "description": "Optional filename glob (e.g. '*.go'). Applied to the base name." },
    "ignore_case": { "type": "boolean", "description": "Case-insensitive match. Defaults to false." }
  },
  "required": ["pattern", "path"]
}
```

**Semántica:**

- Sintaxis Go [RE2](https://github.com/google/re2/wiki/Syntax): sin retrorreferencias, sin lookaround.
- Recorre `path` recursivamente. Omite `.git`, `node_modules`, `vendor`, `.venv`, `__pycache__`, `dist`, `build`.
- Omite archivos más grandes que `MaxFileBytes` (4 MiB por defecto) y contenido binario.
- Limita la salida a `MaxMatches` (200 por defecto); la truncación se anota inline.
- Devuelve filas `<path>:<line>: <matching-line>`.
- Devuelve la cadena `no matches` cuando nada coincidió.

**Errores:** patrón / ruta faltantes, ruta relativa, regex inválida, glob de include inválido.

## `bash`

Ejecuta un comando shell mediante `/bin/sh -c`. **La frontera de seguridad crítica.**

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

**Semántica:**

- Se ejecuta bajo `/bin/sh -c <command>`. No es específico de bash: shell POSIX.
- Se devuelve stdout+stderr combinados.
- Timeout por defecto: 60 segundos. Configurable en el registro vía `NewBashTool(timeout)`.
- El timeout devuelve un error `bash: timed out after <duration>` junto con cualquier salida producida antes del vencimiento.
- Una salida distinta de cero produce un error cuya cadena envuelve el estado de salida; la salida sigue devolviéndose para que el modelo la inspeccione.

**Seguridad:**

- La herramienta no tiene allowlist integrada. El [Aprobador](/es/user-guide/approval-policies/) es la puerta crítica. **Siempre** habilita aprobación en modo pattern en daemons desatendidos.
- El comando se ejecuta con el UID y la visibilidad del sistema de archivos del daemon. Coloca por debajo un contenedor rootless ([Despliegue](/es/deployment/)).

## Errores de herramienta y el bucle

Cuando una herramienta devuelve un error, el agente lo convierte en un bloque `tool_result` con `isError: true` y lo retroalimenta al modelo en la siguiente iteración:

```
[user] make the change
[assistant] tool_use: edit {"path": "/tmp/foo", "old_string": "x", "new_string": "y"}
[user]      tool_result: "edit: old_string not found in /tmp/foo" (isError=true)
[assistant] I couldn't find "x" in /tmp/foo. Could you confirm the path?
```

Este es el mismo canal usado para las denegaciones del aprobador: consulta [Políticas de aprobación](/es/user-guide/approval-policies/).

## Registrar herramientas adicionales

```go
registry := tools.NewRegistry()
registry.MustRegister(builtin.NewReadTool())
registry.MustRegister(builtin.NewWriteTool())
registry.MustRegister(builtin.NewEditTool())
registry.MustRegister(builtin.NewGrepTool(0, 0))    // zero → defaults
registry.MustRegister(builtin.NewBashTool(60 * time.Second))
registry.MustRegister(myCustomTool)                  // any tools.Tool
```

`tools.Registry` es seguro para concurrencia; el registro es thread-safe.

## Implicaciones de seguridad de un vistazo

| Herramienta | Radio de impacto | Cuándo NO usar |
|---|---|---|
| `read` | Lee archivos con la visibilidad de FS del daemon. Puede exfiltrar cualquier archivo legible. | Si hay material secreto en disco en el workspace. Restringe mediante la regex `match` del aprobador. |
| `grep` | Igual que read más un costo de CPU por regex. | Si haces match contra patrones no confiables: ReDoS es posible con regex patológicas. |
| `edit` | Modifica el contenido de archivos in-place. | Si la visibilidad de FS del daemon se extiende más allá del workspace previsto. Combina con un bind mount de contenedor. |
| `write` | Crea/sobrescribe archivos. | Igual que edit, además puede crear archivos en cualquier lugar donde el daemon pueda escribir. |
| `bash` | Ejecución arbitraria de comandos. | En cualquier daemon desatendido sin un aprobador en modo pattern. **La frontera de seguridad principal.** |

## Solución de problemas

### `read: read /path: is a directory`

La herramienta `read` es solo para archivos. Usa `grep` con un patrón de ruta o `bash` (con `ls`) si necesitas contenidos de directorio.

### `edit: old_string not found`

El `old_string` propuesto por el modelo no coincidió byte por byte con el contenido del archivo. Causas comunes: desviación de espacios/saltos de línea, estilo incorrecto de fin de línea, el archivo fue editado entre la lectura del modelo y la llamada edit.

### `edit: old_string is not unique`

La herramienta `edit` de rousseau rechaza ediciones ambiguas: el modelo debe incluir suficiente contexto circundante para hacer de `old_string` una subcadena única. Esto previene reemplazo accidental en múltiples ubicaciones.

### `bash: timed out after 1m0s`

Timeout por defecto de 60s. Los comandos de larga ejecución (build, test) fallarán. Aumenta el timeout con `NewBashTool(2*time.Minute)` al integrar, o divide en pasos más rápidos.

### `grep` no devuelve nada pero el patrón definitivamente está ahí

El `grep` de rousseau usa el paquete `regexp` de Go (RE2), que no admite todas las características de PCRE. Las retrorreferencias y lookarounds fallarán silenciosamente. Reescribe el patrón para RE2.

## Páginas relacionadas

- [Guía de usuario: Políticas de aprobación](/es/user-guide/approval-policies/): la puerta en cada llamada a herramienta.
- [Guía del desarrollador: Añadir una herramienta](/es/developer-guide/add-a-tool/): construye la tuya propia.
- [Conceptos](/es/concepts/): cómo encajan las herramientas en el bucle del agente.
- [Bucle del agente](/es/agent-loop/): cómo los resultados de herramientas alimentan el siguiente turno.
- [Referencia: Esquemas de herramientas](/es/reference/tool-schemas/): esquemas legibles por máquina.

## Lecturas adicionales

- `internal/tools/builtin/read.go`: lectura de archivo con truncación.
- `internal/tools/builtin/write.go`: escritura de archivo.
- `internal/tools/builtin/edit.go`: el ejecutor de restricción de cadena única.
- `internal/tools/builtin/grep.go`: búsqueda regex recursiva.
- `internal/tools/builtin/bash.go`: envoltorio de shell `/bin/sh -c`.
