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
changefreq: "weekly"
description: "rousseau-agent's cron scheduler runs stored jobs on a schedule and delivers replies through any registered transport. Backed by robfig/cron/v3 and SQLite job persistence."
keywords: "cron, robfig/cron, scheduler, scheduled jobs, delivery, transport-agnostic, SQLite persistence"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/cron/"
subtitle: "任意のトランスポートで発火する永続スケジュールジョブ。"
tags: "cron, scheduler, reference"
title: "cron スケジューラ"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, robfig/cron, scheduler, scheduled jobs, delivery, transport-agnostic, SQLite persistence"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "cron スケジューラ"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 24
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/cron/index.html"
item_link: "https://docs.rousseau-agent.dev/cron/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "cron スケジューラ"
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
twitter_description: "rousseau-agent's cron scheduler runs stored jobs on a schedule and delivers replies through any registered transport. Backed by robfig/cron/v3 and SQLite job persistence."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "cron スケジューラ"
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

cron スケジューラ (`internal/cron/scheduler.go`) は、保存された `CronJob` エントリを設定されたスケジュールで実行し、各ジョブのプロンプトをエージェント経由で実行し、応答をトランスポート非依存の `Delivery` 関数に渡すゴルーチンです。

スケジューラは長時間稼働するデーモン (通常は `rousseau whatsapp` または他のチャットトランスポート) と並行して動作します。ジョブはセッションと同じ SQLite データベースに保存されるため、再起動をまたいで残ります。

## スケジュール構文

[robfig/cron/v3](https://pkg.go.dev/github.com/robfig/cron/v3) が背後にあります。パーサーは次をサポートします。

- 標準の 5 フィールド cron: `<minute> <hour> <day-of-month> <month> <day-of-week>`。
- 定義済みのショートカット: `@yearly`、`@monthly`、`@weekly`、`@daily`、`@hourly`、`@every <duration>`。

スケジュールの例:

| 式 | 発火 |
|---|---|
| `0 9 * * 1-5` | 平日 09:00 |
| `*/15 * * * *` | 15 分ごと |
| `@daily` | 毎日 0 時 (サーバータイムゾーン) |
| `@every 30m` | 30 分ごと |

## CLI

```sh
# 保存済みジョブをすべて一覧表示。
rousseau cron list

# ジョブを追加。
rousseau cron add \
  --name morning-standup \
  --schedule '0 9 * * 1-5' \
  --prompt 'What are the top three engineering priorities today?' \
  --target '447900123456@s.whatsapp.net'

# 名前または ID で削除。
rousseau cron remove morning-standup
```

## コンフィグ

ジョブは設定ファイルではなく、ステート DB に保存されます。`~/.config/rousseau/config.yaml` にスケジューラ自体を設定する項目はありません。デフォルトの `PollInterval = 60s` を使用します。

## ジョブフロー

1. スケジューラは `PollInterval` ごとに SQLite からジョブリストを再同期します。
2. `robfig/cron/v3` がスケジュールされた時刻にジョブを発火させます。
3. `TurnRunner.RunOnce(ctx, job.Prompt)` は、新規セッションに対して **シングルターン** のエージェント実行を行います (履歴なし、ランナーがオプトインしない限りセッション横断のリコールもなし)。
4. 応答テキストは `Delivery(ctx, job.Target, replyText)` に渡されます。
5. `Delivery` がエラーを返した場合 → ログに記録され、次のティックでリトライされます。

## 配信

`Delivery` は小さな関数型です。

```go
type Delivery func(ctx context.Context, target, body string) error
```

スケジューラは `internal/transport` をインポートしません。配信コントラクトはトランスポート非依存です。実際には、`rousseau <transport>` デーモンが、target 文字列をアクティブなトランスポートに対して解決する `Delivery` を配線します (トランスポートクライアントの `Deliver`)。

`target` はトランスポートごとに異なります。

- WhatsApp: JID (`447900123456@s.whatsapp.net`)。
- Telegram: 数値のチャット ID。
- Slack: チャンネル ID (`C012345`) またはユーザー ID (`U012345`)。
- Discord: チャンネル ID。
- SMS: E.164 の宛先。
- iMessage: chat GUID。
- Signal: E.164 の宛先。
- Matrix: ルーム ID。
- Email: RFC 5322 の完全なアドレス。

## 永続化

ジョブはステートデータベース (`internal/state/sqlite/`) の `cron_jobs` テーブルに保存されます。フィールドは `id`、`name`、`schedule`、`prompt`、`target`、`created_at`、`updated_at` です。再起動後は、次の `PollInterval` ですべてのジョブが取り込まれます。

`rousseau cron add` で追加された新規ジョブは、1 回の `PollInterval` 以内 (デフォルトで最大 60 秒) に有効になります。

## トランスポートとの相互作用

`Delivery` のクロージャは、実行中のトランスポートへの参照をキャプチャします。単一のデーモンは通常 1 つのトランスポートを実行するため、cron スケジューラはそのトランスポート経由で配信します。マルチトランスポートのデプロイでは、トランスポートごとに 1 つのデーモンを実行し、オペレーターは各 cron ジョブの `target` を対応するトランスポートのデーモンに向けます。

トランスポート横断の配信 (WhatsApp デーモンでジョブが動作し、Slack で応答する) は現在サポートされていません。スケジューラは渡された `Delivery` のみを知っています。

## 障害モード

| 症状 | 対処 |
|---|---|
| ジョブが発火しない | `rousseau status` を確認してください。スケジューラは有効化ごとに `cron.fired` をログに記録します。 |
| ジョブは発火するが何も届かない | 配信エラーです。ログで `cron.delivery_failed` を確認してください。 |
| ジョブは動作するがモデルが動作を拒否する | 承認ポリシーがツール呼び出しを拒否しています。`agent.approver` を緩めるか、`pattern` モードに移行してください。 |
| 配信先が誤っている | スケジューラはトランスポート非依存であり、`target` はデーモンが解釈します。動作しているトランスポートが target 形式と一致していることを確認してください。 |
