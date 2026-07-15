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
description: "Full end-to-end walkthroughs: code-review bot, nightly changelog, VPS deployment, MCP integration, and approver hardening."
keywords: "tutorials, code review bot, changelog, vps deployment, mcp, approval policy"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/tutorials/"
subtitle: "把各个组件串起来的完整端到端教程。"
tags: "tutorials, walkthrough, code review, changelog, deployment, mcp"
title: "教程"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tutorials, code review bot, changelog, vps deployment, mcp, approval policy"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "教程"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/tutorials/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "教程"
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
twitter_description: "Full end-to-end walkthroughs: code-review bot, nightly changelog, VPS deployment, MCP integration, and approver hardening."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "教程"
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

## 教程的用途

指南只回答单一的“我怎么做……”问题。教程则相反：它们从一个完整的真实场景出发，带你走过将其上线所需的每一块 rousseau 组件。每个教程都会产出一个你可以粘贴到自己工作区并期待其工作的成果。

| 教程 | 最终得到 |
|---|---|
| [构建一个代码评审机器人](/zh-Hans/tutorials/build-a-code-review-bot/) | 一个 Slack 频道，在其中对仓库路径 @提及 `@rousseau` 会触发一次 `read` + `grep` 评审。 |
| [每日夜间变更日志](/zh-Hans/tutorials/nightly-changelog/) | 一个 cron 作业，会汇总当天的 `git log` 并在 18:00 推送到 WhatsApp。 |
| [部署到 VPS](/zh-Hans/tutorials/deploy-to-a-vps/) | 在全新 VPS 上、由 systemd 管理的加固 rootless-Podman 部署。 |
| [通过 MCP 暴露工具](/zh-Hans/tutorials/expose-tools-via-mcp/) | Claude Desktop 驱动 `rousseau_search_sessions`、`rousseau_list_sessions`、`rousseau_read_session`、`rousseau_cron_list`。 |
| [加固审批器](/zh-Hans/tutorials/harden-approver-policy/) | 一个严格的 `pattern` 模式审批器，`default: deny`，由 slog 审计轨迹验证。 |

## 先决条件

每个教程都假设你已完成 [Quickstart](/zh-Hans/quickstart/)：`rousseau` 已在 `$PATH` 中，provider 已配置好，且 `rousseau chat` 能产生响应。

除此之外，个别教程会额外说明所需的资源 —— Slack 工作区、VPS、已关联 WhatsApp 的号码，或 `claude` 桌面版。

## 不是教程的场景

如果你想要一个简短的“怎么做 X”配方，请阅读 [指南](/zh-Hans/guides/)。如果你想知道具体的 CLI flag 或配置字段，请跳到 [参考](/zh-Hans/reference/cli-commands/)。如果你想在布线之前先理解 rousseau 某部分的作用，请从 [概念](/zh-Hans/concepts/) 开始。
