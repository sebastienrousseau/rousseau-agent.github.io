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
description: "Use case narrative: a financial-services team running rousseau-agent in-tenant on AWS with Bedrock, pattern-mode approvals, and SLSA-3 supply-chain posture."
keywords: "regulated industry, financial services, bedrock, in-tenant, slsa, cosign, compliance"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/use-cases/regulated-industry/"
subtitle: "In-tenant Bedrock deployment for a financial-services team."
tags: "use-cases, bedrock, regulated, financial-services, slsa"
title: "Caso de uso: sector regulado"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "regulated industry, financial services, bedrock, in-tenant, slsa, cosign, compliance"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Caso de uso: sector regulado"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 73
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/use-cases/regulated-industry/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/regulated-industry/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Caso de uso: sector regulado"
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
twitter_description: "Use case narrative: a financial-services team running rousseau-agent in-tenant on AWS with Bedrock, pattern-mode approvals, and SLSA-3 supply-chain posture."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Caso de uso: sector regulado"
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

Eres un ingeniero de plataforma en un banco de tamaño medio. Cumplimiento exige que cualquier asistente de codificación que usen tus ingenieros debe:

1. Ejecutarse dentro de las cuentas AWS del banco, no en un plano de control SaaS.
2. Enrutar el tráfico al modelo a través de un proveedor con el que el banco tenga contrato y pista de auditoría (Bedrock).
3. Tener una postura de cadena de suministro documentada (SLSA-3, SBOM, verificación de firmas).
4. Aplicar políticas de aprobación con un registro de auditoría legible por máquinas.
5. No exfiltrar código fuente a terceros.

El posicionamiento de rousseau encaja en cada uno de esos requisitos. Lo ejecutas como un `Deployment` de Kubernetes en el clúster EKS del equipo de plataforma, alimentando un transporte de Slack en Socket Mode dirigido al canal de ingeniería.

El despliegue de ingeniería no tiene nada notable — un `Deployment`, un `Secret`, un `ConfigMap`, un `PersistentVolumeClaim`. La historia es lo que ocurre cuando llega el auditor.

## La auditoría

Un auditor externo formula cuatro preguntas.

**P1: ¿A dónde va el tráfico del modelo?**

Los diriges a `internal/llm/bedrock/`. El proveedor usa la cadena estándar de credenciales de AWS (vía IRSA en EKS), por lo que las credenciales son tokens STS de corta duración. El tráfico nunca sale de tu cuenta AWS.

**P2: ¿Cómo verificas el binario que estás ejecutando?**

Les muestras `docker/Dockerfile` — un build multietapa con base `golang:1.26-alpine` fijada — y el script `release-verify.sh` que el equipo SRE ejecuta durante la promoción de imágenes:

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_${VERSION}_checksums.txt.sig \
  rousseau_${VERSION}_checksums.txt

sha256sum -c rousseau_${VERSION}_checksums.txt
```

Añades: la procedencia SLSA-3 se atesta mediante GitHub Actions OIDC. El registro de transparencia de Sigstore es un ancla de confianza pública.

**P3: ¿Cómo evitas que el modelo mute producción?**

Los diriges a la configuración `agent.approver`:

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied — this deployment does not permit destructive operations without operator confirmation"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|grep|rg|find|git status|git diff|git log|go test|go build) "}
    deny:
      - {tool: bash, match: "rm -rf|sudo|curl|wget|chmod|chown"}
      - {tool: bash, match: "kubectl (delete|apply|edit|scale|exec)"}
      - {tool: bash, match: "aws (s3 rm|iam|kms delete)"}
      - {tool: write, match: "\"path\":\"/(etc|root|var|usr)/"}
      - {tool: edit,  match: "\"path\":\"/(etc|root|var|usr)/"}
```

Deny gana sobre allow. Sin coincidencia → deny. Cada decisión se registra como un evento slog estructurado (`tool.execute`, `tool.denied`) y se reenvía al tenant de Datadog del banco vía un daemonset de Vector.

**P4: ¿Dónde se almacena el código fuente que una sesión referencia?**

