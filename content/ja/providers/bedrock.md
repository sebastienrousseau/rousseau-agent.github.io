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
description: "Configure the AWS Bedrock provider: standard credential chain, region and model ID format, required IAM permissions."
keywords: "Bedrock, AWS, SigV4, IAM, InvokeModel, InvokeModelWithResponseStream, Claude on AWS"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/providers/bedrock/"
subtitle: "Anthropic's Claude models on AWS."
tags: "providers, bedrock, AWS"
title: "AWS Bedrock プロバイダ"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Bedrock, AWS, SigV4, IAM, InvokeModel, InvokeModelWithResponseStream, Claude on AWS"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "AWS Bedrock プロバイダ"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 8
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/providers/bedrock/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/bedrock/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "AWS Bedrock プロバイダ"
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
twitter_description: "Configure the AWS Bedrock provider: standard credential chain, region and model ID format, required IAM permissions."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "AWS Bedrock プロバイダ"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">このページで学べること</span><p>AWS 認証情報チェーンでの Bedrock プロバイダの設定、最小権限 IAM ポリシー、クロスアカウントのロール引き受け、プライベート接続のための VPC エンドポイント、リージョン別のモデル可用性マトリクスを扱います。このページと並行して <code>internal/llm/bedrock/client.go</code> を読んでください。</p></aside>

## Bedrock を使う場面

`bedrock` プロバイダは次の場合に最適です。

- AWS 上にあり、Anthropic API ではなく Bedrock 経由で Claude を課金したい場合。
- 標準 AWS 認証情報チェーン（環境変数、`~/.aws/credentials`、IMDS、EKS 上の IRSA）を用いた SigV4 認証が必要な場合。
- データ所在の理由でモデルトラフィックを単一の AWS リージョン内に留めたい場合。
- 公開インターネットに触れないよう VPC エンドポイント経由でモデルトラフィックをルーティングしたい場合。
- `sts:AssumeRole` によるクロスアカウントアクセスが欲しい場合。

## 設定

```yaml
provider: bedrock

bedrock:
  region: us-east-1
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
  profile: default
  max_tokens: 4096
```

| フィールド | デフォルト | 効果 |
|---|---|---|
| `region` | *必須* | AWS リージョン。Bedrock のモデル可用性はリージョン単位です。AWS コンソールで確認してください。 |
| `model` | *必須* | Bedrock モデル ID。Anthropic Claude ID は `anthropic.claude-<name>-<date>-<version>:<revision>` の形式に従います。 |
| `profile` | *空* | `~/.aws/credentials` の認証情報プロファイル。空の場合は標準の認証情報チェーンにフォールスルーします。 |
| `max_tokens` | SDK デフォルト | 補完 1 回あたりの出力トークン上限。 |

## 認証情報チェーン

プロバイダは `awsconfig.LoadDefaultConfig` 経由で Bedrock クライアントを構築します。これは標準チェーンを順に走査します。

1. 環境変数（`AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY`、`AWS_SESSION_TOKEN`）。
2. 共有認証情報ファイル（`~/.aws/credentials`）。`profile` が設定されていれば絞り込み。
3. 共有コンフィグファイル（`~/.aws/config`）。
4. IAM Roles for Tasks（ECS）/ IAM Roles Anywhere。
5. EC2 IMDS（v2）。
6. IRSA — Kubernetes サービスアカウントに紐づく IAM ロール（EKS）。

これらはいずれも rousseau で設定するものではなく、SDK が解決を担います。

## 必要な IAM 権限

