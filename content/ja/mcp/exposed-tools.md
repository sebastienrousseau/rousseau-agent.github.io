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
description: "The exact tool signatures exposed by rousseau's stdio MCP server, mirroring internal/mcp/tools.go."
keywords: "mcp, rousseau_search_sessions, rousseau_list_sessions, rousseau_read_session, rousseau_cron_list"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/mcp/exposed-tools/"
subtitle: "Every tool rousseau's MCP server advertises, with schemas."
tags: "mcp, tools, sessions, cron"
title: "MCP：公開ツール"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, rousseau_search_sessions, rousseau_list_sessions, rousseau_read_session, rousseau_cron_list"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP：公開ツール"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "mcp"
order: 72
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/mcp/exposed-tools/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/exposed-tools/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "MCP：公開ツール"
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
twitter_description: "The exact tool signatures exposed by rousseau's stdio MCP server, mirroring internal/mcp/tools.go."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP：公開ツール"
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

## 登録

`internal/cli/mcp.go` は SQLite セッションストアを開き、`NewCronStore` を構築し、両方を `mcp.NewStoreBackend` にラップし、`mcp.RegisterRousseauTools(s, backend)` を呼び出します。以下の 4 つのツールは挿入順序でアタッチされます — `tools/list` はこの順序でそれらを返します。

すべてのツールは読み取り専用です。今日 MCP 経由の書き込み表面はありません。これは設計によるものであり、MCP ホストが rousseau の状態を変更できないようにするためです。

## `rousseau_search_sessions`

**説明 (ホストに表面化):** _記録されたすべての rousseau セッションにわたる全文検索。SQLite FTS5 構文を使用 (ダブルクォート内のフレーズ、AND/OR/NOT、プレフィックスワイルドカード)。_

**入力スキーマ:**

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "FTS5 query"
    },
    "limit": {
      "type": "integer",
      "description": "Cap hits returned. Default 20."
    }
  },
  "required": ["query"]
}
```

**挙動。** `query` を SQLite の FTS5 エンジン (`internal/state/sqlite/search.go` の `Store.Search`) に逐語的に渡します。結果は BM25 ランクで順序付けされます (低い = より関連性が高い)。各ヒットは 3 行としてレンダリングされます:

```
session <id> (rank 0.42)
    title:   <session title>
    snippet: <~200-char snippet with … ellipses>
```

**エラー。** 空のクエリは `query is required` を返します。FTS5 構文エラーは SQLite エラーとしてバブルアップし、`isError: true` 経由で表面化されます。

## `rousseau_list_sessions`

**説明 (ホストに表面化):** _rousseau セッションを新しい順に一覧表示する。_

**入力スキーマ:**

```json
{
  "type": "object",
  "properties": {
    "limit": {
      "type": "integer",
      "description": "Cap rows returned. Default 20."
    }
  }
}
```

**挙動。** `idx_sessions_updated_at DESC` インデックスを使用する `Store.List` を呼び出します。各行:

```
<session-id>  <title>  msgs=<count>  updated=<iso-8601>
```

ストアが空のとき `(no sessions)` を返します。

## `rousseau_read_session`

**説明 (ホストに表面化):** _ID で rousseau セッションの完全なトランスクリプトを返す。_

**入力スキーマ:**

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "description": "Session id"
    }
  },
  "required": ["id"]
}
```

**挙動。** 完全な `agent.Session` を取得するために `Store.Load` を呼び出します。次のようにレンダリングされます:

```
id: <session-id>
title: <session title>
created: <iso-8601>
updated: <iso-8601>
messages: <count>

[0] user
    <text content>
[1] assistant
    <text content>
    ...
```

テキストコンテンツのみがレンダリングされます — tool_use ブロックと tool_result ブロックは MCP 表面では省略されます (CLI の `rousseau session show` はそれらを含みます。MCP は意図的に含みません)。

**エラー。** 空入力で `id is required`。未知の ID で `state.ErrNotFound`。

## `rousseau_cron_list`

**説明 (ホストに表面化):** _rousseau のスケジュールされた cron ジョブを一覧表示する (name、schedule、prompt、delivery target)。_

**入力スキーマ:**

```json
{
  "type": "object",
  "properties": {}
}
```

**挙動。** `CronStore.List` を呼び出します — `cron_jobs` 行ごとに 1 行:

```
<name> [<on|off>] <cron-expr> → <deliver-to>  prompt="<prompt>"  deliver=<deliver-to>
```

cron テーブルが空のとき `(no jobs)` を返します。構築時に `CronStore` が nil の場合も `(no jobs)` を返します (`storeBackend.CronList` の防御的パス)。

## 公開されていないもの

意図的な省略:

| 表面 | なぜないか |
|---|---|
| `rousseau_write_session` / `rousseau_delete_session` | MCP 経由の変更は、信頼できないホストが rousseau の監査証跡を再形成することを許可します。 |
| `rousseau_add_cron` | 同じ理由 — 変更。cron ジョブは `rousseau cron add` 経由で追加してください。 |
| 組み込みツール (`read`、`write`、`edit`、`grep`、`bash`) | これらは rousseau 独自ループ内の LLM 向けエージェント向けツールであり、ホスト向けではありません。それらを公開すると、MCP ホストが rousseau を実行しているホスト上でシェルアウトする能力を得ることになります — まさに私たちが望まない信頼の反転です。 |
| JID マップルックアップ | PII (電話番号) を公開します。必要なら、デーモンが実行されるマシンで SQLite に直接照会してください。 |

## エラー表面

MCP ハンドラは `([]Content, error)` を返します。エラー時、サーバー (`internal/mcp/server.go` の `handleToolsCall`) はエラーを `ToolsCallResult{Content: text of err, IsError: true}` として表面化します。これは MCP 慣習に沿っています: ツールの失敗は JSON-RPC の `error` チャネルではなく、`isError=true` でコンテンツチャネルを通じて流れます。ホストはテキストをレンダリングして継続する必要があります。

## 関連

- [MCP](/ja/mcp/) — アンブレラリファレンス。
- [MCP: 互換性](/ja/mcp/compatibility/) — テスト済みクライアント。
- [MCP: 公開リソース](/ja/mcp/exposed-resources/) — ロードマップ。
- [リファレンス: ツールスキーマ](/ja/reference/tool-schemas/) — 異なるエージェント向けツールセット。
