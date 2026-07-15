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
description: "Worked example: lock down the bash tool with a pattern-mode approver, deny rules on destructive commands, and slog-driven audit trail."
keywords: "approval policy, pattern mode, bash tool, deny rules, audit trail, slog"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/guides/audit-approval-policies/"
subtitle: "Pattern-mode approver with deny rules on the bash tool."
tags: "guides, audit, approval, pattern-mode, bash, deny"
title: "Guía: auditoría + políticas de aprobación"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approval policy, pattern mode, bash tool, deny rules, audit trail, slog"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guía: auditoría + políticas de aprobación"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 34
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/audit-approval-policies/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/audit-approval-policies/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guía: auditoría + políticas de aprobación"
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
twitter_description: "Worked example: lock down the bash tool with a pattern-mode approver, deny rules on destructive commands, and slog-driven audit trail."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guía: auditoría + políticas de aprobación"
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

## El problema

Un demonio de transporte de chat desatendido no tiene un humano en la terminal para aprobar llamadas a herramientas en tiempo real. Si el modelo quiere ejecutar `rm -rf /workspace/*`, algo tiene que detenerlo. El approver en modo `pattern` de Rousseau es esa palanca.

La amenaza no es que el modelo se descontrole — es que una instrucción comprometida o mal alineada llegue al demonio a través del canal de transporte. Una política en modo pattern con un fallback `default: deny` hace que el riesgo esté acotado y sea auditable.

## Modos del approver

Se incluyen tres modos integrados (véase `internal/agent/approver.go`):

| Modo | Comportamiento | Cuándo usarlo |
|---|---|---|
| `allow_all` | Cada llamada a herramienta se ejecuta. | `rousseau chat` interactivo donde el proveedor `claudecli` gestiona sus propias aprobaciones. |
| `deny_all` | Cada llamada a herramienta se bloquea. Los motivos de denegación se exponen al modelo como errores de `tool_result` para que pueda adaptarse. | Postura de inspección solo lectura; smoke tests. |
| `pattern` | Reglas regex de allow / deny por herramienta. **Deny gana sobre allow.** Las solicitudes no coincidentes caen al `default`. | Cualquier demonio desatendido en producción. |

## Configuración de ejemplo

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by pattern policy — ask the operator"
    allow:
      # Read-side tools: no restriction inside the workspace.
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

      # Edit inside /workspace only.
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}

      # Write inside /workspace only.
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}

      # Shell commands: whitelist of safe read-side utilities plus git status/diff.
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|grep|rg|find|wc|stat|file|which|pwd|env|git status|git diff|git log|go test|go vet|go build)\\b"}

    deny:
      # Absolute deny rules override any allow above.
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s|ncat"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}   # fork bomb
      - {tool: write, match: "\"path\":\"/etc/|/root/|/var/"}
      - {tool: edit, match: "\"path\":\"/etc/|/root/|/var/"}
