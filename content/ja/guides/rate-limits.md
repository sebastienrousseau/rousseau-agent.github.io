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
description: "How rousseau-agent handles provider rate limits: 429s, exponential backoff, prompt-cache markers, and per-provider cost notes."
keywords: "rate limits, 429, backoff, retry, prompt cache, anthropic, bedrock, cost"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/guides/rate-limits/"
subtitle: "429 handling, backoff, and cache-marker optimisation."
tags: "guides, rate limits, prompt cache, anthropic"
title: "ガイド：レート制限"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "rate limits, 429, backoff, retry, prompt cache, anthropic, bedrock, cost"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ガイド：レート制限"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 36
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/guides/rate-limits/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/rate-limits/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "ガイド：レート制限"
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
twitter_description: "How rousseau-agent handles provider rate limits: 429s, exponential backoff, prompt-cache markers, and per-provider cost notes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "ガイド：レート制限"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">学べること</span><p>プロバイダーごとのレート制限、トークンあたりのコスト、リトライセマンティクス、キャッシュエコノミクス、および呼び出し側のリトライ + バックオフレシピ。信頼できる数値については各プロバイダーの料金ページを参照してください — 以下の表はスナップショットです。</p></aside>

## レート制限が発生する場所

rousseau は独自のレート制限処理を実装していません。すべてのプロバイダークライアントは上流の SDK に委任します:

- **Anthropic 直接** — `anthropic-sdk-go` が HTTP リトライを処理し、`Retry-After` を尊重し、5xx と 429 で指数バックオフを適用します。`internal/llm/anthropic/client.go` を参照してください。
- **Bedrock** — `aws-sdk-go-v2` がアダプティブリトライでスロットリングエラーを処理します。
- **Vertex** — Google auth ライブラリが独自のリトライを処理します。
- **OpenAI / OpenRouter / Ollama** — Go の OpenAI 互換クライアントが 429 を処理します。
- **claudecli** — Claude Code 独自の `claude` バイナリが制限を処理します。rousseau は単にシェルアウトします。

失敗したリクエストは `turn.failed`、`whatsapp.handler_failed`、または `cron.run_failed` の slog イベントとして表面化します。メッセージテキストにはプロバイダーのエラー文字列 (通常は推奨バックオフを含む `429 Too Many Requests`) が含まれます。

## 実際に制限に達したとき

ログでの症状:

```jsonl
{"level":"ERROR","msg":"whatsapp.handler_failed","err":"anthropic: complete: 429 Too Many Requests"}
```

rousseau は回復不能なエラーではターンを失敗として扱うため、オペレーターはトランスポート返信で失敗を見ます — デーモンは静かに飲み込みません。これは意図的です。

## レート制限の圧力を減らす

インパクトの順に 3 つのレバー:

### 1. プロンプトキャッシュマーカー (Anthropic 直接)

`internal/llm/anthropic/client.go` の `applyCacheMarkers` は、Anthropic の ephemeral プロンプトキャッシュのためにメッセージの先頭ウィンドウをマークします。`CacheableMessages > 0` の場合、システムプロンプトもキャッシュマークされます。キャッシュされた入力トークンは標準入力レートの約 10% で課金され、キャッシュヒットは標準入力レート制限予算を消費しません。

エージェント (`internal/agent/agent.go`) はマルチターンセッションでこれをオプトインします。rousseau の Go API 上でカスタムループを構築する場合は、`Request.CacheableMessages` と `Request.System` を設定してください — 浅いキャッシュヒットでもコストとレート制限の圧力の両方を削減します。

キャッシュマーカーは今日、Anthropic 直接のみです。Bedrock、Vertex、および OpenAI 互換プロバイダーはそれらを無視します。

### 2. 圧縮

トークン従量課金プロバイダー (Anthropic 直接、Bedrock、Vertex、OpenRouter) 上の長いセッションでは、圧縮を有効化してください:

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60      # from CompressionConfig default
    keep_recent: 8
