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
description: "Reference production deployment for rousseau-agent: rootless Podman + systemd Quadlet with dropped capabilities, read-only rootfs, seccomp, pasta networking. Kubernetes / OpenShift note."
keywords: "deployment, Podman, Quadlet, systemd, rootless, ReadOnly, DropCapability, NoNewPrivileges, seccomp, pasta, Kubernetes, OpenShift"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/deployment/"
subtitle: "Rootless-Podman mit systemd-Quadlet plus Kubernetes-Hinweis."
tags: "deployment, operations, container, systemd"
title: "Bereitstellung"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "deployment, Podman, Quadlet, systemd, rootless, ReadOnly, DropCapability, NoNewPrivileges, seccomp, pasta, Kubernetes, OpenShift"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Bereitstellung"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "operations"
order: 25
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/deployment/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Bereitstellung"
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
twitter_title: "Bereitstellung"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Was Sie lernen</span><p>Die drei Bereitstellungs-Topologien, die rousseau unterstützt – rootless Podman + Quadlet (Referenz), einfaches Docker und Kubernetes – plus Secrets-Verwaltung über Vault, AWS Secrets Manager und GCP Secret Manager. Source of Truth für das Referenz-Quadlet: <code>docker/rousseau-agent.container</code>.</p></aside>

## Referenz-Posture

Die Referenz-Bereitstellung ist ein rootless Podman-Container, verwaltet durch eine systemd-Quadlet-Unit – Ein-Knoten-Setup, keine Kubernetes-Abhängigkeit, übersteht Neustarts, keine Root-Rechte erforderlich.

Source of Truth: `docker/rousseau-agent.container` im rousseau-agent-Repository.

## Topologie wählen

<div class="tabs" data-tabs="deployment-topology">
  <div class="tab-list" role="tablist" aria-label="Deployment topology">
    <button role="tab" aria-selected="true">Podman + Quadlet</button>
    <button role="tab" aria-selected="false">Docker Compose</button>
    <button role="tab" aria-selected="false">Kubernetes</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Die Referenz-Bereitstellung. Rootless, gehärtet, übersteht Neustarts, kein Orchestrator erforderlich.

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
mkdir -p ~/.config/containers/systemd
cp docker/rousseau-agent.container ~/.config/containers/systemd/
systemctl --user daemon-reload
systemctl --user enable --now rousseau-agent.service
```

Die vollständige Quadlet-Unit und deren Begründung finden Sie weiter unten auf dieser Seite.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Docker Compose ist eine vertraute Form, erzwingt aber nicht die Sicherheits-Posture, die Quadlet bietet – Sie müssen jedes Härtungs-Flag manuell setzen:

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

<aside class="admonition" data-type="warning"><span class="admonition-title">Root Docker</span><p>Der klassische Docker-Daemon läuft als Root. Selbst mit <code>user: "1000:1000"</code> besitzt der Daemon die Capabilities des Docker-Socket-Eigentümers. Bevorzugen Sie rootless Docker oder Podman.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Kubernetes benötigt ein Deployment und einen PVC. Siehe das Manifest unten sowie [Guides: Kubernetes-Bereitstellung](/de/guides/kubernetes-deployment/) für ein vollständiges Helm-Chart-Beispiel.

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

## Secrets-Verwaltung

Checken Sie niemals API-Keys oder Token in `config.yaml` ein. Laden Sie sie zur Laufzeit aus einem Secret-Backend:

<div class="tabs" data-tabs="deployment-secrets">
  <div class="tab-list" role="tablist" aria-label="Secrets backend">
    <button role="tab" aria-selected="true">HashiCorp Vault</button>
    <button role="tab" aria-selected="false">AWS Secrets Manager</button>
    <button role="tab" aria-selected="false">GCP Secret Manager</button>
    <button role="tab" aria-selected="false">systemd credentials</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Nutzen Sie `vault agent`, um Env-Variablen in eine von rousseau gelesene Datei zu rendern. Beispiel-Template:

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

Nutzen Sie `aws secretsmanager`, um den Key beim Start in eine Env-Datei zu holen:

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

Kombinieren Sie dies mit IRSA auf EKS, damit das SDK Credentials transparent auflöst – keine statischen AWS-Keys auf dem Host erforderlich.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Nutzen Sie `gcloud secrets versions access`:

```sh
gcloud secrets versions access latest --secret=rousseau-anthropic > /run/rousseau/api_key
```

Oder nutzen Sie in Kubernetes den [Secret Manager CSI driver](https://cloud.google.com/secret-manager/docs/secret-manager-managed-csi-component), um Secrets als Dateien zu mounten.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Systemd-Credentials (verfügbar ab systemd 250+) laden Secrets beim Unit-Start in den Arbeitsspeicher:

```ini
[Service]
LoadCredential=anthropic_key:/etc/rousseau/anthropic.key
ExecStart=/usr/local/bin/rousseau chat
```

Der Daemon liest `$CREDENTIALS_DIRECTORY/anthropic_key` beim Start. Keine Schreibvorgänge auf die Festplatte über den (verschlüsselten) Credential-Store hinaus.

  </div>
</div>

## Image bauen

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
```

