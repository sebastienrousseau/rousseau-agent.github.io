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
description: "Chronological release notes for rousseau-agent. First public snapshot: 9 transports, 5 providers, MCP server, SLSA-3, 76% coverage."
keywords: "changelog, release notes, versions, snapshot"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/changelog/"
subtitle: "rousseau-agent の時系列リリースノート。"
tags: "changelog, reference"
title: "変更履歴"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "changelog, release notes, versions, snapshot"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "変更履歴"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 28
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/changelog/index.html"
item_link: "https://docs.rousseau-agent.dev/changelog/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "変更履歴"
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
twitter_description: "Chronological release notes for rousseau-agent. First public snapshot: 9 transports, 5 providers, MCP server, SLSA-3, 76% coverage."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "変更履歴"
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

## 現在の状態 — 2026 年 7 月

初の公開スナップショット。今日出荷されるものの主なポイント:

- **9 種類のチャットトランスポート。** WhatsApp、Signal、Telegram、Matrix、Slack、Discord、iMessage、Email、SMS。
- **5 種類の LLM プロバイダ。** claudecli、Anthropic 直接、AWS Bedrock、Google Vertex AI、OpenAI 互換。
- **MCP サーバー。** JSON-RPC 2.0 over stdio、仕様リビジョン 2024-11-05。
- **SLSA レベル 3** のビルドプロビナンス、cosign 署名付きリリースチェックサム、CycloneDX SBOM。
- モジュール全体で **76% のテストカバレッジ** (コアパッケージは 85〜100%)。
- **オープンな Dependabot アラート 0 件。**
- `ubuntu-latest` と `macos-latest` での **フルレースモード CI**。

## 詳細

コミット単位の完全な履歴については、https://github.com/sebastienrousseau/rousseau-agent の git ログを参照してください。

すべてのコミットは [Conventional Commits](https://www.conventionalcommits.org/) を使用します。changelog ページには、最初のタグ付きリリースがカットされ次第、構造化されたエントリが追加されます。それまでは `git log --oneline` が権威ある参照です。

## 互換性ポリシー

- **設定ファイル形式** は、スキーマ破壊ではなくフィールド追加でバージョン管理されます。新しいキーは無視して安全です。リネームと削除は、削除に先立つリリースで非推奨警告の後ろに導入されます。
- **`agent.Provider`、`agent.Message`、`agent.Session`** はサードパーティ組み込み者向けの安定エクスポートです。破壊的変更はメジャーバージョンアップで導入されます。
- **`internal/*` パッケージ** は安定 API ではありません — プロジェクトの内部です。サードパーティのコンシューマはインポートすべきではありません (Go の `internal` 可視性がこれを強制します)。

## フィードバックの送り先

- バグと機能要望: GitHub Issues。
- セキュリティ: `sebastian.rousseau@gmail.com` ([/security/](/ja/security/) を参照)。
