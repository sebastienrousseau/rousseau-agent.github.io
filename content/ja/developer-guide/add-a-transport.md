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
hreflang: "ja"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "ja"
locale: "ja_JP"
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
permalink: "https://docs.rousseau-agent.dev/ja/developer-guide/add-a-transport/"
subtitle: "Adding a tenth transport in a few hundred lines."
tags: "developer-guide, transport, extend"
title: "トランスポートを追加する"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add transport, extend, adapter, start stop deliver, fake injection, transport interface"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "トランスポートを追加する"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 62
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-transport/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-transport/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "トランスポートを追加する"
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
twitter_title: "トランスポートを追加する"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "自らのコーディングエージェントを運用するすべてのオペレーターに感謝します。"
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## 「トランスポートの追加」の意味

rousseau のすべてのトランスポートは、上流のプロトコルクライアントに対するアダプタです。アダプタは小さなインターフェースを実装し、cron スケジューラ向けに `Deliver` メソッドを公開し、`internal/cli/` の Cobra サブコマンドとして登録されます。

エージェントコアは動きません。これが不変条件です — 1 つのインターフェース実装 + 1 つの CLI 配線 = 新しいトランスポート。

## インターフェース

`internal/transport/transport.go`:

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

`Start` は `ctx` がキャンセルされるか `Stop` が呼び出されるまでブロックします。`Handle` は受信メッセージを受け取り、応答テキストを返します — ルーターは送信者ごとのセッション分離と許可リストの強制を所有します。

実装は通常、受信ターン由来ではないメッセージを cron スケジューラが送信できるよう、`Deliver(ctx context.Context, target, body string) error` メソッドも公開します。

## スケルトン

仮想的な **XMPP** トランスポートを追加してみましょう。

### ステップ 1 — ディレクトリとアダプタ

`internal/transport/slack/` の形状を反映して `internal/transport/xmpp/` を作成します:

```
internal/transport/xmpp/
├── client.go        # Config, New, Start, Stop, Deliver
├── client_test.go   # Tests using injected fakes
├── dispatch.go      # onMessage → Handler.Handle → send reply
└── dispatch_test.go
```

### ステップ 2 — `client.go`

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

### ステップ 3 — `dispatch.go`

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

## ステップ 4 — 設定面

`internal/config/config.go` に `XMPPConfig` 型を追加します:

```go
type XMPPConfig struct {
    Server      string   `mapstructure:"server"`
    JID         string   `mapstructure:"jid"`
    Password    string   `mapstructure:"password"`
    ReplyHeader string   `mapstructure:"reply_header"`
    Allowlist   []string `mapstructure:"allowlist"`
}
```

また `Config` にフィールドを追加します:

```go
XMPP XMPPConfig `mapstructure:"xmpp"`
```

`setDefaults(v)` で任意のデフォルトを設定します。

## ステップ 5 — CLI 配線

`internal/cli/xmpp.go` を追加します:

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

`internal/cli/root.go` に登録します:

```go
root.AddCommand(newXMPPCmd(opts))
```

## ステップ 6 — テスト

`internal/transport/whatsapp/client_test.go` および `internal/transport/slack/*_test.go` で使われているフェイク注入パターンに従います:

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

## ステップ 7 — ドキュメント

ドキュメントサイト (このリポジトリ) に `content/transports/xmpp.md` を追加します。`content/transports/slack.md` と同じレイアウトに従ってください — 説明、設定面、配線レシピ、注意点。

## ステップ 8 — CI

リントゲートは、エクスポート識別子への godoc コメントの欠落、テストの欠落、未使用のインポート、カバレッジ下限をキャッチします。実行してください:

```sh
make check
```

ローカルですべてパスすれば、CI マトリックスもパスします (Ubuntu + macOS が同じコマンドを実行します)。

## よくある落とし穴

- **`Stop()` の冪等性を忘れる。** インターフェースは `Stop` の複数回呼び出しを許容します。ミューテックス + `stopped` bool を使用してください。
- **`Start` で `ctx` を尊重しない。** デーモンシグナルハンドラはルートコンテキストをキャンセルします。すべての長寿命コンポーネントはそのときに戻る必要があります。
- **上流クライアント型を焼き込む。** 上流用の小さなインターフェースを定義し、それをコンストラクタパラメータとして受け取り、`cli/xmpp.go` では実クライアントを、テストではフェイクを注入します。これはロードベアリングなテスト容易性パターンです。
- **コールバックをブロックする。** `OnMessage` コールバックは通常、上流の goroutine 上で実行されます。遅いモデル呼び出しが上流をバックアップさせないよう、チャネルまたは境界付き goroutine プール経由でハンドラにルーティングしてください。

## トラブルシューティング

### インターフェース充足がコンパイル時に失敗する

`client.go` の末尾に `var _ transport.Transport = (*Client)(nil)` を追加します。コンパイラが欠けているメソッドを指し示します。

### `Start` が戻らない

戻る前に `<-ctx.Done()` を忘れています。デーモンシグナルハンドラは `SIGTERM` / `SIGINT` でルートコンテキストをキャンセルします。すべての `Start` はこれを尊重する必要があります。

### コールバックがバックグラウンド goroutine で実行されるためテストがハングする

チャネル + `require.Eventually` (または `t.Deadline`) を使って応答を待ちます。`time.Sleep` に依存しないでください。

### カバレッジ下限が失敗する

ゲートは全体で 75%、コアパッケージではより高くなっています。少なくともハッピーパスの解決 + 応答ループと、1 つのスキップ理由 (ループ防止または非テキストメッセージ) のテストを追加してください。

### ルーター許可リストがテストをブロックする

テストは、ルーター経由ではなく直接 `transport.HandlerFunc` を使用すべきです。ルーターの動作を確認する必要がある場合は、空の許可リスト (またはテスト送信者を含むもの) を渡してください。

## 関連ページ

- [デベロッパーガイド: アーキテクチャ](/ja/developer-guide/architecture/) — `Transport` が収まる場所。
- [デベロッパーガイド: テスト](/ja/developer-guide/testing/) — 注入パターンの深掘り。
- [デベロッパーガイド: プロバイダの追加](/ja/developer-guide/add-a-provider/) — 同じ形状、異なるインターフェース。
- [デベロッパーガイド: コントリビューション](/ja/developer-guide/contributing/) — コミットスタイルと PR チェックリスト。
- [トランスポート](/ja/transports/) — リファレンス実装としての出荷済みアダプタ。

## 参考資料

- `internal/transport/transport.go` — `Transport`、`Handler`、`IncomingMessage` 型。
- `internal/transport/router.go` — 許可リストとセッションマッピングの仕組み。
- `internal/transport/whatsapp/client.go` — 正典的な中程度の複雑さのアダプタ。
- `internal/transport/slack/client.go` — WebSocket + REST プロトコル用の正典的アダプタ。
- `internal/cli/whatsapp.go`、`internal/cli/slack.go` — CLI 配線の例。
