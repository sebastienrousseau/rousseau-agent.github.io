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
description: "Approval policy reference for rousseau-agent: allow_all, deny_all, and pattern-mode approvers with allow/deny regex rules and a configurable default."
keywords: "approval, approver, pattern mode, allow_all, deny_all, regex, safety, tool call"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/user-guide/approval-policies/"
subtitle: "Deep dive on approver modes with worked config."
tags: "approval, policy, pattern-mode, safety"
title: "Políticas de aprobación"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approval, approver, pattern mode, allow_all, deny_all, regex, safety, tool call"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Políticas de aprobación"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "security"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/approval-policies/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/approval-policies/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Políticas de aprobación"
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
twitter_description: "Approval policy reference for rousseau-agent: allow_all, deny_all, and pattern-mode approvers with allow/deny regex rules and a configurable default."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Políticas de aprobación"
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

## El contrato

Cada llamada a herramienta pasa por `Approver.Approve(ctx, ApprovalRequest)` antes de ejecutarse. La interfaz vive en `internal/agent/approver.go`:

```go
type Decision string

const (
    DecisionAllow Decision = "allow"
    DecisionDeny  Decision = "deny"
)

type ApprovalRequest struct {
    ToolName  string
    Input     json.RawMessage
    SessionID string
}

type Approver interface {
    Approve(ctx context.Context, req ApprovalRequest) (Decision, string)
}
```

`Approve` se invoca de forma síncrona en el camino crítico; las implementaciones deben retornar rápidamente o respetar la cancelación de `ctx`.

Un `DecisionDeny` con un motivo no vacío devuelve el motivo al modelo como un error `tool_result`. El modelo puede entonces adaptarse (normalmente pidiendo al operador una aclaración) en lugar de fallar en silencio. Esta es una decisión de diseño deliberada — las denegaciones silenciosas producen peor comportamiento que las anotadas.

## Tres modos incluidos

### `allow_all`

Cada llamada a herramienta se ejecuta. Este es el comportamiento base cuando no se configura un approver.

```yaml
agent:
  approver:
    mode: allow_all
```

Úsalo cuando:

- Uses `rousseau chat` interactivo con el proveedor `claudecli` (Claude Code gestiona sus propias aprobaciones por llamada).
- Realices smoke tests de desarrollo y quieras ver exactamente qué haría el modelo.

### `deny_all`

Bloquea toda llamada a herramienta con una única cadena de motivo.

```yaml
agent:
  approver:
    mode: deny_all
    reason: "denied by policy for this deployment"
```

Úsalo cuando:

- Hagas smoke test del cableado del approver.
- Adoptes una postura de inspección inicial y quieras ver lo que el modelo *habría* intentado, sin dejarlo actuar.

### `pattern`

Reglas regex de allow / deny por herramienta. **Deny gana sobre allow.** Las solicitudes sin coincidencia caen al `default` (`allow` o `deny`).

```yaml
agent:
  approver:
    mode: pattern
    default: deny         # seguro por defecto; las solicitudes no listadas se bloquean
    reason: "denied by pattern policy"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}
    deny:
      - {tool: bash, match: "rm -rf|sudo|chmod|chown"}
```

## Semántica de reglas

Cada `PatternRule` tiene dos campos:

| Campo | Significado |
|---|---|
| `tool` | Nombre de la herramienta (`read`, `write`, `edit`, `grep`, `bash`, o cualquier herramienta personalizada). Vacío coincide con toda herramienta. |
| `match` | Regex Go RE2 contra la entrada JSON en bruto producida por el modelo. Vacío coincide con toda entrada. |

**Orden de coincidencia:**

1. Cada regla deny se prueba contra la solicitud. Primera coincidencia → deny.
2. Cada regla allow se prueba. Primera coincidencia → allow.
3. Fallback al `default`. Un `default` vacío se trata como `deny` — seguro por defecto.

Deny gana siempre porque se prefiere la disposición más segura. Un operador que añada un bloque `allow` amplio nunca podrá desbloquear accidentalmente una categoría que había denegado.

## Coincidencia contra JSON en bruto

La regex de `match` se aplica contra la **entrada JSON en bruto** que el modelo emitió, no contra campos parseados. Esto tiene dos consecuencias:

1. **Coincides contra la forma JSON.** Para una llamada `bash`, se parece a `{"command":"ls /tmp"}`. Coincide con `"command":\s*"ls\s`.
2. **Puedes coincidir con cualquier campo.** La herramienta `edit` recibe `{"path":"/x","old_string":"...","new_string":"..."}`; puedes hacer match sobre `path`, `old_string` o ambos.

Escapa cuidadosamente los caracteres relevantes en JSON:

- Las comillas dobles son literales en el JSON en bruto — coincide con `\"` en tu regex si usas cadenas YAML con comillas dobles.
- Las contrabarras requieren duplicarse en YAML: `\\` en el archivo YAML se convierte en `\` en la regex compilada.

## Patrones de matcher trabajados

### Restringir ediciones a un árbol de directorios

```yaml
allow:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/[^\"]*\""}
  - {tool: write, match: "\"path\":\"/workspace/repo/[^\"]*\""}
```

### Lista blanca de comandos de shell seguros

```yaml
allow:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|grep|rg|find|git status|git diff|go test) "}
```

### Denegar comandos destructivos independientemente del allow

```yaml
deny:
  - {tool: bash, match: "rm\\s+-rf|sudo|:\\(\\)\\{ :\\|:& \\};:"}
