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
description: "Layered architecture of rousseau-agent: agent core, provider / tool / transport interfaces, module boundaries, cyclic-dependency prevention."
keywords: "architecture, layers, agent, provider, transport, tools, module, cyclic dependency"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/developer-guide/architecture/"
subtitle: "Layered architecture and module boundaries."
tags: "developer-guide, architecture, layers"
title: "Arquitetura"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "architecture, layers, agent, provider, transport, tools, module, cyclic dependency"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Arquitetura"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 61
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/architecture/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/architecture/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Arquitetura"
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
twitter_description: "Layered architecture of rousseau-agent: agent core, provider / tool / transport interfaces, module boundaries, cyclic-dependency prevention."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Arquitetura"
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

## Panorama em camadas

```
+--------------------------------------------------------------------+
|                                CLI                                |
|  chat  whatsapp  slack  discord  ...  mcp  cron  skills  doctor   |
+--------------------------------+-----------------------------------+
                                 |
+--------------------------------v-----------------------------------+
|                              Router                               |
|                  (per-JID session, allowlist, dispatch)           |
+---------------+---------------+-------------------+---------------+
                |                                   |
       transport.Transport                    agent.Agent
       Start / Stop / Deliver                Turn / TurnStream
                |                                   |
     +----------+----------+              +---------+-----------+
     |  9 concrete adapters |              |    agent.Provider  |
     +---------------------+              |    5 concrete impls |
                                          +---------+-----------+
                                                    |
                                          +---------v-----------+
                                          |   tools.Registry   |
                                          |   tools.Tool iface |
                                          +---------+-----------+
                                                    |
                                          +---------v-----------+
                                          |     state.Store    |
                                          | SQLite: sessions, |
                                          | jidmap, FTS5, cron|
                                          +---------------------+
```

## Papéis dos pacotes

| Pacote | Papel | Depende de |
|---|---|---|
| `internal/agent` | Session, Message, Turn, loop do agente, interfaces Provider / Tool / Approver / Compressor / SkillsProvider / RecallProvider. | stdlib + `internal/tools` (apenas interface). |
| `internal/tools` | Interface Tool + Registry seguro para concorrência. | stdlib. |
| `internal/tools/builtin` | `read`, `write`, `edit`, `grep`, `bash`. | `internal/tools`. |
| `internal/llm/{anthropic,bedrock,claudecli,openai,vertex}` | Implementações concretas de `agent.Provider`. | `internal/agent`. |
| `internal/state` | Interface Store + tipo Summary. | stdlib. |
| `internal/state/sqlite` | Implementação SQLite, WAL, FTS5, tabela de cron, JID map. | `internal/state`, `modernc.org/sqlite`. |
| `internal/transport` | Interface Transport + Router. | `internal/agent`, `internal/state`. |
| `internal/transport/{whatsapp,signal,...}` | Nove adaptadores concretos. | `internal/transport`, `internal/agent`. |
| `internal/mcp` | Servidor JSON-RPC 2.0 sobre stdio, MCP spec 2024-11-05. | `internal/agent`, `internal/tools`, `internal/state`. |
| `internal/skills` | Loader agentskills.io + composição. | stdlib. |
| `internal/cron` | Goroutine de scheduler robfig/cron/v3. | `internal/state`, `internal/agent`. |
| `internal/config` | Loader de config baseado em Viper. | stdlib + `viper`. |
| `internal/cli` | Árvore de comandos Cobra, wire-up. | Tudo acima. |
| `internal/tui` | Modelo Bubble Tea. | `internal/agent`, `internal/state`, `bubbletea`. |
| `cmd/rousseau` | Tratamento de sinais + `Execute`. | `internal/cli`. |

## Invariante crítica

**O pacote `agent` depende apenas das interfaces expostas por `tools`, dos seus próprios tipos `Provider` e da biblioteca padrão.**

Tudo que pode variar — o provider, o store, o transport, o approver, o compressor — é expresso como uma interface pertencente a `agent`. Implementações concretas importam `agent`; `agent` nunca as importa de volta. Isso torna o loop testável sem provider vivo, sem rede viva e sem transport vivo.

Se você se pegar adicionando um import de `agent` em `llm/*`, `transport/*` ou `state/sqlite`, pare. O wiring pertence a `cli`, não a `agent`.

## Prevenção de dependências cíclicas

O compilador Go pega ciclos de import de pacotes em tempo de build. A postura em camadas torna ciclos quase impossíveis: cada camada só conhece as camadas abaixo. Concretamente:

- `cli` pode importar qualquer coisa.
- `transport/*`, `llm/*`, `state/*` podem importar `agent`, `tools` e (para transports e state) seus pacotes de interface irmãos.
- `agent` só pode importar `tools` (interfaces) e a biblioteca padrão.
- `tools` importa apenas a biblioteca padrão.

