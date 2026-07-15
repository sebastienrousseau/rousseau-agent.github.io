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
description: "How rousseau's session store partitions by workspace, how to switch workspaces, share sessions across machines, and drop a workspace's history."
keywords: "workspace, session store, state path, sync, rsync, XDG_DATA_HOME"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/guides/managing-workspaces/"
subtitle: "Partition state per project, share history across machines, drop history cleanly."
tags: "guides, workspace, session store, sqlite"
title: "Guía: gestión de espacios de trabajo"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "workspace, session store, state path, sync, rsync, XDG_DATA_HOME"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guía: gestión de espacios de trabajo"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 38
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/managing-workspaces/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/managing-workspaces/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guía: gestión de espacios de trabajo"
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
twitter_description: "How rousseau's session store partitions by workspace, how to switch workspaces, share sessions across machines, and drop a workspace's history."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guía: gestión de espacios de trabajo"
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

## La convención

Rousseau no tiene un concepto de "workspace" de primera clase. Tiene un `state.path` en `internal/config/config.go` (`StateConfig`) y por defecto apunta cada proceso a `~/.local/share/rousseau/sessions.db`. Todas las sesiones, trabajos cron, mapeos JID y el índice de recall FTS5 viven en ese único archivo.

Para la mayoría de operadores eso es exactamente lo correcto. Cuando quieres aislamiento (por proyecto, por máquina, por cliente), apuntas rousseau a un archivo SQLite diferente. Ese archivo **es** el workspace.

## Cambiar workspace por invocación

Dos perillas, cualquiera funciona:

```sh
# 1. flag en cualquier comando rousseau
rousseau --config ~/.config/rousseau/acme.yaml chat

# 2. variable de entorno (Viper la recoge vía ROUSSEAU_STATE_PATH)
ROUSSEAU_STATE_PATH=~/.local/share/rousseau/acme.db rousseau chat
```

Ninguno de los dos enfoques requiere reiniciar rousseau al saltar entre workspaces: cada proceso abre su propio archivo.

## Disposición de workspace por proyecto

```
~/.config/rousseau/
├── acme.yaml         # provider = anthropic, state.path = …/acme.db
├── personal.yaml     # provider = claudecli, state.path = …/personal.db
└── work.yaml         # provider = bedrock,    state.path = …/work.db
```

Cada archivo de configuración sobrescribe `state.path`:

```yaml
state:
  path: /home/seb/.local/share/rousseau/acme.db
```

Luego lanza cada sesión con la configuración correcta. La TUI (`internal/tui/model.go`) muestra el id de sesión + proveedor en su barra de estado: confirmación visual de que estás en el workspace correcto.

## Compartir historial entre máquinas

El almacén de sesiones es un único archivo SQLite. El journaling WAL está habilitado por `Open()` en `internal/state/sqlite/store.go`, por lo que las snapshots en vivo son seguras:

```sh
# Snapshot laptop-a-desktop (ambos inactivos)
rsync -avz --partial \
  ~/.local/share/rousseau/sessions.db \
  desktop:~/.local/share/rousseau/sessions.db
```

**Solo un escritor a la vez.** No ejecutes `rousseau whatsapp` en dos máquinas contra el mismo archivo SQLite sobre NFS: eso es indefinido. Sincroniza cuando nada esté escribiendo, o ejecuta un único escritor con réplicas de lectura.

Una alternativa más segura es el snapshot `.backup`:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db ".backup '/tmp/sessions.snap.db'"
scp /tmp/sessions.snap.db desktop:~/.local/share/rousseau/sessions.db
```

`.backup` usa la API de backup en línea de SQLite y produce un archivo consistente en un punto en el tiempo.

## Migrar un workspace

Mueve el directorio entero; ese es el workspace:

```sh
rsync -avz ~/.local/share/rousseau/ new-host:~/.local/share/rousseau/
```

`whatsapp.db` (credenciales del dispositivo) es separado: o lo traes también (el dispositivo sigue emparejado) o lo dejas atrás y vuelves a escanear el QR en el nuevo host.

## Descartar el historial de un workspace

```sh
rousseau session list                 # confirma qué estás por perder
rm ~/.local/share/rousseau/acme.db*   # incluye los sidecars -wal y -shm
```

El siguiente proceso que abra la ruta la recreará con el esquema en `internal/state/sqlite/schema.sql`.

Si solo quieres descartar un subconjunto de sesiones, usa el CLI:

```sh
rousseau session delete <id> --yes
```

`rousseau session delete` (`internal/cli/session.go`) llama a `Store.Delete`, que cascadea a través de los triggers de FTS5 para mantener el índice de recall consistente. El flag `--yes` es obligatorio: el comando se rehúsa a ejecutarse sin él.

## Eliminación parcial vía SQL

Para limpieza masiva (cada sesión más antigua que 90 días):

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions WHERE updated_at < datetime('now', '-90 days');
SQL
```

Los triggers de FTS5 (`sessions_fts_ad` en `internal/state/sqlite/search.go`) se disparan en el DELETE y mantienen el índice en sincronía automáticamente.

## Aprobadores por workspace

Como el archivo de configuración y el archivo de estado son por workspace, también lo es el aprobador:

```yaml
# work.yaml — aprobador pattern estricto
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

state:
  path: /home/seb/.local/share/rousseau/work.db
```

Un `personal.yaml` separado podría mantener `mode: allow_all` para trabajo interactivo. Consulta [Tutorial: Endurecer el aprobador](/es/tutorials/harden-approver-policy/).

## Relacionado

- [Referencia: Almacén de sesiones](/es/reference/session-store/): esquema.
- [Guías: Multi-proveedor](/es/guides/multi-provider/): el patrón dos configuraciones, dos proveedores.
- [Referencia: Variables de entorno](/es/reference/environment-variables/): cada variable de entorno de ruta.
- [Guía de usuario: CLI](/es/user-guide/cli/): comandos `rousseau session`.
