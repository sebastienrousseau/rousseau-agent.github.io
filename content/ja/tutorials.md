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
description: "Full end-to-end walkthroughs: code-review bot, nightly changelog, VPS deployment, MCP integration, and approver hardening."
keywords: "tutorials, code review bot, changelog, vps deployment, mcp, approval policy"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/tutorials/"
subtitle: "全体を組み合わせるエンドツーエンドの完全ガイド。"
tags: "tutorials, walkthrough, code review, changelog, deployment, mcp"
title: "チュートリアル"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tutorials, code review bot, changelog, vps deployment, mcp, approval policy"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "チュートリアル"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/tutorials/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "チュートリアル"
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
twitter_description: "Full end-to-end walkthroughs: code-review bot, nightly changelog, VPS deployment, MCP integration, and approver hardening."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "チュートリアル"
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

## チュートリアルの目的

ガイドは単一の「どうすれば…できるか」という質問に個別に答えます。チュートリアルは逆方向のアプローチをとります。完全な実世界のシナリオを取り上げ、それを出荷するために必要な rousseau の各部品を通してウォークスルーします。各チュートリアルからは、自分のワークスペースに貼り付けても動作することが期待できる成果物が得られます。

| チュートリアル | 得られる成果物 |
|---|---|
| [Build a code-review bot](/ja/tutorials/build-a-code-review-bot/) | リポジトリパス上で `@rousseau` にメンションすると `read` と `grep` によるレビューが実行される Slack チャンネル。 |
| [Nightly changelog](/ja/tutorials/nightly-changelog/) | その日の `git log` を要約して 18:00 に WhatsApp にプッシュする cron ジョブ。 |
| [Deploy to a VPS](/ja/tutorials/deploy-to-a-vps/) | systemd 配下で新規 VPS 上に堅牢化された rootless Podman デプロイ。 |
| [Expose tools via MCP](/ja/tutorials/expose-tools-via-mcp/) | Claude Desktop から `rousseau_search_sessions`、`rousseau_list_sessions`、`rousseau_read_session`、`rousseau_cron_list` を駆動。 |
| [Harden the approver](/ja/tutorials/harden-approver-policy/) | `default: deny` を伴う厳格な `pattern` モードの承認者と、slog 監査証跡による検証。 |

## 前提条件

すべてのチュートリアルは、[Quickstart](/ja/quickstart/) を完了していることを前提としています。すなわち、`rousseau` が `$PATH` 上にあり、プロバイダーが設定されており、`rousseau chat` が応答することです。

それ以外に必要なもの (Slack ワークスペース、VPS、WhatsApp にリンクされた電話番号、`claude` デスクトップなど) は、各チュートリアルで明記されます。

## チュートリアルではないもの

短い「X を行うにはどうすればいい」というレシピが欲しい場合は [Guides](/ja/guides/) を参照してください。CLI フラグやコンフィグフィールドの正確な仕様を知りたい場合は [Reference](/ja/reference/cli-commands/) に進んでください。rousseau の各部品が何をするかを配線前に理解したい場合は、まず [Concepts](/ja/concepts/) から始めてください。
