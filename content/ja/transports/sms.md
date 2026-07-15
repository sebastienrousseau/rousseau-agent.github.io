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
description: "rousseau-agent's SMS transport is send-only. Twilio (account_sid + auth_token) or Vonage (api_key + auth_token). Inbound not supported because it requires a public webhook."
keywords: "SMS, Twilio, Vonage, Nexmo, send-only, Messaging Service SID, E.164, no webhook"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/transports/sms/"
subtitle: "Send-only SMS via Twilio or Vonage."
tags: "transports, SMS"
title: "SMS トランスポート"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "SMS, Twilio, Vonage, Nexmo, send-only, Messaging Service SID, E.164, no webhook"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "SMS トランスポート"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 19
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/transports/sms/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/sms/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "SMS トランスポート"
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
twitter_description: "rousseau-agent's SMS transport is send-only. Twilio (account_sid + auth_token) or Vonage (api_key + auth_token). Inbound not supported because it requires a public webhook."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "SMS トランスポート"
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

## 設計上、送信専用

SMS トランスポートは **送信専用** です。SMS の受信にはキャリアが POST する公開 HTTP Webhook が必要になり、これは rousseau のインバウンドサーフェスをゼロに保つという方針に真っ向から反します。ユースケースで SMS 受信が必要な場合は、目的専用の Webhook レシーバーと並行して rousseau を実行し、cron スケジューラーまたは agent-loop の埋め込み API 経由でメッセージをルーティングしてください。

`Start` は `ctx.Done()` でブロックするノーオペレーションとして実装されているため、トランスポートは標準デーモンの配線構造にそのまま組み込めます。

## サポート対象のキャリア

| キャリア | コンフィグ `provider` | 必須フィールド |
|---|---|---|
| Twilio | `twilio` | `from`, `account_sid`, `auth_token` |
| Vonage (旧 Nexmo) | `vonage` | `from`, `api_key`, `auth_token` (API シークレット) |

## Twilio コンフィグ

```yaml
sms:
  provider: twilio
  from: "+15550000000"
  account_sid: "AC..."
  auth_token: "..."
```

`from` には、E.164 の送信元番号または **Twilio Messaging Service SID** (`MG…` で始まる) のどちらでも指定できます。Messaging Services はフリート管理、送信元固定 (sticky-sender) ルーティング、地理ベースの送信元選択を処理します。単一国以外のトラフィックには推奨されます。

`base_url` はデフォルトで `https://api.twilio.com/2010-04-01` であり、リージョナルエンドポイントやテスト以外では上書きは不要です。

## Vonage コンフィグ

```yaml
sms:
  provider: vonage
  from: "+15550000000"
  api_key: "abcd1234"
  auth_token: "efgh5678"
```

Vonage コンフィグの `auth_token` は、Vonage の **API シークレット** に対応します。JWT 署名キーではありません。Vonage はシンプルな key/secret ペアで SMS の送信を認証します。

`base_url` はデフォルトで `https://rest.nexmo.com` です。

## コマンドライン

```sh
# Twilio
rousseau sms \
  --provider twilio \
  --from '+15550000000' \
  --account-sid AC... \
  --auth-token ...

# Vonage
rousseau sms \
  --provider vonage \
  --from '+15550000000' \
  --api-key abcd1234 \
  --auth-token efgh5678
```

受信側は存在しないため、`--allow` は適用されません。

## 配信 API

両プロバイダーとも、それぞれの REST エンドポイントを使用します。

- **Twilio。** `POST /2010-04-01/Accounts/{sid}/Messages.json`。SID/トークンで Basic 認証を行います。
- **Vonage。** `POST /sms/json`。ボディに `api_key` と `api_secret` を含めます。

返却されるメッセージ ID はログに記録されますが、配信ステータスの Webhook は消費 **されません** (これも、公開 HTTP サーフェスを持たないためです)。

## E.164 フォーマット

`from` と宛先番号は E.164 (`+<国番号><加入者番号>`) でなければなりません。スペースやハイフンは含めません。Twilio Messaging Service SID は `from` スロットに限りこの要件をバイパスします。

## コスト管理

- プロバイダー側で `max_tokens` を積極的に設定してください。SMS はメッセージ単価が安価ですが、モデルが長い返信を生成するとバイト数が急速に増加します (Twilio は GSM-7 で 160 文字、UCS-2 で 70 文字ごとにセグメント化します)。
- SMS トランスポートに渡す前に、送信する返信を簡潔に書き換えることを検討してください。`agent.Options.SystemPrompt` が適切な設定場所です。
