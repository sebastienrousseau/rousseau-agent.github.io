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
description: "Testing pattern for rousseau-agent: dependency injection via interfaces (WSConn, IMAPClient, HTTPClient), fake generators, race + coverage thresholds."
keywords: "testing, dependency injection, fake, mock, coverage, race, go test, httptest"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/developer-guide/testing/"
subtitle: "Dependency injection, fakes, race, coverage."
tags: "developer-guide, testing, di, fakes"
title: "测试"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "testing, dependency injection, fake, mock, coverage, race, go test, httptest"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "测试"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 65
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/developer-guide/testing/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/testing/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "测试"
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
twitter_description: "Testing pattern for rousseau-agent: dependency injection via interfaces (WSConn, IMAPClient, HTTPClient), fake generators, race + coverage thresholds."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "测试"
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

## 模式

每个与外界对话的 package 都为其依赖定义一个小接口，将该接口作为构造函数参数，并在 `cli/*.go`（生产）中注入真实客户端，或在 `*_test.go`（测试）中注入 fake。

代码树中的示例：

| Package | 接口 | 真实实现 | 测试用 fake |
|---|---|---|---|
| `internal/transport/whatsapp` | `WSConn` | whatsmeow 的 WebSocket | 带 `send` channel 的内存 struct |
| `internal/transport/email` | `IMAPClient` | `emersion/go-imap` 客户端 | 脚本化的消息 channel |
| `internal/transport/whatsapp` | `Sender` | 直接 whatsmeow 发送 | 用于断言的内存 slice |
| `internal/llm/*` | `HTTPClient`（通过 `http.Client` 间接） | `http.DefaultTransport` | `httptest.NewServer` |
| `internal/state/sqlite` | `state.Store`（接口归 `state` 所有） | 磁盘上的 `modernc.org/sqlite` | 内存 `:memory:` DSN |
| `internal/agent` | `Provider`、`Approver`、`Compressor`、`RecallProvider` | 具体的 `llm/*` 类型 | `_test.go` 中的 struct 实现 |

规则：**接口归消费者，实现归提供方。** `Provider` 定义在 `agent`，不在 `llm/anthropic`。`Store` 定义在 `state`，不在 `state/sqlite`。

## 运行门禁

```sh
make check
```

等价于：

```sh
go vet ./...
golangci-lint run
go test -race -count=1 -covermode=atomic ./...
govulncheck ./...
```

CI 在 `ubuntu-latest` 与 `macos-latest` 上运行相同命令。本地通过即 CI 通过 —— 除非有平台特定 bug，这也是 macOS 位于矩阵中的原因。

## Race 检测器

`-race` 不可协商。rousseau 中每个守护进程都涉及多个 goroutine（传输 pump、代理循环、cron 调度器、会话存储写入器）。其中任一个的竞争都是真 bug。

若您发现某个测试仅在 `-race` 下失败，那是被测代码的 bug，而非测试的问题。请不要禁用 `-race`。

## 覆盖率底线

当前覆盖率底线为 **总体 75%**。核心 package（`internal/agent`、`internal/tools`、`internal/state/sqlite`）位于 85–100%，由既有测试套件保持；那些 package 中的新代码不应拉低它们。

在 `go test -race -covermode=atomic ./... -coverprofile=coverage.out` 之后，一个 CI 任务会检查 `coverage.out`。未达底线则构建失败。

## Fake 生成器

Rousseau 不使用 mock 生成库。Fake 是手写的 struct 类型，小到一眼可读：

```go
type fakeProvider struct {
    responses []agent.Response
    calls     []agent.Request
}

func (f *fakeProvider) Complete(_ context.Context, req agent.Request) (agent.Response, error) {
    f.calls = append(f.calls, req)
    if len(f.responses) == 0 {
        return agent.Response{}, errors.New("no more canned responses")
    }
    resp := f.responses[0]
    f.responses = f.responses[1:]
    return resp, nil
}
```

得出两个性质：

