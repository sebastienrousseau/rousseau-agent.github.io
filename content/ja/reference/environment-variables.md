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
description: "Every environment variable rousseau-agent reads: the ROUSSEAU_ prefix from Viper, ANTHROPIC_API_KEY, XDG paths, provider SDK variables."
keywords: "environment variables, ROUSSEAU_, ANTHROPIC_API_KEY, viper, XDG"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/reference/environment-variables/"
subtitle: "Every environment variable rousseau reads, at what layer, with what default."
tags: "reference, environment, viper, secrets"
title: "リファレンス：環境変数"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "environment variables, ROUSSEAU_, ANTHROPIC_API_KEY, viper, XDG"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "リファレンス：環境変数"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 51
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/reference/environment-variables/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/environment-variables/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "リファレンス：環境変数"
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
twitter_description: "Every environment variable rousseau-agent reads: the ROUSSEAU_ prefix from Viper, ANTHROPIC_API_KEY, XDG paths, provider SDK variables."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "リファレンス：環境変数"
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

## rousseau が環境変数を読み取る方法

2 つのメカニズム、この順序で (`internal/config/config.go` の `config.Load` を参照):

1. **Viper の自動 env バインド。** `SetEnvPrefix("ROUSSEAU")` に加えて `SetEnvKeyReplacer(".", "_")` は、すべての config フィールドが `ROUSSEAU_<UPPER_SNAKE>` として到達可能であることを意味します。つまり `provider` は `ROUSSEAU_PROVIDER` に、`agent.approver.mode` は `ROUSSEAU_AGENT_APPROVER_MODE` になります。
2. **明示的な上書き。** `ANTHROPIC_API_KEY` は環境から直接読み取られ、`anthropic.api_key` に強制的に設定されるため、標準の Anthropic SDK 慣習がそのまま動作します。他のキーは暗黙的に取得されません。

このページの他のすべては、Viper でマップされる変数、rousseau は触れないが根底のライブラリが触れる SDK 管理変数、またはデフォルトを計算するために使用される XDG パスのいずれかです。

優先順位は変わりません: **フラグ > 環境変数 > ファイル > デフォルト**。

## `ROUSSEAU_*` プレフィックス

`internal/config/config.go` のすべての `mapstructure` タグは `ROUSSEAU_<UPPER_SNAKE_PATH>` 経由で到達可能です。選ばれた例 — 完全なリストは config 構造体に従います:

