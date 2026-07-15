---

# Front Matter (YAML)

author: "sebastian.rousseau@gmail.com (Sebastien Rousseau) "
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
description: "Configure rousseau-agent as a read-only inspection agent: deny_all approver with a read/grep exception, plan-mode claudecli, read-only bind mounts."
keywords: "read-only, inspection, deny_all, plan mode, bind mount, ro mount, audit"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/guides/read-only-mode/"
subtitle: "An inspection posture that cannot mutate the workspace."
tags: "guides, read-only, deny_all, plan-mode"
title: "指南：只读模式"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "read-only, inspection, deny_all, plan mode, bind mount, ro mount, audit"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "指南：只读模式"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 36
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/guides/read-only-mode/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/read-only-mode/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "指南：只读模式"
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
twitter_description: "Configure rousseau-agent as a read-only inspection agent: deny_all approver with a read/grep exception, plan-mode claudecli, read-only bind mounts."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "指南：只读模式"
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

## 场景

您希望 rousseau 检查一个仓库、回答关于它的问题、生成报告 —— 但它不能写入、编辑或运行破坏性 shell 命令。这是您在首轮审计、事件响应检查或合规审查时会部署的姿态。

三层叠加以使其牢固：

1. **审批策略** —— 拒绝每一个改动型工具。
2. **`claudecli` 权限模式** —— 把 Claude Code 置于 `plan` 模式，让它自身的审批器永不编辑文件。
3. **文件系统** —— 以只读方式 bind-mount 工作区。

腰带、背带，再加第二条腰带。三者中任何一个失败都能安全兜底。

## 第 1 层 —— 审批器

最简单的只读姿态是带白名单的 `pattern` 审批器：

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "read-only inspection posture — this deployment cannot mutate files"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|find|wc|stat|file|which|pwd|env|git status|git diff|git log|git show|git branch)\\b"}
    # 无需 deny 规则 —— default: deny 会捕获其他一切。
    # 没有 edit、write 或不受限的 bash —— 模型触及不到它们。
```

一个更严格的变体使用 `deny_all`，它会拦截包括 `read` 与 `grep` 在内的每一个工具：

```yaml
agent:
  approver:
    mode: deny_all
    reason: "smoke test — no tool calls allowed"
```

`deny_all` 只作为冒烟测试有用；模型将无法做任何有意义的工作。

## 第 2 层 —— `claudecli` 权限模式

当 provider 是 `claudecli` 时，是 Claude Code 自己在运行工具调用。设置 `permission_mode: plan` 会让 Claude Code 在它自己的层面上拒绝每一个写入或编辑侧调用，即使 rousseau 审批器本会允许：

```yaml
provider: claudecli

claudecli:
  binary: claude
  permission_mode: plan
```

有效值（见 `internal/config/config.go` 与 Claude Code 的文档）：`acceptEdits`、`auto`、`bypassPermissions`、`default`、`dontAsk`、`plan`。`plan` 是唯一能持续将 Claude Code 保持在只读姿态的值。

## 第 3 层 —— 文件系统

以只读方式挂载工作区。参考 Podman Quadlet 下：

```
Volume=%h/team-rousseau-workspace:/workspace:ro,Z
```

从容器角度看，`ro` 让挂载只读；即使一个被劫持的二进制试图以 `O_WRONLY` 调用 `open(2)`，内核也会返回 `EROFS`。

在 Kubernetes 下：

```yaml
volumeMounts:
  - name: workspace
    mountPath: /workspace
    readOnly: true
```

会话存储（`~/.local/share/rousseau/`）仍然需要可写 —— 守护进程在每一轮都会向它追加。该挂载保持 `rw`，只把工作区留为只读。

## Dry-run 姿态

守护进程上没有 `--dry-run` flag。如果您想让模型*规划*变更但不执行它们，上述组合达成等价效果：

- 审批器拦截每一个改动型工具 → 模型收到解释拦截的 `tool_result` 错误。
- `claudecli` 中的 `plan` 模式阻止 Claude Code 运行它自己的破坏性工具。
- 只读挂载阻挡任何漏过的东西。

模型通常会回复一份规划文档而不是一个 diff。这就是只读检查的交付物。

## 仍然可用的东西

- 每一个 `read` 与 `grep` 调用。
- 您所枚举的安全读侧实用命令的 `bash`。
- 会话持久化 —— SQLite 存储仍然记录对话。
- 通过 FTS5、MCP 导出、skills 的跨会话回忆 —— 总之都是只读的。

## （有意）失效的东西

- `write` 与 `edit` —— 拒绝。
- Shell 改动命令 —— 拒绝。
- 提示暗示文件写入的 Cron 任务 —— 模型尝试、被拒绝、以规划回复。
- `rousseau init` —— CLI 不受审批器影响，但它写入位于工作区之外的 `~/.config/rousseau/`。在推出只读模式前运行它。

## 测试该姿态

```sh
rousseau chat
> Edit /workspace/README.md to add a footer.
```

预期日志行：

```
WARN tool.denied name=edit reason="read-only inspection posture — this deployment cannot mutate files"
```

预期聊天回复：模型道歉，以文本形式给出规划或 diff 补丁，并请求运维应用它。

对于 `deny_all` 变体，每一个工具调用都被拦截 —— 模型无法检查任何东西，因此该姿态只作为冒烟测试有用。

## 与其他传输分层

同样的三层适用于 WhatsApp、Slack、Discord 和任何其他传输。由于审批器运行在代理循环内部，它并不关心是哪条传输送达了用户轮次。一个只读的 Slack 代理只需一个 `mode: pattern` 块。

## 注意事项

- 只读姿态由 rousseau 的审批器与文件系统执行 —— **不是**由 LLM 执行。模型仍然可以发出 `edit` 工具调用；审批器会静默地拦截它，但该尝试会被记录为 `tool.denied`。这是有意的，让审计轨迹记录模型尝试过什么，而不仅是成功了什么。
- 只读 bind mount 不能防止指向挂载点之外的符号链接。参考 Podman 姿态放弃了所有能力，可以防止大多数逃逸路径，但不要只依赖挂载。
- `claudecli` provider 的 `plan` 模式是 Claude Code 的契约，不是 rousseau 的。如果 Claude Code 改变其权限模式语义，rousseau 的只读姿态会继承该变化。

## 下一步

- [用户指南：审批策略](/zh-Hans/user-guide/approval-policies/) —— 更深入的参考。
- [审计 + 审批策略](/zh-Hans/guides/audit-approval-policies/) —— 改动型的对照篇。
- [部署](/zh-Hans/deployment/) —— 挂载与容器 flag。
