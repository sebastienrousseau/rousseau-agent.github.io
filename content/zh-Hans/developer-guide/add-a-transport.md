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
description: "How to add a tenth transport to rousseau-agent: implement Start/Stop/Deliver, register in cli, add tests using the fake-injection pattern."
keywords: "add transport, extend, adapter, start stop deliver, fake injection, transport interface"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/developer-guide/add-a-transport/"
subtitle: "Adding a tenth transport in a few hundred lines."
tags: "developer-guide, transport, extend"
title: "添加传输"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add transport, extend, adapter, start stop deliver, fake injection, transport interface"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "添加传输"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 62
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-transport/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-transport/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "添加传输"
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
twitter_description: "How to add a tenth transport to rousseau-agent: implement Start/Stop/Deliver, register in cli, add tests using the fake-injection pattern."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "添加传输"
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

## "添加传输"意味着什么

rousseau 中每个传输都是对上游协议客户端的适配器。适配器实现一个小接口，为 cron 调度器暴露一个 `Deliver` 方法，并在 `internal/cli/` 中注册为 Cobra 子命令。

代理核心不动。这是不变量 —— 一次接口实现加一次 CLI 装配即得到一个新传输。

## 接口

`internal/transport/transport.go`：

```go
type IncomingMessage struct {
    From string
    Body string
    At   time.Time
}

type Handler interface {
    Handle(ctx context.Context, msg IncomingMessage) (string, error)
}

type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

`Start` 阻塞直到 `ctx` 被取消或 `Stop` 被调用。`Handle` 接收入站消息并返回回复文本 —— router 拥有按发送者的会话隔离与允许列表强制。

实现通常还会暴露一个 `Deliver(ctx context.Context, target, body string) error` 方法，以便 cron 调度器发送非源自入站轮次的消息。

## 骨架

我们添加一个假想的 **XMPP** 传输。

### 步骤 1 —— 目录与适配器

创建 `internal/transport/xmpp/`，镜像 `internal/transport/slack/` 的形态：

```
internal/transport/xmpp/
├── client.go        # Config, New, Start, Stop, Deliver
├── client_test.go   # Tests using injected fakes
├── dispatch.go      # onMessage → Handler.Handle → send reply
└── dispatch_test.go
```

### 步骤 2 —— `client.go`

```go
// Package xmpp is the XMPP transport adapter.
package xmpp

import (
    "context"
    "fmt"
    "log/slog"
    "sync"

    "github.com/sebastienrousseau/rousseau-agent/internal/transport"
)

// Config configures the XMPP transport.
type Config struct {
    Server      string
    JID         string
    Password    string
    ReplyHeader string
}

// XMPPClient is the abstract interface the adapter needs from the
// upstream client. Kept small so tests can inject a fake.
type XMPPClient interface {
    Connect(ctx context.Context) error
    OnMessage(func(from, body string))
    Send(to, body string) error
    Close() error
}

// Client is the transport adapter.
type Client struct {
    cfg     Config
    logger  *slog.Logger
    upstream XMPPClient

    mu      sync.Mutex
    handler transport.Handler
    stopped bool
}

// New constructs a Client. In production, upstream is a real xmpp.Client;
// in tests, it is a fake.
func New(cfg Config, logger *slog.Logger, upstream XMPPClient) (*Client, error) {
    if cfg.Server == "" || cfg.JID == "" {
        return nil, fmt.Errorf("xmpp: server and JID required")
    }
    return &Client{cfg: cfg, logger: logger, upstream: upstream}, nil
}

// Name satisfies transport.Transport.
func (*Client) Name() string { return "xmpp" }

// Start satisfies transport.Transport.
func (c *Client) Start(ctx context.Context, handler transport.Handler) error {
    c.mu.Lock()
    c.handler = handler
    c.mu.Unlock()

    if err := c.upstream.Connect(ctx); err != nil {
        return fmt.Errorf("xmpp: connect: %w", err)
    }
    c.upstream.OnMessage(func(from, body string) {
        c.onMessage(ctx, from, body)
    })
    <-ctx.Done()
    return c.Stop()
}