Explicas: el estado de sesión vive en un PVC respaldado por EBS con cifrado en reposo. El contexto del modelo se mantiene dentro de la sesión comprimida (véase [Compresión + Recall](/es/user-guide/compression-recall/)). El índice FTS5 de recall corre en el mismo PVC. Nada va a `agentskills.io` ni a ninguna URL externa — las [Skills](/es/skills/) se cargan desde un directorio bind-mounted, no desde un registro hospedado.

El auditor hace una repregunta: "¿Y el modelo en sí?". Explicas que Bedrock es la frontera del modelo; cualquier cosa que Bedrock haga con los prompts se rige por el contrato existente del banco con AWS.

## Lo que eso requiere

### El manifest

Consulta [Guías: despliegue en Kubernetes](/es/guides/kubernetes-deployment/) para el manifest completo. Desviaciones clave para este caso de uso:

- **Namespace `pod-security.kubernetes.io/enforce: restricted`.**
- **IRSA** para las credenciales de Bedrock — sin claves AWS de larga duración en secrets.
- **NetworkPolicy** permitiendo egreso solo a los endpoints regionales de Bedrock y al WSS de Slack.
- **Daemonset de Vector** enviando la salida de slog a Datadog con el campo `msg` parseado como faceta.

### La configuración

```yaml
provider: bedrock

bedrock:
  region: eu-west-1
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
  max_tokens: 4096

log:
  level: info
  format: json

state:
  path: /var/lib/rousseau/sessions.db

agent:
  max_iterations: 32
  compression:
    enabled: true
    trigger_messages: 40
    keep_recent: 6
  approver:
    mode: pattern
    default: deny
    reason: "denied — this deployment does not permit destructive operations without operator confirmation"
    allow: [...as above...]
    deny:  [...as above...]

slack:
  app_token: xapp-<from-Secret>
  bot_token: xoxb-<from-Secret>
  allowlist:
    - U012ABC   # guardia del equipo de plataforma
    - U012DEF   # lead del equipo de plataforma
```

### La historia de auditoría

Cada llamada a herramienta es una línea de slog. Cada denegación es otra. El monitor de Datadog sobre `msg:tool.denied` alerta al SOC. Semanalmente, el equipo de plataforma extrae un informe:

```
# LogQL / Datadog / whichever
sum by (name) (
  count_over_time({job="rousseau-agent"} |= "tool.denied" [1w])
)
```

El informe va al drive de cumplimiento. Como el esquema de slog es estable ([Observabilidad](/es/guides/observability/)), el parseo no se rompe entre upgrades de rousseau.

## Lo que el auditor podría no preguntar pero debería

- **Builds reproducibles.** El CI de rousseau incluye un job `reproducible-build` que verifica salida bit-idéntica sobre checkouts limpios. Puedes reconstruir de forma independiente desde una fuente etiquetada y comparar SHA-256.
- **Fijación de dependencias.** `go.mod` fija versiones exactas; `go.sum` está congelado. Dependabot abre actualizaciones como PRs revisables, no como bumps silenciosos.
- **`govulncheck` en cada commit.** Cualquier vulnerabilidad conocida que alcance un símbolo importado hace fallar el CI.
- **CodeQL**: análisis estático en cada commit.

Todo lo anterior está en [Seguridad](/es/security/) — el cajón de archivos de cumplimiento ya existe.

## La frontera fuera del tenant

Bedrock es la frontera. El tráfico a `bedrock-runtime.eu-west-1.amazonaws.com` sale del pod pero se queda dentro de AWS. El diagrama de flujo de datos del banco muestra una flecha del pod a Bedrock; no existen otras flechas salientes para este despliegue (Slack Socket Mode es WSS saliente hacia `wss-primary.slack.com`, documentado como un egreso permitido aparte).

## Páginas relacionadas

- [Guías: despliegue en Kubernetes](/es/guides/kubernetes-deployment/) — los manifests.
- [Guías: auditoría y políticas de aprobación](/es/guides/audit-approval-policies/) — la historia de cumplimiento.
- [Guías: observabilidad](/es/guides/observability/) — el pipeline de slog.
- [Proveedor Bedrock](/es/providers/bedrock/) — cadena de credenciales y comportamiento por región.
- [Seguridad](/es/security/) — modelo de confianza y controles de cadena de suministro.
