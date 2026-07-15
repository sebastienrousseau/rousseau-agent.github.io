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
description: "Set up rousseau-agent's Matrix transport: homeserver URL, access token, user ID, long-polling /sync, allowlist by MXID."
keywords: "Matrix, client-server, MXID, access token, homeserver, /sync, long polling, Synapse"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/transports/matrix/"
subtitle: "Matrix client-server API with long-polling /sync."
tags: "transports, Matrix"
title: "Matrix トランスポート"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Matrix, client-server, MXID, access token, homeserver, /sync, long polling, Synapse"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Matrix トランスポート"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 15
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/transports/matrix/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/matrix/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Matrix トランスポート"
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
twitter_description: "Set up rousseau-agent's Matrix transport: homeserver URL, access token, user ID, long-polling /sync, allowlist by MXID."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Matrix トランスポート"
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

Matrix トランスポート (`internal/transport/matrix/`) は、Matrix クライアント/サーバー API を直接使用します。サードパーティ SDK は利用しません。受信は `/sync` のロングポーリング、送信は `/rooms/{room}/send/{event_type}/{txn_id}` を使います。

Synapse、Dendrite、Conduit など、仕様に準拠したあらゆるホームサーバーで動作します。

## 前提条件

1. **ボットアカウント** を任意のホームサーバー上に用意します。標準の Matrix クライアント経由、あるいはホームサーバーの管理 API 経由で登録してください。
2. **そのアカウントのアクセストークン。** 一度通常の Matrix クライアントにボットをログインさせ、**Settings → Help & About → Access Token** からトークンをコピーします。あるいは、ログイン API を直接使用します。

   ```sh
   curl -X POST https://matrix.org/_matrix/client/v3/login \
     -H 'Content-Type: application/json' \
     -d '{"type":"m.login.password","user":"bot","password":"..."}'
   ```

3. **ボットの完全な MXID** (例: `@rousseau-bot:matrix.org`)。自身のメッセージのエコー抑制に使用します。

## コンフィグ

```yaml
matrix:
  homeserver_url: "https://matrix.org"
  access_token: "syt_..."
  user_id: "@rousseau-bot:matrix.org"
  reply_header: ""
  allowlist:
    - "@alice:matrix.org"
    - "@bob:example.com"
```

| フィールド | デフォルト | 効果 |
|---|---|---|
| `homeserver_url` | *必須* | ベース URL (`https://matrix.org`)。 |
| `access_token` | *必須* | ボットユーザーのアクセストークン。 |
| `user_id` | *空* | ボットユーザーの完全な MXID。任意ですが推奨されます (自身のメッセージのエコー抑制)。 |
| `reply_header` | *空* | 送信するすべての返信の先頭に追加されます。 |
| `allowlist` | `[]` | メッセージを処理する MXID。 |

## コマンドライン

```sh
rousseau matrix \
  --homeserver-url https://matrix.org \
  --access-token syt_... \
  --user-id @rousseau-bot:matrix.org \
  --allow @alice:matrix.org
```

## ロングポーリング

`PollTimeout` はデフォルトで 30 秒です。各 `/sync` 応答からの `since` カーソルはメモリに保存され、次回の呼び出しで使用されるため、プロセスの生存期間中にメッセージが再配信されることはありません。再起動時には、デーモンはホームサーバーが返す、まだ有効な最古のカーソルまで巻き戻します。これは通常の `sync` セマンティクスであり、あらゆる Matrix クライアントと同様の挙動です。

## ルームへの招待

ボットが返信すべきルームには、あらかじめメンバーとして参加している必要があります。通常の Matrix クライアントから招待してください。rousseau は招待を自動承認しません。ルームへの参加はスコープ外です。

## 障害モード

| 症状 | 対処 |
|---|---|
| `/sync` で 401 | アクセストークンが期限切れまたは無効化されています。再ログインしてください。 |
| ボットがメッセージを認識しない | ボットがルームに招待されているだけでなく、実際にメンバーになっていることを確認してください。 |
| 自身のメッセージによるエコーループ | コンフィグに `user_id` を設定し、rousseau が自身のメッセージをフィルタできるようにしてください。 |
