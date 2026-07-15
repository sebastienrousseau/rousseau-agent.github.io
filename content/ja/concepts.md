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
description: "Architecture overview of rousseau-agent: agent loop, transport interface, tool registry, approval policies, SQLite session store, MCP server, cron scheduler, skills loader."
keywords: "architecture, agent loop, session, transport, tool registry, approval, MCP, cron, skills, compression, FTS5"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/concepts/"
subtitle: "エージェントループ・トランスポート・セッションストアの組み合わせ方。"
tags: "architecture, agent, session, mcp"
title: "コンセプト"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "architecture, agent loop, session, transport, tool registry, approval, MCP, cron, skills, compression, FTS5"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "コンセプト"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "concepts"
order: 3
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/concepts/index.html"
item_link: "https://docs.rousseau-agent.dev/concepts/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "コンセプト"
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
twitter_description: "Architecture overview of rousseau-agent: agent loop, transport interface, tool registry, approval policies, SQLite session store, MCP server, cron scheduler, skills loader."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "コンセプト"
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

## レイヤードアーキテクチャ

```
+---------------------------------------------------------------+
|                             CLI                              |
|  chat  whatsapp  slack  discord  ...  mcp  cron  skills      |
+-------------------------+-------------------------------------+
                          |
+-------------------------v-------------------------------------+
|                          Router                              |
|          (per-JID session, allowlist, dispatch)              |
+-------------+---------------------------+---------------------+
              |                           |
     Transport interface           agent.Agent
     Start / Stop / Deliver        Turn / TurnStream
              |                           |
   +----------+----------+       +--------+--------+
   | 9 concrete adapters |       | Provider iface  |
   +---------------------+       | 5 concrete impls|
                                 +--------+--------+
                                          |
                                 +--------v--------+
                                 | Tools Registry  |
                                 | read/write/edit |
                                 | grep/bash + ext |
                                 +--------+--------+
                                          |
                                 +--------v--------+
                                 |  State (SQLite) |
                                 | sessions, cron, |
                                 | jidmap, FTS5    |
                                 +-----------------+
```

`agent` パッケージは、`tools` が公開するインタフェース、自身の `Provider` 型、および標準ライブラリのみに依存します。具体的なプロバイダ、ストア、トランスポートは `agent` に依存します。逆はありません。

## エージェントループ

`Session → Turn → Provider → tool-use ラウンドトリップ`。すべてのユーザーメッセージは `Agent.Turn` の呼び出しになります。

1. **圧縮チェック。** 設定された `Compressor` は、ターン実行前にセッションを書き換える機会を得ます。書き換えが行われると、次のターンで要約ブロックがキャッシュされるよう `Request.CacheableMessages` が設定されます。
2. **スキル付録。** `SkillsProvider` が設定されていれば、最後のユーザーメッセージを検査し、システムプロンプトに挿入するテキストを返します。
3. **リコール付録。** `RecallProvider` が設定されていれば、過去のセッション横断で FTS5 インデックスを照会し、挿入するテキストを返します。
4. **プロバイダ呼び出し。** `Provider.Complete` の実装は `StopReason` を持つ `Response` を返します。
5. **tool-use ディスパッチ。** `StopReason == StopToolUse` の場合、要求された各ツール呼び出しは `Approver` に送られます。拒否はモデルが適応できるよう `tool_result` エラーになります。許可された呼び出しは `Registry` に対して実行され、その出力は次のイテレーションで再生されます。
6. **ターン終了。** `StopReason == StopEndTurn` または `MaxIterations` に達する（デフォルト 32）までループします。

`internal/agent/agent.go` が正典のリファレンスです。

## トランスポート

すべてのトランスポートは `transport.Transport` を実装します。