// Stop satisfies transport.Transport.
func (c *Client) Stop() error {
    c.mu.Lock()
    if c.stopped {
        c.mu.Unlock()
        return nil
    }
    c.stopped = true
    c.mu.Unlock()
    return c.upstream.Close()
}

// Deliver sends a message outside the request/response loop (e.g. cron).
func (c *Client) Deliver(_ context.Context, target, body string) error {
    return c.upstream.Send(target, c.cfg.ReplyHeader+body)
}
```

### 步骤 3 —— `dispatch.go`

```go
package xmpp

import (
    "context"
    "log/slog"
    "time"

    "github.com/sebastienrousseau/rousseau-agent/internal/transport"
)

func (c *Client) onMessage(ctx context.Context, from, body string) {
    c.mu.Lock()
    handler := c.handler
    c.mu.Unlock()
    if handler == nil {
        return
    }

    reply, err := handler.Handle(ctx, transport.IncomingMessage{
        From: from,
        Body: body,
        At:   time.Now().UTC(),
    })
    if err != nil {
        c.logger.Warn("xmpp.handle_failed", slog.String("err", err.Error()))
        return
    }
    if reply == "" {
        return
    }
    if err := c.upstream.Send(from, c.cfg.ReplyHeader+reply); err != nil {
        c.logger.Warn("xmpp.send_failed", slog.String("err", err.Error()))
    }
}
```

## 步骤 4 —— 配置面

在 `internal/config/config.go` 中新增 `XMPPConfig` 类型：

```go
type XMPPConfig struct {
    Server      string   `mapstructure:"server"`
    JID         string   `mapstructure:"jid"`
    Password    string   `mapstructure:"password"`
    ReplyHeader string   `mapstructure:"reply_header"`
    Allowlist   []string `mapstructure:"allowlist"`
}
```

并在 `Config` 上新增一个字段：

```go
XMPP XMPPConfig `mapstructure:"xmpp"`
```

在 `setDefaults(v)` 中设置任何默认值。

## 步骤 5 —— CLI 装配

新增 `internal/cli/xmpp.go`：

```go
package cli

import (
    "github.com/spf13/cobra"

    "github.com/sebastienrousseau/rousseau-agent/internal/transport/xmpp"
)

