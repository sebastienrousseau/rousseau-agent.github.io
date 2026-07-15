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
description: "Set up rousseau-agent's Telegram transport: BotFather token, long-polling, allowlist by numeric user ID, reply-header customisation."
keywords: "Telegram, Bot API, BotFather, long polling, getUpdates, allowlist, chat ID"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/transports/telegram/"
subtitle: "Telegram Bot API over long-polling."
tags: "transports, Telegram"
title: "Telegram トランスポート"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Telegram, Bot API, BotFather, long polling, getUpdates, allowlist, chat ID"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Telegram トランスポート"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 14
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/transports/telegram/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/telegram/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Telegram トランスポート"
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
twitter_description: "Set up rousseau-agent's Telegram transport: BotFather token, long-polling, allowlist by numeric user ID, reply-header customisation."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Telegram トランスポート"
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

Telegram トランスポート (`internal/transport/telegram/`) は、Telegram Bot HTTP API を直接使用します。サードパーティ SDK は利用しません。受信は `getUpdates` のロングポーリング、送信は `sendMessage` を使います。

## 前提条件

1. **ボット。** Telegram で [@BotFather](https://t.me/BotFather) にメッセージを送り、`/newbot` を実行し、名前と `_bot` サフィックス付きのユーザー名を選択します。BotFather は `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` のような HTTP API トークンを返します。
2. **認可したいユーザー ID。** Telegram のユーザー ID は数値です。ボットは `@username` からユーザー ID を単独で解決できません。標準的な手法は、認可されたすべてのユーザーに一度 `/start` をボットに送信させ、ログから `from.id` を読み取ることです。

## コンフィグ

```yaml
telegram:
  token: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
  reply_header: ""
  allowlist:
    - "12345678"
    - "98765432"
```

| フィールド | デフォルト | 効果 |
|---|---|---|
| `token` | *必須* | BotFather から取得したボットトークン。 |
| `base_url` | `https://api.telegram.org` | ローカルの Bot API サーバー向けの上書き。 |
| `reply_header` | *空* | 送信するすべての返信の先頭に追加されます。 |
| `allowlist` | `[]` | メッセージを処理する Telegram ユーザー ID。 |

## コマンドライン

```sh
rousseau telegram --token 123456:ABC... --allow 12345678 --allow 98765432
```

`--allow` は複数回指定できます。

## ロングポーリング

トランスポートはデフォルトで 30 秒の `PollTimeout` で `getUpdates` を呼び出します (`internal/transport/telegram/client.go`)。返される各アップデートは内部の `offset` を進めるため、再起動をまたいでもメッセージが再配信されることはありません。

Webhook はありません。デーモンはインバウンド HTTP サーフェスを必要としません。

## メッセージ形状

テキストメッセージのみを処理します。メディア、ステッカー、およびボイスメモは無視されます (将来のアップグレードで、WhatsApp と同じ whisper.cpp パスを通じてオーディオをルーティングできる可能性があります)。

## 障害モード

| 症状 | 対処 |
|---|---|
| アップデートが届かない | ボットに対して少なくとも一度メッセージが送信されていることを確認してください。Telegram は過去のメッセージを配信しません。 |
| getUpdates で 409 Conflict | 同じトークンで別のインスタンスがポーリングしています。もう一方を停止してください。 |
| 実在のユーザーが allowlist で拒否される | `from.id` フィールドをログに記録してください。ユーザー ID は数値であり、`@username` とは一致しません。 |
