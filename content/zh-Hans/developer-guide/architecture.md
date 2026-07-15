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
description: "Layered architecture of rousseau-agent: agent core, provider / tool / transport interfaces, module boundaries, cyclic-dependency prevention."
keywords: "architecture, layers, agent, provider, transport, tools, module, cyclic dependency"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/developer-guide/architecture/"
subtitle: "Layered architecture and module boundaries."
tags: "developer-guide, architecture, layers"
title: "架构"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "architecture, layers, agent, provider, transport, tools, module, cyclic dependency"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "架构"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 61
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/developer-guide/architecture/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/architecture/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "架构"
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
twitter_description: "Layered architecture of rousseau-agent: agent core, provider / tool / transport interfaces, module boundaries, cyclic-dependency prevention."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "架构"
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

## 分层示意

```
+--------------------------------------------------------------------+
|                                CLI                                |
|  chat  whatsapp  slack  discord  ...  mcp  cron  skills  doctor   |
+--------------------------------+-----------------------------------+
                                 |
+--------------------------------v-----------------------------------+
|                              Router                               |
|                  (per-JID session, allowlist, dispatch)           |
+---------------+---------------+-------------------+---------------+
                |                                   |
       transport.Transport                    agent.Agent
       Start / Stop / Deliver                Turn / TurnStream
                |                                   |
     +----------+----------+              +---------+-----------+
     |  9 concrete adapters |              |    agent.Provider  |
     +---------------------+              |    5 concrete impls |
                                          +---------+-----------+
                                                    |
                                          +---------v-----------+
                                          |   tools.Registry   |
                                          |   tools.Tool iface |
                                          +---------+-----------+
                                                    |
                                          +---------v-----------+
                                          |     state.Store    |
                                          | SQLite: sessions, |
                                          | jidmap, FTS5, cron|
                                          +---------------------+
```

## Package 角色

| Package | 角色 | 依赖 |
|---|---|---|
| `internal/agent` | Session、Message、Turn、代理循环、Provider / Tool / Approver / Compressor / SkillsProvider / RecallProvider 接口。 | stdlib + `internal/tools`（仅接口）。 |
| `internal/tools` | Tool 接口 + 并发安全的 Registry。 | stdlib。 |
| `internal/tools/builtin` | `read`、`write`、`edit`、`grep`、`bash`。 | `internal/tools`。 |
| `internal/llm/{anthropic,bedrock,claudecli,openai,vertex}` | 具体的 `agent.Provider` 实现。 | `internal/agent`。 |
| `internal/state` | Store 接口 + Summary 类型。 | stdlib。 |
| `internal/state/sqlite` | SQLite 实现、WAL、FTS5、cron 表、JID map。 | `internal/state`、`modernc.org/sqlite`。 |
| `internal/transport` | Transport 接口 + Router。 | `internal/agent`、`internal/state`。 |
| `internal/transport/{whatsapp,signal,...}` | 九个具体适配器。 | `internal/transport`、`internal/agent`。 |
| `internal/mcp` | 基于 stdio 的 JSON-RPC 2.0 服务器，MCP 规范 2024-11-05。 | `internal/agent`、`internal/tools`、`internal/state`。 |
| `internal/skills` | agentskills.io 加载器 + 组合。 | stdlib。 |
| `internal/cron` | robfig/cron/v3 调度器 goroutine。 | `internal/state`、`internal/agent`。 |
| `internal/config` | 基于 Viper 的配置加载器。 | stdlib + `viper`。 |
| `internal/cli` | Cobra 命令树、装配。 | 上面一切。 |
| `internal/tui` | Bubble Tea model。 | `internal/agent`、`internal/state`、`bubbletea`。 |
| `cmd/rousseau` | 信号处理 + `Execute`。 | `internal/cli`。 |

## 承载性不变量

**`agent` package 仅依赖于 `tools` 暴露的接口、其自身的 `Provider` 类型以及标准库。**

一切可变的部分 —— provider、store、transport、approver、compressor —— 都表达为 `agent` 所拥有的接口。具体实现导入 `agent`；`agent` 从不反向导入它们。这让循环无需任何真实 provider、真实网络或真实传输即可测试。

若您发现自己在 `llm/*`、`transport/*` 或 `state/sqlite` 中新增了来自 `agent` 的导入，请停下。装配属于 `cli`，不属于 `agent`。

## 循环依赖的防范

Go 编译器在构建期捕获 package 导入环。分层姿态让环几乎不可能：每一层只知道其下的层。具体而言：