Multi-Stage-Build. Stage 1: `golang:1.26-alpine` kompiliert das statische Binary (`CGO_ENABLED=0`). Stage 2: `node:22-alpine` liefert den `claude`-CLI-Subprozess. Das Runtime-Image ist ~550 MB gross; der Node-Layer existiert nur, damit der optionale `claudecli`-Provider ein Zuhause hat.

Wenn Sie einen anderen Provider verwenden (Anthropic direkt, Bedrock, Vertex, OpenAI-kompatibel), können Sie die Node-Runtime entfernen und das Image verkleinern.

## Quadlet-Unit installieren

```sh
mkdir -p ~/.config/containers/systemd
cp docker/rousseau-agent.container ~/.config/containers/systemd/
systemctl --user daemon-reload
systemctl --user start rousseau-agent.service
journalctl --user -u rousseau-agent.service -f
```

Aktivieren Sie den Autostart beim Booten mit `systemctl --user enable rousseau-agent.service`, nachdem Sie bestätigt haben, dass Lingering aktiv ist (`loginctl enable-linger $USER`).

## Runtime-Posture – jede Quadlet-Einstellung

| Einstellung | Wert | Begründung |
|---|---|---|
| `Network=pasta` | Rootless-Netzwerkstack | `slirp4netns` wurde aus aktuellen Podman-Versionen entfernt; pasta ist auf modernen Kernels schneller und blockiert eingehende Verbindungen vom Host standardmässig. |
| `UserNS=keep-id` | Container-UID 1000 → Host-UID 1000 | Bind-gemountete Dateien behalten den Host-Besitzer; der Container-Prozess kann in Host-eigene Dateien schreiben. |
| `ReadOnly=true` | Root-Dateisystem schreibgeschützt | Der Daemon sollte das Image zur Laufzeit niemals verändern. Alles Schreibbare liegt auf einem Bind-Mount oder dem tmpfs. |
| `Tmpfs=/tmp:rw,size=64m,mode=1777` | Beschreibbares Scratch | Für alles, was zur Laufzeit eine temporäre Datei benötigt (selten). |
| `DropCapability=all` | Jede Capability entfernt | Das Go-Binary benötigt keine erhöhten Capabilities – ausgehendes TCP erfordert kein `CAP_NET_BIND_SERVICE` o.ä. |
| `NoNewPrivileges=true` | `no_new_privs`-Bit gesetzt | Blockiert setuid-Eskalation innerhalb des Containers. |
| `SeccompProfile=/usr/share/containers/seccomp.json` | Standard-seccomp-Filter | Kernel-Level-Syscall-Gating zusätzlich zu entfernten Capabilities. |
| `Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z` | State-Bind-Mount | Sitzungen, WhatsApp-Pairing, Cron-Jobs, JID-Map, FTS5-Index. `:Z` setzt das SELinux-Label. |
| `Volume=%h/.claude:/home/rousseau/.claude:rw,Z` | `claude`-CLI-Auth | Nur relevant, wenn der `claudecli`-Provider aktiv ist. `claude` frischt gecachtes OAuth an Ort und Stelle auf. |
| `Volume=%h/team-rousseau-workspace:/workspace:rw,Z` | Workspace | Nur der Workspace ist aus dem Container heraus sichtbar. Nichts anderes vom Host wird gemountet. |
| `Environment=HOME=/home/rousseau` | Setzt `$HOME` | Wird von Viper, der `claude`-CLI und dem State-Verzeichnis-Resolver konsumiert. |
| `AutoUpdate=disabled` | Podman führt keine Auto-Updates durch | Updates werden vom Betreiber im Release-Rhythmus ausgerollt, nicht stillschweigend. |

## `Exec=`-Zeile

Das Quadlet enthält:

```
Exec=whatsapp --allow 447906009073@s.whatsapp.net
```

Ersetzen Sie dies durch Ihren gewünschten Transport und Ihre Allowlist. Mehrere Transports laufen typischerweise in separaten Quadlet-Units – ein Image, ein Binary, mehrere Units – damit ein Fehler in einem Transport die anderen nicht mitreisst.

## Kubernetes / OpenShift

`rousseau` ist ein Single-Binary-Daemon; ein minimales `Deployment` plus `PersistentVolumeClaim` für das State-Verzeichnis genügt:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rousseau-agent
spec:
  replicas: 1
  strategy:
    type: Recreate           # keine zwei Daemons gegen eine State-DB laufen lassen
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

