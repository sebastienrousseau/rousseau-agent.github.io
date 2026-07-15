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
description: "Approval policy reference for rousseau-agent: allow_all, deny_all, and pattern-mode approvers with allow/deny regex rules and a configurable default."
keywords: "approval, approver, pattern mode, allow_all, deny_all, regex, safety, tool call"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/user-guide/approval-policies/"
subtitle: "Deep dive on approver modes with worked config."
tags: "approval, policy, pattern-mode, safety"
title: "审批策略"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approval, approver, pattern mode, allow_all, deny_all, regex, safety, tool call"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "审批策略"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "security"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/user-guide/approval-policies/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/approval-policies/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "审批策略"
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
twitter_description: "Approval policy reference for rousseau-agent: allow_all, deny_all, and pattern-mode approvers with allow/deny regex rules and a configurable default."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "审批策略"
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

## 契约

每次工具调用在执行前都要通过 `Approver.Approve(ctx, ApprovalRequest)`。接口位于 `internal/agent/approver.go`：

```go
type Decision string

const (
    DecisionAllow Decision = "allow"
    DecisionDeny  Decision = "deny"
)

type ApprovalRequest struct {
    ToolName  string
    Input     json.RawMessage
    SessionID string
}

type Approver interface {
    Approve(ctx context.Context, req ApprovalRequest) (Decision, string)
}
```

`Approve` 在热路径上被同步调用；实现必须迅速返回或遵从 `ctx` 取消。

一个带非空原因的 `DecisionDeny` 会把原因作为 `tool_result` 错误浮回给模型。模型于是可以调整（通常是向运维请求澄清）而不是静默失败。这是有意的设计决定 —— 静默拒绝会产生比带注释拒绝更糟的行为。

## 内置三种模式

### `allow_all`

每个工具调用都执行。这是没有配置审批器时的基线行为。

```yaml
agent:
  approver:
    mode: allow_all
```

何时使用：

- 使用 `claudecli` provider 的交互式 `rousseau chat`（Claude Code 在做自己的每次调用审批）。
- 想要精确看到模型会做什么的开发冒烟测试。

### `deny_all`

以单一原因字符串拦截每次工具调用。

```yaml
agent:
  approver:
    mode: deny_all
    reason: "denied by policy for this deployment"
```

何时使用：

- 冒烟测试审批器接线。
- 想看模型*本会*尝试什么、又不让它动手的初步检查姿态。

### `pattern`

按工具的正则 allow / deny 规则。**deny 优先于 allow。** 未匹配的请求回退到 `default`（`allow` 或 `deny`）。

```yaml
agent:
  approver:
    mode: pattern
    default: deny         # 默认安全；未列出的请求被拦截
    reason: "denied by pattern policy"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}
    deny:
      - {tool: bash, match: "rm -rf|sudo|chmod|chown"}
```

## 规则语义

每个 `PatternRule` 有两个字段：

| 字段 | 含义 |
|---|---|
| `tool` | 工具名（`read`、`write`、`edit`、`grep`、`bash` 或任何自定义工具）。为空匹配每个工具。 |
| `match` | 针对模型产出的原始 JSON 输入的 Go RE2 正则。为空匹配每个输入。 |

**匹配顺序：**

1. 对请求测试每条 deny 规则。第一次匹配 → deny。
2. 测试每条 allow 规则。第一次匹配 → allow。
3. 回退到 `default`。空的 `default` 被视为 `deny` —— 默认安全。

deny 总是优先，因为偏好更安全的处置。运维添加一条宽泛的 `allow` 块永远不会意外解锁他们已拒绝的类别。

## 针对原始 JSON 的匹配

`match` 正则针对模型发出的**原始 JSON 输入**运行，而不是针对解析后的字段。这有两个后果：

1. **您匹配的是 JSON 形状。** 对于 `bash` 调用，它看起来是 `{"command":"ls /tmp"}`。匹配 `"command":\s*"ls\s`。
2. **您可以匹配任何字段。** `edit` 工具接收 `{"path":"/x","old_string":"...","new_string":"..."}`；您可以匹配 `path`、`old_string`，或两者。

小心转义 JSON 相关字符：

- 双引号在原始 JSON 中是字面量 —— 若使用 YAML 双引号字符串，在正则中匹配 `\"`。
- 反斜杠在 YAML 中需要加倍：YAML 文件中的 `\\` 在编译后的正则中变成 `\`。

## 可行的匹配模式

### 将编辑限制到某个目录树

```yaml
allow:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/[^\"]*\""}
  - {tool: write, match: "\"path\":\"/workspace/repo/[^\"]*\""}
```

### 白名单安全 shell 命令

```yaml
allow:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|grep|rg|find|git status|git diff|go test) "}
```

### 不管 allow，都拒绝破坏性命令

```yaml
deny:
  - {tool: bash, match: "rm\\s+-rf|sudo|:\\(\\)\\{ :\\|:& \\};:"}
