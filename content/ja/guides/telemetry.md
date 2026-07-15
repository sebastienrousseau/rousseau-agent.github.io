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
description: "Rousseau-agent ships zero telemetry. No analytics endpoint, no crash-report upload, no license server, no unique identifiers."
keywords: "telemetry, privacy, no phone home, no analytics, no license server"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/guides/telemetry/"
subtitle: "アナリティクスなし、フォンホームなし。検証可能。"
tags: "guides, telemetry, privacy, security"
title: "ガイド：テレメトリ"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "telemetry, privacy, no phone home, no analytics, no license server"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ガイド：テレメトリ"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 40
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/guides/telemetry/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/telemetry/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "ガイド：テレメトリ"
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
twitter_description: "Rousseau-agent ships zero telemetry. No analytics endpoint, no crash-report upload, no license server, no unique identifiers."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "ガイド：テレメトリ"
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

## コミットメント

rousseau-agent はゼロテレメトリを出荷します。rousseau が明示的に行わないことのリスト:

- 分析エンドポイントなし。`metrics.rousseau-agent.dev` またはそれに相当するものはありません。
- クラッシュレポートのアップロードなし。パニックは stderr に届きます。何もどこにもアップロードされません。
- ライセンスサーバーなし。定期的なチェックインもシート検証もありません。
- ユニークなインストール識別子なし。バイナリは同じタグのすべてのインストールでバイト単位で同一です。
- 機能フラグサービスなし。rousseau のすべてのスイッチは `config.yaml` または CLI フラグにあります。
- アップデート ping なし。`rousseau version` はローカルルックアップです。「アップデートを確認しています」ラウンドトリップはありません。

## 検証方法

rousseau バイナリはオープンソース (MIT、`LICENSE` を参照) です。すべてのネットワーク呼び出しは grep 可能です:

```sh
grep -rn 'http.Get\|http.Post\|http.Client\|http.NewRequest\|net/http' \
  /path/to/rousseau-agent/internal/ | head
```

すべてのヒットは次のカテゴリのいずれかに落ちます:

| パッケージ | 目的 |
|---|---|
| `internal/llm/anthropic/` | Anthropic API 呼び出し (公式 SDK 経由)。 |
| `internal/llm/openai/` | OpenAI 互換エンドポイント呼び出し。 |
| `internal/transport/telegram/` | Telegram Bot API。 |
| `internal/transport/matrix/` | Matrix クライアントサーバー API。 |
| `internal/transport/whatsapp/` | Meta への Whatsmeow websocket。 |
| `internal/transport/slack/`、`discord/` | Socket Mode / Discord Gateway。 |
| `internal/transport/imessage/` | BlueBubbles サーバー (LAN 上)。 |
| `internal/transport/sms/` | Twilio / Vonage。 |
| `internal/transport/email/` | IMAP + SMTP。 |

いずれも分析エンドポイントではありません。それぞれ、設定した LLM プロバイダーか、有効化したトランスポートです。

デーモンを `strace -e network` 下で実行するか、`ss -tanp` で監視してください — 見えるのは上記のエンドポイントへのソケットのみです。

## 構造化ロギングはローカル

rousseau は `log/slog` (`internal/cli/root.go`) を使用します。デフォルトではハンドラは stderr に書き込み、Quadlet ユニット下では systemd journal に届きます。何もホスト外にストリームされません。ログを Loki、Datadog、または他の場所に配送したい場合は、そのパイプラインを自分で設定してください — [ガイド: 可観測性](/ja/guides/observability/) を参照してください。

## 比較

| 製品 | 分析 | クラッシュアップロード | ライセンスサーバー |
|---|---|---|---|
| rousseau-agent | なし | なし | なし |
| ベンダー A (典型的な SaaS コーディングアシスタント) | あり | あり | あり |
| ベンダー B (マネージドコントロールプレーン) | あり | オプトアウト | あり |

rousseau の運用モデル: あなたが LLM キーを持ち込み、あなたがデーモンをホストします。Sebastien が制御するサーバー上で実行される rousseau の部分はありません。

## rousseau が LLM プロバイダーに _送信する_ もの

定義上、Anthropic、Bedrock、Vertex、OpenAI、または他の任意の API を通じてメッセージをルーティングすると、そのプロバイダーはメッセージコンテンツを見ます。これは LLM 推論の仕組みに内在しています — rousseau はクライアントであり、シムではありません。

プロバイダーのデータ処理があなたにとって重要な場合の 2 つの緩和策:

1. **セルフホストのモデルに対して実行する。** Ollama、vLLM、LM Studio、または任意の OpenAI 互換エンドポイント。何もあなたのマシンから出ません。[ガイド: セルフホスト vLLM](/ja/guides/self-hosted-vllm/) を参照してください。
2. **データ処理付帯条項付きのリージョンで Bedrock または Vertex を使用する。** AWS と GCP の両方がリージョンごとのデータ居住性保証を公開しています。

## WhatsApp ブリッジが見るもの

whatsmeow によって実装された非公式の WhatsApp Web プロトコルは Meta のサーバーと話します — そのトラフィックは rousseau の制御外です。Meta はブラウザから WhatsApp Web を使用するときと同じ方法であなたのメッセージを見ます。Meta があなたのメッセージを見ることが受け入れられない場合、WhatsApp ブリッジを実行しないでください。

whatsmeow クライアントは公に監査可能です — すべてのパケットは文書化されています。その上に層状に配置される rousseau 固有のネットワーク呼び出しはありません。

## 関連

- [セキュリティ](/ja/security/) — 信頼境界と監査姿勢。
- [プライバシー](/ja/privacy/) — サイトレベルのプライバシー姿勢。
- [プロバイダー: OpenAI 互換](/ja/providers/openai-compatible/) — セルフホスト推論。
- [ガイド: セルフホスト vLLM](/ja/guides/self-hosted-vllm/) — 作業例。
