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
changefreq: "weekly"
description: "rousseau-agent's MCP server exposes its tools and sessions over stdio JSON-RPC. Compatible with Claude Desktop and any MCP host."
keywords: "MCP, Model Context Protocol, JSON-RPC, stdio, Claude Desktop, tools, sessions"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/mcp/"
subtitle: "JSON-RPC 2.0 sobre stdio, revisão de spec 2024-11-05."
tags: "MCP, reference"
title: "Servidor MCP"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "MCP, Model Context Protocol, JSON-RPC, stdio, Claude Desktop, tools, sessions"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Servidor MCP"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 21
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/mcp/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Servidor MCP"
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
twitter_description: "rousseau-agent's MCP server exposes its tools and sessions over stdio JSON-RPC. Compatible with Claude Desktop and any MCP host."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Servidor MCP"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">O que você vai aprender</span><p>O formato de wire JSON-RPC 2.0 completo que o rousseau fala, cada método que o servidor MCP do rousseau implementa com pares de exemplo de requisição/resposta, a semântica de códigos de erro, e como configurar hosts MCP do Claude Desktop / Cursor / IDE para alcançar o servidor. Leia <code>internal/mcp/protocol.go</code> e <code>internal/mcp/server.go</code> junto com esta página.</p></aside>

## Formato de wire

