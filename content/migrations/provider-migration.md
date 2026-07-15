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
description: "Switch LLM providers (claudecli, anthropic, bedrock, vertex, openai-compatible) mid-project without losing conversation history."
keywords: "provider migration, claudecli, anthropic, bedrock, vertex, openai, ollama"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/migrations/provider-migration/"
subtitle: "Switch LLM backends without losing history."
tags: "migrations, provider, llm"
title: "Migration: Switching Providers"

news_genres: "Blog"
news_keywords: "provider migration, claudecli, anthropic, bedrock, vertex"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Migration: Switching Providers"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "migrations"
order: 14
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/migrations/provider-migration/index.html"
item_link: "https://docs.rousseau-agent.dev/migrations/provider-migration/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Migration: Switching Providers"
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
twitter_description: "Switch LLM providers (claudecli, anthropic, bedrock, vertex, openai-compatible) mid-project without losing conversation history."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Migration: Switching Providers"
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

Rousseau's provider abstraction (`agent.Provider` and `agent.StreamingProvider`) lets you switch LLM backends without touching the session store. Every message is stored provider-agnostically. This guide covers the five backends and the practical steps to cut over.

<aside class="admonition" data-type="tip"><span class="admonition-title">Common driver</span><p>Every provider implements the same <code>Chat</code> / <code>ChatStream</code> interface, so the agent loop, tool-registry, and TUI code are unchanged. The switch is entirely at the config layer.</p></aside>

## Provider matrix

| Provider | Auth | Best for |
|---|---|---|
| `claudecli` | Inherits `claude` CLI OAuth | Individual operators; zero API keys plumbed through rousseau |
| `anthropic` | `ANTHROPIC_API_KEY` | Direct API, prompt-cache markers |
| `bedrock` | AWS credential chain | Enterprise with an AWS contract |
| `vertex` | GCP service-account JSON | Enterprise with a GCP contract |
| `openai` / `openrouter` / `ollama` | Depends | Self-hosted vLLM, LM Studio, OpenRouter aggregation, or local Ollama |

## Migration recipes

<div class="tabs" data-tabs="prov-mig">
  <div class="tab-list" role="tablist" aria-label="Direction">
    <button role="tab" aria-selected="true">claudecli → anthropic</button>
    <button role="tab" aria-selected="false">anthropic → bedrock</button>
    <button role="tab" aria-selected="false">any → ollama</button>
    <button role="tab" aria-selected="false">claudecli → vertex</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Motivation: move from OAuth-inherited claude auth to a scoped API key you can rotate.

```yaml
# before
provider: claudecli
claudecli:
  binary: claude
  permission_mode: bypassPermissions

# after
provider: anthropic
anthropic:
  model: claude-sonnet-4-6
  max_tokens: 4096
```

```sh
export ANTHROPIC_API_KEY=sk-ant-…
rousseau doctor    # confirms anthropic.api_key present (masked)
rousseau chat      # smoke-test
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Motivation: unify LLM spend under an AWS contract; centralised billing and data-residency guarantees.

```yaml
# before
provider: anthropic
anthropic: { model: claude-sonnet-4-6 }

# after
provider: bedrock
bedrock:
  region: eu-west-2
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
  profile: platform
```

```sh
aws sso login --profile platform
rousseau doctor
rousseau chat
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Motivation: airgapped deployment or dev-time cost avoidance.

```yaml
provider: ollama
ollama:
  model: llama3.1:70b-instruct
  # base_url defaults to http://localhost:11434/v1
```

```sh
ollama pull llama3.1:70b-instruct
ollama serve &     # or a systemd unit
rousseau doctor
rousseau chat
```

Local models may not honour tool-use as reliably — see [Providers: OpenAI-compatible](/providers/openai-compatible/).

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Motivation: consolidate under a GCP contract.

```yaml
provider: vertex
vertex:
  project: my-gcp-project
  region: europe-west4
  model: claude-sonnet-4-6@20250101
  credentials_file: /etc/rousseau/vertex.json
```

```sh
gcloud auth application-default login   # or set GOOGLE_APPLICATION_CREDENTIALS
rousseau doctor
rousseau chat
```

  </div>
</div>

## Data-store compatibility

Every switch preserves the session store as-is. Messages are provider-agnostic: `agent.Message` records the role, content, and any tool-use blocks — never the model id or the raw provider response.

If you have compression enabled (`agent.compression.enabled: true`), the summary was written by whichever provider was active at the time. This is fine — the summary is plain text.

## Downgrade path

Every provider switch is reversible by editing the config and restarting. There is no data-store lock-in.

## Verification checklist

- [ ] `rousseau doctor` — `provider.selected` matches the new value and any required credentials are `ok`.
- [ ] `rousseau chat` — send "hello", observe a coherent reply.
- [ ] `rousseau session list --limit 5` — pre-existing history remains.
- [ ] For long-running daemons (WhatsApp, Slack, etc.), restart them so they pick up the new provider factory.

## Common failure modes

- **`claudecli: exec: "claude": executable file not found`** — you set `provider: claudecli` but the CLI is missing. Install it or pick another provider.
- **`anthropic: no API key`** — `ANTHROPIC_API_KEY` not exported and `anthropic.api_key` not in the file.
- **`bedrock: NoCredentialProviders`** — AWS credentials not resolved. Check `AWS_PROFILE`, IAM role, or IRSA.
- **`vertex: could not find default credentials`** — set `credentials_file` or `GOOGLE_APPLICATION_CREDENTIALS`.
- **Tool-use quality drops with a local model** — small models fail JSON-schema tool inputs. Try a bigger model or fall back to Anthropic for tool-heavy sessions.

## Related pages

- [Providers](/providers/) — protocol-level detail per provider.
- [Reference: Config: Provider](/reference/config/provider/)
- [Recipes: Bedrock multi-account](/recipes/bedrock-multi-account/)
- [Recipes: Airgapped deployment](/recipes/airgapped-deployment/)
- [Best Practices: Cost control](/best-practices/cost-control/)
