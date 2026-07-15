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
description: "Landing page for the rousseau-agent developer guide: architecture, how to add a transport, provider, or tool, testing pattern, contributing."
keywords: "developer guide, architecture, add transport, add provider, add tool, testing, contributing"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/developer-guide/"
subtitle: "アーキテクチャ、拡張ポイント、テスト、コントリビュート。"
tags: "developer-guide, architecture, extend"
title: "開発者ガイド"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "developer guide, architecture, add transport, add provider, add tool, testing, contributing"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "開発者ガイド"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 60
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/developer-guide/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "開発者ガイド"
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
twitter_description: "Landing page for the rousseau-agent developer guide: architecture, how to add a transport, provider, or tool, testing pattern, contributing."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "開発者ガイド"
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

## コントリビュータとインテグレータ向け

デベロッパーガイドは、rousseau を修正したり、そのエージェントループを独自のバイナリに組み込むために必要なすべてをカバーします。rousseau を実行したいだけの場合は、代わりに [ユーザーガイド](/ja/user-guide/cli/) をお読みください。

## ページ

| ページ | トピック |
|---|---|
| [アーキテクチャ](/ja/developer-guide/architecture/) | 層状アーキテクチャ: agent、provider、tools、transport、cli。モジュール境界。 |
| [トランスポートの追加](/ja/developer-guide/add-a-transport/) | `transport.Transport` を実装し、CLI に登録します。 |
| [プロバイダの追加](/ja/developer-guide/add-a-provider/) | `agent.Provider` (必要に応じて `agent.StreamingProvider` も) を実装します。 |
| [ツールの追加](/ja/developer-guide/add-a-tool/) | `tools.Tool` を実装し、レジストリに配線します。 |
| [テスト](/ja/developer-guide/testing/) | インターフェースによる依存性注入、フェイクジェネレータ、カバレッジ閾値。 |
| [コントリビューション](/ja/developer-guide/contributing/) | PR チェックリスト、コミットスタイル、品質ゲート。 |

## リポジトリレイアウト

```
cmd/rousseau/                 Entry point (signal handling + Execute)
internal/agent/               Session, Message, Turn, agent loop, Provider interfaces, compression
internal/cli/                 Cobra command tree (chat, per-transport commands, doctor, status, cron, mcp, skills, init, version)
internal/config/              Viper-based; flag > env > file > default precedence
internal/cron/                robfig/cron/v3 scheduler goroutine with durable job storage
internal/llm/anthropic/       Direct Anthropic API provider with cache markers
internal/llm/bedrock/         AWS Bedrock provider
internal/llm/claudecli/       Subprocess provider (claude CLI + JSON parser)
internal/llm/openai/          OpenAI-compatible provider
internal/llm/vertex/          Google Vertex AI provider
internal/mcp/                 MCP server (JSON-RPC 2.0 over stdio, spec 2024-11-05)
internal/skills/              agentskills.io-style skill loader + composition
internal/state/               Store interface + Summary type
internal/state/sqlite/        SQLite implementation (WAL, JIDMap, claude cache, FTS5 recall, cron table)
internal/tools/               Tool interface + concurrency-safe Registry
internal/tools/builtin/       read, write, edit, grep, bash
internal/transport/           Transport interface + Router
internal/transport/{whatsapp,signal,telegram,matrix,slack,discord,sms,imessage,email}/
                              Nine transport adapters
internal/tui/                 Bubble Tea model
docker/                       Dockerfile, Podman Quadlet unit
docs/                         Roadmap, gap analysis
examples/embed-agent/         Minimal library-embedding example
```

## 依存関係の方向

`agent` は `tools` が公開するインターフェース、独自の `Provider` 型、標準ライブラリにのみ依存します。具体的なプロバイダ、ストア、トランスポートは `agent` に依存します — 逆方向はありません。

これは規約と CI のリントゲートによって強制されます。`agent` から具体的なプロバイダをインポートする必要があると感じた場合、層状化が認めていないことをしています。立ち止まってください。

## 品質ゲート

すべてのコミットは、ローカルおよび CI で以下をパスする必要があります:

- `go vet ./...`
- `golangci-lint run` (18 個のリンタ、`.golangci.yml` に正確なピン留め)
- Linux と macOS 上での `go test -race -count=1 -covermode=atomic ./...`
- カバレッジ下限 (現在は合計 75%、コアパッケージは 85〜100%)
- `govulncheck ./...`
- CodeQL 静的解析 (Go)
- 再現可能ビルドの検証

ローカルではゲートを `make check` で実行します。

## 次に

- [アーキテクチャ](/ja/developer-guide/architecture/) — 地図。
- [コントリビューション](/ja/developer-guide/contributing/) — プロセス。
