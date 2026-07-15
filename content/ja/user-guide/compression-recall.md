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
description: "Session compression triggers and FTS5 cross-session recall in rousseau-agent. How the agent loop keeps long sessions inside the model's context."
keywords: "compression, recall, fts5, session, context window, summarisation, trigger_messages, keep_recent"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/user-guide/compression-recall/"
subtitle: "Session compression and FTS5 cross-session recall."
tags: "compression, recall, session, fts5"
title: "圧縮とリコール"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "compression, recall, fts5, session, context window, summarisation, trigger_messages, keep_recent"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "圧縮とリコール"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "concepts"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/user-guide/compression-recall/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/compression-recall/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "圧縮とリコール"
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
twitter_description: "Session compression triggers and FTS5 cross-session recall in rousseau-agent. How the agent loop keeps long sessions inside the model's context."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "圧縮とリコール"
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

## 2 つの問題、2 つのメカニズム

- 1 つの長いセッションはモデルのコンテキストウィンドウを超えることがあります。**圧縮** は古いメッセージを要約ブロックに折り畳み、ループが動作し続けるようにします。
- 関連トピックの新しいセッションは、以前の会話の価値を失います。**再呼び出し** はセッション横断で FTS5 インデックスを照会し、抜粋をシステムプロンプトにスプライスします。

圧縮は現在のセッションを in-place で編集します。再呼び出しは決して編集しません — 現在のターンのシステムプロンプトにコンテキストを追記します。

## 圧縮

`internal/agent/compressor.go` は LLM ベースのサマライザーを実装します。エージェントループは各 `Turn` の開始時にそれを参照します:

```go
if changed, err := a.opts.Compressor.Compress(ctx, s); err != nil {
    a.logger.Warn("agent.compress_failed", slog.String("err", err.Error()))
} else if changed {
    a.logger.Info("agent.compressed", slog.Int("messages", len(s.Messages)))
}
```

セッションが短い場合、何も起こりません。メッセージ数が `trigger_messages` を超えると、コンプレッサーは:

1. セッションの末尾 — 最新の `keep_recent` メッセージ — を分離し、逐語的に保持します。
2. それより古いものすべてを要約プロンプト付きでプロバイダーに送ります。
3. 古いブロックを、要約を含む 1 つの合成 `RoleSystem` メッセージで置き換えます。
4. 要約ブロックが次のプロバイダー呼び出しでプロンプトキャッシュ適格なプレフィックスに位置するようにセッションをマークします。

その後ループは、より小さいメッセージリストに対して進みます。ユーザーは継ぎ目を決して見ません。

### 圧縮の有効化

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60      # zero → default 60
    keep_recent: 8            # zero → default 8
    prompt: ""                # zero → sensible default
```

| フィールド | デフォルト | 意味 |
|---|---|---|
| `enabled` | `false` | デフォルトはオフ。 |
| `trigger_messages` | 60 | 圧縮が発火するメッセージ数のしきい値。 |
| `keep_recent` | 8 | 逐語的に保持する最新メッセージ数。 |
| `prompt` | 組み込み | 要約指示を上書きします。 |

### オフのままにするとき

圧縮は発火ごとにプロバイダー 1 ラウンドトリップを使用します。サブスクリプション階層の `claudecli` アカウントでは、そのトリップは無料です — 自由に有効化してください。トークン従量課金 API では、各発火にコストがあるため、`trigger_messages` を上に調整するか、短命セッションでは無効のままにしてください。

### オンのままにするとき

- WhatsApp スレッドが何週間にもわたって成長する長寿命チャットトランスポートデーモン。
- 返信がフォローアップのプロンプトを供給する cron スケジュール済みプロンプト。
- トークンコストがゼロのセルフホストプロバイダー。

### 圧縮を越えて保持されるセマンティクス

- tool-use / tool-result ペアは決して分割されません。`tool_use` が圧縮領域にあり、その `tool_result` が保持領域にある場合、両方が要約に折り畳まれます。
- コンプレッサーは進行中の現在のユーザーターンを決して書き換えません。
- プロンプトキャッシング (`internal/llm/anthropic` の `cache_control` マーカー) は要約ブロックに配置されるため、次の呼び出しはキャッシュから読み取ります。

## 再呼び出し

`internal/state/sqlite/` は、すべてのメッセージをインデックス化する FTS5 仮想テーブルを維持します。`RecallProvider` はこのテーブルに対してクエリを実行し、システムプロンプトの追記を返します。

### インターフェース

```go
type RecallProvider interface {
    SystemAppendix(ctx context.Context, s *Session) string
}
```

エージェントループはイテレーションごとに 1 回これを呼び出します。空でないテキストを返した場合、そのイテレーションのベースシステムプロンプトにそのテキストが追記されます。

### デフォルトプロバイダー

`internal/agent/recall.go` は次のヒューリスティックを出荷します:

1. 現在のセッションの最後のユーザーメッセージから顕著なトークンを抽出します。
2. 他のセッション横断でそれらのトークンについて FTS5 インデックスに対して `MATCH` を実行します。
3. トップ N の抜粋を `Previously in another session:` ブロックとしてフォーマットします。
4. 設定された文字予算を超えないように追記を境界付けします。

### 再呼び出しの有効化

再呼び出しはエージェント構築時に配線されます。各トランスポートがどう配線するかは `internal/cli/chat.go` と `internal/cli/*.go` を参照してください。独自の組み込みでは:

```go
recall, err := sqlitestore.NewRecall(store)
if err != nil { /* ... */ }

