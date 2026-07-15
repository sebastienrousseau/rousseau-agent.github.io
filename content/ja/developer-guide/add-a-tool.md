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
description: "How to add a new built-in tool to rousseau-agent: declare a JSON schema, implement Execute, register with the tool registry."
keywords: "add tool, tool registry, json schema, execute, extend, custom tool"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/developer-guide/add-a-tool/"
subtitle: "Schema, Execute, register — three moving parts."
tags: "developer-guide, tools, extend"
title: "ツールを追加する"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add tool, tool registry, json schema, execute, extend, custom tool"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ツールを追加する"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 64
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-tool/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-tool/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "ツールを追加する"
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
twitter_title: "ツールを追加する"
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

`internal/tools/tool.go` (要約):

```go
type Tool interface {
    Name() string
    Description() string
    InputSchema() map[string]any
    Execute(ctx context.Context, input json.RawMessage) (string, error)
}
```

4 つのメソッド、ライフサイクルなし。ツールはループの視点からはステートレスです — ツールが必要とする任意の状態 (コンパイル済み正規表現キャッシュ、インプロセスインデックス) は、具体型のプライベートフィールドです。

## 新しいツールのスケルトン

URL を取得してその本文を返す仮想的な **`http_get`** ツールを追加してみましょう。

### ステップ 1 — 型

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

### ステップ 2 — メタデータ

```go
// Name satisfies tools.Tool.
func (*HTTPGetTool) Name() string { return "http_get" }

// Description satisfies tools.Tool.
func (*HTTPGetTool) Description() string {
    return "Fetch an HTTPS URL and return the response body. Input: url (string). Redirects are followed up to 10 hops. Response is capped at 1 MiB."
}
```

**説明はモデル向け** です。別のエンジニア向けの短い docstring のように読めるべきです — ツールが何をするか、入力の意味、出力の形状。

### ステップ 3 — 入力スキーマ

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

スキーマは厳密に保ちます。すべてのプロパティに `description` を付けます。`required` 配列はモデルのツール使用バリデータによって強制されます — 欠けたフィールドはランタイムエラーではなく `tool_use` の再試行を引き起こします。

### ステップ 4 — Execute

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

### ステップ 5 — 登録

`internal/cli/chat.go` (およびレジストリを構築する他のすべてのコマンド — `registry.MustRegister` を grep で見つけてください) に配線します:

```go
registry.MustRegister(builtin.NewHTTPGetTool(30 * time.Second))
```

登録されると、ツールは毎ターンモデルから利用可能になります。

### ステップ 6 — テスト

パターンについては `internal/tools/builtin/read_test.go` に従います:

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

### ステップ 7 — 承認ポリシー

ツールはモデルから利用可能になり、[承認ポリシー](/ja/user-guide/approval-policies/) の対象となります。デフォルトの姿勢向けに、ドキュメントで拒否ルールを推奨します:

```yaml
deny:
  - {tool: http_get, match: "\"url\":\"https://(169\\.254|10\\.|192\\.168\\.|172\\.(1[6-9]|2[0-9]|3[01])\\.)"}
```

これは、ツールが AWS IMDS またはプライベート RFC1918 空間を呼び出すのをブロックします — HTTP フェッチツールに対する一般的な要求です。

### ステップ 8 — ドキュメント

新しいツールを記述するセクションを `content/user-guide/tools.md` に追加します: スキーマ、セマンティクス、安全性メモ。既存の 5 つのツールの形状に従ってください。

## 契約の詳細

- **ステートレス性**: `Execute` は、明示的にツール自身のフィールドにプライベートでない状態を呼び出し間で持ち越してはいけません。2 つのセッションでの 2 つの並行ターンが同時に同じツールを呼び出す可能性があります。
- **コンテキストの尊重**: `Execute` は `ctx` キャンセルを尊重する必要があります。長時間実行される作業は、定期的に `ctx.Err()` をチェックするか、コンテキスト対応のライブラリ呼び出しを通じて作業をルーティングする必要があります。
- **パニックなし**: 代わりにエラーを返してください。エージェントループはエラーを `IsError: true` の `tool_result` に変換し、モデルがそれに適応できます。
- **戻り値の形状**: 出力はプレーンな文字列で、次のターンでモデルにフィードバックされます。モデルが推論できるよう、十分な構造 (例: 行番号、ステータスコード) を含めてください。

## ソースを触らずにカスタムツール

rousseau をフォークしたくない場合は、エージェントループを自分のバイナリに組み込み、そこにツールを登録します:

```go
registry := tools.NewRegistry()
registry.MustRegister(builtin.NewReadTool())
registry.MustRegister(builtin.NewWriteTool())
// ...
registry.MustRegister(mypkg.NewMyTool())

ag := agent.New(provider, registry, logger, agent.Options{})
```

完全な組み込み例については、ソースツリーの `examples/embed-agent/` を参照してください。

## よくある落とし穴

- **広すぎるスキーマ。** `type: object` だけを要求してもモデルは助からない。すべてのプロパティを列挙し、すべてのフィールドを説明してください。
- **期限なしの I/O ブロッキング。** 常に `NewRequestWithContext` を使い、常に `http.Client{Timeout: ...}` を設定し、常に `ctx` を尊重してください。
- **返しすぎ。** 出力は次のターンでモデルにフィードバックされます。1 MB のレスポンスはトークンを浪費します。上限を設けてください。
- **副作用の逃げ道。** 世界を変更するツールは、承認者の監査証跡が完全になるよう、行ったことを戻り文字列にログするべきです。
- **コンパイル時インターフェースチェックを忘れる。** パッケージスコープの `var _ tools.Tool = (*MyTool)(nil)` は、ビルド時にインターフェースドリフトをキャッチします。

## 次に

- [ユーザーガイド: ツール](/ja/user-guide/tools/) — スキーマ付きの 5 つの組み込みツール。
- [ユーザーガイド: 承認ポリシー](/ja/user-guide/approval-policies/) — 新しいツールをゲートする方法。
- [テスト](/ja/developer-guide/testing/) — ツールテストのパターン。
