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
hreflang: "en"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "en-GB"
locale: "en_GB"
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
description: "Every provider config field: provider, anthropic.*, claudecli.*, openai.*, bedrock.*, vertex.* with types, defaults and source citations."
keywords: "config, provider, anthropic, claudecli, openai, bedrock, vertex"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/config/provider/"
subtitle: "Every knob under `provider`, `anthropic.*`, `claudecli.*`, `openai.*`, `bedrock.*`, `vertex.*`."
tags: "reference, config, provider"
title: "Config: Providers"

news_genres: "Blog"
news_keywords: "config, provider, anthropic, claudecli, openai, bedrock, vertex"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Config: Providers"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 80
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/config/provider/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/config/provider/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Config: Providers"
last_build_date: "Mon, 13 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
ttl: "60"
type: "website"
webmaster: sebastian.rousseau@gmail.com (Sebastien Rousseau)

apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "rousseau-agent"
apple-touch-fullscreen: "yes"

msapplication-navbutton-color: "rgb(26,58,138)"

twitter_card: "summary"
twitter_creator: "rousseauagent"
twitter_description: "Every provider config field: provider, anthropic.*, claudecli.*, openai.*, bedrock.*, vertex.* with types, defaults and source citations."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Config: Providers"
twitter_url: "https://docs.rousseau-agent.dev"

author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Overview

Every provider-related config key lives on `Config`, `AnthropicConfig`, `ClaudeCLIConfig`, `OpenAIConfig`, `BedrockConfig`, and `VertexConfig` in `internal/config/config.go`. Precedence for every field: CLI flag > environment variable (`ROUSSEAU_<SECTION>_<KEY>`) > YAML file > hard-coded default.

<aside class="admonition" data-type="tip"><span class="admonition-title">Discovery</span><p>Run <code>rousseau doctor</code> after changing provider config. It surfaces the resolved provider, whether the required credentials are present, and (for claudecli) the version of the child binary.</p></aside>

## `provider`

| Field | Type | Default | Required | Description | Source |
|---|---|---|---|---|---|
| `provider` | string | `claudecli` | no | LLM backend selector. One of `claudecli`, `anthropic`, `openai`, `openrouter`, `ollama`, `bedrock`, `vertex`. | `Config.Provider` in `internal/config/config.go` |

## `anthropic.*`

Direct Anthropic API (SDK-backed).

| Field | Type | Default | Required | Description | Source |
|---|---|---|---|---|---|
| `anthropic.api_key` | string | empty | yes when `provider: anthropic` | Injected automatically from the `ANTHROPIC_API_KEY` env var by `config.Load`. | `AnthropicConfig.APIKey` |
| `anthropic.model` | string | `claude-sonnet-4-6` | no | Model id. | `AnthropicConfig.Model` |
| `anthropic.max_tokens` | int64 | `4096` | no | Upper bound on generated tokens per turn. | `AnthropicConfig.MaxTokens` |

## `claudecli.*`

Default provider. Shells out to a local `claude` binary and inherits Claude Code's auth.

| Field | Type | Default | Required | Description | Source |
|---|---|---|---|---|---|
| `claudecli.binary` | string | `claude` | no | Executable name or absolute path. | `ClaudeCLIConfig.Binary` |
| `claudecli.model` | string | empty | no | Overrides claude's default model. | `ClaudeCLIConfig.Model` |
| `claudecli.permission_mode` | string | empty | no | `--permission-mode` value: `acceptEdits`, `auto`, `bypassPermissions`, `default`, `dontAsk`, `plan`. Unattended daemons flip empty values to `bypassPermissions`. | `ClaudeCLIConfig.PermissionMode` |
| `claudecli.extra_args` | []string | empty | no | Appended to every claude invocation. | `ClaudeCLIConfig.ExtraArgs` |

## `openai.*`, `openrouter.*`, `ollama.*`

Three top-level blocks share the same `OpenAIConfig` shape. `openrouter` and `ollama` come pre-seeded with sensible `base_url` defaults.