```

`LLMCompressor` (`internal/agent/compressor.go`) は、メッセージ数が `trigger_messages` を超えたときにセッションの最も古いスライスを 1 つの合成ユーザーメッセージに要約し、最後の `keep_recent` メッセージを逐語的に保持します。ターンあたりのトークン数が少ない = レート制限の圧力が少ない。

圧縮はデフォルトでオフです。参照デプロイメントがサブスクリプション階層で `claudecli` を使用しており、そこではトークン数が課金されないためです。

### 3. より遅い cron 頻度

純粋なバックグラウンドデーモンの場合、cron 頻度を半分にするとリクエストも半分になります。`rousseau cron` の頻度は cron 式です — 鮮度要件が許すなら、15 分ごとから 1 時間ごとへ移行してください。

## プロバイダー別のおおよそのコスト

レート制限とトークンあたりのコストは独立して動きますが、両者は通常相関しています (有料階層はより高い制限を持ちます)。2026-07 時点の大まかなガイド:

| プロバイダー | 入力 $/MTok (Sonnet クラス) | 出力 $/MTok | キャッシュ読み取り $/MTok |
|---|---|---|---|
| `anthropic` 直接 | ~3 | ~15 | ~0.30 |
| `bedrock` (Sonnet-4.6) | ~3 | ~15 | キャッシュ: 執筆時点で N/A |
| `vertex` (Vertex 上の Anthropic) | ~3 | ~15 | キャッシュ: 執筆時点で N/A |
| `openrouter` | モデル依存 | モデル依存 | プロバイダー依存 |
| `ollama` セルフホスト | $0 | $0 | $0 (計算コストは自分持ち) |
| `claudecli` | サブスクリプション階層課金 | 含まれる | N/A |

現在の数値は各プロバイダーの料金ページから取得してください。

## SDK がリトライを使い果たしたとき

プロバイダーの SDK が諦めると、rousseau は最終エラーを表面化します。ターンは失われます — キューもディスク上のリトライもありません。2 つの緩和策:

- **同じチャネル経由でオペレーターにメッセージする。** ターン失敗はトランスポート返信で可視です。オペレーターは言い換えることができます。
- **手動で 2 番目のプロバイダーにフォールバックする。** 2 デーモンパターンについては [ガイド: マルチプロバイダー](/ja/guides/multi-provider/) を参照してください。

自動のクロスプロバイダーフェイルオーバーはロードマップ項目です。

## レート制限トラブルのデバッグ

1. `config.yaml` で `log.level: debug` を設定してください。SDK のデバッグ出力は正確な `Retry-After` 値を示します。
2. ジャーナル内で `turn.failed`、`whatsapp.handler_failed`、`cron.run_failed` を探してください。
3. 実際のクォータ消費についてプロバイダーダッシュボード (Anthropic Console、AWS CloudWatch、GCP Cloud Monitoring) を確認してください。
4. サブスクリプション階層の場合は、日次クォータのリセットに注意してください — SDK エラーには通常リセット時刻が含まれます。

## プロバイダー別クイックリファレンス

<aside class="admonition" data-type="warning"><span class="admonition-title">出典を示してください</span><p>料金と制限は予告なく変更されます。この表の数値は 2026 年半ば時点であり、参考です。信頼できる値については常にプロバイダーの現在の料金ページにリンクしてください。</p></aside>

| プロバイダー | リトライ挙動 | レートシグナル | 1M 入力あたりのコスト | 1M 出力あたりのコスト | キャッシュ読み取りコスト |
|---|---|---|---|---|---|
| `anthropic` 直接 | SDK が 5xx をリトライ; `Retry-After` 付き 429 を尊重 | `429 Too Many Requests` ヘッダがリセット時刻を運ぶ | ~$3 (Sonnet) | ~$15 (Sonnet) | ~$0.30 |
| `bedrock` | AWS SDK アダプティブリトライ | `ThrottlingException` | ~$3 (Sonnet) | ~$15 (Sonnet) | まだなし |
| `vertex` | Google SDK 指数リトライ | `429 RESOURCE_EXHAUSTED` | ~$3 (Sonnet) | ~$15 (Sonnet) | まだなし |
| `openai` | SDK が 5xx をリトライ; 429 を尊重 | `429 Too Many Requests` | モデル固有 | モデル固有 | モデル固有 |
| `openrouter` | 根底のプロバイダーへパススルー | プロバイダー依存 | モデル固有 | モデル固有 | プロバイダー依存 |
| `ollama` | SDK がリトライ; ローカルなので稀にしか発火しない | なし | $0 (計算コスト) | $0 (計算コスト) | N/A |
| `claudecli` | サブプロセスエラーが表面化; rousseau 側のリトライなし | 不透明 | サブスクリプション | サブスクリプション | 不透明 |

信頼できる情報源:

- [Anthropic 料金](https://www.anthropic.com/pricing)
- [AWS Bedrock 料金](https://aws.amazon.com/bedrock/pricing/)
- [Vertex AI 料金](https://cloud.google.com/vertex-ai/generative-ai/pricing)
- [OpenAI 料金](https://openai.com/pricing)
- [OpenRouter モデル一覧](https://openrouter.ai/models)

## 呼び出し側のリトライレシピ

rousseau は `Complete` の内部でリトライしません。エージェントライブラリを組み込む場合は、`Turn` を指数バックオフとジッター付きの独自リトライループでラップしてください:

```go
func retryTurn(ctx context.Context, ag *agent.Agent, sess *agent.Session, maxRetries int) (agent.Message, error) {
    var lastErr error
    for attempt := 0; attempt < maxRetries; attempt++ {
        m, err := ag.Turn(ctx, sess)
        if err == nil {
            return m, nil
        }
        if !isRateLimit(err) {
            return agent.Message{}, err // non-retryable
        }
        lastErr = err
        // Exponential backoff with jitter: 1s, 2s, 4s, 8s, ...
        backoff := time.Duration(1<<attempt) * time.Second
        jitter := time.Duration(rand.Int63n(int64(backoff / 2)))
        select {
        case <-time.After(backoff + jitter):
        case <-ctx.Done():
            return agent.Message{}, ctx.Err()
        }
    }
    return agent.Message{}, fmt.Errorf("giving up after %d retries: %w", maxRetries, lastErr)
}

