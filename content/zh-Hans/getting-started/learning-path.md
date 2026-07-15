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
description: "Recommended reading order for new rousseau-agent users, split by role: individual developer, platform operator, security reviewer."
keywords: "learning path, reading order, docs guide, individual developer, platform operator, security reviewer"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/getting-started/learning-path/"
subtitle: "What to read first, split by role."
tags: "learning-path, reading-order"
title: "学习路径"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "learning path, reading order, docs guide, individual developer, platform operator, security reviewer"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "学习路径"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 22
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/getting-started/learning-path/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/learning-path/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "学习路径"
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
twitter_description: "Recommended reading order for new rousseau-agent users, split by role: individual developer, platform operator, security reviewer."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "学习路径"
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

## 选择您的角色

Rousseau 的受众沿三个轴清晰划分。选一个与您目标匹配的角色，并按顺序阅读 —— 每条路径都假定前面的章节已被吸收。

## 个人开发者

您想要在自己笔记本上的编码助手，能持久化会话并驱动您已有的 `claude` CLI。没有团队，没有共享部署。

| # | 页面 | 原因 |
|---|---|---|
| 1 | [入门](/zh-Hans/getting-started/) | 安装、`rousseau chat`、首次运行演练。 |
| 2 | [概念](/zh-Hans/concepts/) | 在自定义任何东西之前，先理解代理循环与会话存储。 |
| 3 | [用户指南：CLI](/zh-Hans/user-guide/cli/) | 每个命令、每个 flag。 |
| 4 | [用户指南：TUI](/zh-Hans/user-guide/tui/) | 键位映射与面板语义。 |
| 5 | [用户指南：工具](/zh-Hans/user-guide/tools/) | 五个内建工具做什么、不做什么。 |
| 6 | [配置](/zh-Hans/configuration/) | 调整您接触到的部分。 |
| 7 | [Skills](/zh-Hans/skills/) | 编写可复用的提示片段。 |

除非您计划将代理循环嵌入到另一个二进制中，否则请跳过 [开发者指南](/zh-Hans/developer-guide/) 下的所有内容。

## 平台运维者

您正为公司边界之后的团队运行 rousseau。可用性、可审计性和最小权限姿态是承载性的。

| # | 页面 | 原因 |
|---|---|---|
| 1 | [入门](/zh-Hans/getting-started/) | 安装与冒烟测试。 |
| 2 | [平台支持](/zh-Hans/getting-started/platform-support/) | 确认每个依赖版本。 |
| 3 | [概念](/zh-Hans/concepts/) | 分层架构 —— 您可以信任跨 release 保持稳定的部分。 |
| 4 | [部署](/zh-Hans/deployment/) | Rootless Podman + Quadlet。Kubernetes 注释。 |
| 5 | [指南：Kubernetes 部署](/zh-Hans/guides/kubernetes-deployment/) | 如果 Kubernetes 是您的目标。 |
| 6 | [配置](/zh-Hans/configuration/) + [参考：配置 schema](/zh-Hans/reference/config-schema/) | 每个旋钮，结构化呈现。 |
| 7 | [用户指南：审批策略](/zh-Hans/user-guide/approval-policies/) | 呈给审计员的工具调用审批故事。 |
| 8 | [指南：可观测性](/zh-Hans/guides/observability/) | 将 slog 输出接线到您的日志管道。 |
| 9 | [指南：审计 + 审批策略](/zh-Hans/guides/audit-approval-policies/) | 附有 deny 规则的可行 pattern 模式配置。 |
| 10 | [更新](/zh-Hans/getting-started/updating/) | 在版本之间安全迁移。 |

## 安全评审员

您正在部署前评估 rousseau，或代表团队回答供应商问卷。

| # | 页面 | 原因 |
|---|---|---|
| 1 | [安全](/zh-Hans/security/) | 信任模型、供应链姿态、密码学清单。 |
| 2 | [安装](/zh-Hans/getting-started/installation/) | cosign + SHA-256 校验配方。 |
| 3 | [概念](/zh-Hans/concepts/) | 分层架构 —— 信任边界的位置。 |
| 4 | [用户指南：审批策略](/zh-Hans/user-guide/approval-policies/) | 模型与 shell 之间的杠杆。 |
| 5 | [指南：只读模式](/zh-Hans/guides/read-only-mode/) | 面向初步检查部署的姿态。 |
| 6 | [参考：退出码](/zh-Hans/reference/exit-codes/) | 呈现给 init 系统与监控的失败模式。 |
| 7 | [隐私](/zh-Hans/privacy/) | 数据流姿态。 |
| 8 | [部署](/zh-Hans/deployment/) | 运行时加固 —— Podman flag、能力剥离、seccomp。 |

## 交叉阅读

一旦挑好角色，每位读者都能从这些页面获益：

- [故障排除](/zh-Hans/troubleshooting/) —— 您可通过 `rousseau doctor` 触及的每个诊断。
- [Changelog](/zh-Hans/changelog/) —— release 之间的变动。
- [MCP](/zh-Hans/mcp/) —— rousseau 如何向其他代理暴露工具与会话。
- [Cron](/zh-Hans/cron/) —— 按时钟调度提示。

## 下一步

- [平台支持](/zh-Hans/getting-started/platform-support/) —— 什么在哪里运行。
- [首个传输](/zh-Hans/getting-started/first-transport/) —— 可行的 WhatsApp 演练。
