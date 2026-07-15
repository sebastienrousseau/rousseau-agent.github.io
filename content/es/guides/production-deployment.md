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
description: "Beyond the Quadlet reference: log shipping, session-store backup, health checks, rolling restarts, and multi-transport coexistence."
keywords: "production, log shipping, backup, health check, rolling restart, systemd"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/guides/production-deployment/"
subtitle: "Everything the Quadlet reference doesn't already cover."
tags: "guides, production, deployment, backup, logs, health check"
title: "Guía: despliegue en producción"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "production, log shipping, backup, health check, rolling restart, systemd"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guía: despliegue en producción"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/production-deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/production-deployment/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guía: despliegue en producción"
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
twitter_description: "Beyond the Quadlet reference: log shipping, session-store backup, health checks, rolling restarts, and multi-transport coexistence."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guía: despliegue en producción"
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

## Lee esto después

La unidad Quadlet de referencia en `docker/rousseau-agent.container` cubre la historia de "cómo ejecutar rousseau". Esta guía cubre lo que añades alrededor antes de llamarlo producción: logs, backups, salud e higiene de proceso.

## Envío de logs

Rousseau escribe logs estructurados a stderr vía `log/slog` (`internal/cli/root.go`). Cuando lo ejecutas bajo systemd, ese stderr cae en el journal. Opciones para enviar fuera del host:

| Herramienta | Ajuste | Notas |
|---|---|---|
| Vector (`vector.dev`) | Mejor default. | Fuente `journald` + un filtro que descarte DEBUG. Envía a Loki, Datadog, S3, lo que sea. |
| Promtail + Loki | Si ya ejecutas Grafana. | La fuente `journal` de Loki funciona directamente contra `journalctl -o json`. |
| Datadog Agent | Si Datadog es el estándar de la organización. | El agente DD tiene un tail de journald. El JSON estructurado se parsea nativamente. |
| Fluent Bit | Alternativa de huella pequeña. | Establece `log.format: json` en `config.yaml`; la entrada `systemd` de Fluent Bit parsea. |

Configura `log.format: json` (`internal/config/config.go` `LogConfig.Format`) incondicionalmente en producción. La salida de texto está diseñada para `less`, no para parseo por máquina.

Consulta [Guías: Observabilidad](/es/guides/observability/) para una receta completa de pipeline de Loki.

## Backup del almacén de sesiones

El directorio de estado `~/.local/share/rousseau/` es el único estado durable que rousseau posee. Hazle backup cada noche.

Dos enfoques:

**1. SQLite `.backup` (recomendado).**

```sh
sqlite3 ~/.local/share/rousseau/sessions.db \
  ".backup '/backup/sessions.db.$(date +%Y%m%d).bak'"
sqlite3 ~/.local/share/rousseau/whatsapp.db \
  ".backup '/backup/whatsapp.db.$(date +%Y%m%d).bak'"
restic backup /backup
```

`.backup` usa la API online de SQLite: seguro incluso mientras el daemon está escribiendo. Consulta [Referencia: Almacén de sesiones](/es/reference/session-store/).

**2. Snapshot de sistema de archivos.**

Como el journaling WAL está activado (`Open()` en `internal/state/sqlite/store.go`), `restic` y `borg` pueden hacer snapshot de los archivos crudos mientras el daemon se ejecuta. WAL garantiza una imagen consistente en un punto en el tiempo.

No:

- Copies el archivo `.db` con `cp` mientras el daemon se ejecuta salvo que también copies `-wal` y `-shm`.
- Guardes backups en el mismo disco.
- Omitas el archivo de credenciales del dispositivo de WhatsApp: perderlo significa volver a escanear el QR.

## Chequeos de salud

`rousseau status` (`internal/cli/status.go`) sale con 0 en sano, distinto de cero en problemas. Úsalo como probe de salud de systemd:

```ini
[Service]
ExecStartPost=/usr/bin/timeout 30 podman exec rousseau-agent rousseau status
```

Para un probe más rico, escribe un chequeo que:

1. Ejecute `rousseau status`.
2. Confirme que la última escritura del almacén de sesiones fue reciente (`stat sessions.db -c %Y` comparado con ahora).
3. Chequee el uptime del contenedor vía `podman inspect`.

Rousseau no expone un `/healthz` HTTP. Si tu plataforma requiere uno (readiness probes de Kubernetes), consulta [Guías: Despliegue en Kubernetes](/es/guides/kubernetes-deployment/): envuelves rousseau en un pequeño sidecar amigable con `curl`.

## Reinicio rolling

Como el estado es un único archivo SQLite, el daemon es genuinamente de instancia única. Un reinicio rolling es: detener, reemplazar imagen, iniciar. No se requiere calentamiento.

```sh
podman pull localhost/rousseau-agent:local     # o reconstruye localmente
systemctl --user restart rousseau-agent
podman logs -n 50 rousseau-agent | grep -E 'starting|connected'
```

Secuencia de log esperada (de `internal/transport/whatsapp/client.go`):

```
INFO whatsapp.starting store=… allowlist=1
INFO whatsapp.connected
```

Si el daemon no emite `whatsapp.connected` dentro de ~15 segundos, revierte.

## Múltiples transportes en un host

Puedes querer el mismo almacén de sesiones compartido por WhatsApp y Slack. Dos formas:

- **Múltiples unidades Quadlet**: una por cada transporte, cada una apuntando al mismo `state.path`. WAL + `busy_timeout` (consulta `Open()` en `internal/state/sqlite/store.go`) hacen que los escritores concurrentes sean seguros.
- **Un binario, un transporte por invocación.** Los comandos de transporte de rousseau son de un solo transporte (`whatsapp`, `slack`, `signal`, …). Para ejecutar dos transportes, ejecutas dos procesos.

## Cambios de configuración sin downtime

Rousseau no hace hot-reload de `config.yaml`. Los cambios de configuración requieren un reinicio. `SIGHUP` no está cableado para recarga.

Flujo práctico:

1. Edita `~/.config/rousseau/config.yaml`.
2. `systemctl --user restart rousseau-agent`.
3. Verifica desde los logs.

Para la mayoría de transportes la reconexión es rápida (~1-3 segundos). La pausa principal es en WhatsApp, donde whatsmeow restablece el websocket.

## Retención de logs

La retención de `journald` la establece `SystemMaxUse=` en `/etc/systemd/journald.conf`. Para un despliegue amigable con auditoría, envía logs fuera del host y establece journald a una retención más corta en el disco local (p. ej. 7 días) para que el rastro de auditoría viva en Loki/S3, no en un sistema de archivos que un intruso podría rotar.

## Ciclo de vida de la imagen de contenedor

Reconstruye la imagen en cada release de rousseau que quieras adoptar:

```sh
cd ~/rousseau-agent
git pull
podman build -t rousseau-agent:local -f docker/Dockerfile .
systemctl --user restart rousseau-agent
```

La línea Quadlet `AutoUpdate=disabled` (en `docker/rousseau-agent.container`) impide que `podman auto-update` toque el contenedor. Tú controlas la cadencia de actualización.

## Relacionado

- [Despliegue](/es/deployment/): la unidad Quadlet de referencia.
- [Tutorial: Desplegar en un VPS](/es/tutorials/deploy-to-a-vps/): ejemplo probado.
- [Guías: Observabilidad](/es/guides/observability/): pipeline de logs.
- [Guías: Onboarding empresarial](/es/guides/enterprise-onboarding/): lista de verificación completa.
