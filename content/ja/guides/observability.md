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
description: "Wire rousseau-agent's slog JSON output to Loki, Grafana, Datadog, or any log pipeline. OpenTelemetry roadmap notes."
keywords: "observability, slog, json logging, loki, grafana, datadog, opentelemetry"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/guides/observability/"
subtitle: "Slog JSON into your log pipeline. OTel on the roadmap."
tags: "guides, observability, slog, loki, grafana, datadog"
title: "ガイド：可観測性"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "observability, slog, json logging, loki, grafana, datadog, opentelemetry"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ガイド：可観測性"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 35
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/guides/observability/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/observability/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "ガイド：可観測性"
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
twitter_description: "Wire rousseau-agent's slog JSON output to Loki, Grafana, Datadog, or any log pipeline. OpenTelemetry roadmap notes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "ガイド：可観測性"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">このページで学べること</span><p>rousseau が出力する slog の属性キー、構造化 JSON との相性がよいログパイプライン (Loki + Grafana、Datadog、Vector、OTel Collector)、および OTel のロードマップが実装された際のトレースについての呼び出し側のスケッチを扱います。</p></aside>

## rousseau が出力するもの

すべてのデーモンは Go 標準ライブラリの `log/slog` パッケージを使用します。`log.format` によって 2 つのハンドラーから選択できます。

| 値 | ハンドラー | 用途 |
|---|---|---|
| `text` (デフォルト) | `slog.NewTextHandler` | 対話的な `rousseau chat`。色付けはオフで、grep しやすい。 |
| `json` | `slog.NewJSONHandler` | 本番のデーモン全般。各フィールドは JSON キーです。 |

レベル: `debug`、`info`、`warn`、`error`。

本番用のコンフィグ:

```yaml
log:
  level: info
  format: json
```

## 信頼できる構造化キー

以下のキーはコード上重要な意味を持ちます。パースはしても書き換えないでください。これらは `internal/cli/` および `internal/agent/` 全体に現れます。

| キー | 発行元 | フィールド | 意味 |
|---|---|---|---|
| `tool.execute` | `agent.runTools` | `name`, `id` | ツール呼び出しが実行されました。 |
| `tool.denied` | `agent.runTools` | `name`, `reason` | 承認者が呼び出しをブロックしました。 |
| `tool.error` | `agent.runTools` | `name`, `err` | ツールは実行されたがエラーを返しました。 |
| `agent.compressed` | `agent.Turn` | `messages` | セッションの圧縮が発火しました。 |
| `agent.compress_failed` | `agent.Turn` | `err` | 圧縮プロバイダーがエラーになりましたが、ループは継続しました。 |
| `whatsapp.starting` | `cli/whatsapp.go` | `store`, `allowlist` | WhatsApp ブリッジが起動しました。 |
| `whatsapp.voice_enabled` | `cli/whatsapp.go` | `binary`, `model` | 音声文字起こしが有効です。 |
| `cron.fire` | `internal/cron/scheduler.go` | `name`, `job` | cron ジョブが発火しました。 |
| `cron.deliver` | `internal/cron/scheduler.go` | `name`, `target`, `bytes` | cron の応答が配信されました。 |

すべてのログ行には、標準の slog フィールドである `time`、`level`、`msg` と、上記いずれかの属性が付与されます。

## ログパイプライン — スタックを選ぶ

<div class="tabs" data-tabs="observability-stack">
  <div class="tab-list" role="tablist" aria-label="Observability stack">
    <button role="tab" aria-selected="true">Loki + Grafana</button>
    <button role="tab" aria-selected="false">Datadog</button>
    <button role="tab" aria-selected="false">Vector</button>
    <button role="tab" aria-selected="false">OTel Collector</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Loki + Promtail + Grafana。タブ下部の systemd + Promtail の設定を参照してください。LogQL でクエリします。

```
sum by (level) (rate({job="rousseau-agent"} [5m]))
```

承認の拒否に対するアラート:

```
count_over_time({job="rousseau-agent"} |= "tool.denied" [15m]) > 5
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

journald ソースを使用する Datadog Agent。組み込みの JSON パーサーが各 slog 属性をファセットとして持ち上げます。タブ下部の設定を参照してください。

モニター:

- `msg:tool.denied` — ブロックされた各ツール呼び出し。
- `msg:whatsapp.logged_out` — WhatsApp のペアリングが失われました。
- `msg:cron.delivery_failed` — cron ジョブの配信に失敗しました。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Vector をアグリゲータとして、任意のダウンストリームシンク (S3、Kafka、Elasticsearch など) に転送します。タブ下部の設定を参照してください。Vector の `remap` 言語を使うと、rousseau に触れずにノイズのあるイベントを破棄したり、派生属性を追加したりできます。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

OpenTelemetry Collector は journald 経由でログを受け付け、任意の OTLP バックエンドに転送します。

```yaml
# otel-collector-config.yaml
receivers:
  journald:
    units: [rousseau-agent.service]

processors:
  transform:
    log_statements:
      - context: log
        statements:
          - merge_maps(cache, ParseJSON(body), "insert")

exporters:
  otlphttp:
    endpoint: https://otel-backend.internal:4318

service:
  pipelines:
    logs:
      receivers: [journald]
      processors: [transform]
      exporters: [otlphttp]
```

rousseau 自体にロードマップにある OTel エクスポーターが実装されれば、journald を経由しないエンドツーエンドの OTel になります。

  </div>
</div>

## ログパイプライン: Loki + Grafana

### Systemd + Promtail

Promtail を rousseau サービスのジャーナルに向けます。

```yaml
# /etc/promtail/promtail.yaml
scrape_configs:
  - job_name: rousseau-agent
    journal:
      matches: _SYSTEMD_USER_UNIT=rousseau-agent.service
      labels: { job: rousseau-agent }
    relabel_configs:
      - source_labels: [__journal__systemd_user_unit]
        target_label: unit
    pipeline_stages:
      - json:
          expressions: { level: level, msg: msg }
      - labels: { level: "" }
