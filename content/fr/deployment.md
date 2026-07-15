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
description: "Reference production deployment for rousseau-agent: rootless Podman + systemd Quadlet with dropped capabilities, read-only rootfs, seccomp, pasta networking. Kubernetes / OpenShift note."
keywords: "deployment, Podman, Quadlet, systemd, rootless, ReadOnly, DropCapability, NoNewPrivileges, seccomp, pasta, Kubernetes, OpenShift"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/deployment/"
subtitle: "Podman rootless avec un Quadlet systemd, plus une note Kubernetes."
tags: "deployment, operations, container, systemd"
title: "Déploiement"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "deployment, Podman, Quadlet, systemd, rootless, ReadOnly, DropCapability, NoNewPrivileges, seccomp, pasta, Kubernetes, OpenShift"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Déploiement"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "operations"
order: 25
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/deployment/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Déploiement"
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
twitter_title: "Déploiement"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Ce que vous allez apprendre</span><p>Les trois topologies de déploiement supportées par rousseau — Podman rootless + Quadlet (référence), Docker classique et Kubernetes — ainsi que la gestion des secrets via Vault, AWS Secrets Manager et GCP Secret Manager. Source faisant foi pour le Quadlet de référence : <code>docker/rousseau-agent.container</code>.</p></aside>

## Posture de référence

Le déploiement de référence est un conteneur Podman rootless piloté par une unité Quadlet systemd — mono-nœud, sans dépendance à Kubernetes, résilient aux redémarrages, sans privilèges root.

Source faisant foi : `docker/rousseau-agent.container` dans le dépôt rousseau-agent.

## Choisir une topologie

<div class="tabs" data-tabs="deployment-topology">
  <div class="tab-list" role="tablist" aria-label="Deployment topology">
    <button role="tab" aria-selected="true">Podman + Quadlet</button>
    <button role="tab" aria-selected="false">Docker Compose</button>
    <button role="tab" aria-selected="false">Kubernetes</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Le déploiement de référence. Rootless, durci, résilient aux redémarrages, sans orchestrateur.

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
mkdir -p ~/.config/containers/systemd
cp docker/rousseau-agent.container ~/.config/containers/systemd/
systemctl --user daemon-reload
systemctl --user enable --now rousseau-agent.service
```

Voir plus bas dans cette page l'unité Quadlet complète et sa justification.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Docker Compose est une forme familière mais n'applique pas la posture de sécurité qu'impose Quadlet — vous devez régler chaque paramètre de durcissement à la main :

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

<aside class="admonition" data-type="warning"><span class="admonition-title">Docker en root</span><p>Le daemon Docker classique tourne en root. Même avec <code>user: "1000:1000"</code>, le daemon dispose des capacités du propriétaire du socket Docker. Préférez Docker rootless ou Podman.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Kubernetes requiert un Deployment + PVC. Voir le manifeste ci-dessous, ainsi que [Guides : Déploiement Kubernetes](/fr/guides/kubernetes-deployment/) pour un exemple complet de chart Helm.

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

## Gestion des secrets

Ne versionnez jamais de clés API ou de jetons dans `config.yaml`. Chargez-les à l'exécution depuis un backend de secrets :

<div class="tabs" data-tabs="deployment-secrets">
  <div class="tab-list" role="tablist" aria-label="Secrets backend">
    <button role="tab" aria-selected="true">HashiCorp Vault</button>
    <button role="tab" aria-selected="false">AWS Secrets Manager</button>
    <button role="tab" aria-selected="false">GCP Secret Manager</button>
    <button role="tab" aria-selected="false">systemd credentials</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Utilisez `vault agent` pour matérialiser les variables d'environnement dans un fichier lu par rousseau. Exemple de template :

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

Utilisez `aws secretsmanager` pour récupérer la clé dans un fichier d'environnement au démarrage :

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

Associez-le à IRSA sur EKS pour que le SDK résolve les credentials de façon transparente — aucune clé AWS statique sur l'hôte.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Utilisez `gcloud secrets versions access` :

```sh
gcloud secrets versions access latest --secret=rousseau-anthropic > /run/rousseau/api_key
```

Ou, sous Kubernetes, utilisez le [driver CSI Secret Manager](https://cloud.google.com/secret-manager/docs/secret-manager-managed-csi-component) pour monter les secrets sous forme de fichiers.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Les systemd credentials (disponibles à partir de systemd 250) chargent les secrets en mémoire au démarrage de l'unité :

```ini
[Service]
LoadCredential=anthropic_key:/etc/rousseau/anthropic.key
ExecStart=/usr/local/bin/rousseau chat
```

Le daemon lit `$CREDENTIALS_DIRECTORY/anthropic_key` au démarrage. Aucune écriture disque au-delà du magasin de credentials (chiffré).

  </div>
</div>

## Construire l'image

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
```

