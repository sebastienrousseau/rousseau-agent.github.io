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
description: "rousseau-agent's MCP server exposes its tools and sessions over stdio JSON-RPC. Compatible with Claude Desktop and any MCP host."
keywords: "MCP, Model Context Protocol, JSON-RPC, stdio, Claude Desktop, tools, sessions"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/mcp/"
subtitle: "基于 stdio 的 JSON-RPC 2.0，规范修订版 2024-11-05。"
tags: "MCP, reference"
title: "MCP 服务器"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "MCP, Model Context Protocol, JSON-RPC, stdio, Claude Desktop, tools, sessions"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP 服务器"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 21
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/mcp/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "MCP 服务器"
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
twitter_description: "rousseau-agent's MCP server exposes its tools and sessions over stdio JSON-RPC. Compatible with Claude Desktop and any MCP host."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP 服务器"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">你将学到</span><p>rousseau 使用的完整 JSON-RPC 2.0 线协议，rousseau 的 MCP 服务器实现的每个方法（含请求 / 响应示例）、错误码语义，以及如何配置 Claude Desktop / Cursor / IDE MCP 宿主与该服务器通信。请配合 <code>internal/mcp/protocol.go</code> 与 <code>internal/mcp/server.go</code> 一起阅读本页。</p></aside>

## 线协议

