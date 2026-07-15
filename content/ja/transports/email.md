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
description: "Set up rousseau-agent's email transport: IMAP inbound polling, SMTP submission, both over full TLS, PlainAuth on 587, UTF-8 RFC 5322 output."
keywords: "email, IMAP, SMTP, TLS, PlainAuth, INBOX, poll interval, RFC 5322, UTF-8"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/transports/email/"
subtitle: "IMAP inbound plus SMTP outbound over TLS."
tags: "transports, email"
title: "Email トランスポート"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "email, IMAP, SMTP, TLS, PlainAuth, INBOX, poll interval, RFC 5322, UTF-8"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Email トランスポート"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 20
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/transports/email/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/email/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Email トランスポート"
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
twitter_description: "Set up rousseau-agent's email transport: IMAP inbound polling, SMTP submission, both over full TLS, PlainAuth on 587, UTF-8 RFC 5322 output."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Email トランスポート"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">このページで学べること</span><p>Gmail アプリパスワードのウォークスルー、Fastmail / Google Workspace / セルフホストメールサーバー向けのトランスポート設定、STARTTLS のみのサーバーからの移行経路、プレーンと HTML のレンダリングトレードオフを扱います。このページと並行して <code>internal/transport/email/client.go</code> を読んでください。</p></aside>

## 概要

email トランスポート（`internal/transport/email/`）はペアです: **IMAP 受信**（`github.com/emersion/go-imap/v2` 経由）と **SMTP 送信**（Go 標準ライブラリの `net/smtp` 経由）。

INBOX を `UNSEEN` メッセージについてポーリングし、ハンドラへの引き渡し後に `SEEN` フラグを立て、`net/smtp.SendMail` 経由で返信します。

## TLS 姿勢

**両端が完全 TLS です。** トランスポートは IMAP 側で `imapclient.DialTLS`、SMTP 側で `PlainAuth` を用いた `smtp.SendMail` を既に TLS ラップされた接続上で使用します。STARTTLS のみの IMAP や SMTP サーバーは **現状サポートされていません**。デーモンは暗号化されていないソケット上でプレーンテキストの認証情報を送信することを拒否します。

標準 TLS ポート:

- IMAP: `993`
- SMTP submission: `465`（implicit TLS） — 完全 TLS。**プロバイダが 587 でも implicit TLS を行うのでない限り、`587` ではありません。**

一部のプロバイダ（Google Workspace、Fastmail）は `465` での implicit TLS による SMTP submission を受け入れます。設定前にプロバイダを確認してください。

## 設定

```yaml
email:
  imap_addr: "imap.example.com:993"
  imap_username: "bot@example.com"
  imap_password: "..."
  mailbox: "INBOX"
  poll_interval: "30s"

  smtp_addr: "smtp.example.com:465"
  smtp_username: "bot@example.com"
  smtp_password: "..."

  from: "bot@example.com"
  reply_header: ""
```

| フィールド | デフォルト | 効果 |
|---|---|---|
| `imap_addr` | *必須* | TLS IMAP 用の `host:port`。 |
| `imap_username` | *必須* | IMAP ユーザー名。 |
| `imap_password` | *必須* | IMAP パスワード。 |
| `mailbox` | `INBOX` | ポーリング対象のメールボックス。 |
| `poll_interval` | `30s` | UNSEEN メールを確認する頻度。 |
| `smtp_addr` | *必須* | SMTP submission 用の `host:port`。 |
| `smtp_username` | *必須* | SMTP ユーザー名。 |
| `smtp_password` | *必須* | SMTP パスワード。 |
| `from` | *必須* | エンベロープおよびヘッダの `From` アドレス。 |
| `reply_header` | *空* | 送信メッセージ本文の先頭に付加されます。 |

## コマンドライン

```sh
rousseau email \
  --imap-addr imap.example.com:993 \
  --imap-username bot@example.com \
  --imap-password ... \
  --smtp-addr smtp.example.com:465 \
  --smtp-username bot@example.com \
  --smtp-password ... \
  --from bot@example.com
```

## 送信メッセージの形状

返信は RFC 5322 準拠です。rousseau は次を書き込みます。

```
From: bot@example.com
To: sender@example.com
Subject: Re: <inbound subject>
Content-Type: text/plain; charset=utf-8
MIME-Version: 1.0

<reply_header><body>
```

UTF-8 は無条件です。HTML 出力はスコープ外です。テンプレートエンジンは配線されていません。

