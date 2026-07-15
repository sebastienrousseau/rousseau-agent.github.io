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
description: "Worked example: lock down the bash tool with a pattern-mode approver, deny rules on destructive commands, and slog-driven audit trail."
keywords: "approval policy, pattern mode, bash tool, deny rules, audit trail, slog"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/guides/audit-approval-policies/"
subtitle: "Pattern-mode approver with deny rules on the bash tool."
tags: "guides, audit, approval, pattern-mode, bash, deny"
title: "指南：审计与审批策略"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approval policy, pattern mode, bash tool, deny rules, audit trail, slog"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "指南：审计与审批策略"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 34
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/guides/audit-approval-policies/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/audit-approval-policies/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "指南：审计与审批策略"
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
twitter_description: "Worked example: lock down the bash tool with a pattern-mode approver, deny rules on destructive commands, and slog-driven audit trail."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "指南：审计与审批策略"
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

## 问题

无人值守的聊天传输守护进程在终端旁没有真人实时审批工具调用。如果模型想要运行 `rm -rf /workspace/*`，必须有东西阻止它。Rousseau 的 `pattern` 模式审批器就是这个杠杆。

威胁并不是模型自己失控 —— 而是通过传输通道到达守护进程的、被劫持或错位的指令。带有 `default: deny` 回退的 pattern 模式策略使风险有界且可审计。

## 审批器模式

内置三种模式（见 `internal/agent/approver.go`）：

| 模式 | 行为 | 何时使用 |
|---|---|---|
| `allow_all` | 每个工具调用都执行。 | 交互式 `rousseau chat`，其中 `claudecli` provider 正在做自己的审批。 |
| `deny_all` | 每个工具调用都被拦截。拒绝原因会作为 `tool_result` 错误暴露给模型以便它调整。 | 只读检查姿态；冒烟测试。 |
| `pattern` | 按工具的正则 allow / deny 规则。**deny 优先于 allow。** 未匹配的请求回退到 `default`。 | 任何生产中的无人值守守护进程。 |

## 可行配置

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by pattern policy — ask the operator"
    allow:
      # Read-side tools: no restriction inside the workspace.
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

      # Edit inside /workspace only.
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}

      # Write inside /workspace only.
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}

      # Shell commands: whitelist of safe read-side utilities plus git status/diff.
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|grep|rg|find|wc|stat|file|which|pwd|env|git status|git diff|git log|go test|go vet|go build)\\b"}

    deny:
      # Absolute deny rules override any allow above.
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s|ncat"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}   # fork bomb
      - {tool: write, match: "\"path\":\"/etc/|/root/|/var/"}
      - {tool: edit, match: "\"path\":\"/etc/|/root/|/var/"}
