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
date: "July 13, 2026"
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
description: "Full session lifecycle: list, search, show, delete, compression triggers, and restoration from the SQLite session store."
keywords: "session, lifecycle, list, search, delete, compression, sqlite"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/guides/session-management/"
subtitle: "List, search, delete, compress, restore."
tags: "guides, session, sqlite, compression"
title: "ガイド：セッション管理"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "session, lifecycle, list, search, delete, compression, sqlite"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ガイド：セッション管理"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 42
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/guides/session-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/session-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "ガイド：セッション管理"
last_build_date: "Mon, 13 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
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
twitter_description: "Full session lifecycle: list, search, show, delete, compression triggers, and restoration from the SQLite session store."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "ガイド：セッション管理"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "自らのコーディングエージェントを運用するすべてのオペレーターに感謝します。"
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## セッションライフサイクル

セッションは、`sessions` テーブル (`internal/state/sqlite/schema.sql`) の 1 行として永続化される 1 つの `agent.Session` 値です。`id`、`title`、時系列順に並んだ `Message` 値のスライス、タイムスタンプを持ちます。作成されると、削除するまで存在します。

セッションは各エントリポイントによってオンデマンドで作成されます:

- `rousseau chat` — TUI セッションごとに 1 つ (`chat` 呼び出しごとに新しいもの。既存のものを再利用するにはセッションピッカーを構築する必要があります)。
- すべてのトランスポート (`whatsapp`、`slack`、…) — JID マップ (`internal/state/sqlite/jidmap.go`) 経由で JID ごとに 1 セッション。
- `rousseau cron` — 各発火は、その実行に境界付けされたワンショットセッションです。

## 列挙

```sh
rousseau session list --limit 10
```

出力 (`internal/cli/session.go` の `newSessionListCmd` から):

```
<short-id>  <messages>  <updated_at>  <title>
```

`--limit 0` は無制限の行を返します。

## 検索

記録されたすべてのメッセージに対する FTS5:

```sh
rousseau session search 'retry logic'
rousseau session search '"exponential backoff" AND anthropic'
rousseau session search 'retr*'                # prefix
```

このコマンドは `Store.Search` (`internal/state/sqlite/search.go`) を `SearchOptions{Limit: N}` でラップします。ランキングは BM25 です。スニペットは約 200 文字にトリミングされます。

## 表示

```sh
rousseau session show <session-id>
```

アシスタントメッセージ間に `→ tool_use(name, input)` と `← tool_result` マーカーを含む完全なトランスクリプトを出力します。無人デーモンのセッションを監査するのに便利です。

## 削除

```sh
rousseau session delete <session-id> --yes
```

`--yes` フラグは必須です (`newSessionDeleteCmd`)。削除は FTS5 トリガーを通じてカスケードするため、再呼び出しインデックスは一貫性を保ちます。

## 圧縮トリガー

`config.yaml` で `agent.compression.enabled: true` の場合、`LLMCompressor` (`internal/agent/compressor.go`) は各ターンの前に 2 つの条件を確認します:

- `len(s.Messages) >= trigger_messages` (デフォルト 60)。
- `len(s.Messages) > keep_recent` (デフォルト 8)。

両方が成立する場合、コンプレッサーは最も古いスライスを `[rousseau-compressed]` マーカーが先頭に付いた 1 つの合成ユーザーメッセージに要約し、最後の `keep_recent` メッセージを逐語的に保持します。書き直されたセッションはメモリ内で元のものを置き換え、次の `Store.Save` で永続化されます。

すでに圧縮されたセッションでの 2 回目の圧縮は、セッションが `2 * trigger_messages` を超えて成長していない限りスキップされます — これは、毎ターン再要約に支払うことなく、暴走的な成長を境界付けます。

ログ行:

```
INFO agent.compressed messages=68
```

## 復元

セッションは自動的に復元されます。トランスポートルーター (`internal/transport/router.go`) はインバウンドで JID → セッション ID マッピングをルックアップし、次に `Store.Load` が JSON ペイロードを `agent.Session` にアンマーシャルします。手動ステップはありません。

マッピングが古い場合 — セッション ID が `jid_sessions` に存在するが `sessions` にはない場合 — `router.stale_mapping` (WARN) が表示され、ルーターは新しいセッションを作成します。部分削除からのレガシーアーティファクトです。無視して安全です。

## バックアップからの手動復元

`.backup` スナップショットから全体のセッションストアをロールバックするには:

```sh
systemctl --user stop rousseau-agent
cp /backup/sessions.db.2026-07-12.bak ~/.local/share/rousseau/sessions.db
rm -f ~/.local/share/rousseau/sessions.db-wal ~/.local/share/rousseau/sessions.db-shm
systemctl --user start rousseau-agent
```

`-wal` と `-shm` ファイルはプライマリと共に drop する必要があります。SQLite は次回オープン時にそれらを再構築します。

## 経過時間による一括削除

