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
description: "Configure the direct Anthropic provider: ANTHROPIC_API_KEY, model IDs, max_tokens, prompt cache markers on the last messages, streaming."
keywords: "Anthropic, ANTHROPIC_API_KEY, Claude API, prompt caching, cache_control, ephemeral, streaming"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/providers/anthropic/"
subtitle: "Direct Anthropic API with ephemeral prompt-cache markers."
tags: "providers, anthropic"
title: "Anthropic プロバイダ"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Anthropic, ANTHROPIC_API_KEY, Claude API, prompt caching, cache_control, ephemeral, streaming"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Anthropic プロバイダ"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 7
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/providers/anthropic/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/anthropic/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Anthropic プロバイダ"
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
twitter_description: "Configure the direct Anthropic provider: ANTHROPIC_API_KEY, model IDs, max_tokens, prompt cache markers on the last messages, streaming."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Anthropic プロバイダ"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">このページで学べること</span><p>rousseau が送信する Anthropic リクエストの正確なワイヤレベル形状、どのコンテンツブロックがプロンプトキャッシュマーカーを受け取りなぜそうなるか、ストリーミングが <code>agent.StreamingProvider</code> にどうマップされるか、401/429/529 応答の失敗モードを扱います。このページと並行して <code>internal/llm/anthropic/client.go</code> と <code>internal/llm/anthropic/cache.go</code> を読んでください。</p></aside>

## Anthropic プロバイダを使う場面

直接の `anthropic` プロバイダは次の場合に最適です。

- Anthropic API キーを持っており、`api.anthropic.com` でトークン単位の課金を希望する場合。
- rousseau 側のツール実行が欲しい（`Registry` が完全に有効）場合。
- 安定した接頭辞に対する ephemeral プロンプトキャッシュマーカーをオプトインしたい場合。
- `rousseau chat` でストリーミング補完が欲しい（トークンごとにビューポートを更新）場合。
- 明示的で公開されたレート制限が欲しい（`claudecli` のサブスクリプションモードとは異なる）場合。

## 設定

```yaml
provider: anthropic

anthropic:
  api_key: sk-ant-...
  model: claude-sonnet-4-6
  max_tokens: 4096
```

| フィールド | デフォルト | 効果 |
|---|---|---|
| `api_key` | *`ANTHROPIC_API_KEY` から* | `api.anthropic.com` の Bearer。プロバイダが選択されているのに空だと拒否されます。 |
| `model` | `claude-sonnet-4-6` | モデル識別子。 |
| `max_tokens` | `4096` | 補完 1 回あたりの出力トークン上限。 |

環境変数 `ANTHROPIC_API_KEY` はロード時に `anthropic.api_key` にバインドされるため、エクスポートすることは設定することと同等です。コンテナオペレーターは通常、`config.yaml` にコミットするのではなく、systemd ユニットの `Environment=` 行でエクスポートします。

## モデル識別子

`rousseau-agent` は `model` を SDK にそのまま渡します。本番では正確なモデル ID（`claude-sonnet-4-6`、`claude-opus-4-6`）を固定してください。Anthropic が新しいスナップショットを昇格させた際にトラフィックが意図せずシフトしないようにするためです。

## プロンプトキャッシュ内部

Anthropic の ephemeral プロンプトキャッシュは、コンテンツブロックを `cache_control: { type: "ephemeral" }` でマークできます。API は cache-marked ブロックまでの接頭辞をキャッシュし、同じ接頭辞を持つ後続ターンは通常の入力トークンコストの一部（執筆時点で 10 %。現行の価格は Anthropic ドキュメントを参照）で済みます。

Rousseau は `internal/llm/anthropic/cache.go` の `applyCacheMarkers` でマーカーを付与します。送信 `Request` で `CacheableMessages > 0` の場合、2 つのことが起きます。

1. **システムプロンプトに `cache_control: ephemeral` が付与される。** これは毎ターン残るため、オプトインすればキャッシュする価値が常にあります。`internal/llm/anthropic/client.go` の 68–75 行目を参照してください。
2. **直近 `CacheableMessages` 件のメッセージ** の最後のテキストブロックに `cache_control: ephemeral` が付与されます。これによりセッションが伸びても安価に保てます。新しいターンが追加されるとマーカーはトランスクリプトを下って浮かびますが、前のマーカーまでの接頭辞は依然としてホットのままです。

### マークされるブロック

`markLastTextBlock` は `MessageParam` のコンテンツを後ろから走査し、最初に見つけたテキストブロックに `CacheControl` を設定します。`tool_use` と `tool_result` ブロックはスキップされます。SDK はそれらを独自のオプション `CacheControl` フィールドを持つ別のバリアントとしてモデル化しており、テキストが安全な共通因子だからです。`internal/llm/anthropic/cache.go` を参照してください。

