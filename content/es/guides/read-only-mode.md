---

# Front Matter (YAML)

author: "sebastian.rousseau@gmail.com (Sebastien Rousseau) "
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
description: "Configure rousseau-agent as a read-only inspection agent: deny_all approver with a read/grep exception, plan-mode claudecli, read-only bind mounts."
keywords: "read-only, inspection, deny_all, plan mode, bind mount, ro mount, audit"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/guides/read-only-mode/"
subtitle: "An inspection posture that cannot mutate the workspace."
tags: "guides, read-only, deny_all, plan-mode"
title: "Guía: modo de solo lectura"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "read-only, inspection, deny_all, plan mode, bind mount, ro mount, audit"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guía: modo de solo lectura"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 36
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/read-only-mode/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/read-only-mode/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guía: modo de solo lectura"
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
twitter_description: "Configure rousseau-agent as a read-only inspection agent: deny_all approver with a read/grep exception, plan-mode claudecli, read-only bind mounts."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guía: modo de solo lectura"
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

## Escenario

Quieres que rousseau inspeccione un repositorio, responda preguntas sobre él y produzca informes — pero no debe poder escribir, editar ni ejecutar comandos de shell destructivos. Esta es la postura que desplegarías para una primera pasada de auditoría, una inspección de respuesta a incidentes o un walk-through de cumplimiento.

Tres capas se apilan para reforzar esto:

1. **Política de aprobación** — denegar toda herramienta mutante.
2. **Modo de permiso de `claudecli`** — poner Claude Code en modo `plan` para que su propio approver nunca edite archivos.
3. **Sistema de archivos** — bind-mount del workspace en solo lectura.

Doble cinturón y tirantes. Cualquiera de las tres capas falla de forma segura.

## Capa 1 — Approver

La postura read-only más simple usa el approver `pattern` con una lista blanca:

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "read-only inspection posture — this deployment cannot mutate files"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|find|wc|stat|file|which|pwd|env|git status|git diff|git log|git show|git branch)\\b"}
    # No hacen falta reglas deny — default: deny cubre todo lo demás.
    # Sin edit, write ni bash sin restricción — el modelo no puede alcanzarlos.
```

Una variante aún más estricta usa `deny_all`, que bloquea toda herramienta incluidas `read` y `grep`:

```yaml
agent:
  approver:
    mode: deny_all
    reason: "smoke test — no tool calls allowed"
```

`deny_all` solo es útil como smoke test; el modelo no podrá realizar trabajo significativo.

## Capa 2 — Modo de permiso de `claudecli`

Cuando el proveedor es `claudecli`, es Claude Code el que ejecuta las llamadas a herramientas. Establecer `permission_mode: plan` hace que Claude Code rechace toda llamada de escritura o edición en su propia capa, incluso si el approver de rousseau la hubiera permitido:

```yaml
provider: claudecli

claudecli:
  binary: claude
  permission_mode: plan
```

Valores válidos (véase `internal/config/config.go` y la documentación de Claude Code): `acceptEdits`, `auto`, `bypassPermissions`, `default`, `dontAsk`, `plan`. `plan` es el único valor que mantiene consistentemente a Claude Code en postura de solo lectura.

## Capa 3 — Sistema de archivos

Monta el workspace en solo lectura. Bajo la Quadlet de Podman de referencia:

```
Volume=%h/team-rousseau-workspace:/workspace:ro,Z
```

`ro` hace que el mount sea solo lectura desde la perspectiva del contenedor; incluso si un binario comprometido intentara `open(2)` con `O_WRONLY`, el kernel devolvería `EROFS`.

En Kubernetes:

```yaml
volumeMounts:
  - name: workspace
    mountPath: /workspace
    readOnly: true
```

El store de sesiones (`~/.local/share/rousseau/`) sí debe ser escribible — el demonio le añade en cada turno. Deja ese mount como `rw` y deja solo el workspace en solo lectura.

## Postura de dry-run

No existe un flag `--dry-run` en el demonio. Si quieres que el modelo *planifique* cambios sin ejecutarlos, la combinación anterior consigue el equivalente:

- El approver bloquea toda herramienta mutante → el modelo recibe un error `tool_result` explicando el bloqueo.
- El modo `plan` en `claudecli` evita que Claude Code ejecute sus propias herramientas destructivas.
- Los mounts solo lectura detienen cualquier fuga.

El modelo normalmente responderá con un documento de plan en lugar de un diff. Ese es el entregable de la inspección solo lectura.

## Qué sigue funcionando

- Cada llamada `read` y `grep`.
- `bash` para las utilidades de lado de lectura seguras que hayas enumerado.
- Persistencia de sesión — el store SQLite sigue registrando la conversación.
- Recall entre sesiones vía FTS5, exportación MCP, skills — todo es solo lectura de todos modos.

## Qué se rompe (intencionalmente)

- `write` y `edit` — deny.
- Comandos shell de mutación — deny.
- Trabajos de cron cuyo prompt implique escrituras de archivos — el modelo intenta, es denegado, responde con un plan.
- `rousseau init` — el CLI no se ve afectado por el approver, pero escribe en `~/.config/rousseau/` fuera del workspace. Ejecútalo antes de desplegar el modo solo lectura.

## Prueba de la postura

```sh
rousseau chat
> Edita /workspace/README.md para añadir un pie de página.
```

Línea de log esperada:

```
WARN tool.denied name=edit reason="read-only inspection posture — this deployment cannot mutate files"
```

Respuesta esperada en el chat: el modelo se disculpa, produce un plan o un parche diff como texto y pide al operador que lo aplique.

Para la variante `deny_all`, cada llamada a herramienta se bloquea — el modelo no tiene forma de inspeccionar nada, así que esta postura solo es útil como smoke test.

## Combinación con otros transportes

Las mismas tres capas aplican a WhatsApp, Slack, Discord y cada uno de los demás transportes. Como el approver corre dentro del bucle del agente, no le importa qué transporte entregó el turno del usuario. Un agente de Slack solo lectura queda a un bloque `mode: pattern` de distancia.

## Advertencias

- La postura de solo lectura la aplica el approver de rousseau y el sistema de archivos — **no** el LLM. Un modelo aún puede emitir una llamada a la herramienta `edit`; el approver la bloquea silenciosamente, pero el intento se registra como `tool.denied`. Esto es intencional para que los registros de auditoría registren lo que el modelo intentó, no solo lo que tuvo éxito.
- Los bind mounts en solo lectura no protegen contra symlinks que apuntan fuera del mount. La postura de referencia de Podman elimina todas las capabilities, lo que previene la mayoría de rutas de escape, pero no te apoyes solo en el mount.
- El modo `plan` del proveedor `claudecli` es el contrato de Claude Code, no de rousseau. Si Claude Code cambia su semántica de permission-mode, la postura de solo lectura de rousseau hereda ese cambio.

## Siguiente

- [Guía de usuario: políticas de aprobación](/es/user-guide/approval-policies/) — referencia más profunda.
- [Auditoría y políticas de aprobación](/es/guides/audit-approval-policies/) — la contraparte mutante.
- [Despliegue](/es/deployment/) — flags de mount y contenedor.
