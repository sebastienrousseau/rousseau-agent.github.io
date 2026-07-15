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
description: "Every agent config field: agent.*, agent.compression.*, agent.approver.* with types, defaults, and worked examples."
keywords: "config, agent, compression, approver, skills"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/config/agent/"
subtitle: "Every knob under `agent.*`, including compression and approver blocks."
tags: "reference, config, agent"
title: "Config: Agent"

news_genres: "Blog"
news_keywords: "config, agent, compression, approver"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Config: Agent"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 81
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/config/agent/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/config/agent/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Config: Agent"
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
twitter_description: "Every agent config field: agent.*, agent.compression.*, agent.approver.* with types, defaults, and worked examples."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Config: Agent"
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

The `agent.*` block controls the agent loop itself: iteration budget, system prompt, session compression, tool-call approval policies, and skills discovery. Every key lives on `AgentConfig`, `CompressionConfig`, `ApproverConfig`, and `PatternEntry` in `internal/config/config.go`.

## `agent.*`

| Field | Type | Default | Required | Description | Source |
|---|---|---|---|---|---|
| `agent.system_prompt` | string | empty (falls back to the built-in prompt in `internal/cli/chat.go:systemPrompt`) | no | Overrides the system prompt. Empty uses the sensible default. | `AgentConfig.SystemPrompt` |
| `agent.max_iterations` | int | `32` | no | Hard cap on tool-use loops per turn. Set to 0 to fall back to the default. | `AgentConfig.MaxIterations` |
| `agent.skills_dir` | string | empty | no | Directory of agentskills.io-style Markdown files with YAML frontmatter. Empty disables skills discovery. | `AgentConfig.SkillsDir` |

## `agent.compression.*`

LLM-backed session compression. Disabled by default because subscription-tier providers rarely need it — turn on when running against pay-per-token backends.

| Field | Type | Default | Required | Description | Source |
|---|---|---|---|---|---|
| `agent.compression.enabled` | bool | `false` | no | Toggle the LLM-backed compressor. Off = `NoopCompressor`. | `CompressionConfig.Enabled` |
| `agent.compression.trigger_messages` | int | `60` | no | Message count above which compression fires. 0 uses the default. | `CompressionConfig.TriggerMessages` |
| `agent.compression.keep_recent` | int | `8` | no | Recent messages preserved verbatim. 0 uses the default. | `CompressionConfig.KeepRecent` |
| `agent.compression.prompt` | string | empty | no | Overrides the default summarisation instruction. | `CompressionConfig.Prompt` |

## `agent.approver.*`

Picks and configures the tool-call approval policy.

| Field | Type | Default | Required | Description | Source |
|---|---|---|---|---|---|
| `agent.approver.mode` | string | `allow_all` | no | One of `allow_all`, `deny_all`, `pattern`. | `ApproverConfig.Mode` |
| `agent.approver.reason` | string | empty | no | Human-readable reason attached to denials. | `ApproverConfig.Reason` |
| `agent.approver.default` | string | empty (`deny` recommended) | no | Default fallback for `pattern` mode. `allow` or `deny`. | `ApproverConfig.Default` |
| `agent.approver.allow` | []PatternEntry | empty | no | Regex allow rules. Only relevant to `pattern` mode. | `ApproverConfig.Allow` |
| `agent.approver.deny` | []PatternEntry | empty | no | Regex deny rules. Deny wins over allow. | `ApproverConfig.Deny` |

### `PatternEntry`

| Field | Type | Description |
|---|---|---|
| `tool` | string | Tool name (`read`, `write`, `edit`, `grep`, `bash`, or a custom tool). |
| `match` | string | Go regex; matched against the tool call's input rendering. |

## Approver modes

<div class="tabs" data-tabs="approver-mode">
  <div class="tab-list" role="tablist" aria-label="Approver mode">
    <button role="tab" aria-selected="true">allow_all</button>
    <button role="tab" aria-selected="false">deny_all</button>
    <button role="tab" aria-selected="false">pattern</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Every tool call runs unconditionally. Suitable when the provider is `claudecli`, which handles its own approvals — no rousseau-side filtering.

```yaml
agent:
  approver:
    mode: allow_all
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Every tool call is blocked. Useful as a smoke-test or read-only inspection session (the model can still reason, it just cannot touch the filesystem).

```yaml
agent:
  approver:
    mode: deny_all
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Applies allow/deny regex rules; deny wins over allow; unmatched requests fall back to `default`.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read,  match: ".*"}
      - {tool: grep,  match: ".*"}
      - {tool: edit,  match: "^\\./workspace/.*"}
      - {tool: bash,  match: "^(ls|cat|rg|git status|git diff)"}
    deny:
      - {tool: bash,  match: "rm -rf|sudo|:\\(\\)\\{ :\\|:& \\};:"}
      - {tool: write, match: "\\.ssh/|\\.aws/|/etc/"}
```

  </div>
</div>

## Environment variable equivalents

| YAML | Env var |
|---|---|
| `agent.max_iterations` | `ROUSSEAU_AGENT_MAX_ITERATIONS` |
| `agent.skills_dir` | `ROUSSEAU_AGENT_SKILLS_DIR` |
| `agent.compression.enabled` | `ROUSSEAU_AGENT_COMPRESSION_ENABLED` |
| `agent.compression.trigger_messages` | `ROUSSEAU_AGENT_COMPRESSION_TRIGGER_MESSAGES` |
| `agent.compression.keep_recent` | `ROUSSEAU_AGENT_COMPRESSION_KEEP_RECENT` |
| `agent.approver.mode` | `ROUSSEAU_AGENT_APPROVER_MODE` |
| `agent.approver.default` | `ROUSSEAU_AGENT_APPROVER_DEFAULT` |

List types (`allow`, `deny`) must be provided via the YAML file — env vars cannot express them cleanly.

## Related pages

- [Reference: Config: Provider](/reference/config/provider/)
- [Best Practices: Approval rules](/best-practices/approval-rules/)
- [Best Practices: Session hygiene](/best-practices/session-hygiene/)
- [Reference: Tool schemas](/reference/tool-schemas/)
- [Skills](/skills/)