### 元を取れる条件

<aside class="admonition" data-type="note"><span class="admonition-title">キャッシングの経済性</span><p>損益分岐点はキャッシュされた接頭辞がどれだけ再利用されるかに依存します。5–10 kB のシステムプロンプト（スキルロード時に典型的）でセッションあたり 20–100 ターンを実行するチャットトランスポートでは、キャッシュ有効化により通常入力トークン費を半減できます。単発の cron ジョブが 1 回だけ返信を生成する場合、節約はありません。</p></aside>

`Compressor` は書き換え後に `CacheableMessages = len(recentMessages) - 1` を設定し、新しい要約ブロックが次のターンでキャッシュホットになるようにします。他のコード経路は `CacheableMessages = 0` のままにするため、キャッシングはリクエスト単位のオプトインです。プロバイダを直接呼び出す組み込み側は明示的に設定してください。

### キャッシュヒットの検証

Anthropic API はすべてのレスポンスで `usage.cache_read_input_tokens` と `usage.cache_creation_input_tokens` を返します。`agent.Usage` は現状 `InputTokens` と `OutputTokens` のみを公開しているため、内訳の検証にはデバッグロギングの有効化か、SDK の生レスポンスの読み取りが必要です。これは `docs/GAP_ANALYSIS_2026.md` で追跡している既知の可観測性ギャップです。

## ストリーミングセマンティクス

プロバイダは `agent.StreamingProvider` を実装します。`rousseau chat` はデフォルトでストリーミングを使用し、トークンが到着するに従って TUI ビューポートに反映します。チャットトランスポート（WhatsApp、Slack、Discord など）は非ストリーミング補完を使用します。メッセージ指向のトランスポートはどのみち配信をバッチ化するため、中間デルタストリームは最終メッセージ送信前に破棄されるだけだからです。

`internal/llm/anthropic/stream.go` のストリーミング実装は、SDK の `MessageStreamEvent` union を消費します。

| イベント | 処理内容 |
|---|---|
| `message_start` | `agent.StreamEvent{Kind: StreamMessageStart}` を発行。 |
| `content_block_start` | ブロック種別を伴う `agent.StreamEvent{Kind: StreamContentStart}` を発行。 |
| `content_block_delta` | テキストには `agent.StreamEvent{Kind: StreamTextDelta, Text: delta.Text}` を発行。`input_json_delta` イベントは部分的な tool-use 入力に蓄積します。 |
| `content_block_stop` | `agent.StreamEvent{Kind: StreamContentStop}` を発行。 |
| `message_delta` | 最終的な stop reason と累積使用量を運びます。 |
| `message_stop` | ストリーム終了。 |

Bubble Tea TUI はこれらのイベントを `agent.StreamTurn` 経由で購読します。これがストリーム / tool-use ループを制御します。`internal/agent/stream_turn.go` を参照してください。

## ツール使用

`Registry` からのツール定義は `toSDKTools` で Anthropic の `tools` 配列に変換されます。承認ポリシー（`agent.approver`）が適用されます。すべての `tool_use` ブロックは実行前にエージェントループで `Approver.Approve` を通ります。拒否は `is_error: true` の `tool_result` ブロックとしてモデルに返され、モデルは適応（別のアクションを選ぶ、ユーザーに尋ねる、優雅に諦める）できます。

<aside class="admonition" data-type="warning"><span class="admonition-title">スキーマ形状</span><p>SDK はツールの <code>input_schema</code> がトップレベル <code>properties</code> フィールドを持つ JSON Schema オブジェクトであることを期待します。Rousseau の <code>tools.Definition</code> は 1:1 でマップされます（<code>internal/llm/anthropic/client.go</code> の <code>toSDKTools</code> を参照）。非オブジェクトスキーマを発するカスタムツールはリクエスト時に失敗します。</p></aside>

## レート制限の処理

Anthropic API は次を返します。

| コード | 意味 | rousseau の挙動 |
|---|---|---|
| 401 | キーが不正または欠落 | 即失敗、リトライなし。 |
| 400 | 不正なリクエスト（スキーマ、エンコーディング、プロンプトが長すぎる） | SDK のエラーメッセージとともに即失敗。 |
| 429 | 分単位のレート制限超過 | `agent` エラーとして表面化。`Complete` はリトライしません。 |
| 529 | 過負荷（一時的な容量不足） | `agent` エラーとして表面化。`Complete` はリトライしません。 |
| 5xx | サーバーエラー | `agent` エラーとして表面化。`Complete` はリトライしません。 |

