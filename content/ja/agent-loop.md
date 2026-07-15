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
changefreq: "weekly"
description: "Embed rousseau-agent's agent loop into your own Go binary. Provider and StreamingProvider interfaces, Session/Message/Turn shapes, tool registration, approval policies, compression, FTS5 recall."
keywords: "library, embedding, agent.Provider, agent.Session, agent.Turn, tool registry, approver, compression, FTS5, recall"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/agent-loop/"
subtitle: "ライブラリ組み込み契約：Provider、Registry、Session、Turn。"
tags: "library, embedding, reference"
title: "エージェントループ リファレンス"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "library, embedding, agent.Provider, agent.Session, agent.Turn, tool registry, approver, compression, FTS5, recall"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "エージェントループ リファレンス"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 22
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/agent-loop/index.html"
item_link: "https://docs.rousseau-agent.dev/agent-loop/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "エージェントループ リファレンス"
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
twitter_description: "Embed rousseau-agent's agent loop into your own Go binary. Provider and StreamingProvider interfaces, Session/Message/Turn shapes, tool registration, approval policies, compression, FTS5 recall."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "エージェントループ リファレンス"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">このページで学べること</span><p>1 回の <code>Agent.Turn</code> の完全な内部構造: <code>Compressor</code>、<code>SkillsProvider</code>、<code>RecallProvider</code> がどのようにシステムプロンプトを構成するか、モデルの <code>tool_use</code> ブロックが <code>Approver</code> を通過する方法、ツール結果がどのようにセッションに折り込まれるか、そしてループがどのように終了するかを扱います。このページと合わせて <code>internal/agent/agent.go</code> を参照してください。</p></aside>

## ライブラリとしての rousseau

`rousseau-agent` はデーモンであると同時にライブラリでもあります。エージェントループ、ツールレジストリ、プロバイダーの抽象は CLI に依存しません。`internal/cli` や任意のトランスポートパッケージをインポートすることなく、独自のバイナリに組み込めます。

エクスポートされた識別子にはすべて godoc コメントが付いています。`pkg.go.dev/github.com/sebastienrousseau/rousseau-agent` に完全なリファレンスがレンダリングされます。

## Turn の内部構造

`Agent.Turn` 関数は `internal/agent/agent.go` で定義されています。散文的に説明すると、1 ターンは次を実行します。

```
Turn(ctx, session)
  │
  ├── 1. Session guard: empty session → ErrEmptySession
  │
  ├── 2. Compressor.Compress(ctx, session)
  │     • If enabled and len(messages) > TriggerMessages, summarise older
  │       messages in place. Sets CacheableMessages on next Request.
  │
  ├── 3. registry.Definitions() → toolDefs
  │
  └── loop up to MaxIterations (default 32) times:
        │
        ├── a. Build Request{
        │       SessionID:         session.ID,
        │       System:            systemPrompt(session),
        │       Messages:          session.Messages,
        │       Tools:             toolDefs,
        │       CacheableMessages: <hint from compressor>,
        │     }
        │
        ├── b. resp = provider.Complete(ctx, req)
        │
        ├── c. session.Append(resp.Message)
        │
        ├── d. Switch on resp.StopReason:
        │       • StopEndTurn → return resp.Message (success)
        │       • StopMaxTokens / StopOther → return resp.Message
        │       • StopToolUse → continue to (e)
        │
        ├── e. runTools(ctx, resp.Message, sessionID):
        │       For each tool_use block:
        │         • registry.Get(name) → tool or ErrToolNotFound
        │         • approver.Approve(...)
        │             DecisionDeny → tool_result with is_error=true and reason
        │             DecisionAllow → tool.Execute(ctx, input)
        │               err → tool_result with is_error=true and err.Error()
        │               ok  → tool_result with output
        │
        └── f. session.Append(Message{Role: user, Content: []tool_result})
              Loop.

  MaxIterations exhausted → ErrMaxIterations
```

