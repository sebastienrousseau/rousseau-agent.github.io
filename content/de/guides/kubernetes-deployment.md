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
hreflang: "de"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "de"
locale: "de_DE"
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
permalink: "https://docs.rousseau-agent.dev/de/guides/kubernetes-deployment/"
subtitle: "Deployment, PVC, Secret, SecurityContext — restricted profile."
tags: "guides, kubernetes, deployment, pvc"
title: "Leitfaden: Kubernetes-Bereitstellung"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "kubernetes, deployment, pvc, secret, security context, pod security, restricted, self-hosted"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Leitfaden: Kubernetes-Bereitstellung"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 33
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/kubernetes-deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/kubernetes-deployment/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Leitfaden: Kubernetes-Bereitstellung"
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
twitter_title: "Leitfaden: Kubernetes-Bereitstellung"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Danke an jeden Operator, der seinen eigenen Coding-Agenten betreibt."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Szenario

Sie betreiben rousseau neben anderen In-Cluster-Diensten. Sie möchten die gleiche Laufzeit-Haltung wie im Podman + Quadlet-Referenzsetup — non-root, Read-Only-Root-Filesystem, alle Capabilities entfernt, seccomp default — als Kubernetes-Manifeste ausdrücken. Keine eingehende HTTP-Fläche, also weder `Service` noch `Ingress`.

## Namespace + PodSecurity-Profil

Rousseaus Haltung erfüllt das Profil *restricted* der [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/). Als Namespace-Default setzen:

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

Provider-Zugangsdaten gehören in ein `Secret`, nicht in die ConfigMap.

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

Für Bedrock / Vertex Workload Identity (IRSA auf EKS, Workload Identity auf GKE) langlebigen Schlüsseln vorziehen.

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

Der Session-Zustand liegt auf der Platte. Der Claim sorgt für Durability über Pod-Rescheduling hinweg.

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

Die wichtigen Bausteine:

| Feld | Begründung |
|---|---|
| `runAsNonRoot: true` + `runAsUser: 1000` | Entspricht dem Container-Image; der Daemon benötigt nie UID 0. |
| `readOnlyRootFilesystem: true` | Das Binary kann sein eigenes Image nicht verändern. |
| `capabilities.drop: [ALL]` | Kein Transport benötigt erhöhte Capabilities. |
| `allowPrivilegeEscalation: false` | Blockiert setuid-Eskalationspfade. |
| `seccompProfile: RuntimeDefault` | Syscall-Gating auf Kernel-Ebene. |
| `automountServiceAccountToken: false` | Rousseau spricht nicht mit der Kubernetes-API. |
| `replicas: 1` + `Recreate` | SQLite ist Single-Writer; zwei Pods auf demselben PVC korrumpieren den Store. |
| `emptyDir` für `/tmp` und `$HOME` | Beschreibbarer Scratch-Speicher, der den Pod nie verlässt. |

## Kein `Service`, kein `Ingress`

Jeder ausgelieferte Transport nutzt entweder einen ausgehenden WebSocket (Slack Socket Mode, Discord Gateway), einen Subprozess (Signal) oder Polling (Telegram, Matrix, iMessage, Email). WhatsApp verwendet die ausgehende TCP-Session von whatsmeow. **Es gibt keine eingehende HTTP-Fläche**, weshalb weder `Service` noch `Ingress` erforderlich sind.

Wenn Sie den MCP-Server (`rousseau mcp`) aktivieren, ist dieser stdio-only — einen MCP-Client per `kubectl exec` anfügen oder als Side-Car in denselben Pod legen.

## Egress-Policy

Wenn Sie eine `NetworkPolicy` betreiben, die Egress standardmäßig ablehnt, erlauben Sie rousseau den Zugriff auf:

- Den LLM-Provider-Endpunkt (`api.anthropic.com` für Anthropic, regionspezifische Bedrock- / Vertex-URLs oder Ihr internes vLLM, wenn das das Ziel ist).
- Die Endpunkte jedes aktivierten Transports (Slack: `wss://wss-primary.slack.com`, Discord: `wss://gateway.discord.gg`, WhatsApp: die TCP-Endpunkte von whatsmeow usw.).
- Die Transparency-Log-Endpunkte nur, wenn Sie `cosign verify-blob` innerhalb des Pods ausführen — normalerweise verifizieren Sie zur Image-Build-Zeit, nicht zur Laufzeit.

