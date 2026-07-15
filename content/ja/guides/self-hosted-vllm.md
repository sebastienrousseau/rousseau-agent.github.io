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
description: "Worked example: point rousseau-agent at a self-hosted vLLM endpoint on your internal network via the OpenAI-compatible provider."
keywords: "vllm, self-hosted, openai-compatible, air-gapped, internal network, local llm"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/guides/self-hosted-vllm/"
subtitle: "Point rousseau at a vLLM endpoint on your internal network."
tags: "guides, vllm, self-hosted, openai-compatible"
title: "ガイド：セルフホスト vLLM"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "vllm, self-hosted, openai-compatible, air-gapped, internal network, local llm"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ガイド：セルフホスト vLLM"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 32
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/guides/self-hosted-vllm/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/self-hosted-vllm/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "ガイド：セルフホスト vLLM"
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
twitter_description: "Worked example: point rousseau-agent at a self-hosted vLLM endpoint on your internal network via the OpenAI-compatible provider."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "ガイド：セルフホスト vLLM"
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

## シナリオ

内部マシン (`llm.internal:8000`) で vLLM インスタンスが open-weights コーディングモデルを提供しています。推論トラフィックはネットワークから出せません。rousseau をそこに向け、そのエンドポイントを他の任意の OpenAI 互換ターゲットと同じように扱います。

vLLM は OpenAI Chat Completions スキーマを実装しているため、rousseau の `openai` プロバイダーはそのまま動作します。LM Studio、Ollama、Text Generation Inference も同じパターンです。

## 前提条件

- `http://llm.internal:8000/v1` で vLLM が既に起動しており、`/v1/chat/completions` が curl スモークテストに応答すること。
- vLLM を起動したモデルタグ (例: `Qwen/Qwen3-Coder-30B`)。

## ステップ 1 — vLLM を確認する

```sh
curl -fsS http://llm.internal:8000/v1/models
curl -fsS http://llm.internal:8000/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{
    "model": "Qwen/Qwen3-Coder-30B",
    "messages": [{"role": "user", "content": "say hi"}]
  }' | jq .
```

両方ともエラーなしで返る必要があります。2 つ目の呼び出しが 4xx を返す場合は、先に vLLM を修正してください — rousseau のクライアントは薄い JSON シムであり、そのエラー表面を継承します。

## ステップ 2 — rousseau を vLLM に配線する

`~/.config/rousseau/config.yaml` を編集:

```yaml
provider: openai

openai:
  base_url: http://llm.internal:8000/v1
  api_key: not-required        # vLLM ignores the key but the client sends one
  model: Qwen/Qwen3-Coder-30B
  max_tokens: 4096

log:
  level: info
  format: json
```

`openai` プロバイダーは `openrouter` および `ollama` とスキーマを共有します。唯一の違いはプリセットの `base_url` です。`base_url` を明示的に設定するとデフォルトを上書きします。

## ステップ 3 — TUI でスモークテストする

```sh
rousseau chat
```

`explain the difference between goroutines and threads in two paragraphs.` と入力して送信してください。返信がストリーミングされてくれば、配線は正しいです。

されない場合:

```sh
rousseau doctor
```

`provider.selected` の行は `openai` を示します。`provider.openai.base_url` の到達性で `fail` になる場合は、DNS または内部ネットワークパスが壊れているのであり、rousseau ではありません。

## ステップ 4 — ツール利用をオンにする

コーディングモデルはツール利用の忠実性が様々です。rousseau のエージェントループは、モデルがツールの `InputSchema` に対して検証される JSON を持つ `tool_use` ブロックを発することを期待します。vLLM のモデルが OpenAI のツール利用スキーマをネイティブにサポートしていない場合:

- `provider: openai` + それをサポートするモデルから始めてください (最近の Qwen、Mistral、Llama 3.1 8B+ バリアントがこれを謳っています)。
- または vLLM を [vLLM の OpenAI 互換 tool_choice アダプタ](https://docs.vllm.ai/) のようなシムでラップし、再検証してください。

ツール利用が動作すれば、コーディングツール (read、write、edit、grep、bash) は他の任意のプロバイダーと同じように利用可能になります。

## ステップ 5 — 承認ポリシーを検討する

セルフホストのモデルは、フロンティアモデルよりもリスク認識が低い傾向にあります。`pattern` モードの承認者で `bash` ツールをロックするのが賢明です:

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read,  match: ".*"}
      - {tool: grep,  match: ".*"}
      - {tool: edit,  match: "^./workspace/.*"}
      - {tool: bash,  match: "^(ls|cat|grep|rg|find|git status|git diff) "}
    deny:
      - {tool: bash,  match: "rm -rf|sudo|curl|wget|chmod|chown"}
```

より詳細なウォークスルーについては [ガイド: 監査 + 承認ポリシー](/ja/guides/audit-approval-policies/) を参照してください。

## ステップ 6 — パフォーマンスを監視する

セルフホストエンドポイントは、より高い `max_iterations` (エージェントループが同じ結論に至るためにより多くのラウンドトリップを必要とする場合がある) から、そして常にセッション圧縮を有効化することから恩恵を受けることが多いです:

```yaml
agent:
  max_iterations: 48
  compression:
    enabled: true
    trigger_messages: 60
    keep_recent: 8
```

圧縮はデフォルトでオフです。要約に LLM ターンを使用するためです。トークン従量課金のパブリック API では、これは無駄になり得ます。セルフホストエンドポイントではトークンコストがゼロなので、オンのままにしておいてください。

## vLLM の代替

同じレシピが以下に適用されます:

- **Ollama** — `provider: ollama` を使用してください (`base_url` はデフォルトで `http://localhost:11434/v1`、`api_key` は `not-required`)。
- **LM Studio** — `provider: openai` を使用し、`base_url` を LM Studio サーバー (`http://host:1234/v1`) に向けてください。
- **TGI (Text Generation Inference)** — `provider: openai` を使用し、`base_url` を TGI の OpenAI 互換エンドポイントに向けてください。
- **OpenRouter** — `provider: openrouter` を使用してください (`base_url` はデフォルトで `https://openrouter.ai/api/v1`)。

## 注意事項

- プロバイダーがストリーミングしない場合、rousseau はストリーミングしません。一部の vLLM ビルドはストリーミングを無効化して出荷されます — より良い TUI 体験のためにオンにしてください。
- プロンプトキャッシング (`internal/llm/anthropic` は `cache_control` マーカーを使用) は Anthropic 固有であり、vLLM に対しては何もしません。これは主に、トークン従量課金プロバイダーでの長寿命セッションで重要です。
- [openai 互換プロバイダーページ](/ja/providers/openai-compatible/) は、あらゆるノブの決定版リファレンスです。

## 次に

- [OpenAI 互換プロバイダー](/ja/providers/openai-compatible/) — すべての config フィールド。
- [監査 + 承認ポリシー](/ja/guides/audit-approval-policies/) — アライメントの弱いモデルのためのセーフティ姿勢。
- [オフライン](/ja/offline/) — アウトバウンドインターネットなしで rousseau を実行します。
