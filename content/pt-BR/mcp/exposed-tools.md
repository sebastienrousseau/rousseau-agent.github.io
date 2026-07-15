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
description: "The exact tool signatures exposed by rousseau's stdio MCP server, mirroring internal/mcp/tools.go."
keywords: "mcp, rousseau_search_sessions, rousseau_list_sessions, rousseau_read_session, rousseau_cron_list"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/mcp/exposed-tools/"
subtitle: "Every tool rousseau's MCP server advertises, with schemas."
tags: "mcp, tools, sessions, cron"
title: "MCP: ferramentas expostas"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, rousseau_search_sessions, rousseau_list_sessions, rousseau_read_session, rousseau_cron_list"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP: ferramentas expostas"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "mcp"
order: 72
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/mcp/exposed-tools/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/exposed-tools/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "MCP: ferramentas expostas"
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
twitter_description: "The exact tool signatures exposed by rousseau's stdio MCP server, mirroring internal/mcp/tools.go."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP: ferramentas expostas"
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

## Registro

`internal/cli/mcp.go` abre o session store SQLite, constrói um `NewCronStore`, envolve ambos em `mcp.NewStoreBackend` e chama `mcp.RegisterRousseauTools(s, backend)`. As quatro ferramentas abaixo são anexadas em ordem de inserção — `tools/list` as retorna exatamente nessa ordem.

Cada ferramenta é somente leitura. Não há superfície de escrita sobre MCP hoje; isso é por design para que um host MCP não possa alterar o estado do rousseau.

## `rousseau_search_sessions`

**Descrição (exposta aos hosts):** _Busca full-text em cada sessão rousseau gravada. Usa a sintaxe FTS5 do SQLite (frases entre aspas duplas, AND/OR/NOT, wildcards de prefixo)._

**Input schema:**

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "FTS5 query"
    },
    "limit": {
      "type": "integer",
      "description": "Cap hits returned. Default 20."
    }
  },
  "required": ["query"]
}
```

**Comportamento.** Passa `query` verbatim para o motor FTS5 do SQLite (`Store.Search` em `internal/state/sqlite/search.go`). Resultados são ordenados por rank BM25 (menor = mais relevante). Cada hit renderiza como três linhas:

```
session <id> (rank 0.42)
    title:   <session title>
    snippet: <~200-char snippet with … ellipses>
```

**Erros.** Uma query vazia retorna `query is required`. Erros de sintaxe FTS5 sobem como erros do SQLite e aparecem via `isError: true`.

## `rousseau_list_sessions`

**Descrição (exposta aos hosts):** _Lista sessões rousseau, mais novas primeiro._

**Input schema:**

```json
{
  "type": "object",
  "properties": {
    "limit": {
      "type": "integer",
      "description": "Cap rows returned. Default 20."
    }
  }
}
```

**Comportamento.** Chama `Store.List` que usa o índice `idx_sessions_updated_at DESC`. Cada linha:

```
<session-id>  <title>  msgs=<count>  updated=<iso-8601>
```

Retorna `(no sessions)` quando o store está vazio.

## `rousseau_read_session`

**Descrição (exposta aos hosts):** _Retorna a transcrição completa de uma sessão rousseau por id._

**Input schema:**

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "description": "Session id"
    }
  },
  "required": ["id"]
}
```

**Comportamento.** Chama `Store.Load` para buscar a `agent.Session` completa. Renderiza como:

```
id: <session-id>
title: <session title>
created: <iso-8601>
updated: <iso-8601>
messages: <count>

[0] user
    <text content>
[1] assistant
    <text content>
    ...
```

Apenas conteúdo de texto é renderizado — blocos tool_use e blocos tool_result são omitidos na superfície MCP (o CLI `rousseau session show` os inclui; MCP intencionalmente não).

**Erros.** `id is required` em entrada vazia. `state.ErrNotFound` em id desconhecido.

## `rousseau_cron_list`

**Descrição (exposta aos hosts):** _Lista os jobs cron agendados do rousseau (nome, schedule, prompt, alvo de entrega)._

**Input schema:**

```json
{
  "type": "object",
  "properties": {}
}
```

**Comportamento.** Chama `CronStore.List` — uma linha por linha de `cron_jobs`:

```
<name> [<on|off>] <cron-expr> → <deliver-to>  prompt="<prompt>"  deliver=<deliver-to>
```

Retorna `(no jobs)` quando a tabela cron está vazia. Também retorna `(no jobs)` se o `CronStore` for nil no momento da construção (um caminho defensivo em `storeBackend.CronList`).

## O que NÃO é exposto

Omissões deliberadas:

| Superfície | Por que não |
|---|---|
| `rousseau_write_session` / `rousseau_delete_session` | Mutação via MCP deixaria um host não confiável remodelar a trilha de auditoria do rousseau. |
| `rousseau_add_cron` | Mesma razão — mutação. Adicione jobs cron via `rousseau cron add`. |
| As ferramentas embutidas (`read`, `write`, `edit`, `grep`, `bash`) | Estas são ferramentas voltadas ao agente, para o LLM dentro do loop do próprio rousseau, não voltadas ao host. Expô-las daria ao host MCP a capacidade de rodar shell no host que roda o rousseau — exatamente a inversão de confiança que não queremos. |
| Lookup do JID map | Expõe PII (números de telefone). Se você precisar, consulte o SQLite diretamente na máquina onde o daemon roda. |

## Superfície de erros

Handlers MCP retornam `([]Content, error)`. Em erro, o servidor (`internal/mcp/server.go` `handleToolsCall`) traz o erro como `ToolsCallResult{Content: text of err, IsError: true}`. Isso segue a convenção do MCP: falhas de tool fluem pelo canal de conteúdo com `isError=true`, não pelo canal `error` do JSON-RPC. Os hosts devem renderizar o texto e continuar.

## Relacionados

- [MCP](/pt-BR/mcp/) — a referência guarda-chuva.
- [MCP: Compatibilidade](/pt-BR/mcp/compatibility/) — clientes testados.
- [MCP: Recursos expostos](/pt-BR/mcp/exposed-resources/) — roadmap.
- [Referência: Schemas de tool](/pt-BR/reference/tool-schemas/) — o conjunto diferente de ferramentas voltadas ao agente.
