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
description: "Configure the Vertex AI provider: Application Default Credentials or an explicit service-account JSON, region and model ID, required IAM roles."
keywords: "Vertex, Google Cloud, GCP, Application Default Credentials, ADC, service account, aiplatform, endpoints, predict"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/providers/vertex/"
subtitle: "Anthropic's Claude models on Vertex AI."
tags: "providers, vertex, GCP"
title: "Google Vertex AI プロバイダ"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Vertex, Google Cloud, GCP, Application Default Credentials, ADC, service account, aiplatform, endpoints, predict"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Google Vertex AI プロバイダ"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 9
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/providers/vertex/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/vertex/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Google Vertex AI プロバイダ"
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
twitter_description: "Configure the Vertex AI provider: Application Default Credentials or an explicit service-account JSON, region and model ID, required IAM roles."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Google Vertex AI プロバイダ"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">このページで学べること</span><p><code>gcloud</code> コマンドを用いたサービスアカウントのステップバイステップ設定、代わりに Workload Identity Federation を使う場面、Anthropic モデル向けの Vertex リージョンマトリクス、401/403/429 応答の失敗モードを扱います。このページと並行して <code>internal/llm/vertex/client.go</code> を読んでください。</p></aside>

## Vertex を使う場面

`vertex` プロバイダは次の場合に最適です。

- Google Cloud 上にあり、Vertex AI 経由で Claude を課金したい場合。
- サービスアカウント JSON または Application Default Credentials（ADC）で認証したい場合。
- 特定の GCP リージョン内でデータ所在が必要な場合。
- Private Google Access 経由でルーティングし、公開インターネットに触れたくない場合。
- GKE ワークロード向けに Workload Identity Federation を既にセットアップ済みの場合。

## 設定

```yaml
provider: vertex

vertex:
  project: my-gcp-project
  region: us-central1
  model: claude-sonnet-4-6@20260101
  credentials_file: ~/.config/gcloud/vertex-key.json
  max_tokens: 4096
```

| フィールド | デフォルト | 効果 |
|---|---|---|
| `project` | *必須* | GCP プロジェクト ID（数値のプロジェクト番号ではありません）。 |
| `region` | *必須* | Vertex リージョン。Anthropic-on-Vertex はリージョンの一部で利用可能です。GCP コンソールで確認してください。 |
| `model` | *必須* | Anthropic-on-Vertex モデル ID（例: `claude-sonnet-4-6@20260101`）。`@date` サフィックスに注意してください。 |
| `credentials_file` | *空* | サービスアカウントまたは authorized-user JSON キーへのパス。空の場合は ADC を使用。 |
| `max_tokens` | `4096` | 出力トークン上限。 |

## エンドポイントレイアウト

リクエストは次に届きます:

```
https://<region>-aiplatform.googleapis.com/v1/
    projects/<project>/locations/<region>/publishers/anthropic/
    models/<model>:rawPredict
```

`rousseau` は `project`、`region`、`model` からこの URL を構築します。上書きしないでください。

## 認証情報

サポートされる 2 つの経路:

### 1. 明示的な `credentials_file`

サービスアカウント JSON キー、または（`gcloud auth application-default login` からの）authorized-user JSON を指します。

```yaml
vertex:
  credentials_file: /home/rousseau/.config/gcloud/vertex-sa.json
```

ファイルは `service_account` か `authorized_user` の形状の可能性があるため、プロバイダは内部で `google.CredentialsFromJSONWithParams` を呼び出します。`CredentialsParams{Scopes: [cloud-platform]}` は固定です。

### 2. Application Default Credentials

`credentials_file` を空のままにすると、プロバイダは ADC を走査します。

1. `GOOGLE_APPLICATION_CREDENTIALS` 環境変数。
2. `~/.config/gcloud/application_default_credentials.json`（`gcloud auth application-default login` から）。
3. GCE / GKE メタデータサーバー（クラスタ内では Workload Identity が推奨パターン）。

## 必要な IAM

呼び出しアイデンティティにプロジェクトに対する `roles/aiplatform.user` — もしくはより狭い `aiplatform.endpoints.predict` 権限 — を付与します。

GKE サービスアカウント向けの Workload Identity 例:

```sh
gcloud projects add-iam-policy-binding my-gcp-project \
  --member "serviceAccount:my-gcp-project.svc.id.goog[default/rousseau-sa]" \
  --role   "roles/aiplatform.user"
```

## ストリーミング

プロバイダは同じ `rawPredict` エンドポイントの SSE バリアントを用いて `agent.StreamingProvider` を実装します。

## ツール使用

`Registry` からのツール定義は `internal/llm/vertex/client.go` で Vertex の Anthropic ツール JSON に変換されます。承認ポリシーが適用されます。

## サービスアカウントの設定、ステップバイステップ