| 変数 | カテゴリ | デフォルト | 説明 |
|---|---|---|---|
| `ROUSSEAU_PROVIDER` | コア | `claudecli` | プロバイダー識別子: `claudecli`、`anthropic`、`openai`、`openrouter`、`ollama`、`bedrock`、`vertex`。 |
| `ROUSSEAU_LOG_LEVEL` | ロギング | `info` | slog レベル: `debug`、`info`、`warn`、`error`。 |
| `ROUSSEAU_LOG_FORMAT` | ロギング | `text` | `text` または `json`。 |
| `ROUSSEAU_STATE_PATH` | 状態 | `$HOME/.local/share/rousseau/sessions.db` | セッションストア DSN。 |
| `ROUSSEAU_AGENT_MAX_ITERATIONS` | エージェント | `32` | ターンごとのツール使用イテレーション上限。 |
| `ROUSSEAU_AGENT_APPROVER_MODE` | エージェント | `` | `allow_all`、`deny_all`、`pattern`。 |
| `ROUSSEAU_AGENT_APPROVER_DEFAULT` | エージェント | `` | `pattern` 用: マッチしない呼び出しでの `allow` または `deny`。 |
| `ROUSSEAU_AGENT_COMPRESSION_ENABLED` | エージェント | `false` | LLM コンプレッサーをオンにします。 |
| `ROUSSEAU_AGENT_COMPRESSION_TRIGGER_MESSAGES` | エージェント | `60` | メッセージ数がこれを超えたら圧縮。 |
| `ROUSSEAU_AGENT_COMPRESSION_KEEP_RECENT` | エージェント | `8` | 逐語的に保持する最新メッセージの数。 |
| `ROUSSEAU_AGENT_SKILLS_DIR` | エージェント | `$HOME/.local/share/rousseau/skills` | スキルディレクトリ。 |
| `ROUSSEAU_ANTHROPIC_API_KEY` | プロバイダー | — | `ANTHROPIC_API_KEY` と同じ。 |
| `ROUSSEAU_ANTHROPIC_MODEL` | プロバイダー | `claude-sonnet-4-6` | Anthropic モデル ID。 |
| `ROUSSEAU_ANTHROPIC_MAX_TOKENS` | プロバイダー | `4096` | 最大レスポンストークン。 |
| `ROUSSEAU_CLAUDECLI_BINARY` | プロバイダー | `claude` | `claudecli` プロバイダーの実行可能ファイル名。 |
| `ROUSSEAU_CLAUDECLI_MODEL` | プロバイダー | — | `claude --model` に渡されます。 |
| `ROUSSEAU_CLAUDECLI_PERMISSION_MODE` | プロバイダー | — | `default`、`acceptEdits`、`bypassPermissions`、`plan` など。 |
| `ROUSSEAU_OPENAI_API_KEY` | プロバイダー | — | OpenAI 互換エンドポイントの Bearer。 |
| `ROUSSEAU_OPENAI_MODEL` | プロバイダー | — | モデル ID。 |
| `ROUSSEAU_OPENAI_BASE_URL` | プロバイダー | — | エンドポイントを上書き。 |
| `ROUSSEAU_OPENROUTER_API_KEY` | プロバイダー | — | OpenRouter の Bearer。 |
| `ROUSSEAU_OPENROUTER_MODEL` | プロバイダー | — | モデル slug。 |
| `ROUSSEAU_OPENROUTER_BASE_URL` | プロバイダー | `https://openrouter.ai/api/v1` | エンドポイント上書き。 |
| `ROUSSEAU_OLLAMA_MODEL` | プロバイダー | — | モデルタグ。 |
| `ROUSSEAU_OLLAMA_BASE_URL` | プロバイダー | `http://localhost:11434/v1` | ローカル Ollama エンドポイント。 |
| `ROUSSEAU_BEDROCK_REGION` | プロバイダー | — | AWS リージョン。 |
| `ROUSSEAU_BEDROCK_MODEL` | プロバイダー | — | Bedrock モデル ID。 |
| `ROUSSEAU_BEDROCK_PROFILE` | プロバイダー | — | AWS 名前付きプロファイル。 |
| `ROUSSEAU_VERTEX_PROJECT` | プロバイダー | — | GCP プロジェクト。 |
| `ROUSSEAU_VERTEX_REGION` | プロバイダー | — | Vertex リージョン。 |
| `ROUSSEAU_VERTEX_MODEL` | プロバイダー | — | Anthropic-on-Vertex モデル。 |
| `ROUSSEAU_VERTEX_CREDENTIALS_FILE` | プロバイダー | — | サービスアカウント JSON へのパス。 |
| `ROUSSEAU_WHATSAPP_REPLY_HEADER` | トランスポート | `💎 *Rousseau Agent*\n\n` | すべての WhatsApp アウトバウンドメッセージの前に付加。 |
| `ROUSSEAU_WHATSAPP_VOICE_ENABLED` | トランスポート | `false` | ボイスノートの whisper 文字起こしを有効化。 |
| `ROUSSEAU_WHATSAPP_VOICE_BINARY` | トランスポート | `whisper` | whisper.cpp 実行可能ファイル。 |
| `ROUSSEAU_WHATSAPP_VOICE_MODEL` | トランスポート | — | whisper モデル名 (`base.en`、`small`)。 |
| `ROUSSEAU_WHATSAPP_VOICE_MODEL_PATH` | トランスポート | — | 明示的な .bin パス (model より優先)。 |
| `ROUSSEAU_WHATSAPP_VOICE_LANGUAGE` | トランスポート | — | ISO コード。空は自動検出。 |
| `ROUSSEAU_SIGNAL_BINARY` | トランスポート | `signal-cli` | signal-cli 実行可能ファイル。 |
| `ROUSSEAU_SIGNAL_ACCOUNT` | トランスポート | — | E.164 電話番号。 |
| `ROUSSEAU_SIGNAL_REPLY_HEADER` | トランスポート | — | 返信ヘッダー。 |
| `ROUSSEAU_TELEGRAM_TOKEN` | トランスポート | — | Bot API トークン。 |
| `ROUSSEAU_TELEGRAM_BASE_URL` | トランスポート | — | Bot API エンドポイントを上書き。 |
| `ROUSSEAU_MATRIX_HOMESERVER_URL` | トランスポート | — | ホームサーバーベース URL。 |
| `ROUSSEAU_MATRIX_ACCESS_TOKEN` | トランスポート | — | Matrix アクセストークン。 |
| `ROUSSEAU_MATRIX_USER_ID` | トランスポート | — | 完全な MXID (`@bot:example.org`)。 |
| `ROUSSEAU_SLACK_APP_TOKEN` | トランスポート | — | `xapp-…` アプリレベルトークン。 |
| `ROUSSEAU_SLACK_BOT_TOKEN` | トランスポート | — | `xoxb-…` bot トークン。 |
| `ROUSSEAU_SLACK_BOT_USER_ID` | トランスポート | — | セルフエコー抑制用の bot のユーザー ID。 |
| `ROUSSEAU_DISCORD_TOKEN` | トランスポート | — | Discord bot トークン。 |
| `ROUSSEAU_SMS_PROVIDER` | トランスポート | — | `twilio` または `vonage`。 |
| `ROUSSEAU_SMS_FROM` | トランスポート | — | 送信者番号。 |
| `ROUSSEAU_SMS_ACCOUNT_SID` | トランスポート | — | Twilio アカウント SID。 |
| `ROUSSEAU_SMS_AUTH_TOKEN` | トランスポート | — | Twilio/Vonage シークレット。 |
| `ROUSSEAU_SMS_API_KEY` | トランスポート | — | Vonage API キー。 |
| `ROUSSEAU_SMS_BASE_URL` | トランスポート | — | 地域エンドポイントまたはテスト用の上書き。 |
| `ROUSSEAU_IMESSAGE_BASE_URL` | トランスポート | — | BlueBubbles サーバー URL。 |
| `ROUSSEAU_IMESSAGE_PASSWORD` | トランスポート | — | BlueBubbles パスワード。 |
| `ROUSSEAU_IMESSAGE_CHAT_GUID` | トランスポート | — | アウトバウンドターゲット。 |
| `ROUSSEAU_IMESSAGE_POLL_INTERVAL` | トランスポート | `2s` | Duration 文字列。 |
| `ROUSSEAU_EMAIL_IMAP_ADDR` | トランスポート | — | IMAP サーバー。 |
| `ROUSSEAU_EMAIL_IMAP_USERNAME` | トランスポート | — | IMAP ユーザー。 |
| `ROUSSEAU_EMAIL_IMAP_PASSWORD` | トランスポート | — | IMAP パスワード。 |
| `ROUSSEAU_EMAIL_MAILBOX` | トランスポート | — | 監視するフォルダ。 |
| `ROUSSEAU_EMAIL_POLL_INTERVAL` | トランスポート | — | Duration 文字列。 |
| `ROUSSEAU_EMAIL_SMTP_ADDR` | トランスポート | — | SMTP 送信ホスト。 |
| `ROUSSEAU_EMAIL_SMTP_USERNAME` | トランスポート | — | SMTP ユーザー。 |
| `ROUSSEAU_EMAIL_SMTP_PASSWORD` | トランスポート | — | SMTP パスワード。 |
| `ROUSSEAU_EMAIL_FROM` | トランスポート | — | From アドレス。 |

