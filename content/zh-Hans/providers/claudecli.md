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
description: "Configure the claudecli provider: PermissionMode values, model aliases, auth inheritance, and when to prefer this over the direct API."
keywords: "claudecli, claude CLI, subprocess, PermissionMode, bypassPermissions, acceptEdits, Claude Code"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/providers/claudecli/"
subtitle: "Subprocess against the local Claude Code CLI."
tags: "providers, claudecli"
title: "claudecli 提供方"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "claudecli, claude CLI, subprocess, PermissionMode, bypassPermissions, acceptEdits, Claude Code"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "claudecli 提供方"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 6
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/providers/claudecli/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/claudecli/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "claudecli 提供方"
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
twitter_description: "Configure the claudecli provider: PermissionMode values, model aliases, auth inheritance, and when to prefer this over the direct API."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "claudecli 提供方"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">你将学到</span><p><code>claudecli</code> 提供方如何从本地安装的 Claude Code 继承认证、完整的 <code>PermissionMode</code> 矩阵、会话关联语义、模型别名，以及何时选择它而非 Anthropic 直连 API。请对照阅读 <code>internal/llm/claudecli/client.go</code> 以获取真相。</p></aside>

## 何时使用 claudecli

`claudecli` 将 `claude` CLI（Claude Code）作为子进程调起。它是**默认提供方**，在以下场景是正确选择：

- 你已在本地安装并认证了 Claude Code。
- 你希望复用订阅制 Claude Code 账号，而不是传递 API 密钥。
- 你希望模型在 `claude` 自己的工具使用循环中运行（其文件编辑、思考与 plan 模式功能保持完整）。
- 你希望 rousseau 的配置文件中不出现任何机密材料。

代价：此提供方**不**调用 rousseau 的工具 `Registry`——`claude` 在子进程中运行自己的工具。响应对象作为轮末的单条文本消息返回。如果你需要 rousseau 通过审批策略对 `bash`/`edit`/`write` 进行把关，请改用 `anthropic`、`bedrock`、`vertex` 或 OpenAI 兼容提供方。

## 认证继承

`claude` CLI 在三个位置持有认证：

| 位置 | 内容 |
|---|---|
| `~/.claude/` | OAuth 令牌（订阅）、API-key helper 输出、工作区配置。 |
| 系统钥匙串 | 在 macOS 上，`claude` 可能在登录钥匙串中缓存 refresh token。 |
| `ANTHROPIC_API_KEY` 环境变量 | 若已设置，`claude` 会以 API-key 模式使用它，而不是 OAuth。 |

`claudecli` 从不直接读取这些。每次调用都是 `exec.CommandContext(binary, args...)`——子进程继承父进程的环境与主目录，自行查找凭证。这就是它对个人运维人员来说"零配置"的原因。

<aside class="admonition" data-type="tip"><span class="admonition-title">容器绑定挂载</span><p>在容器中运行 rousseau 时，请把 <code>~/.claude</code> 以读写方式绑定挂载进容器，使 <code>claude</code> 可以就地刷新缓存的 OAuth 令牌：</p></aside>

```ini
Volume=%h/.claude:/home/rousseau/.claude:rw,Z
```

在 SELinux 主机上 `Z` 标签至关重要；完整 Quadlet 单元参见 [部署](/zh-Hans/deployment/)。

## 配置

```yaml
provider: claudecli

claudecli:
  binary: claude
  model: sonnet
  permission_mode: bypassPermissions
  extra_args:
    - --add-dir
    - /workspace
```

| 字段 | 默认值 | 作用 |
|---|---|---|
| `binary` | `claude` | 通过 `$PATH` 解析的可执行文件。如果你有多个 `claude` 版本，请指向绝对路径。 |
| `model` | *空* | 作为 `--model <value>` 传入。为空则使用 `claude` 的默认值。 |
| `permission_mode` | *空* | 作为 `--permission-mode <value>` 传入。参见下表。 |
| `extra_args` | `[]` | 在每次调用时插入到 `-p <prompt>` 前面。 |

每个字段都映射到 `internal/config/config.go` 中的 `ClaudeCLIConfig`。每一轮组装的子进程命令行为：

```sh
claude --print --output-format json \
  --session-id <sessionID> \
  --system-prompt <systemPrompt> \
  --model <model> \
  --permission-mode <permissionMode> \
  <extra_args...> \
  <prompt>
```

