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
description: "Rousseau's SQLite session store: sessions table, FTS5 recall index, JID mapping table, cron jobs, and WAL journaling."
keywords: "sqlite, fts5, session store, sessions, jid, cron, WAL, schema"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/reference/session-store/"
subtitle: "The SQLite schema at the heart of rousseau's state."
tags: "reference, sqlite, fts5, session, wal"
title: "Referencia: almacén de sesiones"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "sqlite, fts5, session store, sessions, jid, cron, WAL, schema"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Referencia: almacén de sesiones"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 53
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/session-store/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/session-store/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Referencia: almacén de sesiones"
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
twitter_description: "Rousseau's SQLite session store: sessions table, FTS5 recall index, JID mapping table, cron jobs, and WAL journaling."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Referencia: almacén de sesiones"
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

## Ubicación y driver

El almacén de sesiones es una única base de datos SQLite en `state.path` (por defecto `~/.local/share/rousseau/sessions.db`, consulta `internal/config/config.go` `setDefaults`).

Rousseau usa `modernc.org/sqlite`: un driver SQLite en Go puro. **No hay dependencia de CGO ni libsqlite3**. El binario Go en `bin/rousseau` es totalmente estático.

`internal/state/sqlite/store.go` `Open()` aplica cuatro pragmas en cada apertura:

| PRAGMA | Propósito |
|---|---|
| `journal_mode=WAL` | Write-ahead logging. Habilita lectores concurrentes, backups en vivo seguros. |
| `foreign_keys=ON` | Garantía estándar de integridad. |
| `busy_timeout=15000` | Espera de 15 segundos ante contención de lock: crítico una vez que múltiples transportes escriben concurrentemente. |
| — | `EnsureSearch` se ejecuta después para instalar el esquema FTS5. |

El almacén se abre una vez por proceso. Múltiples daemons apuntando al mismo archivo de DB están soportados gracias a la combinación busy-timeout + WAL: el puente de WhatsApp, `rousseau mcp` y `rousseau session list` pueden compartir el archivo con seguridad.

## Recorrido del esquema

### Tabla: `sessions`

Definida en `internal/state/sqlite/schema.sql`:

```sql
CREATE TABLE IF NOT EXISTS sessions (
    id             TEXT PRIMARY KEY,
    title          TEXT NOT NULL,
    payload        TEXT NOT NULL,        -- blob JSON del agent.Session completo
    message_count  INTEGER NOT NULL DEFAULT 0,
    created_at     TEXT NOT NULL,
    updated_at     TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sessions_updated_at
    ON sessions(updated_at DESC);
```

**Forma del payload.** La columna `payload` almacena el JSON completo de `agent.Session`: roles, bloques de contenido, bloques tool-use y tool-result, timestamps. Consulta `Save`/`Load` en `internal/state/sqlite/store.go`. Mantener la sesión entera como un blob JSON hace raras las migraciones de esquema; las consultas contra los internos pasan por el índice FTS5 abajo.

**Los timestamps** son ISO-8601 con precisión de milisegundos (`2006-01-02T15:04:05.000Z` en sintaxis de tiempo Go), UTC.

**Ordenamiento.** `idx_sessions_updated_at` alimenta `List` y `RecentSessions` (ambos en `store.go` / `search.go`).

### Tabla virtual: `sessions_fts` (FTS5)

Instalada por `searchSchema` en `internal/state/sqlite/search.go`:

```sql
CREATE VIRTUAL TABLE IF NOT EXISTS sessions_fts USING fts5(
    session_id UNINDEXED,
    title,
    body,
    tokenize = 'porter unicode61'
);
```

Tres escrituras dirigidas por triggers la mantienen consistente con `sessions`:

- `sessions_fts_ai`: tras INSERT en `sessions`, replica la fila.
- `sessions_fts_au`: tras UPDATE, elimina + reinserta.
- `sessions_fts_ad`: tras DELETE, elimina la fila FTS.

**Backfill.** `EnsureSearch` ejecuta un `LEFT JOIN` en cada `Open()` para insertar cualquier fila de `sessions` que el índice FTS no tenga ya. Esto hace que el índice sea seguro para añadir a una base de datos existente: sin migración manual.