```

### 拒绝对系统目录的写入

```yaml
deny:
  - {tool: write, match: "\"path\":\"/(etc|root|var|usr)/"}
  - {tool: edit,  match: "\"path\":\"/(etc|root|var|usr)/"}
```

## `Default` 字段

`default: deny` 是更安全的处置，也是任何无人值守守护进程的推荐值。`default: allow` 反转模型 —— 每个未列出的调用都运行，`deny` 规则成为主要杠杆。

何时使用 `default: allow`：

- 守护进程运行在一个被严重锁定的容器（[部署](/zh-Hans/deployment/)）中，且容器是您的主要边界。
- 您在做实验，想在决定拦截什么之前先看模型的行为。

在其他地方，都优选 `default: deny`。

## `Reason` 字段

`reason` 是每次拒绝（或 `default: deny` 回退）时返回给模型的字符串。为空则回退到 `denied by pattern policy`（`deny_all` 时为 `denied by policy`）。

设置一个有帮助的原因能改善模型恢复 —— 与其用 `denied by pattern policy`，不如试 `denied — this deployment only allows reads inside /workspace; ask the operator to widen the scope`，然后看模型给出可行的澄清回复。

## 与 `claudecli` 的交互

当 `provider: claudecli` 时，是 Claude Code 在运行工具调用，它自己的权限模式（`bypassPermissions`、`plan`、`default`）也会门禁每次动作。有效行为是交集：**两方**审批器 —— rousseau 与 Claude Code —— 都必须允许该调用才能运行。

建议让两者保持对齐：

- 无人值守：Claude Code 上 `bypassPermissions`，rousseau 上 `mode: pattern` + `default: deny`。
- 只读检查：Claude Code 上 `plan`，rousseau 上 `mode: pattern` 只允许 `read`/`grep`。见 [指南：只读模式](/zh-Hans/guides/read-only-mode/)。

## 审计轨迹

每次审批决定都通过 slog 发出：

| 事件 | 含义 |
|---|---|
| `tool.execute`（INFO） | 调用已批准，运行中。 |
| `tool.denied`（WARN） | 调用被拦截。包含工具名与原因。 |
| `tool.error`（WARN） | 调用运行但失败。 |

管道配方见 [指南：可观测性](/zh-Hans/guides/observability/)。

## 自定义审批器

任何满足 `Approver` 的类型都可以工作。在嵌入代理循环时接线您自己的：

```go
myApprover := agent.ApproverFunc(func(ctx context.Context, req agent.ApprovalRequest) (agent.Decision, string) {
    // 咨询外部策略引擎、提示运维……
    return agent.DecisionAllow, ""
})

ag := agent.New(provider, registry, logger, agent.Options{Approver: myApprover})
```

该接口有意最小化（`Approve` 是唯一方法），因此对接外部策略引擎（OPA、Cedar 或自定义规则引擎）只是一个小适配器。

## 故障排除

### 有匹配的 allow 但每次调用都被拒绝

deny 优先于 allow。`internal/agent/approver.go` 第 152 行的 `PatternApprover.Approve` 先迭代 deny 规则。在 `tool.denied` 日志中查找确切的 `reason` 字符串。

### 启动时的正则编译错误

`PatternApprover` 在首次 `Approve` 时惰性编译正则。编译错误会导致 `DecisionDeny`，原因为 `approver: pattern compile: <err>`。在 [regex101.com](https://regex101.com) 上以 Go 风格测试正则。

### `mode: pattern` 但 `default:` 被忽略

`default:` 只接受 `allow` 与 `deny` 作为有效值。空值或未知值回退到 `DecisionDeny`（安全默认），且不打印警告。

### allow 规则按字面匹配 JSON

正则针对原始工具调用输入 JSON 运行。要匹配 `path` 字段，请转义引号：`"\"path\":\"/workspace/"`。

### 被拒绝的调用不在日志中出现

它们在 —— 以 `warn` 级别的 `tool.denied` 出现。如果您按级别过滤，请确保包含 `warn`。

## 相关页面

- [指南：审计 + 审批策略](/zh-Hans/guides/audit-approval-policies/) —— 带 slog 审计轨迹的可行示例。
- [指南：只读模式](/zh-Hans/guides/read-only-mode/) —— 检查姿态。
- [用户指南：工具](/zh-Hans/user-guide/tools/) —— 审批器门禁的工具。
- [安全](/zh-Hans/security/) —— 信任边界概览。
- [代理循环](/zh-Hans/agent-loop/) —— 审批器被调用之处。

## 延伸阅读

- `internal/agent/approver.go` —— `PatternApprover`、`AllowAllApprover`、`DenyAllApprover`。
- `internal/agent/approver_test.go` —— 测试矩阵。
- `internal/cli/approver.go` —— 配置 → 审批器 翻译。
- `internal/config/config.go` —— `ApproverConfig`、`PatternEntry`。
