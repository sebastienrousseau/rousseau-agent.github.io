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
description: "Set up rousseau-agent's Slack transport: Socket Mode (xapp-* app token + xoxb-* bot token), no public webhook, allowlist by user ID."
keywords: "Slack, Socket Mode, xapp, xoxb, chat.postMessage, connections:write, no webhook, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/transports/slack/"
subtitle: "Socket Mode with no public HTTP surface."
tags: "transports, Slack"
title: "Slack トランスポート"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Slack, Socket Mode, xapp, xoxb, chat.postMessage, connections:write, no webhook, allowlist"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Slack トランスポート"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 16
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/transports/slack/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/slack/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Slack トランスポート"
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
twitter_description: "Set up rousseau-agent's Slack transport: Socket Mode (xapp-* app token + xoxb-* bot token), no public webhook, allowlist by user ID."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Slack トランスポート"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">このページで学べること</span><p>app.slack.com ウィザードの完全なウォークスルー、付与する正確な OAuth スコープ、設定するイベントサブスクリプション、Socket Mode がなぜ公開 webhook を不要にするか、rousseau の自メッセージループ防止の仕組みを扱います。このページと並行して <code>internal/transport/slack/client.go</code> を読んでください。</p></aside>

## 概要

Slack トランスポート（`internal/transport/slack/`）は **Socket Mode**（Slack への送信 WebSocket）を使用するため、デーモンに公開 HTTP サーフェスは不要です。受信イベントはソケット上を流れ、送信呼び出しは標準の Web API（`chat.postMessage`）に届きます。

<aside class="admonition" data-type="tip"><span class="admonition-title">なぜ Socket Mode か</span><p>代替（Events API + Request URL）は SSL 証明書付きの公開 HTTPS エンドポイントを要求します。Rousseau は設計上、受信 HTTP サーフェスを一切同梱しないため、Socket Mode が唯一サポートされる ingress 経路です。</p></aside>

## 2 つのトークン

Slack Socket Mode は、責任が分離した 2 つのトークンを必要とします。

| トークン | プレフィックス | スコープ | 用途 |
|---|---|---|---|
| App-level トークン | `xapp-` | `connections:write` | Socket Mode WebSocket を開きます。 |
| Bot トークン | `xoxb-` | `chat:write` + イベントサブスクリプション | メッセージ送信、イベント購読。 |

## アプリセットアップ

完全な手順は https://app.slack.com/apps にあります:

1. **新規アプリを作成**（"From scratch"）。ワークスペースを選択します。
2. **Socket Mode を有効化**（Settings → Socket Mode）。`connections:write` を持つ **app-level トークン** を生成します。これが `xapp-*` トークンです。
3. **イベントサブスクリプションを設定**（Features → Event Subscriptions）。`message.channels`、`message.im`、その他ボットに聞かせたいチャンネルスコープを購読します。Socket Mode はイベントをソケット上で配信するため、Request URL は **不要** です。
4. **ボットスコープを追加**（Features → OAuth & Permissions）。最低限: `chat:write`。イベントサブスクリプションに合わせて `im:history`、`channels:history`、`groups:history`、`mpim:history` を追加します。
5. **アプリをワークスペースにインストール。** インストール画面が `xoxb-*` ボットトークンを返します。
6. **オプションでボット自身のユーザー ID を記録**（`U…` で始まるもの）。これは rousseau が自メッセージループ防止に使用します。

## 設定

```yaml
slack:
  app_token: "xapp-1-A0..."
  bot_token: "xoxb-1234..."
  bot_user_id: "U0123ABCD"
  reply_header: ""
  allowlist:
    - "U0ALICE"
    - "U0BOB"
```

| フィールド | デフォルト | 効果 |
|---|---|---|
| `app_token` | *必須* | `connections:write` を持つ `xapp-*` app-level トークン。 |
| `bot_token` | *必須* | `chat:write` を持つ `xoxb-*` bot トークン。 |
| `bot_user_id` | *空* | 自メッセージループ防止用のボットユーザーの `U…` ID。オプション。省略時は `bot_id` フィールドの検査にフォールバックします。 |
| `reply_header` | *空* | 送信メッセージの先頭に付加されます。 |
| `allowlist` | `[]` | 処理対象の Slack ユーザー ID。 |

## コマンドライン

```sh
rousseau slack \
  --app-token xapp-... \
  --bot-token xoxb-... \
  --bot-user-id U0123ABCD
```

## ワイヤフォーマット

- **受信。** Slack は WebSocket 上で JSON エンベロープを送信します。rousseau はエンベロープを ACK し、メッセージテキストと送信者を抽出し、ハンドラに渡します。
- **送信。** `POST https://slack.com/api/chat.postMessage` を `{"channel": "<id>", "text": "…"}` と `Authorization: Bearer <bot_token>` で送信します。

## OAuth スコープの説明

各スコープは特定の API サーフェスを付与します。rousseau が必要とするスコープと、それがないと壊れる機能:

| スコープ | 使用されるエンドポイント | ないと壊れるもの |
|---|---|---|
| `connections:write` | `apps.connections.open`（Socket Mode WebSocket） | ソケットを開けません。**必須。** |
| `chat:write` | `chat.postMessage` | どのメッセージにも返信できません。**必須。** |
| `im:history` | DM の `conversations.history`（イベント経由で間接的に） | ボットがイベントで DM の内容を見られません。 |
| `im:read` | `im.list`、DM メタデータ | 開いている DM を一覧できません。 |
| `im:write` | `conversations.open` | 新しい DM を開けません（ボットが未指示で誰かに DM したい場合のみ関連）。 |
| `mpim:history`、`channels:history`、`groups:history` | マルチパーティ IM / チャンネル / プライベートチャンネル | DM 以外でメッセージ内容が見えません。 |

スコープは *OAuth &amp; Permissions &gt; Bot Token Scopes* で設定します。実際に必要なスコープのみ追加してください。Slack はインストール時に各スコープについて警告を出し、エンドユーザーは権限サーフェスの狭いボットをインストールしやすくなります。

## 自メッセージループ防止

保護がなければ、メッセージに返信するボットは自身の返信も受信イベントとして見て、暴走ループにつながります。Rousseau は `bot_user_id` 経由でこれを処理します。

```go
// Simplified — actual logic in internal/transport/slack/client.go
if msg.User == cfg.BotUserID {
    continue // Skip: this is our own outbound message echoing back.
}
```

ボットのユーザー ID は次のように一度取得します。

```sh
curl -H "Authorization: Bearer xoxb-your-token" \
  https://slack.com/api/auth.test
```

レスポンスは `user_id` を含みます。それをコンフィグの `slack.bot_user_id` に貼り付けるか、`--bot-user-id` で渡してください。

<aside class="admonition" data-type="warning"><span class="admonition-title">フォールバックのループ防止</span><p><code>bot_user_id</code> がなくても、トランスポートは <code>bot_message</code> サブタイプのイベントを無視します。しかし subtype のみに頼るのは脆いです。本番では <code>bot_user_id</code> を設定してください。</p></aside>

## スレッド

Slack メッセージはスレッド内の返信であれば `thread_ts` を持ちます。受信イベントに `thread_ts` があった場合、Rousseau の送信呼び出しはそれを含めるため、ボット返信はスレッド化されたままです。ユーザーがスレッドを開始した場合のみ、トップレベルメッセージが新しいスレッドになります。

## 失敗モード

| 症状 | 修正 |
|---|---|
| ソケット開設時に `invalid_auth` | `app_token` が誤りか `connections:write` を欠いています。再生成してください。 |
| 受信イベントが届かない | **Event Subscriptions** が有効で、関連する `message.*` イベントが購読されているか確認してください。 |
| ボットが自分のメッセージに返信する | コンフィグに `bot_user_id` を設定してください。 |
| 送信時に `not_in_channel` | ボットをチャンネルに招待してください（`/invite @rousseau-bot`）。 |
| DM は動作するがチャンネルは動作しない | `channels:history` スコープが欠けているか、ボットがチャンネルに招待されていません。 |

## トラブルシューティング

### ソケット開設時に `invalid_auth`

`xapp-…` トークンが誤りかスコープを失っています。*Basic Information &gt; App-Level Tokens* から再生成し、新しいトークンに `connections:write` があることを確認してください。

### `chat.postMessage` で `not_authed`

Bot トークン（`xoxb-…`）が欠落か誤りです。*OAuth &amp; Permissions &gt; Bot User OAuth Token* から再生成してください。

### イベントは届くが rousseau は何にも応答しない

allowlist を確認してください。`default: deny` の `pattern` モードでは、未登録ユーザーは静かに破棄されます。ログで `router.transport.rejected` を探してください。

### 送信時に `channel_not_found`

Slack チャンネル ID（`C…`）が変わりました。例えばチャンネルがアーカイブされ再作成された場合。ハードコードされたチャンネル ID を更新してください。Rousseau は通常受信イベントのチャンネルを使うため、これは固定チャンネルへの cron 配信でのみ起こります。

### Slack でボットがオフラインに見える

Socket Mode は約 30 秒ごとに WebSocket をアイドルにします。Slack でボットがオフラインと表示される場合は次を確認してください: (1) デーモンが動作している（`systemctl --user status`）、(2) WebSocket が接続されている（ログ行 `slack.connected`）、(3) マシンの時計が真の時刻から 30 秒以内。

## 関連ページ

- [はじめに: はじめてのトランスポート](/ja/getting-started/first-transport/) — エンドツーエンドのウォークスルー。
- [設定](/ja/configuration/) — `slack` コンフィグブロック。
- [トランスポート](/ja/transports/) — 姉妹トランスポート。
- [デプロイ](/ja/deployment/) — Podman コンテナでの Slack 運用。
- [ガイド: 監査 &amp; 承認ポリシー](/ja/guides/audit-approval-policies/) — 共有 Slack ワークスペース向けのポリシールールセット。

## さらに読む

- `internal/transport/slack/client.go` — Socket Mode 接続、イベントポンプ、`chat.postMessage`。
- `internal/cli/slack.go` — CLI 配線。
- `internal/transport/router.go` — allowlist 強制。
- [Slack API ドキュメント: Socket Mode](https://api.slack.com/apis/socket-mode)。