`rousseau mcp` inicia um servidor MCP que fala JSON-RPC 2.0 pela stdio, conforme a revisão **2024-11-05** da especificação do [Model Context Protocol](https://modelcontextprotocol.io) (declarada em `ProtocolVersion` em `internal/mcp/protocol.go`).

- Uma requisição por linha na stdin (`bufio.Scanner` lê até 8 MiB por linha).
- Uma resposta por linha na stdout (`json.NewEncoder` emite JSON delimitado por newline).
- O servidor bloqueia até a stdin fechar ou o `ctx` ser cancelado.

### Envelope JSON-RPC 2.0

Toda requisição, notificação e resposta usa este envelope (de `internal/mcp/protocol.go` linha 38):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

Os campos presentes dependem do tipo de envelope:

| Campo | Requisição | Notificação | Resposta |
|---|:---:|:---:|:---:|
| `jsonrpc` | sempre `"2.0"` | sempre `"2.0"` | sempre `"2.0"` |
| `id` | obrigatório | ausente | ecoado da requisição |
| `method` | obrigatório | obrigatório | ausente |
| `params` | opcional | opcional | ausente |
| `result` | ausente | ausente | apenas em sucesso |
| `error` | ausente | ausente | apenas em falha |

Notificações não carregam `id` e não recebem resposta. O rousseau recebe apenas uma notificação (`notifications/initialized`), que é silenciosamente aceita.

### Referência de métodos

O `Server.dispatch` do Rousseau (`internal/mcp/server.go` linha 112) roteia estes métodos:

| Método | Finalidade | Resposta |
|---|---|---|
| `initialize` | Handshake. O cliente declara a versão do protocolo e capacidades. | `InitializeResult` |
| `notifications/initialized` | O cliente confirma que está pronto. | (notificação, sem resposta) |
| `ping` | Prova de vida. | `{}` |
| `tools/list` | Enumera as ferramentas registradas. | `ToolsListResult` |
| `tools/call` | Invoca uma ferramenta. | `ToolsCallResult` |
| `resources/list` | Placeholder. Hoje retorna `{ "resources": [] }`. | `{"resources": []}` |
| `prompts/list` | Placeholder. Retorna `{ "prompts": [] }`. | `{"prompts": []}` |
| `shutdown` | Encerramento iniciado pelo cliente. | `{}` |

<aside class="admonition" data-type="note"><span class="admonition-title">Métodos ausentes</span><p><code>resources/list</code> e <code>prompts/list</code> retornam arrays vazios para que hosts que os sondem não deem erro. Suporte completo a resource/prompt está no roadmap — veja <code>docs/GAP_ANALYSIS_2026.md</code>.</p></aside>

## Exemplos de requisição/resposta

### 1. `initialize`

O cliente envia:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","clientInfo":{"name":"claude-desktop","version":"0.7.0"}}}
```

O servidor responde:

```json
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05","serverInfo":{"name":"rousseau","version":"0.6.0"},"capabilities":{"tools":{"listChanged":false}}}}
```

`listChanged: false` porque o conjunto de ferramentas do rousseau é estático na inicialização do processo — sem add/remove em runtime.

### 2. `tools/list`

```json
{"jsonrpc":"2.0","id":2,"method":"tools/list"}
```

O servidor responde com as ferramentas registradas na ordem de inserção:

```json
{"jsonrpc":"2.0","id":2,"result":{"tools":[
  {"name":"read","description":"Read a file...","inputSchema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
  {"name":"grep","description":"Search for a regex...","inputSchema":{"type":"object","properties":{"pattern":{"type":"string"},"path":{"type":"string"}},"required":["pattern"]}},
  {"name":"bash","description":"Execute a shell command...","inputSchema":{"type":"object","properties":{"command":{"type":"string"}},"required":["command"]}}
]}}
```

### 3. `tools/call`

```json
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"read","arguments":{"path":"/etc/hostname"}}}
```

Sucesso:

```json
{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"my-host.example.com\n"}]}}
```

Falha no nível do handler (exposta como conteúdo, não como erro JSON-RPC — essa é a convenção do MCP):

```json
{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"read: open /nope: no such file or directory"}],"isError":true}}
```

### 4. `ping`

```json
{"jsonrpc":"2.0","id":4,"method":"ping"}
```

```json
{"jsonrpc":"2.0","id":4,"result":{}}
```

## Códigos de erro

O Rousseau usa a faixa padrão de erros JSON-RPC 2.0 mais uma extensão MCP:

| Código | Constante | Significado | Quando é emitido |
|---|---|---|---|
| -32700 | `CodeParseError` | JSON inválido no envelope. | O envelope falhou no `json.Unmarshal`. |
| -32600 | `CodeInvalidRequest` | Formato do envelope está errado. | Campo `jsonrpc` não é `"2.0"`. |
| -32601 | `CodeMethodNotFound` | Método não implementado. | Dispatch caiu no caso default. |
| -32602 | `CodeInvalidParams` | Falha ao decodificar params. | `params` não fez unmarshal no formato esperado. |
| -32603 | `CodeInternalError` | Algo deu errado ao serializar a resposta. | Raro — indica um bug. |
| -32000 | `CodeToolNotFound` | Nome de ferramenta não registrado. | `tools/call` com um `name` desconhecido. |

<aside class="admonition" data-type="warning"><span class="admonition-title">Erros de ferramenta vs. erros JSON-RPC</span><p>Falhas no nível do handler — comando <code>bash</code> com saída não-zero, <code>read</code> em arquivo inexistente — retornam via <code>result.content</code> com <code>isError: true</code>, NÃO pelo campo <code>error</code> JSON-RPC. Apenas falhas de nível de protocolo usam <code>error</code>. Hosts que tratam os dois canais como equivalentes vão classificar erroneamente falhas recuperáveis.</p></aside>

## O que é exposto

Duas superfícies:

- **Tools.** Todo `mcp.ToolSpec` registrado antes de `Serve` é anunciado em `tools/list` e invocável via `tools/call`. O rousseau conecta as mesmas implementações de ferramenta que o agent loop local usa: `read`, `write`, `edit`, `grep`, `bash`.
- **Sessões.** O session store SQLite do rousseau é exposto para que um host MCP possa enumerar e ler conversas passadas. `resources/list` retorna uma entrada por sessão.

Falhas de ferramenta são expostas pelo canal `content` com `isError=true`, não pelo canal de erro JSON-RPC. Essa é a convenção MCP.

## Configuração do cliente — Claude Desktop

Adicione a `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) ou ao equivalente da plataforma:

```json
{
  "mcpServers": {
    "rousseau": {
      "command": "rousseau",
      "args": ["mcp"],
      "env": {
        "HOME": "/Users/you"
      }
    }
  }
}
```

Reinicie o Claude Desktop. `rousseau` aparecerá na paleta de ferramentas; toda ferramenta registrada é invocável.

Para um rousseau embutido em uma imagem Podman, a entrada fica:

```json
{
  "mcpServers": {
    "rousseau": {
      "command": "podman",
      "args": [
        "run", "--rm", "-i",
        "-v", "/Users/you/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z",
        "localhost/rousseau-agent:local",
        "mcp"
      ]
    }
  }
}
```

Faça bind-mount do diretório de estado para que o host MCP veja as mesmas sessões que o daemon.

## Registrando uma ferramenta customizada

Embutindo o servidor MCP em seu próprio binário:

