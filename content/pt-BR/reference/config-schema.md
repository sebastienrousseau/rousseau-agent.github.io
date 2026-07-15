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
description: "JSON Schema view of every configuration field in rousseau-agent's internal/config/config.go. Types, defaults, and required flags at a glance."
keywords: "config schema, json schema, viper, defaults, configuration reference"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/reference/config-schema/"
subtitle: "JSON-Schema view of internal/config/config.go."
tags: "reference, config, schema, json-schema"
title: "Esquema de configuração"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "config schema, json schema, viper, defaults, configuration reference"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Esquema de configuração"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 52
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/config-schema/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/config-schema/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Esquema de configuração"
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
twitter_description: "JSON Schema view of every configuration field in rousseau-agent's internal/config/config.go. Types, defaults, and required flags at a glance."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Esquema de configuração"
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

## Propósito

Esta página é a companheira legível por máquina de [Configuração](/pt-BR/configuration/). A referência em prosa explica **por quê**; esta página mostra o **formato**.

O schema abaixo é uma visão em formato JSON Schema do struct `Config` em `internal/config/config.go`. Ele é autoritativo para nomes de campos, tipos e padrões — o struct Go é a fonte de verdade.

## Formato de topo

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "provider":   { "type": "string", "enum": ["claudecli","anthropic","openai","openrouter","ollama","bedrock","vertex"], "default": "claudecli" },
    "anthropic":  { "$ref": "#/$defs/anthropic" },
    "claudecli":  { "$ref": "#/$defs/claudecli" },
    "openai":     { "$ref": "#/$defs/openai" },
    "openrouter": { "$ref": "#/$defs/openai" },
    "ollama":     { "$ref": "#/$defs/openai" },
    "bedrock":    { "$ref": "#/$defs/bedrock" },
    "vertex":     { "$ref": "#/$defs/vertex" },
    "log":        { "$ref": "#/$defs/log" },
    "state":      { "$ref": "#/$defs/state" },
    "agent":      { "$ref": "#/$defs/agent" },
    "whatsapp":   { "$ref": "#/$defs/whatsapp" },
    "signal":     { "$ref": "#/$defs/signal" },
    "telegram":   { "$ref": "#/$defs/telegram" },
    "matrix":     { "$ref": "#/$defs/matrix" },
    "slack":      { "$ref": "#/$defs/slack" },
    "discord":    { "$ref": "#/$defs/discord" },
    "sms":        { "$ref": "#/$defs/sms" },
    "imessage":   { "$ref": "#/$defs/imessage" },
    "email":      { "$ref": "#/$defs/email" }
  },
  "additionalProperties": false
}
```

## Definições

### `anthropic`

```json
{
  "type": "object",
  "properties": {
    "api_key":    { "type": "string" },
    "model":      { "type": "string", "default": "claude-sonnet-4-6" },
    "max_tokens": { "type": "integer", "default": 4096 }
  }
}
```

### `claudecli`

```json
{
  "type": "object",
  "properties": {
    "binary":          { "type": "string", "default": "claude" },
    "model":           { "type": "string" },
    "permission_mode": { "type": "string", "enum": ["acceptEdits","auto","bypassPermissions","default","dontAsk","plan"] },
    "extra_args":      { "type": "array", "items": { "type": "string" } }
  }
}
```

### `openai` (compartilhado por `openai`, `openrouter`, `ollama`)

```json
{
  "type": "object",
  "properties": {
    "api_key":    { "type": "string" },
    "model":      { "type": "string" },
    "base_url":   { "type": "string" },
    "max_tokens": { "type": "integer" }
  }
}
```

Base URLs pré-configuradas:
- `openrouter.base_url`: `https://openrouter.ai/api/v1`
- `ollama.base_url`: `http://localhost:11434/v1`
- `ollama.api_key`: `not-required`

### `bedrock`

```json
{
  "type": "object",
  "properties": {
    "region":     { "type": "string" },
    "model":      { "type": "string" },
    "profile":    { "type": "string" },
    "max_tokens": { "type": "integer" }
  }
}
```

### `vertex`

```json
{
  "type": "object",
  "properties": {
    "project":          { "type": "string" },
    "region":           { "type": "string" },
    "model":            { "type": "string" },
    "credentials_file": { "type": "string" },
    "max_tokens":       { "type": "integer" }
  }
}
```

### `log`

```json
{
  "type": "object",
  "properties": {
    "level":  { "type": "string", "enum": ["debug","info","warn","error"], "default": "info" },
    "format": { "type": "string", "enum": ["text","json"], "default": "text" }
  }
}
```

### `state`

```json
{
  "type": "object",
  "properties": {
    "path": { "type": "string", "default": "~/.local/share/rousseau/sessions.db" }
  }
}
```

### `agent`

```json
{
  "type": "object",
  "properties": {
    "system_prompt":  { "type": "string" },
    "max_iterations": { "type": "integer", "default": 32 },
    "skills_dir":     { "type": "string" },
    "approver":       { "$ref": "#/$defs/approver" },
    "compression":    { "$ref": "#/$defs/compression" }
  }
}
```

### `approver`

```json
{
  "type": "object",
  "properties": {
    "mode":    { "type": "string", "enum": ["allow_all","deny_all","pattern"], "default": "allow_all" },
    "reason":  { "type": "string" },
    "default": { "type": "string", "enum": ["allow","deny"], "default": "deny" },
    "allow":   { "type": "array", "items": { "$ref": "#/$defs/pattern_entry" } },
    "deny":    { "type": "array", "items": { "$ref": "#/$defs/pattern_entry" } }
  }
}
```