### バックプレッシャーとキャンセル

`Turn` に渡された `ctx` は、`Compressor.Compress`、あらゆる `Provider.Complete`、あらゆる `Tool.Execute`、およびあらゆる `Approver.Approve` に伝播します。ターンの途中で中断するにはコンテキストをキャンセルします。現在のイテレーションのプロバイダー呼び出しは `context.Canceled` を返し、セッションにはモデルの最後の完全なメッセージと未処理のツール呼び出しが残ります。呼び出し側は再試行するかどうかを決定できます。

組み込みの `BashTool` は各コマンドを独自の `context.WithTimeout` (デフォルト 60 秒、設定可能) でラップするため、暴走したコマンドが外側のコンテキストを超えることはありません。

### システムプロンプトの構成

`agent.go` 138 行目の `systemPrompt(ctx, session)` は、最大 3 つのパートを組み立てます。

```
<Options.SystemPrompt>

<SkillsProvider.SystemAppendix(session)>

<RecallProvider.SystemAppendix(ctx, session)>
```

空を返すパートは省略されます。結果は `strings.Join(parts, "\n\n")` です。構成はターン単位ではなくイテレーション単位で行われるため、スキルとリコールは最新のメッセージ (関連する場合は中間のツール結果を含む) に反応します。

### コンテキストウィンドウの管理

セッションが大きくなると、いずれモデルのコンテキストウィンドウを超過します。Rousseau は独自にトランケートしません。それは `Compressor` の役割です。デフォルトの `NoopCompressor` は決して書き換えないため、小さなウィンドウで無制限のトランスクリプトを扱いたいエンベッダーは、独自のコンプレッサーを提供するか、ウィンドウが満杯になったときのモデル側エラーを受け入れる必要があります。

`LLMCompressor` (後述) は、メッセージ数が `TriggerMessages` を超えると、`KeepRecent` より古いメッセージを 1 つの要約ブロックに折りたたみます。要約はターンを実行するのと同じプロバイダーによって生成されるため、圧縮サイクルごとに追加で 1 回の補完コストがかかります。

## Provider インターフェース

`internal/agent/provider.go`:

```go
type Provider interface {
    Name() string
    Complete(ctx context.Context, req Request) (Response, error)
}

type StreamingProvider interface {
    Provider
    CompleteStream(ctx context.Context, req Request, out chan<- StreamEvent) error
}
```

`Complete` は 1 回の非ストリーミングターンを実行します。`Request` は `SessionID`、`System`、`Messages`、`Tools`、および `CacheableMessages` (エフェメラルキャッシュのヒント) を運びます。`Response` は 1 つのアシスタント `Message`、`StopReason` (`end_turn`、`tool_use`、`max_tokens`、`other`)、および `Usage` トークン数を返します。

出荷されているすべてのプロバイダー (Anthropic、Bedrock、Vertex、OpenAI 互換、claudecli) は `Provider` を実装しています。`claudecli` を除くすべてが `StreamingProvider` を実装しています。

## Session、Message、Turn

`internal/agent/session.go` と `internal/agent/message.go`:

```go
type Session struct {
    ID        string
    Title     string
    Messages  []Message
    CreatedAt time.Time
    UpdatedAt time.Time
}

type Message struct {
    Role      Role     // "user", "assistant", "system"
    Content   []Content
    CreatedAt time.Time
}

type Content struct {
    Kind       ContentKind  // "text", "tool_use", "tool_result"
    Text       string
    ToolUse    *ToolUse
    ToolResult *ToolResult
}
```

`Session` は追記専用です。すべてのユーザーメッセージは `Agent.Turn(ctx, session)` の呼び出しです。エージェントループはセッションをその場で変更し、最終的なアシスタントの `Message` を返します。

## ツールの登録

`internal/tools`:

```go
registry := tools.NewRegistry()
registry.MustRegister(builtin.NewReadTool())
registry.MustRegister(builtin.NewGrepTool(0, 0))
registry.MustRegister(builtin.NewEditTool())
```

