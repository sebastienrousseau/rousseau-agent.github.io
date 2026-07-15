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
description: "Reference production deployment for rousseau-agent: rootless Podman + systemd Quadlet with dropped capabilities, read-only rootfs, seccomp, pasta networking. Kubernetes / OpenShift note."
keywords: "deployment, Podman, Quadlet, systemd, rootless, ReadOnly, DropCapability, NoNewPrivileges, seccomp, pasta, Kubernetes, OpenShift"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/deployment/"
subtitle: "无 root 权限的 Podman 配合 systemd Quadlet，附带 Kubernetes 说明。"
tags: "deployment, operations, container, systemd"
title: "部署"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "deployment, Podman, Quadlet, systemd, rootless, ReadOnly, DropCapability, NoNewPrivileges, seccomp, pasta, Kubernetes, OpenShift"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "部署"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "operations"
order: 25
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/deployment/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "部署"
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
twitter_title: "部署"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">你将学到</span><p>rousseau 支持的三种部署拓扑——无 root 权限 Podman + Quadlet（参考）、纯 Docker 与 Kubernetes——以及通过 Vault、AWS Secrets Manager 和 GCP Secret Manager 管理机密。参考 Quadlet 的权威来源：<code>docker/rousseau-agent.container</code>。</p></aside>

## 参考姿态

参考部署是由 systemd Quadlet 单元管理的无 root 权限 Podman 容器——单节点、不依赖 Kubernetes、可跨重启存活、无需 root 权限。

权威来源：rousseau-agent 仓库中的 `docker/rousseau-agent.container`。

## 选择拓扑

<div class="tabs" data-tabs="deployment-topology">
  <div class="tab-list" role="tablist" aria-label="Deployment topology">
    <button role="tab" aria-selected="true">Podman + Quadlet</button>
    <button role="tab" aria-selected="false">Docker Compose</button>
    <button role="tab" aria-selected="false">Kubernetes</button>
  </div>
  <div class="tab-panel" role="tabpanel">

参考部署。无 root 权限、已加固、可跨重启存活、无需编排器。

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
mkdir -p ~/.config/containers/systemd
cp docker/rousseau-agent.container ~/.config/containers/systemd/
systemctl --user daemon-reload
systemctl --user enable --now rousseau-agent.service
```

完整的 Quadlet 单元及其原理见本页后续内容。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Docker Compose 形式熟悉，但并不像 Quadlet 那样强制安全姿态——你必须手动设置每一个加固选项：

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

<aside class="admonition" data-type="warning"><span class="admonition-title">root 权限的 Docker</span><p>经典 Docker 守护进程以 root 身份运行。即使指定 <code>user: "1000:1000"</code>，守护进程仍拥有 Docker socket 拥有者的能力。请优先使用无 root 权限的 Docker 或 Podman。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Kubernetes 需要一个 Deployment + PVC。参见下方清单，以及 [指南：Kubernetes 部署](/zh-Hans/guides/kubernetes-deployment/) 中的完整 Helm chart 示例。

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

## 机密管理

切勿将 API 密钥或令牌写入 `config.yaml`。请在运行时从机密后端加载：

<div class="tabs" data-tabs="deployment-secrets">
  <div class="tab-list" role="tablist" aria-label="Secrets backend">
    <button role="tab" aria-selected="true">HashiCorp Vault</button>
    <button role="tab" aria-selected="false">AWS Secrets Manager</button>
    <button role="tab" aria-selected="false">GCP Secret Manager</button>
    <button role="tab" aria-selected="false">systemd credentials</button>
  </div>
  <div class="tab-panel" role="tabpanel">

使用 `vault agent` 将环境变量渲染到 rousseau 读取的文件中。示例模板：

```
{{- with secret "kv/rousseau/anthropic" }}
ANTHROPIC_API_KEY={{ .Data.data.api_key }}
{{- end }}
```

Systemd：

```ini
[Service]
EnvironmentFile=/run/rousseau/env
ExecStartPre=/usr/local/bin/vault-agent -config=/etc/vault/agent.hcl
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

启动时使用 `aws secretsmanager` 将密钥获取到一个环境变量文件中：

```sh
aws secretsmanager get-secret-value \
  --secret-id rousseau/anthropic \
  --query SecretString --output text | \
  jq -r '"ANTHROPIC_API_KEY=\(.api_key)"' > /run/rousseau/env
```

