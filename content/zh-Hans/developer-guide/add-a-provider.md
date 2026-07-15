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
description: "How to add a sixth LLM provider to rousseau-agent: implement Provider.Complete and optionally StreamingProvider.CompleteStream."
keywords: "add provider, llm, chat completion, streaming, agent provider, extend"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/developer-guide/add-a-provider/"
subtitle: "Provider.Complete and StreamingProvider.CompleteStream."
tags: "developer-guide, provider, llm, extend"
title: "添加提供方"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add provider, llm, chat completion, streaming, agent provider, extend"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "添加提供方"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 63
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-provider/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-provider/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "添加提供方"
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
twitter_description: "How to add a sixth LLM provider to rousseau-agent: implement Provider.Complete and optionally StreamingProvider.CompleteStream."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "添加提供方"
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

## 接口

`internal/agent/provider.go`（意译）：

```go
type Request struct {
    SessionID string
    System    string
    Messages  []Message
    Tools     []ToolDefinition
}

type Response struct {
    Message    Message
    StopReason StopReason
}

// Provider drives a single round-trip.
type Provider interface {
    Complete(ctx context.Context, req Request) (Response, error)
}

// StreamingProvider streams response deltas as they arrive.
type StreamingProvider interface {
    Provider
    CompleteStream(ctx context.Context, req Request) (StreamReader, error)
}
```

每个 LLM 适配器至少实现 `Provider`。`StreamingProvider` 为可选 —— 当 provider 未实现它时，TUI 与聊天传输处理器会回退到非流式路径。

`StopReason` 是 `StopEndTurn`、`StopToolUse`、`StopMaxTokens` 之一。代理循环把 `StopEndTurn` 视为终止，把 `StopToolUse` 视为"模型想要一次工具调用"。

## 新 provider 骨架

我们添加一个假想的 **Cohere Command R** provider。

### 步骤 1 —— 目录

```
internal/llm/cohere/
├── client.go        # Config, New
├── complete.go      # Provider.Complete
├── stream.go        # StreamingProvider.CompleteStream (optional)
└── *_test.go
```

### 步骤 2 —— `client.go`

```go
// Package cohere implements the Cohere Command R provider.
package cohere

import (
    "net/http"
    "time"
)

// Config configures the Cohere provider.
type Config struct {
    APIKey    string
    Model     string
    BaseURL   string
    MaxTokens int64
}

// Provider is the Cohere adapter.
type Provider struct {
    cfg    Config
    client *http.Client
}

// New constructs a Provider.
func New(cfg Config) *Provider {
    if cfg.BaseURL == "" {
        cfg.BaseURL = "https://api.cohere.com/v1"
    }
    if cfg.MaxTokens == 0 {
        cfg.MaxTokens = 4096
    }
    return &Provider{
        cfg:    cfg,
        client: &http.Client{Timeout: 120 * time.Second},
    }
}
```

### 步骤 3 —— `complete.go`

实现 `Complete`：

```go
package cohere

import (
    "bytes"
    "context"
    "encoding/json"
    "fmt"
    "net/http"

    "github.com/sebastienrousseau/rousseau-agent/internal/agent"
)

// Complete satisfies agent.Provider.
func (p *Provider) Complete(ctx context.Context, req agent.Request) (agent.Response, error) {
    body, err := p.encodeRequest(req)
    if err != nil {
        return agent.Response{}, fmt.Errorf("cohere: encode: %w", err)
    }

    httpReq, err := http.NewRequestWithContext(ctx, http.MethodPost, p.cfg.BaseURL+"/chat", bytes.NewReader(body))
    if err != nil {
        return agent.Response{}, err
    }
    httpReq.Header.Set("content-type", "application/json")
    httpReq.Header.Set("authorization", "Bearer "+p.cfg.APIKey)

    httpResp, err := p.client.Do(httpReq)
    if err != nil {
        return agent.Response{}, fmt.Errorf("cohere: transport: %w", err)
    }
    defer httpResp.Body.Close()

    if httpResp.StatusCode >= 400 {
        return agent.Response{}, fmt.Errorf("cohere: HTTP %d", httpResp.StatusCode)
    }

    var raw cohereResponse
    if err := json.NewDecoder(httpResp.Body).Decode(&raw); err != nil {
        return agent.Response{}, fmt.Errorf("cohere: decode: %w", err)
    }
    return p.decodeResponse(raw), nil
}

// Compile-time interface check.
var _ agent.Provider = (*Provider)(nil)
```

`encodeRequest`、`decodeResponse` 主体，以及 `cohereResponse` 形态是 Cohere 特定的 —— 它们把 rousseau 与 provider 无关的 `agent.Request` 与 `agent.Response` 类型往返翻译为 Cohere 的传线格式。

### 步骤 4 —— 流式（可选）

若 Cohere 支持 SSE 风格流式，请实现 `CompleteStream`。首轮先跳过；代理循环会自动回退到非流式。

### 步骤 5 —— 配置面

