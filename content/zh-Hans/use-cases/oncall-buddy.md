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
description: "Use case narrative: a solo SRE running rousseau-agent over Slack to triage a 3 a.m. page from the couch, then hand off to full incident response."
keywords: "on-call, sre, slack, incident, page, triage, use case"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/use-cases/oncall-buddy/"
subtitle: "Triaging a 3 a.m. page from the couch over Slack."
tags: "use-cases, on-call, slack, sre"
title: "用例：值班伙伴"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "on-call, sre, slack, incident, page, triage, use case"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "用例：值班伙伴"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 71
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/use-cases/oncall-buddy/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/oncall-buddy/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "用例：值班伙伴"
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
twitter_description: "Use case narrative: a solo SRE running rousseau-agent over Slack to triage a 3 a.m. page from the couch, then hand off to full incident response."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "用例：值班伙伴"
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

凌晨 3 点。您的 pager 响了。PagerDuty 说 checkout 服务正在抛 502。您是一家小公司里的两名 SRE 之一，您的搭档在休假中，走到笔记本前意味着找眼镜、下楼、解锁 VPN。在这之前，您想要一个首轮答案：哪些仪表板看起来糟糕，过去 24 小时内什么变了，适用哪份 runbook。

Rousseau 生活在您衣橱里的运维机器上。它对您的日志栈有只读凭据、对一个命名空间有只读 kubectl、并到 `#incident-oncall` 有一个 Slack Socket Mode 连接。您在手机上点开 DM 通知：

> what changed in checkout in the last 24h?

Rousseau 读 checkout 服务仓库的 git log，与您的部署日志（来自一个 bind-mount 目录）交叉引用，并回复：

> Two changes: PR #4821 (payment retry logic, deployed 21:14 UTC) and a Helm value bump on `checkout-web` at 22:03 UTC. The payment retry change is the more suspicious — it touches the same code path the current 502s originate from.

您问：

> pull the last 100 error lines from checkout-web

Rousseau 在其只读 kubeconfig 下运行 `kubectl logs -n checkout deploy/checkout-web --tail=100 --previous`，并粘回显著的行。您看到一个空指针 trace。您回 DM：

> revert PR #4821 in staging first — call me when it's confirmed green

Rousseau 在 `#incident-oncall` 中发布带计划的消息，对 staging 打开一个 revert PR，并在 staging 转绿后 ping 回来。您起床走到笔记本前。

## 这需要什么

### 守护进程

Rousseau 在运维机器上以 rootless Podman 容器方式运行：

- **Provider**：`bedrock` —— 您公司已有 Bedrock 支出承诺；不需要按用户的 API key。
- **Transport**：Slack Socket Mode —— 没有入站 HTTP 面，只有出站 WebSocket。
- **State**：`~/.local/share/rousseau/sessions.db`，在 LUKS 加密盘上。

### 配置

```yaml
provider: bedrock

bedrock:
  region: us-east-1
  profile: rousseau-oncall
  model: anthropic.claude-sonnet-4-6-20250101-v1:0

log:
  level: info
  format: json

state:
  path: /var/lib/rousseau/sessions.db

agent:
  max_iterations: 32
  approver:
    mode: pattern
    default: deny
    reason: "read-only on-call posture — ask an operator to widen the scope"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(kubectl get|kubectl describe|kubectl logs|git log|git diff|git show|cat|grep|rg|head|tail|wc) "}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"gh pr (view|list|diff) "}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"gh pr create --draft "}   # 允许打开一个 draft revert
    deny:
      - {tool: bash, match: "kubectl (delete|apply|edit|scale|rollout undo|exec)"}
      - {tool: bash, match: "gh pr merge|gh pr close --delete-branch"}

slack:
  app_token: xapp-<...>
  bot_token: xoxb-<...>
  allowlist:
    - U012ABCXYZ    # 您的 Slack 用户 ID
    - U012DEFGHI    # 您搭档的 Slack 用户 ID
```

### bind mount

- `/workspace/repos/` 下的仓库 checkout（只读）。
- `/workspace/deploys/` 下的部署日志（只读）。
- `/home/rousseau/.kube/config` 的 kubeconfig —— 只读挂载，服务账号在 `checkout` 命名空间中拥有只读 cluster role。
- 在 EKS 上通过 IAM Role for Service Accounts (IRSA) 的 AWS 凭据，或本地部署时通过一个挂载的 `~/.aws/`。

### systemd Quadlet 单元

参考的 `docker/rousseau-agent.container`，带：

- `ReadOnly=true`
- `DropCapability=all`
- `NoNewPrivileges=true`
- `Restart=on-failure`

主机重启时启动。日志可通过 `journalctl --user -u rousseau-agent.service` 获取。

## 安全姿态

- **Slack 允许列表** 确保只有您与您搭档能驱动守护进程。所有其他 DM 都被静默丢弃。
- **带 `default: deny` 的 Pattern 审批器** 拦截白名单之外的任何东西。如果模型想运行 `kubectl delete pod`，它会得到一个解释拦截的 `tool_result` 错误，并转向一份计划文档。
- **只读 kubeconfig + 只读仓库挂载** 意味着即使审批器开门失败，守护进程也*不能*改动生产。
- **腰带、背带，再加第二条腰带** —— 每层都安全失败。

## 这里 rousseau 不做什么

- **它不 page 您。** PagerDuty 是谁在 on-call 的真理来源。
- **它不合并 PR。** 审批器拦截 `gh pr merge`。Rousseau 可以打开一个 draft revert；仍需一个人确认。
- **它不运行 `kubectl exec`。** 任何可能改动集群状态的命令都被拒绝。
- **它不从事件中学习。** 通过 FTS5 的跨会话回忆意味着下一次事件的 rousseau 会找到今晚会话的关键字；语义结论仍是运维的工作。

## 负载上升后您会改什么

如果每月两次 3 点的 page 变成每周两次：

- 随着信心增加，考虑把更多 `bash` 匹配器提升到 `allow`。
- 把 slog 输出接线到 [Loki](/zh-Hans/guides/observability/)，让复盘评审能引用 rousseau 做过的确切工具调用。
- 添加 [定时任务](/zh-Hans/guides/scheduled-tasks/)，让 rousseau 把开放事件的每晚摘要送到您的早晨 Slack。

## 相关页面

- [指南：审计 + 审批策略](/zh-Hans/guides/audit-approval-policies/) —— 安全杠杆。
- [指南：只读模式](/zh-Hans/guides/read-only-mode/) —— 最严格姿态。
- [Slack 传输](/zh-Hans/transports/slack/) —— Socket Mode 接线。
- [Bedrock provider](/zh-Hans/providers/bedrock/) —— 认证链。
