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
description: "MCP resources exposed by rousseau's stdio server today (none) and the roadmap for sessions-as-resources."
keywords: "mcp, resources, roadmap, sessions, resources/list"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/mcp/exposed-resources/"
subtitle: "What resources rousseau exposes today, and what is planned."
tags: "mcp, resources, roadmap"
title: "MCP: recursos expostos"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, resources, roadmap, sessions, resources/list"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP: recursos expostos"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "mcp"
order: 73
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/mcp/exposed-resources/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/exposed-resources/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "MCP: recursos expostos"
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
twitter_description: "MCP resources exposed by rousseau's stdio server today (none) and the roadmap for sessions-as-resources."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP: recursos expostos"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Obrigado a cada operador que executa seu próprio agente de codificação."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Status atual

O servidor MCP do rousseau (`internal/mcp/server.go`) declara apenas a capability `Tools`. Ele retorna uma lista vazia em `resources/list`:

```
MethodResourcesList → okResponse(env.ID, map[string]any{"resources": []any{}})
```

A intenção é deliberada. Todo caso de uso que se pareceria com um resource MCP — uma sessão salva, uma descrição de job de cron — é exposto hoje via uma ferramenta (`rousseau_read_session`, `rousseau_cron_list`) para que o host possa solicitar exatamente os dados que precisa, quando precisa, em vez de pré-listar cada sessão.

## Por que não resources hoje

Resources MCP brilham quando um host quer enumerar um conjunto modesto e bem definido de URIs (arquivos, páginas) e desreferenciá-los preguiçosamente. O session store do rousseau pode crescer para milhares de linhas; enumerar cada sessão em cada call `resources/list` explodiria o contexto do host. A superfície de ferramentas (search / list / read) é uma forma melhor para estado de alta cardinalidade.

## Roadmap

Dois candidatos que valem a pena expor como resources MCP, uma vez que a spec MCP suporte enumeração paginada de resources de forma robusta:

### Candidato: `rousseau://sessions/<id>`

Cada sessão do rousseau como um resource. URIs se pareceriam com:

```
rousseau://sessions/1a2b3c4d-…
```

O desreferenciamento retornaria o mesmo transcript que `rousseau_read_session` retorna hoje. Isso permitiria ao host anexar uma sessão específica a uma conversa como cidadã de primeira classe ("attach session 1a2b3c…", drag-and-drop), em vez de exigir que o modelo se lembre de chamar a ferramenta.

Gate: uma lista de resource precisaria ser paginada. Versões recentes da spec MCP propõem paginação baseada em cursor; uma vez que isso pouse e os hosts implementem, isso vira viável.

### Candidato: `rousseau://cron/<name>`

Cada job de cron como um resource. Inspeção somente leitura do prompt, agendamento, alvo de entrega e timestamp da última execução. Lista pequena — provavelmente seguro enumerar hoje, mas não vale a pena expor separadamente de `rousseau_cron_list` até que a forma de sessions-as-resources esteja provada.

## Capability de prompts

Similarmente não exposta hoje. `MethodPromptsList` retorna `{"prompts": []any{}}` em `internal/mcp/server.go` `dispatch`. O rousseau não tem uma biblioteca de prompts curada para expor; o mecanismo de skills (`internal/skills/skills.go`) é o conceito interno equivalente, e não é atualmente exposto via MCP.

Se o roadmap de skills convergir em prompts compartilháveis, expô-los como prompts MCP é o próximo passo natural. Veja [Skills](/pt-BR/skills/).

## Como contornar a lacuna hoje

Se seu host MCP requer resources para uma affordance específica de UI (por exemplo, drag-and-drop de uma sessão), a solução alternativa é:

1. Peça ao host para invocar `rousseau_list_sessions` no início do chat.
2. Copie o session id que você quer referenciar.
3. Invoque `rousseau_read_session` com aquele id.

Não é tão ergonômico quanto desreferenciamento nativo de resource, mas funcionalmente equivalente.

## Solicitando uma superfície de resource

Nem todo operador precisa de resources sobre MCP. Se seu time precisa, o caminho construtivo é abrir uma issue com:

- O host MCP específico com o qual você está integrando.
- A ação voltada ao usuário que seria mais agradável com resources.
- Expectativas aproximadas de tráfego (quantas sessões, com que frequência).

## Relacionado

- [MCP](/pt-BR/mcp/) — a referência guarda-chuva.
- [MCP: Ferramentas expostas](/pt-BR/mcp/exposed-tools/) — o que é exposto hoje.
- [MCP: Compatibilidade](/pt-BR/mcp/compatibility/) — clientes testados.
- [Skills](/pt-BR/skills/) — o conceito interno que pode virar prompts MCP.