各ツールは厳密な JSON スキーマを宣言します。独自のツールを追加するには `Tool` を実装します。

```go
type Tool interface {
    Name() string
    Description() string
    InputSchema() json.RawMessage
    Execute(ctx context.Context, input json.RawMessage) (string, error)
}
```

`MustRegister` は名前が重複するとパニックします。動的にレジストリを構築する場合は `Register` を使用してエラーをチェックしてください。

## 承認ポリシー

`internal/agent/approver.go`。組み込みポリシーは 3 つあります。

- `AllowAllApprover` — すべての呼び出しが実行されます。
- `DenyAllApprover{Reason: "…"}` — すべての呼び出しが指定された理由でブロックされます。
- `PatternApprover{Allow: []PatternRule, Deny: []PatternRule, Default: Decision}` — ツールごとの正規表現による許可/拒否。拒否が優先されます。マッチしないリクエストは `Default` を使用します (空の場合 → `DecisionDeny`)。

パターンルールは遅延コンパイルされて 1 度だけコンパイルされます。コンパイルエラーはエラー文字列を理由とする `DecisionDeny` として表面化するため、不正な形式の正規表現はフェイルセーフになります。

カスタム承認者は次を実装します。

```go
type Approver interface {
    Approve(ctx context.Context, req ApprovalRequest) (Decision, string)
}
```

`ApprovalRequest` は `ToolName`、生の `Input` JSON、および `SessionID` を運びます。`DecisionAllow` または `DecisionDeny` と理由文字列を返します (`tool_result` エラーとしてモデルに返されます)。

## 圧縮

`internal/agent/compressor.go`。`LLMCompressor` は、セッションが閾値を超えた時点で、同じプロバイダーを呼び出して古いメッセージを要約します。

```go
compressor, err := agent.NewLLMCompressor(agent.LLMCompressorConfig{
    Provider:        provider,
    TriggerMessages: 60,
    KeepRecent:      8,
})
```

最新の `KeepRecent` 件のメッセージはそのまま残り、それより古いすべてのものは 1 つの要約ブロックに折りたたまれます。`Compressor` は次のリクエストで `CacheableMessages` を設定するため、要約は次のターンでキャッシュヒットします。

`Compressor` が nil の場合、`NoopCompressor` がデフォルトです。

## FTS5 によるセッション横断リコール

`internal/agent/recall.go` と `internal/state/sqlite/`。セッションストアの FTS5 インデックスはすべてのメッセージを網羅します。`SQLiteRecall` は現在のユーザーメッセージに対してクエリを実行し、最も関連度の高い上位 K 件のスニペットをシステムプロンプトの付録として返します。

```go
recall := recall.NewSQLiteRecall(store, 5)
```

`Options.RecallProvider = recall` を設定して有効化します。空の結果でも問題なく、ループは通常どおり進行します。

## 完全な組み込み例

```go
package main

import (
    "context"
    "fmt"
    "log/slog"
    "os"

    "github.com/sebastienrousseau/rousseau-agent/internal/agent"
    "github.com/sebastienrousseau/rousseau-agent/internal/llm/claudecli"
    "github.com/sebastienrousseau/rousseau-agent/internal/tools"
    "github.com/sebastienrousseau/rousseau-agent/internal/tools/builtin"
)

func main() {
    provider := claudecli.New(claudecli.Config{
        PermissionMode: "bypassPermissions",
    })

    registry := tools.NewRegistry()
    registry.MustRegister(builtin.NewReadTool())
    registry.MustRegister(builtin.NewGrepTool(0, 0))

    ag := agent.New(provider, registry,
        slog.New(slog.NewJSONHandler(os.Stdout, nil)),
        agent.Options{
            SystemPrompt: "You are a careful, concise coding assistant.",
            Approver: &agent.PatternApprover{
                Allow: []agent.PatternRule{
                    {ToolName: "read", Match: ".*"},
                    {ToolName: "grep", Match: ".*"},
                },
                Default: agent.DecisionDeny,
            },
        })

    session := agent.NewSession("hello")
    session.Append(agent.NewUserText("What does main.go do?"))

    reply, err := ag.Turn(context.Background(), session)
    if err != nil {
        fmt.Fprintf(os.Stderr, "turn: %v\n", err)
        os.Exit(1)
    }
    fmt.Println(reply.Content[0].Text)
}
```

