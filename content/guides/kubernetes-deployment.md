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
hreflang: "en"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "en-GB"
locale: "en_GB"
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
permalink: "https://docs.rousseau-agent.dev/guides/kubernetes-deployment/"
subtitle: "Deployment, PVC, Secret, SecurityContext — restricted profile."
tags: "guides, kubernetes, deployment, pvc"
title: "Guide: Kubernetes Deployment"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "kubernetes, deployment, pvc, secret, security context, pod security, restricted, self-hosted"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide: Kubernetes Deployment"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 33
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/kubernetes-deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/kubernetes-deployment/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guide: Kubernetes Deployment"
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
twitter_title: "Guide: Kubernetes Deployment"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Scenario

You run rousseau alongside other in-cluster services. You want the same runtime posture as the Podman + Quadlet reference — non-root, read-only root filesystem, all capabilities dropped, seccomp default — expressed as Kubernetes manifests. No inbound HTTP surface, so no `Service` and no `Ingress`.

## Namespace + PodSecurity profile

Rousseau's posture satisfies the [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/) *restricted* profile. Set that as the namespace default:

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

Provider credentials belong in a `Secret`, not the ConfigMap.

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

For Bedrock / Vertex, prefer workload identity (IRSA on EKS, Workload Identity on GKE) over long-lived keys.

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

Session state lives on disk. The claim ensures durability across pod rescheduling.

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

The important bits:

| Field | Rationale |
|---|---|
| `runAsNonRoot: true` + `runAsUser: 1000` | Matches the container image; the daemon never needs UID 0. |
| `readOnlyRootFilesystem: true` | The binary cannot mutate its own image. |
| `capabilities.drop: [ALL]` | No transport needs elevated capabilities. |
| `allowPrivilegeEscalation: false` | Blocks setuid escalation paths. |
| `seccompProfile: RuntimeDefault` | Kernel-level syscall gating. |
| `automountServiceAccountToken: false` | Rousseau does not talk to the Kubernetes API. |
| `replicas: 1` + `Recreate` | SQLite is single-writer; two pods on the same PVC will corrupt the store. |
| `emptyDir` for `/tmp` and `$HOME` | Writable scratch that never leaves the pod. |

## No `Service`, no `Ingress`

Every shipped transport uses either an outbound WebSocket (Slack Socket Mode, Discord Gateway), a subprocess (Signal), or polling (Telegram, Matrix, iMessage, Email). WhatsApp uses whatsmeow's outbound TCP session. **There is no inbound HTTP surface**, so no `Service` and no `Ingress` are required.

If you enable the MCP server (`rousseau mcp`), that is stdio-only — attach an MCP client via `kubectl exec` or side-car it into the same pod.

## Egress policy

If you run a `NetworkPolicy` denying egress by default, allow rousseau to reach:

- The LLM provider endpoint (`api.anthropic.com` for Anthropic, region-specific Bedrock / Vertex URLs, or your internal vLLM if that's the target).
- Each enabled transport's endpoints (Slack: `wss://wss-primary.slack.com`, Discord: `wss://gateway.discord.gg`, WhatsApp: whatsmeow's TCP endpoints, etc.).
- The transparency log endpoints only if you run `cosign verify-blob` inside the pod — normally you verify at image-build time, not runtime.

## Helm (roadmap)

A first-party Helm chart is on the roadmap. Draft `values.yaml`:

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

Track [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md) for chart availability.

## ArgoCD application manifest

For GitOps deployments:

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

## NetworkPolicy example

Restrict egress to only the LLM provider and the transport backends:

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

<aside class="admonition" data-type="warning"><span class="admonition-title">CIDR churn</span><p>Provider IP ranges shift. Prefer a DNS-based egress proxy or a service mesh (Istio, Linkerd) with FQDN-aware policy if you need durable egress control.</p></aside>

## Caveats

- **SQLite requires a single writer.** Do not scale replicas above 1. If you need HA, run a passive standby with a fast failover script — do not run two active writers against the same PVC.
- **Session store is not encrypted at rest.** Mount the PVC on an encrypted storage class if required by policy.
- **Provider auth material** should always live in `Secret` or workload identity, never in the ConfigMap.

## Troubleshooting

### `PodSecurity restricted violation` on apply

Your namespace enforces the restricted PodSecurity profile and the manifest is missing `runAsNonRoot`, a seccomp profile, or has `allowPrivilegeEscalation: true`. The manifests above set all of these — cross-check line by line.

### PVC stuck in `Pending`

Your storage class does not provision automatically, or the requested size exceeds the quota. Check with `kubectl describe pvc rousseau-state`.

### Pod cannot resolve `api.anthropic.com`

DNS not allowed through your `NetworkPolicy`. Add an egress rule to `kube-dns` on UDP/53.

### IRSA / Workload Identity: `NoCredentialProviders`

Service account annotation is wrong or missing. Verify with `kubectl get sa rousseau -n agents -o yaml` — the annotation must be an ARN (AWS) or a `iam.gke.io/gcp-service-account` (GCP).

### Rolling out a new image kills the old pod but the new one never becomes Ready

The `Recreate` strategy means the old pod stops before the new one starts. If the new image cannot start (bad config, missing secret), you have an outage. Fix the config first, then re-apply.

## Related pages

- [Deployment](/deployment/) — the reference Podman + Quadlet posture.
- [Guides: Observability](/guides/observability/) — wire slog output into your log pipeline.
- [Guides: Audit &amp; Approval Policies](/guides/audit-approval-policies/) — the safety posture you present to auditors.
- [Providers: Bedrock](/providers/bedrock/) — IRSA setup for AWS.
- [Providers: Vertex](/providers/vertex/) — Workload Identity setup for GCP.

## Further reading

- `docker/Dockerfile` — the image the manifests reference.
- `docker/rousseau-agent.container` — the Quadlet equivalent (for a non-K8s alternative).
- Kubernetes docs: [PodSecurityStandards](https://kubernetes.io/docs/concepts/security/pod-security-standards/).
- Kubernetes docs: [NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/).
