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
description: "Use case narrative: a financial-services team running rousseau-agent in-tenant on AWS with Bedrock, pattern-mode approvals, and SLSA-3 supply-chain posture."
keywords: "regulated industry, financial services, bedrock, in-tenant, slsa, cosign, compliance"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/use-cases/regulated-industry/"
subtitle: "In-tenant Bedrock deployment for a financial-services team."
tags: "use-cases, bedrock, regulated, financial-services, slsa"
title: "ユースケース：規制業界"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "regulated industry, financial services, bedrock, in-tenant, slsa, cosign, compliance"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ユースケース：規制業界"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 73
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/use-cases/regulated-industry/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/regulated-industry/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "ユースケース：規制業界"
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
twitter_description: "Use case narrative: a financial-services team running rousseau-agent in-tenant on AWS with Bedrock, pattern-mode approvals, and SLSA-3 supply-chain posture."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "ユースケース：規制業界"
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

## ストーリー

あなたは中規模銀行のプラットフォームエンジニアです。コンプライアンスは、エンジニアが使用する任意のコーディングアシスタントが以下を満たす必要があると言います:

1. SaaS コントロールプレーンではなく、銀行の AWS アカウント内で実行される。
2. 銀行が契約と監査証跡を持つプロバイダー (Bedrock) を通じてモデルトラフィックをルーティングする。
3. 文書化されたサプライチェーン姿勢 (SLSA-3、SBOM、シグネチャ検証) を持つ。
4. マシン可読な監査証跡で承認ポリシーを強制する。
5. サードパーティにソースコードを持ち出さない。

rousseau のポジショニングは、それらの要件のすべてにマップします。プラットフォームチームの EKS クラスター内で Kubernetes `Deployment` として実行し、エンジニアリングチャネルへの Slack Socket Mode トランスポートを駆動します。

エンジニアリングのロールアウトは平凡です — `Deployment`、`Secret`、`ConfigMap`、`PersistentVolumeClaim`。ストーリーは監査人が到着したときに起こることです。

## 監査

外部監査人が 4 つの質問をします。

**Q1: モデルトラフィックはどこに行きますか?**

`internal/llm/bedrock/` を指し示します。プロバイダーは標準の AWS 認証情報チェーン (EKS 上の IRSA 経由) を使用するため、資格情報は短命の STS トークンです。トラフィックは AWS アカウントを決して離れません。

**Q2: 実行中のバイナリをどう検証しますか?**

`docker/Dockerfile` を見せます — 固定された `golang:1.26-alpine` ベースを持つマルチステージビルド — と、SRE チームがイメージプロモーション中に実行する `release-verify.sh` スクリプト:

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_${VERSION}_checksums.txt.sig \
  rousseau_${VERSION}_checksums.txt

sha256sum -c rousseau_${VERSION}_checksums.txt
```

追加: SLSA-3 プロバナンスは GitHub Actions OIDC 経由で証明されます。Sigstore 透明性ログは公的な信頼アンカーです。

**Q3: モデルがプロダクションを変更するのをどう防ぎますか?**

`agent.approver` config を指し示します:

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied — this deployment does not permit destructive operations without operator confirmation"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|grep|rg|find|git status|git diff|git log|go test|go build) "}
    deny:
      - {tool: bash, match: "rm -rf|sudo|curl|wget|chmod|chown"}
      - {tool: bash, match: "kubectl (delete|apply|edit|scale|exec)"}
      - {tool: bash, match: "aws (s3 rm|iam|kms delete)"}
      - {tool: write, match: "\"path\":\"/(etc|root|var|usr)/"}
      - {tool: edit,  match: "\"path\":\"/(etc|root|var|usr)/"}
```

deny が allow に勝ちます。マッチしない → deny。すべての判定は構造化 slog イベント (`tool.execute`、`tool.denied`) としてログに記録され、Vector daemonset 経由で銀行の Datadog テナントに転送されます。

**Q4: セッションが参照するソースコードはどこに保存されていますか?**

