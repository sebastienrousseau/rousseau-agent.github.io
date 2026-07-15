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
description: "Configure OpenAI-compatible endpoints: OpenAI, OpenRouter, Ollama, self-hosted vLLM or LM Studio. BaseURL, model naming, streaming, and Ollama's not-required key."
keywords: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, base_url, chat completions, API key, streaming"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/providers/openai-compatible/"
subtitle: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, and any Chat Completions clone."
tags: "providers, openai, openrouter, ollama"
title: "OpenAI 互換プロバイダ"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, base_url, chat completions, API key, streaming"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "OpenAI 互換プロバイダ"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 10
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/providers/openai-compatible/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/openai-compatible/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "OpenAI 互換プロバイダ"
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
twitter_description: "Configure OpenAI-compatible endpoints: OpenAI, OpenRouter, Ollama, self-hosted vLLM or LM Studio. BaseURL, model naming, streaming, and Ollama's not-required key."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "OpenAI 互換プロバイダ"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">このページで学べること</span><p>rousseau の <code>openai</code> プロバイダが単一実装で 6 種類の異なるエンドポイント（OpenAI、OpenRouter、Ollama、vLLM、LM Studio、LiteLLM）をどう扱うか、それぞれの正確な <code>base_url</code> と <code>model</code> の値、どのエンドポイントがツール使用をサポートするかを扱います。このページと並行して <code>internal/llm/openai/client.go</code> を読んでください。</p></aside>

## 1 つの実装、多くのエンドポイント

`internal/llm/openai/` は OpenAI Chat Completions API を話します。`base_url` が設定可能なため、同じコードがあらゆる OpenAI 互換エンドポイントを扱います: OpenAI 本体、OpenRouter、together.ai、DeepInfra、セルフホストの vLLM、Ollama の OpenAI シム、LM Studio、LiteLLM。

プロバイダ名は `openai`、`openrouter`、`ollama` のいずれかで、それぞれが独自のコンフィグブロックに対応し、`base_url` が事前設定されます（`internal/config/config.go` の `setDefaults` を参照）。汎用スロットとして `openai` を使い、セルフホストバックエンドを指す際に `base_url` を上書きしてください。

## エンドポイントレシピ

<div class="tabs" data-tabs="openai-compat-endpoints">
  <div class="tab-list" role="tablist" aria-label="OpenAI-compatible endpoint">
    <button role="tab" aria-selected="true">OpenAI</button>
    <button role="tab" aria-selected="false">OpenRouter</button>
    <button role="tab" aria-selected="false">Ollama</button>
    <button role="tab" aria-selected="false">vLLM</button>
    <button role="tab" aria-selected="false">LM Studio</button>
    <button role="tab" aria-selected="false">LiteLLM</button>
  </div>
  <div class="tab-panel" role="tabpanel">

OpenAI 直接。`api.openai.com/v1` は SDK デフォルトです。`base_url` の上書きは不要です。

```yaml
provider: openai

openai:
  api_key: sk-...
  model: gpt-5
  max_tokens: 4096
```

ツール使用: あり（ネイティブ `tools` 配列）。ストリーミング: あり（SSE）。

<aside class="admonition" data-type="note"><span class="admonition-title">モデル命名</span><p>モデル ID は OpenAI 独自の命名（<code>gpt-4o</code>、<code>gpt-5</code>、<code>o1</code>、<code>o3-mini</code>）に従います。本番では正確な ID を固定してください。エイリアスは意図せずシフトすることがあります。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

OpenRouter は 1 つの API の背後に数十のプロバイダを集約します。モデル ID は `provider/model` 規約を使います。

```yaml
provider: openrouter

openrouter:
  api_key: sk-or-...
  model: anthropic/claude-sonnet-4-6
```

`base_url` のデフォルトは `https://openrouter.ai/api/v1` です。ツール使用は基盤プロバイダに依存します。Anthropic と OpenAI のモデルは動作しますが、多くのオープンウェイトモデルは動作しません。

<aside class="admonition" data-type="tip"><span class="admonition-title">無料層モデル</span><p>OpenRouter は実験用に無料層バリアント（<code>:free</code> サフィックス）を公開しています。レート制限と日次クォータが適用されます。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

