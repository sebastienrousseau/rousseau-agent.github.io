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
description: "End-to-end walkthrough for wiring your first chat transport. Uses WhatsApp as the canonical example: pair, allowlist, send a test message, verify the reply."
keywords: "first transport, whatsapp, pairing, allowlist, e2e walkthrough, test message"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/getting-started/first-transport/"
subtitle: "End-to-end WhatsApp walkthrough: pair, allowlist, verify."
tags: "first-transport, whatsapp, walkthrough"
title: "はじめてのトランスポート"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "first transport, whatsapp, pairing, allowlist, e2e walkthrough, test message"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "はじめてのトランスポート"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 25
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/getting-started/first-transport/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/first-transport/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "はじめてのトランスポート"
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
twitter_description: "End-to-end walkthrough for wiring your first chat transport. Uses WhatsApp as the canonical example: pair, allowlist, send a test message, verify the reply."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "はじめてのトランスポート"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">このページで学べること</span><p>rousseau デーモンとチャットトランスポートをペアリングし、それを駆動する JID / ユーザー ID を allowlist に追加し、最初のテストメッセージを送って返信を確認する方法を扱います。WhatsApp はペアリングが最も厳格なため正典のウォークスルーです。以下のタブに Slack と Discord の並列ウォークスルーがあります。</p></aside>

## はじめてのトランスポートを選ぶ

すべてのトランスポートは同じ `transport.Transport` インタフェースの薄いアダプタです。allowlist、セッションルーティング、cron 配信はどれでも同一です。違うのはペアリング UX とトランスポートごとの識別子フォーマット（JID、ユーザー ID、ルーム ID）です。最も早くペアリングできるものを選んでください。

<div class="tabs" data-tabs="first-transport">
  <div class="tab-list" role="tablist" aria-label="First transport">
    <button role="tab" aria-selected="true">WhatsApp</button>
    <button role="tab" aria-selected="false">Slack</button>
    <button role="tab" aria-selected="false">Discord</button>
    <button role="tab" aria-selected="false">Telegram</button>
    <button role="tab" aria-selected="false">Signal</button>
  </div>
  <div class="tab-panel" role="tabpanel">

WhatsApp はリファレンスです。ペアリングは最も難しく、テストは最も簡単です（スマートフォンにアプリが既に入っているため）。

**前提条件:** WhatsApp が入ったスマートフォン、E.164 JID（例: `447900123456@s.whatsapp.net`）。

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

**WhatsApp &gt; 設定 &gt; リンク済みデバイス &gt; デバイスをリンク** から QR をスキャンします。自分に `hello` を送ると、rousseau が WhatsApp 経由で返信します。完全なウォークスルーは以下を参照してください。