「X より古いセッションを削除する」組み込み CLI はありません。SQLite を通じて drop してください:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions WHERE updated_at < datetime('now', '-90 days');
SQL
```

FTS5 トリガーが再呼び出しインデックスを一貫性のある状態に保ちます。

## プライバシーの保護

セッションコンテンツは JSON ブロブ内にプレーンテキストで格納されるため、`sessions.db` を機密として扱ってください。オプション:

- **ファイルシステムレベルの暗号化。** Linux では LUKS、macOS では FileVault。
- **暗号化されたバックアップ。** `restic` と `borg` は両方とも保存時に暗号化します。
- **ワンショットセッションの完了時削除。** cron 駆動のデーモンでは、post-run フックが完了したばかりのセッション ID を `rousseau session delete` することができます。今日は組み込まれていません。レビューについては [ガイド: エンタープライズオンボーディング](/ja/guides/enterprise-onboarding/) を参照してください。

## `rousseau session` コマンドの完全リファレンス

<div class="tabs" data-tabs="session-commands">
  <div class="tab-list" role="tablist" aria-label="Session subcommand">
    <button role="tab" aria-selected="true">list</button>
    <button role="tab" aria-selected="false">show</button>
    <button role="tab" aria-selected="false">search</button>
    <button role="tab" aria-selected="false">delete</button>
    <button role="tab" aria-selected="false">export</button>
  </div>
  <div class="tab-panel" role="tabpanel">

セッションを新しい順に列挙:

```sh
rousseau session list
rousseau session list --limit 100
rousseau session list --json
```

カラム: `ID`、`Title`、`Messages`、`UpdatedAt`。`--json` フラグは、スクリプト化されたコンシューマー向けに 1 行あたり 1 オブジェクトを発します。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

セッションの完全なトランスクリプトを出力:

```sh
rousseau session show <session-id>
rousseau session show <session-id> --raw
```

`--raw` は格納されているとおりの JSON を出力します (デバッグに便利)。`--raw` なしでは、ツール呼び出しは `→ tool_use(name, input)` として、結果は `← tool_result` としてレンダリングされます。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

すべてのセッションにわたる全文検索:

```sh
rousseau session search "refactor login"
rousseau session search "TODO" --limit 10
```

FTS5 インデックスを使用します (`internal/state/sqlite/` を参照)。結果は関連性でランク付けされ、マッチした用語がハイライトされたスニペットを含みます。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

セッションとその FTS5 エントリを削除:

```sh
rousseau session delete <session-id> --yes
```

`--yes` フラグは必須です — 対話的な確認はありません。削除は SQL トリガー経由でカスケードするため、再呼び出しインデックスは一貫性を保ちます。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

セッションを JSON としてエクスポート:

```sh
rousseau session export <session-id> > session.json
```

エクスポートされた形式は、ディスク上の JSON ブロブと一致します。再インポートはまだサポートされていません (ロードマップ)。

  </div>
</div>

## トラブルシューティング

### `session not found`

渡した ID は存在しません。大文字と小文字を区別します。有効な ID を確認するには `rousseau session list` を使用してください。

### FTS5 検索が何も返さない

FTS5 が配線される前にインポートされたレガシーセッションでは、インデックスが古くなっている可能性があります。何らかのコンテンツ変更操作を実行して再構築するか (削除で reindex がトリガーされます)、SQLite 経由で手動で reindex してください。

### 読み取り時の `database is locked`

別のデーモンが WAL 書き込みロックを保持しています。読むだけであれば、読み取り専用 DSN (`?mode=ro`) を使用してください。

### セッションストアが速く成長しすぎる

圧縮を有効化し (`agent.compression.enabled: true`)、SQLite ファイルを定期的に `VACUUM` してスペースを回収してください。

### バックアップからの復元が古い状態を生成する

デーモンを起動する前に `-wal` と `-shm` を drop したことを確認してください。`-wal` が存在する場合、SQLite は WAL を再生し、復元を取り消す可能性があります。

## 関連ページ

- [リファレンス: セッションストア](/ja/reference/session-store/) — スキーマと DDL。
- [ガイド: ワークスペースの管理](/ja/guides/managing-workspaces/) — ワークスペースごとのストア。
- [ガイド: コンテキスト管理](/ja/guides/context-management/) — 圧縮が何を保持するかを決定する方法。
- [ユーザーガイド: CLI](/ja/user-guide/cli/) — コマンドシグネチャ。
- [ユーザーガイド: 圧縮 &amp; 再呼び出し](/ja/user-guide/compression-recall/) — コンプレッサーと FTS5 再呼び出しの内部。

## さらに読む

- `internal/cli/session.go` — CLI 配線。
- `internal/state/sqlite/store.go` — DSN、WAL、インデックス。
- `internal/agent/session.go` — `Session` 構造体。
- `internal/agent/compressor.go` — `LLMCompressor`。
- `internal/agent/recall.go` — `SQLiteRecall`。
