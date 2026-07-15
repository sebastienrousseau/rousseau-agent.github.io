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
description: "Set up rousseau-agent's Discord transport: Gateway v10 WebSocket, bot token, Message Content intent, allowlist by user ID."
keywords: "Discord, Gateway v10, WebSocket, bot token, Message Content intent, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/transports/discord/"
subtitle: "Discord Gateway v10 over WebSocket."
tags: "transports, Discord"
title: "Discord トランスポート"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Discord, Gateway v10, WebSocket, bot token, Message Content intent, allowlist"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Discord トランスポート"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 17
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/transports/discord/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/discord/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Discord トランスポート"
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
twitter_description: "Set up rousseau-agent's Discord transport: Gateway v10 WebSocket, bot token, Message Content intent, allowlist by user ID."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Discord トランスポート"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">このページで学べること</span><p>Discord Developer Portal のウォークスルー、rousseau が必要とする Gateway インテントとその理由、パーミッションのビット計算方法、そしてよくある設定ミスに対応する障害モードです。このページと合わせて <code>internal/transport/discord/client.go</code> を参照してください。</p></aside>

## 概要

Discord トランスポート (`internal/transport/discord/`) は、Discord Gateway v10 プロトコルを直接使用します。サードパーティ SDK は利用しません。受信は WebSocket (`Identify → Ready → Heartbeat/Ack → Dispatch(MESSAGE_CREATE)`)、送信は REST (`POST /channels/{id}/messages`) を使います。

## 前提条件

1. **Bot ユーザーを持つ Discord Application。** https://discord.com/developers/applications → **New Application** → **Bot** タブ → **Add Bot** から作成します。
2. **Bot トークン** (Bot タブ → **Reset Token** → トークンをコピー。一度しか表示されません)。
3. **Message Content インテントの有効化** (Bot タブ → **Privileged Gateway Intents**)。これを有効にしないと、Gateway はすべてのイベントからメッセージ本文を取り除き、rousseau には空のボディが届きます。
4. **少なくとも 1 つのサーバーへのボットの招待** (あるいは DM を有効化)。**OAuth2 → URL Generator** で `bot` スコープと `Send Messages` および `Read Message History` の権限を選択し、招待 URL を生成します。

## コンフィグ

```yaml
discord:
  token: "Bot MTIz..."
  reply_header: ""
  allowlist:
    - "123456789012345678"
```

| フィールド | デフォルト | 効果 |
|---|---|---|
| `token` | *必須* | Developer Portal から取得したボットトークン。 |
| `reply_header` | *空* | 送信するすべての返信の先頭に追加されます。 |
| `allowlist` | `[]` | メッセージを処理する Discord ユーザー ID。 |

## コマンドライン

```sh
rousseau discord --token 'MTIz...' --allow 123456789012345678
```

## Gateway インテント

rousseau は 3 つのインテントをリクエストします (`internal/transport/discord/client.go`)。

| インテント | ビット | 目的 |
|---|---|---|
| `GUILD_MESSAGES` | `1 << 9` | サーバーチャンネル内のメッセージ。 |
| `DIRECT_MESSAGES` | `1 << 12` | ボット宛の DM。 |
| `MESSAGE_CONTENT` | `1 << 15` | `content` フィールドを埋めます。**ポータルで有効化する必要があります。** |

Message Content インテントを有効化しないと、`MESSAGE_CREATE` イベントは `content` が空の状態で届き、rousseau は `discord.empty_body` をログに記録します。

## ハートビート

トランスポートは Hello オペコードから通知される Gateway の `heartbeat_interval` を尊重し、Heartbeat を送信して `heartbeat_ack` を追跡します。ACK が欠落するとソケットを閉じ、systemd がプロセスを再起動します。

## 返信ヘッダー

Discord は `**text**` を太字としてレンダリングし、ヘッダー形状に特定の要件はありません。必要に応じて上書きしてください。

```yaml
discord:
  reply_header: "**Rousseau Agent**\n"
```

## パーミッションのビット計算

Discord はボットのチャンネル権限をビットマスクでエンコードします。各権限は 2 のべき乗です。rousseau で一般的に使用されるものは次のとおりです。

| 権限 | ビット |
|---|---|
| Read Messages / View Channels | `1 << 10` = `1024` |
| Send Messages | `1 << 11` = `2048` |
| Send Messages in Threads | `1 << 38` = `274877906944` |
| Read Message History | `1 << 16` = `65536` |
| Add Reactions | `1 << 6` = `64` |

複数の権限を付与するには、ビット同士を OR で結合し、その結果の整数を OAuth2 URL Generator の `permissions=` パラメータに貼り付けます。