在 `internal/config/config.go` 中新增 `CohereConfig`：

```go
type CohereConfig struct {
    APIKey    string `mapstructure:"api_key"`
    Model     string `mapstructure:"model"`
    BaseURL   string `mapstructure:"base_url"`
    MaxTokens int64  `mapstructure:"max_tokens"`
}
```

在 `Config` 中新增一个字段：

```go
Cohere CohereConfig `mapstructure:"cohere"`
```

用一个合理的模型默认值扩展 `setDefaults`：

```go
v.SetDefault("cohere.model", "command-r-plus")
```

### 步骤 6 —— CLI 装配

在 `internal/cli/provider.go` 中扩展 `buildProvider(cfg *config.Config)`：

```go
func buildProvider(cfg *config.Config) (agent.Provider, error) {
    switch cfg.Provider {
    // ...existing cases...
    case "cohere":
        return cohere.New(cohere.Config{
            APIKey:    cfg.Cohere.APIKey,
            Model:     cfg.Cohere.Model,
            BaseURL:   cfg.Cohere.BaseURL,
            MaxTokens: cfg.Cohere.MaxTokens,
        }), nil
    default:
        return nil, fmt.Errorf("unknown provider %q", cfg.Provider)
    }
}
```

扩展 `rousseau doctor`（`internal/cli/doctor.go`），当 `cfg.Provider == "cohere"` 时新增一段 `provider.cohere.*` 检查块。镜像现有 anthropic 检查。

## 代理循环假定的契约细节

- **`Complete` 尊重 `ctx`。** 长 HTTP 请求必须遵守 context 取消，否则守护进程的 `SIGTERM` 关停会挂起。
- **Tool-use 往返。** 当模型发出 `tool_use` 块时，响应的 `StopReason` 必须为 `StopToolUse`，且消息内容必须为每次请求的调用包含 `Content{Kind: ContentToolUse, ToolUse: &ToolUse{Name, Input, ID}}`。代理循环会把它们路由到 `Registry`、执行，并在下一次 `Complete` 调用中把结果管道传回。
- **`tool_result` 处理。** 下一次调用时，`req.Messages` 中包含一条用户消息，其内容为每次已执行调用包含 `Content{Kind: ContentToolResult, ToolResult: &ToolResult{ToolUseID, Output, IsError}}`。Provider 必须把这些渲染为上游 API 期望的形态。
- **编译期接口检查。** 在 package 作用域加上 `var _ agent.Provider = (*Provider)(nil)`，可在构建期捕获接口漂移。

## 流式契约

若您实现 `StreamingProvider`：

```go
type StreamReader interface {
    Next(ctx context.Context) (StreamChunk, error)
    Close() error
}

type StreamChunk struct {
    Delta     string       // partial text delta
    Done      bool         // final chunk
    Response  *Response    // final Response, non-nil only on Done
}
```

TUI 与聊天传输处理器在 delta 到来时读取；最终的 `Response` 用于把完全成形的 assistant 消息追加到会话。

## 提示缓存

`internal/llm/anthropic` 在请求的最后两条消息上放置 `cache_control` 标记。若您的 provider 支持提示缓存，请照做 —— 这可把压缩 + 召回（见 [压缩 + 召回](/zh-Hans/user-guide/compression-recall/)）从 token 消耗大的模式变为廉价的模式。

## 测试

使用 `httptest.NewServer` 搭建一个 fake 上游。`internal/llm/anthropic/*_test.go` 是参考。模式：

1. 启动带有返回预设 JSON 的处理器的 `httptest.NewServer`。
2. 构造 provider，让 `BaseURL` 指向测试服务器。
3. 使用预设的 `Request` 调用 `Complete`。
4. 对返回的 `Response` 形态做断言。

对于流式，`httptest` 也支持 Server-Sent Events —— 参见 `internal/llm/anthropic/stream.go`。

## 文档

在本文档站中添加 `content/providers/cohere.md`。遵循 `content/providers/anthropic.md` 的形态 —— 描述、配置面、认证细节、provider 特定注意事项。

## 常见坑

- **静默重写 `Messages`。** 代理循环是会话状态的真理之源。Provider 必须在不改变语义的情况下翻译形态。
- **丢失 tool-use ID。** 响应中的每个 `ToolUse.ID` 必须匹配下一次请求中的 `ToolResult.ToolUseID`。若您的 provider 会分配自己的 ID，请仔细翻译。
- **忽略 `MaxTokens`。** 某些 provider 拒绝没有显式上限的请求。在 `New` 中设置一个合理默认值。
- **用重试策略阻塞循环。** 重试属于 provider 适配器，不属于代理循环。设定上限；快速失败胜过挂起。

## 下一步

- [测试](/zh-Hans/developer-guide/testing/) —— 如何为 provider 编写 `_test.go`。
- [添加工具](/zh-Hans/developer-guide/add-a-tool/) —— 最小的扩展点。
- [配置](/zh-Hans/configuration/) —— 每个 provider 暴露的配置面。
