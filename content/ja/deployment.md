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
description: "Reference production deployment for rousseau-agent: rootless Podman + systemd Quadlet with dropped capabilities, read-only rootfs, seccomp, pasta networking. Kubernetes / OpenShift note."
keywords: "deployment, Podman, Quadlet, systemd, rootless, ReadOnly, DropCapability, NoNewPrivileges, seccomp, pasta, Kubernetes, OpenShift"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/deployment/"
subtitle: "rootless Podman と systemd Quadlet、Kubernetes に関するメモ付き。"
tags: "deployment, operations, container, systemd"
title: "デプロイ"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "deployment, Podman, Quadlet, systemd, rootless, ReadOnly, DropCapability, NoNewPrivileges, seccomp, pasta, Kubernetes, OpenShift"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "デプロイ"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "operations"
order: 25
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/deployment/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "デプロイ"
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
twitter_description: "Reference production deployment for rousseau-agent: rootless Podman + systemd Quadlet with dropped capabilities, read-only rootfs, seccomp, pasta networking. Kubernetes / OpenShift note."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "デプロイ"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">このページで学べること</span><p>rousseau がサポートする 3 つのデプロイトポロジー — ルートレス Podman + Quadlet（リファレンス）、素の Docker、Kubernetes — に加え、Vault、AWS Secrets Manager、GCP Secret Manager によるシークレット管理を扱います。リファレンス Quadlet の正典: <code>docker/rousseau-agent.container</code>。</p></aside>

## リファレンス構成

リファレンスデプロイは、systemd Quadlet ユニットで管理されるルートレス Podman コンテナです。単一ノード、Kubernetes 非依存、再起動後も存続し、root 権限は不要です。

正典: rousseau-agent リポジトリ内の `docker/rousseau-agent.container`。

## トポロジーの選択

<div class="tabs" data-tabs="deployment-topology">
  <div class="tab-list" role="tablist" aria-label="Deployment topology">
    <button role="tab" aria-selected="true">Podman + Quadlet</button>
    <button role="tab" aria-selected="false">Docker Compose</button>
    <button role="tab" aria-selected="false">Kubernetes</button>
  </div>
  <div class="tab-panel" role="tabpanel">

リファレンスデプロイです。ルートレス、堅牢化、再起動後も存続、オーケストレーター不要。

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
mkdir -p ~/.config/containers/systemd
cp docker/rousseau-agent.container ~/.config/containers/systemd/
systemctl --user daemon-reload
systemctl --user enable --now rousseau-agent.service
```

完全な Quadlet ユニットとその根拠は、このページの後半にあります。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Docker Compose は馴染みのある形ですが、Quadlet のようにセキュリティ姿勢を強制しません。堅牢化フラグを手作業ですべて設定する必要があります。

```yaml
services:
  rousseau:
    image: rousseau-agent:local
    read_only: true
    cap_drop: [ALL]
    security_opt:
      - no-new-privileges:true
      - seccomp:default
    user: "1000:1000"
    tmpfs:
      - /tmp:size=64m,mode=1777
    volumes:
      - ${HOME}/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
      - ${HOME}/.claude:/home/rousseau/.claude:rw,Z
      - ${HOME}/team-rousseau-workspace:/workspace:rw,Z
    environment:
      HOME: /home/rousseau
    restart: unless-stopped
    command: ["whatsapp", "--allow", "447900123456@s.whatsapp.net"]
```

<aside class="admonition" data-type="warning"><span class="admonition-title">root Docker</span><p>従来の Docker デーモンは root で動作します。<code>user: "1000:1000"</code> を指定しても、デーモンは Docker ソケットの所有者の capability を持ちます。ルートレス Docker または Podman を推奨します。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Kubernetes には Deployment と PVC が必要です。以下のマニフェストと、完全な Helm チャート例については [ガイド: Kubernetes デプロイ](/ja/guides/kubernetes-deployment/) を参照してください。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: rousseau-agent, namespace: agents }
spec:
  replicas: 1
  strategy: { type: Recreate }
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        seccompProfile: { type: RuntimeDefault }
      containers:
        - name: rousseau
          image: ghcr.io/sebastienrousseau/rousseau-agent:v0.6.0
          args: ["whatsapp", "--allow", "447900123456@s.whatsapp.net"]
          securityContext:
            allowPrivilegeEscalation: false
            capabilities: { drop: [ALL] }
            readOnlyRootFilesystem: true
          volumeMounts:
            - { name: state, mountPath: /home/rousseau/.local/share/rousseau }
            - { name: tmp,   mountPath: /tmp }
      volumes:
        - name: state
          persistentVolumeClaim: { claimName: rousseau-state }
        - name: tmp
          emptyDir: { medium: Memory, sizeLimit: 64Mi }
```

  </div>