Duas regras estruturais previnem regressões:

1. Interfaces vivem no pacote **consumidor**. `Provider` é definida em `agent`, não em `llm/anthropic`. `Tool` é definida em `tools`, não em `tools/builtin`.
2. Test doubles vivem junto ao consumidor. `agent_test.go` define providers fake; `transport/whatsapp/client_test.go` define conexões WebSocket fake.

## Interface Provider

```go
// Provider drives a single request/response round-trip.
type Provider interface {
    Complete(ctx context.Context, req Request) (Response, error)
}

// StreamingProvider streams response deltas.
type StreamingProvider interface {
    Provider
    CompleteStream(ctx context.Context, req Request) (StreamReader, error)
}
```

Cada adaptador LLM satisfaz pelo menos `Provider`. Streaming é opt-in.

## Interface Tool

```go
// Tool is a callable capability the model can request.
type Tool interface {
    Name() string
    Description() string
    InputSchema() map[string]any
    Execute(ctx context.Context, input json.RawMessage) (string, error)
}
```

`InputSchema()` retorna um map no formato JSON Schema; a forma deve validar contra as expectativas de tool-use do modelo.

## Interface Transport

```go
type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

Espera-se que `Start` bloqueie até `ctx` ser cancelado ou `Stop` ser chamado. A entrega de volta ao remetente é tratada pelo transport internamente; adaptadores tipicamente expõem um método `Deliver(ctx, target, body)` usado pelo scheduler de cron.

## Interface Approver

```go
type Approver interface {
    Approve(ctx context.Context, req ApprovalRequest) (Decision, string)
}
```

Chamado no hot path antes de cada tool call. Veja [Políticas de aprovação](/pt-BR/user-guide/approval-policies/).

## Compressor e Recall

Mais duas interfaces que o loop do agente consulta a cada turno:

```go
type Compressor interface {
    Compress(ctx context.Context, s *Session) (changed bool, err error)
}

