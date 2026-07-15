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
description: "Full CLI reference for rousseau-agent: every command, every flag, exit codes, per-transport subcommands."
keywords: "cli, cobra, commands, flags, subcommands, exit codes"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/user-guide/cli/"
subtitle: "Every command, every flag."
tags: "cli, reference, commands"
title: "CLI リファレンス"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cli, cobra, commands, flags, subcommands, exit codes"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "CLI リファレンス"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 40
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/user-guide/cli/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/cli/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "CLI リファレンス"
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
twitter_description: "Full CLI reference for rousseau-agent: every command, every flag, exit codes, per-transport subcommands."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "CLI リファレンス"
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

## 起動

```
rousseau [--config <path>] <command> [flags]
```

すべてのコマンドは `~/.config/rousseau/config.yaml` (または `--config` 経由で渡されたファイル) からデフォルトを読み込みます。フラグは環境変数を上書きし、環境変数はファイルを上書きし、ファイルはハードコードされたデフォルトを上書きします。

## グローバルフラグ

| フラグ | 型 | デフォルト | 備考 |
|---|---|---|---|
| `--config` | string | `$XDG_CONFIG_HOME/rousseau/config.yaml` | このファイルから設定をロードします。指定なしはデフォルトの XDG パスを意味します。 |
| `--help`, `-h` | bool | — | 現在のコマンドのヘルプを印刷します。 |

## コマンドツリー

```
rousseau
├── chat                Bubble Tea TUI
├── whatsapp            WhatsApp bridge (whatsmeow)
├── signal              Signal bridge (signal-cli JSON-RPC)
├── telegram            Telegram Bot API long-polling
├── matrix              Matrix client-server API
├── slack               Slack Socket Mode
├── discord             Discord Gateway
├── sms                 SMS send-only (Twilio / Vonage)
├── imessage            BlueBubbles-backed iMessage bridge
├── email               IMAP inbound + SMTP outbound
├── mcp                 MCP JSON-RPC 2.0 server over stdio
├── cron                Manage scheduled prompts
├── session             Inspect / delete session store
├── skills              List / show / lint skills
├── doctor              Diagnose the local installation
├── status              Print daemon status
├── init                Write a default config to ~/.config/rousseau/
└── version             Print version, commit, build date
```

## `rousseau chat`

対話的な Bubble Tea TUI を開きます。

| フラグ | 型 | デフォルト | 備考 |
|---|---|---|---|
| `--session` | string | — | ID で既存のセッションを再開します。 |
| `--title` | string | タイムスタンプ | 新規セッションのタイトル。 |

## `rousseau whatsapp`

WhatsApp ブリッジを実行します。初回起動時に QR コードを印刷します。

| フラグ | 型 | デフォルト | 備考 |
|---|---|---|---|
| `--store` | string | `$XDG_DATA_HOME/rousseau/whatsapp.db` | whatsmeow デバイスストアへのパス。 |
| `--allow` | []string | なし | インバウンドの処理をこれらの JID に制限します。繰り返し可能。**公開番号では絶対に空のままにしないでください。** |

## `rousseau signal`

Signal ブリッジを実行します。`signal-cli jsonRpc` をサブプロセスとして生成します。

| フラグ | 型 | デフォルト | 備考 |
|---|---|---|---|
| `--account` | string | `signal.account` から | デーモンが実行される E.164 電話番号。 |
| `--binary` | string | `signal-cli` | signal-cli 実行ファイルへのパス。 |
| `--allow` | []string | なし | インバウンドをこれらの E.164 番号に制限します。 |

## `rousseau telegram`

Telegram Bot API ロングポーラーを実行します。

| フラグ | 型 | デフォルト | 備考 |
|---|---|---|---|
| `--token` | string | `telegram.token` から | BotFather トークン。 |
| `--allow` | []string | なし | インバウンドをこれらのチャット ID に制限します。 |

## `rousseau matrix`

Matrix ブリッジを実行します。

