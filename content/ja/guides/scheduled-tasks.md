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
description: "Worked example: use rousseau-agent's cron scheduler + WhatsApp to run a scheduled prompt daily and deliver the result to your phone."
keywords: "cron, scheduled tasks, whatsapp, code review, robfig, daily reminder"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/guides/scheduled-tasks/"
subtitle: "Nag yourself daily via WhatsApp."
tags: "guides, cron, scheduled, whatsapp"
title: "ガイド：スケジュールタスク"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cron, scheduled tasks, whatsapp, code review, robfig, daily reminder"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ガイド：スケジュールタスク"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 31
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/guides/scheduled-tasks/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/scheduled-tasks/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "ガイド：スケジュールタスク"
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
twitter_description: "Worked example: use rousseau-agent's cron scheduler + WhatsApp to run a scheduled prompt daily and deliver the result to your phone."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "ガイド：スケジュールタスク"
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

## シナリオ

コードレビューの受信箱に古くなったものがあるかを尋ねる毎日のリマインドを、09:00 に WhatsApp で受け取りたいとします。エージェントはローカルのレビューキューファイルを読み、要約し、その要約をあなたの電話に配信する必要があります — ラップトップが別のタスクの最中でも関係ありません。

構成要素:

- 実行中の `rousseau whatsapp` デーモン。
- `rousseau cron add` によって SQLite に永続化された cron ジョブ。
- デーモン内部の `robfig/cron/v3` スケジューラ goroutine がジョブを発火します。返信は同じ WhatsApp トランスポートを通じて配送されます。

## 前提条件

- ペアリング済みで、少なくとも 1 つの JID にメッセージを配信している `rousseau whatsapp` ([最初のトランスポート](/ja/getting-started/first-transport/))。
- プロンプトがポイントできるファイル — このウォークスルーでは、`/workspace/review-queue.md` にある Markdown キュー。

## ステップ 1 — ジョブを登録する

```sh
rousseau cron add \
  --name daily-review-nag \
  --schedule "0 9 * * *" \
  --prompt "Read /workspace/review-queue.md and list every PR that has been open for more than 3 days. Reply with 3 bullets max." \
  --deliver-to 447900123456@s.whatsapp.net
```

`--schedule` は `robfig/cron/v3` によってパースされる 5 フィールドの POSIX スタイル cron 式 (`min hour dom mon dow`) です。rousseau は追加時に式を検証します。無効なスケジュールは、ストアに入る前に fail-fast します。

`--deliver-to` は返信を受け取る WhatsApp JID です。グループの場合は `@g.us` 形式を使用してください。

## ステップ 2 — ジョブが有効になったことを確認する

```sh
rousseau cron list
```

出力:

```
b7a3f2e1  on   daily-review-nag      0 9 * * *             last=never
    Read /workspace/review-queue.md and list every PR that has been open for more than 3 days. Reply with 3 bullets max. → 447900123456@s.whatsapp.net
```

新しいジョブは次のスケジューラポーリング間隔内 (デフォルト 60 秒) で有効になります。再起動は不要です。

## ステップ 3 — ドライランを強制する

スケジュールされたジョブは実行中の `rousseau whatsapp` デーモンによって発火されます。09:00 を待たずに配線を検証するには、スケジュールを一時的に 1 分後に実行するように変更してください:

```sh
rousseau cron remove daily-review-nag
rousseau cron add \
  --name daily-review-nag \
  --schedule "*/1 * * * *" \
  --prompt "..." \
  --deliver-to 447900123456@s.whatsapp.net
```

デーモンのログを監視:

```
cron.fire   name=daily-review-nag job=b7a3f2e1
tool.execute name=read id=t_1
cron.deliver name=daily-review-nag target=447900123456@s.whatsapp.net bytes=284
```

電話にメッセージが表示されたら、毎分のコピーを削除し、毎日のバージョンを再追加してください。

## ステップ 4 — 削除せずに無効化する

```sh
rousseau cron disable daily-review-nag
```

`enabled=false` に切り替えると、ジョブはストアに残りますが、すべての発火でスキップされます。`rousseau cron enable daily-review-nag` で再有効化してください。

## 内部で起こること

1. `rousseau cron add` は `~/.local/share/rousseau/sessions.db` の `cron` テーブルに行を書き込みます。
2. `rousseau whatsapp` デーモンは起動時に `robfig/cron/v3` スケジューラ goroutine を開始し、`PollInterval` (デフォルト 60 秒) ごとにテーブルをポーリングします。
3. cron 式が発火すると、`Runner.RunOnce(ctx, prompt)` は新しいセッション (過去の発火からの履歴なし) に対してワンショットのエージェントターンを実行します。
4. 返信は `Delivery` を通過します — デーモンが `client.Deliver(ctx, target, body)` に配線しているトランスポート非依存のコールバックです。
5. ストアの `last_run_at` が更新されます。失敗はログに記録されますが、ジョブは無効化されません。

スケジューラは durable です: デーモンが発火の途中で死んでも、次の起動時にキューを拾います。`robfig/cron/v3` が tick で重複を排除するため、同じ分にジョブが 2 回発火することはありません。

## 一般的なパターン

| スケジュール | 意味 |
|---|---|
| `0 9 * * *` | 毎日 09:00。 |
| `*/15 9-17 * * 1-5` | 15 分ごと、09:00–17:59、月–金。 |
| `0 * * * *` | 毎時 0 分。 |
| `0 0 * * 0` | 毎週日曜日の 0 時。 |

## スキルとのレイヤリング

長いプロンプトは退屈です。スケジュールされたジョブのプロンプトが増え続ける場合は、ボイラープレートを [スキル](/ja/skills/) に移動し、プロンプトからそれを参照させてください。スキルは発火時にシステムプロンプトにスプライスされます。

## 注意事項

- スケジュールされたジョブは、デーモンの設定済みプロバイダーに対して実行されます。プライマリプロバイダーが `claudecli` で、根底の `claude` ログインをローテートすると、再認証するまで発火は失敗します。
- 配信先はデーモンの allowlist に属している必要があります。スケジュールされたジョブが要求しても、rousseau は allowlist 外の JID には配信しません。
- cron スケジューラは設計上 `rousseau whatsapp` デーモン内で実行されます。`rousseau slack` を並行して実行すると、同じテーブルを読み取る 2 つの独立したスケジューラができます — ジョブは 2 回発火します。1 つのデーモンにスケジュールを所有させてください。

## 次に

- [Cron リファレンス](/ja/cron/) — すべてのサブコマンド、すべてのフラグ。
- [スキル](/ja/skills/) — ジョブ間でプロンプトのボイラープレートを共有します。
- [監査 + 承認ポリシー](/ja/guides/audit-approval-policies/) — スケジュールされたプロンプトができることをロックダウンします。
