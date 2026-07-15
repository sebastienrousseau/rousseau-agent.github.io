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
description: "Monitoring rousseau's LLM spend: prompt-cache markers, compression, max-iteration ceilings, per-project counters."
keywords: "cost, monitoring, prompt cache, compression, ceilings, best practices"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/best-practices/cost-control/"
subtitle: "Watch prompt spend, catch loops before they cost."
tags: "best-practices, cost, monitoring"
title: "Cost Control"

news_genres: "Blog"
news_keywords: "cost, monitoring, prompt cache"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Cost Control"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "best-practices"
order: 17
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/best-practices/cost-control/index.html"
item_link: "https://docs.rousseau-agent.dev/best-practices/cost-control/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Cost Control"
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
twitter_description: "Monitoring rousseau's LLM spend."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Cost Control"
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

Rousseau's cost knobs sit at three levels: what the model spends per turn, how many turns happen per session, and how often a daemon fires. Setting all three lets you catch a runaway prompt loop before it becomes an invoice.

## The four levers

<div class="tabs" data-tabs="cost-lever">
  <div class="tab-list" role="tablist" aria-label="Lever">
    <button role="tab" aria-selected="true">Iteration cap</button>
    <button role="tab" aria-selected="false">Prompt-cache markers</button>
    <button role="tab" aria-selected="false">Compression</button>
    <button role="tab" aria-selected="false">max_tokens</button>
  </div>
  <div class="tab-panel" role="tabpanel">

`agent.max_iterations` caps the tool-use loop. Default 32.

```yaml
agent:
  max_iterations: 24
```

Set lower for narrow-purpose bots (community FAQ), higher for pair programming. Runaway loops (model calls the same tool 60 times) are always a bug or a prompt issue — the cap ensures they never burn through your budget.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

The Anthropic provider (`internal/llm/anthropic/`) writes prompt-cache markers on the last two messages. Anthropic's prompt-cache pricing is roughly 10% of full inference for cache reads. In long sessions with a stable prefix (system prompt + skills + early context), this is the biggest single lever.

No config knob — it's automatic when `provider: anthropic`.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Compression rewrites older history into a summary once you cross `trigger_messages`.

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60
    keep_recent: 8
```

Turn on for pay-per-token providers. The one-time compression cost pays off after ~10 more messages.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Bound the output size per turn:

```yaml
anthropic:  { max_tokens: 4096 }
bedrock:    { max_tokens: 4096 }
vertex:     { max_tokens: 4096 }
```

Community and triage bots do fine with 2048; code-review bots often need 8192.

  </div>
</div>

## Monitoring

Rousseau logs one `agent.turn.finished` event per turn with token usage (when the provider exposes it). Aggregate with the log platform of your choice.

<div class="tabs" data-tabs="cost-monitor">
  <div class="tab-list" role="tablist" aria-label="Platform">
    <button role="tab" aria-selected="true">Loki + Grafana</button>
    <button role="tab" aria-selected="false">Provider console</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Loki query:

```logql
sum by (project) (
  rate({service="rousseau"} |= "agent.turn.finished" | json | unwrap output_tokens [1h])
)
```

Graph per project, alert on >2× the moving average.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

- Anthropic console: usage per API key.
- AWS: CloudWatch Bedrock model invocations.
- GCP: Vertex AI usage in the billing dashboard.

Tag rousseau's requests with a unique metadata field (via provider-specific request options) to distinguish from other apps.

  </div>
</div>

## Anti-patterns

- **Unbounded max_iterations** — a stuck agent can call `read` on a 500MB file 30 times. Cap it.
- **Long system prompts without cache markers** — you pay full price for the same tokens every turn if the provider is not Anthropic. Consider moving big context into `agent.skills_dir` instead.
- **No allowlist on public transports** — every message from a stranger costs LLM tokens. Always allowlist.

## Related pages

- [Reference: Config: Agent](/reference/config/agent/)
- [Reference: Logs](/reference/logs/)
- [Providers: Anthropic](/providers/anthropic/) — prompt-cache markers detail
- [Best Practices: Multi-tenant](/best-practices/multi-tenant/)
- [Recipes: Airgapped deployment](/recipes/airgapped-deployment/) — the ultimate cost control is not being on a paid provider
