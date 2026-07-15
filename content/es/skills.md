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
description: "rousseau-agent's skills loader: Markdown + YAML frontmatter, discovery from skills_dir, trigger-based activation, composition into the system prompt."
keywords: "skills, agentskills.io, markdown, YAML frontmatter, triggers, system prompt, activation"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/skills/"
subtitle: "Archivos de habilidades Markdown compatibles con agentskills.io."
tags: "skills, reference"
title: "Habilidades"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "skills, agentskills.io, markdown, YAML frontmatter, triggers, system prompt, activation"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Habilidades"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 23
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/skills/index.html"
item_link: "https://docs.rousseau-agent.dev/skills/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Habilidades"
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
twitter_description: "rousseau-agent's skills loader: Markdown + YAML frontmatter, discovery from skills_dir, trigger-based activation, composition into the system prompt."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Habilidades"
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

## Formato de skill

Un skill es un archivo Markdown con una cabecera opcional YAML front-matter. El formato se aproxima deliberadamente a la convención de [agentskills.io](https://agentskills.io) para que los archivos sean portables a otras herramientas.

Ejemplo — `~/.local/share/rousseau/skills/git-rebase.md`:

```markdown
---
name: git-rebase
description: Guide the user through an interactive rebase safely.
triggers:
  - rebase
  - git rebase
  - squash
  - autosquash
---
When helping with a git rebase, first verify the current HEAD is
pushed to a remote branch. Prefer `git rebase -i --autosquash`
when the user has fixup commits. Never force-push to `main`.
```

## Campos del frontmatter

| Campo | Tipo | Efecto |
|---|---|---|
| `name` | string | Debe cumplir `^[a-z][a-z0-9-]*$`. Mostrado por `rousseau skills list`. |
| `description` | string | Resumen de una línea. |
| `triggers` | `[]string` | Subcadenas insensibles a mayúsculas. Si alguna aparece en el mensaje del usuario, el skill se activa. Vacío significa que el skill nunca se autoactiva. |

Todo lo que sigue al `---` de cierre es el cuerpo del skill, tal cual.

## Descubrimiento

El cargador escanea `agent.skills_dir` buscando archivos `*.md` (no recursivo). Un directorio inexistente no es un error; Load devuelve `nil`. Los subdirectorios se ignoran.

```yaml
agent:
  skills_dir: ~/.local/share/rousseau/skills
```

## Activación

En cada turno del usuario, `SkillsProvider.SystemAppendix(session)` inspecciona el mensaje de usuario más reciente y compara los `triggers` de cada skill (sin distinción de mayúsculas). Cada coincidencia se concatena (en orden de carga) y se inserta en el system prompt de ese turno.

Los skills con `triggers` vacíos nunca se autoactivan, pero pueden incluirse programáticamente por quienes integren la biblioteca.

## CLI

```sh
# Listar los skills descubiertos.
rousseau skills list

# Mostrar el contenido de un skill.
rousseau skills show git-rebase
```

## Restricciones de diseño

- **Sin ejecución de código.** Los skills son cadenas. No pueden ejecutar scripts ni comandos de shell. Si buscas automatización, conecta una nueva herramienta vía `Registry.Register`.
- **Sin versionado.** rousseau no rastrea versiones de skills. Gestiónalo en git; se espera que `skills_dir` sea una copia de trabajo de un repositorio.
- **Determinista.** La misma sesión + mensaje de usuario produce el mismo apéndice. No hay LLM en el bucle.

## Cómo escribir skills efectivos

- Mantén el cuerpo corto (100–500 palabras). Cada activación se antepone al system prompt de ese turno.
- Prefiere oraciones imperativas ("Cuando el usuario pregunte por X, haz Y") por sobre exposición.
- Usa `triggers` para frases de alta precisión; los triggers amplios ("code", "help") se activan en casi todos los turnos y ahogan a otros skills.
- Prueba en la TUI (`rousseau chat`) antes de desplegarlo en un servicio de transporte de chat; la línea de log `agent.skills_activated` lista qué skills se activaron.