| Field | Type | Default | Required | Description | Source |
|---|---|---|---|---|---|
| `openai.api_key` | string | empty | yes when `provider: openai` | OpenAI-compatible API key. | `OpenAIConfig.APIKey` |
| `openai.model` | string | empty | yes when `provider: openai` | Model id (e.g. `gpt-4o-mini`). | `OpenAIConfig.Model` |
| `openai.base_url` | string | empty | no | Override to hit a self-hosted vLLM, LM Studio, etc. | `OpenAIConfig.BaseURL` |
| `openai.max_tokens` | int64 | 0 (SDK default) | no | Cap on generated tokens. | `OpenAIConfig.MaxTokens` |
| `openrouter.api_key` | string | empty | yes when `provider: openrouter` | OpenRouter key. | shared |
| `openrouter.model` | string | empty | yes when `provider: openrouter` | Model id, e.g. `anthropic/claude-sonnet-4`. | shared |
| `openrouter.base_url` | string | `https://openrouter.ai/api/v1` | no | Set by `setDefaults`. | shared |
| `ollama.api_key` | string | `not-required` | no | Ollama does not need a key; the string exists to satisfy the SDK. | shared |
| `ollama.model` | string | empty | yes when `provider: ollama` | Local model id, e.g. `llama3.1:70b`. | shared |
| `ollama.base_url` | string | `http://localhost:11434/v1` | no | Set by `setDefaults`. | shared |

## `bedrock.*`

AWS-managed Claude on Bedrock. Uses the standard AWS credential chain.

| Field | Type | Default | Required | Description | Source |
|---|---|---|---|---|---|
| `bedrock.region` | string | empty | yes when `provider: bedrock` | AWS region. | `BedrockConfig.Region` |
| `bedrock.model` | string | empty | yes when `provider: bedrock` | Bedrock model id, e.g. `anthropic.claude-sonnet-4-6-20250101-v1:0`. | `BedrockConfig.Model` |
| `bedrock.profile` | string | empty | no | Named AWS profile from `~/.aws/credentials`. | `BedrockConfig.Profile` |
| `bedrock.max_tokens` | int64 | 0 (SDK default) | no | Cap on generated tokens. | `BedrockConfig.MaxTokens` |

## `vertex.*`

GCP-managed Claude on Vertex AI.

| Field | Type | Default | Required | Description | Source |
|---|---|---|---|---|---|
| `vertex.project` | string | empty | yes when `provider: vertex` | GCP project id. | `VertexConfig.Project` |
| `vertex.region` | string | empty | yes when `provider: vertex` | GCP region. | `VertexConfig.Region` |
| `vertex.model` | string | empty | yes when `provider: vertex` | Model id, e.g. `claude-sonnet-4-6@20250101`. | `VertexConfig.Model` |
| `vertex.credentials_file` | string | empty | no | Path to service-account JSON; falls back to `GOOGLE_APPLICATION_CREDENTIALS`. | `VertexConfig.CredentialsFile` |
| `vertex.max_tokens` | int64 | 0 (SDK default) | no | Cap on generated tokens. | `VertexConfig.MaxTokens` |

## Environment variable equivalents

Every YAML key maps to `ROUSSEAU_<SECTION>_<KEY>`. `.` becomes `_`. Examples:

<div class="tabs" data-tabs="prov-env">
  <div class="tab-list" role="tablist" aria-label="Provider">
    <button role="tab" aria-selected="true">Anthropic</button>
    <button role="tab" aria-selected="false">claudecli</button>
    <button role="tab" aria-selected="false">Bedrock</button>
    <button role="tab" aria-selected="false">Vertex</button>
  </div>
  <div class="tab-panel" role="tabpanel">

```sh
export ANTHROPIC_API_KEY=sk-ant-…      # magic path; injected by config.Load
export ROUSSEAU_ANTHROPIC_MODEL=claude-sonnet-4-6
export ROUSSEAU_ANTHROPIC_MAX_TOKENS=8192
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```sh
export ROUSSEAU_CLAUDECLI_BINARY=/opt/claude/claude
export ROUSSEAU_CLAUDECLI_PERMISSION_MODE=bypassPermissions
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```sh
export ROUSSEAU_BEDROCK_REGION=eu-west-2
export ROUSSEAU_BEDROCK_MODEL=anthropic.claude-sonnet-4-6-20250101-v1:0
export AWS_PROFILE=platform
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```sh
export ROUSSEAU_VERTEX_PROJECT=my-gcp-project
export ROUSSEAU_VERTEX_REGION=europe-west4
export GOOGLE_APPLICATION_CREDENTIALS=/etc/rousseau/vertex.json
```

  </div>
</div>

## Related pages

- [Reference: Config Schema](/reference/config-schema/)
- [Providers: claudecli](/providers/claudecli/)
- [Providers: Anthropic](/providers/anthropic/)
- [Providers: Bedrock](/providers/bedrock/)
- [Providers: Vertex](/providers/vertex/)
- [Providers: OpenAI-compatible](/providers/openai-compatible/)
- [Reference: Environment variables](/reference/environment-variables/)
