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
changefreq: "weekly"
description: "Complete configuration reference for rousseau-agent. Every provider, transport, and agent knob with type, default, and effect."
keywords: "configuration, config.yaml, viper, precedence, YAML, provider, transport, approver, compression"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/configuration/"
subtitle: "internal/config/config.go のすべてのフィールド。"
tags: "configuration, reference"
title: "設定リファレンス"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "configuration, config.yaml, viper, precedence, YAML, provider, transport, approver, compression"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "設定リファレンス"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 4
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/configuration/index.html"
item_link: "https://docs.rousseau-agent.dev/configuration/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "設定リファレンス"
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
twitter_description: "Complete configuration reference for rousseau-agent. Every provider, transport, and agent knob with type, default, and effect."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "設定リファレンス"
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

## 優先順位

`rousseau` は設定を **フラグ > 環境変数 > ファイル > デフォルト** の順で解決します。ファイルはデフォルトで `~/.config/rousseau/config.yaml` にあり、`--config` で上書き可能です。

環境変数はプレフィックス `ROUSSEAU_` を用い、`.` は `_` に置き換わります。つまり `provider` は `ROUSSEAU_PROVIDER`、`anthropic.api_key` は `ROUSSEAU_ANTHROPIC_API_KEY` になります。`ANTHROPIC_API_KEY` も直接尊重されます（ロード時に `anthropic.api_key` にバインドされます）。

## トップレベル

| フィールド | 型 | デフォルト | 効果 |
|---|---|---|---|
| `provider` | string | `claudecli` | LLM バックエンド: `claudecli`、`anthropic`、`bedrock`、`vertex`、`openai`、`openrouter`、`ollama`。 |

## `anthropic` — Anthropic API 直接

| フィールド | 型 | デフォルト | 効果 |
|---|---|---|---|
| `api_key` | string | *`ANTHROPIC_API_KEY` から* | `api.anthropic.com` の Bearer。プロバイダが選択されているのに空だと拒否されます。 |
| `model` | string | `claude-sonnet-4-6` | SDK に渡されるモデル識別子。 |
| `max_tokens` | int64 | `4096` | 補完 1 回あたりの出力トークン上限。 |

[/providers/anthropic/](/ja/providers/anthropic/) を参照してください。

## `bedrock` — AWS Bedrock

| フィールド | 型 | デフォルト | 効果 |
|---|---|---|---|
| `region` | string | *必須* | AWS リージョン（`us-east-1`、`eu-west-2`）。 |
| `model` | string | *必須* | Bedrock モデル ID（`anthropic.claude-sonnet-4-6-20260101-v1:0`）。 |
| `profile` | string | *空* | `~/.aws/credentials` の認証情報プロファイル。空の場合は標準の AWS 認証情報チェーンにフォールスルーします。 |
| `max_tokens` | int64 | SDK デフォルト | 出力トークン上限。 |

[/providers/bedrock/](/ja/providers/bedrock/) を参照してください。

## `vertex` — Google Vertex AI

| フィールド | 型 | デフォルト | 効果 |
|---|---|---|---|
| `project` | string | *必須* | GCP プロジェクト ID。 |
| `region` | string | *必須* | Vertex リージョン（`us-central1`）。 |
| `model` | string | *必須* | Anthropic-on-Vertex モデル ID（`claude-sonnet-4-6@20260101`）。 |
| `credentials_file` | string | *空* | サービスアカウントまたは authorized-user JSON へのパス。空の場合は Application Default Credentials を使用します。 |
| `max_tokens` | int64 | `4096` | 出力トークン上限。 |

[/providers/vertex/](/ja/providers/vertex/) を参照してください。

## `claudecli` — ローカル `claude` CLI のサブプロセス

| フィールド | 型 | デフォルト | 効果 |
|---|---|---|---|
| `binary` | string | `claude` | 実行ファイル。`$PATH` から解決されます。 |
| `model` | string | *空* | `--model` に渡されます。空の場合は claude のデフォルトを使用。 |
| `permission_mode` | string | *空* | `--permission-mode` に渡されます。値: `acceptEdits`、`auto`、`bypassPermissions`、`default`、`dontAsk`、`plan`。無人稼働のデーモンは通常 `bypassPermissions` が必要です。 |
| `extra_args` | []string | `[]` | 起動のたびに `-p` の前に追加されます。`--add-dir`、`--allowed-tools`、`--disallowed-tools`、`--plugin-dir` に有用です。 |

