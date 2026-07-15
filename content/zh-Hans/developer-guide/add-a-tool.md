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
description: "How to add a new built-in tool to rousseau-agent: declare a JSON schema, implement Execute, register with the tool registry."
keywords: "add tool, tool registry, json schema, execute, extend, custom tool"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/developer-guide/add-a-tool/"
subtitle: "Schema, Execute, register — three moving parts."
tags: "developer-guide, tools, extend"
title: "添加工具"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add tool, tool registry, json schema, execute, extend, custom tool"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "添加工具"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 64
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-tool/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-tool/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "添加工具"
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
twitter_description: "How to add a new built-in tool to rousseau-agent: declare a JSON schema, implement Execute, register with the tool registry."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "添加工具"
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

`internal/tools/tool.go`（意译）：

```go
type Tool interface {
    Name() string
    Description() string
    InputSchema() map[string]any
    Execute(ctx context.Context, input json.RawMessage) (string, error)
}
```

四个方法，无生命周期。从循环角度看，工具是无状态的 —— 工具需要的任何状态（编译后的正则缓存、进程内索引）都是具体类型上的私有字段。

## 新工具骨架

让我们添加一个假想的 **`http_get`** 工具，它抓取一个 URL 并返回其 body。

### 步骤 1 —— 类型

```go
package builtin

import (
    "context"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "time"

    "github.com/sebastienrousseau/rousseau-agent/internal/tools"
)

// HTTPGetTool fetches a URL over HTTPS and returns the response body.
type HTTPGetTool struct {
    Timeout time.Duration
    client  *http.Client
}

// NewHTTPGetTool constructs an HTTPGetTool. Zero timeout uses 30s.
func NewHTTPGetTool(timeout time.Duration) *HTTPGetTool {
    if timeout == 0 {
        timeout = 30 * time.Second
    }
    return &HTTPGetTool{
        Timeout: timeout,
        client:  &http.Client{Timeout: timeout},
    }
}
```

### 步骤 2 —— 元数据

```go
// Name satisfies tools.Tool.
func (*HTTPGetTool) Name() string { return "http_get" }

// Description satisfies tools.Tool.
func (*HTTPGetTool) Description() string {
    return "Fetch an HTTPS URL and return the response body. Input: url (string). Redirects are followed up to 10 hops. Response is capped at 1 MiB."
}
```

**描述面向模型**。它应读起来像写给另一位工程师的简短 docstring —— 工具做什么、其输入的含义、输出的形态。

### 步骤 3 —— 输入 schema

```go
// InputSchema satisfies tools.Tool.
func (*HTTPGetTool) InputSchema() map[string]any {
    return map[string]any{
        "type": "object",
        "properties": map[string]any{
            "url": map[string]any{
                "type":        "string",
                "description": "Absolute HTTPS URL to fetch.",
            },
        },
        "required": []string{"url"},
    }
}
```

保持 schema 严格。每个属性都有 `description`。`required` 数组由模型的 tool-use 校验器强制执行 —— 缺失字段会导致 `tool_use` 重试，而非运行时错误。

### 步骤 4 —— Execute

```go
type httpGetInput struct {
    URL string `json:"url"`
}

// Execute satisfies tools.Tool.
func (t *HTTPGetTool) Execute(ctx context.Context, raw json.RawMessage) (string, error) {
    var in httpGetInput
    if err := json.Unmarshal(raw, &in); err != nil {
        return "", fmt.Errorf("http_get: parse input: %w", err)
    }
    if in.URL == "" {
        return "", fmt.Errorf("http_get: url is required")
    }
    // Refuse plaintext HTTP; refuse non-http schemes.
    if !strings.HasPrefix(in.URL, "https://") {
        return "", fmt.Errorf("http_get: only https:// URLs are permitted")
    }

    req, err := http.NewRequestWithContext(ctx, http.MethodGet, in.URL, nil)
    if err != nil {
        return "", fmt.Errorf("http_get: build request: %w", err)
    }
    req.Header.Set("user-agent", "rousseau-agent/http_get")

    resp, err := t.client.Do(req)
    if err != nil {
        return "", fmt.Errorf("http_get: transport: %w", err)
    }
    defer func() { _ = resp.Body.Close() }()

    body, err := io.ReadAll(io.LimitReader(resp.Body, 1<<20))
    if err != nil {
        return "", fmt.Errorf("http_get: read body: %w", err)
    }
    return fmt.Sprintf("HTTP %d\n%s", resp.StatusCode, string(body)), nil
}

// Compile-time interface satisfaction check.
var _ tools.Tool = (*HTTPGetTool)(nil)
```

