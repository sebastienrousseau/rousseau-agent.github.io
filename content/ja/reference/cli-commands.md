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
description: "Compact reference table of every rousseau-agent command mirroring the output of rousseau --help."
keywords: "cli, commands, reference, table, rousseau --help"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/reference/cli-commands/"
subtitle: "Every command tabulated."
tags: "reference, cli, commands"
title: "CLI コマンド"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cli, commands, reference, table, rousseau --help"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "CLI コマンド"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 50
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/reference/cli-commands/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/cli-commands/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "CLI コマンド"
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
twitter_description: "Compact reference table of every rousseau-agent command mirroring the output of rousseau --help."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "CLI コマンド"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">学べること</span><p>完全な <code>rousseau</code> CLI 表面: すべてのコマンド、そのフラグ、終了コードセマンティクス、各フラグが上書きする config キー。これはスキャン可能なリファレンスです — 作業例付きのウォークスルーについては <a href="/ja/user-guide/cli/">ユーザーガイド: CLI</a> を参照してください。</p></aside>

## コマンドツリー

すべてのコマンドは `rousseau <cmd> --help` 経由でヘルプを表面化します。このページはその一覧表化されたサマリーです。

| コマンド | 説明 |
|---|---|
| `chat` | 対話的な Bubble Tea TUI を開きます。 |
| `whatsapp` | WhatsApp ブリッジ (whatsmeow) を実行します。 |
| `signal` | Signal ブリッジ (signal-cli JSON-RPC) を実行します。 |
| `telegram` | Telegram Bot API ロングポーラーを実行します。 |
| `matrix` | Matrix クライアントサーバーブリッジを実行します。 |
| `slack` | Slack Socket Mode ブリッジを実行します。 |
| `discord` | Discord Gateway ブリッジを実行します。 |
| `sms` | Twilio または Vonage 経由の送信専用 SMS。 |
| `imessage` | BlueBubbles ベースの iMessage ブリッジ。 |
| `email` | IMAP インバウンド + SMTP アウトバウンドブリッジ。 |
| `mcp` | stdio 上で MCP JSON-RPC 2.0 サーバーを起動します。 |
| `cron add` | スケジュールされたプロンプトを追加します。 |
| `cron list` | すべてのスケジュールされたジョブを一覧表示します。 |
| `cron remove` | スケジュールされたジョブを削除します。 |
| `cron enable` | 無効化されたスケジュールジョブを有効化します。 |
| `cron disable` | 有効化されたスケジュールジョブを無効化します。 |
| `session list` | ストア内のセッションを新しい順に一覧表示します。 |
| `session search` | すべてのセッションのメッセージコンテンツにわたる FTS5 検索。 |
| `session show` | セッションのメッセージ履歴を出力します。 |
| `session delete` | セッションを削除します。 |
| `skills list` | `skills_dir` から発見されたスキルを一覧表示します。 |
| `skills show` | スキルの YAML フロントマターと本文を出力します。 |
| `skills lint` | スキルをスキーマ準拠のために検証します。 |
| `doctor` | ローカルインストールを診断します。レポートを出力します。 |
| `status` | デーモンステータスを出力します。 |
| `init` | デフォルト config を `~/.config/rousseau/` に書き込みます。 |
| `version` | バージョン、コミット、ビルド日を出力します。 |

## グローバルフラグ

すべてのコマンドがこれらを受け入れます:

| フラグ | 型 | config キー | 備考 |
|---|---|---|---|
| `--config` | string | — | このファイルから設定をロードします。デフォルト: `$XDG_CONFIG_HOME/rousseau/config.yaml`。 |
| `--help`, `-h` | bool | — | 現在のコマンドのヘルプを出力します。 |

## トランスポートごとのフラグ

### `rousseau whatsapp`

| フラグ | 型 | config キー | 備考 |
|---|---|---|---|
| `--store` | string | — | whatsmeow デバイスストアへのパス。デフォルト `$XDG_DATA_HOME/rousseau/whatsapp.db`。 |
| `--allow` | []string | `whatsapp.allowlist` | インバウンドをこれらの JID に制限します。繰り返し可能。 |

### `rousseau slack`

| フラグ | 型 | config キー |
|---|---|---|
| `--app-token` | string | `slack.app_token` |
| `--bot-token` | string | `slack.bot_token` |
| `--bot-user-id` | string | `slack.bot_user_id` |
| `--allow` | []string | `slack.allowlist` |

