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
description: "Concrete deployment narratives for rousseau-agent: on-call SRE, mobile PR review, regulated-industry Bedrock deployment."
keywords: "use cases, narratives, on-call, sre, mobile review, whatsapp, bedrock, regulated"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/use-cases/"
subtitle: "具体的な事例 — 誰がなぜ rousseau を運用しているか。"
tags: "use-cases, narratives"
title: "ユースケース"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "use cases, narratives, on-call, sre, mobile review, whatsapp, bedrock, regulated"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ユースケース"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 70
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/use-cases/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "ユースケース"
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
twitter_description: "Concrete deployment narratives for rousseau-agent: on-call SRE, mobile PR review, regulated-industry Bedrock deployment."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "ユースケース"
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

## マニュアルではなく全体像が欲しいときに読んでください

ユースケースは短い物語です。それぞれ、想定されるオペレーター、直面する問題、使用する正確な設定を記述します。各ユースケースは 1 ページです — 自分の状況に合うものを読んでください。

| ユースケース | ペルソナ | 問題 |
|---|---|---|
| [オンコールバディ](/ja/use-cases/oncall-buddy/) | 小企業の単独 SRE。 | 午前 3 時の Slack ページ、完全に目が覚める前のトリアージ。 |
| [モバイル PR レビュー](/ja/use-cases/mobile-review/) | 通勤中の個人開発者。 | 電話からプルリクエストをレビュー。 |
| [規制業界](/ja/use-cases/regulated-industry/) | 金融サービスチーム。 | Bedrock ホスト型 VPC 内の、パターンモード承認付きコーディングエージェント。 |

これらは例示であり、網羅的ではありません — rousseau の設計は一般化します。あなたの状況がこれらのいずれかに似ている場合は、そこから始めてください。

## すべてのユースケースに共通するもの

- rootless コンテナ内の単一の Go バイナリ。
- インスタンスあたり 1 つのトランスポート (Slack、WhatsApp、Signal のいずれか 1 つを選ぶ)。
- 妥当な拒否ルールを持つ `pattern` モードの承認者。
- SQLite 内のセッション状態。再起動しても会話が失われません。
- SaaS コントロールプレーンなし、テレメトリエンドポイントなし、ライセンスサーバーなし。

## 変わるもの

- **プロバイダ** — 個人ラップトップには `claudecli`、規制環境には `bedrock`/`vertex`、セルフホスト vLLM には `openai` 互換。
- **トランスポート** — エンジニアがすでに使っている媒体を選ぶ。
- **承認ポリシー** — 高リスク環境では厳しく、ロックダウンされたコンテナ内では緩く。
- **デプロイ面** — ラップトップ、シングルノード Podman、Kubernetes。

## 次に

- [オンコールバディ](/ja/use-cases/oncall-buddy/) — 最も一般的なストーリー。
- [モバイル PR レビュー](/ja/use-cases/mobile-review/) — WhatsApp がリファレンストランスポートである理由。
- [規制業界](/ja/use-cases/regulated-industry/) — エンタープライズストーリー。
