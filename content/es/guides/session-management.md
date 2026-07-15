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
description: "Full session lifecycle: list, search, show, delete, compression triggers, and restoration from the SQLite session store."
keywords: "session, lifecycle, list, search, delete, compression, sqlite"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/guides/session-management/"
subtitle: "List, search, delete, compress, restore."
tags: "guides, session, sqlite, compression"
title: "Guía: gestión de sesiones"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "session, lifecycle, list, search, delete, compression, sqlite"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guía: gestión de sesiones"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 42
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/session-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/session-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guía: gestión de sesiones"
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
twitter_description: "Full session lifecycle: list, search, show, delete, compression triggers, and restoration from the SQLite session store."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guía: gestión de sesiones"
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

## Ciclo de vida de una sesión

Una sesión es un valor `agent.Session` persistido como una fila en la tabla `sessions` (`internal/state/sqlite/schema.sql`). Tiene un `id`, un `title`, un slice de valores `Message` ordenados cronológicamente y timestamps. Una vez creada, existe hasta que la elimines.

Las sesiones se crean bajo demanda por cada punto de entrada:

- `rousseau chat` — una sesión por sesión de TUI (una nueva en cada invocación de `chat`; tendrías que construir un selector de sesiones para reutilizar una existente).
- Cada transporte (`whatsapp`, `slack`, …) — una sesión por JID, vía el JID map (`internal/state/sqlite/jidmap.go`).
- `rousseau cron` — cada disparo es una sesión one-shot acotada a esa ejecución.

## Enumerar

```sh
rousseau session list --limit 10
```

Salida (desde `newSessionListCmd` en `internal/cli/session.go`):

```
<short-id>  <messages>  <updated_at>  <title>
```

`--limit 0` devuelve filas sin límite.

## Buscar

FTS5 a través de cada mensaje registrado:

```sh
rousseau session search 'retry logic'
rousseau session search '"exponential backoff" AND anthropic'
rousseau session search 'retr*'                # prefijo
```

El comando envuelve `Store.Search` (`internal/state/sqlite/search.go`) con `SearchOptions{Limit: N}`. El ranking es BM25; los snippets se recortan a ~200 caracteres.

## Mostrar

```sh
rousseau session show <session-id>
```

Imprime la transcripción completa con marcadores `→ tool_use(name, input)` y `← tool_result` entre mensajes del asistente. Útil para auditar la sesión de un demonio desatendido.

## Eliminar

```sh
rousseau session delete <session-id> --yes
```

El flag `--yes` es obligatorio (`newSessionDeleteCmd`). La eliminación cascada a través de los triggers de FTS5 mantiene el índice de recall consistente.

## Disparadores de compresión

Cuando `agent.compression.enabled: true` en `config.yaml`, `LLMCompressor` (`internal/agent/compressor.go`) comprueba dos condiciones antes de cada turno:

- `len(s.Messages) >= trigger_messages` (default 60).
- `len(s.Messages) > keep_recent` (default 8).

Si ambas se cumplen, el compresor resume el slice más antiguo en un único mensaje de usuario sintético con el prefijo `[rousseau-compressed]`, y luego conserva los últimos `keep_recent` mensajes textualmente. La sesión reescrita reemplaza a la original en memoria y se persiste en la siguiente `Store.Save`.

Una segunda compresión sobre una sesión ya comprimida se salta salvo que la sesión haya crecido a más de `2 * trigger_messages` — esto acota el crecimiento descontrolado sin pagar por re-resumir cada turno.

Línea de log:

```
INFO agent.compressed messages=68
```

## Restauración

Las sesiones se restauran automáticamente. El router de transporte (`internal/transport/router.go`) busca el mapeo JID → session id al recibir un mensaje, luego `Store.Load` deserializa el payload JSON de vuelta a un `agent.Session`. Sin paso manual.

Si un mapeo está obsoleto — el session id existe en `jid_sessions` pero no en `sessions` — verás `router.stale_mapping` (WARN), y el router crea una sesión nueva. Artefacto residual de una eliminación parcial; se puede ignorar sin problema.

## Restauración manual desde un backup

Para revertir el store de sesiones completo desde un snapshot `.backup`:

```sh
systemctl --user stop rousseau-agent
cp /backup/sessions.db.2026-07-12.bak ~/.local/share/rousseau/sessions.db
rm -f ~/.local/share/rousseau/sessions.db-wal ~/.local/share/rousseau/sessions.db-shm
systemctl --user start rousseau-agent
```

Los archivos `-wal` y `-shm` deben eliminarse junto al primario; SQLite los reconstruye al siguiente open.

## Borrado masivo por antigüedad

