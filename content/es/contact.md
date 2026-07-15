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
description: "Support routing for rousseau-agent. GitHub issues for bugs and features. sebastian.rousseau@gmail.com for security reports."
keywords: "contact, support, GitHub issues, security disclosure, email"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/contact/"
subtitle: "Dónde reportar bugs, funcionalidades e informes de seguridad."
tags: "contact, support"
title: "Contacto"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "contact, support, GitHub issues, security disclosure, email"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Contacto"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "support"
order: 29
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/contact/index.html"
item_link: "https://docs.rousseau-agent.dev/contact/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Contacto"
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
twitter_description: "Support routing for rousseau-agent. GitHub issues for bugs and features. sebastian.rousseau@gmail.com for security reports."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Contacto"
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

## Errores y funcionalidades

Abre una incidencia en https://github.com/sebastienrousseau/rousseau-agent/issues. Incluye:

- Salida de `rousseau version`.
- Versión de Go, sistema operativo y runtime de contenedores.
- Reproducción mínima — idealmente una prueba que falle.
- Extracto del log con `ROUSSEAU_LOG_LEVEL=debug`, con secretos redactados.

## Divulgación de seguridad

**No** abras una incidencia pública para reportes que afecten a la seguridad. Envía un correo a:

**sebastian.rousseau@gmail.com**

SLA de acuse de recibo: 72 horas. La tabla completa de SLA de divulgación está en la [página de seguridad](/es/security/).

Incluye un vector CVSS 3.1 si dispones de uno, el componente afectado (ruta de archivo y rango de líneas o módulo de dependencia), una reproducción mínima y cualquier calendario de divulgación coordinada que necesites respetar.

La política completa está en `SECURITY.md` en el repositorio de código fuente.

## Comercial / consultoría

`rousseau-agent` es un proyecto open-source con licencia MIT. No existe un nivel de soporte comercial. Los servicios de consultoría son ad hoc — contacta con el mantenedor en el correo indicado arriba.
