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
description: "Expose rousseau's session store and cron jobs to Claude Desktop as an MCP server that Claude can drive from its own tool interface."
keywords: "mcp, claude desktop, stdio, tools, rousseau_search_sessions, rousseau_read_session"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/tutorials/expose-tools-via-mcp/"
subtitle: "Wire rousseau mcp into Claude Desktop and let it query the session store."
tags: "tutorials, mcp, claude-desktop, stdio, sessions"
title: "チュートリアル：MCP でツールを公開する"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, claude desktop, stdio, tools, rousseau_search_sessions, rousseau_read_session"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "チュートリアル：MCP でツールを公開する"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/tutorials/expose-tools-via-mcp/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/expose-tools-via-mcp/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "チュートリアル：MCP でツールを公開する"
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
twitter_description: "Expose rousseau's session store and cron jobs to Claude Desktop as an MCP server that Claude can drive from its own tool interface."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "チュートリアル：MCP でツールを公開する"
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

## 構築するもの

rousseau を MCP stdio サーバーとする Claude Desktop。Claude Desktop チャット内から「リトライロジックについて議論したセッションを見つけて」と尋ねると、Claude は `rousseau_search_sessions` を呼び出し、次に `rousseau_read_session` を呼び出して完全なトランスクリプトを取得します。

想定時間: 5 分。

## 前提条件

- インストール済みの Claude Desktop (macOS または Windows)。Linux は Desktop ではなく Claude CLI を使用します — 下部の代替を参照してください。
- rousseau がインストールされ、`$PATH` にあること。
- `~/.local/share/rousseau/sessions.db` にいくつかの既存セッション履歴があること — ファイルが空の場合は `rousseau chat` を何度か実行してください。

## ステップ 1: 何が公開されるかを理解する

`rousseau mcp` (`internal/cli/mcp.go`) は Model Context Protocol を話す stdio JSON-RPC サーバーを起動します。`RegisterRousseauTools` (`internal/mcp/tools.go`) は 4 つの読み取り専用ツールをアタッチします:

| ツール | 目的 |
|---|---|
| `rousseau_search_sessions` | 記録されたすべてのセッションにわたる FTS5 全文検索 (`internal/state/sqlite/search.go` 経由)。 |
| `rousseau_list_sessions` | セッションを新しい順に列挙。 |
| `rousseau_read_session` | ID による 1 つのセッションの完全なトランスクリプトを返します。 |
| `rousseau_cron_list` | rousseau のスケジュールされた cron ジョブを列挙。 |

書き込みツールはありません。MCP ホストはブラウズできますが、変更はできません。正確な入力スキーマについては [MCP: 公開ツール](/ja/mcp/exposed-tools/) を参照してください。

## ステップ 2: Claude Desktop を配線する

Claude Desktop は `claude_desktop_config.json` を読み込みます:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

`rousseau` バイナリを指す `mcpServers` エントリを追加してください:

```json
{
  "mcpServers": {
    "rousseau": {
      "command": "/usr/local/bin/rousseau",
      "args": ["mcp"]
    }
  }
}
```

Claude Desktop を再起動してください。

## ステップ 3: 検証

Claude Desktop チャットを開き、ツールがツールピッカーに表示されることを確認してください。`rousseau_` で始まる 4 つのツールが見えるはずです。試してみてください:

```
Use rousseau_list_sessions to show me my 5 most recent sessions,
then read the top one with rousseau_read_session.
```

Claude は両方のツールを呼び出し、rousseau の MCP サーバー (`internal/mcp/server.go`) は stdin/stdout 上で各 JSON-RPC エンベロープを処理します。舞台裏では:

1. Claude Desktop は `initialize`、次に `tools/list` を呼び出します — rousseau は挿入順序で宣言された 4 つのツールで応答します。
2. Claude はツールを選択し、引数付きで `tools/call` を呼び出します — rousseau のハンドラ (`internal/mcp/tools.go` から) は SQLite を照会し、テキストコンテンツを返します。
3. エラーの場合、rousseau はコンテンツチャネル (`isError=true`) を通じてエラーを表面化し、JSON-RPC エラーとしては決してしません — MCP ホストはこれを期待しています。

## ステップ 4: (オプション) Claude CLI / 他の MCP ホストにアタッチする

stdio プロトコルはホスト非依存です。Claude CLI 用:

```sh
claude --mcp-config <(cat <<'JSON'
{ "mcpServers": { "rousseau": { "command": "rousseau", "args": ["mcp"] } } }
JSON
)
```

Continue.dev、Codeium、または他の MCP ホストの場合は、`command: rousseau`、`args: [mcp]` でそれらの MCP サーバー登録フローに従ってください。テスト済みクライアントについては [MCP: 互換性](/ja/mcp/compatibility/) を参照してください。

## ステップ 5: FTS5 構文チートシート

rousseau_search_sessions は SQLite FTS5 (`internal/state/sqlite/search.go`) の薄いラッパーであるため、クエリフィールドは以下をサポートします:

| クエリ | 意味 |
|---|---|
| `retry logic` | 両方の用語を含む任意のドキュメント。 |
| `"retry logic"` | 完全一致フレーズ。 |
| `retr*` | プレフィックスマッチ。 |
| `retry OR backoff` | 論理和 OR。 |
| `retry NOT retries` | 除外。 |

ランキングは BM25 を使用します (ランクが低いほど関連性が高い)。`Search` の `snippet()` 呼び出しはヒットごとに 200 文字のプレビューを与えます。

## トラブルシューティング

- **Claude Desktop で "unknown tool"。** アプリを再起動してください。ツール一覧はセッション開始時にのみ取得されます。
- **サーバーがすぐに終了する。** `rousseau mcp` は SQLite 状態ファイルを開きます。`state.path` のパスが書き込み可能でない場合、`Open()` は失敗し、プロセスは 0 以外のコードで終了します。エラーを見るためにシェルから実行してください。
- **空の検索結果。** FTS5 インデックスが populate されていることを確認してください: `sqlite3 ~/.local/share/rousseau/sessions.db "SELECT count(*) FROM sessions_fts"`。`internal/state/sqlite/search.go` の `EnsureSearch` はオープンごとにインデックスを back-fill しますが、破損した状態ファイルは手動での再構築が必要な場合があります。

## 関連

- [MCP](/ja/mcp/) — リファレンスドキュメント。
- [MCP: 公開ツール](/ja/mcp/exposed-tools/) — すべてのツールスキーマ。
- [MCP: 互換性](/ja/mcp/compatibility/) — テスト済みクライアント。
- [リファレンス: セッションストア](/ja/reference/session-store/) — ツールの背後にある SQLite スキーマ。
