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
description: "Go from bypassPermissions to a pattern-mode approver with default: deny and validate the audit trail through slog."
keywords: "approver, pattern mode, default deny, tool denied, audit, slog"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/tutorials/harden-approver-policy/"
subtitle: "From bypassPermissions to default-deny with slog-audited rule matching."
tags: "tutorials, approver, pattern-mode, security, audit"
title: "Tutorial: endurecer el aprobador"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approver, pattern mode, default deny, tool denied, audit, slog"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorial: endurecer el aprobador"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 46
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/harden-approver-policy/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/harden-approver-policy/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorial: endurecer el aprobador"
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
twitter_description: "Go from bypassPermissions to a pattern-mode approver with default: deny and validate the audit trail through slog."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorial: endurecer el aprobador"
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

## Qué construyes

Un daemon de rousseau que empezó ejecutando el proveedor `claudecli` en modo `bypassPermissions` (el default desatendido) termina bajo un aprobador de rousseau-agent en modo `pattern` con `default: deny`. Cada llamada a herramienta está explícitamente en allowlist o bloqueada; cada denegación produce un evento slog `tool.denied` que puedes auditar.

Tiempo estimado: 30 minutos para una pasada de reglas apropiada con pruebas.

## Requisitos previos

- Rousseau instalado con algún puente de transporte en ejecución (WhatsApp, Slack, Signal: cualquier cosa desatendida).
- Familiaridad básica con regex de Go: las reglas del aprobador son regex Go RE2 sobre la entrada JSON de la herramienta.

## Dónde vive el aprobador

Dos capas independientes pueden aprobar llamadas a herramientas:

1. **El propio modo de permisos del proveedor.** El proveedor `claudecli` (`internal/llm/claudecli/client.go`) delega en `claude --permission-mode`. Valores documentados en `ClaudeCLIConfig.PermissionMode` (`internal/config/config.go`): `acceptEdits`, `auto`, `bypassPermissions`, `default`, `dontAsk`, `plan`. Los daemons desatendidos fijan `bypassPermissions` en `setUnattendedPermissionDefault`.
2. **El aprobador propio de rousseau.** Configurado bajo `agent.approver` (`internal/config/config.go` `ApproverConfig`; implementación en `internal/agent/approver.go`). Tres modos: `allow_all`, `deny_all`, `pattern`. **Deny gana sobre allow, y las llamadas sin coincidencia caen al `default`.**

Para un daemon desatendido, el aprobador de rousseau es la mitigación que configuras a mano. El propio modo de `claudecli` es el cinturón de seguridad.

## Paso 1: auditoría de base

Antes de escribir reglas, ejecuta unas cuantas sesiones realistas con `mode: allow_all` y `log.format: json`. Cada llamada a herramienta emite `tool.execute` (`internal/agent/agent.go`):

```sh
jq -c 'select(.msg == "tool.execute") | {name, input: .input}' \
  < /var/log/rousseau.jsonl \
  | sort | uniq -c | sort -rn | head
```

Ahora tienes una distribución empírica de qué herramientas usa el agente y contra qué rutas. Esa es la semilla para la allowlist.

## Paso 2: redactar una política pattern

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by pattern policy — ask the operator to loosen the rules"
    allow:
      # Lado de lectura: sin restricción dentro de la vista de sistema de archivos del daemon.
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

      # Edición fijada a /workspace.
      - {tool: edit,  match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}

      # Shell: allowlist de utilidades de solo lectura más git status/diff/log.
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|grep|rg|find|wc|stat|file|which|pwd|env|git status|git diff|git log|go test|go vet|go build)\\b"}

    deny:
      # Las denegaciones absolutas anulan cualquier allow anterior.
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s|ncat"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}    # fork bomb
      - {tool: write, match: "\"path\":\"/etc/|/root/|/var/"}
      - {tool: edit,  match: "\"path\":\"/etc/|/root/|/var/"}