type RecallProvider interface {
    SystemAppendix(ctx context.Context, s *Session) string
}
```

Veja [Compressão + Recall](/pt-BR/user-guide/compression-recall/).

## Wire-up em `cli`

`internal/cli/chat.go` é o exemplo canônico de wire-up. Ele:

1. Carrega a config.
2. Constrói um provider (`buildProvider(cfg)`).
3. Abre o store SQLite (`openStore`).
4. Cria um tool registry e registra as ferramentas embutidas.
5. Constrói um approver a partir de `cfg.Agent.Approver`.
6. Constrói um compressor a partir de `cfg.Agent.Compression`.
7. Constrói `agent.New(...)`.
8. Entrega o agente ao modelo Bubble Tea.

Todo outro comando segue o mesmo padrão — as partes específicas de daemon são apenas o construtor do transport e sua invocação de `Start`.

## Padrão de teste

As interfaces de cada camada tornam possível testar em isolamento:

- `agent_test.go` usa um `Provider` fake que retorna valores `Response` prontos.
- `transport/whatsapp/client_test.go` usa um `WSConn` fake e um `Sender` fake.
- `state/sqlite/*_test.go` usa SQLite em memória (`file::memory:`).
- `tools/builtin/*_test.go` usa `testing/fstest.MapFS` (onde relevante) e arquivos temporários.

Veja [Testes](/pt-BR/developer-guide/testing/) para o padrão de injeção.

## Grafo de dependências de pacotes

```
cmd/rousseau/               (entry point)
    │
    ▼
internal/cli/               (Cobra command tree)
    │
    ├───▶ internal/config/  (Viper-driven config)
    ├───▶ internal/agent/   (Turn loop, session, provider iface, approver, compressor)
    │        │
    │        └───▶ internal/tools/           (Tool iface + Registry)
    │                    │
    │                    └───▶ internal/tools/builtin/   (read, write, edit, grep, bash)
    │
    ├───▶ internal/llm/anthropic/  ─────┐
    ├───▶ internal/llm/bedrock/    ─────┤
    ├───▶ internal/llm/claudecli/  ─────┼─▶ implements agent.Provider
    ├───▶ internal/llm/openai/     ─────┤
    ├───▶ internal/llm/vertex/     ─────┘
    │
    ├───▶ internal/transport/           (Transport iface + Router)
    │        │
    │        ├───▶ whatsapp/    (whatsmeow)
    │        ├───▶ slack/       (Socket Mode)
    │        ├───▶ discord/     (Gateway v10)
    │        ├───▶ telegram/    (Bot API)
    │        ├───▶ matrix/      (Client-Server)
    │        ├───▶ signal/      (signal-cli JSON-RPC)
    │        ├───▶ email/       (IMAP + SMTP)
    │        ├───▶ sms/         (Twilio / Vonage REST)
    │        └───▶ imessage/    (BlueBubbles)
    │
    ├───▶ internal/cron/        (scheduled prompts)
    ├───▶ internal/mcp/         (JSON-RPC 2.0 server)
    ├───▶ internal/skills/      (agentskills.io loader)
    ├───▶ internal/state/       (Store iface)
    │        │
    │        └───▶ internal/state/sqlite/   (WAL, FTS5)
    │
    └───▶ internal/tui/         (Bubble Tea model)
```

Propriedade crítica: `internal/agent` depende apenas da biblioteca padrão, de `internal/tools` (por sua interface estreita) e de seus próprios subpacotes. Cada provider, cada store e cada transport depende de `agent` — nunca o contrário.

## Racional estilo ADR

Decisões selecionadas de fronteira e por que existem:

### ADR-1: Provider é uma interface, não um plugin

Consideramos um modelo de plugin (`plugin.Open` ou `hashicorp/go-plugin`). Rejeitado porque:

- Builds estáticos são mais fáceis de assinar, reproduzir e distribuir.
- ABIs de plugin são frágeis entre versões do Go.
- Cada provider com o qual nos importamos é pequeno o suficiente para vendorizar.

Trade-off: adicionar um provider requer um rebuild. Aceitável.

### ADR-2: Tools ficam em `internal/tools/builtin`, não em `pkg/tools`

Consideramos expor o tool registry publicamente. Rejeitado porque:

- `internal/` desencoraja acoplamento acidental.
- Callers embutindo o agente ainda podem registrar suas próprias ferramentas via a interface exportada `Registry` — apenas o fazem pelo pacote `tools` em vez de importar um builtin.

Trade-off: usuários não podem importar `rousseau/tools/builtin` diretamente. Eles importam `rousseau/agent` e `rousseau/tools` e constroem seu próprio registry, que é o que `examples/embed-agent` demonstra.

### ADR-3: SQLite via `modernc.org/sqlite`, não `mattn/go-sqlite3`

`modernc.org/sqlite` é um port em Go puro; `mattn/go-sqlite3` usa cgo. Escolhido porque:

- `CGO_ENABLED=0` mantém o binário estático.
- Binários estáticos são mais fáceis de assinar, reproduzir e distribuir.
- O job de CI de build reprodutível seria muito mais difícil com cgo.

Trade-off: `modernc.org/sqlite` é mais lento para cargas de escrita intensa. Aceitável — o rousseau não é um banco de escrita intensa.

### ADR-4: Servidor MCP é minimalista, não o SDK oficial

O pacote `internal/mcp/` tem ~200 linhas de JSON-RPC feito à mão. Escolhido porque:

- A superfície MCP que o rousseau precisa é pequena (initialize, tools/list, tools/call, ping, shutdown).
- O SDK Go oficial ainda não era estável quando o código foi escrito.
- Manter a superfície pequena torna a troca indolor quando o SDK se estabilizar.

Trade-off: algumas features do MCP (resources, prompts, notificações list-changed) são stubs. Roadmap.

### ADR-5: O provider `claudecli` não usa o tool registry do rousseau

O subprocesso do `claude` roda seu próprio loop de tool-use. O approver do rousseau, portanto, não consegue ver as tool calls. Essa é uma aceitação deliberada:

- O provider `claudecli` existe para permitir que assinantes usem sua auth do Claude Code sem uma chave de API.
- Se o rousseau interceptasse o loop de ferramentas, teríamos que enviar cada entrada e saída pela fronteira do subprocesso — lento e propenso a erros.
- Usuários que querem aprovação do lado rousseau usam um provider não-`claudecli`.

Trade-off: usuários do `claudecli` precisam confiar no modelo de permissões do `claude`. Documentado em [Providers: claudecli](/pt-BR/providers/claudecli/).

## Próximo

- [Adicionar um transport](/pt-BR/developer-guide/add-a-transport/) — como se parece um novo implementador de interface.
- [Adicionar um provider](/pt-BR/developer-guide/add-a-provider/) — mesmo padrão, interface diferente.
- [Adicionar uma tool](/pt-BR/developer-guide/add-a-tool/) — o menor ponto de extensão.

## Páginas relacionadas

- [Conceitos](/pt-BR/concepts/) — tour em alto nível.
- [Loop do agente](/pt-BR/agent-loop/) — a forma de runtime.
- [MCP](/pt-BR/mcp/) — exposição de tools externas.
- [Configuração](/pt-BR/configuration/) — a superfície de config que cada interface lê.

## Leitura adicional

- `README.md` — posicionamento no nível do repositório e matriz de capacidade.
- `internal/agent/agent.go` — o loop core.
- `internal/agent/provider.go` — as interfaces `Provider` e `StreamingProvider`.
- `internal/transport/transport.go` — a interface `Transport`.
- `internal/tools/registry.go` — a interface `Tool` e `Registry`.