| フラグ | 型 | デフォルト | 備考 |
|---|---|---|---|
| `--homeserver-url` | string | config から | 例: `https://matrix.org`。 |
| `--access-token` | string | config から | Bot のアクセストークン。 |
| `--user-id` | string | config から | Bot の Matrix ユーザー ID (`@bot:matrix.org`)。 |
| `--allow` | []string | なし | インバウンドをこれらのユーザー ID に制限します。 |

## `rousseau slack`

Slack Socket Mode ブリッジを実行します。

| フラグ | 型 | デフォルト | 備考 |
|---|---|---|---|
| `--app-token` | string | config から | `xapp-...` Socket Mode トークン。 |
| `--bot-token` | string | config から | `xoxb-...` Bot User OAuth トークン。 |
| `--allow` | []string | なし | インバウンドをこれらの Slack ユーザー ID に制限します。 |

## `rousseau discord`

Discord Gateway ブリッジを実行します。

| フラグ | 型 | デフォルト | 備考 |
|---|---|---|---|
| `--token` | string | config から | Bot トークン。 |
| `--allow` | []string | なし | インバウンドをこれらの Discord ユーザー ID に制限します。 |

## `rousseau sms`

Twilio または Vonage 経由の送信専用 SMS。インバウンドなし。

| フラグ | 型 | デフォルト | 備考 |
|---|---|---|---|
| `--provider` | string | config から | `twilio` または `vonage`。 |
| `--from` | string | config から | E.164 送信者番号。 |
| `--account-sid` | string | config から | Twilio Account SID。 |
| `--auth-token` | string | config から | Twilio auth トークンまたは Vonage シークレット。 |
| `--api-key` | string | config から | Vonage API キー。 |

## `rousseau imessage`

BlueBubbles ベースの iMessage ブリッジ。

| フラグ | 型 | デフォルト | 備考 |
|---|---|---|---|
| `--base-url` | string | `http://localhost:1234` | BlueBubbles サーバー URL。 |
| `--password` | string | config から | BlueBubbles サーバーパスワード。 |
| `--chat-guid` | string | config から | 送信ターゲット。 |
| `--poll-interval` | duration | 5s | 新しいメッセージのポーリング頻度。 |
| `--allow` | []string | なし | インバウンドを制限します。 |

## `rousseau email`

IMAP + SMTP 経由のメールブリッジ。

| フラグ | 型 | デフォルト | 備考 |
|---|---|---|---|
| `--imap-addr` | string | config から | 例: `imap.example.com:993`。 |
| `--imap-username`, `--imap-password` | string | config から | IMAP 資格情報。 |
| `--smtp-addr` | string | config から | 例: `smtp.example.com:587`。 |
| `--smtp-username`, `--smtp-password` | string | config から | SMTP 資格情報。 |
| `--from` | string | config から | エンベロープ送信者。 |
| `--poll-interval` | duration | 30s | IMAP ポーリング頻度。 |
| `--allow` | []string | なし | インバウンド送信者アドレスを制限します。 |

## `rousseau mcp`

stdio 上で MCP サーバーを起動します。フラグなし — すべてのノブは `config.yaml` にあります。

## `rousseau cron`

| サブコマンド | 説明 |
|---|---|
| `cron add` | スケジュールされたプロンプトを追加します。フラグ: `--name`、`--schedule` (5 フィールド cron)、`--prompt`、`--deliver-to`。 |
| `cron list` | すべてのジョブを `on/off` ステータスと最終実行タイムスタンプで一覧表示します。 |
| `cron remove <name-or-id>` | ジョブを削除します。 |
| `cron enable <name-or-id>` | 無効化されたジョブを有効化します。 |
| `cron disable <name-or-id>` | 有効化されたジョブを (削除せずに) 無効化します。 |

## `rousseau session`

| サブコマンド | 説明 |
|---|---|
| `session list` | ストア内のセッションを新しい順に一覧表示します。 |
| `session search <query>` | すべてのセッションのメッセージコンテンツにわたる FTS5 検索。 |
| `session show <id>` | セッションのメッセージ履歴を印刷します。 |
| `session delete <id>` | セッションを削除します。 |

## `rousseau skills`