### `rousseau discord`

| フラグ | 型 | config キー |
|---|---|---|
| `--token` | string | `discord.token` |
| `--allow` | []string | `discord.allowlist` |

### `rousseau telegram`

| フラグ | 型 | config キー |
|---|---|---|
| `--token` | string | `telegram.token` |
| `--allow` | []string | `telegram.allowlist` |

### `rousseau matrix`

| フラグ | 型 | config キー |
|---|---|---|
| `--homeserver-url` | string | `matrix.homeserver_url` |
| `--access-token` | string | `matrix.access_token` |
| `--user-id` | string | `matrix.user_id` |
| `--allow` | []string | `matrix.allowlist` |

### `rousseau signal`

| フラグ | 型 | config キー |
|---|---|---|
| `--account` | string | `signal.account` |
| `--binary` | string | `signal.binary` |
| `--allow` | []string | `signal.allowlist` |

### `rousseau email`

| フラグ | 型 | config キー |
|---|---|---|
| `--imap-addr` | string | `email.imap_addr` |
| `--imap-username` | string | `email.imap_username` |
| `--imap-password` | string | `email.imap_password` |
| `--smtp-addr` | string | `email.smtp_addr` |
| `--smtp-username` | string | `email.smtp_username` |
| `--smtp-password` | string | `email.smtp_password` |
| `--from` | string | `email.from` |
| `--mailbox` | string | `email.mailbox` |
| `--poll-interval` | string | `email.poll_interval` |

### `rousseau sms`

| フラグ | 型 | config キー |
|---|---|---|
| `--provider` | string | `sms.provider` |
| `--from` | string | `sms.from` |
| `--to` | string | (位置引数) |

### `rousseau imessage`

| フラグ | 型 | config キー |
|---|---|---|
| `--base-url` | string | `imessage.base_url` |
| `--password` | string | `imessage.password` |
| `--chat-guid` | string | `imessage.chat_guid` |

## 終了コード

| コード | 意味 |
|---|---|
| 0 | クリーン終了 — コマンドが完了。長時間実行デーモンには典型的ではありません (通常はシグナルで終了)。 |
| 1 | `Execute` から表面化した任意のエラー。分類については [リファレンス: 終了コード](/ja/reference/exit-codes/) を参照してください。 |

## 優先順位

config 値は **フラグ &gt; 環境変数 &gt; ファイル &gt; デフォルト** の順で解決されます (`internal/config/config.go` の `config.Load` を参照)。環境変数はドットをアンダースコアに置き換えた `ROUSSEAU_` プレフィックス付きです — 例: `ROUSSEAU_ANTHROPIC_MODEL` は `anthropic.model` を上書きします。ベアな `ANTHROPIC_API_KEY` 環境変数も尊重されます (`config.Load` で特別ケース)。

## トラブルシューティング

### `rousseau chat` で `unknown flag: --allow`

`--allow` はトランスポートスコープです。`chat` にはイングレスがないため allowlist はありません。代わりに `rousseau whatsapp --allow …` を使用してください。

### 繰り返し可能なフラグではフラグ順序が重要

`--allow A --allow B` は 2 値ですが、`--allow=A,B` はたまたまカンマを含む 1 値です。別々のフラグを推奨します。

### 環境変数の上書きが取得されない

rousseau は起動時のみ環境変数を読み取ります。環境変数を変更した後にデーモンを再起動するか、`--config` を使用して再ロードを強制してください。

### `flag provided but not defined`

Cobra は未知のフラグを拒否します。新しいバージョンからフラグをコピーする場合、現在のスペルについて `rousseau <cmd> --help` を確認してください。

## 関連ページ

- [ユーザーガイド: CLI](/ja/user-guide/cli/) — 作業例付きのすべてのコマンド。
- [リファレンス: 終了コード](/ja/reference/exit-codes/) — シグナルセマンティクス。
- [リファレンス: config スキーマ](/ja/reference/config-schema/) — すべての設定フィールド。
- [リファレンス: 環境変数](/ja/reference/environment-variables/) — 環境変数上書きマトリックス。
- [設定](/ja/configuration/) — 完全な config ファイルウォークスルー。

## さらに読む

- `internal/cli/root.go` — Cobra コマンドツリー。
- `internal/cli/*.go` — サブコマンドごとに 1 ファイル。
- `internal/config/config.go` — `Load` とデフォルト解決。