No hay un CLI integrado del tipo "eliminar sesiones con más de X". Baja a SQLite:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions WHERE updated_at < datetime('now', '-90 days');
SQL
```

Los triggers de FTS5 mantienen el índice de recall consistente.

## Preservar la privacidad

Dado que el contenido de la sesión se almacena en texto plano en un blob JSON, trata `sessions.db` como sensible. Opciones:

- **Cifrado a nivel de sistema de archivos.** LUKS en Linux, FileVault en macOS.
- **Backups cifrados.** `restic` y `borg` cifran ambos en reposo.
- **Delete-on-completion para sesiones one-shot.** Para demonios dirigidos por cron, un hook post-run podría hacer `rousseau session delete` sobre el id de sesión recién completada. No está integrado hoy; consulta [Guías: onboarding empresarial](/es/guides/enterprise-onboarding/) para la revisión.

## Referencia completa del comando `rousseau session`

<div class="tabs" data-tabs="session-commands">
  <div class="tab-list" role="tablist" aria-label="Session subcommand">
    <button role="tab" aria-selected="true">list</button>
    <button role="tab" aria-selected="false">show</button>
    <button role="tab" aria-selected="false">search</button>
    <button role="tab" aria-selected="false">delete</button>
    <button role="tab" aria-selected="false">export</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Lista sesiones, las más recientes primero:

```sh
rousseau session list
rousseau session list --limit 100
rousseau session list --json
```

Columnas: `ID`, `Title`, `Messages`, `UpdatedAt`. El flag `--json` emite un objeto por línea para consumidores automatizados.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Imprime la transcripción completa de una sesión:

```sh
rousseau session show <session-id>
rousseau session show <session-id> --raw
```

`--raw` imprime el JSON tal y como se almacena (útil para depuración). Sin `--raw`, las llamadas a herramientas se muestran como `→ tool_use(name, input)` y los resultados como `← tool_result`.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Búsqueda full-text a través de cada sesión:

```sh
rousseau session search "refactor login"
rousseau session search "TODO" --limit 10
```

Usa el índice FTS5 (véase `internal/state/sqlite/`). Los resultados se ordenan por relevancia e incluyen un snippet con los términos coincidentes resaltados.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Elimina una sesión y sus entradas FTS5:

```sh
rousseau session delete <session-id> --yes
```

El flag `--yes` es obligatorio — sin confirmación interactiva. La eliminación se propaga en cascada vía triggers SQL para mantener el índice de recall consistente.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Exporta una sesión como JSON:

```sh
rousseau session export <session-id> > session.json
```

El formato exportado coincide con el blob JSON en disco; la reimportación aún no está soportada (en la hoja de ruta).

  </div>
</div>

## Solución de problemas

### `session not found`

El ID que pasaste no existe. Distingue entre mayúsculas y minúsculas. Usa `rousseau session list` para ver los IDs válidos.

### La búsqueda FTS5 no devuelve nada

El índice puede estar desactualizado en sesiones antiguas importadas antes de que se cableara FTS5. Reconstrúyelo ejecutando cualquier operación que mute contenido (un delete dispara la reindexación), o reindexa manualmente vía SQLite.

### `database is locked` en lectura

Otro demonio mantiene un lock de escritura WAL. Usa un DSN de solo lectura (`?mode=ro`) si solo necesitas leer.

### El store de sesiones crece demasiado rápido

Habilita la compresión (`agent.compression.enabled: true`) y ejecuta `VACUUM` periódicamente sobre el archivo SQLite para recuperar espacio.

### La restauración desde backup produce estado obsoleto

Asegúrate de haber eliminado `-wal` y `-shm` antes de iniciar el demonio. SQLite replayará el WAL si `-wal` está presente, potencialmente deshaciendo tu restauración.

## Páginas relacionadas

- [Referencia: session store](/es/reference/session-store/) — esquema y DDL.
- [Guías: gestión de workspaces](/es/guides/managing-workspaces/) — stores por workspace.
- [Guías: gestión de contexto](/es/guides/context-management/) — cómo la compresión decide qué mantener.
- [Guía de usuario: CLI](/es/user-guide/cli/) — firmas de comando.
- [Guía de usuario: compresión y recall](/es/user-guide/compression-recall/) — internos del compresor y del recall FTS5.

## Lecturas adicionales

- `internal/cli/session.go` — cableado del CLI.
- `internal/state/sqlite/store.go` — DSN, WAL, índices.
- `internal/agent/session.go` — la estructura `Session`.
- `internal/agent/compressor.go` — `LLMCompressor`.
- `internal/agent/recall.go` — `SQLiteRecall`.