Build multi-étape. Étape 1 : `golang:1.26-alpine` compile le binaire statique (`CGO_ENABLED=0`). Étape 2 : `node:22-alpine` fournit le sous-processus CLI `claude`. L'image de runtime pèse ~550 Mo ; la couche Node n'existe que pour héberger le fournisseur optionnel `claudecli`.

Si vous utilisez un autre fournisseur (Anthropic direct, Bedrock, Vertex, compatible OpenAI), vous pouvez retirer le runtime Node et alléger l'image.

## Installer l'unité Quadlet

```sh
mkdir -p ~/.config/containers/systemd
cp docker/rousseau-agent.container ~/.config/containers/systemd/
systemctl --user daemon-reload
systemctl --user start rousseau-agent.service
journalctl --user -u rousseau-agent.service -f
```

Activez au démarrage avec `systemctl --user enable rousseau-agent.service` après avoir confirmé que le lingering est activé (`loginctl enable-linger $USER`).

## Posture d'exécution — chaque réglage Quadlet

| Réglage | Valeur | Justification |
|---|---|---|
| `Network=pasta` | Pile réseau rootless | `slirp4netns` a été retiré des Podman récents ; pasta est plus rapide sur les noyaux modernes et bloque l'entrant depuis l'hôte par défaut. |
| `UserNS=keep-id` | UID 1000 conteneur → UID 1000 hôte | Les fichiers en bind-mount conservent leur propriétaire hôte ; le processus conteneur peut écrire dans des fichiers appartenant à l'hôte. |
| `ReadOnly=true` | Système de fichiers racine en lecture seule | Le daemon ne doit jamais modifier l'image à l'exécution. Tout ce qui est modifiable réside sur un bind mount ou dans le tmpfs. |
| `Tmpfs=/tmp:rw,size=64m,mode=1777` | Espace scratch modifiable | Pour tout besoin de fichier temporaire à l'exécution (rare). |
| `DropCapability=all` | Toutes les capabilities retirées | Le binaire Go n'a besoin d'aucune capacité élevée — le TCP sortant ne requiert pas `CAP_NET_BIND_SERVICE` ou similaire. |
| `NoNewPrivileges=true` | Bit `no_new_privs` positionné | Bloque l'élévation setuid dans le conteneur. |
| `SeccompProfile=/usr/share/containers/seccomp.json` | Filtre seccomp par défaut | Filtrage des appels système au niveau noyau, en plus des capabilities retirées. |
| `Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z` | Bind mount d'état | Sessions, appairage WhatsApp, cron jobs, table des JID, index FTS5. `:Z` positionne le label SELinux. |
| `Volume=%h/.claude:/home/rousseau/.claude:rw,Z` | Authentification CLI `claude` | Pertinent uniquement lorsque le fournisseur `claudecli` est actif. `claude` rafraîchit l'OAuth mis en cache sur place. |
| `Volume=%h/team-rousseau-workspace:/workspace:rw,Z` | Workspace | Seul le workspace est visible depuis l'intérieur du conteneur. Rien d'autre sur l'hôte n'est monté. |
| `Environment=HOME=/home/rousseau` | Positionne `$HOME` | Utilisé par Viper, la CLI `claude` et le résolveur de répertoire d'état. |
| `AutoUpdate=disabled` | Podman ne met pas à jour automatiquement | Les mises à jour sont déclenchées par l'opérateur selon la cadence des releases, jamais en silence. |

## Ligne `Exec=`

Le Quadlet livre :

```
Exec=whatsapp --allow 447906009073@s.whatsapp.net
```

Remplacez par le transport de votre choix et votre allowlist. Plusieurs transports tournent typiquement dans des unités Quadlet distinctes — une image, un binaire, plusieurs unités — pour qu'une panne sur un transport n'affecte pas les autres.

## Kubernetes / OpenShift

`rousseau` est un daemon mono-binaire ; un `Deployment` + `PersistentVolumeClaim` minimal pour le répertoire d'état suffisent :

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