**Allowlist 配列** (`ROUSSEAU_SLACK_ALLOWLIST`、`ROUSSEAU_DISCORD_ALLOWLIST`、`ROUSSEAU_TELEGRAM_ALLOWLIST`、…) は Viper でサポートされていますが、カンマ区切りの env 文字列パースは扱いにくい — これらは `config.yaml` に設定するのを推奨します。

## 明示的な環境変数 (ROUSSEAU_ プレフィックス外)

| 変数 | ソース | 目的 |
|---|---|---|
| `ANTHROPIC_API_KEY` | `config.Load` (`internal/config/config.go` の 275 行目) | `anthropic.api_key` にポピュレート。標準 Anthropic SDK 慣習。 |
| `HOME` | `internal/cli/init.go` | `rousseau init` がデフォルト状態パスを計算するために使用。 |

## rousseau が触れない SDK 所有の変数

一部のプロバイダーライブラリは独自の環境を拾います。rousseau はこれらを自身では読み取りませんが、対応するプロバイダーが選択されているときに挙動に影響します:

| 変数 | 消費者 | 備考 |
|---|---|---|
| `AWS_PROFILE`、`AWS_REGION`、`AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY`、`AWS_SESSION_TOKEN`、`AWS_WEB_IDENTITY_TOKEN_FILE` | `aws-sdk-go-v2` (Bedrock) | 標準の認証情報チェーン。静的キーより IRSA またはプロファイルベースの資格情報を推奨。 |
| `GOOGLE_APPLICATION_CREDENTIALS` | Google 認証ライブラリ (Vertex) | サービスアカウント JSON へのパス。`config.yaml` の `vertex.credentials_file` が設定されている場合はそれで代替されます。 |
| `OPENAI_API_KEY` | 上流 Go OpenAI クライアントは通常これを読み取ります | rousseau は `openai.api_key` を通じてキーを明示的に配線します。暗黙的なものはありません。 |
| `HTTP_PROXY`、`HTTPS_PROXY`、`NO_PROXY` | Go net/http | 汎用 Go プロキシ変数。企業 egress パスに便利。 |

