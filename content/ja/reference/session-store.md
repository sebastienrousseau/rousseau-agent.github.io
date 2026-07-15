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
description: "Rousseau's SQLite session store: sessions table, FTS5 recall index, JID mapping table, cron jobs, and WAL journaling."
keywords: "sqlite, fts5, session store, sessions, jid, cron, WAL, schema"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/reference/session-store/"
subtitle: "The SQLite schema at the heart of rousseau's state."
tags: "reference, sqlite, fts5, session, wal"
title: "リファレンス：セッションストア"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "sqlite, fts5, session store, sessions, jid, cron, WAL, schema"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "リファレンス：セッションストア"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 53
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/reference/session-store/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/session-store/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "リファレンス：セッションストア"
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
twitter_description: "Rousseau's SQLite session store: sessions table, FTS5 recall index, JID mapping table, cron jobs, and WAL journaling."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "リファレンス：セッションストア"
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

## 場所とドライバー

セッションストアは `state.path` にある単一の SQLite データベースです (デフォルトは `~/.local/share/rousseau/sessions.db`、`internal/config/config.go` の `setDefaults` を参照)。

rousseau は `modernc.org/sqlite` を使用します — 純粋 Go の SQLite ドライバー。**CGO や libsqlite3 依存はありません**。`bin/rousseau` の Go バイナリは完全に静的です。

`internal/state/sqlite/store.go` の `Open()` は、開くたびに 4 つの pragma を適用します:

| PRAGMA | 目的 |
|---|---|
| `journal_mode=WAL` | write-ahead logging。並行リーダー、安全なライブバックアップを可能にします。 |
| `foreign_keys=ON` | 標準の整合性保証。 |
| `busy_timeout=15000` | ロック競合時の 15 秒待機 — 複数トランスポートが並行して書き込むと重要。 |
| — | `EnsureSearch` が後で実行され、FTS5 スキーマをインストールします。 |

ストアはプロセスごとに一度開かれます。同じ DB ファイルを指す複数のデーモンは、busy-timeout + WAL の組み合わせのおかげでサポートされます — WhatsApp ブリッジ、`rousseau mcp`、`rousseau session list` は安全にファイルを共有できます。

## スキーマツアー

### テーブル: `sessions`

`internal/state/sqlite/schema.sql` で定義:

```sql
CREATE TABLE IF NOT EXISTS sessions (
    id             TEXT PRIMARY KEY,
    title          TEXT NOT NULL,
    payload        TEXT NOT NULL,        -- JSON blob of the full agent.Session
    message_count  INTEGER NOT NULL DEFAULT 0,
    created_at     TEXT NOT NULL,
    updated_at     TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sessions_updated_at
    ON sessions(updated_at DESC);
```

**ペイロード形状。** `payload` カラムは完全な `agent.Session` JSON を格納します — 役割、コンテンツブロック、tool-use と tool-result ブロック、タイムスタンプ。`internal/state/sqlite/store.go` の `Save`/`Load` を参照してください。セッション全体を 1 つの JSON ブロブとして保持することで、スキーママイグレーションはまれになります。内部に対するクエリは以下の FTS5 インデックスを通ります。

**タイムスタンプ** はミリ秒精度の ISO-8601 (Go time 構文で `2006-01-02T15:04:05.000Z`)、UTC です。

**順序付け。** `idx_sessions_updated_at` は `List` と `RecentSessions` (両方とも `store.go` / `search.go` にある) を動かします。

### 仮想テーブル: `sessions_fts` (FTS5)

`internal/state/sqlite/search.go` の `searchSchema` でインストール:

```sql
CREATE VIRTUAL TABLE IF NOT EXISTS sessions_fts USING fts5(
    session_id UNINDEXED,
    title,
    body,
    tokenize = 'porter unicode61'
);
```

3 つのトリガー駆動の書き込みが `sessions` と一貫性を保ちます:

- `sessions_fts_ai` — `sessions` への INSERT 後、行をミラーします。
- `sessions_fts_au` — UPDATE 後、削除 + 再挿入します。
- `sessions_fts_ad` — DELETE 後、FTS 行を drop します。

**バックフィル。** `EnsureSearch` は各 `Open()` で `LEFT JOIN` を実行し、FTS インデックスがまだ持っていない `sessions` 行を挿入します。これにより、既存データベースへのインデックス追加が安全になります — 手動マイグレーション不要。