Puisqu'il n'y a aucune surface HTTP entrante, **aucun `Service` ni `Ingress` n'est requis** pour les transports en WebSocket sortant (Slack, Discord, WhatsApp, Matrix). Seul un transport de type webhook nécessiterait un `Service`, et rousseau n'en fournit aucun par défaut.

La stratégie `Recreate` est délibérée — le fichier d'état SQLite n'est pas conçu pour deux écrivains concurrents. Pour de la HA, faites tourner un daemon par transport et appuyez-vous sur l'état du transport lui-même (Slack Socket Mode, Discord Gateway) pour la sémantique de reconnexion.

## Destination des logs systemd

Le Quadlet hérite de la configuration du journal systemd. `journalctl --user -u rousseau-agent.service` lit les logs. Pour l'agrégation, utilisez un sidecar journal-to-Loki / journal-to-Fluent-Bit ; n'écrivez pas directement le format de log rousseau sur disque (rousseau n'effectue pas de rotation).

Configurez rousseau pour émettre du JSON afin que les agrégateurs puissent le parser :

```yaml
log:
  level: info
  format: json
```

## Verrouillage nftables du trafic sortant (optionnel)

`docker/nftables.rules.example` fournit dans l'arbre source un template de durcissement du trafic sortant au niveau noyau — rejeter tout sauf les plages WhatsApp Web de Meta, Anthropic (derrière CloudFront, donc filtre par domaine) et Signal. Superposez-le au namespace du conteneur pour obtenir la posture la plus stricte. Voir [security](/fr/security/) pour le raisonnement.

## Chart Helm (roadmap)

Un chart Helm first-party figure sur la roadmap. En attendant, les manifestes ci-dessus suffisent pour un déploiement minimal. Suivez l'avancement dans [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md).

Ébauche de `values.yaml` (à titre indicatif, pour relecture par les futurs utilisateurs) :

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

## Dépannage

### `podman play kube` échoue avec `permission denied` sur un bind mount

Label SELinux manquant. Chaque volume doit se terminer par `:Z` (ou `:z` pour partagé). Voir [Dépannage : Échec du bind mount de conteneur](/fr/troubleshooting/#container-fails-to-bind-mount).

### Pod Kubernetes en CrashLoopBackOff au premier démarrage

Le volume d'état n'a pas été pré-créé, ou son propriétaire ne correspond pas à l'UID 1000. Ajoutez un initContainer pour `chown` le volume :

```yaml
initContainers:
  - name: chown-state
    image: busybox
    command: ["sh", "-c", "chown -R 1000:1000 /state"]
    volumeMounts: [{ name: state, mountPath: /state }]
    securityContext: { runAsUser: 0 }
```

### `systemctl --user` ne trouve pas l'unité Quadlet

`daemon-reload` n'a pas été exécuté, ou le fichier d'unité contient une faute de frappe. Confirmez avec `systemctl --user cat rousseau-agent.service` — Quadlet génère l'unité à la volée, donc cat est l'outil de débogage le plus rapide.

### Après un redémarrage, le daemon ne démarre pas

Activez le lingering : `loginctl enable-linger $USER`. Sans lingering, le gestionnaire user de systemd s'arrête à la déconnexion et ne redémarre qu'à la reconnexion suivante.

### Deux daemons se sont marchés dessus et la base d'état est corrompue

Ne faites jamais tourner deux daemons sur le même `state.path`. En cas de corruption, sauvegardez le fichier, `rm sessions.db{,-wal,-shm}`, puis redémarrez. L'historique de session est perdu ; l'appairage survit si `whatsapp.db` est séparé (ce qui est le cas par défaut).

## Pages liées

- [Guides : Déploiement Kubernetes](/fr/guides/kubernetes-deployment/) — chart Helm complet et exemple de NetworkPolicy.
- [Guides : Déploiement en production](/fr/guides/production-deployment/) — la checklist de production.
- [Guides : Observabilité](/fr/guides/observability/) — logs et métriques.
- [Sécurité](/fr/security/) — frontières de confiance, seccomp, egress.
- [Configuration](/fr/configuration/) — chaque paramètre.

## Pour aller plus loin

- `docker/Dockerfile` — le build multi-étape.
- `docker/rousseau-agent.container` — l'unité Quadlet.
- `docker/example-nftables.rules` — exemple de jeu de règles egress.
- `Makefile` — automatisation du build.
- Docs systemd : [Quadlet](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html).
