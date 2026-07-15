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
description: "Post a PR URL in Slack; rousseau produces a structured code review with cross-session recall of prior review patterns."
keywords: "code review, slack, pr, github, recall, recipes"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/recipes/code-review-bot/"
subtitle: "Slack-driven code review with cross-session recall."
tags: "recipes, slack, code review"
title: "Recipe: Code Review Bot"

news_genres: "Blog"
news_keywords: "code review, slack, pr"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Recipe: Code Review Bot"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "recipes"
order: 14
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/recipes/code-review-bot/index.html"
item_link: "https://docs.rousseau-agent.dev/recipes/code-review-bot/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Recipe: Code Review Bot"
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
twitter_description: "Post a PR URL in Slack; rousseau produces a structured code review."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Recipe: Code Review Bot"
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

Paste a PR link in a Slack channel; rousseau checks out the branch (read-only worktree), reads the diff, cross-references the codebase, and posts a structured review with a "must-fix / nice-to-have / questions" breakdown. Cross-session recall means it remembers your team's review patterns.

## Prerequisites

- Slack app with Socket Mode (as in [on-call Slack triage](/recipes/oncall-slack-triage/)).
- `gh` CLI installed and authenticated.
- A workspace bind mount containing a shallow clone of each repo you want reviewed.
- `anthropic` provider recommended for tool-use fidelity.

## Config

```yaml
provider: anthropic

anthropic:
  model: claude-sonnet-4-6
  max_tokens: 8192

agent:
  system_prompt: |
    You are a careful code reviewer. Given a PR URL:
    1. Use `gh pr diff` (read-only) to fetch the diff.
    2. `grep`/`read` the touched files for context.
    3. Produce a review with three sections: must-fix, nice-to-have, questions.
    4. Cite file paths + line numbers.
  max_iterations: 40
  skills_dir: ~/.config/rousseau/skills
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^(gh pr (view|diff|checks) [0-9]+|git (log|diff|show|status|blame)|rg )"}
    deny:
      - {tool: bash, match: "gh pr (merge|close|edit)"}
      - {tool: write, match: ".*"}
      - {tool: edit,  match: ".*"}

slack:
  app_token: "xapp-…"
  bot_token: "xoxb-…"
  bot_user_id: "U0ABC1234"
```

Notice `write` and `edit` are both denied — the reviewer bot should never modify code.

## Launch

```sh
rousseau slack
```

Post to Slack: `@rousseau review https://github.com/org/repo/pull/123`.

## Skills

`~/.config/rousseau/skills/review.md`:

```markdown
---
name: review
trigger: review, pr, pull request
---
Structure every review as:

**Must fix**
- <bullet>

**Nice to have**
- <bullet>

**Questions**
- <bullet>

Cite as `path/to/file.go:42–58`. Prefer specific over general. If tests are missing, say so.
```

## Verification

- [ ] Post a small PR URL; a structured review lands within 60 s.
- [ ] Ask about a previous review in the same channel; the bot recalls the pattern (cross-session recall via FTS5).

## Failure modes

- **`gh` fails auth** — `gh auth status` from the daemon's shell context. The container needs `~/.config/gh` mounted or a `GH_TOKEN` env var.
- **Reviews too generic** — increase `max_tokens`, and lower the prompt to enumerate specific concerns (nil checks, error propagation, tests).
- **Rate-limited by GitHub** — throttle by using a personal PAT with a longer TTL, or install a GitHub App with higher limits.

## Related pages

- [Reference: Commands: slack](/reference/commands/slack/)
- [Providers: Anthropic](/providers/anthropic/)
- [Best Practices: Approval rules](/best-practices/approval-rules/)
- [Recipes: On-call Slack triage](/recipes/oncall-slack-triage/)
