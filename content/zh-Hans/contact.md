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
description: "Support routing for rousseau-agent. GitHub issues for bugs and features. sebastian.rousseau@gmail.com for security reports."
keywords: "contact, support, GitHub issues, security disclosure, email"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/contact/"
subtitle: "Bug、新功能与安全报告的对接渠道。"
tags: "contact, support"
title: "联系我们"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "contact, support, GitHub issues, security disclosure, email"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "联系我们"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "support"
order: 29
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/contact/index.html"
item_link: "https://docs.rousseau-agent.dev/contact/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "联系我们"
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
twitter_description: "Support routing for rousseau-agent. GitHub issues for bugs and features. sebastian.rousseau@gmail.com for security reports."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "联系我们"
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

## Bug 与功能建议

请在 https://github.com/sebastienrousseau/rousseau-agent/issues 提交 issue。请包含：

- `rousseau version` 输出。
- Go 版本、操作系统、容器运行时。
- 最小复现 —— 最好是一个失败的测试。
- 使用 `ROUSSEAU_LOG_LEVEL=debug` 采集的日志片段，并对机密信息做脱敏处理。

## 安全披露

**请勿** 为涉及安全的报告提交公开 issue。请发送邮件：

**sebastian.rousseau@gmail.com**

确认 SLA：72 小时。完整披露 SLA 表格位于 [安全页面](/zh-Hans/security/)。

如果您已有 CVSS 3.1 向量，请附上；同时说明受影响的组件（文件路径与行号范围，或依赖模块）、最小复现步骤，以及您需要遵守的任何协同披露时间线。

完整策略见源码仓库中的 `SECURITY.md`。

## 商业 / 咨询

`rousseau-agent` 是一个 MIT 许可的开源项目。不存在商业支持层级。咨询合作按需进行 —— 请通过上方邮箱联系维护者。