ローカルの Ollama は `http://localhost:11434/v1` に Chat Completions 互換シムを公開します。

```yaml
provider: ollama

ollama:
  model: llama3.1:8b
```

`ollama.api_key` はデフォルトで `not-required` です（シムは無視しますが、SDK は空文字列を拒否します。`internal/llm/openai/client.go` の `New` を参照）。`ollama.base_url` はデフォルトで `http://localhost:11434/v1` です。

ツール使用: Ollama 0.4+ 以降はあり（Chat Completions リクエストの `tools` 配列経由）。それより古いビルドはプレーンテキストを返します。

<aside class="admonition" data-type="warning"><span class="admonition-title">レイテンシ</span><p>ノートパソコン上の CPU のみの Ollama は 1 ターンあたり数十秒かかることがあります。呼び出し側の HTTP タイムアウトを 60 秒以上に設定するか、GPU バックのホストを使ってください。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

vLLM は本番グレードのセルフホストエンジンです。認証が欲しい場合は `--api-key` 付きで起動します。

```sh
python -m vllm.entrypoints.openai.api_server \
  --model mistralai/Mixtral-8x22B-Instruct-v0.1 \
  --host 0.0.0.0 --port 8000 \
  --api-key sk-vllm-secret
```

```yaml
provider: openai

openai:
  api_key: sk-vllm-secret
  base_url: http://vllm.internal:8000/v1
  model: mistralai/Mixtral-8x22B-Instruct-v0.1
  max_tokens: 4096
```

ツール使用: ツール使用チャットテンプレートを持つモデル（`Hermes-2-Pro`、`Mistral-Nemo`、`Llama-3.1-8B-Instruct` 以上）ではあり。ストリーミング: あり。完全なデプロイは [ガイド: セルフホスト vLLM](/ja/guides/self-hosted-vllm/) を参照してください。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

LM Studio は `http://localhost:1234/v1` に OpenAI 互換サーバーを出荷します。

```yaml
provider: openai

openai:
  api_key: not-required
  base_url: http://localhost:1234/v1
  model: lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF
```

ツール使用: 現行ビルド（2026 年中頃時点）では **サポートされていません**。エンドポイントは `tools` 配列を受け付けますが無視してプレーンテキストを返します。チャット専用ワークロードに使うか、機能実装を待ってください。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

LiteLLM は多くのプロバイダを 1 つの API の背後に置くプロキシです。rousseau をそこに向けます。

```yaml
provider: openai

openai:
  api_key: sk-litellm-...
  base_url: http://litellm.internal:4000
  model: bedrock/anthropic.claude-sonnet-4-6-20260101-v1:0
```

注意: LiteLLM のデフォルトポートは 4000 で、`/v1` プレフィックスはデプロイ方法によってはオプションです。バージョン別に LiteLLM のドキュメントに従ってください。

ツール使用: 基盤プロバイダに透過的にパススルー。ストリーミング: あり。LLM トラフィックの単一チョークポイント（レート制限、予算追跡、監査）を望むチームに有用です。

  </div>
</div>

## 設定リファレンス

| フィールド | デフォルト | 効果 |
|---|---|---|
| `api_key` | *必須* | Bearer トークン。認証を無視するローカルエンドポイントには `not-required` を使ってください。 |
| `model` | *必須* | モデル識別子。エンドポイント横断の共通デフォルトはありません。 |
| `base_url` | *プロバイダ名依存* | エンドポイントを上書き。`setDefaults` のプリセットを参照。 |
| `max_tokens` | SDK デフォルト | 補完 1 回あたりの出力トークン上限。 |

`openai`、`openrouter`、`ollama` プロバイダ名はそれぞれ独自のコンフィグブロック（`OpenAIConfig`、`OpenAIConfig`、`OpenAIConfig`）にマップされます。同じ形状を共有しますが、1 つの `config.yaml` に複数エンドポイントを設定し、`provider:` を変えて切り替えられます。

## ストリーミング

プロバイダは SSE 経由で `agent.StreamingProvider` を実装します。上記のすべてのエンドポイントはストリーミングをサポートします。Ollama のシムには最近のビルド（0.5+）が必要です。

## ツール使用

