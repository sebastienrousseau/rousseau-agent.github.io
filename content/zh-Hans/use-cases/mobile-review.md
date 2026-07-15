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
description: "Use case narrative: reviewing pull requests from WhatsApp on the train, driven by rousseau-agent on a home box."
keywords: "mobile review, whatsapp, pr review, commute, use case, pull request"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/use-cases/mobile-review/"
subtitle: "Reviewing PRs from your phone on the train."
tags: "use-cases, whatsapp, mobile, pr"
title: "用例：手机端 PR 审查"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mobile review, whatsapp, pr review, commute, use case, pull request"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "用例：手机端 PR 审查"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 72
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/use-cases/mobile-review/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/mobile-review/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "用例：手机端 PR 审查"
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
twitter_description: "Use case narrative: reviewing pull requests from WhatsApp on the train, driven by rousseau-agent on a home box."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "用例：手机端 PR 审查"
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

## 故事

您是一家中型公司的 staff 工程师。您的收件箱里有八个待您评审的 PR。您在一趟 45 分钟的火车上，有信号但没有笔记本。历史上，从手机评审 PR 意味着眯着眼看 GitHub 的 diff 视图，并敲下空洞的"LGTM"评论。

Rousseau 生活在您衣橱里的那台 Intel NUC 小机器上。它与您的 JID 建立了 WhatsApp 连接，本地 `claude` CLI 上开启了 `bypassPermissions`，并对您评审的三个仓库的本地 checkout 有读权限。您用 WhatsApp 私聊：

> review PR #4821 in checkout-service

Rousseau 运行 `gh pr diff 4821`，读代码，并回复：

> PR #4821 adds retry-with-backoff to the Stripe webhook handler. Three observations:
>
> 1. The backoff is uncapped — if Stripe is truly down, we'll accumulate goroutines forever. Suggest a `context.WithTimeout` at the caller.
> 2. Test file adds two new tests but neither covers the timeout path.
> 3. `pkg/webhook.go:82` — the mutex is held across the network call. Minor.
>
> Should I draft a review comment stub?

您回复：

> yes, with all three

Rousseau 使用带 `--draft` 的 `gh pr review`（审批器阻拦最终批准；仍需要一个人点击"submit review"）。等您到达桌前时，草稿评论已在等待。

## 这需要什么

### 守护进程

NUC 上以 rootless Podman 容器形式运行的 Rousseau：

- **Provider**：`claudecli` —— 继承您本地的 Claude Code 认证。
- **Transport**：WhatsApp —— 面向移动可达性的首选传输。
- **State**：`~/.local/share/rousseau/sessions.db`。

### 配置

```yaml
provider: claudecli

claudecli:
  binary: claude
  permission_mode: bypassPermissions

whatsapp:
  reply_header: "🚂 *rousseau*\n\n"

log:
  level: info
  format: text                # 这是单用户守护进程；文本日志即可

agent:
  max_iterations: 32
  compression:
    enabled: true             # 订阅层的 claudecli；压缩免费
    trigger_messages: 60
    keep_recent: 8
  approver:
    mode: pattern
    default: deny
    reason: "denied — this daemon reviews code, it does not merge it"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(gh pr view|gh pr diff|gh pr list|gh pr review --draft|gh pr comment|git status|git diff|git log|git show) "}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(go test|go vet|go build|npm test|pnpm test|cargo check) "}
    deny:
      - {tool: bash, match: "gh pr merge|gh pr close|gh pr approve"}
      - {tool: bash, match: "git (push|reset --hard|clean)"}
      - {tool: write, match: "\"path\":\"/etc/|/root/|/var/"}
      - {tool: edit,  match: "\"path\":\"/etc/|/root/|/var/"}
```

### bind mount

- `~/repos/checkout-service/`（只读）。
- `~/repos/payments-api/`（只读）。
- `~/repos/web-frontend/`（只读）。
- `~/.claude/` —— Claude Code 的 OAuth token（读写，但仅用于 token 刷新）。
- `~/.config/gh/` —— GitHub CLI 的 OAuth token（读写，同样原因）。

只读挂载阻止模型意外编辑您的工作副本。评审通过 GitHub 走，而不是您的 checkout。

### 首次启动

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

您扫一次 QR 码。从此守护进程活在 Quadlet 单元中，主机重启时启动。您的允许列表就是您个人手机的 JID。

## 安全姿态

- **允许列表锁住传输。** 只有您的手机能驱动守护进程。任何以某种方式发现电话号码的其他人都会被静默丢弃。
- **Pattern 审批器拦截每次 merge / push / close。** Rousseau 评审、起草、评论 —— 仍然需要一个人点击 "Merge" 或 "Approve"。
- **只读挂载** 保护您工作用的 checkout。
- **claudecli 上的 `bypassPermissions`** 之所以可容忍，只因为审批器在做安全工作。绝不要把 `bypassPermissions` 与 `mode: allow_all` 组合。

## 可达性

- **信号在地铁上会掉。** WhatsApp 的背压很优雅 —— 您发一个问题，等守护进程有信号回复时您就能拿到答案。Rousseau 不需要与您的手机保持一个活的 TCP 会话。
- **语音笔记可用。** 在 NUC 上启用 [语音模式](/zh-Hans/user-guide/voice-mode/) 并安装 `whisper.cpp` 后，您可以口述一条语音笔记 "what's the diff on 4821" 并得到文本回复。当在动车里的手机上打字很烦人时很有用。
- **守护进程运行在您自己的硬件上。** 您的评审推理没有一分子送往第三方 SaaS。唯一出站调用是 `claude` CLI 子进程通过您已有订阅到 Anthropic。

## 这里 rousseau 不做什么

- **它不点击 "Merge"。** 那是人类决定，审批器强制这一点。
- **它不学习您的评审风格。** 除非您写一份捕捉您风格的 [skill](/zh-Hans/skills/)，否则下一个 PR 得到同样的通用清单。
- **它不排队评审。** 每个请求都是独立的；没有"评审我所有开放 PR"的后台任务（除非您通过 [cron](/zh-Hans/guides/scheduled-tasks/) 接线一个）。

## 负载上升后您会改什么

- 添加一份名为 `pr-review-checklist.md` 的 [skill](/zh-Hans/skills/)，把您总是要检查的六件事编码化。当用户消息中出现匹配触发器时，skill 会被拼接进系统提示。
- 添加一个每晚 cron：`0 8 * * 1-5 rousseau ... deliver a summary of every open PR`。
- 如果 `claudecli` 订阅速率限制成为瓶颈，切换到付费 Anthropic API 路径。下游零配置改动。

## 相关页面

- [WhatsApp 传输](/zh-Hans/transports/whatsapp/) —— 传输参考。
- [claudecli provider](/zh-Hans/providers/claudecli/) —— 继承的认证。
- [Skills](/zh-Hans/skills/) —— 如何把您的评审风格编码化。
- [语音模式](/zh-Hans/user-guide/voice-mode/) —— 口述评审。
