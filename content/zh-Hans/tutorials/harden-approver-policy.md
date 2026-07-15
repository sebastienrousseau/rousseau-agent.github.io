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
description: "Go from bypassPermissions to a pattern-mode approver with default: deny and validate the audit trail through slog."
keywords: "approver, pattern mode, default deny, tool denied, audit, slog"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/tutorials/harden-approver-policy/"
subtitle: "From bypassPermissions to default-deny with slog-audited rule matching."
tags: "tutorials, approver, pattern-mode, security, audit"
title: "教程：加固审批器"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approver, pattern mode, default deny, tool denied, audit, slog"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "教程：加固审批器"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 46
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/tutorials/harden-approver-policy/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/harden-approver-policy/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "教程：加固审批器"
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
twitter_description: "Go from bypassPermissions to a pattern-mode approver with default: deny and validate the audit trail through slog."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "教程：加固审批器"
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

## 您将构建什么

一个原本以 `bypassPermissions` 模式（无人值守默认）运行 `claudecli` provider 的 rousseau 守护进程，最后落入一个 `default: deny` 的 `pattern` 模式 rousseau-agent 审批器之下。每次工具调用要么被显式加入允许列表，要么被拦截；每次拒绝都会产生一个可审计的 `tool.denied` slog 事件。

预计时间：30 分钟做一次带测试的正式规则梳理。

## 先决条件

- 已安装 rousseau，且任一传输桥在运行（WhatsApp、Slack、Signal —— 任何无人值守）。
- 基本 Go 正则熟悉度 —— 审批器规则是对 JSON 工具输入的 Go RE2 正则。

## 审批器住在哪里

两个独立层可以批准工具调用：

1. **provider 自己的权限模式。** `claudecli` provider（`internal/llm/claudecli/client.go`）委托给 `claude --permission-mode`。`ClaudeCLIConfig.PermissionMode`（`internal/config/config.go`）中记录的值：`acceptEdits`、`auto`、`bypassPermissions`、`default`、`dontAsk`、`plan`。无人值守守护进程在 `setUnattendedPermissionDefault` 中固定为 `bypassPermissions`。
2. **Rousseau 自己的审批器。** 在 `agent.approver` 下配置（`internal/config/config.go` 的 `ApproverConfig`；实现在 `internal/agent/approver.go`）。三种模式：`allow_all`、`deny_all`、`pattern`。**deny 优先于 allow，未匹配的调用回退到 `default`。**

对无人值守的守护进程，rousseau 审批器是您手动配置的缓解。`claudecli` 自己的模式是安全带。

## 第 1 步：基线审计

在写规则之前，用 `mode: allow_all` 与 `log.format: json` 跑几次真实会话。每次工具调用都发出 `tool.execute`（`internal/agent/agent.go`）：

```sh
jq -c 'select(.msg == "tool.execute") | {name, input: .input}' \
  < /var/log/rousseau.jsonl \
  | sort | uniq -c | sort -rn | head
```

您现在得到一份代理使用哪些工具、针对哪些路径的经验分布。那是允许列表的种子。

## 第 2 步：起草一份 pattern 策略

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by pattern policy — ask the operator to loosen the rules"
    allow:
      # 读侧：在守护进程的文件系统视图内不受限。
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

      # 编辑锚定到 /workspace。
      - {tool: edit,  match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}

      # Shell：只读实用命令的白名单 加 git status/diff/log。
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|grep|rg|find|wc|stat|file|which|pwd|env|git status|git diff|git log|go test|go vet|go build)\\b"}

    deny:
      # 绝对 deny 覆盖任何上面的 allow。
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s|ncat"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}    # fork bomb
      - {tool: write, match: "\"path\":\"/etc/|/root/|/var/"}
      - {tool: edit,  match: "\"path\":\"/etc/|/root/|/var/"}
```

部署并观察 slog 流。相关事件（`internal/agent/agent.go`）：

- `tool.execute` —— 调用已运行。字段：`name`、`id`。
- `tool.denied` —— 审批器拦截了它。字段：`name`、`reason`。
- `tool.error` —— 它运行了但失败。字段：`name`、`err`。

## 第 3 步：迭代

头一天会浮出误报：审批器拦截了合法的工具调用。grep 出它们：

```sh
jq -c 'select(.msg == "tool.denied") | {name, input}' \
  < /var/log/rousseau.jsonl \
  | sort | uniq -c | sort -rn | head
```

每一条反复出现的 `tool.denied` 都值得决策：

- **确实需要** —— 扩展 allow 规则。首选窄的（路径锚定）而不是宽的（开放正则）。
- **不需要** —— 保持拒绝。模型会转向另一种方法。

不要削弱 `default: deny`。那正是让被遗忘的工具依然安全的属性。

## 第 4 步：审计日志摘录

带一个陌生提示的一次生产运行看起来像这样：

```jsonl
{"time":"2026-07-13T18:00:12Z","level":"INFO", "msg":"whatsapp.incoming","from":"447900123456@s.whatsapp.net"}
{"time":"2026-07-13T18:00:14Z","level":"INFO", "msg":"tool.execute","name":"grep","id":"t_1"}
{"time":"2026-07-13T18:00:15Z","level":"INFO", "msg":"tool.execute","name":"read","id":"t_2"}
{"time":"2026-07-13T18:00:17Z","level":"WARN", "msg":"tool.denied","name":"bash","reason":"denied by pattern policy — ask the operator to loosen the rules"}
{"time":"2026-07-13T18:00:18Z","level":"INFO", "msg":"tool.execute","name":"read","id":"t_3"}
{"time":"2026-07-13T18:00:20Z","level":"INFO", "msg":"whatsapp.handler_ok","elapsed":"7.4s"}
```

这里唯一的 `tool.denied` 是 `bash: "curl https://…"`。deny 规则捕获了它，模型退化到 `read` + `grep`，回复仍然发出。

## 第 5 步：固化

一旦误报率稳定，冻结配置，把它提交到源代码控制（排除 secret —— 见 [指南：企业接入](/zh-Hans/guides/enterprise-onboarding/)），并在代码评审之后再允许配置变更。源代码树中的 `internal/agent/approver_test.go` 是您如何为规则集编写测试的模型 —— 若您希望 CI 抓到被破坏的策略，把它的形状复制到一个内部包中。

## 该策略仍不做的

即使有最紧的 pattern 规则：

- **不沙箱化。** 一次允许的 `bash` 调用仍以守护进程的 UID 与文件系统可见性运行。在其下叠加一个 rootless 容器（[部署](/zh-Hans/deployment/)）。
- **不做速率限制。** 每秒十次允许的调用都被允许。如果需要，请包装工具注册表。
- **不做出站网络审计。** 审批器看到的是初始的 `bash` `command` 字符串，而不是它 curl 的东西。直接拒绝 `curl` 与 `wget` —— 示例 deny 规则这么做。

更深入的讨论见 [指南：审计 + 审批策略](/zh-Hans/guides/audit-approval-policies/)。

## 相关

- [用户指南：审批策略](/zh-Hans/user-guide/approval-policies/) —— 每种模式的参考。
- [用户指南：工具](/zh-Hans/user-guide/tools/) —— 工具 schema，对写正则有用。
- [指南：可观测性](/zh-Hans/guides/observability/) —— 把 `tool.denied` 管道到 Loki/Datadog。
- [参考：日志](/zh-Hans/reference/logs/) —— 每个知名的 slog 消息。
