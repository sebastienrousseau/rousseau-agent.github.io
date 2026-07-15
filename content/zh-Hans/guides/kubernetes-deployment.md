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
hreflang: "zh-Hans"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "zh-Hans"
locale: "zh_CN"
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
permalink: "https://docs.rousseau-agent.dev/zh-Hans/guides/kubernetes-deployment/"
subtitle: "Deployment, PVC, Secret, SecurityContext — restricted profile."
tags: "guides, kubernetes, deployment, pvc"
title: "指南：Kubernetes 部署"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "kubernetes, deployment, pvc, secret, security context, pod security, restricted, self-hosted"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "指南：Kubernetes 部署"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 33
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/guides/kubernetes-deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/kubernetes-deployment/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "指南：Kubernetes 部署"
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
twitter_title: "指南：Kubernetes 部署"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "感谢每一位运行自有编码代理的运维者。"
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## 场景

你在集群中与其他服务并肩运行 rousseau。你希望以 Kubernetes 清单表达与 Podman + Quadlet 参考一致的运行时姿态 —— 非 root、只读根文件系统、放弃所有 capability、默认 seccomp。因为没有入站 HTTP 接口，所以不需要 `Service` 和 `Ingress`。

## Namespace + PodSecurity profile

Rousseau 的姿态满足 [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/) 的 *restricted* profile。把它设为该命名空间的默认：

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

Provider 凭据应放在 `Secret` 中，而不是 ConfigMap。

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: rousseau-secrets
  namespace: rousseau
type: Opaque
stringData:
  ANTHROPIC_API_KEY: "sk-ant-..."
  # Add SLACK_APP_TOKEN, SLACK_BOT_TOKEN, etc. as needed.
```

对于 Bedrock / Vertex，优先使用 workload identity（EKS 上的 IRSA，GKE 上的 Workload Identity），而非长期密钥。

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
      # tokens come from the Secret via env vars
      allowlist:
        - U0123456789
```

## PersistentVolumeClaim

会话状态保存在磁盘上。该 claim 确保跨 Pod 重新调度时状态的持久性。

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
  # Set your storageClassName as appropriate.
```

## Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rousseau-agent
  namespace: rousseau
spec:
  replicas: 1                            # single-writer; SQLite session store
  strategy: { type: Recreate }           # avoid two pods sharing the PVC
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
          args: ["slack"]                # or "whatsapp", "discord", etc.
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

关键点：

| 字段 | 理由 |
|---|---|
| `runAsNonRoot: true` + `runAsUser: 1000` | 与容器镜像匹配；守护进程从不需要 UID 0。 |
| `readOnlyRootFilesystem: true` | 二进制无法修改自身镜像。 |
| `capabilities.drop: [ALL]` | 没有传输需要提升的 capability。 |
| `allowPrivilegeEscalation: false` | 屏蔽 setuid 提升路径。 |
| `seccompProfile: RuntimeDefault` | 内核级 syscall 门控。 |
| `automountServiceAccountToken: false` | Rousseau 不与 Kubernetes API 通信。 |
| `replicas: 1` + `Recreate` | SQLite 是单写者；两个 Pod 共用同一 PVC 会损坏存储。 |
| `/tmp` 与 `$HOME` 使用 `emptyDir` | 可写的临时区，永不离开 Pod。 |

## 没有 `Service`，没有 `Ingress`

所有随包发布的传输要么使用出站 WebSocket（Slack Socket Mode、Discord Gateway），要么使用子进程（Signal），要么使用轮询（Telegram、Matrix、iMessage、Email）。WhatsApp 使用 whatsmeow 的出站 TCP 会话。**没有入站 HTTP 接口**，因此不需要 `Service` 与 `Ingress`。

如果你启用 MCP 服务器（`rousseau mcp`），那只使用 stdio —— 请通过 `kubectl exec` 挂接 MCP 客户端，或以 sidecar 形式放入同一 Pod。

## 出站策略

如果你运行的 `NetworkPolicy` 默认拒绝出站，请允许 rousseau 访问：

- LLM provider 端点（Anthropic 是 `api.anthropic.com`，或按区域的 Bedrock / Vertex URL，或你的内部 vLLM）。
- 每个启用传输的端点（Slack：`wss://wss-primary.slack.com`，Discord：`wss://gateway.discord.gg`，WhatsApp：whatsmeow 的 TCP 端点，等等）。
- 透明日志端点，仅在 Pod 内运行 `cosign verify-blob` 时需要 —— 通常在镜像构建期校验，而非运行期。