| サブコマンド | 説明 |
|---|---|
| `skills list` | `skills_dir` から発見されたスキルを一覧表示します。 |
| `skills show <name>` | スキルの YAML フロントマターと本文を印刷します。 |
| `skills lint` | スキルをスキーマ準拠のために検証します。 |

## `rousseau doctor`

すべての実行時依存関係と設定選択をウォークします。`ok`、`warn`、`fail`、`info` のタグが付いた行のステータスレポートを印刷します。いずれかの行が `fail` の場合は終了コード 1。

現在フラグはありません。グローバルレベルの `--config` 経由で拡張します。

## `rousseau status`

コンパクトなデーモンステータスサマリー — プロバイダー、セッション数、cron ジョブ — を印刷します。読み取り専用。

## `rousseau init`

デフォルトの `config.yaml` を `~/.config/rousseau/` に書き込みます。`--force` が渡されない限り、既存ファイルの上書きは拒否します。

| フラグ | 型 | デフォルト | 備考 |
|---|---|---|---|
| `--force` | bool | false | 既存の config を上書きします。 |

## `rousseau version`

バージョン、コミットハッシュ、ビルド日を印刷します。ビルド時に `-ldflags` 経由で刻印されます。

## 終了コード

| コード | 意味 |
|---|---|
| 0 | コマンドが正常に完了しました。 |
| 1 | コマンドが失敗しました。エラーは stderr に印刷されます。 |

デーモンシグナルセマンティクスについては [リファレンス: 終了コード](/ja/reference/exit-codes/) を参照してください。

## 環境変数

すべての config フィールドは、`ROUSSEAU_` プレフィックスと `_` をセクションセパレータとして使用する環境変数で上書きできます: `ROUSSEAU_LOG_LEVEL=debug`、`ROUSSEAU_ANTHROPIC_API_KEY=sk-ant-...` など。

特別なケースは `ANTHROPIC_API_KEY` (プレフィックスなし) です — 慣習に合わせるために config ローダーが直接拾います。

## トラブルシューティング

### サブコマンドを渡すときに `unknown command`

rousseau のサブコマンドは `internal/cli/root.go` で宣言されています。`rousseau <cmd>` が unknown を報告する場合、フラグの綴りが間違っているか、古いバイナリを使用しています。`rousseau version` で持っているものが分かります。

### 繰り返し可能なフラグには複数の呼び出しが必要

`--allow` はフラグごとに 1 つの JID を受け入れます。複数の値にはフラグを繰り返してください: `--allow A --allow B`、`--allow A,B` ではありません。

### 環境変数がサイレントに無視される

rousseau は `ROUSSEAU_` プレフィックス + アンダースコアセクションセパレータを使用します: `anthropic.model` は `ROUSSEAU_ANTHROPIC_MODEL` になります。大文字と小文字を区別します。

### `rousseau chat` が空白画面のみを表示する

Bubble Tea TUI は ANSI 対応ターミナルが必要です。`TERM=xterm-256color` を設定し、対話的に実行してください (`nohup` やパイプの下ではなく)。

### コマンドがすぐに 0 で終了する

一部のフラグ (`--help`、`--version` 系) は短絡します。コマンドが実行されない場合は、渡したフラグを確認してください。

## 関連ページ

- [ユーザーガイド: TUI](/ja/user-guide/tui/) — `rousseau chat` 内のキーバインド。
- [ユーザーガイド: ツール](/ja/user-guide/tools/) — すべての組み込みツールの JSON スキーマ。
- [リファレンス: CLI コマンド](/ja/reference/cli-commands/) — コマンドテーブル。
- [リファレンス: 環境変数](/ja/reference/environment-variables/) — 上書きマトリックス。
- [設定](/ja/configuration/) — すべてのコマンドを支える config ファイル。

## さらに読む

- `internal/cli/root.go` — Cobra ツリー。
- `internal/cli/chat.go`、`internal/cli/whatsapp.go`、`internal/cli/slack.go`、… — サブコマンドごとに 1 ファイル。
- `internal/config/config.go` — 環境変数 / フラグ解決。
