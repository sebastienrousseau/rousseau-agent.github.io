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
description: "Concrete deployment narratives for rousseau-agent: on-call SRE, mobile PR review, regulated-industry Bedrock deployment."
keywords: "use cases, narratives, on-call, sre, mobile review, whatsapp, bedrock, regulated"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/use-cases/"
subtitle: "具体案例——谁在使用 rousseau，以及为何使用。"
tags: "use-cases, narratives"
title: "用例"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "use cases, narratives, on-call, sre, mobile review, whatsapp, bedrock, regulated"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "用例"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 70
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/use-cases/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "用例"
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
twitter_description: "Concrete deployment narratives for rousseau-agent: on-call SRE, mobile PR review, regulated-industry Bedrock deployment."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "用例"
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

## 当您想要一张图，而不是一本手册时，请阅读这些

用例是简短叙事。每一个都描述了一个可信的运维者、他们面对的问题，以及他们会使用的确切配置。每个用例只有一页 —— 读与您情况相符的那一个。

| 用例 | 角色 | 问题 |
|---|---|---|
| [值班伙伴](/zh-Hans/use-cases/oncall-buddy/) | 小公司的独立 SRE。 | 凌晨 3 点的 Slack 告警，在您完全清醒之前进行 triage。 |
| [移动端 PR 评审](/zh-Hans/use-cases/mobile-review/) | 通勤中的个人开发者。 | 从手机评审 pull request。 |
| [受监管行业](/zh-Hans/use-cases/regulated-industry/) | 金融服务团队。 | 在 Bedrock 托管 VPC 内运行的编码代理，采用 pattern 模式审批。 |

这些用例是示意性的，并非穷尽 —— rousseau 的设计具有通用性。如果您的情况与其中之一相似，请从那里开始。

## 每个用例的共通之处

- rootless 容器中的单一 Go 二进制。
- 每个实例一种传输（Slack、WhatsApp 或 Signal —— 选一个）。
- 一个 `pattern` 模式审批器，配以合理的 deny 规则。
- 会话状态位于 SQLite，重启不会丢失会话。
- 没有 SaaS 控制面、没有遥测端点、没有许可服务器。

## 什么在变

- **Provider** —— 个人笔记本用 `claudecli`，受监管环境用 `bedrock`/`vertex`，自托管 vLLM 用 `openai` 兼容。
- **传输** —— 选工程师已经使用的介质。
- **审批策略** —— 在高风险环境中更严格；在锁死的容器内更宽松。
- **部署面** —— 笔记本、单节点 Podman、Kubernetes。

## 下一步

- [值班伙伴](/zh-Hans/use-cases/oncall-buddy/) —— 最常见的故事。
- [移动端 PR 评审](/zh-Hans/use-cases/mobile-review/) —— WhatsApp 成为参考传输的原因。
- [受监管行业](/zh-Hans/use-cases/regulated-industry/) —— 企业级故事。
