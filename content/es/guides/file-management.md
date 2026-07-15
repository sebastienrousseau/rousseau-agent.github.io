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
description: "How rousseau's write and edit tools interact with the workspace bind mount, SELinux :Z labels, container UID mapping, and safe editing outside /workspace."
keywords: "workspace, bind mount, SELinux, :Z, UserNS, write, edit, permissions"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/guides/file-management/"
subtitle: "Workspace bind mount, SELinux :Z, UID mapping, and safe file edits."
tags: "guides, files, container, selinux, workspace"
title: "Guía: gestión de archivos"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "workspace, bind mount, SELinux, :Z, UserNS, write, edit, permissions"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guía: gestión de archivos"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 37
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/file-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/file-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guía: gestión de archivos"
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
twitter_description: "How rousseau's write and edit tools interact with the workspace bind mount, SELinux :Z labels, container UID mapping, and safe editing outside /workspace."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guía: gestión de archivos"
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

## Las dos herramientas

Dos herramientas mutan el sistema de archivos:

- [`write`](/es/reference/tool-schemas/#write): sobrescritura de archivo completo. `internal/tools/builtin/write.go` escribe con modo `0o644` y `MkdirAll(dir, 0o755)`.
- [`edit`](/es/reference/tool-schemas/#edit): reemplazo único por cadena exacta dentro de un archivo existente. `internal/tools/builtin/edit.go`.

Ambas requieren una **ruta absoluta** (llaman a `filepath.IsAbs`). Ninguna realiza baile de intercambio atómico: usan `os.WriteFile` directamente.

## La vista del contenedor sobre el mundo

La unidad Quadlet de referencia en `docker/rousseau-agent.container` monta tres directorios del host en el contenedor:

```
Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
Volume=%h/.claude:/home/rousseau/.claude:rw,Z
Volume=%h/team-rousseau-workspace:/workspace:rw,Z
```

Nada más del host es visible. Desde dentro del contenedor, una llamada a la herramienta `edit` contra `/workspace/repos/foo/main.go` resuelve a `~/team-rousseau-workspace/repos/foo/main.go` en el host.

### `:Z`: la etiqueta SELinux

El flag `:Z` en cada `Volume=` le dice a Podman que reetiquete el mount con una categoría MCS de SELinux **privada del contenedor**. Sin él, en un sistema con SELinux en modo enforcing:

- Las lecturas aún funcionan la mayor parte del tiempo (`container_file_t` es ampliamente legible).
- Las escrituras fallan con `EACCES` y `avc: denied { write }` en el log de auditoría.

Si cambias el flag por `:z` (minúscula), Podman reetiqueta con una categoría **compartida**, más seguro para hosts que compartes entre múltiples usuarios de contenedor, pero no el default.

En sistemas sin SELinux (Debian, Ubuntu no endurecido), `:Z` es un no-op silencioso.

### `UserNS=keep-id`: mapeo de UID

El contenedor se ejecuta como UID/GID 1000. Sin mapeo de espacio de nombres de usuario, Podman rootless remapearía 1000 en el rango subuid (típicamente `100000+`) y los archivos escritos desde dentro del contenedor serían propiedad de ese UID mapeado en el host: inutilizables para el operador.

`UserNS=keep-id` mapea el UID 1000 del contenedor al UID del usuario del host (también 1000 en la configuración de referencia). Los archivos escritos dentro de `/workspace` terminan siendo propiedad de `seb:seb` en el host: exactamente lo que quieres.

Si el usuario de tu host no es UID 1000, el mapeo aún funciona; `keep-id` usa el UID real del usuario invocador.

## Editar fuera de `/workspace`

Como los bind mounts son la única vista del contenedor sobre el sistema de archivos del host, `write` o `edit` contra `/etc/nginx/nginx.conf` fallará con un error de ruta no encontrada: la ruta simplemente no existe dentro del contenedor. Esto es una **característica**: significa que la política del aprobador del operador puede confiar en la frontera del contenedor.

Si genuinamente necesitas que el daemon toque una ruta diferente del host:

1. **Preferido:** añade una nueva línea `Volume=` a la unidad Quadlet. Toma la elección menos permisiva: `:ro` para solo lectura, `:Z` para etiquetado SELinux privado.
2. **No** ejecutes rousseau fuera del contenedor para saltarte la frontera: pierdes seccomp, drop-caps y el sistema de archivos raíz de solo lectura.

## Editar fuera del contenedor

Si ejecutas rousseau directamente en el host (sin contenedor), las herramientas operan contra la vista del proceso del daemon: todo bajo el HOME del usuario por defecto. El aprobador es la única capa de contención. Consulta [Guías: Auditoría + políticas de aprobación](/es/guides/audit-approval-policies/) para la receta modo pattern + `default: deny`.

## `write` vs `edit`: cuándo usar cuál

| Situación | Usar |
|---|---|
| Crear un archivo nuevo. | `write`. |
| Reescribir un archivo por completo. | `write`. |
| Cambiar una sección de un archivo grande. | `edit`. Falla de forma segura cuando `old_string` no es único. |
| Renombrar un símbolo en todo el archivo. | Múltiples llamadas `edit` con contexto circundante progresivamente mayor, o un único `write` con el contenido reescrito completo. No uses `edit` con semántica tipo `replace_all`: la herramienta lo rechaza. |

La restricción de unicidad exacta en `edit` es deliberada. Se toma directamente de la herramienta Edit de Claude Code. Busca en `internal/tools/builtin/edit.go` el bloque de comentario que explica el porqué.

## Modos de falla comunes

| Síntoma | Causa | Solución |
|---|---|---|
| `edit: path must be absolute, got "…"` | El modelo pasó una ruta relativa. | Rechaza o reescribe en el aprobador; pide al modelo que use rutas absolutas. |
| `edit: old_string not found in …` | El archivo cambió desde la última lectura del modelo, o el modelo alucinó el contexto circundante. | Típicamente el modelo leerá de nuevo y reintentará. |
| `edit: old_string is not unique in … (found 3 occurrences)` | La misma cadena aparece varias veces. | El modelo debe suministrar más líneas circundantes para desambiguar. |
| `write: permission denied` | Desajuste de etiqueta SELinux o mapeo de UID incorrecto. | Verifica `:Z` en el volumen y `UserNS=keep-id` en el contenedor. |
| `read: does not look like UTF-8 text` | El archivo contiene bytes NUL en los primeros 512 bytes (`isLikelyText` en `read.go`). | Rechaza lecturas binarias a nivel del aprobador; usa la herramienta `bash` con `file` si necesitas identificación. |

## Backups antes de reescrituras grandes

Las herramientas no crean copias `.bak`. Para cambios de alto riesgo, enseña al modelo a escribir primero en una ruta hermana, hacer diff con `bash` y luego intercambiar. Alternativamente, ejecuta todo a través de una rama git: rousseau deja `git` completamente fuera de su ruta de ejecución, por lo que cualquier versionado sucede a través de tu flujo de trabajo normal.

## Relacionado

- [Referencia: Esquemas de herramientas](/es/reference/tool-schemas/): esquemas de entrada exactos.
- [Guía de usuario: Herramientas](/es/user-guide/tools/).
- [Despliegue](/es/deployment/): la unidad Quadlet que define los bind mounts.
- [Guías: Auditoría + políticas de aprobación](/es/guides/audit-approval-policies/): fijar escrituras a un árbol de directorios.