- `cli` 允许导入一切。
- `transport/*`、`llm/*`、`state/*` 允许导入 `agent`、`tools`，以及（对 transport 与 state）它们的姊妹接口 package。
- `agent` 只允许导入 `tools`（接口）与标准库。
- `tools` 只导入标准库。

两条结构规则防止回归：

1. 接口位于 **消费者** package。`Provider` 定义在 `agent`，不在 `llm/anthropic`。`Tool` 定义在 `tools`，不在 `tools/builtin`。
2. 测试替身与消费者同侧。`agent_test.go` 定义 fake provider；`transport/whatsapp/client_test.go` 定义 fake WebSocket 连接。

## Provider 接口

```go
// Provider drives a single request/response round-trip.
type Provider interface {
    Complete(ctx context.Context, req Request) (Response, error)
}

// StreamingProvider streams response deltas.
type StreamingProvider interface {
    Provider
    CompleteStream(ctx context.Context, req Request) (StreamReader, error)
}
```

每个 LLM 适配器至少实现 `Provider`。流式为可选。

## Tool 接口

```go
// Tool is a callable capability the model can request.
type Tool interface {
    Name() string
    Description() string
    InputSchema() map[string]any
    Execute(ctx context.Context, input json.RawMessage) (string, error)
}
```

`InputSchema()` 返回 JSON-Schema 形式的 map；该形态必须满足模型对工具调用的期望。

## Transport 接口

```go
type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

`Start` 期望阻塞直到 `ctx` 被取消或 `Stop` 被调用。回送给发送者由传输内部处理；适配器通常暴露一个 `Deliver(ctx, target, body)` 方法供 cron 调度器使用。

## Approver 接口

```go
type Approver interface {
    Approve(ctx context.Context, req ApprovalRequest) (Decision, string)
}
```

在每次工具调用前的热路径上被调用。参见 [审批策略](/zh-Hans/user-guide/approval-policies/)。

## Compressor 与 Recall

代理循环在每轮还会咨询另两个接口：

```go
type Compressor interface {
    Compress(ctx context.Context, s *Session) (changed bool, err error)
}