### `pattern_entry`

```json
{
  "type": "object",
  "properties": {
    "tool":  { "type": "string" },
    "match": { "type": "string", "description": "Go RE2 regex against raw tool-input JSON" }
  }
}
```

### `compression`

```json
{
  "type": "object",
  "properties": {
    "enabled":          { "type": "boolean", "default": false },
    "trigger_messages": { "type": "integer", "default": 60 },
    "keep_recent":      { "type": "integer", "default": 8 },
    "prompt":           { "type": "string" }
  }
}
```

### `whatsapp`

```json
{
  "type": "object",
  "properties": {
    "reply_header": { "type": "string" },
    "voice":        { "$ref": "#/$defs/voice" }
  }
}
```

### `voice`

```json
{
  "type": "object",
  "properties": {
    "enabled":    { "type": "boolean", "default": false },
    "binary":     { "type": "string", "default": "whisper" },
    "model":      { "type": "string" },
    "model_path": { "type": "string" },
    "language":   { "type": "string" },
    "extra_args": { "type": "array", "items": { "type": "string" } }
  }
}
```

### `signal`

```json
{
  "type": "object",
  "properties": {
    "binary":       { "type": "string", "default": "signal-cli" },
    "account":      { "type": "string" },
    "extra_args":   { "type": "array", "items": { "type": "string" } },
    "reply_header": { "type": "string" },
    "allowlist":    { "type": "array", "items": { "type": "string" } }
  }
}
```

### `telegram`

```json
{
  "type": "object",
  "properties": {
    "token":        { "type": "string" },
    "base_url":     { "type": "string" },
    "reply_header": { "type": "string" },
    "allowlist":    { "type": "array", "items": { "type": "string" } }
  }
}
```

### `matrix`

```json
{
  "type": "object",
  "properties": {
    "homeserver_url": { "type": "string" },
    "access_token":   { "type": "string" },
    "user_id":        { "type": "string" },
    "reply_header":   { "type": "string" },
    "allowlist":      { "type": "array", "items": { "type": "string" } }
  }
}
```

### `slack`

```json
{
  "type": "object",
  "properties": {
    "app_token":    { "type": "string" },
    "bot_token":    { "type": "string" },
    "bot_user_id":  { "type": "string" },
    "reply_header": { "type": "string" },
    "allowlist":    { "type": "array", "items": { "type": "string" } }
  }
}
```

### `discord`

```json
{
  "type": "object",
  "properties": {
    "token":        { "type": "string" },
    "reply_header": { "type": "string" },
    "allowlist":    { "type": "array", "items": { "type": "string" } }
  }
}
```

### `sms`

```json
{
  "type": "object",
  "properties": {
    "provider":     { "type": "string", "enum": ["twilio","vonage"] },
    "from":         { "type": "string" },
    "account_sid":  { "type": "string" },
    "auth_token":   { "type": "string" },
    "api_key":      { "type": "string" },
    "base_url":     { "type": "string" },
    "reply_header": { "type": "string" }
  }
}
```

### `imessage`

```json
{
  "type": "object",
  "properties": {
    "base_url":      { "type": "string", "default": "http://localhost:1234" },
    "password":      { "type": "string" },
    "chat_guid":     { "type": "string" },
    "poll_interval": { "type": "string", "description": "Go duration string, e.g. \"5s\"" },
    "reply_header":  { "type": "string" }
  }
}
```

### `email`

```json
{
  "type": "object",
  "properties": {
    "imap_addr":     { "type": "string" },
    "imap_username": { "type": "string" },
    "imap_password": { "type": "string" },
    "mailbox":       { "type": "string" },
    "poll_interval": { "type": "string" },
    "smtp_addr":     { "type": "string" },
    "smtp_username": { "type": "string" },
    "smtp_password": { "type": "string" },
    "from":          { "type": "string" },
    "reply_header":  { "type": "string" }
  }
}
```

## Precedência

Ordem de resolução (de `internal/config/config.go`):

1. Flag de CLI (via `viper.BindPFlag` no caller).
2. Variável de ambiente (`ROUSSEAU_<UPPERSNAKE>` para qualquer chave; caso especial `ANTHROPIC_API_KEY`).
3. Arquivo de configuração (`~/.config/rousseau/config.yaml` por padrão).
4. Padrões hard-coded (veja `setDefaults` em `internal/config/config.go`).

## Mapeamento de ambiente

Cada campo mapeia para `ROUSSEAU_<SEÇÃO>_<CHAVE>` em maiúsculas com `.` substituído por `_`. Exemplos:

| Chave | Variável de ambiente |
|---|---|
| `log.level` | `ROUSSEAU_LOG_LEVEL` |
| `anthropic.api_key` | `ROUSSEAU_ANTHROPIC_API_KEY` (também `ANTHROPIC_API_KEY`) |
| `agent.max_iterations` | `ROUSSEAU_AGENT_MAX_ITERATIONS` |
| `slack.app_token` | `ROUSSEAU_SLACK_APP_TOKEN` |

## Próximo

- [Configuração](/pt-BR/configuration/) — referência em prosa com explicação de cada botão.
- [Referência: Comandos de CLI](/pt-BR/reference/cli-commands/) — flags sobrescrevem cada campo de config.
- [Referência: Códigos de saída](/pt-BR/reference/exit-codes/) — como erros de parse de config chegam aos sistemas init.
