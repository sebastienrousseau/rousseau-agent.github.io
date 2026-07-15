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
description: "MCP resources exposed by rousseau's stdio server today (none) and the roadmap for sessions-as-resources."
keywords: "mcp, resources, roadmap, sessions, resources/list"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/mcp/exposed-resources/"
subtitle: "What resources rousseau exposes today, and what is planned."
tags: "mcp, resources, roadmap"
title: "MCP：公開リソース"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, resources, roadmap, sessions, resources/list"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP：公開リソース"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "mcp"
order: 73
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/mcp/exposed-resources/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/exposed-resources/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "MCP：公開リソース"
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
twitter_description: "MCP resources exposed by rousseau's stdio server today (none) and the roadmap for sessions-as-resources."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP：公開リソース"
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

## 現在のステータス

rousseau の MCP サーバー (`internal/mcp/server.go`) は `Tools` capability のみを宣言します。`resources/list` に対しては空のリストを返します:

```
MethodResourcesList → okResponse(env.ID, map[string]any{"resources": []any{}})
```

意図的なものです。MCP リソースのように見えるあらゆるユースケース — 保存されたセッション、cron ジョブの説明 — は、今日ツール (`rousseau_read_session`、`rousseau_cron_list`) を通じて公開されているため、ホストはすべてのセッションを事前列挙するのではなく、必要なときに必要なデータを正確に要求できます。

## なぜ今日はリソースではないのか

MCP リソースは、ホストが控えめで明確に定義された URI (ファイル、ページ) のセットを列挙し、遅延的にデリファレンスしたい場合に光ります。rousseau のセッションストアは数千行に成長し得ます。`resources/list` 呼び出しごとにすべてのセッションを列挙すると、ホストのコンテキストが爆発します。ツール表面 (検索 / list / read) は、高カーディナリティ状態にとってより良い形状です。

## ロードマップ

MCP 仕様がページ分割リソース列挙を堅牢にサポートするようになれば、MCP リソースとして公開する価値のある 2 つの候補:

### 候補: `rousseau://sessions/<id>`

各 rousseau セッションをリソースとして。URI は次のようになります:

```
rousseau://sessions/1a2b3c4d-…
```

デリファレンスは、今日 `rousseau_read_session` が返すのと同じトランスクリプトを返します。これにより、ホストは特定のセッションをファーストクラスのシチズンとして会話にアタッチできます (「セッション 1a2b3c… をアタッチ」、ドラッグアンドドロップ)。モデルがツールを呼び出すことを覚えている必要はなくなります。

ゲーティング: リソース一覧はページ分割される必要があります。最近の MCP 仕様のバージョンはカーソルベースのページ分割を提案しています。それが実装され、ホストが実装したら、これは実現可能になります。

### 候補: `rousseau://cron/<name>`

各 cron ジョブをリソースとして。プロンプト、スケジュール、配信ターゲット、および最終実行タイムスタンプの読み取り専用検査。小さなリスト — おそらく今日列挙しても安全ですが、sessions-as-resources 形状が実証されるまで `rousseau_cron_list` と別に公開する価値はありません。

## Prompts capability

同様に今日は公開されていません。`MethodPromptsList` は `internal/mcp/server.go` の `dispatch` で `{"prompts": []any{}}` を返します。rousseau には公開する厳選されたプロンプトライブラリはありません。スキルメカニズム (`internal/skills/skills.go`) が同等の内部コンセプトであり、現在 MCP 経由では表面化されていません。

スキルロードマップが共有可能なプロンプトに収束すれば、それらを MCP プロンプトとして公開するのが自然な次のステップです。[スキル](/ja/skills/) を参照してください。

## 今日ギャップを回避する方法

MCP ホストが特定の UI アフォーダンス (例: セッションのドラッグアンドドロップ) のためにリソースを必要とする場合、回避策は:

1. チャット開始時にホストに `rousseau_list_sessions` を呼び出させる。
2. 参照したいセッション ID をコピーする。
3. その ID で `rousseau_read_session` を呼び出す。

ネイティブのリソースデリファレンスほどエルゴノミックではありませんが、機能的には同等です。

## リソース表面のリクエスト

すべてのオペレーターが MCP 経由のリソースを必要とするわけではありません。あなたのチームが必要とする場合、建設的な道筋は次を含む issue を提出することです:

- 統合している特定の MCP ホスト。
- リソースがあればより良くなるユーザー向けアクション。
- おおまかなトラフィック想定 (何セッション、どのくらいの頻度で)。

## 関連

- [MCP](/ja/mcp/) — アンブレラリファレンス。
- [MCP: 公開ツール](/ja/mcp/exposed-tools/) — 今日公開されているもの。
- [MCP: 互換性](/ja/mcp/compatibility/) — テスト済みクライアント。
- [スキル](/ja/skills/) — MCP プロンプトになり得る内部コンセプト。
