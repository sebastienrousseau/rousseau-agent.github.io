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
hreflang: "fr"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "fr"
locale: "fr_FR"
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
permalink: "https://docs.rousseau-agent.dev/fr/guides/kubernetes-deployment/"
subtitle: "Deployment, PVC, Secret, SecurityContext — restricted profile."
tags: "guides, kubernetes, deployment, pvc"
title: "Guide : déploiement Kubernetes"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "kubernetes, deployment, pvc, secret, security context, pod security, restricted, self-hosted"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide : déploiement Kubernetes"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 33
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/kubernetes-deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/kubernetes-deployment/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guide : déploiement Kubernetes"
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
twitter_title: "Guide : déploiement Kubernetes"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Merci à chaque opérateur qui exploite son propre agent de codage."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Scénario

Vous exécutez rousseau aux côtés d'autres services dans le cluster. Vous souhaitez la même posture d'exécution que celle de la référence Podman + Quadlet — non-root, système de fichiers racine en lecture seule, toutes capabilities retirées, seccomp par défaut — exprimée sous forme de manifests Kubernetes. Aucune surface HTTP entrante, donc pas de `Service` ni d'`Ingress`.

## Namespace + profil PodSecurity

La posture de rousseau satisfait le profil *restricted* des [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/). Positionnez-le comme défaut du namespace :

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

Les identifiants de fournisseur ont leur place dans un `Secret`, pas dans le ConfigMap.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: rousseau-secrets
  namespace: rousseau
type: Opaque
stringData:
  ANTHROPIC_API_KEY: "sk-ant-..."
  # Ajoutez SLACK_APP_TOKEN, SLACK_BOT_TOKEN, etc. au besoin.
```

Pour Bedrock / Vertex, préférez la workload identity (IRSA sur EKS, Workload Identity sur GKE) aux clés à longue durée de vie.

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
      # les jetons proviennent du Secret via des variables d'environnement
      allowlist:
        - U0123456789
```

## PersistentVolumeClaim

L'état de session vit sur disque. Le claim garantit la durabilité au fil des replanifications de pod.

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
  # Positionnez votre storageClassName selon vos besoins.
```

## Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rousseau-agent
  namespace: rousseau
spec:
  replicas: 1                            # single-writer ; store de sessions SQLite
  strategy: { type: Recreate }           # évite que deux pods partagent le PVC
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

Les points importants :

| Champ | Justification |
|---|---|
| `runAsNonRoot: true` + `runAsUser: 1000` | Correspond à l'image de conteneur ; le daemon n'a jamais besoin d'UID 0. |
| `readOnlyRootFilesystem: true` | Le binaire ne peut pas muter sa propre image. |
| `capabilities.drop: [ALL]` | Aucun transport ne requiert de capabilities élevées. |
| `allowPrivilegeEscalation: false` | Bloque les chemins d'escalade via setuid. |
| `seccompProfile: RuntimeDefault` | Filtrage des appels système au niveau noyau. |
| `automountServiceAccountToken: false` | Rousseau ne dialogue pas avec l'API Kubernetes. |
| `replicas: 1` + `Recreate` | SQLite est single-writer ; deux pods sur le même PVC corrompent le store. |
| `emptyDir` pour `/tmp` et `$HOME` | Espace scratch inscriptible qui ne quitte jamais le pod. |

## Ni `Service`, ni `Ingress`

Chaque transport livré utilise soit un WebSocket sortant (Slack Socket Mode, Discord Gateway), soit un sous-processus (Signal), soit du polling (Telegram, Matrix, iMessage, Email). WhatsApp utilise la session TCP sortante de whatsmeow. **Aucune surface HTTP entrante**, donc ni `Service` ni `Ingress` ne sont requis.

Si vous activez le serveur MCP (`rousseau mcp`), il est stdio uniquement — attachez un client MCP via `kubectl exec` ou placez-le en side-car dans le même pod.

## Politique d'egress

Si vous exécutez une `NetworkPolicy` qui refuse l'egress par défaut, autorisez rousseau à joindre :

- L'endpoint du fournisseur LLM (`api.anthropic.com` pour Anthropic, les URLs régionales Bedrock / Vertex, ou votre vLLM interne si c'est la cible).
- Les endpoints de chaque transport activé (Slack : `wss://wss-primary.slack.com`, Discord : `wss://gateway.discord.gg`, WhatsApp : endpoints TCP de whatsmeow, etc.).
- Les endpoints du transparency log uniquement si vous exécutez `cosign verify-blob` à l'intérieur du pod — normalement, la vérification s'effectue au build de l'image, pas au runtime.

