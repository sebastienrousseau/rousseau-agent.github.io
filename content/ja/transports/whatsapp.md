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
description: "Set up rousseau-agent's WhatsApp transport: QR pairing, E.164 allowlist, LID vs phone-JID normalisation, voice-note transcription with whisper.cpp."
keywords: "WhatsApp, whatsmeow, QR pairing, JID, LID, allowlist, voice notes, whisper, transcription"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/transports/whatsapp/"
subtitle: "Whatsmeow-backed WhatsApp bridge with QR pairing."
tags: "transports, WhatsApp"
title: "WhatsApp トランスポート"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "WhatsApp, whatsmeow, QR pairing, JID, LID, allowlist, voice notes, whisper, transcription"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "WhatsApp トランスポート"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 12
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/transports/whatsapp/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/whatsapp/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "WhatsApp トランスポート"
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
twitter_description: "Set up rousseau-agent's WhatsApp transport: QR pairing, E.164 allowlist, LID vs phone-JID normalisation, voice-note transcription with whisper.cpp."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "WhatsApp トランスポート"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">このページで学べること</span><p>WhatsApp トランスポートがスマートフォンとどうペアリングするか、LID と電話 JID の正規化ルール、ボイスノート文字起こしフロー、メディアダウンロード、allowlist の正規表現パターン、初回オペレーターがつまずく失敗モードを扱います。このページと並行して <code>internal/transport/whatsapp/client.go</code>、<code>resolve.go</code>、<code>dispatch.go</code> を読んでください。</p></aside>

## 概要

WhatsApp トランスポート（`internal/transport/whatsapp/`）は `go.mau.fi/whatsmeow`（リバースエンジニアリングされた WhatsApp Web マルチデバイスクライアント）に基づいています。Meta はこれを非公式クライアントとみなしています。重要な用途に頼っている個人番号では実行しないでください。

Signal プロトコルのエンドツーエンド暗号化は維持されます（whatsmeow は WhatsApp モバイルアプリと同じプロトコルを使用します）。デーモンはデバイス認証情報をセッションストアと別の SQLite ファイルに保持するため、デバイスの再リンクは会話履歴に触れません。

<aside class="admonition" data-type="caution"><span class="admonition-title">非公式プロトコル</span><p>Meta は非公式クライアントを実行する番号を時折 BAN します。WhatsApp のレート制限を守り責任ある挙動を取っていても、<code>whatsmeow</code> で使う電話番号は予告なく BAN されることがあります。個人番号ではなく専用番号を使ってください。</p></aside>

## ペアリング

初回起動:

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

QR コードが `mdp/qrterminal/v3` 経由で stdout に出力されます。WhatsApp 電話アプリ（**設定 → リンク済みデバイス → デバイスをリンク**）でスキャンしてください。ペアリング状態は状態ディレクトリ配下の `whatsapp.db`（通常は `~/.local/share/rousseau/whatsapp.db`）に書き込まれます。

以降の起動はペアリング済みデバイスを静かに再利用します。QR が再表示される場合、電話側からペアリングが取り消されています。`whatsapp.db` を削除して再度ペアリングしてください。

## allowlist

`--allow` は受信処理を制限します。複数フラグは累積されます。

```sh
rousseau whatsapp \
  --allow 447900123456@s.whatsapp.net \
  --allow 442071234567@s.whatsapp.net
```

値は WhatsApp の **JID** です。E.164 電話番号（`+` なし）に `@s.whatsapp.net` を続けたものです。グループ JID（`<id>@g.us`）もサポートされます。

空の allowlist はすべての送信者を受け入れます。チャットトランスポートデーモンでは、常に少なくとも 1 エントリを設定してください。

## LID と電話 JID の正規化

WhatsApp はユーザーに 2 つの識別子フォーマットを使用します。

| フォーマット | 例 | 意味 |
|---|---|---|
| 電話 JID | `447900123456@s.whatsapp.net` | E.164 電話番号（`+` なし）に `@s.whatsapp.net` を続けたもの。時間を越えて安定するが、電話番号を漏らす。 |
| LID | `1234567890@lid` | Location-Independent ID。電話番号を明かさないランダムに見える文字列。安定しているが、直接番号にリンクできない。 |
| デバイスサフィックス | `447900123456:5@s.whatsapp.net` | 任意の JID はデバイスアドレスサフィックス（`:N`）を持てます。WhatsApp は送信元の特定デバイスと共にメッセージをレポートします。 |

Rousseau の受信ハンドラ（`internal/transport/whatsapp/resolve.go` の `ResolveInbound`）は、ディスパッチ前にすべてのイベントを正規形に正規化します。

