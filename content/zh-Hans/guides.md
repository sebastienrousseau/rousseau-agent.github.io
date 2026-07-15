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
changefreq: "monthly"
description: "Worked examples for rousseau-agent: scheduled tasks, self-hosted vLLM, Kubernetes deployment, approval-policy audits, observability, read-only mode."
keywords: "guides, tutorials, worked examples, vllm, kubernetes, audit, observability, read-only"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/guides/"
subtitle: "带可运行配置的实战示例。"
tags: "guides, tutorials"
title: "指南"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "guides, tutorials, worked examples, vllm, kubernetes, audit, observability, read-only"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "指南"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 30
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/guides/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "指南"
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
twitter_description: "Worked examples for rousseau-agent: scheduled tasks, self-hosted vLLM, Kubernetes deployment, approval-policy audits, observability, read-only mode."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "指南"
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

## 本节内容

指南是带有可运行配置的实战示例。每篇指南端到端回答一个“我怎么做……”的问题。

| 指南 | 回答 |
|---|---|
| [定时任务](/zh-Hans/guides/scheduled-tasks/) | 如何让 rousseau 按计划通过 WhatsApp 提醒我？ |
| [自托管 vLLM](/zh-Hans/guides/self-hosted-vllm/) | 如何将 rousseau 指向内网中的 vLLM 端点？ |
| [Kubernetes 部署](/zh-Hans/guides/kubernetes-deployment/) | 如何以 Kubernetes `Deployment` 的形式运行 rousseau？ |
| [审计 + 审批策略](/zh-Hans/guides/audit-approval-policies/) | 如何锁定 `bash` 工具的同时仍让 agent 做有用的工作？ |
| [可观测性](/zh-Hans/guides/observability/) | 如何把 rousseau 的 slog 输出接入 Loki / Grafana / Datadog？ |
| [只读模式](/zh-Hans/guides/read-only-mode/) | 如何将 rousseau 作为一个从不修改工作区的只读巡检 agent 运行？ |

## 何时读指南、概念还是参考

- **[概念](/zh-Hans/concepts/)** —— 想理解 agent loop 的工作原理。
- **指南** —— 想解决一个具体的运维问题。
- **[参考](/zh-Hans/reference/cli-commands/)** —— 想知道某个 flag 的确切签名。

## 下一步

- [定时任务](/zh-Hans/guides/scheduled-tasks/) —— 通常是运维者最先查阅的指南。