<div class="tabs" data-tabs="vertex-auth">
  <div class="tab-list" role="tablist" aria-label="Vertex auth pattern">
    <button role="tab" aria-selected="true">Service-account JSON</button>
    <button role="tab" aria-selected="false">Workload Identity (GKE)</button>
    <button role="tab" aria-selected="false">WIF from AWS/Azure</button>
    <button role="tab" aria-selected="false">User ADC (dev)</button>
  </div>
  <div class="tab-panel" role="tabpanel">

オンプレミスや非 GKE ホストで最も単純なパターンです。専用のサービスアカウントを作成し、最小ロールを付与し、JSON キーをダウンロードして、rousseau をそのファイルに向けます。

```sh
PROJECT=my-gcp-project
SA_NAME=rousseau-vertex

gcloud iam service-accounts create $SA_NAME \
  --display-name "rousseau-agent Vertex caller" \
  --project $PROJECT

gcloud projects add-iam-policy-binding $PROJECT \
  --member "serviceAccount:${SA_NAME}@${PROJECT}.iam.gserviceaccount.com" \
  --role   "roles/aiplatform.user"

gcloud iam service-accounts keys create ~/vertex-sa.json \
  --iam-account "${SA_NAME}@${PROJECT}.iam.gserviceaccount.com"
```

```yaml
vertex:
  project: my-gcp-project
  region: europe-west4
  model: claude-sonnet-4-6@20260101
  credentials_file: /etc/rousseau/vertex-sa.json
```

<aside class="admonition" data-type="caution"><span class="admonition-title">キーローテーション</span><p>サービスアカウント JSON キーは期限切れになりません。少なくとも 90 日ごとにローテートしてください。静的キーを管理せずに済むよう、Workload Identity Federation（下記）を推奨します。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

GKE で推奨のパターンです。Kubernetes サービスアカウントを Google サービスアカウントにバインドし、Pod がメタデータサーバー経由で認証情報を継承するようにします。ディスク上に JSON キーはありません。

```sh
PROJECT=my-gcp-project
KSA=rousseau
GSA=rousseau-vertex
NAMESPACE=agents

# GSA already exists from the previous step. Bind the KSA:
gcloud iam service-accounts add-iam-policy-binding \
  "${GSA}@${PROJECT}.iam.gserviceaccount.com" \
  --role "roles/iam.workloadIdentityUser" \
  --member "serviceAccount:${PROJECT}.svc.id.goog[${NAMESPACE}/${KSA}]"
```

Kubernetes サービスアカウントにアノテーションを付けます:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: rousseau
  namespace: agents
  annotations:
    iam.gke.io/gcp-service-account: rousseau-vertex@my-gcp-project.iam.gserviceaccount.com
```

その後、`credentials_file` を空のままにしてください。ADC が GKE メタデータサーバーから自動的に認証情報を取得します。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Workload Identity Federation は、AWS IAM ロールや Azure マネージド ID がサービスアカウントキーなしで GCP API を呼び出せるようにします。マルチクラウドデプロイに有用です。

フェデレーテッドアイデンティティを作成します:

```sh
gcloud iam workload-identity-pools create rousseau-pool \
  --location=global --project=$PROJECT

gcloud iam workload-identity-pools providers create-aws rousseau-aws \
  --location=global \
  --workload-identity-pool=rousseau-pool \
  --account-id=<AWS_ACCOUNT_ID>
```

AWS ロールを GSA にバインドします:

```sh
gcloud iam service-accounts add-iam-policy-binding \
  "${GSA}@${PROJECT}.iam.gserviceaccount.com" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/rousseau-pool/attribute.aws_role/arn:aws:iam::${AWS_ACCOUNT_ID}:role/rousseau"
