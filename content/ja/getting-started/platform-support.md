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
description: "Support matrix for rousseau-agent: operating systems, CPU architectures, container runtimes, provider authentication methods, transport backing libraries."
keywords: "platform support, os matrix, architecture, container runtime, provider auth, linux, macos, windows, arm64, amd64"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/getting-started/platform-support/"
subtitle: "OS, architectures, container runtimes, provider auth methods."
tags: "platform, support, matrix"
title: "対応プラットフォーム"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "platform support, os matrix, architecture, container runtime, provider auth, linux, macos, windows, arm64, amd64"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "対応プラットフォーム"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 23
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/getting-started/platform-support/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/platform-support/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "対応プラットフォーム"
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
twitter_description: "Support matrix for rousseau-agent: operating systems, CPU architectures, container runtimes, provider authentication methods, transport backing libraries."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "対応プラットフォーム"
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

## オペレーティングシステム

| OS | サポート階層 | 備考 |
|---|---|---|
| Linux (glibc、カーネル 5.10+) | ティア 1 | CI はプッシュごとに `ubuntu-latest` を実行します。リファレンスデプロイターゲット。 |
| Linux (musl / Alpine) | ティア 1 | コンテナイメージは Alpine ベースです。 |
| macOS 13+ (Ventura 以上) | ティア 1 | CI はプッシュごとに `macos-latest` を実行します。Bubble Tea TUI が検証されています。 |
| Windows 10 / 11 | ティア 2 | バイナリはビルドされ出荷されますが、CI は Windows 上で完全なレースマトリックスを実行しません。チャットトランスポートは動作します。Podman + Quadlet リファレンスデプロイは Linux を前提としています。 |
| FreeBSD / OpenBSD | ベストエフォート | 純粋 Go ビルドですが、CI ジョブはありません。コミュニティレポートを歓迎します。 |

## CPU アーキテクチャ

| アーキテクチャ | サポート階層 | リリース命名 |
|---|---|---|
| `amd64` (x86-64) | ティア 1 | `_linux_amd64`、`_darwin_amd64`、`_windows_amd64` |
| `arm64` (aarch64) | ティア 1 | `_linux_arm64`、`_darwin_arm64` (Apple Silicon) |
| `armv7` (32 ビット ARM) | ベストエフォート | `GOARCH=arm GOARM=7` でビルド可能。リリースなし。 |
| `riscv64` | ベストエフォート | `GOARCH=riscv64` でビルド可能。リリースなし。 |

すべてのターゲットで `CGO_ENABLED=0` — `modernc.org/sqlite` は純粋 Go なので、クロスコンパイルは摩擦なしです。

## コンテナランタイム

| ランタイム | サポート階層 | 備考 |
|---|---|---|
| Podman 4.4+ (rootless) | ティア 1 | リファレンスデプロイ。宣言的ハードニングのために systemd Quadlet ユニットを使用します。 |
| Docker 24+ | ティア 1 | Dockerfile は変更なしで動作します。ランタイムハードニングはあなたの責任です (Quadlet 相当なし)。 |
| containerd + `nerdctl` | ティア 2 | 同じイメージ。nerdctl は同じ OCI アーティファクトを消費します。 |
| Kubernetes 1.27+ | ティア 2 | [ガイド: Kubernetes デプロイ](/ja/guides/kubernetes-deployment/) を参照してください。 |

## プロバイダ認証方式

| プロバイダ | 認証メカニズム | 設定キー |
|---|---|---|
| `claudecli` (デフォルト) | `~/.claude/` から Claude Code の OAuth トークンを継承。rousseau の設定にキーなし。 | `claudecli.binary`、`claudecli.permission_mode` |
| `anthropic` | 直接 API キー。 | `ANTHROPIC_API_KEY` 環境変数、または `anthropic.api_key` |
| `openai` | OpenAI API キーまたはサードパーティトークン。 | `OPENAI_API_KEY`、または `openai.api_key` |
| `openrouter` | OpenRouter API キー。`openrouter.base_url` プリセットで OpenAI スキーマを使用します。 | `openrouter.api_key` |
| `ollama` | ローカルエンドポイント。キー不要 (`ollama.api_key` はデフォルトで `not-required`)。 | `ollama.base_url` は `http://localhost:11434/v1` にプリセット |
| `bedrock` | 標準の AWS 認証情報チェーン (環境変数、`~/.aws/credentials`、IMDS、IAM ロール)。 | `bedrock.region`、`bedrock.profile`、`bedrock.model` |
| `vertex` | GCP サービスアカウント JSON、または Application Default Credentials。 | `vertex.project`、`vertex.region`、`vertex.credentials_file` |

## トランスポートバッキングライブラリ

すべてのトランスポートは、上流クライアント上の薄いアダプタです。サポートは上流プロジェクトの存続可能性によって制限されます。

| トランスポート | 上流 | プロトコル |
|---|---|---|
| WhatsApp | `go.mau.fi/whatsmeow` | 非公式 WhatsApp Web プロトコル (Signal 互換)。 |
| Signal | `signal-cli` サブプロセス | Signal JSON-RPC。 |
| Telegram | 直接 Bot API クライアント | ロングポーリング。 |
| Matrix | 直接クライアント/サーバー API クライアント | HTTPS ポーリング。 |
| Slack | 直接 Socket Mode クライアント | 送信 WebSocket。 |
| Discord | 直接 Gateway クライアント | 送信 WebSocket + インテント。 |
| iMessage | BlueBubbles HTTP クライアント | BlueBubbles ポーリング。BlueBubbles Server を実行する macOS ホストが必要。 |
| Email | 標準の `net/smtp` + IMAP クライアント | TLS 上の IMAP + SMTP。 |
| SMS | 直接 Twilio / Vonage REST | 送信専用。 |

## オプションのランタイム依存

| 依存関係 | 必要な機能 | バージョン |
|---|---|---|
| `claude` CLI | `provider: claudecli` (デフォルト)。 | 最新。 |
| `signal-cli` | Signal トランスポート。 | 0.13+。JVM が必要。 |
| BlueBubbles Server | iMessage トランスポート。 | 1.9+。macOS ホスト上で実行。 |
| `whisper.cpp` CLI | WhatsApp ボイスノート書き起こし (`whatsapp.voice.enabled: true`)。 | 1.5+。コンテナイメージには同梱されません。 |
| `podman` | リファレンスデプロイ。 | Quadlet サポート用に 4.4+。 |
| `systemd` (ユーザーセッション) | リファレンスデプロイ。 | Quadlet 用に 249+。 |

## コンパイラとツールチェーン

| コンポーネント | バージョン | 備考 |
|---|---|---|
| Go | 1.26+ | `go.mod` はモジュールグラフを正確にピン留めします。 |
| golangci-lint | v2 | 18 個のリンタ、`.golangci.yml` に正確なピン留め。 |
| govulncheck | 最新 | すべての CI ビルドで実行。 |
| cosign | 2.2+ | 署名付きリリースの検証時のみ。 |

## 次に

- [インストール](/ja/getting-started/installation/) — プラットフォームに合わせてインストールします。
- [更新](/ja/getting-started/updating/) — バージョン間を安全に移動します。