## 受信メッセージの形状

`UNSEEN` メッセージは次を持つ `IncomingMessage` にパースされます。

- `From` = パースされた `From` ヘッダアドレス。
- `Body` = 連結された `text/plain` パート。
- `At` = IMAP からの `INTERNALDATE`。

添付ファイル、`text/html`、インライン画像は無視されます。

## メールボックスの選択

`mailbox: "INBOX"` がデフォルトです。細かいフィルタリング用に Gmail ラベル（`"[Gmail]/label"`）や Fastmail フォルダを指すこともできます。IMAP サーバーが公開するものは何でも使えます。

## プロバイダ固有のセットアップ

<div class="tabs" data-tabs="email-provider">
  <div class="tab-list" role="tablist" aria-label="Email provider">
    <button role="tab" aria-selected="true">Gmail / Workspace</button>
    <button role="tab" aria-selected="false">Fastmail</button>
    <button role="tab" aria-selected="false">Outlook / M365</button>
    <button role="tab" aria-selected="false">Self-hosted</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**Gmail アプリパスワードのウォークスルー。** 通常の Gmail パスワードは、2FA が有効な状態では IMAP/SMTP 経由での認証に使えません。アプリパスワードを生成します。

1. https://myaccount.google.com/security にアクセス。**2 段階認証プロセス** が有効か確認します。
2. **アプリ パスワード** をクリック（2FA 有効時のみ表示）。
3. アプリ名を "rousseau-agent" として生成。16 文字のパスワードをコピーします（スペースは任意）。

コンフィグ:

```yaml
email:
  imap_addr: imap.gmail.com:993
  imap_username: your.address@gmail.com
  imap_password: "aaaa bbbb cccc dddd"

  smtp_addr: smtp.gmail.com:465
  smtp_username: your.address@gmail.com
  smtp_password: "aaaa bbbb cccc dddd"

  from: your.address@gmail.com
```

<aside class="admonition" data-type="warning"><span class="admonition-title">Google Workspace の管理者ロック</span><p>一部の Workspace 管理者は組織全体でアプリパスワードを無効化しています。セキュリティページに <em>アプリ パスワード</em> がない場合、「安全性の低いアプリのアクセス」を許可するか OAuth を設定するよう管理者に依頼してください。rousseau はまだ Gmail OAuth をサポートしていません（ロードマップ）。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Fastmail は *Settings &gt; Password &amp; Security &gt; App passwords* でアプリパスワードをサポートします。*Mail (IMAP/POP/SMTP)* にスコープしたパスワードを作成してください。

```yaml
email:
  imap_addr: imap.fastmail.com:993
  imap_username: your.address@fastmail.com
  imap_password: "..."

  smtp_addr: smtp.fastmail.com:465
  smtp_username: your.address@fastmail.com
  smtp_password: "..."

  from: your.address@fastmail.com
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Microsoft 365 は多くのテナントで基本認証（ユーザー名 + パスワード）を非推奨としています。Rousseau はまだ Modern Auth / OAuth をサポートしていません（ロードマップ）。オプション:

1. M365 管理センターでメールボックスごとに *Authenticated SMTP* を有効化する（一部テナントで可能）。
2. リレーを使う: セルフホストの IMAP+SMTP に対して rousseau を実行し、それがアプリパスワードを持つ SMTP で M365 に転送する。
3. OAuth サポートの実装を待つ。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

993 で TLS 上の IMAP、465 で implicit TLS 上の SMTP submission を話すセルフホストメールサーバーはそのまま動作します。ポート 465 で `smtpd_tls_wrappermode=yes` の Postfix + Dovecot は古典的なセットアップです。

```yaml
email:
  imap_addr: mail.internal:993
  imap_username: rousseau
  imap_password: "..."

  smtp_addr: mail.internal:465
  smtp_username: rousseau
  smtp_password: "..."

  from: rousseau@internal