[/providers/claudecli/](/ja/providers/claudecli/) を参照してください。

## `openai` / `openrouter` / `ollama` — OpenAI 互換エンドポイント

共通の形状です。`openrouter.base_url` のデフォルトは `https://openrouter.ai/api/v1`、`ollama.base_url` は `http://localhost:11434/v1`、`ollama.api_key` は `not-required` です。

| フィールド | 型 | デフォルト | 効果 |
|---|---|---|---|
| `api_key` | string | *必須* | Bearer トークン。Ollama でも空にはできません（任意のプレースホルダで可）。 |
| `model` | string | *必須* | モデル識別子。エンドポイント横断の共通デフォルトはありません。 |
| `base_url` | string | *プロバイダデフォルト* | 完全なエンドポイント URL。 |
| `max_tokens` | int64 | SDK デフォルト | 出力トークン上限。 |

[/providers/openai-compatible/](/ja/providers/openai-compatible/) を参照してください。

## `log`

| フィールド | 型 | デフォルト | 効果 |
|---|---|---|---|
| `level` | string | `info` | `debug`、`info`、`warn`、`error`。 |
| `format` | string | `text` | `text`（人間向け）または `json`（本番 / ログ集約）。 |

## `state`

| フィールド | 型 | デフォルト | 効果 |
|---|---|---|---|
| `path` | string | `~/.local/share/rousseau/sessions.db` | SQLite データベースパス（WAL モード、`busy_timeout=15s`）。 |

## `agent`

| フィールド | 型 | デフォルト | 効果 |
|---|---|---|---|
| `system_prompt` | string | *空* | 組み込みデフォルトを上書きします。 |
| `max_iterations` | int | `32` | `Turn` あたりのモデルラウンドトリップ上限。 |
| `skills_dir` | string | *空* | `*.md` スキルファイルのディレクトリ。空の場合はスキルを無効化します。 |

### `agent.compression`

| フィールド | 型 | デフォルト | 効果 |
|---|---|---|---|
| `enabled` | bool | `false` | LLM ベースのセッション圧縮を有効化します。 |
| `trigger_messages` | int | `60` | この件数を超えると圧縮が発火します。 |
| `keep_recent` | int | `8` | そのまま保持される最近のメッセージ数。 |
| `prompt` | string | *組み込み* | デフォルトの要約指示を上書きします。 |

### `agent.approver`

| フィールド | 型 | デフォルト | 効果 |
|---|---|---|---|
| `mode` | string | `allow_all` | `allow_all`、`deny_all`、または `pattern`。 |
| `reason` | string | *空* | モデルに提示される拒否理由。 |
| `default` | string | `deny` | `allow` や `deny` ルールがマッチしなかった場合のフォールバック（pattern モード時）。 |
| `allow` | []PatternEntry | `[]` | ツールごとの正規表現 allow ルール。 |
| `deny` | []PatternEntry | `[]` | ツールごとの正規表現 deny ルール。deny は allow に勝ります。 |

各 `PatternEntry` は `{tool: <name>, match: <regex>}` です。`tool: ""` はすべてのツールにマッチし、`match: ""` はすべての入力にマッチします。

## トランスポートブロック

### `whatsapp`

| フィールド | 型 | デフォルト | 効果 |
|---|---|---|---|
| `reply_header` | string | `💎 *Rousseau Agent*\n\n` | 送信するすべてのメッセージの先頭に付加されます。`" "` にすると無効化できます。 |
| `voice.enabled` | bool | `false` | 受信ボイスノートの Whisper ベース文字起こし。 |
| `voice.binary` | string | `whisper` | Whisper CLI 実行ファイル。 |
| `voice.model` | string | *空* | `--model` に渡されます（`base.en`、`small`）。 |
| `voice.model_path` | string | *空* | 明示的な `.bin` パス。`model` より優先されます。 |
| `voice.language` | string | *空* | `--language` に渡されます。空の場合は自動検出。 |
| `voice.extra_args` | []string | `[]` | 各 whisper 呼び出しに追加されます。 |

### `signal`

