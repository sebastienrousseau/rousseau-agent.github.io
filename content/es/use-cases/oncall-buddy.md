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
description: "Use case narrative: a solo SRE running rousseau-agent over Slack to triage a 3 a.m. page from the couch, then hand off to full incident response."
keywords: "on-call, sre, slack, incident, page, triage, use case"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/use-cases/oncall-buddy/"
subtitle: "Triaging a 3 a.m. page from the couch over Slack."
tags: "use-cases, on-call, slack, sre"
title: "Caso de uso: compañero de guardia"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "on-call, sre, slack, incident, page, triage, use case"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Caso de uso: compañero de guardia"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 71
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/use-cases/oncall-buddy/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/oncall-buddy/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Caso de uso: compañero de guardia"
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
twitter_description: "Use case narrative: a solo SRE running rousseau-agent over Slack to triage a 3 a.m. page from the couch, then hand off to full incident response."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Caso de uso: compañero de guardia"
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

## La historia

Son las 3 de la madrugada. Tu pager suena. PagerDuty dice que el servicio de checkout devuelve 502. Eres uno de los dos SRE de una empresa pequeña, tu co-lead está de vacaciones, y llegar al portátil implica encontrar las gafas, bajar y desbloquear una VPN. Antes de todo eso, quieres una respuesta preliminar: qué dashboards se ven mal, qué cambió en las últimas 24 horas, qué runbook aplica.

Rousseau vive en la ops box de tu armario. Tiene credenciales de solo lectura a tu stack de logs, kubectl de solo lectura en un namespace y una conexión Slack Socket Mode a `#incident-oncall`. Tocas la notificación de DM en tu móvil:

> ¿qué cambió en checkout en las últimas 24h?

Rousseau lee el git log del repositorio del servicio checkout, lo cruza con tu log de despliegues (de un directorio bind-mounted) y responde:

> Dos cambios: PR #4821 (lógica de reintentos de pago, desplegado a las 21:14 UTC) y un bump de un valor Helm en `checkout-web` a las 22:03 UTC. El cambio de reintentos de pago es el más sospechoso — toca el mismo camino de código donde se originan los 502 actuales.

Preguntas:

> saca las últimas 100 líneas de error de checkout-web

Rousseau ejecuta `kubectl logs -n checkout deploy/checkout-web --tail=100 --previous` bajo su kubeconfig de solo lectura y devuelve pegadas las líneas relevantes. Detectas un traceback de null-pointer. Le respondes por DM:

> revierte primero el PR #4821 en staging — avísame cuando confirmes que está verde

Rousseau publica en `#incident-oncall` con un plan, abre un PR de revert contra staging y avisa cuando staging está verde. Te levantas y vas al portátil.

## Lo que eso requiere

### El demonio

Rousseau se ejecuta como un contenedor Podman sin root en la ops box:

- **Proveedor**: `bedrock` — tu empresa ya tiene un compromiso de gasto con Bedrock; no se requieren API keys por usuario.
- **Transporte**: Slack Socket Mode — sin superficie HTTP entrante, solo WebSocket saliente.
- **Estado**: `~/.local/share/rousseau/sessions.db`, en un disco cifrado con LUKS.

### Configuración

```yaml
provider: bedrock

bedrock:
  region: us-east-1
  profile: rousseau-oncall
  model: anthropic.claude-sonnet-4-6-20250101-v1:0

log:
  level: info
  format: json

state:
  path: /var/lib/rousseau/sessions.db

agent:
  max_iterations: 32
  approver:
    mode: pattern
    default: deny
    reason: "read-only on-call posture — ask an operator to widen the scope"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(kubectl get|kubectl describe|kubectl logs|git log|git diff|git show|cat|grep|rg|head|tail|wc) "}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"gh pr (view|list|diff) "}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"gh pr create --draft "}   # permite abrir un revert como borrador
    deny:
      - {tool: bash, match: "kubectl (delete|apply|edit|scale|rollout undo|exec)"}
      - {tool: bash, match: "gh pr merge|gh pr close --delete-branch"}

slack:
  app_token: xapp-<...>
  bot_token: xoxb-<...>
  allowlist:
    - U012ABCXYZ    # tu ID de usuario de Slack
    - U012DEFGHI    # ID de usuario de Slack de tu co-lead
```

### Los bind mounts

- Checkouts de repositorio bajo `/workspace/repos/` (solo lectura).
- Log de despliegues bajo `/workspace/deploys/` (solo lectura).
- kubeconfig en `/home/rousseau/.kube/config` — montado en solo lectura, la service account tiene un cluster role de solo lectura en el namespace `checkout`.
- Credenciales AWS vía IAM Role for Service Accounts (IRSA) si es EKS, o vía un `~/.aws/` montado para on-prem.

### La unidad Quadlet de systemd

La referencia `docker/rousseau-agent.container` con:

- `ReadOnly=true`
- `DropCapability=all`
- `NoNewPrivileges=true`
- `Restart=on-failure`

Arranca al reiniciar el host. Journal disponible vía `journalctl --user -u rousseau-agent.service`.

## La postura de seguridad

- **La allowlist de Slack** garantiza que solo tú y tu co-lead pueden dirigir el demonio. Cualquier otro DM se descarta en silencio.
- **Pattern approver con `default: deny`** bloquea todo lo que esté fuera de la lista blanca. Si el modelo quiere ejecutar `kubectl delete pod`, obtiene un error `tool_result` explicando el bloqueo y redirige a un documento de plan.
- **kubeconfig de solo lectura + mounts de repositorio de solo lectura** implican que el demonio *no puede* mutar producción incluso si el approver fallara abierto.
- **Doble cinturón y tirantes** — cada capa falla de forma segura.

## Lo que rousseau no hace aquí

- **No te llama.** PagerDuty es la fuente de verdad para quién está de guardia.
- **No hace merge de PRs.** El approver bloquea `gh pr merge`. Rousseau puede abrir un revert como borrador; un humano aún debe confirmarlo.
- **No ejecuta `kubectl exec`.** Cualquier comando que pudiera mutar el estado del clúster es denegado.
- **No aprende del incidente.** El recall entre sesiones vía FTS5 significa que el rousseau del próximo incidente encontrará palabras clave de la sesión de esta noche; las conclusiones semánticas siguen siendo trabajo del operador.

## Lo que cambiarías con más carga

Si dos llamadas a las 3 de la madrugada al mes pasan a ser dos por semana:

- Considera promover más matchers de `bash` a `allow` a medida que ganas confianza.
- Cablea la salida de slog a [Loki](/es/guides/observability/) para que las revisiones post-mortem puedan citar las llamadas exactas a herramientas que hizo rousseau.
- Añade [tareas programadas](/es/guides/scheduled-tasks/) para que rousseau ejecute un resumen nocturno de los incidentes abiertos en tu Slack matutino.

## Páginas relacionadas

- [Guías: auditoría y políticas de aprobación](/es/guides/audit-approval-policies/) — la palanca de seguridad.
- [Guías: modo solo lectura](/es/guides/read-only-mode/) — la postura más estricta.
- [Transporte Slack](/es/transports/slack/) — cableado de Socket Mode.
- [Proveedor Bedrock](/es/providers/bedrock/) — cadena de autenticación.