## Helm (Roadmap)

Ein first-party Helm-Chart steht auf der Roadmap. Entwurf `values.yaml`:

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

Zur Verfügbarkeit des Charts siehe [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md).

## ArgoCD-Application-Manifest

Für GitOps-Deployments:

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

## NetworkPolicy-Beispiel

Egress auf LLM-Provider und Transport-Backends beschränken:

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

<aside class="admonition" data-type="warning"><span class="admonition-title">CIDR-Churn</span><p>IP-Bereiche der Provider ändern sich. Bevorzugen Sie einen DNS-basierten Egress-Proxy oder ein Service-Mesh (Istio, Linkerd) mit FQDN-fähiger Policy, wenn Sie eine dauerhaft belastbare Egress-Kontrolle benötigen.</p></aside>

## Einschränkungen

- **SQLite erfordert einen Single-Writer.** Skalieren Sie die Replikate nicht über 1 hinaus. Bei HA-Bedarf einen passiven Standby mit schnellem Failover-Skript betreiben — niemals zwei aktive Writer gegen dasselbe PVC.
- **Der Session-Store ist nicht verschlüsselt at rest.** Das PVC auf einer verschlüsselten Storage-Class einhängen, falls die Policy dies verlangt.
- **Auth-Material des Providers** gehört stets in ein `Secret` oder in Workload Identity, niemals in die ConfigMap.

## Troubleshooting

### `PodSecurity restricted violation` beim Apply

Ihr Namespace erzwingt das restricted-PodSecurity-Profil, und dem Manifest fehlen `runAsNonRoot`, ein seccomp-Profil oder es setzt `allowPrivilegeEscalation: true`. Die obigen Manifeste setzen all dies — Zeile für Zeile abgleichen.

### PVC hängt in `Pending`

Ihre Storage-Class provisioniert nicht automatisch, oder die angeforderte Größe überschreitet das Quota. Mit `kubectl describe pvc rousseau-state` prüfen.

### Pod kann `api.anthropic.com` nicht auflösen

DNS ist durch Ihre `NetworkPolicy` nicht erlaubt. Eine Egress-Regel zu `kube-dns` auf UDP/53 hinzufügen.

### IRSA / Workload Identity: `NoCredentialProviders`

Die Service-Account-Annotation ist falsch oder fehlt. Mit `kubectl get sa rousseau -n agents -o yaml` prüfen — die Annotation muss eine ARN (AWS) oder ein `iam.gke.io/gcp-service-account` (GCP) sein.

### Ausrollen eines neuen Images beendet den alten Pod, aber der neue wird nie Ready

Die `Recreate`-Strategie hält den alten Pod an, bevor der neue startet. Kann das neue Image nicht starten (falsche Konfiguration, fehlendes Secret), haben Sie einen Ausfall. Zuerst die Konfiguration korrigieren, dann erneut anwenden.

## Verwandte Seiten

- [Deployment](/de/deployment/) — die Referenz-Haltung mit Podman + Quadlet.
- [Leitfäden: Observability](/de/guides/observability/) — slog-Ausgabe in die Log-Pipeline einbinden.
- [Leitfäden: Audit- &amp; Genehmigungsrichtlinien](/de/guides/audit-approval-policies/) — die Sicherheitsdarstellung gegenüber Auditoren.
- [Providers: Bedrock](/de/providers/bedrock/) — IRSA-Setup für AWS.
- [Providers: Vertex](/de/providers/vertex/) — Workload-Identity-Setup für GCP.

## Weiterführende Literatur

- `docker/Dockerfile` — das von den Manifesten referenzierte Image.
- `docker/rousseau-agent.container` — das Quadlet-Äquivalent (für eine Non-K8s-Alternative).
- Kubernetes-Dokumentation: [PodSecurityStandards](https://kubernetes.io/docs/concepts/security/pod-security-standards/).
- Kubernetes-Dokumentation: [NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/).