func isRateLimit(err error) bool {
    s := err.Error()
    return strings.Contains(s, "429") || strings.Contains(s, "rate limit") || strings.Contains(s, "ThrottlingException")
}
```

## トラブルシューティング

### あらゆるリクエストで `429 Too Many Requests`

低い階層にいるか、別のワークロードがクォータを消費しています。オプション: (1) 制限の引き上げを要求する、(2) プロバイダー間で負荷を分割する、(3) サブスクリプション専用のワークロードには `claudecli` を実行する。

### 断続的な `529 Overloaded`

Anthropic のシステムが容量に達しています。アカウントごとのスロットリングではなく — リージョン全体がロードされています。バックオフでリトライしてください。

### キャッシュマーカーが設定されているのに目に見えるコスト削減がない

`CacheableMessages` が実際に設定されていることを確認してください。`internal/llm/anthropic/cache.go` の `applyCacheMarkers` はゼロに対しては no-op です。プレフィックスが安定していることも確認してください — ターンごとに再生成されるシステムプロンプトはキャッシングを打ち負かします。

### 低ボリュームでの Bedrock の `ThrottlingException`

Bedrock のクォータはアカウントごと、モデルごと、リージョンごとです。一部のモデルはデフォルトで非常に低いクォータ (1 分あたり 2–5 リクエスト) です。Service Quotas コンソールで引き上げをリクエストしてください。

### 低使用量にもかかわらず遅い API レスポンス

一部のプロバイダーは、グローバルロード下で低階層アカウントを de-prioritise します。Anthropic の `x-ratelimit-*` レスポンスヘッダは現在のバケット状態を示します — SDK アクセスがあれば検査してください。

## 関連ページ

- [プロバイダー: Anthropic](/ja/providers/anthropic/) — キャッシュマーカーの詳細。
- [設定](/ja/configuration/) — すべての圧縮ノブ。
- [ユーザーガイド: 圧縮 + 再呼び出し](/ja/user-guide/compression-recall/) — より深い圧縮議論。
- [ガイド: マルチプロバイダー](/ja/guides/multi-provider/) — エンドポイント間で負荷を分割します。
- [ガイド: レート/モデルスワップ](/ja/guides/rate-model-swap/) — 失敗時にプロバイダーをホットスワップします。

## さらに読む

- `internal/llm/anthropic/client.go` — SDK 呼び出し。
- `internal/llm/anthropic/cache.go` — キャッシュマーカーヘルパー。
- `internal/agent/agent.go` — ターン失敗が表面化する場所。
- 上記でリンクされているプロバイダー料金ページ。