```
Read Messages (1024) OR Send Messages (2048) OR Read Message History (65536) = 68608
```

<aside class="admonition" data-type="note"><span class="admonition-title">ポータルのヘルパー</span><p>Developer Portal の <em>OAuth2 URL Generator</em> では、権限チェックボックスをオンにすると整数を自動的に計算してくれます。生成された URL をブックマークしておくと、サーバー管理者がボットを任意の Discord サーバーに招待できます。</p></aside>

## Gateway ライフサイクル

Gateway はステートフルです。

```
Client                        Discord Gateway
  │
  │   ────  Connect  ────▶
  │   ◀── HELLO (heartbeat_interval)
  │
  │   ───── IDENTIFY (token, intents) ────▶
  │   ◀── READY (session_id, user)
  │
  │   ─── Heartbeat every N ms ─▶
  │   ◀── HEARTBEAT_ACK
  │
  │   ◀── MESSAGE_CREATE (a user typed)
  │   ─── (rousseau handles + POSTs reply)
  │
  │   ◀── Disconnect (code 4009: session timed out)
  │   ─── RESUME (session_id) or re-IDENTIFY
```

クライアントは `heartbeat_ack` を追跡します。ACK が欠落するとソケットが閉じ、プロセスが終了します。systemd あるいはコンテナランタイムが再起動します。

## 障害モード

| 症状 | 対処 |
|---|---|
| ボットが空のメッセージを受け取る | Developer Portal で Message Content インテントを有効化してください。 |
| Gateway がコード 4004 でクローズ | トークンが無効です。再生成してください。 |
| ボットがいずれのチャンネルも認識できない | OAuth2 の招待に `bot` スコープが含まれているか確認してください。 |
| 送信で 403 | ボットにそのチャンネルの `Send Messages` 権限がありません。 |
| Identify でコード 4014 | アプリが承認されていないインテント (通常は 100 サーバー以上のボットにおける Message Content) をリクエストしています。ボットを認証してください。 |
| コード 4009 (session timed out) | 長時間のアイドル後に発生する通常の状態です。Rousseau は透過的に再接続します。 |

## トラブルシューティング

### Gateway 4013 (Invalid Intents)

存在しないインテントビットをリクエストしています。通常は、クライアントライブラリのインテント定数と Discord の現在のインテントマップの不一致を意味します。Rousseau は `internal/transport/discord/client.go` でインテントのビットマスクを構築します。Discord API の変更後に 4013 が発生する場合は、最新のリリースにアップグレードしてください。

### ボットがイベントを受信するが応答しない

allowlist の不一致です。`--allow` の値は、数値の Discord ユーザー ID (ユーザー名でも表示名でもない) でなければなりません。Discord での取得方法: *User Settings &gt; Advanced* で Developer Mode を有効にし、ユーザーを右クリックして *Copy User ID* を選択します。

### DM は動作するがギルドチャンネルでは動作しない

`GUILD_MESSAGES` インテントが欠けているか、ボットがそのギルドに招待されていません。ギルドの権限は DM の権限とは別です。ボットはそのチャンネルの `Read Messages` 権限を持っている必要があります。

### 送信で `429 Too Many Requests`

Discord は、ボットあたり全体で 50 req/s のレート制限に加え、チャンネル単位の制限も適用しています。継続的な負荷下では、rousseau は現在リトライを行いません。呼び出し側でバックオフを行う必要があります。[ガイド: レート制限](/ja/guides/rate-limits/) を参照してください。

### ボットのオンラインステータスが不安定になる

Discord はハートビートが約 40 秒欠落するとボットをオフラインとみなします。ログ行 `discord.heartbeat_missed` は、ネットワークの問題または CPU が不足しているデーモンを示します。コンテナに十分な CPU が割り当てられていることを確認してください。

## 関連ページ

- [Getting Started: First Transport](/ja/getting-started/first-transport/) — エンドツーエンドのウォークスルー。
- [Configuration](/ja/configuration/) — `discord` コンフィグブロック。
- [Transports](/ja/transports/) — 兄弟トランスポート。
- [Guides: Audit &amp; Approval Policies](/ja/guides/audit-approval-policies/) — Discord サーバー向けのポリシー。
- [Deployment](/ja/deployment/) — Podman コンテナで Discord を実行する方法。

## さらに読む

- `internal/transport/discord/client.go` — Gateway 接続、ハートビート、イベントポンプ。
- `internal/cli/discord.go` — CLI 配線。
- `internal/transport/router.go` — allowlist の適用。
- [Discord API docs: Gateway](https://discord.com/developers/docs/topics/gateway)。
- [Discord API docs: Permissions](https://discord.com/developers/docs/topics/permissions)。
