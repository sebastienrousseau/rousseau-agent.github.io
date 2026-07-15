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
description: "Architecture overview of rousseau-agent: agent loop, transport interface, tool registry, approval policies, SQLite session store, MCP server, cron scheduler, skills loader."
keywords: "architecture, agent loop, session, transport, tool registry, approval, MCP, cron, skills, compression, FTS5"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/concepts/"
subtitle: "Como o loop do agente, os transportes e o armazenamento de sessões se encaixam."
tags: "architecture, agent, session, mcp"
title: "Conceitos"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "architecture, agent loop, session, transport, tool registry, approval, MCP, cron, skills, compression, FTS5"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Conceitos"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "concepts"
order: 3
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/concepts/index.html"
item_link: "https://docs.rousseau-agent.dev/concepts/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Conceitos"
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
twitter_description: "Architecture overview of rousseau-agent: agent loop, transport interface, tool registry, approval policies, SQLite session store, MCP server, cron scheduler, skills loader."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Conceitos"
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

## Arquitetura em camadas

```
+---------------------------------------------------------------+
|                             CLI                              |
|  chat  whatsapp  slack  discord  ...  mcp  cron  skills      |
+-------------------------+-------------------------------------+
                          |
+-------------------------v-------------------------------------+
|                          Router                              |
|          (per-JID session, allowlist, dispatch)              |
+-------------+---------------------------+---------------------+
              |                           |
     Transport interface           agent.Agent
     Start / Stop / Deliver        Turn / TurnStream
              |                           |
   +----------+----------+       +--------+--------+
   | 9 concrete adapters |       | Provider iface  |
   +---------------------+       | 5 concrete impls|
                                 +--------+--------+
                                          |
                                 +--------v--------+
                                 | Tools Registry  |
                                 | read/write/edit |
                                 | grep/bash + ext |
                                 +--------+--------+
                                          |
                                 +--------v--------+
                                 |  State (SQLite) |
                                 | sessions, cron, |
                                 | jidmap, FTS5    |
                                 +-----------------+
```

O pacote `agent` depende apenas de interfaces expostas por `tools`, de seus próprios tipos `Provider` e da biblioteca padrão. Providers, stores e transportes concretos dependem de `agent` — nunca o contrário.

## O loop do agente

`Session → Turn → Provider → round trip de tool-use`. Cada mensagem do usuário se torna uma chamada a `Agent.Turn`:

1. **Verificação de compressão.** O `Compressor` configurado tem a chance de reescrever a sessão antes de o turno rodar. Quando o faz, `Request.CacheableMessages` é definido para que o bloco de sumário seja cacheado no próximo turno.
2. **Apêndice de skills.** Se um `SkillsProvider` estiver configurado, ele inspeciona a última mensagem do usuário e retorna texto para inserir no system prompt.
3. **Apêndice de recall.** Se um `RecallProvider` estiver configurado, ele consulta o índice FTS5 entre sessões anteriores e retorna texto para inserir.
4. **Chamada ao provider.** A implementação de `Provider.Complete` retorna uma `Response` com um `StopReason`.
5. **Dispatch de tool-use.** Se `StopReason == StopToolUse`, cada chamada de tool solicitada é enviada ao `Approver`. Negações se tornam erros `tool_result` para que o modelo possa se adaptar. Chamadas permitidas são executadas contra o `Registry` e suas saídas são reproduzidas na próxima iteração.
6. **Fim do turno.** Faz loop até `StopReason == StopEndTurn` ou até `MaxIterations` ser atingido (padrão 32).

`internal/agent/agent.go` é a referência canônica.

## Transportes

Cada transporte implementa `transport.Transport`:

