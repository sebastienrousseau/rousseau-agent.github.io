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
description: "Layered architecture of rousseau-agent: agent core, provider / tool / transport interfaces, module boundaries, cyclic-dependency prevention."
keywords: "architecture, layers, agent, provider, transport, tools, module, cyclic dependency"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/developer-guide/architecture/"
subtitle: "Layered architecture and module boundaries."
tags: "developer-guide, architecture, layers"
title: "アーキテクチャ"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "architecture, layers, agent, provider, transport, tools, module, cyclic dependency"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "アーキテクチャ"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 61
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/developer-guide/architecture/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/architecture/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "アーキテクチャ"
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
twitter_description: "Layered architecture of rousseau-agent: agent core, provider / tool / transport interfaces, module boundaries, cyclic-dependency prevention."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "アーキテクチャ"
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

## 層状の全体像

```
+--------------------------------------------------------------------+
|                                CLI                                |
|  chat  whatsapp  slack  discord  ...  mcp  cron  skills  doctor   |
+--------------------------------+-----------------------------------+
                                 |
+--------------------------------v-----------------------------------+
|                              Router                               |
|                  (per-JID session, allowlist, dispatch)           |
+---------------+---------------+-------------------+---------------+
                |                                   |
       transport.Transport                    agent.Agent
       Start / Stop / Deliver                Turn / TurnStream
                |                                   |
     +----------+----------+              +---------+-----------+
     |  9 concrete adapters |              |    agent.Provider  |
     +---------------------+              |    5 concrete impls |
                                          +---------+-----------+
                                                    |
                                          +---------v-----------+
                                          |   tools.Registry   |
                                          |   tools.Tool iface |
                                          +---------+-----------+
                                                    |
                                          +---------v-----------+
                                          |     state.Store    |
                                          | SQLite: sessions, |
                                          | jidmap, FTS5, cron|
                                          +---------------------+
```

## パッケージの役割

| パッケージ | 役割 | 依存先 |
|---|---|---|
| `internal/agent` | Session、Message、Turn、エージェントループ、Provider / Tool / Approver / Compressor / SkillsProvider / RecallProvider インターフェース。 | 標準ライブラリ + `internal/tools` (インターフェースのみ)。 |
| `internal/tools` | Tool インターフェース + 並行性安全な Registry。 | 標準ライブラリ。 |
| `internal/tools/builtin` | `read`、`write`、`edit`、`grep`、`bash`。 | `internal/tools`。 |
| `internal/llm/{anthropic,bedrock,claudecli,openai,vertex}` | 具体的な `agent.Provider` 実装。 | `internal/agent`。 |
| `internal/state` | Store インターフェース + Summary 型。 | 標準ライブラリ。 |
| `internal/state/sqlite` | SQLite 実装、WAL、FTS5、cron テーブル、JID マップ。 | `internal/state`、`modernc.org/sqlite`。 |
| `internal/transport` | Transport インターフェース + Router。 | `internal/agent`、`internal/state`。 |
| `internal/transport/{whatsapp,signal,...}` | 9 個の具体的なアダプタ。 | `internal/transport`、`internal/agent`。 |
| `internal/mcp` | stdio 上の JSON-RPC 2.0 サーバー、MCP 仕様 2024-11-05。 | `internal/agent`、`internal/tools`、`internal/state`。 |
| `internal/skills` | agentskills.io ローダ + 合成。 | 標準ライブラリ。 |
| `internal/cron` | robfig/cron/v3 スケジューラ goroutine。 | `internal/state`、`internal/agent`。 |
| `internal/config` | Viper ベースの設定ローダ。 | 標準ライブラリ + `viper`。 |
| `internal/cli` | Cobra コマンドツリー、配線。 | 上記すべて。 |
| `internal/tui` | Bubble Tea モデル。 | `internal/agent`、`internal/state`、`bubbletea`。 |
| `cmd/rousseau` | シグナルハンドリング + `Execute`。 | `internal/cli`。 |

## ロードベアリング不変条件

**`agent` パッケージは、`tools` が公開するインターフェース、独自の `Provider` 型、標準ライブラリにのみ依存します。**

変化しうるすべて — プロバイダ、ストア、トランスポート、承認者、コンプレッサ — は `agent` が所有するインターフェースとして表現されます。具体的な実装は `agent` をインポートします。`agent` はそれらを逆にインポートしません。これによりループは、稼働中のプロバイダ、稼働中のネットワーク、稼働中のトランスポートなしでテスト可能です。

`agent` から `llm/*`、`transport/*`、`state/sqlite` へのインポートを追加していることに気づいたら、止めてください。配線は `agent` ではなく `cli` に属します。

## 循環依存の防止

Go コンパイラはビルド時にパッケージのインポートサイクルをキャッチします。層状の姿勢は、サイクルをほぼ不可能にします: 各層は自分より下の層のみを知っています。具体的には:

- `cli` はすべてをインポートできます。
- `transport/*`、`llm/*`、`state/*` は `agent`、`tools`、および (トランスポートとステートについては) 兄弟のインターフェースパッケージをインポートできます。
- `agent` は `tools` (インターフェース) と標準ライブラリのみをインポートできます。
- `tools` は標準ライブラリのみをインポートします。

