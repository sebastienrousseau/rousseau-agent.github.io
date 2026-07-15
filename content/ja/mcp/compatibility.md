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
description: "MCP clients tested against rousseau's stdio server: Claude Desktop, Claude CLI, Continue, Codeium, plus setup snippets."
keywords: "mcp, compatibility, claude desktop, continue, codeium, stdio, claude_desktop_config"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/mcp/compatibility/"
subtitle: "Which MCP clients talk to rousseau's stdio server."
tags: "mcp, compatibility, claude, continue, stdio"
title: "MCP：互換性"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, compatibility, claude desktop, continue, codeium, stdio, claude_desktop_config"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP：互換性"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "mcp"
order: 71
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/mcp/compatibility/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/compatibility/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "MCP：互換性"
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
twitter_description: "MCP clients tested against rousseau's stdio server: Claude Desktop, Claude CLI, Continue, Codeium, plus setup snippets."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP：互換性"
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

## プロトコルコントラクト

rousseau の MCP サーバー (`internal/mcp/server.go`) は stdio 上で JSON-RPC 2.0 を話し、`internal/mcp/tools.go` で宣言されたツールをアドバタイズします。以下のメソッドを処理します:

- `initialize` — `ServerCapabilities.Tools` を返します。
- `initialized` — 通知、返信なし。
- `ping` — `{}` を返します。
- `tools/list` — 挿入順で 4 つのツールを返します。
- `tools/call` — ツールハンドラを呼び出し、`content` と `isError` を持つ `ToolsCallResult` を返します。
- `resources/list`、`prompts/list` — 空の配列を返します (以下のロードマップノートを参照)。
- `shutdown` — `{}` を返します。

stdio JSON-RPC を話し、上記の 4 つのメソッドを呼び出す任意の MCP ホストが互換です。

## テスト済みクライアント

| クライアント | ステータス | 登録方法 |
|---|---|---|
| Claude Desktop (macOS / Windows) | 動作。 | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) または `%APPDATA%\Claude\claude_desktop_config.json` (Windows)。 |
| Claude CLI (`claude`) | 動作。 | `--mcp-config <file>` または `~/.claude/config.json` の `[mcp]` ブロック。 |
| Continue.dev (VS Code / JetBrains) | 動作。 | `~/.continue/config.json` の `mcpServers` ブロック。 |
| Codeium (IDE 拡張) | Codeium が MCP ホストモードを公開しているとき動作 (最近のリリース)。セットアップは IDE ごとに異なります。 |
| Cursor (最近のバージョン) | 動作。Cursor 独自の MCP 設定 UI で登録します。 |
| 任意の Go / TypeScript / Python MCP ホスト SDK | 動作。`command: "rousseau", args: ["mcp"]` でインスタンス化します。 |

未知 / 未テストだがおそらく互換: `zed`、`windsurf`、`aider`。ホストが MCP stdio 仕様をサポートしていれば、rousseau は動作します。

## Claude Desktop

`claude_desktop_config.json` (上記のパス) を編集して追加:

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

Claude Desktop を再起動してください。4 つの `rousseau_*` ツールが次のチャットセッションでツールピッカーに表示されます。

ワークスペースごとの状態には、env 上書きを追加:

```json
{
  "mcpServers": {
    "rousseau-work": {
      "command": "/usr/local/bin/rousseau",
      "args": ["--config", "/home/seb/.config/rousseau/work.yaml", "mcp"]
    }
  }
}
```

## Claude CLI

CLI を config に向けます:

```sh
claude --mcp-config <(cat <<'JSON'
{
  "mcpServers": {
    "rousseau": {
      "command": "rousseau",
      "args": ["mcp"]
    }
  }
}
JSON
)
```

または、同じ形状を使用して `~/.claude/config.json` の `mcpServers` ブロックの下に焼き付けてください。

## Continue.dev

`~/.continue/config.json` に追加:

```json
{
  "mcpServers": [
    {
      "name": "rousseau",
      "command": "rousseau",
      "args": ["mcp"]
    }
  ]
}
```

Continue は次のモデル呼び出しでツールを拾います。

## Cursor

Cursor は設定 > MCP UI で MCP 登録を公開します。コマンド `rousseau`、args `mcp` で `rousseau` という新しいサーバーを登録します。config ファイルの編集は不要です。

## Codeium

Codeium の MCP サポートは、IDE 拡張の最近のバージョンで機能フラグの背後で出荷されます。拡張のドキュメントを参照してください — 登録はまたも `command / args` ペアです。

## 環境変数とシークレット

rousseau の MCP 表面はセッションストア上で読み取り専用のため、プロバイダー資格情報を必要としません。`ANTHROPIC_API_KEY` などは `rousseau mcp` では使用されません — セッションを _生成する_ トランスポート / チャットデーモンのみが使用します。

## 一般的な問題

- **「Server exited immediately.」** rousseau の `mcp` コマンドは `state.path` を開きます。ファイルが書き込み不可の場合、プロセスは 0 以外で終了します。正確なエラーを見るためにシェルから `rousseau mcp` を実行してください。
- **「Unknown tool: rousseau_search_sessions.」** ホストが古いツール一覧をキャッシュしました。ホストを再起動してください。
- **重複登録。** 同じ名前で 2 つの rousseau サーバーが登録されている場合、最後の 1 つだけが勝ちます。

## リソースとプロンプト

`resources/list` と `prompts/list` は現在空を返します。セッションを MCP リソースとして公開するロードマップは [公開リソース](/ja/mcp/exposed-resources/) ページが追跡します。

## 関連

- [MCP](/ja/mcp/) — アンブレラリファレンス。
- [MCP: 公開ツール](/ja/mcp/exposed-tools/) — すべてのツールシグネチャ。
- [MCP: 公開リソース](/ja/mcp/exposed-resources/) — ロードマップ。
- [チュートリアル: MCP 経由でツールを公開する](/ja/tutorials/expose-tools-via-mcp/) — 作業例。
