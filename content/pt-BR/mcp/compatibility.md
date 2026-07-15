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
description: "MCP clients tested against rousseau's stdio server: Claude Desktop, Claude CLI, Continue, Codeium, plus setup snippets."
keywords: "mcp, compatibility, claude desktop, continue, codeium, stdio, claude_desktop_config"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/mcp/compatibility/"
subtitle: "Which MCP clients talk to rousseau's stdio server."
tags: "mcp, compatibility, claude, continue, stdio"
title: "MCP: compatibilidade"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, compatibility, claude desktop, continue, codeium, stdio, claude_desktop_config"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP: compatibilidade"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "mcp"
order: 71
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/mcp/compatibility/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/compatibility/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "MCP: compatibilidade"
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
twitter_description: "MCP clients tested against rousseau's stdio server: Claude Desktop, Claude CLI, Continue, Codeium, plus setup snippets."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP: compatibilidade"
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

## O contrato do protocolo

O servidor MCP do rousseau (`internal/mcp/server.go`) fala JSON-RPC 2.0 sobre stdio e anuncia as ferramentas declaradas em `internal/mcp/tools.go`. Ele lida com esses métodos:

- `initialize` — retorna `ServerCapabilities.Tools`.
- `initialized` — notificação, sem resposta.
- `ping` — retorna `{}`.
- `tools/list` — retorna as quatro ferramentas em ordem de inserção.
- `tools/call` — invoca um handler de ferramenta, retorna `ToolsCallResult` com `content` e `isError`.
- `resources/list`, `prompts/list` — retornam arrays vazios (veja notas de roadmap abaixo).
- `shutdown` — retorna `{}`.

Qualquer host MCP que fale JSON-RPC via stdio e chame os quatro métodos acima é compatível.

## Clientes testados

| Cliente | Status | Como registrar |
|---|---|---|
| Claude Desktop (macOS / Windows) | Funciona. | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) ou `%APPDATA%\Claude\claude_desktop_config.json` (Windows). |
| Claude CLI (`claude`) | Funciona. | `--mcp-config <file>` ou um bloco `[mcp]` em `~/.claude/config.json`. |
| Continue.dev (VS Code / JetBrains) | Funciona. | Bloco `mcpServers` em `~/.continue/config.json`. |
| Codeium (extensões de IDE) | Funciona quando o Codeium expõe modo host MCP (releases recentes). Setup varia por IDE. |
| Cursor (versões recentes) | Funciona. Registre pela própria UI de settings MCP do Cursor. |
| Qualquer SDK de host MCP em Go / TypeScript / Python | Funciona. Instancie com `command: "rousseau", args: ["mcp"]`. |

Desconhecido / não testado mas provavelmente compatível: `zed`, `windsurf`, `aider`. Se seu host suporta a spec MCP stdio, o rousseau funcionará.

## Claude Desktop

Edite `claude_desktop_config.json` (caminho acima) e adicione:

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

Reinicie o Claude Desktop. As quatro ferramentas `rousseau_*` aparecem no picker de ferramentas na próxima sessão de chat.

Para estado por workspace, adicione um override de env:

```json
{
  "mcpServers": {
    "rousseau-work": {
      "command": "/usr/local/bin/rousseau",
      "args": ["--config", "/home/seb/.config/rousseau/work.yaml", "mcp"]
    }
  }
}
```

## Claude CLI

Aponte o CLI para uma config:

```sh
claude --mcp-config <(cat <<'JSON'
{
  "mcpServers": {
    "rousseau": {
      "command": "rousseau",
      "args": ["mcp"]
    }
  }
}
JSON
)
```

Ou coloque em `~/.claude/config.json` sob um bloco `mcpServers` usando a mesma forma.

## Continue.dev

Adicione a `~/.continue/config.json`:

```json
{
  "mcpServers": [
    {
      "name": "rousseau",
      "command": "rousseau",
      "args": ["mcp"]
    }
  ]
}
```

O Continue pega as ferramentas na próxima call de modelo.

## Cursor

O Cursor expõe registro MCP em Settings > MCP UI. Registre um novo servidor chamado `rousseau` com command `rousseau` e args `mcp`. Sem edição de arquivo de config necessária.

## Codeium

O suporte MCP do Codeium vem atrás de uma feature flag em versões recentes da extensão de IDE. Consulte os docs da extensão — o registro é novamente um par `command / args`.

## Variáveis de ambiente e segredos

Como a superfície MCP do rousseau é somente leitura sobre o session store, ela não precisa de credenciais de provider. `ANTHROPIC_API_KEY` e similares não são usadas por `rousseau mcp` — apenas pelos daemons de transporte / chat que _geram_ sessões.

## Problemas comuns

- **"Server exited immediately."** O comando `mcp` do rousseau abre `state.path`. Se o arquivo não é gravável, o processo sai com não-zero. Rode `rousseau mcp` de um shell para ver o erro exato.
- **"Unknown tool: rousseau_search_sessions."** O host cacheou uma lista de ferramentas antiga. Reinicie o host.
- **Registro duplicado.** Se dois servidores rousseau estão registrados com o mesmo nome, apenas o último vence.

## Resources e prompts

`resources/list` e `prompts/list` atualmente retornam vazio. A página [Resources expostos](/pt-BR/mcp/exposed-resources/) rastreia o roadmap para expor sessões como resources MCP.

## Relacionado

- [MCP](/pt-BR/mcp/) — a referência guarda-chuva.
- [MCP: Ferramentas expostas](/pt-BR/mcp/exposed-tools/) — cada assinatura de ferramenta.
- [MCP: Resources expostos](/pt-BR/mcp/exposed-resources/) — roadmap.
- [Tutorial: Expor ferramentas via MCP](/pt-BR/tutorials/expose-tools-via-mcp/) — exemplo trabalhado.