```

### Denegar escrituras a directorios de sistema

```yaml
deny:
  - {tool: write, match: "\"path\":\"/(etc|root|var|usr)/"}
  - {tool: edit,  match: "\"path\":\"/(etc|root|var|usr)/"}
```

## El campo `Default`

`default: deny` es la disposición más segura y el valor recomendado para cualquier demonio desatendido. `default: allow` invierte el modelo — cada llamada no listada se ejecuta, y las reglas `deny` se convierten en la palanca principal.

Cuándo usar `default: allow`:

- El demonio se ejecuta dentro de un contenedor fuertemente restringido ([Despliegue](/es/deployment/)) y el contenedor es tu frontera principal.
- Estás experimentando y quieres ver el comportamiento del modelo antes de decidir qué bloquear.

En todos los demás casos, prefiere `default: deny`.

## El campo `Reason`

`reason` es la cadena devuelta al modelo en cada denegación (o fallback de `default: deny`). Si está vacío, se usa `denied by pattern policy` (o `denied by policy` para `deny_all`).

Establecer un motivo útil mejora la recuperación del modelo — en lugar de `denied by pattern policy`, prueba con `denegado — este despliegue solo permite lecturas dentro de /workspace; pide al operador que amplíe el alcance` y verás que el modelo responde con una aclaración accionable.

## Interacción con `claudecli`

Cuando `provider: claudecli`, Claude Code está ejecutando las llamadas a herramientas, y su propio modo de permisos (`bypassPermissions`, `plan`, `default`) también controla cada acción. El comportamiento efectivo es la intersección: **tanto** el approver de rousseau como el de Claude Code deben permitir la llamada para que se ejecute.

Prefiere mantener ambos alineados:

- Desatendido: `bypassPermissions` en Claude Code, `mode: pattern` + `default: deny` en rousseau.
- Inspección de solo lectura: `plan` en Claude Code, `mode: pattern` permitiendo solo `read`/`grep` en rousseau. Consulta [Guías: modo solo lectura](/es/guides/read-only-mode/).

## Registro de auditoría

Cada decisión del approver se emite mediante slog:

| Evento | Significado |
|---|---|
| `tool.execute` (INFO) | Llamada aprobada, en ejecución. |
| `tool.denied` (WARN) | Llamada bloqueada. Incluye nombre de herramienta y motivo. |
| `tool.error` (WARN) | La llamada se ejecutó pero falló. |

Consulta [Guías: observabilidad](/es/guides/observability/) para recetas de pipeline.

## Approvers personalizados

Cualquier tipo que satisfaga `Approver` funciona. Cablea el tuyo al embeber el bucle del agente:

```go
myApprover := agent.ApproverFunc(func(ctx context.Context, req agent.ApprovalRequest) (agent.Decision, string) {
    // Consultar un motor de políticas externo, preguntar al operador, ...
    return agent.DecisionAllow, ""
})

ag := agent.New(provider, registry, logger, agent.Options{Approver: myApprover})
```

La interfaz es deliberadamente minimalista (`Approve` es el único método), de modo que integrarla con un motor de políticas externo (OPA, Cedar o un motor de reglas propio) es un adaptador pequeño.

## Solución de problemas

### Toda llamada denegada aunque hay un allow que coincide

Deny gana sobre allow. `PatternApprover.Approve` en `internal/agent/approver.go` línea 152 itera primero las reglas deny. Busca la cadena `reason` exacta en los logs de `tool.denied`.

### Error de compilación de regex al arrancar

`PatternApprover` compila las regex de forma perezosa en el primer `Approve`. Un error de compilación produce `DecisionDeny` con motivo `approver: pattern compile: <err>`. Prueba las regex en [regex101.com](https://regex101.com) con el sabor de Go.

### `mode: pattern` pero `default:` se ignora

Solo `allow` y `deny` son valores válidos para `default:`. Los valores vacíos o desconocidos caen a `DecisionDeny` (default seguro) y no emiten warning.

### La regla allow coincide con el JSON literalmente

La regex se aplica contra el JSON de entrada de la llamada a herramienta en bruto. Para hacer match con un campo `path`, escapa comillas: `"\"path\":\"/workspace/"`.

### Las llamadas denegadas no aparecen en los logs

Sí aparecen — como `tool.denied` a nivel `warn`. Si filtras por nivel, asegúrate de incluir `warn`.

## Páginas relacionadas

- [Guías: auditoría y políticas de aprobación](/es/guides/audit-approval-policies/) — ejemplo trabajado con registro de auditoría slog.
- [Guías: modo solo lectura](/es/guides/read-only-mode/) — la postura de inspección.
- [Guía de usuario: herramientas](/es/user-guide/tools/) — las herramientas que el approver controla.
- [Seguridad](/es/security/) — visión general de las fronteras de confianza.
- [Bucle del agente](/es/agent-loop/) — dónde se invoca el approver.

## Lecturas adicionales

- `internal/agent/approver.go` — `PatternApprover`, `AllowAllApprover`, `DenyAllApprover`.
- `internal/agent/approver_test.go` — la matriz de pruebas.
- `internal/cli/approver.go` — traducción config → approver.
- `internal/config/config.go` — `ApproverConfig`, `PatternEntry`.