### 步骤 5 —— 注册

在 `internal/cli/chat.go` 中接线（以及其他每个构造 registry 的命令 —— grep `registry.MustRegister` 找到它们）：

```go
registry.MustRegister(builtin.NewHTTPGetTool(30 * time.Second))
```

注册之后，工具在每一轮都可供模型使用。

### 步骤 6 —— 测试

模式请参考 `internal/tools/builtin/read_test.go`：

```go
func TestHTTPGetTool_Execute_Success(t *testing.T) {
    srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
        _, _ = w.Write([]byte("hello"))
    }))
    defer srv.Close()

    // The tool refuses plaintext HTTP; wrap the test server behind httptest.NewTLSServer instead
    // for a real integration test, or expose an internal seam that permits `http://` in tests only.
    // The skeleton here is illustrative.
}

func TestHTTPGetTool_Execute_RejectsPlaintextHTTP(t *testing.T) {
    tool := builtin.NewHTTPGetTool(0)
    _, err := tool.Execute(context.Background(), json.RawMessage(`{"url":"http://example.com"}`))
    require.Error(t, err)
    require.Contains(t, err.Error(), "only https")
}
```

### 步骤 7 —— 审批策略

现在工具已对模型可用，受 [审批策略](/zh-Hans/user-guide/approval-policies/) 约束。请在文档中建议一条默认姿态的 deny 规则：

```yaml
deny:
  - {tool: http_get, match: "\"url\":\"https://(169\\.254|10\\.|192\\.168\\.|172\\.(1[6-9]|2[0-9]|3[01])\\.)"}
```

这可阻止工具调用 AWS IMDS 或私有 RFC1918 段 —— 对于抓取 HTTP 的工具这是一个常见诉求。

### 步骤 8 —— 文档

在 `content/user-guide/tools.md` 中添加一节描述新工具：schema、语义、安全注释。遵循既有五个工具的形态。

## 契约细节

- **无状态**：`Execute` 不得在调用之间携带非明确私有于工具自身字段的状态。两个会话上的两次并发轮次可能同时调用同一工具。
- **尊重 context**：`Execute` 必须遵循 `ctx` 取消。长时间工作应周期性检查 `ctx.Err()`，或通过 context 感知的库调用路由。
- **不 panic**：改为返回错误。代理循环会把错误转换为 `IsError: true` 的 `tool_result`，模型可据此适配。
- **返回形态**：输出是一个纯字符串，下一轮回喂给模型。包含足够结构（例如行号、状态码）以便模型推理。

## 不改动源码的自定义工具

若您不想 fork rousseau，请将代理循环嵌入到您自己的二进制中，并在那里注册您的工具：

```go
registry := tools.NewRegistry()
registry.MustRegister(builtin.NewReadTool())
registry.MustRegister(builtin.NewWriteTool())
// ...
registry.MustRegister(mypkg.NewMyTool())

ag := agent.New(provider, registry, logger, agent.Options{})
```

完整的嵌入示例参见源码树中的 `examples/embed-agent/`。

## 常见坑

- **过于宽泛的 schema。** 只要求 `type: object` 对模型毫无帮助。请枚举每个属性、描述每个字段。
- **阻塞 I/O 而无 deadline。** 请始终使用 `NewRequestWithContext`，始终设置 `http.Client{Timeout: ...}`，始终尊重 `ctx`。
- **返回过多。** 输出会在下一轮回喂给模型。1 MB 响应会烧掉 token；请设定上限。
- **副作用溢出。** 会改变外部世界的工具应在返回字符串中记录其所做的事，以让审批器的审计链条完整。
- **忘记编译期接口检查。** 在 package 作用域加上 `var _ tools.Tool = (*MyTool)(nil)`，可在构建期捕获接口漂移。

## 下一步

- [用户指南：工具](/zh-Hans/user-guide/tools/) —— 五个内建工具及其 schema。
- [用户指南：审批策略](/zh-Hans/user-guide/approval-policies/) —— 如何对新工具设置门禁。
- [测试](/zh-Hans/developer-guide/testing/) —— 工具测试的模式。