## Helm（路线图）

官方 Helm chart 在路线图中。示例 `values.yaml` 草稿：

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
  # API key sourced from an existing secret; do not template raw values.
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
    - 3.5.0.0/16      # Anthropic (illustrative — CIDRs shift)
    - 157.240.0.0/16  # Meta

serviceAccount:
  create: true
  annotations: {}    # e.g. eks.amazonaws.com/role-arn for IRSA

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

chart 的可用性请跟踪 [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md)。

## ArgoCD 应用清单

用于 GitOps 部署：

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

## NetworkPolicy 示例

将出站限制为仅 LLM provider 与传输后端：

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
    # DNS to CoreDNS
    - to:
        - namespaceSelector: { matchLabels: { kubernetes.io/metadata.name: kube-system } }
          podSelector: { matchLabels: { k8s-app: kube-dns } }
      ports:
        - protocol: UDP
          port: 53
    # Anthropic API
    - to:
        - ipBlock: { cidr: 3.5.0.0/16 }        # illustrative CIDR
      ports:
        - protocol: TCP
          port: 443
```

<aside class="admonition" data-type="warning"><span class="admonition-title">CIDR 变动</span><p>Provider 的 IP 范围会变动。如果你需要持久的出站控制，请优先使用基于 DNS 的出站代理，或使用带 FQDN 感知策略的服务网格（Istio、Linkerd）。</p></aside>

## 注意事项

- **SQLite 要求单写者。** 请勿将副本数调到 1 以上。如需 HA，请运行一个被动 standby，并配一个快速故障切换脚本 —— 不要针对同一 PVC 运行两个活跃写者。
- **会话存储在磁盘上未加密。** 如果策略要求，请把 PVC 挂载到加密的 storage class 上。
- **Provider 鉴权凭据**必须放在 `Secret` 或 workload identity 中，绝不要放在 ConfigMap。

## 故障排查

### 应用时报 `PodSecurity restricted violation`

你的命名空间强制执行 restricted PodSecurity profile，而清单缺少 `runAsNonRoot`、seccomp profile，或存在 `allowPrivilegeEscalation: true`。上面的清单都设置了这些 —— 请逐行核对。

### PVC 卡在 `Pending`

你的 storage class 未自动 provision，或请求的容量超过配额。用 `kubectl describe pvc rousseau-state` 查看。

### Pod 无法解析 `api.anthropic.com`

DNS 未被 `NetworkPolicy` 放行。请添加一条到 `kube-dns` 的 UDP/53 出站规则。

### IRSA / Workload Identity：`NoCredentialProviders`

Service account 注解错误或缺失。用 `kubectl get sa rousseau -n agents -o yaml` 验证 —— 注解必须是 ARN（AWS）或 `iam.gke.io/gcp-service-account`（GCP）。

### 发布新镜像时旧 Pod 停止但新 Pod 始终不 Ready

`Recreate` 策略意味着新 Pod 启动前旧 Pod 会先停止。若新镜像无法启动（配置错误、缺少 secret），你就会经历一段停服。请先修复配置，再重新 apply。

## 相关页面

- [部署](/zh-Hans/deployment/) —— 参考的 Podman + Quadlet 姿态。
- [指南：可观测性](/zh-Hans/guides/observability/) —— 把 slog 输出接入日志管道。
- [指南：审计与审批策略](/zh-Hans/guides/audit-approval-policies/) —— 对审计员展示的安全姿态。
- [Providers：Bedrock](/zh-Hans/providers/bedrock/) —— AWS 上的 IRSA 配置。
- [Providers：Vertex](/zh-Hans/providers/vertex/) —— GCP 上的 Workload Identity 配置。

## 延伸阅读

- `docker/Dockerfile` —— 清单引用的镜像。
- `docker/rousseau-agent.container` —— 对应的 Quadlet（非 K8s 备选）。
- Kubernetes 文档：[PodSecurityStandards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)。
- Kubernetes 文档：[NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/)。
