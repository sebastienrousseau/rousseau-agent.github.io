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
description: "Configure the claudecli provider: PermissionMode values, model aliases, auth inheritance, and when to prefer this over the direct API."
keywords: "claudecli, claude CLI, subprocess, PermissionMode, bypassPermissions, acceptEdits, Claude Code"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/providers/claudecli/"
subtitle: "Subprocess against the local Claude Code CLI."
tags: "providers, claudecli"
title: "Proveedor claudecli"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "claudecli, claude CLI, subprocess, PermissionMode, bypassPermissions, acceptEdits, Claude Code"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Proveedor claudecli"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 6
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/claudecli/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/claudecli/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Proveedor claudecli"
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
twitter_description: "Configure the claudecli provider: PermissionMode values, model aliases, auth inheritance, and when to prefer this over the direct API."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Proveedor claudecli"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Qué aprenderás</span><p>Cómo el proveedor <code>claudecli</code> hereda la autenticación de tu instalación local de Claude Code, la matriz completa de <code>PermissionMode</code>, la semántica de correlación de sesión, los alias de modelo y cuándo preferir esto sobre la API directa de Anthropic. Lee <code>internal/llm/claudecli/client.go</code> junto a esta página para la verdad de base.</p></aside>

## Cuándo usar claudecli

`claudecli` ejecuta el CLI `claude` (Claude Code) como subproceso. Es el **proveedor por defecto** y la elección correcta cuando:

- Ya tienes Claude Code instalado y autenticado localmente.
- Quieres reutilizar una cuenta de nivel de suscripción de Claude Code en lugar de canalizar claves de API.
- Quieres que el modelo se ejecute dentro del propio bucle de uso de herramientas de `claude` (sus funciones de edición de archivos, pensamiento y modo plan quedan intactas).
- Quieres cero material secreto en el archivo de configuración de rousseau.

La contrapartida: el `Registry` de herramientas de rousseau **no** se invoca para este proveedor — `claude` ejecuta sus propias herramientas dentro del subproceso. Los objetos de respuesta regresan como un único mensaje de texto de fin de turno. Si necesitas que rousseau controle `bash`/`edit`/`write` a través de la política de aprobación, usa en su lugar `anthropic`, `bedrock`, `vertex` o un proveedor compatible con OpenAI.

## Herencia de autenticación

El CLI `claude` guarda la autenticación en tres lugares:

| Ubicación | Contenido |
|---|---|
| `~/.claude/` | Tokens OAuth (suscripción), salida del helper de API key, configuración del workspace. |
| Llavero del sistema | En macOS, `claude` puede cachear tokens de refresco en el llavero de login. |
| Variable `ANTHROPIC_API_KEY` | Si está establecida, `claude` la usa para el modo API key en lugar de OAuth. |

`claudecli` nunca las lee directamente. Cada invocación es `exec.CommandContext(binary, args...)` — el subproceso hereda el entorno y directorio de inicio del padre y busca sus propias credenciales. Eso es lo que lo hace "sin configuración" para operadores individuales.

<aside class="admonition" data-type="tip"><span class="admonition-title">Bind mounts de contenedor</span><p>Al ejecutar rousseau en un contenedor, monta <code>~/.claude</code> con bind mount de lectura/escritura en el contenedor para que <code>claude</code> pueda refrescar los tokens OAuth cacheados en el mismo lugar:</p></aside>

```ini
Volume=%h/.claude:/home/rousseau/.claude:rw,Z
```

La etiqueta `Z` es crítica en hosts con SELinux; consulta [Despliegue](/es/deployment/) para la unidad Quadlet completa.

## Configuración

```yaml
provider: claudecli

claudecli:
  binary: claude
  model: sonnet
  permission_mode: bypassPermissions
  extra_args:
    - --add-dir
    - /workspace
```

| Campo | Por defecto | Efecto |
|---|---|---|
| `binary` | `claude` | Ejecutable resuelto en `$PATH`. Apunta a una ruta absoluta si tienes múltiples versiones de `claude`. |
| `model` | *vacío* | Pasado como `--model <valor>`. Vacío usa el por defecto de `claude`. |
| `permission_mode` | *vacío* | Pasado como `--permission-mode <valor>`. Consulta la tabla a continuación. |
| `extra_args` | `[]` | Antepuesto antes de `-p <prompt>` en cada invocación. |

Cada campo se mapea a `ClaudeCLIConfig` en `internal/config/config.go`. La línea de comandos del subproceso ensamblada en cada turno es:

```sh
claude --print --output-format json \
  --session-id <sessionID> \
  --system-prompt <systemPrompt> \
  --model <model> \
  --permission-mode <permissionMode> \
  <extra_args...> \
  <prompt>
```

