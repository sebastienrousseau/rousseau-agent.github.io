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
hreflang: "pt-BR"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "pt-BR"
locale: "pt_BR"
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
permalink: "https://docs.rousseau-agent.dev/pt-BR/use-cases/"
subtitle: "Histórias concretas — quem usa rousseau e por quê."
tags: "use-cases, narratives"
title: "Casos de uso"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "use cases, narratives, on-call, sre, mobile review, whatsapp, bedrock, regulated"
news_language: "pt-BR"
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
item_description: Feed RSS do rousseau-agent
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
thanks: "Obrigado a cada operador que executa seu próprio agente de codificação."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Leia estes quando quiser um panorama, não um manual

Use cases são narrativas curtas. Cada um descreve um operador plausível, o problema que ele enfrenta e a configuração exata que ele usaria. Cada use case cabe em uma página — leia o que combinar com sua situação.

| Use case | Persona | Problema |
|---|---|---|
| [Companheiro de on-call](/pt-BR/use-cases/oncall-buddy/) | SRE solo, empresa pequena. | Página no Slack às 3 da manhã, triagem antes de estar totalmente acordado. |
| [Revisão de PR pelo celular](/pt-BR/use-cases/mobile-review/) | Desenvolvedor individual no trajeto. | Revisar pull requests pelo celular. |
| [Setor regulado](/pt-BR/use-cases/regulated-industry/) | Time de serviços financeiros. | Agente de codificação dentro de uma VPC hospedada no Bedrock com aprovação em modo pattern. |

Isto é ilustrativo, não exaustivo — o design do rousseau generaliza. Se sua situação lembra uma dessas, comece por ela.

## O que cada use case tem em comum

- Um único binário Go em um contêiner rootless.
- Um transporte por instância (um Slack, ou um WhatsApp, ou um Signal — escolha um).
- Um approver em modo `pattern` com regras de negação sensatas.
- Estado de sessão em SQLite, então um restart não perde a conversa.
- Sem control plane SaaS, sem endpoint de telemetria, sem servidor de licenças.

## O que varia

- **Provider** — `claudecli` para laptops individuais, `bedrock`/`vertex` para ambientes regulados, compatível com `openai` para vLLM auto-hospedado.
- **Transporte** — escolha o meio que os engenheiros já usam.
- **Política de aprovação** — mais estrita em ambientes de alta aposta; mais frouxa dentro de um contêiner blindado.
- **Superfície de implantação** — laptop, Podman em nó único, Kubernetes.

## Próximo

- [Companheiro de on-call](/pt-BR/use-cases/oncall-buddy/) — a história mais comum.
- [Revisão de PR pelo celular](/pt-BR/use-cases/mobile-review/) — a razão pela qual o WhatsApp é o transporte de referência.
- [Setor regulado](/pt-BR/use-cases/regulated-industry/) — a história corporativa.
