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
hreflang: "zh-Hans"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "zh-Hans"
locale: "zh_CN"
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
permalink: "https://docs.rousseau-agent.dev/zh-Hans/skills/"
subtitle: "兼容 agentskills.io 的 Markdown 技能文件。"
tags: "skills, reference"
title: "技能"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "skills, agentskills.io, markdown, YAML frontmatter, triggers, system prompt, activation"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "技能"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 23
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/skills/index.html"
item_link: "https://docs.rousseau-agent.dev/skills/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "技能"
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
twitter_title: "技能"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "感谢每一位运行自有编码代理的运维者。"
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## 技能格式

一个技能是带可选 YAML front-matter 头的 Markdown 文件。格式刻意接近 [agentskills.io](https://agentskills.io) 惯例，以便文件可以移植到其他工具。

示例 —— `~/.local/share/rousseau/skills/git-rebase.md`：

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

## Frontmatter 字段

| 字段 | 类型 | 作用 |
|---|---|---|
| `name` | string | 匹配 `^[a-z][a-z0-9-]*$`。由 `rousseau skills list` 显示。 |
| `description` | string | 单行摘要。 |
| `triggers` | `[]string` | 不区分大小写的子串。若其中任意一个出现在用户消息中，该技能就会被激活。为空表示该技能永远不会自动激活。 |

结束的 `---` 之后的所有内容都是技能正文，原样保留。

## 发现

加载器扫描 `agent.skills_dir` 中的 `*.md` 文件（非递归）。目录不存在不是错误 —— Load 返回 `nil`。子目录会被忽略。

```yaml
agent:
  skills_dir: ~/.local/share/rousseau/skills
```

## 激活

在每次用户 turn 中，`SkillsProvider.SystemAppendix(session)` 会检查最近一条用户消息，并（不区分大小写地）匹配每个技能的 `triggers`。所有匹配都会按加载顺序拼接，并拼接到该次 turn 的系统提示词中。

`triggers` 为空的技能从不自动激活，但嵌入本库的调用者可以以编程方式包含它们。

## CLI

```sh
# 列出已发现的技能。
rousseau skills list

# 显示单个技能的内容。
rousseau skills show git-rebase
```

## 设计约束

- **不执行代码。** 技能只是字符串。它们不能运行脚本或 shell 命令。如果需要自动化，请通过 `Registry.Register` 布线一个新工具。
- **不做版本管理。** rousseau 不跟踪技能版本。请在 git 中管理 —— `skills_dir` 应该是某个仓库的工作副本。
- **确定性。** 相同的会话 + 用户消息会产生相同的附录。回路中没有 LLM。

## 编写高效技能

- 正文保持简短（100–500 字）。每次激活都会被前置到该次 turn 的系统提示词。
- 优先使用祈使句（“当用户询问 X 时，请做 Y”），而不是叙述性文字。
- 对 `triggers` 使用高精度短语；宽泛的触发词（"code"、"help"）几乎每次 turn 都会激活，会淹没其他技能。
- 上线到聊天传输守护进程前，先在 TUI（`rousseau chat`）中测试 —— 日志行 `agent.skills_activated` 会列出触发的技能。
