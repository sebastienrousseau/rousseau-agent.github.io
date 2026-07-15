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
hreflang: "pt-BR"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "pt-BR"
locale: "pt_BR"
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
permalink: "https://docs.rousseau-agent.dev/pt-BR/guides/kubernetes-deployment/"
subtitle: "Deployment, PVC, Secret, SecurityContext — restricted profile."
tags: "guides, kubernetes, deployment, pvc"
title: "Guia: implantação no Kubernetes"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "kubernetes, deployment, pvc, secret, security context, pod security, restricted, self-hosted"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guia: implantação no Kubernetes"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 33
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/kubernetes-deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/kubernetes-deployment/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guia: implantação no Kubernetes"
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
twitter_title: "Guia: implantação no Kubernetes"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Obrigado a cada operador que executa seu próprio agente de codificação."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Cenário

Você executa o rousseau ao lado de outros serviços no cluster. Você quer a mesma postura de runtime da referência Podman + Quadlet — não-root, sistema de arquivos raiz somente leitura, todas as capabilities descartadas, seccomp default — expressa como manifests do Kubernetes. Sem superfície HTTP de entrada, então nenhum `Service` e nenhum `Ingress`.

## Namespace + perfil PodSecurity

A postura do Rousseau satisfaz o perfil *restricted* dos [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/). Defina como padrão do namespace:

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

Credenciais do provider ficam em um `Secret`, não no ConfigMap.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: rousseau-secrets
  namespace: rousseau
type: Opaque
stringData:
  ANTHROPIC_API_KEY: "sk-ant-..."
  # Adicione SLACK_APP_TOKEN, SLACK_BOT_TOKEN, etc. conforme necessário.
```

Para Bedrock / Vertex, prefira workload identity (IRSA no EKS, Workload Identity no GKE) em vez de chaves de longa duração.

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
      # tokens vêm do Secret via env vars
      allowlist:
        - U0123456789
```

## PersistentVolumeClaim

O estado da sessão fica em disco. O claim garante durabilidade através de reescalonamentos do pod.

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
  # Defina seu storageClassName conforme apropriado.
```

## Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rousseau-agent
  namespace: rousseau
spec:
  replicas: 1                            # gravador único; session store SQLite
  strategy: { type: Recreate }           # evita dois pods compartilhando o PVC
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
          args: ["slack"]                # ou "whatsapp", "discord", etc.
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

Os pontos importantes:

| Campo | Justificativa |
|---|---|
| `runAsNonRoot: true` + `runAsUser: 1000` | Corresponde à imagem do contêiner; o daemon nunca precisa de UID 0. |
| `readOnlyRootFilesystem: true` | O binário não pode alterar sua própria imagem. |
| `capabilities.drop: [ALL]` | Nenhum transporte precisa de capabilities elevadas. |
| `allowPrivilegeEscalation: false` | Bloqueia caminhos de escalada por setuid. |
| `seccompProfile: RuntimeDefault` | Gating de syscalls no kernel. |
| `automountServiceAccountToken: false` | O Rousseau não fala com a API do Kubernetes. |
| `replicas: 1` + `Recreate` | SQLite é single-writer; dois pods no mesmo PVC corrompem o store. |
| `emptyDir` para `/tmp` e `$HOME` | Scratch gravável que nunca sai do pod. |

## Sem `Service`, sem `Ingress`

Todo transporte incluído usa ou um WebSocket de saída (Slack Socket Mode, Discord Gateway), um subprocesso (Signal), ou polling (Telegram, Matrix, iMessage, Email). O WhatsApp usa a sessão TCP de saída do whatsmeow. **Não há superfície HTTP de entrada**, então nenhum `Service` e nenhum `Ingress` são necessários.

Se você habilitar o servidor MCP (`rousseau mcp`), ele é stdio-only — anexe um cliente MCP via `kubectl exec` ou coloque-o como side-car no mesmo pod.

## Política de egress

Se você executa um `NetworkPolicy` negando egress por padrão, permita o rousseau alcançar:

- O endpoint do provider de LLM (`api.anthropic.com` para Anthropic, URLs regionais de Bedrock / Vertex, ou seu vLLM interno se esse for o alvo).
- Os endpoints de cada transporte habilitado (Slack: `wss://wss-primary.slack.com`, Discord: `wss://gateway.discord.gg`, WhatsApp: endpoints TCP do whatsmeow, etc.).
- Os endpoints de transparency log apenas se você rodar `cosign verify-blob` dentro do pod — normalmente você verifica no build-time da imagem, não em runtime.