`rousseau mcp` 会启动一个 MCP 服务器，通过 stdio 使用 JSON-RPC 2.0 通信，遵循 [Model Context Protocol](https://modelcontextprotocol.io) 规范修订版 **2024-11-05**（在 `internal/mcp/protocol.go` 的 `ProtocolVersion` 中声明）。

- stdin 上每行一个请求（`bufio.Scanner` 每行最多读取 8 MiB）。
- stdout 上每行一个响应（`json.NewEncoder` 输出以换行分隔的 JSON）。
- 服务器会阻塞，直到 stdin 关闭或 `ctx` 被取消。

### JSON-RPC 2.0 信封

每个请求、通知和响应都使用以下信封（来自 `internal/mcp/protocol.go` 第 38 行）：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

出现的字段视信封类型而定：

| 字段 | 请求 | 通知 | 响应 |
|---|:---:|:---:|:---:|
| `jsonrpc` | 始终为 `"2.0"` | 始终为 `"2.0"` | 始终为 `"2.0"` |
| `id` | 必需 | 不存在 | 与请求相同 |
| `method` | 必需 | 必需 | 不存在 |
| `params` | 可选 | 可选 | 不存在 |
| `result` | 不存在 | 不存在 | 仅成功时存在 |
| `error` | 不存在 | 不存在 | 仅失败时存在 |

通知不携带 `id`，也不会收到响应。rousseau 仅接收一个通知（`notifications/initialized`），并静默接受。

### 方法参考

Rousseau 的 `Server.dispatch`（`internal/mcp/server.go` 第 112 行）路由以下方法：

| 方法 | 用途 | 响应 |
|---|---|---|
| `initialize` | 握手。客户端声明协议版本和能力。 | `InitializeResult` |
| `notifications/initialized` | 客户端确认已就绪。 | （通知，无响应） |
| `ping` | 存活探测。 | `{}` |
| `tools/list` | 枚举已注册的工具。 | `ToolsListResult` |
| `tools/call` | 调用一个工具。 | `ToolsCallResult` |
| `resources/list` | 占位符。当前返回 `{ "resources": [] }`。 | `{"resources": []}` |
| `prompts/list` | 占位符。返回 `{ "prompts": [] }`。 | `{"prompts": []}` |
| `shutdown` | 客户端发起的关闭。 | `{}` |

<aside class="admonition" data-type="note"><span class="admonition-title">缺失的方法</span><p><code>resources/list</code> 和 <code>prompts/list</code> 返回空数组，避免探测它们的宿主报错。完整的 resource / prompt 支持在规划中 —— 参见 <code>docs/GAP_ANALYSIS_2026.md</code>。</p></aside>

## 请求 / 响应示例

### 1. `initialize`

客户端发送：

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","clientInfo":{"name":"claude-desktop","version":"0.7.0"}}}
```

服务器响应：

```json
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05","serverInfo":{"name":"rousseau","version":"0.6.0"},"capabilities":{"tools":{"listChanged":false}}}}
```

`listChanged: false` 因为 rousseau 的工具集合在进程启动时是静态的 —— 没有运行时的增减。

### 2. `tools/list`

```json
{"jsonrpc":"2.0","id":2,"method":"tools/list"}
```

服务器按插入顺序返回已注册的工具：

```json
{"jsonrpc":"2.0","id":2,"result":{"tools":[
  {"name":"read","description":"Read a file...","inputSchema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
  {"name":"grep","description":"Search for a regex...","inputSchema":{"type":"object","properties":{"pattern":{"type":"string"},"path":{"type":"string"}},"required":["pattern"]}},
  {"name":"bash","description":"Execute a shell command...","inputSchema":{"type":"object","properties":{"command":{"type":"string"}},"required":["command"]}}
]}}
```

### 3. `tools/call`

```json
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"read","arguments":{"path":"/etc/hostname"}}}
```

成功：

```json
{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"my-host.example.com\n"}]}}
```

处理程序层失败（以 content 形式返回，而非 JSON-RPC error —— 这是 MCP 惯例）：

```json
{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"read: open /nope: no such file or directory"}],"isError":true}}
```

### 4. `ping`

```json
{"jsonrpc":"2.0","id":4,"method":"ping"}
```

```json
{"jsonrpc":"2.0","id":4,"result":{}}
```

## 错误码

Rousseau 使用标准的 JSON-RPC 2.0 错误码范围外加一个 MCP 扩展：

| Code | 常量 | 含义 | 何时触发 |
|---|---|---|---|
| -32700 | `CodeParseError` | 信封中 JSON 无效。 | 信封无法通过 `json.Unmarshal`。 |
| -32600 | `CodeInvalidRequest` | 信封结构错误。 | `jsonrpc` 字段不是 `"2.0"`。 |
| -32601 | `CodeMethodNotFound` | 方法未实现。 | 分发命中了 default 分支。 |
| -32602 | `CodeInvalidParams` | 参数解码失败。 | `params` 无法反序列化为期望结构。 |
| -32603 | `CodeInternalError` | 序列化响应时出错。 | 罕见 —— 表示存在 bug。 |
| -32000 | `CodeToolNotFound` | 工具名未注册。 | `tools/call` 使用了未知的 `name`。 |

<aside class="admonition" data-type="warning"><span class="admonition-title">工具错误 vs JSON-RPC 错误</span><p>处理程序级失败 —— <code>bash</code> 命令非零退出、<code>read</code> 打开不存在的文件 —— 会通过 <code>result.content</code> 与 <code>isError: true</code> 返回，而**不是**通过 JSON-RPC 的 <code>error</code> 字段。仅协议级失败才使用 <code>error</code>。将两种通道等同处理的宿主会错误分类可恢复的失败。</p></aside>

## 暴露的内容

两个层面：

- **工具。** 每个在 `Serve` 之前注册的 `mcp.ToolSpec` 都会在 `tools/list` 中被公布，并可通过 `tools/call` 调用。rousseau 布线的工具实现与本地 agent loop 使用的相同：`read`、`write`、`edit`、`grep`、`bash`。
- **会话。** rousseau 的 SQLite 会话存储被暴露出来，MCP 宿主可以枚举并读取历史对话。`resources/list` 会为每个会话返回一条记录。

工具失败通过 `content` 通道以 `isError=true` 呈现，而不是 JSON-RPC 错误通道。这是 MCP 惯例。

## 客户端配置 —— Claude Desktop

添加到 `~/Library/Application Support/Claude/claude_desktop_config.json`（macOS）或平台对应位置：

```json
{
  "mcpServers": {
    "rousseau": {
      "command": "rousseau",
      "args": ["mcp"],
      "env": {
        "HOME": "/Users/you"
      }
    }
  }
}
```

重启 Claude Desktop。`rousseau` 会出现在工具面板中；所有已注册的工具都可以调用。

若 rousseau 被打包进 Podman 镜像，条目变为：

```json
{
  "mcpServers": {
    "rousseau": {
      "command": "podman",
      "args": [
        "run", "--rm", "-i",
        "-v", "/Users/you/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z",
        "localhost/rousseau-agent:local",
        "mcp"
      ]
    }
  }
}
```

对状态目录进行绑定挂载，使 MCP 宿主看到与守护进程相同的会话。

## 注册自定义工具

将 MCP 服务器嵌入你自己的二进制中：

```go
srv := mcp.NewServer("rousseau", "0.1.0", logger)

