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
description: "Reference production deployment for rousseau-agent: rootless Podman + systemd Quadlet with dropped capabilities, read-only rootfs, seccomp, pasta networking. Kubernetes / OpenShift note."
keywords: "deployment, Podman, Quadlet, systemd, rootless, ReadOnly, DropCapability, NoNewPrivileges, seccomp, pasta, Kubernetes, OpenShift"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/deployment/"
subtitle: "Rootless Podman with a systemd Quadlet, plus a Kubernetes note."
tags: "deployment, operations, container, systemd"
title: "Deployment"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "deployment, Podman, Quadlet, systemd, rootless, ReadOnly, DropCapability, NoNewPrivileges, seccomp, pasta, Kubernetes, OpenShift"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Deployment"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "operations"
order: 25
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/deployment/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Deployment"
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
twitter_title: "Deployment"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">What you'll learn</span><p>The three deployment topologies rousseau supports — rootless Podman + Quadlet (reference), plain Docker, and Kubernetes — plus secrets management via Vault, AWS Secrets Manager, and GCP Secret Manager. Source of truth for the reference Quadlet: <code>docker/rousseau-agent.container</code>.</p></aside>

## Reference posture

The reference deployment is a rootless Podman container managed by a systemd Quadlet unit — one-node, no Kubernetes dependency, survives reboots, no root privileges required.

Source of truth: `docker/rousseau-agent.container` in the rousseau-agent repo.

## Pick a topology

<div class="tabs" data-tabs="deployment-topology">
  <div class="tab-list" role="tablist" aria-label="Deployment topology">
    <button role="tab" aria-selected="true">Podman + Quadlet</button>
    <button role="tab" aria-selected="false">Docker Compose</button>
    <button role="tab" aria-selected="false">Kubernetes</button>
  </div>
  <div class="tab-panel" role="tabpanel">

The reference deployment. Rootless, hardened, survives reboots, no orchestrator required.

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
mkdir -p ~/.config/containers/systemd
cp docker/rousseau-agent.container ~/.config/containers/systemd/
systemctl --user daemon-reload
systemctl --user enable --now rousseau-agent.service
```

See the full Quadlet unit and its rationale further down this page.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Docker Compose is a familiar shape but does not enforce the security posture Quadlet does — you must set every hardening flag by hand:

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

<aside class="admonition" data-type="warning"><span class="admonition-title">Root Docker</span><p>Classic Docker daemon runs as root. Even with <code>user: "1000:1000"</code>, the daemon has the capabilities of the Docker socket owner. Prefer rootless Docker or Podman.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Kubernetes needs a Deployment + PVC. See the manifest below, plus [Guides: Kubernetes Deployment](/guides/kubernetes-deployment/) for a full Helm chart example.

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

## Secrets management

Never check API keys or tokens into `config.yaml`. Load them at runtime from a secret backend:

<div class="tabs" data-tabs="deployment-secrets">
  <div class="tab-list" role="tablist" aria-label="Secrets backend">
    <button role="tab" aria-selected="true">HashiCorp Vault</button>
    <button role="tab" aria-selected="false">AWS Secrets Manager</button>
    <button role="tab" aria-selected="false">GCP Secret Manager</button>
    <button role="tab" aria-selected="false">systemd credentials</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Use `vault agent` to render env vars into a file rousseau reads. Sample template:

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

Use `aws secretsmanager` to fetch the key into an env file at boot:

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

Combine with IRSA on EKS so the SDK resolves credentials transparently — no static AWS keys needed on the host.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Use `gcloud secrets versions access`:

```sh
gcloud secrets versions access latest --secret=rousseau-anthropic > /run/rousseau/api_key
```

Or, in Kubernetes, use the [Secret Manager CSI driver](https://cloud.google.com/secret-manager/docs/secret-manager-managed-csi-component) to mount secrets as files.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Systemd credentials (available on systemd 250+) load secrets into memory at unit start:

```ini
[Service]
LoadCredential=anthropic_key:/etc/rousseau/anthropic.key
ExecStart=/usr/local/bin/rousseau chat
```

The daemon reads `$CREDENTIALS_DIRECTORY/anthropic_key` at start. No writes to disk beyond the (encrypted) credential store.

  </div>
</div>

## Build the image

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
```

Multi-stage build. Stage 1: `golang:1.26-alpine` compiles the static binary (`CGO_ENABLED=0`). Stage 2: `node:22-alpine` supplies the `claude` CLI subprocess. The runtime image is ~550 MB; the Node layer only exists so the optional `claudecli` provider has a home.

If you use a different provider (Anthropic direct, Bedrock, Vertex, OpenAI-compatible), you can drop the Node runtime and shrink the image.

## Install the Quadlet unit

```sh
mkdir -p ~/.config/containers/systemd
cp docker/rousseau-agent.container ~/.config/containers/systemd/
systemctl --user daemon-reload
systemctl --user start rousseau-agent.service
journalctl --user -u rousseau-agent.service -f
```

Enable on boot with `systemctl --user enable rousseau-agent.service` after confirming lingering is on (`loginctl enable-linger $USER`).

## Runtime posture — every Quadlet setting