## Helm (roadmap)

Um Helm chart oficial está no roadmap. Rascunho de `values.yaml`:

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
  # A API key vem de um secret existente; não faça template de valores brutos.
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
    - 3.5.0.0/16      # Anthropic (ilustrativo — CIDRs mudam)
    - 157.240.0.0/16  # Meta

serviceAccount:
  create: true
  annotations: {}    # ex.: eks.amazonaws.com/role-arn para IRSA

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

Acompanhe [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md) para saber sobre a disponibilidade do chart.

## Manifest de aplicação ArgoCD

Para implantações GitOps:

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

## Exemplo de NetworkPolicy

Restringe egress apenas ao provider de LLM e aos backends de transporte:

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
    # DNS para CoreDNS
    - to:
        - namespaceSelector: { matchLabels: { kubernetes.io/metadata.name: kube-system } }
          podSelector: { matchLabels: { k8s-app: kube-dns } }
      ports:
        - protocol: UDP
          port: 53
    # API Anthropic
    - to:
        - ipBlock: { cidr: 3.5.0.0/16 }        # CIDR ilustrativo
      ports:
        - protocol: TCP
          port: 443
```

<aside class="admonition" data-type="warning"><span class="admonition-title">Rotatividade de CIDR</span><p>As faixas de IP dos providers mudam. Prefira um proxy de egress baseado em DNS ou um service mesh (Istio, Linkerd) com política ciente de FQDN se você precisa de controle de egress durável.</p></aside>

## Ressalvas

- **SQLite exige um único gravador.** Não escale replicas acima de 1. Se você precisa de HA, execute um standby passivo com um script rápido de failover — não rode dois gravadores ativos contra o mesmo PVC.
- **O session store não é criptografado em repouso.** Monte o PVC em uma storage class criptografada se a política exigir.
- **Material de autenticação do provider** deve sempre residir em `Secret` ou workload identity, nunca no ConfigMap.

## Solução de problemas

### `PodSecurity restricted violation` no apply

Seu namespace impõe o perfil PodSecurity restricted e o manifest não tem `runAsNonRoot`, um perfil seccomp, ou tem `allowPrivilegeEscalation: true`. Os manifests acima definem todos esses — verifique linha por linha.

### PVC preso em `Pending`

Sua storage class não provisiona automaticamente, ou o tamanho requisitado excede a quota. Verifique com `kubectl describe pvc rousseau-state`.

### O pod não consegue resolver `api.anthropic.com`

DNS não permitido pela sua `NetworkPolicy`. Adicione uma regra de egress para `kube-dns` em UDP/53.

### IRSA / Workload Identity: `NoCredentialProviders`

A anotação do service account está errada ou ausente. Verifique com `kubectl get sa rousseau -n agents -o yaml` — a anotação precisa ser um ARN (AWS) ou um `iam.gke.io/gcp-service-account` (GCP).

### Rolar uma nova imagem mata o pod antigo, mas o novo nunca fica Ready

A estratégia `Recreate` significa que o pod antigo para antes do novo iniciar. Se a nova imagem não conseguir iniciar (config ruim, secret ausente), você tem uma indisponibilidade. Corrija a config primeiro, depois re-aplique.

## Páginas relacionadas

- [Implantação](/pt-BR/deployment/) — a postura de referência Podman + Quadlet.
- [Guias: Observabilidade](/pt-BR/guides/observability/) — direcione a saída slog ao seu pipeline de log.
- [Guias: Auditoria &amp; Políticas de aprovação](/pt-BR/guides/audit-approval-policies/) — a postura de segurança que você apresenta aos auditores.
- [Providers: Bedrock](/pt-BR/providers/bedrock/) — configuração de IRSA para AWS.
- [Providers: Vertex](/pt-BR/providers/vertex/) — configuração de Workload Identity para GCP.

## Leitura adicional

- `docker/Dockerfile` — a imagem à qual os manifests referenciam.
- `docker/rousseau-agent.container` — o equivalente Quadlet (para uma alternativa fora do K8s).
- Docs do Kubernetes: [PodSecurityStandards](https://kubernetes.io/docs/concepts/security/pod-security-standards/).
- Docs do Kubernetes: [NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/).
