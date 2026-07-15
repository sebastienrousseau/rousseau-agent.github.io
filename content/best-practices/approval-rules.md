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
description: "Pattern-mode approver playbooks by role: reviewer, on-call, community bot, docs writer, security auditor."
keywords: "approver, pattern, roles, best practices, allow deny"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/best-practices/approval-rules/"
subtitle: "Pattern-mode playbooks by role."
tags: "best-practices, approver, security"
title: "Approval Rules"

news_genres: "Blog"
news_keywords: "approver, pattern, roles"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Approval Rules"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "best-practices"
order: 14
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/best-practices/approval-rules/index.html"
item_link: "https://docs.rousseau-agent.dev/best-practices/approval-rules/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Approval Rules"
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
twitter_description: "Pattern-mode approver playbooks by role."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Approval Rules"
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

`agent.approver` decides whether every tool call runs. Three modes: `allow_all`, `deny_all`, `pattern`. This page catalogues pattern-mode configs by role.

Deny wins over allow. Unmatched requests use `default`. The full field reference lives at [Reference: Config: Agent](/reference/config/agent/).

<aside class="admonition" data-type="tip"><span class="admonition-title">Test in isolation</span><p>Before shipping a new pattern config, run <code>rousseau chat</code> with the change and try to make the agent do the destructive thing you want blocked. If it refuses, you have coverage. If it doesn't, tighten the rules.</p></aside>

## Role playbooks

<div class="tabs" data-tabs="approve-role">
  <div class="tab-list" role="tablist" aria-label="Role">
    <button role="tab" aria-selected="true">Code reviewer</button>
    <button role="tab" aria-selected="false">On-call SRE</button>
    <button role="tab" aria-selected="false">Community bot</button>
    <button role="tab" aria-selected="false">Docs writer</button>
    <button role="tab" aria-selected="false">Security auditor</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Reads/greps everywhere, no writes.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^(git (log|diff|show|blame|status)|gh pr (view|diff|checks) [0-9]+|rg )"}
    deny:
      - {tool: bash, match: "gh pr (merge|close|edit|approve)"}
      - {tool: write, match: ".*"}
      - {tool: edit,  match: ".*"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Read runbooks, tail logs, inspect kubernetes but never mutate.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^(kubectl get|kubectl describe|kubectl logs|journalctl -u [a-z0-9-]+|dmesg|systemctl status [a-z0-9-]+)"}
    deny:
      - {tool: bash, match: "kubectl (delete|scale|patch|apply|edit|exec)|systemctl (stop|restart|start)|sudo"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Reads docs only. No shell, no writes.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: "^/workspace/docs/.*"}
      - {tool: grep, match: "^/workspace/docs/.*"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Reads and edits docs; no other tools.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read,  match: ".*"}
      - {tool: grep,  match: ".*"}
      - {tool: edit,  match: "^/workspace/docs/.*"}
      - {tool: write, match: "^/workspace/docs/.*"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Runs vulnerability scanners; no writes, no destructive shell.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^(govulncheck ./...|npm audit --json|trivy fs .|semgrep --config auto .)"}
```

  </div>
</div>

## Universally-safe deny rules

Add these to *every* pattern config:

```yaml
deny:
  - {tool: bash,  match: "rm -rf|:\\(\\)\\{ :\\|:& \\};:"}   # fork bomb, rm -rf
  - {tool: bash,  match: "sudo|doas|pkexec"}                  # privilege escalation
  - {tool: bash,  match: "curl [^|]*\\| *sh|wget [^|]*\\| *sh"}  # pipe to shell
  - {tool: write, match: "\\.ssh/|\\.aws/|\\.gnupg/|/etc/"}   # sensitive paths
  - {tool: edit,  match: "\\.ssh/|\\.aws/|\\.gnupg/|/etc/"}
```

## Testing

- Log every denial with `agent.approver.reason` set to a descriptive string. Denials appear in the transport reply so users know why.
- Grep `journalctl … | grep "denied by pattern policy"` in staging to find prompts that hit unexpected denies.

## Related pages

- [Reference: Config: Agent](/reference/config/agent/)
- [Reference: Tool schemas](/reference/tool-schemas/)
- [Security](/security/)
- [Recipes: Code review bot](/recipes/code-review-bot/)
- [Recipes: On-call Slack triage](/recipes/oncall-slack-triage/)
