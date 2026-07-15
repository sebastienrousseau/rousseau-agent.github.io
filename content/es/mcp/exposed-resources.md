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
description: "MCP resources exposed by rousseau's stdio server today (none) and the roadmap for sessions-as-resources."
keywords: "mcp, resources, roadmap, sessions, resources/list"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/mcp/exposed-resources/"
subtitle: "What resources rousseau exposes today, and what is planned."
tags: "mcp, resources, roadmap"
title: "MCP: recursos expuestos"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, resources, roadmap, sessions, resources/list"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP: recursos expuestos"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "mcp"
order: 73
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/mcp/exposed-resources/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/exposed-resources/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "MCP: recursos expuestos"
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
twitter_description: "MCP resources exposed by rousseau's stdio server today (none) and the roadmap for sessions-as-resources."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP: recursos expuestos"
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

## Estado actual

El servidor MCP de rousseau (`internal/mcp/server.go`) declara únicamente la capacidad `Tools`. Retorna una lista vacía en `resources/list`:

```
MethodResourcesList → okResponse(env.ID, map[string]any{"resources": []any{}})
```

La intención es deliberada. Cada caso de uso que parecería un recurso MCP (una sesión guardada, una descripción de trabajo cron) se expone hoy a través de una herramienta (`rousseau_read_session`, `rousseau_cron_list`) para que el host pueda pedir exactamente los datos que necesita, cuando los necesita, en lugar de pre-listar cada sesión.

## Por qué no recursos hoy

Los recursos MCP brillan cuando un host quiere enumerar un conjunto modesto y bien definido de URIs (archivos, páginas) y dereferenciarlos de forma perezosa. El almacén de sesiones de rousseau puede crecer a miles de filas; enumerar cada sesión en cada llamada `resources/list` haría explotar el contexto del host. La superficie de herramientas (search / list / read) es una mejor forma para estado de alta cardinalidad.

## Roadmap

Dos candidatos que vale la pena exponer como recursos MCP, una vez que la spec MCP admita enumeración de recursos paginada de forma robusta:

### Candidato: `rousseau://sessions/<id>`

Cada sesión de rousseau como un recurso. Las URIs se verían como:

```
rousseau://sessions/1a2b3c4d-…
```

Dereferenciarlas retornaría la misma transcripción que `rousseau_read_session` retorna hoy. Esto permitiría al host adjuntar una sesión específica a una conversación como ciudadano de primera clase ("adjuntar sesión 1a2b3c…", drag-and-drop), en lugar de requerir que el modelo recuerde llamar a la herramienta.

Restricción: una lista de recursos necesitaría paginación. Versiones recientes de la spec MCP proponen paginación basada en cursor; una vez que aterrice y los hosts la implementen, esto se vuelve viable.

### Candidato: `rousseau://cron/<name>`

Cada trabajo cron como un recurso. Inspección de solo lectura del prompt, cronograma, destino de entrega y timestamp de última ejecución. Lista pequeña: probablemente seguro de enumerar hoy, pero no vale la pena exponerlo separado de `rousseau_cron_list` hasta que la forma sesiones-como-recursos esté probada.

## Capacidad de prompts

Similarmente no expuesta hoy. `MethodPromptsList` retorna `{"prompts": []any{}}` en `internal/mcp/server.go` `dispatch`. Rousseau no tiene una biblioteca de prompts curada para exponer; el mecanismo de skills (`internal/skills/skills.go`) es el concepto interno equivalente, y no está actualmente expuesto por MCP.

Si el roadmap de skills converge en prompts compartibles, exponerlos como prompts MCP es el siguiente paso natural. Consulta [Skills](/es/skills/).

## Cómo sortear la brecha hoy

Si tu host MCP requiere recursos para una affordance de UI específica (p. ej. drag-and-drop de una sesión), la solución alternativa es:

1. Pídele al host que invoque `rousseau_list_sessions` al inicio del chat.
2. Copia el id de sesión al que quieres referirte.
3. Invoca `rousseau_read_session` con ese id.

No tan ergonómico como la dereferenciación nativa de recursos, pero funcionalmente equivalente.

## Solicitar una superficie de recursos

No todo operador necesita recursos por MCP. Si tu equipo lo necesita, la ruta constructiva es abrir un issue con:

- El host MCP específico con el que estás integrando.
- La acción de cara al usuario que sería más agradable con recursos.
- Expectativas aproximadas de tráfico (cuántas sesiones, con qué frecuencia).

## Relacionado

- [MCP](/es/mcp/): la referencia paraguas.
- [MCP: Herramientas expuestas](/es/mcp/exposed-tools/): qué se expone hoy.
- [MCP: Compatibilidad](/es/mcp/compatibility/): clientes probados.
- [Skills](/es/skills/): el concepto interno que puede convertirse en prompts MCP.
