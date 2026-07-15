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
description: "The five built-in tools shipped with rousseau-agent: read, write, edit, grep, bash. JSON schemas, execution semantics, safety notes."
keywords: "tools, read, write, edit, grep, bash, json schema, tool registry"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/user-guide/tools/"
subtitle: "The five built-in tools, with schemas and safety notes."
tags: "tools, reference, read, write, edit, grep, bash"
title: "組み込みツール"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tools, read, write, edit, grep, bash, json schema, tool registry"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "組み込みツール"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 42
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/user-guide/tools/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/tools/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "組み込みツール"
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
twitter_description: "The five built-in tools shipped with rousseau-agent: read, write, edit, grep, bash. JSON schemas, execution semantics, safety notes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "組み込みツール"
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

## 出荷されるもの

`internal/tools/builtin/` は、すべての rousseau デーモンがデフォルトで配線する 5 つのツールを提供します (配線については `internal/cli/chat.go` を参照):

| ツール | 目的 | 変更する? |
|---|---|:---:|
| `read` | UTF-8 テキストファイル読み取り。 | いいえ |
| `write` | UTF-8 テキストファイル上書き。親を作成。 | はい |
| `edit` | 完全一致文字列の置換、ユニークマッチが必要。 | はい |
| `grep` | ディレクトリ配下の RE2 正規表現検索。 | いいえ |
| `bash` | タイムアウト付き `/bin/sh -c <cmd>`。 | はい |

各ツールは `registry.MustRegister(builtin.NewXTool())` 経由で登録されます。エージェントコアに触れずに追加のツールを登録できます — [デベロッパーガイド: ツールの追加](/ja/developer-guide/add-a-tool/) を参照してください。

## `read`

ローカルファイルシステムから UTF-8 テキストファイルを読み取ります。

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

**セマンティクス:**

- `path` は絶対パスである必要があります。相対パスは拒否されます。
- 先頭 512 バイトに対する `\x00` スニフィングでバイナリコンテンツを拒否します。
- ファイル内容を文字列として逐語的に返します。

**エラー:** パス欠落、相対パス、読み取り不能ファイル、非テキストコンテンツ。

## `write`

UTF-8 テキストをファイルに書き込み、既存の内容を置き換えます。必要に応じて親ディレクトリを作成します。

**入力スキーマ:**

```json
{
  "type": "object",
  "properties": {
    "path":    { "type": "string", "description": "Absolute filesystem path to write." },
    "content": { "type": "string", "description": "The complete file contents to write." }
  },
  "required": ["path", "content"]
}
```

**セマンティクス:**

- ファイルを上書きします (追記ではありません)。増分変更には `edit` を使用してください。
- 親ディレクトリで `MkdirAll(dir, 0o755)`。
- パーミッション `0o644` でファイルを書き込みます。
- 成功時は `wrote <n> bytes to <path>` を返します。

**エラー:** パス欠落、相対パス、mkdir 失敗、書き込み失敗。

## `edit`

**ユニークマッチ制約** 付きの完全一致文字列の置換。Claude Code の Edit ツールから借用されています。

**入力スキーマ:**

```json
{
  "type": "object",
  "properties": {
    "path":       { "type": "string", "description": "Absolute filesystem path to the file to edit." },
    "old_string": { "type": "string", "description": "Exact text to find. Must be unique in the file." },
    "new_string": { "type": "string", "description": "Text to replace old_string with." }
  },
  "required": ["path", "old_string", "new_string"]
}
```

**セマンティクス:**

- `old_string` はファイル内に **正確に 1 回** 出現する必要があります。0 回 → エラー。2 回以上 → エラー (モデルにさらなる周辺コンテキストの提供を求めます)。
- `old_string == new_string` → エラー (no-op 編集は拒否されます)。
- インデントと空白を逐語的に保持します。
- 成功時は `edited <path> (1 replacement)` を返します。

ユニークマッチルールは意図的です: モデルが偶発的な一括置換を実行するのを防ぎます。モデルがすべての出現を変更したい場合は、それぞれ十分な周辺コンテキストで曖昧性をなくす複数の `edit` 呼び出しを作成する必要があります。

**エラー:** パス欠落 / 相対パス、`old_string` 欠落、マッチなし、ユニークでないマッチ、同一文字列、読み取り / 書き込み失敗。

## `grep`

ディレクトリ配下の正規表現検索。ripgrep より意図的にシンプル — 依存なし、in-process で実行されます。

**入力スキーマ:**

```json
{
  "type": "object",
  "properties": {
    "pattern":     { "type": "string",  "description": "Go RE2 regular expression to match." },
    "path":        { "type": "string",  "description": "Absolute directory to search under." },
    "include":     { "type": "string",  "description": "Optional filename glob (e.g. '*.go'). Applied to the base name." },
    "ignore_case": { "type": "boolean", "description": "Case-insensitive match. Defaults to false." }
  },
  "required": ["pattern", "path"]
}
```

**セマンティクス:**