```go
type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

`Handler.Handle` は `IncomingMessage`（`From`、`Body`、`At`）を受け取り、返信テキストを返します。`Router` はトランスポートの上に位置し、送信者ごとのセッション分離、allowlist の強制、および `Agent` へのディスパッチを担います。

同梱されているトランスポートは、デフォルトで公開の HTTP サーフェスを露出しません。Slack は Socket Mode（送信 WebSocket）を使用します。Discord は Gateway（送信 WebSocket）を使用します。Signal はサブプロセスです。WhatsApp は TCP 上の Meta の Web プロトコルです。Matrix、Telegram、iMessage、email はポーリングを使用します。SMS は送信のみです。受信側には webhook が必要になるためです。

## ツールレジストリ

`internal/tools` は `Tool` インタフェースと並行安全な `Registry` を定義します。組み込みツールは `internal/tools/builtin/` にあります。

- `read` — ファイル読み取り。
- `write` — ファイル書き込み。
- `edit` — 誤って大量置換されるのを防ぐため一意マッチを強制する文字列置換。
- `grep` — テキスト検索。
- `bash` — コマンド実行。**荷重を支えるセキュリティ境界です。**

すべてのツールは厳格な JSON スキーマを宣言します。ツールの追加は配線時に `registry.MustRegister(myTool)` を 1 回呼ぶだけで、エージェントコアは変更されません。

## 承認ポリシー

すべてのツール呼び出しは実行前に `Approver.Approve` を通ります。3 つの組み込みポリシーが `internal/agent/approver.go` にあります。

| モード | 挙動 |
|---|---|
| `allow_all` | すべての呼び出しが実行されます。自身で承認を処理する `claudecli` プロバイダで妥当です。 |
| `deny_all` | すべての呼び出しがブロックされます。スモークテストや読み取り専用セッションに有用です。 |
| `pattern` | ツールごとの正規表現 allow / deny ルール。deny は allow に勝ちます。マッチしないリクエストは `Default`（`allow` または `deny`）にフォールバックします。 |

拒否理由は `tool_result` エラーとしてモデルに返され、モデルは静かに失敗するのではなく適応する機会を得ます。

## セッションストア

`internal/state/sqlite/` は `modernc.org/sqlite` 上に `state.Store` インタフェースを実装します。純 Go、libc なし、CGo なしです。特徴:

- `busy_timeout=15s` の **WAL ジャーナリング**。
- Close 時の **WAL チェックポイント** により、バックアップ用にプライマリデータベースファイルの整合性を保ちます。
- **FTS5 リコール** テーブルがすべてのメッセージをインデックスし、`RecallProvider` がセッション横断のルックアップを行います。
- **JID マップ** テーブルは WhatsApp LID 識別子を電話 JID に正規化します。
- **cron テーブル** は再起動を越えてスケジュール済みジョブを永続化します。

## MCP サーバー

`internal/mcp/server.go` は stdio 上の JSON-RPC 2.0 サーバーで、仕様リビジョンは **2024-11-05** です。`rousseau mcp` で起動します。`server.Register(mcp.ToolSpec{...})` でツールを登録し、クライアント（Claude Desktop、IDE 拡張、別のエージェント）に駆動させます。

ツールの失敗は JSON-RPC のエラーチャネルではなく、`isError=true` を伴う `content` チャネルで表面化されます。これが MCP ホストの期待する形です。

## cron スケジューラ

`internal/cron/scheduler.go` は `robfig/cron/v3` をラップします。ジョブは SQLite に保存され再起動を越えて存続します。各発火は `Runner.RunOnce(ctx, prompt)`（新規セッションに対するワンショットのエージェントターン）を呼び出し、返信を `Delivery` に渡します。`Delivery` はメッセージを配信するトランスポート非依存の関数です。

`rousseau cron add` で追加された新規ジョブは、次の `PollInterval`（デフォルト 60 秒）以内に有効になります。

## スキルローダー

`internal/skills/skills.go` は `skills_dir` を走査して `*.md` ファイルを探します。各ファイルは `name`、`description`、`triggers` を宣言する YAML フロントマターを持てます。現在のユーザーメッセージにいずれかのトリガが現れると、そのターンのシステムプロンプトにスキル本体が挿入されます。フォーマットは意図的に [agentskills.io](https://agentskills.io) の規約に近づけてあります。

## 圧縮

`internal/agent/compressor.go` は、セッションが `TriggerMessages`（デフォルト 60）を超えると LLM ベースの要約を実行します。最新の `KeepRecent` メッセージ（デフォルト 8）はそのまま残り、それより古いものはすべて単一の要約ブロックに畳み込まれます。デフォルトで無効化されています。サブスクリプション帯の `claudecli` アカウントではめったに必要ないためです。従量課金型プロバイダに対しては有効化してください。

## 次に読む

- [設定リファレンス](/ja/configuration/) — すべてのフィールド。
- [エージェントループリファレンス](/ja/agent-loop/) — ライブラリ組み込み契約。
- [MCP](/ja/mcp/) — クライアントの配線。
