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
description: "How to add a sixth LLM provider to rousseau-agent: implement Provider.Complete and optionally StreamingProvider.CompleteStream."
keywords: "add provider, llm, chat completion, streaming, agent provider, extend"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/developer-guide/add-a-provider/"
subtitle: "Provider.Complete and StreamingProvider.CompleteStream."
tags: "developer-guide, provider, llm, extend"
title: "プロバイダを追加する"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add provider, llm, chat completion, streaming, agent provider, extend"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "プロバイダを追加する"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 63
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-provider/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-provider/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "プロバイダを追加する"
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
twitter_title: "プロバイダを追加する"
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

## インターフェース

`internal/agent/provider.go` (要約):

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

すべての LLM アダプタは少なくとも `Provider` を満たします。`StreamingProvider` はオプトインです — TUI とチャットトランスポートハンドラは、プロバイダが実装していない場合、非ストリーミングパスにフォールバックします。

`StopReason` は `StopEndTurn`、`StopToolUse`、`StopMaxTokens` のいずれかです。エージェントループは `StopEndTurn` を終端として扱い、`StopToolUse` を「モデルがツール呼び出しを要求している」として扱います。

## 新しいプロバイダのスケルトン

仮想的な **Cohere Command R** プロバイダを追加してみましょう。

### ステップ 1 — ディレクトリ

```
internal/llm/cohere/
├── client.go        # Config, New
├── complete.go      # Provider.Complete
├── stream.go        # StreamingProvider.CompleteStream (optional)
└── *_test.go
```

### ステップ 2 — `client.go`

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

### ステップ 3 — `complete.go`

`Complete` を実装します:

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

本体 `encodeRequest`、`decodeResponse`、および `cohereResponse` 形状は Cohere 固有です — rousseau のプロバイダ非依存の `agent.Request` および `agent.Response` 型を、Cohere のワイヤ形式との間で変換します。

### ステップ 4 — ストリーミング (オプション)

Cohere が SSE スタイルのストリーミングをサポートする場合、`CompleteStream` を実装します。初回は省略してかまいません。エージェントループは自動的に非ストリーミングにフォールバックします。

### ステップ 5 — 設定面

`internal/config/config.go` に `CohereConfig` を追加します:

```go
type CohereConfig struct {
    APIKey    string `mapstructure:"api_key"`
    Model     string `mapstructure:"model"`
    BaseURL   string `mapstructure:"base_url"`
    MaxTokens int64  `mapstructure:"max_tokens"`
}
```

`Config` にフィールドを追加します:

```go
Cohere CohereConfig `mapstructure:"cohere"`
```

`setDefaults` を妥当なモデルデフォルトで拡張します:

```go
v.SetDefault("cohere.model", "command-r-plus")
```

### ステップ 6 — CLI 配線

`internal/cli/provider.go` で `buildProvider(cfg *config.Config)` を拡張します:

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

`rousseau doctor` (`internal/cli/doctor.go`) を拡張し、`cfg.Provider == "cohere"` のときに `provider.cohere.*` チェックブロックを追加します。既存の anthropic チェックを反映してください。

## エージェントループが仮定する契約の詳細

- **`Complete` は `ctx` を尊重する。** 長時間の HTTP リクエストはコンテキストキャンセルを尊重する必要があります。さもなければ、デーモンの `SIGTERM` シャットダウンがハングします。
- **ツール使用ラウンドトリップ。** モデルが `tool_use` ブロックを発行するとき、レスポンスの `StopReason` は `StopToolUse` でなければならず、メッセージコンテンツは要求された各呼び出しについて `Content{Kind: ContentToolUse, ToolUse: &ToolUse{Name, Input, ID}}` を含む必要があります。エージェントループは各々を `Registry` にルーティングし、実行し、結果を次の `Complete` 呼び出しにパイプします。
- **`tool_result` の処理。** 次の呼び出しでは、`req.Messages` は、実行された各呼び出しについて `Content{Kind: ContentToolResult, ToolResult: &ToolResult{ToolUseID, Output, IsError}}` を含むユーザーメッセージを含みます。プロバイダはこれらを上流 API が期待する形状にレンダリングする必要があります。
- **コンパイル時インターフェースチェック。** パッケージスコープの `var _ agent.Provider = (*Provider)(nil)` は、ビルド時にインターフェースドリフトをキャッチします。

## ストリーミング契約

`StreamingProvider` を実装する場合:

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

TUI とチャットトランスポートハンドラは、到着するデルタを読み取ります。最終的な `Response` は、完全に構築されたアシスタントメッセージをセッションに追加するために使用されます。

## プロンプトキャッシング

`internal/llm/anthropic` は、リクエストの最後の 2 つのメッセージに `cache_control` マーカーを配置します。プロバイダがプロンプトキャッシングをサポートしている場合、同じことをしてください — 圧縮 + リコール ([圧縮 + リコール](/ja/user-guide/compression-recall/) を参照) を、トークンを多く消費するパターンから安価なパターンに変えます。

## テスト

`httptest.NewServer` を使ってフェイクの上流を立ち上げます。`internal/llm/anthropic/*_test.go` がリファレンスです。パターン:

1. 缶詰の JSON を返すハンドラで `httptest.NewServer` を開始します。
2. `BaseURL` をテストサーバーに向けてプロバイダを構築します。
3. 缶詰の `Request` で `Complete` を呼び出します。
4. 返された `Response` 形状に対してアサートします。

ストリーミングについては、`httptest` は Server-Sent Events もサポートします — `internal/llm/anthropic/stream.go` を参照してください。

## ドキュメント

このドキュメントサイトに `content/providers/cohere.md` を追加します。`content/providers/anthropic.md` の形状に従ってください — 説明、設定面、認証詳細、プロバイダ固有の注意点。

## よくある落とし穴

- **`Messages` を黙って書き換える。** エージェントループは会話状態の真実の源です。プロバイダはセマンティクスを変更せずに形状を変換する必要があります。
- **ツール使用 ID を失う。** レスポンス内のすべての `ToolUse.ID` は、次のリクエストの `ToolResult.ToolUseID` と一致する必要があります。プロバイダが独自の ID を割り当てる場合、慎重に変換してください。
- **`MaxTokens` を無視する。** 一部のプロバイダは、明示的な制限なしのリクエストを拒否します。`New` で妥当なデフォルトを設定してください。
- **リトライポリシーでループをブロックする。** リトライはエージェントループではなく、プロバイダアダプタに属します。境界を設定してください。ハングよりも早く失敗する方が優れています。

## 次に

- [テスト](/ja/developer-guide/testing/) — プロバイダの `_test.go` の書き方。
- [ツールの追加](/ja/developer-guide/add-a-tool/) — 最も小さな拡張ポイント。
- [設定](/ja/configuration/) — すべてのプロバイダが公開する設定面。