ag := agent.New(provider, registry, logger, agent.Options{
    RecallProvider: recall,
})
```

### 承認者との相互作用

再呼び出しはセッションストアから読み取ります。ツール呼び出しを発火しません。承認者は相談されません。ストアの内容自体が信頼境界です。

### CLI からのセッション検索

再呼び出しはマシン向け機能です。人間には、同じ FTS5 インデックスが以下を動かします:

```sh
rousseau session search "kubectl"
rousseau session search "PVC not binding"
```

同じクエリエンジン、同じ結果、適切な RecallProvider が追加するかもしれない LLM 再ランキングを除いたもの。

## スキルとの相互作用

スキル ([スキル](/ja/skills/)) と再呼び出しは両方ともシステムプロンプトに追加します。固定順で構成されます:

1. ベースシステムプロンプト (`agent.system_prompt` またはデフォルトから)。
2. スキル追記 (もしあれば)。
3. 再呼び出し追記 (もしあれば)。

すべては 2 つの改行で区切られます。何も追加する必要がなければ、ベースプロンプトは変更されずに通過します。

## 要約ブロックのセマンティクス

合成要約メッセージは `RoleSystem` で発行されます。それはユーザーまたはアシスタントメッセージではないため、`rousseau session show` で会話ターンとして決して表示されません — `[compressed summary]` メタデータとして表示されます。

`rousseau chat --session <id>` で圧縮されたセッションを再開すると、要約は保持されます。仮想的なスキーマ編集経由で要約ブロックを削除するのは安全ではありません: モデルはそれを通じてのみ知られる事実を参照している可能性があります。

## 圧縮が発火していることの確認

```
INFO agent.compressed messages=12
```

`messages` は要約ブロックが圧縮プレフィックスを置き換えた後の新しいセッション長です。`WARN agent.compress_failed err=...` は要約プロバイダーがエラーになったことを意味します。ループは非圧縮セッションに対して継続しました。

## 注意事項

- 圧縮はロッシーです。要約はモデル生成テキストです。重要な詳細がドロップされる可能性があります。監査証跡のためには、完全なセッションをストアに保持してください — 圧縮はモデルが見るものにのみ影響し、SQLite が永続化するものには影響しません。
- 再呼び出しは FTS5 SQLite 拡張を必要とします。`modernc.org/sqlite` はデフォルトでそれを組み込みます。ストア実装をスワップする場合は、FTS5 が利用可能であることを確認してください。
- 両方の機能は UTF-8 テキストを想定します。ボイスノート文字起こし ([ボイスモード](/ja/user-guide/voice-mode/) を参照) は文字起こしされると通常のユーザーメッセージとしてカウントされます。

## 次に

- [コンセプト](/ja/concepts/) — エージェントループの概要。
- [設定](/ja/configuration/) — すべての `agent.compression.*` ノブ。
- [スキル](/ja/skills/) — 3 番目のシステムプロンプト入力。
