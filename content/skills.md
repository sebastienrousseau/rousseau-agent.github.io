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
changefreq: "weekly"
description: "rousseau-agent's skills loader: Markdown + YAML frontmatter, discovery from skills_dir, trigger-based activation, composition into the system prompt."
keywords: "skills, agentskills.io, markdown, YAML frontmatter, triggers, system prompt, activation"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/skills/"
subtitle: "agentskills.io-compatible markdown skill files."
tags: "skills, reference"
title: "Skills"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "skills, agentskills.io, markdown, YAML frontmatter, triggers, system prompt, activation"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Skills"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 23
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/skills/index.html"
item_link: "https://docs.rousseau-agent.dev/skills/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Skills"
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
twitter_description: "rousseau-agent's skills loader: Markdown + YAML frontmatter, discovery from skills_dir, trigger-based activation, composition into the system prompt."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Skills"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Skill format

A skill is a Markdown file with an optional YAML front-matter header. Format is deliberately close to the [agentskills.io](https://agentskills.io) convention so files are portable to other tools.

Example — `~/.local/share/rousseau/skills/git-rebase.md`:

```markdown
---
name: git-rebase
description: Guide the user through an interactive rebase safely.
triggers:
  - rebase
  - git rebase
  - squash
  - autosquash
---
When helping with a git rebase, first verify the current HEAD is
pushed to a remote branch. Prefer `git rebase -i --autosquash`
when the user has fixup commits. Never force-push to `main`.
```

## Frontmatter fields

| Field | Type | Effect |
|---|---|---|
| `name` | string | Matches `^[a-z][a-z0-9-]*$`. Displayed by `rousseau skills list`. |
| `description` | string | One-line summary. |
| `triggers` | `[]string` | Case-insensitive substrings. If any appears in the user message, the skill activates. Empty means the skill never auto-activates. |

Everything after the closing `---` is the skill body, verbatim.

## Discovery

The loader scans `agent.skills_dir` for `*.md` files (non-recursive). A missing directory is not an error — Load returns `nil`. Subdirectories are ignored.

```yaml
agent:
  skills_dir: ~/.local/share/rousseau/skills
```

## Activation

For every user turn, `SkillsProvider.SystemAppendix(session)` inspects the most recent user message and matches each skill's `triggers` (case-insensitively). Every match is concatenated (in load order) and spliced into the system prompt for that turn.

Skills with empty `triggers` never auto-activate but can be included programmatically by callers embedding the library.

## CLI

```sh
# List discovered skills.
rousseau skills list

# Show the content of a single skill.
rousseau skills show git-rebase
```

## Design constraints

- **No code execution.** Skills are strings. They cannot run scripts or shell commands. If you want automation, wire a new tool via `Registry.Register` instead.
- **No versioning.** rousseau does not track skill versions. Manage that in git — the `skills_dir` is expected to be a working copy of a repository.
- **Deterministic.** The same session + user message produces the same appendix. There is no LLM in the loop.

## Writing effective skills

- Keep the body short (100–500 words). Every activation is prepended to the system prompt for that turn.
- Prefer imperative sentences ("When the user asks about X, do Y") over exposition.
- Use `triggers` for high-precision phrases; wide triggers ("code", "help") activate on nearly every turn and drown out other skills.
- Test in the TUI (`rousseau chat`) before rolling into a chat-transport daemon — the log line `agent.skills_activated` lists which skills fired.