**Tokenización.** `porter unicode61`: stemmer Porter + casefolding con conciencia Unicode. Insensible a mayúsculas, maneja la morfología del inglés (`retry`/`retries`/`retried`).

**Ranking.** `Search()` ordena por `bm25(sessions_fts)` (menor es más relevante). `SearchHit.Rank` lo expone.

**Sintaxis de consulta.** Pasada a FTS5 textualmente. Consulta [Tutorial: Exponer herramientas vía MCP](/es/tutorials/expose-tools-via-mcp/) para la chuleta del operador.

### Tabla: `jid_sessions`

Persiste los mapeos plataforma-remitente a session-id; instalada por `NewJIDMap` en `internal/state/sqlite/jidmap.go`:

```sql
CREATE TABLE IF NOT EXISTS jid_sessions (
    jid         TEXT PRIMARY KEY,
    session_id  TEXT NOT NULL,
    created_at  TEXT NOT NULL
);
```

Cada transporte de larga duración usa el mapa JID para que el mismo número de teléfono, usuario de Matrix o usuario de Slack retome la misma conversación entre reinicios. `Router.Handle` (`internal/transport/router.go`) lo consulta en la entrada; `Put` lo escribe tras `Save`.

El espacio JID es específico del transporte: `447900123456@s.whatsapp.net` para WhatsApp, `@user:matrix.org` para Matrix, `U01ABC…` para Slack. El transporte es responsable de canonicalizar.

### Tabla: `cron_jobs`

Instalada por `NewCronStore` en `internal/state/sqlite/cron.go`:

```sql
CREATE TABLE IF NOT EXISTS cron_jobs (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    cron_expr   TEXT NOT NULL,
    prompt      TEXT NOT NULL,
    deliver_to  TEXT NOT NULL,
    enabled     INTEGER NOT NULL DEFAULT 1,
    created_at  TEXT NOT NULL,
    last_run_at TEXT
);
```

`UNIQUE(name)` previene duplicados. `rousseau cron add/list/remove/enable/disable` (de `internal/cli/cron.go`) hacen round-trip a través de esta tabla. El planificador en `internal/cron/scheduler.go` reconcilia desde ella cada `poll_interval`. MCP la expone en solo lectura vía `rousseau_cron_list`.

## Postura de concurrencia

- **WAL** permite lectores concurrentes ilimitados junto a un único escritor.
- **`busy_timeout=15000`** significa que un escritor que golpea contención espera hasta 15 s en lugar de fallar rápido. En la práctica el puente de WhatsApp mantiene el rol de escritor mientras `rousseau mcp` y `rousseau session list` son visitantes de solo lectura.
- El almacén no está diseñado para concurrencia cross-máquina. Dos hosts escribiendo al mismo archivo sobre NFS es comportamiento indefinido: usa un único escritor y rsync la DB a otro lado para réplicas de lectura.

## Hacer backup

El enfoque más seguro es un `sqlite3 .backup` en vivo:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db ".backup '/backup/sessions.db.$(date -I).bak'"
```

`.backup` usa la API online de backup de SQLite y funciona mientras el primario está siendo escrito. Los snapshots de `restic` / `borg` sobre el archivo crudo también son seguros gracias a WAL: el backup obtiene un snapshot consistente al momento de leer el archivo.

El archivo `whatsapp.db` (credenciales del dispositivo whatsmeow) es una base de datos separada; hazle backup de la misma forma si quieres evitar el re-emparejamiento tras una restauración.

## Reconstruir el índice FTS

Si el índice FTS5 se desincroniza (extremadamente raro: los triggers lo mantienen consistente), reconstrúyelo:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions_fts;
INSERT INTO sessions_fts (session_id, title, body)
SELECT id, title, payload FROM sessions;
SQL
```

`EnsureSearch` de rousseau no deshará esto; los triggers simplemente retoman desde un estado limpio.

## Relacionado

- [Conceptos](/es/concepts/): dónde se sitúa el almacén en la arquitectura global.
- [Guía de usuario: Compresión + Recall](/es/user-guide/compression-recall/): cómo se expone el índice FTS al modelo.
- [MCP: Herramientas expuestas](/es/mcp/exposed-tools/): la superficie de solo lectura sobre este esquema.
- [Guías: Gestión de workspaces](/es/guides/managing-workspaces/): compartir / particionar el almacén entre máquinas.