**トークン化。** `porter unicode61` — Porter ステマー + Unicode 対応の casefolding。大文字と小文字を区別せず、英語の形態論 (`retry`/`retries`/`retried`) を処理します。

**ランキング。** `Search()` は `bm25(sessions_fts)` で順序付けします (低いほど関連性が高い)。`SearchHit.Rank` がそれを公開します。

**クエリ構文。** FTS5 に逐語的に渡されます。オペレーターのチートシートについては [チュートリアル: MCP 経由でツールを公開する](/ja/tutorials/expose-tools-via-mcp/) を参照してください。

### テーブル: `jid_sessions`

プラットフォーム送信者からセッション ID へのマッピングを永続化します。`internal/state/sqlite/jidmap.go` の `NewJIDMap` でインストール:

```sql
CREATE TABLE IF NOT EXISTS jid_sessions (
    jid         TEXT PRIMARY KEY,
    session_id  TEXT NOT NULL,
    created_at  TEXT NOT NULL
);
```

すべての長時間実行トランスポートは JID マップを使用するため、同じ電話番号、Matrix ユーザー、または Slack ユーザーが再起動をまたいで同じ会話を継続します。`Router.Handle` (`internal/transport/router.go`) はインバウンドで検索します。`Put` は `Save` の後に書き込みます。

JID 空間はトランスポート固有です — WhatsApp の `447900123456@s.whatsapp.net`、Matrix の `@user:matrix.org`、Slack の `U01ABC…`。トランスポートが正規化を担当します。

### テーブル: `cron_jobs`

`internal/state/sqlite/cron.go` の `NewCronStore` でインストール:

```sql
CREATE TABLE IF NOT EXISTS cron_jobs (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    cron_expr   TEXT NOT NULL,
    prompt      TEXT NOT NULL,
    deliver_to  TEXT NOT NULL,
    enabled     INTEGER NOT NULL DEFAULT 1,
    created_at  TEXT NOT NULL,
    last_run_at TEXT
);
```

`UNIQUE(name)` は重複を防止します。`rousseau cron add/list/remove/enable/disable` (`internal/cli/cron.go` から) はすべてこのテーブルをラウンドトリップします。`internal/cron/scheduler.go` のスケジューラは `poll_interval` ごとに調停します。MCP は `rousseau_cron_list` 経由で読み取り専用に公開します。

## 並行性姿勢

- **WAL** は、単一ライターと並行して無制限の並行リーダーを許可します。
- **`busy_timeout=15000`** は、競合に当たったライターが fail-fast ではなく最大 15 秒待機することを意味します。実際には、WhatsApp ブリッジがライター役を保持し、`rousseau mcp` と `rousseau session list` は読み取り専用の訪問者です。
- ストアはクロスマシン並行性のために設計されていません。NFS 経由で同じファイルに書き込む 2 つのホストは未定義の挙動です — 単一ライターを使用し、リードレプリカのために DB を別の場所に rsync してください。

## バックアップ

最も安全なアプローチはライブ `sqlite3 .backup` です:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db ".backup '/backup/sessions.db.$(date -I).bak'"
```

`.backup` は SQLite のオンラインバックアップ API を使用し、プライマリが書き込まれている間に動作します。生ファイルに対する `restic` / `borg` スナップショットも WAL のおかげで安全です — バックアップは、ファイルが読み取られた瞬間の一貫したスナップショットを取得します。

`whatsapp.db` ファイル (whatsmeow デバイス資格情報) は別のデータベースです。復元後の再ペアリングを避けたい場合は、同じ方法でバックアップしてください。

## FTS インデックスの再構築

FTS5 インデックスが同期外れになった場合 (極めてまれ — トリガーが一貫性を保ちます)、それを再構築してください:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions_fts;
INSERT INTO sessions_fts (session_id, title, body)
SELECT id, title, payload FROM sessions;
SQL
```

rousseau の `EnsureSearch` はこれを取り消しません。トリガーはクリーン状態から再開するだけです。

## 関連

- [コンセプト](/ja/concepts/) — ストアが全体アーキテクチャのどこに位置するか。
- [ユーザーガイド: 圧縮 + 再呼び出し](/ja/user-guide/compression-recall/) — FTS インデックスがモデルにどう公開されるか。
- [MCP: 公開ツール](/ja/mcp/exposed-tools/) — このスキーマ上の読み取り専用表面。
- [ガイド: ワークスペースの管理](/ja/guides/managing-workspaces/) — マシン間でストアを共有 / パーティション化します。