呼び出し側が引き受け可能でなければならない最小ポリシー:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-sonnet-4-6-*"
    }
  ]
}
```

`Resource` は呼び出そうとする特定のモデルファミリに絞ってください。より広いワイルドカードも動作しますが、通常はやりすぎです。

## ワイヤフォーマット

プロバイダは標準の Anthropic messages JSON ボディ（`anthropic_version`、`messages`、`system`、`tools`、`max_tokens`）を `bedrock:InvokeModel` に送信し、同じ形状を受け取ります。これは Anthropic 直接 API を反映しており、tool use、stop reason、使用量カウンターは同じです。

ストリーミングは SDK のイベントストリームデコーダで `bedrock:InvokeModelWithResponseStream` を使用します。

## ストリーミング

プロバイダは `agent.StreamingProvider` を実装します。ストリーミングは `rousseau chat` で自動的に使用されます。

## ツール使用

`Registry` からのツール定義は `internal/llm/bedrock/client.go` で Bedrock のツール JSON に変換されます。承認ポリシーが適用されます。

## デプロイ別の認証パターン

<div class="tabs" data-tabs="bedrock-auth">
  <div class="tab-list" role="tablist" aria-label="Bedrock auth deployment">
    <button role="tab" aria-selected="true">Laptop</button>
    <button role="tab" aria-selected="false">EC2</button>
    <button role="tab" aria-selected="false">EKS (IRSA)</button>
    <button role="tab" aria-selected="false">Cross-account</button>
  </div>
  <div class="tab-panel" role="tabpanel">

ローカル開発では、SSO または長期キーを持つ名前付きプロファイルを使用してください。

```sh
aws configure sso --profile rousseau-dev
aws sso login --profile rousseau-dev
```

```yaml
bedrock:
  region: us-east-1
  profile: rousseau-dev
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
```

rousseau は非空のとき `awsconfig.WithSharedConfigProfile(cfg.Profile)` を渡すため、`profile:` は尊重されます（`internal/llm/bedrock/client.go` の 63 行目を参照）。`profile` を省略するとデフォルトチェーンにフォールスルーします。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

`bedrock:InvokeModel` 権限を持つインスタンスプロファイルを接続し（以下の IAM ポリシーを参照）、`profile` は空のままにしてください。

```yaml
bedrock:
  region: us-east-1
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
```

SDK は IMDS v2 から自動的に認証情報を解決します。環境変数もプロファイルファイルも不要です。

<aside class="admonition" data-type="note"><span class="admonition-title">IMDS v2</span><p>インスタンスが IMDS v2 を要求するよう設定されていることを確認してください（hop limit 2、トークン必須）。AWS Go SDK v2 はトークン交換を透過的に処理しますが、<code>169.254.169.254</code> へのネットワーク到達性が必要です。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

EKS では IAM Roles for Service Accounts（IRSA）が推奨パターンです。Pod のサービスアカウントにロールを接続します。

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: rousseau
  namespace: agents
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/rousseau-bedrock
```

ロールの信頼ポリシーはこれを EKS OIDC プロバイダとサービスアカウントに紐付けます。完全な例は [ガイド: Kubernetes デプロイ](/ja/guides/kubernetes-deployment/) を参照してください。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau がアカウント A に、Bedrock がアカウント B にある場合。ロール引き受けを設定します。

`~/.aws/config`:

```ini
[profile rousseau]
role_arn = arn:aws:iam::222222222222:role/rousseau-bedrock
source_profile = default
region = us-east-1
```

アカウント B のターゲットロールはモデルに対する `bedrock:InvokeModel` を持ち、アカウント A のプリンシパルによる引き受けを許可する信頼ポリシーを持ちます。それから:

```yaml
bedrock:
  region: us-east-1
  profile: rousseau
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
```

SDK は STS `AssumeRole` のラウンドトリップを透過的に処理します。

  </div>
</div>

## 最小権限 IAM ポリシー

呼び出し側が引き受け可能でなければならない最小ポリシー:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-sonnet-4-6-*"
    }
  ]
}
```

`Resource` は特定のモデルファミリに絞ってください。より広いワイルドカードも動作しますが、必要以上の権限を付与することになります。プロビジョンドスループットの場合、プロビジョンドモデルの ARN を第 2 のリソースとして追加してください。

クロスアカウント用の信頼ポリシー（アカウント B、モデルホスト側）:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "AWS": "arn:aws:iam::111111111111:role/rousseau-caller" },
    "Action": "sts:AssumeRole",
    "Condition": { "StringEquals": { "sts:ExternalId": "rousseau-prod" } }
  }]
}
```

`ExternalId` は、サードパーティのクロスアカウントアクセスに対して AWS セキュリティガイダンスが要求するものです。

## VPC エンドポイント

公開インターネットに到達してはいけないデプロイでは、VPC 内に Bedrock のインタフェース VPC エンドポイントを作成します。

```sh
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-0123456789abcdef0 \
  --vpc-endpoint-type Interface \
  --service-name com.amazonaws.us-east-1.bedrock-runtime \
  --subnet-ids subnet-aaa subnet-bbb \
  --security-group-ids sg-xxx
```

セキュリティグループとルートテーブルが許可すれば、AWS SDK は自動的にエンドポイント経由で解決します。rousseau 側のコンフィグ変更は不要です。これはプロバイダに対して透過的です。

<aside class="admonition" data-type="warning"><span class="admonition-title">エンドポイントポリシー</span><p>受け入れるプリンシパルとアクションを制約するため、エンドポイントにリソースポリシーを付与してください。制約のないエンドポイントは分離の利点を無効化します。</p></aside>

## リージョン別モデル可用性

可用性は AWS が新しいスナップショットを展開するにつれ変化します。2026 年中頃時点のスナップショット:

