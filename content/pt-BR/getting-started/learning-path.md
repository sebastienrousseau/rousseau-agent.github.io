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
description: "Recommended reading order for new rousseau-agent users, split by role: individual developer, platform operator, security reviewer."
keywords: "learning path, reading order, docs guide, individual developer, platform operator, security reviewer"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/getting-started/learning-path/"
subtitle: "What to read first, split by role."
tags: "learning-path, reading-order"
title: "Trilha de aprendizado"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "learning path, reading order, docs guide, individual developer, platform operator, security reviewer"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Trilha de aprendizado"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 22
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/learning-path/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/learning-path/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Trilha de aprendizado"
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
twitter_title: "Trilha de aprendizado"
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

## Escolha seu papel

O público do rousseau se divide de forma limpa em três eixos. Escolha aquele que combina com seu objetivo e leia em ordem — cada caminho assume que a seção anterior foi absorvida.

## Desenvolvedor individual

Você quer um assistente de codificação no seu próprio laptop que persista sessões e acione sua CLI `claude` existente. Sem time, sem implantação compartilhada.

| # | Página | Por quê |
|---|---|---|
| 1 | [Começando](/pt-BR/getting-started/) | Instalação, `rousseau chat`, walkthrough da primeira execução. |
| 2 | [Conceitos](/pt-BR/concepts/) | Entenda o loop do agente e o armazenamento de sessão antes de customizar qualquer coisa. |
| 3 | [Guia do usuário: CLI](/pt-BR/user-guide/cli/) | Cada comando, cada flag. |
| 4 | [Guia do usuário: TUI](/pt-BR/user-guide/tui/) | Keybindings e semântica de painéis. |
| 5 | [Guia do usuário: Tools](/pt-BR/user-guide/tools/) | O que as cinco tools embutidas fazem e o que não fazem. |
| 6 | [Configuração](/pt-BR/configuration/) | Ajuste as peças que você tocou. |
| 7 | [Skills](/pt-BR/skills/) | Escreva fragmentos de prompt reutilizáveis. |

Pule tudo sob [Guia do desenvolvedor](/pt-BR/developer-guide/) a menos que planeje embutir o loop do agente em outro binário.

## Operador de plataforma

Você está rodando o rousseau para um time atrás de um perímetro corporativo. Uptime, auditabilidade e postura de menor privilégio são críticos.

| # | Página | Por quê |
|---|---|---|
| 1 | [Começando](/pt-BR/getting-started/) | Instalação e smoke test. |
| 2 | [Suporte de plataforma](/pt-BR/getting-started/platform-support/) | Confirme cada versão de dependência. |
| 3 | [Conceitos](/pt-BR/concepts/) | Arquitetura em camadas — no que você pode confiar para permanecer estável entre releases. |
| 4 | [Implantação](/pt-BR/deployment/) | Podman rootless + Quadlet. Nota sobre Kubernetes. |
| 5 | [Guias: Implantação no Kubernetes](/pt-BR/guides/kubernetes-deployment/) | Se Kubernetes é seu alvo. |
| 6 | [Configuração](/pt-BR/configuration/) + [Referência: Schema de config](/pt-BR/reference/config-schema/) | Cada botão, estruturado. |
| 7 | [Guia do usuário: Políticas de aprovação](/pt-BR/user-guide/approval-policies/) | A história de aprovação de tool calls que você apresenta aos auditores. |
| 8 | [Guias: Observabilidade](/pt-BR/guides/observability/) | Conecte a saída slog ao seu pipeline de logs. |
| 9 | [Guias: Auditoria + Políticas de aprovação](/pt-BR/guides/audit-approval-policies/) | Config em modo pattern trabalhada com regras de negação. |
| 10 | [Atualizando](/pt-BR/getting-started/updating/) | Mude entre versões com segurança. |

## Revisor de segurança

Você está avaliando o rousseau antes do rollout, ou respondendo um questionário de fornecedor em nome do seu time.

| # | Página | Por quê |
|---|---|---|
| 1 | [Segurança](/pt-BR/security/) | Modelo de confiança, postura de cadeia de suprimentos, inventário de criptografia. |
| 2 | [Instalação](/pt-BR/getting-started/installation/) | Receita de verificação cosign + SHA-256. |
| 3 | [Conceitos](/pt-BR/concepts/) | Arquitetura em camadas — onde ficam os limites de confiança. |
| 4 | [Guia do usuário: Políticas de aprovação](/pt-BR/user-guide/approval-policies/) | A alavanca entre o modelo e o shell. |
| 5 | [Guias: Modo somente leitura](/pt-BR/guides/read-only-mode/) | Postura para uma implantação de inspeção inicial. |
| 6 | [Referência: Códigos de saída](/pt-BR/reference/exit-codes/) | Modos de falha expostos a sistemas init e monitores. |
| 7 | [Privacidade](/pt-BR/privacy/) | Postura de fluxo de dados. |
| 8 | [Implantação](/pt-BR/deployment/) | Endurecimento de runtime — flags do Podman, descarte de capabilities, seccomp. |

## Leitura transversal

Todo leitor se beneficia disso depois de escolher um papel:

- [Solução de problemas](/pt-BR/troubleshooting/) — cada diagnóstico que você pode alcançar com `rousseau doctor`.
- [Changelog](/pt-BR/changelog/) — o que mudou entre releases.
- [MCP](/pt-BR/mcp/) — como o rousseau expõe ferramentas e sessões para outros agentes.
- [Cron](/pt-BR/cron/) — agende prompts com relógio.

## Próximo

- [Suporte de plataforma](/pt-BR/getting-started/platform-support/) — o que roda onde.
- [Primeiro transporte](/pt-BR/getting-started/first-transport/) — walkthrough trabalhado de WhatsApp.
