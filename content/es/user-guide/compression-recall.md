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
description: "Session compression triggers and FTS5 cross-session recall in rousseau-agent. How the agent loop keeps long sessions inside the model's context."
keywords: "compression, recall, fts5, session, context window, summarisation, trigger_messages, keep_recent"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/user-guide/compression-recall/"
subtitle: "Session compression and FTS5 cross-session recall."
tags: "compression, recall, session, fts5"
title: "Compresión + recuperación"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "compression, recall, fts5, session, context window, summarisation, trigger_messages, keep_recent"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Compresión + recuperación"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "concepts"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/compression-recall/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/compression-recall/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Compresión + recuperación"
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
twitter_description: "Session compression triggers and FTS5 cross-session recall in rousseau-agent. How the agent loop keeps long sessions inside the model's context."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Compresión + recuperación"
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

## Dos problemas, dos mecanismos

- Una única sesión larga puede desbordar la ventana de contexto del modelo. La **compresión** colapsa mensajes antiguos en un bloque de resumen para que el bucle siga funcionando.
- Una sesión nueva sobre un tema relacionado pierde el valor de conversaciones previas. El **recall** consulta el índice FTS5 en todas las sesiones e inserta extractos en el prompt del sistema.

La compresión edita la sesión actual in situ. El recall nunca edita — anexa contexto al prompt del sistema para el turno actual.

## Compresión

`internal/agent/compressor.go` implementa un summariser respaldado por LLM. El bucle del agente lo consulta al inicio de cada `Turn`:

```go
if changed, err := a.opts.Compressor.Compress(ctx, s); err != nil {
    a.logger.Warn("agent.compress_failed", slog.String("err", err.Error()))
} else if changed {
    a.logger.Info("agent.compressed", slog.Int("messages", len(s.Messages)))
}
```

Si la sesión es corta, no ocurre nada. Cuando el número de mensajes supera `trigger_messages`, el compresor:

1. Aísla la cola de la sesión — los `keep_recent` mensajes más recientes — y los preserva textualmente.
2. Alimenta al proveedor con todo lo más antiguo junto a un prompt de resumen.
3. Reemplaza el bloque más antiguo con un único mensaje sintético `RoleSystem` que contiene el resumen.
4. Marca la sesión para que el bloque de resumen quede en el prefijo elegible para caché de prompt en la siguiente llamada al proveedor.

Después el bucle continúa contra la lista de mensajes más pequeña. El usuario nunca ve la costura.

### Habilitar la compresión

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60      # cero → default 60
    keep_recent: 8            # cero → default 8
    prompt: ""                # cero → default sensato
```

| Campo | Default | Significado |
|---|---|---|
| `enabled` | `false` | Desactivado por defecto. |
| `trigger_messages` | 60 | Número de mensajes por encima del cual se dispara la compresión. |
| `keep_recent` | 8 | Cuántos mensajes recientes preservar textualmente. |
| `prompt` | integrado | Sobrescribe la instrucción de resumen. |

### Cuándo dejarla desactivada

La compresión usa un round-trip al proveedor por cada disparo. En una cuenta `claudecli` con nivel de suscripción, ese trip es gratis — actívala libremente. En una API de pago por token, cada disparo tiene coste, así que ajusta `trigger_messages` al alza o mantenla desactivada para sesiones de corta duración.

### Cuándo dejarla activada

- Demonios de transporte de chat de vida larga donde un hilo de WhatsApp crece durante semanas.
- Prompts programados por cron cuyas respuestas alimentan un prompt de seguimiento.
- Proveedores autoalojados donde el coste por token es cero.

### Semántica preservada durante la compresión

- Los pares tool-use / tool-result nunca se dividen. Si un `tool_use` está en la región comprimida y su `tool_result` en la región preservada, ambos se colapsan en el resumen.
- El compresor nunca reescribe el turno de usuario en curso.
- La caché de prompt (marcadores `cache_control` en `internal/llm/anthropic`) se coloca en el bloque de resumen para que la siguiente llamada lo lea desde la caché.

## Recall

`internal/state/sqlite/` mantiene una tabla virtual FTS5 que indexa cada mensaje. Un `RecallProvider` ejecuta una consulta contra esta tabla y devuelve un apéndice para el prompt del sistema.

### La interfaz

```go
type RecallProvider interface {
    SystemAppendix(ctx context.Context, s *Session) string
}
```

El bucle del agente la invoca una vez por iteración. Cuando devuelve texto no vacío, ese texto se anexa al prompt del sistema base para esa iteración.

### El proveedor por defecto

`internal/agent/recall.go` incluye una heurística que:

1. Extrae tokens relevantes del último mensaje de usuario de la sesión actual.
2. Ejecuta `MATCH` contra el índice FTS5 para esos tokens en otras sesiones.
3. Da formato a los N extractos principales como un bloque `Previously in another session:`.
4. Acota el apéndice para que nunca supere un presupuesto de caracteres configurado.

### Habilitar el recall

El recall se cablea en la construcción del agente. Consulta `internal/cli/chat.go` e `internal/cli/*.go` para ver cómo lo cablea cada transporte. En tu propio embedding:

```go
recall, err := sqlitestore.NewRecall(store)
if err != nil { /* ... */ }

