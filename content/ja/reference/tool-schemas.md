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
description: "The exact JSON schemas for the five built-in tools rousseau ships: read, write, edit, grep, bash."
keywords: "tool schemas, read, write, edit, grep, bash, JSON Schema"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/reference/tool-schemas/"
subtitle: "JSON schemas for the five built-in tools, verbatim from internal/tools/builtin."
tags: "reference, tools, json-schema, read, write, edit, grep, bash"
title: "リファレンス：ツールスキーマ"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tool schemas, read, write, edit, grep, bash, JSON Schema"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "リファレンス：ツールスキーマ"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 54
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/reference/tool-schemas/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/tool-schemas/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "リファレンス：ツールスキーマ"
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
twitter_description: "The exact JSON schemas for the five built-in tools rousseau ships: read, write, edit, grep, bash."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "リファレンス：ツールスキーマ"
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

## このページとは

`internal/tools/builtin/*.go` のすべての組み込みツールは、JSON Schema マップを返す `InputSchema()` メソッドを公開しています。このページはそれらのスキーマを正確に再現し、各ツールの実行時コントラクトに関する 1 段落を加えます。

5 つの組み込みツールは: [`read`](#read)、[`write`](#write)、[`edit`](#edit)、[`grep`](#grep)、[`bash`](#bash) です。5 つすべてがデーモン配線で構築されます。承認者 (`internal/agent/approver.go`) はモデルのツール呼び出しとツールの `Execute` メソッドの間に位置します。

## read

ソース: `internal/tools/builtin/read.go`。

**説明 (モデルに表面化):** _UTF-8 テキストファイルの内容を読み取る。入力: 絶対パス。ファイルの内容またはエラーを返す。_

**入力スキーマ:**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "Absolute filesystem path to the file to read."
    }
  },
  "required": ["path"]
}
```

**コントラクト。** `path` は絶対パス (`filepath.IsAbs`) である必要があります。ツールはファイル全体をメモリに読み込み、最初の 512 バイトに NUL バイトが含まれていれば拒否します (`isLikelyText`)。成功時にはファイル内容を文字列として返し、そうでなければエラー。ツールレベルでは行数やサイズ制限は強制されません — ファイルサイズを境界付けるには承認ポリシーが正しい場所です。

## write

ソース: `internal/tools/builtin/write.go`。

**説明 (モデルに表面化):** _UTF-8 テキストをファイルに書き込み、既存の内容を置き換える。必要に応じて親ディレクトリを作成。入力: 絶対パス + コンテンツ。_

**入力スキーマ:**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "Absolute filesystem path to write."
    },
    "content": {
      "type": "string",
      "description": "The complete file contents to write."
    }
  },
  "required": ["path", "content"]
}
```

**コントラクト。** ファイル全体を上書きします。モード `0o755` で親ディレクトリを作成します。モード `0o644` で書き込みます。絶対パスが必要です。`"wrote N bytes to /path"` を返します。意図的にアトミックスワップのダンスはありません — pattern モードの承認者は書き込みターゲットを特定のディレクトリツリーに固定します。ツール自体はファイルシステムの安全性について賢くしようとしません。

## edit

ソース: `internal/tools/builtin/edit.go`。

**説明 (モデルに表面化):** _ファイル内で old_string の正確に 1 つの出現を new_string で置き換える。old_string はファイル内でユニークである必要がある。ゼロ回または複数回出現する場合は編集が失敗する。インデントを正確に保持する。_