```go
srv := mcp.NewServer("rousseau", "0.1.0", logger)

srv.MustRegister(mcp.ToolSpec{
    Name:        "count_files",
    Description: "Count files under a path.",
    InputSchema: json.RawMessage(`{
      "type": "object",
      "properties": {"path": {"type": "string"}},
      "required": ["path"]
    }`),
    Handler: func(ctx context.Context, args json.RawMessage) ([]mcp.Content, error) {
        var in struct{ Path string }
        if err := json.Unmarshal(args, &in); err != nil {
            return nil, fmt.Errorf("bad input: %w", err)
        }
        // ... count files ...
        return []mcp.Content{{Type: "text", Text: fmt.Sprintf("%d", n)}}, nil
    },
})

_ = srv.Serve(ctx, os.Stdin, os.Stdout)
```

Registros duplicados retornam erro; `MustRegister` faz panic em caso de duplicata (reservado para o wire-up em `main`).

## Concorrência

`Serve` pode ser chamado concorrentemente em transportes independentes (stdin/stdout para o host MCP, além de um canal de controle se quiser). O mapa de ferramentas do servidor é protegido por um RWMutex; a execução do handler não é serializada — as implementações precisam ser seguras para uso concorrente.

## Depuração

Todo envelope de requisição/resposta é registrado no nível `debug` por padrão. Habilite com:

```yaml
log:
  level: debug
  format: text
```

Or:

```sh
ROUSSEAU_LOG_LEVEL=debug rousseau mcp 2>/tmp/mcp.log
```

O host MCP consome a stdout; mantenha o stream de log na stderr.

## Solução de problemas

### Claude Desktop / Cursor nunca mostra as ferramentas do rousseau

Quase sempre é um erro de configuração, não um problema do rousseau. Verifique: (1) o `command` e `args` na config do host invocam `rousseau mcp` (não `rousseau chat`); (2) o arquivo de configuração foi salvo e o host reiniciado; (3) `rousseau mcp </dev/null` a partir de um shell não trava — se travar, resolva isso primeiro.

### `parse error` já na primeira mensagem

O host não está enviando JSON delimitado por linha. Algumas implementações antigas de MCP enviam mensagens com framing (`Content-Length: N\r\n\r\n<body>`); o rousseau espera delimitado por `\n`. Atualize o host para uma versão que usa framing stdio (todos os principais hosts atuais usam).

### `method not found: <foo>`

O host está chamando um método que o rousseau não implementa. `resources/list` e `prompts/list` vazios são fornecidos como no-ops para as sondagens comuns; qualquer outra coisa retorna `-32601`. Verifique `dispatch()` em `internal/mcp/server.go` para a lista completa de métodos.

### Chamadas de ferramenta têm sucesso, mas o host as reporta como erro

O handler da ferramenta retornou o erro do jeito errado. Handlers devem retornar `[]Content{{Type: "text", Text: err.Error()}}, err != nil` — o rousseau captura o erro e o embala como `isError: true`. Não retorne o erro pelo canal `error` do JSON-RPC a menos que seja uma falha de nível de protocolo.

### MCP baseado em contêiner falha com `permission denied` no diretório de estado

A invocação `podman run` a partir do Claude Desktop precisa incluir um `-v` para o diretório de estado com o rótulo SELinux correto. Use `:Z` (privado) a menos que o contêiner seja compartilhado com outras cargas Podman. Verifique também se o UID do host dentro do contêiner corresponde à propriedade dos arquivos.

## Páginas relacionadas

- [MCP: Ferramentas expostas](/pt-BR/mcp/exposed-tools/) — o conjunto de ferramentas que o rousseau publica.
- [MCP: Recursos expostos](/pt-BR/mcp/exposed-resources/) — enumeração e leitura de sessões.
- [MCP: Compatibilidade](/pt-BR/mcp/compatibility/) — matriz de hosts testados.
- [Tutoriais: Expor ferramentas via MCP](/pt-BR/tutorials/expose-tools-via-mcp/) — passo a passo de ponta a ponta.
- [Agent loop](/pt-BR/agent-loop/) — como as mesmas ferramentas são usadas dentro do rousseau.

## Leitura adicional

- `internal/mcp/protocol.go` — envelope, nomes de métodos, códigos de erro.
- `internal/mcp/server.go` — `Serve`, `dispatch`, registro de ferramentas.
- `internal/mcp/tools.go` — helpers para registrar as ferramentas nativas do rousseau.
- `internal/cli/mcp.go` — o wiring do comando `rousseau mcp`.
- [Especificação do Model Context Protocol](https://modelcontextprotocol.io) — referência externa.