2 つの構造ルールが退行を防ぎます:

1. インターフェースは **コンシューマ** パッケージに存在します。`Provider` は `llm/anthropic` ではなく `agent` で定義されます。`Tool` は `tools/builtin` ではなく `tools` で定義されます。
2. テストダブルはそのコンシューマの隣に存在します。`agent_test.go` はフェイクプロバイダを定義します。`transport/whatsapp/client_test.go` はフェイク WebSocket 接続を定義します。

## Provider インターフェース

```go
// Provider drives a single request/response round-trip.
type Provider interface {
    Complete(ctx context.Context, req Request) (Response, error)
}

// StreamingProvider streams response deltas.
type StreamingProvider interface {
    Provider
    CompleteStream(ctx context.Context, req Request) (StreamReader, error)
}
```

すべての LLM アダプタは少なくとも `Provider` を満たします。ストリーミングはオプトインです。

## Tool インターフェース

```go
// Tool is a callable capability the model can request.
type Tool interface {
    Name() string
    Description() string
    InputSchema() map[string]any
    Execute(ctx context.Context, input json.RawMessage) (string, error)
}
```

`InputSchema()` は JSON スキーマ形状のマップを返します。形状はモデルのツール使用の期待に対して検証される必要があります。

## Transport インターフェース

```go
type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

`Start` は `ctx` がキャンセルされるか `Stop` が呼び出されるまでブロックすることが期待されます。送信者への配信はトランスポート内部で処理されます。アダプタは通常、cron スケジューラが使用する `Deliver(ctx, target, body)` メソッドを公開します。

## Approver インターフェース

```go
type Approver interface {
    Approve(ctx context.Context, req ApprovalRequest) (Decision, string)
}
```

すべてのツール呼び出しの前に、ホットパスで呼び出されます。[承認ポリシー](/ja/user-guide/approval-policies/) を参照してください。

## Compressor と Recall

エージェントループが各ターンで参照する、さらに 2 つのインターフェース:

```go
type Compressor interface {
    Compress(ctx context.Context, s *Session) (changed bool, err error)
}