```

Grafana ダッシュボードでは `level=WARN` と `msg="tool.denied"` でフィルタし、「ブロックされたツール呼び出し」パネルを構築できます。

### Kubernetes

Grafana Agent (または Loki + Alloy) を DaemonSet としてデプロイします。rousseau はコンテナ内で stdout に書き出すため、ファイルスクレイピングは不要です。

## ログパイプライン: Datadog

```
# /etc/datadog-agent/conf.d/rousseau.d/conf.yaml
logs:
  - type: journald
    include_units:
      - rousseau-agent.service
    service: rousseau-agent
    source: rousseau-agent
```

rousseau は JSON を出力するため、Datadog の組み込み JSON パーサーが `level`、`msg`、および各属性をファーストクラスのファセットとして持ち上げます。承認ポリシーに関するアラートには `msg:tool.denied` のモニターを設定してください。

## ログパイプライン: Vector

```toml
# /etc/vector/vector.toml
[sources.rousseau_journal]
type = "journald"
include_units = ["rousseau-agent.service"]

[transforms.rousseau_parse]
type = "remap"
inputs = ["rousseau_journal"]
source = '''
. = merge(., parse_json(.message) ?? {})
'''

[sinks.loki]
type = "loki"
inputs = ["rousseau_parse"]
endpoint = "https://loki.internal:3100"
labels = { job = "rousseau-agent", level = "{{ level }}" }
```

## グラフ化する主要メトリクス

現時点で Prometheus エンドポイントはありません。必要なメトリクスはログストリームに載っています。

| メトリクス | 導出方法 |
|---|---|
| ツール呼び出しレート | `msg:tool.execute` をカウント |
| 拒否レート | `msg:tool.denied` をカウント |
| エラーレート | `msg:tool.error` をカウント |
| 圧縮イベント | `msg:agent.compressed` をカウント |
| cron の発火 | `msg:cron.fire` をカウント |
| cron 配信のバイト数 | `msg:cron.deliver` の `bytes` を合計 |

Loki + LogQL: `sum by (name) (count_over_time({job="rousseau-agent"} |= "tool.denied" [1h]))`。

## OpenTelemetry のロードマップ

OpenTelemetry 統合はロードマップに含まれています。実装された際には次を期待できます。

- エージェントループを通じた `otel.trace` コンテキストの伝播 (`Turn` ごとに 1 スパン、ツール呼び出しごとに子スパン)。
- 現在ログに載っている同じカウンターに対するメトリクスエクスポーター。
- 環境変数で設定可能な OTLP エンドポイント。

それまでは、構造化された slog 出力を可観測性の基盤として扱ってください。メトリクスやトレースとして欲しいすべてのイベントは既にそこにあります。メタデータは完全で、ワイヤーフォーマットが異なるだけです。

## ログパイプラインなしでのデバッグ

対話的:

```sh
rousseau --config /etc/rousseau/config.yaml whatsapp \
  --allow 447900123456@s.whatsapp.net 2>&1 | jq
```

デーモンは slog を stderr に書き出します。`jq` にパイプすると対話的なフィルタが得られます。`jq 'select(.msg == "tool.denied")'` はブロックされたすべての呼び出しを表示します。

`rousseau doctor` はもう 1 つの可観測性レバーです。ある時点の依存関係と設定選択のスナップショットを提供します。

## トラブルシューティング

### `journal has no entries`

デーモンがまだ何も書き出していないか、journald のマッチャーが誤っています。`journalctl --user -u rousseau-agent.service --no-pager` で確認してください。

### パイプラインでの JSON パースエラー

Rousseau はイベントごとに 1 行をログします。ログイベントの `msg` に改行が含まれる場合 (一部のトランスポートは複数行のエラー文字列を含みます。まれです)、パイプラインが 2 つのイベントに分割することがあります。正規表現でフィルタするか、埋め込みの改行を考慮した構造化パースを使用してください。

### ダウンストリームで属性が欠落する

Loki はラベルにマップできない属性をドロップします。LogQL の `line_format` を使用して属性をレンダリング出力に投影するか、`pipeline_stages.labels` でラベルとしてインデックス化してください。

### Datadog の service タグが欠落する

Datadog はフィルタリングに `service` フィールドを使用します。journald ソースが設定からこれを設定します。`service: rousseau-agent` が存在することを確認してください。

### Grafana ダッシュボードにデータが表示されない

LogQL クエリがラベルと一致していることを確認してください。Promtail のデフォルトの `job` ラベルはスクレイプ設定で設定されます。変更した場合は、すべてのダッシュボードのクエリを更新してください。

## 関連ページ

- [Configuration](/ja/configuration/) — `log.level` および `log.format`。
- [Guides: Audit &amp; Approval Policies](/ja/guides/audit-approval-policies/) — 最も必要なアラートシグナル。
- [Reference: Exit codes](/ja/reference/exit-codes/) — デーモンが init システムに失敗を通知する方法。
- [Security](/ja/security/) — slog による監査証跡。
- [Reference: Logs](/ja/reference/logs/) — rousseau が出力するすべての slog キー。

## さらに読む

- `internal/cli/root.go` — `newLogger` が slog ハンドラーを設定します。
- `internal/agent/agent.go` — `tool.execute`、`tool.denied`、`agent.compressed` イベント。
- `internal/transport/whatsapp/dispatch.go` — トランスポート側のイベント発行。
- Grafana LogQL ドキュメントと Datadog のログ処理ドキュメント (外部)。