| フィールド | 型 | デフォルト | 効果 |
|---|---|---|---|
| `binary` | string | `signal-cli` | JSON-RPC デーモンモードで呼び出す実行ファイル。 |
| `account` | string | *必須* | デーモンが動作する E.164 電話番号。 |
| `extra_args` | []string | `[]` | `-a <account>` と `jsonRpc` の間に挿入されます。 |
| `reply_header` | string | *空* | 送信メッセージの先頭に付加されます。 |
| `allowlist` | []string | `[]` | 処理対象の E.164 番号リスト。空の場合はすべての送信者を受け入れます。 |

### `telegram`

| フィールド | 型 | デフォルト | 効果 |
|---|---|---|---|
| `token` | string | *必須* | BotFather のボットトークン。 |
| `base_url` | string | `https://api.telegram.org` | ローカル Bot API サーバー用の上書き。 |
| `reply_header` | string | *空* | 送信返信の先頭に付加されます。 |
| `allowlist` | []string | `[]` | 処理対象の Telegram ユーザー ID リスト。 |

### `matrix`

| フィールド | 型 | デフォルト | 効果 |
|---|---|---|---|
| `homeserver_url` | string | *必須* | ベース URL（例: `https://matrix.org`）。 |
| `access_token` | string | *必須* | ボットユーザーのアクセストークン。 |
| `user_id` | string | *空* | ボットユーザーの完全な MXID（`@bot:matrix.org`）。オプションだが推奨（自メッセージのエコー抑止に使用）。 |
| `reply_header` | string | *空* | 送信返信の先頭に付加されます。 |
| `allowlist` | []string | `[]` | 処理対象の Matrix ID リスト。 |

### `slack`

| フィールド | 型 | デフォルト | 効果 |
|---|---|---|---|
| `app_token` | string | *必須* | `connections:write` を持つ `xapp-*` アプリレベルトークン。 |
| `bot_token` | string | *必須* | `chat:write` を持つ `xoxb-*` ボットトークン。 |
| `bot_user_id` | string | *空* | 自メッセージループ防止用のボット自身の `U…` ID。 |
| `reply_header` | string | *空* | 送信メッセージの先頭に付加されます。 |
| `allowlist` | []string | `[]` | 処理対象の Slack ユーザー ID リスト。 |

### `discord`

| フィールド | 型 | デフォルト | 効果 |
|---|---|---|---|
| `token` | string | *必須* | Developer Portal のボットトークン。 |
| `reply_header` | string | *空* | 送信返信の先頭に付加されます。 |
| `allowlist` | []string | `[]` | 処理対象の Discord ユーザー ID リスト。 |

### `sms`

| フィールド | 型 | デフォルト | 効果 |
|---|---|---|---|
| `provider` | string | *必須* | `twilio` または `vonage`。 |
| `from` | string | *必須* | E.164 送信元、または Twilio Messaging Service SID。 |
| `account_sid` | string | *twilio では必須* | Twilio アカウント SID（`AC…`）。 |
| `auth_token` | string | *必須* | Twilio 認証トークンまたは Vonage API シークレット。 |
| `api_key` | string | *vonage では必須* | Vonage API キー。 |
| `base_url` | string | *プロバイダデフォルト* | 地域・テスト用エンドポイントの上書き。 |
| `reply_header` | string | *空* | 送信メッセージの先頭に付加されます。 |

### `imessage`

| フィールド | 型 | デフォルト | 効果 |
|---|---|---|---|
| `base_url` | string | *必須* | BlueBubbles サーバー URL（`http://localhost:1234`）。 |
| `password` | string | *必須* | BlueBubbles サーバーパスワード。 |
| `chat_guid` | string | *空* | 送信先の GUID。 |
| `poll_interval` | duration | `5s` | `/api/v1/message` に対するポーリング間隔。 |
| `reply_header` | string | *空* | 送信メッセージの先頭に付加されます。 |

### `email`

| フィールド | 型 | デフォルト | 効果 |
|---|---|---|---|
| `imap_addr` | string | *必須* | TLS ラップの IMAP 用 `host:port`（通常 `:993`）。 |
| `imap_username` | string | *必須* | IMAP ユーザー名。 |
| `imap_password` | string | *必須* | IMAP パスワード。 |
| `mailbox` | string | `INBOX` | ポーリング対象のメールボックス。 |
| `poll_interval` | duration | `30s` | UNSEEN メールを確認する頻度。 |
| `smtp_addr` | string | *必須* | SMTP submission 用の `host:port`（通常 `:587`）。 |
| `smtp_username` | string | *必須* | SMTP ユーザー名。 |
| `smtp_password` | string | *必須* | SMTP パスワード。 |
| `from` | string | *必須* | エンベロープおよびヘッダの `From` アドレス。 |
| `reply_header` | string | *空* | 送信メッセージ本文の先頭に付加されます。 |