```

SDK に AWS ロールを GCP トークンに交換するよう指示する credential-source JSON ファイルを `GOOGLE_APPLICATION_CREDENTIALS` にエクスポートしてください。credential-source の形状は [GCP WIF ドキュメント](https://cloud.google.com/iam/docs/workload-identity-federation) を参照してください。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

ローカル開発では、`gcloud` 経由で自分のユーザー認証情報を使います。

```sh
gcloud auth application-default login
gcloud auth application-default set-quota-project my-gcp-project
```

これにより `~/.config/gcloud/application_default_credentials.json` が書き込まれます。`credentials_file` を空のままにすれば、rousseau は ADC 経由でそれを読みます。

<aside class="admonition" data-type="warning"><span class="admonition-title">本番では絶対に使わない</span><p>ユーザー ADC はリクエストを個人のアイデンティティとクォータに紐付けます。本番でユーザー ADC を持つデーモンをデプロイしないでください。サービスアカウントか Workload Identity に切り替えてください。</p></aside>

  </div>
</div>

## リージョンマトリクス

Vertex 上の Anthropic モデルはリージョンスコープです。Google が新しいスナップショットを展開するにつれ可用性は変化します。2026 年中頃時点:

| モデル | us-central1 | us-east5 | europe-west1 | europe-west4 | asia-southeast1 |
|---|:---:|:---:|:---:|:---:|:---:|
| `claude-sonnet-4-6` | あり | あり | あり | あり | あり |
| `claude-opus-4-6` | あり | 限定 | 限定 | あり | なし |
| `claude-haiku-4-6` | あり | あり | あり | あり | あり |

正典は Vertex Model Garden — *Model Garden &gt; Anthropic &gt; Region availability* です。アクセス申請は即時で、手動承認ステップはありません（Bedrock とは異なります）。

## プライベート接続

公開インターネットへ egress してはいけないデプロイでは、VPC で Private Google Access を有効化し、DNS で `*-aiplatform.googleapis.com` を `restricted.googleapis.com` に解決するよう設定します。rousseau が構築する Vertex エンドポイント URL はそのまま機能し、トラフィックは Google のバックボーンに留まります。

DNS ゾーンの設定については [GCP Private Google Access ドキュメント](https://cloud.google.com/vpc/docs/private-google-access) を参照してください。

## 注意点

- **モデル ID フォーマット。** Vertex は `@date`（`claude-sonnet-4-6@20260101`）、Bedrock は `-<date>-v1:0`、Anthropic 直接は `claude-sonnet-4-6` を使用します。互いに貼り付けないでください。
- **リージョン可用性。** すべての Anthropic モデルがすべてのリージョンにあるわけではありません。`us-central1` と `europe-west4` はよくあるところです。
- **クォータ。** Vertex のクォータはプロジェクト × リージョン × モデル別です。クォータに触れるとリクエストは 429 になります。呼び出し側で指数バックオフを有効化してください。
- **`anthropic_version` 文字列。** rousseau は `vertex-2023-10-16` を送信します（`internal/llm/vertex/client.go` の `buildVertexBody` を参照）。Anthropic が Vertex の anthropic_version を上げると、古い rousseau ビルドは 400 になります。
- **User-agent が必要。** 一部の Vertex エンドポイントは User-Agent なしのリクエストを拒否します。Go SDK は自動的に設定しますが、カスタム `HTTPClient` を注入する場合は User-Agent ヘッダを保持してください。

## トラブルシューティング

### `vertex: HTTP 401 unauthorized`

認証情報チェーンが有効な認証情報を返しませんでした。よくある原因: `credentials_file` のパスがコンテナ内で読めない、`GOOGLE_APPLICATION_CREDENTIALS` 環境変数が存在しないファイルを指している、`gcloud auth application-default login` を実行していない。`gcloud auth application-default print-access-token` で確認してください。

### `vertex: HTTP 403 permission denied on resource`

アイデンティティは認証済みですが、プロジェクトに対する `aiplatform.endpoints.predict` を欠いています。`roles/aiplatform.user`（またはより狭い権限）を付与し、IAM 反映のため約 30 秒待ってください。

### `vertex: HTTP 404 not found`

モデル ID がそのリージョンに存在しません。Vertex Model Garden で `@date` サフィックスを再確認し、可用性マトリクスでリージョンがそのモデルを示すことを確認してください。

### `vertex: HTTP 429 resource exhausted`

クォータ超過。オプション: (1) IAM コンソール経由でクォータ増加を申請、(2) 呼び出し側でバックオフ付きキュー、(3) 複数リージョンにトラフィックを分散。

### `vertex: credentials: could not find default credentials`

ADC が走査するものが何もありません。`credentials_file` を明示的に設定するか、`export GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json` を実行するか、（GKE の場合）クラスタで Workload Identity が有効で KSA が正しくアノテートされているか確認してください。

## 関連ページ

- [プロバイダ: Anthropic](/ja/providers/anthropic/) — 同じワイヤフォーマット、直接 API。
- [プロバイダ: Bedrock](/ja/providers/bedrock/) — AWS マネージドの Claude。
- [ガイド: Kubernetes デプロイ](/ja/guides/kubernetes-deployment/) — Workload Identity 設定。
- [ガイド: エンタープライズオンボーディング](/ja/guides/enterprise-onboarding/) — プラットフォームチーム向けチェックリスト。
- [セキュリティ](/ja/security/) — 信頼境界とネットワーク egress。

## さらに読む

- `internal/llm/vertex/client.go` — エンドポイント URL 構築、ADC 処理、ワイヤ型。
- `internal/llm/vertex/oauth2.go` — OAuth2 HTTP クライアント構築。
- `internal/config/config.go` — `VertexConfig` 構造体。
- GCP ドキュメント: [Anthropic on Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude)。
- GCP ドキュメント: [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)。