- Go の [RE2](https://github.com/google/re2/wiki/Syntax) 構文 — バックリファレンスなし、ルックアラウンドなし。
- `path` を再帰的にウォークします。`.git`、`node_modules`、`vendor`、`.venv`、`__pycache__`、`dist`、`build` をスキップします。
- `MaxFileBytes` (デフォルト 4 MiB) より大きいファイルとバイナリコンテンツをスキップします。
- 出力を `MaxMatches` (デフォルト 200) で上限し、切り詰めはインラインで注釈されます。
- `<path>:<line>: <matching-line>` の行を返します。
- 何もマッチしない場合は `no matches` 文字列を返します。

**エラー:** パターン / パス欠落、相対パス、無効な正規表現、無効な include glob。

## `bash`

`/bin/sh -c` 経由でシェルコマンドを実行します。**ロードベアリングなセキュリティ境界。**

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

**セマンティクス:**

- `/bin/sh -c <command>` の下で実行されます。bash 固有ではありません — POSIX シェル。
- 結合された stdout+stderr が返されます。
- デフォルトタイムアウト: 60 秒。登録時に `NewBashTool(timeout)` 経由で設定可能。
- タイムアウトは、期限前に生成された任意の出力とともに `bash: timed out after <duration>` エラーを返します。
- 0 以外の終了は終了ステータスをラップした文字列を持つエラーを生成します。出力は依然としてモデルが検査できるように返されます。

**セーフティ:**

- ツールには組み込みの allowlist はありません。[承認者](/ja/user-guide/approval-policies/) がロードベアリングなゲートです。無人デーモンでは **常に** pattern モード承認を有効化してください。
- コマンドはデーモンの UID とファイルシステム可視性で実行されます。下に rootless コンテナを重ねてください ([デプロイ](/ja/deployment/))。

## ツールエラーとループ

ツールがエラーを返すと、エージェントはそれを `isError: true` の `tool_result` ブロックに変換し、次のイテレーションでモデルにフィードバックします:

```
[user] make the change
[assistant] tool_use: edit {"path": "/tmp/foo", "old_string": "x", "new_string": "y"}
[user]      tool_result: "edit: old_string not found in /tmp/foo" (isError=true)
[assistant] I couldn't find "x" in /tmp/foo. Could you confirm the path?
```

これは承認者の拒否に使われるのと同じチャネルです — [承認ポリシー](/ja/user-guide/approval-policies/) を参照してください。

## 追加のツールを登録する

```go
registry := tools.NewRegistry()
registry.MustRegister(builtin.NewReadTool())
registry.MustRegister(builtin.NewWriteTool())
registry.MustRegister(builtin.NewEditTool())
registry.MustRegister(builtin.NewGrepTool(0, 0))    // zero → defaults
registry.MustRegister(builtin.NewBashTool(60 * time.Second))
registry.MustRegister(myCustomTool)                  // any tools.Tool
```

`tools.Registry` は並行安全です。登録はスレッドセーフです。

## セキュリティ上の影響の一覧

| ツール | ブラスト半径 | 使わないべき場面 |
|---|---|---|
| `read` | デーモンの FS 可視性でファイルを読み取り。読み取り可能な任意のファイルを外に持ち出し得ます。 | ワークスペースのディスクに秘密素材がある場合。承認者の `match` 正規表現で制限してください。 |
| `grep` | read と同じ + 正規表現の CPU コスト。 | 信頼できないパターンをマッチする場合 — 病理的な正規表現では ReDoS が可能です。 |
| `edit` | ファイル内容を in-place で変更。 | デーモンの FS 可視性が意図されたワークスペースを超えて広がっている場合。コンテナのバインドマウントと組み合わせてください。 |
| `write` | ファイルを作成 / 上書き。 | edit と同じ、加えてデーモンが書き込める任意の場所にファイルを作成可能。 |
| `bash` | 任意コマンドの実行。 | pattern モード承認者のない任意の無人デーモン。**プライマリセキュリティ境界。** |

## トラブルシューティング

### `read: read /path: is a directory`

`read` ツールはファイル専用です。ディレクトリの内容が必要な場合は、パスパターン付きの `grep` または (`ls` 付きの) `bash` を使用してください。

### `edit: old_string not found`

モデルの提案する `old_string` がファイルの内容とバイト単位でマッチしませんでした。よくある原因: 空白 / 改行のドリフト、間違った行末スタイル、モデルの read と edit 呼び出しの間にファイルが編集された。

### `edit: old_string is not unique`

rousseau の `edit` ツールは曖昧な編集を拒否します — モデルは `old_string` がユニークなサブストリングになるように十分な周辺コンテキストを含める必要があります。これは偶発的なマルチサイト置換を防ぎます。

### `bash: timed out after 1m0s`

デフォルト 60 秒のタイムアウト。長時間実行コマンド (build、test) は失敗します。組み込み時に `NewBashTool(2*time.Minute)` でタイムアウトを引き上げるか、より速いステップに分割してください。

### `grep` が何も返さないが、パターンは確かにそこにある

rousseau の `grep` は Go の `regexp` パッケージ (RE2) を使用しており、これはすべての PCRE 機能をサポートしていません。バックリファレンスとルックアラウンドはサイレントに失敗します。RE2 用にパターンを書き直してください。

## 関連ページ

- [ユーザーガイド: 承認ポリシー](/ja/user-guide/approval-policies/) — すべてのツール呼び出しのゲート。
- [デベロッパーガイド: ツールの追加](/ja/developer-guide/add-a-tool/) — 独自のものを構築します。
- [コンセプト](/ja/concepts/) — ツールがエージェントループにどう収まるか。
- [エージェントループ](/ja/agent-loop/) — ツール結果が次のターンにどうフィードバックされるか。
- [リファレンス: ツールスキーマ](/ja/reference/tool-schemas/) — マシン可読なスキーマ。

## さらに読む

- `internal/tools/builtin/read.go` — 切り詰め付きファイル読み取り。
- `internal/tools/builtin/write.go` — ファイル書き込み。
- `internal/tools/builtin/edit.go` — ユニーク文字列制約の enforcer。
- `internal/tools/builtin/grep.go` — 再帰的な正規表現検索。
- `internal/tools/builtin/bash.go` — `/bin/sh -c` シェルラッパー。