説明します: セッション状態は EBS に裏付けられた PVC 上に、保存時暗号化ありで存在します。モデルコンテキストは圧縮されたセッション内に留まります ([圧縮 + 再呼び出し](/ja/user-guide/compression-recall/) を参照)。FTS5 再呼び出しインデックスは同じ PVC 上で実行されます。`agentskills.io` や外部 URL には何も行きません — [スキル](/ja/skills/) はホスト型レジストリではなく、バインドマウントされたディレクトリからロードされます。

監査人はフォローアップを尋ねます: 「モデル自体はどうですか?」Bedrock がモデル境界であり、Bedrock がプロンプトで行うことは銀行の AWS との既存契約によって支配されると説明します。

## それに必要なもの

### マニフェスト

完全なマニフェストについては [ガイド: Kubernetes デプロイ](/ja/guides/kubernetes-deployment/) を参照してください。このユースケースの重要な逸脱:

- **名前空間 `pod-security.kubernetes.io/enforce: restricted`。**
- Bedrock 資格情報用の **IRSA** — シークレット内に長命の AWS キーなし。
- Bedrock リージョナルエンドポイントと Slack WSS のみへの egress を許可する **NetworkPolicy**。
- `msg` フィールドを facet としてパースして slog 出力を Datadog に配送する **Vector daemonset**。

### Config

```yaml
provider: bedrock

bedrock:
  region: eu-west-1
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
  max_tokens: 4096

log:
  level: info
  format: json

state:
  path: /var/lib/rousseau/sessions.db

agent:
  max_iterations: 32
  compression:
    enabled: true
    trigger_messages: 40
    keep_recent: 6
  approver:
    mode: pattern
    default: deny
    reason: "denied — this deployment does not permit destructive operations without operator confirmation"
    allow: [...as above...]
    deny:  [...as above...]

slack:
  app_token: xapp-<from-Secret>
  bot_token: xoxb-<from-Secret>
  allowlist:
    - U012ABC   # platform team on-call
    - U012DEF   # platform team lead
```

### 監査ストーリー

すべてのツール呼び出しは 1 つの slog 行です。すべての拒否はもう 1 つです。Datadog の `msg:tool.denied` 上のモニターが SOC にアラートします。毎週、プラットフォームチームはレポートを引き出します:

```
# LogQL / Datadog / whichever
sum by (name) (
  count_over_time({job="rousseau-agent"} |= "tool.denied" [1w])
)
```

レポートはコンプライアンスドライブに行きます。slog スキーマが安定している ([可観測性](/ja/guides/observability/)) ため、パースは rousseau のアップグレードをまたいで壊れません。

## 監査人が尋ねないかもしれないが尋ねるべきこと

- **再現可能ビルド。** rousseau の CI には、新しいチェックアウトでビットレベルで同一の出力を検証する `reproducible-build` ジョブが含まれます。タグ付きソースから独立して再ビルドし、SHA-256 を比較できます。
- **依存関係の固定。** `go.mod` は正確なバージョンを固定します。`go.sum` は凍結されています。Dependabot はサイレントなバンプではなく、レビュー可能な PR としてアップデートを開きます。
- **すべてのコミットで `govulncheck`。** インポートされたシンボルに到達する任意の既知の脆弱性は CI を失敗させます。
- **すべてのコミットで CodeQL** 静的解析。

上記のすべては [セキュリティ](/ja/security/) にあります — コンプライアンスファイルドロワーはすでに存在します。

## テナント外境界

Bedrock が境界です。`bedrock-runtime.eu-west-1.amazonaws.com` へのトラフィックは Pod を離れますが、AWS 内に留まります。銀行のデータフロー図は Pod から Bedrock への 1 つの矢印を示します。このデプロイメントに他のアウトバウンド矢印は存在しません (Slack Socket Mode は `wss-primary.slack.com` へのアウトバウンド WSS であり、別途許可された egress として文書化されています)。

## 関連ページ

- [ガイド: Kubernetes デプロイ](/ja/guides/kubernetes-deployment/) — マニフェスト。
- [ガイド: 監査 + 承認ポリシー](/ja/guides/audit-approval-policies/) — コンプライアンスストーリー。
- [ガイド: 可観測性](/ja/guides/observability/) — slog パイプライン。
- [Bedrock プロバイダー](/ja/providers/bedrock/) — 認証情報チェーンとリージョン挙動。
- [セキュリティ](/ja/security/) — 信頼モデルとサプライチェーン制御。
