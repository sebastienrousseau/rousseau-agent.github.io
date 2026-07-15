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
description: "Overview of rousseau-agent's nine chat transports: WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, Email, SMS. Every transport implements Start / Stop / Deliver."
keywords: "transports, WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, email, SMS"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/transports/"
subtitle: "9 種類のチャットトランスポートを 1 つの Transport インターフェースで扱う。"
tags: "transports, overview"
title: "トランスポート"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "transports, WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, email, SMS"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "トランスポート"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 11
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/transports/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "トランスポート"
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
twitter_description: "Overview of rousseau-agent's nine chat transports: WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, Email, SMS. Every transport implements Start / Stop / Deliver."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "トランスポート"
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

## Transport インターフェース

すべてのトランスポートは 1 つの小さなインターフェースを実装します (`internal/transport/transport.go`):

```go
type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

トランスポートの上には `Router` があり、送信者ごとのセッションルックアップ、許可リストの強制、`Agent` へのディスパッチを処理します。下にはトランスポート固有のワイヤコードがあります。

出荷されるトランスポートは、いずれもデフォルトで公開 HTTP 面を公開しません。これは意図的な姿勢の選択です — rousseau デーモンは、ポートフォワーディングルールなしで NAT の背後で安全に実行できるべきです。

## サポートされるトランスポート

| トランスポート | 受信 | 送信 | バッキングライブラリ / プロトコル | 認証 | 1 行セットアップ |
|---|:---:|:---:|---|---|---|
| [WhatsApp](/ja/transports/whatsapp/) | あり | あり | `go.mau.fi/whatsmeow` | デバイスペア (QR) | `rousseau whatsapp --allow <jid>` |
| [Signal](/ja/transports/signal/) | あり | あり | `signal-cli` JSON-RPC | 事前登録済みアカウント | `rousseau signal --account +447900123456` |
| [Telegram](/ja/transports/telegram/) | あり | あり | Bot API ロングポーリング | BotFather トークン | `rousseau telegram --token <token>` |
| [Matrix](/ja/transports/matrix/) | あり | あり | クライアント/サーバー API `/sync` | アクセストークン | `rousseau matrix --homeserver-url … --access-token …` |
| [Slack](/ja/transports/slack/) | あり | あり | Socket Mode + Web API | `xapp-*` + `xoxb-*` | `rousseau slack --app-token … --bot-token …` |
| [Discord](/ja/transports/discord/) | あり | あり | Gateway v10 + REST | Bot トークン | `rousseau discord --token <token>` |
| [iMessage](/ja/transports/imessage/) | あり | あり | BlueBubbles HTTP ポーリング | サーバーパスワード | `rousseau imessage --base-url … --password …` |
| [Email](/ja/transports/email/) | あり | あり | IMAP + SMTP | ユーザー名 + パスワード | `rousseau email --imap-addr … --smtp-addr …` |
| [SMS](/ja/transports/sms/) | なし | あり | Twilio または Vonage REST | Account SID / API キー | `rousseau sms --provider twilio --account-sid … --auth-token …` |

## 公開 HTTP 面がない理由

2 つの設計選択が、リストされたすべてのトランスポートを公開 Webhook から遠ざけます:

- **WebSocket ベースの受信。** Slack Socket Mode と Discord Gateway は、デーモンの視点からは送信専用です — デーモンは TLS でベンダーにダイヤルし、メッセージは同じ接続で到着します。
- **ポーリング。** WhatsApp、Telegram、Matrix、iMessage、Email は独自のケイデンスで更新を取得します。ベンダーが呼び出す Webhook はありません。

SMS は例外で、rousseau は SMS を **送信専用** にすることで解決します。受信 SMS には Twilio / Vonage の Webhook が必要ですが、それはこのプロジェクトが導入を拒む面そのものです。

## ルーターの動作

ルーター (`internal/transport/router.go`) はすべてのトランスポートと `Agent` の間にあります:

- **セッション分離。** 個別の `From` 値ごとに独自の `Session` が割り当てられるため、並行会話が相互汚染しません。WhatsApp の LID アイデンティティは、まず電話 JID に正規化されます (`internal/transport/whatsapp/resolve.go` を参照)。
- **許可リスト。** 受信をサポートするすべてのトランスポートは、設定に `Allowlist []string` を持ちます。空は「すべての送信者を受け入れる」を意味します — デーモンには常に少なくとも 1 エントリが必要です。
- **ディスパッチ。** ルーターはセッションごとにターンを直列化するため、ユーザーは同時に受信メッセージを 2 つ積み重ねることはできません。

## 10 番目のトランスポートを追加する

`transport.Transport` (3 つのメソッド) を実装します。`internal/config/` 配下でブロックレイアウトを反映した `Config` 型を追加します。`internal/cli/` に CLI コマンドを配線します。それが面のすべてです — エージェントコアは触れられません。

## トランスポート別のページ

- [WhatsApp](/ja/transports/whatsapp/)
- [Signal](/ja/transports/signal/)
- [Telegram](/ja/transports/telegram/)
- [Matrix](/ja/transports/matrix/)
- [Slack](/ja/transports/slack/)
- [Discord](/ja/transports/discord/)
- [iMessage](/ja/transports/imessage/)
- [Email](/ja/transports/email/)
- [SMS](/ja/transports/sms/)