```

De `PatternApprover.Approve` se desprenden dos propiedades importantes:

1. **Deny gana.** Cada regla deny se comprueba antes que cualquier regla allow. Esto es más seguro que lo contrario: un operador que añada un allow amplio nunca podrá desbloquear accidentalmente una categoría que creía denegada.
2. **Sin coincidencia → deny.** Con `default: deny`, cualquier llamada a herramienta que el operador haya olvidado enumerar queda bloqueada. Esta es la disposición segura por defecto; si quieres lo contrario, define `default: allow`.

## Lectura del registro de auditoría

Cada llamada a herramienta y cada denegación se emite mediante el logger slog:

```
INFO tool.execute name=read id=t_1
INFO tool.execute name=grep id=t_2
WARN tool.denied  name=bash reason="denied by pattern policy — ask the operator"
```

El demonio usa `slog` con nivel y formato configurables (`log.level`, `log.format`). En producción, prefiere `format: json` para que las herramientas aguas abajo (Loki, Vector, Datadog) parseen sin problemas. Consulta [Guías: observabilidad](/es/guides/observability/) para la receta de pipeline.

Cada denegación lleva una clave estructurada estable:

- `tool.denied` — la llamada a herramienta fue bloqueada. Campos: `name` (identificador de herramienta), `reason` (de `PatternApprover.DenyReason` o del fallback integrado).
- `tool.execute` — la llamada a herramienta se ejecutó. Campos: `name`, `id` (el ID de llamada emitido por el modelo, para correlación).
- `tool.error` — la herramienta se ejecutó pero falló. Campos: `name`, `err`.

Un filtro `slog` sobre `tool.denied` te da la vista de auditoría de "intentos bloqueados" que la mayoría de marcos de cumplimiento requieren.

## Prueba de la política

`internal/agent/approver_test.go` en el árbol de código ejercita `PatternApprover` con una matriz amplia. Para hacer un smoke test de tus propias reglas:

```sh
rousseau chat
> Ejecuta `rm -rf /tmp/foo` por mí.
```

El modelo intentará la llamada a la herramienta `bash`. El demonio registra `tool.denied` y devuelve la cadena `reason` al modelo, que normalmente pivotará ("No puedo ejecutar eso — ¿puedes decirme qué intentabas hacer?").

Para la matriz de pruebas de referencia, consulta `internal/agent/approver_test.go` — allí se ejercitan las mismas formas de reglas.

## Añadir una sobrescritura manual

A veces un operador quiere aprobar manualmente una única llamada peligrosa. El patrón más simple:

1. Establece `mode: allow_all` en `rousseau chat` (TUI interactiva). El proveedor `claudecli` gestiona sus propios prompts de aprobación por llamada.
2. Mantén `mode: pattern` en todo demonio desatendido.

Hoy en día no existe una UI de aprobación por llamada interactiva en los transportes de chat — la historia de seguridad es enteramente regex + slog.

## Lo que la política no hace

- **No aísla la herramienta en sandbox.** Una llamada `bash` que sobreviva al approver se ejecuta con el UID del demonio y su visibilidad de sistema de ficheros. Coloca por debajo un contenedor sin root ([Despliegue](/es/deployment/)).
- **No aplica rate-limit.** Diez llamadas `bash` permitidas por segundo pasan. Si necesitas rate limiting, envuelve el registro de herramientas.
- **No audita llamadas de red salientes.** Si una invocación `bash` hace curl a algo, el approver no verá la URL — solo la cadena `command` inicial del `bash`. Deniega `curl` y `wget` de forma tajante a nivel de pattern.

## Patrones comunes

### Restringir la edición a un árbol de directorios

```yaml
allow:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/[^\"]*\""}
  - {tool: write, match: "\"path\":\"/workspace/repo/[^\"]*\""}
deny:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/(\\.git|node_modules|vendor)/"}
```

### Auditor de solo lectura

```yaml
mode: pattern
default: deny
allow:
  - {tool: read, match: ".*"}
  - {tool: grep, match: ".*"}
