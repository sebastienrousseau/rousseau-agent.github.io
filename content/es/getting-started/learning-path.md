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
description: "Recommended reading order for new rousseau-agent users, split by role: individual developer, platform operator, security reviewer."
keywords: "learning path, reading order, docs guide, individual developer, platform operator, security reviewer"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/getting-started/learning-path/"
subtitle: "What to read first, split by role."
tags: "learning-path, reading-order"
title: "Ruta de aprendizaje"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "learning path, reading order, docs guide, individual developer, platform operator, security reviewer"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Ruta de aprendizaje"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 22
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/learning-path/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/learning-path/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Ruta de aprendizaje"
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
twitter_description: "Recommended reading order for new rousseau-agent users, split by role: individual developer, platform operator, security reviewer."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Ruta de aprendizaje"
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

## Elige tu rol

La audiencia de Rousseau se divide claramente en tres ejes. Elige el que coincida con tu objetivo y lee en orden: cada ruta asume que la sección anterior ya fue asimilada.

## Desarrollador individual

Quieres un asistente de codificación en tu propia laptop que persista sesiones y controle tu CLI `claude` existente. Sin equipo, sin despliegue compartido.

| # | Página | Por qué |
|---|---|---|
| 1 | [Primeros pasos](/es/getting-started/) | Instalación, `rousseau chat`, recorrido de primer uso. |
| 2 | [Conceptos](/es/concepts/) | Comprende el bucle del agente y el almacén de sesiones antes de personalizar cualquier cosa. |
| 3 | [Guía de usuario: CLI](/es/user-guide/cli/) | Cada comando, cada opción. |
| 4 | [Guía de usuario: TUI](/es/user-guide/tui/) | Atajos de teclado y semántica de paneles. |
| 5 | [Guía de usuario: Herramientas](/es/user-guide/tools/) | Qué hacen y qué no hacen las cinco herramientas integradas. |
| 6 | [Configuración](/es/configuration/) | Ajusta las piezas que tocaste. |
| 7 | [Skills](/es/skills/) | Crea fragmentos de prompt reutilizables. |

Omite todo lo que está bajo [Guía del desarrollador](/es/developer-guide/) salvo que planees integrar el bucle del agente en otro binario.

## Operador de plataforma

Estás ejecutando rousseau para un equipo detrás de un perímetro corporativo. El tiempo de actividad, la auditabilidad y la postura de menor privilegio son críticos.

| # | Página | Por qué |
|---|---|---|
| 1 | [Primeros pasos](/es/getting-started/) | Instalar y probar. |
| 2 | [Plataformas admitidas](/es/getting-started/platform-support/) | Confirma cada versión de dependencia. |
| 3 | [Conceptos](/es/concepts/) | Arquitectura por capas: en qué puedes confiar que se mantenga estable entre versiones. |
| 4 | [Despliegue](/es/deployment/) | Podman rootless + Quadlet. Nota sobre Kubernetes. |
| 5 | [Guías: Despliegue en Kubernetes](/es/guides/kubernetes-deployment/) | Si Kubernetes es tu objetivo. |
| 6 | [Configuración](/es/configuration/) + [Referencia: Esquema de configuración](/es/reference/config-schema/) | Cada perilla, estructurada. |
| 7 | [Guía de usuario: Políticas de aprobación](/es/user-guide/approval-policies/) | La historia de aprobación de llamadas a herramientas que presentas a los auditores. |
| 8 | [Guías: Observabilidad](/es/guides/observability/) | Conecta la salida de slog a tu canalización de logs. |
| 9 | [Guías: Auditoría + Políticas de aprobación](/es/guides/audit-approval-policies/) | Configuración probada de modo por patrones con reglas de denegación. |
| 10 | [Actualización](/es/getting-started/updating/) | Moverse entre versiones de forma segura. |

## Revisor de seguridad

Estás evaluando rousseau antes del despliegue, o respondiendo un cuestionario de proveedor en nombre de tu equipo.

| # | Página | Por qué |
|---|---|---|
| 1 | [Seguridad](/es/security/) | Modelo de confianza, postura de cadena de suministro, inventario criptográfico. |
| 2 | [Instalación](/es/getting-started/installation/) | Receta de verificación cosign + SHA-256. |
| 3 | [Conceptos](/es/concepts/) | Arquitectura por capas: dónde viven las fronteras de confianza. |
| 4 | [Guía de usuario: Políticas de aprobación](/es/user-guide/approval-policies/) | La palanca entre el modelo y la shell. |
| 5 | [Guías: Modo de solo lectura](/es/guides/read-only-mode/) | Postura para un despliegue de inspección inicial. |
| 6 | [Referencia: Códigos de salida](/es/reference/exit-codes/) | Modos de falla expuestos a sistemas init y monitores. |
| 7 | [Privacidad](/es/privacy/) | Postura del flujo de datos. |
| 8 | [Despliegue](/es/deployment/) | Endurecimiento en tiempo de ejecución: flags de Podman, eliminación de capacidades, seccomp. |

## Lectura transversal

Todo lector se beneficia de estas una vez elegido su rol:

- [Solución de problemas](/es/troubleshooting/): cada diagnóstico al que puedes acceder con `rousseau doctor`.
- [Registro de cambios](/es/changelog/): qué se movió entre versiones.
- [MCP](/es/mcp/): cómo rousseau expone herramientas y sesiones a otros agentes.
- [Cron](/es/cron/): programa prompts en un reloj.

## Siguiente

- [Plataformas admitidas](/es/getting-started/platform-support/): qué se ejecuta dónde.
- [Primer transporte](/es/getting-started/first-transport/): recorrido probado con WhatsApp.