## 完全な例

```yaml
provider: claudecli

anthropic:
  api_key: sk-ant-...
  model: claude-sonnet-4-6
  max_tokens: 4096

bedrock:
  region: us-east-1
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
  profile: default

vertex:
  project: my-gcp-project
  region: us-central1
  model: claude-sonnet-4@20260101
  credentials_file: ~/.config/gcloud/vertex-key.json

claudecli:
  binary: claude
  model: sonnet
  permission_mode: bypassPermissions
  extra_args: []

log:
  level: info
  format: json

state:
  path: ~/.local/share/rousseau/sessions.db

agent:
  system_prompt: ""
  max_iterations: 32
  skills_dir: ~/.local/share/rousseau/skills
  compression:
    enabled: true
    trigger_messages: 60
    keep_recent: 8
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "^./workspace/.*"}
    deny:
      - {tool: bash, match: "rm -rf|sudo|:\\(\\)\\{ :\\|:& \\};:"}

whatsapp:
  reply_header: "💎 *Rousseau Agent*\n\n"
  voice:
    enabled: false

signal:
  account: "+447900123456"
  allowlist: ["+447900654321"]

telegram:
  token: "123:ABC"
  allowlist: ["12345678"]

matrix:
  homeserver_url: "https://matrix.org"
  access_token: "syt_..."
  user_id: "@bot:matrix.org"
  allowlist: ["@alice:matrix.org"]

slack:
  app_token: "xapp-..."
  bot_token: "xoxb-..."
  bot_user_id: "U0123ABCD"

discord:
  token: "bot-token"
  allowlist: ["123456789012345678"]

sms:
  provider: twilio
  from: "+15550000000"
  account_sid: "AC..."
  auth_token: "..."

imessage:
  base_url: "http://localhost:1234"
  password: "..."
  poll_interval: "5s"

email:
  imap_addr: "imap.example.com:993"
  imap_username: "bot@example.com"
  imap_password: "..."
  smtp_addr: "smtp.example.com:587"
  smtp_username: "bot@example.com"
  smtp_password: "..."
  from: "bot@example.com"
  poll_interval: "30s"
```

## トラブルシューティング

### `config: unmarshal: 1 error(s) decoding: ...`

YAML は有効ですが、あるフィールドの型が誤っています。エラーメッセージにフィールド名が示されます。`internal/config/config.go` で型を確認してください。

### 環境変数の上書きが反映されない

Rousseau は環境変数に `ROUSSEAU_` プレフィックスを付け、ドットをアンダースコアに置き換えます。`anthropic.model` は `ROUSSEAU_ANTHROPIC_MODEL` になります。`ANTHROPIC_API_KEY` は特例で、直接 `anthropic.api_key` に配線されています。

### `config: read: yaml: line X: found character that cannot start any token`

タブによるインデントです。YAML はスペースを要求します。

### `config.yaml` の変更が反映されない

Rousseau は起動時に一度だけコンフィグを読み込みます。デーモンを再起動してください。

### 2 つのコンフィグ値が同時に効いているように見える

優先順位は **フラグ > 環境変数 > ファイル > デフォルト** です。`log.level: debug` を有効化し、`config.loaded` を grep して解決された値を確認してください。

## 関連ページ

- [リファレンス: Config Schema](/ja/reference/config-schema/) — すべてのフィールド。
- [リファレンス: 環境変数](/ja/reference/environment-variables/) — 上書きマトリクス。
- [リファレンス: CLI コマンド](/ja/reference/cli-commands/) — トランスポート別フラグ。
- [プロバイダ](/ja/providers/) — プロバイダ固有のスタンザ。
- [トランスポート](/ja/transports/) — トランスポート固有のスタンザ。

## さらに読む

- `internal/config/config.go` — 正典の構造体。
- `internal/cli/root.go` — コンフィグが読み込まれる場所。
- `internal/config/config_test.go` — ロードセマンティクスのテストマトリクス。
