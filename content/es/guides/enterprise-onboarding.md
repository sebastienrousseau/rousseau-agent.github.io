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
description: "A checklist for platform teams adopting rousseau-agent: SBOM, cosign, seccomp, network egress, approval policy, at-rest encryption, security SLOs."
keywords: "enterprise, checklist, sbom, cosign, seccomp, egress, encryption, slo"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/guides/enterprise-onboarding/"
subtitle: "The platform-team checklist before rousseau ships beyond a proof-of-concept."
tags: "guides, enterprise, security, checklist, sbom, cosign"
title: "Guía: adopción empresarial"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "enterprise, checklist, sbom, cosign, seccomp, egress, encryption, slo"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guía: adopción empresarial"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/enterprise-onboarding/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/enterprise-onboarding/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guía: adopción empresarial"
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
twitter_description: "A checklist for platform teams adopting rousseau-agent: SBOM, cosign, seccomp, network egress, approval policy, at-rest encryption, security SLOs."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guía: adopción empresarial"
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

## Para quién es esto

Un equipo de plataforma que evalúa rousseau-agent antes de que se acerque a producción. Responde a la pregunta "¿qué necesitamos aprobar?". Cada punto referencia algo concreto que rousseau incluye para que la aprobación sea objetiva y no estética.

## Checklist

### 1. Cadena de suministro

- [ ] **SBOM.** Confirma que cada release publica `rousseau_<v>_sbom.cdx.json` (CycloneDX 1.5). Impórtalo en tu escáner SCA. Accionable: ejecuta `cyclonedx-cli tree` contra el SBOM y busca con grep excepciones de licencia que tu organización prohíba.
- [ ] **Procedencia SLSA-3.** Cada release publica `rousseau_<v>_provenance.intoto.jsonl`. Verifica con `slsa-verifier verify-artifact --source-uri github.com/sebastienrousseau/rousseau-agent …`.
- [ ] **Trust root de cosign.** Fija la regex de identidad de certificado: `sebastienrousseau/rousseau-agent`. Cachea la receta de verificación de checksums en tu tooling de bootstrap; consulta el paso 5 de [Inicio rápido](/es/quickstart/).
- [ ] **Build reproducible.** `make check` ejecuta `go test -race` más `govulncheck`. Configura un escaneo periódico de vulnerabilidades para la versión que estás ejecutando.

### 2. Endurecimiento en runtime

- [ ] **Contenedor sin root.** `docker/rousseau-agent.container` ejecuta la unidad Quadlet bajo un usuario sin privilegios dedicado con `loginctl enable-linger`. Confirma que tu host está configurado igual.
- [ ] **Todas las capabilities eliminadas.** `DropCapability=all`. `podman inspect | jq '.[0].EffectiveCaps'` debería mostrar `[]`.
- [ ] **`NoNewPrivileges=true`.** Impide que procesos hijos ganen privilegios.
- [ ] **Sistema de archivos raíz en solo lectura.** `ReadOnly=true` + `Tmpfs=/tmp:rw,size=64m`.
- [ ] **Perfil seccomp.** `SeccompProfile=/usr/share/containers/seccomp.json`. Audítalo contra la línea base de tu host.
- [ ] **Mapeo de user namespace.** `UserNS=keep-id`. Confirma que los archivos bind-mounted son propiedad correcta en ambos lados.

### 3. Postura de red

- [ ] **Sin entradas.** Rousseau tiene cero superficie HTTP. `ss -tanp | grep rousseau` muestra sockets solo salientes.
- [ ] **Allowlist de egreso.** Aplica nftables o Cloudflare Zero-Trust por fuera del contenedor. Permite solo:
  - El proveedor de LLM (`api.anthropic.com`, `bedrock-runtime.<region>.amazonaws.com`, `us-east1-aiplatform.googleapis.com`, etc.).
  - El transporte (`web.whatsapp.com`, `mtproto.telegram.org`, homeserver de matrix, Slack `wss-*`).
- [ ] **Resolutor DNS bloqueado.** Opcionalmente, ejecuta un `unbound` en un contenedor adyacente que solo resuelva los nombres de la allowlist.

### 4. Política de aprobación

- [ ] **`mode: pattern` para cada demonio desatendido.** Verifica `agent.approver.mode: pattern` en la config de cada servicio de transporte.
- [ ] **`default: deny`.** Ninguna llamada sin coincidencia pasa.
- [ ] **Lista deny de `bash`.** `rm\s+-rf`, `sudo`, `curl`, `wget`, `chmod`, `chown`, `nc`, `ncat`. Consulta [Tutorial: endurecer el approver](/es/tutorials/harden-approver-policy/).
- [ ] **Restricción de ruta para `write` / `edit`.** La regex restringe las escrituras a `/workspace/...`.
- [ ] **Configuración en control de código.** El YAML del approver es código — revísalo en PR.

