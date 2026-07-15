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
changefreq: "weekly"
description: "Embed rousseau-agent's agent loop into your own Go binary. Provider and StreamingProvider interfaces, Session/Message/Turn shapes, tool registration, approval policies, compression, FTS5 recall."
keywords: "library, embedding, agent.Provider, agent.Session, agent.Turn, tool registry, approver, compression, FTS5, recall"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/agent-loop/"
subtitle: "库嵌入契约：Provider、Registry、Session、Turn。"
tags: "library, embedding, reference"
title: "Agent 循环参考"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "library, embedding, agent.Provider, agent.Session, agent.Turn, tool registry, approver, compression, FTS5, recall"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Agent 循环参考"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 22
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/agent-loop/index.html"
item_link: "https://docs.rousseau-agent.dev/agent-loop/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Agent 循环参考"
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
twitter_description: "Embed rousseau-agent's agent loop into your own Go binary. Provider and StreamingProvider interfaces, Session/Message/Turn shapes, tool registration, approval policies, compression, FTS5 recall."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Agent 循环参考"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">你将学到</span><p>一次 <code>Agent.Turn</code> 的完整剖析：<code>Compressor</code>、<code>SkillsProvider</code> 和 <code>RecallProvider</code> 如何组合系统提示词，模型的 <code>tool_use</code> 块如何经过 <code>Approver</code>，工具结果如何被折回到会话中，以及循环如何终止。请配合 <code>internal/agent/agent.go</code> 一起阅读本页。</p></aside>

## rousseau 作为库

`rousseau-agent` 既是守护进程，也是一个库。agent loop、工具注册表和 provider 抽象都不依赖 CLI。你可以把它们组合进自己的二进制，而无需引入 `internal/cli` 或任何传输包。

每个导出的标识符都有 godoc 注释。`pkg.go.dev/github.com/sebastienrousseau/rousseau-agent` 呈现完整参考。

## 一次 Turn 的剖析

`Agent.Turn` 函数定义在 `internal/agent/agent.go` 中。用文字描述，一次 turn 做了如下事情：

```
Turn(ctx, session)
  │
  ├── 1. Session guard: empty session → ErrEmptySession
  │
  ├── 2. Compressor.Compress(ctx, session)
  │     • If enabled and len(messages) > TriggerMessages, summarise older
  │       messages in place. Sets CacheableMessages on next Request.
  │
  ├── 3. registry.Definitions() → toolDefs
  │
  └── loop up to MaxIterations (default 32) times:
        │
        ├── a. Build Request{
        │       SessionID:         session.ID,
        │       System:            systemPrompt(session),
        │       Messages:          session.Messages,
        │       Tools:             toolDefs,
        │       CacheableMessages: <hint from compressor>,
        │     }
        │
        ├── b. resp = provider.Complete(ctx, req)
        │
        ├── c. session.Append(resp.Message)
        │
        ├── d. Switch on resp.StopReason:
        │       • StopEndTurn → return resp.Message (success)
        │       • StopMaxTokens / StopOther → return resp.Message
        │       • StopToolUse → continue to (e)
        │
        ├── e. runTools(ctx, resp.Message, sessionID):
        │       For each tool_use block:
        │         • registry.Get(name) → tool or ErrToolNotFound
        │         • approver.Approve(...)
        │             DecisionDeny → tool_result with is_error=true and reason
        │             DecisionAllow → tool.Execute(ctx, input)
        │               err → tool_result with is_error=true and err.Error()
        │               ok  → tool_result with output
        │
        └── f. session.Append(Message{Role: user, Content: []tool_result})
              Loop.

  MaxIterations exhausted → ErrMaxIterations
```

### 背压与取消

传给 `Turn` 的 `ctx` 会向下贯穿所有环节：`Compressor.Compress`、每一次 `Provider.Complete`、每一次 `Tool.Execute` 以及每一次 `Approver.Approve`。取消该 context 即可在 turn 中途中止 —— 当前迭代的 provider 调用会返回 `context.Canceled`，会话中留下模型的最后一条完整消息加上尚未完成的工具调用，调用方可自行决定是否重试。

内置的 `BashTool` 会将每条命令包装在其自身的 `context.WithTimeout` 中（默认 60s，可配置），因此失控的命令不会超出外层 context 的时限。

### 系统提示词的组合

`agent.go` 第 138 行的 `systemPrompt(ctx, session)` 最多汇总三部分：

```
<Options.SystemPrompt>

<SkillsProvider.SystemAppendix(session)>

<RecallProvider.SystemAppendix(ctx, session)>
```

任何返回空字符串的部分都会被省略。最终结果是 `strings.Join(parts, "\n\n")`。组合发生在每一次迭代中（不是每个 turn），因此 skills 和 recall 会对最新的消息作出反应 —— 相关时也包括中间的工具结果。

