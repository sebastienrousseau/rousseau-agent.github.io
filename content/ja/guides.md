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
description: "Worked examples for rousseau-agent: scheduled tasks, self-hosted vLLM, Kubernetes deployment, approval-policy audits, observability, read-only mode."
keywords: "guides, tutorials, worked examples, vllm, kubernetes, audit, observability, read-only"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/guides/"
subtitle: "実行可能な設定付きの実践例集。"
tags: "guides, tutorials"
title: "ガイド"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "guides, tutorials, worked examples, vllm, kubernetes, audit, observability, read-only"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ガイド"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 30
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/guides/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "ガイド"
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
twitter_description: "Worked examples for rousseau-agent: scheduled tasks, self-hosted vLLM, Kubernetes deployment, approval-policy audits, observability, read-only mode."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "ガイド"
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

## ここに掲載されているもの

ガイドは、実行可能なコンフィグ付きの実践例です。各ガイドは、1 つの「どうすれば…できるか」という質問にエンドツーエンドで答えます。

| ガイド | 回答 |
|---|---|
| [Scheduled tasks](/ja/guides/scheduled-tasks/) | WhatsApp 経由でスケジュールされたリマインダーを rousseau に送信させるには? |
| [Self-hosted vLLM](/ja/guides/self-hosted-vllm/) | 内部ネットワーク上の vLLM エンドポイントに rousseau を接続するには? |
| [Kubernetes deployment](/ja/guides/kubernetes-deployment/) | Kubernetes の `Deployment` として rousseau を実行するには? |
| [Audit + approval policies](/ja/guides/audit-approval-policies/) | `bash` ツールを制限しながら、エージェントに有用な作業を行わせるには? |
| [Observability](/ja/guides/observability/) | rousseau の slog 出力を Loki / Grafana / Datadog に取り込むには? |
| [Read-only mode](/ja/guides/read-only-mode/) | ワークスペースを一切変更しない読み取り専用の検査エージェントとして rousseau を実行するには? |

## ガイド、コンセプト、リファレンスの読み分け

- **[Concepts](/ja/concepts/)** — エージェントループの仕組みを理解したい場合。
- **ガイド** — 具体的な運用上の課題を解決したい場合。
- **[Reference](/ja/reference/cli-commands/)** — フラグの正確なシグネチャを知りたい場合。

## 次のステップ

- [Scheduled tasks](/ja/guides/scheduled-tasks/) — オペレーターが最初に手に取ることの多いガイドです。