`Registry` からのツール定義は `internal/llm/openai/client.go` で OpenAI の `tools` 配列に変換されます。すべての OpenAI 互換エンドポイントがツール使用をサポートするわけではありません。有効化前にバックエンドを確認してください。Ollama は 0.4 以降サポートしますが、古い LM Studio ビルドはサポートしません。

`tool_calls` を返すエンドポイントには承認ポリシーが適用されます。ツール使用非対応のエンドポイントはプレーンテキストを返し、`Registry` は参照されません。

## 注意点

- **モデル命名。** エンドポイントごとに独自の規約があります: OpenAI（`gpt-5`）、OpenRouter（`anthropic/claude-sonnet-4-6`）、Ollama（`llama3.1:8b`）、vLLM（HuggingFace 名）。エンドポイント横断のポータビリティはありません。
- **空の API キー。** SDK は空文字列を拒否します。認証不要のローカルエンドポイントには `not-required`（または任意のプレースホルダ）を渡してください。
- **BaseURL の末尾スラッシュ。** `/v1` パスセグメントを含めてください。末尾スラッシュは含めないでください。
- **タイムアウト。** CPU 上のローカル Ollama は 1 ターンあたり数十秒かかることがあります。プロバイダを自前でラップする場合、HTTP クライアントのタイムアウトを引き上げてください。`rousseau` は SDK デフォルトを使用します。
- **ツール使用の差異。** OpenAI と OpenRouter 経由の Anthropic は確実にツールをサポートします。Ollama は最近のビルドとツール使用チャットテンプレートを持つモデルが必要です。LM Studio はツールをサポートしません。`tool_calls` がプレーンテキストで届く場合、`Registry` は参照されません。
- **Reasoning モデル。** OpenAI o1/o3 系列は挙動が異なります: `max_tokens` は `max_completion_tokens` に置き換わり、システムプロンプトが制限されます。SDK が処理しますが、ターンあたりのレイテンシは長くなります。

## トラブルシューティング

### `openai: complete: 401 Unauthorized`

API キーが誤りか欠落しています。OpenRouter では `sk-or-…` トークンを使ってください。ローカルエンドポイントでは、エンドポイントが無視するとしても `api_key` が空でないことを確認してください。

### `openai: complete: 404 model not found`

`model` 文字列がエンドポイントの認識するものと一致しません。OpenRouter ではプロバイダプレフィックスを含めてください（`claude-sonnet-4-6` ではなく `anthropic/claude-sonnet-4-6`）。Ollama ではモデルが pull されていることを確認してください（`ollama pull llama3.1:8b`）。

### モデルが `tools` を無視する

エンドポイントがこのモデルのツール使用をサポートしていません。既知の良好なエンドポイント（OpenAI、Anthropic 直接、OpenRouter に Anthropic モデル）で同じモデルを指して確認してください。上のレシピのツール使用列を参照してください。

### ローカル Ollama で `context deadline exceeded`

CPU 推論は遅いです。オプション: (1) 呼び出し側のタイムアウトを引き上げる、(2) GPU ホストで Ollama を実行、(3) より小さいモデルに切り替え（`70b` ではなく `llama3.1:8b`）。

### 応答の途中でストリーミングが停止する

一部のプロキシ（LiteLLM、企業 egress プロキシ）は SSE をバッファリングします。プロキシで `text/event-stream` のバッファリングを無効化するか、rousseau をエンドポイントと同じネットワークセグメントで実行してください。

## 関連ページ

- [ガイド: セルフホスト vLLM](/ja/guides/self-hosted-vllm/) — 本番デプロイ。
- [プロバイダ: Anthropic](/ja/providers/anthropic/) — Claude の直接 API 代替。
- [ガイド: マルチプロバイダ](/ja/guides/multi-provider/) — トランスポート別に異なるプロバイダを運用。
- [ガイド: レート制限](/ja/guides/rate-limits/) — プロバイダ別のリトライ手引き。
- [設定](/ja/configuration/) — 文脈内の `openai`/`openrouter`/`ollama` スタンザ。

## さらに読む

- `internal/llm/openai/client.go` — `Complete`、メッセージ変換、ツールスキーマ。
- `internal/llm/openai/client.go` — ストリーミング実装。
- `internal/config/config.go` — `OpenAIConfig` 構造体、`base_url` プリセットの `setDefaults`。