<aside class="admonition" data-type="warning"><span class="admonition-title">STDOUT 解析</span><p>Rousseau 期望 <code>claude</code> 在 stdout 上输出一个 JSON 信封。如果你用 shell 脚本包装 <code>claude</code>（用于审计、脱敏或限流），包装器必须原样转发 stdout。解析器容忍在第一个 <code>{</code> 前有一行日志——见 <code>internal/llm/claudecli/client.go</code> 中的 <code>parseResult</code>——但 JSON 信封后的垃圾内容会导致失败。</p></aside>

## PermissionMode 矩阵

`PermissionMode` 选项镜像 `claude` 自身的 `--permission-mode`。该值由子进程强制执行；rousseau 不做二次检查。

<div class="tabs" data-tabs="claudecli-permission-modes">
  <div class="tab-list" role="tablist" aria-label="PermissionMode selector">
    <button role="tab" aria-selected="true">有人值守</button>
    <button role="tab" aria-selected="false">无人值守</button>
    <button role="tab" aria-selected="false">只读</button>
  </div>
  <div class="tab-panel" role="tabpanel">

交互式 TUI 会话——终端前有人可以批准工具调用。

| 模式 | 行为 |
|---|---|
| `default` | Claude Code 对每次工具调用交互式提示。最适合探索性会话。 |
| `acceptEdits` | 文件编辑无提示执行；其他工具仍会提示。当你信任编辑面时合适。 |
| `auto` | 按工具自动判断。希望 claude 内置启发式做决定时使用。 |

```yaml
claudecli:
  permission_mode: acceptEdits
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

聊天传输（WhatsApp、Slack、Discord、Signal 等）没有人在终端前应答提示。

| 模式 | 行为 |
|---|---|
| `bypassPermissions` | 每次工具调用都无提示执行。接受完整的爆炸半径。 |
| `dontAsk` | 别名，处理方式类似 bypass。 |

```yaml
claudecli:
  permission_mode: bypassPermissions
```

如果运维人员未指定，CLI 会为无人值守守护进程自动设置 `bypassPermissions`——见 `internal/cli` 中的 `setUnattendedPermissionDefault`。

<aside class="admonition" data-type="caution"><span class="admonition-title">爆炸半径</span><p><code>bypassPermissions</code> 让模型以守护进程权限直接访问 <code>bash</code>。请与 (a) 已加固的容器、(b) 允许列表、(c) rousseau 侧的 pattern 模式审批器结合使用——或使用非 <code>claudecli</code> 提供方，让 rousseau 在工具运行前强制执行审批。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

用于大型重构或代码审查的探索模式，不希望进行任何写入。

| 模式 | 行为 |
|---|---|
| `plan` | 规划模式。允许 read 与 grep；抑制写入。 |

```yaml
claudecli:
  permission_mode: plan
```

与 rousseau 自身的只读模式（见 [指南：只读模式](/zh-Hans/guides/read-only-mode/)）配合可实现双重保险。

  </div>
</div>

## 会话关联

`claudecli` 在子进程内维护对话状态。Rousseau 通过两个选项将自身会话 ID 与 `claude` 的对应：

- `claude -p --session-id <uuid>` 创建新会话。若 UUID 已存在，`claude` 报错 `already in use`。
- `claude -p --resume <uuid>` 恢复现有会话。若未知，`claude` 报错。

Rousseau 借助内存中的 `SessionCache`（默认为 `InMemorySessionCache`）选择相应选项。在冷启动缓存未命中且 `claude` 已保存了先前 rousseau 运行的状态时，提供方会乐观地先尝试 `--session-id`，捕获 `already in use` 错误后以 `--resume` 重试。参见 `internal/llm/claudecli/client.go` 中 `(*Provider).Complete` 的注释。

嵌入该提供方的调用方可以通过 `provider.WithCache(store)` 替换为持久缓存——`state.sqlite` 存储实现同一接口并可跨守护进程重启存活，从而避免重启后首轮的冷启动往返。

## 模型别名

`claude` 的模型别名会被子进程原样识别：

| 别名 | 指向 |
|---|---|
| `sonnet` | 当前默认的 Sonnet 级模型。 |
| `opus` | 当前默认的 Opus 级模型。 |
| `haiku` | 当前默认的 Haiku 级模型。 |

为在守护进程重启间保持可复现性（技能基准、定时任务、批量运行），请固定精确的模型 ID：

```yaml
claudecli:
  model: claude-sonnet-4-6
```

<aside class="admonition" data-type="note"><span class="admonition-title">别名随发布变化</span><p>当 Anthropic 发布新模型时，别名会移动。2026 年 7 月的 <code>sonnet</code> 别名并不指向 2026 年 4 月 <code>sonnet</code> 别名所指向的相同权重。如果你的工作流依赖特定行为，请固定精确 ID。</p></aside>

## 与技能结合

`claudecli` 在会话创建时通过 `--system-prompt` 发送系统提示。`claude` 会原样接受，在 `--resume` 时忽略后续的 `--system-prompt` 值——这正符合 rousseau 的使用方式。`SkillsProvider` 的输出会在调用前拼接：

```
<agent.SystemPrompt>

<skill 1 markdown>

<skill 2 markdown>

<RecallProvider appendix>
```

参见 `internal/agent/agent.go` 中的 `systemPrompt()`。技能在所有提供方间的工作方式一致；组合机制发生在 `agent.Agent` 中，而非提供方。

<aside class="admonition" data-type="tip"><span class="admonition-title">提示缓存</span><p>Anthropic 直连提供方会把系统提示标记为临时提示缓存（见 <code>internal/llm/anthropic/cache.go</code>）。<code>claudecli</code> 不会——<code>claude</code> 在内部拥有自己的缓存。若你希望获得可衡量的提示缓存节省，请使用 <code>provider: anthropic</code>。</p></aside>

## 注意事项

- **不可跨提供方迁移。** 基于 `claudecli` 创建的会话不能移植到 `anthropic`——模型侧状态存在于 `claude` 内部。中途切换提供方会强制开启新会话。
- **不调用工具注册表。** `bash`、`edit`、`write`、`grep`、`read` 由 `claude` 执行，而非 `rousseau`。Rousseau 的 `agent.Approver` 无法把关这些调用。如果你需要 rousseau 侧的审批强制执行，请使用非 `claudecli` 提供方。
- **`--add-dir` 作用域。** `claude` 默认拒绝读取其自身工作区之外的内容。通过 `extra_args` 传入 `--add-dir /workspace`（或你的源码所在位置）以扩大范围。如需弥补控制上的损失，可在传输层结合 rousseau 的审批策略。
- **流式传输。** `claudecli` 使用 `claude -p --output-format json`（非流式）。`internal/llm/claudecli/stream.go` 中的流式路径读取 `--output-format stream-json`；在嵌入式集成中通过 `StreamingProvider` 开启。
- **环境泄漏。** 子进程继承父进程的所有环境变量。若 rousseau 的环境中设置了 `ANTHROPIC_API_KEY`，`claude` 会优先使用它而非缓存的 OAuth。通常无碍，但会改变计费方式。

## 故障排查

### `claudecli: run: exec: "claude": executable file not found in $PATH`

`claude` 不在 `PATH` 中（或容器镜像未附带）。两种修复：

1. 将 `claudecli.binary` 设为绝对路径。
2. 在容器的运行时层添加 Claude Code——参考 `docker/Dockerfile` 正是出于此原因使用 `node:22-alpine`。

### `claudecli: model error: session id already in use`

你在同一 `claude` 安装上运行了两个针对同一会话 ID 的 rousseau 进程，或者内存缓存丢弃了 `claude` 仍然记得的会话。上文描述的乐观重试处理第二种情况；第一种意味着你有并发守护进程相互干扰。

### `claudecli: no JSON in output`

`claude` 向 stdout 打印了非 JSON，或在发出信封前退出。常见原因：Claude Code 侧的 API 密钥无效、`claude` 版本早于 `--output-format json`，或包装脚本写入进度标记。直接运行 `claude -p --output-format json 'hello'` 进行隔离。

### 回复中途被截断

`claude` 的输出受 `--max-turns` 和其内部 token 预算限制。Rousseau 不设置 `--max-turns`；若你通过 `extra_args` 设置了，请提高该值。对于长生成，可以考虑使用直连 API 提供方，从 `internal/llm/anthropic/client.go` 控制 `MaxTokens`。

### 订阅计划被限流但 API 正常

订阅计划的 `claude` CLI 有隐藏的按对话与按窗口限制。若命中，请切换到 `provider: anthropic` 并使用 API 密钥——直连 API 有明确的公开限制（参见 [指南：速率限制](/zh-Hans/guides/rate-limits/)）。

## 相关页面

- [提供方：Anthropic](/zh-Hans/providers/anthropic/)——带提示缓存与流式传输的直连 API。
- [提供方：Bedrock](/zh-Hans/providers/bedrock/)——AWS 托管的 Claude。
- [用户指南：审批策略](/zh-Hans/user-guide/approval-policies/)——如何在 rousseau 层把关工具调用。
- [技能](/zh-Hans/skills/)——系统提示附录的组合方式。
- [配置](/zh-Hans/configuration/)——上下文中的 `claudecli` 配置块。

## 延伸阅读

- `internal/llm/claudecli/client.go`——子进程调用、会话关联、JSON 解析。
- `internal/llm/claudecli/stream.go`——使用 `--output-format stream-json` 的流式变体。
- `internal/config/config.go`——`ClaudeCLIConfig` 结构体。
- `internal/cli/root.go`——`setUnattendedPermissionDefault` 如何为聊天传输选择 `bypassPermissions`。
