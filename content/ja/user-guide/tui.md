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
description: "Bubble Tea TUI keybindings, panels, spinner and streaming semantics for rousseau-agent's rousseau chat command."
keywords: "tui, bubble tea, keybindings, viewport, textarea, spinner, streaming, session"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/user-guide/tui/"
subtitle: "Bubble Tea keybindings, panels, streaming."
tags: "tui, bubble-tea, keybindings"
title: "TUI"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tui, bubble tea, keybindings, viewport, textarea, spinner, streaming, session"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "TUI"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/user-guide/tui/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/tui/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "TUI"
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
twitter_description: "Bubble Tea TUI keybindings, panels, spinner and streaming semantics for rousseau-agent's rousseau chat command."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "TUI"
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

## 概要

`rousseau chat` は 3 領域を持つ Bubble Tea TUI を開きます:

```
+------------------------------------------------------+
|                       Header                         |  session title
+------------------------------------------------------+
|                                                      |
|                                                      |
|                     Viewport                         |  scrollable history
|          (messages, streamed reply preview)          |
|                                                      |
|                                                      |
+------------------------------------------------------+
|                     Textarea                         |  input, Enter to send
+------------------------------------------------------+
| status: idle | spinner | streaming | error           |
+------------------------------------------------------+
```

Bubble Tea の alt-screen モードで実行されます — TUI はターミナルバッファを乗っ取り、終了時に復元します。

## キーバインド

rousseau の TUI はバインドセットを小さく保ちます。迷ったら、標準の Bubble Tea viewport / textarea のショートカットが適用されます。

### グローバル

| キー | アクション |
|---|---|
| `Ctrl+C` | 終了。現在のセッションを保存し、終了時に何も印刷しません。 |
| `Esc` | 終了。`Ctrl+C` と同じ。 |
| `Enter` | 現在の textarea の内容を送信します。エージェントがビジー中は no-op。 |

### Textarea (入力)

標準の Bubble Tea textarea 挙動:

| キー | アクション |
|---|---|
| 任意の印字可能文字 | カーソル位置に挿入。 |
| `Backspace` | カーソル前の文字を削除。 |
| `Delete` | カーソル下の文字を削除。 |
| 矢印キー | カーソル移動。 |
| `Home` / `End` | 行頭 / 行末へジャンプ。 |
| `Ctrl+A` / `Ctrl+E` | 行頭 / 行末へジャンプ (Emacs バインド)。 |
| `Ctrl+U` | 行頭までキル。 |
| `Ctrl+K` | 行末までキル。 |
| `Shift+Enter` | (ターミナル依存) 送信せずに改行。しばしばリテラル `\n` にマップされます。 |

textarea はコンテンツがラップされるにつれて垂直方向に成長します。viewport は適応するために縮小します。

### Viewport (履歴)

viewport は通常の Bubble Tea viewport ショートカットをサポートします。textarea が空の場合はフォーカスが viewport にあります。タイピングは自動的に textarea にルーティングされます。

| キー | アクション |
|---|---|
| `PgUp` / `PgDn` | 1 ページスクロール。 |
| `↑` / `↓` | 1 行スクロール。 |
| `Home` / `End` | 先頭 / 末尾へジャンプ。 |
| マウスホイール | スクロール。 |

## パネルセマンティクス

### ヘッダー

`rousseau · <session title>`。タイトルはセッション作成時の `--title` から来ます (デフォルト: `chat YYYY-MM-DD HH:MM`)。

### Viewport

レンダリングされた履歴、加えて、ターン進行中には下部に **ストリーミングプレビュー**。プレビューはプロバイダーがストリームするにつれてデルタを反映します。ターンが終了すると、プレビューは最終アシスタントメッセージで置き換えられます。

すべてのメッセージにはその役割 (`you`、`rousseau`、`tool`) が先頭に付くため、モデルがツール呼び出しを要求するとフローが明白になります。

### Textarea

プレースホルダーテキスト: `Ask, or press Ctrl+C to quit…`。Enter で送信。textarea は送信時にリセットされます。

エージェントがビジー中は、`Enter` は no-op になり、偶発的な二重送信でターンがスタックしないようにします。

### ステータスライン

textarea の下。コンテンツは変わります:

| 状態 | ライン |
|---|---|
| アイドル | 空。 |
| ビジー | スピナー + `thinking…`。スピナーティックは `bubbles/spinner` から来ます。 |
| ストリーミング | スピナーは続きます。ストリーミングデルタは viewport プレビューに表示されます。 |
| エラー | 赤色のエラー文字列。次の成功ターンでクリアされます。 |

## セッション永続化

すべてのターンは `state.Store.Save` 経由で `~/.local/share/rousseau/sessions.db` に永続化されます。デーモンがターンの途中でクラッシュした場合:

- ユーザーターンは既に保存されています (`doTurn` が発火する前に追記されました)。
- アシスタントの返信はターンが完了したときにのみ保存されます。

再起動時、`rousseau chat --session <id>` は最後に成功して保存された状態から再開します。

## CLI からのセッションコマンド

TUI はすべてのセッション操作を表面化しません。シェルからセッションを管理してください:

```sh
rousseau session list
rousseau session show <id>
rousseau session search "kubectl"
rousseau session delete <id>
```

## ストリーミングセマンティクス

`StreamingProvider.ChatStream` を実装するプロバイダー (Anthropic、`claudecli`) はデルタを viewport プレビューにストリームします。`Provider.Chat` のみを実装するプロバイダー (Bedrock、Vertex、シム次第で OpenAI 互換) は、ターン完了時に単一ブロックとして返信を配信します — プレビューは空のままで、`busy` が `false` になったときに返信が現れます。

## うまくいかないとき

- **TUI がハングする** — `Ctrl+C` を 2 回。最初の `Ctrl+C` は `tea.Quit` をシグナルし、状態をフラッシュします。2 回目は OS に捕捉されます。
- **viewport が空で、textarea が入力を受け付けない** — alt-screen がエスケープシーケンスを発するサブプロセス (例: ANSI コードを印刷するツール呼び出し) によって破損している可能性があります。TUI を再起動してください。
- **ステータスラインが `thinking…` のままになる** — プロバイダーが返っていません。デーモンの stderr を確認してください (rousseau は slog を stderr に書きます。パイプで流してしまった場合は表面化してください)。

## 次に

- [ユーザーガイド: CLI](/ja/user-guide/cli/) — TUI 外のすべてのコマンド。
- [コンセプト](/ja/concepts/) — その下のエージェントループ。
- [圧縮 + 再呼び出し](/ja/user-guide/compression-recall/) — 長いチャットが使い続けられる方法。