</div>

## シークレット管理

API キーやトークンを `config.yaml` にコミットしてはいけません。実行時にシークレットバックエンドからロードしてください。

<div class="tabs" data-tabs="deployment-secrets">
  <div class="tab-list" role="tablist" aria-label="Secrets backend">
    <button role="tab" aria-selected="true">HashiCorp Vault</button>
    <button role="tab" aria-selected="false">AWS Secrets Manager</button>
    <button role="tab" aria-selected="false">GCP Secret Manager</button>
    <button role="tab" aria-selected="false">systemd credentials</button>
  </div>
  <div class="tab-panel" role="tabpanel">

`vault agent` を使って環境変数をファイルにレンダリングし、rousseau に読み込ませます。サンプルテンプレート:

```
{{- with secret "kv/rousseau/anthropic" }}
ANTHROPIC_API_KEY={{ .Data.data.api_key }}
{{- end }}
```

Systemd:

```ini
[Service]
EnvironmentFile=/run/rousseau/env
ExecStartPre=/usr/local/bin/vault-agent -config=/etc/vault/agent.hcl
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

`aws secretsmanager` を使って起動時に env ファイルへキーを取り込みます。

```sh
aws secretsmanager get-secret-value \
  --secret-id rousseau/anthropic \
  --query SecretString --output text | \
  jq -r '"ANTHROPIC_API_KEY=\(.api_key)"' > /run/rousseau/env
```

Systemd:

```ini
[Service]
EnvironmentFile=/run/rousseau/env
ExecStartPre=/usr/local/bin/fetch-secrets.sh
```

EKS 上の IRSA と組み合わせれば SDK が透過的に認証情報を解決し、ホスト上に静的な AWS キーを持たずに済みます。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

`gcloud secrets versions access` を使用します。

```sh
gcloud secrets versions access latest --secret=rousseau-anthropic > /run/rousseau/api_key
```

または Kubernetes 上では、[Secret Manager CSI ドライバ](https://cloud.google.com/secret-manager/docs/secret-manager-managed-csi-component) を用いてシークレットをファイルとしてマウントできます。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

systemd credentials（systemd 250 以降で利用可能）はユニット開始時にシークレットをメモリに読み込みます。

```ini
[Service]
LoadCredential=anthropic_key:/etc/rousseau/anthropic.key
ExecStart=/usr/local/bin/rousseau chat
```

デーモンは起動時に `$CREDENTIALS_DIRECTORY/anthropic_key` を読み取ります。（暗号化された）認証情報ストア以外にディスクへの書き込みは行われません。

  </div>
</div>

## イメージのビルド

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
```

マルチステージビルドです。ステージ 1 は `golang:1.26-alpine` が静的バイナリをコンパイル（`CGO_ENABLED=0`）し、ステージ 2 は `node:22-alpine` が `claude` CLI サブプロセスを提供します。実行時イメージは約 550 MB で、Node レイヤーはオプションの `claudecli` プロバイダのために存在するだけです。

別のプロバイダ（Anthropic 直接、Bedrock、Vertex、OpenAI 互換）を使う場合は、Node ランタイムを削除してイメージを縮小できます。

## Quadlet ユニットのインストール

```sh
mkdir -p ~/.config/containers/systemd
cp docker/rousseau-agent.container ~/.config/containers/systemd/
systemctl --user daemon-reload
systemctl --user start rousseau-agent.service
journalctl --user -u rousseau-agent.service -f
```

lingering が有効か確認したうえで（`loginctl enable-linger $USER`）、`systemctl --user enable rousseau-agent.service` で起動時に有効化します。

## 実行時の姿勢 — Quadlet の全設定

