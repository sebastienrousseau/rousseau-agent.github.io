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
description: "Expose rousseau's session store and cron jobs to Claude Desktop as an MCP server that Claude can drive from its own tool interface."
keywords: "mcp, claude desktop, stdio, tools, rousseau_search_sessions, rousseau_read_session"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/tutorials/expose-tools-via-mcp/"
subtitle: "Wire rousseau mcp into Claude Desktop and let it query the session store."
tags: "tutorials, mcp, claude-desktop, stdio, sessions"
title: "Tutorial: expor ferramentas via MCP"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, claude desktop, stdio, tools, rousseau_search_sessions, rousseau_read_session"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorial: expor ferramentas via MCP"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/expose-tools-via-mcp/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/expose-tools-via-mcp/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorial: expor ferramentas via MCP"
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
twitter_description: "Expose rousseau's session store and cron jobs to Claude Desktop as an MCP server that Claude can drive from its own tool interface."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorial: expor ferramentas via MCP"
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

## O que você constrói

Claude Desktop com rousseau como um servidor MCP stdio. De dentro de um chat do Claude Desktop você pode pedir "find the session where we discussed the retry logic" e o Claude chamará `rousseau_search_sessions`, depois `rousseau_read_session` para pegar o transcript completo.

Tempo estimado: 5 minutos.

## Pré-requisitos

- Claude Desktop instalado (macOS ou Windows). Linux usa o Claude CLI, não Desktop — veja a alternativa no final.
- Rousseau instalado e no `$PATH`.
- Algum histórico de sessão existente em `~/.local/share/rousseau/sessions.db` — rode `rousseau chat` algumas vezes se o arquivo estiver vazio.

## Passo 1: entenda o que fica exposto

`rousseau mcp` (`internal/cli/mcp.go`) inicia um servidor stdio JSON-RPC que fala o Model Context Protocol. `RegisterRousseauTools` (`internal/mcp/tools.go`) anexa quatro ferramentas somente leitura:

| Ferramenta | Propósito |
|---|---|
| `rousseau_search_sessions` | Busca full-text FTS5 em cada sessão registrada (via `internal/state/sqlite/search.go`). |
| `rousseau_list_sessions` | Lista sessões mais recente primeiro. |
| `rousseau_read_session` | Retorna o transcript completo de uma sessão por id. |
| `rousseau_cron_list` | Lista os jobs de cron agendados do rousseau. |

Não há ferramentas de escrita; hosts MCP podem navegar mas não mutar. Veja [MCP: Ferramentas expostas](/pt-BR/mcp/exposed-tools/) para os schemas de entrada exatos.

## Passo 2: conecte o Claude Desktop

O Claude Desktop lê `claude_desktop_config.json`:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Adicione uma entrada `mcpServers` apontando para seu binário `rousseau`:

```json
{
  "mcpServers": {
    "rousseau": {
      "command": "/usr/local/bin/rousseau",
      "args": ["mcp"]
    }
  }
}
```

Reinicie o Claude Desktop.

## Passo 3: verifique

Abra um chat do Claude Desktop e verifique que as ferramentas aparecem no picker de ferramentas. Você deve ver quatro ferramentas prefixadas com `rousseau_`. Tente:

```
Use rousseau_list_sessions to show me my 5 most recent sessions,
then read the top one with rousseau_read_session.
```

O Claude invocará ambas as ferramentas, e o servidor MCP do rousseau (`internal/mcp/server.go`) tratará cada envelope JSON-RPC via stdin/stdout. Por baixo dos panos:

1. O Claude Desktop chama `initialize`, depois `tools/list` — o rousseau responde com as quatro ferramentas declaradas em ordem de inserção.
2. O Claude escolhe uma ferramenta e chama `tools/call` com os argumentos — o handler do rousseau (de `internal/mcp/tools.go`) consulta o SQLite e retorna conteúdo textual.
3. Em erro, o rousseau expõe o erro pelo canal de conteúdo (`isError=true`), nunca como erro JSON-RPC — hosts MCP esperam isso.

## Passo 4: (opcional) anexar ao Claude CLI / outro host MCP

O protocolo stdio é agnóstico de host. Para o Claude CLI:

```sh
claude --mcp-config <(cat <<'JSON'
{ "mcpServers": { "rousseau": { "command": "rousseau", "args": ["mcp"] } } }
JSON
)
```

Para Continue.dev, Codeium ou outro host MCP, siga o fluxo de registro de servidor MCP deles com `command: rousseau`, `args: [mcp]`. Veja [MCP: Compatibilidade](/pt-BR/mcp/compatibility/) para os clientes testados.

## Passo 5: cheat-sheet de sintaxe FTS5

Como rousseau_search_sessions é um wrapper fino sobre SQLite FTS5 (`internal/state/sqlite/search.go`), o campo de query suporta:

| Query | Significado |
|---|---|
| `retry logic` | Qualquer doc contendo ambos os termos. |
| `"retry logic"` | Frase exata. |
| `retr*` | Match por prefixo. |
| `retry OR backoff` | OR boolean. |
| `retry NOT retries` | Exclusão. |

O ranqueamento usa BM25 (rank menor = mais relevante); a chamada `snippet()` em `Search` te dá um preview de 200 caracteres por hit.

## Solução de problemas

- **"unknown tool" no Claude Desktop.** Reinicie o app. A lista de ferramentas só é buscada no início da sessão.
- **Servidor sai imediatamente.** `rousseau mcp` abre o arquivo de estado SQLite; se o caminho em `state.path` não for gravável, `Open()` falha e o processo sai com código não-zero. Rode a partir de um shell para ver o erro.
- **Resultados de busca vazios.** Confirme que o índice FTS5 está populado: `sqlite3 ~/.local/share/rousseau/sessions.db "SELECT count(*) FROM sessions_fts"`. `EnsureSearch` em `internal/state/sqlite/search.go` back-fila o índice em cada open, mas um arquivo de estado corrompido pode precisar de rebuild manual.

## Relacionado

- [MCP](/pt-BR/mcp/) — o doc de referência.
- [MCP: Ferramentas expostas](/pt-BR/mcp/exposed-tools/) — cada schema de ferramenta.
- [MCP: Compatibilidade](/pt-BR/mcp/compatibility/) — clientes testados.
- [Referência: Session store](/pt-BR/reference/session-store/) — o schema SQLite por trás das ferramentas.