<aside class="admonition" data-type="warning"><span class="admonition-title">Parseo de STDOUT</span><p>Rousseau espera que <code>claude</code> emita un envoltorio JSON en stdout. Si envuelves <code>claude</code> en un script de shell (para auditoría, redacción o limitación de tasa), el envoltorio debe reenviar stdout sin modificar. El parser tolera una línea de log inicial antes del primer <code>{</code> — consulta <code>parseResult</code> en <code>internal/llm/claudecli/client.go</code> — pero basura tras el envoltorio JSON fallará.</p></aside>

## Matriz de PermissionMode

El flag `PermissionMode` refleja el propio `--permission-mode` de `claude`. El subproceso impone el valor; rousseau no lo verifica de nuevo.

<div class="tabs" data-tabs="claudecli-permission-modes">
  <div class="tab-list" role="tablist" aria-label="PermissionMode selector">
    <button role="tab" aria-selected="true">Supervisado</button>
    <button role="tab" aria-selected="false">No supervisado</button>
    <button role="tab" aria-selected="false">Solo lectura</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Sesiones TUI interactivas donde un humano está en el terminal y puede aprobar invocaciones de herramientas.

| Modo | Comportamiento |
|---|---|
| `default` | Claude Code pide interactivamente cada invocación de herramienta. Mejor para sesiones exploratorias. |
| `acceptEdits` | Las ediciones de archivo proceden sin pedirlo; otras herramientas aún preguntan. Bueno cuando confías en la superficie de edición. |
| `auto` | Automático según la herramienta. Úsalo cuando quieras que la heurística incorporada de claude decida. |

```yaml
claudecli:
  permission_mode: acceptEdits
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Los transportes de chat (WhatsApp, Slack, Discord, Signal, …) no tienen un humano en el terminal para responder a los avisos.

| Modo | Comportamiento |
|---|---|
| `bypassPermissions` | Cada invocación de herramienta se ejecuta sin preguntar. Acepta el radio de impacto completo. |
| `dontAsk` | Alias tratado de forma similar a bypass. |

```yaml
claudecli:
  permission_mode: bypassPermissions
```

El CLI establece `bypassPermissions` automáticamente para servicios no supervisados si el operador no especificó uno — consulta `setUnattendedPermissionDefault` en `internal/cli`.

<aside class="admonition" data-type="caution"><span class="admonition-title">Radio de impacto</span><p><code>bypassPermissions</code> da al modelo acceso directo a <code>bash</code> con los privilegios del servicio. Combínalo con (a) un contenedor endurecido, (b) una allowlist y (c) un aprobador en modo pattern del lado de rousseau — o usa un proveedor distinto de <code>claudecli</code> que permita a rousseau imponer aprobaciones antes de que la herramienta se ejecute.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Modo de exploración para refactorizaciones grandes o revisiones de código donde no quieres ninguna escritura.

| Modo | Comportamiento |
|---|---|
| `plan` | Modo planificador. Se permiten lecturas y grep; las escrituras están inhibidas. |

```yaml
claudecli:
  permission_mode: plan
```

Combínalo con el modo de solo lectura propio de rousseau (consulta [Guías: Modo de solo lectura](/es/guides/read-only-mode/)) para un refuerzo con cinturón y tirantes.

  </div>
</div>

## Correlación de sesión

`claudecli` mantiene el estado de la conversación dentro del subproceso. Rousseau correlaciona sus propios IDs de sesión con los de `claude` mediante dos flags:

- `claude -p --session-id <uuid>` crea una nueva sesión. Si el UUID ya existe, `claude` falla con `already in use`.
- `claude -p --resume <uuid>` reanuda una sesión existente. Si es desconocida, `claude` falla.

Rousseau elige el flag usando un `SessionCache` en memoria (`InMemorySessionCache` por defecto). En un miss de caché al arranque en frío donde `claude` ya tiene estado de una ejecución previa de rousseau, el proveedor intenta optimistamente `--session-id`, atrapa el error `already in use` y reintenta con `--resume`. Consulta el comentario sobre `(*Provider).Complete` en `internal/llm/claudecli/client.go`.

Los llamadores que incrustan el proveedor pueden intercambiar por una caché persistente vía `provider.WithCache(store)` — el almacén `state.sqlite` implementa la misma interfaz y sobrevive a reinicios del servicio, evitando la ida y vuelta de arranque en frío en el primer turno tras un reinicio.

## Alias de modelo

Los alias de modelo de `claude` son respetados por el subproceso sin cambios:

| Alias | Apunta a |
|---|---|
| `sonnet` | El modelo por defecto actual de nivel Sonnet. |
| `opus` | El modelo por defecto actual de nivel Opus. |
| `haiku` | El modelo por defecto actual de nivel Haiku. |

Para reproducibilidad entre reinicios del servicio (benchmarks de skills, tareas cron, ejecuciones por lote), fija un ID de modelo exacto:

```yaml
claudecli:
  model: claude-sonnet-4-6
```

<aside class="admonition" data-type="note"><span class="admonition-title">Los alias siguen a los releases</span><p>Los alias se mueven cuando Anthropic publica un nuevo modelo. El alias <code>sonnet</code> en julio de 2026 no apunta a los mismos pesos a los que apuntaba el alias <code>sonnet</code> en abril de 2026. Si tu flujo de trabajo depende de un comportamiento específico, fija el ID exacto.</p></aside>

## Combinando con skills

`claudecli` envía el system prompt vía `--system-prompt` al crear la sesión. `claude` lo respeta textualmente e ignora valores subsecuentes de `--system-prompt` en `--resume` — lo que coincide con cómo lo usa rousseau. La salida del `SkillsProvider` se inserta antes de la invocación:

```
<agent.SystemPrompt>

<skill 1 markdown>

<skill 2 markdown>

<RecallProvider appendix>
```

Consulta `systemPrompt()` en `internal/agent/agent.go`. Los skills funcionan idénticamente en cada proveedor; la mecánica de la composición ocurre en `agent.Agent`, no en el proveedor.

<aside class="admonition" data-type="tip"><span class="admonition-title">Caché de prompt</span><p>El proveedor Anthropic directo marca el system prompt para la caché de prompt efímera (consulta <code>internal/llm/anthropic/cache.go</code>). <code>claudecli</code> no lo hace — <code>claude</code> posee su propia caché internamente. Si quieres ahorros medibles con la caché de prompt, usa <code>provider: anthropic</code>.</p></aside>

## Gotchas

- **Sin portabilidad entre proveedores.** Una sesión creada contra `claudecli` no es portable a `anthropic` — el estado del lado del modelo vive dentro de `claude`. Cambiar de proveedor a mitad de camino fuerza una nueva sesión.
- **El registro de herramientas no se invoca.** `bash`, `edit`, `write`, `grep`, `read` son ejecutados por `claude`, no por `rousseau`. El `agent.Approver` de rousseau no puede controlar esas invocaciones. Usa un proveedor distinto de `claudecli` si necesitas aplicación de aprobación del lado de rousseau.
- **Alcance de `--add-dir`.** Por defecto `claude` se niega a leer fuera de su propio workspace. Pasa `--add-dir /workspace` (o donde viva tu fuente) vía `extra_args` para ampliarlo. Combina con la política de aprobación de rousseau a nivel de transporte si quieres compensar la pérdida de control.
- **Streaming.** `claudecli` usa `claude -p --output-format json` (sin streaming). La ruta de streaming en `internal/llm/claudecli/stream.go` lee `--output-format stream-json`; opta por ella usando `StreamingProvider` desde una integración incrustada.
- **Fuga del entorno.** El subproceso hereda cada variable de entorno del padre. Si `ANTHROPIC_API_KEY` está establecida en el entorno de rousseau, `claude` la preferirá sobre el OAuth cacheado. Eso normalmente está bien, pero cambia la facturación.

## Solución de problemas

### `claudecli: run: exec: "claude": executable file not found in $PATH`

`claude` no está en `PATH` (o la imagen de contenedor no lo incluye). Dos soluciones:

1. Establece `claudecli.binary` a una ruta absoluta.
2. Añade Claude Code a la capa de runtime del contenedor — el `docker/Dockerfile` de referencia usa `node:22-alpine` por esta razón.

### `claudecli: model error: session id already in use`

Estás ejecutando dos procesos de rousseau contra el mismo ID de sesión y la misma instalación de `claude`, o la caché en memoria descartó una sesión que `claude` aún recuerda. El reintento optimista descrito arriba maneja el segundo caso; el primero significa que tienes servicios concurrentes pisándose.

### `claudecli: no JSON in output`

`claude` imprimió algo que no es JSON en stdout, o salió antes de emitir el envoltorio. Causas comunes: una clave de API inválida del lado de Claude Code, una versión de `claude` anterior a `--output-format json`, o un envoltorio de shell escribiendo marcadores de progreso. Ejecuta `claude -p --output-format json 'hello'` directamente para aislar.

### La respuesta se corta a mitad de frase

La salida de `claude` está limitada por `--max-turns` y su propio presupuesto interno de tokens. Rousseau no establece `--max-turns`; si lo estableces vía `extra_args`, súbelo. Para generaciones largas, considera un proveedor de API directa donde controles `MaxTokens` desde `internal/llm/anthropic/client.go`.

### El plan de suscripción tiene rate limit pero la API está bien

El CLI `claude` en un plan de suscripción tiene límites ocultos por conversación y por ventana. Si los alcanzas, cambia a `provider: anthropic` con una clave de API — la API directa tiene límites explícitos y publicados (consulta [Guías: Límites de tasa](/es/guides/rate-limits/)).

## Páginas relacionadas

- [Proveedores: Anthropic](/es/providers/anthropic/) — API directa con caché de prompt y streaming.
- [Proveedores: Bedrock](/es/providers/bedrock/) — Claude gestionado por AWS.
- [Guía de usuario: Políticas de aprobación](/es/user-guide/approval-policies/) — cómo controlar invocaciones de herramientas en la capa de rousseau.
- [Skills](/es/skills/) — cómo se compone el apéndice del system prompt.
- [Configuración](/es/configuration/) — el bloque `claudecli` en contexto.

## Lectura adicional

- `internal/llm/claudecli/client.go` — invocación del subproceso, correlación de sesión, parseo JSON.
- `internal/llm/claudecli/stream.go` — variante de streaming usando `--output-format stream-json`.
- `internal/config/config.go` — struct `ClaudeCLIConfig`.
- `internal/cli/root.go` — cómo `setUnattendedPermissionDefault` elige `bypassPermissions` para transportes de chat.