| 設定 | 値 | 根拠 |
|---|---|---|
| `Network=pasta` | ルートレスネットワークスタック | `slirp4netns` は最近の Podman から削除されました。pasta は現代的なカーネル上で高速で、デフォルトでホストからの受信をブロックします。 |
| `UserNS=keep-id` | コンテナ UID 1000 → ホスト UID 1000 | バインドマウントされたファイルはホストの所有権を保ち、コンテナプロセスはホスト所有のファイルに書き込めます。 |
| `ReadOnly=true` | ルートファイルシステム読み取り専用 | デーモンは実行時にイメージを変更すべきではありません。書き込み可能なものはバインドマウントか tmpfs 上に置きます。 |
| `Tmpfs=/tmp:rw,size=64m,mode=1777` | 書き込み可能なスクラッチ | 実行時にスクラッチファイルが必要な場合用（まれ）。 |
| `DropCapability=all` | すべての capability を drop | Go バイナリに昇格した capability は不要です。送信 TCP に `CAP_NET_BIND_SERVICE` などは必要ありません。 |
| `NoNewPrivileges=true` | `no_new_privs` ビット設定 | コンテナ内での setuid 昇格を阻止します。 |
| `SeccompProfile=/usr/share/containers/seccomp.json` | デフォルト seccomp フィルタ | drop した capability に加え、カーネルレベルのシステムコールゲート。 |
| `Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z` | 状態バインドマウント | セッション、WhatsApp ペアリング、cron ジョブ、JID マップ、FTS5 インデックス。`:Z` は SELinux ラベルを設定します。 |
| `Volume=%h/.claude:/home/rousseau/.claude:rw,Z` | `claude` CLI 認証 | `claudecli` プロバイダを使用する場合のみ関連。`claude` はキャッシュされた OAuth をその場でリフレッシュします。 |
| `Volume=%h/team-rousseau-workspace:/workspace:rw,Z` | ワークスペース | コンテナ内から見えるのはワークスペースのみで、ホスト上の他のものはマウントされません。 |
| `Environment=HOME=/home/rousseau` | `$HOME` の設定 | Viper、`claude` CLI、状態ディレクトリリゾルバが使用します。 |
| `AutoUpdate=disabled` | Podman は自動更新しない | 更新はオペレーターがリリースの節目で行い、暗黙に行われることはありません。 |

## `Exec=` 行

Quadlet には以下が含まれます。

```
Exec=whatsapp --allow 447906009073@s.whatsapp.net
```

選択したトランスポートと allowlist に置き換えてください。複数のトランスポートは通常、別々の Quadlet ユニットで動作させます（イメージ 1 つ、バイナリ 1 つ、ユニット複数）。これにより 1 つのトランスポートの障害が他のトランスポートを巻き添えにしません。

## Kubernetes / OpenShift

`rousseau` は単一バイナリのデーモンです。状態ディレクトリ用の最小限の `Deployment` + `PersistentVolumeClaim` で十分です。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rousseau-agent
spec:
  replicas: 1
  strategy:
    type: Recreate           # do not run two daemons against one state DB
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        seccompProfile: {type: RuntimeDefault}
      containers:
        - name: rousseau
          image: registry.example.com/rousseau-agent:v1.0.0
          args: ["whatsapp", "--allow", "447900123456@s.whatsapp.net"]
          securityContext:
            allowPrivilegeEscalation: false
            capabilities: {drop: [ALL]}
            readOnlyRootFilesystem: true
          volumeMounts:
            - {name: state, mountPath: /home/rousseau/.local/share/rousseau}
            - {name: tmp,   mountPath: /tmp}
      volumes:
        - name: state
          persistentVolumeClaim: {claimName: rousseau-state}
        - name: tmp
          emptyDir: {medium: Memory, sizeLimit: 64Mi}
```

受信 HTTP サーフェスが存在しないため、送信 WebSocket 型のトランスポート（Slack、Discord、WhatsApp、Matrix）には **`Service` も `Ingress` も不要** です。webhook 型のトランスポートだけが `Service` を必要としますが、rousseau はデフォルトでは webhook 型を同梱していません。

`Recreate` 戦略は意図的です。SQLite の状態ファイルは 2 つの同時ライターを想定していません。HA が必要な場合は、トランスポートごとに 1 つのデーモンを動かし、再接続セマンティクスはトランスポート自身の状態（Slack Socket Mode、Discord Gateway）に依存させます。

## systemd ログの送信先

Quadlet は systemd のジャーナル設定を継承します。`journalctl --user -u rousseau-agent.service` でログを読めます。ログ集約には journal-to-Loki / journal-to-Fluent-Bit サイドカーを利用し、rousseau のログをそのままディスクにパイプしないでください（rousseau 自身はログローテーションを行いません）。

集約器がパースできるように rousseau に JSON を出力させます。

```yaml
log:
  level: info
  format: json