func newXMPPCmd(opts *Options) *cobra.Command {
    var allow []string
    cmd := &cobra.Command{
        Use:   "xmpp",
        Short: "Run the XMPP bridge",
        RunE: func(cmd *cobra.Command, _ []string) error {
            setUnattendedPermissionDefault(opts, "xmpp")
            ctx := cmd.Context()

            wiring, err := assembleDaemon(ctx, opts, allow)
            if err != nil {
                return err
            }
            defer func() { _ = wiring.Sessions.Close() }() //nolint:errcheck

            upstream, err := newRealXMPPClient(opts.Config.XMPP)
            if err != nil {
                return err
            }

            client, err := xmpp.New(xmpp.Config{
                Server:      opts.Config.XMPP.Server,
                JID:         opts.Config.XMPP.JID,
                Password:    opts.Config.XMPP.Password,
                ReplyHeader: opts.Config.XMPP.ReplyHeader,
            }, opts.Logger, upstream)
            if err != nil {
                return err
            }

            shutdown, err := wiring.startCron(ctx, client.Deliver, opts.Logger)
            if err != nil {
                return err
            }
            defer shutdown()

            return client.Start(ctx, wiring.Router)
        },
    }
    cmd.Flags().StringSliceVar(&allow, "allow", nil, "restrict inbound to these XMPP JIDs")
    return cmd
}
```

在 `internal/cli/root.go` 中注册：

```go
root.AddCommand(newXMPPCmd(opts))
```

## 步骤 6 —— 测试

遵循 `internal/transport/whatsapp/client_test.go` 与 `internal/transport/slack/*_test.go` 使用的 fake 注入模式：

```go
type fakeXMPP struct {
    connectErr error
    onMsg      func(from, body string)
    sent       []struct{ To, Body string }
}

func (f *fakeXMPP) Connect(context.Context) error { return f.connectErr }
func (f *fakeXMPP) OnMessage(fn func(from, body string)) { f.onMsg = fn }
func (f *fakeXMPP) Send(to, body string) error {
    f.sent = append(f.sent, struct{ To, Body string }{to, body})
    return nil
}
func (f *fakeXMPP) Close() error { return nil }

func TestClient_ReplyRoundTrip(t *testing.T) {
    up := &fakeXMPP{}
    c, err := xmpp.New(xmpp.Config{Server: "s", JID: "j"}, slog.Default(), up)
    require.NoError(t, err)

    handler := transport.HandlerFunc(func(_ context.Context, m transport.IncomingMessage) (string, error) {
        return "hello " + m.From, nil
    })

    ctx, cancel := context.WithCancel(context.Background())
    go func() { _ = c.Start(ctx, handler) }()
    // Simulate an inbound message.
    up.onMsg("alice@x", "hi")
    // Give the goroutine a moment; usually via a channel signal in real tests.
    cancel()

    require.Len(t, up.sent, 1)
    require.Equal(t, "hello alice@x", up.sent[0].Body)
}
```

## 步骤 7 —— 文档

在文档站（本仓库）中新增 `content/transports/xmpp.md`。遵循 `content/transports/slack.md` 的相同布局 —— 描述、配置面、装配配方、注意事项。

## 步骤 8 —— CI

Lint 门禁会捕获导出标识符缺失的 godoc 注释、缺失的测试、未使用的导入以及覆盖率底线。运行：

```sh
make check
```

若本地全部通过，CI 矩阵也会通过（Ubuntu + macOS 运行同一命令）。

## 常见坑

- **忘记 `Stop()` 幂等。** 接口允许多次调用 `Stop`。请使用 mutex + `stopped` bool。
- **在 `Start` 中不尊重 `ctx`。** 守护进程信号处理器取消根 context；每个长生命周期组件必须在此时返回。
- **把上游客户端类型硬编码进去。** 为上游定义一个小接口，将其作为构造函数参数，在 `cli/xmpp.go` 中注入真实客户端、在测试中注入 fake。这是承载性的可测试性模式。
- **阻塞回调。** `OnMessage` 回调通常在上游的 goroutine 中运行。请通过 channel 或有界 goroutine 池路由到 handler，以防慢速模型调用把上游堵住。

## 故障排除

### 编译时接口不满足

在您 `client.go` 底部加上 `var _ transport.Transport = (*Client)(nil)`。编译器会指出缺失的方法。

### `Start` 从不返回

您忘了在返回前 `<-ctx.Done()`。守护进程信号处理器在 `SIGTERM` / `SIGINT` 时取消根 context；每个 `Start` 都必须尊重。

### 因为回调运行在后台 goroutine 上，测试挂起

请使用 channel + `require.Eventually`（或 `t.Deadline`）等待回复。不要依赖 `time.Sleep`。

### 覆盖率底线失败

门禁总体为 75%，核心 package 更高。至少为快乐路径 resolve + 回复循环以及一个跳过原因（循环防止或非文本消息）添加测试。

### Router 允许列表阻断了您的测试

测试应直接使用 `transport.HandlerFunc`，不要经过 router。若必须行使 router 行为，请传入空允许列表（或包含测试发送者的允许列表）。

## 相关页面

- [开发者指南：架构](/zh-Hans/developer-guide/architecture/) —— `Transport` 的位置。
- [开发者指南：测试](/zh-Hans/developer-guide/testing/) —— 注入模式深入。
- [开发者指南：添加 provider](/zh-Hans/developer-guide/add-a-provider/) —— 相同形态，不同接口。
- [开发者指南：贡献](/zh-Hans/developer-guide/contributing/) —— 提交风格与 PR 清单。
- [传输](/zh-Hans/transports/) —— 作为参考实现的既有适配器。

## 延伸阅读

- `internal/transport/transport.go` —— `Transport`、`Handler` 与 `IncomingMessage` 类型。
- `internal/transport/router.go` —— 允许列表与会话映射如何工作。
- `internal/transport/whatsapp/client.go` —— 一个规范的中等复杂度适配器。
- `internal/transport/slack/client.go` —— 一个针对 WebSocket + REST 协议的规范适配器。
- `internal/cli/whatsapp.go`、`internal/cli/slack.go` —— CLI 装配示例。
