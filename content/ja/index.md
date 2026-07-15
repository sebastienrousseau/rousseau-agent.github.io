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
description: "9 つのチャットトランスポート、5 つの LLM プロバイダ、MCP サーバー、SLSA-3 プロビナンス、cosign 署名リリースを備えたセルフホスト型コーディングエージェント。"
keywords: "rousseau-agent, coding agent, self-hosted, container-native, MCP, SLSA-3, cosign, SBOM, LLM, WhatsApp, Signal, Slack"
layout: "index"
permalink: "https://docs.rousseau-agent.dev/ja/"
subtitle: "セルフホスト・コンテナネイティブ・MCP ネイティブなコーディングエージェント。"
tags: "overview, self-hosted, mcp, security"
title: "rousseau-agent"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "rousseau-agent, coding agent, self-hosted, container-native, MCP, SLSA-3, cosign, SBOM, LLM, WhatsApp, Signal, Slack"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "rousseau-agent"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "welcome"
order: 1
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/index.html"
item_link: "https://docs.rousseau-agent.dev/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "rousseau-agent"
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
twitter_description: "9 つのチャットトランスポート、5 つの LLM プロバイダ、MCP サーバー、SLSA-3 プロビナンス、cosign 署名リリースを備えたセルフホスト型コーディングエージェント。"
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "rousseau-agent"
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

## セルフホスト・コンテナネイティブ・MCP ネイティブなコーディングエージェント

**rousseau-agent** は、あなたのコードが動く場所で動く Go 製のコーディングアシスタントです。デーモン、認証情報、モデルとの通信は、すべて運用側が管理するハードウェア上に留まります。**9 種類のトランスポート・5 種類の LLM プロバイダ・SLSA-3・cosign・SBOM。**

```sh
rousseau chat
```

このコマンド一つで、設定した LLM プロバイダに接続された Bubble Tea 製の TUI が起動します。ネットワーク境界を越えるのは、プロバイダへの API 呼び出しそのものだけです。

## 3 つの柱

### エンタープライズ向けに硬化

- **SLSA レベル 3** のビルド来歴を `slsa-framework/slsa-github-generator` で提供。
- 各リリースのチェックサムファイルに対する **cosign** キーレス署名。Sigstore のトランスパレンシログで検証可能。
- 各リリースに **CycloneDX** の JSON SBOM を同梱。
- CI 上でクリーンチェックアウトから **再現可能なビルド** を検証。
- rootless Podman を `ReadOnly=true`、`DropCapability=all`、`NoNewPrivileges=true`、デフォルトの seccomp フィルタ、非 root の UID 1000、`keep-id` ユーザーネームスペースマッピングで運用。
- 18 のリンタを束ねた `golangci-lint` v2 ゲート、CodeQL (Go)、CI 実行毎の `govulncheck`、`gomod` と `github-actions` の Dependabot。

### マルチモーダルな到達範囲

9 種類のチャットトランスポートが 1 つのデーモンの背後で動作します:

- [WhatsApp](/ja/transports/whatsapp/) (`go.mau.fi/whatsmeow`、Signal プロトコル互換)
- [Signal](/ja/transports/signal/) (`signal-cli` の JSON-RPC サブプロセス)
- [Telegram](/ja/transports/telegram/) (Bot API のロングポーリング)
- [Matrix](/ja/transports/matrix/) (クライアント/サーバー API)
- [Slack](/ja/transports/slack/) (Socket Mode、公開 HTTP 面なし)
- [Discord](/ja/transports/discord/) (Gateway v10)
- [iMessage](/ja/transports/imessage/) (BlueBubbles の HTTP ポーリング)
- [Email](/ja/transports/email/) (IMAP + SMTP)
- [SMS](/ja/transports/sms/) (Twilio または Vonage、送信専用)

### モデル非依存

5 種類の LLM プロバイダ・ファミリを、1 つの `agent.Provider` インターフェースで扱います:

- [claudecli](/ja/providers/claudecli/) — ローカルの `claude` CLI へのサブプロセス。認証はそちらから継承。
- [Anthropic](/ja/providers/anthropic/) — 直接の API。エフェメラルなプロンプトキャッシュマーカー付き。
- [AWS Bedrock](/ja/providers/bedrock/) — 標準の AWS クレデンシャルチェーン。
- [Google Vertex AI](/ja/providers/vertex/) — サービスアカウント JSON または ADC。
- [OpenAI 互換](/ja/providers/openai-compatible/) — OpenAI、OpenRouter、Ollama、vLLM、LM Studio。

## 次に読むもの

- [はじめに](/ja/getting-started/) — インストール、初回実行、最初のトランスポート。
- [設定](/ja/configuration/) — `internal/config/config.go` のすべてのフィールド。
- [デプロイ](/ja/deployment/) — rootless Podman + Quadlet、Kubernetes に関するメモ。
- [セキュリティ](/ja/security/) — サプライチェーン、信頼モデル、cosign の手順。
- [コンセプト](/ja/concepts/) — エージェントループ、セッションストア、MCP、cron、スキル。