```

サーバーが STARTTLS のみ（ポート 587 SMTP submission）の場合、rousseau は認証を拒否します。トランスポートはプレーンテキストの認証情報を送信しません。以下の移行セクションを参照してください。

  </div>
</div>

## STARTTLS のみのサーバーからの移行

Rousseau は IMAP（993）と SMTP（465）の両方で implicit TLS を使用します。既存のメールインフラが 143（IMAP）や 587（SMTP submission）で STARTTLS しか提供しない場合、選択肢は 3 つあります。

1. **サーバーで implicit TLS を有効化する。** Postfix はポート 465 にバインドした `smtpd_tls_wrappermode=yes` をサポートします。Dovecot はポート 993 の `imaps` サービスをそのままサポートします。
2. **TLS 終端プロキシでサーバーの前段に立てる。** `stunnel` は 465 で implicit TLS を受け、587 で STARTTLS として転送できます。
3. **STARTTLS サポートを待つ。** ロードマップアイテム。`docs/GAP_ANALYSIS_2026.md` を参照してください。

## プレーン vs HTML レンダリング

送信は `text/plain; charset=utf-8` です。HTML テンプレートはありません。これは意図的です。プレーンテキストは普遍的にレンダリングされ、トラッキングピクセルを埋め込まず、テキストのみのメールクライアントで壊れることがありません。HTML 出力が欲しい場合、トランスポートをラップして `SendMail` を書き換えてください。

```go
// Custom transport that emits multipart/alternative.
type MyEmailClient struct{ email.Client }

func (c *MyEmailClient) Deliver(ctx context.Context, to, body string) error {
    html := markdown.ToHTML([]byte(body), nil, nil)
    // ... construct multipart/alternative message, call net/smtp.SendMail ...
}
```

Rousseau のコアはプレーンテキストのままです。HTML は呼び出し側の懸念です。

## 失敗モード

| 症状 | 修正 |
|---|---|
| `imapclient.DialTLS` エラー | ポート 993 の送信が開いていること、TLS 証明書が有効であることを確認してください。 |
| `SMTP AUTH failed` | `PlainAuth` は認証サーバーのホスト名が `smtp_addr` と一致することを要求します。ロードバランサ付きのプロバイダは別名を提示することがあります。 |
| メッセージに SEEN フラグが立たない | ハンドラがエラーを返しました。根本原因を修正してください。rousseau は無限にリトライしません。 |
| 返信が重複する | 同じメールボックスに 2 つの rousseau インスタンスが動作しています。1 つだけ動かしてください。 |
| `AUTHENTICATE failed: Application-specific password required` | 2FA 有効の Gmail でアプリパスワードではなくアカウントパスワードを使用しました。上記の Gmail ウォークスルーを参照してください。 |

## トラブルシューティング

### `dial tcp: connect: connection refused`

ポートが誤っています。`imap_addr` が `:993`（`:143` ではない）を、`smtp_addr` が `:465`（STARTTLS のみのサーバー向けの `:587` ではない）を使っていることを確認してください。

### ボットがスパムに返信する

INBOX 内の `UNSEEN` メッセージはすべて処理されます。メールボックスレベルでスパムをフィルタする（サーバー側ルール、Gmail スパムフィルタ）か、INBOX 以外の `mailbox:` を設定し、サーバー側ルールでそこにメールを振り分けてください。

### `SendMail` は成功するがメッセージが届かない

SMTP サーバーのメールログを確認してください。よくある原因: DKIM 署名失敗（`From:` ドメインがサーバーの署名可能なドメインと一致しない）、逆引き DNS 不一致、受信ドメインの SPF が IP をブロックしている。

### メッセージ本文の Unicode が `?????` としてレンダリングされる

経路のどこかで UTF-8 が剥がれています。送信メッセージに `Content-Type: text/plain; charset=utf-8` があること（rousseau は常に設定します）、リレーが transcoding していないことを確認してください。

### コンフィグ変更後もポーリング間隔が変わらない

`poll_interval` はデーモン起動時にのみ読み直されます。新しい値を反映するには再起動してください。

## 関連ページ

- [はじめに: はじめてのトランスポート](/ja/getting-started/first-transport/) — エンドツーエンドのウォークスルー。
- [設定](/ja/configuration/) — `email` コンフィグブロック。
- [トランスポート](/ja/transports/) — 姉妹トランスポート。
- [デプロイ](/ja/deployment/) — Podman コンテナでの Email 運用。
- [Cron](/ja/cron/) — email 経由で定期ダイジェストを送信。

## さらに読む

- `internal/transport/email/client.go` — IMAP ポーリング、SMTP 送信、メッセージパース。
- `internal/cli/email.go` — CLI 配線。
- `internal/config/config.go` — `EmailConfig` 構造体。
- [emersion/go-imap ドキュメント](https://github.com/emersion/go-imap) — IMAP ライブラリ。