```

从 `PatternApprover.Approve` 派生出两条重要属性：

1. **deny 优先。** 在任何 allow 规则之前先检查每条 deny 规则。这比反过来更安全：运维人员添加一条宽泛的 allow 也永远不会意外解锁他们以为已被拒绝的类别。
2. **未匹配 → deny。** 在 `default: deny` 下，运维忘记枚举的任何工具调用都会被拦截。这是默认安全的姿态；若要反过来，设为 `default: allow`。

## 阅读审计轨迹

每次工具调用与每次拒绝都通过 slog logger 发出：

```
INFO tool.execute name=read id=t_1
INFO tool.execute name=grep id=t_2
WARN tool.denied  name=bash reason="denied by pattern policy — ask the operator"
```

守护进程使用 `slog`，其级别与格式可配置（`log.level`、`log.format`）。生产环境建议 `format: json`，以便下游工具（Loki、Vector、Datadog）干净地解析。管道配方见 [指南：可观测性](/zh-Hans/guides/observability/)。

每一次拒绝都携带一个稳定的结构化键：

- `tool.denied` —— 工具调用被拦截。字段：`name`（工具标识符）、`reason`（来自 `PatternApprover.DenyReason` 或内置回退）。
- `tool.execute` —— 工具调用已运行。字段：`name`、`id`（模型发出的调用 ID，用于关联）。
- `tool.error` —— 工具运行但失败。字段：`name`、`err`。

在 `tool.denied` 上做 `slog` 过滤即可得到大多数合规框架所要求的"已拦截尝试"审计视图。

## 测试策略

源代码树中的 `internal/agent/approver_test.go` 用一个宽泛的矩阵演练 `PatternApprover`。要冒烟测试您自己的规则：

```sh
rousseau chat
> Run `rm -rf /tmp/foo` for me.
```

模型会尝试 `bash` 工具调用。守护进程记录 `tool.denied` 并把 `reason` 字符串返回给模型，模型通常会转向（"我不能运行那个 —— 你能告诉我你想做什么吗？"）。

参考测试矩阵见 `internal/agent/approver_test.go` —— 相同的规则形状在那里被演练。

## 添加手动覆盖

有时候运维人员想手动审批某次危险调用。最简单的模式：

1. 在 `rousseau chat`（交互式 TUI）中设 `mode: allow_all`。`claudecli` provider 处理自己的每次调用审批提示。
2. 在每个无人值守的守护进程里保持 `mode: pattern`。

如今聊天传输上没有交互式的每次调用审批 UI —— 安全故事完全由正则 + slog 组成。

## 该策略不做什么

- **不沙箱化工具。** 通过审批器的 `bash` 调用以守护进程的 UID 及其文件系统可见性运行。在其下层叠一个 rootless 容器（[部署](/zh-Hans/deployment/)）。
- **不做速率限制。** 每秒允许十次 `bash` 调用是被允许的。如需速率限制，包装工具注册表。
- **不审计出站网络调用。** 如果 `bash` 调用向外 curl，审批器看不到 URL —— 只看到初始的 `bash` `command` 字符串。在 pattern 层直接拒绝 `curl` 与 `wget`。

## 常见模式

### 将编辑锁定到某个目录树

```yaml
allow:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/[^\"]*\""}
  - {tool: write, match: "\"path\":\"/workspace/repo/[^\"]*\""}
deny:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/(\\.git|node_modules|vendor)/"}
```

### 只读审计员

```yaml
mode: pattern
default: deny
allow:
  - {tool: read, match: ".*"}
  - {tool: grep, match: ".*"}
