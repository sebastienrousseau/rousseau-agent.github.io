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
description: "Worked Kubernetes example for rousseau-agent: Deployment, PersistentVolumeClaim, Secret, SecurityContext, and PodSecurity restricted-profile posture."
keywords: "kubernetes, deployment, pvc, secret, security context, pod security, restricted, self-hosted"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/guides/kubernetes-deployment/"
subtitle: "Deployment, PVC, Secret, SecurityContext — restricted profile."
tags: "guides, kubernetes, deployment, pvc"
title: "ガイド：Kubernetes デプロイ"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "kubernetes, deployment, pvc, secret, security context, pod security, restricted, self-hosted"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ガイド：Kubernetes デプロイ"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 33
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/guides/kubernetes-deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/kubernetes-deployment/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "ガイド：Kubernetes デプロイ"
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
twitter_description: "Worked Kubernetes example for rousseau-agent: Deployment, PersistentVolumeClaim, Secret, SecurityContext, and PodSecurity restricted-profile posture."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "ガイド：Kubernetes デプロイ"
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

rousseau をクラスター内の他のサービスと並行して実行します。Podman + Quadlet リファレンスと同じランタイムポスチャ (非 root、読み取り専用のルートファイルシステム、全 capability の drop、seccomp デフォルト) を Kubernetes マニフェストとして表現します。インバウンドの HTTP サーフェスがないため、`Service` も `Ingress` も不要です。

## Namespace と PodSecurity プロファイル

Rousseau のポスチャは [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/) の *restricted* プロファイルを満たします。名前空間のデフォルトとして設定します。

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: rousseau
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
```

## Secret

プロバイダーの認証情報は、ConfigMap ではなく `Secret` に属します。

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: rousseau-secrets
  namespace: rousseau
type: Opaque
stringData:
  ANTHROPIC_API_KEY: "sk-ant-..."
  # 必要に応じて SLACK_APP_TOKEN、SLACK_BOT_TOKEN などを追加します。
```

Bedrock / Vertex では、長期の認証キーではなくワークロード ID (EKS では IRSA、GKE では Workload Identity) を推奨します。

## ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: rousseau-config
  namespace: rousseau
data:
  config.yaml: |
    provider: anthropic
    anthropic:
      model: claude-sonnet-4-6
      max_tokens: 4096

    log:
      level: info
      format: json

    state:
      path: /var/lib/rousseau/sessions.db

    agent:
      max_iterations: 32
      approver:
        mode: pattern
        default: deny
        allow:
          - {tool: read,  match: ".*"}
          - {tool: grep,  match: ".*"}
          - {tool: edit,  match: "^/workspace/.*"}
        deny:
          - {tool: bash,  match: "rm -rf|sudo|curl|wget"}

    slack:
      # トークンは環境変数を通じて Secret から取得します
      allowlist:
        - U0123456789
```

## PersistentVolumeClaim

セッションの状態はディスク上に存在します。クレームによって、Pod の再スケジュール時にも耐久性が保証されます。

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: rousseau-state
  namespace: rousseau
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 5Gi
  # 必要に応じて storageClassName を設定してください。
```

## Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rousseau-agent
  namespace: rousseau
spec:
  replicas: 1                            # 単一ライター。SQLite セッションストア
  strategy: { type: Recreate }           # PVC を共有する 2 つの Pod を回避
  selector:
    matchLabels: { app: rousseau-agent }
  template:
    metadata:
      labels: { app: rousseau-agent }
    spec:
      automountServiceAccountToken: false
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
        seccompProfile: { type: RuntimeDefault }
      containers:
        - name: rousseau
          image: ghcr.io/sebastienrousseau/rousseau-agent:<pin-a-tag>
          imagePullPolicy: IfNotPresent
          args: ["slack"]                # または "whatsapp"、"discord" など
          env:
            - name: ROUSSEAU_ANTHROPIC_API_KEY
              valueFrom:
                secretKeyRef: { name: rousseau-secrets, key: ANTHROPIC_API_KEY }
            - name: HOME
              value: /home/rousseau
          volumeMounts:
            - { name: config,    mountPath: /etc/rousseau, readOnly: true }
            - { name: state,     mountPath: /var/lib/rousseau }
            - { name: tmp,       mountPath: /tmp }
            - { name: home,      mountPath: /home/rousseau }
          command: ["/usr/local/bin/rousseau"]
          args:
            - --config
            - /etc/rousseau/config.yaml
            - slack
          resources:
            requests: { cpu: "100m", memory: "128Mi" }
            limits:   { cpu: "1000m", memory: "512Mi" }
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities: { drop: ["ALL"] }
      volumes:
        - name: config
          configMap: { name: rousseau-config }
        - name: state
          persistentVolumeClaim: { claimName: rousseau-state }
        - name: tmp
          emptyDir: { medium: Memory, sizeLimit: 64Mi }
        - name: home
          emptyDir: { medium: Memory, sizeLimit: 16Mi }