### 5. Manejo de secretos

- [ ] **Sin API keys en `config.yaml`.** Almacena los secretos en un `EnvironmentFile=` de `systemd` (`chmod 0600`) o en el gestor de secretos de la organización.
- [ ] **`ANTHROPIC_API_KEY` canalizada vía env.** `config.Load` (`internal/config/config.go`) la recoge.
- [ ] **IRSA de Bedrock / ADC de Vertex.** Prefiere federación de identidad sobre API keys de larga duración.
- [ ] **Cadencia de rotación.** 90 días o lo que exija tu política. Rousseau no cachea credenciales — una clave rotada se recoge en el siguiente reinicio del demonio.

### 6. Datos en reposo

- [ ] **Cifrado de `sessions.db`.** Cifrado de disco completo (LUKS en Linux, FileVault en macOS, volúmenes EBS cifrados en AWS). Rousseau no implementa cifrado a nivel de aplicación sobre el store de sesiones.
- [ ] **Backups cifrados.** Restic o borg cifran ambos en reposo con una clave que tú controlas.
- [ ] **Política de retención.** Borra masivamente sesiones con más de `N` días — consulta [Guías: gestión de sesiones](/es/guides/session-management/) para el SQL.
- [ ] **Manejo del JID map.** La tabla `jid_sessions` mapea números de teléfono a IDs de sesión. Trátala como PII.

### 7. Logs y auditoría

- [ ] **`log.format: json`.** Salida parseable por máquina.
- [ ] **Envío de logs fuera del host.** Vector / Promtail / Datadog. Consulta [Guías: observabilidad](/es/guides/observability/).
- [ ] **Retención.** Mínimo 90 días en cold storage. El registro de auditoría de rousseau está enteramente en slog; tú lo haces duradero.
- [ ] **Alertas sobre `tool.denied`.** Alerta ante cualquier denegación — puede ser benigna o un intento de inyección.
- [ ] **Alertas sobre `whatsapp.logged_out`.** Un incumplimiento de política de Meta significa que la cuenta está fuera de servicio.

### 8. Gestión del cambio

- [ ] **Los cambios de configuración son código.** Revisados por PR, versionados en git.
- [ ] **Los bumps de imagen son deliberados.** `AutoUpdate=disabled` en la unidad Quadlet es intencional.
- [ ] **Plan de rollback.** Mantén la imagen anterior etiquetada y disponible. `podman tag localhost/rousseau-agent:local rousseau-agent:previous` antes de cada build.

### 9. Respuesta a incidentes

- [ ] **Turno de guardia.** Alguien puede ejecutar `systemctl --user stop rousseau-agent` dentro de tu SLO de MTTR.
- [ ] **Playbook de compromiso.** Pasos para: revocar la API key del LLM, revocar el token del transporte (por ejemplo, reinstalación del bot de Slack), snapshot del store de sesiones, imagen del sistema de archivos del contenedor, desvincular el dispositivo de WhatsApp.
- [ ] **Canal de divulgación de seguridad.** Lee `SECURITY.md` en el repositorio rousseau-agent para la dirección de divulgación coordinada.
- [ ] **SLO para arreglos de seguridad.** Rastrea CVEs contra la versión fijada de rousseau. `govulncheck` en `make check` detecta issues conocidos de la stdlib de Go y de dependencias.

### 10. Mapeo de cumplimiento

- [ ] **Evidencia SOC 2.** Procedencia SLSA-3 + cosign + SBOM cubre CC7.1 (operaciones del sistema). Los logs del approver cubren CC7.2.
- [ ] **ISO 27001 A.12 Operations Security.** Políticas de aprobación + scoping de workspace + logs de auditoría.
- [ ] **OWASP LLM Top-10.** Rousseau no atesta el LLM Top-10 hoy — está en la hoja de ruta. Documenta tus controles compensatorios (approver + contenedor) en tu auditoría.

## Plantilla de aprobación

Lo siguiente es una plantilla ligera que tu equipo de plataforma puede copiar en un runbook:

```
Aprobación de despliegue de rousseau-agent
==========================================
Versión: <tag>            (verificada vía cosign / SLSA verifier)
Proveedor: <anthropic|bedrock|vertex|openai>
Transportes habilitados: <lista>
Modo del approver: pattern
Default del approver: deny
Destino de logs: <Loki / Datadog / etc>
Destino de backups: <s3://... / restic repo>
Guardia: <equipo>
Divulgación de seguridad: <dirección interna>
```

## Relacionado

- [Seguridad](/es/security/) — las fronteras de confianza que protege esta checklist.
- [Despliegue](/es/deployment/) — la unidad Quadlet.
- [Tutorial: desplegar en un VPS](/es/tutorials/deploy-to-a-vps/) — ejemplo trabajado.
- [Guías: despliegue en producción](/es/guides/production-deployment/) — detalles operativos.
