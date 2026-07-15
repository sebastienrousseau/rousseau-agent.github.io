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
hreflang: "fr"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "fr"
locale: "fr_FR"
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
permalink: "https://docs.rousseau-agent.dev/fr/reference/config-schema/"
subtitle: "JSON-Schema view of internal/config/config.go."
tags: "reference, config, schema, json-schema"
title: "Schéma de configuration"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "config schema, json schema, viper, defaults, configuration reference"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Schéma de configuration"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 52
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/config-schema/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/config-schema/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Schéma de configuration"
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
twitter_title: "Schéma de configuration"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Merci à chaque opérateur qui exploite son propre agent de codage."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Objectif

Cette page est le compagnon lisible par machine de [Configuration](/fr/configuration/). La référence prose explique le **pourquoi** ; cette page montre la forme.

Le schéma ci-dessous est une vue en forme de JSON-Schema de la structure `Config` dans `internal/config/config.go`. Elle fait autorité pour les noms de champs, les types et les défauts — la structure Go est la source de vérité.

## Forme de premier niveau

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

## Définitions

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

### `openai` (partagé par `openai`, `openrouter`, `ollama`)

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

URL de base préréglées :
- `openrouter.base_url` : `https://openrouter.ai/api/v1`
- `ollama.base_url` : `http://localhost:11434/v1`
- `ollama.api_key` : `not-required`

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
    "match": { "type": "string", "description": "Regex RE2 Go contre le JSON brut d'entrée d'outil" }
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
    "poll_interval": { "type": "string", "description": "Chaîne de durée Go, par ex. \"5s\"" },
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

## Précédence

Ordre de résolution (depuis `internal/config/config.go`) :

1. Flag CLI (via `viper.BindPFlag` chez l'appelant).
2. Variable d'environnement (`ROUSSEAU_<UPPERSNAKE>` pour toute clé ; cas spécial `ANTHROPIC_API_KEY`).
3. Fichier de config (`~/.config/rousseau/config.yaml` par défaut).
4. Défauts codés en dur (voir `setDefaults` dans `internal/config/config.go`).

## Mappage vers l'environnement

Chaque champ se mappe à `ROUSSEAU_<SECTION>_<KEY>` en majuscules avec `.` remplacé par `_`. Exemples :

| Clé | Variable env |
|---|---|
| `log.level` | `ROUSSEAU_LOG_LEVEL` |
| `anthropic.api_key` | `ROUSSEAU_ANTHROPIC_API_KEY` (aussi `ANTHROPIC_API_KEY`) |
| `agent.max_iterations` | `ROUSSEAU_AGENT_MAX_ITERATIONS` |
| `slack.app_token` | `ROUSSEAU_SLACK_APP_TOKEN` |

## Suite

- [Configuration](/fr/configuration/) — référence prose avec explication de chaque bouton.
- [Référence : commandes CLI](/fr/reference/cli-commands/) — les flags surchargent chaque champ de config.
- [Référence : codes de sortie](/fr/reference/exit-codes/) — comment les erreurs de parsing de config remontent aux systèmes d'init.