### 上下文窗口管理

大型会话最终会超出模型的上下文窗口。Rousseau 自身并不截断 —— 这是 `Compressor` 的职责。默认的 `NoopCompressor` 从不重写，因此想在小窗口中承载无界对话记录的嵌入者，必须自行提供 compressor，或接受窗口填满时来自模型侧的错误。

`LLMCompressor`（见下文）会在消息数量超过 `TriggerMessages` 时，将早于 `KeepRecent` 的消息折叠成单个摘要块。摘要由运行该 turn 的同一个 provider 生成，因此每个压缩周期额外产生一次 completion。

## Provider 接口

`internal/agent/provider.go`：

```go
type Provider interface {
    Name() string
    Complete(ctx context.Context, req Request) (Response, error)
}

type StreamingProvider interface {
    Provider
    CompleteStream(ctx context.Context, req Request, out chan<- StreamEvent) error
}
```

`Complete` 运行单次非流式 turn。`Request` 携带 `SessionID`、`System`、`Messages`、`Tools` 和 `CacheableMessages`（一个短时缓存提示）。`Response` 返回一条 assistant `Message`、一个 `StopReason`（`end_turn`、`tool_use`、`max_tokens`、`other`）以及 `Usage` token 计数。

所有随包发布的 provider（Anthropic、Bedrock、Vertex、OpenAI 兼容、claudecli）都实现了 `Provider`。除 `claudecli` 外，每一个都实现了 `StreamingProvider`。

## Session、Message、Turn

`internal/agent/session.go` 和 `internal/agent/message.go`：

```go
type Session struct {
    ID        string
    Title     string
    Messages  []Message
    CreatedAt time.Time
    UpdatedAt time.Time
}

type Message struct {
    Role      Role     // "user", "assistant", "system"
    Content   []Content
    CreatedAt time.Time
}

type Content struct {
    Kind       ContentKind  // "text", "tool_use", "tool_result"
    Text       string
    ToolUse    *ToolUse
    ToolResult *ToolResult
}
```

`Session` 只追加不修改。每一条用户消息都对应一次 `Agent.Turn(ctx, session)` 调用；agent loop 会就地修改会话，并返回最终的 assistant `Message`。

## 注册工具

`internal/tools`：

```go
registry := tools.NewRegistry()
registry.MustRegister(builtin.NewReadTool())
registry.MustRegister(builtin.NewGrepTool(0, 0))
registry.MustRegister(builtin.NewEditTool())
```

每个工具都声明严格的 JSON schema。添加自定义工具就是实现一个 `Tool`：

```go
type Tool interface {
    Name() string
    Description() string
    InputSchema() json.RawMessage
    Execute(ctx context.Context, input json.RawMessage) (string, error)
}
```

`MustRegister` 在名称重复时会 panic；如果你在运行时动态构建注册表，请使用 `Register` 并检查错误。

## 审批策略

`internal/agent/approver.go`。有三种内置策略：

- `AllowAllApprover` —— 每次调用都执行。
- `DenyAllApprover{Reason: "…"}` —— 每次调用都被阻止，并给出指定原因。
- `PatternApprover{Allow: []PatternRule, Deny: []PatternRule, Default: Decision}` —— 按工具进行正则允许 / 拒绝。拒绝优先；未匹配的请求使用 `Default`（空 → `DecisionDeny`）。

模式规则会被惰性编译一次。编译错误会以 `DecisionDeny` 返回，错误字符串作为原因，因此非法正则会安全失败。

自定义 approver 实现：

```go
type Approver interface {
    Approve(ctx context.Context, req ApprovalRequest) (Decision, string)
}
```

`ApprovalRequest` 携带 `ToolName`、原始的 `Input` JSON 以及 `SessionID`。返回 `DecisionAllow` 或 `DecisionDeny` 加上原因字符串（会作为 `tool_result` 错误反馈给模型）。

## 压缩

`internal/agent/compressor.go`。`LLMCompressor` 在会话越过阈值后，调用同一 provider 对较早的消息进行摘要：

```go
compressor, err := agent.NewLLMCompressor(agent.LLMCompressorConfig{
    Provider:        provider,
    TriggerMessages: 60,
    KeepRecent:      8,
})
```

最近的 `KeepRecent` 条消息原样保留；更早的全部折叠为单个摘要块。`Compressor` 会在下一次请求中设置 `CacheableMessages`，使得下一个 turn 时摘要正好命中缓存。

当 `Compressor` 为 nil 时，默认使用 `NoopCompressor`。

## FTS5 跨会话召回

`internal/agent/recall.go` + `internal/state/sqlite/`。会话存储的 FTS5 索引覆盖每一条消息。`SQLiteRecall` 针对当前用户消息进行查询，并把最相关的 top-K 片段作为系统提示词附录返回：