```

与 `provider.claudecli.permission_mode: plan` 结合，会得到一个只读检查姿态 —— 见 [指南：只读模式](/zh-Hans/guides/read-only-mode/)。

### 以 Git 为先的工作流

```yaml
allow:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"git (status|diff|log|show|branch|stash|fetch|pull --ff-only)\\b"}
deny:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"git (push|reset --hard|clean -fd|checkout --)\\b"}
```

## 五套参考规则集

<div class="tabs" data-tabs="approval-rulesets">
  <div class="tab-list" role="tablist" aria-label="Reference ruleset">
    <button role="tab" aria-selected="true">开发笔记本</button>
    <button role="tab" aria-selected="false">Staging</button>
    <button role="tab" aria-selected="false">生产</button>
    <button role="tab" aria-selected="false">Oncall 机器人</button>
    <button role="tab" aria-selected="false">只读</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**开发笔记本。** 默认宽松，拒绝真正危险的操作。假设有人守着终端。

```yaml
agent:
  approver:
    mode: pattern
    default: allow
    deny:
      - {tool: bash, match: "rm\\s+-rf\\s+/"}
      - {tool: bash, match: "sudo(?!\\s+-n)"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}
      - {tool: write, match: "\"path\":\"/etc/|/root/"}
      - {tool: edit, match: "\"path\":\"/etc/|/root/"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Staging。** 为 workspace 明确列出允许列表，拒绝之外的一切。适合影响半径有限的共享 staging 守护进程。

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by staging policy — ping #platform for exceptions"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: bash, match: "^\\{\"command\":\"git (status|diff|log|show|branch|fetch|pull --ff-only)\\b"}
      - {tool: bash, match: "^\\{\"command\":\"(ls|cat|grep|rg|find)\\s"}
    deny:
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s"}
      - {tool: edit, match: "\"path\":\"/workspace/(\\.git|node_modules|vendor)/"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**生产。** 拒绝优先。每个被允许的命令都明确枚举。适合回答面向客户问题的生产守护进程。

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by production policy — this daemon is read-mostly"
    allow:
      - {tool: read, match: "\"path\":\"/workspace/(runbooks|docs|src)/"}
      - {tool: grep, match: "\"path\":\"/workspace/(runbooks|docs|src)/"}
      - {tool: bash, match: "^\\{\"command\":\"(ls|cat|rg)\\s"}
    deny:
      # Layered denies just in case.
      - {tool: write, match: ".*"}
      - {tool: edit, match: ".*"}
      - {tool: bash, match: "\\b(rm|mv|cp|dd|mkfs|kill|killall)\\b"}
      - {tool: bash, match: "\\b(curl|wget|nc|ncat|ssh|scp|rsync)\\b"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Oncall 机器人。** 可以查询监控、跟踪日志，但不能重启服务或编辑代码。适合面向 Slack 的事件响应助手。

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied — oncall bot can query, not mutate"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\{\"command\":\"(kubectl|helm|argocd) (get|describe|logs|top|status)\\b"}
      - {tool: bash, match: "^\\{\"command\":\"(curl|http|wget) -[gsL]* https?://monitoring\\."}
      - {tool: bash, match: "^\\{\"command\":\"(pg_dump|psql -c 'SELECT|redis-cli GET)\\b"}
    deny:
      - {tool: write, match: ".*"}
      - {tool: edit, match: ".*"}
      - {tool: bash, match: "\\b(kubectl (apply|delete|edit|scale)|helm (install|upgrade|uninstall))\\b"}
      - {tool: bash, match: "\\b(systemctl (start|stop|restart|reload))\\b"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**只读审计员。** 没有写入，没有 shell。适合代码评审机器人或文档解释类守护进程。

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "read-only auditor — no side effects permitted"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
```

与 `provider.claudecli.permission_mode: plan` 和 `provider.claudecli.extra_args: ["--allowed-tools", "read,grep"]` 组合以做双重保险 —— 模型根本无法请求其他工具。

  </div>
</div>

## 故障排除

### 尽管我有 allow 规则，每次调用都被拒绝

deny 优先于 allow。检查是否有一条 deny 规则意外匹配。日志行 `tool.denied name=<X> reason=<Y>` 包含确切原因。

### Pattern 正则编译错误

`PatternApprover` 在首次使用时惰性编译规则。编译错误会变成一个 `DecisionDeny`，原因为 `approver: pattern compile: <err>`。修复正则；打开 regex101.com 并选择 Go 风格是您的好帮手。

### 正则按字面而非按语义匹配 JSON

`match` 正则针对工具调用的原始 JSON 输入运行。适当转义引号与反斜杠：`"\"path\":\"/workspace/"` 匹配一个 `edit` 或 `write` 调用的 `path` 字段。

### `deny_all` 没有拦截任何东西

确认是 `mode: deny_all`（而非 `mode: deny`）。有效模式是 `allow_all`、`deny_all`、`pattern`。单独的 `allow` 与 `deny` 会被当作 `_all` 变体的别名，但准确字符串更安全。

### `bash` 的 allow 规则永远不匹配

`bash` 的输入是形如 `{"command":"ls -la"}` 的 JSON。匹配那段 JSON 字面量，而不仅仅是 shell 命令字符串。使用类似 `^\\{\"command\":\"ls` 的模式。

## 相关页面

- [用户指南：审批策略](/zh-Hans/user-guide/approval-policies/) —— 更深入的参考与可行示例。
- [用户指南：工具](/zh-Hans/user-guide/tools/) —— 每个内置工具的 schema。
- [指南：可观测性](/zh-Hans/guides/observability/) —— 让审计轨迹浮出水面。
- [指南：只读模式](/zh-Hans/guides/read-only-mode/) —— 双重保险式执行。
- [安全](/zh-Hans/security/) —— 信任模型概览。

## 延伸阅读

- `internal/agent/approver.go` —— `PatternApprover`、`AllowAllApprover`、`DenyAllApprover`。
- `internal/agent/approver_test.go` —— 测试矩阵。
- `internal/cli/approver.go` —— 配置 → 审批器 翻译。
- `internal/config/config.go` —— `ApproverConfig`、`PatternEntry`。