| モデル | us-east-1 | us-west-2 | eu-west-2 | eu-central-1 | ap-southeast-1 | ap-northeast-1 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Claude Sonnet 4.6 | あり | あり | あり | あり | あり | あり |
| Claude Opus 4.6 | あり | あり | 限定 | 限定 | なし | なし |
| Claude Haiku 4.6 | あり | あり | あり | あり | あり | あり |

<aside class="admonition" data-type="note"><span class="admonition-title">コンソールを確認</span><p>可用性は予告なく変わります。正典は Bedrock コンソールの <em>Foundation models &gt; Model access</em> です。リージョンがサポートしていても、モデルが呼び出し可能になる前に、そこで明示的にアクセスを申請する必要があります。</p></aside>

## 注意点

- **モデル ID はリージョン別に異なる。** `us-east-1` の `anthropic.claude-sonnet-4-6-20260101-v1:0` は `eu-west-2` では別のスナップショットの可能性があります。Bedrock コンソールで確認してください。
- **アクセスはモデル別に付与が必要。** IAM が `InvokeModel` を許可していても、Bedrock は最初の呼び出しが成功する前に、コンソールで *Model access &gt; Request access* を通す必要があります。
- **スロットリング。** Bedrock はアカウントおよびモデルごとの並行度制限（tokens-per-minute、requests-per-minute）を強制します。`max_tokens` は控えめに設定してください。
- **プロビジョンドスループット。** プロビジョンドスループットを持っている場合、`model` にプロビジョンドモデル ID（`arn:aws:bedrock:us-east-1:<account>:provisioned-model/…`）を渡してください。
- **ストリーミングデコーダの失敗。** イベントストリームフォーマットは SDK バージョン間で微妙に変わっています。`aws-sdk-go-v2/service/bedrockruntime` を既知の良好なバージョンに固定し、バンプごとに再テストしてください。

## トラブルシューティング

### `AccessDeniedException: You don't have access to the model`

2 つの別々のチェックがあります: (1) 呼び出し側の IAM ポリシーがモデル ARN に対する `bedrock:InvokeModel` を許可している、(2) アカウントが Bedrock コンソールで明示的にモデルアクセスを申請している。項目 2 が初回ユーザーの大半を捕らえます。

### `ValidationException: The model ID isn't valid`

モデル ID 文字列が、設定されたリージョンで利用可能なモデルと一致しません。タイピングではなく、Bedrock コンソール（*Providers &gt; Anthropic &gt; Model catalog*）から正確な ID をコピーしてください。日付とバージョンのサフィックスは厳密に一致する必要があります。

### `ThrottlingException`

トークンまたは分あたりリクエストのクォータに当たっています。オプション: (1) サービスクォータの引き上げ申請、(2) 呼び出し側で指数バックオフ付きのキュー、(3) プロビジョンドスループットへの切り替え。

### `bedrock: parse response: json:` — 不正な JSON

レスポンスボディが期待される Anthropic-on-Bedrock 形状ではありません。通常、非 Anthropic モデルが `model` として渡されたことを示します。`internal/llm/bedrock/client.go` の `buildBedrockBody` は Anthropic ワイヤフォーマットしか生成しません。

### VPC エンドポイント到達不能 — `dial tcp: no route to host`

Pod / インスタンスがエンドポイントの ENI に到達できません。エンドポイントのセキュリティグループ（呼び出し側 SG からのポート 443 を許可する必要があります）、エンドポイントのサブネットルートテーブル、DNS 解決（エンドポイントは VPC 上で private DNS を有効化する必要があります）を確認してください。

## 関連ページ

- [プロバイダ: Anthropic](/ja/providers/anthropic/) — 同じワイヤフォーマット、直接 API 経路。
- [ガイド: Kubernetes デプロイ](/ja/guides/kubernetes-deployment/) — IRSA 設定。
- [ガイド: エンタープライズオンボーディング](/ja/guides/enterprise-onboarding/) — プラットフォームチーム向けチェックリスト。
- [ガイド: レート制限](/ja/guides/rate-limits/) — スロットリングハンドブック。
- [セキュリティ](/ja/security/) — 信頼境界とネットワーク egress。

## さらに読む

- `internal/llm/bedrock/client.go` — `Complete`、メッセージ変換、ワイヤ型。
- `internal/config/config.go` — `BedrockConfig` 構造体。
- AWS ドキュメント: [Amazon Bedrock IAM permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html)。
- AWS ドキュメント: [Bedrock interface VPC endpoints](https://docs.aws.amazon.com/bedrock/latest/userguide/vpc-interface-endpoints.html)。
