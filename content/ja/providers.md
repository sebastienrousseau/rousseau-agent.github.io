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
description: "Overview of the five LLM provider families supported by rousseau-agent: claudecli, Anthropic, AWS Bedrock, Google Vertex AI, and any OpenAI-compatible endpoint."
keywords: "providers, LLM, Anthropic, Bedrock, Vertex, OpenAI, OpenRouter, Ollama, claudecli"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/providers/"
subtitle: "5 種類の LLM プロバイダを 1 つの Provider インターフェースで扱う。"
tags: "providers, LLM"
title: "プロバイダ"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "providers, LLM, Anthropic, Bedrock, Vertex, OpenAI, OpenRouter, Ollama, claudecli"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "プロバイダ"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 5
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/providers/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "プロバイダ"
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
twitter_description: "Overview of the five LLM provider families supported by rousseau-agent: claudecli, Anthropic, AWS Bedrock, Google Vertex AI, and any OpenAI-compatible endpoint."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "プロバイダ"
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

## Provider インターフェース

すべての LLM バックエンドは `agent.Provider` を実装します:

```go
type Provider interface {
    Name() string
    Complete(ctx context.Context, req Request) (Response, error)
}
```

`StreamingProvider` バリアントはトークン単位の配信のために `CompleteStream` を追加します。6 番目のバックエンドの追加は、1 つの `Complete` 実装と `internal/cli/provider.go` での配線だけです。

## サポートするファミリ

| プロバイダ | 認証モデル | エンドポイント | ストリーミング | プロンプトキャッシング | 推奨用途 |
|---|---|---|:---:|:---:|---|
| [claudecli](/ja/providers/claudecli/) | `claude` CLI の認証を継承 | ローカルサブプロセス | あり | サブプロセス経由 | 個人オペレーター、サブスクリプション階層の Claude Code |
| [Anthropic](/ja/providers/anthropic/) | `ANTHROPIC_API_KEY` | `api.anthropic.com` | あり | エフェメラルマーカー | Anthropic API を使うチーム |
| [AWS Bedrock](/ja/providers/bedrock/) | AWS 認証情報チェーン | `bedrock-runtime.<region>.amazonaws.com` | あり | SDK 経由 | AWS 上のエンタープライズ |
| [Google Vertex AI](/ja/providers/vertex/) | サービスアカウントまたは ADC | `<region>-aiplatform.googleapis.com` | あり | SDK 経由 | GCP 上のエンタープライズ |
| [OpenAI 互換](/ja/providers/openai-compatible/) | ベアラトークン | `api.openai.com` またはオーバーライド | あり | プロバイダ依存 | OpenAI、OpenRouter、Ollama、vLLM、LM Studio |

## プロバイダの選択

`~/.config/rousseau/config.yaml` の先頭で `provider` キーを設定します:

```yaml
provider: anthropic

anthropic:
  api_key: sk-ant-...
  model: claude-sonnet-4-6
```

またはシェルで上書きします:

```sh
ROUSSEAU_PROVIDER=bedrock rousseau chat
```

`ANTHROPIC_API_KEY` はロード時に `anthropic.api_key` にバインドされるため、環境変数で渡しても等価です。

## 各プロバイダがツール使用する場所

`claudecli` プロバイダは、`claude` サブプロセス内で独自のツール使用ループを実行します。rousseau の `Registry` に登録されたツールは、このプロバイダでは呼び出され **ません**。`Response` は常に claude の最終回答を含む単一のターン終了テキストメッセージです。

その他すべてのプロバイダ (`anthropic`、`bedrock`、`vertex`、`openai`) は rousseau の `Registry` を使用します。ツール定義は各プロバイダパッケージによって、プロバイダが期待する JSON 形状に変換されます。
