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
description: "Fully airgapped rousseau deployment using Ollama or vLLM as the LLM provider. No SaaS calls, no external DNS."
keywords: "airgapped, offline, ollama, vllm, self-hosted, recipes"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/recipes/airgapped-deployment/"
subtitle: "Fully offline rousseau with Ollama or vLLM."
tags: "recipes, airgap, offline, ollama"
title: "Recipe: Airgapped Deployment"

news_genres: "Blog"
news_keywords: "airgapped, offline, ollama, vllm"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Recipe: Airgapped Deployment"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "recipes"
order: 21
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/recipes/airgapped-deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/recipes/airgapped-deployment/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Recipe: Airgapped Deployment"
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
twitter_description: "Fully airgapped rousseau deployment using Ollama or vLLM as the LLM provider."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Recipe: Airgapped Deployment"
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

Run rousseau on a network with no outbound access to Anthropic, OpenAI, Bedrock, or Vertex. Use a locally hosted OpenAI-compatible endpoint (Ollama or vLLM) and one of the fully self-hosted transports (Matrix on your own Synapse, Signal via `signal-cli`, or email via your own SMTP host).

## Prerequisites

- A machine capable of running the target model (GPU or lots of RAM).
- Ollama or vLLM installed and serving a model.
- All outbound firewall rules blocked except to the LLM endpoint and, if used, your Matrix homeserver / signal-cli / IMAP+SMTP host.

## Config

```yaml
provider: ollama

ollama:
  model: llama3.1:70b-instruct
  base_url: http://ollama.internal:11434/v1
  api_key: not-required

state:
  path: /var/lib/rousseau/sessions.db

agent:
  max_iterations: 24
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "^/workspace/.*"}
    deny:
      - {tool: bash, match: ".*"}   # extra strict for high-assurance deployment
```

For vLLM, swap:

```yaml
provider: openai

openai:
  api_key: sk-anything-vllm-ignores
  model: mistralai/Mistral-Large-Latest
  base_url: http://vllm.internal:8000/v1
```

## Network egress

Combine with the nftables recipe:

```text
# /etc/nftables.d/rousseau.nft
table inet rousseau {
  chain output {
    type filter hook output priority 0; policy drop;
    ct state established,related accept
    ip daddr { 10.42.0.10 } tcp dport { 11434 } accept  # ollama
    ip daddr { 10.42.0.20 } tcp dport { 8448 } accept   # matrix homeserver
    ip daddr { 10.42.0.30 } tcp dport { 993, 465 } accept  # imap + smtp
    log prefix "[rousseau blocked] " counter drop
  }
}
```

See [Best Practices: Network egress](/best-practices/network-egress/).

## Verification

- [ ] `curl https://api.anthropic.com` from the rousseau host fails / times out.
- [ ] `curl http://ollama.internal:11434/api/tags` returns the served models.
- [ ] `rousseau doctor` shows `provider.selected: ollama`.
- [ ] `rousseau chat` responds — potentially slower than cloud providers.

## Failure modes

- **Tool-use quality plummets** — small models fail structured tool inputs. Use a 70B-scale model minimum, or accept degraded tool use and rely on `read`/`grep` only.
- **Latency spikes** — GPU memory pressure. Monitor VRAM; smaller batch sizes.
- **`context length exceeded`** — enable `agent.compression.enabled: true` to trim session length before token overflow.
- **DNS leaks** — the container inherits host DNS. Point at an internal DNS resolver only.

## Related pages

- [Providers: OpenAI-compatible](/providers/openai-compatible/)
- [Guides: Self-hosted vLLM](/guides/self-hosted-vllm/)
- [Best Practices: Network egress](/best-practices/network-egress/)
- [Best Practices: Secret management](/best-practices/secret-management/)
- [Migrations: Provider migration](/migrations/provider-migration/)