**入力スキーマ:**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "Absolute filesystem path to the file to edit."
    },
    "old_string": {
      "type": "string",
      "description": "Exact text to find. Must be unique in the file."
    },
    "new_string": {
      "type": "string",
      "description": "Text to replace old_string with."
    }
  },
  "required": ["path", "old_string", "new_string"]
}
```

**コントラクト。** 完全一致文字列の置換、正規表現ではありません。`old_string` はファイル内に **正確に 1 回** 出現する必要があります — ゼロマッチまたは複数マッチはどちらも記述的なエラーで失敗します。これは意図的です (Claude Code の Edit ツールから借用)。偶発的なマス置換を防止し、曖昧さを解消するためにモデルに十分な周辺コンテキストを含めることを強制します。`old_string == new_string` もエラーになります。`"edited /path (1 replacement)"` を返します。

## grep

ソース: `internal/tools/builtin/grep.go`。

**説明 (モデルに表面化):** _ディレクトリ配下のファイルを Go 正規表現で検索する。バイナリファイルと設定された制限より大きいファイルをスキップする。'path:line: matched_line' 行を返す。_

**入力スキーマ:**

```json
{
  "type": "object",
  "properties": {
    "pattern": {
      "type": "string",
      "description": "Go RE2 regular expression to match."
    },
    "path": {
      "type": "string",
      "description": "Absolute directory to search under."
    },
    "include": {
      "type": "string",
      "description": "Optional filename glob (e.g. '*.go'). Applied to the base name."
    },
    "ignore_case": {
      "type": "boolean",
      "description": "Case-insensitive match. Defaults to false."
    }
  },
  "required": ["pattern", "path"]
}
```

**コントラクト。** RE2 正規表現、PCRE ではありません。`ignore_case: true` のとき大文字と小文字を区別しません (`(?i)` を先頭に付けることで実装)。`.git`、`node_modules`、`vendor`、`.venv`、`__pycache__`、`dist`、`build` という名前のディレクトリをスキップします。`MaxFileBytes` (デフォルト 4 MiB) より大きいファイルをスキップします。出力を `MaxMatches` (デフォルト 200) で切り詰め、上限にヒットしたとき `(truncated at N matches)` フッターを追加します。現在の行に NUL バイトを含むファイルをスキップします (大まかなバイナリ検出)。

## bash

ソース: `internal/tools/builtin/bash.go`。

**説明 (モデルに表面化):** _`/bin/sh -c` 経由でシェルコマンドを実行する。終了ステータスとともに結合された stdout+stderr を返す。_

**入力スキーマ:**

```json
{
  "type": "object",
  "properties": {
    "command": {
      "type": "string",
      "description": "The shell command to execute."
    }
  },
  "required": ["command"]
}
```

**コントラクト。** `/bin/sh -c <command>`。結合された stdout + stderr、`bytes.Buffer` (すなわち RAM) に収まるものまで上限。デフォルト 60 秒のタイムアウト (構築時に設定可能)。タイムアウト時: 部分出力と `bash: timed out after 60s` エラーを返します。**ツールレベルではサンドボックスなし。** デーモンの OS ユーザー、ファイルシステムビュー、ネットワーク姿勢、seccomp プロファイルが封じ込めです。pattern モードの承認者が許可されるコマンドを狭める方法です — [チュートリアル: 承認者をハーデンする](/ja/tutorials/harden-approver-policy/) を参照してください。

## MCP 公開ツール

rousseau の stdio MCP サーバー (`rousseau mcp`) は **異なる** ツールセットを公開します — セッションストアと cron ジョブに対する読み取り専用クエリ。`rousseau_search_sessions`、`rousseau_list_sessions`、`rousseau_read_session`、`rousseau_cron_list` については [MCP: 公開ツール](/ja/mcp/exposed-tools/) を参照してください。

## 関連

- [ユーザーガイド: ツール](/ja/user-guide/tools/) — オペレーター向けのビュー。
- [ガイド: ファイル管理](/ja/guides/file-management/) — `write`/`edit` がバインドマウントと SELinux とどう相互作用するか。
- [ガイド: 監査 + 承認ポリシー](/ja/guides/audit-approval-policies/) — pattern 正規表現が各ツールの入力をどう制約するか。
- [デベロッパーガイド: ツールの追加](/ja/developer-guide/add-a-tool/) — このセットを拡張します。
