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
date: "July 13, 2026"
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
description: "Schedule a rousseau cron job that summarises git log every evening and posts the result to WhatsApp."
keywords: "cron, git log, changelog, whatsapp, scheduled prompt, deliver-to"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/tutorials/nightly-changelog/"
subtitle: "A daily 18:00 cron job that pushes a git-log summary to WhatsApp."
tags: "tutorials, cron, changelog, whatsapp, git"
title: "チュートリアル：夜間の Changelog 生成"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, git log, changelog, whatsapp, scheduled prompt, deliver-to"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "チュートリアル：夜間の Changelog 生成"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/tutorials/nightly-changelog/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/nightly-changelog/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "チュートリアル：夜間の Changelog 生成"
last_build_date: "Mon, 13 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
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
twitter_description: "Schedule a rousseau cron job that summarises git log every evening and posts the result to WhatsApp."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "チュートリアル：夜間の Changelog 生成"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "自らのコーディングエージェントを運用するすべてのオペレーターに感謝します。"
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## 構築するもの

rousseau 独自の SQLite 状態 (`cron_jobs` テーブル、スキーマは `internal/state/sqlite/cron.go`) に格納される cron ジョブで、平日のローカル時間 18:00 に発火します。モデルに `git log --since=today` を要約するよう求めるプロンプトを実行し、結果を WhatsApp 経由でスマートフォンに配信します。

想定時間: 10 分。

## 前提条件

- ペアリング済みの WhatsApp ブリッジ ([クイックスタート](/ja/quickstart/) ステップ 4、または [トランスポート: WhatsApp](/ja/transports/whatsapp/) を参照)。
- 実行中の `rousseau whatsapp` デーモン — `internal/cron/scheduler.go` の cron スケジューラは、`rousseau chat` ではなく、`wiring.startCron()` 経由でトランスポートデーモンによって起動されます。
- 要約させたい git リポジトリを含むワークスペースで、コンテナにバインドマウントされている (またはコンテナ外で rousseau を実行する場合はホスト上に)。

## rousseau cron の仕組み

`rousseau cron add` は `cron_jobs` テーブル (`internal/state/sqlite/cron.go`) に行を書き込みます。約 15 秒ごとに `scheduler.sync` がテーブルを再読み込みし、robfig/cron/v3 のメモリ内スケジュールと調停します。ジョブが発火すると、スケジューラは `cron.firing` を発し、設定済みプロバイダー経由でプロンプトを実行し、プロセスを所有するトランスポートブリッジ (このチュートリアルでは WhatsApp) 経由で `deliver_to` に結果を配信します。

見ることになる構造化ログ名 (`internal/cron/scheduler.go` から):

- `cron.started` — スケジューラが `poll_interval=…` で起動された。
- `cron.scheduled` — ジョブが受け入れられた。
- `cron.firing` — ジョブが実行されようとしている。
- `cron.completed` — ジョブが正常に完了した。
- `cron.run_failed`、`cron.delivery_failed`、`cron.record_failed` — 失敗モード。

## ステップ 1: ジョブを追加する

```sh
rousseau cron add \
  --name        nightly-changelog \
  --schedule    "0 18 * * 1-5" \
  --prompt      "Summarise git log --since=yesterday under /workspace/rousseau-agent as a Slack-style bullet list. Keep it under 200 words. If nothing changed, reply with a single line 'no commits'." \
  --deliver-to  447900123456@s.whatsapp.net
```

cron 式は `newCronAddCmd` (`internal/cli/cron.go`) の `robfig/cron/v3` でパースされます。無効な式は書き込み前に拒否されます。`--deliver-to` の値は WhatsApp 用の E.164 JID (`<digits>@s.whatsapp.net`) です。配信ターゲット形式はトランスポート固有です。

## ステップ 2: 検証

```sh
rousseau cron list
```

出力形状 (`newCronListCmd` から):

```
NAME               STATUS SCHEDULE       PROMPT                       DELIVER-TO
nightly-changelog  on     0 18 * * 1-5   Summarise git log …          447900123456@s.whatsapp.net
```

このリストは `rousseau_cron_list` として MCP 経由でも公開されます (`internal/mcp/tools.go` を参照)。

## ステップ 3: ドライラン

組み込みの「今すぐ発火」トリガーはありません。スモークテストするには、ジョブを 1 分後にスケジュールしてください:

```sh
rousseau cron remove nightly-changelog
rousseau cron add --name test --schedule "*/1 * * * *" --prompt "say hi" --deliver-to "$JID"
journalctl --user -u rousseau-agent -f | grep cron.
```

期待されるログシーケンス:

```
INFO cron.scheduled  job=test expr=*/1 * * * *
INFO cron.firing     job=test
INFO cron.completed  job=test
```

完了したらテストジョブを削除し、実際のジョブを再追加してください。

## ステップ 4: プロンプトを引き締める

最良の cron プロンプトは自己完結型です: モデルは以前の実行の記憶を持ちません。リポジトリパス、期待される出力形式、空のケースのフォールバックを含めてください。2 回目のイテレーションの例:

```
Summarise commits authored since 07:00 UTC today under
/workspace/rousseau-agent. Use this format:

- <short type>: <one-line summary> — <sha>

Group by author. If no commits landed, reply exactly: no commits.
```

## トグルと削除

```sh
rousseau cron disable nightly-changelog   # keeps the row, stops firing
rousseau cron enable  nightly-changelog
rousseau cron remove  nightly-changelog   # deletes the row
```

これらは `internal/state/sqlite/cron.go` の `SetEnabled` と `Delete` を呼び出します。

## 関連

- [Cron](/ja/cron/) — スケジューラのリファレンス。
- [ガイド: スケジュールタスク](/ja/guides/scheduled-tasks/) — より深い議論。
- [トランスポート: WhatsApp](/ja/transports/whatsapp/) — delivery-to の仕組み。
- [リファレンス: CLI コマンド](/ja/reference/cli-commands/) — すべての `rousseau cron` フラグ。