実行可能な複製がソースツリーの `examples/embed-agent` にあります。

## トラブルシューティング

### `agent: max iterations exceeded`

モデルが `end_turn` を発行することなくツール呼び出しを要求し続けました。よくある原因: 常にエラーを返すツール (モデルがバリエーションを変えてリトライを続ける)、または真に複雑なタスクに対して `MaxIterations` の値が低すぎる場合。デフォルトは 32 で、大規模なリファクタリングでは 64 に引き上げてください。`MaxIterations: 0` を設定するとデフォルトが使用されます。

### `agent: tool not found: <name>`

モデルはレジストリに存在しないツール名を含む `tool_use` ブロックを発行しました。通常は、システムプロンプトが古い状態 (ツールは削除されたがモデルはまだ覚えている)、あるいは幻覚 (ハルシネーション) によるツールを示します。Rousseau はこれを呼び出し側にエラーとして表面化します。モデルには適応の機会は与えられません。グレースフルな低下を望む場合は、レジストリの参照を独自のツールディスパッチャーでラップしてください。

### プロバイダーが空のメッセージで `end_turn` を返した

一部のプロバイダーは、モデルが沈黙を選んだ場合など、コンテンツブロックなしで `stop_reason=end_turn` を返します。Rousseau は空の `Message` を返します。「空」が UI にとって有効な結果かどうかは呼び出し側が判断します。チャットトランスポートのハンドラーは `whatsapp.empty_reply`、`slack.empty_reply` などをログに記録します。

### ツール結果が切り詰められる

`Content.ToolResult.Output` はプレーンな Go 文字列です。一部のツール実装 (特に巨大なファイルに対する `read`) は、モデルが吸収できるより大きな出力を返します。ツール自体で出力を制限してください。組み込みの `read` ツールは 200 KB でトランケートします。

### 圧縮が発火するが要約が意味をなさない

デフォルトの圧縮プロンプトは箇条書きの要約を要求します。モデルの要約に重要な事実が欠けている場合は、`KeepRecent` を引き上げてより多くのメッセージがそのまま残るようにするか、`CompressionConfig.Prompt` をタスク固有の指示で上書きしてください。指示はオペレーターにとってのレバーです。それ以外の方法でコンプレッサーがモデルを誘導することはありません。

## 関連ページ

- [Concepts](/ja/concepts/) — 各サブシステムの概要。
- [User Guide: Approval Policies](/ja/user-guide/approval-policies/) — ポリシーの完全なセマンティクス。
- [User Guide: Tools](/ja/user-guide/tools/) — 組み込みツールのスキーマ。
- [User Guide: Compression &amp; Recall](/ja/user-guide/compression-recall/) — コンプレッサーと FTS5 リコールの内部。
- [MCP](/ja/mcp/) — エージェントのツールを外部ホストに公開する方法。

## さらに読む

- `internal/agent/agent.go` — `Turn`、`runTools`、`systemPrompt`。
- `internal/agent/approver.go` — `PatternApprover`、`AllowAllApprover`、`DenyAllApprover`。
- `internal/agent/compressor.go` — `LLMCompressor` と `NoopCompressor`。
- `internal/agent/recall.go` — `SQLiteRecall` および FTS5 クエリ形状。
- `internal/agent/stream_turn.go` — トークン単位の進捗を表面化するストリーミングバリアント。
- `internal/tools/tool.go` — `Tool` インターフェース。
- `examples/embed-agent/main.go` — 実行可能な組み込み例。