## Helm (feuille de route)

Un chart Helm officiel figure sur la feuille de route. `values.yaml` en projet :

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
  # Clé d'API issue d'un Secret existant ; ne pas mettre en dur.
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
    - 3.5.0.0/16      # Anthropic (indicatif — les CIDR évoluent)
    - 157.240.0.0/16  # Meta

serviceAccount:
  create: true
  annotations: {}    # par ex. eks.amazonaws.com/role-arn pour IRSA

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

Suivez [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md) pour la disponibilité du chart.

## Manifest ArgoCD

Pour les déploiements GitOps :

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

## Exemple de NetworkPolicy

Restreignez l'egress au seul fournisseur LLM et aux backends de transport :

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
    # DNS vers CoreDNS
    - to:
        - namespaceSelector: { matchLabels: { kubernetes.io/metadata.name: kube-system } }
          podSelector: { matchLabels: { k8s-app: kube-dns } }
      ports:
        - protocol: UDP
          port: 53
    # API Anthropic
    - to:
        - ipBlock: { cidr: 3.5.0.0/16 }        # CIDR indicatif
      ports:
        - protocol: TCP
          port: 443
```

<aside class="admonition" data-type="warning"><span class="admonition-title">Volatilité des CIDR</span><p>Les plages IP des fournisseurs évoluent. Préférez un proxy d'egress basé DNS ou un service mesh (Istio, Linkerd) avec une politique FQDN-aware si vous avez besoin d'un contrôle d'egress durable.</p></aside>

## Réserves

- **SQLite exige un seul writer.** Ne montez pas le nombre de replicas au-delà de 1. Si vous avez besoin de HA, exécutez un standby passif avec un script de failover rapide — n'exécutez pas deux writers actifs sur le même PVC.
- **Le store de sessions n'est pas chiffré au repos.** Montez le PVC sur une classe de stockage chiffrée si la politique l'exige.
- **Les identifiants d'authentification du fournisseur** doivent toujours vivre dans un `Secret` ou une workload identity, jamais dans le ConfigMap.

## Dépannage

### `PodSecurity restricted violation` à l'application

Votre namespace applique le profil PodSecurity restricted et le manifest n'a pas `runAsNonRoot`, pas de profil seccomp, ou porte `allowPrivilegeEscalation: true`. Les manifests ci-dessus définissent tous ces éléments — comparez ligne par ligne.

### PVC bloqué en `Pending`

Votre classe de stockage ne provisionne pas automatiquement, ou la taille demandée dépasse le quota. Vérifiez avec `kubectl describe pvc rousseau-state`.

### Le pod ne peut pas résoudre `api.anthropic.com`

DNS non autorisé par votre `NetworkPolicy`. Ajoutez une règle d'egress vers `kube-dns` sur UDP/53.

### IRSA / Workload Identity : `NoCredentialProviders`

L'annotation du service account est incorrecte ou absente. Vérifiez avec `kubectl get sa rousseau -n agents -o yaml` — l'annotation doit être un ARN (AWS) ou un `iam.gke.io/gcp-service-account` (GCP).

### Le déploiement d'une nouvelle image tue l'ancien pod, mais le nouveau ne devient jamais Ready

La stratégie `Recreate` implique que l'ancien pod s'arrête avant le démarrage du nouveau. Si la nouvelle image ne démarre pas (mauvaise config, Secret manquant), vous êtes en panne. Corrigez d'abord la config, puis réappliquez.

## Pages liées

- [Déploiement](/fr/deployment/) — la posture de référence Podman + Quadlet.
- [Guides : Observabilité](/fr/guides/observability/) — brancher la sortie slog sur votre pipeline de logs.
- [Guides : Audit &amp; politiques d'approbation](/fr/guides/audit-approval-policies/) — la posture de sécurité à présenter aux auditeurs.
- [Fournisseurs : Bedrock](/fr/providers/bedrock/) — mise en place IRSA pour AWS.
- [Fournisseurs : Vertex](/fr/providers/vertex/) — mise en place Workload Identity pour GCP.

## Lectures complémentaires

- `docker/Dockerfile` — l'image référencée par les manifests.
- `docker/rousseau-agent.container` — l'équivalent Quadlet (pour une alternative non-K8s).
- Documentation Kubernetes : [PodSecurityStandards](https://kubernetes.io/docs/concepts/security/pod-security-standards/).
- Documentation Kubernetes : [NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/).