Da es keine eingehende HTTP-Oberfläche gibt, **ist kein `Service` oder `Ingress` erforderlich** für ausgehende WebSocket-Transports (Slack, Discord, WhatsApp, Matrix). Nur ein Webhook-artiger Transport würde einen `Service` benötigen, und rousseau liefert standardmässig keinen mit.

Die `Recreate`-Strategie ist bewusst gewählt – die SQLite-State-Datei ist nicht für zwei gleichzeitige Schreiber ausgelegt. Wenn Sie HA benötigen, führen Sie einen Daemon pro Transport aus und verlassen Sie sich auf den transporteigenen State (Slack Socket Mode, Discord Gateway) für Reconnect-Semantik.

## systemd-Log-Ziel

Das Quadlet erbt die Journal-Konfiguration von systemd. `journalctl --user -u rousseau-agent.service` liest die Logs. Für Log-Aggregation nutzen Sie einen Journal-zu-Loki- / Journal-zu-Fluent-Bit-Sidecar; leiten Sie das rousseau-Log-Format nicht direkt auf die Festplatte um (es wird nicht von rousseau log-rotiert).

Konfigurieren Sie rousseau so, dass es JSON ausgibt, damit Aggregatoren es parsen können:

```yaml
log:
  level: info
  format: json
```

## Nftables-Egress-Sperre (optional)

`docker/nftables.rules.example` im Source-Tree liefert ein Template für Kernel-Level-Egress-Härtung – blockiert alles ausser Metas WhatsApp-Web-Bereichen, Anthropic (hinter CloudFront, daher domänenbasiertes Filter verwenden) und Signal. Legen Sie dies über den Container-Namespace für die strengste Posture. Siehe [Sicherheit](/de/security/) für die Begründung.

## Helm-Chart (Roadmap)

Ein First-Party-Helm-Chart steht auf der Roadmap. Bis dahin genügen die obigen Manifeste für eine minimale Bereitstellung. Den Fortschritt verfolgen Sie unter [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md).

Entwurfs-`values.yaml`-Struktur (zur Prüfung durch potenzielle Nutzer):

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
  # egress: Liste erlaubter CIDRs
```

## Fehlerbehebung

### `podman play kube` schlägt mit `permission denied` an einem Bind-Mount fehl

SELinux-Label fehlt. Jedes Volume muss auf `:Z` (oder `:z` für Shared) enden. Siehe [Fehlerbehebung: Container schlägt beim Bind-Mount fehl](/de/troubleshooting/#container-fails-to-bind-mount).

### Kubernetes-Pod im CrashLoopBackOff beim ersten Start

Das State-Volume wurde nicht vorab angelegt, oder sein Eigentümer stimmt nicht mit UID 1000 überein. Fügen Sie einen initContainer hinzu, um das Volume zu `chown`en:

```yaml
initContainers:
  - name: chown-state
    image: busybox
    command: ["sh", "-c", "chown -R 1000:1000 /state"]
    volumeMounts: [{ name: state, mountPath: /state }]
    securityContext: { runAsUser: 0 }
```

### `systemctl --user` findet die Quadlet-Unit nicht

`daemon-reload` wurde nicht ausgeführt oder die Unit-Datei enthält einen Tippfehler. Prüfen Sie mit `systemctl --user cat rousseau-agent.service` – Quadlet generiert die Unit on the fly, weshalb cat das schnellste Debug-Tool ist.

### Nach dem Neustart startet der Daemon nicht

Aktivieren Sie Lingering: `loginctl enable-linger $USER`. Ohne Lingering beendet sich der User-Manager von systemd beim Logout und startet erst beim nächsten Login neu.

### Zwei Daemons sind sich in die Quere gekommen und die State-DB ist beschädigt

Führen Sie niemals zwei Daemons gegen denselben `state.path` aus. Bei Korruption sichern Sie die Datei, führen `rm sessions.db{,-wal,-shm}` aus und starten neu. Die Sitzungshistorie geht verloren; das Pairing bleibt erhalten, wenn `whatsapp.db` separat liegt (standardmässig ja).

## Verwandte Seiten

- [Guides: Kubernetes-Bereitstellung](/de/guides/kubernetes-deployment/) – vollständiges Helm-Chart- und NetworkPolicy-Beispiel.
- [Guides: Produktions-Bereitstellung](/de/guides/production-deployment/) – die Produktions-Checkliste.
- [Guides: Observability](/de/guides/observability/) – Logs und Metriken.
- [Sicherheit](/de/security/) – Vertrauensgrenzen, seccomp, Egress.
- [Konfiguration](/de/configuration/) – jeder Regler.

## Weiterführende Lektüre

- `docker/Dockerfile` – der Multi-Stage-Build.
- `docker/rousseau-agent.container` – die Quadlet-Unit.
- `docker/example-nftables.rules` – Beispiel-Egress-Regelwerk.
- `Makefile` – Build-Automatisierung.
- systemd-Dokumentation: [Quadlet](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html).
