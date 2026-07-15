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
description: "Support routing for rousseau-agent. GitHub issues for bugs and features. sebastian.rousseau@gmail.com for security reports."
keywords: "contact, support, GitHub issues, security disclosure, email"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/contact/"
subtitle: "バグ・要望・セキュリティ報告の連絡先。"
tags: "contact, support"
title: "お問い合わせ"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "contact, support, GitHub issues, security disclosure, email"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "お問い合わせ"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "support"
order: 29
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/contact/index.html"
item_link: "https://docs.rousseau-agent.dev/contact/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "お問い合わせ"
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
twitter_description: "Support routing for rousseau-agent. GitHub issues for bugs and features. sebastian.rousseau@gmail.com for security reports."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "お問い合わせ"
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

## バグと機能要望

https://github.com/sebastienrousseau/rousseau-agent/issues で Issue を作成してください。以下を含めてください:

- `rousseau version` の出力。
- Go のバージョン、OS、コンテナランタイム。
- 最小再現手順 — 理想的には失敗するテスト。
- `ROUSSEAU_LOG_LEVEL=debug` でのログ抜粋 (シークレットは黒塗り)。

## セキュリティ開示

セキュリティに影響するレポートについては、公開 Issue を作成 **しないでください**。以下にメールしてください:

**sebastian.rousseau@gmail.com**

受領 SLA: 72 時間。完全開示の SLA 表は [セキュリティページ](/ja/security/) にあります。

お持ちであれば CVSS 3.1 ベクター、影響を受けるコンポーネント (ファイルパスと行範囲、または依存モジュール)、最小再現手順、遵守が必要な調整開示タイムラインを含めてください。

完全なポリシーはソースリポジトリの `SECURITY.md` にあります。

## 商用 / コンサルティング

`rousseau-agent` は MIT ライセンスのオープンソースプロジェクトです。商用サポート階層は存在しません。コンサルティング業務はアドホックです — 上記のメールでメンテナに連絡してください。
