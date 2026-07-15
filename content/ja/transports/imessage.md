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
description: "Set up rousseau-agent's iMessage transport: BlueBubbles server on macOS, HTTP polling, poll interval, cursor deduplication, chat GUID for outbound."
keywords: "iMessage, BlueBubbles, macOS, HTTP polling, chat GUID, cursor, deduplication"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/transports/imessage/"
subtitle: "BlueBubbles HTTP polling from a macOS host."
tags: "transports, iMessage"
title: "iMessage トランスポート"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "iMessage, BlueBubbles, macOS, HTTP polling, chat GUID, cursor, deduplication"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "iMessage トランスポート"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 18
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/transports/imessage/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/imessage/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "iMessage トランスポート"
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
twitter_description: "Set up rousseau-agent's iMessage transport: BlueBubbles server on macOS, HTTP polling, poll interval, cursor deduplication, chat GUID for outbound."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "iMessage トランスポート"
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

## 概要

iMessage トランスポート (`internal/transport/imessage/`) は iMessage を直接扱いません。Apple はクライアント向けのサポートされた API を提供していないためです。代わりに、iMessage を HTTP と Socket.IO 経由で公開する macOS 側デーモンである [BlueBubbles](https://bluebubbles.app) をポーリングします。

rousseau は BlueBubbles の HTTP エンドポイントのみを使用します (依存フットプリントを小さく保つため、Socket.IO は意図的に避けています)。

## アーキテクチャ

```
+-----------+     iMessage      +---------+     HTTP      +-----------+
| Apple ID  | <---------------> | macOS   | <-----------> | rousseau  |
|  server   |                   | Blue    |               | daemon    |
+-----------+                   | Bubbles |               |           |
                                +---------+               +-----------+
```

macOS ホストは BlueBubbles を実行し、iMessage にサインインしたままにしておきます。rousseau は BlueBubbles の `/api/v1/message` エンドポイントを設定されたペースでポーリングし、新規到着分をハンドラーに転送します。

## 前提条件

1. **iMessage にサインイン済みの macOS ホスト。** 必ずしも rousseau が動作するマシンと同じである必要はありません。
2. **BlueBubbles サーバー** をそのホストにインストールし、rousseau から到達可能な URL (LAN アドレス、VPN、または Tailscale) でリッスンさせます。
3. **BlueBubbles のパスワード** (サーバー GUI → Settings → Server Password)。
4. **送信用の chat GUID。** BlueBubbles の GUI または `GET /api/v1/chat` で確認します。

## コンフィグ

```yaml
imessage:
  base_url: "http://mac.internal:1234"
  password: "..."
  chat_guid: "iMessage;-;+15550001234"
  poll_interval: "5s"
  reply_header: ""
```

| フィールド | デフォルト | 効果 |
|---|---|---|
| `base_url` | *必須* | BlueBubbles サーバーの URL。 |
| `password` | *必須* | BlueBubbles サーバーのパスワード。 |
| `chat_guid` | *空* | 送信先の GUID。 |
| `poll_interval` | `5s` | `/api/v1/message` に対するポーリング間隔。 |
| `reply_header` | *空* | 送信するすべてのメッセージの先頭に追加されます。 |

## コマンドライン

```sh
rousseau imessage \
  --base-url http://mac.internal:1234 \
  --password ... \
  --chat-guid 'iMessage;-;+15550001234' \
  --poll-interval 5s
```

## カーソルによる重複排除

起動時にトランスポートは `lastID` カーソルを既存の最新メッセージに初期化するため、オペレーターに iMessage の全履歴が一気に届くことはありません。以降のポーリングごとに、最新の `PageSize` 件 (デフォルト 25) を取得し、カーソルより新しいものだけを転送します。

カーソルはインメモリです。再起動時にはカーソルが BlueBubbles から再初期化されるため、デーモンが停止していた間に到着した少数のメッセージは失われます。これは意図的なトレードオフです。永続的なカーソルロジックはステートストアに別のテーブルを必要としますし、iMessage の配信タイムスタンプはデバイス間で単調増加であることが保証されていません。

## 到達性

BlueBubbles は rousseau の実行環境からネットワーク到達可能である必要があります。一般的なパターンは次のとおりです。

- **同一 LAN。** `http://<mac-lan-ip>:1234`。
- **Tailscale。** `http://mac.tailnet.ts.net:1234`。リンクを暗号化し、NAT を超えて動作します。
- **リバーストンネル。** Mac からの SSH `-R` トンネルを使って rousseau ホスト上で `http://localhost:1234`。

認証モデル (単一パスワード) を十分に理解していない限り、BlueBubbles を公衆インターネットに公開しないでください。

## 障害モード

| 症状 | 対処 |
|---|---|
| 起動時に `imessage.prime_failed` | BlueBubbles に到達できません。`base_url` と `password` を確認してください。 |
| 過去のメッセージがすべて再生される | `lastID` の初期化ができていません。パーミッションと認証を確認してください。 |
| 送信メッセージがサイレントに破棄される | `chat_guid` が誤っています。`GET /api/v1/chat` で確認してください。 |
| メッセージが数分遅れて届く | BlueBubbles 自身のポーリング頻度を上げるか、`poll_interval` を下げてください。 |
