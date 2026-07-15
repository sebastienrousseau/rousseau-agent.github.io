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
description: "Testing pattern for rousseau-agent: dependency injection via interfaces (WSConn, IMAPClient, HTTPClient), fake generators, race + coverage thresholds."
keywords: "testing, dependency injection, fake, mock, coverage, race, go test, httptest"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/developer-guide/testing/"
subtitle: "Dependency injection, fakes, race, coverage."
tags: "developer-guide, testing, di, fakes"
title: "テスト"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "testing, dependency injection, fake, mock, coverage, race, go test, httptest"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "テスト"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 65
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/developer-guide/testing/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/testing/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "テスト"
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
twitter_title: "テスト"
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

## パターン

外部と通信するすべてのパッケージは、その依存関係のための小さなインターフェースを定義し、そのインターフェースをコンストラクタパラメータとして受け取り、`cli/*.go` (プロダクション) では実クライアントを、`*_test.go` (テスト) ではフェイクを注入します。

ツリー内の例:

| パッケージ | インターフェース | 実 | テスト用フェイク |
|---|---|---|---|
| `internal/transport/whatsapp` | `WSConn` | whatsmeow の WebSocket | `send` チャネル付きインメモリ構造体 |
| `internal/transport/email` | `IMAPClient` | `emersion/go-imap` クライアント | メッセージのスクリプト化チャネル |
| `internal/transport/whatsapp` | `Sender` | 直接の whatsmeow 送信 | アサーション用インメモリスライス |
| `internal/llm/*` | `HTTPClient` (`http.Client` 経由の間接) | `http.DefaultTransport` | `httptest.NewServer` |
| `internal/state/sqlite` | `state.Store` (`state` が所有するインターフェース) | `modernc.org/sqlite` オンディスク | インメモリの `:memory:` DSN |
| `internal/agent` | `Provider`、`Approver`、`Compressor`、`RecallProvider` | 具体的な `llm/*` 型 | `_test.go` の構造体実装 |

ルール: **インターフェースはコンシューマ側、実装はプロバイダ側。** `Provider` は `llm/anthropic` ではなく `agent` で定義されます。`Store` は `state/sqlite` ではなく `state` で定義されます。

## ゲートの実行

```sh
make check
```

は以下と等価です:

```sh
go vet ./...
golangci-lint run
go test -race -count=1 -covermode=atomic ./...
govulncheck ./...
```

CI は `ubuntu-latest` と `macos-latest` で同じコマンドを実行します。ローカルでパスすれば CI でもパスします — プラットフォーム固有のバグを除いて。それが macOS がマトリックスに含まれる理由です。

## レース検出器

`-race` は交渉の余地がありません。rousseau のすべてのデーモンは複数の goroutine (トランスポートポンプ、エージェントループ、cron スケジューラ、セッションストアライター) を含みます。それらのいずれか 1 つでのレースは実際のバグです。

`-race` の下でのみ失敗するテストを見つけた場合、それはテストではなくテスト対象コードのバグです。`-race` を無効にしないでください。

## カバレッジ下限

現在のカバレッジ下限は **合計 75%** です。コアパッケージ (`internal/agent`、`internal/tools`、`internal/state/sqlite`) は 85〜100% で、既存のテストスイートによってそこに保たれています。これらのパッケージの新しいコードはそれを下げるべきではありません。

CI ジョブは `go test -race -covermode=atomic ./... -coverprofile=coverage.out` の後に実行され、`coverage.out` を検査します。下限を下回るとビルドが失敗します。

## フェイクジェネレータ

rousseau はモック生成ライブラリを使用しません。フェイクは、一目で読めるほど小さな手書きの構造体型です:

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

2 つの特性が導き出せます:

1. フェイクは検査可能です — `calls` はすべてのリクエストをキャプチャするため、アサーションはテスト対象コードが発行した内容を確認できます。
2. フェイクは決定論的です — 缶詰の応答は順番に消費されます。

## HTTP 形状のプロバイダ用の `httptest`

HTTP を話すすべての LLM アダプタは、テストに `httptest.NewServer` を使用します:

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

SSE スタイルのストリーミングにも同じ手法が使えます — `http.Flusher` はレスポンスライターで利用できます。

## Fuzz コーパス

すべてのパーサーは `Fuzz*` 関数を持ちます。フルバッテリを実行します:

```sh
make fuzz
```

CI では、fuzz は制限時間 (`-fuzztime`) で実行されます。ローカルでは、コーパスをシードするためにより長く実行してください。

## テーブル駆動テスト

rousseau のテストは、テーブル駆動形式に大きく寄っています。例の形状:

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

これはスケールします — すべての新しいルール形状が 1 つのテーブル行になります。

## Goroutine リーク

goroutine をスポーンするテストはそれらを join する必要があります。一般的なパターン:

- テスト終了時に `context.WithCancel` と `cancel()` を使用する。
- `sync.WaitGroup` と `wg.Wait()` を使用する。
- すべてのチャネルを `close` まで消費する。

テストが goroutine をリークした場合、`go test -race` はテストファイルの `main` が終了した後、リークした goroutine 上の nil レシーバーパニックによってそれをキャッチする可能性があります。事前に規律正しくする方が安価です。

## 決定論的な時間

時間に敏感なテスト (cron、リコール新しさランキング) では、`time.Time` プロバイダを注入します:

```go
type Clock interface {
    Now() time.Time
}
```

`cli/*` では実際の `time.Now` を、テストではフェイクの `time.Time` を配線してください。`internal/cron/scheduler.go` スケジューラはこのパターンを使用します。

## TUI のテスト

`internal/tui/model_test.go` は `bubbletea` の `TestModel` ヘルパーを使用します。`View()` はモデルの純粋な文字列関数であるため、ほとんどのアサーションは「この更新を実行し、この View 出力を期待する」になります。

## テストしないもの

- サードパーティライブラリ。rousseau は whatsmeow や `signal-cli` の上流テストを影で覆いません。
- Go 標準ライブラリ。`net/http` は動作します。
- Cobra による CLI フラグ登録。Cobra 自身のテストがそれをカバーします。

代わりに、あなたが書いたコードをテストしてください: 配線、分岐、エラーパス、リカバリパス。

## 次に

- [トランスポートの追加](/ja/developer-guide/add-a-transport/) — 完全なトランスポートに適用されたフェイク注入パターン。
- [プロバイダの追加](/ja/developer-guide/add-a-provider/) — `httptest` の実際の使用。
- [コントリビューション](/ja/developer-guide/contributing/) — PR チェックリスト。
