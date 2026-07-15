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
description: "The exact JSON schemas for the five built-in tools rousseau ships: read, write, edit, grep, bash."
keywords: "tool schemas, read, write, edit, grep, bash, JSON Schema"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/reference/tool-schemas/"
subtitle: "JSON schemas for the five built-in tools, verbatim from internal/tools/builtin."
tags: "reference, tools, json-schema, read, write, edit, grep, bash"
title: "Referência: esquemas de ferramentas"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tool schemas, read, write, edit, grep, bash, JSON Schema"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Referência: esquemas de ferramentas"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 54
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/tool-schemas/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/tool-schemas/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Referência: esquemas de ferramentas"
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
twitter_description: "The exact JSON schemas for the five built-in tools rousseau ships: read, write, edit, grep, bash."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Referência: esquemas de ferramentas"
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

## O que esta página é

Cada ferramenta embutida em `internal/tools/builtin/*.go` publica um método `InputSchema()` que retorna um mapa JSON Schema. Esta página reproduz esses schemas exatamente, mais um parágrafo sobre o contrato de runtime de cada ferramenta.

As cinco ferramentas embutidas são: [`read`](#read), [`write`](#write), [`edit`](#edit), [`grep`](#grep), [`bash`](#bash). Todas as cinco são construídas no wiring do daemon; o approver (`internal/agent/approver.go`) fica entre a tool call do modelo e o método `Execute` da ferramenta.

## read

Fonte: `internal/tools/builtin/read.go`.

**Descrição (exposta ao modelo):** _Read the contents of a UTF-8 text file. Input: absolute path. Returns file contents or an error._

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

**Contrato.** O `path` deve ser absoluto (`filepath.IsAbs`). A ferramenta lê o arquivo inteiro para memória e o rejeita se os primeiros 512 bytes contêm um byte NUL (`isLikelyText`). Retorna o conteúdo do arquivo como string em sucesso; um erro caso contrário. Nenhum limite de contagem de linhas ou tamanho é aplicado no nível da ferramenta — políticas de aprovação são o lugar certo para limitar tamanhos de arquivo.

## write

Fonte: `internal/tools/builtin/write.go`.

**Descrição (exposta ao modelo):** _Write UTF-8 text to a file, replacing existing contents. Creates parent directories as needed. Input: absolute path + content._

**Schema de entrada:**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "Absolute filesystem path to write."
    },
    "content": {
      "type": "string",
      "description": "The complete file contents to write."
    }
  },
  "required": ["path", "content"]
}
```

**Contrato.** Sobrescrita de arquivo completo. Cria diretórios pais com modo `0o755`. Escreve com modo `0o644`. Caminho absoluto obrigatório. Retorna `"wrote N bytes to /path"`. Deliberadamente não há dança de atomic-swap — approvers em modo pattern fixam o alvo de escrita em uma árvore de diretório específica; a própria ferramenta não tenta ser inteligente sobre segurança de filesystem.

## edit

Fonte: `internal/tools/builtin/edit.go`.

**Descrição (exposta ao modelo):** _Replace exactly one occurrence of old_string with new_string in a file. old_string must be unique in the file; if it appears zero or multiple times the edit fails. Preserve indentation exactly._

**Schema de entrada:**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "Absolute filesystem path to the file to edit."
    },
    "old_string": {
      "type": "string",
      "description": "Exact text to find. Must be unique in the file."
    },
    "new_string": {
      "type": "string",
      "description": "Text to replace old_string with."
    }
  },
  "required": ["path", "old_string", "new_string"]
}
```

**Contrato.** Substituição exata de string, não regex. `old_string` deve aparecer **exatamente uma vez** no arquivo — zero matches ou múltiplos matches falham com um erro descritivo, o que é intencional (emprestado da ferramenta Edit do Claude Code). Previne mass-replace acidental e força o modelo a incluir contexto suficiente ao redor para desambiguar. `old_string == new_string` também gera erro. Retorna `"edited /path (1 replacement)"`.

## grep

Fonte: `internal/tools/builtin/grep.go`.

**Descrição (exposta ao modelo):** _Search files under a directory for a Go regular expression. Skips binary files and files larger than the configured limit. Returns 'path:line: matched_line' rows._

**Schema de entrada:**

```json
{
  "type": "object",
  "properties": {
    "pattern": {
      "type": "string",
      "description": "Go RE2 regular expression to match."
    },
    "path": {
      "type": "string",
      "description": "Absolute directory to search under."
    },
    "include": {
      "type": "string",
      "description": "Optional filename glob (e.g. '*.go'). Applied to the base name."
    },
    "ignore_case": {
      "type": "boolean",
      "description": "Case-insensitive match. Defaults to false."
    }
  },
  "required": ["pattern", "path"]
}
```

**Contrato.** Regex RE2, não PCRE. Case-insensitive quando `ignore_case: true` (implementado prefixando `(?i)`). Pula diretórios chamados `.git`, `node_modules`, `vendor`, `.venv`, `__pycache__`, `dist`, `build`. Pula arquivos maiores que `MaxFileBytes` (padrão 4 MiB). Trunca a saída em `MaxMatches` (padrão 200) e anexa um footer `(truncated at N matches)` quando bate no cap. Pula arquivos que contêm um byte NUL na linha atual (detecção binária aproximada).

## bash

Fonte: `internal/tools/builtin/bash.go`.

**Descrição (exposta ao modelo):** _Execute a shell command via `/bin/sh -c`. Returns combined stdout+stderr with exit status._

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

**Contrato.** `/bin/sh -c <command>`. Stdout + stderr combinados, limitados ao que cabe em um `bytes.Buffer` (isto é, RAM). Timeout de 60 segundos por padrão (configurável na construção). Em timeout: retorna saída parcial mais um erro `bash: timed out after 60s`. **Sem sandbox no nível da ferramenta.** O usuário OS do daemon, a view de filesystem, a postura de rede e o perfil seccomp são a contenção. Approvers em modo pattern são como você estreita os comandos permitidos — veja [Tutorial: Endurecer o approver](/pt-BR/tutorials/harden-approver-policy/).

## Ferramentas expostas por MCP

O servidor MCP stdio do rousseau (`rousseau mcp`) expõe um conjunto **diferente** de ferramentas — queries somente leitura contra o session store e jobs de cron. Veja [MCP: Ferramentas expostas](/pt-BR/mcp/exposed-tools/) para `rousseau_search_sessions`, `rousseau_list_sessions`, `rousseau_read_session`, `rousseau_cron_list`.

## Relacionado

- [Guia do usuário: Tools](/pt-BR/user-guide/tools/) — a view voltada ao operador.
- [Guias: Gerenciamento de arquivos](/pt-BR/guides/file-management/) — como `write`/`edit` interagem com bind mounts e SELinux.
- [Guias: Auditoria + políticas de aprovação](/pt-BR/guides/audit-approval-policies/) — como regexes de pattern restringem a entrada de cada ferramenta.
- [Guia do desenvolvedor: Adicionar uma ferramenta](/pt-BR/developer-guide/add-a-tool/) — estenda este conjunto.