```go
recall := recall.NewSQLiteRecall(store, 5)
```

通过设置 `Options.RecallProvider = recall` 启用。空结果是安全的 —— 循环会正常继续。

## 完整嵌入示例

```go
package main

import (
    "context"
    "fmt"
    "log/slog"
    "os"

    "github.com/sebastienrousseau/rousseau-agent/internal/agent"
    "github.com/sebastienrousseau/rousseau-agent/internal/llm/claudecli"
    "github.com/sebastienrousseau/rousseau-agent/internal/tools"
    "github.com/sebastienrousseau/rousseau-agent/internal/tools/builtin"
)

func main() {
    provider := claudecli.New(claudecli.Config{
        PermissionMode: "bypassPermissions",
    })

    registry := tools.NewRegistry()
    registry.MustRegister(builtin.NewReadTool())
    registry.MustRegister(builtin.NewGrepTool(0, 0))

    ag := agent.New(provider, registry,
        slog.New(slog.NewJSONHandler(os.Stdout, nil)),
        agent.Options{
            SystemPrompt: "You are a careful, concise coding assistant.",
            Approver: &agent.PatternApprover{
                Allow: []agent.PatternRule{
                    {ToolName: "read", Match: ".*"},
                    {ToolName: "grep", Match: ".*"},
                },
                Default: agent.DecisionDeny,
            },
        })

    session := agent.NewSession("hello")
    session.Append(agent.NewUserText("What does main.go do?"))

    reply, err := ag.Turn(context.Background(), session)
    if err != nil {
        fmt.Fprintf(os.Stderr, "turn: %v\n", err)
        os.Exit(1)
    }
    fmt.Println(reply.Content[0].Text)
}
```

源码树中的 `examples/embed-agent` 里有一个可运行的副本。

## 故障排查

### `agent: max iterations exceeded`

模型一直请求工具调用而从不发出 `end_turn`。常见原因：某个工具总是报错（模型不断尝试变体），或者 `MaxIterations` 数值对于确实复杂的任务过低。默认值是 32 —— 大型重构可提升到 64。设置 `MaxIterations: 0` 会使用默认值。

### `agent: tool not found: <name>`

模型发出了 `tool_use` 块，指向一个不在注册表中的工具。通常表示系统提示词过时（该工具已被移除但模型还记得它），或工具名是幻觉产生的。Rousseau 会将这个错误抛给调用方；模型没有机会自适应。如果你希望优雅降级，请把注册表查找封装到你自己的工具分发器中。

### Provider 返回带空消息的 `end_turn`

某些 provider 会以 `stop_reason=end_turn` 返回，但没有任何 content 块 —— 例如模型选择保持沉默。Rousseau 会返回空 `Message`；调用方来判断“空”在其 UI 里是否算有效结果。聊天传输处理程序会记录 `whatsapp.empty_reply`、`slack.empty_reply` 等日志。

### 工具结果被截断

`Content.ToolResult.Output` 是普通的 Go 字符串。某些工具实现（尤其是对大文件的 `read`）会返回超出模型可消化能力的输出。请在工具自身内部限制输出 —— 内置的 `read` 工具在 200 KB 处截断。

### 触发了压缩，但摘要不知所云

默认的压缩提示词要求生成要点列表摘要。如果模型的摘要漏掉了关键事实，可提高 `KeepRecent` 让更多消息原样保留，或用具体任务指令覆盖 `CompressionConfig.Prompt`。这个指令是运维者的调节杠杆 —— 压缩器本身并不引导模型。

## 相关页面

- [概念](/zh-Hans/concepts/) —— 各子系统概览。
- [用户指南：审批策略](/zh-Hans/user-guide/approval-policies/) —— 完整策略语义。
- [用户指南：工具](/zh-Hans/user-guide/tools/) —— 内置工具 schema。
- [用户指南：压缩与召回](/zh-Hans/user-guide/compression-recall/) —— compressor 与 FTS5 召回内部机制。
- [MCP](/zh-Hans/mcp/) —— 将 agent 工具暴露给外部宿主。

## 延伸阅读

- `internal/agent/agent.go` —— `Turn`、`runTools`、`systemPrompt`。
- `internal/agent/approver.go` —— `PatternApprover`、`AllowAllApprover`、`DenyAllApprover`。
- `internal/agent/compressor.go` —— `LLMCompressor` 和 `NoopCompressor`。
- `internal/agent/recall.go` —— `SQLiteRecall` 与 FTS5 查询结构。
- `internal/agent/stream_turn.go` —— 流式变体，逐 token 呈现进度。
- `internal/tools/tool.go` —— `Tool` 接口。
- `examples/embed-agent/main.go` —— 可运行的嵌入示例。
