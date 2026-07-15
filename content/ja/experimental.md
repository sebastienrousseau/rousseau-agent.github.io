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
description: "Off-by-default rousseau-agent behaviour: voice mode via whisper.cpp, FTS5 recall, LLM compression, and other opt-in surface."
keywords: "experimental, voice, whisper, fts5, compression, opt-in, feature flag"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/experimental/"
subtitle: "デフォルトで無効な挙動と、その理由。"
tags: "experimental, opt-in, voice, compression, fts5"
title: "実験的機能"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "experimental, voice, whisper, fts5, compression, opt-in, feature flag"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "実験的機能"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "system"
order: 60
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/experimental/index.html"
item_link: "https://docs.rousseau-agent.dev/experimental/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "実験的機能"
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
twitter_description: "Off-by-default rousseau-agent behaviour: voice mode via whisper.cpp, FTS5 recall, LLM compression, and other opt-in surface."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "実験的機能"
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

## ここで「実験的」が意味すること

Rousseau のデフォルトの姿勢は最小限です: 1 つの静的 Go バイナリ、1 つの SQLite ファイル、外部依存なし。追加のランタイム (`whisper.cpp`)、追加の状態 (リコール用の FTS5 インデックス)、追加のプロバイダコスト (LLM ベースの圧縮) を必要とする機能はすべてオプトインです。

これらはいずれも不安定ではありません。出荷され、テストがあり、サポートされます。しかし運用コストや面積を変えるため、デフォルトはオフです — 必要なものをオンにします。

## ボイスモード (whisper.cpp)

whisper.cpp の `whisper` バイナリをデーモンホストにインストールする必要があるため、デフォルトでオフです。

**トグル:** `config.yaml` の `whatsapp.voice.enabled: true`。`internal/config/config.go` の `VoiceConfig` を参照してください。

**機能内容。** WhatsApp がボイスノートを配信すると、whatsmeow クライアントは OGG ペイロードをダウンロードし、設定されたモデルで `whisper` を呼び出し、書き起こしを受信メッセージテキストとして扱います。構造化ログイベント (`internal/transport/whatsapp/dispatch.go`):

- `whatsapp.audio_downloaded size=N`
- `whatsapp.transcribed elapsed=N`

**オフの理由。** 2 つの理由があります: (1) `whisper` バイナリが存在しない場合、新規インストールが分かりにくく失敗する。(2) 書き起こしはリアルタイムの CPU 消費で、多くのオペレーターは驚かされるよりも自分でオプトインすることを望みます。

完全なセットアップについては [ユーザーガイド: ボイスモード](/ja/user-guide/voice-mode/) を参照してください。

## FTS5 リコール

**トグル。** デフォルトでオンですが、要求するツールによってのみ使用されます。FTS5 インデックスはいずれにせよ構築・維持されます (`internal/state/sqlite/search.go` の `EnsureSearch`)。「オプトイン」なのは、エージェントがモデルにそれを検索させるかどうかです。

**機能内容。** すべての保存済みセッションに対する SQLite FTS5 全文インデックス。`rousseau session search`、MCP ツール `rousseau_search_sessions` を通じて動作し、(エージェントがリコールサーチャで設定されている場合) モデルがターン中にクエリできます。

**この構造の理由。** インデックスは維持コストが低く — `internal/state/sqlite/search.go` のトリガが処理します — しかし毎ターンモデルに公開するのはコストがかかります。エージェントループが `RecallSearcher` (`internal/state/sqlite/recall.go`) で構築された場合にのみ配線されます。

[ユーザーガイド: 圧縮 + リコール](/ja/user-guide/compression-recall/) を参照してください。

## LLM ベースの圧縮

トークンを消費するため、デフォルトでオフです。

**トグル:** `agent.compression.enabled: true`。完全なフィールド一覧は [ガイド: コンテキスト管理](/ja/guides/context-management/) にあります。

**機能内容。** セッションが `trigger_messages` (デフォルト 60) を超えて成長すると、`LLMCompressor` (`internal/agent/compressor.go`) が最も古いスライスを 1 つの合成ユーザーメッセージに要約し、最新の `keep_recent` メッセージをそのまま保持します。以降のすべてのターンはより小さく、より安価になります。

**オフの理由。** リファレンスデプロイはサブスクリプション階層で `claudecli` を実行し、そこではトークン数は課金されません。圧縮は Anthropic 直接、Bedrock、Vertex、OpenAI 互換プロバイダで元が取れます。

## OpenRouter と Ollama のベース URL (プリコンフィグ済み、依然オプトイン)

厳密には実験的ではありませんが、名前を挙げる価値があります: `internal/config/config.go` の rousseau の `setDefaults` は、OpenRouter と Ollama のベース URL をプリコンフィグします:

- `openrouter.base_url: https://openrouter.ai/api/v1`
- `ollama.base_url: http://localhost:11434/v1`
- `ollama.api_key: not-required`

これらのプロバイダの選択は `provider: openrouter` / `provider: ollama` によりオプトインです — エンドポイントは覚えなくて済むように事前入力されているだけです。

## プロンプトインジェクション検出 (ロードマップ)

未出荷です。誠実な脅威モデルについては [ガイド: プロンプトインジェクション](/ja/guides/prompt-injection/) を参照してください。今日の緩和策は完全に承認者ベースです。分類器ベースの検出は、実際に機能する研究待ちのロードマップ項目です。

## Anthropic 以外のプロバイダへのストリーミング (部分的)

Anthropic プロバイダ (`internal/llm/anthropic/client.go`) は SDK のストリーミングインターフェースをサポートします。他のアダプタは現在非ストリーミングモードで動作します。すべてのアダプタでストリーミングを統一するパスが計画されています。

## 関連

- [設定](/ja/configuration/) — すべての設定ノブ。
- [ユーザーガイド: ボイスモード](/ja/user-guide/voice-mode/)。
- [ガイド: コンテキスト管理](/ja/guides/context-management/) — 圧縮の詳細。
- [リファレンス: セッションストア](/ja/reference/session-store/) — FTS5 スキーマ。
