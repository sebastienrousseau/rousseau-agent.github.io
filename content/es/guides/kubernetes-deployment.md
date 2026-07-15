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
hreflang: "es"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "es"
locale: "es_ES"
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
permalink: "https://docs.rousseau-agent.dev/es/guides/kubernetes-deployment/"
subtitle: "Deployment, PVC, Secret, SecurityContext — restricted profile."
tags: "guides, kubernetes, deployment, pvc"
title: "Guía: despliegue en Kubernetes"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "kubernetes, deployment, pvc, secret, security context, pod security, restricted, self-hosted"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guía: despliegue en Kubernetes"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 33
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/kubernetes-deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/kubernetes-deployment/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guía: despliegue en Kubernetes"
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
twitter_title: "Guía: despliegue en Kubernetes"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Gracias a cada operador que ejecuta su propio agente de codificación."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Escenario

Ejecutas rousseau junto con otros servicios dentro del clúster. Quieres la misma postura de ejecución que la referencia Podman + Quadlet —usuario no-root, sistema de archivos raíz de solo lectura, todas las capabilities eliminadas, seccomp por defecto— expresada como manifiestos de Kubernetes. Sin superficie HTTP entrante, así que sin `Service` ni `Ingress`.

## Namespace + perfil PodSecurity

La postura de rousseau satisface el perfil *restricted* de los [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/). Configúralo como predeterminado del namespace:

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

Las credenciales del proveedor van en un `Secret`, no en el ConfigMap.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: rousseau-secrets
  namespace: rousseau
type: Opaque
stringData:
  ANTHROPIC_API_KEY: "sk-ant-..."
  # Añade SLACK_APP_TOKEN, SLACK_BOT_TOKEN, etc. según sea necesario.
```

Para Bedrock / Vertex, prefiere workload identity (IRSA en EKS, Workload Identity en GKE) sobre claves de larga vida.

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
      # los tokens provienen del Secret vía variables de entorno
      allowlist:
        - U0123456789
```

## PersistentVolumeClaim

El estado de la sesión vive en disco. El claim asegura durabilidad ante reprogramaciones de pods.

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
  # Ajusta storageClassName según corresponda.
```

## Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rousseau-agent
  namespace: rousseau
spec:
  replicas: 1                            # single-writer; almacén de sesiones SQLite
  strategy: { type: Recreate }           # evita que dos pods compartan el PVC
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
          args: ["slack"]                # o "whatsapp", "discord", etc.
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

Los puntos importantes:

| Campo | Justificación |
|---|---|
| `runAsNonRoot: true` + `runAsUser: 1000` | Coincide con la imagen del contenedor; el servicio nunca necesita UID 0. |
| `readOnlyRootFilesystem: true` | El binario no puede modificar su propia imagen. |
| `capabilities.drop: [ALL]` | Ningún transporte necesita capabilities elevadas. |
| `allowPrivilegeEscalation: false` | Bloquea rutas de escalada por setuid. |
| `seccompProfile: RuntimeDefault` | Bloqueo de llamadas al sistema a nivel de kernel. |
| `automountServiceAccountToken: false` | Rousseau no habla con la API de Kubernetes. |
| `replicas: 1` + `Recreate` | SQLite es de escritor único; dos pods sobre el mismo PVC corromperán el almacén. |
| `emptyDir` para `/tmp` y `$HOME` | Espacio de escritura que nunca sale del pod. |

## Sin `Service`, sin `Ingress`

Cada transporte incluido usa o un WebSocket saliente (Slack Socket Mode, Discord Gateway), un subproceso (Signal), o polling (Telegram, Matrix, iMessage, Email). WhatsApp usa la sesión TCP saliente de whatsmeow. **No hay superficie HTTP entrante**, así que no se requieren `Service` ni `Ingress`.

Si habilitas el servidor MCP (`rousseau mcp`), este es solo stdio: adjunta un cliente MCP vía `kubectl exec` o córrelo como side-car en el mismo pod.

## Política de salida

Si ejecutas una `NetworkPolicy` que deniega egreso por defecto, permite a rousseau alcanzar:

- El endpoint del proveedor LLM (`api.anthropic.com` para Anthropic, URLs específicas de región de Bedrock / Vertex, o tu vLLM interno si ese es el destino).
- Los endpoints de cada transporte habilitado (Slack: `wss://wss-primary.slack.com`, Discord: `wss://gateway.discord.gg`, WhatsApp: endpoints TCP de whatsmeow, etc.).
- Los endpoints del transparency log solo si ejecutas `cosign verify-blob` dentro del pod; normalmente verificas en tiempo de build de la imagen, no en runtime.