```

Despliega y observa el stream de slog. Los eventos relevantes (`internal/agent/agent.go`):

- `tool.execute`: la llamada se ejecutó. Campos: `name`, `id`.
- `tool.denied`: el aprobador la bloqueó. Campos: `name`, `reason`.
- `tool.error`: se ejecutó y falló. Campos: `name`, `err`.

## Paso 3: iterar

El primer día aflora falsos positivos: llamadas legítimas a herramientas que el aprobador bloqueó. Búscalas con grep:

```sh
jq -c 'select(.msg == "tool.denied") | {name, input}' \
  < /var/log/rousseau.jsonl \
  | sort | uniq -c | sort -rn | head
```

Cada `tool.denied` recurrente merece una decisión:

- **Genuinamente necesario**: extiende la regla allow. Prefiere una estrecha (con la ruta fijada) sobre una amplia (regex abierta).
- **No necesario**: déjalo denegado. El modelo pivotará a un enfoque diferente.

No debilites `default: deny`. Esa es la propiedad que hace segura una herramienta olvidada.

## Paso 4: extracto del log de auditoría

Una ejecución de producción con un prompt desconocido se vio así:

```jsonl
{"time":"2026-07-13T18:00:12Z","level":"INFO", "msg":"whatsapp.incoming","from":"447900123456@s.whatsapp.net"}
{"time":"2026-07-13T18:00:14Z","level":"INFO", "msg":"tool.execute","name":"grep","id":"t_1"}
{"time":"2026-07-13T18:00:15Z","level":"INFO", "msg":"tool.execute","name":"read","id":"t_2"}
{"time":"2026-07-13T18:00:17Z","level":"WARN", "msg":"tool.denied","name":"bash","reason":"denied by pattern policy — ask the operator to loosen the rules"}
{"time":"2026-07-13T18:00:18Z","level":"INFO", "msg":"tool.execute","name":"read","id":"t_3"}
{"time":"2026-07-13T18:00:20Z","level":"INFO", "msg":"whatsapp.handler_ok","elapsed":"7.4s"}
```

El único `tool.denied` aquí fue `bash: "curl https://…"`. La regla deny lo atrapó, el modelo degradó a `read` + `grep`, y la respuesta igualmente llegó.

## Paso 5: consolidarlo

Una vez que la tasa de falsos positivos se estabilice, congela la configuración, comprométela en control de código (secretos excluidos: consulta [Guías: Onboarding empresarial](/es/guides/enterprise-onboarding/)), y protege los cambios de configuración detrás de una revisión de código. `internal/agent/approver_test.go` en el árbol de código es tu modelo para escribir pruebas contra el ruleset: copia su forma en un paquete interno si quieres que CI atrape una política rota.

## Lo que la política sigue sin hacer

Incluso con las reglas pattern más estrictas:

- **Sin sandboxing.** Una llamada `bash` permitida sigue ejecutándose con el UID y la visibilidad de sistema de archivos del daemon. Coloca por debajo un contenedor rootless ([Despliegue](/es/deployment/)).
- **Sin rate limiting.** Diez llamadas permitidas por segundo son todas permitidas. Envuelve el registro de herramientas si necesitas esto.
- **Sin auditoría de red saliente.** El aprobador ve la cadena `command` inicial de `bash`, no lo que hace curl. Deniega `curl` y `wget` de forma tajante: las reglas deny de ejemplo hacen esto.

Consulta [Guías: Auditoría + políticas de aprobación](/es/guides/audit-approval-policies/) para la discusión más profunda.

## Relacionado

- [Guía de usuario: Políticas de aprobación](/es/user-guide/approval-policies/): referencia para cada modo.
- [Guía de usuario: Herramientas](/es/user-guide/tools/): esquemas de herramientas, útiles para escribir regex.
- [Guías: Observabilidad](/es/guides/observability/): dirige `tool.denied` a Loki/Datadog.
- [Referencia: Logs](/es/reference/logs/): cada mensaje slog bien conocido.