1. **デバイスサフィックスを除去。** `447900:5@s.whatsapp.net` は `447900@s.whatsapp.net` になります。これにより、リンクされたどのデバイスから送られたメッセージでも、bare なユーザー JID として書かれた allowlist が一致します。
2. **セルフチャットではアカウント所有者の電話 JID に LID を置き換える。** アカウント所有者が送信者の場合（`IsFromMe=true`）、WhatsApp は送信者を電話 JID ではなくアカウントの LID（プライバシーハッシュ）としてレポートします。Rousseau はアカウント自身の JID に置き換えるため、オペレーターは `<phone>@s.whatsapp.net` を allowlist に入れれば、セルフチャットのテストが正しくルーティングされます。
3. **パース不能な送信者は破棄する。** 空の `User` や `Server` フィールド（`FuzzResolveInbound` で発見されたもの）は安全にルーティングできません。不正な From としてハンドラに渡すのではなく、静かにメッセージをスキップします。

### セルフチャットの落とし穴

WhatsApp で自分にメッセージを送る（ボットをテストするため）場合、送信者フィールドは LID として届きます。電話 JID を allowlist に入れていると、素朴なルックアップは失敗します。Rousseau の置換 — `if evt.Info.IsFromMe && ownID != nil { from = ownID.ToNonAD() }` — がこれを修正します。

### ループ防止

`IsFromMe=true` は、*このリンクされた* デバイスから送信されたメッセージ（rousseau の送信返信がエコーバックしたもの）にも発火します。トランスポートはデバイス ID が一致する場合それらを破棄します。

```go
if evt.Info.IsFromMe && ownID != nil && evt.Info.Sender.Device == ownID.Device {
    return Resolved{Skip: SkipOwnDevice}
}
```

アカウントの *他の* リンクされたデバイス（例えば「自分にメッセージ」をテストするプライマリの電話）からのメッセージは `IsFromMe=true` を持つが異なるデバイス ID を持ちます。これらは通常通り処理されます。

## allowlist 正規表現パターン

`--allow` フラグは正規表現ではなく厳密な文字列を取ります。rousseau は `router.go` で大文字小文字を無視する等価チェックを行います。パターンマッチングが欲しい場合、（承認ポリシーと同じ）`pattern` モードのコンフィグファイルを使ってください。

```yaml
whatsapp:
  allowlist:
    - "447900123456@s.whatsapp.net"
    - "447900654321@s.whatsapp.net"
```

グループ（`<hash>@g.us`）も同様に追加してください。ある国コードのすべての送信者を許可するには、カスタム `Router.Allow` 実装が必要です。組み込みエンフォーサは設計上、プレフィックスマッチングを行いません。

<aside class="admonition" data-type="warning"><span class="admonition-title">空の allowlist</span><p>空の allowlist はすべての送信者を受け入れます。公開番号で allowlist なしのチャットトランスポートを実行しないでください。番号を知る誰もがエージェントのオペレーターになります。</p></aside>

## 返信ヘッダ

送信メッセージには、送信者がどのボットと話しているか分かるようヘッダが接頭辞として付きます。デフォルト:

```
💎 *Rousseau Agent*

<message body>
```

WhatsApp は `*text*` を太字としてレンダリングします。コンフィグで上書き:

```yaml
whatsapp:
  reply_header: "🤖 *Coding bot*\n\n"
```

半角スペース 1 文字 `" "` にすると接頭辞を完全に無効化できます。

## ボイスノート文字起こし

オペレーターがオプトインした場合、受信ボイスノートは `whisper.cpp` で文字起こしされます。`whisper` CLI のインストールが必要なため、デフォルトではオフです。

```yaml
whatsapp:
  voice:
    enabled: true
    binary: whisper
    model: base.en
    language: en
    extra_args:
      - --threads
      - "4"
```

| フィールド | 効果 |
|---|---|
| `enabled` | オン/オフ切替。オフの場合、音声メッセージはログに記録されスキップされます。 |
| `binary` | Whisper CLI 実行ファイル。空の場合デフォルトは `whisper`。 |
| `model` | `--model` に渡されます（`base.en`、`small`、`medium`）。 |
| `model_path` | 明示的な `.bin` パス。`model` より優先されます。 |
| `language` | `--language` に渡されます。空の場合は自動検出。 |
| `extra_args` | 各呼び出しに追加されます。 |

文字起こしされたテキストは、ユーザーがタイプしたかのようにエージェントに渡されます。

## コンテナデプロイ

リファレンスの Podman Quadlet ユニット（`docker/rousseau-agent.container`）は、ペアリングが再起動を越えて残るよう、状態ディレクトリを読み書き可能でマウントします。

```
Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
```

`Network=pasta` はコンテナにルートレスな egress 専用スタックを提供します。Whatsmeow は昇格した capability を必要とせず、`DropCapability=all` は安全です。

## ボイスノート文字起こしフロー

ボイスノートが到着すると、標準リゾルバは `SkipEmptyText`（テキスト内容なし）を返します。`Dispatch` は音声メッセージについてこれを特別に検知し、`Transcriber` が設定されていれば次の経路を進みます。

```
Inbound audio message
  │
  ├── Downloader.Download(ctx, audioMsg)
  │     • bytes []byte, mimetype string, err error
  │     • Logs whatsapp.audio_downloaded on success
  │
  ├── Transcriber.Transcribe(ctx, audio, mimetype)
  │     • Returns plain-text transcription
  │     • Logs whatsapp.transcribed with duration
  │
  └── Re-enter handleTextMessage with the transcription as `Body`
```