srv.MustRegister(mcp.ToolSpec{
    Name:        "count_files",
    Description: "Count files under a path.",
    InputSchema: json.RawMessage(`{
      "type": "object",
      "properties": {"path": {"type": "string"}},
      "required": ["path"]
    }`),
    Handler: func(ctx context.Context, args json.RawMessage) ([]mcp.Content, error) {
        var in struct{ Path string }
        if err := json.Unmarshal(args, &in); err != nil {
            return nil, fmt.Errorf("bad input: %w", err)
        }
        // ... count files ...
        return []mcp.Content{{Type: "text", Text: fmt.Sprintf("%d", n)}}, nil
    },
})

_ = srv.Serve(ctx, os.Stdin, os.Stdout)
```

重复注册会返回错误；`MustRegister` 在重复注册时 panic（保留给 `main` 中布线使用）。

## 并发

`Serve` 可以在独立传输上并发调用（MCP 宿主的 stdin/stdout，以及你需要的控制通道）。服务器的工具映射由 RWMutex 保护；处理程序执行不会串行化 —— 实现必须支持并发使用。

## 调试

默认情况下，每个请求 / 响应信封都会以 `debug` 级别记录日志。启用方式：

```yaml
log:
  level: debug
  format: text
```

或：

```sh
ROUSSEAU_LOG_LEVEL=debug rousseau mcp 2>/tmp/mcp.log
```

MCP 宿主消费 stdout；请将日志流保留在 stderr 上。

## 故障排查

### Claude Desktop / Cursor 始终看不到 rousseau 工具

几乎总是布线错误，不是 rousseau 的问题。请检查：(1) 宿主配置中的 `command` 和 `args` 调用的是 `rousseau mcp`（而不是 `rousseau chat`）；(2) 配置文件已保存且宿主已重启；(3) 从 shell 运行 `rousseau mcp </dev/null` 不会崩溃 —— 如果崩溃，请先修复它。

### 首条消息就出现 `parse error`

宿主没有发送以换行分隔的 JSON。一些早期的 MCP 实现使用带帧头的消息（`Content-Length: N\r\n\r\n<body>`）；rousseau 期望 `\n` 分隔。请将宿主升级到使用 stdio 帧的构建（当前所有主要宿主都是如此）。

### `method not found: <foo>`

宿主调用了 rousseau 没有实现的方法。空的 `resources/list` 和 `prompts/list` 作为常见探测的 no-op 提供；其他方法都会返回 `-32601`。完整方法列表请查看 `internal/mcp/server.go` 的 `dispatch()`。

### 工具调用成功但宿主报告为错误

工具处理程序以错误方式返回错误。处理程序应返回 `[]Content{{Type: "text", Text: err.Error()}}, err != nil` —— rousseau 会捕获错误并将其包装为 `isError: true`。除非是协议级失败，否则不要通过 JSON-RPC 的 `error` 通道返回错误。

### 基于容器的 MCP 在状态目录上因 `permission denied` 失败

Claude Desktop 发起的 `podman run` 调用必须包含一个针对状态目录的 `-v`，并带上正确的 SELinux 标签。除非容器与其他 Podman 工作负载共享，否则请使用 `:Z`（私有）。此外，请确认容器内的宿主 UID 与文件属主一致。

## 相关页面

- [MCP：暴露的工具](/zh-Hans/mcp/exposed-tools/) —— rousseau 发布的工具集。
- [MCP：暴露的资源](/zh-Hans/mcp/exposed-resources/) —— 会话枚举与读取。
- [MCP：兼容性](/zh-Hans/mcp/compatibility/) —— 已测试的宿主矩阵。
- [教程：通过 MCP 暴露工具](/zh-Hans/tutorials/expose-tools-via-mcp/) —— 端到端演练。
- [Agent loop](/zh-Hans/agent-loop/) —— rousseau 内部如何使用这些工具。

## 延伸阅读

- `internal/mcp/protocol.go` —— 信封、方法名、错误码。
- `internal/mcp/server.go` —— `Serve`、`dispatch`、工具注册表。
- `internal/mcp/tools.go` —— 用于注册 rousseau 内置工具的辅助函数。
- `internal/cli/mcp.go` —— `rousseau mcp` 命令布线。
- [Model Context Protocol 规范](https://modelcontextprotocol.io) —— 外部参考。