```

重要なポイント:

| フィールド | 根拠 |
|---|---|
| `runAsNonRoot: true` + `runAsUser: 1000` | コンテナイメージに一致します。デーモンが UID 0 を必要とすることはありません。 |
| `readOnlyRootFilesystem: true` | バイナリが自身のイメージを変更できません。 |
| `capabilities.drop: [ALL]` | 昇格された capability を必要とするトランスポートはありません。 |
| `allowPrivilegeEscalation: false` | setuid による昇格経路をブロックします。 |
| `seccompProfile: RuntimeDefault` | カーネルレベルの syscall ゲート。 |
| `automountServiceAccountToken: false` | Rousseau は Kubernetes API と通信しません。 |
| `replicas: 1` + `Recreate` | SQLite は単一ライターです。同じ PVC 上の 2 つの Pod はストアを破損させます。 |
| `/tmp` と `$HOME` に `emptyDir` | Pod 外に出ることのない書き込み可能なスクラッチ領域。 |

## `Service` も `Ingress` も不要

出荷されるすべてのトランスポートは、アウトバウンドの WebSocket (Slack Socket Mode、Discord Gateway)、サブプロセス (Signal)、またはポーリング (Telegram、Matrix、iMessage、Email) のいずれかを使用します。WhatsApp は whatsmeow のアウトバウンド TCP セッションを使用します。**インバウンドの HTTP サーフェスは存在しない** ため、`Service` も `Ingress` も不要です。

MCP サーバー (`rousseau mcp`) を有効にする場合、これは stdio のみです。`kubectl exec` で MCP クライアントを接続するか、同じ Pod にサイドカーとして配置してください。

## エグレスポリシー

デフォルトでエグレスを拒否する `NetworkPolicy` を運用している場合、rousseau に対して以下への到達を許可してください。

- LLM プロバイダーのエンドポイント (Anthropic は `api.anthropic.com`、リージョン固有の Bedrock / Vertex URL、あるいはターゲットが内部の vLLM であればそれ)。
- 有効化されている各トランスポートのエンドポイント (Slack: `wss://wss-primary.slack.com`、Discord: `wss://gateway.discord.gg`、WhatsApp: whatsmeow の TCP エンドポイントなど)。
- Pod 内で `cosign verify-blob` を実行する場合のみ、透過ログのエンドポイント。通常はランタイムではなくイメージビルド時に検証します。

## Helm (ロードマップ)

一次的な Helm チャートはロードマップに含まれています。`values.yaml` のドラフト:

```yaml
image:
  repository: ghcr.io/sebastienrousseau/rousseau-agent
  tag: v0.6.0
  pullPolicy: IfNotPresent

transport:
  name: whatsapp
  args: ["--allow", "447900123456@s.whatsapp.net"]

provider:
  name: anthropic
  # API キーは既存の Secret から取得します。生の値をテンプレート化してはいけません。
  existingSecret: rousseau-anthropic
  existingSecretKey: api_key

persistence:
  enabled: true
  size: 4Gi
  storageClassName: fast-ssd

resources:
  requests: { cpu: "100m", memory: "128Mi" }
  limits:   { cpu: "1",    memory: "512Mi" }

networkPolicy:
  enabled: true
  egressCIDRs:
    - 3.5.0.0/16      # Anthropic (例示。CIDR は変動します)
    - 157.240.0.0/16  # Meta

serviceAccount:
  create: true
  annotations: {}    # 例: IRSA では eks.amazonaws.com/role-arn

podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000

containerSecurityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities: { drop: [ALL] }
  seccompProfile: { type: RuntimeDefault }
```