**リトライは呼び出し側の責任です。** `rousseau chat` TUI とトランスポートの `RouterHandler` は現在バックオフを実装していません。429 はターンを終わらせます。これは意図的な設計判断です: リトライは tool_use のセマンティクス（部分的なツール呼び出し、冪等性）と絡み、正しい判断を下すコンテキストは呼び出し側にあります。予定されているリトライヘルパについては `docs/GAP_ANALYSIS_2026.md` を参照してください。

<aside class="admonition" data-type="tip"><span class="admonition-title">チャットトランスポートでの 429 処理</span><p>トランスポートの <code>RouterHandler</code> を、指数バックオフとジッタを持つ呼び出し側レベルのリトライループでラップしてください。<a href="/ja/guides/rate-limits/">レート制限ガイド</a> に完成例があります。</p></aside>

## コスト衛生

- **`max_tokens` を低く設定する**（2048–4096）。返信が数段落を超えることの稀なチャットトランスポート向け。`max_tokens` は上限であり目標ではありません。実際に生成された出力にのみ課金されます。
- **`agent.compression` を有効化** して、トランスクリプトが `trigger_messages`（デフォルト 60）を超えたら古いメッセージを畳み込みます。要約は生のトランスクリプトよりずっと安価です。
- エージェントライブラリを組み込む場合は **`CacheableMessages > 0` を使用** してください。直接 API はプロンプトキャッシュが最も効果を発揮する場所です。
- **tool-use ループには Sonnet を優先** してください。Opus はより高価で遅いです。特定のタスクで測定した勝利がない限り、Sonnet がデフォルトなのには理由があります。
- **ストリーム中断の課金に注意。** 応答途中でストリームがキャンセルされても、API はキャンセル時点までに生成されたトークンに課金します。呼び出し側でタイムアウトの上限を設定してください。

## トラブルシューティング

### `anthropic: complete: 401 unauthorized`

`ANTHROPIC_API_KEY` が欠落、失効、またはアクセス権のなくなったワークスペース / 組織に設定されています。`curl -H "x-api-key: $ANTHROPIC_API_KEY" https://api.anthropic.com/v1/messages` で確認してください。

### `anthropic: complete: 400 messages: too many messages`

トランスクリプトがコンテキストウィンドウを超えて成長しました。`agent.compression.enabled: true` を有効化（デフォルトで通常は問題なし）し再実行してください。圧縮が有効でも発火し続ける場合は、`trigger_messages` を下げるか `keep_recent` を上げて圧縮をより早く発火させます。

### `anthropic: unsupported content block <type>`

SDK が rousseau のモデル化していないコンテンツブロック種別を返しました。現在サポートされているのは `text` と `tool_use` のみです（`fromSDKResponse` を参照）。モデルが `thinking` ブロック（extended thinking モード）を発する場合に起こり得ます。rousseau はまだこれらを表面化していません。サポートが実装されるまでプロバイダコンフィグで extended thinking を無効化してください。

### 継続負荷下での 429

分単位の出力トークンレート制限に当たっています。オプション: (1) Anthropic に上限引き上げを要請、(2) 呼び出し側でターンをキューし直列処理、(3) エンタープライズクォータが通常より高い Bedrock か Vertex に切り替え。

### `CacheableMessages > 0` にもかかわらずキャッシュミスする

Anthropic は接頭辞が変わるとキャッシュを無効化します。よくある原因: ターンごとにシステムプロンプトが再生成される（ユーザーメッセージごとに変わるスキル）、モデル ID の変更、`MaxTokens` の相違。リクエストペイロードをログ出力し、2 つのターン間で diff して切り分けてください。

## 関連ページ

- [プロバイダ: claudecli](/ja/providers/claudecli/) — サブプロセスと直接 API のトレードオフ。
- [プロバイダ: Bedrock](/ja/providers/bedrock/) — エンタープライズクォータを持つ AWS マネージド Claude。
- [ガイド: レート制限](/ja/guides/rate-limits/) — リトライとバックオフの手引き。
- [エージェントループ](/ja/agent-loop/) — ストリーミングとツール使用の組み合わせ方。
- [ユーザーガイド: 圧縮 & リコール](/ja/user-guide/compression-recall/) — 入力トークン数を健全に保つ仕組み。

## さらに読む

- `internal/llm/anthropic/client.go` — `Complete`、メッセージ変換、ツールスキーマ。
- `internal/llm/anthropic/stream.go` — ストリーミング実装。
- `internal/llm/anthropic/cache.go` — キャッシュマーカーヘルパ。
- `internal/agent/stream_turn.go` — エージェントループがストリーミングイベントをどう消費するか。
- `internal/agent/compressor.go` — 圧縮器が `CacheableMessages` をどう仕込むか。