Systemd：

```ini
[Service]
EnvironmentFile=/run/rousseau/env
ExecStartPre=/usr/local/bin/fetch-secrets.sh
```

在 EKS 上与 IRSA 结合，SDK 会透明地解析凭证——主机无需静态 AWS 密钥。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

使用 `gcloud secrets versions access`：

```sh
gcloud secrets versions access latest --secret=rousseau-anthropic > /run/rousseau/api_key
```

或者在 Kubernetes 中使用 [Secret Manager CSI 驱动](https://cloud.google.com/secret-manager/docs/secret-manager-managed-csi-component) 将机密挂载为文件。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Systemd 凭证（systemd 250+ 可用）在单元启动时将机密加载到内存：

```ini
[Service]
LoadCredential=anthropic_key:/etc/rousseau/anthropic.key
ExecStart=/usr/local/bin/rousseau chat
```

守护进程启动时读取 `$CREDENTIALS_DIRECTORY/anthropic_key`。除（加密的）凭证存储外不写入磁盘。

  </div>
</div>

## 构建镜像

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
```

多阶段构建。阶段 1：`golang:1.26-alpine` 编译静态二进制（`CGO_ENABLED=0`）。阶段 2：`node:22-alpine` 提供 `claude` CLI 子进程。运行时镜像约 550 MB；Node 层的存在只是为了给可选的 `claudecli` 提供方一个运行环境。

如果使用其他提供方（Anthropic 直连、Bedrock、Vertex、OpenAI 兼容），可以去掉 Node 运行时以缩小镜像。

## 安装 Quadlet 单元

```sh
mkdir -p ~/.config/containers/systemd
cp docker/rousseau-agent.container ~/.config/containers/systemd/
systemctl --user daemon-reload
systemctl --user start rousseau-agent.service
journalctl --user -u rousseau-agent.service -f
```

在确认已启用 lingering（`loginctl enable-linger $USER`）后，使用 `systemctl --user enable rousseau-agent.service` 使其在开机时启动。

## 运行时姿态——每一个 Quadlet 设置

| 设置 | 值 | 原理 |
|---|---|---|
| `Network=pasta` | 无 root 权限网络栈 | 近期版本的 Podman 已移除 `slirp4netns`；pasta 在新内核上更快，并默认阻止来自主机的入站流量。 |
| `UserNS=keep-id` | 容器 UID 1000 → 主机 UID 1000 | 绑定挂载的文件保留主机所有权；容器进程可写主机拥有的文件。 |
| `ReadOnly=true` | 根文件系统只读 | 守护进程绝不应在运行时修改镜像。任何可写内容都放在绑定挂载或 tmpfs 上。 |
| `Tmpfs=/tmp:rw,size=64m,mode=1777` | 可写临时空间 | 供运行时需要临时文件的场景（较少）。 |
| `DropCapability=all` | 剥离所有能力 | Go 二进制无需任何提升的能力——出站 TCP 不需要 `CAP_NET_BIND_SERVICE` 之类。 |
| `NoNewPrivileges=true` | 设置 `no_new_privs` 位 | 阻止容器内的 setuid 提权。 |
| `SeccompProfile=/usr/share/containers/seccomp.json` | 默认 seccomp 过滤器 | 在剥离能力之上再增加内核级系统调用管控。 |
| `Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z` | 状态绑定挂载 | 会话、WhatsApp 配对、定时任务、JID 映射、FTS5 索引。`:Z` 设置 SELinux 标签。 |
| `Volume=%h/.claude:/home/rousseau/.claude:rw,Z` | `claude` CLI 认证 | 仅在使用 `claudecli` 提供方时相关。`claude` 就地刷新缓存的 OAuth。 |
| `Volume=%h/team-rousseau-workspace:/workspace:rw,Z` | 工作区 | 容器内只能看到工作区。主机上的其他内容不被挂载。 |
| `Environment=HOME=/home/rousseau` | 设置 `$HOME` | Viper、`claude` CLI 与状态目录解析器都会读取。 |
| `AutoUpdate=disabled` | Podman 不自动更新 | 由运维人员按发布节奏发起更新，不会静默进行。 |

## `Exec=` 行

Quadlet 中默认提供：

```
Exec=whatsapp --allow 447906009073@s.whatsapp.net
```

替换为你所选的传输和你的允许列表。多个传输通常运行在独立的 Quadlet 单元中——一个镜像、一个二进制、多个单元——这样一个传输故障不会拖垮其他传输。

## Kubernetes / OpenShift

`rousseau` 是单二进制守护进程；最小化的 `Deployment` + 用于状态目录的 `PersistentVolumeClaim` 足矣：

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

由于没有入站 HTTP 面，对于出站 WebSocket 传输（Slack、Discord、WhatsApp、Matrix），**无需 `Service` 或 `Ingress`**。只有 webhook 风格的传输才需要 `Service`，而 rousseau 默认不提供任何此类传输。

`Recreate` 策略是刻意为之——SQLite 状态文件的设计不允许两个并发写入者。如需 HA，请每个传输运行一个守护进程，并依赖传输本身的状态（Slack Socket Mode、Discord Gateway）来处理重连语义。

## systemd 日志去向

Quadlet 继承 systemd 的日志配置。`journalctl --user -u rousseau-agent.service` 读取日志。对于日志聚合，请使用 journal-to-Loki / journal-to-Fluent-Bit 边车；不要将 rousseau 的日志格式直接管道到磁盘（rousseau 不会为日志做轮转）。

配置 rousseau 输出 JSON，聚合器就能解析：

```yaml
log:
  level: info
  format: json
```

## Nftables 出站锁定（可选）

源码树中的 `docker/nftables.rules.example` 提供了内核级出站加固模板——除 Meta 的 WhatsApp Web 网段、Anthropic（在 CloudFront 之后，因此使用基于域名的过滤）和 Signal 之外全部丢弃。将其叠加在容器命名空间之上以获得最严格的姿态。理由请参见 [安全](/zh-Hans/security/)。

## Helm chart（路线图）

第一方 Helm chart 已列入路线图。在其发布前，上述清单足以进行最小化部署。进度请关注 [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md)。

草稿 `values.yaml` 大纲（供潜在用户审阅）：

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

## 故障排查

### `podman play kube` 在绑定挂载上报 `permission denied`

缺少 SELinux 标签。每个卷都必须以 `:Z` 结尾（共享则用 `:z`）。参见 [故障排查：容器绑定挂载失败](/zh-Hans/troubleshooting/#container-fails-to-bind-mount)。

### Kubernetes pod 首次启动 CrashLoopBackOff

状态卷未预先创建，或其所有者不匹配 UID 1000。添加一个 initContainer 来 `chown` 该卷：

```yaml
initContainers:
  - name: chown-state
    image: busybox
    command: ["sh", "-c", "chown -R 1000:1000 /state"]
    volumeMounts: [{ name: state, mountPath: /state }]
    securityContext: { runAsUser: 0 }
```

### `systemctl --user` 找不到 Quadlet 单元

`daemon-reload` 未执行，或者单元文件有拼写错误。使用 `systemctl --user cat rousseau-agent.service` 确认——Quadlet 会即时生成单元，所以 cat 是最快的调试工具。

### 重启后守护进程未启动

启用 lingering：`loginctl enable-linger $USER`。若无 lingering，systemd 的用户管理器会在登出时退出，直到下次登录才会重新启动。

### 两个守护进程互相影响导致状态 DB 损坏

切勿针对同一个 `state.path` 运行两个守护进程。如果发生损坏，请备份文件，`rm sessions.db{,-wal,-shm}`，然后重启。会话历史会丢失；如果 `whatsapp.db` 是分离的（默认如此），配对可以保留。

## 相关页面

- [指南：Kubernetes 部署](/zh-Hans/guides/kubernetes-deployment/)——完整的 Helm chart 与 NetworkPolicy 示例。
- [指南：生产部署](/zh-Hans/guides/production-deployment/)——生产清单。
- [指南：可观测性](/zh-Hans/guides/observability/)——日志与指标。
- [安全](/zh-Hans/security/)——信任边界、seccomp、出站。
- [配置](/zh-Hans/configuration/)——每一项配置。

## 延伸阅读

- `docker/Dockerfile`——多阶段构建。
- `docker/rousseau-agent.container`——Quadlet 单元。
- `docker/example-nftables.rules`——示例出站规则集。
- `Makefile`——构建自动化。
- systemd 文档：[Quadlet](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html)。