チャートの提供状況は [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md) で追跡してください。

## ArgoCD アプリケーションマニフェスト

GitOps デプロイの場合:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: rousseau-agent
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/platform-manifests
    path: rousseau-agent
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: agents
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true
```

## NetworkPolicy の例

エグレスを LLM プロバイダーとトランスポートバックエンドのみに制限します。

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: rousseau-egress
  namespace: agents
spec:
  podSelector:
    matchLabels: { app: rousseau-agent }
  policyTypes: [Egress]
  egress:
    # CoreDNS への DNS
    - to:
        - namespaceSelector: { matchLabels: { kubernetes.io/metadata.name: kube-system } }
          podSelector: { matchLabels: { k8s-app: kube-dns } }
      ports:
        - protocol: UDP
          port: 53
    # Anthropic API
    - to:
        - ipBlock: { cidr: 3.5.0.0/16 }        # 例示的な CIDR
      ports:
        - protocol: TCP
          port: 443
```

<aside class="admonition" data-type="warning"><span class="admonition-title">CIDR の変動</span><p>プロバイダーの IP レンジは変動します。永続的なエグレス制御が必要な場合は、DNS ベースのエグレスプロキシ、または FQDN 対応ポリシーを持つサービスメッシュ (Istio、Linkerd) を推奨します。</p></aside>

## 注意点

- **SQLite は単一ライターを必要とします。** レプリカを 1 より上にスケールしないでください。HA が必要な場合は、高速なフェイルオーバースクリプトを備えたパッシブスタンバイを運用してください。同じ PVC に対して 2 つのアクティブライターを実行してはいけません。
- **セッションストアは保存時暗号化されていません。** ポリシー上必要な場合は、暗号化されたストレージクラス上に PVC をマウントしてください。
- **プロバイダーの認証情報** は常に `Secret` またはワークロード ID に保管し、ConfigMap には決して含めないでください。

## トラブルシューティング

### apply 時に `PodSecurity restricted violation`

名前空間が restricted PodSecurity プロファイルを強制しており、マニフェストに `runAsNonRoot`、seccomp プロファイルが欠けている、あるいは `allowPrivilegeEscalation: true` になっています。上記のマニフェストはこれらをすべて設定しています。行ごとに突き合わせて確認してください。

### PVC が `Pending` のまま

ストレージクラスが自動プロビジョニングしないか、要求サイズがクォータを超えています。`kubectl describe pvc rousseau-state` で確認してください。

### Pod が `api.anthropic.com` を解決できない

`NetworkPolicy` を通じて DNS が許可されていません。UDP/53 で `kube-dns` へのエグレスルールを追加してください。

### IRSA / Workload Identity: `NoCredentialProviders`

サービスアカウントのアノテーションが誤っているか欠落しています。`kubectl get sa rousseau -n agents -o yaml` で確認してください。アノテーションは ARN (AWS) または `iam.gke.io/gcp-service-account` (GCP) である必要があります。

### 新しいイメージのロールアウトで古い Pod は停止するが、新しい Pod が Ready にならない

`Recreate` 戦略では、新しい Pod が起動する前に古い Pod が停止します。新しいイメージが起動できない場合 (不正な設定、欠落した Secret) 、サービス停止となります。まず設定を修正してから再適用してください。

## 関連ページ

- [Deployment](/ja/deployment/) — リファレンスの Podman + Quadlet ポスチャ。
- [Guides: Observability](/ja/guides/observability/) — slog 出力をログパイプラインに配線する方法。
- [Guides: Audit &amp; Approval Policies](/ja/guides/audit-approval-policies/) — 監査人に提示する安全ポスチャ。
- [Providers: Bedrock](/ja/providers/bedrock/) — AWS 向けの IRSA セットアップ。
- [Providers: Vertex](/ja/providers/vertex/) — GCP 向けの Workload Identity セットアップ。

## さらに読む

- `docker/Dockerfile` — マニフェストが参照するイメージ。
- `docker/rousseau-agent.container` — Quadlet の同等物 (非 K8s の代替として)。
- Kubernetes docs: [PodSecurityStandards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)。
- Kubernetes docs: [NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/)。