## XDG パス変数

rousseau は状態と config に対して XDG Base Directory Specification に従い、2 つのフォールバックがあります:

| 変数 | 効果 |
|---|---|
| `XDG_CONFIG_HOME` | `$XDG_CONFIG_HOME/rousseau/config.yaml` がデフォルトの config パス (`internal/cli/root.go` で参照)。 |
| `XDG_DATA_HOME` | デフォルトの状態パス `$XDG_DATA_HOME/rousseau/sessions.db` (`whatsapp.go`、`skills.go`、`init.go` で参照)。 |
| `HOME` | XDG 変数が未設定のときのフォールバック。rousseau は `internal/config/config.go` で `os.UserHomeDir()` を使用します。 |

`docker/rousseau-agent.container` のコンテナ Quadlet ユニットは `HOME=/home/rousseau` と `XDG_DATA_HOME=/home/rousseau/.local/share` の両方を設定します。

## シークレット衛生

シークレットは以下の 3 つの場所のいずれかに格納してください:

1. **systemd ユニットの `EnvironmentFile=`** — `chmod 0600`、適切に root 所有またはユーザー所有。Quadlet ユニットから参照されます — [VPS デプロイチュートリアル](/ja/tutorials/deploy-to-a-vps/) を参照してください。
2. **シェルによってロードされる `.env` ファイル。** デスクトップ使用のみ。ソース管理外に保管してください。
3. **シークレットマネージャ。** AWS Secrets Manager、HashiCorp Vault、または `pass`/`gopass`。起動時に値をプロセスにパイプします。

`config.yaml` には決してシークレットをコミットしないでください。`config.yaml` は allowlist、ベース URL、非シークレット設定の正しい場所です。API キーや bot トークンには間違った場所です。

## トラブルシューティング

### `ROUSSEAU_...` が設定されているが、rousseau は依然としてデフォルトを使用する

環境変数は起動時に読み取られます。export の後にデーモンを再起動してください。変換ルールも確認してください: config キーのドットはアンダースコアになり、プレフィックスは `ROUSSEAU_` (大文字、正確) です。

### `ANTHROPIC_API_KEY` が無視されているように見える

環境変数は `provider: anthropic` がアクティブなときのみ相談されます。`provider: claudecli` の下では、`claude` CLI が独自の資格情報を読み取ります。

### ホストによって異なる値

優先順位は **フラグ &gt; 環境変数 &gt; ファイル &gt; デフォルト** です。フラグが設定されている場合 (例えば systemd ユニットの `ExecStart` から)、環境変数とファイルの両方に勝ちます。

### コンテナ内で `GOOGLE_APPLICATION_CREDENTIALS` が読み取れない

ファイルがコンテナに読み取り専用でバインドマウントされていて、コンテナ UID (デフォルトで 1000) がそれを読み取れることを確認してください。

## 関連ページ

- [設定](/ja/configuration/) — デフォルト付きのすべての config フィールド。
- [リファレンス: config スキーマ](/ja/reference/config-schema/) — YAML 構造。
- [リファレンス: CLI コマンド](/ja/reference/cli-commands/) — トランスポートごとのフラグ。
- [ガイド: エンタープライズオンボーディング](/ja/guides/enterprise-onboarding/) — プロダクションでのシークレット処理。
- [デプロイ](/ja/deployment/) — シークレット管理オプション。

## さらに読む

- `internal/config/config.go` — `Load` が env プレフィックスとドット-アンダースコアキーリプレーサを設定します。
- `internal/cli/root.go` — `Load` が呼び出される場所。