type RecallProvider interface {
    SystemAppendix(ctx context.Context, s *Session) string
}
```

参见 [压缩 + 召回](/zh-Hans/user-guide/compression-recall/)。

## `cli` 中的装配

`internal/cli/chat.go` 是标准装配示例。它：

1. 加载配置。
2. 构建 provider（`buildProvider(cfg)`）。
3. 打开 SQLite 存储（`openStore`）。
4. 创建 tool registry 并注册内建工具。
5. 从 `cfg.Agent.Approver` 构建审批器。
6. 从 `cfg.Agent.Compression` 构建压缩器。
7. 构造 `agent.New(...)`。
8. 把 agent 交给 Bubble Tea model。

其他每个命令都遵循相同模式 —— 守护进程特定的部分只是传输构造器与其 `Start` 调用。

## 测试模式

每一层的接口都能实现隔离测试：

- `agent_test.go` 使用返回预设 `Response` 的 fake `Provider`。
- `transport/whatsapp/client_test.go` 使用 fake `WSConn` 与 fake `Sender`。
- `state/sqlite/*_test.go` 使用内存 SQLite（`file::memory:`）。
- `tools/builtin/*_test.go` 使用 `testing/fstest.MapFS`（在合适处）与临时文件。

注入模式参见 [测试](/zh-Hans/developer-guide/testing/)。

## Package 依赖图

```
cmd/rousseau/               (entry point)
    │
    ▼
internal/cli/               (Cobra command tree)
    │
    ├───▶ internal/config/  (Viper-driven config)
    ├───▶ internal/agent/   (Turn loop, session, provider iface, approver, compressor)
    │        │
    │        └───▶ internal/tools/           (Tool iface + Registry)
    │                    │
    │                    └───▶ internal/tools/builtin/   (read, write, edit, grep, bash)
    │
    ├───▶ internal/llm/anthropic/  ─────┐
    ├───▶ internal/llm/bedrock/    ─────┤
    ├───▶ internal/llm/claudecli/  ─────┼─▶ implements agent.Provider
    ├───▶ internal/llm/openai/     ─────┤
    ├───▶ internal/llm/vertex/     ─────┘
    │
    ├───▶ internal/transport/           (Transport iface + Router)
    │        │
    │        ├───▶ whatsapp/    (whatsmeow)
    │        ├───▶ slack/       (Socket Mode)
    │        ├───▶ discord/     (Gateway v10)
    │        ├───▶ telegram/    (Bot API)
    │        ├───▶ matrix/      (Client-Server)
    │        ├───▶ signal/      (signal-cli JSON-RPC)
    │        ├───▶ email/       (IMAP + SMTP)
    │        ├───▶ sms/         (Twilio / Vonage REST)
    │        └───▶ imessage/    (BlueBubbles)
    │
    ├───▶ internal/cron/        (scheduled prompts)
    ├───▶ internal/mcp/         (JSON-RPC 2.0 server)
    ├───▶ internal/skills/      (agentskills.io loader)
    ├───▶ internal/state/       (Store iface)
    │        │
    │        └───▶ internal/state/sqlite/   (WAL, FTS5)
    │
    └───▶ internal/tui/         (Bubble Tea model)
```

承载性属性：`internal/agent` 仅依赖标准库、`internal/tools`（通过其狭窄接口）以及其自身的子 package。每个 provider、每个 store、每个 transport 都依赖 `agent` —— 反之从不。

## ADR 风格的原理

选定的边界决策及其存在原因：

### ADR-1：Provider 是接口，而非插件

我们考虑过插件模型（`plugin.Open` 或 `hashicorp/go-plugin`）。被拒绝的原因：

- 静态构建更易于签名、复现和分发。
- 插件 ABI 在 Go 版本之间脆弱。
- 我们关心的每个 provider 都足够小以便 vendor。

权衡：新增 provider 需要重构建。可接受。

### ADR-2：工具位于 `internal/tools/builtin`，而非 `pkg/tools`

我们考虑过公开导出 tool registry。被拒绝的原因：

- `internal/` 抑制意外耦合。
- 嵌入代理的调用方仍可通过导出的 `Registry` 接口注册自己的工具 —— 他们只是通过 `tools` package 来做，而不是导入某个内建工具。

权衡：用户无法直接导入 `rousseau/tools/builtin`。他们导入 `rousseau/agent` 与 `rousseau/tools` 并构建自己的 registry，`examples/embed-agent` 展示了这一点。

### ADR-3：SQLite 使用 `modernc.org/sqlite`，而非 `mattn/go-sqlite3`

`modernc.org/sqlite` 是纯 Go 移植；`mattn/go-sqlite3` 使用 cgo。选择原因：

- `CGO_ENABLED=0` 让二进制保持静态。
- 静态二进制更易于签名、复现和分发。
- 使用 cgo 会让可复现构建 CI 任务困难得多。

权衡：`modernc.org/sqlite` 在写密集负载下更慢。可接受 —— rousseau 不是写密集型数据库。

### ADR-4：MCP 服务器最小化，而非官方 SDK

`internal/mcp/` package 是约 200 行手工编写的 JSON-RPC。选择原因：

- rousseau 需要的 MCP 表面较小（initialize、tools/list、tools/call、ping、shutdown）。
- 代码编写时官方 Go SDK 尚不稳定。
- 保持表面较小让 SDK 稳定后的替换无痛。

权衡：某些 MCP 特性（resources、prompts、list-changed 通知）为 stub。位于路线图。

### ADR-5：`claudecli` provider 不使用 rousseau 的 tool registry

`claude` 的子进程运行其自身的工具调用循环。因此 rousseau 的审批器看不到工具调用。这是一种刻意的接受：

- `claudecli` provider 存在是为了让订阅用户能在没有 API 密钥的情况下使用其 Claude Code 认证。
- 若 rousseau 拦截工具循环，我们就必须把每个输入输出经由子进程边界管道传输 —— 慢且易错。
- 想要 rousseau 侧审批的用户应使用非 `claudecli` 的 provider。

权衡：`claudecli` 用户必须信任 `claude` 的权限模型。已记录于 [Providers：claudecli](/zh-Hans/providers/claudecli/)。

## 下一步

- [添加传输](/zh-Hans/developer-guide/add-a-transport/) —— 新接口实现者长什么样。
- [添加 provider](/zh-Hans/developer-guide/add-a-provider/) —— 相同模式，不同接口。
- [添加工具](/zh-Hans/developer-guide/add-a-tool/) —— 最小的扩展点。

## 相关页面

- [概念](/zh-Hans/concepts/) —— 高层巡览。
- [代理循环](/zh-Hans/agent-loop/) —— 运行时形态。
- [MCP](/zh-Hans/mcp/) —— 对外工具暴露。
- [配置](/zh-Hans/configuration/) —— 每个接口读取的配置面。

## 延伸阅读

- `README.md` —— 仓库级定位与能力矩阵。
- `internal/agent/agent.go` —— 核心循环。
- `internal/agent/provider.go` —— `Provider` 与 `StreamingProvider` 接口。
- `internal/transport/transport.go` —— `Transport` 接口。
- `internal/tools/registry.go` —— `Tool` 接口与 `Registry`。
