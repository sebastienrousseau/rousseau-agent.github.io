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
description: "Recommended reading order for new rousseau-agent users, split by role: individual developer, platform operator, security reviewer."
keywords: "learning path, reading order, docs guide, individual developer, platform operator, security reviewer"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/getting-started/learning-path/"
subtitle: "What to read first, split by role."
tags: "learning-path, reading-order"
title: "学習パス"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "learning path, reading order, docs guide, individual developer, platform operator, security reviewer"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "学習パス"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 22
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/getting-started/learning-path/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/learning-path/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "学習パス"
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
twitter_description: "Recommended reading order for new rousseau-agent users, split by role: individual developer, platform operator, security reviewer."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "学習パス"
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

## 役割を選ぶ

rousseau の対象読者は 3 つの軸に沿ってきれいに分かれます。目的に合うものを選び、順番に読んでください — すべてのパスは、前のセクションが吸収されていることを前提としています。

## 個人開発者

セッションを永続化し、既存の `claude` CLI を駆動する、自分のラップトップ上のコーディングアシスタントが欲しい。チームなし、共有デプロイなし。

| # | ページ | 理由 |
|---|---|---|
| 1 | [はじめに](/ja/getting-started/) | インストール、`rousseau chat`、初回実行ウォークスルー。 |
| 2 | [コンセプト](/ja/concepts/) | 何かをカスタマイズする前に、エージェントループとセッションストアを理解します。 |
| 3 | [ユーザーガイド: CLI](/ja/user-guide/cli/) | すべてのコマンド、すべてのフラグ。 |
| 4 | [ユーザーガイド: TUI](/ja/user-guide/tui/) | キーバインドとパネルセマンティクス。 |
| 5 | [ユーザーガイド: ツール](/ja/user-guide/tools/) | 5 つの組み込みツールが何をし、何をしないか。 |
| 6 | [設定](/ja/configuration/) | 触れた部分をチューニングします。 |
| 7 | [スキル](/ja/skills/) | 再利用可能なプロンプト断片を作成します。 |

エージェントループを別のバイナリに組み込む予定がなければ、[デベロッパーガイド](/ja/developer-guide/) 以下はすべてスキップしてください。

## プラットフォームオペレーター

企業境界の背後でチーム向けに rousseau を運用しています。稼働時間、監査可能性、最小権限姿勢がロードベアリングです。

| # | ページ | 理由 |
|---|---|---|
| 1 | [はじめに](/ja/getting-started/) | インストールとスモークテスト。 |
| 2 | [プラットフォームサポート](/ja/getting-started/platform-support/) | すべての依存関係バージョンを確認します。 |
| 3 | [コンセプト](/ja/concepts/) | 層状アーキテクチャ — リリース間で安定したままだと信頼できるもの。 |
| 4 | [デプロイ](/ja/deployment/) | Rootless Podman + Quadlet。Kubernetes メモ。 |
| 5 | [ガイド: Kubernetes デプロイ](/ja/guides/kubernetes-deployment/) | Kubernetes がターゲットの場合。 |
| 6 | [設定](/ja/configuration/) + [リファレンス: 設定スキーマ](/ja/reference/config-schema/) | すべてのノブ、構造化。 |
| 7 | [ユーザーガイド: 承認ポリシー](/ja/user-guide/approval-policies/) | 監査人に提示するツール呼び出し承認のストーリー。 |
| 8 | [ガイド: 可観測性](/ja/guides/observability/) | slog 出力をログパイプラインに配線します。 |
| 9 | [ガイド: 監査 + 承認ポリシー](/ja/guides/audit-approval-policies/) | 拒否ルール付きのパターンモード設定の作業例。 |
| 10 | [更新](/ja/getting-started/updating/) | バージョン間を安全に移動します。 |

## セキュリティレビュアー

ロールアウト前に rousseau を審査しているか、チームに代わってサプライヤーアンケートに回答しています。

| # | ページ | 理由 |
|---|---|---|
| 1 | [セキュリティ](/ja/security/) | 信頼モデル、サプライチェーン姿勢、暗号インベントリ。 |
| 2 | [インストール](/ja/getting-started/installation/) | cosign + SHA-256 検証レシピ。 |
| 3 | [コンセプト](/ja/concepts/) | 層状アーキテクチャ — 信頼境界が存在する場所。 |
| 4 | [ユーザーガイド: 承認ポリシー](/ja/user-guide/approval-policies/) | モデルとシェルの間のレバー。 |
| 5 | [ガイド: 読み取り専用モード](/ja/guides/read-only-mode/) | 初回検査デプロイの姿勢。 |
| 6 | [リファレンス: 終了コード](/ja/reference/exit-codes/) | init システムとモニターに表面化する障害モード。 |
| 7 | [プライバシー](/ja/privacy/) | データフロー姿勢。 |
| 8 | [デプロイ](/ja/deployment/) | ランタイムハードニング — Podman フラグ、capability の drop、seccomp。 |

## 横断的な読み物

役割を選んだ後、すべての読者はこれらの恩恵を受けます:

- [トラブルシューティング](/ja/troubleshooting/) — `rousseau doctor` で到達できるすべての診断。
- [変更履歴](/ja/changelog/) — リリース間で何が動いたか。
- [MCP](/ja/mcp/) — rousseau が他のエージェントにツールとセッションを公開する方法。
- [Cron](/ja/cron/) — 時計上でプロンプトをスケジュールします。

## 次に

- [プラットフォームサポート](/ja/getting-started/platform-support/) — 何がどこで動作するか。
- [最初のトランスポート](/ja/getting-started/first-transport/) — WhatsApp の作業ウォークスルー。
