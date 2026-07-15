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
description: "Beyond the Quadlet reference: log shipping, session-store backup, health checks, rolling restarts, and multi-transport coexistence."
keywords: "production, log shipping, backup, health check, rolling restart, systemd"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/guides/production-deployment/"
subtitle: "Everything the Quadlet reference doesn't already cover."
tags: "guides, production, deployment, backup, logs, health check"
title: "ガイド：本番デプロイ"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "production, log shipping, backup, health check, rolling restart, systemd"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ガイド：本番デプロイ"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/guides/production-deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/production-deployment/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "ガイド：本番デプロイ"
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
twitter_description: "Beyond the Quadlet reference: log shipping, session-store backup, health checks, rolling restarts, and multi-transport coexistence."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "ガイド：本番デプロイ"
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

## この後に読んでください

`docker/rousseau-agent.container` のリファレンス Quadlet ユニットは「rousseau の実行方法」のストーリーをカバーします。このガイドは、それをプロダクションと呼ぶ前にその周りに追加するものをカバーします: ログ、バックアップ、ヘルス、プロセスの衛生。

## ログ配送

rousseau は `log/slog` (`internal/cli/root.go`) 経由で構造化ログを stderr に書き込みます。systemd の下で実行すると、その stderr はジャーナルに到達します。ホスト外に配送するためのオプション:

| ツール | 適合性 | 備考 |
|---|---|---|
| Vector (`vector.dev`) | 最良のデフォルト。 | `journald` ソース + DEBUG を落とすフィルタ。Loki、Datadog、S3 など、任意の場所に配送。 |
| Promtail + Loki | すでに Grafana を運用している場合。 | Loki の `journal` ソースは `journalctl -o json` に対して直接動作します。 |
| Datadog Agent | Datadog が組織の標準の場合。 | DD エージェントには journald tail があります。構造化 JSON はネイティブにパースされます。 |
| Fluent Bit | 小さなフットプリントの代替。 | `config.yaml` で `log.format: json` を設定します。Fluent Bit の `systemd` 入力がパースします。 |

プロダクションでは無条件に `log.format: json` (`internal/config/config.go` `LogConfig.Format`) を設定してください。テキスト出力はマシンパースではなく `less` 用に設計されています。

完全な Loki パイプラインレシピについては [ガイド: 可観測性](/ja/guides/observability/) を参照してください。

## セッションストアのバックアップ

ステートディレクトリ `~/.local/share/rousseau/` は、rousseau が所有する唯一の永続的なステートです。夜次でバックアップしてください。

2 つのアプローチ:

**1. SQLite `.backup` (推奨)。**

```sh
sqlite3 ~/.local/share/rousseau/sessions.db \
  ".backup '/backup/sessions.db.$(date +%Y%m%d).bak'"
sqlite3 ~/.local/share/rousseau/whatsapp.db \
  ".backup '/backup/whatsapp.db.$(date +%Y%m%d).bak'"
restic backup /backup
```

`.backup` は SQLite のオンライン API を使用します — デーモンが書き込んでいる間でも安全です。[リファレンス: セッションストア](/ja/reference/session-store/) を参照してください。

**2. ファイルシステムスナップショット。**

WAL ジャーナリングがオン (`internal/state/sqlite/store.go` の `Open()`) であるため、`restic` と `borg` はデーモン実行中に生のファイルをスナップショットできます。WAL は一貫したポイントインタイムイメージを保証します。

やってはいけないこと:

- デーモンが実行中に、`-wal` と `-shm` も一緒にコピーしない限り、`cp` で `.db` ファイルをコピーする。
- バックアップを同じディスクに保存する。
- WhatsApp デバイス認証情報ファイルをスキップする — 失うと QR の再スキャンを意味します。

## ヘルスチェック

`rousseau status` (`internal/cli/status.go`) は健康時に 0、問題時に非ゼロで終了します。systemd ヘルスプローブとして使用します:

```ini
[Service]
ExecStartPost=/usr/bin/timeout 30 podman exec rousseau-agent rousseau status
```

より豊富なプローブには、以下を行うチェックをスクリプト化します:

1. `rousseau status` を実行します。
2. セッションストアの最後の書き込みが最近であることを確認します (`stat sessions.db -c %Y` を現在と比較)。
3. `podman inspect` を通じてコンテナの稼働時間をチェックします。

rousseau は HTTP `/healthz` を公開しません。プラットフォームが要求する場合 (Kubernetes readiness プローブ)、[ガイド: Kubernetes デプロイ](/ja/guides/kubernetes-deployment/) を参照してください — rousseau を小さな `curl` フレンドリーなサイドカーでラップします。

## ローリング再起動

ステートが単一の SQLite ファイルであるため、デーモンは真にシングルインスタンスです。ローリング再起動は: 停止、イメージ置換、開始。ウォームアップは不要です。

```sh
podman pull localhost/rousseau-agent:local     # or rebuild locally
systemctl --user restart rousseau-agent
podman logs -n 50 rousseau-agent | grep -E 'starting|connected'
```

期待されるログシーケンス (`internal/transport/whatsapp/client.go` から):

```
INFO whatsapp.starting store=… allowlist=1
INFO whatsapp.connected
```

If the daemon does not emit `whatsapp.connected` within ~15 seconds, roll back.

## Multiple transports on one host

You may want the same session store shared by WhatsApp and Slack. Two ways:

- **Multiple Quadlet units** — one for each transport, each pointing at the same `state.path`. WAL + `busy_timeout` (see `Open()` in `internal/state/sqlite/store.go`) makes concurrent writers safe.
- **One binary, one transport per invocation.** Rousseau's transport commands are single-transport (`whatsapp`, `slack`, `signal`, …). To run two transports you run two processes.

## Zero-downtime configuration changes

Rousseau does not hot-reload `config.yaml`. Config changes require a restart. `SIGHUP` is not wired for reload.

Practical workflow:

1. Edit `~/.config/rousseau/config.yaml`.
2. `systemctl --user restart rousseau-agent`.
3. Verify from logs.

For most transports the reconnection is fast (~1-3 seconds). The main pause is on WhatsApp, where whatsmeow re-establishes the websocket.

## Log retention

`journald` retention is set by `SystemMaxUse=` in `/etc/systemd/journald.conf`. For an audit-friendly deployment, ship logs off-host and set journald to a shorter retention on the local disk (e.g. 7 days) so the audit trail lives in Loki/S3, not on a filesystem an intruder might rotate.

## Container image lifecycle

Rebuild the image on every rousseau release you want to adopt:

```sh
cd ~/rousseau-agent
git pull
podman build -t rousseau-agent:local -f docker/Dockerfile .
systemctl --user restart rousseau-agent
```

The Quadlet `AutoUpdate=disabled` line (in `docker/rousseau-agent.container`) prevents `podman auto-update` from touching the container. You control the update cadence.

## Related

- [Deployment](/ja/deployment/) — the reference Quadlet unit.
- [Tutorial: Deploy to a VPS](/ja/tutorials/deploy-to-a-vps/) — worked example.
- [Guides: Observability](/ja/guides/observability/) — log pipeline.
- [Guides: Enterprise Onboarding](/ja/guides/enterprise-onboarding/) — full checklist.
