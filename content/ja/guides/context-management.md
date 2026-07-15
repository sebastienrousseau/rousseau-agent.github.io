---

# Front Matter (YAML)

author: "sebastian.rousseau@gmail.com (Sebastien Rousseau) "
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
description: "How the LLM compressor decides what to keep, the roles of trigger_messages and keep_recent, and a before/after diagram of a compressed session."
keywords: "compression, context, keep_recent, trigger_messages, summariser, marker"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/guides/context-management/"
subtitle: "trigger_messages, keep_recent, and the compressed-marker convention."
tags: "guides, context, compression, summariser"
title: "ガイド：コンテキスト管理"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "compression, context, keep_recent, trigger_messages, summariser, marker"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ガイド：コンテキスト管理"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/guides/context-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/context-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "ガイド：コンテキスト管理"
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
twitter_description: "How the LLM compressor decides what to keep, the roles of trigger_messages and keep_recent, and a before/after diagram of a compressed session."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "ガイド：コンテキスト管理"
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

## 問題

何週間も実行されるセッションは、何百ものメッセージを蓄積します。それぞれがターンごとにプロバイダーに再送信されます。コストはターン数に比例して成長します。レイテンシも成長します。rousseau の `LLMCompressor` (`internal/agent/compressor.go`) は、小さな一回限りのコスト — 圧縮ごとに 1 回の要約呼び出し — を、以降のすべてのターンでの永続的な節約と引き換えます。

圧縮は **デフォルトでオフ** です。参照デプロイメントがサブスクリプション階層で `claudecli` を使用しており、そこではトークン数が課金されないためです。Anthropic 直接、Bedrock、Vertex、または OpenAI 互換のトークン従量課金プロバイダーに対して実行する場合はオンにしてください。

## ノブ

`internal/config/config.go` の `CompressionConfig` から:

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60        # zero uses the default 60
    keep_recent: 8              # zero uses the default 8
    prompt: ""                  # overrides the default summariser prompt
```

意味:

| フィールド | 何をするか |
|---|---|
| `enabled` | 圧縮をオンにします。false のとき、エージェントは `NoopCompressor` を使用し、このセクション全体は no-op になります。 |
| `trigger_messages` | `len(session.Messages) >= trigger_messages` になると圧縮が発火します。 |
| `keep_recent` | 圧縮後に逐語的に保持される最新メッセージの数。 |
| `prompt` | デフォルトの要約プロンプトを上書きします。カスタム指示 (例: JSON 出力を保持、常にファイルパスを引用) が必要な場合のみ設定してください。 |

## デフォルトの要約プロンプト

```
Summarise the following conversation in <=200 words. Preserve every
commitment, TODO, credential, filename, and quoted output. Skip
pleasantries. Return only the summary — no preamble.
```

`internal/agent/compressor.go` の `defaultSummaryPrompt` として定義されています。`config.yaml` の `agent.compression.prompt` で上書きしてください。

## Before / after

68 メッセージ、`trigger_messages: 60`、`keep_recent: 8` のセッション:

```
Before compression:                        After compression:

┌──────────────────────────┐              ┌──────────────────────────────┐
│ msg[0]  user             │              │ msg[0]  user (synthetic)     │
│ msg[1]  assistant        │              │   [rousseau-compressed]      │
│ msg[2]  user             │              │   (summary of prior 60       │
│  …  (60 messages)        │      →       │    messages): …              │
│ msg[59] assistant        │              ├──────────────────────────────┤
├──────────────────────────┤              │ msg[1]  user       — verbatim │
│ msg[60] user   verbatim  │              │ msg[2]  assistant  — verbatim │
│ msg[61] assistant        │              │ msg[3]  user       — verbatim │
│  …                       │              │ msg[4]  assistant  — verbatim │
│ msg[67] assistant        │              │ msg[5]  user       — verbatim │
└──────────────────────────┘              │ msg[6]  assistant  — verbatim │
                                          │ msg[7]  user       — verbatim │
                                          │ msg[8]  assistant  — verbatim │
                                          └──────────────────────────────┘
Total messages: 68                        Total messages: 9
Input tokens: ~5000 per turn              Input tokens: ~800 per turn
```

## マーカー

コンプレッサーは合成ユーザーメッセージの前に `[rousseau-compressed]` (`internal/agent/compressor.go` の定数 `DefaultCompressorMarker`) を付けます。以降のターンでは、`headAlreadyCompressed()` がマーカーを使用してすでに圧縮されたプレフィックスを検出し、セッションが `2 * trigger_messages` に成長していない限り繰り返し圧縮をスキップします。

これが圧縮を境界付けているものです — 60 メッセージごとに要約を再要約するために支払うことはありません。

## 値の選択

| 状況 | 推奨 |
|---|---|
| 有料プロバイダー上の長時間実行トランスポートデーモン。 | `trigger_messages: 60`、`keep_recent: 8`。デフォルトはこれにチューニングされています。 |
| すべてをコンテキストに入れたい対話的 TUI。 | `enabled: false`。 |
| 引用されたコード / ログが大量にある高度に技術的なセッション。 | `trigger_messages: 40`、`keep_recent: 12`。より新しいコンテキストを保持し、より早く圧縮します。 |
| コストクリティカルなバッチサマライザー (cron)。 | 各 cron 実行は新しいセッションであるため、圧縮はめったにトリガーされません。デフォルトのままにしてください。 |

## 圧縮パスのコスト

発火ごとに 1 回の要約呼び出し。使用されるプロバイダーは `Config.Provider` が選択するもの — エージェントが使用するのと同じものです。それは:

- Sonnet クラスのコンプレッサー呼び出し: ~1-2 秒、およそ 2 ターン分の入力トークンのコスト。
- セッションの形状によって以降 ~5-10 ターン後に損益分岐。

より安価なコンプレッサーの場合は、コンプレッサーデーモンに Haiku クラスのモデルを使用する 2 デーモンのマルチプロバイダーパターンで rousseau を実行してください。[ガイド: マルチプロバイダー](/ja/guides/multi-provider/) を参照してください。

## 緊急事態: セッションがロードするには大きすぎる

圧縮が発火する前にセッションのペイロードがモデルのコンテキストウィンドウを超えて成長した場合 — まれですが、非常に小さい `trigger_messages` と大きなツール出力で可能 — 次のターンはプロバイダーの「context length exceeded」エラーで失敗します。回復:

```sh
rousseau session delete <id> --yes
```

その後、新しく始めてください。または SQLite 経由で手動で縮小:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
UPDATE sessions SET payload = json_set(payload, '$.messages',
  json_extract(payload, '$.messages[-8:]'))
WHERE id = '<session-id>';
SQL
```

注意: 正確な JSON パス構文は SQLite バージョンに依存します。まず `SELECT payload` で確認してください。

## 関連

- [ユーザーガイド: 圧縮 + 再呼び出し](/ja/user-guide/compression-recall/) — より深いリファレンス。
- [ガイド: レート制限](/ja/guides/rate-limits/) — コストへの影響。
- [ガイド: セッション管理](/ja/guides/session-management/) — セッションライフサイクル。
- [リファレンス: config スキーマ](/ja/reference/config-schema/) — すべてのフィールド。