| Setting | Value | Rationale |
|---|---|---|
| `Network=pasta` | Rootless network stack | `slirp4netns` was removed from recent Podman; pasta is faster on modern kernels and blocks inbound from the host by default. |
| `UserNS=keep-id` | Container UID 1000 → host UID 1000 | Bind-mounted files retain host ownership; the container process can write to host-owned files. |
| `ReadOnly=true` | Root filesystem read-only | The daemon should never mutate the image at runtime. Anything writable lives on a bind mount or the tmpfs. |
| `Tmpfs=/tmp:rw,size=64m,mode=1777` | Writable scratch | For anything that needs a scratch file at runtime (rare). |
| `DropCapability=all` | Every capability dropped | The Go binary needs no elevated capabilities — outbound TCP does not require `CAP_NET_BIND_SERVICE` or similar. |
| `NoNewPrivileges=true` | `no_new_privs` bit set | Blocks setuid escalation inside the container. |
| `SeccompProfile=/usr/share/containers/seccomp.json` | Default seccomp filter | Kernel-level syscall gating on top of dropped capabilities. |
| `Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z` | State bind mount | Sessions, WhatsApp pairing, cron jobs, JID map, FTS5 index. `:Z` sets the SELinux label. |
| `Volume=%h/.claude:/home/rousseau/.claude:rw,Z` | `claude` CLI auth | Only relevant when the `claudecli` provider is active. `claude` refreshes cached OAuth in place. |
| `Volume=%h/team-rousseau-workspace:/workspace:rw,Z` | Workspace | Only the workspace is visible from inside the container. Nothing else on the host is mounted. |
| `Environment=HOME=/home/rousseau` | Sets `$HOME` | Consumed by Viper, the `claude` CLI, and the state directory resolver. |
| `AutoUpdate=disabled` | Podman does not auto-update | Updates are cut by the operator on a release cadence, not silently. |

## `Exec=` line

The Quadlet ships with:

```
Exec=whatsapp --allow 447906009073@s.whatsapp.net
```

Replace with your transport of choice and your allowlist. Multiple transports typically run in separate Quadlet units — one image, one binary, several units — so that a failure in one transport does not take the others down.

## Kubernetes / OpenShift

`rousseau` is a single-binary daemon; a minimal `Deployment` + `PersistentVolumeClaim` for the state directory is sufficient:

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

Because there is no inbound HTTP surface, **no `Service` or `Ingress` is required** for outbound-WebSocket transports (Slack, Discord, WhatsApp, Matrix). Only a webhook-style transport would need a `Service`, and rousseau ships none by default.

`Recreate` strategy is deliberate — the SQLite state file is not designed for two concurrent writers. If you need HA, run one daemon per transport and rely on the transport's own state (Slack Socket Mode, Discord Gateway) for reconnect semantics.

## systemd log destination

The Quadlet inherits systemd's journal configuration. `journalctl --user -u rousseau-agent.service` reads the logs. For log aggregation, use a journal-to-Loki / journal-to-Fluent-Bit sidecar; do not pipe rousseau's log format directly to disk (it is not log-rotated by rousseau).

Configure rousseau to emit JSON so aggregators can parse it:

```yaml
log:
  level: info
  format: json
```

## Nftables egress lockdown (optional)

`docker/nftables.rules.example` in the source tree ships a template for kernel-level egress hardening — drop everything except Meta's WhatsApp Web ranges, Anthropic (behind CloudFront so use domain-based filter), and Signal. Layer this on top of the container namespace for the tightest posture. See [security](/security/) for the reasoning.

## Helm chart (roadmap)

A first-party Helm chart is on the roadmap. Until it ships, the manifests above are sufficient for a minimal deployment. Track [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md) for progress.

Draft `values.yaml` outline (for prospective users to review):

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

## Troubleshooting

### `podman play kube` fails with `permission denied` on a bind mount

SELinux label missing. Every volume must end with `:Z` (or `:z` for shared). See [Troubleshooting: Container fails to bind mount](/troubleshooting/#container-fails-to-bind-mount).

### Kubernetes pod CrashLoopBackOff on first start

The state volume was not pre-created, or its ownership does not match UID 1000. Add an initContainer to `chown` the volume:

```yaml
initContainers:
  - name: chown-state
    image: busybox
    command: ["sh", "-c", "chown -R 1000:1000 /state"]
    volumeMounts: [{ name: state, mountPath: /state }]
    securityContext: { runAsUser: 0 }
```

### `systemctl --user` cannot find the Quadlet unit

`daemon-reload` was not run, or the unit file has a typo. Confirm with `systemctl --user cat rousseau-agent.service` — Quadlet generates the unit on the fly, so cat is the fastest debugging tool.

### After reboot, the daemon does not start

Enable lingering: `loginctl enable-linger $USER`. Without lingering, systemd's user manager exits on logout and does not respawn until the next login.

### Two daemons stepped on each other and the state DB is corrupt

Never run two daemons against the same `state.path`. If corruption occurs, back up the file, `rm sessions.db{,-wal,-shm}`, restart. Session history is lost; pairing survives if `whatsapp.db` is separate (it is by default).

## Related pages

- [Guides: Kubernetes Deployment](/guides/kubernetes-deployment/) — full Helm chart and NetworkPolicy example.
- [Guides: Production Deployment](/guides/production-deployment/) — the production checklist.
- [Guides: Observability](/guides/observability/) — logs and metrics.
- [Security](/security/) — trust boundaries, seccomp, egress.
- [Configuration](/configuration/) — every knob.

## Further reading

- `docker/Dockerfile` — the multi-stage build.
- `docker/rousseau-agent.container` — the Quadlet unit.
- `docker/example-nftables.rules` — sample egress ruleset.
- `Makefile` — build automation.
- systemd docs: [Quadlet](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html).
