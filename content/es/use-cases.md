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
description: "Concrete deployment narratives for rousseau-agent: on-call SRE, mobile PR review, regulated-industry Bedrock deployment."
keywords: "use cases, narratives, on-call, sre, mobile review, whatsapp, bedrock, regulated"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/use-cases/"
subtitle: "Historias concretas — quién ejecuta rousseau y por qué."
tags: "use-cases, narratives"
title: "Casos de uso"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "use cases, narratives, on-call, sre, mobile review, whatsapp, bedrock, regulated"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Casos de uso"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 70
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/use-cases/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Casos de uso"
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
twitter_description: "Concrete deployment narratives for rousseau-agent: on-call SRE, mobile PR review, regulated-industry Bedrock deployment."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Casos de uso"
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

## Léelas cuando quieras una imagen, no un manual

Los casos de uso son narrativas cortas. Cada uno describe un operador plausible, el problema que enfrenta y la configuración exacta que usaría. Cada caso de uso es una página: lee el que coincida con tu situación.

| Caso de uso | Persona | Problema |
|---|---|---|
| [Compañero de guardia](/es/use-cases/oncall-buddy/) | SRE en solitario, empresa pequeña. | Aviso de Slack a las 3 a. m., triage antes de estar completamente despierto. |
| [Revisión de PR móvil](/es/use-cases/mobile-review/) | Desarrollador individual en un trayecto. | Revisar pull requests desde tu teléfono. |
| [Industria regulada](/es/use-cases/regulated-industry/) | Equipo de servicios financieros. | Agente de codificación dentro de una VPC alojada en Bedrock con aprobación en modo pattern. |

Estos son ilustrativos, no exhaustivos: el diseño de rousseau generaliza. Si tu situación se parece a uno de estos, comienza ahí.

## Qué tienen en común todos los casos de uso

- Un único binario Go en un contenedor rootless.
- Un transporte por instancia (un Slack, o un WhatsApp, o un Signal: elige uno).
- Un aprobador en modo `pattern` con reglas deny sensatas.
- Estado de sesión en SQLite, para que un reinicio no pierda la conversación.
- Sin plano de control SaaS, sin endpoint de telemetría, sin servidor de licencias.

## Qué varía

- **Proveedor**: `claudecli` para laptops individuales, `bedrock`/`vertex` para entornos regulados, compatible con `openai` para vLLM autohospedado.
- **Transporte**: elige el medio que los ingenieros ya usan.
- **Política de aprobación**: más estricta en entornos de alto riesgo; más laxa dentro de un contenedor bloqueado.
- **Superficie de despliegue**: laptop, Podman de un solo nodo, Kubernetes.

## Siguiente

- [Compañero de guardia](/es/use-cases/oncall-buddy/): la historia más común.
- [Revisión de PR móvil](/es/use-cases/mobile-review/): la razón por la que WhatsApp es el transporte de referencia.
- [Industria regulada](/es/use-cases/regulated-industry/): la historia empresarial.
