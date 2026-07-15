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
changefreq: "monthly"
description: "MCP resources exposed by rousseau's stdio server today (none) and the roadmap for sessions-as-resources."
keywords: "mcp, resources, roadmap, sessions, resources/list"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/mcp/exposed-resources/"
subtitle: "What resources rousseau exposes today, and what is planned."
tags: "mcp, resources, roadmap"
title: "MCP：暴露的资源"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, resources, roadmap, sessions, resources/list"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP：暴露的资源"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "mcp"
order: 73
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/mcp/exposed-resources/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/exposed-resources/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "MCP：暴露的资源"
last_build_date: "Mon, 13 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
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
twitter_description: "MCP resources exposed by rousseau's stdio server today (none) and the roadmap for sessions-as-resources."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP：暴露的资源"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "感谢每一位运行自有编码代理的运维者。"
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## 当前状态

Rousseau 的 MCP 服务器（`internal/mcp/server.go`）只声明 `Tools` 能力。它在 `resources/list` 上返回空列表：

```
MethodResourcesList → okResponse(env.ID, map[string]any{"resources": []any{}})
```

意图是有意的。任何看起来像 MCP 资源的用例 —— 已保存的会话、cron 任务描述 —— 目前都通过一个工具（`rousseau_read_session`、`rousseau_cron_list`）暴露，这样宿主可以在需要时请求它确切需要的数据，而不是预先列出每个会话。

## 为什么目前不做资源

当宿主想要枚举一个规模适中、良好定义的 URI 集合（文件、页面）并惰性解引用时，MCP 资源大放异彩。Rousseau 的会话存储可能增长到数千行；在每次 `resources/list` 调用上枚举每个会话会撑爆宿主的上下文。工具面（search / list / read）对高基数状态是更好的形状。

## 路线图

一旦 MCP 规范稳健地支持分页资源枚举，有两个候选者值得作为 MCP 资源暴露：

### 候选：`rousseau://sessions/<id>`

每个 rousseau 会话作为一个资源。URI 会看起来像：

```
rousseau://sessions/1a2b3c4d-…
```

解引用会返回 `rousseau_read_session` 今天返回的相同对话稿。这将让宿主把某个特定会话作为一等公民附加到对话上（"附加会话 1a2b3c…"，拖放），而不要求模型记得调用工具。

门禁：资源列表需要分页。近期版本的 MCP 规范提出了基于游标的分页；一旦落地并且宿主实现它，这就变得可行。

### 候选：`rousseau://cron/<name>`

每个 cron 任务作为一个资源。对提示、调度、投递目标与最后运行时间戳的只读检查。列表较小 —— 今天枚举可能安全，但在会话作为资源的形状被证明之前，不值得从 `rousseau_cron_list` 中单独暴露。

## Prompts 能力

同样今天没有暴露。`internal/mcp/server.go` 的 `dispatch` 中，`MethodPromptsList` 返回 `{"prompts": []any{}}`。Rousseau 没有一个策展好的提示库要暴露；skills 机制（`internal/skills/skills.go`）是等价的内部概念，目前没有通过 MCP 表面化。

如果 skills 路线图收敛到可共享提示，把它们作为 MCP prompts 暴露是自然的下一步。见 [Skills](/zh-Hans/skills/)。

## 如何在今天绕过这个空缺

如果您的 MCP 宿主需要资源以支持特定的 UI 功能（例如会话的拖放），变通做法是：

1. 请求宿主在聊天开始时调用 `rousseau_list_sessions`。
2. 复制您想引用的会话 id。
3. 用该 id 调用 `rousseau_read_session`。

不如原生资源解引用符合人体工学，但功能等价。

## 请求一个资源面

不是每个运维都需要 MCP 上的资源。如果您的团队需要，建设性的路径是提交 issue，附带：

- 您正对接的具体 MCP 宿主。
- 有了资源会更愉悦的用户面动作。
- 大致的流量预期（会话数量、频率）。

## 相关

- [MCP](/zh-Hans/mcp/) —— 综合参考。
- [MCP：暴露的工具](/zh-Hans/mcp/exposed-tools/) —— 今天暴露的是什么。
- [MCP：兼容性](/zh-Hans/mcp/compatibility/) —— 已测试的客户端。
- [Skills](/zh-Hans/skills/) —— 可能成为 MCP prompts 的内部概念。