```go
type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

`Handler.Handle` recebe uma `IncomingMessage` (`From`, `Body`, `At`) e retorna o texto de resposta. O `Router` fica acima do transporte e é responsável pelo isolamento de sessão por remetente, imposição de allowlist e dispatch para o `Agent`.

Nenhum dos transportes entregues expõe uma superfície HTTP pública por padrão. Slack usa Socket Mode (WebSocket de saída). Discord usa o Gateway (WebSocket de saída). Signal é um subprocesso. WhatsApp é o protocolo Web da Meta sobre TCP. Matrix, Telegram, iMessage e email usam polling. SMS é somente envio porque o lado de entrada exigiria um webhook.

## Registry de tools

`internal/tools` define a interface `Tool` e um `Registry` seguro para concorrência. Tools embutidas vivem em `internal/tools/builtin/`:

- `read` — leitura de arquivo.
- `write` — gravação de arquivo.
- `edit` — substituição de string com imposição de unique-match para prevenir substituições em massa acidentais.
- `grep` — busca de texto.
- `bash` — execução de comando. **O limite de segurança crítico.**

Cada tool declara um schema JSON estrito. Adicionar uma tool é uma única chamada `registry.MustRegister(myTool)` no wire-up; o core do agente não muda.

## Políticas de aprovação

Cada chamada de tool passa por `Approver.Approve` antes da execução. Três políticas embutidas vivem em `internal/agent/approver.go`:

| Modo | Comportamento |
|---|---|
| `allow_all` | Cada chamada roda. Sensato com o provider `claudecli`, que faz seus próprios approvals. |
| `deny_all` | Cada chamada é bloqueada. Útil para smoke tests e sessões somente leitura. |
| `pattern` | Regras regex de allow / deny por tool. Deny prevalece sobre allow. Requisições não casadas recorrem a `Default` (`allow` ou `deny`). |

Motivos de negação são retornados ao modelo como erros `tool_result`, para que o modelo tenha a chance de se adaptar em vez de falhar silenciosamente.

## Armazenamento de sessão

`internal/state/sqlite/` implementa a interface `state.Store` sobre `modernc.org/sqlite` — Go puro, sem libc, sem CGo. Recursos:

- **Journaling WAL** com `busy_timeout=15s`.
- **Checkpoint do WAL no Close** para que o arquivo primário do banco fique consistente para backups.
- **Tabela de recall FTS5** indexa cada mensagem; o `RecallProvider` realiza buscas entre sessões.
- **Tabela de mapa de JID** normaliza identidades LID do WhatsApp para JIDs de telefone.
- **Tabela de cron** persiste jobs agendados entre restarts.

## Servidor MCP

`internal/mcp/server.go` é um servidor JSON-RPC 2.0 sobre stdio, revisão de spec **2024-11-05**. `rousseau mcp` o inicia. Registre tools com `server.Register(mcp.ToolSpec{...})` e deixe um cliente (Claude Desktop, uma extensão de IDE, outro agente) acioná-las.

Falhas de tool são reportadas pelo canal `content` com `isError=true`, não pelo canal de erro do JSON-RPC — isso é o que hosts MCP esperam.

## Scheduler de cron

`internal/cron/scheduler.go` envelopa `robfig/cron/v3`. Jobs são armazenados em SQLite para sobreviverem a restarts. Cada disparo chama `Runner.RunOnce(ctx, prompt)` (um turno one-shot do agente contra uma sessão nova), e então entrega a resposta ao `Delivery` — uma função agnóstica de transporte que envia a mensagem.

Novos jobs adicionados via `rousseau cron add` entram em atividade dentro do próximo `PollInterval` (padrão 60s).

## Loader de skills

`internal/skills/skills.go` escaneia `skills_dir` por arquivos `*.md`. Cada arquivo pode carregar um frontmatter YAML declarando `name`, `description` e `triggers`. Quando qualquer trigger aparece na mensagem atual do usuário, o corpo da skill é inserido no system prompt para aquele turno. O formato é deliberadamente próximo da convenção [agentskills.io](https://agentskills.io).

## Compressão

`internal/agent/compressor.go` executa sumarização baseada em LLM assim que a sessão cruza `TriggerMessages` (padrão 60). As `KeepRecent` mensagens mais recentes (padrão 8) sobrevivem literalmente; tudo mais antigo colapsa em um único bloco de sumário. Desabilitado por padrão porque uma conta `claudecli` em nível de subscrição raramente precisa dele; habilite ao executar contra providers pay-per-token.

## Para onde ir a seguir

- [Referência de configuração](/pt-BR/configuration/) — todos os campos.
- [Referência do loop do agente](/pt-BR/agent-loop/) — contrato para embutir a biblioteca.
- [MCP](/pt-BR/mcp/) — wire-up de cliente.
