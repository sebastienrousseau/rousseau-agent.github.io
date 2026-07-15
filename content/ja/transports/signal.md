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
description: "Set up rousseau-agent's Signal transport: signal-cli subprocess in JSON-RPC mode, account registration out-of-band, E.164 allowlist, extra_args knob."
keywords: "Signal, signal-cli, JSON-RPC, subprocess, E.164, account registration, linked device"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/transports/signal/"
subtitle: "signal-cli subprocess in JSON-RPC daemon mode."
tags: "transports, Signal"
title: "Signal トランスポート"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Signal, signal-cli, JSON-RPC, subprocess, E.164, account registration, linked device"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Signal トランスポート"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 13
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/transports/signal/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/signal/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Signal トランスポート"
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
twitter_description: "Set up rousseau-agent's Signal transport: signal-cli subprocess in JSON-RPC mode, account registration out-of-band, E.164 allowlist, extra_args knob."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Signal トランスポート"
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

Signal トランスポート (`internal/transport/signal/`) は、`signal-cli` (https://github.com/AsamK/signal-cli) を JSON-RPC デーモンモードでサブプロセスとして起動します。

`signal-cli --output=json -a <account> jsonRpc` は、stdin/stdout 上で JSON-RPC 2.0 をストリーミングします。送信の `send` リクエストがメッセージを配信し、着信は `receive` 通知として到着します。

## 前提条件

rousseau が Signal と通信するには、次の 2 つが揃っている必要があります。

1. **`signal-cli` が `$PATH` 上にある** (もしくはコンフィグで `binary` を明示的に設定)。
2. **アカウントが帯域外で登録またはリンクされている。**

アカウント登録は意図的に rousseau のスコープ外です。`signal-cli` のドキュメントに従って、2 つの経路がサポートされます。

- **新しい番号を登録。** `signal-cli register` は SMS または音声による検証を開始します。`signal-cli verify <code>` で完了します。番号はデーモンが所有する形になります。
- **セカンダリデバイスとしてリンク。** `signal-cli link` は `tsdevice://` URI を出力します。モバイル版 Signal アプリの **設定 → リンク済みデバイス** でスキャンしてください。番号は電話が所有したままとなり、デーモンはセカンダリとして動作します。

どちらのフローも、状態を `~/.local/share/signal-cli/` に永続化します。Podman でデプロイする場合は、そこをコンテナにバインドマウントしてください。

## コンフィグ

```yaml
signal:
  binary: signal-cli
  account: "+447900123456"
  extra_args:
    - --verbose
  reply_header: "*Rousseau Agent*\n\n"
  allowlist:
    - "+447900654321"
```

| フィールド | デフォルト | 効果 |
|---|---|---|
| `binary` | `signal-cli` | 起動する実行ファイル。 |
| `account` | *必須* | デーモンが動作する E.164 電話番号。 |
| `extra_args` | `[]` | `-a <account>` と `jsonRpc` の間に挿入されます。`--config <path>` や `--verbose` に便利です。 |
| `reply_header` | *空* | 送信するすべての返信の先頭に追加されます。 |
| `allowlist` | `[]` | メッセージを処理する E.164 番号。空の場合はすべての送信者を受け入れます。 |

## コマンドライン

```sh
rousseau signal --account +447900123456 --allow +447900654321
```

フラグはコンフィグブロックと対応しています。`--allow` は複数回指定できます。

## メッセージフロー

- **受信。** `signal-cli` は到着したメッセージごとに `receive` JSON-RPC 通知を発行します。rousseau はそれをパースし、allowlist にないものを破棄し、本文を `Handler` に渡します。
- **送信。** rousseau は `signal-cli` の stdin に JSON-RPC `send` リクエストを書き込みます。配信 ACK は同じチャネルで届きます。

## タイムアウト

トランスポートはサブプロセスに対して独自のタイムアウトを課しません。`signal-cli` 自身のネットワークレイヤーが Signal サーバーへの再接続を処理します。プロセスが終了しても、rousseau はそれを再起動しません。systemd の `Restart=on-failure` (リファレンスの Quadlet がすでに設定しています) が rousseau デーモン全体を再起動し、それに伴って `signal-cli` も再起動されます。

## 障害モード

| 症状 | 対処 |
|---|---|
| `signal-cli` が即座に終了する | アカウントが登録もリンクもされていません。帯域外で登録を完了してください。 |
| `receive` 通知が届かない | キューを消費している別の場所でアカウントがリンクされていないか確認してください。 |
| JSON のパースエラー | `signal-cli` のバージョンが 0.13 以上であることを確認してください。旧バージョンは異なるエンベロープを使用していました。 |