1. Fake 是可检查的 —— `calls` 捕获每个请求，从而断言可以检查被测代码所发送的内容。
2. Fake 是确定性的 —— 预设响应按序被消费。

## 面向 HTTP 形态 provider 的 `httptest`

每个走 HTTP 的 LLM 适配器在测试中都使用 `httptest.NewServer`：

```go
srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
    _ = json.NewEncoder(w).Encode(map[string]any{
        "role":       "assistant",
        "content":    []map[string]any{{"type": "text", "text": "hello"}},
        "stop_reason":"end_turn",
    })
}))
defer srv.Close()

p := anthropic.New(anthropic.Config{
    APIKey:  "test",
    BaseURL: srv.URL,
    Model:   "test-model",
})
```

对于 SSE 风格的流式，同一技术照样可用 —— response writer 上可用 `http.Flusher`。

## Fuzz 语料

每个解析器都有 `Fuzz*` 函数。运行完整批次：

```sh
make fuzz
```

CI 下 fuzz 在有界时间内运行（`-fuzztime`）。本地可运行更久以填充语料。

## 表驱动测试

Rousseau 的测试大量倚重表驱动形式。示例形态：

```go
func TestPatternApprover_Approve(t *testing.T) {
    tests := []struct {
        name     string
        approver *agent.PatternApprover
        req      agent.ApprovalRequest
        want     agent.Decision
    }{
        {
            name:     "allow read",
            approver: &agent.PatternApprover{Allow: []agent.PatternRule{{ToolName: "read"}}},
            req:      agent.ApprovalRequest{ToolName: "read"},
            want:     agent.DecisionAllow,
        },
        {
            name:     "deny wins over allow",
            approver: &agent.PatternApprover{
                Allow: []agent.PatternRule{{ToolName: "bash"}},
                Deny:  []agent.PatternRule{{ToolName: "bash", Match: "rm"}},
            },
            req:  agent.ApprovalRequest{ToolName: "bash", Input: json.RawMessage(`{"command":"rm -rf /"}`)},
            want: agent.DecisionDeny,
        },
    }
    for _, tc := range tests {
        t.Run(tc.name, func(t *testing.T) {
            got, _ := tc.approver.Approve(context.Background(), tc.req)
            require.Equal(t, tc.want, got)
        })
    }
}
```

这具可扩展性 —— 每个新规则形态就是一行表。

## Goroutine 泄漏

派生 goroutine 的测试必须 join 它们。常见模式：

- 使用 `context.WithCancel`，并在测试末尾调用 `cancel()`。
- 使用 `sync.WaitGroup` 与 `wg.Wait()`。
- 消费每个 channel 直至 `close`。

若测试泄漏了 goroutine，`go test -race` 可能会在测试文件 `main` 退出后于泄漏的 goroutine 上通过 nil 接收者 panic 捕获它。前置守纪律更省事。

## 确定性时间

对时间敏感的测试（cron、召回按新旧排名），注入 `time.Time` provider：

```go
type Clock interface {
    Now() time.Time
}
```

在 `cli/*` 中接线真实的 `time.Now`，在测试中接线一个 fake `time.Time`。`internal/cron/scheduler.go` 调度器就使用该模式。

## 测试 TUI

`internal/tui/model_test.go` 使用 `bubbletea` 的 `TestModel` 助手。`View()` 是 model 的一个纯字符串函数，因此大多数断言变成"运行这次 update，期望这个 View 输出"。

## 什么不该测

- 第三方库。Rousseau 不影子测试 whatsmeow 或 `signal-cli` 的上游测试。
- Go 标准库。`net/http` 是工作的。
- Cobra 的 CLI flag 注册。Cobra 自身的测试已覆盖。

而应测试您所编写的代码：装配、分支、错误路径、恢复路径。

## 下一步

- [添加传输](/zh-Hans/developer-guide/add-a-transport/) —— 对完整传输应用 fake 注入模式。
- [添加 provider](/zh-Hans/developer-guide/add-a-provider/) —— `httptest` 的实战。
- [贡献](/zh-Hans/developer-guide/contributing/) —— PR 清单。