## Helm (roadmap)

Un chart oficial de Helm está en el roadmap. Borrador de `values.yaml`:

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
  # La API key se obtiene de un secret existente; no plantillar valores en crudo.
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
    - 3.5.0.0/16      # Anthropic (ilustrativo; los CIDRs cambian)
    - 157.240.0.0/16  # Meta

serviceAccount:
  create: true
  annotations: {}    # p. ej. eks.amazonaws.com/role-arn para IRSA

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

Sigue [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md) para conocer la disponibilidad del chart.

## Manifiesto de aplicación ArgoCD

Para despliegues GitOps:

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

## Ejemplo de NetworkPolicy

Restringe el egreso únicamente al proveedor LLM y a los backends de transporte:

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
    # DNS a CoreDNS
    - to:
        - namespaceSelector: { matchLabels: { kubernetes.io/metadata.name: kube-system } }
          podSelector: { matchLabels: { k8s-app: kube-dns } }
      ports:
        - protocol: UDP
          port: 53
    # API de Anthropic
    - to:
        - ipBlock: { cidr: 3.5.0.0/16 }        # CIDR ilustrativo
      ports:
        - protocol: TCP
          port: 443
```

<aside class="admonition" data-type="warning"><span class="admonition-title">Volatilidad de CIDRs</span><p>Los rangos de IP de los proveedores cambian. Prefiere un proxy de egreso basado en DNS o un service mesh (Istio, Linkerd) con política consciente de FQDN si necesitas control de egreso duradero.</p></aside>

## Advertencias

- **SQLite requiere un único escritor.** No escales las réplicas por encima de 1. Si necesitas HA, ejecuta un standby pasivo con un script de failover rápido; no ejecutes dos escritores activos contra el mismo PVC.
- **El almacén de sesiones no está cifrado en reposo.** Monta el PVC sobre una storage class cifrada si tu política lo exige.
- **El material de autenticación del proveedor** debe vivir siempre en un `Secret` o en workload identity, nunca en el ConfigMap.

## Solución de problemas

### `PodSecurity restricted violation` al aplicar

Tu namespace impone el perfil restricted de PodSecurity y al manifiesto le falta `runAsNonRoot`, un perfil seccomp, o tiene `allowPrivilegeEscalation: true`. Los manifiestos anteriores fijan todo esto; contrasta línea por línea.

### PVC atascado en `Pending`

Tu storage class no aprovisiona automáticamente, o el tamaño solicitado excede la cuota. Verifica con `kubectl describe pvc rousseau-state`.

### El pod no puede resolver `api.anthropic.com`

El DNS no está permitido a través de tu `NetworkPolicy`. Añade una regla de egreso a `kube-dns` en UDP/53.

### IRSA / Workload Identity: `NoCredentialProviders`

La anotación de la service account es incorrecta o falta. Verifica con `kubectl get sa rousseau -n agents -o yaml`; la anotación debe ser un ARN (AWS) o `iam.gke.io/gcp-service-account` (GCP).

### El despliegue de una nueva imagen mata el pod antiguo, pero el nuevo nunca queda Ready

La estrategia `Recreate` implica que el pod antiguo se detiene antes de que arranque el nuevo. Si la imagen nueva no puede iniciar (config incorrecta, secret faltante), tienes una interrupción. Corrige primero la configuración y vuelve a aplicar.

## Páginas relacionadas

- [Despliegue](/es/deployment/) — la postura de referencia Podman + Quadlet.
- [Guías: Observabilidad](/es/guides/observability/) — conecta la salida de slog a tu pipeline de logs.
- [Guías: Auditoría y políticas de aprobación](/es/guides/audit-approval-policies/) — la postura de seguridad que presentas a los auditores.
- [Proveedores: Bedrock](/es/providers/bedrock/) — configuración IRSA para AWS.
- [Proveedores: Vertex](/es/providers/vertex/) — configuración Workload Identity para GCP.

## Lecturas adicionales

- `docker/Dockerfile` — la imagen a la que hacen referencia los manifiestos.
- `docker/rousseau-agent.container` — el equivalente Quadlet (para una alternativa no-K8s).
- Documentación de Kubernetes: [PodSecurityStandards](https://kubernetes.io/docs/concepts/security/pod-security-standards/).
- Documentación de Kubernetes: [NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/).