<aside class="admonition" data-type="warning"><span class="admonition-title">非公式プロトコル</span><p>WhatsApp サポートは <code>whatsmeow</code>（リバースエンジニアリングされたクライアント）を使います。Meta は非公式クライアントを実行する番号を時折 BAN します。頼りにしている番号では実行しないでください。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**前提条件:** Slack ワークスペースの管理者権限、[api.slack.com/apps](https://api.slack.com/apps) で作成したアプリ、Socket Mode 有効化。

1. Slack アプリを作成し、<em>設定 &gt; Socket Mode</em> で **Socket Mode** を有効化します。
2. `connections:write` を持つ **App-Level Token** を作成します。これが `xapp-…` トークンです。
3. <em>OAuth &amp; Permissions</em> でボットスコープ `chat:write`、`im:history`、`im:read`、`im:write`、`mpim:history`、`mpim:read` を追加します。ワークスペースにインストールして `xoxb-…` ボットトークンを取得します。
4. <em>Event Subscriptions</em> で `message.im`（DM）と、必要なチャンネルイベントを購読します。

```sh
rousseau slack --app-token xapp-... --bot-token xoxb-... --allow U01234567
```

Slack でボットに DM を送ると、rousseau が同じ DM で返信します。OAuth スコープの根拠を含む完全なウォークスルーは [トランスポート: Slack](/ja/transports/slack/) を参照してください。

<aside class="admonition" data-type="tip"><span class="admonition-title">公開 HTTP なし</span><p>Socket Mode ではデーモンが Slack の WebSocket に送信接続します。公開 webhook や ngrok、ingress は不要です。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**前提条件:** [discord.com/developers/applications](https://discord.com/developers/applications) の Discord アプリケーション、ボットユーザー、<em>Bot</em> 配下の **Message Content Intent** 有効化。

1. アプリケーションを作成し、ボットを追加し、ボットトークンをコピーします。
2. <em>Bot &gt; Privileged Gateway Intents</em> で **Message Content Intent** を有効化します。これがないとメッセージ本文が空で届きます。
3. <em>OAuth2 &gt; URL Generator</em> でボットを招待します。scope は `bot`、permissions は `Send Messages`、`Read Message History`。

```sh
rousseau discord --token <bot-token> --allow 234567890123456789
```

ボットに DM を送ると rousseau が返信します。権限と intent の詳細は [トランスポート: Discord](/ja/transports/discord/) を参照してください。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**前提条件:** [@BotFather](https://t.me/BotFather) の Telegram ボット。

1. `@BotFather` に `/newbot` と送信し、プロンプトに従います。トークンをコピーしてください。
2. Telegram がチャットを作成するよう、ボットに一度は話しかけます。

```sh
rousseau telegram --token 1234567890:AA... --allow 987654321
```

`--allow` の値は Telegram の数値ユーザー ID（ユーザー名ではありません）です。[@userinfobot](https://t.me/userinfobot) にメッセージを送ると取得できます。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**前提条件:** `signal-cli` がインストールされ、Signal アカウントにリンクされていること。ペアリング手順は [signal-cli ドキュメント](https://github.com/AsamK/signal-cli) を参照してください。

```sh
rousseau signal --account +447900123456 --allow +447900654321
```

Rousseau は `signal-cli` をサブプロセスとして起動し（`internal/cli/signal.go` を参照）、JSON-RPC 経由で通信します。[トランスポート: Signal](/ja/transports/signal/) を参照してください。

  </div>
</div>

## なぜ WhatsApp のウォークスルーか

このページの残りは WhatsApp を正典の例として使います。ここでパターンをつかめば、他のトランスポートはすべてバリエーションです（安定した ID を allowlist に追加し、ペアリング UX を一度実行し、テストを送り、返信を確認する）。すでにトークンを持っているなら、姉妹のトランスポートページへ飛んでください。

- [Slack](/ja/transports/slack/) — Socket Mode トークンとイベントサブスクリプション。
- [Discord](/ja/transports/discord/) — ボットトークン、intent、権限整数。
- [Telegram](/ja/transports/telegram/) — BotFather トークン。
- [Signal](/ja/transports/signal/) — signal-cli サブプロセス。
- [Matrix](/ja/transports/matrix/) — homeserver URL + アクセストークン。

## 前提条件

- `$PATH` 上の `rousseau`（[インストール](/ja/getting-started/installation/) を参照）。
- 動作するプロバイダ — `claudecli` が Claude Code の認証を継承するデフォルトです。それ以外はまずコンフィグを埋める必要があります（[設定](/ja/configuration/)）。
- WhatsApp をインストールしたスマートフォン。E.164 の電話 JID（例: `447900123456@s.whatsapp.net`）。

## ステップ 1 — デーモンを駆動する JID を選ぶ

Rousseau は allowlist を使って受信処理を固定の JID セットに制限します。それ以外の送信者は静かに破棄されます。これは荷重を支える部分です。allowlist なしだと、番号を知る誰もがエージェントを駆動できてしまいます。

E.164 JID は電話番号の数字のみに `@s.whatsapp.net` を続けたものです。

```
447900123456@s.whatsapp.net
```

グループ JID は `@g.us` で終わります。デーモンはそれもサポートしますが、まずは個人 JID から始めてください。

## ステップ 2 — 初回起動とペアリング

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

初回起動時、QR コードが stdout に出力されます。電話で WhatsApp を開き、**設定 → リンク済みデバイス → デバイスをリンク** から QR をスキャンしてください。

デーモンは次のような出力を出します。

```
whatsapp.starting store=file:/home/you/.local/share/rousseau/whatsapp.db?_pragma=... allowlist=1
```

スキャンすると、whatsmeow がデバイス認証情報を `whatsapp.db` に永続化します。以後の起動は静かに接続され、QR は表示されません。

## ステップ 3 — テストメッセージを送る

スマートフォンから自分に `hello` を送ります。デーモンは受信イベントをログに記録し、エージェントにディスパッチし、設定されたヘッダとともに WhatsApp 経由で返信を配信します。

```
💎 *Rousseau Agent*

Hello — what would you like to work on?
```

返信ヘッダは `whatsapp.reply_header` で設定できます。半角スペース 1 文字にすると接頭辞を無効化できます。

## ステップ 4 — 長いフラグを不要にするため `config.yaml` を用意する

`~/.config/rousseau/config.yaml` を作成します。

```yaml
provider: claudecli

claudecli:
  binary: claude
  permission_mode: bypassPermissions

whatsapp:
  reply_header: "💎 *Rousseau Agent*\n\n"
```

これで `rousseau whatsapp --allow 447900123456@s.whatsapp.net` は自動的にヘッダを読み取ります。すべてのトランスポートは同じファイルから自分のスタンザを読み込みます。全リストは [設定](/ja/configuration/) を参照してください。

`bypassPermissions` は無人稼働のデーモンでのデフォルトです。ターミナルの反対側で対話的にツール呼び出しを承認する人間がいないためです。重要なものにデーモンを向ける前に、**承認ポリシーを設定してください**（[ユーザーガイド: 承認ポリシー](/ja/user-guide/approval-policies/)）。

## ステップ 5 — エンドツーエンドを確認する

スマートフォンからコーディング質問を送ります。

```
Read the file at /workspace/README.md and summarise it in 3 bullets.
```

デーモンは `read` ツール呼び出しを実行し、ファイルをモデルに渡し、要約を返信します。これでループを閉じたことになります。

- 電話 → WhatsApp → whatsmeow WebSocket
- rousseau-agent → エージェントループ → ツール呼び出し → プロバイダ呼び出し
- 返信 → whatsmeow → WhatsApp → 電話

プロバイダ呼び出し以外は、あなたのネットワーク境界を越えていません。プロバイダがローカルの Claude Code 上の `claudecli` なら、プロバイダ呼び出しさえ越えていません。

## `rousseau doctor` での検証

```sh
rousseau doctor
```

WhatsApp 経路のすべてのチェックがカバーされます。

- `provider.claudecli.binary`、`provider.claudecli.version` — LLM 経路。
- `state.path`、`state.db_size`、`state.sessions` — SQLite セッションストア。
- `whatsapp.store`、`whatsapp.paired` — デバイス認証情報。
- `whatsapp.voice` — ボイスノート文字起こしの姿勢。

`fail` 行は致命的停止です。`warn` 行はロールアウト前に調査する価値があります。

## トラブルシューティング

### QR コードは表示されるが電話が拒否する

よくある原因は 3 つあります。第一に、途中で終わった過去のペアリングで `whatsapp.db` が whatsmeow が再利用できない状態のまま残っている場合。`~/.local/share/rousseau/whatsapp.db` を削除して再スキャンしてください。第二に、時計が 30 秒以上ズレている場合（NTP クライアントが動作しないコンテナでよくあります）。WhatsApp のハンドシェイクは時刻に敏感です。第三に、古い `whatsmeow` バージョンが Meta のプロトコル更新に追随していない場合。rousseau をアップグレードしてください。

### メッセージを送ったがデーモンが `router.transport.rejected` をログに残す

JID が allowlist と一致していません。`--allow` に渡す値は、WhatsApp がレポートするそのままの送信者 JID（`447900123456@s.whatsapp.net`、`+` なし、スペースなし）でなければなりません。セルフチャットのテストは、rousseau が LID プライバシーハッシュをアカウント自身の JID に置き換えるため動作します（`internal/transport/whatsapp/resolve.go` を参照）。

### QR コードが表示されず、デーモンが `no rows` で終了する

whatsmeow ストアが初期化されていません。親ディレクトリ（`~/.local/share/rousseau/`）が存在し、書き込み可能であることを確認してください。`rousseau doctor` はこれを `whatsapp.store` の下で報告します。

### Rousseau は返信するがモデル出力が空

`rousseau doctor` で `provider.claudecli.binary` と `provider.claudecli.version` を確認してください。空返信の最もよくある原因は、`claudecli` 呼び出しが `is_error: true` を返すことです。デーモンは切り詰められたエラーを `warn` レベルでログに記録します。サブプロセスを切り分けるため、プロバイダを `anthropic` または `bedrock` に切り替えてください。

### Slack / Discord: "invalid_auth" または "401 Unauthorized"

Slack では `xapp-…`（アプリトークン）と `xoxb-…`（ボットトークン）は別物です。取り違えると `invalid_auth` が出ます。Discord では <em>Bot &gt; Reset Token</em> に表示されるトークンは一度きりです。一度コピーして失くしたなら、再度リセットしなければなりません。

## 関連ページ

- [トランスポート](/ja/transports/) — 各トランスポート、ワイヤプロトコル、allowlist フォーマット。
- [ユーザーガイド: CLI](/ja/user-guide/cli/) — すべてのコマンドとフラグ。
- [ユーザーガイド: 承認ポリシー](/ja/user-guide/approval-policies/) — 主要な安全レバー。
- [デプロイ](/ja/deployment/) — フォアグラウンドの `rousseau whatsapp` から systemd ユニットへの引き渡し。
- [Voice モード](/ja/user-guide/voice-mode/) — WhatsApp のボイスノートをエージェントのターンに変換する。

## さらに読む

- `internal/transport/whatsapp/client.go` — 接続、QR、イベントポンプ。
- `internal/transport/whatsapp/resolve.go` — LID/JID 正規化とセルフチャット処理。
- `internal/cli/whatsapp.go` — CLI 配線、ストア DSN、文字起こしツール選択。
- `internal/cli/slack.go`、`internal/cli/discord.go` — 姉妹トランスポート CLI。
- `internal/transport/router.go` — allowlist 強制。
