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
description: "Exit codes and signal semantics for the rousseau-agent binary. What init systems can rely on."
keywords: "exit codes, signals, sigterm, sigint, systemd, restart policy"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/reference/exit-codes/"
subtitle: "Exit codes and signal semantics."
tags: "reference, exit-codes, signals"
title: "終了コード"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "exit codes, signals, sigterm, sigint, systemd, restart policy"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "終了コード"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 51
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/reference/exit-codes/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/exit-codes/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "終了コード"
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
twitter_description: "Exit codes and signal semantics for the rousseau-agent binary. What init systems can rely on."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "終了コード"
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

## 終了コード

rousseau の CLI は意図的に保守的です — 2 つの終了コードがすべてのパスをカバーします。

| コード | 発行元 | 意味 |
|---|---|---|
| 0 | `cmd/rousseau/main.go` の `cli.Execute` 経由 | コマンドが正常に完了しました。デーモンは正常なシャットダウン (SIGINT / SIGTERM) で 0 を返します。 |
| 1 | `cmd/rousseau/main.go` の `cli.Execute` 経由 | コマンドが失敗しました。エラー文字列は stderr に印刷されます。すべての失敗 — config パースエラー、プロバイダー認証失敗、トランスポートパニック、ツール配線エラー — がこのコードにマップされます。 |

`rousseau doctor` は同じ規約に従います: すべてのチェックが通過するとき exit 0、任意のチェックが `fail` のとき exit 1。警告と info レベルの行は終了コードに影響しません。

将来のリリースでは、失敗を明確に異なるコード (config vs runtime vs network) に分割する可能性があります。今日は、任意の 0 以外の終了はリトライ可能だがログ検査が必要と扱ってください。

## シグナル処理

`cmd/rousseau/main.go` は `SIGINT` および `SIGTERM` でルート `context.Context` をキャンセルするシグナルハンドラをインストールします。すべての長時間実行コンポーネント (エージェントループ、トランスポート、cron スケジューラ、MCP サーバー) がコンテキストキャンセレーションを尊重するため、シャットダウンパスは:

1. `SIGINT` / `SIGTERM` を受信。
2. ルートコンテキストがキャンセルされる。
3. トランスポートが自身に `Stop()` を呼び、進行中のメッセージをフラッシュします。
4. cron スケジューラが新しい発火の受け入れを停止します。実行中の発火は完了します。
5. `defer` 経由でセッションストアの `Close()` が呼び出され、WAL をチェックポイントします。
6. `Execute` は 0 を返します。

`SIGKILL` は捕捉できません。デーモンがターンの途中で `kill -9` されると、セッションストアの WAL は破損から保護しますが、進行中のターンは永続化されません。次の起動時に、最後に保存された状態から再開します。

## systemd リスタートポリシー

参照 Quadlet ユニットの場合:

```
[Service]
Restart=on-failure
RestartSec=10
```

`on-failure` は任意の 0 以外の終了でリスタートします。rousseau の終了コード規約と組み合わせるとこれは意味します: exit 0 (`systemctl stop` からの `SIGTERM`) はリスタートしません、exit 1 はリスタートします。

永続的なエラー (不正な config、間違ったプロバイダー認証) にぶつかるデーモンでは、`on-failure` はスラッシングします。リトライループが回復すると仮定する前に、失敗理由を `journalctl` で監視してください。

## Kubernetes プローブセマンティクス

rousseau は設計上 HTTP の liveness/readiness エンドポイントを出荷しません。Kubernetes プローブは次のいずれかである必要があります:

- `rousseau doctor --config /etc/rousseau/config.yaml` を実行する `exec` プローブ (健全時 0、失敗時 1 を返す)、または
- なし。Pod は `restartPolicy: Always` とデーモン自身のエラーハンドリングに頼ります。

`rousseau doctor` は安価 (~50ms) なので、良好な liveness プローブです。readiness プローブとしては使用しないでください — `provider.claudecli.binary` の `fail` は、失敗が自己修復しない場合に Pod をローテーションから外すべきではありません。

## 処理されるエラー

CLI エラー表面を通じて終了コード 1 を生成するエラーには次のものが含まれます:

- **Config ロード失敗** — YAML パースエラー、未知のフィールド、無効な型。
- **プロバイダー認証失敗** — API キー欠落、無効な資格情報、無効な Bedrock / Vertex リージョン。
- **トランスポート起動失敗** — トークン欠落、到達不可能な IMAP/SMTP ホスト、whatsmeow プロトコルエラー。
- **ストアオープン失敗** — `~/.local/share/rousseau/` のパーミッション拒否、ディスクフル。
- **Doctor チェック失敗** — 任意の `fail` 行が doctor を exit 1 で返させます。
- **Cron cron 式パース失敗** — `rousseau cron add` は永続化する前に検証します。

## 処理されないパニック

`go test -race` はすべての CI ビルドで実行されるため、パニックは極めてまれです。発生した場合、Go ランタイムはパニック + スタックトレースを stderr に印刷し、ランタイムから 0 以外のコードで終了します — 通常 2 ですが、これは Go の規約であり、rousseau が制御するものではありません。

プロダクションでは、異常終了時に stderr を捕捉してトレースを報告するスーパーバイザーでデーモンをラップしてください。

## 次に

- [ユーザーガイド: CLI](/ja/user-guide/cli/) — すべてのコマンド。
- [ガイド: 可観測性](/ja/guides/observability/) — 終了コードを超えて slog シグナルを表面化します。
- [トラブルシューティング](/ja/troubleshooting/) — 終了コードで十分でない場合に何をするか。