```

## Nftables 送信ロックダウン（オプション）

ソースツリー内の `docker/nftables.rules.example` はカーネルレベルの送信堅牢化テンプレートを提供します。Meta の WhatsApp Web レンジ、Anthropic（CloudFront 経由のためドメインベースフィルタ）、Signal 以外はすべて drop します。コンテナ名前空間の上にこれを重ねると最も堅い姿勢になります。理由は [セキュリティ](/ja/security/) を参照してください。

## Helm チャート（ロードマップ）

一次配布の Helm チャートはロードマップにあります。リリースされるまでは、上記のマニフェストで最小限のデプロイには十分です。進捗は [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md) を追跡してください。

`values.yaml` の草案（利用予定者のレビュー用）:

```yaml
image:
  repository: ghcr.io/sebastienrousseau/rousseau-agent
  tag: v0.6.0
transport:
  name: whatsapp
  args: ["--allow", "447900123456@s.whatsapp.net"]
provider:
  name: anthropic
  # api_key sourced from a Secret
persistence:
  size: 4Gi
  storageClass: fast-ssd
resources:
  requests: { cpu: "100m", memory: "128Mi" }
  limits:   { cpu: "1",    memory: "512Mi" }
networkPolicy:
  enabled: true
  # egress: allowed CIDRs list
```

## トラブルシューティング

### `podman play kube` がバインドマウントで `permission denied` を返す

SELinux ラベルが欠けています。すべてのボリュームは `:Z`（共有の場合は `:z`）で終える必要があります。[トラブルシューティング: コンテナがバインドマウントに失敗する](/ja/troubleshooting/#container-fails-to-bind-mount) を参照してください。

### Kubernetes Pod が初回起動時に CrashLoopBackOff になる

状態ボリュームが事前作成されていないか、その所有権が UID 1000 と一致していません。ボリュームを `chown` する initContainer を追加してください。

```yaml
initContainers:
  - name: chown-state
    image: busybox
    command: ["sh", "-c", "chown -R 1000:1000 /state"]
    volumeMounts: [{ name: state, mountPath: /state }]
    securityContext: { runAsUser: 0 }
```

### `systemctl --user` が Quadlet ユニットを見つけられない

`daemon-reload` が実行されていないか、ユニットファイルにタイポがあります。`systemctl --user cat rousseau-agent.service` で確認してください。Quadlet はユニットを動的に生成するため、cat が最速のデバッグ手段です。

### 再起動後にデーモンが起動しない

lingering を有効化してください: `loginctl enable-linger $USER`。lingering がないと、systemd のユーザーマネージャはログアウト時に終了し、次のログインまで再起動しません。

### 2 つのデーモンが競合し、状態 DB が壊れた

同じ `state.path` に対して 2 つのデーモンを絶対に走らせないでください。破損した場合はファイルをバックアップし、`rm sessions.db{,-wal,-shm}`、再起動します。セッション履歴は失われますが、`whatsapp.db` が別ファイル（デフォルトで別）ならペアリングは残ります。

## 関連ページ

- [ガイド: Kubernetes デプロイ](/ja/guides/kubernetes-deployment/) — 完全な Helm チャートと NetworkPolicy の例。
- [ガイド: 本番デプロイ](/ja/guides/production-deployment/) — 本番向けチェックリスト。
- [ガイド: 可観測性](/ja/guides/observability/) — ログとメトリクス。
- [セキュリティ](/ja/security/) — 信頼境界、seccomp、送信制御。
- [設定](/ja/configuration/) — すべてのノブ。

## さらに読む

- `docker/Dockerfile` — マルチステージビルド。
- `docker/rousseau-agent.container` — Quadlet ユニット。
- `docker/example-nftables.rules` — サンプル送信ルールセット。
- `Makefile` — ビルド自動化。
- systemd ドキュメント: [Quadlet](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html)。