文字起こしツールが設定されていない場合、デーモンは `whatsapp.audio_ignored reason=transcriber_not_configured` をログに記録しメッセージを破棄します。ボイスノートは決して「無音」返信を引き起こしません。空の受信は空の送信を生じます。

## メディアダウンロード

`Downloader` インタフェースは意図的に小さく保たれています。

```go
type Downloader interface {
    Download(ctx context.Context, msg DownloadableAudio) (bytes []byte, mimetype string, err error)
}
```

現在は音声ダウンロードのみ配線されています。画像と動画のダウンロードはロードマップにあります。これらは `waProto.ImageMessage` / `VideoMessage` として届き、対応する `DownloadableMedia` インタフェースが必要になります。プランについては [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md) を追跡してください。

## 入力中インジケータ

ハンドラは各返信を `SendPresence(Composing, Paused)` 呼び出しでラップし、モデルが考えている間、送信者に「…入力中」インジケータが見えるようにします。両呼び出しには 5 秒のタイムアウトがあり best-effort です。プレゼンス失敗は返信自体をブロックしません。

## 失敗モード

| 症状 | 修正 |
|---|---|
| 起動のたびに QR が再表示される | 電話側でペアリングが取り消されています。`whatsapp.db` を削除して再ペアリング。 |
| WhatsApp の再接続ループ | `pool.ntp.org` に対する時計ズレを確認。whatsmeow のハンドシェイクは時刻に敏感です。 |
| 受信メッセージが無視される | 送信者が `--allow` リストにあることを確認。ログで `router.transport.rejected` を確認。 |
| Meta に番号を BAN される | 個人番号では実行しないでください。プロトコルは非公式です。 |
| セルフチャットの "hello" がルーティングされない | セルフチャットは LID を使います。rousseau は allowlist マッチのため電話 JID に置き換えます。`ownID` が初期化されているか確認してください。初期化されるとデーモンは `whatsapp.connected` をログに記録します。 |
| ボイスノートが静かに破棄される | `whatsapp.voice.enabled: false` か `whisper` バイナリが欠けています。ログ行: `whatsapp.audio_ignored`。 |
| すべての返信が 2 回返ってくる | ループ防止がオフです。最近のビルドを実行していることを確認してください。修正は whatsmeow マルチデバイス展開初期に `ResolveInbound` に取り込まれました。 |

## トラブルシューティング

### QR は出力されるが電話アプリが拒否する

よくある原因 3 つ: (1) 途中で終わった過去のペアリングで `whatsapp.db` が whatsmeow が再利用できない状態のまま残っている場合 — ファイルを削除して再スキャン、(2) 時計が 30 秒以上ずれている場合（NTP のないコンテナでよくあります） — `timedatectl status` で確認、(3) 古い `whatsmeow` バージョンが Meta のプロトコル更新に追随していない場合。

### `whatsapp.connected` から `whatsapp.disconnected` へのループ

時計ズレか、Meta がペアリングを無効化しました。ログで `whatsapp.logged_out` イベントを確認してください。それが決定的なシグナルです。

### ボイスノートは届くが文字起こしされない

文字起こしバイナリが解決できません。`whatsapp.voice.binary` と `whatsapp.voice.model_path` を確認してください。両方とも実際のファイルを指す必要があります（または `binary` が `PATH` になければなりません）。

### allowlist の正規表現が一致しない

Rousseau の allowlist は正規表現ではなく厳密な文字列です。送信者範囲にマッチさせるには、各々を明示的にリスト化するか、カスタムルーターを追加してください。

### 返信ヘッダがリテラルの `*` 文字として表示される

受信者のクライアントが WhatsApp Markdown をレンダリングしていません。これはクライアント側のレンダリング問題です。受信者が古いクライアントを使っている場合はプレーンテキストを使ってください。

## 関連ページ

- [はじめに: はじめてのトランスポート](/ja/getting-started/first-transport/) — エンドツーエンドのウォークスルー。
- [ユーザーガイド: Voice モード](/ja/user-guide/voice-mode/) — ボイスノートの詳細。
- [設定](/ja/configuration/) — `whatsapp` コンフィグブロック。
- [トランスポート](/ja/transports/) — 他の 8 つのトランスポート。
- [デプロイ](/ja/deployment/) — Podman コンテナでの WhatsApp 運用。

## さらに読む

- `internal/transport/whatsapp/client.go` — 接続、QR ペアリング、イベントポンプ。
- `internal/transport/whatsapp/resolve.go` — LID/JID 正規化とセルフチャット処理。
- `internal/transport/whatsapp/dispatch.go` — ボイスノート分岐付きの受信メッセージディスパッチ。
- `internal/transport/whatsapp/whisper.go` — リファレンス whisper-cpp 文字起こしツール。
- `internal/cli/whatsapp.go` — CLI 配線、ストア DSN、文字起こしツール選択。