ag := agent.New(provider, registry, logger, agent.Options{
    RecallProvider: recall,
})
```

### Interacción con el approver

El recall lee del store de sesiones; nunca dispara una llamada a herramienta. El approver no se consulta. El propio contenido del store es la frontera de confianza.

### Búsqueda de sesiones desde el CLI

El recall es una funcionalidad orientada a máquina. Para humanos, el mismo índice FTS5 impulsa:

```sh
rousseau session search "kubectl"
rousseau session search "PVC not binding"
```

Mismo motor de consulta, mismos resultados, menos el re-ranking por LLM que un RecallProvider adecuado podría añadir.

## Interacción con las skills

Las skills ([Skills](/es/skills/)) y el recall añaden ambos al prompt del sistema. Se componen en un orden fijo:

1. Prompt del sistema base (desde `agent.system_prompt` o el default).
2. Apéndice de skills (si lo hay).
3. Apéndice de recall (si lo hay).

Todo se separa con dos saltos de línea. Si no hay nada que añadir, el prompt base pasa sin cambios.

## Semántica del bloque de resumen

El mensaje de resumen sintético se emite con `RoleSystem`. No es un mensaje de usuario ni de asistente, así que nunca aparece en `rousseau session show` como un turno conversacional — aparece como metadatos `[compressed summary]`.

Si reanudas una sesión comprimida con `rousseau chat --session <id>`, el resumen se preserva. Eliminar el bloque de resumen mediante una edición hipotética del esquema es inseguro: el modelo puede referenciar hechos que solo se conocen a través de él.

## Verificar que la compresión se está disparando

```
INFO agent.compressed messages=12
```

`messages` es la nueva longitud de la sesión después de que el bloque de resumen reemplazara el prefijo comprimido. Un `WARN agent.compress_failed err=...` indica que el proveedor de resumen dio error; el bucle continuó contra la sesión sin comprimir.

## Advertencias

- La compresión es con pérdida. El resumen es texto generado por el modelo; detalles importantes pueden perderse. Para pistas de auditoría, mantén la sesión completa en el store — la compresión solo afecta a lo que ve el modelo, no a lo que SQLite persiste.
- El recall requiere la extensión SQLite FTS5. `modernc.org/sqlite` la incluye por defecto; si cambias la implementación del store, asegúrate de que FTS5 esté disponible.
- Ambas funcionalidades asumen texto UTF-8. Las transcripciones de notas de voz (véase [modo voz](/es/user-guide/voice-mode/)) cuentan como mensajes de usuario regulares una vez transcritas.

## Siguiente

- [Conceptos](/es/concepts/) — visión general del bucle del agente.
- [Configuración](/es/configuration/) — cada opción `agent.compression.*`.
- [Skills](/es/skills/) — la tercera entrada del prompt del sistema.
