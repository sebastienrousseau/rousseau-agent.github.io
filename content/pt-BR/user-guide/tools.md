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
description: "The five built-in tools shipped with rousseau-agent: read, write, edit, grep, bash. JSON schemas, execution semantics, safety notes."
keywords: "tools, read, write, edit, grep, bash, json schema, tool registry"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/user-guide/tools/"
subtitle: "The five built-in tools, with schemas and safety notes."
tags: "tools, reference, read, write, edit, grep, bash"
title: "Ferramentas integradas"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tools, read, write, edit, grep, bash, json schema, tool registry"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Ferramentas integradas"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 42
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/tools/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/tools/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Ferramentas integradas"
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
twitter_description: "The five built-in tools shipped with rousseau-agent: read, write, edit, grep, bash. JSON schemas, execution semantics, safety notes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Ferramentas integradas"
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

## O que vem incluído

`internal/tools/builtin/` fornece as cinco ferramentas que todo daemon rousseau conecta por padrão (veja `internal/cli/chat.go` para o wiring):

| Ferramenta | Propósito | Muta? |
|---|---|:---:|
| `read` | Leitura de arquivo texto UTF-8. | Não |
| `write` | Sobrescrita de arquivo texto UTF-8. Cria pais. | Sim |
| `edit` | Substituição exata de string, exigindo match único. | Sim |
| `grep` | Busca regex RE2 sob um diretório. | Não |
| `bash` | `/bin/sh -c <cmd>` com timeout. | Sim |

Cada uma é registrada via `registry.MustRegister(builtin.NewXTool())`. Registre ferramentas adicionais sem tocar no core do agente — veja [Guia do desenvolvedor: Adicionar uma ferramenta](/pt-BR/developer-guide/add-a-tool/).

## `read`

Lê um arquivo texto UTF-8 do filesystem local.