type RecallProvider interface {
    SystemAppendix(ctx context.Context, s *Session) string
}
```

[圧縮 + リコール](/ja/user-guide/compression-recall/) を参照してください。

## `cli` での配線

`internal/cli/chat.go` は正典的な配線例です。以下を行います:

1. 設定をロードします。
2. プロバイダを構築します (`buildProvider(cfg)`)。
3. SQLite ストアを開きます (`openStore`)。
4. ツールレジストリを作成し、組み込みツールを登録します。
5. `cfg.Agent.Approver` から承認者を構築します。
6. `cfg.Agent.Compression` からコンプレッサを構築します。
7. `agent.New(...)` を構築します。
8. Bubble Tea モデルにエージェントを渡します。

他のすべてのコマンドは同じパターンに従います — デーモン固有の部分はトランスポートコンストラクタとその `Start` 呼び出しだけです。

## テストパターン

各層のインターフェースにより、隔離してテスト可能です:

- `agent_test.go` は缶詰の `Response` 値を返すフェイク `Provider` を使用します。
- `transport/whatsapp/client_test.go` はフェイク `WSConn` とフェイク `Sender` を使用します。
- `state/sqlite/*_test.go` はインメモリ SQLite (`file::memory:`) を使用します。
- `tools/builtin/*_test.go` は `testing/fstest.MapFS` (関連する場所) と一時ファイルを使用します。

注入パターンについては [テスト](/ja/developer-guide/testing/) を参照してください。

## パッケージ依存関係グラフ

```
cmd/rousseau/               (entry point)
    │
    ▼
internal/cli/               (Cobra command tree)
    │
    ├───▶ internal/config/  (Viper-driven config)
    ├───▶ internal/agent/   (Turn loop, session, provider iface, approver, compressor)
    │        │
    │        └───▶ internal/tools/           (Tool iface + Registry)
    │                    │
    │                    └───▶ internal/tools/builtin/   (read, write, edit, grep, bash)
    │
    ├───▶ internal/llm/anthropic/  ─────┐
    ├───▶ internal/llm/bedrock/    ─────┤
    ├───▶ internal/llm/claudecli/  ─────┼─▶ implements agent.Provider
    ├───▶ internal/llm/openai/     ─────┤
    ├───▶ internal/llm/vertex/     ─────┘
    │
    ├───▶ internal/transport/           (Transport iface + Router)
    │        │
    │        ├───▶ whatsapp/    (whatsmeow)
    │        ├───▶ slack/       (Socket Mode)
    │        ├───▶ discord/     (Gateway v10)
    │        ├───▶ telegram/    (Bot API)
    │        ├───▶ matrix/      (Client-Server)
    │        ├───▶ signal/      (signal-cli JSON-RPC)
    │        ├───▶ email/       (IMAP + SMTP)
    │        ├───▶ sms/         (Twilio / Vonage REST)
    │        └───▶ imessage/    (BlueBubbles)
    │
    ├───▶ internal/cron/        (scheduled prompts)
    ├───▶ internal/mcp/         (JSON-RPC 2.0 server)
    ├───▶ internal/skills/      (agentskills.io loader)
    ├───▶ internal/state/       (Store iface)
    │        │
    │        └───▶ internal/state/sqlite/   (WAL, FTS5)
    │
    └───▶ internal/tui/         (Bubble Tea model)
```

ロードベアリング特性: `internal/agent` は標準ライブラリ、`internal/tools` (その狭いインターフェースを通じて)、および独自のサブパッケージにのみ依存します。すべてのプロバイダ、すべてのストア、すべてのトランスポートは `agent` に依存します — 逆はありません。

## ADR スタイルの根拠

選択された境界の決定とその存在理由:

### ADR-1: Provider はプラグインではなくインターフェース

プラグインモデル (`plugin.Open` または `hashicorp/go-plugin`) を検討しました。以下の理由で却下しました:

- 静的ビルドは署名、再現、配布が容易です。
- プラグイン ABI は Go バージョン間で脆弱です。
- 我々が関心を持つすべてのプロバイダは、ベンダーするのに十分小さいです。

トレードオフ: プロバイダの追加には再ビルドが必要です。許容範囲です。

### ADR-2: ツールは `pkg/tools` ではなく `internal/tools/builtin` に存在する

ツールレジストリを公開エクスポートすることを検討しました。以下の理由で却下しました:

- `internal/` は偶発的な結合を思いとどまらせます。
- エージェントを組み込む呼び出し側は、依然としてエクスポートされた `Registry` インターフェース経由で独自のツールを登録できます — 組み込みをインポートするのではなく `tools` パッケージ経由で行うだけです。

トレードオフ: ユーザーは `rousseau/tools/builtin` を直接インポートできません。`rousseau/agent` と `rousseau/tools` をインポートし、独自のレジストリを構築します。これは `examples/embed-agent` が示すものです。

### ADR-3: SQLite は `mattn/go-sqlite3` ではなく `modernc.org/sqlite` 経由

`modernc.org/sqlite` は純粋 Go ポートです。`mattn/go-sqlite3` は cgo を使用します。以下の理由で選択しました:

- `CGO_ENABLED=0` がバイナリを静的に保ちます。
- 静的バイナリは署名、再現、配布が容易です。
- 再現可能ビルドの CI ジョブは cgo だとはるかに難しくなります。

トレードオフ: `modernc.org/sqlite` は書き込みの多いワークロードでは遅いです。許容範囲です — rousseau は書き込みの多いデータベースではありません。

### ADR-4: MCP サーバーは公式 SDK ではなく最小限

`internal/mcp/` パッケージは手書きの JSON-RPC 約 200 行です。以下の理由で選択しました:

- rousseau に必要な MCP 面は小さいです (initialize、tools/list、tools/call、ping、shutdown)。
- コードが書かれた時点で公式 Go SDK はまだ安定していませんでした。
- 面を小さく保つことで、SDK が安定したときの入れ替えが痛みなく行えます。

トレードオフ: 一部の MCP 機能 (resources、prompts、list-changed 通知) はスタブです。ロードマップです。

### ADR-5: `claudecli` プロバイダは rousseau のツールレジストリを使用しない

`claude` のサブプロセスは独自のツール使用ループを実行します。したがって、rousseau の承認者はツール呼び出しを見ることができません。これは意図的な受容です:

- `claudecli` プロバイダは、サブスクライバが API キーなしで Claude Code の認証を使用できるようにするために存在します。
- rousseau がツールループを傍受した場合、すべての入力と出力をサブプロセス境界を通じてパイプする必要があります — 遅く、エラーが起きやすいです。
- rousseau 側の承認を望むユーザーは `claudecli` 以外のプロバイダを使用します。

トレードオフ: `claudecli` ユーザーは `claude` の許可モデルを信頼する必要があります。[Providers: claudecli](/ja/providers/claudecli/) に文書化されています。

## 次に

- [トランスポートの追加](/ja/developer-guide/add-a-transport/) — 新しいインターフェース実装者の見え方。
- [プロバイダの追加](/ja/developer-guide/add-a-provider/) — 同じパターン、異なるインターフェース。
- [ツールの追加](/ja/developer-guide/add-a-tool/) — 最も小さな拡張ポイント。

## 関連ページ

- [コンセプト](/ja/concepts/) — 高レベルのツアー。
- [エージェントループ](/ja/agent-loop/) — ランタイムの形状。
- [MCP](/ja/mcp/) — 外部ツールの公開。
- [設定](/ja/configuration/) — 各インターフェースが読み取る設定面。

## 参考資料

- `README.md` — リポジトリレベルのポジショニングと機能マトリックス。
- `internal/agent/agent.go` — コアループ。
- `internal/agent/provider.go` — `Provider` と `StreamingProvider` インターフェース。
- `internal/transport/transport.go` — `Transport` インターフェース。
- `internal/tools/registry.go` — `Tool` インターフェースと `Registry`。