```

Combinado con `provider.claudecli.permission_mode: plan`, esto genera una postura de inspección de solo lectura — consulta [Guías: modo solo lectura](/es/guides/read-only-mode/).

### Flujos con Git primero

```yaml
allow:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"git (status|diff|log|show|branch|stash|fetch|pull --ff-only)\\b"}
deny:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"git (push|reset --hard|clean -fd|checkout --)\\b"}
```

## Cinco conjuntos de reglas de referencia

<div class="tabs" data-tabs="approval-rulesets">
  <div class="tab-list" role="tablist" aria-label="Reference ruleset">
    <button role="tab" aria-selected="true">Portátil de desarrollo</button>
    <button role="tab" aria-selected="false">Staging</button>
    <button role="tab" aria-selected="false">Producción</button>
    <button role="tab" aria-selected="false">Bot de guardia</button>
    <button role="tab" aria-selected="false">Solo lectura</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**Portátil de desarrollo.** Permisivo por defecto, deniega lo realmente peligroso. Asume una terminal atendida.

```yaml
agent:
  approver:
    mode: pattern
    default: allow
    deny:
      - {tool: bash, match: "rm\\s+-rf\\s+/"}
      - {tool: bash, match: "sudo(?!\\s+-n)"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}
      - {tool: write, match: "\"path\":\"/etc/|/root/"}
      - {tool: edit, match: "\"path\":\"/etc/|/root/"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Staging.** Lista de allow explícita para el workspace, denegar todo lo demás. Adecuado para un demonio de staging compartido con radio de impacto limitado.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by staging policy — ping #platform for exceptions"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: bash, match: "^\\{\"command\":\"git (status|diff|log|show|branch|fetch|pull --ff-only)\\b"}
      - {tool: bash, match: "^\\{\"command\":\"(ls|cat|grep|rg|find)\\s"}
    deny:
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s"}
      - {tool: edit, match: "\"path\":\"/workspace/(\\.git|node_modules|vendor)/"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Producción.** Deny primero. Cada comando permitido está explícitamente enumerado. Adecuado para un demonio de producción que responde preguntas orientadas al cliente.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by production policy — this daemon is read-mostly"
    allow:
      - {tool: read, match: "\"path\":\"/workspace/(runbooks|docs|src)/"}
      - {tool: grep, match: "\"path\":\"/workspace/(runbooks|docs|src)/"}
      - {tool: bash, match: "^\\{\"command\":\"(ls|cat|rg)\\s"}
    deny:
      # Denegaciones en capas por si acaso.
      - {tool: write, match: ".*"}
      - {tool: edit, match: ".*"}
      - {tool: bash, match: "\\b(rm|mv|cp|dd|mkfs|kill|killall)\\b"}
      - {tool: bash, match: "\\b(curl|wget|nc|ncat|ssh|scp|rsync)\\b"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Bot de guardia.** Puede consultar monitorización, seguir logs, pero no reiniciar servicios ni editar código. Adecuado para un asistente de respuesta a incidentes de cara a Slack.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied — oncall bot can query, not mutate"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\{\"command\":\"(kubectl|helm|argocd) (get|describe|logs|top|status)\\b"}
      - {tool: bash, match: "^\\{\"command\":\"(curl|http|wget) -[gsL]* https?://monitoring\\."}
      - {tool: bash, match: "^\\{\"command\":\"(pg_dump|psql -c 'SELECT|redis-cli GET)\\b"}
    deny:
      - {tool: write, match: ".*"}
      - {tool: edit, match: ".*"}
      - {tool: bash, match: "\\b(kubectl (apply|delete|edit|scale)|helm (install|upgrade|uninstall))\\b"}
      - {tool: bash, match: "\\b(systemctl (start|stop|restart|reload))\\b"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Auditor de solo lectura.** Sin escrituras, sin shell. Adecuado para un bot de revisión de código o un demonio que explique documentación.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "read-only auditor — no side effects permitted"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
```

Combínalo con `provider.claudecli.permission_mode: plan` y `provider.claudecli.extra_args: ["--allowed-tools", "read,grep"]` para un refuerzo con doble cinturón — el modelo literalmente no puede solicitar otras herramientas.

  </div>
</div>

## Solución de problemas

### Cada llamada se deniega aunque tengo reglas allow

Deny gana sobre allow. Comprueba si alguna de tus reglas deny coincide de forma no intencionada. La línea de log `tool.denied name=<X> reason=<Y>` incluye el motivo exacto.

### Error al compilar la regex de un pattern

`PatternApprover` compila las reglas de forma perezosa en el primer uso. Un error de compilación se convierte en un `DecisionDeny` con motivo `approver: pattern compile: <err>`. Corrige la regex; regex101.com con el sabor de Go seleccionado es tu aliado.

### La regex coincide con el JSON literalmente, no semánticamente

La regex de `match` se aplica sobre la entrada JSON en bruto de la llamada a herramienta. Escapa comillas y contrabarras apropiadamente: `"\"path\":\"/workspace/"` coincide con el campo `path` de una llamada `edit` o `write`.

### `deny_all` no está bloqueando nada

Confirma `mode: deny_all` (no `mode: deny`). Los modos válidos son `allow_all`, `deny_all`, `pattern`. `allow` y `deny` por sí solos se tratan como alias de las variantes `_all`, pero las cadenas exactas son más seguras.

### La regla allow para `bash` no coincide nunca

La entrada de `bash` es JSON como `{"command":"ls -la"}`. Haz match contra ese literal JSON, no solo contra la cadena del comando shell. Usa un patrón como `^\\{\"command\":\"ls`.

## Páginas relacionadas

- [Guía de usuario: políticas de aprobación](/es/user-guide/approval-policies/) — referencia más profunda y ejemplos trabajados.
- [Guía de usuario: herramientas](/es/user-guide/tools/) — el esquema de cada herramienta integrada.
- [Guías: observabilidad](/es/guides/observability/) — expone el registro de auditoría.
- [Guías: modo solo lectura](/es/guides/read-only-mode/) — refuerzo con doble cinturón.
- [Seguridad](/es/security/) — visión general del modelo de confianza.

## Lecturas adicionales

- `internal/agent/approver.go` — `PatternApprover`, `AllowAllApprover`, `DenyAllApprover`.
- `internal/agent/approver_test.go` — matriz de pruebas.
- `internal/cli/approver.go` — traducción config → approver.
- `internal/config/config.go` — `ApproverConfig`, `PatternEntry`.