**Schema de entrada:**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "Absolute filesystem path to the file to read."
    }
  },
  "required": ["path"]
}
```

**Semântica:**

- `path` deve ser absoluto; caminhos relativos são rejeitados.
- Rejeita conteúdo binário via um sniff de `\x00` sobre os primeiros 512 bytes.
- Retorna o conteúdo do arquivo literalmente como uma string.

**Erros:** path ausente, path relativo, arquivo ilegível, conteúdo não textual.

## `write`

Escreve texto UTF-8 em um arquivo, substituindo o conteúdo existente. Cria diretórios pais conforme necessário.

**Schema de entrada:**

```json
{
  "type": "object",
  "properties": {
    "path":    { "type": "string", "description": "Absolute filesystem path to write." },
    "content": { "type": "string", "description": "The complete file contents to write." }
  },
  "required": ["path", "content"]
}
```

**Semântica:**

- Sobrescreve o arquivo (não faz append). Use `edit` para mudanças incrementais.
- `MkdirAll(dir, 0o755)` no diretório pai.
- Arquivo escrito com permissão `0o644`.
- Retorna `wrote <n> bytes to <path>` em sucesso.

**Erros:** path ausente, path relativo, falha de mkdir, falha de write.

## `edit`

Substituição exata de string com uma **restrição de match único**. Emprestado da ferramenta Edit do Claude Code.

**Schema de entrada:**

```json
{
  "type": "object",
  "properties": {
    "path":       { "type": "string", "description": "Absolute filesystem path to the file to edit." },
    "old_string": { "type": "string", "description": "Exact text to find. Must be unique in the file." },
    "new_string": { "type": "string", "description": "Text to replace old_string with." }
  },
  "required": ["path", "old_string", "new_string"]
}
```

**Semântica:**

- `old_string` deve aparecer **exatamente uma vez** no arquivo. Zero ocorrências → erro. Duas ou mais → erro (pede ao modelo para fornecer mais contexto ao redor).
- `old_string == new_string` → erro (edições no-op são rejeitadas).
- Preserva indentação e whitespace literalmente.
- Retorna `edited <path> (1 replacement)` em sucesso.

A regra de match único é deliberada: previne o modelo de realizar substituição em massa acidental. Quando o modelo quer mudar cada ocorrência, ele tem que produzir múltiplas calls de `edit`, cada uma com contexto suficiente ao redor para desambiguar.

**Erros:** path ausente / relativo, `old_string` ausente, sem match, match não único, strings idênticas, falha de read / write.

## `grep`

Busca regex sob um diretório. Deliberadamente mais simples que ripgrep — sem dependência, roda in-process.

**Schema de entrada:**

```json
{
  "type": "object",
  "properties": {
    "pattern":     { "type": "string",  "description": "Go RE2 regular expression to match." },
    "path":        { "type": "string",  "description": "Absolute directory to search under." },
    "include":     { "type": "string",  "description": "Optional filename glob (e.g. '*.go'). Applied to the base name." },
    "ignore_case": { "type": "boolean", "description": "Case-insensitive match. Defaults to false." }
  },
  "required": ["pattern", "path"]
}
```

**Semântica:**

- Sintaxe [RE2](https://github.com/google/re2/wiki/Syntax) do Go — sem backreferences, sem lookaround.
- Percorre recursivamente `path`. Pula `.git`, `node_modules`, `vendor`, `.venv`, `__pycache__`, `dist`, `build`.
- Pula arquivos maiores que `MaxFileBytes` (padrão 4 MiB) e conteúdo binário.
- Limita a saída em `MaxMatches` (padrão 200); truncamento é anotado inline.
- Retorna linhas `<path>:<line>: <matching-line>`.
- Retorna a string `no matches` quando nada bateu.

**Erros:** pattern / path ausente, path relativo, regex inválida, glob de include inválido.

## `bash`

Executa um comando shell via `/bin/sh -c`. **A fronteira de segurança load-bearing.**

**Schema de entrada:**

```json
{
  "type": "object",
  "properties": {
    "command": {
      "type": "string",
      "description": "The shell command to execute."
    }
  },
  "required": ["command"]
}
```

**Semântica:**

- Roda sob `/bin/sh -c <command>`. Não específico do bash — shell POSIX.
- Stdout+stderr combinados são retornados.
- Timeout padrão: 60 segundos. Configurável no registro via `NewBashTool(timeout)`.
- Timeout retorna um erro `bash: timed out after <duration>` junto com qualquer saída produzida antes do prazo.
- Saída não-zero produz um erro cuja string envolve o exit status; a saída ainda é retornada para o modelo inspecionar.

**Segurança:**

- A ferramenta não tem allowlist embutida. O [Approver](/pt-BR/user-guide/approval-policies/) é o gate load-bearing. **Sempre** habilite aprovação em modo pattern em daemons sem supervisão.
- O comando roda com o UID e a visibilidade de filesystem do daemon. Coloque um contêiner rootless por baixo ([Implantação](/pt-BR/deployment/)).

## Erros de ferramenta e o loop

Quando uma ferramenta retorna um erro, o agente o converte em um bloco `tool_result` com `isError: true` e o alimenta de volta ao modelo na próxima iteração:

```
[user] make the change
[assistant] tool_use: edit {"path": "/tmp/foo", "old_string": "x", "new_string": "y"}
[user]      tool_result: "edit: old_string not found in /tmp/foo" (isError=true)
[assistant] I couldn't find "x" in /tmp/foo. Could you confirm the path?
```

Este é o mesmo canal usado para negações do approver — veja [Políticas de aprovação](/pt-BR/user-guide/approval-policies/).

## Registrando ferramentas adicionais

```go
registry := tools.NewRegistry()
registry.MustRegister(builtin.NewReadTool())
registry.MustRegister(builtin.NewWriteTool())
registry.MustRegister(builtin.NewEditTool())
registry.MustRegister(builtin.NewGrepTool(0, 0))    // zero → defaults
registry.MustRegister(builtin.NewBashTool(60 * time.Second))
registry.MustRegister(myCustomTool)                  // any tools.Tool
```

`tools.Registry` é seguro para concorrência; registro é thread-safe.

## Implicações de segurança em um piscar de olhos

| Ferramenta | Raio de impacto | Quando NÃO usar |
|---|---|---|
| `read` | Lê arquivos com a visibilidade FS do daemon. Pode exfiltrar qualquer arquivo legível. | Se qualquer material secreto está em disco no workspace. Restrinja via regex `match` do approver. |
| `grep` | Igual a read mais um custo de CPU de regex. | Se estiver casando patterns não confiáveis — ReDoS é possível com regex patológica. |
| `edit` | Modifica conteúdo de arquivo in-place. | Se a visibilidade FS do daemon se estende além do workspace pretendido. Combine com um bind mount de contêiner. |
| `write` | Cria/sobrescreve arquivos. | Igual a edit, mais pode criar arquivos em qualquer lugar em que o daemon possa escrever. |
| `bash` | Execução de comando arbitrária. | Em qualquer daemon sem supervisão sem um approver em modo pattern. **A fronteira de segurança primária.** |

## Solução de problemas

### `read: read /path: is a directory`

A ferramenta `read` é somente arquivo. Use `grep` com um pattern de path ou `bash` (com `ls`) se precisar de conteúdo de diretório.

### `edit: old_string not found`

O `old_string` proposto pelo modelo não bateu com o conteúdo do arquivo byte a byte. Causas comuns: drift de whitespace/newline, estilo errado de line-ending, o arquivo foi editado entre a leitura do modelo e a call de edit.

### `edit: old_string is not unique`

A ferramenta `edit` do rousseau recusa edições ambíguas — o modelo deve incluir contexto suficiente ao redor para tornar `old_string` uma substring única. Isso previne substituição multi-site acidental.

### `bash: timed out after 1m0s`

Timeout padrão de 60s. Comandos de longa execução (build, test) falharão. Ou aumente o timeout com `NewBashTool(2*time.Minute)` ao embutir, ou divida em passos mais rápidos.

### `grep` não retorna nada mas o pattern está definitivamente lá

O `grep` do rousseau usa o pacote `regexp` do Go (RE2), que não suporta todas as features do PCRE. Backreferences e lookarounds falharão silenciosamente. Reescreva o pattern para RE2.

## Páginas relacionadas

- [Guia do usuário: Políticas de aprovação](/pt-BR/user-guide/approval-policies/) — o gate em cada tool call.
- [Guia do desenvolvedor: Adicionar uma ferramenta](/pt-BR/developer-guide/add-a-tool/) — construa a sua.
- [Conceitos](/pt-BR/concepts/) — como as ferramentas se encaixam no agent loop.
- [Agent loop](/pt-BR/agent-loop/) — como os resultados de ferramenta voltam para o próximo turno.
- [Referência: Schemas de ferramentas](/pt-BR/reference/tool-schemas/) — schemas legíveis por máquina.

## Leitura adicional

- `internal/tools/builtin/read.go` — leitura de arquivo com truncamento.
- `internal/tools/builtin/write.go` — escrita de arquivo.
- `internal/tools/builtin/edit.go` — reforçador da restrição de string única.
- `internal/tools/builtin/grep.go` — busca regex recursiva.
- `internal/tools/builtin/bash.go` — wrapper de shell `/bin/sh -c`.
